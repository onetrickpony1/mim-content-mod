"""Qagħqa tal-Appostli item icon (candidates, 2026-11-17).

The apostles' ring: a large Holy Week bread ring. From the owner's photos in art/references/qaghqa_appostli_owner/
(reference only, never traced): a thick, glossy, golden-orange egg-washed ring with a smallish hole, whole dark
brown almonds pressed into the top all the way round, and pale sesame scattered over it.

It must read apart from the two other rings in the mod:
- qagħaq tal-għasel (accepted): a thin pale pastry ring with a big hole and near-black treacle slits;
- qagħaq tal-ħmira: a smaller everyday sesame ring.
So this one is the biggest (full icon width), the thickest, the warmest and the only one with almonds.

Run:  art/.venv/bin/python art/src/qaghqa_appostli.py
Writes art/candidates/qaghqa_appostli_{a,b,c}.png and art/candidates/qaghqa_appostli_compare.png, and installs the
PICK as mod/.../textures/item/qaghqa_appostli.png. Deterministic: a rerun is byte-identical.
"""
import math
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import food_items as F  # noqa: E402  (shared: hx, render, outline3, check, compare, paths)
from measure import measure  # noqa: E402

hx = F.hx

# glossy golden-orange egg-washed crust, dark brown almonds, pale sesame
PAL = {"o": hx("#94561c"), "O": hx("#703a12"),
       "h": hx("#f4c46a"), "l": hx("#e4a24a"), "m": hx("#cc8434"), "d": hx("#a86424"), "D": hx("#84481a"),
       "a": hx("#4a2410"), "A": hx("#74401c"),                      # almond, its lit end
       "s": hx("#f8e6b4")}                                          # sesame
PICK = "b"


def shade(k):
    return "h" if k > 0.62 else "l" if k > 0.25 else "m" if k > -0.15 else "d" if k > -0.55 else "D"


def hash01(x, y, seed):
    v = math.sin(x * 127.1 + y * 311.7 + seed * 74.7) * 43758.5453
    return v - math.floor(v)


def ring(cx, cy, rx, ry, hole, depth):
    """A thick bread ring (torus shading lit from the top left); with depth > 0 a low side shows below the front and
    the far inner wall shows through the hole. Returns the grid and the zone of each pixel."""
    g = [["."] * 16 for _ in range(16)]
    zone = [[None] * 16 for _ in range(16)]
    mid, half = (1 + hole) / 2, (1 - hole) / 2
    for y in range(16):
        for x in range(16):
            u, v = (x + .5 - cx) / rx, (y + .5 - cy) / ry
            r = math.hypot(u, v)
            if hole < r <= 1:
                zone[y][x] = "top"
                s = (r - mid) / half
                nx, ny = (u / r) * s, (v / r) * s
                k = 0.6 * math.sqrt(max(0, 1 - s * s)) - 0.6 * nx - 0.6 * ny - 0.12
                g[y][x] = shade(k)
            elif depth and v > 0 and r > 1 and any(
                    math.hypot(u, (y + .5 - j - cy) / ry) <= 1 for j in range(1, depth + 1)):
                zone[y][x] = "side"
                g[y][x] = "d" if x + .5 < cx - 2 else "D"
            elif depth and r <= hole and v < 0 and math.hypot(u, (y + .5 - 1 - cy) / ry) > hole:   # 1 px of far wall
                zone[y][x] = "wall"
                g[y][x] = "D"
    return g, zone


def finish(g):
    e = F.outline3(g)
    for y in range(16):
        for x in range(16):
            if e[y][x] == "#" and g[y][x] != ".":
                g[y][x] = "o" if x + y < 15 else "O"
    return g


