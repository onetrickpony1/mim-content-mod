"""The two dried ġbejniet item icons: ġbejna niexfa (plain, dried) and ġbejna tal-bżar (dried, in black pepper).

The owner (2026-11-17): "there are 2 others besides the fresh which we did: both dry, one plain and one with
pepper flakes all over it. they are smaller and slant inwards as they go up, such that the area of the top circle
of the gbejna is much smaller than the one at the base of the gbejna".

The family is the fresh ġbejna (food_items.gbejna_v6): a round seen a little from above, an elliptical top face lit
from the top left, a short side with faint basket ribs, a warm dark outline (darker on the bottom and right).
These two keep that view, outline and light, but are:
- smaller, and a FRUSTUM: the top ellipse much narrower than the base, the sides slanting inwards as they rise;
- drier: a warm ivory cream, a little more yellow than the fresh one, with a darker rind (art/references/gbejniet_1.jpg, the
  middle bowl);
- tal-bżar: the same cheese coated all over, top and sides, in coarse cracked black pepper, near-black flakes with
  a few tan cracked bits (art/references/gbejniet_2.jpg and gbejniet/gbejniet_bzar_*.jpg).
Both share one shape per candidate letter, so they read as a set. Vertical centre kept at 7.5-8.0 like the fresh one.

Writes art/candidates/gbejna_niexfa_{a,b}.png and gbejna_tal_bzar_{a,b,c}.png, installs the PICK of each as
mod textures item/gbejna_niexfa.png and gbejna_tal_bzar.png, and writes art/candidates/gbejniet_compare.png (with
the in-game hotbar crop when art/candidates/ingame_gbejniet/ holds the 18-hotbar-cheese shot).
Run:  art/.venv/bin/python art/src/gbejniet.py
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
from food_items import reoutline, render, hx  # noqa: E402  (read only: food_items' own output is unchanged)

ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
VANILLA = os.path.join(ROOT, "art", ".vanilla", "item")
OUT = os.path.join(ROOT, "art", "candidates")
INGAME = os.path.join(OUT, "ingame_gbejniet_v4")
REFS = os.path.join(ROOT, "art", "references")

PICK = "c"  # round 3  # the recommended candidate, installed for both

# shape per candidate: row -> (first x, last x, part), outline included. Parts: "back" (the far rim of the top
# disc, outline only), "top" (the top face), "lip" (the near rim of the top disc), "side", "base" (the base's near
# curve, outline only). At 16 px a frustum only reads with explicit steps, so the rows are written out.
SHAPES = {
    # round 2 (critic 2026-11-17): round 1's "a" top (6 px inside, cols 5-10, a lit rim row), sides as two straight
    # diagonals stepping out every 2 rows (rows 6/7 col 4, 8/9 col 3, 10/11 col 2), rows 3-12 (centre 7.5).
    # "a": the base's near curve inset 1 px at each corner
    "a": {3: (6, 9, "back"), 4: (5, 10, "top"), 5: (4, 11, "top"), 6: (4, 11, "lip"), 7: (4, 11, "side"),
          8: (3, 12, "side"), 9: (3, 12, "side"), 10: (2, 13, "side"), 11: (2, 13, "side"), 12: (3, 12, "base")},
    # "b": the same, bottom corners rounded more, like the fresh one (the base row inset 2 px)
    "b": {3: (6, 9, "back"), 4: (5, 10, "top"), 5: (4, 11, "top"), 6: (4, 11, "lip"), 7: (4, 11, "side"),
          8: (3, 12, "side"), 9: (3, 12, "side"), 10: (2, 13, "side"), 11: (2, 13, "side"), 12: (4, 11, "base")},
    # "c" (round 3, critic): no flaring foot; the sides run straight down from row 8 to a rounded base
    # (row 11's corners are outline, the base row inset 1 more)
    "c": {3: (6, 9, "back"), 4: (5, 10, "top"), 5: (4, 11, "top"), 6: (4, 11, "lip"), 7: (4, 11, "side"),
          8: (3, 12, "side"), 9: (3, 12, "side"), 10: (3, 12, "side"), 11: (3, 12, "side"), 12: (4, 11, "base")},
}

# dried (owner 2026-11-17: "less yellow, though more yellow than fresh ones"): a warm ivory cream, a touch more
# yellow than the fresh ġbejna (#f2eedc/#e6e0c8/#d8d0b4), the rind a little darker and warmer, rough
NIEXFA = {"T": hx("#f3eaca"), "t": hx("#e7dbb2"), "S": hx("#d6c292"), "Q": hx("#bba374"), "r": hx("#c9b384"),
          "k": hx("#ddcc9c"), "x": hx("#b09a6c"),
          "o": hx("#8e7248"), "O": hx("#6c5434")}
# peppered: the same dried cheese under its coat, cracked black pepper (black, dark grey, tan bits)
BZAR = {"T": hx("#f3eaca"), "t": hx("#e7dbb2"), "S": hx("#d6c292"), "Q": hx("#bba374"), "r": hx("#c9b384"),
        "k": hx("#ddcc9c"), "x": hx("#b09a6c"),
        "p": hx("#362d26"), "P": hx("#42382e"), "n": hx("#7a6444"),  # grey-brown, luminance ~45-55 of 255
        "o": hx("#86683f"), "O": hx("#624c2e")}


def h2(x, y, s):
    """Stable pixel hash in [0, 1) (integer mixing, so no diagonal banding)."""
    n = (x * 374761393 + y * 668265263 + s * 2246822519) & 0xFFFFFFFF
    n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFFFF) / 0x1000000


def frustum(shape):
    """The frustum from its row extents: T/t top face (lightest at the top left), k near lip, S/r/Q side (lit left,
    faint basket ribs on every other column, shaded right), outline o (lit) / O (bottom and right, from the side down)."""
    G = [["."] * 16 for _ in range(16)]
    part = {}
    for y, (x0, x1, p) in shape.items():
        for x in range(x0, x1 + 1):
            part[(x, y)] = p
            G[y][x] = "?"
    tops = [y for y, v in shape.items() if v[2] == "top"]
    for (x, y), p in part.items():
        x0, x1 = shape[y][0], shape[y][1]
        u = (x - x0) / max(1, x1 - x0)  # 0 left .. 1 right within the row
        if p == "top":
            d = u + 0.35 * (y - tops[0])
            G[y][x] = "T" if d < 0.55 else "t"
        elif p == "lip":
            G[y][x] = "k" if u < 0.7 else "t"
        elif p == "side":
            G[y][x] = "S" if u < 0.3 else ("Q" if u > 0.72 else ("r" if (x + y // 3) % 2 else "S"))
            if u > 0.3 and (x + y // 3) % 2 and u <= 0.72:
                G[y][x] = "r"
        else:
            G[y][x] = "t"  # becomes outline below
    edge = reoutline(G)
    for y in range(16):
        for x in range(16):
            if edge[y][x] == "#" and G[y][x] != ".":
                below = y + 1 >= 16 or G[y + 1][x] == "."
                right = x + 1 >= 16 or G[y][x + 1] == "."
                side_down = part[(x, y)] in ("side", "base")
                G[y][x] = "O" if (below or right) and side_down else "o"
    return G


def rough(G, seed):
    """A rough dry rind: a few darker specks on the side (the top stays smooth, so it reads as the face)."""
    for y in range(16):
        for x in range(16):
            c = G[y][x]
            if c in "SQr" and h2(x, y, seed) < 0.12:
                G[y][x] = "x"
    return G


def pepper(G, seed, counts=(5, 16)):
    """Cracked black pepper all over, top and sides (round 4: 17 grains, 5 on the top face, irregular): grains never
    stacked, a few horizontal pairs, at most one diagonal neighbour each (no checkerboard or chain-mail, and some
    2-3 px gaps), none beside the outline's left or right (the silhouette stays clean)."""
    flakes = set()
    for region, want in zip(("Ttk", "SQr"), counts):
        cells = [(h2(x, y, seed), x, y) for y in range(16) for x in range(16) if G[y][x] in region]
        got = 0
        for v, x, y in sorted(cells):
            if got >= want:
                break
            if any(G[y][x + dx] in "oO" for dx in (1, -1)):
                continue
            if (x, y - 1) in flakes or (x, y + 1) in flakes:
                continue  # never stacked
            side = [(x + dx, y) for dx in (1, -1) if (x + dx, y) in flakes]
            if side and (h2(x, y, seed + 9) > 0.4 or len(side) > 1
                         or any((sx + dx, y) in flakes for sx, _ in side for dx in (1, -1) if sx + dx != x)):
                continue  # a few horizontal pairs (coarse cracked bits), never runs of three
            if sum((x + dx, y + dy) in flakes for dx, dy in ((1, 1), (-1, -1), (1, -1), (-1, 1))) > 1:
                continue  # at most one diagonal neighbour: no checkerboard, no chain-mail
            flakes.add((x, y))
            got += 1
    for x, y in flakes:
        r = h2(x, y, seed + 7)
        G[y][x] = "n" if r < 0.25 else ("P" if r < 0.6 else "p")
    return G


