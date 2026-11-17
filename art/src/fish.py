"""Item textures for the lampuka (dolphinfish, Coryphaena hippurus) and lampuka moqlija (fried lampuka on a plate).
Candidates, 2026-11-17.

Owner: "for the lampuka, we need to research what the fish looks like to first make the caught fish icon (similar to
cod, salmon, etc), then we have to make a "fried" version which should look like a deep fried version of the fish on a
plate with a slice of lemon (whole fish). technically fried lampuka doesnt look like that, but otherwise it doesnt come
across".

What makes it a lampuka (FishBase, Coryphaena hippurus; photos art/references/lampuka/, see SOURCES.tsv):
- a steep, blunt forehead (a bony crest in mature males), a long, compressed body tapering to a thin tail stalk;
- one long dorsal fin from above the eye almost to the tail; a long dark anal fin under the back half;
- a deeply forked tail;
- fresh: metallic blue-green back, golden-yellow sides with small dark spots, a pale belly; the colours fade to grey
  with a green tinge after death, so the icon shows the fresh golden-green fish.

The silhouettes are hand-placed parts (fin, back, side, belly, anal fin, tail, eye) in vanilla's fish pose (head bottom
left, tail top right, like cod and salmon). Light, edges, spots and the fried crust are rules on top, so the same fish
is used raw and fried. Vanilla fish are measured (art/tools/measure.py), never copied.

Run:  art/.venv/bin/python art/src/fish.py
Writes art/candidates/lampuka_{a,b,c}.png, lampuka_moqlija_{a,b,c}.png and lampuka_compare.png
(with the in-game screenshots from art/candidates/ingame_lampuka/ and the reference photos, if present).
"""
import glob
import math
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import food_items as F  # noqa: E402

hx, render, check = F.hx, F.render, F.check
OUT, VANILLA, ART = F.OUT, F.VANILLA, F.ART
label_font = F.label_font

PAL = {
    # fresh lampuka
    "f": hx("#1c5158"), "F": hx("#123a40"),   # dorsal fin, its edge
    "a": hx("#2c4a48"),                       # anal fin (dark)
    "b": hx("#5cbc9e"), "B": hx("#2f7a68"),   # blue-green back, its edge
    "s": hx("#9ae2bc"),                       # back, lit
    "g": hx("#a8c03c"),                       # green-gold where the back meets the side
    "y": hx("#e6c12c"), "Y": hx("#f4dc58"),   # golden side, lit
    "o": hx("#a67c18"), "O": hx("#70521a"),   # golden side in shade, its edge
    "w": hx("#f1e6a6"), "W": hx("#786024"),   # pale belly, its edge
    "k": hx("#26382c"), "K": hx("#3f7fb0"),   # spots: dark green, blue
    "t": hx("#c4b43a"), "T": hx("#5e5a1c"),   # tail, tail edge
    "e": hx("#101010"),                       # eye
    "c": hx("#f6eecb"),                       # cream belly under the head
    # fried lampuka (a deep-fried golden-brown crust)
    "1": hx("#f4cd78"), "2": hx("#e0a448"), "3": hx("#c6822e"), "4": hx("#9c5c1e"), "5": hx("#6a3a12"),
    "7": hx("#fde8ae"),                       # crisp crumb highlight
    # plain white plate
    "p": hx("#f8f6f0"), "q": hx("#e6e2d8"), "r": hx("#cdc7ba"), "R": hx("#8c867b"),
    # lemon slice
    "L": hx("#f6dc3e"), "l": hx("#fcf4c0"), "m": hx("#d8a818"), "M": hx("#946e10"),
}

