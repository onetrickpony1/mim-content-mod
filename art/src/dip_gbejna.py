"""Dip tal-Ġbejna (ġbejna dip, catalogue D69): item icon candidates.

Peppered dried ġbejna blended with cream cheese, olive oil, garlic and parsley: a thick pale cream dip flecked with
black pepper and green parsley, a drizzle of oil and cracked pepper on top, often a few ġbejna cubes and a parsley
sprig in the middle; eaten with galletti. References (web photos, reference only, not in git):
art/references/dip_gbejna_refonly/apronwhisk_{1,3,4,6}.jpg (apronandwhisk.com/gbejna-dip/).

The container is the shared terracotta bowl "b" (art/src/bowls.py, plain rim), the same as the accepted bigilla, so the
dips read as a set. The cream is the dried ġbejniet's warm ivory (art/src/gbejniet.py), a little greyer, as in the
photos. What sets it apart from bigilla (dark brown, red chilli) is the pale cream with black pepper.
- a: flat and swirled, an oil pool on the left, ġbejna cubes and a parsley sprig in the middle;
- b: heaped to the back rim in a soft mound (lit top left), pepper and parsley flecks, a little oil;
- c: flat, an oil drizzle curving across, a parsley sprig and cracked pepper.

Installed (owner 2026-11-17, "i like the low terracotta dish, but without the galletta"): candidate a's fill heaped in
the dips' own low dish (art/src/dip_dish.py), not the soup bowl.

Writes art/candidates/dip_gbejna_{a,b,c}.png, dip_gbejna_dish.png and dip_gbejna_compare.png, installs the dish
version as mod textures item/dip_gbejna.png. Reads bowls.py's bowl, never writes its files.
Run:  art/.venv/bin/python art/src/dip_gbejna.py
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
import bowls as B  # noqa: E402  (read only)
import food_items as F  # noqa: E402  (read only)
import dip_dish  # noqa: E402  (the dips' own dish)

hx, render = F.hx, F.render
ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
OUT = os.path.join(ROOT, "art", "candidates")
INGAME = os.path.join(OUT, "ingame_dip_gbejna")

PICK = "a"

PAL = {k: B.PAL[k] for k in "oOHLlmdD"}   # the shared terracotta bowl
PAL.update({
    "1": hx("#e8dec2"), "2": hx("#d4c8a6"), "4": hx("#beb08c"), "3": hx("#a89a78"),   # dip: lit, mid, swirl, back shade
    "p": hx("#2e2620"), "P": hx("#4e4236"),                                             # cracked black pepper
    "j": hx("#e0c048"), "J": hx("#c4a236"),                                             # olive oil, pooled darker
    "z": hx("#4f8a3a"), "Z": hx("#2f5e24"),                                             # parsley
    "c": hx("#fbf6e6"), "C": hx("#d6c9a2"),                                             # ġbejna cube, its side
    "q": hx("#9c8a68"), "Q": hx("#7c6a4c"),                                             # the mound's outline (b)
})


def onto_bowl(contents, over=None):
    """Bowl b with its surface ('?' cells, rows 5-8) filled left to right from contents[y]; over = {y: row} replaces
    whole rows (the mound in b)."""
    g, zone = B.bowl("b")
    for y, s in contents.items():
        xs = [x for x in range(16) if zone[y][x]]
        assert len(xs) == len(s), (y, len(xs), s)
        for x, c in zip(xs, s):
            g[y][x] = c
    for y, row in (over or {}).items():
        assert len(row) == 16, (y, row)
        g[y] = list(row)
    return ["".join(r) for r in g]


def cand_a():
    return onto_bowl({5: "3333p333",
                      6: "1j12zZ1p42",
                      7: "2JjcCz24p2",
                      8: "2p224P22"})


def cand_b():
    return onto_bowl({5: "1z1j1242",
                      6: "212z214p22",
                      7: "2p2142z242",
                      8: "42p22422"},
                     {3: "....ooqqqqoo....",
                      4: "..ooHH1j12LLOO.."})


def cand_c():
    return onto_bowl({5: "33333p33",
                      6: "12jj21z2p2",
                      7: "pj21zZ2412",
                      8: "2jJ22p22"})


CANDS = (("a", cand_a), ("b", cand_b), ("c", cand_c))

# Candidate a's fill in the dip dish: cream, black pepper, a yellow oil pool, ġbejna cubes (i lit, k side), parsley.
DISH_PAL = {"a": PAL["1"], "b": PAL["2"], "c": hx("#b4a684"), "q": hx("#7c6e52"),
            "p": PAL["p"], "j": PAL["j"], "e": PAL["J"], "z": PAL["z"], "Z": PAL["Z"], "i": PAL["c"], "k": PAL["C"]}
# The heap, hand-drawn rows 3-9 for art/src/dip_dish.py (owner 2026-11-17: "theyre heaped a bit too perfectly"):
# '?' paste, other chars toppings; an uneven, lopsided spooned-in silhouette of its own.
DISH_HEAP = {y: r for y, r in enumerate([
    "......ii........",
    "....??kk?.......",
    "...??p????.???..",
    "...?jjp??p?ii?..",
    "..??ejjZz??kk?..",
    "...?p??z??p??...",
    "...??????????..."], start=3)}  # a cube on the tall spoonful, oil in the swoop


# The critic's pixel fixes (2026-11-17, art/candidates/critic_dips_C/fix_preview.png), on the finished icon.
DISH_FIXES = {(10, 6): "b", (11, 6): "k", (12, 6): "k"}


def dish():
    return dip_dish.icon(DISH_PAL, DISH_HEAP, fixes=DISH_FIXES)


def vcentre(im):
    ys = [y for y in range(16) for x in range(16) if im.getpixel((x, y))[3]]
    return (min(ys) + max(ys)) / 2


def main():
    os.makedirs(OUT, exist_ok=True)
    ims = []
    for k, make in CANDS:
        rows = make()
        F.check(f"dip_gbejna_{k}", rows)
        im = render(rows, PAL)
        p = os.path.join(OUT, f"dip_gbejna_{k}.png")
        im.save(p)
        m = measure(p)
        print(f"dip_gbejna_{k}", {x: m[x] for x in ("coverage", "colours", "edge_l", "interior_l", "tl_minus_br")},
              "outline/inside", round(m["edge_l"] / m["interior_l"], 2), "vcentre", vcentre(im))
        ims.append((f"Dip tal-Ġbejna {k}" + (" (pick)" if k == PICK else ""), im))
    rows, im = dish()
    F.check("dip_gbejna_dish", rows)
    p = os.path.join(OUT, "dip_gbejna_dish.png")
    im.save(p)
    m = measure(p)
    print("dip_gbejna_dish", {x: m[x] for x in ("coverage", "colours", "edge_l", "interior_l", "tl_minus_br")},
          "outline/inside", round(m["edge_l"] / m["interior_l"], 2), "vcentre", vcentre(im))
    im.save(os.path.join(ITEMS, "dip_gbejna.png"))
    ims.insert(0, ("Dip tal-Ġbejna (dish, installed)", im))
    for n, lbl in (("bigilla", "Bigilla"), ("gbejna_niexfa", "Ġbejna niexfa"), ("gbejna_tal_bzar", "Ġbejna tal-bżar"),
                   ("galletti", "Galletti")):
        ims.append((lbl, Image.open(os.path.join(ITEMS, n + ".png")).convert("RGBA")))
    for v in ("bowl", "beetroot_soup", "mushroom_stew"):
        ims.append(("vanilla " + v, Image.open(os.path.join(F.VANILLA, v + ".png")).convert("RGBA")))
    sheet = F.compare(ims)
    shots = sorted(glob.glob(os.path.join(INGAME, "*21-hotbar-dips*.png")))
    if shots:
        crop = Image.open(shots[-1]).convert("RGBA")
        crop = crop.resize((crop.width * 2, crop.height * 2), Image.NEAREST)
        pad, lab = 16, 22
        full = Image.new("RGBA", (max(sheet.width, crop.width + 2 * pad), sheet.height + crop.height + lab + pad),
                         (198, 198, 198, 255))
        full.alpha_composite(sheet, (0, 0))
        ImageDraw.Draw(full).text((pad, sheet.height), "in game (x2): bigilla, ġbejna dip, tuna dip, garlic dip, "
                                  "galletti, aljotta, beetroot soup, mushroom stew, bowl", font=label_font(12),
                                  fill=(30, 30, 30, 255))
        full.alpha_composite(crop, (pad, sheet.height + lab))
        sheet = full
    p = os.path.join(OUT, "dip_gbejna_compare.png")
    sheet.save(p)
    print("wrote", os.path.relpath(p, ROOT))


if __name__ == "__main__":
    main()
