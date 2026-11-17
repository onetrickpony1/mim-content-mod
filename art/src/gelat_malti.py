"""The Ġelat Malti item icon (ġelat tan-nanna, "grandma's" ice cream, catalogue D68).

From the owner's picture and recipe in art/references/gelat_malti_owner/ (reference only, never traced, not in git):
three rough, grainy cream scoops heaped in a cream fluted ceramic bowl with a tan rim, speckled with toasted almond
bits (tan-brown), red glacé cherry pieces and a few green ones. The recipe (evaporated milk, sugar, cinnamon, vanilla,
toasted chopped almonds, chopped glacé cherries) gives the scoops a faint warm tint.

The container must read apart from the soups' terracotta bowl (art/src/bowls.py) and the dips' low terracotta dish
(art/src/dip_dish.py) at 1x, and the scoops must read as ice cream (rounded, grainy scoops with an outline each), not as
a dip or ricotta. Candidates:
- a: the owner's picture: a deep cream bowl with vertical flutes and a tan rim, three scoops (one on top);
- b: the same scoops in a smaller cream footed cup on a stem, so the scoops overhang the rim like a coupe;
- c: the scoops in a pale blue-grey glass coupe on a stem (the cold glass of a gelateria), as a colder option.

Writes art/candidates/gelat_malti_{a,b,c}.png and art/candidates/gelat_malti_compare.png (1x, 2x and 8x beside the
accepted sweets, bigilla, aljotta and vanilla items on inventory grey, plus the in-game hotbar crop when
art/candidates/ingame_gelat_malti/ holds the 22-hotbar-gelat shot, saved beside it as 22-hotbar-gelat_crop.png), and
installs candidate PICK as the mod texture item/gelat_malti.png. Re-running gives the same bytes.
Run:  art/.venv/bin/python art/src/gelat_malti.py
"""
import glob
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "art", "tools"))
sys.path.insert(0, HERE)
from font import label_font  # noqa: E402
from measure import measure  # noqa: E402
from food_items import hx, render, check  # noqa: E402
from pixel import shade_dome, hash01  # noqa: E402

ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
VANILLA = os.path.join(ROOT, "art", ".vanilla", "item")
OUT = os.path.join(ROOT, "art", "candidates")
INGAME = os.path.join(OUT, "ingame_gelat_malti")

PICK = "a"   # maker's provisional install; the critic and the owner decide

PAL = {
    # scoops: warm cream (evaporated milk, a hint of cinnamon), lit to shade, and their outline (lit side, shade side)
    "1": hx("#fbf0d4"), "2": hx("#f1dfb6"), "3": hx("#dfc697"), "4": hx("#c4a676"),
    "q": hx("#8e6c46"), "Q": hx("#6e5236"), "p": hx("#b08a5c"),
    # toppings: toasted almond bits, red and green glacé cherry
    "n": hx("#a46c3a"), "r": hx("#cc2a2c"), "e": hx("#4e9a38"),
    # cream ceramic bowl: lit, mid, flute shade, deep shade; tan rim, its shade; outline lit / shade side
    "W": hx("#f4efe2"), "w": hx("#e0d7c2"), "v": hx("#c7bba0"), "V": hx("#a89a7e"),
    "t": hx("#d2a670"), "T": hx("#ae824e"),
    "o": hx("#80705a"), "O": hx("#5e5242"),
    # glass coupe (c): pale blue-grey, lit / mid / shade, outline lit / shade side
    "G": hx("#e4eef0"), "g": hx("#bcd0d6"), "s": hx("#98b0b8"), "S": hx("#7a949c"),
    "x": hx("#5c7480"), "X": hx("#465a64"),
}

# Each scoop: centre x, centre y, radius x, radius y, back to front. Toppings: (dx, dy, colour) from the centre.
SCOOPS = {
    "a": [((7.5, 3.6, 3.4, 3.0), [(-1, -1, "n"), (1, 0, "r"), (-1, 1, "e"), (2, -1, "n")]),
          ((4.6, 6.8, 3.7, 3.2), [(-1, -1, "r"), (1, -1, "n"), (-2, 1, "n"), (0, 1, "e")]),
          ((10.5, 6.9, 3.7, 3.2), [(-1, -1, "n"), (1, 0, "r"), (0, 1, "n"), (2, -1, "e")])],
    "b": [((7.5, 3.7, 3.4, 2.7), [(-1, -1, "n"), (1, 0, "r"), (-1, 1, "e"), (2, -1, "n")]),
          ((4.4, 6.2, 3.7, 3.1), [(-1, -1, "r"), (1, -1, "n"), (-2, 1, "n"), (0, 1, "e")]),
          ((10.7, 6.3, 3.7, 3.1), [(-1, -1, "n"), (1, 0, "r"), (0, 1, "n"), (2, -1, "e")])],
}
SCOOPS["c"] = SCOOPS["b"]