# ---- silhouettes (parts: f dorsal fin, b back, y side, w belly, a anal fin, t tail, e eye) ----
# Bull (male): the forehead is a straight, steep front from the crest (1,11) down to the mouth (3,14).
BULL = [
    "................",
    "...........t....",
    "...........tt...",
    "...........t..t.",
    "..........ftttt.",
    "........ffbttt..",
    "......ffbbyy....",
    ".....fbbyyya....",
    "....fbbyyyya....",
    "...fbbyyyywa....",
    "..fbbyyyyw......",
    ".fbbyyyyw.......",
    ".fbeyyyw........",
    "..byyyw.........",
    "...yww..........",
    "................",
]
# The same bull with a fuller tail: lobes two pixels wide where they leave the stalk.
BULL_T = [r if i != 3 else "...........tt.t." for i, r in enumerate(BULL)]
# v2 (critic round 1: "thin generic fish ... not a mahi"): a deeper bull, one more row along the back, a square
# teal forehead (x 1, rows 10-13) with the eye just behind it, a dark ridge of dorsal fin along the whole back, and
# pale cream belly pixels (c) under the head.
DEEP = [
    "................",
    "...........t....",
    "...........tt...",
    "...........tt.t.",
    ".........fftttt.",
    ".......ffbbttt..",
    ".....ffbbbyy....",
    "....fbbbyyya....",
    "...fbbbyyyya....",
    "..fbbbyyyywa....",
    ".fbbbyyyyw......",
    ".bbbyyyyw.......",
    ".bbeyyyw........",
    ".byyyyc.........",
    "..ccW...........",
    "................",
]
# Cow (female): a rounder, lower forehead; the same body and tail.
COW = [
    "................",
    "...........t....",
    "...........tt...",
    "...........t..t.",
    "..........ftttt.",
    "........ffbttt..",
    "......ffbbyy....",
    ".....fbbyyya....",
    "....fbbyyyya....",
    "...fbbyyyywa....",
    "..fbbyyyyw......",
    "..bbyyyyw.......",
    ".bbeyyyw........",
    ".byyyyw.........",
    "..yww...........",
    "................",
]


def neighbours(x, y):
    return ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))


def inside(g, x, y):
    return 0 <= x < 16 and 0 <= y < 16 and g[y][x] != "."


def paint_raw(sil, spots, blue=False, lit_back=True):
    """Fresh colours. Edges take each part's dark tone (vanilla fish have no single outline colour); the upper-left
    pixels of the back and side are lit, the lower-right ones shaded."""
    g = [list(r) for r in sil]
    out = [r[:] for r in g]
    edge = {"f": "F", "b": "B", "y": "O", "w": "W", "t": "T", "a": "a", "e": "e", "c": "c", "W": "W"}
    lit_edge = {"f": "f", "b": "b", "y": "o", "t": "t"}
    for y in range(16):
        for x in range(16):
            c = g[y][x]
            if c == ".":
                continue
            if any(not inside(g, a, b) for a, b in neighbours(x, y)):
                # vanilla's way: edges facing the light (up, left) stay a mid tone, those facing away go dark
                lit = (not inside(g, x - 1, y) or not inside(g, x, y - 1)) and inside(g, x + 1, y) \
                    and inside(g, x, y + 1)
                out[y][x] = lit_edge.get(c, edge[c]) if lit else edge[c]
                continue
            up, lf = g[y - 1][x], g[y][x - 1]
            dn, rt = g[y + 1][x], g[y][x + 1]
            if c == "b" and lit_back and (up == "f" or lf == "f"):
                out[y][x] = "s"
            elif c == "y" and (up == "b" or lf == "b"):
                out[y][x] = "g"
            elif c == "y" and (dn in "wa" or rt in "wa"):
                out[y][x] = "o"
            elif c == "y" and (x + y) % 4 == 1 and x + y < 16:
                out[y][x] = "Y"
    for x, y in spots:
        if out[y][x] in "yYgo":
            out[y][x] = "K" if blue else "k"
    return ["".join(r) for r in out]


def lampuka(kind):
    if kind == "a":     # bull head, dark spots
        # owner 2026-11-17: no spot at (5, 10), next to the eye ("makes the eye look like another dot")
        return paint_raw(shift(DEEP, 0, -1), [(8, 7), (10, 5), (7, 9)])  # a pixel up: centre nearer cod
    if kind == "b":     # cow head, fewer spots
        return paint_raw([r if i != 3 else "...........tt.t." for i, r in enumerate(COW)], [(6, 10), (8, 7)])
    return paint_raw(BULL, [(5, 10), (7, 8), (9, 6), (8, 10)], blue=True, lit_back=False)  # c: blue spots, flatter back


# ---- fried ----
def hash01(x, y, seed):
    v = math.sin(x * 127.1 + y * 311.7 + seed * 74.7) * 43758.5453
    return v - math.floor(v)


