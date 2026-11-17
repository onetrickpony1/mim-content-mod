"""Art pilot textures (2026-11-17): ħobż tal-Malti, pastizz tal-irkotta, ġbejna, the kenur, the borma.

References: art/references/ (photos, licences in SOURCES.tsv). Style numbers: art/STYLE.md.
Run: art/.venv/bin/python art/src/pilot_textures.py
"""
import math
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from pixel import N, Canvas, ramp, hash01, tile_noise, smooth_noise, shade_dome, pick, outline, ellipse_mask, hexrgb

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
TEX = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
os.makedirs(os.path.join(TEX, "block"), exist_ok=True)
os.makedirs(os.path.join(TEX, "item"), exist_ok=True)

# --- palettes (dark -> light), from the reference photos, kept inside vanilla's ranges (art/STYLE.md) ---
# review r1: crust golden-tan not red; outlines ~0.25-0.3 luminance; brightest pixel <= ~0.85
CRUST = ramp("#5e3416", "#7a4620", "#8e5524", "#a86a2e", "#c88a40", "#d9a457")
CRACK = hexrgb("#6a3a14")
FLOUR = hexrgb("#e2cf9f")
BREAD_EDGE = hexrgb("#4a2a12")
PASTRY = ramp("#7c4615", "#9a5a1c", "#b87426", "#d08e36", "#e0a64e", "#e8b860")
LAYER = hexrgb("#9a561a")
PASTRY_EDGE = hexrgb("#55300e")
RICOTTA = ramp("#d4c7a6", "#e8dcc0")
CHEESE = ramp("#8f8566", "#a89d78", "#c2b68e", "#d6cba2", "#ddd2a9", "#e4d9b0")
CHEESE_EDGE = hexrgb("#6e6548")
# limestone: greyer honey, few colours, so it stands apart from sandstone
LIMESTONE = ramp("#a59a80", "#bdb08f", "#cbbd98", "#d6c69c", "#ddd0aa")
SOOT = ramp("#1f1b17", "#2f2822", "#433930")
ASH = ramp("#3a3631", "#57524b", "#77726a")
EMBER = ramp("#a12a0a", "#e0651a", "#ffb43a")
CLAY = ramp("#6b3423", "#7c3d29", "#8a452e", "#985034")
CLAY_LINE = hexrgb("#55291b")
LIME = hexrgb("#b99a80")
SAUCE = ramp("#50200f", "#6e2a1a", "#7d321e")
MEAT = ramp("#5c3420", "#7a4a30")
PEA = hexrgb("#5f7f2c")


def bread():
    """Ħobż tal-Malti: a tall round dome loaf, flat underneath, golden crust with dark crackle lines."""
    c = Canvas()
    cx, base, rx, ry = 8.0, 13.0, 6.2, 9.0
    m = np.zeros((N, N), dtype=bool)
    for y in range(N):
        for x in range(N):
            u, v = (x + 0.5 - cx) / rx, (y + 0.5 - base) / ry
            m[y, x] = (u * u + v * v <= 1.0 and y < base) or (abs(x + 0.5 - cx) <= rx - 0.8 and base <= y < base + 1)
    light = shade_dome(m, cx, base - 3.5, rx, 6.5, height=1.0)
    for y in range(N):
        for x in range(N):
            if m[y, x]:
                t = 0.35 + light[y, x] * 0.6 + (hash01(x, y, 3) - 0.5) * 0.14
                if y >= base - 1:
                    t -= 0.3  # the darker bottom crust
                c.set(x, y, pick(CRUST, t))
    # crackle lines, 1 px, with flour only along their upper edge
    cracks = [((4, 8), (6, 7), (7, 7)), ((8, 6), (9, 7), (10, 7), (11, 8)), ((6, 10), (7, 10), (8, 11)), ((10, 10), (11, 11))]
    for line in cracks:
        for (x, y) in line:
            if m[y, x]:
                c.set(x, y, CRACK)
                if m[y - 1, x] and (x + y) % 2 == 0:
                    c.set(x, y - 1, FLOUR)
    outline(c, BREAD_EDGE)
    return c


