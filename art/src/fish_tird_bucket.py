"""Bucket of tird (ornate wrasse, Thalassoma pavo, the male): the fish layer of the item icon (16 x 16), night job 2026-11-19.

Night job piece 3 of 3 (docs/Decisions/2026-11-18 Night job - the rest of the fish, Claude decides.md).

The bucket is not ours: the item model puts the player's own vanilla minecraft:item/cod_bucket underneath as layer0
and this texture on top as layer1, so the mod ships no Mojang pixels (STYLE rule 3) and the bucket matches whatever
resource pack the player uses. This file is therefore ONLY the fish, the bucket's back outline and our water: rows
6-15 are clear, and in rows 0-5 every opaque pixel of the cod in cod_bucket is covered so no cod shows through
(check_cover()), and the back-rim outline stays dark except where the tird's head sits in front of it (check_rim() in
art/src/fish_bucket_rim.py).

Owner rules this follows:
- buckets show the head rising out of the water, the vanilla way, never the tail;
- the bucket's back outline stays visible: the head covers row 2 x5-10 and the left corner 3,3-4,3; the right corner
  (11,3 ours, 12,3 cod_bucket's own) and both sides stay dark;
- the eye looks like nothing else: one black pixel with head colour on every side.

What shows of the tird: the slim pointed head rising up and to the left out of the water, turquoise-blue and lit on
its crown, the black eye, the pink-violet line on the cheek, then the collar running across the fish (the pale
turquoise bar and the red-orange band) and the green back going under the water on the right.
Bucket critic rounds: 8 (rounds 1-7 failed, PASS in round 8, the last allowed).
Colours start from the critic-passed tird item icon's (art/src/fish_tird_icon.py, palette A). Candidate A uses its
own greener head (j, J, N), redder band (r) and near-white bar (W), because with the icon's colours the bucket read
too close to vanilla's tropical fish bucket and the bar vanished (critic rounds 3 and 6), and our own greys for the
bucket's inner back wall (Z, Y). The water is the shared shades of the other buckets.

Candidates (art/candidates/tird_bucket/): A (this design), B (the head more upright, the snout straight up), C (the
head lower, only the crown and eye above the rim). CHOSEN is written to the mod.

Writes: mod/src/main/resources/assets/mimcontent/textures/item/tird_bucket.png (byte-identical on rerun), the
candidates, the review sheet art/candidates/fish_tird_bucket.png and the hotbar previews.
Run:    art/.venv/bin/python art/src/fish_tird_bucket.py
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fish_bucket_rim import RIM, check_rim  # noqa: E402
import fish_tird_icon as icon  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
ART = os.path.join(ROOT, "art")
ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
OUT = os.path.join(ITEMS, "tird_bucket.png")
CAND = os.path.join(ART, "candidates", "tird_bucket")
VANILLA = os.path.join(ART, ".vanilla", "item")
SHEET = os.path.join(ART, "candidates", "fish_tird_bucket.png")
CHOSEN = "A"
PY = os.path.join(ART, ".venv", "bin", "python")


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = {
    "~": hx("#2a55c4"),  # water: the shared shades of the accepted buckets
    "v": hx("#1d3c96"),  # shadow on the water beside the fish where it goes under
    "^": hx("#6a92ea"),  # a glint of light on the water
    "#": RIM,            # the bucket's back-rim outline where we cover a cod pixel
    "Z": hx("#7c7c7c"),  # the bucket's inner back wall, below the rim (vanilla's water bucket shows one there)
    "Y": hx("#9c9c9c"),  # its lit end
    # (bucket critic round 3: too close to vanilla's tropical fish bucket) a greener turquoise head and a redder band
    # than the icon's, for the bucket only
    "j": hx("#6ad8c4"),  # the head, lit
    "J": hx("#3fb4a6"),  # the head
    "r": hx("#e4461e"),  # the band
    "N": hx("#2e8c82"),  # the head's shaded lower edge
    "W": hx("#e2fff4"),  # the bar, near-white so it shows against the head (round 6)
}
PAL.update({k: v for k, v in icon.PALS["A"].items() if k in "SHhEnLcBbRqmlgwo"})

# rows 0-5, columns 0-15; "." is clear (vanilla cod_bucket's own outline or water shows there)
GRIDS = {
    # Row 0: the lit tip of the head h. Row 1: the snout S, the head, the eye E ringed by head colour, the crown h,
    # then the collar starting at the nape (the bar B, the band R). Rows 2-4: the chin and throat n (and the cheek c),
    # the bar and the band running down to the left, parallel, then two green pixels g going under beside the water's
    # shadow v; our rim grey at 9,2 and the right corner 11,3. Row 5: water.
    # (bucket critic round 1, FAIL: specks at the lower left, the bar two scattered pixels, a flat cap, a lone orange
    # pixel under the eye) the head comes to a point and the bar and band run as clean parallel diagonals.
    # (bucket critic round 2, FAIL: the whole fish seemed to lie across the opening, and the rim was lost) only the
    # head and collar rise, at the left; two green pixels show at the waterline; the rim runs on dark from x9 to the
    # right and the water fills the rest of the mouth. The head is the icon's lit turquoise (h) all over, with the dark
    # teal (n) only under the chin, so it stands clear of the water's blue.
    # (bucket critic round 3, FAIL: no back rim on the right, water up to the top edge, the head a blunt blob, the
    # bands smeared diagonally, a second dark pixel on the chin, colours too close to vanilla's tropical fish) the head
    # rises upright with a pointed snout leaning left (one pixel on row 0), and the colours run in clean rows down the
    # fish: the greener turquoise head with the eye (rows 0-2), the pale cyan bar (row 3), the redder band (row 4),
    # the green body going under (row 5). Behind the head the bucket's back rim runs dark (8,2 9,2) over its inner
    # wall, our own greys Z and Y (row 3, as in vanilla's water bucket a row higher), so the water sits inside the rim.
    # (bucket critic round 4, FAIL: the flat rows read as a striped lid or a little robot head) the head leans up and
    # to the left again, one clean taper to a 1 px snout with a darker turquoise N along its lower edge; the bar,
    # band and two green pixels step down the neck at the fish's own width, three pixels each, into the water; the
    # rim and its inner wall stay dark and grey to the right.
    # (bucket critic round 5, FAIL: a small diagonal smear, a 1 px spike on top, 1 px bands like confetti, dark water
    # pixels beside the band) a bigger head on the item icon's proportions, its snout tip pointing out to the left
    # (2,1), three pixels of solid turquoise round the eye, the pale bar one pixel, the band two pixels wide and the
    # green two, stepping down into mid-blue water; the rim's inner wall grey (Z) beside the green.
    # (bucket critic round 6, FAIL: upright on a "neck" it read as a duck or parrot head; the band and green hid the
    # rim; the bar too close to the head's turquoise; the eye on the head's edge) the head leans at 45 degrees from
    # the water at the left, a 1 px snout at the top left, the eye inside the head with a pale highlight (c) before it;
    # the bar near-white (W); only the bar, band and one green pixel per row step down the neck into the water; the
    # dark rim (8,2 9,2 and vanilla's own) and its grey inner wall run unbroken from the neck to the right corner.
    # (bucket critic round 7, FAIL: the thin leaning wedge read as a beak, a feather or a needlefish) back to round 6's
    # bigger head, which the blind readers took for a wrasse, with round 6's faults fixed: no narrowing "neck" (the
    # head widens from its tip down to the waterline, so it can't read as a bird's head), the eye inside the turquoise
    # with turquoise all round it, the bar near-white, the band two pixels wide, the green only at the waterline, and
    # the rim dark at 9,2 (and vanilla's 10,2) over the grey inner wall at the right.
    "A": [
        "...jjJ..........",
        "...jEJWr........",
        "..NJJJWrr#......",
        "..NJJWrrgZZ#....",
        "...NWrrgg~^~~...",
        "....~~~^~~~~....",
    ],
    "B": [
        "....Sh..........",
        "....HEhB........",
        "...ncHBRRm......",
        "...nLBRRlgm#....",
        "...nbqgwv~^~~...",
        "...ov~~~^~~~~...",
    ],
    "C": [
        "................",
        "....hhhB........",
        "...SHEHBRm......",
        "...cHcBRRlm#....",
        "...nbqgwv~^~~...",
        "...ov~~~^~~~~...",
    ],
}
FISH_OVER_RIM = {
    "A": [(5, 2), (6, 2), (7, 2), (8, 2), (3, 3), (4, 3)],
    "B": [(5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (3, 3), (4, 3)],
    "C": [(6, 2), (7, 2), (8, 2), (9, 2), (3, 3), (4, 3)],     # (5, 2) is the eye, dark like the rim
}


def build(grid):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(grid):
        assert len(row) == 16, (y, len(row))
        for x, ch in enumerate(row):
            if ch != ".":
                px[x, y] = PAL[ch] + (255,)
    return img


def composite(layer):
    """What players see: our layer over vanilla's cod bucket (review only; vanilla is never written out)."""
    base = Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")
    base.alpha_composite(layer)
    return base