# Containers, row by row: (y, x from, x to, kind). kind: "rim" (the tan rim), "body" (fluted ceramic), "foot",
# "glass" (glass bowl), "stem" (glass stem / foot).
BOWLS = {
    "a": [(8, 1, 14, "rim"), (9, 1, 14, "body"), (10, 2, 13, "body"), (11, 2, 13, "body"), (12, 3, 12, "body"),
          (13, 4, 11, "body"), (14, 5, 10, "foot")],
    "b": [(8, 2, 13, "rim"), (9, 2, 13, "body"), (10, 3, 12, "body"), (11, 4, 11, "body"), (12, 6, 9, "foot"),
          (13, 6, 9, "foot"), (14, 4, 11, "foot")],
    "c": [(8, 2, 13, "glass"), (9, 2, 13, "glass"), (10, 3, 12, "glass"), (11, 4, 11, "glass"), (12, 6, 9, "stem"),
          (13, 6, 9, "stem"), (14, 4, 11, "stem")],
}


def make(letter):
    grid = [["."] * 16 for _ in range(16)]
    owner = [[-1] * 16 for _ in range(16)]   # which scoop covers a pixel (front-most wins)
    scoops = SCOOPS[letter]
    for i, ((cx, cy, rx, ry), _) in enumerate(scoops):
        for y in range(16):
            for x in range(16):
                u, v = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
                if u * u + v * v <= 1.0:
                    owner[y][x] = i
    # shade each scoop as a dome, with a grainy, rough texture (the beaten, part-frozen milk)
    for i, ((cx, cy, rx, ry), tops) in enumerate(scoops):
        mask = __import__("numpy").array([[owner[y][x] == i for x in range(16)] for y in range(16)])
        light = shade_dome(mask, cx, cy, rx, ry)
        for y in range(16):
            for x in range(16):
                if owner[y][x] != i:
                    continue
                air = inner = False
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if not (0 <= xx < 16 and 0 <= yy < 16) or owner[yy][xx] == -1:
                        air = True
                    elif owner[yy][xx] < i:
                        inner = True
                if air:
                    grid[y][x] = "q" if (x + 0.5 - cx) + (y + 0.5 - cy) < 0 else "Q"
                    continue
                if inner:   # where a front scoop lies on the one behind: a softer seam, not a full outline
                    grid[y][x] = "p"
                    continue
                t = light[y, x] + (hash01(x, y, 7 + i) - 0.5) * 0.4 + (0.08 if x + y < 15 else -0.04)   # gentle top-left light over the whole heap
                grid[y][x] = "1" if t > 0.66 else "2" if t > 0.42 else "3" if t > 0.22 else "4"
        for dx, dy, c in tops:
            x, y = int(cx + dx), int(cy + dy)
            if owner[y][x] == i and grid[y][x] not in "qQ":
                grid[y][x] = c
    # the container, in front of the scoops
    rows = BOWLS[letter]
    cells = {(x, y): kind for y, x0, x1, kind in rows for x in range(x0, x1 + 1)}
    for (x, y), kind in cells.items():
        x0 = min(xx for xx, yy in cells if yy == y)
        x1 = max(xx for xx, yy in cells if yy == y)
        side = (x - x0) / max(1, x1 - x0)          # 0 left (lit) .. 1 right (shade)
        below = (x, y + 1) not in cells
        above_open = (x, y - 1) not in cells and grid[y - 1][x] == "."
        edge = x in (x0, x1) or below or above_open
        glass = kind in ("glass", "stem")
        if edge:
            dark = side > 0.5 or below
            grid[y][x] = ("X" if dark else "x") if glass else ("O" if dark else "o")
        elif kind == "rim":
            grid[y][x] = "t" if side < 0.6 else "T"
        elif kind == "body":
            # vertical flutes: every other column a step darker; lit left, shaded right and low
            base = side * 1.7 + (y - rows[0][0]) * 0.22
            if x % 2 == 0:
                base += 0.7
            grid[y][x] = "W" if base < 0.7 else "w" if base < 1.5 else "v" if base < 2.2 else "V"
        elif kind == "foot":
            grid[y][x] = "w" if side < 0.5 else "v"
        elif kind == "glass":
            if y == rows[0][0]:
                grid[y][x] = "G" if side < 0.6 else "g"   # the lit glass lip
            else:
                # the scoops show through the glass as a pale cream haze on the left, shade on the right
                base = side * 1.5 + (y - rows[0][0]) * 0.3
                grid[y][x] = "G" if base < 0.5 else "g" if base < 1.2 else "s" if base < 1.8 else "S"
        else:  # stem
            grid[y][x] = "g" if side < 0.5 else "s"
    for (x, y), c in FIXES.get(letter, {}).items():
        grid[y][x] = c
    return ["".join(r) for r in grid]


