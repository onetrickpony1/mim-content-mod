"""Bucket of awrata: the fish layer of the item icon (16 x 16), 2026-11-18.

The bucket is not ours: the item model puts the player's own vanilla minecraft:item/cod_bucket underneath as layer0
and this texture on top as layer1, so the mod ships no Mojang pixels (STYLE rule 3) and the bucket matches whatever
resource pack the player uses. This file is therefore ONLY the fish: rows 6-15 are clear, and in rows 1-5 every opaque
pixel of the cod in cod_bucket is covered so no cod shows through (checked by check_cover() on every run, against
art/.vanilla's cod_bucket when it is there). Same method as the owner-accepted cerna bucket
(art/src/fish_cerna_bucket.py), whose layout this follows.

Owner 2026-11-18 (the cerna bucket): "it should be the head mostly visible as vanilla fish". So, as vanilla's cod,
salmon and tropical fish buckets do, only the head and the front of the body rise out of the water inside the rim:
head at the upper left (eye in row 2), the body sloping down to the right into the water. No tail shows. The back of
the rim stays visible at the right (11,2 / 12,3 / 13,4) and the water at the front edge. No black outline of its own.

The awrata (gilthead sea bream, Sparus aurata) is told apart at 1x by its head:
- the GOLDEN band over the forehead, just above the eye (the fish is named after it);
- the gill mark: a short dark stroke on the gill cover behind the eye, never level with it, ending in a red foot;
- the silver body running a light ramp from the sheen behind the eye (top left) to the shaded throat (bottom right),
  under a blue-grey back;
- the steep, rounded forehead and the small mouth with thick lips at the front.
Colours are the owner-accepted awrata item icon's (textures/item/awrata.png, art/src/fish_awrata_icon.py PAL),
nothing new; the water where the fish goes under is our own shades, the same as the cerna bucket's.
Photos (reference only): art/references/fish_awrata_refonly/ (list.tsv).

Writes: mod/src/main/resources/assets/mimcontent/textures/item/awrata_bucket.png (byte-identical on rerun)
With --sheet it also writes the review sheet art/candidates/fish_awrata_bucket.png and the hotbar previews
art/candidates/fish_awrata_bucket_hotbar.png (scale 2) and _hotbar_x4.png (scale 4).
Run:    art/.venv/bin/python art/src/fish_awrata_bucket.py [--sheet]
"""
import os
import subprocess

from PIL import Image

from fish_bucket_rim import check_rim

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
ART = os.path.join(ROOT, "art")
ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
OUT = os.path.join(ITEMS, "awrata_bucket.png")


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = {
    # water where the fish goes under: our own shades (as the cerna bucket's)
    "~": hx("#2a55c4"),
    "#": hx("#383838"),  # the bucket's back-rim outline where we cover a cod pixel: our own grey (vanilla's is #353535)
    "v": hx("#1d3c96"),  # the shadow on the water beside the fish
    "^": hx("#6a92ea"),  # a glint of light on the water
    # the awrata: the owner-accepted item icon's palette (art/src/fish_awrata_icon.py PAL), same keys
    "K": hx("#4f6477"), "b": hx("#7d91a3"),   # blue-grey back: lit rim, and the band just inside it
    "W": hx("#e6ecee"), "1": hx("#cdd6db"), "2": hx("#b4bec6"), "3": hx("#9ba7b1"), "4": hx("#83909b"),
    "5": hx("#6b7783"),                       # silver, sheen to shaded belly
    "o": hx("#343d47"),                       # rim on the shaded belly side
    "O": hx("#56626e"),                       # softer rim: chin, mouth corner
    "e": hx("#0a0a0a"),                       # the eye (the only black)
    "G": hx("#e8bf4c"), "g": hx("#c39a42"),   # golden forehead band: lit, shaded
    "p": hx("#68747f"), "P": hx("#46535e"),   # dark patch on the gill cover: soft edge, core
    "R": hx("#b8664a"),                       # red-orange foot of the gill mark
    "L": hx("#a2aab1"),                       # thick lips
}

