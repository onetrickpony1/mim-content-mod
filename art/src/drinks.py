"""Drink icons: Kinnie (2026-11-17).

Kinnie is Malta's bittersweet soft drink, made by Simonds Farsons Cisk since 1952 from bitter oranges and
aromatic herbs. The owner asked for the real label to show ("they'd go crazy to see kinnie in a video game"), so
the icons carry the label's signature colours and layout, pixel-sized:
- the classic glass bottle (owner's product photo, art/references/kinnie/kinnie_owner_bottle.png, not in git):
  clear glass showing the red-amber drink, a long neck with an orange neck label and a dark-red cap, and the oval
  body label (red ring, orange disc, lighter centre, the white "Kinnie" script on a red banner across the middle);
- the current can: bright orange with lighter yellow-orange swirls, the same red band and white script, silver
  lid and base;
- a glass of Kinnie: red-amber drink, fizz at the top and rising bubbles, ice, an orange slice on the rim.

References (art/references/kinnie/, licences in SOURCES.tsv): Commons photos of the bottle and glass, the can,
and Kinnie on ice with orange. Drink colour sampled from them: #4e1207 (deep, in a tumbler) to #9f6348 (thin,
in the bottle); served over ice with an orange slice in bars.

The glass follows vanilla's bottle family (measured, not copied): a light glass edge on the top left, a darker
blue-grey edge on the bottom right, a white glint down the left, rows 1-14 like the vanilla bottles' 2-14.

Writes candidates only: art/candidates/kinnie_a.png (bottle), _b.png (can), _c.png (glass), and
kinnie_plain.png, kinnie_can_plain.png, kinnie_glass_plain.png: the unbranded versions (BRANDED switch below).
Install is done by hand after review (copy the pick to textures/item/kinnie.png).
Run:  art/.venv/bin/python art/src/drinks.py
"""
import glob
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "art", "candidates")
VANILLA = os.path.join(ROOT, "art", ".vanilla", "item")
REFS = os.path.join(ROOT, "art", "references", "kinnie")
sys.path.insert(0, os.path.join(ROOT, "art", "tools"))
from font import label_font  # noqa: E402


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


# Shared colours ---------------------------------------------------------------------------------------------
GLASS = {
    "H": hx("#d8e6f2"),  # glass edge, lit (top / left)
    "G": hx("#a9c2da"),  # glass edge, middle
    "B": hx("#5f86ad"),  # glass edge, shade (bottom / right)
    "w": hx("#c4d6e6"),  # empty glass inside
    "h": hx("#f4f8fc"),  # glint
}
DRINK = {
    "1": hx("#de6c16"),  # thin drink by the glint, lit (owner's photo: shoulder #dd6b0d)
    "2": hx("#bc4410"),  # drink, lit (photo: #bd4b10, red-amber, not cola-brown)
    "3": hx("#963008"),  # drink, mid (photo: #b33600 in the middle, darker to the right)
    "4": hx("#66220a"),  # drink, deep / shade (photo: #5d240b)
}
LABEL = {
    "O": hx("#ee7a22"),  # label orange
    "o": hx("#c85a1a"),  # label orange, shade side
    "Y": hx("#fbbd3a"),  # the orange-disc yellow
    "y": hx("#e09a28"),  # disc, shade side
    "R": hx("#d8361a"),  # the wordmark band red
    "r": hx("#a82814"),  # band, shade side
    "W": hx("#fff4e4"),  # white script
    "C": hx("#9a2a1a"),  # crown cap, dark red (owner's photo)
    "c": hx("#661a10"),  # crown cap, shade
}

# (a) The classic bottle -------------------------------------------------------------------------------------
BOTTLE = [
    "................",
    "......CCCc......",
    "......OOOo......",
    "......H12B......",
    "......H12B......",
    ".....H1233B.....",
    "....H122334B....",
    "....H122334B....",
    "....HROOOOrB....",
    "....RWYYYYOr....",
    "....RWRWWRWr....",
    "....ROYYYYOr....",
    "....HROOOOrB....",
    "....H123344B....",
    ".....BBBBBB.....",
    "................",
]
# Proportions from the owner's product photo (cap 6 %, neck label 8-21 %, shoulder 27-46 %, oval label 49-80 % of
# the height; body twice the neck's width). Everything is symmetrical about the centre line between x 7 and 8:
# the oval label (rows 8-12) is a red ring round an orange disc with a lighter yellow-orange centre, the red banner
# across its middle (row 10) carries the white script (the tall K at x 5, then "innie" broken into letters, x 5-10).

# (b) The can ------------------------------------------------------------------------------------------------
CAN_PAL = {
    "S": hx("#e6e8ea"),  # silver, lit
    "s": hx("#b4b8bc"),  # silver, mid
    "d": hx("#7c8288"),  # silver, shade / outline
    "A": hx("#ffa53a"),  # can orange, lit
    "a": hx("#f08a1e"),  # can orange
    "n": hx("#c86414"),  # can orange, shade
    "m": hx("#96460e"),  # can outline, shade side
    "L": hx("#ffd06a"),  # swirl, light yellow-orange
}
CAN = [
    "................",
    "................",
    ".....SSSSSs.....",
    "....SsddddsSd...",
    "....nALaaaanm...",
    "....nAaLaaanm...",
    "....nAaaLLanm...",
    "....OYYYYYyom...",
    "....RWRRRRRrm...",
    "....RWWWWWWrm...",
    "....OYYYYYyom...",
    "....nALLaaanm...",
    "....nAaaLLanm...",
    "....nAaaaaLnm...",
    ".....dsssssd....",
    "................",
]

