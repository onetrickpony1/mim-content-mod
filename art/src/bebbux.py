"""Stuffat tal-bebbux (Maltese snail stew): item icon candidates (2026-11-17).

The owner's photos (art/references/bebbux_owner/, reference only): the pot or bowl is packed with snails in their
shells, golden-tan shells with dark brown spiral bands and pale cream mouths, in a thin orange-red tomato sauce with
onion, small carrot cubes and chopped parsley (one photo adds potato and olives; no peas in any of them).

The signature is the SPIRAL SHELL: a golden-tan shell with a dark band coiling to a light centre and a cream mouth at
the lower right, rising over the rim, outlined dark like the shank bone of kawlata. That sets it apart from stuffat
tal-fenek and tal-qarnit (red-brown sauce, flat pieces inside the bowl), aljotta (white fish, lemon) and minestra
(many small vegetables).

Same terracotta bowl as the accepted bowl dishes (bowls.py, bowl "b", plain terracotta rim, lit from the top left).
Uses bowls.py without changing anything it writes.

Run:  art/.venv/bin/python art/src/bebbux.py
Writes art/candidates/stuffat_bebbux_{a,b,c}.png, stuffat_bebbux_compare.png (with the in-game hotbar crop and
reference thumbnails when they exist) and installs PICK as the mod texture item/stuffat_bebbux.png.
"""
import glob
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import bowls as B  # noqa: E402
import food_items as F  # noqa: E402
from font import label_font  # noqa: E402

hx = F.hx
ART = os.path.normpath(os.path.join(HERE, ".."))
PICK = "b"

PAL = {k: B.PAL[k] for k in "oOHLlmdD"}          # the shared bowl
PAL.update({
    "S": hx("#e6c27a"), "s": hx("#c4964e"), "x": hx("#94683a"),   # snail shell: lit / mid / shade
    "w": hx("#5a3a20"),                                            # the shell's dark spiral band
    "u": hx("#f2e4bc"), "n": hx("#3e2416"),                        # the shell's cream mouth, its dark inside
    "%": hx("#4a2c1a"),                                            # shell outline
    "1": hx("#c8622e"), "2": hx("#a44a24"),                        # orange-red tomato sauce: lit / shade
    "c": hx("#ec8a2c"), "g": hx("#5f9a3a"),                        # carrot cube, parsley
})

# one snail shell, 8 x 7 with its outline: the band coils from the top in to the light centre, the mouth lower right
SHELL = [
    "..%%%%..",
    ".%SSSs%.",
    "%SwwwSs%",
    "%SwSwSx%",
    "%sSwwux%",
    ".%xxuun%",
    "..%%%%%.",
]

# bowl b with sauce, carrot and parsley in rows 5-8
BASE = (["................"] * 3
        + ["....oooooooo....", "..ooHHHHLLLLOO..",
           ".oHH1g1c121cLLO.", ".oH1c2121g12clO.", ".oL2112c2112llO.", ".OLL2g12c2g2llO.",
           ".OLLLLLlllllldO.", "..OOllllmmmdOO..", "....ODDDDDDO....", ".....OOOOOO....."]
        + ["................"] * 3)


def stamp(rows, spr, x0, y0, extra=None):
    g = [list(r) for r in rows]
    for y, r in enumerate(spr):
        for x, c in enumerate(r):
            if c != ".":
                g[y0 + y][x0 + x] = c
    for (x, y), c in (extra or {}).items():
        g[y][x] = c
    return ["".join(r) for r in g]


# (a) one big snail rising out of the sauce, carrot and parsley either side
BEBBUX_A = stamp(BASE, SHELL, 4, 2, {(3, 6): "1", (2, 7): "c", (3, 7): "2", (4, 8): "1", (5, 8): "g", (11, 5): "2",
                                       (12, 6): "1", (12, 7): "2", (11, 8): "2", (12, 5): "1", (3, 5): "2"})

# (b) the big snail with more shells either side: their tan, band and cream mouths showing past it
BEBBUX_B = stamp(BEBBUX_A, [], 0, 0, {(3, 5): "S", (2, 6): "S", (3, 6): "w", (2, 7): "x", (3, 7): "u", (4, 8): "c",
                                      (12, 5): "S", (12, 6): "w", (13, 6): "s", (12, 7): "u", (13, 7): "x",
                                      (11, 7): "1", (11, 8): "2",
                                      (6, 8): "2", (10, 8): "2", (12, 8): "1"})   # critic: sauce showing past the shell

# (c) two snails heaped, the front one lower and to the right
BEBBUX_C = stamp(stamp(BASE, SHELL, 2, 2), SHELL, 6, 3)

CANDS = (("a", BEBBUX_A), ("b", BEBBUX_B), ("c", BEBBUX_C))
LABELS = {"a": "Bebbux a: one snail", "b": "Bebbux b: snail + more", "c": "Bebbux c: two snails"}


def scaled(im, s):
    return im.resize((16 * s, 16 * s), Image.NEAREST)


