"""Schneider least-squares cubic-Bezier curve fitting.

A vendored port of Philip J. Schneider, "An Algorithm for Automatically Fitting
Digitized Curves" (Graphics Gems, 1990). This is the curve-fit simplifier the plan
calls for: it fits the *fewest* cubic Beziers that hold a polyline within a max
error, with C1 continuity at the joins. It is deliberately NOT Ramer-Douglas-Peucker
— RDP simplifies polylines into straight segments and would flatten the curves a
mark depends on. Used only as a fallback when trace-time params leave a path with
excess anchors (anchor reduction is primarily a trace-parameter job).

Operates on Nx2 arrays; returns a list of [P0, C1, C2, P3] cubic control quads.

HeyHi Confidential.
"""
from __future__ import annotations

import numpy as np


def _normalize(v):
    n = np.linalg.norm(v)
    return v / n if n > 1e-12 else np.zeros_like(v)


def fit_curve(points, max_error: float):
    """Fit a sequence of cubic Beziers to `points` (Nx2). Returns list of 4x2 arrays."""
    pts = np.asarray(points, dtype=float)
    # drop consecutive duplicates (they break tangent estimation)
    keep = [0]
    for i in range(1, len(pts)):
        if np.linalg.norm(pts[i] - pts[keep[-1]]) > 1e-9:
            keep.append(i)
    pts = pts[keep]
    if len(pts) < 2:
        return []
    if len(pts) == 2:
        dist = np.linalg.norm(pts[1] - pts[0]) / 3.0
        t = _normalize(pts[1] - pts[0])
        return [np.array([pts[0], pts[0] + t * dist, pts[1] - t * dist, pts[1]])]
    left = _normalize(pts[1] - pts[0])
    right = _normalize(pts[-2] - pts[-1])
    return _fit_cubic(pts, left, right, max_error)


def _fit_cubic(pts, t_left, t_right, max_error):
    if len(pts) == 2:
        dist = np.linalg.norm(pts[1] - pts[0]) / 3.0
        return [np.array([pts[0], pts[0] + t_left * dist, pts[1] + t_right * dist, pts[1]])]

    u = _chord_length_parameterize(pts)
    bez = _generate_bezier(pts, u, t_left, t_right)
    err, split = _max_error(pts, bez, u)
    if err < max_error:
        return [bez]

    # in-tolerance enough to try reparameterizing before splitting
    if err < max_error * max_error:
        for _ in range(20):
            u = _reparameterize(pts, bez, u)
            bez = _generate_bezier(pts, u, t_left, t_right)
            err, split = _max_error(pts, bez, u)
            if err < max_error:
                return [bez]

    # split at the worst point and recurse, with a shared center tangent
    center_t = _normalize(pts[split - 1] - pts[split + 1])
    left = _fit_cubic(pts[: split + 1], t_left, center_t, max_error)
    right = _fit_cubic(pts[split:], -center_t, t_right, max_error)
    return left + right


def _generate_bezier(pts, u, t_left, t_right):
    n = len(pts)
    A = np.zeros((n, 2, 2))
    for i, ui in enumerate(u):
        A[i, 0] = t_left * (3 * ui * (1 - ui) ** 2)
        A[i, 1] = t_right * (3 * ui ** 2 * (1 - ui))
    C = np.zeros((2, 2))
    X = np.zeros(2)
    p0, p3 = pts[0], pts[-1]
    for i, ui in enumerate(u):
        b0 = (1 - ui) ** 3
        b1 = 3 * ui * (1 - ui) ** 2
        b2 = 3 * ui ** 2 * (1 - ui)
        b3 = ui ** 3
        C[0, 0] += A[i, 0] @ A[i, 0]
        C[0, 1] += A[i, 0] @ A[i, 1]
        C[1, 0] += A[i, 0] @ A[i, 1]
        C[1, 1] += A[i, 1] @ A[i, 1]
        tmp = pts[i] - (p0 * (b0 + b1) + p3 * (b2 + b3))
        X[0] += A[i, 0] @ tmp
        X[1] += A[i, 1] @ tmp
    det_C = C[0, 0] * C[1, 1] - C[1, 0] * C[0, 1]
    det_X0 = X[0] * C[1, 1] - C[0, 1] * X[1]
    det_X1 = C[0, 0] * X[1] - X[0] * C[1, 0]
    alpha_l = 0.0 if abs(det_C) < 1e-12 else det_X0 / det_C
    alpha_r = 0.0 if abs(det_C) < 1e-12 else det_X1 / det_C

    seg = np.linalg.norm(p3 - p0)
    if alpha_l < 1e-6 or alpha_r < 1e-6:  # fall back to Wu/Barsky heuristic
        alpha_l = alpha_r = seg / 3.0
    return np.array([p0, p0 + t_left * alpha_l, p3 + t_right * alpha_r, p3])


def _bezier_point(bez, t):
    mt = 1 - t
    return (bez[0] * mt ** 3 + bez[1] * 3 * mt ** 2 * t
            + bez[2] * 3 * mt * t ** 2 + bez[3] * t ** 3)


def _chord_length_parameterize(pts):
    u = np.zeros(len(pts))
    for i in range(1, len(pts)):
        u[i] = u[i - 1] + np.linalg.norm(pts[i] - pts[i - 1])
    if u[-1] > 0:
        u /= u[-1]
    return u


def _reparameterize(pts, bez, u):
    return np.array([_newton(bez, p, ui) for p, ui in zip(pts, u)])


def _newton(bez, point, t):
    d = _bezier_point(bez, t) - point
    # first and second derivatives
    q1 = [3 * (bez[i + 1] - bez[i]) for i in range(3)]
    q2 = [2 * (q1[i + 1] - q1[i]) for i in range(2)]
    mt = 1 - t
    d1 = q1[0] * mt ** 2 + q1[1] * 2 * mt * t + q1[2] * t ** 2
    d2 = q2[0] * mt + q2[1] * t
    num = d @ d1
    den = d1 @ d1 + d @ d2
    return t if abs(den) < 1e-12 else t - num / den


def _max_error(pts, bez, u):
    max_d, split = 0.0, len(pts) // 2
    for i in range(1, len(pts) - 1):
        diff = _bezier_point(bez, u[i]) - pts[i]
        d = diff @ diff
        if d > max_d:
            max_d, split = d, i
    return max_d, split
