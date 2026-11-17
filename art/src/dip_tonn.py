"""The Dip tat-Tonn item icon (Maltese tuna dip, catalogue D70 †: named as a Maltese classic, no single recipe).

What Maltese sources show (research 2026-11-17; photos in art/references/dip_tonn_refonly/, reference only, never
traced, not in git):
- Arjoli, the best-known Maltese tuna dip: tinned tuna, anchovies, tomato paste (kunserva), onion, garlic, olives,
  parsley, chilli, olive oil and vinegar, blitzed with galletti or bread into a coarse paste and eaten with galletti or
  ħobż (Simon Bajada, "Malta: Mediterranean Recipes From the Islands", via nigella.com/recipes/guests/tuna-tomato-dip).
  The book's photo shows a brick-red to orange-red rough paste, flecked with green herbs, beside galletti.
- thefooddictator.com's arjoli adds capers, green olives, sun-dried tomato and the seba' rwejjaħ herbs; its photo
  shows an orange-red, flaky, heaped paste with dark green specks of herb and caper, pale bits of garlic/onion, and
  red oil pooling round the edge of the dish, a parsley sprig on top.
- guidememalta.com (galletti toppings) names arjoli as "made from tuna, anchovies, tomatoes, garlic, onion and herbs"
  and says it "varies from kitchen to kitchen".
- MaltaToday's Gourmet "Tuna dip" is a creamy kind: tuna, pesto, garlic, parsley and chilli folded into home-made
  mayonnaise, served with galletti, crudités and bread; its photo shows a pale khaki-green dip with chopped parsley
  in a terracotta-red bowl. "Everybody has their own tuna dip recipe" (same page).
- † Whether "dip tat-tonn" is the everyday Maltese name for arjoli, or for the creamy mayonnaise kind, is unchecked.

The icon uses the accepted bigilla's terracotta bowl (art/src/bowls.py, bowl "b", plain rim) so every dip matches.
It must read apart from bigilla (brown paste, yellow oil, parsley, chilli), the ġbejna dip (pale cream, pepper,
parsley), the garlic dip, and the aljotta (smooth orange broth, white fish, lemon). So the arjoli candidates are a
deeper tomato red, rough and flaky, with pale tuna flakes, dark capers and olives, and red oil at the rim:
- a: the paste level in the bowl, red oil showing at the back and sides, tuna flakes and capers;
- b: the paste heaped up in a mound that rises over the back rim (a thick spread, not a broth), a parsley sprig on top;
- c: the creamy kind †: a pale salmon-pink tuna mayonnaise with a red kunserva swirl, parsley and capers.

Writes art/candidates/dip_tonn_{a,b,c}.png and art/candidates/dip_tonn_compare.png (1x, 2x and 8x beside the accepted
bigilla and vanilla bowls on inventory grey, plus the in-game hotbar crop when art/candidates/ingame_dip_tonn/ holds
the 21-hotbar-dips shot), and installs candidate c's fill in the dips' own low dish (art/src/dip_dish.py; owner
2026-11-17) as the mod texture item/dip_tonn.png (also art/candidates/dip_tonn_dish.png).
Run:  art/.venv/bin/python art/src/dip_tonn.py
"""
import glob
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "art", "tools"))
sys.path.insert(0, HERE)
from font import label_font  # noqa: E402
from measure import measure  # noqa: E402
import bowls  # noqa: E402  (read only: the shared bowl and its colours)
import dip_dish  # noqa: E402  (the dips' own dish)
from food_items import hx, render, check  # noqa: E402

ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
VANILLA = os.path.join(ROOT, "art", ".vanilla", "item")
OUT = os.path.join(ROOT, "art", "candidates")
INGAME = os.path.join(OUT, "ingame_dip_tonn")

PICK = "c"   # owner 2026-11-17: the creamy pink kind, in the dips' own dish (art/src/dip_dish.py)

