"""Kawlata (Maltese pork and vegetable soup): item icon candidates (2026-11-17).

The owner's photos and recipe (art/references/bowls_owner/kawlata/, reference only): a golden-orange broth thick with
pale green-white cabbage, carrot, pumpkin, marrow, cauliflower and split fava beans, cooked with pork shanks and often
Maltese sausage (zalzett). The agreed signature (owner: "these soups can look similar so something has to make them
stand apart look wise") is VISIBLE PORK: round sausage slices (pinkish-brown inside, dark coarse specks, a darker rim)
and/or a pork shank whose bone sticks up out of the bowl.

Same terracotta bowl as the accepted bowl dishes (bowls.py, bowl "b", plain terracotta rim, lit from the top left).
Uses bowls.py without changing anything it writes.

Run:  art/.venv/bin/python art/src/kawlata.py
Writes art/candidates/kawlata_{a,b,c}.png, kawlata_compare.png (with the in-game hotbar crop and reference thumbnails
when they exist) and installs PICK as the mod texture item/kawlata.png.
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
PICK = "c"

PAL = {k: B.PAL[k] for k in "oOHLlmdD"}          # the shared bowl
PAL.update({
    "1": hx("#e4b44a"), "2": hx("#c98e30"), "3": hx("#8e5a1c"),   # golden-orange broth: lit / mid / back shadow
    "y": hx("#743424"), "Z": hx("#5a2618"),           # sausage rim: lit side / shaded side
    "z": hx("#e09a88"), "s": hx("#7a3628"),           # sausage inside (pinkish-brown), coarse speck
    "p": hx("#c88a6a"), "P": hx("#a0604a"), "Q": hx("#74402c"),   # browned pork shank: lit / mid / shade (critic)
    "#": hx("#7a6244"), "%": hx("#4e3a22"),           # bone outline: lit / shaded side
    "&": hx("#6a3022"),                               # pork outline
    "b": hx("#f6eedc"), "e": hx("#d6c8a4"),           # bone, its shade
    "c": hx("#e2ecc0"), "C": hx("#a8bc78"),           # cabbage, its shade
    "v": hx("#c8d48a"), "j": hx("#e0a838"),   # cabbage leaf, golden broth gap (critic)
    "k": hx("#e8702a"), "w": hx("#f6f0dc"), "q": hx("#f2a02c"),   # carrot, cauliflower, pumpkin
})

BOWL_TOP = ["................"] * 3 + ["....oooooooo....", "..ooHHHHLLLLOO.."]
BOWL_BOTTOM = [".OLLLLLlllllldO.", "..OOllllmmmdOO..", "....ODDDDDDO....", ".....OOOOOO....."] + ["................"] * 3


def bowl(surface, top=None):
    """surface: the four rows 5-8 of bowl b; top: optional rows 0-4 (for a bone over the lip)."""
    rows = (top or BOWL_TOP) + surface + BOWL_BOTTOM
    assert len(rows) == 16 and all(len(r) == 16 for r in rows), rows
    return rows


# (a) two sausage slices and cabbage: each coin a dark rim (a touch lighter top-left) round a pinkish-brown inside
# with a dark coarse speck.
KAWLATA_A = bowl([
    ".oHHyyy3cCckLLO.",
    ".oHyzszZCyyy1LO.",
    ".oLcZZZ1yzszZlO.",
    ".OLLCcqk2ZZZllO.",
])

# (b) a pork shank sitting up out of the broth like a drumstick: a pink-brown meat mound over the back lip, its bone
# with a knobbed end sticking up to the right.
SHANK_TOP = [
    "................",
    "............#%..",
    "...........#bb%.",
    "....&&&&o#be%...",
    "..o&pppPPbe%OO..",
]
KAWLATA_B = bowl([
    ".oH&pPPPQQ3cLLO.",
    ".oH2&QQQ&2cCkLO.",
    ".oLk1qc2w1q22lO.",
    ".OLLC2k2cC2q2lO.",
], SHANK_TOP)

# (c) both: the shank and one big sausage slice in front, cabbage and carrot round them.
KAWLATA_C = bowl([
    ".oH&pPPPQQ3cLLO.",
    ".oH2&QQQ&yyy1LO.",
    ".oLvvkcjyzszZlO.",
    ".OLLvvqcjZZZllO.",
], SHANK_TOP)

CANDS = (("a", KAWLATA_A), ("b", KAWLATA_B), ("c", KAWLATA_C))
LABELS = {"a": "Kawlata a: sausage", "b": "Kawlata b: shank", "c": "Kawlata c: both"}


def scaled(im, s):
    return im.resize((16 * s, 16 * s), Image.NEAREST)


def sheet(cands):
    """Candidates at 1x/2x/8x beside the accepted bowls, soppa and minestra (if installed), vanilla rabbit stew;
    then the in-game hotbar crop and reference thumbnails."""
    others = []
    for item, lbl in (("aljotta", "Aljotta"), ("stuffat_fenek", "Stuffat tal-fenek"), ("stuffat_qarnit", "Qarnit"),
                      ("bigilla", "Bigilla"), ("soppa_tal_armla", "Soppa tal-armla"), ("minestra", "Minestra")):
        p = os.path.join(F.MOD_ITEMS, item + ".png")
        if os.path.exists(p):
            others.append((lbl, Image.open(p).convert("RGBA")))
    for v in ("rabbit_stew", "beetroot_soup", "mushroom_stew"):
        p = os.path.join(F.VANILLA, v + ".png")
        if os.path.exists(p):
            others.append(("vanilla " + v.replace("_", " "), Image.open(p).convert("RGBA")))
    ims = cands + others
    slot, bg, ink = (139, 139, 139, 255), (198, 198, 198, 255), (30, 30, 30, 255)
    f = label_font(12)
    cw = 16 * 8 + 20
    hot = sorted(glob.glob(os.path.join(ART, "candidates", "ingame_kawlata", "*hotbar-soups*.png")))
    crop = None
    if hot:
        h = Image.open(hot[-1]).convert("RGBA")
        w, hh = h.size
        gs = max(1, min(w // 320, hh // 240))           # the GUI scale the game picked for this window size
        crop = h.crop((w // 2 - 91 * gs, hh - 22 * gs, w // 2 + 91 * gs, hh))
        crop = crop.resize((728, 88), Image.NEAREST)   # shown at GUI scale 4
    refs = []
    rd = os.path.join(ART, "references", "bowls_owner", "kawlata")
    for n in ("Kawlata-1024x1024-1.jpg", "KAWLATA.00_00_04_16.Still117.webp", "16830997_1984790995081757_4125655192660059258_n.jpg"):
        p = os.path.join(rd, n)
        if os.path.exists(p):
            r = Image.open(p).convert("RGBA")
            r.thumbnail((220, 160))
            refs.append(r)
    top_h = 16 + 40 + 16 * 8 + 40
    W = max(16 + len(ims) * cw, 16 + (crop.width if crop else 0), 16 + sum(r.width + 10 for r in refs))
    H = top_h + (crop.height + 30 if crop else 0) + (170 if refs else 0)
    sh = Image.new("RGBA", (W, H), bg)
    d = ImageDraw.Draw(sh)
    for i, (n, im) in enumerate(ims):
        x0 = 16 + i * cw
        d.rectangle([x0, 16, x0 + 17, 33], fill=slot)
        sh.alpha_composite(im, (x0 + 1, 17))
        d.rectangle([x0 + 30, 16, x0 + 30 + 35, 51], fill=slot)
        sh.alpha_composite(scaled(im, 2), (x0 + 32, 18))
        sh.alpha_composite(scaled(im, 8), (x0, 56))
        d.text((x0, 56 + 128 + 6), n, font=f, fill=ink)
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
        F.check("kawlata_" + k, rows)
        im = F.render(rows, PAL)
        im.save(os.path.join(F.OUT, f"kawlata_{k}.png"))
        cands.append((LABELS[k], im))
    sheet(cands).save(os.path.join(F.OUT, "kawlata_compare.png"))
    F.render(dict(CANDS)[PICK], PAL).save(os.path.join(F.MOD_ITEMS, "kawlata.png"))
    print("wrote kawlata_a-c, kawlata_compare.png; installed", PICK)


if __name__ == "__main__":
    main()