def pastizz():
    """Pastizz tal-irkotta: flaky diamond, one tip curling up, layer arcs from the tips, ricotta along the top seam."""
    c = Canvas()
    m = np.zeros((N, N), dtype=bool)
    for y in range(N):
        for x in range(N):
            # centre line rises towards the right tip (the curl)
            mid = 9.6 - max(0.0, x - 8) * 0.45
            half = 4.6 * (1 - abs(x + 0.5 - 8) / 7.2) ** 0.75 if abs(x + 0.5 - 8) < 7.2 else 0
            m[y, x] = abs(y + 0.5 - mid) <= half
    light = shade_dome(m, 8, 9, 6.5, 4.5, height=0.8)
    for y in range(N):
        for x in range(N):
            if m[y, x]:
                c.set(x, y, pick(PASTRY, 0.3 + light[y, x] * 0.6 + (hash01(x, y, 11) - 0.5) * 0.1))
    # layer arcs: 1 px darker curves around each tip
    for tip, radii in (((1.0, 9.6), (3.5, 6.0)), ((15.0, 6.0), (3.5, 6.0))):
        for r in radii:
            for y in range(N):
                for x in range(N):
                    if m[y, x]:
                        d = math.hypot(x + 0.5 - tip[0], (y + 0.5 - tip[1]) * 1.5)
                        if abs(d - r) < 0.5:
                            c.set(x, y, LAYER)
    # the ricotta seam along the top ridge, 2-3 px, near the middle
    for x in range(6, 10):
        ys = [y for y in range(N) if m[y, x]]
        if ys:
            c.set(x, ys[0] + 1, RICOTTA[1] if x % 2 else RICOTTA[0])
    outline(c, PASTRY_EDGE)
    return c


def gbejna():
    """Ġbejna in 3/4 view: cream-yellow top with the basket ring, side with alternating basket ridges."""
    c = Canvas()
    cx, rx, ry = 8.0, 5.6, 2.5
    top_y, bot_y = 5.0, 11.0
    top = ellipse_mask(cx, top_y, rx, ry)
    bottom = ellipse_mask(cx, bot_y, rx, ry)
    body = np.zeros((N, N), dtype=bool)
    for y in range(N):
        for x in range(N):
            body[y, x] = bottom[y, x] or (abs(x + 0.5 - cx) <= rx and top_y <= y + 0.5 <= bot_y)
    for y in range(N):
        for x in range(N):
            if body[y, x] and not top[y, x]:
                t = 0.7 - (x + 0.5 - (cx - rx)) / (2 * rx) * 0.45
                t += 0.14 if x % 2 == 0 else -0.08  # ridges: >= 0.1 luminance apart
                c.set(x, y, pick(CHEESE, t))
            elif top[y, x]:
                d = math.hypot((x + 0.5 - cx) / rx, (y + 0.5 - top_y) / ry)
                t = 1.0 - d * 0.2 - (0.25 if 0.55 < d < 0.8 else 0)
                c.set(x, y, pick(CHEESE, t))
    outline(c, CHEESE_EDGE)
    return c


def limestone(seed, flecks=True):
    """Globigerina limestone, worked by hand: few colours, soft mottling, a few chisel marks."""
    c = Canvas()
    for y in range(N):
        for x in range(N):
            t = 0.62 + (tile_noise(x, y, 4, seed) - 0.5) * 0.7 + (hash01(x, y, seed) - 0.5) * 0.2
            c.set(x, y, pick(LIMESTONE, t))
    if flecks:
        for i in range(5):
            x0, y0 = int(hash01(i, 1, seed) * 14), int(hash01(i, 2, seed) * 15)
            for k in range(2):
                c.set((x0 + k) % N, y0, LIMESTONE[0])
    return c


