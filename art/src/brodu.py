"""Kusksu, brodu tat-tiġieġ and brodu tal-laħam: item icon candidates (2026-11-17).

No owner photos yet; references art/references/soups/ (Wikimedia Commons, see SOURCES.tsv):
- Kusksu (kusksu_1-3; en Wikipedia "Kusksu"; guidememalta.com "6 Maltese soups"): a spring and Lenten soup of fresh
  broad beans (ful) and tiny pasta beads (kusksu) in a tomato-tinted, mustard-orange broth, with ġbejniet and/or eggs
  poached in it. The photo: pale yellow-green beans, cream beads, orange-gold broth. The ġbejna is soppa tal-armla's
  signature, so kusksu's is the cream BEADS speckling the bowl plus GREEN BEANS.
- Brodu (brodu_1-2; guidememalta.com; malteserecipes.pages.dev "Brodu"): a clear broth of meat simmered for hours with
  onion, carrot, marrow, celery and potato, served with small pasta (beads, stars, tortellini). brodu_1 ("Maltese broth
  with chicken"): a clear gold-orange broth, a pale chicken piece, carrot, marrow, little pasta wheels.
  Brodu tal-laħam: beef (often with a marrow bone), a darker amber-brown broth.
The brodu signature is visible LIQUID: a lot of open broth with a light reflection and a few fat "eyes".
Chicken = golden broth + a pale chicken piece; beef = brown-amber broth + a dark beef chunk.

Same terracotta bowl "b" as the accepted bowl dishes (bowls.py, plain terracotta rim, lit from the top left); bowls.py's output
is not changed.

Run:  art/.venv/bin/python art/src/brodu.py
Writes art/candidates/{kusksu,brodu_tat_tigieg,brodu_tal_laham}_{a,b,c}.png and brodu_compare.png (with the in-game
hotbar crop from art/candidates/ingame_brodu/ when it exists) and installs PICKS as the mod textures.
"""
import glob
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import bowls as B  # noqa: E402
import food_items as F  # noqa: E402
from font import label_font  # noqa: E402

hx = F.hx
ART = os.path.normpath(os.path.join(HERE, ".."))
PICKS = {"kusksu": "d", "brodu_tat_tigieg": "d", "brodu_tal_laham": "d"}

PAL = {k: B.PAL[k] for k in "oOHLlmdD"}          # the shared bowl
PAL.update({
    # kusksu: tomato-tinted mustard-orange broth, broad beans, pasta beads, parsley
    "1": hx("#dca444"), "2": hx("#c4862c"), "3": hx("#8c5a1c"),
    "f": hx("#b4dc64"), "F": hx("#6c9c34"), "V": hx("#4e7a26"),   # bean lit / shade / deep shade
    "b": hx("#f6e4a4"), "e": hx("#d8bc70"),                       # bead, bead in shade
    "p": hx("#3c7428"),                                           # parsley
    # brodu tat-tiġieġ: clear golden broth
    "4": hx("#f0b848"), "5": hx("#e09e34"), "6": hx("#a06a1c"), "h": hx("#fff6d8"), "y": hx("#f6d070"),
    "c": hx("#fbf4e4"), "C": hx("#caa87a"),                       # chicken, its shade
    # brodu tal-laħam: clear brown-amber broth
    "7": hx("#b07034"), "8": hx("#945424"), "9": hx("#58300f"), "j": hx("#f0c890"), "J": hx("#c08048"),
    "r": hx("#a84c38"), "R": hx("#6c2a1e"), "Q": hx("#44180e"),   # beef lit / mid / shade
    # shared vegetables and pasta
    "k": hx("#ec7428"), "K": hx("#c4561c"),                       # carrot lit / shade
    "z": hx("#9cc050"), "Z": hx("#5e8a30"),                       # marrow flesh / skin
    "n": hx("#faeec4"), "N": hx("#dccc98"),                       # small pasta, its shade
    "s": hx("#d8e0a0"),                                           # celery
    # critic round 1: d variants
    "%": hx("#c8a040"),                                           # kusksu: mustard broth between the beads
    "$": hx("#8ab04a"), "+": hx("#c88a40"),                       # critic r2: brighter bean, laham amber glint
    "q": hx("#e0a838"), "^": hx("#b88428"),                       # tiġieġ: even golden broth, its back shade
    "!": hx("#f0e4c8"), "@": hx("#d8c4a0"),                       # tiġieġ: chicken piece, its underside
    # laħam: calm amber-brown, highlight, back shade; broth and highlight one step darker (critic, after the glaze line
    # went: the old #a8642c broth matched the bowl's clay walls and read as an empty bowl)
    "a": hx("#8a4a1e"), "A": hx("#a8642c"), "w": hx("#7a4220"),
    "x": hx("#5a2a18"), "X": hx("#46200f"),                       # laħam: beef chunk, its underside
})

