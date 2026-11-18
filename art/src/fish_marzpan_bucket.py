"""Bucket of marzpan: the fish layer of the item icon (16 x 16), 2026-11-19.

Same method as the accepted cerna, cawl and other buckets (art/src/fish_cerna_bucket.py): the item model puts the
player's own vanilla minecraft:item/cod_bucket underneath as layer0 and this texture on top as layer1, so the mod ships
no Mojang pixels (STYLE rule 3). This file is ONLY the fish: rows 6-15 are clear, and in rows 1-5 every opaque pixel of
the cod in cod_bucket is covered so no cod shows through (check_cover()); the back rim's dark outline stays wherever
the fish isn't in front of it (check_rim(), art/src/fish_bucket_rim.py).

Laid out the vanilla way: only the head rises out of the water at the upper left, the body slopes down to the right
into the water; no tail shows. The marzpan (Mediterranean parrotfish, the red female) is told apart at 1x by:
- the blunt red head, its front a short column with the mouth corner (M) at its foot;
- the grey-lilac cheek patch with the black eye at its front (no gold beside the eye: here at 1x it read as a beak);
- the yellow stripe under the cheek, starting two columns behind the eye so it never reads as a beak;
- the start of the dark dorsal fin behind the head.
Colours are the passed item icon's (art/src/fish_marzpan_icon.py PAL); the water is our own shades, as the other
buckets'. Photos (reference only): art/references/fish_marzpan_refonly/ (list.tsv).

Candidates: A (installed; reworked after critic round 1, the first version kept as A1 on the sheet), B (no cheek
stripe), C (the head a row higher, more of the back and dorsal fin showing).
Writes: mod/src/main/resources/assets/mimcontent/textures/item/marzpan_bucket.png
With --sheet also art/candidates/fish_marzpan_bucket.png (candidates over vanilla's cod_bucket at 8x, 1x and 2x beside
vanilla's fish buckets and the cerna bucket, with measure.py numbers) and the candidates as
art/candidates/marzpan_bucket_<X>.png.
Run:    art/.venv/bin/python art/src/fish_marzpan_bucket.py [--sheet]
"""
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fish_bucket_rim import check_rim  # noqa: E402
from fish_cerna_bucket import check_cover  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
OUT = os.path.join(ITEMS, "marzpan_bucket.png")
VANILLA = os.path.join(ROOT, "art", ".vanilla", "item")


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = {
    # water where the fish goes under: our own shades (as the other buckets)
    "~": hx("#2a55c4"), "v": hx("#1d3c96"), "^": hx("#6a92ea"),
    "#": hx("#383838"),  # the back-rim outline where we cover a cod pixel (our grey, vanilla's is #353535)
    # the marzpan: the passed item icon's palette (art/src/fish_marzpan_icon.py), same keys
    "1": hx("#ff9470"), "2": hx("#ff7048"), "3": hx("#f45a38"), "4": hx("#dc4630"), "5": hx("#bc3828"),
    "k": hx("#a83224"),                       # the outline on the lit forehead
    "M": hx("#5e1a14"),                       # the mouth corner (dark red-brown, not black)
    "m": hx("#7a2218"),                       # the mouth corner beside the bucket's rim, a little lighter so it stays apart
    "G": hx("#bca4b6"), "g": hx("#9c8498"),   # the grey-lilac cheek patch and its gill edge
    "E": hx("#0a0a0a"),                       # the eye (the only black)
    "O": hx("#ff9a2c"),                       # the gold ring behind the eye
    "Y": hx("#fff05a"), "y": hx("#f2d23c"), "w": hx("#d8a82c"),   # the yellow cheek stripe, shading under
    "D": hx("#a02c20"),                       # the dorsal fin
}