def paint_fried(sil, seed=3):
    """The same fish deep-fried: a golden-brown crust, crumb speckles, crisp dark fins and tail. Returns the fish layer
    (its own edges, so it can lie on a plate)."""
    g = [[{"c": "w", "W": "w"}.get(ch, ch) for ch in r] for r in sil]
    out = [r[:] for r in g]
    for y in range(16):
        for x in range(16):
            c = g[y][x]
            if c == ".":
                continue
            is_edge = any(not inside(g, a, b) for a, b in neighbours(x, y))
            if c == "e":
                out[y][x] = "e"
            elif c in "fat":
                # crisp fins and tail: brown, darkest on the edges facing away from the light
                away = not inside(g, x + 1, y) or not inside(g, x, y + 1)
                out[y][x] = "5" if away and c != "f" or c == "a" else "4"
            elif is_edge:
                lit = not inside(g, x - 1, y) or not inside(g, x, y - 1)   # top-left edges a step lighter
                out[y][x] = "3" if lit else "4"
            else:
                up, lf = g[y - 1][x], g[y][x - 1]
                dn, rt = g[y + 1][x], g[y][x + 1]
                if up == "f" or lf == "f":
                    out[y][x] = "1"
                elif dn in "wa." or rt in "wa.":
                    out[y][x] = "3"
                else:
                    out[y][x] = "2"
                h = hash01(x, y, seed)
                if h > 0.82 and out[y][x] in "12":
                    out[y][x] = "7"
                elif h < 0.14 and out[y][x] in "12":
                    out[y][x] = "3"
    return out