# rows 0-15, columns 0-15; "." is clear
# The head comes up out of the water at the left of the bucket mouth; the rest of the fish is under the water, so no
# tail shows. The forehead is steep and rounded (front at x 4, 3, 3, 3, 4 down the rows), and the golden band runs
# over it: lit (G, 5-6,1) right above the eye, shaded (g) where it turns down the front of the head (4,1 and 3,2), so
# it reads as a band across the forehead. The one eye (5,2) has only gold, lit silver or the sheen (W) around it.
# The gill mark is a curved stroke on the gill cover, like the icon's: soft top (p, 8,2) under the blue-grey back,
# core (P, 7,3) one row below the eye and two pixels behind it, ending in the red-orange foot (R, 7,4); it is never
# level with the eye as a dark spot. The silver runs from the lit cheek (W, 4,3) to the shaded throat (4, 5) and the
# dark belly rim (o) where the fish meets the water; the thick lips (L, 3,4) and the chin (O) close the small mouth.
# Where the fish no longer covers the cod (rows 3-5 at the right), our own water covers it: a shadow (v) beside the
# fish where it goes under and a glint of light (^), leaving the back of vanilla's rim (11,2 / 12,3 / 13,4) showing.
GRID = [
    "................",
    "....gGGbK.......",
    "...g1eW1pbK.....",
    "...1W12P234#....",
    "...L234R345v~...",
    "....O45oov~^....",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]