# the bowl's own colours (o O H L l m d D), then the dip's
PAL = {k: bowls.PAL[k] for k in "oOHLlmdD"}
PAL.update({
    # arjoli: tomato-red paste lit / mid / shade, the mound's outline
    "1": hx("#d26a3a"), "2": hx("#b04a2a"), "3": hx("#86321c"), "q": hx("#5c2214"),
    "f": hx("#eec29a"), "F": hx("#cc9268"),     # tuna flake, its shade
    "k": hx("#4a5a24"), "K": hx("#3a2630"),     # caper, kalamata olive
    "z": hx("#4f8a3a"), "Z": hx("#356a2a"),     # parsley, its shade
    "r": hx("#9e1e16"), "R": hx("#e4643a"),     # pooled red oil, its shine
    "g": hx("#f2e6c8"),                         # a bit of garlic / onion
    # c: creamy tuna mayonnaise with kunserva
    "4": hx("#e2b89c"), "5": hx("#c8947a"), "6": hx("#a87262"), "7": hx("#c0503a"),
})

# Contents on bowl b (surface rows 5-8: x 4-11, 3-12, 3-12, 4-11). Each map is the whole icon.
MAPS = {
    "a": [
        "................",
        "................",
        "................",
        "....oooooooo....",
        "..ooHHHHLLLLOO..",
        ".oHHR33r3r3rLLO.",
        ".oHR1f2k21fF2LO.",
        ".oL21Ff1z3Kg3lO.",
        ".OLL21k2fF3rllO.",
        ".OLLLLLlllllldO.",
        "..OOllllmmmdOO..",
        "....ODDDDDDO....",
        ".....OOOOOO.....",
        "................",
        "................",
        "................",
    ],
    "b": [
        "................",
        "................",
        "................",
        "....oooqzZqo....",
        "..ooHHq1Z12qOO..",
        ".oHH31f12k23LLO.",
        ".oHR1f2K21fF2LO.",
        ".oL21Ff1z3kg3lO.",
        ".OLL21k2fF3rllO.",
        ".OLLLLLlllllldO.",
        "..OOllllmmmdOO..",
        "....ODDDDDDO....",
        ".....OOOOOO.....",
        "................",
        "................",
        "................",
    ],
    "c": [
        "................",
        "................",
        "................",
        "....oooooooo....",
        "..ooHHHHLLLLOO..",
        ".oHH66656666LLO.",
        ".oH4457774z56LO.",
        ".oL5z4457k455lO.",
        ".OLL5k5577z5llO.",
        ".OLLLLLlllllldO.",
        "..OOllllmmmdOO..",
        "....ODDDDDDO....",
        ".....OOOOOO.....",
        "................",
        "................",
        "................",
    ],
}
# Candidate c's fill, colours unchanged, heaped in the dip dish: pale salmon-pink tuna mayonnaise (4 lit, 5 mid,
# 6 shade), a red kunserva swirl (7), parsley (z) and capers (k); q, a darker pink-brown outline, keeps the mound apart
# from the terracotta.
DISH_PAL = {"a": PAL["4"], "b": PAL["5"], "c": PAL["6"], "q": hx("#7a4a3e"), "7": PAL["7"], "z": PAL["z"],
            "k": PAL["k"]}
# The heap, hand-drawn rows 3-9 for art/src/dip_dish.py (owner 2026-11-17: "theyre heaped a bit too perfectly"):
# '?' paste, other chars toppings; an uneven, lopsided spooned-in silhouette of its own.
DISH_HEAP = {y: r for y, r in enumerate([
    "................",
    "...????.........",
    "..??z???7??.....",
    "..?77?k??777??..",
    "...?z?777??z???.",
    "...?k??z??7?z...",
    "...??????????..."], start=3)}  # slumped to the left, the kunserva swirled through


# The critic's pixel fixes (2026-11-17, art/candidates/critic_dips_C/fix_preview.png), on the finished icon.
DISH_FIXES = {(2, 7): "q", (14, 7): "."}


def dish():
    return dip_dish.icon(DISH_PAL, DISH_HEAP, fixes=DISH_FIXES)


LABELS = {"a": "Dip tat-Tonn a", "b": "Dip tat-Tonn b", "c": "Dip tat-Tonn c †"}


def vcentre(im):
    ys = [y for y in range(16) for x in range(16) if im.getpixel((x, y))[3]]
    return (min(ys) + max(ys)) / 2


