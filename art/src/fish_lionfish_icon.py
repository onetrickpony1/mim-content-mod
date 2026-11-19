"""Item icon for the lionfish (Pterois miles): the caught fish, like vanilla cod and salmon.

The 3D model came first (art/src/fish_lionfish_model.py, candidate C, passed by the night critic in round 2), so the
icon follows it: the same features, and the model's palette C lifted about x1.2 for out of the water (the model's
colours are already a step lighter than the photos for the water; an item is seen in daylight).

What makes it a lionfish at 16 px, and not its relative the skorfna (mottled brown, one joined spiny fin) or the
John Dory ("a spiny fish"):
  - bold bands across the whole body, 2 px dark chocolate red-brown then 1 px cream, darker on the back and fading to
    an off-white belly;
  - long SEPARATE spines standing up from the back with clear gaps, banded red-brown and cream;
  - a big fan pectoral under the body sweeping back, its rays banded red-brown and cream over a light red-brown
    membrane, with a fringed rim;
  - a small banded tentacle over the eye; the eye the only black pixel, in pale skin, with a dark cheek bar behind it
    (never touching it);
  - a banded fan tail on a short stalk.
Pose and light follow vanilla's fish items (measured, never copied): head lower left, tail upper right.

Run:  art/.venv/bin/python art/src/fish_lionfish_icon.py
Writes mod/.../textures/item/lionfish.png (byte-identical on rerun), the review sheet
art/candidates/lionfish_icon/sheet.png (candidates at 8x, 1x and 2x beside vanilla cod and salmon, the skorfna and the
pixxi San Pietru) and the offline hotbar previews art/candidates/lionfish_icon/hotbar*.png (no slot selected).
"""
import colorsys
import math
import os
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(ART, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ART, "tools"))
from font import label_font  # noqa: E402
from fish_lionfish_model import PALETTES  # noqa: E402

MODEL_CANDIDATE = "C"   # the model palette the accepted icon was drawn from (owner 2026-11-19: icon accepted)

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
OUT_ICON = os.path.join(TEXTURES, "item", "lionfish.png")
OUT_DIR = os.path.join(ART, "candidates", "lionfish_icon")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
LIFT = 1.2
CHOICE = "A"


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16))


def lifted(c, k):
    h, s, v = colorsys.rgb_to_hsv(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
    r, g, b = colorsys.hsv_to_rgb(h, s, min(1.0, v * k))
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))


def palette():
    m = PALETTES[MODEL_CANDIDATE]
    src = {
        "d": m["d3"], "D": m["d2"], "w": m["d0"],      # the dark bands: back, middle, belly (pinkish)
        "p": m["p3"], "P": m["p1"], "W": m["p0"],      # the cream bands: back (tan), middle, belly
        "q": m["p2"],                                  # the shaded chin
        "E": m["E"], "e": m["e"],                      # the eye, the pale skin round it
        "S": m["S"], "s": m["s"],                      # the spines' bands
        "R": m["R"], "r": m["r"], "F": m["F"],         # fin rays, fan membrane, pale fin
    }
    return {k: (hexc(v) if k == "E" else lifted(hexc(v), LIFT)) for k, v in src.items()}


PAL = palette()

# --- the drawing -----------------------------------------------------------------------------------------------------
# The body, row by row (y: (first x, last x)): an oval on the diagonal, 5-6 px thick, from the snout (2,13) to the
# stalk (12,3). t = x - y runs along the fish from the head (-11) to the stalk (+9), so a band across the fish is a
# run of equal t (a diagonal from upper left to lower right).
BODY = {3: (11, 13), 4: (10, 13), 5: (9, 12), 6: (7, 12), 7: (6, 11), 8: (5, 11), 9: (4, 10), 10: (3, 10),
        11: (2, 9), 12: (2, 8), 13: (2, 6), 14: (3, 4)}
TAIL = {0: (14, 15), 1: (13, 15), 2: (13, 15), 3: (14, 14)}
EYE = (4, 11)


def make(var):
    g = [["."] * 16 for _ in range(16)]

    def put(x, y, c):
        if 0 <= x < 16 and 0 <= y < 16:
            g[y][x] = c

    # the fan: below and behind the head, sweeping back along the belly; rays on the diagonals x + y = 21 and 24
    # (parallel to the body), the pinkish-brown membrane between them; drawn first, the body covers its root
    fan = {9: (11, 11), 10: (11, 12), 11: (10, 13), 12: (9, 13), 13: (7, 12), 14: (8, 10)}
    if var == "C":
        fan = {10: (11, 11), 11: (10, 12), 12: (9, 12), 13: (7, 11), 14: (8, 9)}
    for y, (a, b) in fan.items():
        for x in range(a, b + 1):
            put(x, y, "R" if (x + y) in (21, 24) else "r")
    # the tail: a fan, a red-brown ray band across it
    for y, (a, b) in TAIL.items():
        for x in range(a, b + 1):
            put(x, y, "R" if x - y in (13,) else "F")
    cols = {}
    for y, (a, b) in BODY.items():
        for x in range(a, b + 1):
            cols.setdefault(x - y, []).append(x + y)
    period = 3 if var != "B" else 4
    for y, (a, b) in BODY.items():
        for x in range(a, b + 1):
            t, s = x - y, x + y
            lo, hi = min(cols[t]), max(cols[t])
            rel = (s - lo) / max(1, hi - lo)
            if t == -9 and rel < 0.9:
                c = "d" if rel < 0.3 else "D"                           # a band across the head, before the eye
            elif t <= -6:
                c = "p" if rel < 0.3 else ("P" if rel < 0.8 else "q")    # the head: tan, mid, a shaded chin
            elif t >= 8:
                c = "d" if rel < 0.5 else "D"                           # the stalk
            elif (t + 6) % period < period - 1:
                c = "d" if rel < 0.3 else ("D" if rel < 0.75 else "w")  # a red-brown band
            else:
                c = "p" if rel < 0.3 else ("P" if rel < 0.75 else "W")  # a cream band
            put(x, y, c)
    put(*EYE, "E")
    put(3, 9, "R")                    # the tentacle over the eye: red-brown, a cream tip
    put(3, 8, "s")
    # the separate spines, standing up from the back: red-brown bases, cream tips
    spines = {5: (5, 7), 7: (2, 5), 9: (1, 4)}
    if var == "C":
        spines = {5: (5, 7), 7: (3, 5), 9: (2, 4), 11: (1, 2)}
    for x, (a, b) in spines.items():
        for y in range(a, b + 1):
            put(x, y, "s" if y == a else "S")
    return ["".join(r) for r in g]