def check_cover(layer):
    """No cod may show through; rows 6-15 must be clear; no pixel may equal vanilla's at the same place."""
    cod = os.path.join(VANILLA, "cod_bucket.png")
    for y in range(6, 16):
        assert all(layer.getpixel((x, y))[3] == 0 for x in range(16)), f"row {y} not clear"
    if not os.path.exists(cod):
        print("note: art/.vanilla missing, cover not checked")
        return
    base = Image.open(cod).convert("RGBA")
    fishy = [(x, y) for y in range(6) for x in range(16)
             if base.getpixel((x, y))[3] and base.getpixel((x, y))[:3] not in ((0x35, 0x35, 0x35), (0x23, 0x4f, 0xcc))]
    shows = [p for p in fishy if layer.getpixel(p)[3] == 0]
    assert not shows, f"cod shows through at {shows}"
    same = []
    for n in ("cod_bucket", "salmon_bucket", "tropical_fish_bucket", "water_bucket", "bucket"):
        v = Image.open(os.path.join(VANILLA, n + ".png")).convert("RGBA")
        same += [(n, x, y) for y in range(16) for x in range(16)
                 if layer.getpixel((x, y))[3] and layer.getpixel((x, y)) == v.getpixel((x, y))]
    assert not same, f"pixels identical to vanilla: {same}"
    print(f"cover ok: all {len(fishy)} cod pixels covered, 0 pixels identical to vanilla")


