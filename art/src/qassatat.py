"""The qassata item icon (plural qassatat): the round, pleated cousin of the pastizz.

A qassata is a round pastry case (shortcrust-like, not the pastizz's flaky layers) gathered up round the filling in
pleats, the top left open so the baked ricotta (or the curried peas) shows in the middle. Shape and bake from the
owner's photos (art/references/qassatat_owner/, reference only, never traced) and art/references/qassata_1.jpg:
- a squat round bun seen a little from above, wider than tall;
- 6 to 9 soft pleats running from the open top down the sides, sometimes with a slight swirl;
- the opening shows ricotta, white with a few oven-browned (and darker scorched) spots;
- golden all over, the pleat ridges lighter, the folds between them darker.
The colours are the accepted pastizz's (food_items.P3: outline #713c15 and its golden ramp, ricotta #f7f3e8), so
the qassata sits with the pastizzi as one family, lit from the top left like vanilla.

Owner 2026-11-17: "qassata b is the clear winner, but it needs a peas version too (pizelli vs irkotta)". So there are
two items, qassata tal-irkotta (b) and qassata tal-piżelli: b's map exactly, only the filling in the opening changed to
the curried mushy peas in the accepted pastizz tal-piżelli's colours (food_items.P3 "Y" #c8c24a lit, "y" #a39f35 in
shade, "s" #6d6a2a deep), as the owner's pea qassatat photos show the yellow-green filling in the opening.

Ricotta candidates (round 1):
- a: squat bun, a wide oval opening with 7 pleats, the opening's rim a pale lip;
- b: taller "money bag", the pastry gathered higher round a smaller opening, the pleats longer and more upright;
- c: as a, with a slight swirl to the pleats (qassata_1.jpg and the owner's hand photo) and a scalloped crown.
Pea candidates (both on b):
- pizelli a: a smooth pea filling, lit, with the far rim's shadow along its top and one deep pea;
- pizelli b: a lumpier filling, lit and shaded peas mixed so single peas read.

Writes art/candidates/qassatat_{a,b,c}.png, art/candidates/qassata_pizelli_{a,b}.png and
art/candidates/qassatat_compare.png (1x and 8x beside vanilla bread, cookie and the accepted pastizzi, on inventory
grey, plus the in-game hotbar crop when art/candidates/ingame_qassatat/ holds the 20-hotbar-bakes shot), and installs
PICK as the mod texture item/qassata_irkotta.png and PEA_PICK as item/qassata_pizelli.png.
Run:  art/.venv/bin/python art/src/qassatat.py
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
from food_items import P3, hx, render  # noqa: E402  (read only)

ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
VANILLA = os.path.join(ROOT, "art", ".vanilla", "item")
OUT = os.path.join(ROOT, "art", "candidates")
INGAME = os.path.join(OUT, "ingame_qassatat")

PICK = "b"  # the owner's pick, 2026-11-17
PEA_PICK = "b"

# the pastizz's ramp (with its peas), plus the ricotta's oven browning
PAL = dict(P3)
PAL.update({"b": hx("#e3c48a"),  # ricotta browned in the oven
            "B": hx("#a8692c"),  # a scorched spot
            "o": hx("#a25c22")})  # outline on the lit (top-left) side (the first pastizz's), lighter than "#"

# At 16 px the pleats only read when placed by hand, so each candidate is an explicit map (drawn after a procedural
# layout of the opening and the radial folds, then cleaned up). Characters: "o" outline on the lit top-left, "#"
# outline in shade, "D" a fold between two pleats, "d" "m" "l" "h" the pastry from shade to highlight, "r" ricotta,
# "R" ricotta in the far rim's shadow, "b" browned, "B" scorched.
MAPS = {
    # a: squat bun (rows 3-13), a wide oval opening, a crown of three pleat tips at the back, the near lip lit,
    # four folds fanning down the front
    "a": [
        "................",
        "................",
        "................",
        "....oo.ooo.##...",
        "...ohlohhlomd#..",
        "..ohldRRRRRdmd#.",
        ".ohlrrrrbbrRmd#.",
        ".olhrrrrrBrrmd#.",
        ".olhlrrrrrrlmd#.",
        ".#lDhhlllmmmDd#.",
        ".#llDlmDlmDmDd#.",
        ".#lmDlmDlmDdDd#.",
        "..#mDlmDmmDdd#..",
        "...##########...",
        "................",
        "................",
    ],
    # b: the taller "money bag" (rows 2-14): the pastry gathered higher round a smaller opening, longer upright folds
    "b": [
        "................",
        "................",
        ".....oo.oo.##...",
        "....ohlohlomd#..",
        "...ohdRRRRdmd#..",
        "...olrrrbbRmd#..",
        "..ohlhrrrBlmmd#.",
        "..olDhhhhllDmd#.",
        ".olDlmDlmmDmDd#.",
        ".olDlmmDlmDmDd#.",
        ".#lDlmmDlmDmDd#.",
        ".#lDlmmDlmmDdd#.",
        ".#mDlmmDlmmDdd#.",
        "..#mDlmDlmDdd#..",
        "...##########...",
        "................",
    ],
    # c: as a, the folds swirling a little to the right as they run down (qassata_1.jpg, the owner's hand photo),
    # the ricotta more browned
    "c": [
        "................",
        "................",
        "................",
        "....oo.ooo.##...",
        "...ohlohhlomd#..",
        "..ohldRRRRRdmd#.",
        ".ohlrbbrrrrRmd#.",
        ".olhrrbrrBbrmd#.",
        ".olhlrrrrbrlmd#.",
        ".#lDhhlllmmmDd#.",
        ".#llDlmDlmDmDd#.",
        ".#llmDlmDlmDdd#.",
        "..#lmmDlmDmdD#..",
        "...##########...",
        "................",
        "................",
    ],
}


# the pea fillings: b's map with only the opening's rows (4-6) replaced; the pastry pixels are b's, unchanged
PEAS = {
    "a": {4: "...ohdyyyydmd#..",
          5: "...olYYYYYymd#..",
          6: "..ohlhYYYslmmd#."},
    "b": {4: "...ohdyyyydmd#..",
          5: "...olYyYYsymd#..",
          6: "..ohlhYsYylmmd#."},
}


def pea_map(letter):
    rows = list(MAPS["b"])
    for y, row in PEAS[letter].items():
        assert len(row) == 16 and all((a == c) or (a in "rRbB" and c in "Yys")
                                      for a, c in zip(rows[y], row)), (letter, y)  # only the filling changes
        rows[y] = row
    return rows


def draw(letter, lit_rows=8):
    """The map, with the lit outline "o" carried down the whole upper half and the left side (vanilla's outline is
    about 0.6 of the inside; the bright ricotta lifts the inside, so the outline is lifted too). The dark "#" stays
    along the base and the lower right."""
    rows = [list(r) for r in (MAPS[letter] if letter in MAPS else pea_map(letter[-1]))]
    top = min(y for y, r in enumerate(rows) if set(r) != {"."})
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch == "#" and (y - top <= lit_rows - 3 or (x <= 2 and rows[y + 1][x] != "#")):
                r[x] = "o"
    return ["".join(r) for r in rows]


def vcentre(im):
    ys = [y for y in range(16) for x in range(16) if im.getpixel((x, y))[3]]
    return (min(ys) + max(ys)) / 2


def up(im, k):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def compare(cands):
    font = label_font(14)
    ours = [(n, Image.open(os.path.join(ITEMS, n + ".png")).convert("RGBA"))
            for n in ("pastizz_irkotta", "pastizz_pizelli")]
    van = [(n, Image.open(os.path.join(VANILLA, n + ".png")).convert("RGBA")) for n in ("bread", "cookie")]
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
    # a 1x strip as in the hotbar, and the same at 2x (the hotbar at GUI scale 2)
    for k in (1, 2):
        strip = Image.new("RGBA", (pad + len(pieces) * (16 * k + 4 * k), 16 * k + 2 * pad), bg)
        for i, (n, im) in enumerate(pieces):
            strip.alpha_composite(up(im, k), (pad + i * (16 * k + 4 * k), pad))
        rows.append(strip)
    shots = sorted(glob.glob(os.path.join(INGAME, "*20-hotbar-bakes*.png")))
    if shots:
        s = Image.open(shots[-1]).convert("RGBA")
        w, h = s.size
        crop = s.crop((w // 2 - 182, h - 44, w // 2 + 182, h))
        crop = up(crop, 2)
        img = Image.new("RGBA", (crop.width + 2 * pad, crop.height + lab + 2 * pad), (232, 232, 228, 255))
        ImageDraw.Draw(img).text((pad, 2), "in game: bread, pastizz tal-irkotta, pastizz tal-piżelli, qassata tal-irkotta, "
                                 "qassata tal-piżelli, qagħaq tal-ħmira, qagħqa tal-appostli, qagħaq tal-għasel, ħobż",
                                 font=font, fill=(20, 20, 20, 255))
        img.alpha_composite(crop, (pad, lab + pad // 2))
        rows.append(img)
    W = max(r.width for r in rows)
    sheet = Image.new("RGBA", (W, sum(r.height + 4 for r in rows)), (200, 200, 196, 255))
    y = 0
    for r in rows:
        sheet.alpha_composite(r, (0, y))
        y += r.height + 4
    p = os.path.join(OUT, "qassatat_compare.png")
    sheet.save(p)
    print("wrote", os.path.relpath(p, ROOT))


def main():
    os.makedirs(OUT, exist_ok=True)
    cands = []
    for letter in list(MAPS) + ["pizelli_" + k for k in PEAS]:
        im = render(draw(letter), PAL)
        name = f"qassatat_{letter}" if letter in MAPS else f"qassata_{letter}"
        p = os.path.join(OUT, name + ".png")
        im.save(p)
        m = measure(p)
        print(name, {k: m[k] for k in ("coverage", "colours", "edge_l", "interior_l", "tl_minus_br")},
              "outline/inside", round(m["edge_l"] / m["interior_l"], 2), "vcentre", vcentre(im))
        cands.append((name, im))
        if letter == PICK:
            im.save(os.path.join(ITEMS, "qassata_irkotta.png"))
        if letter == "pizelli_" + PEA_PICK:
            im.save(os.path.join(ITEMS, "qassata_pizelli.png"))
    compare(cands)


if __name__ == "__main__":
    main()
