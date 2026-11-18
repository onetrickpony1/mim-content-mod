"""Check every block model in the mod for elements that cut into each other or flicker (z-fighting).

For every pair of elements in one model it reports:
  overlap   the two boxes share volume (one cuts through the other);
  zfight    two faces lie in the same plane, face the same way and overlap: they flicker in the game;
  touching  two faces lie in the same plane facing each other and overlap: hidden inside, harmless, counted only.
Rotated elements (axis + angle about an origin, with rescale) are handled as turned boxes.

    art/.venv/bin/python art/tools/model_check.py [model.json ...]     (no arguments: every block model in the mod)
Exit code 1 when any overlap or zfight is found.
"""
import glob
import json
import math
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "models")
EPS = 1e-3        # gaps and depths below this count as touching
AREA = 1e-3       # face overlaps smaller than this (in square pixels) are ignored

AXES = {"x": np.array([1.0, 0, 0]), "y": np.array([0, 1.0, 0]), "z": np.array([0, 0, 1.0])}
# face -> (axis index, which end: 0 = from, 1 = to)
FACES = {"west": (0, 0), "east": (0, 1), "down": (1, 0), "up": (1, 1), "north": (2, 0), "south": (2, 1)}


def rot_matrix(axis, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    if axis == "x":
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    if axis == "y":
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def transform(e):
    """A function taking model-space points of the unrotated box to their final place."""
    r = e.get("rotation")
    if not r or not r.get("angle"):
        return lambda p: np.asarray(p, float)
    o = np.array(r.get("origin", [8, 8, 8]), float)
    m = rot_matrix(r["axis"], r["angle"])
    if r.get("rescale"):
        k = 1 / math.cos(math.radians(abs(r["angle"])))
        sc = np.array([1.0 if a == r["axis"] else k for a in "xyz"])
        m = m @ np.diag(sc)
    return lambda p: (np.asarray(p, float) - o) @ m.T + o


def corners(e):
    f, t = np.array(e["from"], float), np.array(e["to"], float)
    pts = np.array([[(f, t)[i][0], (f, t)[j][1], (f, t)[k][2]] for i in (0, 1) for j in (0, 1) for k in (0, 1)])
    return transform(e)(pts)


def box_axes(e):
    r = e.get("rotation")
    if not r or not r.get("angle"):
        return [AXES["x"], AXES["y"], AXES["z"]]
    m = rot_matrix(r["axis"], r["angle"])
    return [m @ AXES[a] for a in "xyz"]


def overlap_depth(ca, cb, axa, axb):
    """Separating-axis test on the two corner sets; returns the smallest penetration (<= EPS means apart)."""
    tests = list(axa) + list(axb)
    for u in axa:
        for v in axb:
            w = np.cross(u, v)
            n = np.linalg.norm(w)
            if n > 1e-6:
                tests.append(w / n)
    depth = math.inf
    for ax in tests:
        pa, pb = ca @ ax, cb @ ax
        d = min(pa.max(), pb.max()) - max(pa.min(), pb.min())
        depth = min(depth, d)
        if depth <= EPS:
            return depth
    return depth


def faces(e):
    """(name, 4 corners, outward normal) of every face the element draws."""
    f, t = np.array(e["from"], float), np.array(e["to"], float)
    tr = transform(e)
    r = e.get("rotation")
    m = rot_matrix(r["axis"], r["angle"]) if r and r.get("angle") else np.eye(3)
    out = []
    for name in e.get("faces", {}):
        ax, end = FACES[name]
        o1, o2 = [i for i in range(3) if i != ax]
        quad = []
        for a, b in ((0, 0), (1, 0), (1, 1), (0, 1)):
            p = np.zeros(3)
            p[ax] = (f, t)[end][ax]
            p[o1] = (f, t)[a][o1]
            p[o2] = (f, t)[b][o2]
            quad.append(p)
        n = np.zeros(3)
        n[ax] = 1 if end else -1
        out.append((name, tr(np.array(quad)), m @ n))
    return out


def clip(subject, clipper):
    """Sutherland-Hodgman: the part of convex polygon subject inside convex polygon clipper (2-D, any winding)."""
    def area2(poly):
        return sum(poly[i - 1][0] * poly[i][1] - poly[i][0] * poly[i - 1][1] for i in range(len(poly)))
    sign = 1 if area2(clipper) > 0 else -1
    out = list(subject)
    for i in range(len(clipper)):
        a, b = clipper[i - 1], clipper[i]
        inp, out = out, []
        if not inp:
            break

        def inside(p):
            return sign * ((b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])) >= -1e-9

        def cross(p, q):
            d1 = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
            d2 = (b[0] - a[0]) * (q[1] - a[1]) - (b[1] - a[1]) * (q[0] - a[0])
            s = d1 / (d1 - d2)
            return (p[0] + s * (q[0] - p[0]), p[1] + s * (q[1] - p[1]))
        for j in range(len(inp)):
            p, q = inp[j - 1], inp[j]
            if inside(q):
                if not inside(p):
                    out.append(cross(p, q))
                out.append(q)
            elif inside(p):
                out.append(cross(p, q))
    return abs(area2(out)) / 2 if len(out) >= 3 else 0.0