def up(im, k):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def compare(cands):
    font = label_font(14)
    ours = [("Bigilla", Image.open(os.path.join(ITEMS, "bigilla.png")).convert("RGBA")),
            ("Aljotta", Image.open(os.path.join(ITEMS, "aljotta.png")).convert("RGBA"))]
    van = [("vanilla " + n, Image.open(os.path.join(VANILLA, n + ".png")).convert("RGBA"))
           for n in ("bowl", "beetroot_soup", "mushroom_stew")]
    pieces = cands + ours + van
    pad, lab, cw = 12, 20, 128 + 16 + 3 * 12
    bg = (139, 139, 139, 255)
    rows = []
    img = Image.new("RGBA", (pad + len(pieces) * cw, lab + 128 + 2 * pad), bg)
    d = ImageDraw.Draw(img)
    for i, (n, im) in enumerate(pieces):
        x0 = pad + i * cw
        d.text((x0, 2), n, font=font, fill=(20, 20, 20, 255))
        img.alpha_composite(up(im, 8), (x0, lab + pad // 2))
        img.alpha_composite(im, (x0 + 128 + pad // 2, lab + 56))
    rows.append(img)
    for k in (1, 2):   # as in the hotbar, and at GUI scale 2
        strip = Image.new("RGBA", (pad + len(pieces) * (16 * k + 4 * k), 16 * k + 2 * pad), bg)
        for i, (n, im) in enumerate(pieces):
            strip.alpha_composite(up(im, k), (pad + i * (16 * k + 4 * k), pad))
        rows.append(strip)
    shots = sorted(glob.glob(os.path.join(INGAME, "*21-hotbar-dips*.png")))
    if shots:
        s = Image.open(shots[-1]).convert("RGBA")
        w, h = s.size
        crop = up(s.crop((w // 2 - 182, h - 44, w // 2 + 182, h)), 2)
        img = Image.new("RGBA", (crop.width + 2 * pad, crop.height + lab + 2 * pad), (232, 232, 228, 255))
        ImageDraw.Draw(img).text((pad, 2), "in game: bigilla, ġbejna dip, dip tat-tonn, garlic dip, galletti, aljotta, "
                                 "beetroot soup, mushroom stew, bowl", font=font, fill=(20, 20, 20, 255))
        img.alpha_composite(crop, (pad, lab + pad // 2))
        rows.append(img)
    W = max(r.width for r in rows)
    sheet = Image.new("RGBA", (W, sum(r.height + 4 for r in rows)), (200, 200, 196, 255))
    y = 0
    for r in rows:
        sheet.alpha_composite(r, (0, y))
        y += r.height + 4
    p = os.path.join(OUT, "dip_tonn_compare.png")
    sheet.save(p)
    print("wrote", os.path.relpath(p, ROOT))


def main():
    os.makedirs(OUT, exist_ok=True)
    cands = []
    for letter, rows in MAPS.items():
        name = f"dip_tonn_{letter}"
        check(name, rows)
        im = render(rows, PAL)
        p = os.path.join(OUT, name + ".png")
        im.save(p)
        m = measure(p)
        print(name, {k: float(m[k]) if k != "colours" else m[k] for k in ("coverage", "colours", "edge_l", "interior_l",
                                                                       "tl_minus_br")},
              "outline/inside", round(float(m["edge_l"] / m["interior_l"]), 2), "vcentre", vcentre(im))
        cands.append((LABELS[letter], im))
    rows, im = dish()
    check("dip_tonn_dish", rows)
    p = os.path.join(OUT, "dip_tonn_dish.png")
    im.save(p)
    m = measure(p)
    print("dip_tonn_dish", {k: float(m[k]) if k != "colours" else m[k] for k in ("coverage", "colours", "edge_l",
                                                                             "interior_l", "tl_minus_br")},
          "outline/inside", round(float(m["edge_l"] / m["interior_l"]), 2), "vcentre", vcentre(im))
    im.save(os.path.join(ITEMS, "dip_tonn.png"))
    cands.insert(0, ("Dip tat-Tonn (dish, c, installed)", im))
    compare(cands)


if __name__ == "__main__":
    main()
