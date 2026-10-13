"""SVG path parsing, flattening, and Schneider re-emission.

Supports the command set vtracer/potrace emit (M/L/H/V/C/S/Q/T/Z, abs + rel). Arcs
(A) are not emitted by either tracer; a path containing one is left untouched and
flagged rather than mis-fit. The curve-fit stage flattens each subpath to a dense
polyline and refits the fewest cubic Beziers within a pixel tolerance (fit_curve) —
the optional anchor-reduction fallback the plan specifies.

HeyHi Confidential.
"""
from __future__ import annotations

import math
import re

import numpy as np

import fit_curve as fc

_TOKEN_RE = re.compile(
    r"([MmLlHhVvCcSsQqTtAaZz])|([-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?)"
)


def _tokens(d):
    out = []
    for m in _TOKEN_RE.finditer(d):
        out.append(("c", m.group(1)) if m.group(1) else ("n", float(m.group(2))))
    return out


class UnsupportedCommand(Exception):
    pass


def _arc_to_points(p0, rx, ry, phi_deg, large_arc, sweep, p1, samples=24):
    """Sample an SVG elliptical arc into points (endpoint -> center parameterization).

    Assumes space-separated flags (vtracer's form). Returns a list of [x,y] including
    the endpoint; the arc is appended to the polyline as line segments for refitting.
    """
    p0 = np.asarray(p0, float)
    p1 = np.asarray(p1, float)
    rx, ry = abs(rx), abs(ry)
    if rx < 1e-9 or ry < 1e-9 or np.allclose(p0, p1):
        return [p1]
    phi = math.radians(phi_deg % 360)
    cp, sp = math.cos(phi), math.sin(phi)
    dx, dy = (p0 - p1) / 2.0
    x1p = cp * dx + sp * dy
    y1p = -sp * dx + cp * dy
    lam = x1p ** 2 / rx ** 2 + y1p ** 2 / ry ** 2
    if lam > 1:
        s = math.sqrt(lam)
        rx, ry = rx * s, ry * s
    den = rx ** 2 * y1p ** 2 + ry ** 2 * x1p ** 2
    num = rx ** 2 * ry ** 2 - den
    co = math.sqrt(max(0.0, num / den)) if den > 0 else 0.0
    if large_arc == sweep:
        co = -co
    cxp = co * (rx * y1p / ry)
    cyp = -co * (ry * x1p / rx)
    cx = cp * cxp - sp * cyp + (p0[0] + p1[0]) / 2
    cy = sp * cxp + cp * cyp + (p0[1] + p1[1]) / 2

    def angle(ux, uy, vx, vy):
        dot = ux * vx + uy * vy
        ln = math.hypot(ux, uy) * math.hypot(vx, vy)
        a = math.acos(max(-1.0, min(1.0, dot / ln))) if ln else 0.0
        return -a if (ux * vy - uy * vx) < 0 else a

    theta1 = angle(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dtheta = angle((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if not sweep and dtheta > 0:
        dtheta -= 2 * math.pi
    elif sweep and dtheta < 0:
        dtheta += 2 * math.pi
    pts = []
    for k in range(1, samples + 1):
        t = theta1 + dtheta * k / samples
        x = cp * rx * math.cos(t) - sp * ry * math.sin(t) + cx
        y = sp * rx * math.cos(t) + cp * ry * math.sin(t) + cy
        pts.append([x, y])
    return pts


def parse_subpaths(d):
    """Parse `d` into absolute subpaths. Each subpath: dict(start, segs, closed).

    segs is a list of ('L', p) | ('C', c1, c2, p). Q is degree-elevated to C; H/V
    become L; S/T reflect the previous control. Raises UnsupportedCommand on arcs.
    """
    toks = _tokens(d)
    subs, cur_sub = [], None
    i, N = 0, len(toks)
    cmd = None
    pos = np.zeros(2)
    start = np.zeros(2)
    prev_cubic_c2 = None
    prev_quad_c = None

    def flush():
        nonlocal cur_sub
        if cur_sub is not None and cur_sub["segs"]:
            subs.append(cur_sub)

    while i < N:
        kind, val = toks[i]
        if kind == "c":
            cmd = val
            i += 1
            if cmd in "Zz":
                if cur_sub is not None:
                    cur_sub["closed"] = True
                    cur_sub["segs"].append(("L", start.copy()))
                    pos = start.copy()
                flush()
                cur_sub = None
                cmd = None
                continue
        if cmd is None:
            i += 1
            continue
        base = cmd.upper()
        rel = cmd.islower()

        def take(n):
            nonlocal i
            vals = [toks[i + k][1] for k in range(n)]
            i += n
            return vals

        if base == "A":
            rx, ry, rot, laf, sf, x, y = take(7)
            base_pt = pos
            end = (base_pt + [x, y]) if rel else np.array([x, y])
            for p in _arc_to_points(base_pt, rx, ry, rot, int(laf), int(sf), end):
                cur_sub["segs"].append(("L", np.asarray(p, float)))
            pos = end
            prev_cubic_c2 = prev_quad_c = None
            continue

        if base == "M":
            x, y = take(2)
            pos = (pos + [x, y]) if rel else np.array([x, y])
            flush()
            start = pos.copy()
            cur_sub = {"start": pos.copy(), "segs": [], "closed": False}
            cmd = "l" if rel else "L"  # implicit lineto
            prev_cubic_c2 = prev_quad_c = None
        elif base == "L":
            x, y = take(2)
            pos = (pos + [x, y]) if rel else np.array([x, y])
            cur_sub["segs"].append(("L", pos.copy()))
            prev_cubic_c2 = prev_quad_c = None
        elif base == "H":
            (x,) = take(1)
            pos = np.array([pos[0] + x if rel else x, pos[1]])
            cur_sub["segs"].append(("L", pos.copy()))
            prev_cubic_c2 = prev_quad_c = None
        elif base == "V":
            (y,) = take(1)
            pos = np.array([pos[0], pos[1] + y if rel else y])
            cur_sub["segs"].append(("L", pos.copy()))
            prev_cubic_c2 = prev_quad_c = None
        elif base == "C":
            x1, y1, x2, y2, x, y = take(6)
            base_pt = pos
            c1 = (base_pt + [x1, y1]) if rel else np.array([x1, y1])
            c2 = (base_pt + [x2, y2]) if rel else np.array([x2, y2])
            pos = (base_pt + [x, y]) if rel else np.array([x, y])
            cur_sub["segs"].append(("C", c1, c2, pos.copy()))
            prev_cubic_c2 = c2
            prev_quad_c = None
        elif base == "S":
            x2, y2, x, y = take(4)
            base_pt = pos
            c1 = 2 * pos - prev_cubic_c2 if prev_cubic_c2 is not None else pos.copy()
            c2 = (base_pt + [x2, y2]) if rel else np.array([x2, y2])
            pos = (base_pt + [x, y]) if rel else np.array([x, y])
            cur_sub["segs"].append(("C", c1, c2, pos.copy()))
            prev_cubic_c2 = c2
            prev_quad_c = None
        elif base == "Q":
            x1, y1, x, y = take(4)
            base_pt = pos
            q = (base_pt + [x1, y1]) if rel else np.array([x1, y1])
            end = (base_pt + [x, y]) if rel else np.array([x, y])
            c1 = base_pt + 2.0 / 3.0 * (q - base_pt)
            c2 = end + 2.0 / 3.0 * (q - end)
            cur_sub["segs"].append(("C", c1, c2, end.copy()))
            pos = end
            prev_quad_c = q
            prev_cubic_c2 = None
        elif base == "T":
            x, y = take(2)
            base_pt = pos
            q = 2 * pos - prev_quad_c if prev_quad_c is not None else pos.copy()
            end = (base_pt + [x, y]) if rel else np.array([x, y])
            c1 = base_pt + 2.0 / 3.0 * (q - base_pt)
            c2 = end + 2.0 / 3.0 * (q - end)
            cur_sub["segs"].append(("C", c1, c2, end.copy()))
            pos = end
            prev_quad_c = q
            prev_cubic_c2 = None
        else:
            i += 1
    flush()
    return subs


def _cubic(p0, c1, c2, p3, t):
    mt = 1 - t
    return p0 * mt ** 3 + c1 * 3 * mt ** 2 * t + c2 * 3 * mt * t ** 2 + p3 * t ** 3


def flatten_subpath(sub, samples=24):
    pts = [np.asarray(sub["start"], float)]
    cur = pts[0]
    for seg in sub["segs"]:
        if seg[0] == "L":
            pts.append(seg[1])
            cur = seg[1]
        else:  # 'C'
            c1, c2, p = seg[1], seg[2], seg[3]
            for k in range(1, samples + 1):
                pts.append(_cubic(cur, c1, c2, p, k / samples))
            cur = p
    return np.array(pts)


def _fmt(p, prec):
    return f"{p[0]:.{prec}f} {p[1]:.{prec}f}"


def refit_path_d(d, max_error, samples=24, prec=2):
    """Flatten every subpath and refit with Schneider; return (new_d, anchors)."""
    subs = parse_subpaths(d)  # may raise UnsupportedCommand
    parts, anchors = [], 0
    for sub in subs:
        poly = flatten_subpath(sub, samples)
        if sub["closed"] and len(poly) > 1 and np.allclose(poly[0], poly[-1]):
            poly = poly[:-1]
        if len(poly) < 2:
            continue
        cubics = fc.fit_curve(poly, max_error)
        if not cubics:
            continue
        p0 = cubics[0][0]
        parts.append(f"M{_fmt(p0, prec)}")
        anchors += 1
        for b in cubics:
            parts.append(f"C{_fmt(b[1], prec)} {_fmt(b[2], prec)} {_fmt(b[3], prec)}")
            anchors += 1
        if sub["closed"]:
            parts.append("Z")
    return " ".join(parts), anchors


def curve_fit_svg(svg_text, threshold, max_error, samples=24, prec=2):
    """Refit only paths whose anchor count exceeds `threshold`. Returns (svg, stats)."""
    from svg_tools import count_anchors_in_path

    stats = {"refit_paths": 0, "skipped_arc": 0, "anchors_before": 0, "anchors_after": 0}

    def repl(m):
        d = m.group(2)
        before = count_anchors_in_path(d)
        stats["anchors_before"] += before
        if before <= threshold:
            stats["anchors_after"] += before
            return m.group(0)
        try:
            new_d, after = refit_path_d(d, max_error, samples, prec)
        except UnsupportedCommand:
            stats["skipped_arc"] += 1
            stats["anchors_after"] += before
            return m.group(0)
        if not new_d or after >= before:  # never make it worse
            stats["anchors_after"] += before
            return m.group(0)
        stats["refit_paths"] += 1
        stats["anchors_after"] += after
        return f'{m.group(1)}d="{new_d}"'

    new_svg = re.sub(r'(<path[^>]*?\s)d="([^"]*)"', repl, svg_text)
    return new_svg, stats
