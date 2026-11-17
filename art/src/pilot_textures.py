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
CRUST = ramp("#7a4a22", "#9a6430", "#b47c3c", "#c99a52", "#d8ad60", "#e0b870")
CRACK = hexrgb("#7a4a22")
FLOUR = hexrgb("#ead9b0")
BREAD_EDGE = hexrgb("#6b4420")
PASTRY = ramp("#8a5019", "#a86624", "#c4802e", "#dca050", "#e4ae5c", "#eabb6a")
LAYER = hexrgb("#9a561a")
PASTRY_EDGE = hexrgb("#55300e")
RICOTTA = ramp("#d4c7a6", "#e8dcc0")
CHEESE = ramp("#a39a7e", "#b8b094", "#cfc6a6", "#ddd6bc", "#e6e0c8", "#ece6cf")
BASKET_DOT = hexrgb("#c2b68e")
GROOVE = hexrgb("#a39670")  # r4: darker rib shadows
CHEESE_SHADOW = hexrgb("#4a4432")  # r4: bottom/right outline, stands off the slot grey
CHEESE_EDGE = hexrgb("#59513a")  # r5: top/left outline (8a8166 matched the slot grey)
# limestone: greyer honey, few colours, so it stands apart from sandstone
LIMESTONE = ramp("#8f8772", "#a39a82", "#b2a88f", "#bdb39a", "#cfc6ad")
PIT = hexrgb("#9d947c")
INNER = ramp("#5e574a", "#6f675a", "#7f776a")
SOOT = ramp("#1f1b17", "#2f2822", "#433930")
ASH = ramp("#3a3631", "#57524b", "#77726a")
EMBER = ramp("#a12a0a", "#e0651a", "#ffb43a")
CLAY = ramp("#874a33", "#94523a", "#a0583a", "#ab6446")
CLAY_LINE = hexrgb("#6e3a26")
LIME = hexrgb("#b07a5c")
SAUCE = ramp("#4a1f12", "#5c2a18")
TOMATO = hexrgb("#8e3a22")
POT_INSIDE = ramp("#4a2a1e", "#5a3424")
MEAT = ramp("#7a4a32", "#93604a")
PEA = hexrgb("#6f8f3a")


def bread():
    """Ħobż tal-Malti: a round dome loaf 13 wide x 11 tall, flat underneath, golden-tan, thin crackle lines."""
    c = Canvas()
    cx, base, rx, ry = 8.0, 13.0, 7.0, 10.0
    m = np.zeros((N, N), dtype=bool)
    for y in range(N):
        for x in range(N):
            u, v = (x + 0.5 - cx) / rx, (y + 0.5 - base) / ry
            m[y, x] = (u * u + v * v <= 1.0 and y < base) or (y == base and abs(x + 0.5 - cx) <= rx - 1.0)
    light = shade_dome(m, cx, base - 4.0, rx, 7.0, height=1.0)
    for y in range(N):
        for x in range(N):
            if m[y, x]:
                c.set(x, y, pick(CRUST, 0.3 + light[y, x] * 0.7 + (hash01(x, y, 3) - 0.5) * 0.12))
    # three single-pixel diagonal crackle lines, each with one flour pixel on its upper edge
    for line in (((5, 7), (6, 6)), ((11, 9), (12, 8)), ((8, 10), (9, 9))):
        for (x, y) in line:
            if m[y, x]:
                c.set(x, y, CRACK)
    c.set(6, 5, CRUST[5])  # one flour-dust highlight above the first crack
    outline(c, BREAD_EDGE)
    # rounded base: drop the corner pixels of the bottom row, a one-shade shadow row above it
    xs = [x for x in range(N) if c.opaque(x, int(base))]
    if xs:
        c.set(xs[0], int(base), (0, 0, 0), a=0)
        c.set(xs[-1], int(base), (0, 0, 0), a=0)
        for x in range(xs[0] + 2, xs[-1] - 1):
            c.set(x, int(base) - 1, CRUST[1])
    outline(c, BREAD_EDGE)
    return c


