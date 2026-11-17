"""Dip containers: candidate concepts so a dip never reads as a soup (candidates only, 2026-11-17; NOT in the mod).

The owner (2026-11-17): "we need to rethink the containers of the dips, as with so many it will be confusing which are
dips and which are soups (they share a bowl) so we need something different". Today every dip and every soup sits in
the shared terracotta bowl "b" (art/src/bowls.py). Each concept below puts all four dips in the same new container:
- A, ramekin: a small, low, straight-sided blue glazed ramekin, the dip heaped above its rim;
- B, galletta: a small shallow terracotta dish, lower than the soup bowl, with a galletta stood upright in the dip;
- C, plate: a flat white plate with a blue rim (a platt Malti), a dollop of dip and two galletti beside it;
- D, tub: a clear deli tub heaped with dip, as bigilla is sold at pastizzeriji and kiosks (the owner's bigilla photos).
In every concept the dip is a thick paste heaped into a mound with its own outline, never a flat liquid level.

The fills (critic and owner, 2026-11-17):
- bigilla: the accepted brown bean paste, olive oil, parsley, red chilli (art/src/bowls.py, BIGILLA_ACCEPTED colours);
- ġbejna dip: candidate a's fill (cream, black pepper, a yellow oil pool, ġbejna cubes, parsley; art/src/dip_gbejna.py);
- tuna dip: the creamy kind (owner's pick), pale khaki-green with parsley, one chilli fleck and a caper, no pink and no
  kunserva swirl (the critic's recolour of art/src/dip_tonn.py c);
- garlic dip (owner: "needs to seem thicker, possibly by being more greyish too rather than so white"): a stiff, ridged,
  peaked grey-cream paste, no pepper, a few parsley flecks and an unpeeled garlic clove on top as the garlic sign.

References (reference only, never traced, not in git): art/references/bowls_owner/bigilla/ (small bowls, clear tubs,
galletti beside), art/references/dip_{gbejna,tonn,tewm}_refonly/.

Writes art/candidates/dip_containers/{A,B,C,D}_{bigilla,gbejna,tonn,tewm}.png, hotbar_{A,B,C,D}.png and
art/candidates/dip_containers_compare.png. Reads the installed soups and vanilla items; writes nothing into the mod.
The owner picked B without the galletta (2026-11-17): that dish is art/src/dip_dish.py, used by every dip script.
Run:  art/.venv/bin/python art/src/dip_containers.py
"""
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "art", "tools"))
sys.path.insert(0, HERE)
from font import label_font  # noqa: E402
from measure import measure  # noqa: E402
import bowls as B  # noqa: E402  (read only: the terracotta colours and galletti colours)
import dip_dish as D  # noqa: E402  (the paste mound, shared with the installed dips)
from food_items import hx, render, check  # noqa: E402  (read only)

ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
VANILLA = os.path.join(ROOT, "art", ".vanilla", "item")
OUT = os.path.join(ROOT, "art", "candidates", "dip_containers")
SHEET = os.path.join(ROOT, "art", "candidates", "dip_containers_compare.png")


def mix(c1, c2, t):
    return tuple(round(a + (b - a) * t) for a, b in zip(c1, c2))


# ---- The four dips: paste ramp a lit / b mid / c shade / q outline, then toppings. ----
# Topping patterns are centred on the paste's centre; '.' keeps the paste; only inner paste cells are painted.
DIPS = {
    "bigilla": dict(
        label="Bigilla",
        pal={"a": hx("#8e766a"), "b": hx("#6e5a50"), "c": hx("#4e3e38"), "q": hx("#3a2c28"),
             "j": hx("#d6b04a"), "e": hx("#b89a3e"), "z": hx("#4f8a3a"), "x": hx("#c8402a")},
        tops=["..x..z...",
              ".ejjz.zx.",
              "z.ez.x..z",
              "..zx..z.."]),
    "gbejna": dict(
        label="Dip tal-Ġbejna",
        pal={"a": hx("#e8dec2"), "b": hx("#d4c8a6"), "c": hx("#b4a684"), "q": hx("#8c7e60"),
             "p": hx("#2e2620"), "j": hx("#e0c048"), "e": hx("#c4a236"), "z": hx("#4f8a3a"), "Z": hx("#2f5e24"),
             "i": hx("#fbf6e6"), "k": hx("#d6c9a2")},
        tops=["..p...p..",
              ".jj.iiz.p",
              "pej.kkZ..",
              "...p..p.z"]),
    "tonn": dict(
        label="Dip tat-Tonn",
        pal={"a": hx("#cccb9c"), "b": hx("#aeae7e"), "c": hx("#8a8a5e"), "q": hx("#62623e"),
             "z": hx("#4f8a3a"), "Z": hx("#356a2a"), "x": hx("#c0503a"), "k": hx("#3e4a1e")},
        tops=["..z...z..",
              ".zZz..x.z",
              "z..k.zZ..",
              "..z..z.z."]),
    "tewm": dict(
        label="Dip tat-Tewm",
        pal={"a": hx("#dcd8cc"), "b": hx("#c2beb0"), "c": hx("#a29e90"), "q": hx("#77736a"),
             "w": hx("#aca796"), "W": hx("#e8e5dc"),       # ridge shadow, ridge highlight (a stiff, combed paste)
             "z": hx("#5e8f36"),                           # parsley†
             "i": hx("#f7f3ea"), "v": hx("#c896a6"), "n": hx("#8a5a70")},   # garlic clove: skin, pink, purple
        peak=True,
        tops=[".Ww..Ww..",
              "w.Ww.iv.w",
              ".w..Wvnw.",
              "z.w..w.zw"]),
}
DIP_ORDER = ("bigilla", "gbejna", "tonn", "tewm")

