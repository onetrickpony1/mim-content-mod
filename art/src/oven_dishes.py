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


if __name__ == "__main__":
    main()
