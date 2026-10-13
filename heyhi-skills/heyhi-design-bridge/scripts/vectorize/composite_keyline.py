#!/usr/bin/env python3
"""HeyHi Design Bridge — Mode 2 keyline compositing (Phase 1, PRO-24).

A refined emblem is objects composited over frame primitives (a ring/badge that
sits BEHIND the subject). Where they overlap, the design needs a managed keyline —
the negative-space (or positive-stroke) separation that makes the object read as
on top. This module knocks a uniform keyline between an object silhouette and a
frame primitive, as one operation parameterised by a single width.

Two kinds:
  occlusion (default) — frame MINUS dilate(object, w). A cream/background gap.
  stroke             — dilate(object, w) AND NOT object. A positive outline path.

DEF-5 guardrail (the trap this build exists to not repeat): potrace's SVG backend
wraps every path in a `<g transform="translate(0,H) scale(0.1,-0.1)">`. Extracting
the raw `d` and embedding it without that transform renders the path off-canvas,
so the mask silently does nothing — yet a small thumbnail still LOOKS fixed. This
module always CARRIES the transform, and `assert_keyline_opens()` proves the frame
actually opened where the figure crosses (an A/B pixel-diff vs the continuous
frame), so the craft is checked by geometry, not by eyeballing a render.

Status: DRAFT in skill-updates/. Promotion to the deployed skill is human-gated and
happens with the Phase 5 doc edits. Not wired into vectorize.py yet.

HeyHi Confidential.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import tempfile
from collections import deque

import numpy as np
from PIL import Image, ImageFilter


# --------------------------------------------------------------------------- #
# raster ops
# --------------------------------------------------------------------------- #

def ink_mask(path_or_img, thresh: int = 110) -> np.ndarray:
    """Boolean ink mask (True = dark ink) from a grayscale-able image."""
    img = path_or_img if isinstance(path_or_img, Image.Image) else Image.open(path_or_img)
    return np.asarray(img.convert("L")) < thresh


def outer_silhouette(mask: np.ndarray) -> np.ndarray:
    """Fill interior holes of a binary object mask -> solid outer silhouette.

    The keyline follows the object's OUTER profile, not its interior knockout
    holes (eye, muzzle). Flood-fill the background inward from the border; any
    non-ink pixel the flood cannot reach is an interior hole and is filled.
    """
    h, w = mask.shape
    bg = np.zeros_like(mask, dtype=bool)
    q: deque = deque()
    for x in range(w):
        for y in (0, h - 1):
            if not mask[y, x] and not bg[y, x]:
                bg[y, x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if not mask[y, x] and not bg[y, x]:
                bg[y, x] = True
                q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not mask[ny, nx] and not bg[ny, nx]:
                bg[ny, nx] = True
                q.append((ny, nx))
    return mask | (~bg)


def dilate_disk(mask: np.ndarray, r: int) -> np.ndarray:
    """Disk dilation by r px. scipy distance transform when available (true disk),
    else iterated 3x3 max filter (diamond-ish; potrace smooths the trace edge)."""
    if r <= 0:
        return mask
    try:
        from scipy.ndimage import distance_transform_edt
        return distance_transform_edt(~mask) <= r
    except Exception:
        im = Image.fromarray((mask * 255).astype("uint8"))
        for _ in range(r):
            im = im.filter(ImageFilter.MaxFilter(3))
        return np.asarray(im) > 127


# --------------------------------------------------------------------------- #
# trace (transform-carrying — DEF-5)
# --------------------------------------------------------------------------- #

def bake_transform(d: str, transform: str) -> str:
    """Bake an affine `translate(tx,ty) scale(sx,sy)` (potrace's form — no rotation)
    into a path's coordinates, returning clean viewBox-space `d`.

    This kills DEF-5 at the source: with the transform folded into the numbers, no
    downstream assembly has to carry a `<g transform>` (the silent, thumbnail-
    deceptive trap that recurred at four sites before this).

    General affine bake (no rotation): every ABSOLUTE command (uppercase) gets
    scale + translate; every RELATIVE command (lowercase) gets scale only. potrace
    emits absolute `M` per subpath + relative c/l between, but this handles any mix.
    Raises on arcs (A/a) — potrace emits none — so a mis-bake fails loudly.
    """
    m = re.match(r"translate\(([-\d.]+)[ ,]([-\d.]+)\)\s*scale\(([-\d.]+)[ ,]([-\d.]+)\)",
                 transform.strip())
    if not m:
        return d  # no recognised transform -> already viewBox space
    tx, ty, sx, sy = map(float, m.groups())
    out = []
    for c, nstr in re.findall(r"([A-Za-z])([^A-Za-z]*)", d):
        cl, absolute = c.lower(), c.isupper()
        nums = [float(n) for n in re.findall(r"-?\d*\.?\d+", nstr)]
        if cl == "z":
            out.append(c)
            continue
        if cl == "a":
            raise ValueError("bake_transform: arc commands unsupported (potrace emits none)")
        tn = []
        if cl == "h":            # x only
            tn = [n * sx + (tx if absolute else 0) for n in nums]
        elif cl == "v":          # y only
            tn = [n * sy + (ty if absolute else 0) for n in nums]
        else:                    # (x,y) pairs — M L C S Q T
            for k, n in enumerate(nums):
                tn.append(n * sx + (tx if absolute else 0) if k % 2 == 0
                          else n * sy + (ty if absolute else 0))
        out.append(c + " " + " ".join(f"{v:.2f}" for v in tn))
    return " ".join(out)


def potrace_path(mask: np.ndarray, turdsize: int = 20, alphamax: float = 1.0,
                 opttol: float = 1.0, tmp: str | None = None, bake: bool = True):
    """Trace a binary mask -> (path_d, transform).

    bake=True (default): potrace's `translate/scale` is folded into `path_d`
    (viewBox coords) and `transform` is "" — callers never carry it (DEF-5 fix at
    the source). bake=False returns the raw potrace `d` + its `transform`; the
    caller MUST embed `<g transform>` or the path renders off-canvas.
    """
    tmp = tmp or tempfile.mkdtemp(prefix="keyline_")
    pbm = os.path.join(tmp, "_m.pbm")
    svg = os.path.join(tmp, "_m.svg")
    # potrace traces black as foreground: object -> 0 (black), bg -> 255 (white)
    Image.fromarray(((~mask) * 255).astype("uint8")).convert("1").save(pbm)
    subprocess.run(
        ["potrace", "-s", "-o", svg, "--turdsize", str(turdsize),
         "--alphamax", str(alphamax), "--opttolerance", str(opttol), pbm],
        check=True, capture_output=True,
    )
    t = open(svg).read()
    gm = re.search(r'<g [^>]*transform="([^"]+)"', t)
    transform = gm.group(1) if gm else ""
    d = " ".join(re.findall(r'<path[^>]*\bd="([^"]+)"', t))
    d = re.sub(r"\s+", " ", d).strip()
    if not d:
        raise ValueError("potrace produced no path (empty mask?)")
    if bake and transform:
        d, transform = bake_transform(d, transform), ""
    return d, transform


# --------------------------------------------------------------------------- #
# keyline kinds
# --------------------------------------------------------------------------- #

def keyline_occlusion(object_mask: np.ndarray, w: int, **trace):
    """The subtractor: dilate(outer_silhouette(object), w). Returns (d, transform)."""
    sub = dilate_disk(outer_silhouette(object_mask), w)
    return potrace_path(sub, **trace)


def keyline_stroke(object_mask: np.ndarray, w: int, **trace):
    """A positive outline band: dilate(object, w) AND NOT object. Returns (d, transform)."""
    sil = outer_silhouette(object_mask)
    band = dilate_disk(sil, w) & (~sil)
    return potrace_path(band, **trace)


def default_keyline_width(frame_diameter_px: float) -> int:
    """Calibrated default keyline width (Phase 4, PRO-24): ~1.8% of the frame diameter
    (= ~3.7% of radius). Calibrated at w=11 on a 600px-diameter worked emblem; it
    generalised cleanly to two further marks at the same ratio. Pass 2*R_out from refine_primitive.fit_circle."""
    return max(2, round(0.018 * frame_diameter_px))


# --------------------------------------------------------------------------- #
# SVG assembly
# --------------------------------------------------------------------------- #

def _wrap(d: str, transform: str, fill: str) -> str:
    inner = f'<path d="{d}" fill="{fill}"/>'
    return f'<g transform="{transform}">{inner}</g>' if transform else inner


def knockout_svg(frame_d: str, object_art_ds, sub_d: str, sub_transform: str,
                 fill: str, viewbox: int = 656, title: str = "keyline emblem",
                 art_transform: str = "") -> str:
    """Occlusion composite: frame masked by the dilated figure, object art on top.

    `art_transform` wraps the object art in a `<g transform>` — pass it when the art
    comes straight from potrace (10x-flipped coords). Omit for clean viewBox-space art.
    Dropping it is the DEF-5 trap: the art renders off-canvas yet a thumbnail can look fine.
    """
    art = "".join(f'<path d="{d}"/>' for d in object_art_ds)
    if art_transform:
        art = f'<g transform="{art_transform}">{art}</g>'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {viewbox} {viewbox}" '
        f'role="img" aria-label="{title}">\n'
        f'  <defs><mask id="kl" maskUnits="userSpaceOnUse" x="0" y="0" '
        f'width="{viewbox}" height="{viewbox}">\n'
        f'    <rect width="{viewbox}" height="{viewbox}" fill="#fff"/>\n'
        f'    {_wrap(sub_d, sub_transform, "#000")}\n  </mask></defs>\n'
        f'  <g fill="{fill}" fill-rule="nonzero">\n'
        f'    <path d="{frame_d}" mask="url(#kl)"/>\n    {art}\n  </g>\n</svg>\n'
    )


def stroke_svg(frame_d: str, object_art_ds, outline_d: str, outline_transform: str,
               fill: str, keyline_color: str, viewbox: int = 656,
               title: str = "keyline emblem", art_transform: str = "") -> str:
    """Stroke composite: frame, then a positive outline, then the object art.

    `art_transform` wraps the object art (see knockout_svg — same DEF-5 trap).
    """
    art = "".join(f'<path d="{d}"/>' for d in object_art_ds)
    if art_transform:
        art = f'<g transform="{art_transform}">{art}</g>'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {viewbox} {viewbox}" '
        f'role="img" aria-label="{title}">\n'
        f'  <path d="{frame_d}" fill="{fill}"/>\n'
        f'  {_wrap(outline_d, outline_transform, keyline_color)}\n'
        f'  <g fill="{fill}" fill-rule="nonzero">{art}</g>\n</svg>\n'
    )


def expanded_figure_svg(sub_d: str, sub_transform: str, viewbox: int = 656) -> str:
    """The subtractor as a standalone SVG — feed to Figma createNodeFromSvg, then
    figma.subtract([ring, expanded], parent) for the live Boolean-Subtract form."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {viewbox} {viewbox}">'
        f'{_wrap(sub_d, sub_transform, "#000")}</svg>'
    )