GALL = {"(": B.GAL3["o"], ")": B.GAL3["O"], "[": B.GAL3["s"], "]": B.GAL3["h"], "{": B.GAL3["l"],
        "}": B.GAL3["t"], "<": B.GAL3["k"]}


# ---- Containers: rows with '?' for the paste; digits (and the bowl letters in B) for the container. ----
RAMEKIN = [   # A: a small, low, straight-sided blue glazed ramekin; dip heaped over the rim
    "................",
    "................",
    "................",
    "................",
    "......????......",
    "....????????....",
    "..5??????????5..",
    "..56????????45..",
    "..566666666445..",
    "..501010101225..",
    "..500101012225..",
    "...5555555555...",
    "................",
    "................",
    "................",
    "................",
]
RAMEKIN_PAL = {"0": hx("#6a94cc"), "1": hx("#4a76b4"), "2": hx("#365c96"), "4": hx("#7ea0cc"),
               "5": hx("#223e6c"), "6": hx("#b4cce8")}

DISH = [      # B: a small shallow terracotta dish (the borma clay) with a flared lip, much lower than the soup bowl
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    ".....??????.....",
    "...??????????...",
    "..o??????????O..",
    ".oH??????????lO.",
    ".OHLLLLLLllllldO",
    "..OOlllmmmmdOO..",
    "....OODDDDOO....",
    "................",
    "................",
    "................",
]
DISH_PAL = {k: B.PAL[k] for k in "oOHLlmdD"}
# The galletta stood upright in the dip at the back right, drawn before the paste so the paste covers its foot.
GALLETTA_UP = [
    "..())..",
    ".(]]{).",
    "(]<{<{)",
    "(]{{{})",
    "({<{<})",
    ".(}}}).",
    "..)))..",
]


def tub_pal(dip):
    """D: the clear tub shows the paste through its sides, paler; a white rim and a light streak."""
    p = DIPS[dip]["pal"]
    w = (246, 246, 244)
    return {"0": mix(p["a"], w, 0.25), "1": mix(p["b"], w, 0.18), "2": mix(p["c"], w, 0.1),
            "5": mix(p["q"], (40, 40, 44), 0.35), "6": hx("#eeeeec"), "4": hx("#c8c8c6"), "3": hx("#fafaf8")}


TUB = [       # D: a clear deli tub, taller and tapered, heaped with dip; '3' a light streak down the plastic
    "................",
    "................",
    "................",
    "......????......",
    "....????????....",
    "...??????????...",
    "..6??????????4..",
    "..566666666445..",
    "..530111111225..",
    "..530111111225..",
    "...5301111225...",
    "...5301111225...",
    "...5301112225...",
    "....55555555....",
    "................",
    "................",
]


PLATE_PAL = {"7": hx("#f2eee4"), "8": hx("#dcd6c8"), "9": hx("#b8b0a0"), "3": hx("#4a72b0"),
             "5": hx("#3c4a64"), "6": hx("#8e8878")}


def ell(x, y, cx, cy, rx, ry):
    return ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2