def almonds(g, zone, cx, cy, rx, ry, hole, angles, radial=False):
    """Whole almonds pressed into the top along the ring's middle: two pixels each, dark, the end nearer the light a
    shade lighter. Tangential by default (as most lie in the photos); radial=True turns them across the ring."""
    mid = (1 + hole) / 2
    for th in angles:
        t = math.radians(th)
        px, py = cx + mid * rx * math.cos(t), cy + mid * ry * math.sin(t)
        tx, ty = (-math.sin(t), math.cos(t)) if not radial else (math.cos(t), math.sin(t))
        x0, y0 = int(math.floor(px)), int(math.floor(py))
        sx, sy = round(tx), round(ty)
        if sx == 0 and sy == 0:
            sx = 1
        pts = [(x0, y0), (x0 + sx, y0 + sy)]
        pts.sort(key=lambda p: p[0] + p[1])            # nearer the top left first
        for i, (x, y) in enumerate(pts):
            if 0 <= x < 16 and 0 <= y < 16 and zone[y][x] == "top":
                g[y][x] = "A" if i == 0 else "a"


def sesame(g, zone, seed, rate):
    for y in range(16):
        for x in range(16):
            if zone[y][x] != "top" or g[y][x] not in "lm":
                continue
            near = any(0 <= x + dx < 16 and 0 <= y + dy < 16 and g[y + dy][x + dx] in "aAs"
                       for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)))
            if not near and hash01(x, y, seed) < rate:
                g[y][x] = "s"


def make(cx, cy, rx, ry, hole, depth, n, start, radial=False, seed=3, rate=0.16):
    g, zone = ring(cx, cy, rx, ry, hole, depth)
    almonds(g, zone, cx, cy, rx, ry, hole, [start + i * 360 / n for i in range(n)], radial)
    g = finish(g)
    zone = [[zone[y][x] if g[y][x] not in "oO" else None for x in range(16)] for y in range(16)]
    sesame(g, zone, seed, rate)
    return ["".join(r) for r in g]


def cand_a():
    """Seen from above, barely tilted (as the owner's first photo): a full-width thick ring, eight almonds."""
    return make(8.0, 8.0, 7.6, 7.0, 0.34, 0, 8, 22.5)


def cand_b():
    """Three-quarter view: the ring as a wide ellipse with a low baked side and the far inner wall in the hole,
    seven almonds lying along the ring."""
    return make(8.0, 7.0, 7.6, 5.8, 0.34, 2, 7, 10, seed=3, rate=0.2)


def cand_c():
    """As b, but the almonds lie across the ring (as some do in the photos) and more sesame."""
    return make(8.0, 7.0, 7.6, 5.8, 0.34, 2, 8, 0, radial=True, seed=7, rate=0.22)


CANDS = (("a", cand_a), ("b", cand_b), ("c", cand_c))


def vcentre(im):
    ys = [y for y in range(16) for x in range(16) if im.getpixel((x, y))[3]]
    return (min(ys) + max(ys)) / 2


def main():
    os.makedirs(F.OUT, exist_ok=True)
    ims = []
    for k, make_fn in CANDS:
        rows = make_fn()
        name = "qaghqa_appostli_" + k
        F.check(name, rows)
        im = F.render(rows, PAL)
        p = os.path.join(F.OUT, name + ".png")
        im.save(p)
        m = measure(p)
        print(name, {q: m[q] for q in ("coverage", "colours", "lmin", "lmax", "edge_l", "interior_l", "tl_minus_br")},
              "outline/inside", round(m["edge_l"] / m["interior_l"], 2), "vcentre", vcentre(im))
        ims.append(("Qagħqa tal-Appostli " + k, im))
        if k == PICK:
            im.save(os.path.join(F.MOD_ITEMS, "qaghqa_appostli.png"))
    for lbl, f in (("Qagħaq tal-għasel", "qaghaq_ghasel"), ("Ħobż", "hobz_malti")):
        ims.append((lbl, Image.open(os.path.join(F.MOD_ITEMS, f + ".png")).convert("RGBA")))
    for v in ("bread", "cookie"):
        ims.append(("vanilla " + v, Image.open(os.path.join(F.VANILLA, v + ".png")).convert("RGBA")))
    F.compare(ims).save(os.path.join(F.OUT, "qaghqa_appostli_compare.png"))


if __name__ == "__main__":
    main()