def figma_boolean_landing_js(frame_d: str, object_art_ds, sub_d: str, sub_transform: str,
                             fill_hex: str, parent_id: str, name: str = "emblem (keyline)",
                             x: int = 0, y: int = 0, target: int = 432, viewbox: int = 656) -> str:
    """Generate the `use_figma` JS for a repeatable live **Boolean-Subtract** keyline
    landing (Phase 3, PRO-24). The routine: import frame + expanded-figure + object art,
    `figma.subtract([frame, expanded])` → keyline ring, recolor, group with the art,
    scale + position. The keyline stays editable (a live boolean) — adjust the expanded
    figure's offset and it reflows, no re-import.

    Pass baked paths (`bake=True`, the default) so no `<g transform>` is needed. Returns
    a JS string to hand to the use_figma tool; verify the landing with a screenshot +
    hole-transparency check (the DEF-4 guardrail) — see SKILL.md Mode 2 step 6.
    """
    art = "".join(f'<path d="{d}"/>' for d in object_art_ds)
    ring = f'<svg viewBox="0 0 {viewbox} {viewbox}"><path d="{frame_d}" fill="#000"/></svg>'
    arts = f'<svg viewBox="0 0 {viewbox} {viewbox}"><g fill="#000" fill-rule="nonzero">{art}</g></svg>'
    exps = expanded_figure_svg(sub_d, sub_transform, viewbox)
    r = int(fill_hex.lstrip('#')[0:2], 16)
    g = int(fill_hex.lstrip('#')[2:4], 16)
    b = int(fill_hex.lstrip('#')[4:6], 16)
    return f"""
const COL = {{ r: {r/255:.4f}, g: {g/255:.4f}, b: {b/255:.4f} }};
const ringSvg = `{ring}`;
const expSvg  = `{exps}`;
const artSvg  = `{arts}`;
function leaves(svg, parent) {{
  const f = figma.createNodeFromSvg(svg); const acc = [];
  (function rec(n){{ if (n.type === 'VECTOR') acc.push(n); else if ('children' in n) [...n.children].forEach(rec); }})(f);
  acc.forEach(v => parent.appendChild(v)); f.remove(); return acc;
}}
function setFill(n, c) {{ if ('fills' in n && n.type !== 'FRAME') n.fills = [{{ type:'SOLID', color:c }}]; if ('children' in n) n.children.forEach(x => setFill(x, c)); }}
const parent = await figma.getNodeByIdAsync("{parent_id}");
const ringV = leaves(ringSvg, parent);
const expV  = leaves(expSvg, parent);
const ko = figma.subtract([ringV[0], expV[0]], parent);
ko.name = "ring (keyline)"; ko.fills = [{{ type:'SOLID', color:COL }}];
const artV = leaves(artSvg, parent); artV.forEach(v => setFill(v, COL));
const emblem = figma.group([ko, ...artV], parent);
emblem.name = "{name}";
emblem.rescale({target} / {viewbox});
emblem.x = {x}; emblem.y = {y};
figma.currentPage.selection = [emblem]; figma.viewport.scrollAndZoomIntoView([emblem]);
return JSON.stringify({{ emblem: emblem.id, w: Math.round(emblem.width), ko: ko.type }});
""".strip()