CANDIDATES = [(v, make(v)) for v in "ABC"]


def render(rows):
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), PAL[ch] + (255,))
    return im


def check(name, rows):
    """One eye; nothing as dark as the eye anywhere else; no dark band pixel touching the eye."""
    eyes = [(x, y) for y, r in enumerate(rows) for x, c in enumerate(r) if c == "E"]
    assert len(eyes) == 1, (name, eyes)
    ex, ey = eyes[0]
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        c = rows[ey + dy][ex + dx]
        if c in "dDS":
            print(f"warning: {name}: dark {c} touching the eye at {ex + dx},{ey + dy}")


def hotbars(paths):
    py = os.path.join(ART, ".venv", "bin", "python")
    tool = os.path.join(ART, "tools", "hotbar_preview.py")
    T = os.path.join(TEXTURES, "item")
    sets = (("hotbar_x4", ["mc:cod", "file:" + paths[CHOICE], "mod:skorfna", "mc:salmon", "mod:pixxi_san_pietru",
                           "mc:tropical_fish", "mod:cerna", "mc:pufferfish"], "4"),
            ("hotbar", ["mc:cod", "file:" + paths[CHOICE], "mod:skorfna", "mc:salmon", "mod:pixxi_san_pietru",
                        "mc:tropical_fish", "mod:cerna", "mc:pufferfish"], "2"),
            ("hotbar_candidates_x4", ["mc:cod"] + ["file:" + paths[v] for v, _ in CANDIDATES]
             + ["mod:skorfna", "mod:pixxi_san_pietru", "mc:salmon"], "4"))
    out = []
    for name, items, scale in sets:
        p = os.path.join(OUT_DIR, name + ".png")
        subprocess.run([py, tool, p] + items + ["--scale", scale], check=True, capture_output=True)
        out.append(p)
    return out


def tiles(band, im, x0, y0):
    tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
    tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
    band.paste(tile.convert("RGB"), (x0, y0))
    for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
        t = Image.new("RGBA", (16 * s + 8, 16 * s + 8), col + (255,))
        t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (x0 + 136 + (j % 2) * 44, y0 + (j // 2) * 46))


def sheet(icons, hb):
    bg, ink = (52, 52, 56), (235, 235, 235)
    items = [(("> " if n == CHOICE else "") + "candidate " + n, icons[n]) for n, _ in CANDIDATES]
    items += [("vanilla " + n, Image.open(os.path.join(VANILLA, n + ".png")).convert("RGBA")) for n in ("cod", "salmon")]
    items += [(n, Image.open(os.path.join(TEXTURES, "item", n + ".png")).convert("RGBA"))
              for n in ("skorfna", "pixxi_san_pietru")]
    W = 4 * 244 + 20
    rows_n = (len(items) + 3) // 4
    grid = Image.new("RGB", (W, rows_n * 170 + 10), bg)
    d = ImageDraw.Draw(grid)
    for i, (name, im) in enumerate(items):
        x0, y0 = 10 + (i % 4) * 244, 22 + (i // 4) * 170
        tiles(grid, im, x0, y0)
        d.text((x0, y0 - 20), name, fill=ink, font=label_font(13))
    hbs = [Image.open(p).convert("RGB") for p in hb]
    H = grid.height + sum(h.height + 10 for h in hbs) + 50
    out = Image.new("RGB", (max(W, max(h.width for h in hbs) + 20), H), bg)
    ImageDraw.Draw(out).text((10, 8), "Lionfish item icon (8x, then 1x and 2x on light and dark grey); hotbars: cod, "
                             "LIONFISH, skorfna, salmon, pixxi San Pietru, tropical fish, cerna, pufferfish; then cod, "
                             "candidates A B C, skorfna, pixxi San Pietru, salmon", fill=ink, font=label_font(14))
    out.paste(grid, (0, 36))
    y = 36 + grid.height
    for h in hbs:
        out.paste(h, (10, y))
        y += h.height + 10
    out.save(os.path.join(OUT_DIR, "sheet.png"))


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    icons, paths = {}, {}
    for name, rows in CANDIDATES:
        check(name, rows)
        icons[name] = render(rows)
        paths[name] = os.path.join(OUT_DIR, "icon_%s.png" % name)
        icons[name].save(paths[name])
    icons[CHOICE].save(OUT_ICON)
    sheet(icons, hotbars(paths))
    print("wrote", os.path.relpath(OUT_ICON, ROOT), "and", os.path.relpath(os.path.join(OUT_DIR, "sheet.png"), ROOT))


if __name__ == "__main__":
    main()