def kenur_side():
    return limestone(21)


def kenur_top():
    return limestone(22, flecks=False)


def kenur_front():
    """The front: limestone, with hard-edged soot around the mouth (model x 5..11, y 1..6 -> u 5..11, v 10..15)."""
    c = limestone(23)
    for y in range(N):
        for x in range(N):
            d = max(abs(x + 0.5 - 8) / 4.5, (15.5 - (y + 0.5)) / 7.0)
            if d < 0.75:
                c.set(x, y, SOOT[2])
            elif d < 0.95 and (x + y) % 3:
                c.set(x, y, SOOT[2] if d < 0.85 else LIMESTONE[0])
    return c


def soot():
    c = Canvas()
    for y in range(N):
        for x in range(N):
            c.set(x, y, pick(SOOT, tile_noise(x, y, 4, 31) + (hash01(x, y, 32) - 0.5) * 0.4))
    return c


def ash(lit):
    c = Canvas()
    for y in range(N):
        for x in range(N):
            c.set(x, y, pick(ASH, tile_noise(x, y, 4, 41) + (hash01(x, y, 42) - 0.5) * 0.4))
    for i in range(8):
        x0, y0 = int(hash01(i, 3, 43) * 15), int(hash01(i, 4, 43) * 15)
        c.set(x0, y0, SOOT[0])
        c.set(x0 + 1, y0, SOOT[1])
        if lit:
            c.set(x0, y0 + 1, EMBER[i % 3])
    return c


def clay_side():
    """The borma: plain mottled terracotta, one incised line under the rim, a couple of lime flecks."""
    c = Canvas()
    for y in range(N):
        for x in range(N):
            t = 0.5 + (tile_noise(x, y, 4, 51) - 0.5) * 0.8 + (hash01(x, y, 52) - 0.5) * 0.2
            c.set(x, y, pick(CLAY, t))
    for x in range(N):
        c.set(x, 7, CLAY_LINE)  # model y 8..9: just under the rim
    for (x, y) in ((4, 11), (11, 13), (13, 10)):
        c.set(x, y, LIME)
    return c


def borma_top(contents):
    """Looking into the pot: the interior (model x/z 4..12) is dark, or the stuffat."""
    c = clay_side()
    for y in range(4, 12):
        for x in range(4, 12):
            if contents == "empty":
                d = math.hypot(x + 0.5 - 8, y + 0.5 - 8)
                c.set(x, y, pick(SOOT, 1.0 - d * 0.2))
            else:
                c.set(x, y, pick(SAUCE, 0.5 + (hash01(x, y, 61) - 0.5) * 0.9))
    if contents == "stuffat":
        for (x0, y0) in ((5, 5), (9, 6), (6, 9), (9, 9)):  # rabbit pieces, 2x2
            for dx in (0, 1):
                for dy in (0, 1):
                    c.set(x0 + dx, y0 + dy, MEAT[1] if dx == 0 and dy == 0 else MEAT[0])
        for (x, y) in ((8, 5), (5, 8)):  # peas
            c.set(x, y, PEA)
    return c


def main():
    out = {
        "item/hobz_malti": bread(),
        "item/pastizz_irkotta": pastizz(),
        "item/gbejna": gbejna(),
        "block/kenur_side": kenur_side(),
        "block/kenur_top": kenur_top(),
        "block/kenur_front": kenur_front(),
        "block/kenur_soot": soot(),
        "block/kenur_ash": ash(False),
        "block/kenur_ash_lit": ash(True),
        "block/borma_side": clay_side(),
        "block/borma_top_empty": borma_top("empty"),
        "block/borma_top_stuffat": borma_top("stuffat"),
    }
    for name, canvas in out.items():
        canvas.save(os.path.join(TEX, name + ".png"))
        print("wrote", name)


if __name__ == "__main__":
    main()