# Critic round 1 (2026-11-17), candidate a, no new colours, so it reads as three scoops in a footed bowl and not as a
# cupcake: a full outline down the gap between the front scoops; the top scoop's seam undercut at both ends; the
# bowl's bottom row narrowed into a foot ring.
FIXES = {"a": {(7, 5): "q", (7, 6): "q", (7, 7): "q", (4, 4): "q", (10, 4): "q",
               (4, 13): ".", (11, 13): ".", (5, 13): "O", (10, 13): "O"}}


LABELS = {"a": "Ġelat a (fluted bowl)", "b": "Ġelat b (footed cup)", "c": "Ġelat c (glass coupe)"}


def vcentre(im):
    ys = [y for y in range(16) for x in range(16) if im.getpixel((x, y))[3]]
    return (min(ys) + max(ys)) / 2


def up(im, k):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def compare(cands):
    font = label_font(14)
    ours = [(lbl, Image.open(os.path.join(ITEMS, n + ".png")).convert("RGBA")) for lbl, n in (
        ("Kannoli", "kannoli"), ("Imqaret", "imqaret"), ("Bigilla", "bigilla"), ("Aljotta", "aljotta"))]
    van = [("vanilla " + n.replace("_", " "), Image.open(os.path.join(VANILLA, n + ".png")).convert("RGBA"))
           for n in ("snowball", "cookie", "pumpkin_pie", "bowl", "mushroom_stew")]
    pieces = cands + ours + van
    pad, lab, cw = 12, 20, 128 + 16 + 3 * 12
    bg = (139, 139, 139, 255)
    rows = []
    img = Image.new("RGBA", (pad + len(pieces) * cw, lab + 128 + 2 * pad), bg)
    d = ImageDraw.Draw(img)
    for i, (n, im) in enumerate(pieces):
        x0 = pad + i * cw
        d.text((x0, 2), n, font=font, fill=(20, 20, 20, 255))
        img.alpha_composite(up(im, 8), (x0, lab + pad // 2))
        img.alpha_composite(im, (x0 + 128 + pad // 2, lab + 56))
    rows.append(img)
    for k in (1, 2):   # as in the hotbar, and at GUI scale 2
        strip = Image.new("RGBA", (pad + len(pieces) * (16 * k + 4 * k), 16 * k + 2 * pad), bg)
        for i, (n, im) in enumerate(pieces):
            strip.alpha_composite(up(im, k), (pad + i * (16 * k + 4 * k), pad))
        rows.append(strip)
    shots = [p for p in sorted(glob.glob(os.path.join(INGAME, "*22-hotbar-gelat*.png"))) if not p.endswith("_crop.png")]
    if shots:
        s = Image.open(shots[-1]).convert("RGBA")
        w, h = s.size
        crop = s.crop((w // 2 - 182, h - 44, w // 2 + 182, h))
        crop.save(os.path.join(INGAME, "22-hotbar-gelat_crop.png"))
        crop = up(crop, 2)
        img = Image.new("RGBA", (crop.width + 2 * pad, crop.height + lab + 2 * pad), (232, 232, 228, 255))
        ImageDraw.Draw(img).text((pad, 2), "in game (GUI scale 2, crop shown x2): snowball, cookie, pumpkin pie, "
                                 "ġelat Malti, kannoli, imqaret, bigilla, aljotta, mushroom stew", font=font,
                                 fill=(20, 20, 20, 255))
        img.alpha_composite(crop, (pad, lab + pad // 2))
        rows.append(img)
    W = max(r.width for r in rows)
    sheet = Image.new("RGBA", (W, sum(r.height + 4 for r in rows)), (200, 200, 196, 255))
    y = 0
    for r in rows:
        sheet.alpha_composite(r, (0, y))
        y += r.height + 4
    p = os.path.join(OUT, "gelat_malti_compare.png")
    sheet.save(p)
    print("wrote", os.path.relpath(p, ROOT))


def main():
    os.makedirs(OUT, exist_ok=True)
    cands = []
    for letter in "abc":
        name = f"gelat_malti_{letter}"
        rows = make(letter)
        check(name, rows)
        im = render(rows, PAL)
        p = os.path.join(OUT, name + ".png")
        im.save(p)
        m = measure(p)
        print(name, {k: float(m[k]) if k != "colours" else m[k] for k in ("coverage", "colours", "edge_l", "interior_l",
                                                                       "tl_minus_br")},
              "outline/inside", round(float(m["edge_l"] / m["interior_l"]), 2), "vcentre", vcentre(im))
        cands.append((LABELS[letter], im))
        if letter == PICK:
            im.save(os.path.join(ITEMS, "gelat_malti.png"))
    compare(cands)


if __name__ == "__main__":
    main()
