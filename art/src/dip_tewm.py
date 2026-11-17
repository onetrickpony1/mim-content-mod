"""The dip tat-tewm item icon (Maltese garlic dip, catalogue D71 †), in the shared terracotta bowl.

What the dip is (research 2026-11-17):
- "Garlic dip" is named among the classic Maltese galletti dips next to bigilla, arjoli, tuna dip and cheese dip
  (Apron & Whisk, "Ġbejna dip", https://apronandwhisk.com/gbejna-dip/), but no Maltese recipe or description of it
  was found on Maltese recipe sites, menus or guides (Guide Me Malta's nine galletti toppings, Lolly's Kitchen's Maltese
  platter, The Healthy Malteser, Mananni's menu).
- It is not arjoli: arjoli is a separate dish in the catalogue (D11), a red-brown bread, tomato, herb, olive, caper and
  anchovy paste (https://apronandwhisk.com/maltese-arjoli-dip/, https://thehealthymalteser.com/arjoli_dip/).
- So its look is an assumption †: a smooth, very white creamy garlic dip (the cream cheese, mayonnaise or yoghurt kind
  sold for platters, like the garlic yoghurt dip and the Levantine toum in the reference photos), with a swirl on top,
  a little green herb (parsley†) and no pepper.
References (reference only, never traced; not in git): art/references/dip_tewm_refonly/.

Telling it apart from the other dips in the same bowl:
- bigilla: brown bean paste, oil, red chilli, lots of parsley;
- ġbejna dip: pale cream with black pepper flecks and parsley;
- this one: the whitest and smoothest of the set (a cool white, not cream), a raised swirl, no pepper, only a few green
  flecks, and a garlic sign the others don't have: an unpeeled clove (white with a pink-purple skin) or a whole bulb.

Candidates (all in bowl b, the bigilla bowl from bowls.py, plain rim):
- a: white swirl, a few herb flecks, one unpeeled garlic clove resting on the right of the rim;
- b: white swirl, a few herb flecks, a whole garlic bulb in front of the bowl at the bottom right;
- c: white swirl with a small green herb sprig in the middle and a drop of olive oil, no garlic piece.

Installed version (owner 2026-11-17): "the garlic dip needs to seem thicker, possibly by being more greyish too rather
than so white", and the dips get their own low terracotta dish (art/src/dip_dish.py, "without the galletta"). So the
installed icon is a stiff, combed grey-cream paste (lit #dcd8cc, mid #c2beb0, shade #a29e90, ridges #aca796 with
#e8e5dc highlights) standing up in a small peak, no pepper, a few parsley flecks, and an unpeeled garlic clove (white
with a pink-purple streak) lying on top as the garlic sign; the ġbejna dip stays warm ivory with black pepper.

Writes art/candidates/dip_tewm_{a,b,c}.png, dip_tewm_dish.png and dip_tewm_compare.png (1x, 2x and 8x beside bigilla
and the vanilla bowls, on inventory grey) and installs the dish version as mod texture item/dip_tewm.png.
Run:  art/.venv/bin/python art/src/dip_tewm.py
"""
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "art", "tools"))
sys.path.insert(0, HERE)
from font import label_font  # noqa: E402
import bowls as B  # noqa: E402  (read only: the bowl colours and the accepted bigilla)
import dip_dish  # noqa: E402  (the dips' own dish)
from measure import measure  # noqa: E402
from food_items import hx, render, check  # noqa: E402

ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
VANILLA = os.path.join(ROOT, "art", ".vanilla", "item")
OUT = os.path.join(ROOT, "art", "candidates")

PAL = {k: B.PAL[k] for k in "oOHLlmdD"}   # the shared terracotta bowl
PAL.update({
    "w": hx("#f7f5ee"), "q": hx("#e6e2d6"), "Q": hx("#c4bcaa"),   # garlic dip: lit / mid / shade under the back lip
    "s": hx("#d0c9b8"),                                          # the swirl's shadow side
    "g": hx("#5e8f36"), "G": hx("#3f6a26"),                      # parsley† / its shade
    "y": hx("#d8bc54"),                                          # olive oil
    "1": hx("#f4eee6"), "2": hx("#dcc2bc"), "3": hx("#a8707e"),  # garlic skin: lit / pink / purple streak
    "u": hx("#8e6e74"), "U": hx("#5e4450"), "k": hx("#b49a72"),  # garlic outline lit / shade, dry stem
})

# Bowl b with the dip; rows 5-8 are the surface. The swirl: a raised ring lit on its top-left, 's' on its lower-right.
DIP = [
    "................",
    "................",
    "................",
    "....oooooooo....",
    "..ooHHHHLLLLOO..",
    ".oHHQQQQQQQQLLO.",
    ".oHqwwwwsqqgqLO.",
    ".oLqwsqwwsqwqlO.",
    ".OLLqgqqssqqllO.",
    ".OLLLLLlllllldO.",
    "..OOllllmmmdOO..",
    "....ODDDDDDO....",
    ".....OOOOOO.....",
    "................",
    "................",
    "................",
]

# a: one unpeeled clove leaning on the right of the rim (pointed tip up, plump base, purple streak, dark outline).
CLOVE = {(12, 2): "u", (11, 3): "u", (12, 3): "1", (13, 3): "U", (11, 4): "1", (12, 4): "2", (13, 4): "U",
         (11, 5): "1", (12, 5): "3", (13, 5): "U", (12, 6): "U"}