# The back-rim outline pixels (art/src/fish_bucket_rim.py) that the head and its back cover; every other one stays dark
FISH_OVER_RIM = [(6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (3, 3), (4, 3)]


def build(grid=GRID):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(grid):
        assert len(row) == 16, (y, len(row))
        for x, ch in enumerate(row):
            if ch != ".":
                px[x, y] = PAL[ch] + (255,)
    return img


VANILLA = os.path.join(ART, ".vanilla", "item")
REFS = os.path.join(ART, "references", "fish_awrata_refonly")
SHEET = os.path.join(ART, "candidates", "fish_awrata_bucket.png")
HOTBAR = ["mc:cod_bucket", "bucket:cerna_bucket", "bucket:awrata_bucket"]
SLOT = (139, 139, 139, 255)
PY = os.path.join(ART, ".venv", "bin", "python")


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


def hotbars():
    outs = []
    for scale, name in ((2, "fish_awrata_bucket_hotbar.png"), (4, "fish_awrata_bucket_hotbar_x4.png")):
        p = os.path.join(ART, "candidates", name)
        subprocess.run([PY, os.path.join(ART, "tools", "hotbar_preview.py"), p] + HOTBAR
                       + ["--select", "2", "--scale", str(scale)], check=True, capture_output=True)
        outs.append(p)
    return outs


def sheet():
    import sys
    from PIL import ImageDraw
    sys.path.insert(0, os.path.join(ART, "tools"))
    from font import label_font
    from measure import measure

    font, small = label_font(16), label_font(13)
    W = 1500
    parts = []

    def text(lines, f=font):
        h = len(lines) * (f.size + 6) + 6
        im = Image.new("RGBA", (W, h), (255, 255, 255, 255))
        d = ImageDraw.Draw(im)
        for i, ln in enumerate(lines):
            d.text((10, 4 + i * (f.size + 6)), ln, fill=(0, 0, 0), font=f)
        return im

    parts.append(text(["Bucket of awrata (16 x 16): references (photos and a drawing, reference only)"]))
    row = Image.new("RGBA", (W, 190), (255, 255, 255, 255))
    x = 10
    for f in ("awrata_06.jpg", "awrata_02.jpg", "awrata_08.jpg", "awrata_09.jpg"):
        p = os.path.join(REFS, f)
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGBA")
        im.thumbnail((340, 180))
        row.alpha_composite(im, (x, 5))
        x += im.width + 10
    parts.append(row)

    ours = composite(Image.open(OUT).convert("RGBA"))
    icons = [("cod", Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")),
             ("salmon", Image.open(os.path.join(VANILLA, "salmon_bucket.png")).convert("RGBA")),
             ("tropical fish", Image.open(os.path.join(VANILLA, "tropical_fish_bucket.png")).convert("RGBA")),
             ("pufferfish", Image.open(os.path.join(VANILLA, "pufferfish_bucket.png")).convert("RGBA")),
             ("cerna (accepted)", composite(Image.open(os.path.join(ITEMS, "cerna_bucket.png")).convert("RGBA"))),
             ("AWRATA (in game)", ours),
             ("our layer alone", Image.open(OUT).convert("RGBA")),
             ("awrata item", Image.open(os.path.join(ITEMS, "awrata.png")).convert("RGBA"))]
    parts.append(text(["8x on the slot grey: vanilla cod, salmon, tropical fish, pufferfish buckets | accepted cerna "
                       "bucket | AWRATA bucket (over cod_bucket) | the layer alone | accepted awrata item"]))
    row = Image.new("RGBA", (W, 16 * 8 + 30), SLOT)
    d = ImageDraw.Draw(row)
    for i, (n, im) in enumerate(icons):
        row.alpha_composite(im.resize((128, 128), Image.NEAREST), (10 + i * 150, 4))
        d.text((10 + i * 150, 134), n, fill=(0, 0, 0), font=small)
    parts.append(row)

    parts.append(text(["1x and 2x (same order)"]))
    row = Image.new("RGBA", (W, 60), SLOT)
    for i, (n, im) in enumerate(icons):
        row.alpha_composite(im, (10 + i * 20, 20))
        row.alpha_composite(im.resize((32, 32), Image.NEAREST), (200 + i * 40, 12))
    parts.append(row)

    lines = ["art/tools/measure.py (whole bucket as players see it):"]
    tmp = os.path.join(os.path.dirname(SHEET), "fish_awrata_bucket_measure.tmp.png")
    for n, im in icons[:6]:
        im.save(tmp)
        m = measure(tmp)
        lines.append(f"  {n:18s} coverage {m['coverage']:.2f}  colours {m['colours']:2d}  darkest {float(m['lmin']):.2f}"
                     f"  lightest {float(m['lmax']):.2f}  outline {float(m['edge_l']):.2f}  inside {float(m['interior_l']):.2f}"
                     f"  top-left minus bottom-right {float(m['tl_minus_br']):+.2f}")
    os.remove(tmp)
    parts.append(text(lines, small))

    for p in hotbars():
        parts.append(text([f"Hotbar preview (art/tools/hotbar_preview.py): vanilla cod bucket, cerna bucket, AWRATA "
                           f"bucket (selected), on sky and night: {os.path.relpath(p, ROOT)}"]))
        im = Image.open(p).convert("RGBA")
        row = Image.new("RGBA", (W, im.height + 10), (255, 255, 255, 255))
        row.alpha_composite(im, (10, 5))
        parts.append(row)

    out = Image.new("RGBA", (W, sum(p.height for p in parts)), (255, 255, 255, 255))
    y = 0
    for p in parts:
        out.alpha_composite(p, (0, y))
        y += p.height
    os.makedirs(os.path.dirname(SHEET), exist_ok=True)
    out.convert("RGB").save(SHEET)
    print("wrote", os.path.relpath(SHEET, ROOT))


if __name__ == "__main__":
    import sys
    layer = build()
    check_cover(layer)
    check_rim(layer, os.path.join(VANILLA, "cod_bucket.png"), FISH_OVER_RIM)
    layer.save(OUT, optimize=False)
    print("wrote", os.path.relpath(OUT, ROOT))
    if "--sheet" in sys.argv[1:]:
        sheet()
