"""Bucket of lampuka: the fish layer of the item icon (16 x 16), 2026-11-18.

The bucket is not ours: the item model (made by art/src/pilot_models.py) puts the player's own vanilla
minecraft:item/cod_bucket underneath as layer0 and this texture on top as layer1, so the mod ships no Mojang
pixels (STYLE rule 3) and the bucket matches whatever resource pack the player uses. This file is therefore ONLY
the fish: rows 6-15 are clear, and in rows 1-5 the lampuka covers every opaque pixel of the cod in cod_bucket so no
cod shows through (checked by check_cover() on every run, against art/.vanilla's cod_bucket when it is there).

Laid out the way vanilla lays its live fish in a bucket (measured from cod_bucket, salmon_bucket,
tropical_fish_bucket): the fish lies across the bucket mouth in rows 1 to 5, head to the left and a little higher,
tail to the right against the back of the rim, with no black outline of its own (its darkest shades make its edge).

The lampuka (dolphinfish, Coryphaena hippurus) is told apart at 1x by:
- the blunt, steep green head at the left: row 1 starts one column in, so the forehead is the front edge;
- the long dark dorsal fin, running from the top of the head down the whole back to the tail;
- the gold body with a cream throat and belly;
- the forked yellow tail at the right, its two lobes opening around a notch of water (our own blue).
Colours are the accepted lampuka item icon's (textures/item/lampuka.png). Photos (reference only):
art/references/fish_lampuka_refonly/ (list.tsv).

Writes: mod/src/main/resources/assets/mimcontent/textures/item/lampuka_bucket.png
With --sheet it also writes the review sheet art/candidates/fish_lampuka_bucket.png (references, what players see,
i.e. this layer over vanilla's cod_bucket, at 8x and 1x beside vanilla's fish buckets, the layer alone,
measure.py numbers, and the in-game hotbar crop from the lampukabucket2 art run).
Run:    art/.venv/bin/python art/src/fish_lampuka_bucket.py [--sheet]
"""
import os

from PIL import Image

from fish_bucket_rim import check_rim

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item",
                   "lampuka_bucket.png")


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = {
    # water seen in the tail's notch and behind the tail: our own shade, near the bucket's deep water
    "w": hx("#2a55c4"),
    # the lampuka: the accepted item icon's colours
    "J": hx("#2c4a48"),  # dark slate: the dorsal fin, running from the top of the head
    "N": hx("#2f7a68"),  # mid green: the steep forehead / snout
    "E": hx("#5cbc9e"),  # green: the head
    "D": hx("#9ae2bc"),  # pale mint: light on the head
    "H": hx("#a8c03c"),  # yellow-green: where green turns to gold
    "K": hx("#e6c12c"),  # gold: the flank
    "I": hx("#a67c18"),  # dark gold: lower flank
    "O": hx("#f6eecb"),  # cream: throat and belly
    "M": hx("#101010"),  # the eye
    "B": hx("#c4b43a"),  # yellow: the tail
    "A": hx("#5e5a1c"),  # olive: tail edge and wrist
}