def face_overlap(fa, fb):
    """(kind, area) when the two faces lie in one plane and overlap, else None."""
    _, qa, na = fa
    _, qb, nb = fb
    dot = float(na @ nb)
    if abs(dot) < 1 - 1e-6 or abs(float(na @ (qb[0] - qa[0]))) > EPS:
        return None
    u = qa[1] - qa[0]
    u = u / np.linalg.norm(u)
    v = np.cross(na, u)
    a2 = [(float(p @ u), float(p @ v)) for p in qa]
    b2 = [(float(p @ u), float(p @ v)) for p in qb]
    area = clip(a2, b2)
    if area < AREA:
        return None
    return ("zfight" if dot > 0 else "touching"), area


def elements_of(path, seen=0):
    d = json.load(open(path))
    if "elements" in d:
        return d["elements"]
    p = d.get("parent", "")
    if p.startswith("mimcontent:") and seen < 8:
        sub = os.path.join(MODELS, p.split(":", 1)[1] + ".json")
        if os.path.exists(sub):
            return elements_of(sub, seen + 1)
    return []


def check(path):
    els = elements_of(path)
    cs = [corners(e) for e in els]
    axs = [box_axes(e) for e in els]
    fs = [faces(e) for e in els]
    found = {"overlap": [], "zfight": [], "touching": []}
    for i in range(len(els)):
        for j in range(i + 1, len(els)):
            d = overlap_depth(cs[i], cs[j], axs[i], axs[j])
            if d > EPS:
                found["overlap"].append((i, j, round(d, 3)))
            for fa in fs[i]:
                for fb in fs[j]:
                    r = face_overlap(fa, fb)
                    if r:
                        found[r[0]].append((i, j, fa[0], fb[0], round(r[1], 3)))
    return els, found


def main(args):
    paths = args or sorted(glob.glob(os.path.join(MODELS, "block", "**", "*.json"), recursive=True))
    bad = 0
    for p in paths:
        els, found = check(p)
        rel = os.path.relpath(p, MODELS)
        if found["overlap"] or found["zfight"]:
            bad += 1
            print(f"{rel}: {len(els)} elements, {len(found['overlap'])} overlapping pairs, "
                  f"{len(found['zfight'])} z-fighting face pairs ({len(found['touching'])} hidden touching)")
            for i, j, d in found["overlap"][:6]:
                print(f"   overlap  #{i} {els[i]['from']}..{els[i]['to']}  x  #{j} {els[j]['from']}..{els[j]['to']}  depth {d}")
            for i, j, a, b, ar in found["zfight"][:6]:
                print(f"   zfight   #{i}.{a}  x  #{j}.{b}  area {ar}")
        else:
            print(f"{rel}: ok ({len(els)} elements, {len(found['touching'])} hidden touching)")
    print(f"\n{bad} of {len(paths)} block models flagged")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