# (c) A glass of Kinnie, ice and an orange slice --------------------------------------------------------------
GLASS_PAL = {
    "I": hx("#eef6fa"),  # ice, lit
    "i": hx("#b6cfdc"),  # ice, shade
    "P": hx("#ffb02e"),  # orange slice flesh
    "p": hx("#e8781a"),  # orange slice peel
    "q": hx("#fff0c0"),  # pith / segment lines
    "f": hx("#f6d2a4"),  # fizz at the top of the drink
    "b": hx("#f0a060"),  # rising bubbles
}
TUMBLER = [
    "................",
    "...........pp...",
    "..........pPqp..",
    "...HGGGGGGpPPp..",
    "...HhfIiffpqPB..",
    "...Hh2Ii2b3pB...",
    "...Hh12b2334B...",
    "...Hh122b334B...",
    "....H1b2334B....",
    "....H122b34B....",
    "....H122334B....",
    "....H12b344B....",
    "....H123344B....",
    "....HhwwwwwB....",
    ".....BBBBBB.....",
    "................",
]


# The brand switch. If Farsons ever objects, BRANDED = False turns Kinnie into a plain "bitter citrus soft drink":
# the same bottle and can with a generic label (orange with a plain red band: no yellow disc, no white script).
BRANDED = True
PLAIN = {"Y": "O", "y": "o", "W": "R"}


def render(grid, *pals, branded=None):
    branded = BRANDED if branded is None else branded
    if not branded:
        grid = ["".join(PLAIN.get(ch, ch) for ch in row) for row in grid]
    pal = {}
    for p in pals:
        pal.update(p)
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(grid):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), pal[ch] + (255,))
    return im


CANDIDATES = {
    "kinnie_a": (BOTTLE, GLASS, DRINK, LABEL),
    "kinnie_b": (CAN, LABEL, CAN_PAL),
    "kinnie_c": (TUMBLER, GLASS, DRINK, GLASS_PAL),
}

# Installed (owner 2026-11-17: the can and the glass are their own items): kinnie_a -> textures/item/kinnie.png,
# kinnie_b -> kinnie_can.png, kinnie_c -> kinnie_glass.png. The plain versions stay in candidates.
PLAIN_OUT = {"kinnie_a": "kinnie_plain", "kinnie_b": "kinnie_can_plain", "kinnie_c": "kinnie_glass_plain"}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, (grid, *pals) in CANDIDATES.items():
        path = os.path.join(OUT, name + ".png")
        render(grid, *pals).save(path)
        print("wrote", os.path.relpath(path, ROOT))
    for name, plain in PLAIN_OUT.items():
        grid, *pals = CANDIDATES[name]
        path = os.path.join(OUT, plain + ".png")
        render(grid, *pals, branded=False).save(path)
        print("wrote", os.path.relpath(path, ROOT), "(unbranded fallback of", name + ")")


def compare():
    """art/candidates/kinnie_compare.png: candidates beside vanilla bottles at 1x/2x/8x, the in-game hotbar crop
    (art/candidates/ingame_kinnie_v4/*19-hotbar-drinks*), and the free reference photos."""
    tiles = [(n, os.path.join(VANILLA, n + ".png")) for n in
             ("glass_bottle", "potion", "honey_bottle", "experience_bottle", "dragon_breath")]
    tiles += [(n, os.path.join(OUT, n + ".png")) for n in ("kinnie_a", "kinnie_b", "kinnie_c", "kinnie_plain", "kinnie_can_plain")]
    font = label_font(14)
    cell = 140
    width = cell * len(tiles)
    hot = sorted(glob.glob(os.path.join(OUT, "ingame_kinnie_v4", "*19-hotbar-drinks*.png")))
    crop = None
    prev = os.path.join(OUT, "kinnie_a_v2.png")  # the previous bottle, if kept, for an 8x side-by-side
    if os.path.exists(prev):
        tiles.append(("kinnie_a_v2 (prev)", prev))
        width = cell * len(tiles)
    if hot:
        shot = Image.open(hot[-1]).convert("RGBA")
        w, h = shot.size
        g = 2 if w < 1200 else 4  # GUI scale: the small test window runs at 2, a big one at 4
        crop = shot.crop((w // 2 - 91 * g, h - 22 * g, w // 2 + 91 * g, h)).resize((728, 88), Image.NEAREST)
    refs = [Image.open(p).convert("RGB") for p in sorted(glob.glob(os.path.join(REFS, "*.jpg")) + glob.glob(os.path.join(REFS, "*.png")))]
    for r in refs:
        r.thumbnail((220, 220))
    height = 230 + (crop.height + 30 if crop else 0) + (250 if refs else 0)
    sheet = Image.new("RGBA", (max(width, 760), height), (139, 139, 139, 255))
    dr = ImageDraw.Draw(sheet)
    for i, (name, path) in enumerate(tiles):
        im = Image.open(path).convert("RGBA")
        x = i * cell + 6
        sheet.alpha_composite(im.resize((128, 128), Image.NEAREST), (x, 4))
        sheet.alpha_composite(im.resize((32, 32), Image.NEAREST), (x + 20, 150))
        sheet.alpha_composite(im, (x + 80, 158))
        dr.text((x, 200), name, fill=(255, 255, 255), font=font)
    y = 230
    if crop:
        dr.text((6, y), "in game (hotbar crop)", fill=(255, 255, 255), font=font)
        sheet.alpha_composite(crop, (6, y + 22))
        y += crop.height + 30
    x = 6
    for r in refs:
        sheet.paste(r, (x, y))
        x += r.width + 8
    path = os.path.join(OUT, "kinnie_compare.png")
    sheet.save(path)
    print("wrote", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    main()
    compare()