def check_eye(grid):
    """One eye, with no dark or pink pixel beside it."""
    eyes = [(x, y) for y, r in enumerate(grid) for x, c in enumerate(r) if c == "E"]
    assert len(eyes) == 1, eyes
    ex, ey = eyes[0]
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if (dx, dy) != (0, 0) and 0 <= ey + dy < len(grid):
                assert grid[ey + dy][ex + dx] not in "#Lonvq", ("beside the eye", ex + dx, ey + dy)


def hotbar(out, items, scale):
    subprocess.run([PY, os.path.join(ART, "tools", "hotbar_preview.py"), out] + items + ["--scale", str(scale)],
                   check=True, capture_output=True)
    return Image.open(out).convert("RGB")


def sheet(layers):
    sys.path.insert(0, os.path.join(ART, "tools"))
    from font import label_font
    font, small = label_font(16), label_font(13)
    W = 1500
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []
    band = Image.new("RGB", (W, 200), bg)
    d = ImageDraw.Draw(band)
    x = 10
    for v, layer in layers.items():
        im = composite(layer)
        for s in (8, 2, 1):
            t = Image.new("RGBA", (16 * s + 8, 16 * s + 8), (139, 139, 139, 255))
            t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
            band.paste(t.convert("RGB"), (x, 24))
            d.text((x, 4), f"{v} {s}x" + (" (chosen)" if v == CHOSEN and s == 8 else ""), fill=ink, font=small)
            x += max(16 * s + 20, 60)
        x += 30
    parts.append(("Candidates A, B, C over vanilla cod_bucket at 8x, 2x, 1x", band))
    others = [("cod bucket", Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA"))]
    others += [(n, composite(Image.open(os.path.join(ITEMS, n + "_bucket.png")).convert("RGBA")))
               for n in ("cawl", "cerna", "sardina", "kavall") if os.path.exists(os.path.join(ITEMS, n + "_bucket.png"))]
    others += [("tird item", Image.open(os.path.join(ITEMS, "tird.png")).convert("RGBA")),
               ("layer alone", layers[CHOSEN])]
    band = Image.new("RGB", (W, 170), bg)
    d = ImageDraw.Draw(band)
    for i, (n, im) in enumerate([("TIRD", composite(layers[CHOSEN]))] + others):
        t = Image.new("RGBA", (136, 136), (139, 139, 139, 255))
        t.alpha_composite(im.resize((128, 128), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (10 + i * 150, 24))
        d.text((10 + i * 150, 4), n, fill=ink, font=small)
    parts.append(("The chosen bucket at 8x beside vanilla's cod bucket, other mod buckets, the tird item, the layer alone",
                  band))
    hb = [hotbar(os.path.join(CAND, "hotbar.png"), ["mc:water_bucket", "mc:cod_bucket", "bucket:tird_bucket",
                                                      "mod:tird", "mc:tropical_fish_bucket", "bucket:cawl_bucket",
                                                      "bucket:cerna_bucket", "mc:salmon_bucket", "bucket:sardina_bucket"], 2),
          hotbar(os.path.join(CAND, "hotbar_x4.png"), ["mc:cod_bucket", "bucket:tird_bucket", "mod:tird",
                                                         "mc:tropical_fish_bucket"], 4)]
    band = Image.new("RGB", (W, sum(i.height + 10 for i in hb) + 10), bg)
    y = 4
    for im in hb:
        band.paste(im, (10, y))
        y += im.height + 10
    parts.append(("Hotbar preview, unselected: water, cod, TIRD bucket, tird item, tropical fish, cawl, cerna, salmon, "
                  "sardina buckets at scale 2; cod bucket, TIRD bucket, tird item, tropical fish bucket at 4", band))
    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Bucket of tird (ornate wrasse), textures/item/tird_bucket.png", fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    out.save(SHEET)
    print("sheet:", SHEET)


def main():
    os.makedirs(CAND, exist_ok=True)
    layers = {}
    for v, rows in GRIDS.items():
        grid = rows + ["................"] * 10
        check_eye(rows)
        layer = build(grid)
        check_cover(layer)
        check_rim(layer, os.path.join(VANILLA, "cod_bucket.png"), FISH_OVER_RIM[v])
        layer.save(os.path.join(CAND, f"layer_{v}.png"))
        composite(layer).save(os.path.join(CAND, f"bucket_{v}.png"))
        layers[v] = layer
    layers[CHOSEN].save(OUT, optimize=False)
    print("wrote", os.path.relpath(OUT, ROOT))
    sheet(layers)


if __name__ == "__main__":
    main()
