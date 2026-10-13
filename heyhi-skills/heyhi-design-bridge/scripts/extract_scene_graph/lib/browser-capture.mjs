// browser-capture.mjs — the in-page capture. This function is serialized by
// Playwright and runs INSIDE the browser, so it must be fully self-contained
// (no imports, no closures over module scope; only the `opts` arg crosses in).
//
// It returns a rich, loss-tolerant capture tree. Mapping that down to the strict
// v0.1 IR happens Node-side in build-ir.mjs. Keeping capture rich and mapping
// strict is what lets the extractor honour "no silent drops": everything the page
// declares is carried out of the browser; build-ir decides what maps and what is
// flagged.

/**
 * @param {{rootSelector: string, brandFamilies: string[]}} opts
 */
export function captureScene(opts) {
  const ROOT_SELECTOR = opts.rootSelector;

  // ---- CSSOM: flatten every style rule with a specificity + source order ----
  // getComputedStyle returns resolved literals (rgb(...), 51px); the DECLARED
  // text (var(--token), clamp(...)) only survives in the stylesheet rules. We
  // rebuild a minimal cascade so we can read what the author actually wrote.
  const flatRules = [];
  let order = 0;
  const pushRule = (rule, mediaMatches) => {
    if (!rule.selectorText || !rule.style) return;
    if (!mediaMatches) return;
    for (const sub of rule.selectorText.split(",")) {
      flatRules.push({ selector: sub.trim(), style: rule.style, spec: specificity(sub.trim()), order: order++ });
    }
  };
  const walkRules = (rules, mediaMatches) => {
    for (const rule of rules) {
      if (rule.type === CSSRule.STYLE_RULE) pushRule(rule, mediaMatches);
      else if (rule.type === CSSRule.MEDIA_RULE) {
        let m = true;
        try { m = window.matchMedia(rule.conditionText || rule.media.mediaText).matches; } catch { m = true; }
        walkRules(rule.cssRules, mediaMatches && m);
      }
      // @keyframes, @font-face, @import etc. carry no element declarations we map.
    }
  };
  for (const sheet of document.styleSheets) {
    // skip the extractor's own animation-freeze sheet so it does not pollute the
    // DECLARED-value cascade (its !important reset would mask real declarations)
    if (sheet.ownerNode && sheet.ownerNode.dataset && sheet.ownerNode.dataset.extractorFreeze) continue;
    let rules = null;
    try { rules = sheet.cssRules; } catch { rules = null; } // cross-origin (Google Fonts) — skip
    if (rules) walkRules(rules, true);
  }

  // Crude-but-stable CSS specificity for cascade ordering. Exact for the simple
  // selectors ui-studio emits; only relative order matters here.
  function specificity(sel) {
    const ids = (sel.match(/#[\w-]+/g) || []).length;
    const cls =
      (sel.match(/\.[\w-]+/g) || []).length +
      (sel.match(/\[[^\]]+\]/g) || []).length +
      (sel.match(/(^|[^:]):(?!:)[\w-]+/g) || []).length;
    const els =
      (sel.match(/::[\w-]+/g) || []).length +
      (sel.replace(/::?[\w-]+(\([^)]*\))?/g, " ").match(/\b[a-z][\w-]*/gi) || []).length;
    return ids * 1e6 + cls * 1e3 + els;
  }

  /** Winning declared value for el+prop across the cascade, or null. */
  function getDeclared(el, prop) {
    // Inline style wins over stylesheet rules (ignoring !important nuance).
    const inline = el.style && el.style.getPropertyValue(prop);
    if (inline) return inline.trim();
    let best = null;
    for (const r of flatRules) {
      const v = r.style.getPropertyValue(prop);
      if (!v) continue;
      let matches = false;
      try { matches = el.matches(r.selector); } catch { matches = false; }
      if (!matches) continue;
      const important = r.style.getPropertyPriority(prop) === "important" ? 1 : 0;
      const rank = important * 1e12 + r.spec * 10 + r.order / 1e6;
      if (!best || rank > best.rank) best = { rank, value: v.trim() };
    }
    return best ? best.value : null;
  }

  // ---- pseudo-element probe: a plain DOM walk cannot see ::before/::after ----
  // R-1=D (region-scoped block): capture the pseudo's GEOMETRY + paint, not just a
  // boolean, so build-ir can emit it as a needs-human placeholder at its real box.
  // getComputedStyle(el, which) resolves an absolutely-positioned pseudo's width/height
  // to px in Chromium (proven: coverage ramp 50/33/20/0px) even for `width:var(--%)` and
  // `width:auto`; the parent's getBoundingClientRect() is always available, so an
  // inset/offset overlay reconstructs to an exact viewport box (same coord system as
  // node.bbox). An in-flow `position:static` pseudo returns width/height `auto` (no
  // resolvable box) — box:null, and build-ir keeps it a flag rather than misplacing it.
  function probePseudo(el, which) {
    const cs = window.getComputedStyle(el, which);
    const content = cs.content;
    if (!content || content === "none" || content === "normal") return null;
    // A faithful box needs the host to BE the pseudo's containing block. That holds only for
    // an `absolute` pseudo whose host is itself positioned (otherwise the containing block is
    // an ancestor, and host.rect + inset would misplace it); a `fixed` pseudo resolves against
    // the viewport. Outside that, return box:null so build-ir REFUSES (blocks) rather than
    // emitting a misplaced placeholder — refuse over emit-wrong.
    const hostPositioned = window.getComputedStyle(el).position !== "static";
    const canBox = cs.position === "absolute" && hostPositioned;
    const host = el.getBoundingClientRect();
    const left = parseFloat(cs.left), top = parseFloat(cs.top);
    const w = parseFloat(cs.width), h = parseFloat(cs.height);
    const box = (canBox && isFinite(w) && isFinite(h))
      ? { x: host.x + (isFinite(left) ? left : 0), y: host.y + (isFinite(top) ? top : 0), w, h }
      : null;
    const bw = parseFloat(cs.borderTopWidth);
    return {
      content, position: cs.position,
      color: cs.color, background: cs.backgroundColor,
      backgroundImage: cs.backgroundImage && cs.backgroundImage !== "none" ? cs.backgroundImage : null,
      border: isFinite(bw) && bw > 0 ? { w: bw, style: cs.borderTopStyle, color: cs.borderTopColor } : null,
      radius: cs.borderTopLeftRadius,
      box,
    };
  }

  const GENERIC_FAMILIES = new Set(["serif", "sans-serif", "monospace", "system-ui", "ui-sans-serif", "ui-serif", "ui-monospace", "cursive", "fantasy", "inherit", "initial"]);
  function firstFamily(ff) {
    return String(ff || "").split(",")[0].replace(/['"]/g, "").trim();
  }

  const BLOCKISH = new Set(["block", "flex", "inline-flex", "grid", "inline-grid", "list-item", "table", "flow-root"]);
  function isFlexOrGrid(disp) {
    return disp === "flex" || disp === "inline-flex" || disp === "grid" || disp === "inline-grid";
  }

  // Extract a leaf's text AND its inline styled runs in one walk (P4, Gap 4c).
  // Preserves <br> as a newline and never fuses words across inline boundaries
  // (Gap 4b); additionally records the {start,end} character span of each inline
  // styled descendant (<em>/<strong>/<i>/<b>, or any inline element whose computed
  // colour/style/weight differs from the leaf base) so a multi-style block keeps its
  // accent and emphasis instead of collapsing to one style. start/end index into the
  // same collapsed `text` the IR carries as `characters` (built incrementally so the
  // offsets and the whitespace-collapse stay consistent).
  const RUN_EMPHASIS = new Set(["em", "i", "strong", "b"]);
  function extractRich(el, baseCS) {
    let text = "";
    const runs = [];
    function append(s) {
      for (let i = 0; i < s.length; i++) {
        const ch = s[i];
        if (ch === "\n") {
          text = text.replace(/ +$/, "");
          if (text.length && !text.endsWith("\n")) text += "\n";
        } else if (ch === " " || ch === "\t" || ch === "\r" || ch === "\f" || ch === "\v") {
          if (text.length && !/\s$/.test(text)) text += " ";
        } else {
          text += ch;
        }
      }
    }
    function isStyledRun(node) {
      const tag = node.tagName.toLowerCase();
      if (tag === "br") return false;
      if (RUN_EMPHASIS.has(tag)) return true;
      if (!baseCS) return false;
      const cs = window.getComputedStyle(node);
      return cs.color !== baseCS.color || cs.fontStyle !== baseCS.fontStyle || cs.fontWeight !== baseCS.fontWeight;
    }
    function walk(node) {
      for (const n of node.childNodes) {
        if (n.nodeType === 3) append(n.nodeValue);
        else if (n.nodeType === 1) {
          if (n.tagName === "BR") { append("\n"); }
          else if (isStyledRun(n)) {
            const start = text.length;
            walk(n);
            const end = text.length;
            if (end > start) {
              const cs = window.getComputedStyle(n);
              runs.push({ start, end, classes: [...n.classList], declaredColor: getDeclared(n, "color"),
                          computed: { color: cs.color, fontStyle: cs.fontStyle, fontWeight: cs.fontWeight, fontFamily: cs.fontFamily } });
            }
          } else walk(n);
        }
      }
    }
    walk(el);
    text = text.replace(/\s+$/, "");
    return { text, runs };
  }

  // WS4 (D): synthesize a leaf TEXT node from a loose text node that sits BESIDE an inline
  // element (e.g. a label next to an inline <img> arrow inside a flex span). It inherits the
  // parent's font/colour (the text renders in the parent's style) and carries a transparent
  // background so build-ir classifies it as TEXT, never a CHIP. This is what keeps the
  // "See service"/"Learn more" label alive next to its arrow (the card__more drop bug).
  function looseTextNode(textNode, parentEl, parentCS) {
    const t = (textNode.nodeValue || "").replace(/\s+/g, " ").trim();
    if (!t) return null;
    let rect = { x: 0, y: 0, width: 0, height: 0 };
    try { const r = document.createRange(); r.selectNode(textNode); rect = r.getBoundingClientRect(); } catch { /* detached */ }
    const fam = firstFamily(parentCS.fontFamily);
    return {
      tag: "span", id: null, classes: [], dataAudit: null, role: null, href: null,
      bbox: { x: rect.x, y: rect.y, w: rect.width, h: rect.height },
      computed: {
        display: "inline", position: "static", overflowX: "visible", overflowY: "visible",
        flexDirection: "row", justifyContent: "normal", alignItems: "normal", alignContent: "normal", flexWrap: "nowrap",
        rowGap: "0px", columnGap: "0px", gridTemplateColumns: "none", transform: "none", boxShadow: "none",
        borderTopWidth: "0px", borderRightWidth: "0px", borderBottomWidth: "0px", borderLeftWidth: "0px",
        borderTopStyle: "none", borderTopColor: "rgba(0, 0, 0, 0)",
        borderTopLeftRadius: "0px", borderTopRightRadius: "0px", borderBottomRightRadius: "0px", borderBottomLeftRadius: "0px",
        opacity: "1", animationName: "none", transitionDuration: "0s",
        backgroundColor: "rgba(0, 0, 0, 0)", backgroundImage: "none",
        color: parentCS.color, fontFamily: parentCS.fontFamily, fontWeight: parentCS.fontWeight,
        fontSize: parentCS.fontSize, lineHeight: parentCS.lineHeight, letterSpacing: parentCS.letterSpacing,
        paddingTop: "0px", paddingRight: "0px", paddingBottom: "0px", paddingLeft: "0px",
      },
      declared: {
        color: getDeclared(parentEl, "color"), backgroundColor: null, fontSize: null,
        padding: null, gap: null, borderColor: null, animation: null,
      },
      pseudo: { before: null, after: null },
      font: (() => {
        const generic = GENERIC_FAMILIES.has(fam.toLowerCase());
        const brand = opts.brandFamilies.map((f) => f.toLowerCase()).includes(fam.toLowerCase());
        let loaded = true;
        try { loaded = document.fonts.check(`${parentCS.fontWeight} ${parentCS.fontSize} "${fam}"`); } catch { loaded = true; }
        return { family: fam, generic, brand, loaded };
      })(),
      svgOuter: null, imgSrc: null, text: t, isFlexOrGrid: false, hasAbsChild: false, children: [],
    };
  }

  // ---- the recursive element capture ----
  function captureEl(el) {
    const cs = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    const tag = el.tagName.toLowerCase();
    const disp = cs.display;

    const node = {
      tag,
      id: el.id || null,
      classes: [...el.classList],
      dataAudit: el.getAttribute("data-audit") || null,
      // WS4 (A): semantic affordance signals so build-ir can classify interactive controls
      // (<a>/<button>/role=button/.btn/.cta) instead of guessing from box shape alone.
      role: el.getAttribute("role") || null,
      href: tag === "a" ? (el.getAttribute("href") || null) : null,
      bbox: { x: rect.x, y: rect.y, w: rect.width, h: rect.height },
      computed: {
        display: disp,
        position: cs.position,
        overflowX: cs.overflowX,
        overflowY: cs.overflowY,
        flexDirection: cs.flexDirection,
        justifyContent: cs.justifyContent,
        alignItems: cs.alignItems,
        alignContent: cs.alignContent,
        flexWrap: cs.flexWrap,
        rowGap: cs.rowGap,
        columnGap: cs.columnGap,
        gridTemplateColumns: cs.gridTemplateColumns,
        transform: cs.transform,
        boxShadow: cs.boxShadow,
        borderTopWidth: cs.borderTopWidth,
        borderRightWidth: cs.borderRightWidth,
        borderBottomWidth: cs.borderBottomWidth,
        borderLeftWidth: cs.borderLeftWidth,
        borderTopStyle: cs.borderTopStyle,
        borderTopColor: cs.borderTopColor,
        borderTopLeftRadius: cs.borderTopLeftRadius,
        borderTopRightRadius: cs.borderTopRightRadius,
        borderBottomRightRadius: cs.borderBottomRightRadius,
        borderBottomLeftRadius: cs.borderBottomLeftRadius,
        opacity: cs.opacity,
        animationName: cs.animationName,
        transitionDuration: cs.transitionDuration,
        backgroundColor: cs.backgroundColor,
        backgroundImage: cs.backgroundImage,
        color: cs.color,
        fontFamily: cs.fontFamily,
        fontWeight: cs.fontWeight,
        fontSize: cs.fontSize,
        lineHeight: cs.lineHeight,
        letterSpacing: cs.letterSpacing,
        paddingTop: cs.paddingTop,
        paddingRight: cs.paddingRight,
        paddingBottom: cs.paddingBottom,
        paddingLeft: cs.paddingLeft,
      },
      declared: {
        color: getDeclared(el, "color"),
        backgroundColor: getDeclared(el, "background-color") || getDeclared(el, "background"),
        fontSize: getDeclared(el, "font-size"),
        padding: getDeclared(el, "padding"),
        gap: getDeclared(el, "gap") || getDeclared(el, "column-gap") || getDeclared(el, "row-gap"),
        borderColor: getDeclared(el, "border-color") || getDeclared(el, "border-top-color") || getDeclared(el, "border"),
        // recovered from the stylesheet so the animation flag survives the freeze
        animation: getDeclared(el, "animation-name") || getDeclared(el, "animation"),
      },
      pseudo: { before: probePseudo(el, "::before"), after: probePseudo(el, "::after") },
      font: (() => {
        const fam = firstFamily(cs.fontFamily);
        const generic = GENERIC_FAMILIES.has(fam.toLowerCase());
        const brand = opts.brandFamilies.map((f) => f.toLowerCase()).includes(fam.toLowerCase());
        let loaded = true;
        try { loaded = document.fonts.check(`${cs.fontWeight} ${cs.fontSize} "${fam}"`); } catch { loaded = true; }
        return { family: fam, generic, brand, loaded };
      })(),
      svgOuter: tag === "svg" ? el.outerHTML : null,
      imgSrc: tag === "img" ? (el.getAttribute("src") || null) : null,
      text: null,
      isFlexOrGrid: isFlexOrGrid(disp),
      hasAbsChild: false,
      children: [],
    };

    if (tag === "svg" || tag === "img") return node; // leaf media — never recurse into

    const elementChildren = [...el.children];
    // A child counts as an absolute-positioning child (forces parent off auto-layout).
    node.hasAbsChild = elementChildren.some((c) => window.getComputedStyle(c).position === "absolute");

    let childNodes;
    if (node.isFlexOrGrid) {
      // Flex/grid items are all real nodes regardless of their own display.
      childNodes = elementChildren;
    } else {
      // Block flow: only block-level element children become nodes; inline
      // phrasing (a/strong/span used for text) folds into the text leaf.
      childNodes = elementChildren.filter((c) => BLOCKISH.has(window.getComputedStyle(c).display));
    }

    if (childNodes.length > 0) {
      if (node.isFlexOrGrid) {
        // WS4 (D): in a flex/grid box every element child is a real node, but loose text
        // sitting BETWEEN them (e.g. <span class="card__more">See service <img></span>) used
        // to be dropped — only the <img> survived. Walk childNodes in document order and keep
        // significant loose text as a synthesized TEXT leaf so the label rides with its icon.
        const keep = new Set(childNodes);
        const out = [];
        for (const ch of el.childNodes) {
          if (ch.nodeType === 1 && keep.has(ch)) out.push(captureEl(ch));
          else if (ch.nodeType === 3 && ch.nodeValue && ch.nodeValue.replace(/\s+/g, " ").trim()) {
            const ln = looseTextNode(ch, el, cs);
            if (ln) out.push(ln);
          }
        }
        node.children = out;
      } else {
        node.children = childNodes.map(captureEl);
      }
    } else {
      const { text: txt, runs } = extractRich(el, cs);
      if (txt) { node.text = txt; if (runs.length) node.inlineRuns = runs; }
    }
    return node;
  }

  const rootEl = document.querySelector(ROOT_SELECTOR) || document.body;
  return {
    meta: {
      viewport: { w: window.innerWidth, h: window.innerHeight },
      rootSelector: ROOT_SELECTOR,
      fontsReady: document.fonts ? document.fonts.status : "unknown",
      ruleCount: flatRules.length,
    },
    root: captureEl(rootEl),
  };
}