def plate(cx, cy, rx, ry, well=0.72):
    """A plain white plate seen from above at an angle: a rim, a slightly greyer well, the outline, the front lip
    in shade. Returns a 16x16 grid."""
    g = [["."] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            u, v = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
            d = u * u + v * v
            if d <= 1.0:
                g[y][x] = "q" if d <= well * well else "p"
    edges = [(x, y) for y in range(16) for x in range(16)
             if g[y][x] != "." and any(not inside(g, a, b) for a, b in neighbours(x, y))]
    for x, y in edges:
        g[y][x] = "R"
    for y in range(16):
        for x in range(16):
            if g[y][x] == "p" and y + 1 < 16 and g[y + 1][x] == "R" and y + 0.5 > cy:
                g[y][x] = "r"      # the rim's front lip: the plate's thickness
            if g[y][x] == "q" and g[y - 1][x] == "p" and y + 0.5 < cy:
                g[y][x] = "r"      # the well's far side in a little shade
    return g


def lay(base, layer):
    out = [r[:] for r in base]
    for y in range(16):
        for x in range(16):
            if layer[y][x] != ".":
                out[y][x] = layer[y][x]
    return out


def shift(sil, dx, dy):
    g = [["."] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            if sil[y][x] != "." and 0 <= x + dx < 16 and 0 <= y + dy < 16:
                g[y + dy][x + dx] = sil[y][x]
    return ["".join(r) for r in g]


def lemon(g, x0, y0, kind="slice"):
    """A lemon slice lying on the plate (seen at an angle: a flattened round, pale flesh, yellow rind) or a wedge."""
    if kind == "slice":
        pts = {(1, 0): "m", (2, 0): "m", (0, 1): "m", (1, 1): "l", (2, 1): "L", (3, 1): "m", (0, 2): "M",
               (1, 2): "m", (2, 2): "m", (3, 2): "M"}
    elif kind == "wedge2":   # v2: flesh on top with one darker segment line, the pale pith, the rind arc below
        pts = {(0, 0): "L", (1, 0): "L", (2, 0): "m", (3, 0): "L",
               (0, 1): "l", (1, 1): "l", (2, 1): "l", (3, 1): "l",
               (1, 2): "M", (2, 2): "M"}
    else:
        pts = {(0, 0): "L", (1, 0): "l", (2, 0): "L", (0, 1): "m", (1, 1): "L", (2, 1): "m", (1, 2): "M"}
    for (dx, dy), c in pts.items():
        g[y0 + dy][x0 + dx] = c
    return g


# Flat (for the platter in moqlija c): the same fish lying level, head left, tail right.
FLAT = [
    "................",
    "................",
    "................",
    "................",
    "..fffffff....tt.",
    ".fbbbbbbbbf..t..",
    ".bbeyyyyyyyftt..",
    ".yyyyyyyyyyyt...",
    ".yyyyyyyyyyatt..",
    "..wwwwwaaaa..t..",
    ".............tt.",
    "................",
    "................",
    "................",
    "................",
    "................",
]


def lampuka_moqlija(kind):
    if kind == "a":     # the whole fish, diagonal as raw, over a round white plate; lemon slice front right
        # v2: the deeper fish, the whole icon a pixel higher, the plate's rim showing all round, a clear lemon wedge
        g = lay(plate(8.3, 7.5, 7.4, 6.4), paint_fried(shift(DEEP, 0, -1)))
        lemon(g, 10, 9, "wedge2")
    elif kind == "b":   # the same on a flatter plate; lemon wedge at the back left
        g = lay(plate(8.0, 8.8, 7.8, 5.4), paint_fried(BULL_T))
        lemon(g, 2, 5, "wedge")
    else:               # level on an oval platter, lemon slice in front
        g = lay(plate(8.0, 8.4, 7.8, 5.2), paint_fried(FLAT))
        lemon(g, 8, 10)
    return ["".join(r) for r in g]


# ---- output ----
def vcentre(im):
    ys = [y for y in range(16) for x in range(16) if im.getpixel((x, y))[3] > 0]
    return sum(ys) / len(ys) + 0.5


def ensure():
    os.makedirs(OUT, exist_ok=True)
    made = {}
    for name, fn in (("lampuka", lampuka), ("lampuka_moqlija", lampuka_moqlija)):
        for k in "abc":
            rows = fn(k)
            check(f"{name}_{k}", rows)
            im = render(rows, PAL)
            im.save(os.path.join(OUT, f"{name}_{k}.png"))
            made[f"{name}_{k}"] = im
    return made


def compare(made):
    font = label_font(14)
    van = [("cod", "cod"), ("salmon", "salmon"), ("cooked cod", "cooked_cod"), ("cooked salmon", "cooked_salmon")]
    items = [(n, Image.open(os.path.join(VANILLA, f + ".png")).convert("RGBA")) for n, f in van]
    items += [(k.replace("lampuka_moqlija", "moqlija").replace("_", " "), im) for k, im in made.items()]
    cols, ch = 5, 8 * 16 + 40
    cell = 8 * 16 + 70
    rows = math.ceil(len(items) / cols)
    # the hotbar crop (enlarged x2 when the screenshot was taken at GUI scale 2)
    hot = sorted(glob.glob(os.path.join(OUT, "ingame_lampuka_v3", "*hotbar*crop_x2.png"))) or \
        sorted(glob.glob(os.path.join(OUT, "ingame_lampuka_v3", "*hotbar*crop*.png")))
    hot_im = Image.open(hot[0]).convert("RGBA") if hot else None
    refs = [p for p in (os.path.join(ART, "references", "lampuka", f"lampuka_{i}.jpg") for i in (1, 2, 3))
            if os.path.exists(p)]
    W = max(cell * cols + 20, (hot_im.width + 20) if hot_im else 0)
    H = rows * ch + 20 + ((hot_im.height + 30) if hot_im else 0) + (180 if refs else 0)
    sheet = Image.new("RGBA", (W, H), (139, 139, 139, 255))
    d = ImageDraw.Draw(sheet)
    for i, (n, im) in enumerate(items):
        x0, y0 = 10 + (i % cols) * cell, 10 + (i // cols) * ch
        sheet.alpha_composite(im.resize((128, 128), Image.NEAREST), (x0, y0))
        sheet.alpha_composite(im, (x0 + 136, y0))
        sheet.alpha_composite(im.resize((32, 32), Image.NEAREST), (x0 + 136, y0 + 24))
        d.text((x0, y0 + 130), n, fill=(255, 255, 255, 255), font=font)
    y = 10 + rows * ch
    if hot_im:
        d.text((10, y), "in game (hotbar): " + os.path.basename(hot[0]), fill=(255, 255, 255, 255), font=font)
        sheet.alpha_composite(hot_im, (10, y + 22))
        y += hot_im.height + 30
    for i, r in enumerate(refs):
        im = Image.open(r).convert("RGBA")
        im.thumbnail((260, 170))
        sheet.alpha_composite(im, (10 + i * 270, y))
    sheet.convert("RGB").save(os.path.join(OUT, "lampuka_compare.png"))


def main():
    made = ensure()
    compare(made)
    for k, im in made.items():
        print(k, "vertical centre", round(vcentre(im), 2))


if __name__ == "__main__":
    main()