# --------------------------------------------------------------------------- #
# verification (DEF-5 guardrail)
# --------------------------------------------------------------------------- #

def _render(svg_text: str, bg: str, size: int, tmp: str) -> np.ndarray:
    s = os.path.join(tmp, "_r.svg")
    p = os.path.join(tmp, "_r.png")
    open(s, "w").write(svg_text)
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size),
                    "-b", bg, "-o", p, s], check=True, capture_output=True)
    return np.asarray(Image.open(p).convert("RGB")).astype(int)


def assert_keyline_opens(fixed_svg: str, continuous_svg: str, region, min_changed: int,
                         bg: str = "#F2E9CF", size: int = 600, tmp: str | None = None) -> int:
    """Geometric proof the keyline opened the frame in `region` (x0,y0,x1,y1 in
    `size` space). Renders both and asserts the changed-pixel count exceeds
    `min_changed`. This is the check a thumbnail cannot fake (DEF-5)."""
    tmp = tmp or tempfile.mkdtemp(prefix="keyline_chk_")
    a = _render(continuous_svg, bg, size, tmp)
    b = _render(fixed_svg, bg, size, tmp)
    x0, y0, x1, y1 = region
    changed = int((np.abs(a[y0:y1, x0:x1] - b[y0:y1, x0:x1]).sum(2) > 60).sum())
    if changed < min_changed:
        raise AssertionError(
            f"keyline did not open the frame in {region}: {changed} px changed "
            f"(< {min_changed}). Likely a dropped potrace transform (DEF-5)."
        )
    return changed


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def _frame_path_from_svg(svg_path: str) -> str:
    return re.findall(r'<path[^>]*\bd="([^"]+)"', open(svg_path).read())[0]