# b: a whole bulb in front of the bowl, bottom right (dry stem, round body, purple streaks, shaded lower right).
BULB = {(13, 9): "k", (12, 10): "u", (13, 10): "1", (14, 10): "u",
        (11, 11): "u", (12, 11): "1", (13, 11): "1", (14, 11): "2", (15, 11): "U",
        (11, 12): "u", (12, 12): "1", (13, 12): "3", (14, 12): "2", (15, 12): "U",
        (11, 13): "u", (12, 13): "2", (13, 13): "1", (14, 13): "3", (15, 13): "U",
        (12, 14): "U", (13, 14): "U", (14, 14): "U"}
# c: a herb sprig on the swirl's top and a small pool of oil in the dip.
SPRIG = {(7, 6): "g", (8, 5): "g", (8, 6): "G", (9, 6): "g", (6, 7): "y", (7, 8): "y"}


DISH_PAL = {"a": hx("#dcd8cc"), "b": hx("#c2beb0"), "c": hx("#a29e90"), "q": hx("#77736a"),
            "w": hx("#aca796"), "W": hx("#e8e5dc"),                        # ridge shadow, ridge highlight
            "z": hx("#5e8f36"),                                            # parsley†
            "i": hx("#f7f3ea"), "v": hx("#c896a6"), "n": hx("#8a5a70")}    # garlic clove: skin, pink, purple
# The heap, hand-drawn rows 3-9 for art/src/dip_dish.py (owner 2026-11-17: "theyre heaped a bit too perfectly"):
# '?' paste, other chars toppings; an uneven, lopsided spooned-in silhouette of its own.
DISH_HEAP = {y: r for y, r in enumerate([
    ".........??.....",
    "........?W??....",
    "......?Ww?w??...",
    "....??iv?Ww?w?..",
    "...?w?vnW?w??w?.",
    "...w?z?w??w?z...",
    "...??????????..."], start=3)}  # stiff: a peak off to the right, the clove on the left slope


# The critic's pixel fixes (2026-11-17, art/candidates/critic_dips_C/fix_preview.png), on the finished icon.
DISH_FIXES = {(14, 7): ".", (13, 7): "q"}


def dish():
    return dip_dish.icon(DISH_PAL, DISH_HEAP, fixes=DISH_FIXES)


def make(extra):
    g = [list(r) for r in DIP]
    for (x, y), c in extra.items():
        g[y][x] = c
    return ["".join(r) for r in g]


CANDS = (("a", "clove on the rim", CLOVE), ("b", "garlic bulb in front", BULB), ("c", "herb sprig, oil", SPRIG))


def v_centre(im):
    ys = [y for y in range(16) for x in range(16) if im.getpixel((x, y))[3]]
    return sum(ys) / len(ys)


def compare(ims):
    slot, bg, ink = (139, 139, 139, 255), (198, 198, 198, 255), (30, 30, 30, 255)
    S, cw = 8, 16 * 8 + 20
    sheet = Image.new("RGBA", (16 + len(ims) * cw, 16 + 48 + 16 * S + 40), bg)
    d = ImageDraw.Draw(sheet)
    f = label_font(12)
    for i, (n, im) in enumerate(ims):
        x0 = 16 + i * cw
        d.rectangle([x0, 16, x0 + 17, 33], fill=slot)
        sheet.alpha_composite(im, (x0 + 1, 17))
        d.rectangle([x0 + 30, 16, x0 + 65, 51], fill=slot)
        sheet.alpha_composite(im.resize((32, 32), Image.NEAREST), (x0 + 32, 18))
        y8 = 64
        d.rectangle([x0, y8, x0 + 16 * S - 1, y8 + 16 * S - 1], fill=slot)
        sheet.alpha_composite(im.resize((16 * S, 16 * S), Image.NEAREST), (x0, y8))
        d.text((x0, y8 + 16 * S + 4), n, fill=ink, font=f)
    return sheet


def main():
    os.makedirs(OUT, exist_ok=True)
    ims = []
    for k, desc, extra in CANDS:
        rows = make(extra)
        check("dip_tewm_" + k, rows)
        im = render(rows, PAL)
        im.save(os.path.join(OUT, f"dip_tewm_{k}.png"))
        ims.append((f"Dip tat-tewm {k}", im))
        print(f"dip_tewm_{k}: {desc}, vertical centre {v_centre(im):.2f}")
    ims.insert(0, ("Dip tat-Tewm (dish, installed)", dish()[1]))
    ims.append(("Bigilla", B.bigilla_dish()[1]))
    for v in ("bowl", "mushroom_stew", "beetroot_soup"):
        ims.append(("vanilla " + v, Image.open(os.path.join(VANILLA, v + ".png")).convert("RGBA")))
    compare(ims).save(os.path.join(OUT, "dip_tewm_compare.png"))
    rows, im = dish()
    check("dip_tewm_dish", rows)
    p = os.path.join(OUT, "dip_tewm_dish.png")
    im.save(p)
    m = measure(p)
    print("dip_tewm_dish", {k: m[k] for k in ("coverage", "colours", "edge_l", "interior_l", "tl_minus_br")},
          "outline/inside", round(m["edge_l"] / m["interior_l"], 2), "vcentre", (lambda ys: (min(ys) + max(ys)) / 2)(
              [y for y in range(16) for x in range(16) if im.getpixel((x, y))[3]]))
    im.save(os.path.join(ITEMS, "dip_tewm.png"))
    print("installed dip_tewm (dish)")


if __name__ == "__main__":
    main()