TOP = ["................"] * 3 + ["....oooooooo....", "..ooHHHHLLLLOO.."]
BOTTOM = [".OLLLLLlllllldO.", "..OOllllmmmdOO..", "....ODDDDDDO....", ".....OOOOOO....."] + ["................"] * 3


def bowl(r5, r6, r7, r8):
    """The contents of bowl b's surface rows 5-8 (8, 10, 10 and 8 pixels wide) inside the shared bowl."""
    assert (len(r5), len(r6), len(r7), len(r8)) == (8, 10, 10, 8), (r5, r6, r7, r8)
    rows = TOP + [".oHH" + r5 + "LLO.", ".oH" + r6 + "LO.", ".oL" + r7 + "lO.", ".OLL" + r8 + "llO."] + BOTTOM
    assert len(rows) == 16 and all(len(r) == 16 for r in rows)
    return rows


# ---- Kusksu: beads speckle everything, green beans as 2-pixel ovals (lit left, shaded right) ----
KUSKSU = {
    "a": bowl("3b3fF3b3",            # beads + beans, broth showing between
              "bfFb2bfF2b",
              "2b1fFb2bfF",
              "fFb2bfFb"),
    "b": bowl("3fF3bfF3",            # more beans, a bean-green bowl at a glance
              "fFbfF2bfFb",
              "b1fFbfF2bV",
              "bfF2bfFb"),
    "c": bowl("3b3fFp3b",            # a: plus parsley flecks (the photo's garnish)
              "bfFb2bpfFb",
              "2bpfFb2bfF",
              "fFb2pbfF"),
    "d": bowl("33b33b33",            # critic r1: mustard broth between separate bead dots, only two beans
              "%b%$$%b%b%",
              "b%b%b%$$%b",
              "%b%b%b%b"),
}

# ---- Brodu tat-tiġieġ: open golden broth (darker under the back lip, glowing where it is shallow at the front), a
# small white reflection, one pale chicken piece, a carrot and marrow dice, a few bits of pasta ----
TIGIEG = {
    "a": bowl("6666cc66",
              "5hh55ccC5k",
              "555n55CC5K",
              "55z5n555"),
    "b": bowl("66cc6666",            # the chicken to the left, the reflection on the open broth to the right
              "5ccC5hh5k5",
              "4CC5n5y5K5",
              "5n5z55n5"),
    "c": bowl("6666cc66",            # a plus fat "eyes" and more pasta
              "5hhy5ccC5k",
              "4n5n5yCCnK",
              "5n5zn5n5"),
    "d": bowl("^^^^^^^^",            # critic r1: flat even gold, one 3x2 chicken piece, no orange specks
              "qhhq!!!qqq",
              "qqqq@@@qqq",
              "qqzqqnqq"),
}

# ---- Brodu tal-laħam: the same layout in brown-amber, a dark red-brown beef chunk ----
LAHAM = {
    "a": bowl("9999rr99",
              "8jj88rRQ8k",
              "788n8RQ88K",
              "78z8n888"),
    "b": bowl("99rr9999",
              "8rRQ8jj8k8",
              "7RQ8n8J8K8",
              "7n8z8n88"),
    "c": bowl("9999rr99",
              "8jjJ8rRQ8k",
              "7n8n8JRQnK",
              "7n8zn8n8"),
    "d": bowl("w++++www",            # critic r1+r2 (amber glint): plain, calm amber-brown, one dark 3x2 beef chunk off centre, one carrot
              "aAAaaxxxaa",
              "akaaaXXXaa",
              "aaaaaaaa"),
}

DISHES = (("kusksu", "Kusksu", KUSKSU), ("brodu_tat_tigieg", "Brodu tat-Tiġieġ", TIGIEG),
          ("brodu_tal_laham", "Brodu tal-Laħam", LAHAM))


def vcentre(im):
    a = np.asarray(im)[:, :, 3] > 0
    ys = np.nonzero(a)[0]
    return round(float(ys.mean()) + 0.5, 2)