def pastizz():
    """Pastizz tal-irkotta: a fat shell with blunt tips, the right one curling up, a spiral from the left tip,
    a continuous ricotta seam along the top ridge."""
    c = Canvas()
    m = np.zeros((N, N), dtype=bool)
    mid = lambda x: 9.4 - max(0.0, x - 7) * 0.42
    for y in range(N):
        for x in range(1, 15):
            d = abs(x + 0.5 - 8) / 7.5
            half = max(1.0, 4.6 * max(0.0, 1 - d) ** 0.6)
            m[y, x] = abs(y + 0.5 - mid(x)) <= half and y <= 12
    light = shade_dome(m, 8, 8.5, 6.5, 4.5, height=0.8)
    for y in range(N):
        for x in range(N):
            if m[y, x]:
                c.set(x, y, pick(PASTRY, 0.3 + light[y, x] * 0.6 + (hash01(x, y, 11) - 0.5) * 0.1))
    for (x, y) in ((3, 10), (4, 9), (5, 8), (4, 11), (5, 10), (6, 9), (7, 8)):  # layer arcs curling from the left tip
        if m[y, x]:
            c.set(x, y, LAYER)
    for x in range(3, 13):  # the seam: one pixel under the top edge, all along the ridge
        ys = [y for y in range(N) if m[y, x]]
        if ys:
            c.set(x, ys[0] + 1, RICOTTA[1])
    outline(c, PASTRY_EDGE)
    return c


def gbejna(top_cy=5.0, bot_cy=9.5, rx=5.6, top_ry=2.5):
    """Ġbejna in 3/4 view: a real top with a ring of basket dots, a short side with ridges.
    v3 (2026-11-17): moved down and widened a little (see GBEJNA_V3) so it sits in the hotbar like vanilla foods."""
    c = Canvas()
    cx = 8.0
    top = ellipse_mask(cx, top_cy, rx, top_ry)
    bottom = ellipse_mask(cx, bot_cy, rx, top_ry)
    for y in range(N):
        for x in range(N):
            inside_side = abs(x + 0.5 - cx) <= rx and top_cy <= y + 0.5 <= bot_cy
            if (bottom[y, x] or inside_side) and not top[y, x]:
                t = 0.65 - (x + 0.5 - (cx - rx)) / (2 * rx) * 0.45
                c.set(x, y, pick(CHEESE, t + 0.1) if x % 2 == 0 else GROOVE)
            elif top[y, x]:
                d = math.hypot((x + 0.5 - cx) / rx, (y + 0.5 - top_cy) / top_ry)
                c.set(x, y, pick(CHEESE, 0.95 - d * 0.25))
                if 0.6 < d < 0.85 and (x + y) % 2 == 0 and y >= top_cy:
                    c.set(x, y, BASKET_DOT)
    dy = round(top_cy - 5.0)  # the hand-placed details below were set for top_cy = 5
    for (x, y) in ((5, 5 + dy), (8, 5 + dy), (10, 5 + dy)):
        if top[y, x]:
            c.set(x, y, CHEESE[2])
    outline(c, CHEESE_EDGE)
    ry0 = int(math.floor(top_cy - top_ry)) + 2  # r4: a lighter row just inside the top rim, so the top reads domed
    for x in range(4, 12):
        if c.opaque(x, ry0) and tuple(c.get(x, ry0)) != CHEESE_EDGE and top[ry0, x]:
            c.set(x, ry0, CHEESE[2])
    for x in range(6, 10):  # r5: basket imprint on the top: a light ring and a dimple
        c.set(x, 5 + dy, CHEESE[2])
    for x in (7, 8):
        c.set(x, 6 + dy, BASKET_DOT)
    for y in range(N):  # a darker edge on the shadow side (bottom and right) for contrast at hotbar size
        for x in range(N):
            if c.opaque(x, y) and (not c.opaque(x, y + 1) or not c.opaque(x + 1, y)) and y >= 8 + dy:
                c.set(x, y, CHEESE_SHADOW)
    return c


