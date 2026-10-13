#!/usr/bin/env python3
"""Build the 'Governed Loop' orientation artifact, embedding the six real
Sheerline SVG figures as isolated, theme-aware data URIs.

Source of truth for governed-loop.html — edit here and re-run (`python3
governed-loop.build.py`); do not hand-edit the generated HTML. Reads the six
figures from ./diagrams/ (the same set docs/architecture.md renders), so it
regenerates portably from wherever this file lives.
Published (private) artifact: https://claude.ai/code/artifact/1c395448-a9fb-4063-9a23-051bfcee5ad5
HeyHi Confidential.
"""
import base64, pathlib

DIAG = pathlib.Path(__file__).parent / "diagrams"
OUT = pathlib.Path(__file__).parent / "governed-loop.html"

def datauri(name):
    raw = (DIAG / f"{name}.svg").read_bytes()
    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:image/svg+xml;base64,{b64}"

# alt text lifted from architecture.md (already accessible + accurate)
FIG = {
    "lineage": (
        "1", "Where Sheerline sits", "keel", "diagrams/lineage.svg",
        "A hull has two defining lines. keel is the structural line below the "
        "waterline; sheer is the beautiful visible line above it. Three things stay "
        "separate: keel the general harness, Sheerline the whole design-practice OS, "
        "and the Design-Systems quality loop, which is one module of Sheerline.",
        "A hull's two lines: sheer above the waterline, keel below. keel the general "
        "harness, Sheerline the whole design-practice OS that reuses keel, and the "
        "Design-Systems quality loop as one module of Sheerline."),
    "three-layer-model": (
        "2", "The three layers, instantiated for design", "keel",
        "diagrams/three-layer-model.svg",
        "Sheerline rents the same runtime, owns the same configuration, and extends the "
        "same deployment layer keel does. The one structural difference is the slot keel "
        "has no room for: os/foundations/&lt;area&gt;/, per-area governed design context "
        "that loads only when the session type calls for it.",
        "Deployment and Configuration sit above a crimson owned-rented line; Runtime sits "
        "below it, rented and swappable. Foundations is the one net-new slot keel lacks."),
    "registry": (
        "3", "The 13-area practice registry", "sheer", "diagrams/registry.svg",
        "Deep but lopsided: strong in Visual and Design Systems, thin upstream. Governance "
        "turns that into a tracked state. Every area carries a coverage tag and a phase, so "
        "a gap is a thing you can see and schedule, not a silence. Only active, governed "
        "areas ever enter a session.",
        "Thirteen design-practice areas as one flat tagged registry, grouped Craft, "
        "Operating, Conditional. Each carries a coverage bar and the phase that fills it."),
    "quality-loop": (
        "4", "The Design-Systems quality loop", "sheer", "diagrams/quality-loop.svg",
        "The module that is built. Retrieve the system through the MCP, never paste it. "
        "Validate the output against it with deterministic, zero-token checks. Grade it "
        "over time. Learn from correction. Learn folds back into the next retrieval, and "
        "grades inform, never gate.",
        "Four verbs over three real subsystems, looping: retrieve through the Design System "
        "MCP, validate with the deterministic validator, grade with the evaluator that emits "
        "a series, learn through the corrections registry. Grades inform, never gate."),
    "boundary-moat": (
        "5", "The boundary and the retained moat", "line", "diagrams/boundary-moat.svg",
        "The MCP, the evaluator, and the corrections registry are reached through the MCP as "
        "a boundary tool, nested and referenced, never embedded. The scaffold is potentially "
        "publishable; the populated instance (the calibrated evaluator, the corpus, the "
        "promotion judgment) stays in a separate unpublished tree.",
        "A crimson wall divides the scaffold that ships (os layer, registry engine, "
        "corrections schema, MCP contract, DS-MCP scaffold) from the retained moat that "
        "stays (the graded evaluator, the populated corpus, the calibrated thresholds)."),
    "session-lifecycle": (
        "6", "How a design task runs", "sheer", "diagrams/session-lifecycle.svg",
        "Scope it, route it to one skill, load only what fits, run the loop, then do the "
        "thing source inspection cannot: render it and look. The design smoke test is the "
        "standing form of grades-inform. Close through the same gate every time, and capture "
        "the correction so it loads before the mistake can happen again.",
        "Six stages, looping: Intake scopes with the practice's own system as default, Route answers "
        "through the confidence gate, Load brings only in-scope foundations, Run executes the "
        "loop, Render-and-look is the design smoke test, the Exit Gate captures the correction."),
}

