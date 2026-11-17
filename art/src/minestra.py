"""Item texture for minestra, the Maltese vegetable soup (candidates, 2026-11-17).

The bowl dishes' shared terracotta bowl b (bowls.py, unchanged), with minestra inside: a thick, chunky soup in an
orange-brown, tomato-tinted broth (kunserva), "all about texture". From the owner's recipe and photos
(art/references/bowls_owner/minestra/, reference only): cabbage, cauliflower, pumpkin, carrot, potato, kohlrabi,
zucchini, mixed lentils, pulses and beans, sometimes small pasta; vegetarian, no soft cheese, no ġbejniet (those are
soppa tal-armla). Some grate hard cheese on top.

What sets it apart from aljotta (bright orange broth, white fish) and vanilla's stews: a dense mix of many small
pieces (pale cabbage/cauliflower/potato, orange pumpkin and carrot, green zucchini, dark lentils and red beans) with
little broth showing, and a browner broth.

Run:  art/.venv/bin/python art/src/minestra.py
Writes art/candidates/minestra_{a,b,c}.png and minestra_compare.png, installs the pick (PICK) as textures/item/minestra.png.
"""
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import food_items as F  # noqa: E402
import bowls as B  # noqa: E402

hx, render = F.hx, F.render

# the bowl's own colours from bowls.py, then the soup's
PAL = {k: B.PAL[k] for k in "oOHLlmdD"}
PAL.update({
    "1": hx("#c8803a"), "2": hx("#a8642c"), "3": hx("#7a4420"),     # broth lit / mid / back shadow (orange-brown)
    "p": hx("#ecdcaa"), "P": hx("#c4ae7a"),                        # cauliflower, potato, kohlrabi; shade
    "y": hx("#cfcc88"),                                            # cabbage (pale yellow-green)
    "c": hx("#ec8a2c"), "C": hx("#c4661c"),                        # pumpkin, carrot; shade
    "z": hx("#b4c46c"), "Z": hx("#4e7a2e"),                        # zucchini flesh, zucchini skin / cabbage leaf
    "b": hx("#5a3420"), "r": hx("#86302a"),                        # lentils (dark), red beans
    "w": hx("#fbf4d4"), "h": hx("#4f8a3a"),                        # grated cheese, parsley
})

TOP = ["................"] * 3 + ["....oooooooo....", "..ooHHHHLLLLOO.."]
FOOT = [".OLLLLLlllllldO.", "..OOllllmmmdOO..", "....ODDDDDDO....", ".....OOOOOO....."] + ["................"] * 3


def bowl(r5, r6, r7, r8):
    """The contents' rows 5-8 (8, 10, 10, 8 pixels) set into bowl b, its plain terracotta rim."""
    assert (len(r5), len(r6), len(r7), len(r8)) == (8, 10, 10, 8)
    return TOP + [".oHH" + r5 + "LLO.", ".oH" + r6 + "LO.", ".oL" + r7 + "lO.", ".OLL" + r8 + "llO."] + FOOT


CANDS = {
    # a: thick and chunky, little broth: a dense speckle of every vegetable and lentils in the orange-brown broth
    "a": bowl("3c3b3Z3p",
              "1pcb2zrcy2",
              "c2Zyb1cb2P",
              "2bcp2Zcb"),
    # b: bigger two-pixel pieces (a lit top, a shaded side) in a bit more broth
    "b": bowl("33pp3cc3",
              "1bPP1zCC2b",
              "cc2rb1Zyy1",
              "CC1b2b2b"),
    # c: a with grated hard cheese and a little parsley on top
    "c": bowl("3c3b3Z3w",
              "1wcb2hrcy2",
              "c2Zwb1cbw2",
              "2bch2Zwb"),
}

# ---- d (critic r1: a, b, c read like aljotta and stuffat at 1x): a dense orange-red base (brightness between
# stuffat and aljotta), 2x2 chunks (pumpkin, zucchini, one cauliflower floret), single dark beans, heaped so a few
# pieces rise above the rim. ----
PAL.update({
    "4": hx("#c8582a"), "5": hx("#a8442a"), "6": hx("#82341e"),     # orange-red base lit / mid / back shadow
    "B": hx("#4a2a1c"),                                            # beans
    "x": hx("#d4e08a"),                                            # zucchini pale centre
    "W": hx("#e8dcb0"), "Q": hx("#c8b88e"),                        # cauliflower floret (cream, critic r2), its shade
})


