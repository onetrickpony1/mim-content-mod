"""Torta tal-lampuki item icon, drawn the vanilla cake way (top-and-front view).

A round double-crust pie in a shallow round terracotta dish, seen from above and in front:
the golden top is a wide oval band with a crimped rim, below it a thin golden-brown crust edge,
then the terracotta dish wall curving round. Colours follow the accepted placed model
(textures/block/torta_lampuki_top/plate/side.png).

Run:  art/.venv/bin/python art/src/torta_icon_cake.py
Out:  the picked icon into the mod (textures/item/torta_lampuki.png), plus art/candidates/torta_cake_a.png, _b.png, _c.png
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "art", "candidates")

# pastry (from torta_lampuki_top / _side)
P_HI = (244, 204, 122)
P_LT = (232, 182, 92)
P_MD = (220, 160, 68)
P_SH = (196, 132, 50)
P_DK = (164, 104, 42)
P_OL = (140, 86, 36)     # pastry outline / vent
SES = (250, 232, 184)    # sesame
# terracotta dish (from torta_lampuki_plate)
D_LT = (204, 134, 92)
D_MD = (172, 106, 70)
D_SH = (136, 80, 54)
D_DK = (108, 60, 40)
D_OL = (92, 50, 32)      # dish outline


def inside(x, y, cx, cy, rx, ry):
    dx = (x + 0.5 - cx) / rx
    dy = (y + 0.5 - cy) / ry
    return dx * dx + dy * dy <= 1.0


def cyl(x, y, cx, cy, rx, ry, h):
    """Pixel is in the silhouette of an upright cylinder (top ellipse at cy, height h)."""
    if inside(x, y, cx, cy, rx, ry) or inside(x, y, cx, cy + h, rx, ry):
        return True
    return abs(x + 0.5 - cx) <= rx and cy <= y + 0.5 <= cy + h


def h2(x, y, s):
    return ((x * 73856093) ^ (y * 19349663) ^ (s * 83492791)) & 0xFF


def draw(dish_top, dish_ry, dish_h, crust_top, crust_rx, crust_ry, crust_h, vent, sesame, seed, speck=28):
    g = [[None] * 16 for _ in range(16)]
    kind = [[None] * 16 for _ in range(16)]
    cx = 8.0
    # 1. dish
    for y in range(16):
        for x in range(16):
            if not cyl(x, y, cx, dish_top, 8.0, dish_ry, dish_h):
                continue
            if inside(x, y, cx, dish_top, 8.0, dish_ry):
                # dish rim (top face), lit top-left
                t = (x - 8) * 0.6 + (y - dish_top) * 0.8
                g[y][x] = D_LT if t < 1 else D_MD
            else:
                # wall: light on the left, dark on the right
                t = x / 15.0
                if inside(x, y - 1, cx, dish_top, 8.0, dish_ry):
                    g[y][x] = D_SH if t < 0.7 else D_DK  # shadow under the rim lip
                else:
                    g[y][x] = D_LT if t < 0.3 else (D_MD if t < 0.75 else D_SH)
            kind[y][x] = "d"
    # 2. crust edge (side band) and top
    for y in range(16):
        for x in range(16):
            if not cyl(x, y, cx, crust_top, crust_rx, crust_ry, crust_h):
                continue
            kind[y][x] = "p"
            if inside(x, y, cx, crust_top, crust_rx, crust_ry):
                # rim ring: crimps along the outer edge of the top
                inner = inside(x, y, cx, crust_top, crust_rx - 1.15, crust_ry - 1.0)
                light = (x - 8) * 0.55 + (y - crust_top) * 0.9  # negative = top-left
                if not inner:
                    # crimp: alternate light/dark along the rim
                    on = (x + y) % 2 == 0
                    if light < 0:
                        c = P_HI if on else P_MD
                    else:
                        c = P_MD if on else P_DK
                    g[y][x] = c
                else:
                    c = P_LT if light < -1.0 else (P_MD if light < 2.0 else P_SH)
                    r = h2(x, y, seed)
                    if r < speck:  # matte speckle: one step darker
                        c = {P_LT: P_MD, P_MD: P_SH, P_SH: P_DK}[c]
                    elif r > 245 and c != P_LT:
                        c = P_LT
                    g[y][x] = c
            else:
                # crust edge below the top: golden brown, darker right
                g[y][x] = P_SH if x < 9 else P_DK
    # 3. vent slits and sesame
    for (x, y) in vent:
        g[y][x] = P_OL
    for (x, y) in sesame:
        g[y][x] = SES
    # 4. outline: opaque pixels next to transparency, and a seam between crust and dish
    out = [row[:] for row in g]
    for y in range(16):
        for x in range(16):
            if g[y][x] is None:
                continue
            nb = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            edge = any(not (0 <= a < 16 and 0 <= b < 16) or g[b][a] is None for a, b in nb)
            if edge:
                out[y][x] = P_OL if kind[y][x] == "p" else D_OL
            elif kind[y][x] == "p" and y + 1 < 16 and kind[y + 1][x] == "d" and not inside(
                x, y, cx, crust_top, crust_rx, crust_ry
            ):
                out[y][x] = P_OL  # bottom of the crust edge meets the dish
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y in range(16):
        for x in range(16):
            if out[y][x] is not None:
                im.putpixel((x, y), out[y][x] + (255,))
    return im


VARIANTS = {
    # a: shallow dish with a terracotta rim showing all round, domed crust, one cross vent
    "a": dict(dish_top=6.4, dish_ry=4.6, dish_h=2.4, crust_top=5.2, crust_rx=6.2, crust_ry=3.5, crust_h=1.2,
              vent=[(7, 5), (8, 5), (9, 5), (8, 4), (8, 6)], sesame=[(5, 4), (11, 4), (5, 7), (11, 7)], seed=3),
    # b: cake proportions (top ~7 rows, side ~6), thicker crust edge, two slit vents
    "b": dict(dish_top=6.2, dish_ry=4.8, dish_h=2.6, crust_top=4.8, crust_rx=6.4, crust_ry=3.6, crust_h=1.8,
              vent=[(6, 4), (7, 4), (9, 5), (10, 5)], sesame=[(5, 5), (11, 3), (7, 7), (11, 6)], seed=5),
    # c: crust nearly fills the dish (narrow rim), dish shows mostly as the wall
    "c": dict(dish_top=6.2, dish_ry=4.7, dish_h=2.6, crust_top=5.4, crust_rx=6.9, crust_ry=4.0, crust_h=1.2,
              vent=[(7, 5), (8, 5), (8, 4), (9, 5)], sesame=[(5, 5), (10, 3), (11, 7), (5, 8)], seed=7),
}


def compare(cands):
    """Each candidate beside vanilla cake / pumpkin pie and the mod's oven dishes, 1x/2x/8x on slot grey."""
    import sys
    sys.path.insert(0, os.path.join(ROOT, "art", "tools"))
    from font import label_font
    from PIL import ImageDraw

    item = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
    van = os.path.join(ROOT, "art", ".vanilla", "item")
    refs = [("cake", os.path.join(van, "cake.png")), ("pumpkin_pie", os.path.join(van, "pumpkin_pie.png")),
            ("ross_il_forn", os.path.join(item, "ross_il_forn.png")),
            ("imqarrun_il_forn", os.path.join(item, "imqarrun_il_forn.png")),
            ("timpana", os.path.join(item, "timpana.png"))]
    icons = [(f"torta_cake_{k}", im) for k, im in cands] + [(n, Image.open(p).convert("RGBA")) for n, p in refs]
    grey, cell = (139, 139, 139, 255), 150
    font = label_font(13)
    W, H = cell * len(icons) + 20, 20 + 128 + 60 + 24 + 120
    sheet = Image.new("RGBA", (W, H), grey)
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(icons):
        x = 10 + i * cell
        d.text((x, 2), name, font=font, fill=(20, 20, 20, 255))
        big = im.resize((128, 128), Image.NEAREST)
        sheet.alpha_composite(big, (x, 20))
        sheet.alpha_composite(im, (x, 160))
        sheet.alpha_composite(im.resize((32, 32), Image.NEAREST), (x + 30, 160))
    # hotbar-like row of 1x icons (20 px slots, as in the game at GUI scale 1)
    y = 230
    d.text((10, y - 2), "hotbar 1x", font=font, fill=(20, 20, 20, 255))
    for row, scale in ((0, 1), (1, 2)):
        yy = y + 18 + row * 44
        for i, (_, im) in enumerate(icons):
            s = 20 * scale
            x = 10 + i * (s + 2)
            d.rectangle([x, yy, x + s + 1, yy + s + 1], fill=(55, 55, 55, 255))
            d.rectangle([x + 1, yy + 1, x + s, yy + s], fill=grey)
            ic = im if scale == 1 else im.resize((32, 32), Image.NEAREST)
            sheet.alpha_composite(ic, (x + 1 + 2 * scale, yy + 1 + 2 * scale))
    sheet.save(os.path.join(OUT, "torta_cake_compare.png"))
    print("wrote torta_cake_compare.png")


PICK = "c"  # owner 2026-11-17: "lets go with torta cake c"
ICON = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item", "torta_lampuki.png")


def main():
    os.makedirs(OUT, exist_ok=True)
    draw(**VARIANTS[PICK]).save(ICON)
    print("installed", PICK, "as textures/item/torta_lampuki.png")
    cands = []
    for k, v in VARIANTS.items():
        im = draw(**v)
        im.save(os.path.join(OUT, f"torta_cake_{k}.png"))
        cands.append((k, im))
        print("wrote", f"torta_cake_{k}.png")
    compare(cands)


if __name__ == "__main__":
    main()