# rows 0-15, columns 0-15; "." is clear
GRID = [
    "................",
    "....JJJJJJ......",
    "...NDEEEHJ..B...",
    "...NEMHKKKJB....",
    "...NEHKKKIAAw...",
    "....NOOIIAwBB...",
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


# The back-rim outline pixels (art/src/fish_bucket_rim.py) that the head, the dorsal fin along the back and the upper tail lobe cover; every other one stays dark
FISH_OVER_RIM = [(5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (3, 3), (4, 3), (11, 3)]


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
REFS = os.path.join(ROOT, "art", "references", "fish_lampuka_refonly")
SHOTS = os.path.join(ROOT, ".art-runs", "lampukabucket2", "build", "smoke-run", "screenshots")
SHEET = os.path.join(ROOT, "art", "candidates", "fish_lampuka_bucket.png")
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
    parts = []  # (image, gap after)

    def text(lines, f=font, h=None):
        h = h or (len(lines) * (f.size + 6) + 6)
        im = Image.new("RGBA", (W, h), (255, 255, 255, 255))
        d = ImageDraw.Draw(im)
        for i, ln in enumerate(lines):
            d.text((10, 4 + i * (f.size + 6)), ln, fill=(0, 0, 0), font=f)
        return im

    # references
    parts.append(text(["Bucket of lampuka (16 x 16): references (photos, reference only)"]))
    row = Image.new("RGBA", (W, 190), (255, 255, 255, 255))
    x = 10
    for f in ("side_spain.jpg", "side_tunisia.png", "male_bull.jpg", "dominica.jpg"):
        im = Image.open(os.path.join(REFS, f)).convert("RGBA")
        im.thumbnail((360, 180))
        row.alpha_composite(im, (x, 5))
        x += im.width + 10
    parts.append(row)

    # 8x beside vanilla
    names = [("cod", os.path.join(VANILLA, "cod_bucket.png")), ("salmon", os.path.join(VANILLA, "salmon_bucket.png")),
             ("tropical fish", os.path.join(VANILLA, "tropical_fish_bucket.png")),
             ("LAMPUKA (in game)", None), ("our layer alone", OUT), ("lampuka item (accepted)", os.path.join(ITEMS, "lampuka.png"))]
    lamp = composite(Image.open(OUT).convert("RGBA"))
    lamp_path = os.path.join(os.path.dirname(SHEET), "fish_lampuka_bucket_composite.tmp.png")
    lamp.save(lamp_path)
    icons = [(n, lamp if p is None else Image.open(p).convert("RGBA")) for n, p in names]
    parts.append(text(["8x on the slot grey: vanilla cod, salmon, tropical fish buckets | the lampuka bucket as players "
                       "see it (our layer over their cod_bucket) | our layer alone | the accepted lampuka item"]))
    row = Image.new("RGBA", (W, 16 * 8 + 30), SLOT)
    d = ImageDraw.Draw(row)
    for i, (n, im) in enumerate(icons):
        row.alpha_composite(im.resize((128, 128), Image.NEAREST), (10 + i * 150, 4))
        d.text((10 + i * 150, 134), n, fill=(0, 0, 0), font=small)
    parts.append(row)

    # 1x and 2x hotbar-like rows
    parts.append(text(["1x and 2x, as in the hotbar (same order)"]))
    row = Image.new("RGBA", (W, 60), SLOT)
    for i, (n, im) in enumerate(icons):
        row.alpha_composite(im, (10 + i * 20, 20))
        row.alpha_composite(im.resize((32, 32), Image.NEAREST), (200 + i * 40, 12))
    parts.append(row)

    # numbers
    lines = ["art/tools/measure.py:"]
    for n, p in names[:5]:
        m = measure(p or lamp_path)
        lines.append(f"  {n:14s} coverage {m['coverage']:.2f}  colours {m['colours']:2d}  darkest {float(m['lmin']):.2f}"
                     f"  lightest {float(m['lmax']):.2f}  outline {float(m['edge_l']):.2f}  inside {float(m['interior_l']):.2f}"
                     f"  top-left minus bottom-right {float(m['tl_minus_br']):+.2f}")
    os.remove(lamp_path)
    parts.append(text(lines, small))

    # in-game crops
    shots = sorted(glob.glob(os.path.join(SHOTS, "*fish-08*.png")))
    parts.append(text(["In game, hotbar at 3x (art run lampukabucket2; slot 1 vanilla cod, slot 2 the lampuka, last vanilla salmon; the rest are other fish placeholders): " + (", ".join(os.path.basename(s) for s in shots)
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
    check_rim(layer, os.path.join(VANILLA, "cod_bucket.png"), FISH_OVER_RIM)
    layer.save(OUT, optimize=False)
    print("wrote", os.path.relpath(OUT, ROOT))
    if "--sheet" in sys.argv[1:]:
        sheet()