def scaled(im, s):
    return im.resize((16 * s, 16 * s), Image.NEAREST)


def sheet(cands):
    """Candidates at 1x/2x/8x beside every installed Maltese soup and vanilla beetroot soup; then the in-game hotbar
    crop (GUI scale 2 at 854x480, enlarged) and the reference thumbnails."""
    others = []
    for item, lbl in (("aljotta", "Aljotta"), ("soppa_tal_armla", "Soppa tal-armla"), ("minestra", "Minestra"),
                      ("kawlata", "Kawlata"), ("stuffat_fenek", "Stuffat tal-fenek")):
        p = os.path.join(F.MOD_ITEMS, item + ".png")
        if os.path.exists(p):
            others.append((lbl, Image.open(p).convert("RGBA")))
    p = os.path.join(F.VANILLA, "beetroot_soup.png")
    if os.path.exists(p):
        others.append(("vanilla beetroot soup", Image.open(p).convert("RGBA")))
    slot, bg, ink = (139, 139, 139, 255), (198, 198, 198, 255), (30, 30, 30, 255)
    f = label_font(12)
    cw = 16 * 8 + 24
    per_row = 12
    rows = [cands[i:i + per_row] for i in range(0, len(cands), per_row)] + [others]
    row_h = 16 + 40 + 128 + 30
    hot = sorted(glob.glob(os.path.join(ART, "candidates", "ingame_brodu", "*11c-hotbar-all-soups*.png")))
    crop = None
    if hot:
        h = Image.open(hot[-1]).convert("RGBA")
        w, hh = h.size
        crop = h.crop((w // 2 - 182, hh - 44, w // 2 + 182, hh)).resize((364 * 3, 44 * 3), Image.NEAREST)
    refs = []
    for n in ("kusksu_1.jpg", "kusksu_2.jpg", "brodu_1.jpg", "brodu_2.jpg"):
        p = os.path.join(ART, "references", "soups", n)
        if os.path.exists(p):
            r = Image.open(p).convert("RGBA")
            r.thumbnail((260, 180))
            refs.append(r)
    W = max(16 + per_row * cw, 16 + (crop.width if crop else 0), 16 + sum(r.width + 10 for r in refs))
    H = 16 + len(rows) * row_h + (crop.height + 30 if crop else 0) + (200 if refs else 0)
    sh = Image.new("RGBA", (W, H), bg)
    d = ImageDraw.Draw(sh)
    y0 = 16
    for row in rows:
        for i, (n, im) in enumerate(row):
            x0 = 16 + i * cw
            d.rectangle([x0, y0, x0 + 17, y0 + 17], fill=slot)
            sh.alpha_composite(im, (x0 + 1, y0 + 1))
            d.rectangle([x0 + 30, y0, x0 + 30 + 35, y0 + 35], fill=slot)
            sh.alpha_composite(scaled(im, 2), (x0 + 32, y0 + 2))
            sh.alpha_composite(scaled(im, 8), (x0, y0 + 40))
            d.text((x0, y0 + 40 + 128 + 6), n, font=f, fill=ink)
        y0 += row_h
    if crop:
        d.text((16, y0), "in game, hotbar (GUI 2, shown x3): aljotta, soppa, minestra, kawlata, KUSKSU, BRODU "
                         "TAT-TIĠIEĠ, BRODU TAL-LAĦAM, fenek, vanilla beetroot soup", font=f, fill=ink)
        sh.alpha_composite(crop, (16, y0 + 18))
        y0 += crop.height + 30
    x = 16
    for r in refs:
        sh.alpha_composite(r, (x, y0))
        x += r.width + 10
    return sh


def main():
    cands, made = [], {}
    for item, lbl, variants in DISHES:
        for k, rows in variants.items():
            F.check(f"{item}_{k}", rows)
            im = F.render(rows, PAL)
            im.save(os.path.join(F.OUT, f"{item}_{k}.png"))
            made[(item, k)] = im
            cands.append((f"{lbl} {k}", im))
            print(f"{item}_{k}: vertical centre {vcentre(im)}")
    sheet(cands).save(os.path.join(F.OUT, "brodu_compare.png"))
    for item, k in PICKS.items():
        made[(item, k)].save(os.path.join(F.MOD_ITEMS, item + ".png"))
    print("wrote", len(cands), "candidates, brodu_compare.png; installed", PICKS)


if __name__ == "__main__":
    main()
