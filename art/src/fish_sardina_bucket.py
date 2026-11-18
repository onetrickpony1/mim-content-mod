"""Bucket of sardina: the fish layer of the item icon (16 x 16), 2026-11-18.

The bucket is not ours: the item model (made by art/src/pilot_models.py) puts the player's own vanilla
minecraft:item/cod_bucket underneath as layer0 and this texture on top as layer1, so the mod ships no Mojang
pixels (STYLE rule 3) and the bucket matches whatever resource pack the player uses. This file is therefore ONLY
the fish: rows 6-15 are clear, and in rows 1-5 every opaque pixel of the cod in cod_bucket is covered so no cod
shows through (checked by check_cover() on every run, against art/.vanilla's cod_bucket when it is there).
Same method as the accepted lampuka and tonn buckets (art/src/fish_lampuka_bucket.py, fish_tonn_bucket.py).

Laid out the way vanilla lays its live fish in a bucket: across the bucket mouth, head to the left and a little
higher, tail to the right over the back of the rim, no black outline of its own. A sardine is far slimmer than the
cod, so it fills only rows 1 to 3 (2 rows at the tail half, 1 at the stalk); the rest of the cod's place, rows 4
and 5, is our own water, with the fish's shadow under its belly and two glints of light.

The sardina (European sardine, Sardina pilchardus) is told apart at 1x by:
- the slim spindle shape: three rows deep at the head, two behind the dorsal fin, one at the tail stalk;
- the dark blue-green back with a lit teal edge on the forehead (light from the top left);
- the bright silver-white side and belly, with two dark spots along the upper flank behind the gill cover;
- the big black eye just behind the snout and the gold-tinged gill cover behind it;
- the deeply forked tail at the right, its two lobes opening around a clear notch.
Colours are the sardina item icon's (textures/item/sardina.png, art/src/fish_sardina_icon.py); the water and
the shadow are our own shades (the water the same as the lampuka and tonn buckets'). Photos (reference only):
art/references/fish_sardina_refonly/ (list.tsv).

Writes: mod/src/main/resources/assets/mimcontent/textures/item/sardina_bucket.png
With --sheet it also writes the review sheet art/candidates/fish_sardina_bucket.png (references, what players
see, i.e. this layer over vanilla's cod_bucket, at 8x and 1x beside vanilla's fish buckets and the lampuka and
tonn buckets, the layer alone, measure.py numbers, and the in-game hotbar crop from the sardinabucket2 art run).
Run:    art/.venv/bin/python art/src/fish_sardina_bucket.py [--sheet]
"""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item",
                   "sardina_bucket.png")


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = {
    # water and the fish's shadow on it: our own shades, near the bucket's deep water
    "~": hx("#2a55c4"),  # water (as the lampuka and tonn buckets)
    "v": hx("#1d3c96"),  # the shadow under the belly
    "^": hx("#6a92ea"),  # a glint of light on the water
    # the sardina: the item icon's colours
    "b": hx("#8cc6be"),  # lit teal: the forehead, the sheen on the back facing the light
    "C": hx("#24525e"),  # dark blue-green: the back
    "E": hx("#4a7076"),  # teal: the dorsal fin, the upper tail lobe
    "A": hx("#587a80"),  # mid teal: the snout
    "F": hx("#eef3f2"),  # silver-white: cheek, side, belly
    "G": hx("#b4c2c9"),  # silver
    "D": hx("#7e8e99"),  # grey silver: the shaded lower flank near the tail
    "I": hx("#5f7684"),  # the soft dark spots on the upper flank, well behind the eye (the icon's softened spot)
    "H": hx("#2f3a45"),  # dark slate: the tail stalk and the lower tail lobe
    "K": hx("#0a0a0a"),  # the eye
    "L": hx("#dcbc62"),  # gold: the gill cover
    "M": hx("#a88a44"),  # dark gold: the gill cover's lower edge
}