# rows 0-5, columns 0-15 ("." clear); rows 6-15 are always clear
A = [
    "................",
    "....k24D........",
    "...k4GGgD3......",
    "...4EGGg334#....",
    "...mGgywwv~~~...",
    "....45v~~^~~....",
]
# the first version (critic round 1: the gold ring and the stripe made an L-shaped yellow blob behind the eye); sheet only
A1 = [
    "................",
    "....k44D........",
    "...k2GGgD3......",
    "...4EOGg334#....",
    "...MGyYw4v~~~...",
    "....45v~~^~~....",
]
B = [r for r in A1]
B[4] = "...MGGgg4v~~~..."
C = [
    "................",
    "....k4DD........",
    "...k2GgDD3......",
    "...4EOGg3345#...",
    "...MGyYw45v~~...",
    "....4v~~~^~~....",
]
CANDIDATES = {"A": A, "A1": A1, "B": B, "C": C}
CHOSEN = "A"
# the back-rim outline pixels (art/src/fish_bucket_rim.py) that the head and its dorsal fin cover, per candidate
FISH_OVER_RIM = {
    "A": [(5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (3, 3)],
    "A1": [(5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (3, 3)],
    "B": [(5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (3, 3)],
    "C": [(5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (3, 3), (11, 3)],
}


def build(rows):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != ".":
                img.putpixel((x, y), PAL[ch] + (255,))
    return img


def composite(layer):
    """What players see: our layer over vanilla's cod bucket (review only; vanilla is never written out)."""
    base = Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")
    base.alpha_composite(layer)
    return base


def sheet(layers):
    from PIL import ImageDraw
    sys.path.insert(0, os.path.join(ROOT, "art", "tools"))
    from font import label_font
    from measure import measure
    small = label_font(13)
    W = 1500
    shown = [("cod", Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")),
             ("salmon", Image.open(os.path.join(VANILLA, "salmon_bucket.png")).convert("RGBA")),
             ("tropical fish", Image.open(os.path.join(VANILLA, "tropical_fish_bucket.png")).convert("RGBA")),
             ("cerna bucket", composite(Image.open(os.path.join(ITEMS, "cerna_bucket.png")).convert("RGBA")))]
    for k, layer in layers.items():
        p = os.path.join(ROOT, "art", "candidates", f"marzpan_bucket_{k}.png")
        composite(layer).save(p)
        shown.append((f"candidate {k}" + (" (installed)" if k == CHOSEN else ""), composite(layer)))
    out = Image.new("RGBA", (W, 330), (139, 139, 139, 255))
    d = ImageDraw.Draw(out)
    for i, (n, im) in enumerate(shown):
        out.alpha_composite(im.resize((128, 128), Image.NEAREST), (10 + i * 150, 24))
        d.text((10 + i * 150, 4), n, fill=(0, 0, 0), font=small)
        out.alpha_composite(im, (10 + i * 150, 170))
        out.alpha_composite(im.resize((32, 32), Image.NEAREST), (40 + i * 150, 162))
    tmp = os.path.join(ROOT, "art", "candidates", "marzpan_bucket_measure.tmp.png")
    y = 210
    for n, im in shown:
        im.save(tmp)
        m = measure(tmp)
        d.text((10, y), f"{n:16s} coverage {m['coverage']:.2f}  colours {m['colours']:2d}  darkest {float(m['lmin']):.2f}  "
               f"lightest {float(m['lmax']):.2f}  TL-BR {float(m['tl_minus_br']):+.2f}", fill=(0, 0, 0), font=small)
        y += 16
    os.remove(tmp)
    dest = os.path.join(ROOT, "art", "candidates", "fish_marzpan_bucket.png")
    out.convert("RGB").save(dest)
    print("sheet:", dest)


if __name__ == "__main__":
    layers = {}
    for k, rows in CANDIDATES.items():
        layer = build(rows)
        check_cover(layer)
        check_rim(layer, os.path.join(VANILLA, "cod_bucket.png"), FISH_OVER_RIM[k])
        layers[k] = layer
    layers[CHOSEN].save(OUT, optimize=False)
    print("wrote", os.path.relpath(OUT, ROOT))
    if "--sheet" in sys.argv[1:]:
        sheet(layers)