def sheet(cands):
    """Candidates at 1x/2x/8x beside every accepted bowl icon and vanilla's stews; then the in-game hotbar crop and
    reference thumbnails."""
    others = []
    for item, lbl in (("stuffat_fenek", "Stuffat tal-fenek"), ("stuffat_qarnit", "Stuffat tal-qarnit"),
                      ("aljotta", "Aljotta"), ("minestra", "Minestra"), ("kawlata", "Kawlata"),
                      ("soppa_tal_armla", "Soppa tal-armla"), ("brodu_tal_laham", "Brodu tal-laħam"),
                      ("brodu_tat_tigieg", "Brodu tat-tiġieġ"), ("kusksu", "Kusksu"), ("bigilla", "Bigilla")):
        p = os.path.join(F.MOD_ITEMS, item + ".png")
        if os.path.exists(p):
            others.append((lbl, Image.open(p).convert("RGBA")))
    for v in ("rabbit_stew", "mushroom_stew", "beetroot_soup", "suspicious_stew"):
        p = os.path.join(F.VANILLA, v + ".png")
        if os.path.exists(p):
            others.append(("vanilla " + v.replace("_", " "), Image.open(p).convert("RGBA")))
    ims = cands + others
    slot, bg, ink = (139, 139, 139, 255), (198, 198, 198, 255), (30, 30, 30, 255)
    f = label_font(12)
    cw = 16 * 8 + 20
    per_row = 9
    rows_n = (len(ims) + per_row - 1) // per_row
    cell_h = 16 + 40 + 16 * 8 + 30
    hot = sorted(glob.glob(os.path.join(ART, "candidates", "ingame_stuffat_bebbux", "*hotbar-bebbux*.png")))
    crop = None
    if hot:
        h = Image.open(hot[-1]).convert("RGBA")
        w, hh = h.size
        crop = h if w == 364 else h.crop((w // 2 - 182, hh - 44, w // 2 + 182, hh))
        crop = crop.resize((728, 88), Image.NEAREST)   # shown at GUI scale 4
    refs = []
    rd = os.path.join(ART, "references", "bebbux_owner")
    for n in ("STUFFAT+TAL-BEBBUX.00_01_33_09.Still121.webp", "STUFFAT+TAL-BEBBUX.00_03_32_21.Still120.webp",
              "images.jpg", "illustration.png"):
        p = os.path.join(rd, n)
        if os.path.exists(p):
            r = Image.open(p).convert("RGBA")
            r.thumbnail((220, 160))
            refs.append(r)
    top_h = 16 + rows_n * cell_h
    W = max(16 + per_row * cw, 16 + (crop.width if crop else 0), 16 + sum(r.width + 10 for r in refs))
    H = top_h + (crop.height + 30 if crop else 0) + (170 if refs else 0)
    sh = Image.new("RGBA", (W, H), bg)
    d = ImageDraw.Draw(sh)
    for i, (n, im) in enumerate(ims):
        x0 = 16 + (i % per_row) * cw
        y0 = 16 + (i // per_row) * cell_h
        d.rectangle([x0, y0, x0 + 17, y0 + 17], fill=slot)
        sh.alpha_composite(im, (x0 + 1, y0 + 1))
        d.rectangle([x0 + 30, y0, x0 + 30 + 35, y0 + 35], fill=slot)
        sh.alpha_composite(scaled(im, 2), (x0 + 32, y0 + 2))
        d.rectangle([x0, y0 + 40, x0 + 127, y0 + 40 + 127], fill=slot)
        sh.alpha_composite(scaled(im, 8), (x0, y0 + 40))
        d.text((x0, y0 + 40 + 128 + 6), n, font=f, fill=ink)
    y = top_h
    if crop:
        d.text((16, y), "in game (hotbar)", font=f, fill=ink)
        sh.alpha_composite(crop, (16, y + 18))
        y += crop.height + 30
    x = 16
    for r in refs:
        sh.alpha_composite(r, (x, y))
        x += r.width + 10
    return sh


def main():
    cands = []
    for k, rows in CANDS:
        F.check("stuffat_bebbux_" + k, rows)
        im = F.render(rows, PAL)
        im.save(os.path.join(F.OUT, f"stuffat_bebbux_{k}.png"))
        cands.append((LABELS[k], im))
        ys = [y for y in range(16) for x in range(16) if im.getpixel((x, y))[3] > 0]
        print(f"stuffat_bebbux_{k}: vertical centre {sum(ys) / len(ys) + 0.5:.2f}")
    sheet(cands).save(os.path.join(F.OUT, "stuffat_bebbux_compare.png"))
    F.render(dict(CANDS)[PICK], PAL).save(os.path.join(F.MOD_ITEMS, "stuffat_bebbux.png"))
    print("wrote stuffat_bebbux_a-c, stuffat_bebbux_compare.png; installed", PICK)


if __name__ == "__main__":
    main()
