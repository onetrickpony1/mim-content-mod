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


def tray():
    S, B = "side", "bottom"
    e = [P.box([1, 0, 1], [15, 1, 15], {"down": B, "up": B, **{k: S for k in P.ALL}})]       # floor
    for f, t, inner in (([1, 1, 1], [15, 5, 2], "south"), ([1, 1, 14], [15, 5, 15], "north"),
                        ([1, 1, 2], [2, 5, 14], "east"), ([14, 1, 2], [15, 5, 14], "west")):
        outer = {"south": "north", "north": "south", "east": "west", "west": "east"}[inner]
        e.append(P.box(f, t, {outer: S, inner: S, "up": B}))
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


def models():
    tex = {"particle": f"{NS}:block/ross_il_forn_top", "top": f"{NS}:block/ross_il_forn_top",
           "side": f"{NS}:block/ross_il_forn_side", "inside": f"{NS}:block/ross_il_forn_inside",
           "bottom": f"{NS}:block/ross_il_forn_bottom"}
    for n in range(6):
        P.write(f"models/block/ross_il_forn_eaten{n}.json", P.model(tray() + rice(n), tex))
    rot = {"north": 0, "east": 90, "south": 180, "west": 270}
    variants = {f"eaten={n},facing={f}": ({"model": f"{NS}:block/ross_il_forn_eaten{n}", "y": y} if y else
                                          {"model": f"{NS}:block/ross_il_forn_eaten{n}"})
                for f, y in rot.items() for n in range(6)}
    P.write("blockstates/ross_il_forn.json", {"variants": variants})
    P.write("models/item/ross_il_forn.json", {"parent": "minecraft:item/generated",
                                               "textures": {"layer0": f"{NS}:item/ross_il_forn"}})
    P.write("items/ross_il_forn.json", {"model": {"type": "minecraft:model", "model": f"{NS}:item/ross_il_forn"}})


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
    F.render(ICON, ICON_PAL).save(os.path.join(TEX, "item", "ross_il_forn.png"))
    models()
    compare()


if __name__ == "__main__":
    main()