def make(letter):
    shape = SHAPES[letter]
    dry = rough(frustum(shape), 3)
    pep = pepper(frustum(shape), 399, (5, 12))  # seed 399: 17 grains on shape c (5 on the top), irregular
    return render(["".join(r) for r in dry], NIEXFA), render(["".join(r) for r in pep], BZAR)


def vcentre(im):
    ys = [y for y in range(16) for x in range(16) if im.getpixel((x, y))[3]]
    return (min(ys) + max(ys)) / 2


def up(im, k):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def compare(cands):
    font = label_font(14)
    fresh = Image.open(os.path.join(ITEMS, "gbejna.png")).convert("RGBA")
    van = [(n, Image.open(os.path.join(VANILLA, n + ".png")).convert("RGBA")) for n in ("egg", "cookie")]
    pieces = [("gbejna (fresh)", fresh)] + cands + van
    pad, lab, cw = 12, 20, 128 + 16 + 32 + 3 * 12
    rows = []
    for bg in ((232, 232, 228, 255), (139, 139, 139, 255)):
        img = Image.new("RGBA", (pad + len(pieces) * cw, lab + 128 + 2 * pad), bg)
        d = ImageDraw.Draw(img)
        for i, (n, im) in enumerate(pieces):
            x0 = pad + i * cw
            d.text((x0, 2), n, font=font, fill=(20, 20, 20, 255))
            img.alpha_composite(up(im, 8), (x0, lab + pad // 2))
            img.alpha_composite(im, (x0 + 128 + pad, lab + 56))
            img.alpha_composite(up(im, 2), (x0 + 128 + 2 * pad + 16, lab + 48))
        rows.append(img)
    shots = sorted(glob.glob(os.path.join(INGAME, "*18-hotbar-cheese*.png")))
    if shots:
        s = Image.open(shots[-1]).convert("RGBA")
        w, h = s.size
        crop = s.crop((w // 2 - 364, h - 88, w // 2 + 364, h))
        img = Image.new("RGBA", (crop.width + 2 * pad, crop.height + lab + 2 * pad), (232, 232, 228, 255))
        ImageDraw.Draw(img).text((pad, 2), "in game: egg, fresh, niexfa, tal-bżar, cookie, bread, ħobż, pastizz, milk",
                                 font=font, fill=(20, 20, 20, 255))
        img.alpha_composite(crop, (pad, lab + pad // 2))
        rows.append(img)
    refs = [os.path.join(REFS, "gbejniet_1.jpg"), os.path.join(REFS, "gbejniet_2.jpg"),
            os.path.join(REFS, "gbejniet", "gbejniet_bzar_packed_1.jpg")]
    th = []
    for p in refs:
        r = Image.open(p).convert("RGBA")
        r.thumbnail((360, 240))
        th.append(r)
    img = Image.new("RGBA", (pad + sum(t.width + pad for t in th), 240 + lab + pad), (232, 232, 228, 255))
    ImageDraw.Draw(img).text((pad, 2), "references (Wikimedia Commons, see SOURCES.tsv)", font=font,
                             fill=(20, 20, 20, 255))
    x = pad
    for t in th:
        img.alpha_composite(t, (x, lab))
        x += t.width + pad
    rows.append(img)
    W = max(r.width for r in rows)
    sheet = Image.new("RGBA", (W, sum(r.height + 4 for r in rows)), (200, 200, 196, 255))
    y = 0
    for r in rows:
        sheet.alpha_composite(r, (0, y))
        y += r.height + 4
    p = os.path.join(OUT, "gbejniet_compare.png")
    sheet.save(p)
    print("wrote", os.path.relpath(p, ROOT))


def main():
    os.makedirs(OUT, exist_ok=True)
    cands = []
    for letter in SHAPES:
        dry, pep = make(letter)
        for name, im in ((f"gbejna_niexfa_{letter}", dry), (f"gbejna_tal_bzar_{letter}", pep)):
            p = os.path.join(OUT, name + ".png")
            im.save(p)
            m = measure(p)
            print(name, {k: m[k] for k in ("coverage", "colours", "edge_l", "interior_l", "tl_minus_br")},
                  "outline/inside", round(m["edge_l"] / m["interior_l"], 2), "vcentre", vcentre(im))
            cands.append((name, im))
        if letter == PICK:
            dry.save(os.path.join(ITEMS, "gbejna_niexfa.png"))
            pep.save(os.path.join(ITEMS, "gbejna_tal_bzar.png"))
    compare(cands)


if __name__ == "__main__":
    main()