imgs = {k: datauri(k) for k in FIG}

def figure_card(key):
    n, title, tone, path, caption, alt = FIG[key]
    return f'''
      <figure class="fig fig--{tone}">
        <div class="fig__head">
          <span class="fig__n">{n}</span>
          <h3 class="fig__title">{title}</h3>
          <span class="chip chip--{tone}">{'inherited from keel' if tone=='keel' else ("the boundary" if tone=='line' else "Sheerline&rsquo;s own")}</span>
        </div>
        <div class="fig__frame">
          <img loading="lazy" src="{imgs[key]}" alt="{alt}" />
        </div>
        <figcaption>{caption} <span class="path">{path}</span></figcaption>
      </figure>'''

figs_inherited = figure_card("lineage") + figure_card("three-layer-model")
figs_own = "".join(figure_card(k) for k in ("registry","quality-loop","boundary-moat","session-lifecycle"))

HTML = r"""<title>The Governed Loop</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root{
    --paper:#f6f7fb; --surface:#ffffff; --surface-2:#eef0f7; --inset:#f0f2f9;
    --ink:#16182a; --ink-soft:#4a4e66; --ink-faint:#7c8098; --hair:#e1e4ef;
    --keel:#4f46e5; --keel-soft:#ecebfb;
    --sheer:#0d9488; --sheer-soft:#d8f1ec;
    --line:#b3322c; --line-soft:#f7e2df;
    --ok:#2f7a54; --warn:#a56410; --stop:#b3322c;
    --display:'Sora',system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;
    --body:'Lora',Georgia,'Times New Roman',serif;
    --mono:'DM Mono',ui-monospace,'SF Mono',Menlo,Consolas,monospace;
    --measure:68ch;
  }
  @media (prefers-color-scheme:dark){
    :root:not([data-theme="light"]){
      --paper:#0e1020; --surface:#171a2c; --surface-2:#1e2236; --inset:#12152444;
      --ink:#e9eaf4; --ink-soft:#b1b4ca; --ink-faint:#80849f; --hair:#2a2e46;
      --keel:#8f8bf6; --keel-soft:#22254733;
      --sheer:#3fd0c0; --sheer-soft:#12363433;
      --line:#f0736f; --line-soft:#3a202033;
      --ok:#56c98d; --warn:#e0a44a; --stop:#f0736f;
    }
  }
  :root[data-theme="dark"]{
      --paper:#0e1020; --surface:#171a2c; --surface-2:#1e2236; --inset:#12152444;
      --ink:#e9eaf4; --ink-soft:#b1b4ca; --ink-faint:#80849f; --hair:#2a2e46;
      --keel:#8f8bf6; --keel-soft:#22254733;
      --sheer:#3fd0c0; --sheer-soft:#12363433;
      --line:#f0736f; --line-soft:#3a202033;
      --ok:#56c98d; --warn:#e0a44a; --stop:#f0736f;
  }

  *{box-sizing:border-box}
  html{-webkit-text-size-adjust:100%}
  body{
    margin:0; background:var(--paper); color:var(--ink);
    font-family:var(--body); font-size:17px; line-height:1.62;
    -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility;
  }
  .wrap{max-width:940px; margin:0 auto; padding:clamp(28px,5vw,72px) clamp(20px,5vw,40px) 96px}

  /* ---- type ---- */
  h1,h2,h3,.eyebrow,.chip,.fig__n,.mono,.path,.tag,th{font-family:var(--display)}
  .mono,.path,.tag,.chip,.eyebrow,.tok{font-family:var(--mono)}
  h1{font-size:clamp(2.5rem,6.2vw,3.9rem); line-height:1.02; letter-spacing:-.02em;
     font-weight:700; margin:.35em 0 .28em; text-wrap:balance}
  h2{font-size:clamp(1.35rem,3.2vw,1.85rem); line-height:1.12; letter-spacing:-.015em;
     font-weight:650; margin:0 0 .5em; text-wrap:balance}
  h3{font-weight:600}
  p{margin:0 0 1em; max-width:var(--measure)}
  a{color:var(--keel); text-underline-offset:2px}
  strong{font-weight:600; color:var(--ink)}
  .eyebrow{font-size:.72rem; letter-spacing:.18em; text-transform:uppercase;
    color:var(--ink-faint); font-weight:500}
  .lede{font-size:clamp(1.12rem,2.4vw,1.32rem); line-height:1.5; color:var(--ink-soft);
    max-width:60ch; margin:.2em 0 0}
  .meta{font-family:var(--mono); font-size:.76rem; color:var(--ink-faint);
    letter-spacing:.02em; margin-top:1.5em; display:flex; flex-wrap:wrap; gap:.4em 1.4em}
  .meta b{color:var(--ink-soft); font-weight:500}

  section{margin-top:clamp(48px,7vw,84px)}
  .sec-head{display:flex; align-items:baseline; gap:.9em; margin-bottom:1.4em;
    border-bottom:1px solid var(--hair); padding-bottom:.7em}
  .sec-head .eyebrow{white-space:nowrap}
  .sec-head h2{margin:0}

  /* ---- the frame callout ---- */
  .frame{background:var(--surface); border:1px solid var(--hair);
    border-left:3px solid var(--keel); border-radius:0 12px 12px 0;
    padding:1.25em 1.5em; margin:0; box-shadow:0 1px 0 rgba(20,24,45,.02)}
  .frame p{margin:0; max-width:none; font-size:1.06rem}
  .frame .verbs{font-family:var(--mono); font-size:.82rem; margin-top:.85em;
    color:var(--ink-soft); letter-spacing:.01em}
  .frame .verbs b{color:var(--sheer)}

  /* ---- the spine ---- */
  .spine{display:grid; gap:14px; margin-top:.5em}
  @media(min-width:760px){ .spine{grid-template-columns:repeat(5,1fr); gap:0} }
  .node{position:relative; background:var(--surface); border:1px solid var(--hair);
    border-radius:12px; padding:1.05em 1.1em}
  @media(min-width:760px){
    .node{border-radius:0; margin-right:20px}
    .node:first-child{border-radius:12px 0 0 12px}
    .node:last-child{border-radius:0 12px 12px 0; margin-right:0}
    .node:not(:last-child)::after{content:"→"; position:absolute; right:-15px; top:50%;
      transform:translateY(-50%); color:var(--ink-faint); font-family:var(--display);
      font-weight:700; z-index:2}
  }
  .node__k{font-family:var(--mono); font-size:.68rem; letter-spacing:.06em;
    text-transform:uppercase; color:var(--ink-faint)}
  .node__t{font-family:var(--display); font-weight:650; font-size:1.02rem;
    margin:.15em 0 .35em; letter-spacing:-.01em; display:flex; align-items:center; gap:.4em}
  .node__t .dot{width:9px; height:9px; border-radius:50%; flex:none}
  .node__b{font-size:.88rem; line-height:1.42; color:var(--ink-soft); font-family:var(--body)}
  .node--keel .node__t .dot{background:var(--keel)}
  .node--sheer .node__t .dot{background:var(--sheer)}
  .node--built .node__t .dot{background:var(--ok)}
  .node__tag{display:inline-block; margin-top:.6em; font-family:var(--mono);
    font-size:.66rem; letter-spacing:.03em; padding:.12em .5em; border-radius:20px}
  .node--built .node__tag{background:var(--sheer-soft); color:var(--ok);
    border:1px solid color-mix(in srgb,var(--ok) 30%,transparent)}

  /* ---- figures ---- */
  .fig{margin:0 0 26px; background:var(--surface); border:1px solid var(--hair);
    border-radius:14px; overflow:hidden}
  .fig__head{display:flex; align-items:center; gap:.7em; padding:1em 1.2em .2em}
  .fig__n{font-family:var(--mono); font-size:.8rem; color:var(--ink-faint);
    border:1px solid var(--hair); border-radius:7px; width:1.9em; height:1.9em;
    display:grid; place-items:center; flex:none; font-weight:500}
  .fig__title{margin:0; font-size:1.08rem; font-weight:600; letter-spacing:-.01em; flex:1}
  .fig__frame{padding:8px clamp(8px,2vw,20px) 4px; overflow-x:auto}
  .fig__frame img{display:block; width:100%; max-width:560px; margin:0 auto; height:auto}
  figcaption{padding:.4em 1.4em 1.3em; font-size:.92rem; color:var(--ink-soft);
    line-height:1.5; max-width:none}
  .fig--keel{border-top:3px solid var(--keel)}
  .fig--sheer{border-top:3px solid var(--sheer)}
  .fig--line{border-top:3px solid var(--line)}

  .chip{font-size:.64rem; letter-spacing:.04em; text-transform:uppercase; font-weight:500;
    padding:.24em .6em; border-radius:20px; white-space:nowrap; flex:none}
  .chip--keel{background:var(--keel-soft); color:var(--keel);
    border:1px solid color-mix(in srgb,var(--keel) 28%,transparent)}
  .chip--sheer{background:var(--sheer-soft); color:var(--sheer);
    border:1px solid color-mix(in srgb,var(--sheer) 28%,transparent)}
  .chip--line{background:var(--line-soft); color:var(--line);
    border:1px solid color-mix(in srgb,var(--line) 28%,transparent)}
  .path{font-family:var(--mono); font-size:.82em; color:var(--ink-faint);
    text-decoration:none; border-bottom:1px dotted var(--ink-faint)}
  .fig-group-label{font-family:var(--mono); font-size:.72rem; letter-spacing:.1em;
    text-transform:uppercase; color:var(--ink-faint); margin:0 0 1em; display:flex;
    align-items:center; gap:.8em}
  .fig-group-label::after{content:""; flex:1; height:1px; background:var(--hair)}
  .fig-group-label b{color:var(--keel); font-weight:600}
  .fig-group-label.teal b{color:var(--sheer)}

  /* ---- tables ---- */
  .tbl-scroll{overflow-x:auto; margin:0 -2px}
  table{border-collapse:collapse; width:100%; font-size:.92rem; min-width:560px}
  th{font-size:.68rem; letter-spacing:.06em; text-transform:uppercase; text-align:left;
    color:var(--ink-faint); font-weight:600; padding:.7em .9em; border-bottom:1px solid var(--hair);
    vertical-align:bottom}
  td{padding:.75em .9em; border-bottom:1px solid var(--hair); vertical-align:top;
    line-height:1.42; color:var(--ink-soft)}
  td:first-child{color:var(--ink)}
  tr:last-child td{border-bottom:none}
  .verb{font-family:var(--mono); font-weight:500; font-size:.82rem; letter-spacing:.02em;
    color:var(--sheer); text-transform:uppercase; white-space:nowrap}
  .tok{font-size:.86em; background:var(--inset); border:1px solid var(--hair);
    border-radius:5px; padding:.05em .4em; color:var(--ink-soft); white-space:nowrap}

  .tag{display:inline-block; font-size:.66rem; letter-spacing:.03em; padding:.14em .55em;
    border-radius:20px; font-weight:500; white-space:nowrap}
  .tag--ok{background:var(--sheer-soft); color:var(--ok);
    border:1px solid color-mix(in srgb,var(--ok) 30%,transparent)}
  .tag--warn{background:color-mix(in srgb,var(--warn) 12%,transparent); color:var(--warn);
    border:1px solid color-mix(in srgb,var(--warn) 32%,transparent)}
  .tag--stop{background:var(--line-soft); color:var(--stop);
    border:1px solid color-mix(in srgb,var(--stop) 30%,transparent)}

  /* ---- learning + application cards ---- */
  .cards{display:grid; gap:16px; margin-top:.4em}
  @media(min-width:720px){ .cards.two{grid-template-columns:1fr 1fr} }
  .card{background:var(--surface); border:1px solid var(--hair); border-radius:12px;
    padding:1.2em 1.3em}
  .card h3{margin:0 0 .5em; font-size:1.05rem; display:flex; gap:.5em; align-items:center;
    flex-wrap:wrap}
  .card p{font-size:.94rem; color:var(--ink-soft); max-width:none}
  .card ul{margin:.3em 0 0; padding-left:1.15em; font-size:.92rem; color:var(--ink-soft)}
  .card li{margin:.35em 0; line-height:1.45}
  .card li b{color:var(--ink)}

  .files{background:var(--surface-2); border:1px solid var(--hair); border-radius:12px;
    padding:1.1em 1.35em; font-family:var(--mono); font-size:.82rem; line-height:1.9;
    overflow-x:auto}
  .files .row{display:flex; gap:1em; white-space:nowrap}
  .files .fp{color:var(--ink); flex:none}
  .files .fd{color:var(--ink-faint); white-space:normal}
  .files .grp{color:var(--sheer); margin-top:.7em; letter-spacing:.04em; text-transform:uppercase;
    font-size:.7rem}
  .files .grp:first-child{margin-top:0}

  footer{margin-top:72px; padding-top:1.5em; border-top:1px solid var(--hair);
    font-family:var(--mono); font-size:.74rem; color:var(--ink-faint); letter-spacing:.02em}
  .conf{color:var(--line)}

  @media (prefers-reduced-motion:no-preference){
    .fig img{transition:none}
  }
</style>

<div class="wrap">
  <header>
    <div class="eyebrow">HeyHi Confidential &nbsp;&middot;&nbsp; Sheerline &nbsp;&middot;&nbsp; context management &amp; the governed loop</div>
    <h1>The Governed Loop</h1>
    <p class="lede">One place to see the current architecture: how context management, the Sheerline harness, the Design&#8209;System quality loop, and its application to a client engagement&rsquo;s prototype skill all connect &mdash; with the six architecture figures and the seminar that teaches them.</p>
    <div class="meta">
      <span><b>As of</b> 2026-08-19</span>
      <span><b>Spine</b> keel &rarr; Sheerline &rarr; the loop &rarr; client proof &rarr; client prototype skill</span>
      <span><b>Figures</b> Sheerline architecture set (6)</span>
    </div>
  </header>

  <section aria-label="The frame to hold">
    <div class="frame">
      <p><strong>keel is the firm&#8209;of&#8209;one harness; Sheerline is the same idea aimed at design output.</strong> The Design&#8209;System quality loop is one module of Sheerline, its most&#8209;built one, not the whole thing. Conflating the module with the harness is the trap the OS exists to avoid.</p>
      <div class="verbs">Four verbs run through it: &nbsp;<b>retrieve</b> the system &nbsp;&rarr;&nbsp; <b>validate</b> against it &nbsp;&rarr;&nbsp; <b>grade</b> the result over time &nbsp;&rarr;&nbsp; <b>learn</b> from correction. &nbsp;Grades inform, never gate.</div>
    </div>
  </section>

  <section aria-label="Through-line">
    <div class="sec-head"><span class="eyebrow">01</span><h2>The through&#8209;line</h2></div>
    <p>Five steps, and each depends on the one before it: a general harness, aimed at design, narrowed to its most&#8209;built module, proven on a system that is not HeyHi&rsquo;s, then wired into a real client&rsquo;s build process. That last step is the newest work, and it is what makes the loop concrete rather than architectural.</p>
    <div class="spine">
      <div class="node node--keel">
        <div class="node__k">the harness</div>
        <div class="node__t"><span class="dot"></span>keel</div>
        <div class="node__b">The general firm&#8209;of&#8209;one harness. Runtime rented, configuration owned, deployment reproducible.</div>
      </div>
      <div class="node node--sheer">
        <div class="node__k">the instance</div>
        <div class="node__t"><span class="dot"></span>Sheerline</div>
        <div class="node__b">keel aimed at design output. Adds the one slot keel lacks: per&#8209;area governed <span class="tok">foundations/</span>.</div>
      </div>
      <div class="node node--sheer">
        <div class="node__k">the module</div>
        <div class="node__t"><span class="dot"></span>The quality loop</div>
        <div class="node__b">One module of Sheerline. Four verbs over three real subsystems: MCP, validator, evaluator + corrections.</div>
      </div>
      <div class="node node--built">
        <div class="node__k">the proof</div>
        <div class="node__t"><span class="dot"></span>Proven on a client system</div>
        <div class="node__b">The ingestion half run against a real external system &mdash; dark, aliased, multi&#8209;mode. It held.</div>
        <span class="node__tag">proved</span>
      </div>
      <div class="node node--built">
        <div class="node__k">the application</div>
        <div class="node__t"><span class="dot"></span>Client prototype skill</div>
        <div class="node__b">The loop now runs inside a client build: load the contract, gate on the linter, capture the correction.</div>
        <span class="node__tag">executed</span>
      </div>
    </div>
  </section>

  <section aria-label="Architecture figures">
    <div class="sec-head"><span class="eyebrow">02</span><h2>The architecture, in six figures</h2></div>
    <p>The Sheerline set. Read them in order the first time; after that each stands alone. The first two place Sheerline in the keel lineage and show the layer model it inherits; the next four are Sheerline&rsquo;s own. Each figure follows your theme and carries its own caveat rather than overclaiming.</p>

    <p class="fig-group-label"><b>inherited from keel</b></p>
    __FIGS_INHERITED__

    <p class="fig-group-label teal"><b>Sheerline&rsquo;s own</b></p>
    __FIGS_OWN__
  </section>

  <section aria-label="The loop, concretely">
    <div class="sec-head"><span class="eyebrow">03</span><h2>The loop, made concrete in a client build</h2></div>
    <p>This is the payoff, and the reason the last two spine steps matter. The four verbs are not a diagram in the abstract &mdash; each one now has a real implementation inside a client engagement&rsquo;s prototype&#8209;authoring skill. The right column is where the governed loop actually runs on a client&rsquo;s work.</p>
    <div class="tbl-scroll">
      <table>
        <thead><tr>
          <th style="width:9em">Verb</th>
          <th>In Sheerline (the module)</th>
          <th>In the client prototype skill (executed)</th>
        </tr></thead>
        <tbody>
          <tr>
            <td><span class="verb">Retrieve</span></td>
            <td>Retrieve the system through the MCP, never paste it. One summary resource plus retrieval tools.</td>
            <td>Step&nbsp;1 loads <span class="tok">DESIGN.md</span> + the DTCG contract (the 70 chrome roles, legal component variants) and declares the target mode. Static contract today; the live MCP is the optional higher&#8209;fidelity gate.</td>
          </tr>
          <tr>
            <td><span class="verb">Validate</span></td>
            <td>Deterministic, zero&#8209;token checks against the system, not the self&#8209;reported manifest.</td>
            <td><span class="tok">ds-lint.js</span> wired into Step&nbsp;6 as a blocking gate: raw hex in chrome, unknown token, off&#8209;scale value, illegal variant, value&#8209;fidelity, sub&#8209;AA pairs, a 12px type floor. Feature colors exempt by marker.</td>
          </tr>
          <tr>
            <td><span class="verb">Grade</span></td>
            <td>A linter emits a boolean; an evaluator emits a series. Grades inform, never gate.</td>
            <td>Errors block; warnings stay advisory &mdash; density sub&#8209;scale type, tokenless overlays, a missing <span class="tok">surface-warning</span> role surface for a designer to read, not auto&#8209;block.</td>
          </tr>
          <tr>
            <td><span class="verb">Learn</span></td>
            <td>One corrections registry, four readers. A factual correction injects; a behavioral one reminds a human.</td>
            <td>Two client&#8209;side corrections (the fabrication pattern; the 12px floor and token overlays) logged and promoted into the skill, so they load before the mistake can recur.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>

  <section aria-label="Learning material">
    <div class="sec-head"><span class="eyebrow">04</span><h2>The learning material</h2></div>
    <p>Two layers. The <strong>seminar</strong> teaches the harness from first principles to the point where you could stand it up, extend it, or teach it. The <strong>context&#8209;architecture foundations</strong> in <span class="tok">_core</span> are the deeper reference the seminar draws on for how context is actually governed.</p>

    <div class="cards">
      <div class="card">
        <h3>The seminar <span class="tag tag--warn">tracks 3&ndash;4 dispatched</span></h3>
        <p>A self&#8209;paced novice&#8209;to&#8209;SME curriculum, 5 tracks / 21 modules, each an 8&#8209;part reading unit with a lab against the real repo. A <span class="tok">teaches:</span> tag keeps the keel half liftable to public docs later without a rewrite.</p>
        <div class="tbl-scroll" style="margin-top:.7em">
          <table style="min-width:0">
            <tbody>
              <tr><td><b>0 &middot; Orientation</b></td><td>Why a harness exists; the ship lineage; the four invariants</td><td><span class="tag tag--ok">built</span></td></tr>
              <tr><td><b>1 &middot; keel</b></td><td>The general harness end to end (6 modules)</td><td><span class="tag tag--ok">built</span></td></tr>
              <tr><td><b>2 &middot; Sheerline</b></td><td>keel as a design harness; the foundations slot (4 modules)</td><td><span class="tag tag--ok">built</span></td></tr>
              <tr><td><b>3 &middot; Quality loop</b></td><td>retrieve &rarr; validate &rarr; grade &rarr; learn through the real subsystems</td><td><span class="tag tag--warn">dispatched</span></td></tr>
              <tr><td><b>4 &middot; SME synthesis</b></td><td>The boundary, running a loop end to end, extending the system</td><td><span class="tag tag--warn">dispatched</span></td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="card">
        <h3>Context&#8209;architecture foundations</h3>
        <p>How the harness governs what enters a session &mdash; the <strong>Earn the Room</strong> discipline, made mechanical.</p>
        <ul>
          <li><b>Four&#8209;tier loading.</b> always &middot; skills (procedural) &middot; references (knowledge, on&#8209;demand) &middot; archive. If content is relevant to fewer than half of sessions, it does not load by default.</li>
          <li><b>Discovery&#8209;aware selection.</b> A capability registry with semantic search replaces static injection, so an agent finds what it needs by querying intent, not by scanning a pre&#8209;loaded list.</li>
          <li><b>Three harness layers.</b> runtime (rented from the vendor) &middot; configuration (HeyHi&rsquo;s IP) &middot; deployment (the reproducible framework). The line between rented and owned is the one that matters for valuation.</li>
        </ul>
      </div>
    </div>
  </section>

  <section aria-label="The client application">
    <div class="sec-head"><span class="eyebrow">05</span><h2>The client application, in full</h2></div>
    <p>The DS&#8209;MCP onboarding arc proved the loop on two differently&#8209;shaped systems: the practice&rsquo;s own (the self&#8209;test reproducibility proof) and a client&rsquo;s real, external one. The client system&rsquo;s Figma&#8209;native, dark&#8209;canonical shape stress&#8209;tested axes the demo system lacks and exposed three harness gaps. One, G&#8209;ING&#8209;1 (the missing Figma&#8209;Variables adapter), is genuinely unique to that client system; the other two are not, and the practice&rsquo;s own aliased, multi&#8209;mode system re&#8209;surfaced them independently.</p>

    <div class="cards two">
      <div class="card">
        <h3>The proof <span class="tag tag--ok">G3: PASS</span></h3>
        <p>The ingestion pipeline plus the staged MCP server, run against the client&rsquo;s real design system: several variable collections, hundreds of variables with alias references, Light and Dark. It converted to DTCG, ingested, derived a 6&#8209;component contract, served an MCP that is the client&rsquo;s tokens and only the client&rsquo;s, and the validator caught real drift. All machine conditions met, and the human reviewer signed off on the audit quality. <b>G3: PASS.</b></p>
        <ul>
          <li><b>G&#8209;ING&#8209;1</b> &mdash; no first&#8209;party Figma&#8209;Variables adapter <span class="tag tag--warn">open, high</span></li>
          <li><b>G&#8209;ING&#8209;2</b> &mdash; worksheet did not resolve aliases before contrast <span class="tag tag--ok">fixed in place</span></li>
          <li><b>G&#8209;ING&#8209;3</b> &mdash; single&#8209;mode ingestion; a themed system collapses <span class="tag tag--warn">open, medium</span></li>
        </ul>
        <p style="margin-top:.7em; font-size:.88rem">Effort shape for a first onboarding pass this size: about half a day of human judgment, dominated by component behavior authoring and contrast sanctioning, on a seconds&#8209;long mechanical pipeline. That number feeds the service scope.</p>
      </div>

      <div class="card">
        <h3>The prototype&#8209;skill integration <span class="tag tag--ok">executed</span></h3>
        <p>The problem was structural: prototypes fabricated values because no canonical source was ever in context and verification had no conformance gate. The fix put a reconciled source in context and added a gate that blocks drift before delivery.</p>
        <ul>
          <li><b>Phase 1</b> &mdash; reconciled <span class="tok">DESIGN.md</span> to the contract; the DS&#8209;faithful shell is the default, legacy blue quarantined.</li>
          <li><b>Phase 2</b> &mdash; <span class="tok">ds-lint.js</span> conformance gate wired into Step&nbsp;6; annotation conventions defined.</li>
          <li><b>Phase 4</b> &mdash; corrections logged, freshness + both&#8209;modes notes added.</li>
          <li><b>Phase 3</b> (live MCP) &mdash; <span class="tag tag--stop">deferred by design</span>, the linter is the always&#8209;available gate.</li>
        </ul>
        <p style="margin-top:.7em; font-size:.88rem">Verified end to end: a fabricated value (raw chrome hex, invented token, illegal variant) is caught; a legitimate map feature color is not. A migrated prototype finished at 0 errors, on&#8209;brand in&#8209;browser.</p>
      </div>
    </div>
  </section>

  <section aria-label="Where it lives">
    <div class="sec-head"><span class="eyebrow">06</span><h2>Where it lives</h2></div>
    <p>Every source, by path. The Sheerline tree and the client contract are separate: tracked architecture on one side, engagement deliverables (gitignored, client&#8209;side) on the other.</p>
    <div class="files">
      <div class="grp">architecture &amp; diagrams &middot; tracked</div>
      <div class="row"><span class="fp">sheerline/docs/architecture.md</span><span class="fd">the six figures + narrative</span></div>
      <div class="row"><span class="fp">sheerline/docs/diagrams/*.svg</span><span class="fd">the figures, self&#8209;contained &amp; theme&#8209;aware</span></div>
      <div class="row"><span class="fp">sheerline/os/foundations/registry.yaml</span><span class="fd">the 13&#8209;area practice registry</span></div>
      <div class="grp">learning material</div>
      <div class="row"><span class="fp">sheerline/seminar/README.md</span><span class="fd">curriculum map, 5 tracks / 21 modules</span></div>
      <div class="row"><span class="fp">ai-services/_core/context-architecture-overview.md</span><span class="fd">four&#8209;tier loading + discovery</span></div>
      <div class="row"><span class="fp">ai-services/_core/harness-architecture.md</span><span class="fd">runtime / configuration / deployment</span></div>
      <div class="grp">the client application &middot; the instance&rsquo;s engagement folder (gitignored)</div>
      <div class="row"><span class="fp">&lt;engagement folder&gt;/proof record</span><span class="fd">the proving&#8209;ground record + gap list</span></div>
      <div class="row"><span class="fp">&lt;engagement folder&gt;/integration plan</span><span class="fd">the executed integration plan</span></div>
      <div class="row"><span class="fp">&lt;engagement folder&gt;/prototype skill</span><span class="fd">the client&rsquo;s SKILL.md + ds-lint.js</span></div>
    </div>
  </section>

  <footer>
    <span class="conf">HeyHi Confidential.</span> Orientation surface assembled 2026-08-19 from the Sheerline architecture set, the seminar, the _core context&#8209;architecture foundations, and the DS&#8209;MCP onboarding arc. The figures document the scaffold as architecture; the calibrated content behind the moat wall in figure 5 is never drawn here.
  </footer>
</div>
"""

HTML = HTML.replace("__FIGS_INHERITED__", figs_inherited).replace("__FIGS_OWN__", figs_own)
# Strip per-line trailing whitespace so the generated file satisfies the repo's
# trailing-whitespace pre-commit hook and stays byte-stable across regenerations.
HTML = "\n".join(line.rstrip() for line in HTML.split("\n"))
OUT.write_text(HTML, encoding="utf-8")
print(f"wrote {OUT}  ({len(HTML):,} bytes)")