def main(argv=None):
    ap = argparse.ArgumentParser(description="HeyHi Design Bridge — keyline compositing")
    ap.add_argument("--object-mask", required=True, help="PNG; dark ink = the object")
    ap.add_argument("--object-art", required=True, help="SVG whose paths render on top")
    ap.add_argument("--frame", required=True, help="SVG with the frame primitive path")
    ap.add_argument("--out", required=True)
    ap.add_argument("--keyline-width", type=int, default=11)
    ap.add_argument("--kind", choices=["occlusion", "stroke"], default="occlusion")
    ap.add_argument("--fill", default="#2F4A31")
    ap.add_argument("--keyline-color", default="#F2E9CF", help="stroke kind only")
    ap.add_argument("--viewbox", type=int, default=656)
    ap.add_argument("--expanded-out", default=None, help="write the subtractor SVG (Figma)")
    ap.add_argument("--assert-against", default=None, help="continuous-frame SVG for the guardrail")
    ap.add_argument("--assert-region", default="300,20,600,240")
    ap.add_argument("--assert-min", type=int, default=1500)
    a = ap.parse_args(argv)

    mask = ink_mask(a.object_mask)
    frame_d = _frame_path_from_svg(a.frame)
    art_ds = re.findall(r'<path[^>]*\bd="([^"]+)"', open(a.object_art).read())
    tr = dict(viewbox=a.viewbox)

    if a.kind == "occlusion":
        sub_d, sub_tf = keyline_occlusion(mask, a.keyline_width)
        svg = knockout_svg(frame_d, art_ds, sub_d, sub_tf, a.fill, a.viewbox)
        if a.expanded_out:
            open(a.expanded_out, "w").write(expanded_figure_svg(sub_d, sub_tf, a.viewbox))
    else:
        out_d, out_tf = keyline_stroke(mask, a.keyline_width)
        svg = stroke_svg(frame_d, art_ds, out_d, out_tf, a.fill, a.keyline_color, a.viewbox)

    open(a.out, "w").write(svg)
    result = {"out": a.out, "kind": a.kind, "keyline_width": a.keyline_width}

    if a.assert_against:
        cont = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {a.viewbox} {a.viewbox}">'
                f'<g fill="{a.fill}" fill-rule="nonzero"><path d="{frame_d}"/>'
                + "".join(f'<path d="{d}"/>' for d in art_ds) + '</g></svg>') \
            if a.assert_against == "auto" else open(a.assert_against).read()
        region = tuple(int(v) for v in a.assert_region.split(","))
        result["keyline_px_changed"] = assert_keyline_opens(svg, cont, region, a.assert_min)
        result["assert"] = "PASS"

    print(result)
    return result


if __name__ == "__main__":
    main()
