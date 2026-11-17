"""Soppa tal-armla ("widow's soup"): item icon candidates (2026-11-17).

The owner's photos (art/references/bowls_owner/soppa_armla/, reference only): an orange-red vegetable broth with
cauliflower, potato, carrot and marrow chunks and green peas, one or two whole white ġbejniet (fresh cheeselets, ridged
from the basket mould) sitting in it, sometimes a poached egg, a parsley sprig on top.

Same terracotta bowl as the accepted bowl dishes (bowls.py, bowl "b", plain terracotta rim, lit from the top left); the
ġbejniet are drawn like the accepted fresh ġbejna icon (cream top, ridged sides, dark brown outline) and rise above the
lip so they read at 1x. Uses bowls.py without changing anything it writes.

Run:  art/.venv/bin/python art/src/soppa.py
Writes art/candidates/soppa_tal_armla_{a,b,c,d}.png, soppa_compare.png (with the in-game hotbar crop and reference
thumbnails when they exist) and installs PICK as the mod texture item/soppa_tal_armla.png.
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
PICK = "d"

PAL = {k: B.PAL[k] for k in "oOHLlmdD"}          # the shared bowl
PAL.update({
    "#": hx("#5e4a2e"), "%": hx("#4a3a24"),           # ġbejna outline (as the fresh ġbejna icon), its shaded side
    "W": hx("#f6f2e4"), "w": hx("#e6e0c8"),           # ġbejna top, lit / shade
    "r": hx("#ece6d2"), "R": hx("#d2c8a8"),           # ġbejna ridges, light / dark (kept pale: the white reads)
    "1": hx("#e0743a"), "2": hx("#c8552a"), "3": hx("#8e3418"),   # orange-red broth: lit / mid / shade
    "c": hx("#f2ead0"), "C": hx("#cfc29c"),           # cauliflower, its shade
    "p": hx("#eac46a"), "k": hx("#f2961e"),           # potato, carrot
    "v": hx("#b2c066"),                               # marrow (pale green)
    "e": hx("#7cc23e"), "E": hx("#4f8e2a"),           # peas, pea shade
    "z": hx("#3e7c2a"), "Z": hx("#64a63a"),           # parsley, lit
    # critic round 1 (for d): a warm grey-cream ġbejna outline (not a dark lid), orange-red broth under it
    "[": hx("#e2dac2"), "]": hx("#d8cfb0"),           # d's ridges, a touch deeper (the front of the cheese)
    "(": hx("#a89a7a"), ")": hx("#76684c"), "!": hx("#d8582a"),
})


def base():
    """The bowl with the broth in it (bowls.fill on bowl b, its plain terracotta rim)."""
    return B.fill("b", "123", {})


def cheese(g, x0, y0, w, th, sh, soft=False):
    """One whole ġbejna seen a little from above: top outline row, th rows of top face, sh rows of ridged side, then a
    broth shadow where it sits in the soup (or the outline where it is over the bowl)."""
    x1 = x0 + w - 1
    for x in range(x0 + 1, x1):
        g[y0][x] = "#"
    for j in range(1, th + 1):
        y = y0 + j
        g[y][x0], g[y][x1] = "#", "%"
        for x in range(x0 + 1, x1):
            g[y][x] = "W" if (x - x0) + j <= min(4, (w - 1) // 2 + 1) - (w >= 8) else "w"
    if w >= 7 and th >= 2:                                    # the shallow dip the mould leaves in the top
        g[y0 + 2][x0 + w // 2 - 1] = g[y0 + 2][x0 + w // 2] = "r"
    for j in range(1, sh + 1):
        y = y0 + th + j
        g[y][x0], g[y][x1] = "#", "%"
        for x in range(x0 + 1, x1):
            g[y][x] = "R" if (x - x0) % 2 == 0 or x == x1 - 1 else "r"
    y = y0 + th + sh + 1
    for x in range(x0 + 1, x1):
        if g[y][x] in "123":
            g[y][x] = "!" if soft else "3"
        elif g[y][x] != ".":
            g[y][x] = "%"
    if soft:                                                  # round the top corners, a light outline
        g[y0][x0 + 1], g[y0][x1 - 1] = B.BOWL_B[y0][x0 + 1], B.BOWL_B[y0][x1 - 1]
        g[y0 + 1][x0 + 1], g[y0 + 1][x1 - 1] = "#", "%"
        g[y0 + 1][x0], g[y0 + 1][x1] = B.BOWL_B[y0 + 1][x0], B.BOWL_B[y0 + 1][x1]
        for x in range(x0 + 3, x1):                           # one small highlight, the rest of the top in shade
            for j in range(1, th + 1):
                if g[y0 + j][x] == "W":
                    g[y0 + j][x] = "w"
        for yy in range(y0, y + 1):
            for xx in range(x0, x1 + 1):
                g[yy][xx] = {"#": ")" if yy == y0 else "(", "%": ")", "r": "[" if yy > y0 + th else "r",
                             "R": "]"}.get(g[yy][xx], g[yy][xx])
    return g


def put(g, pts):
    for (x, y), c in pts.items():
        g[y][x] = c
    return g


def cand_a():
    """One large ġbejna on the left, the vegetables beside and in front."""
    g = cheese(base(), 3, 2, 7, 2, 2)
    return put(g, {(10, 5): "c", (11, 5): "C", (10, 6): "e", (11, 6): "p", (12, 6): "k", (11, 7): "c", (12, 7): "C",
                   (10, 7): "2", (3, 7): "k", (4, 8): "e", (6, 8): "v", (7, 8): "p", (9, 8): "e", (10, 8): "k",
                   (11, 8): "e"})


def cand_b():
    """Two smaller ġbejniet, the back one higher; peas, cauliflower and carrot round them."""
    g = cheese(base(), 2, 2, 5, 1, 2)
    g = cheese(g, 7, 3, 5, 1, 2)
    return put(g, {(12, 5): "e", (12, 6): "c", (12, 7): "C", (3, 7): "e", (4, 7): "k", (3, 8): "2", (4, 8): "c",
                   (5, 8): "C", (7, 8): "e", (8, 8): "p", (9, 8): "e", (10, 8): "k", (11, 8): "e", (6, 6): "v",
                   (6, 7): "p"})


def cand_c():
    """A slightly smaller ġbejna, more broth showing on the right, and a parsley sprig on the broth."""
    g = cheese(base(), 3, 2, 6, 2, 2)
    return put(g, {(10, 4): "Z", (11, 4): "z", (10, 5): "z", (11, 5): "Z", (12, 5): "z", (9, 6): "c", (10, 6): "C",
                   (11, 6): "e", (12, 6): "p", (9, 7): "2", (10, 7): "k", (11, 7): "c", (12, 7): "C", (3, 7): "k",
                   (4, 8): "e", (6, 8): "v", (7, 8): "p", (9, 8): "e", (10, 8): "1", (11, 8): "e"})


def cand_d():
    """Owner: the soups must stand apart; the white ġbejna is this one's signature. A wider ġbejna (8 px) that fills
    most of the bowl, broth, peas and a parsley sprig only on the right and in front."""
    g = cheese(base(), 3, 2, 8, 2, 2, soft=True)
    return put(g, {(11, 4): "z", (12, 4): "Z", (11, 5): "Z", (12, 5): "c", (11, 6): "1", (12, 6): "c", (11, 7): "c",
                   (12, 7): "c", (3, 7): "2", (4, 8): "!", (5, 8): "v", (6, 8): "!", (7, 8): "e", (8, 8): "p",
                   (9, 8): "k", (10, 8): "k", (11, 8): "p", (10, 7): "p", (9, 7): "c",
                   (4, 7): "2", (5, 7): "2", (6, 7): "2", (6, 4): "]", (7, 4): "]", (4, 5): "]", (4, 6): "]"})


CANDS = (("a", "one ġbejna", cand_a), ("b", "two ġbejniet", cand_b), ("c", "ġbejna + parsley", cand_c),
         ("d", "wide ġbejna", cand_d))


def thumb(path, size=128):
    im = Image.open(path).convert("RGB")
    s = min(im.size)
    im = im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width - s) // 2 + s, (im.height - s) // 2 + s))
    return im.resize((size, size), Image.LANCZOS).convert("RGBA")


def sheet(ims):
    top = F.compare(ims)
    extra = []
    shot = sorted(glob.glob(os.path.join(F.OUT, "ingame_soppa", "*11b-hotbar-soups*.png")))
    if shot:
        im = Image.open(shot[-1]).convert("RGBA")
        w, h = im.size
        k = max(1, w // 427)                                  # the GUI scale (4 at 1708 wide, 2 at 854)
        crop = im.crop((w // 2 - 91 * k, h - 22 * k, w // 2 + 91 * k, h))
        extra.append(("in game (hotbar)", crop.resize((728, 88), Image.NEAREST)))
    refs = sorted(glob.glob(os.path.join(ART, "references", "bowls_owner", "soppa_armla", "*")))
    for i in (1, 2, 3):
        if i < len(refs):
            extra.append(("owner photo", thumb(refs[i])))
    if not extra:
        return top
    hh = max(im.height for _, im in extra) + 40
    W = max(top.width, 16 + sum(im.width + 16 for _, im in extra))
    out = Image.new("RGBA", (W, top.height + hh), (198, 198, 198, 255))
    out.alpha_composite(top, (0, 0))
    d, f, x = ImageDraw.Draw(out), label_font(12), 16
    for n, im in extra:
        out.alpha_composite(im, (x, top.height))
        d.text((x, top.height + im.height + 4), n, fill=(30, 30, 30, 255), font=f)
        x += im.width + 16
    return out


def main():
    ims = []
    for k, lbl, make in CANDS:
        rows = ["".join(r) for r in make()]
        F.check("soppa_" + k, rows)
        im = F.render(rows, PAL)
        im.save(os.path.join(F.OUT, f"soppa_tal_armla_{k}.png"))
        ims.append((f"Soppa {k}: {lbl}", im))
        if k == PICK:
            im.save(os.path.join(F.MOD_ITEMS, "soppa_tal_armla.png"))
    for item, lbl in (("stuffat_fenek", "Stuffat tal-fenek"), ("aljotta", "Aljotta"),
                      ("stuffat_qarnit", "Stuffat tal-qarnit"), ("bigilla", "Bigilla")):
        ims.append((lbl, Image.open(os.path.join(F.MOD_ITEMS, item + ".png")).convert("RGBA")))
    ims.append(("vanilla beetroot_soup", Image.open(os.path.join(F.VANILLA, "beetroot_soup.png")).convert("RGBA")))
    sheet(ims).save(os.path.join(F.OUT, "soppa_compare.png"))
    print("wrote soppa_tal_armla_{a,b,c,d}.png, soppa_compare.png; installed", PICK)


if __name__ == "__main__":
    main()