def limestone(seed, flecks=True):
    """Globigerina limestone, worked by hand: few colours, soft mottling, a few chisel marks."""
    c = Canvas()
    for y in range(N):
        for x in range(N):
            t = 0.62 + (tile_noise(x, y, 4, seed) - 0.5) * 0.7 + (hash01(x, y, seed) - 0.5) * 0.2
            c.set(x, y, pick(LIMESTONE, t))
    for i in range(5):  # a few darker pits
        c.set(int(hash01(i, 9, seed) * 16), int(hash01(i, 10, seed) * 16), PIT)
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
    """Front face: limestone with a symmetric soot rim around the arched mouth (model x 5..11, y 3..7 ->
    u 5..11, v 9..13), darkest at the mouth and fading upwards; a little ash spill under it."""
    c = limestone(23)
    for y in range(N):
        for x in range(N):
            in_mouth = 5 <= x < 11 and 9 <= y < 13
            if in_mouth:
                c.set(x, y, SOOT[1])
                continue
            if 4 <= x < 12 and 8 <= y < 14:
                c.set(x, y, SOOT[2])
            elif y == 7 and 4 <= x < 12:
                c.set(x, y, INNER[1])
            elif y == 6 and 5 <= x < 11:
                c.set(x, y, LIMESTONE[0])
    return c


def kenur_inner():
    """Inside walls: smoke-stained limestone, darker but not black, so the cradle reads from above."""
    c = Canvas()
    for y in range(N):
        for x in range(N):
            c.set(x, y, pick(INNER, tile_noise(x, y, 4, 33) + (hash01(x, y, 34) - 0.5) * 0.4))
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
    """The borma: plain mottled terracotta, one incised line under the rim, two clay-toned flecks."""
    c = Canvas()
    for y in range(N):
        for x in range(N):
            c.set(x, y, pick(CLAY, 0.5 + (tile_noise(x, y, 4, 51) - 0.5) * 0.8 + (hash01(x, y, 52) - 0.5) * 0.2))
    for x in range(N):
        c.set(x, 7, CLAY_LINE)  # model y 8..9, just under the shoulder
    for (x, y) in ((4, 11), (12, 13)):
        c.set(x, y, LIME)
    return c


def borma_top(contents):
    """Looking into the pot: the interior (model x/z 4..12) is dark, or the stuffat."""
    c = clay_side()
    for y in range(4, 12):
        for x in range(4, 12):
            if contents == "empty":
                c.set(x, y, POT_INSIDE[0] if math.hypot(x + 0.5 - 8, y + 0.5 - 8) < 2.5 else POT_INSIDE[1])
            else:
                c.set(x, y, SAUCE[1] if hash01(x, y, 61) > 0.4 else SAUCE[0])
    if contents == "stuffat":
        for (x0, y0) in ((5, 5), (9, 7), (5, 9)):  # rabbit pieces, 2x2 with a highlight
            for dx in (0, 1):
                for dy in (0, 1):
                    c.set(x0 + dx, y0 + dy, MEAT[1] if (dx, dy) == (0, 0) else MEAT[0])
        c.set(8, 5, TOMATO)
        c.set(9, 10, PEA)
        c.set(7, 8, PEA)
    return c


# v3 placement: vanilla food bounding boxes centre on rows 7.5-9 (bread 8.0, cookie 7.5, baked potato 8.5,
# egg 8.0, pumpkin pie 9.0) and end on rows 13-15; v2 sat on rows 3-11 (centre 7.0), too high in the hotbar.
# r5: one row lower again, rows 5-13, so its bottom lines up with the pastizzi and the ħobż (row 13)
GBEJNA_V3 = dict(top_cy=7.3, bot_cy=11.6, rx=6.0, top_ry=2.6)


def main():
    out = {
        # hobz_malti and pastizz_irkotta are now made by art/src/food_items.py (v3); bread()/pastizz() kept for history
        # item/gbejna is now made by food_items.gbejna_v6 (r6); gbejna() kept for history
        "block/kenur_side": kenur_side(),
        "block/kenur_top": kenur_top(),
        "block/kenur_front": kenur_front(),
        "block/kenur_inner": kenur_inner(),
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