# rows 0-15, columns 0-15; "." is clear
GRID = [
    "................",
    "....bCCCCE......",
    "...AKLFFIGIC.EE.",
    "...GFMFFFGGDHH..",
    "...~~vvvvv~~~HH.",
    "....~~^~~~^~....",
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


def build():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(GRID):
        assert len(row) == 16, (y, len(row))
        for x, ch in enumerate(row):
            if ch != ".":
                px[x, y] = PAL[ch] + (255,)
    return img


VANILLA = os.path.join(ROOT, "art", ".vanilla", "item")
ITEMS = os.path.dirname(OUT)
REFS = os.path.join(ROOT, "art", "references", "fish_sardina_refonly")
SHOTS = os.path.join(ROOT, ".art-runs", "sardinabucket2", "build", "smoke-run", "screenshots")
SHEET = os.path.join(ROOT, "art", "candidates", "fish_sardina_bucket.png")
SLOT = (139, 139, 139, 255)


def sheet():
    import glob
    import sys
    from PIL import ImageDraw
    sys.path.insert(0, os.path.join(ROOT, "art", "tools"))
    from font import label_font
    from measure import measure

    font, small = label_font(16), label_font(13)
    W = 1500
    parts = []

    def text(lines, f=font, h=None):
        h = h or (len(lines) * (f.size + 6) + 6)
        im = Image.new("RGBA", (W, h), (255, 255, 255, 255))
        d = ImageDraw.Draw(im)
        for i, ln in enumerate(lines):
            d.text((10, 4 + i * (f.size + 6)), ln, fill=(0, 0, 0), font=f)
        return im

    # references
    parts.append(text(["Bucket of sardina (16 x 16): references (photos and drawings, reference only)"]))
    row = Image.new("RGBA", (W, 190), (255, 255, 255, 255))
    x = 10
    for f in ("side_1.jpg", "sardina_galicia.jpg", "drawing_gervais.jpg", "school_monterey.jpg"):
        im = Image.open(os.path.join(REFS, f)).convert("RGBA")
        im.thumbnail((340, 180))
        row.alpha_composite(im, (x, 5))
        x += im.width + 10
    parts.append(row)

    # 8x beside vanilla and the accepted lampuka and tonn buckets
    ours = composite(Image.open(OUT).convert("RGBA"))
    lamp = composite(Image.open(os.path.join(ITEMS, "lampuka_bucket.png")).convert("RGBA"))
    tonn = composite(Image.open(os.path.join(ITEMS, "tonn_bucket.png")).convert("RGBA"))
    icons = [("cod", Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")),
             ("salmon", Image.open(os.path.join(VANILLA, "salmon_bucket.png")).convert("RGBA")),
             ("tropical fish", Image.open(os.path.join(VANILLA, "tropical_fish_bucket.png")).convert("RGBA")),
             ("lampuka bucket", lamp), ("tonn bucket", tonn), ("SARDINA (in game)", ours),
             ("our layer alone", Image.open(OUT).convert("RGBA")),
             ("sardina item", Image.open(os.path.join(ITEMS, "sardina.png")).convert("RGBA"))]
    parts.append(text(["8x on the slot grey: vanilla cod, salmon, tropical fish buckets | the lampuka and tonn buckets | "
                       "the sardina bucket as players see it (our layer over their cod_bucket) | our layer alone | "
                       "the sardina item"]))
    row = Image.new("RGBA", (W, 16 * 8 + 30), SLOT)
    d = ImageDraw.Draw(row)
    for i, (n, im) in enumerate(icons):
        row.alpha_composite(im.resize((128, 128), Image.NEAREST), (10 + i * 150, 4))
        d.text((10 + i * 150, 134), n, fill=(0, 0, 0), font=small)
    parts.append(row)

    parts.append(text(["1x and 2x, as in the hotbar (same order)"]))
    row = Image.new("RGBA", (W, 60), SLOT)
    for i, (n, im) in enumerate(icons):
        row.alpha_composite(im, (10 + i * 20, 20))
        row.alpha_composite(im.resize((32, 32), Image.NEAREST), (200 + i * 40, 12))
    parts.append(row)

    lines = ["art/tools/measure.py:"]
    tmp = os.path.join(os.path.dirname(SHEET), "fish_sardina_bucket_measure.tmp.png")
    for n, im in icons[:6]:
        im.save(tmp)
        m = measure(tmp)
        lines.append(f"  {n:18s} coverage {m['coverage']:.2f}  colours {m['colours']:2d}  darkest {float(m['lmin']):.2f}"
                     f"  lightest {float(m['lmax']):.2f}  outline {float(m['edge_l']):.2f}  inside {float(m['interior_l']):.2f}"
                     f"  top-left minus bottom-right {float(m['tl_minus_br']):+.2f}")
    os.remove(tmp)
    parts.append(text(lines, small))

    shots = sorted(glob.glob(os.path.join(SHOTS, "*fish-08*.png")))
    parts.append(text(["In game, hotbar at 3x (art run sardinabucket2; slot 1 vanilla cod, last vanilla salmon; the rest are "
                       "the mod's fish items, buckets and eggs): " + (", ".join(os.path.basename(s) for s in shots)
                                                                      or "no shots yet")]))
    for s in shots:
        im = Image.open(s).convert("RGBA")
        sx = im.width / 854
        hb = im.crop((round(240 * sx), round(430 * sx), round(612 * sx), im.height))  # the hotbar
        hb = hb.resize((hb.width * 3, hb.height * 3), Image.NEAREST)
        row = Image.new("RGBA", (W, hb.height + 10), (255, 255, 255, 255))
        row.alpha_composite(hb, (10, 5))
        parts.append(row)

    out = Image.new("RGBA", (W, sum(p.height for p in parts)), (255, 255, 255, 255))
    y = 0
    for p in parts:
        out.alpha_composite(p, (0, y))
        y += p.height
    os.makedirs(os.path.dirname(SHEET), exist_ok=True)
    out.convert("RGB").save(SHEET)
    print("wrote", os.path.relpath(SHEET, ROOT))


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


if __name__ == "__main__":
    import sys
    layer = build()
    check_cover(layer)
    layer.save(OUT, optimize=False)
    print("wrote", os.path.relpath(OUT, ROOT))
    if "--sheet" in sys.argv[1:]:
        sheet()