def heaped(r4, r5, r6, r7, r8):
    """bowl() with pixels set into the rim row 4 (x4-11): 'H' and 'L' keep the plain rim (lit left, shaded right)."""
    assert len(r4) == 8
    rows = bowl(r5, r6, r7, r8)
    rows[4] = "..oo" + r4 + "OO.."
    return rows


CANDS["d"] = heaped("HHccLZLL",
                    "64cC4xZ6",
                    "4B44454WQ5",
                    "5cc4B44QQ4",
                    "CC44B454")
LABELS = {"a": "Minestra a (thick)", "b": "Minestra b (chunks)", "c": "Minestra c (cheese)", "d": "Minestra d (heaped)"}
PICK = "d"


def main():
    ims = []
    for k, rows in CANDS.items():
        F.check("minestra_" + k, rows)
        im = render(rows, PAL)
        im.save(os.path.join(F.OUT, f"minestra_{k}.png"))
        ims.append((LABELS[k], im))
    render(CANDS[PICK], PAL).save(os.path.join(F.MOD_ITEMS, "minestra.png"))
    print("wrote minestra_a/b/c, installed", PICK)
    return ims


REFS = ("IMG_20220125_224957.webp", "Minestra-Maltese-Soup-Apron-and-Whisk-4.jpg", "2121.jpg")


def compare(ims):
    """minestra_compare.png: the candidates beside the accepted bowls, the soppa tal-armla and kawlata if installed,
    vanilla beetroot soup; then the in-game hotbar crop (if art/candidates/ingame_minestra/ has it) and reference
    thumbnails (the owner's photos, for the review sheet only)."""
    from font import label_font  # art/tools/font.py
    for n in ("aljotta", "stuffat_fenek", "stuffat_qarnit", "bigilla", "soppa_tal_armla", "kawlata"):
        p = os.path.join(F.MOD_ITEMS, n + ".png")
        if os.path.exists(p):
            ims.append((n.replace("_", " "), Image.open(p).convert("RGBA")))
    ims.append(("vanilla beetroot soup", Image.open(os.path.join(F.VANILLA, "beetroot_soup.png")).convert("RGBA")))
    top = F.compare(ims)
    parts = [top]
    shots = os.path.join(F.OUT, "ingame_minestra")
    hb = [f for f in sorted(os.listdir(shots)) if "hotbar-soups" in f] if os.path.isdir(shots) else []
    if hb:
        im = Image.open(os.path.join(shots, hb[-1])).convert("RGBA")
        w, h = im.size
        k = min(4, max(1, round(w / 427)))          # GUI scale: 4 at 1708+ wide (the brief's crop), 2 at 854
        crop = im.crop((w // 2 - 91 * k, h - 22 * k, w // 2 + 91 * k, h))
        parts.append(crop)                          # as the game shows it (1x)
    refdir = os.path.join(F.ART, "references", "bowls_owner", "minestra")
    thumbs = []
    for r in REFS:
        t = Image.open(os.path.join(refdir, r)).convert("RGBA")
        t.thumbnail((240, 200))
        thumbs.append(t)
    row = Image.new("RGBA", (sum(t.width + 12 for t in thumbs) + 12, 224), (198, 198, 198, 255))
    x = 12
    for t in thumbs:
        row.alpha_composite(t, (x, 4))
        x += t.width + 12
    from PIL import ImageDraw
    ImageDraw.Draw(row).text((12, 206), "references (owner's photos, not traced)", fill=(30, 30, 30, 255),
                             font=label_font(12))
    parts.append(row)
    W = max(p.width for p in parts)
    sheet = Image.new("RGBA", (W, sum(p.height + 8 for p in parts)), (198, 198, 198, 255))
    y = 0
    for p in parts:
        sheet.alpha_composite(p, (0, y))
        y += p.height + 8
    sheet.save(os.path.join(F.OUT, "minestra_compare.png"))


if __name__ == "__main__":
    sys.path.insert(0, os.path.join(HERE, "..", "tools"))
    compare(main())