def plate():
    """C: a flat round plate seen from three-quarter: white glaze, a blue rim line, a thin underside, a dark outline;
    a dollop of dip on the left, two galletti lying flat on the right."""
    g = [["."] * 16 for _ in range(16)]
    cx, cy, rx, ry = 8.0, 8.2, 7.6, 3.4
    for y in range(16):
        for x in range(16):
            e = ell(x, y, cx, cy, rx, ry)
            if e <= 1:
                s = (x + .5 - cx) / rx + (y + .5 - cy) / ry
                g[y][x] = "3" if 0.55 <= e <= 0.8 else ("7" if s < -0.5 else "9" if s > 0.9 else "8")
            elif ell(x, y - 1, cx, cy, rx, ry) <= 1:
                g[y][x] = "6"
    out = [r[:] for r in g]
    for y in range(16):
        for x in range(16):
            if g[y][x] == ".":
                continue
            if any(not (0 <= x + dx < 16 and 0 <= y + dy < 16) or g[y + dy][x + dx] == "."
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y][x] = "5"
    g = out
    # two galletti lying flat (ellipses), the back one first
    for gx, gy in ((12.2, 6.6), (11.2, 8.9)):
        cells = {(x, y) for y in range(16) for x in range(16) if ell(x, y, gx, gy, 2.9, 1.75) <= 1}
        for x, y in cells:
            edge = any((x + dx, y + dy) not in cells for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            s = (x + .5 - gx) + (y + .5 - gy) * 1.6
            g[y][x] = (")" if s > 0 else "(") if edge else ("}" if s > 1.2 else "]" if s < -1 else "{")
        for hxp, hyp in ((-1, 0), (1, 0)):
            x, y = int(gx + hxp), int(gy)
            if g[y][x] in "]{}":
                g[y][x] = "<"
    # the dollop's zone
    zone = {(x, y) for y in range(16) for x in range(16) if ell(x, y, 6.0, 6.6, 4.6, 3.6) <= 1 and y <= 8}
    for x, y in zone:
        g[y][x] = "?"
    return ["".join(r) for r in g]


def galletta_dish():
    g = [list(r) for r in DISH]
    for j, r in enumerate(GALLETTA_UP):
        for i, c in enumerate(r):
            if c != ".":
                g[3 + j][8 + i] = c
    return ["".join(r) for r in g]


CONCEPTS = {
    "A": dict(label="A: blue ramekin", rows=lambda d: RAMEKIN, pal=lambda d: dict(RAMEKIN_PAL)),
    "B": dict(label="B: shallow dish + galletta", rows=lambda d: galletta_dish(), pal=lambda d: {**DISH_PAL, **GALL}),
    "C": dict(label="C: plate with galletti", rows=lambda d: plate(), pal=lambda d: {**PLATE_PAL, **GALL}),
    "D": dict(label="D: clear tub", rows=lambda d: TUB, pal=tub_pal),
}


def paste(rows, dip):
    spec = DIPS[dip]
    return D.paste(rows, spec["tops"], spec.get("peak", False))


def make(concept, dip):
    c = CONCEPTS[concept]
    rows = paste(c["rows"](dip), dip)
    pal = {**c["pal"](dip), **DIPS[dip]["pal"]}
    return rows, render(rows, pal)


def vcentre(im):
    ys = [y for y in range(16) for x in range(16) if im.getpixel((x, y))[3]]
    return (min(ys) + max(ys)) / 2


def up(im, k):
    return im.resize((16 * k, 16 * k), Image.NEAREST)


def item(name):
    return Image.open(os.path.join(ITEMS, name + ".png")).convert("RGBA")


def vanilla(name):
    return Image.open(os.path.join(VANILLA, name + ".png")).convert("RGBA")


SOUPS = (("Aljotta", "aljotta"), ("Minestra", "minestra"), ("Brodu tat-tiġieġ", "brodu_tat_tigieg"),
         ("Kawlata", "kawlata"))
VANILLA_SOUPS = (("vanilla mushroom stew", "mushroom_stew"), ("vanilla beetroot soup", "beetroot_soup"))
GREY, BG, INK = (139, 139, 139, 255), (198, 198, 198, 255), (24, 24, 24, 255)


def hotbar(icons, k):
    """A mock vanilla hotbar: 9 slots, each 20 px (x k) with a dark frame, the icon in the middle."""
    w = 9 * 20 * k + 2 * k
    im = Image.new("RGBA", (w, 22 * k), (40, 40, 40, 255))
    d = ImageDraw.Draw(im)
    for i in range(9):
        x0 = k + i * 20 * k
        d.rectangle([x0, k, x0 + 20 * k - 1, 21 * k - 1], fill=(82, 82, 82, 255))
        d.rectangle([x0 + k, 2 * k, x0 + 19 * k - 1, 20 * k - 1], fill=GREY)
        if i < len(icons):
            im.alpha_composite(up(icons[i], k), (x0 + 2 * k, 3 * k))
    return im


def hotbar_icons(made):
    return [made["bigilla"], item("aljotta"), made["gbejna"], item("minestra"), made["tonn"], item("kawlata"),
            made["tewm"], item("brodu_tat_tigieg"), vanilla("mushroom_stew")]


def sheet(all_made):
    f, fs = label_font(15), label_font(12)
    cw = 128 + 12 + 16 + 14
    pieces = [(DIPS[d]["label"], None, d) for d in DIP_ORDER] + \
             [(lbl, item(n), None) for lbl, n in SOUPS] + [(lbl, vanilla(n), None) for lbl, n in VANILLA_SOUPS]
    rowh = 22 + 128 + 20
    blocks = []
    for ck, made in all_made.items():
        hb1, hb2 = hotbar(hotbar_icons(made), 1), hotbar(hotbar_icons(made), 2)
        W = 16 + len(pieces) * cw
        H = 26 + rowh + 18 + hb1.height + 10 + hb2.height + 18
        im = Image.new("RGBA", (W, H), BG)
        d = ImageDraw.Draw(im)
        d.text((16, 4), CONCEPTS[ck]["label"] + "  (dips left, soups right)", font=f, fill=INK)
        for i, (lbl, soup, dip) in enumerate(pieces):
            ic = made[dip] if dip else soup
            x0, y0 = 16 + i * cw, 26
            if i == len(DIP_ORDER):
                d.line([x0 - 8, y0, x0 - 8, y0 + rowh - 4], fill=(90, 90, 90, 255), width=2)
            d.rectangle([x0, y0, x0 + 127, y0 + 127], fill=GREY)
            im.alpha_composite(up(ic, 8), (x0, y0))
            d.rectangle([x0 + 134, y0 + 56, x0 + 134 + 17, y0 + 56 + 17], fill=GREY)
            im.alpha_composite(ic, (x0 + 135, y0 + 57))
            d.text((x0, y0 + 131), lbl, font=fs, fill=INK)
        y = 26 + rowh
        d.text((16, y), "hotbar 1x and 2x: bigilla, aljotta, ġbejna dip, minestra, tuna dip, kawlata, garlic dip, "
                        "brodu tat-tiġieġ, vanilla mushroom stew", font=fs, fill=INK)
        im.alpha_composite(hb1, (16, y + 18))
        im.alpha_composite(hb2, (16, y + 18 + hb1.height + 10))
        blocks.append(im)
    # for reference: the dips as installed in the mod
    old = {d: item("dip_" + d) if d != "bigilla" else item("bigilla") for d in DIP_ORDER}
    hb = hotbar(hotbar_icons(old), 2)
    im = Image.new("RGBA", (16 + hb.width + 380, 26 + hb.height + 10), BG)
    ImageDraw.Draw(im).text((16, 4), "for reference: the same hotbar with the installed dips (2x)", font=f,
                            fill=INK)
    im.alpha_composite(hb, (16, 26))
    blocks.append(im)
    W = max(b.width for b in blocks)
    out = Image.new("RGBA", (W, sum(b.height + 6 for b in blocks)), (170, 170, 168, 255))
    y = 0
    for b in blocks:
        out.alpha_composite(b, (0, y))
        y += b.height + 6
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    all_made = {}
    for ck in CONCEPTS:
        made = {}
        for dip in DIP_ORDER:
            rows, im = make(ck, dip)
            name = f"{ck}_{dip}"
            check(name, rows)
            p = os.path.join(OUT, name + ".png")
            im.save(p)
            m = measure(p)
            print(f"{name:10s} coverage {m['coverage']:.2f} colours {m['colours']:2d} outline/inside "
                  f"{m['edge_l'] / m['interior_l']:.2f} tl_minus_br {m['tl_minus_br']:+.2f} vcentre {vcentre(im):.1f}")
            made[dip] = im
        hotbar(hotbar_icons(made), 2).save(os.path.join(OUT, f"hotbar_{ck}.png"))
        all_made[ck] = made
    sheet(all_made).save(SHEET)
    print("wrote", os.path.relpath(OUT, ROOT), "and", os.path.relpath(SHEET, ROOT))


if __name__ == "__main__":
    main()
