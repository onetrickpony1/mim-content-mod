"""Oven dishes placed on a table and eaten in slices like a vanilla cake (art trial, 2026-11-17): ross il-forn.

Ross il-forn (Maltese baked rice): from the owner's photos art/references/oven_owner/ross_il_forn/ (reference only):
a rectangular foil tray (or glass/enamel dish), an orange-red crusty top speckled dark where it caught, sometimes
golden cheese; the cut face shows orange rice packed with mince and bits of egg.

Writes, into the mod's resources:
- textures/block/ross_il_forn_{top,side,inside,bottom}.png
- models/block/ross_il_forn_eaten0..5.json (a foil tray 14x14, 5 tall; the rice in a 2x3 grid of portions, one
  portion removed per eaten step, starting at the front (north, the side facing the player); cut faces use _inside)
- blockstates/ross_il_forn.json (facing x eaten)
- textures/item/ross_il_forn.png, models/item/ross_il_forn.json, items/ross_il_forn.json
- art/candidates/ross_compare.png (with the in-game screenshots, if present in art/candidates/ingame_ross/)
Run:  art/.venv/bin/python art/src/oven_dishes.py
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import food_items as F  # noqa: E402
import pilot_models as P  # noqa: E402

hx = F.hx
TEX = os.path.join(P.RES, "textures")
NS = P.NS

# foil tray
FOIL = {"rim": "#eef0f2", "hi": "#d8dce0", "mid": "#b8bcc2", "lo": "#9ca0a6", "dark": "#8a8e94"}
# baked top and the rice inside
CRUST = {"light": "#e0763a", "mid": "#c85a2a", "dark": "#a04220", "char": "#5a2a14", "gold": "#f0a850"}
RICE = {"base": "#d8803e", "grain": "#f2d6a0", "mince": "#7a3a1e", "shade": "#b8602a", "yolk": "#f2d060",
        "white": "#f6f0e0"}


def noise_tex(base, picks, seed):
    """16x16: base colour with a share of pixels swapped for others; picks = [(hex, share)]."""
    rs = np.random.RandomState(seed)
    a = np.zeros((16, 16, 4), np.uint8)
    a[..., :3] = hx(base)
    a[..., 3] = 255
    r = rs.rand(16, 16)
    acc = 0.0
    for col, share in picks:
        m = (r >= acc) & (r < acc + share)
        a[m, :3] = hx(col)
        acc += share
    return a


def top_tex(edges=True):
    a = noise_tex(CRUST["mid"], [(CRUST["light"], 0.32), (CRUST["dark"], 0.2), (CRUST["char"], 0.06),
                                 (CRUST["gold"], 0.05)], 11)
    if edges:                               # critic r1: charred edges against the tray (every third pixel)
        for i in range(0, 16, 3):
            for x, y in ((i, 2), (i, 13), (2, i), (13, i)):
                a[y, x, :3] = hx(RICE["mince"])
    return a


def inside_tex():
    a = noise_tex(RICE["base"], [(RICE["grain"], 0.26), (RICE["mince"], 0.15), (RICE["shade"], 0.15),
                                 (RICE["yolk"], 0.04), (RICE["white"], 0.03)], 12)
    a[12] = top_tex(False)[3]               # the crust line
    # critic r1: no pale grains on the used rows (they read as sponge cake); two egg flecks; more mince
    m = (a[11:16, :, :3] == hx(RICE["grain"])).all(axis=2)
    a[11:16][m, :3] = hx(RICE["base"])
    for x, y in ((3, 13), (12, 15)):
        a[y, x, :3] = hx(RICE["white"])
    for x, y in ((5, 14), (10, 12)):
        a[y, x, :3] = hx(RICE["mince"])
    return a


def side_tex():
    a = np.zeros((16, 16, 4), np.uint8)
    a[..., 3] = 255
    for x in range(16):
        col = FOIL["lo"] if x % 4 == 3 else (FOIL["hi"] if x % 2 == 0 else FOIL["mid"])   # pleated foil
        a[:, x, :3] = hx(col)
    a[11, :, :3] = hx(FOIL["rim"])          # the rolled rim (y 5 in the model)
    a[15, :, :3] = hx(FOIL["dark"])
    return a


def bottom_tex():
    return noise_tex(FOIL["mid"], [(FOIL["hi"], 0.3), (FOIL["lo"], 0.15)], 13)


# ---- model ----
X0, X1, Z0, Z1, Y0, Y1 = 2, 14, 2, 14, 1, 5          # the rice, packed flush with the rim (critic r1)
XS = (2, 8, 14)                                       # 2 columns
ZS = (2, 6, 10, 14)                                   # 3 rows, front (north) first
ORDER = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)]   # (column, row) eaten in this order


def tray(handles=False):
    """The dish: floor and four walls. handles: the two short end walls (east and west, outer faces) use the
    'handle' texture (a moulded grip lip painted on)."""
    S, B = "side", "bottom"
    e = [P.box([1, 0, 1], [15, 1, 15], {"down": B, "up": B, **{k: S for k in P.ALL}})]       # floor
    for f, t, inner in (([1, 1, 1], [15, 5, 2], "south"), ([1, 1, 14], [15, 5, 15], "north"),
                        ([1, 1, 2], [2, 5, 14], "east"), ([14, 1, 2], [15, 5, 14], "west")):
        outer = {"south": "north", "north": "south", "east": "west", "west": "east"}[inner]
        e.append(P.box(f, t, {outer: ("handle" if handles and outer in ("east", "west") else S), inner: S, "up": B}))
    return e


def rice(eaten):
    gone = set(ORDER[:eaten])
    left = [c for c in ORDER if c not in gone]
    e = []
    for (c, r) in left:
        x0, x1, z0, z1 = XS[c], XS[c + 1], ZS[r], ZS[r + 1]
        faces = {"up": "top"}
        if (c, r - 1) in gone or (r == 0 and False):
            faces["north"] = "inside"
        if (c, r + 1) in gone:
            faces["south"] = "inside"
        if (c - 1, r) in gone:
            faces["west"] = "inside"
        if (c + 1, r) in gone:
            faces["east"] = "inside"
        e.append(P.box([x0, Y0, z0], [x1, Y1, z1], faces))
    return e


def models(name="ross_il_forn", extra=None, handles=False):
    """The six eaten models, the blockstate and the item JSONs of one slice dish (same geometry for every dish).
    extra(eaten) adds elements on top of the remaining portions (the imqarrun's raised penne)."""
    tex = {"particle": f"{NS}:block/{name}_top", "top": f"{NS}:block/{name}_top",
           "side": f"{NS}:block/{name}_side", "inside": f"{NS}:block/{name}_inside",
           "bottom": f"{NS}:block/{name}_bottom"}
    if extra:
        tex["penne"] = f"{NS}:block/{name}_penne"
    if handles:
        tex["handle"] = f"{NS}:block/{name}_handle"
    for n in range(6):
        P.write(f"models/block/{name}_eaten{n}.json", P.model(tray(handles) + rice(n) + (extra(n) if extra else []), tex))
    rot = {"north": 0, "east": 90, "south": 180, "west": 270}
    variants = {f"eaten={n},facing={f}": ({"model": f"{NS}:block/{name}_eaten{n}", "y": y} if y else
                                          {"model": f"{NS}:block/{name}_eaten{n}"})
                for f, y in rot.items() for n in range(6)}
    P.write(f"blockstates/{name}.json", {"variants": variants})
    P.write(f"models/item/{name}.json", {"parent": "minecraft:item/generated",
                                          "textures": {"layer0": f"{NS}:item/{name}"}})
    P.write(f"items/{name}.json", {"model": {"type": "minecraft:model", "model": f"{NS}:item/{name}"}})


# ---- item icon: the whole foil tray in 3/4, orange crusty top, pleated front wall ----
# critic r1: 3/4 view like vanilla pumpkin pie (the front-on box read as a microwave), plain vertical foil ridges,
# a cut corner at the front right showing the rice, one dark outline.
ICON_PAL = {"O": hx("#4e5258"), "H": hx("#eef0f2"), "w": hx("#d8dce0"), "W": hx("#a4a8ae"), "s": hx("#a4a8ae"),
            "L": hx(CRUST["light"]), "r": hx(CRUST["mid"]), "x": hx(CRUST["char"]),
            "c": hx(RICE["base"]), "e": hx(RICE["white"]), "R": hx(CRUST["dark"])}
ICON = [
    "................",
    "................",
    "...OOOOOOOOOO...",
    "..OHHHHHHHHHHO..",
    "..OHLrLrrLxrHO..",
    ".OHrLxrLrrLrrHO.",
    ".OHrrLrrxrcecHO.",
    ".OHLrrxLrRcccHO.",
    ".OHrLrrrLrsssHO.",
    ".OHHHHHHHHHHHHO.",
    ".OwWwWwWwWwWwWO.",
    ".OwWwWwWwWwWwWO.",
    ".OwWwWwWwWwWwWO.",
    "..OOOOOOOOOOOO..",
    "................",
    "................",
]
# light from the top left: the rim's right side and the right half of the front rim one step greyer
for _y in range(4, 9):
    ICON[_y] = ICON[_y][:13] + ICON[_y][13:].replace("H", "w", 1) if _y > 3 else ICON[_y]
ICON[9] = ICON[9][:8] + "wwwwww" + ICON[9][14:]
ICON[3] = ICON[3][:12] + "w" + ICON[3][13:]


# ---- Icon v3 (owner: "its mostly the light ... which makes it feel extra 2d"): candidates only, not installed ----
# The baked top is the lit face (brightest top-left); foil walls in shade, never the brightest; only the top-left rim
# edge highlighted; the right side darkest; a 1-px shadow where the rice meets the front wall; the cut face darker.
ICON3_PAL = {"O": hx("#3e4248"), "o": hx("#5e6268"), "v": hx("#74787e"), "H": hx("#eef0f2"), "m": hx("#b8bcc2"), "n": hx("#7a7e84"), "f": hx("#a4a8ae"),
             "w": hx("#9a9ea4"), "W": hx("#84888e"), "k": hx("#6e7278"), "s": hx("#8c9096"),
             "L": hx("#e88a48"), "r": hx(CRUST["mid"]), "R": hx(CRUST["dark"]), "x": hx(CRUST["char"]),
             "D": hx("#7e3418"), "c": hx(RICE["shade"]), "e": hx(RICE["white"])}
ICON3A = [
    "................",
    "................",
    "...OOOOOOOOOO...",
    "..OHHHHHHmmmmO..",
    "..OHLLLLrLxrnO..",
    ".OHLLxLrLrrrrnO.",
    ".OHLLrrxrrcecnO.",
    ".OHLrrrrRrcccnO.",
    ".OHDDDDDDDsssnO.",
    ".OmffffffffffnO.",
    ".OmWwWwWwWwWwkO.",
    ".OmWwWwWwWwWwkO.",
    ".OmWwWwWwWwWwkO.",
    "..OOOOOOOOOOOO..",
    "................",
    "................",
]
ICON3B = [   # steeper: more of the top, a shorter front wall
    "................",
    "...OOOOOOOOOO...",
    "..OHHHHHHmmmmO..",
    "..OHLLLLrLxrnO..",
    ".OHLLxLLrLrrrnO.",
    ".OHLLrrLxrrrrnO.",
    ".OHLrLrrrrcecnO.",
    ".OHLrrxrRrcccnO.",
    ".OHrrrRrrRsssnO.",
    ".OHDDDDDDDsssnO.",
    ".OmffffffffffnO.",
    ".OmWwWwWwWwWwkO.",
    ".OmWwWwWwWwWwkO.",
    "..OOOOOOOOOOOO..",
    "................",
    "................",
]


# v4 (owner: "remove the cut and work on v3b a bit more"): the icon is the whole, uncut dish.
ICON3_PAL["g"] = hx(CRUST["gold"])
ICON4A = [r[:10] + {6: "rRr", 7: "RrR", 8: "RRR", 9: "DDD"}.get(y, r[10:13]) + r[13:] for y, r in enumerate(ICON3B)]
ICON4B = [   # refined: speckled crust with char and golden (cheesy) bits, shadow under the back/left rim,
    "................",   # light only on the top-left rim edges, pleated foil (two light, one dark)
    "...OOOOOOOOOO...",
    "..OHHHHHHmmmmO..",
    "..OHRRRRRRRRnO..",
    ".OHRLLgLLrLxrnO.",
    ".OHRLgLxLrrLrnO.",
    ".OHRLLrLrrgrrnO.",
    ".OHRLxrrrRrxRnO.",
    ".OHRrrRrrRrRRnO.",
    ".OHDDDDDDDDDDnO.",
    ".OmffffffffffnO.",
    ".OmwwWwwWwwWwkO.",
    ".OmwwWwwWwwWwkO.",
    "..OOOOOOOOOOOO..",
    "................",
    "................",
]


def relight(rows, front=False):
    """Outline lighter on the top/left, darker on the bottom/right; the front wall's right half one step darker."""
    g = [list(r) for r in rows]
    for y in range(16):
        for x in range(16):
            if g[y][x] == "O" and x + y < 15:
                g[y][x] = "o"
            elif g[y][x] == "W" and x >= 8:
                g[y][x] = "v"
            elif g[y][x] == "w" and x >= 10:
                g[y][x] = "W"
            elif front and g[y][x] == "f" and x >= 8:
                g[y][x] = "w"
    return ["".join(r) for r in g]


def icon_compare():
    ims = []
    for n, rows in (("v3a", ICON3A), ("v3b", ICON3B), ("v4a", ICON4A), ("v4b", ICON4B)):
        im = F.render(relight(rows), ICON3_PAL)
        im.save(os.path.join(F.OUT, f"ross_icon_{n}.png"))
        if n != "v3a":
            ims.append(("Ross il-forn " + n, im))
    for v in ("cake", "pumpkin_pie"):
        ims.append(("vanilla " + v, Image.open(os.path.join(F.VANILLA, v + ".png")).convert("RGBA")))
    F.compare(ims).save(os.path.join(F.OUT, "ross_icon_compare.png"))


# ---- Imqarrun il-forn (baked macaroni), owner's photos art/references/oven_owner/imqarrun_il_forn/ (reference only):
# penne/rigatoni in orange-red tomato sauce with blackened tube tips and crusty dark patches, baked in a glass or
# white ceramic dish; the cut face shows layered tubes with mince, egg/cheese binding, sometimes peas. Told apart from
# ross il-forn by the tubes (not rice) and the white dish (not foil).
PASTA = {"sauce": "#c8502a", "sauce_dark": "#a03e20", "lit": "#f2a862", "body": "#e0843e", "shade": "#b45a28",
         "char": "#2e160c", "char2": "#5a2a14", "pale": "#f2c878", "bind": "#f0d890", "mince": "#7a3a1e",
         "pea": "#6f9a3a"}
DISH = {"rim": "#f8f6f0", "hi": "#ece8e0", "mid": "#dcd8ce", "lo": "#c4c0b6", "dark": "#a8a49a"}


def penne_top():
    """Sauce with a jumble of short penne tubes (diagonal and level), each lit on its upper-left, a blackened tip."""
    a = noise_tex(PASTA["sauce"], [(PASTA["sauce_dark"], 0.18), (PASTA["char2"], 0.04)], 21)
    rs = np.random.RandomState(22)
    dirs = ((1, 1), (1, -1), (1, 0), (0, 1))
    for _ in range(26):
        x, y = rs.randint(0, 16), rs.randint(0, 16)
        dx, dy = dirs[rs.randint(0, 4)]
        n = 4
        for i in range(n):
            px, py = (x + dx * i) % 16, (y + dy * i) % 16
            a[py, px, :3] = hx(PASTA["char"] if i == n - 1 else PASTA["lit"] if i == 0 else PASTA["body"])
            sx, sy = (px + (1 if dy != 0 or dx == 0 else 0)) % 16, (py + (1 if dx != 0 else 0)) % 16
            if i < n - 1 and dx != 0:
                a[sy, px, :3] = hx(PASTA["shade"])            # the tube's shaded underside
    return a


def penne_inside():
    """The cut face: tubes cut across (pale rings with a sauce-dark hole) and lengthwise, mince, egg/cheese, a pea."""
    a = noise_tex(PASTA["sauce"], [(PASTA["bind"], 0.15), (PASTA["mince"], 0.12), (PASTA["body"], 0.15)], 23)
    for x0, y0 in ((1, 12), (6, 13), (11, 12), (3, 14), (9, 14), (13, 14), (2, 7), (8, 8), (12, 5), (5, 3)):
        for dx, dy, c in ((0, 0, "pale"), (1, 0, "shade"), (2, 0, "pale")):
            a[y0 + dy, (x0 + dx) % 16, :3] = hx(PASTA[c])     # a tube end: pale wall, dark middle, pale wall
    for x in range(1, 15, 3):
        a[13, x, :3] = hx(PASTA["pale"]) if a[13, x, 0] != hx(PASTA["shade"])[0] else a[13, x, :3]
    a[11] = penne_top()[4]                  # the crusty top edge (y 5 in the model)
    a[14, 7, :3] = hx(PASTA["pea"])
    return a


def dish_side():
    a = np.zeros((16, 16, 4), np.uint8)
    a[..., 3] = 255
    a[:, :, :3] = hx(DISH["mid"])
    a[11, :, :3] = hx(DISH["rim"])          # the glazed rim (y 5)
    a[12, :, :3] = hx(DISH["hi"])
    a[15, :, :3] = hx(DISH["lo"])
    for x in (3, 9, 14):
        a[13, x, :3] = hx(DISH["hi"])       # a little glaze shine
    return a


def dish_handle():
    """The end walls with a moulded grip lip (owner: "add shading on the side implying handles"): the wall face uses
    x 2-14, rows 11-15 (row 11 the rim); a light ledge on row 12, shadow beneath, 7 px wide and centred."""
    a = dish_side()
    for x in range(5, 12):
        a[12, x, :3] = hx("#f8f6f0")
        a[13, x, :3] = hx("#c8c4ba")
    for x in range(6, 11):
        a[14, x, :3] = hx("#a8a49a")
    return a


def dish_bottom():
    return noise_tex(DISH["mid"], [(DISH["hi"], 0.25), (DISH["lo"], 0.15)], 24)


IMQ_PAL = {"O": hx("#4a463e"), "o": hx("#6a665e"), "H": hx("#f8f6f0"), "m": hx("#dcd8ce"), "n": hx("#a8a49a"),
           "f": hx("#e4e0d6"), "w": hx("#d4d0c6"), "W": hx("#c0bcb2"), "v": hx("#aeaaa0"), "k": hx("#96928a"),
           "R": hx(PASTA["sauce_dark"]), "r": hx(PASTA["sauce"]), "D": hx("#7e3418"),
           "L": hx(PASTA["lit"]), "p": hx(PASTA["body"]), "P": hx(PASTA["shade"]), "x": hx(PASTA["char"])}
IMQ_ICON = [   # same 3/4 view and light as ross_icon_v4b: penne tubes on top, a white ceramic dish
    "................",
    "...OOOOOOOOOO...",
    "..OHHHHHHmmmmO..",
    "..OHRRRRRRRRnO..",
    ".OHRLpxrLppxrnO.",
    ".OHLprLppxLpPnO.",
    ".OHpPxrLpPprxnO.",
    ".OHRLppxRLpPrnO.",
    ".OHrpPrLppxPRnO.",
    ".OHDDDDDDDDDDnO.",
    ".OmffffffffffnO.",
    ".OmwwwwwwwwwwkO.",
    ".OmWWWWWWWWWWkO.",
    "..OOOOOOOOOOOO..",
    "................",
    "................",
]


# critic r1: big readable tubes on the top, a layered cut face, the food raised above the rim on the icon
def penne_top_v2():
    a = np.zeros((16, 16, 4), np.uint8)
    a[..., 3] = 255
    for y in range(16):
        for x in range(16):
            a[y, x, :3] = hx("#7e3418" if (x * 3 + y * 5) % 4 == 0 else "#a03e20")    # sauce in the gaps
    UP, LO, END, NEAR = hx("#f2a862"), hx("#d07038"), hx("#2e160c"), hx("#5a2a12")

    def level(y, x0, x1, ends):
        for x in range(x0, x1 + 1):
            a[y, x % 16, :3], a[(y + 1) % 16, x % 16, :3] = UP, LO
        for e, n in ends:
            for yy in (y, y + 1):
                a[yy % 16, e % 16, :3] = END
                a[yy % 16, n % 16, :3] = NEAR

    def diag(pts, step_up=False):
        for i, (x, y) in enumerate(pts):
            last = i == len(pts) - 1
            a[y % 16, x % 16, :3] = END if last else (NEAR if i == len(pts) - 2 else UP)
            a[(y + 1) % 16, x % 16, :3] = END if last else LO

    level(3, 2, 6, [(2, 3), (6, 5)])
    level(6, 9, 14, [(14, 13)])
    level(1, 9, 13, [(9, 10)])
    level(13, 10, 15, [(15, 14)])
    level(14, 1, 5, [(5, 4)])
    level(6, 0, 4, [(4, 3)])
    diag([(4, 9), (5, 10), (6, 11), (7, 12)])
    diag([(8, 12), (9, 11), (10, 10), (11, 9)])
    return a


def penne_inside_v2():
    a = np.zeros((16, 16, 4), np.uint8)
    a[..., 3] = 255
    a[:, :, :3] = hx("#8a4020")
    a[0, :, :3] = hx("#e0843e")
    a[1, :, :3] = hx("#e0843e")
    for x in (2, 6, 7, 11, 14):
        a[0, x, :3] = hx("#2e160c")
    for i, y in enumerate((2, 5, 8, 11)):                     # rows of tube ends, mince bands between
        off = 0 if i % 2 == 0 else 2
        for x0 in range(off - 4, 16, 4):
            for dx in range(3):
                x = x0 + dx
                if 0 <= x < 16:
                    a[y, x, :3] = hx("#7e3418" if dx == 1 else "#e8c48a")
                    a[y + 1, x, :3] = hx("#e8c48a")
        a[y + 2, :, :3] = hx("#6a3018" if i % 2 == 0 else "#8a4020")
    a[14:16, :, :3] = hx("#f0d890")                           # egg/cheese base
    return a


IMQ_PAL2 = dict(IMQ_PAL, n=hx("#8a867c"), c=hx("#c8602a"), b=hx("#e0843e"), B=hx("#b45a28"), Y=hx("#5a2a12"),
                L=hx("#f2a862"), R=hx("#a03e20"), f=hx("#c8c4ba"), w=hx("#aca89e"), W=hx("#98948a"),
                v=hx("#868278"), k=hx("#726e66"), m=hx("#e4e0d6"))
IMQ_ICON2 = [   # the pasta raised above the rim like vanilla pumpkin pie, four big tubes, a 3-row dish front
    "................",
    "..OOOOOOOOOOOO..",
    ".OHLLpRRRRxRRnO.",
    ".OHLLLLxRRRRRnO.",
    ".OHccccxbbbbxnO.",
    ".OHRRRRRBBBBxnO.",
    ".OHxLLLLLRRRRnO.",
    ".OHxcccccYbbbnO.",
    ".OHRRRRRRYBBBnO.",
    ".OmffffffffffnO.",
    ".OmwwwwwwwwwwkO.",
    ".OmwwwwwwwwwwkO.",
    ".OmWWWWWWWWWWkO.",
    "..OOOOOOOOOOOO..",
    "................",
    "................",
]


# ---- v3 (owner: "needs more char, the icon is terrible, and the slices look like 3 tubes running through it") ----
CHAR = {"black": "#1e0e08", "char": "#2e160c", "crust": "#5a2a12", "lit": "#e88a48", "body": "#d07038",
        "low": "#b45a28", "sauce": "#c8602a", "pale": "#e8c48a", "mince": "#6a3018", "base": "#dc9a5a"}


def penne_top_v3():
    """Heavily charred: a jumble of 2-px-wide tubes at many angles with near-black tips and edges, dark-brown crust
    patches all over (about a third of the top dark), orange only between."""
    rs = np.random.RandomState(31)
    a = np.zeros((16, 16, 4), np.uint8)
    a[..., 3] = 255
    a[:, :, :3] = hx(CHAR["sauce"])
    dirs = ((1, 0), (0, 1), (1, 1), (1, -1), (2, 1), (1, 2))
    for _ in range(16):
        x, y = rs.randint(0, 16), rs.randint(0, 16)
        dx, dy = dirs[rs.randint(0, len(dirs))]
        n = rs.randint(4, 7)
        for i in range(n):
            px, py = x + (dx * i) // max(1, max(dx, dy) // 1), y + (dy * i) // max(1, max(dx, dy) // 1)
            px, py = px % 16, py % 16
            qx, qy = (px + (1 if dy and not dx else 0)) % 16, (py + (1 if dx else 0)) % 16
            tip = i >= n - 2 or i == 0
            a[py, px, :3] = hx(CHAR["black"] if i == n - 1 else CHAR["char"] if tip else CHAR["lit"])
            a[qy, qx, :3] = hx(CHAR["char"] if tip else CHAR["low"])
    dark = lambda: (np.abs(a[..., :3].astype(int).sum(2)) < 300).mean()
    while dark() < 0.33:                                    # crusty patches until about a third is dark
        x, y = rs.randint(0, 16), rs.randint(0, 16)
        for ddx, ddy in ((0, 0), (1, 0), (0, 1)):
            if rs.rand() < 0.8:
                a[(y + ddy) % 16, (x + ddx) % 16, :3] = hx(CHAR["crust"])
    return a


def penne_inside_v3():
    """A dense irregular jumble: small pale tube ends (1-2 px, some slanted) at varied heights in orange sauce, mince
    flecks, a charred top band (row 11, the top of the face in the model; also rows 0-1) and a paler bound base."""
    rs = np.random.RandomState(32)
    a = noise_tex(CHAR["sauce"], [(CHAR["low"], 0.18), (CHAR["mince"], 0.12)], 33)
    for _ in range(46):
        x, y = rs.randint(0, 16), rs.randint(0, 16)
        shape = rs.randint(0, 4)
        pts = [(x, y)] + ([(x + 1, y)] if shape == 1 else [(x, y + 1)] if shape == 2 else
                          [(x + 1, y + 1)] if shape == 3 else [])
        for px, py in pts:
            a[py % 16, px % 16, :3] = hx(CHAR["pale"])
    for row in (0, 1, 11):
        for x in range(16):
            a[row, x, :3] = hx(CHAR["char"] if (x * 7 + row) % 3 == 0 else CHAR["crust"] if (x + row) % 2 else CHAR["low"])
    for x in range(16):
        if rs.rand() < 0.6:
            a[15, x, :3] = hx(CHAR["base"])
    return a


ICON_V3_PAL = {"O": hx("#3e1e0c"), "o": hx("#6a3a1a"), "x": hx(CHAR["char"]), "X": hx(CHAR["black"]),
               "c": hx(CHAR["crust"]), "L": hx("#f2a862"), "p": hx(CHAR["body"]), "q": hx(CHAR["low"]),
               "e": hx(CHAR["pale"]), "s": hx(CHAR["sauce"]), "Q": hx(CHAR["mince"]), "b": hx(CHAR["base"]),
               "D": hx("#6e2a14"), "d": hx("#4a1c0a"), "E": hx("#8a6a40"),
               # white dish / plate
               "H": hx("#f8f6f0"), "m": hx("#e4e0d6"), "n": hx("#8a867c"), "f": hx("#c8c4ba"), "w": hx("#aca89e"),
               "W": hx("#98948a"), "v": hx("#868278"), "k": hx("#726e66"), "P": hx("#5a564e"),
               "u": hx("#4a6ab0"), "r": hx("#d0607a")}
IMQ_ICON3A = [   # the white dish, the pasta heaped and heavily charred, tubes as 2-row strokes
    "................",
    "..OOOOOOOOOOOO..",
    ".OHcLLLxcLLLxnO.",
    ".OHcpppxcpppxnO.",
    ".OHxLLLLcxLLcnO.",
    ".OHxppppcxqqcnO.",
    ".OHcLLxcqqqqxnO.",
    ".OHcppxcxxxxXnO.",
    ".OHxcxcxXcxXXnO.",
    ".OmffffffffffnO.",
    ".OmwwwwwwwwwwkO.",
    ".OmwwwwwwwwwwkO.",
    ".OmWWWWWWWWWWkO.",
    "..OOOOOOOOOOOO..",
    "................",
    "................",
]
IMQ_ICON3B = [   # one cut portion: charred top, the jumbled tube ends on its cut faces, the right face in shade
    "................",
    "................",
    "................",
    ".....ooooooooo..",
    "....oxLxLLxpxcO.",
    "...oLxcLpxLcxDO.",
    "..oLLxLcpxLxDdO.",
    ".oxxcxxcxxcDddO.",
    ".oeseQseQesDEdO.",
    ".oseQeseseQDdEO.",
    ".oQesesQeseDdO..",
    ".oseeQesQseDO...",
    ".Obbbbbbbbb O...".replace(" ", "O"),
    "..OOOOOOOOOO....",
    "................",
    "................",
]
IMQ_ICON3C = [   # the portion on a small white plate with a flowered rim (the owner's plated photo)
    "................",
    "................",
    ".....ooooooooo..",
    "....oxLxLLxpxcO.",
    "...oLxcLpxLcxDO.",
    "..oLLxLcpxLxDdO.",
    "..oxcxxcxxcDdO..",
    "..oeseQseQeDEO..",
    "..oseQesesQDdO..",
    ".ooQesesQesDOOo.",
    "oHuHbbbbbbbbOmro",
    "oHmHmumHmrmHmnmO",
    ".OmmHmmumrmmnnO.",
    "..OOnnnnnnnnOO..",
    "....OOOOOOOO....",
    "................",
]


# Square pans (owner: "make the ross il forn pan a square. its a square when placed"): straight edges, square corners
def square(rows):
    """Square corners: the first and last outline rows run the full width."""
    g = [list(r) for r in rows]
    ys = [y for y in range(16) if any(c != "." for c in g[y])]
    for y in (ys[0], ys[-1]):
        g[y] = list(".OOOOOOOOOOOOOO.")
    return ["".join(r) for r in g]


def plate_shade(rows):
    """The plate in shade on its right: white one step greyer from x 8 on, rows 10 and below."""
    g = [list(r) for r in rows]
    for y in range(9, 16):
        for x in range(8, 16):
            g[y][x] = {"H": "m", "m": "n"}.get(g[y][x], g[y][x])
    return ["".join(r) for r in g]


# Ross v5 (owner: "follow v4bs black specs, but without its brown border"): the rice meets the foil rim directly,
# only a thin shade line at the front; a square pan.
ROSS_V5 = square([
    "................",
    ".OOOOOOOOOOOOOO.",
    ".OHHHHHHHHmmmmO.",
    ".OHLLLgLLrLLxnO.",
    ".OHLLLgLLrLxrnO.",
    ".OHLLgLxLrrLrnO.",
    ".OHLLLrLrrgrrnO.",
    ".OHLLxrrrRrxRnO.",
    ".OHLrrRrrRrRRnO.",
    ".OHRRRRRRRRRRnO.",
    ".OmffffffffffnO.",
    ".OmwwWwwWwwWwkO.",
    ".OmwwWwwWwwWwkO.",
    ".OOOOOOOOOOOOOO.",
    "................",
    "................",
])


# Ross v6 (owner: "a bit darker in the top left, similar to how dark it is in the top right. not identical"):
# the lit orange becomes a tone between it and the mid orange, except the three pixels nearest the top-left corner.
ICON3_PAL["M"] = hx("#d8703a")
ROSS_V6 = [r[:3] + "".join("M" if c == "L" and (x + 3, y) not in ((3, 3), (4, 3), (3, 4)) else c
                           for x, c in enumerate(r[3:13])) + r[13:] if 3 <= y <= 8 else r
           for y, r in enumerate(ROSS_V5)]


def ross_icon_compare():
    ims = []
    for n, rows in (("v5", ROSS_V5), ("v6", ROSS_V6)):
        im = F.render(relight(rows), ICON3_PAL)
        if n == "v6":
            im.save(os.path.join(F.OUT, "ross_icon_v6.png"))
        ims.append(("Ross il-forn " + n, im))
    F.compare(ims).save(os.path.join(F.OUT, "ross_icon_compare.png"))


def icon_v3_compare():
    ims = []
    for n, rows in (("v3a", square(IMQ_ICON3A)), ("v3b", IMQ_ICON3B[1:] + IMQ_ICON3B[:1]),
                    ("v3c", plate_shade(IMQ_ICON3C[1:] + IMQ_ICON3C[:1]))):
        rows = relight(rows, front=True) if n == "v3a" else rows
        im = F.render(rows, ICON_V3_PAL)
        im.save(os.path.join(F.OUT, f"imqarrun_icon_{n}.png"))
        ims.append(("Imqarrun il-forn " + n, im))
    im = F.render(relight(ROSS_V5), ICON3_PAL)
    im.save(os.path.join(F.OUT, "ross_icon_v5.png"))
    ims.append(("Ross il-forn v5", im))
    return ims


# ---- v4 (owner: "everything is quite bad"; a 3-D top "like penne pasta curling as it bakes"; the cut face from the
# plated-portion photo; the icon = the ross v5 icon with a white ceramic dish and penne-coloured food) ----
def penne_tex():
    """Small raised penne (owner: "far too large ... burnt at the end that should be hollow"): x 0-2 rows 0-3 the body
    (row 0 the upper surface with blackened ridges, rows 1-3 the sides), x 12-14 rows 12-14 the hollow end: a pale
    pasta rim round a dark centre."""
    a = np.zeros((16, 16, 4), np.uint8)
    a[..., 3] = 255
    a[:, :, :3] = hx("#d08038")
    for x in range(16):
        a[0, x, :3] = hx("#2e160c" if x % 3 == 1 else "#5a2a12" if x % 5 == 0 else "#f2c47a")
        a[1, x, :3] = hx("#e8a050")
        a[2, x, :3] = hx("#d08038")
        a[3, x, :3] = hx("#b06028")
    for y in range(12, 15):
        for x in range(12, 15):
            a[y, x, :3] = hx("#3a1a0c" if (x, y) == (13, 13) else "#f2a862" if y == 12 or x == 12 else "#e8c48a")
    return a


TOP_UV, SIDE_UV, END_UV = [0, 0, 3, 1], [0, 1, 3, 3], [12, 12, 15, 15]
BODY_UV = SIDE_UV
# per portion (x0, z0 = its corner, 6 x 4): small tubes, 1 x 1 across, 2.8-3 long: (from, to, along, rotation)
PENNE = [
    ([0.6, 5, 0.6], [3.4, 6, 1.6], "x", {"axis": "y", "angle": 22.5}),
    ([4.2, 5, 0.4], [5.2, 6, 3.2], "z", {"axis": "x", "angle": 22.5}),        # one end lifted
    ([1.0, 5, 2.4], [3.8, 6, 3.4], "x", {"axis": "z", "angle": -22.5}),       # curling up
    ([2.8, 5, 1.4], [5.6, 6, 2.4], "x", {"axis": "y", "angle": -45}),
    ([0.4, 5, 1.2], [1.4, 6, 3.8], "z", {"axis": "x", "angle": -22.5}),
]


def penne(eaten, per=8):
    """About 8 small tubes per portion (owner: "there arent enough penne"): 1 x 1 across, about 3 long, lying along x
    or z, some stacked half a pixel higher, at varied yaws and lifts; the same layout every eaten state."""
    gone = set(ORDER[:eaten])
    rs = np.random.RandomState(41)
    rots = [("y", 22.5), ("y", -22.5), ("y", 45), ("y", -45), ("x", 22.5), ("x", -22.5), ("z", 22.5), ("z", -22.5)]
    e = []
    for i, (c, r) in enumerate(ORDER):
        x0, z0 = XS[c], ZS[r]
        for j in range(per):
            along = "x" if rs.rand() < 0.6 else "z"
            L = 2.6 + rs.rand() * 0.6
            y = 5 + (0.6 if j >= per - 3 else 0)                 # the last few stacked on the others
            if along == "x":
                fx, fz = x0 + 0.3 + rs.rand() * (6 - L - 0.6), z0 + 0.2 + rs.rand() * 2.6
                fr, to = [fx, y, fz], [fx + L, y + 1, fz + 1]
            else:
                fx, fz = x0 + 0.2 + rs.rand() * 4.6, z0 + 0.2 + rs.rand() * (4 - L - 0.4)
                fr, to = [fx, y, fz], [fx + 1, y + 1, fz + L]
            axis, angle = rots[rs.randint(0, len(rots))]
            if (c, r) in gone:
                continue
            fr, to = [round(v, 2) for v in fr], [round(v, 2) for v in to]
            ends = ("east", "west") if along == "x" else ("north", "south")
            faces = {k: {"uv": END_UV if k in ends else TOP_UV if k == "up" else SIDE_UV, "texture": "#penne"}
                     for k in ("north", "south", "east", "west", "up", "down")}
            e.append({"from": fr, "to": to, "faces": faces,
                      "rotation": {"origin": [round((fr[0] + to[0]) / 2, 2), y, round((fr[2] + to[2]) / 2, 2)],
                                   "axis": axis, "angle": angle}})
    return e


def penne_top_v4():
    """A dense layer of flat-lying penne (owner: "the top orange is quite terribly flat"): many small tubes, light on
    top and dark underneath so they read round, in gold, orange and red-orange, dark sauce between, charred patches
    and blackened tube edges; colours from the owner's close-up."""
    rs = np.random.RandomState(42)
    a = noise_tex("#8a3a1c", [("#a84a24", 0.4), ("#6a2c14", 0.2)], 43)      # sauce between
    tones = (("#f4c87e", "#d89048", "#a85a24"), ("#eaa058", "#c06a30", "#8a4018"),
             ("#dc7c40", "#a85028", "#6e2c14"))
    dirs = ((1, 0, 0, 1), (0, 1, 1, 0), (1, 1, 1, -1), (1, -1, 1, 1))     # step, and the "underside" offset
    for _ in range(30):
        x, y = rs.randint(0, 16), rs.randint(0, 16)
        dx, dy, ox, oy = dirs[rs.randint(0, 4)]
        hi, mid, lo = tones[rs.randint(0, 3)]
        n = rs.randint(3, 6)
        for i in range(n):
            px, py = (x + dx * i) % 16, (y + dy * i) % 16
            qx, qy = (px + ox) % 16, (py + oy) % 16
            a[py, px, :3] = hx(hi if i < n - 1 else mid)
            a[qy, qx, :3] = hx(lo)
            if i == n - 1 and rs.rand() < 0.5:
                a[py, px, :3] = hx("#2e160c")                         # a blackened tube edge
    for _ in range(9):                                                   # charred patches
        x, y = rs.randint(0, 16), rs.randint(0, 16)
        for ddx, ddy in ((0, 0), (1, 0), (0, 1), (1, 1)):
            if rs.rand() < 0.7:
                a[(y + ddy) % 16, (x + ddx) % 16, :3] = hx("#2e160c" if rs.rand() < 0.5 else "#5a2a12")
    return a


def penne_inside_v4():
    """The plated portion seen from the side: mostly pale orange pasta, tubes cut on the slant as short pale dashes with
    darker sauce lines between, all leaning the same way; a charred top band (row 11 is the top of the face in the
    model, rows 0-1 too) and a paler bound base."""
    a = np.zeros((16, 16, 4), np.uint8)
    a[..., 3] = 255
    for y in range(16):
        for x in range(16):
            k = (x + 2 * y) % 5
            col = "#a84a24" if k == 0 else "#f2cf94" if k == 2 else "#e0a060"
            if k == 3 and (x - y) % 4 == 0:
                col = "#c8602a"                       # a tube's open end
            if (x * 7 + y * 3) % 23 == 0:
                col = "#6a3018"                       # mince
            a[y, x, :3] = hx(col)
    for row in (0, 1, 11):
        for x in range(16):
            a[row, x, :3] = hx("#2e160c" if (x + row) % 3 == 0 else "#5a2a12" if (x + row) % 3 == 1 else "#b06028")
    for x in range(16):
        a[15, x, :3] = hx("#f0d090" if x % 3 else "#e0a060")
    return a


ICON_V4_PAL = dict(ICON3_PAL, **{
    "O": hx("#4a463e"), "o": hx("#6a665e"), "H": hx("#f8f6f0"), "m": hx("#e4e0d6"), "n": hx("#8a867c"),
    "f": hx("#d4d0c6"), "w": hx("#bdb9af"), "W": hx("#a9a59b"), "v": hx("#959187"), "k": hx("#807c74"),
    "L": hx("#f6c47a"), "r": hx("#e09a48"), "R": hx("#b86a2c"), "g": hx("#fadc9a")})
IMQ_ICON4 = [r.replace("mwwWwwWwwWwk", "mwwwwwwwwwwk") for r in ROSS_V5]   # smooth glazed wall, no foil pleats


# ---- Icon v5 (owner: "too exact to the original ross il-forn ... definitely should look more burnt") ----
ICON_V5_PAL = dict(ICON_V4_PAL, **{"T": hx("#f4c87e"), "t": hx("#d89048"), "q": hx("#a85a24"), "S": hx("#8a3a1c"),
                                   "z": hx("#2e160c"), "Z": hx("#5a2a12")})


def penne_food(w, h, seed, lift=0):
    """w x h of jumbled little penne seen from above: diagonal 3-px tubes (lit top T, body t, dark underside q), a
    blackened end, dark-brown crust patches; more char towards the bottom right (light from the top left)."""
    rs = np.random.RandomState(seed)
    g = [["S"] * w for _ in range(h)]
    for _ in range(w * h // 4):
        x, y = rs.randint(-1, w), rs.randint(-1, h)
        d = 1 if rs.rand() < 0.6 else -1
        for i in range(3):
            px, py = x + i, y + i * d
            if 0 <= px < w and 0 <= py < h:
                g[py][px] = "z" if i == 2 and rs.rand() < 0.7 else ("T" if i == 0 else "t")
            if 0 <= px < w and 0 <= py + 1 < h and i < 2 and g[py + 1][px] == "S":
                g[py + 1][px] = "q"
    cells = [(x, y) for y in range(h) for x in range(w)]
    dark = lambda: sum(g[y][x] in "zZS" for x, y in cells) / len(cells)
    while dark() < 0.36:
        x, y = rs.randint(0, w), rs.randint(0, h)
        if rs.rand() < 0.35 + 0.5 * (x / w + y / h) / 2:        # crust patches lean to the bottom right
            g[y][x] = "Z" if rs.rand() < 0.5 else "z"
    for x, y in ((0, 0), (1, 0), (0, 1)):                       # the lit corner keeps pale pasta
        g[y][x] = "T"
    return ["".join(r) for r in g]


def with_food(base, food, top):
    rows = [list(r) for r in base]
    for j, fr in enumerate(food):
        for i, c in enumerate(fr):
            rows[top + j][3 + i] = c
    return ["".join(r) for r in rows]


IMQ_V5A = with_food(IMQ_ICON4, penne_food(10, 6, 51), 3)
IMQ_V5B = with_food(IMQ_ICON4, penne_food(10, 7, 103), 2)      # heaped: the middle rises over the back rim
IMQ_V5B[1] = ".OOOOOOOOOOOOOO."
IMQ_V5B[2] = IMQ_ICON4[2][:5] + IMQ_V5B[2][5:11] + IMQ_ICON4[2][11:]


def imqarrun_icon_compare():
    ims = []
    for n, rows in (("v5a", IMQ_V5A), ("v5b", IMQ_V5B)):
        im = F.render(relight(rows), ICON_V5_PAL)
        im.save(os.path.join(F.OUT, f"imqarrun_icon_{n}.png"))
        ims.append(("Imqarrun il-forn " + n, im))
    ims.append(("Ross il-forn (installed)", Image.open(os.path.join(TEX, "item", "ross_il_forn.png")).convert("RGBA")))
    for v in ("cake", "pumpkin_pie"):
        ims.append(("vanilla " + v, Image.open(os.path.join(F.VANILLA, v + ".png")).convert("RGBA")))
    F.compare(ims).save(os.path.join(F.OUT, "imqarrun_icon_compare.png"))


def imqarrun():
    save_png(penne_top_v4(), "block/imqarrun_il_forn_top.png")
    save_png(dish_side(), "block/imqarrun_il_forn_side.png")
    save_png(penne_inside_v4(), "block/imqarrun_il_forn_inside.png")
    save_png(dish_bottom(), "block/imqarrun_il_forn_bottom.png")
    save_png(penne_tex(), "block/imqarrun_il_forn_penne.png")
    F.render(relight(IMQ_V5A), ICON_V5_PAL).save(os.path.join(TEX, "item", "imqarrun_il_forn.png"))  # accepted: v5a
    F.render(relight(IMQ_ICON4), ICON_V4_PAL).save(os.path.join(F.OUT, "imqarrun_icon_v4.png"))
    save_png(dish_handle(), "block/imqarrun_il_forn_handle.png")
    models("imqarrun_il_forn", extra=penne, handles=True)


def imqarrun_compare():
    ims = icon_v3_compare()
    ims = [("Imqarrun il-forn v4", Image.open(os.path.join(F.OUT, "imqarrun_icon_v4.png")).convert("RGBA"))] + \
        [i for i in ims if i[0].startswith(("Ross", "vanilla"))]
    for v in ("cake", "pumpkin_pie"):
        ims.append(("vanilla " + v, Image.open(os.path.join(F.VANILLA, v + ".png")).convert("RGBA")))
    sheet = F.compare(ims)
    shots = os.path.join(F.OUT, "ingame_imqarrun_v6")
    crops = []
    if os.path.isdir(shots):
        for key in ("14-imqarrun-table", "14b-imqarrun-above"):
            fs = [f for f in sorted(os.listdir(shots)) if key + ".png" in f]
            if fs:
                im = Image.open(os.path.join(shots, fs[0])).convert("RGBA")
                crops.append(im)
                if key.endswith("above"):                 # a close crop of the dish tops, 3x
                    w, h = im.size
                    c = im.crop((int(w * 0.08), int(h * 0.27), int(w * 0.70), int(h * 0.47)))
                    crops.append(c.resize((c.width * 3 // 2, c.height * 3 // 2), Image.NEAREST))
    H = sheet.height + sum(c.height + 8 for c in crops)
    out = Image.new("RGBA", (max([sheet.width] + [c.width for c in crops]), H), (198, 198, 198, 255))
    out.alpha_composite(sheet, (0, 0))
    y = sheet.height + 8
    for c in crops:
        out.alpha_composite(c, (0, y))
        y += c.height + 8
    out.save(os.path.join(F.OUT, "imqarrun_compare.png"))


# ---- Timpana (owner: "the exact same as imqarrun, but baked in pie crust. use a clear glass dish ... the top and sides
# from the outside (its glass so see through) should also have the pastry"); photo art/references/oven_owner/timpana/
# (reference only): a thick golden blistered shortcrust lid, a pale pastry wall down the sides and base, the imqarrun
# penne and mince inside. ----
PASTRY = {"pale": "#ecd29a", "lit": "#f6e4b8", "gold": "#d8a85e", "brown": "#b87a3a", "mark": "#9a6a34",
          "crimp": "#c8904a"}
GLASS = {"rim": "#eef8f8", "streak": "#f4fcfc", "tint": "#d6dcc0", "tint2": "#c8d0b4", "edge": "#a8bcb8"}


def pastry_lid():
    """The lid seen from above (the portions' top faces use x 2-13, z 2-13): pale shortcrust with golden-brown baked
    patches and blisters, a few fork marks, a crimped edge round the dish."""
    rs = np.random.RandomState(61)
    a = noise_tex(PASTRY["pale"], [(PASTRY["lit"], 0.18), (PASTRY["gold"], 0.2), (PASTRY["brown"], 0.07)], 62)
    for _ in range(6):                                          # baked patches
        x, y = rs.randint(2, 13), rs.randint(2, 13)
        for ddx, ddy in ((0, 0), (1, 0), (0, 1), (1, 1), (-1, 0)):
            a[(y + ddy) % 16, (x + ddx) % 16, :3] = hx(PASTRY["gold"] if rs.rand() < 0.7 else PASTRY["brown"])
    for x, y in ((5, 5), (5, 6), (10, 9), (10, 10), (7, 11), (8, 11), (11, 4), (11, 5)):   # fork marks / vents
        a[y, x, :3] = hx(PASTRY["mark"])
    for i in range(2, 14):                                      # crimped edge
        col = hx(PASTRY["crimp"] if i % 2 else PASTRY["lit"])
        a[2, i, :3] = a[13, i, :3] = a[i, 2, :3] = a[i, 13, :3] = col
    return a


def glass_wall():
    """The glass wall (rows 11-15 used; row 11 the rim): pale pastry seen through a faintly cyan glass, a glassy rim
    and diagonal highlight streaks."""
    a = noise_tex(GLASS["tint"], [(GLASS["tint2"], 0.3)], 63)
    a[11, :, :3] = hx(GLASS["rim"])
    a[15, :, :3] = hx(GLASS["edge"])
    for x in range(16):
        for y in range(12, 15):
            if (x + y) % 7 == 0:
                a[y, x, :3] = hx(GLASS["streak"])
    return a


def glass_bottom():
    return noise_tex(GLASS["tint"], [(GLASS["tint2"], 0.25), (GLASS["streak"], 0.1)], 64)


def timpana_inside():
    """The imqarrun cut face with a ~2-px pastry lid at the top of the face (rows 11-12), a 1-px pastry base (row 15)
    and 1-px pastry walls at the dish's sides (columns 2 and 13)."""
    a = penne_inside_v4()
    for x in range(16):
        a[11, x, :3] = hx(PASTRY["gold"] if x % 3 else PASTRY["brown"])
        a[12, x, :3] = hx(PASTRY["pale"])
        a[15, x, :3] = hx(PASTRY["pale"])
    for y in range(11, 16):
        for x in (2, 13):
            a[y, x, :3] = hx(PASTRY["pale"] if y > 11 else PASTRY["gold"])
    return a


TIMP_PAL = dict(ICON3_PAL, **{
    "O": hx("#46585a"), "o": hx("#6a7e80"), "H": hx("#f2fafa"), "m": hx("#d4e4e2"), "n": hx("#8aa2a0"),
    "f": hx("#d0d8c0"), "w": hx("#d8d0a0"), "W": hx("#c2b888"), "v": hx("#aca478"), "k": hx("#8e8c70"),
    "L": hx(PASTRY["lit"]), "r": hx(PASTRY["pale"]), "R": hx(PASTRY["gold"]), "x": hx(PASTRY["mark"]),
    "g": hx("#fff2cc"), "M": hx(PASTRY["brown"])})
TIMP_LID = ["RLRLRLRLRL",
            "LrrgrrRrrR",
            "RrgrxrrRrL",
            "LrrrxrRRrR",
            "RrRrrrgRMM",
            "MRMRMRMRMR"]
TIMP_ICON = with_food(IMQ_ICON4, TIMP_LID, 3)


# v2 (owner: "from the sides the pastry reads as green through the glass. on top, the crust doesnt really look like
# crust just streaks, the icons dotting is too uniform")
def pastry_lid_v2():
    """A thick shortcrust lid: pale cream-gold with irregular rounded golden-brown blotches (darker in the middle),
    small blisters (light, darker beneath), a few cracks, two vent slits, a thumbed/crimped rim."""
    rs = np.random.RandomState(71)
    a = noise_tex("#ecd29a", [("#f2dcaa", 0.25), ("#e2c286", 0.15)], 72)
    for _ in range(7):                                          # baked blotches
        cx, cy, r = 3 + rs.rand() * 10, 3 + rs.rand() * 10, 1.4 + rs.rand() * 1.8
        for y in range(16):
            for x in range(16):
                d = np.hypot(x + .5 - cx, (y + .5 - cy) * (0.8 + rs.rand() * 0.4))
                if d < r * 0.45:
                    a[y, x, :3] = hx("#b07034")
                elif d < r * 0.8:
                    a[y, x, :3] = hx("#c8904a")
                elif d < r and rs.rand() < 0.6:
                    a[y, x, :3] = hx("#dcae66")
    for _ in range(7):                                          # blisters
        x, y = rs.randint(3, 13), rs.randint(3, 12)
        a[y, x, :3] = hx("#fbefcc")
        a[y + 1, x, :3] = hx("#c8944e")
    for pts in (((5, 9), (6, 10), (6, 11)), ((10, 4), (11, 5))):  # cracks
        for x, y in pts:
            a[y, x, :3] = hx("#9a6a34")
    for x, y in ((7, 6), (8, 6), (9, 9), (10, 9)):             # vent slits
        a[y, x, :3] = hx("#7a4a22")
    for i in range(2, 14):                                      # thumbed rim: two light, one dark
        col = hx("#c8904a" if i % 3 == 0 else "#f2dcaa")
        a[2, i, :3] = a[13, i, :3] = a[i, 2, :3] = a[i, 13, :3] = col
    return a


def glass_wall_v2():
    """Warm pastry seen through clear glass: cream-gold, golden-brown where it baked against the glass (lower rows);
    the glass only as a pale rim line, a cool base edge and two near-white vertical streaks."""
    a = noise_tex("#e6cc94", [("#dcb878", 0.3), ("#f0daa8", 0.15)], 73)
    rs = np.random.RandomState(74)
    for y in (13, 14):
        for x in range(16):
            if rs.rand() < 0.45:
                a[y, x, :3] = hx("#c08848")
    a[11, :, :3] = hx("#f4f8f6")
    a[15, :, :3] = hx("#d8e0dc")
    for x in (3, 4, 11):
        for y in (12, 13, 14):
            if not (x == 4 and y == 14):
                a[y, x, :3] = hx("#fbfcf6")
    return a


TIMP_PAL2 = dict(TIMP_PAL, **{"w": hx("#e2c890"), "W": hx("#cbb07a"), "v": hx("#b49a68"), "k": hx("#988458"),
                              "f": hx("#e4e8de"), "r": hx("#ecd29a"), "R": hx("#c8904a"), "M": hx("#a86c32"),
                              "L": hx("#f6e4b8"), "g": hx("#fdf2d0")})
TIMP_LID2 = ["LRLLRLLRLR",
             "LrRRrrrgrL",
             "RRMRrgrrrR",
             "LrRrrRrrRL",
             "RrrrRMRrrR",
             "MRMMRMRMMR"]
TIMP_ICON2 = with_food(IMQ_ICON4, TIMP_LID2, 3)


def glass_wall_v3():
    """v2's warm pastry and rim/base lines, with v1's short diagonal glass streaks (bottom-left to top-right) back
    (owner: "the classic vanilla glass streeks are replaced by whatever these lines are")."""
    a = noise_tex("#e6cc94", [("#dcb878", 0.3), ("#f0daa8", 0.15)], 73)
    rs = np.random.RandomState(74)
    for y in (13, 14):
        for x in range(16):
            if rs.rand() < 0.45:
                a[y, x, :3] = hx("#c08848")
    a[11, :, :3] = hx("#f4f8f6")
    a[15, :, :3] = hx("#d8e0dc")
    for x in range(16):
        for y in range(12, 15):
            if (x + y) % 7 == 0:
                a[y, x, :3] = hx("#fbfcf6")
    return a


def timpana():
    save_png(pastry_lid_v2(), "block/timpana_top.png")
    save_png(glass_wall_v3(), "block/timpana_side.png")
    save_png(timpana_inside(), "block/timpana_inside.png")
    save_png(glass_bottom(), "block/timpana_bottom.png")
    F.render(relight(TIMP_ICON2), TIMP_PAL2).save(os.path.join(TEX, "item", "timpana.png"))
    models("timpana")


def timpana_compare():
    ims = [("Timpana", Image.open(os.path.join(TEX, "item", "timpana.png")).convert("RGBA"))]
    for n, lbl in (("ross_il_forn", "Ross il-forn"), ("imqarrun_il_forn", "Imqarrun il-forn")):
        ims.append((lbl, Image.open(os.path.join(TEX, "item", n + ".png")).convert("RGBA")))
    for v in ("cake", "pumpkin_pie"):
        ims.append(("vanilla " + v, Image.open(os.path.join(F.VANILLA, v + ".png")).convert("RGBA")))
    sheet = F.compare(ims)
    shots = os.path.join(F.OUT, "ingame_timpana_v3")
    crops = []
    if os.path.isdir(shots):
        for key in ("15-timpana-table", "15b-timpana-above"):
            fs = [f for f in sorted(os.listdir(shots)) if key + ".png" in f]
            if fs:
                im = Image.open(os.path.join(shots, fs[0])).convert("RGBA")
                w, h = im.size
                c = im.crop((0, int(h * 0.25), w, int(h * 0.62)))
                crops.append(c)
                cc = im.crop((0, int(h * 0.30), int(w * 0.5), int(h * 0.55)))   # close: the whole dish's top and side
                crops.append(cc.resize((cc.width * 2, cc.height * 2), Image.NEAREST))
    out = Image.new("RGBA", (max([sheet.width] + [c.width for c in crops]),
                             sheet.height + sum(c.height + 8 for c in crops)), (198, 198, 198, 255))
    out.alpha_composite(sheet, (0, 0))
    y = sheet.height + 8
    for c in crops:
        out.alpha_composite(c, (0, y))
        y += c.height + 8
    out.save(os.path.join(F.OUT, "timpana_compare.png"))


# ---- Torta tal-lampuki (owner's photos and recipe, art/references/oven_owner/torta_lampuki/, reference only): a round
# double-crusted pie, golden egg-washed shortcrust lid (sometimes sesame), crimped edge, on a plate or in a round pan;
# the cut face: dark-green spinach, white flaked fish, cauliflower, black olives, peas, capers, a little carrot,
# between a top and a bottom crust. Placed: a round pie (a stepped circle) on a round white plate, eaten in six
# wedges, each a sector made of boxes. ----
CX, CZ, PIE_R, PIE_Y0, PIE_Y1 = 8.0, 8.0, 5.8, 0.5, 4.5


def torta_cells():
    """{(x, z): sector} for the 1x1 cells of the pie; sector 0 faces north (the side facing the player), then
    clockwise."""
    cells = {}
    for z in range(16):
        for x in range(16):
            dx, dz = x + .5 - CX, z + .5 - CZ
            if dx * dx + dz * dz <= PIE_R * PIE_R:
                ang = (math.degrees(math.atan2(dx, -dz)) + 30) % 360
                cells[(x, z)] = int(ang // 60)
    return cells


def check_torta_faces():
    """Test: in every eaten state, a wedge face uses the filling ("inside") only where every cell it faces belongs to
    an eaten wedge, and the crust ("side") only where every cell it faces is outside the pie."""
    cells = torta_cells()
    step = {"north": (0, -1), "south": (0, 1), "west": (-1, 0), "east": (1, 0)}
    bad = []
    for n in range(6):
        for b in torta_elements(n):
            if b["from"][1] != PIE_Y0:
                continue
            (x0, _, z0), (x1, _, z1) = b["from"], b["to"]
            for d, f in b["faces"].items():
                if d not in step:
                    continue
                dx, dz = step[d]
                nbs = ([(x, z0 - 1 if dz < 0 else z1) for x in range(int(x0), int(x1))] if dz else
                       [(x0 - 1 if dx < 0 else x1, z) for z in range(int(z0), int(z1))])
                t = f["texture"]
                ok = (all(c in cells for c in nbs) and any(cells[c] < n for c in nbs) if t == "#inside" else
                      not any(c in cells and cells[c] < n for c in nbs))
                if not ok:
                    bad.append((n, b["from"], d, t))
    assert not bad, bad
    return True


def torta_dish():
    """A round terracotta pie dish (owner: "can we have the pie in a dish"): a floor and a low octagonal rim (four
    straight walls plus the north and south walls turned 45 degrees about the centre for the diagonals) = 10 elements."""
    D = {k: "plate" for k in ("north", "south", "east", "west", "up", "down")}
    e = [P.box([2, 0, 4], [14, 0.5, 12], D), P.box([4, 0, 2], [12, 0.5, 14], D)]
    n = P.box([5.1, 0, 1], [10.9, 2, 2], D)
    s_ = P.box([5.1, 0, 14], [10.9, 2, 15], D)
    e += [n, s_, P.box([1, 0, 5.1], [2, 2, 10.9], D), P.box([14, 0, 5.1], [15, 2, 10.9], D)]
    for b in (n, s_):
        for ang in (45, -45):
            r = json.loads(json.dumps(b))
            r["rotation"] = {"origin": [8, 1, 8], "axis": "y", "angle": ang}
            e.append(r)
    return e


def torta_elements(eaten):
    cells = torta_cells()
    gone = set(range(eaten))
    keep = {c: k for c, k in cells.items() if k not in gone}
    e = torta_dish()

    def face(nb):
        if nb in keep:
            return None
        return "inside" if nb in cells else "side"
    for k in sorted(set(keep.values())):
        for z in range(16):
            xs = sorted(x for (x, zz), kk in keep.items() if zz == z and kk == k)
            runs, run = [], []
            for x in xs:   # a run also breaks where its north or south face changes kind (owner: green seen from
                # outside, when one box's face ran along both a cut and the outer crust)
                if run and (x != run[-1] + 1 or any({face((xx, z + dz)) for xx in run + [x]} >= {"inside", "side"}
                                                    for dz in (-1, 1))):
                    runs.append(run)
                    run = []
                run.append(x)
            if run:
                runs.append(run)
            for run in runs:
                x0, x1 = run[0], run[-1] + 1
                faces = {"up": "top"}
                for d, nbs in (("north", [(x, z - 1) for x in run]), ("south", [(x, z + 1) for x in run]),
                               ("west", [(x0 - 1, z)]), ("east", [(x1, z)])):
                    kinds = {face(nb) for nb in nbs}   # a kept neighbour hides its part of the face
                    assert not kinds >= {"inside", "side"}, (eaten, z, run, d)
                    if "inside" in kinds:
                        faces[d] = "inside"
                    elif "side" in kinds:
                        faces[d] = "side"
                b = P.box([x0, PIE_Y0, z], [x1, PIE_Y1, z + 1], faces)
                for d, f in b["faces"].items():
                    if d != "up":
                        f["uv"] = [f["uv"][0], f["uv"][1] - .5, f["uv"][2], f["uv"][3] - .5]
                e.append(b)
    return e


def torta_top():
    """Even, warm golden egg-washed shortcrust (critic v2): a few sesame specks, two short steam slits, a darker
    crimped ring at the edge."""
    rs = np.random.RandomState(81)
    a = noise_tex("#dca044", [("#e4ac52", 0.18), ("#d09238", 0.12)], 82)
    for y in range(16):
        for x in range(16):
            d = math.hypot(x + .5 - CX, y + .5 - CZ)
            if PIE_R - 1.2 < d <= PIE_R + .5:
                ang = math.degrees(math.atan2(x + .5 - CX, y + .5 - CZ))
                a[y, x, :3] = hx("#c08030" if int((ang + 360) // 24) % 2 else "#a4682a")   # crimped folds
    for x, y in ((8, 6), (8, 7), (6, 9), (10, 9)):                                         # steam slits
        a[y, x, :3] = hx("#8a5424")
    n = 0
    while n < 7:                                                                            # sesame
        x, y = rs.randint(3, 13), rs.randint(3, 13)
        if math.hypot(x + .5 - CX, y + .5 - CZ) < PIE_R - 1.5 and tuple(a[y, x, :3]) != tuple(hx("#8a5424")):
            a[y, x, :3] = hx("#f6e2b0")
            n += 1
    return a


def torta_side():
    """The pie's outer crust (rows 11-15 used): golden-brown, the lid's crimped edge on top, darker at the base."""
    a = noise_tex("#c88a3c", [("#d4984a", 0.2), ("#b87a32", 0.15)], 85)
    for x in range(16):
        a[11, x, :3] = hx("#dca044" if x % 2 else "#a4682a")
    a[15, :, :3] = hx("#9e6428")
    return a


def torta_inside():
    """The cut face (rows 11-15 used): a 2 px golden top crust, 2 px of filling (dark spinach with tan flaked lampuki,
    a black olive, a pea, a fleck of carrot), a 1 px bottom crust."""
    a = noise_tex("#3a5222", [("#b8946a", 0.22), ("#c4a878", 0.3), ("#a88c60", 0.14), ("#2a3c18", 0.12), ("#22201c", 0.05),
                              ("#78a040", 0.04), ("#d0742a", 0.02)], 83)
    a[11, :, :3] = hx("#d89c48")      # owner: "crust is too thick on top" -> a 1 px top crust
    a[15, :, :3] = hx("#b07434")
    return a


def plate_tex():
    """The terracotta pie dish (the borma's clay family): a glazed, slightly lighter top edge."""
    a = noise_tex("#9c5c40", [("#a46646", 0.3), ("#885036", 0.15)], 84)
    a[14, :, :3] = hx("#ae704a")
    return a


TORTA_PAL = {"O": hx("#5e3c1c"), "o": hx("#74502a"), "L": hx("#f0c470"), "l": hx("#e0a84e"), "m": hx("#cc9040"),
             "d": hx("#a86c2c"), "D": hx("#8c5824"), "x": hx("#6e4220"), "s": hx("#f8e8c0"),
             "P": hx("#ae704a"), "p": hx("#9c5c40"), "q": hx("#824834"), "Q": hx("#6a3a26"), "r": hx("#8a4c32")}

# critic v2: a shallow pie (lid 5 px, 14 px wide) in the terracotta dish (2 px rim), a closed lid with three sesame
# seeds and one 2 px steam slit, the crimp only along the front edge
TORTA_ICON2 = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "...oooooooooo...",
    "..oLlLsLLllllO..",
    ".oLlLLlxxllslmO.",
    ".oLsllllllllmmO.",
    "oLdLdldldldmdmmO",
    "oPpppppppppppppO",
    "oPpppppppppppppO",
    ".oPppppppppppqO.",
    "..oqqqqqqqqqqO..",
    "....OOOOOOOO....",
    "................",
]


def torta_icon():
    return TORTA_ICON2[2:] + TORTA_ICON2[:2]


# owner: "make the icon more similar to the timpana ross il forn etc in style but rounded instead inside of the dish":
# the dish icons' framing, rim and front wall, rounded into an oval terracotta pie dish, a thin golden lid inside
TORTA_PAL3 = {"O": hx("#623a26"), "o": hx("#8a583c"), "H": hx("#c08060"), "m": hx("#a86a4c"), "n": hx("#7c4630"),
              "f": hx("#b47454"), "w": hx("#9c5c40"), "W": hx("#884e36"), "v": hx("#74422e"), "k": hx("#6c3a28"),
              "L": hx("#f0c470"), "r": hx("#e0a84e"), "R": hx("#c08030"), "M": hx("#a86c2c"), "g": hx("#f8e8c0"),
              "x": hx("#6e4220")}
TORTA_ICON3 = [
    "................",
    "...OOOOOOOOOO...",
    ".OOHHHHHHHmmmOO.",
    ".OHRLLRLLRLLRnO.",
    "OHLLrrrgrrrrrLnO",
    "OHRLgrrrrrrrrRnO",
    "OHLrrrrxxrrrrLnO",
    "OHRrrgrrrrrrrRnO",
    "OHLrrrrrrrgrrLnO",
    ".OHRMRMRMRMRMnO.",
    ".OmffffffffffnO.",
    ".OmwwwwwwwwwwkO.",
    "..OmwwwwwwwwkO..",
    "...OOOOOOOOOO...",
    "................",
    "................",
]


# owner: "looks like a soup in the dish in the icon": the lid now rises as a low dome above the dish rim, a dry
# blistered pastry (light blisters top-left, baked patches), crimped all round over the rim, short dark slits,
# sesame; no darker ring inside the rim. Two variants for the owner.
TORTA_PAL4 = dict(TORTA_PAL3, **{"B": hx("#f8d890"), "L": hx("#ecc06a"), "r": hx("#dca44c"), "R": hx("#bc8236"),
                                 "M": hx("#a06a2c"), "x": hx("#5a3418"), "g": hx("#fbefcc"), "Y": hx("#6e4422")})
TORTA_ICON_PICK = "a"


def torta_icon4(variant):
    """The pie (narrower than the dish, so the rim shows each side) domes 1-2 px above the dish's back rim."""
    rs = np.random.RandomState(91 if variant == "a" else 92)
    g = [list(r) for r in TORTA_ICON3]
    for y in range(16):                                                # the template's lid becomes the rim's top
        for x in range(16):
            if g[y][x] in "LrRMgx":
                g[y][x] = "m"
    cy, ry = (5.0, 4.7) if variant == "a" else (5.3, 4.4)
    lid = {}
    for y in range(16):
        for x in range(16):
            u, v = (x + .5 - 8) / 5.7, (y + .5 - cy) / ry
            if u * u + v * v <= 1:
                lid[(x, y)] = (u, v)
    for (x, y), (u, v) in lid.items():
        r = math.hypot(u, v)
        k = -0.6 * u - 0.6 * v
        if r > 0.74 and v > -0.3:                                      # crimp over the rim, alternating
            c = ("B" if k > 0 else "L") if x % 2 else ("R" if k > -0.2 else "M")
        else:
            c = "B" if k > 0.8 else "L" if k > 0.35 else "r" if k > -0.5 else "R"
            n = rs.rand()
            if n < 0.18:
                c = {"B": "L", "L": "r", "r": "R", "R": "M"}[c]          # baked patches
            elif n > 0.9 and k > -0.2:
                c = "B"                                                # blisters
        g[y][x] = c
    for (x, y), (u, v) in lid.items():                                 # outline where the dome stands free
        if v < 0 and any((x + dx, y + dy) not in lid and g[y + dy][x + dx] in ".O"
                         for dx, dy in ((0, -1), (-1, 0), (1, 0))):
            g[y][x] = "O"
    for y in range(16):                                                # a dish outline pixel next to the dome's top
        for x in range(16):
            if g[y][x] == "." and any((x + dx, y + dy) in lid and g[y + dy][x + dx] != "O"
                                      for dx, dy in ((0, 1), (1, 0), (-1, 0))):
                g[y][x] = "O"
    slits = [(7, 3), (8, 3)] if variant == "a" else [(6, 4), (6, 5), (10, 4), (10, 5)]
    seeds = [(5, 5), (10, 2), (11, 6), (8, 6)] if variant == "a" else [(8, 2), (4, 6), (12, 4)]
    for x, y in slits:
        g[y][x] = "x"
    for x, y in seeds:
        g[y][x] = "g"
    return ["".join(r) for r in g]


def torta_icons():
    ims = {}
    for v in ("a", "b"):
        im = F.render(relight(torta_icon4(v)), TORTA_PAL4)
        im.save(os.path.join(F.OUT, f"torta_icon_{v}.png"))
        ims[v] = im
    return ims


def torta():
    check_torta_faces()
    save_png(torta_top(), "block/torta_lampuki_top.png")
    save_png(torta_side(), "block/torta_lampuki_side.png")
    save_png(torta_inside(), "block/torta_lampuki_inside.png")
    save_png(plate_tex(), "block/torta_lampuki_plate.png")
    torta_icons()[TORTA_ICON_PICK].save(os.path.join(TEX, "item", "torta_lampuki.png"))
    name = "torta_lampuki"
    tex = {"particle": f"{NS}:block/{name}_top", "top": f"{NS}:block/{name}_top", "side": f"{NS}:block/{name}_side",
           "inside": f"{NS}:block/{name}_inside", "plate": f"{NS}:block/{name}_plate"}
    for n in range(6):
        P.write(f"models/block/{name}_eaten{n}.json", P.model(torta_elements(n), tex))
    rot = {"north": 0, "east": 90, "south": 180, "west": 270}
    P.write(f"blockstates/{name}.json", {"variants": {
        f"eaten={n},facing={f}": ({"model": f"{NS}:block/{name}_eaten{n}", "y": y} if y else
                                  {"model": f"{NS}:block/{name}_eaten{n}"}) for f, y in rot.items() for n in range(6)}})
    P.write(f"models/item/{name}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/{name}"}})
    P.write(f"items/{name}.json", {"model": {"type": "minecraft:model", "model": f"{NS}:item/{name}"}})


def torta_compare():
    tv = torta_icons()
    ims = [("Torta v5a", tv["a"]), ("Torta v5b", tv["b"])] + [
        (t, Image.open(os.path.join(TEX, "item", n + ".png")).convert("RGBA")) for t, n in (("Timpana", "timpana"), ("Ross il-forn", "ross_il_forn"),
        ("Imqarrun il-forn", "imqarrun_il_forn"))]
    for v in ("pumpkin_pie", "cake"):
        ims.append(("vanilla " + v, Image.open(os.path.join(F.VANILLA, v + ".png")).convert("RGBA")))
    sheet = F.compare(ims)
    shots = os.path.join(F.OUT, "ingame_torta_v5_fix")
    crops = []
    for v in ("a", "b"):                                               # the hotbar with each variant
        d = os.path.join(F.OUT, f"ingame_torta_v5{v}")
        fs = [f for f in sorted(os.listdir(d)) if "13-hotbar-oven" in f] if os.path.isdir(d) else []
        if fs:
            im = Image.open(os.path.join(d, fs[0])).convert("RGBA")
            w, h = im.size
            c = im.crop((w // 2 - 92, h - 46, w // 2 + 92, h))
            crops.append(c.resize((c.width * 3, c.height * 3), Image.NEAREST))
    if os.path.isdir(shots):
        for key in ("16-torta-table", "16b-torta-above"):
            fs = [f for f in sorted(os.listdir(shots)) if key + ".png" in f]
            if fs:
                im = Image.open(os.path.join(shots, fs[0])).convert("RGBA")
                w, h = im.size
                crops.append(im.crop((0, int(h * 0.25), w, int(h * 0.62))))
                if key == "16-torta-table":   # a close crop of the cut face (the pie eaten 2)
                    c = im.crop((int(w * 0.27), int(h * 0.42), int(w * 0.40), int(h * 0.58)))
                    crops.append(c.resize((c.width * 4, c.height * 4), Image.NEAREST))
    out = Image.new("RGBA", (max([sheet.width] + [c.width for c in crops]),
                             sheet.height + sum(c.height + 8 for c in crops)), (198, 198, 198, 255))
    out.alpha_composite(sheet, (0, 0))
    y = sheet.height + 8
    for c in crops:
        out.alpha_composite(c, (0, y))
        y += c.height + 8
    out.save(os.path.join(F.OUT, "torta_compare.png"))


def save_png(a, rel):
    p = os.path.join(TEX, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    Image.fromarray(a, "RGBA").save(p)
    print("wrote", rel)


def compare():
    icon = Image.open(os.path.join(TEX, "item", "ross_il_forn.png")).convert("RGBA")
    ims = [("Ross il-forn", icon)]
    for v in ("cake", "pumpkin_pie"):
        ims.append(("vanilla " + v, Image.open(os.path.join(F.VANILLA, v + ".png")).convert("RGBA")))
    sheet = F.compare(ims)
    shots = os.path.join(F.OUT, "ingame_ross_v2")
    table = [f for f in sorted(os.listdir(shots)) if f.endswith("12-ross-il-forn-table.png")] if os.path.isdir(shots) else []
    if table:
        shot = Image.open(os.path.join(shots, table[0])).convert("RGBA")
        w, h = shot.size
        crop = shot  # the whole shot (the dishes sit near its top edge)
        crop.thumbnail((sheet.width * 2, 600))
        out = Image.new("RGBA", (max(sheet.width, crop.width), sheet.height + crop.height + 8), (198, 198, 198, 255))
        out.alpha_composite(sheet, (0, 0))
        out.alpha_composite(crop, (0, sheet.height + 8))
        sheet = out
    sheet.save(os.path.join(F.OUT, "ross_compare.png"))
    print("wrote ross_compare.png")


def main():
    save_png(top_tex(), "block/ross_il_forn_top.png")
    save_png(side_tex(), "block/ross_il_forn_side.png")
    save_png(inside_tex(), "block/ross_il_forn_inside.png")
    save_png(bottom_tex(), "block/ross_il_forn_bottom.png")
    F.render(relight(ROSS_V6), ICON3_PAL).save(os.path.join(TEX, "item", "ross_il_forn.png"))   # accepted: ross_icon_v6
    models()
    compare()
    icon_compare()
    imqarrun()
    imqarrun_compare()
    ross_icon_compare()
    imqarrun_icon_compare()
    timpana()
    timpana_compare()
    torta()
    torta_compare()


if __name__ == "__main__":
    main()
