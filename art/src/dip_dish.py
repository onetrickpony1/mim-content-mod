"""The dips' own container: a low terracotta dish with a flared lip, the dip heaped in a mound above it.

Owner 2026-11-17: the dips needed a container of their own so they don't read as soups ("we need to rethink the
containers of the dips ... they share a bowl"); from the four concepts in art/src/dip_containers.py they chose concept
B "the low terracotta dish, but without the galletta". The dish is in the borma's clay (the same colours as the soup
bowl in art/src/bowls.py, so the food stays one family), but much lower, with a flared lip and no deep body; the dip is
a thick paste heaped into a mound with its own outline, never a flat liquid level as in the soups.

Used by bowls.py (bigilla), dip_gbejna.py, dip_tonn.py and dip_tewm.py: each gives its own fill (paste colours and a
hand-drawn rough heap with its toppings) to icon(); they install the textures.

Run on its own, it writes the review sheet art/candidates/dips_B_compare.png from the installed textures: the four dips
at 1x and 8x beside the soups in their bowl and the vanilla bowls, on inventory grey; the earlier round from
art/candidates/dips_B_v1/ when kept there; and the in-game hotbar crop when art/candidates/ingame_dips_B/ holds a
21-hotbar-dips screenshot (tools/run-art.sh; the crop is saved beside it), with the earlier rounds' *_crop_v1.png, *_crop_v2.png ...
Run:  art/.venv/bin/python art/src/dip_dish.py
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from food_items import hx, render  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))

# the borma clay, as bowls.py's PAL (o O H L l m d D)
CLAY = {"o": hx("#7e4028"), "O": hx("#62301c"), "H": hx("#d49a72"), "L": hx("#c27a52"), "l": hx("#b06a46"),
        "m": hx("#a0583a"), "d": hx("#874a33"), "D": hx("#6e3a26")}

# '?' = the dip. The dish sits in rows 8-12 and each dip draws its own rough heap above it (HEAP rows 3-9, see
# paste()), so the icon spans rows 3/4-12 (vertical centre 7.5-8 like vanilla foods); the lip is lit on the left,
# shaded on the right.
DISH = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "......????......",
    "....????????....",
    "...??????????...",
    "..o??????????O..",
    ".oH??????????lO.",
    ".OHLLLLLLlllldO.",
    "..OOlllmmmmdOO..",
    "....OODDDDOO....",
    "................",
    "................",
    "................",
]
RIM = 8   # the first row where the paste sits inside the dish's lip


def paste(rows, tops=None, peak=False, rim=False, heap=None):
    """Fill the '?' cells as a heaped paste: 'q' outline where it meets the air, 'a' lit top left, 'b' mid, 'c' shade
    lower right, then the toppings pattern (rows of chars, '.' keeps the paste) centred on the paste, inner cells only.
    peak: a stiff paste stands up in a two-pixel peak above the mound's top.
    rim: also outline the paste along the front lip, so a paste close to the clay's colours stays apart.
    heap: the dip's own hand-drawn heap instead of the shared dome and tops (owner 2026-11-17: "theyre heaped a bit
    too perfectly"), as {row: 16 chars} for rows 3 to RIM+1: '?' is paste (shaded and outlined as above), '.' is
    nothing, any other char is drawn as given (toppings, or a, b, c, q placed by hand). Above RIM the heap's cells
    replace the dish's '?'; from RIM down the dish stays full of paste and only the heap's own chars are laid on it."""
    g = [list(r) for r in rows]
    zone = {(x, y) for y in range(16) for x in range(16) if g[y][x] == "?"}
    given = {}
    if heap:
        for x, y in list(zone):
            if y < RIM:
                g[y][x] = "."
                zone.discard((x, y))
        for y, r in heap.items():
            assert len(r) == 16, (y, r)
            for x, c in enumerate(r):
                if c == "." or (y >= RIM and (x, y) not in zone):
                    continue
                zone.add((x, y))
                if c != "?":
                    given[(x, y)] = c
    if peak:
        top = min(y for _, y in zone)
        xs = sorted(x for x, y in zone if y == top)
        mid = xs[len(xs) // 2]
        zone |= {(mid - 1, top - 1), (mid, top - 1)}
    xs = [x for x, _ in zone]
    ys = [y for _, y in zone]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    rx, ry = max(1, (max(xs) - min(xs)) / 2), max(1, (max(ys) - min(ys)) / 2)
    outline = set()
    for x, y in zone:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            xx, yy = x + dx, y + dy
            if not (0 <= xx < 16 and 0 <= yy < 16) or ((xx, yy) not in zone and ((rim and dy == 1) or g[yy][xx] == ".")):
                outline.add((x, y))
    for x, y in zone:
        if (x, y) in outline:
            g[y][x] = "q"
        else:
            s = (x - cx) / rx + (y - cy) / ry
            g[y][x] = "a" if s < -0.55 else "c" if s > 0.8 else "b"
    for (x, y), c in given.items():
        g[y][x] = c
    tops = tops or []
    ox, oy = (round(cx - len(tops[0]) / 2 + 0.5), round(cy - len(tops) / 2 + 0.5)) if tops else (0, 0)
    for j, r in enumerate(tops):
        for i, c in enumerate(r):
            p = (ox + i, oy + j)
            if c != "." and p in zone and p not in outline:
                g[p[1]][p[0]] = c
    return ["".join(r) for r in g]


def icon(pal, heap, rim=True, fixes=None):
    """The dip in the dish: (rows, image). pal holds the paste (a b c q) and topping colours; they must not use the
    clay's letters o O H L l m d D. fixes: the critic's last pixel fixes {(x, y): char}, '.' for transparent, laid on
    the finished icon so nothing else moves."""
    assert not set(pal) & set(CLAY), set(pal) & set(CLAY)
    rows = paste(DISH, rim=rim, heap=heap)
    if fixes:
        g = [list(r) for r in rows]
        for (x, y), c in fixes.items():
            g[y][x] = c
        rows = ["".join(r) for r in g]
    return rows, render(rows, {**CLAY, **pal})


def main():
    from PIL import Image, ImageDraw
    sys.path.insert(0, os.path.join(ROOT, "art", "tools"))
    from font import label_font
    items = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
    vanilla = os.path.join(ROOT, "art", ".vanilla", "item")
    cands = os.path.join(ROOT, "art", "candidates")
    ingame = os.path.join(cands, "ingame_dips_B")
    names = (("Bigilla", "bigilla"), ("Dip tal-Ġbejna", "dip_gbejna"), ("Dip tat-Tonn", "dip_tonn"),
             ("Dip tat-Tewm", "dip_tewm"))
    pieces = [(lbl, Image.open(os.path.join(items, n + ".png")).convert("RGBA")) for lbl, n in names + (
        ("Aljotta", "aljotta"), ("Minestra", "minestra"), ("Brodu tat-tiġieġ", "brodu_tat_tigieg"),
        ("Kawlata", "kawlata"))]
    pieces += [("vanilla " + n.replace("_", " "), Image.open(os.path.join(vanilla, n + ".png")).convert("RGBA"))
               for n in ("bowl", "mushroom_stew", "beetroot_soup")]
    grey, bg, ink = (139, 139, 139, 255), (198, 198, 198, 255), (24, 24, 24, 255)
    f = label_font(13)
    cw = 128 + 12 + 18 + 12

    def strip(title, pieces, split=None):
        im = Image.new("RGBA", (16 + len(pieces) * cw, 22 + 128 + 26), bg)
        d = ImageDraw.Draw(im)
        d.text((16, 2), title, font=f, fill=ink)
        for i, (lbl, ic) in enumerate(pieces):
            x0 = 16 + i * cw
            if i == split:
                d.line([x0 - 7, 22, x0 - 7, 160], fill=(90, 90, 90, 255), width=2)
            d.rectangle([x0, 22, x0 + 127, 149], fill=grey)
            im.alpha_composite(ic.resize((128, 128), Image.NEAREST), (x0, 22))
            d.rectangle([x0 + 134, 76, x0 + 151, 93], fill=grey)
            im.alpha_composite(ic, (x0 + 135, 77))
            d.text((x0, 153), lbl, font=f, fill=ink)
        return im

    rows = [strip("now (installed): the dips heaped roughly in the low dish, beside the soups and vanilla bowls", pieces, 4)]
    before = os.path.join(cands, "dips_B_v1")
    if os.path.isdir(before):
        rows.append(strip("before (v1, the owner: \"theyre heaped a bit too perfectly\")",
                          [(lbl, Image.open(os.path.join(before, n + ".png")).convert("RGBA")) for lbl, n in names]))

    def shot_row(title, crop):
        crop = crop.resize((crop.width * 2, crop.height * 2), Image.NEAREST)
        im = Image.new("RGBA", (max(crop.width + 32, 1000), crop.height + 30), bg)
        ImageDraw.Draw(im).text((16, 4), title, font=f, fill=ink)
        im.alpha_composite(crop, (16, 26))
        return im

    order = ": bigilla, ġbejna dip, tuna dip, garlic dip, galletti, aljotta, beetroot soup, mushroom stew, bowl"
    shots = sorted(p for p in glob.glob(os.path.join(ingame, "*21-hotbar-dips*.png"))
                   if not p.endswith("_crop.png") and "_v" not in os.path.basename(p))
    if shots:
        s = Image.open(shots[-1]).convert("RGBA")
        w, h = s.size
        crop = s.crop((w // 2 - 182, h - 44, w // 2 + 182, h))
        crop.save(os.path.join(ingame, "21-hotbar-dips_crop.png"))
        rows.append(shot_row("in game now (GUI scale 2, crop shown x2)" + order, crop))
    for old in sorted(glob.glob(os.path.join(ingame, "21-hotbar-dips_crop_v*.png")), reverse=True):
        v = old[-6:-4]
        rows.append(shot_row(f"in game before ({v})" + order, Image.open(old).convert("RGBA")))
    W = max(r.width for r in rows)
    sheet = Image.new("RGBA", (W, sum(r.height for r in rows) + 8 * len(rows)), bg)
    y = 0
    for r in rows:
        sheet.alpha_composite(r, (0, y))
        y += r.height + 8
    out = os.path.join(cands, "dips_B_compare.png")
    sheet.save(out)
    print("wrote", os.path.relpath(out, ROOT))


if __name__ == "__main__":
    main()
