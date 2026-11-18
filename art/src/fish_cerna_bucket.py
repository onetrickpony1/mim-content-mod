"""Bucket of cerna: the fish layer of the item icon (16 x 16), 2026-11-18.

The bucket is not ours: the item model (made by art/src/pilot_models.py) puts the player's own vanilla
minecraft:item/cod_bucket underneath as layer0 and this texture on top as layer1, so the mod ships no Mojang
pixels (STYLE rule 3) and the bucket matches whatever resource pack the player uses. This file is therefore ONLY
the fish: rows 6-15 are clear, and in rows 1-5 every opaque pixel of the cod in cod_bucket is covered so no cod
shows through (checked by check_cover() on every run, against art/.vanilla's cod_bucket when it is there).
Same method as the accepted lampuka, tonn and sardina buckets (art/src/fish_lampuka_bucket.py, fish_tonn_bucket.py,
fish_sardina_bucket.py).

Laid out the way vanilla shows its live fish in a bucket (cod, salmon, tropical fish and pufferfish buckets, measured
in art/.vanilla): only the fish's head and the front of its body rise out of the water inside the rim, the head at
the upper left (eye in rows 2-3), the body sloping down to the right into the water; the back of the rim stays visible
at the right (11,2 / 12,3 / 13,4) and the water at the front edge. No tail shows: the rest of the fish is under water.
No black outline of its own (its darkest shades make its edge).

The cerna (dusky grouper, Epinephelus marginatus) is told apart at 1x by:
- the big, deep head, five rows high, with the spiny dorsal fin starting just behind it;
- the reddish-brown colour, lit on the forehead (top left), shading to the throat;
- the pale cream blotches among darker mottling on the head and flank, kept away from the eye;
- the one eye high on the head, and the mouth a soft brown corner above the jutting lit lower lip.
Colours are the owner-accepted cerna item icon's (textures/item/cerna.png, art/src/fish_cerna_icon.py), nothing
new; the water where the fish goes under is our own shades, the same as the other buckets'.
Photos (reference only): art/references/fish_cerna_refonly/ (list.tsv).

Writes: mod/src/main/resources/assets/mimcontent/textures/item/cerna_bucket.png
With --sheet it also writes the review sheet art/candidates/fish_cerna_bucket.png (references, what players see,
i.e. this layer over vanilla's cod_bucket, at 8x and 1x beside vanilla's fish buckets, the lampuka, tonn and
sardina buckets and the rejected cerna bucket, the layer alone, the accepted cerna item, measure.py numbers, and the
in-game hotbar crop from the cernabucket4 art run).
Run:    art/.venv/bin/python art/src/fish_cerna_bucket.py [--sheet]
"""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item",
                   "cerna_bucket.png")


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = {
    # water where the fish goes under: our own shades (as the lampuka, tonn and sardina buckets)
    "~": hx("#2a55c4"),
    "v": hx("#1d3c96"),  # the shadow on the water beside the fish (as the sardina bucket's)
    "^": hx("#6a92ea"),  # a glint of light on the water (as the sardina bucket's)
    # the cerna: the owner-accepted item icon's palette (textures/item/cerna.png, art/src/fish_cerna_icon.py), same keys
    "h": hx("#c8956a"),                       # the brightest light on the back, behind the eye
    "1": hx("#b27a55"), "2": hx("#a66c4a"), "3": hx("#93593f"), "4": hx("#7a4434"), "5": hx("#5e3228"),  # lit to shade
    "k": hx("#7a4632"),                       # rim on the lit forehead
    "o": hx("#2e1a14"),                       # rim on the shaded belly side and the stalk
    "C": hx("#ccac88"), "c": hx("#a8866a"),   # pale blotches: in the light, and partly shaded
    "e": hx("#0a0a0a"),                       # the eye (the only black)
    "L": hx("#b07a5e"), "l": hx("#8a5844"),   # the jutting lower lip (lit) and the shaded jaw behind it
    "M": hx("#4e2a1e"),                       # the corner of the mouth (brown, not black)
    "D": hx("#5a3224"), "f": hx("#8a5440"),   # the spiny dorsal fin along the back: dark spines, lit membrane
    "T": hx("#9a5e48"), "t": hx("#7a4838"), "u": hx("#4a2a20"),  # rounded tail: lit, mid, shaded rim
}

# rows 0-15, columns 0-15; "." is clear
# The head comes up out of the water at the left of the bucket mouth, as vanilla's fish do; the rest of the fish is
# under the water, so no tail shows. The front steps 4, 3, 3, 3, 4 down the rows (forehead, face, chin), inside the
# bucket's own rim: the mouth is a soft brown corner (M, 3,3) above the jutting lit lower lip (L, 3,4) and the
# shaded jaw curving back under it (l, 4,4 and 4,5). The one eye
# (6,2) sits high on the head with only lit or mid pixels around it. The spiny dorsal starts behind the head (f, D) and
# the back slopes down to the right into the water at 10,3. The head is lit at the top left and shades to the throat,
# mottled 2/3/4 among the pale blotches like the icon. Where the fish no longer covers the cod (rows 3-5 at the
# right), our own water covers it: a shadow (v) beside the fish where it goes under and a glint of light (^).
GRID = [
    "................",
    "....k12fD.......",
    "...k1he2C3f.....",
    "...M122C3c4~....",
    "...Ll3C45v~~~...",
    "....l45v~^~~....",
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

# The version the owner sent back (2026-11-18, art run cernabucket3): the whole fish lying across the mouth with its
# tail at the right ("it doesnt make sense if its tail is there, then its been snapped in half"). Sheet only.
REJECTED = [
    "................",
    "....kfDfDD......",
    "...ke1h2C34.Tt..",
    "...214CC3c5oTtu.",
    "...M3434c55ottu.",
    "...Ll4c55oo~tu..",
] + ["................"] * 10


def build(grid=GRID):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(grid):
        assert len(row) == 16, (y, len(row))
        for x, ch in enumerate(row):
            if ch != ".":
                px[x, y] = PAL[ch] + (255,)
    return img


VANILLA = os.path.join(ROOT, "art", ".vanilla", "item")
ITEMS = os.path.dirname(OUT)
REFS = os.path.join(ROOT, "art", "references", "fish_cerna_refonly")
SHOTS = os.path.join(ROOT, ".art-runs", "cernabucket4", "build", "smoke-run", "screenshots")
SHEET = os.path.join(ROOT, "art", "candidates", "fish_cerna_bucket.png")
SLOT = (139, 139, 139, 255)


def sheet():
    import glob
    import sys
    from PIL import ImageDraw
    sys.path.insert(0, os.path.join(ROOT, "art", "tools"))
    from font import label_font
    from measure import measure

    font, small = label_font(16), label_font(13)
    W = 1700
    parts = []

    def text(lines, f=font, h=None):
        h = h or (len(lines) * (f.size + 6) + 6)
        im = Image.new("RGBA", (W, h), (255, 255, 255, 255))
        d = ImageDraw.Draw(im)
        for i, ln in enumerate(lines):
            d.text((10, 4 + i * (f.size + 6)), ln, fill=(0, 0, 0), font=f)
        return im

    # references
    parts.append(text(["Bucket of cerna (16 x 16): references (photos and drawings, reference only)"]))
    row = Image.new("RGBA", (W, 190), (255, 255, 255, 255))
    x = 10
    for f in ("side_4.jpg", "caught_1.jpg", "head_1.jpg", "side_1.jpg"):
        im = Image.open(os.path.join(REFS, f)).convert("RGBA")
        im.thumbnail((340, 180))
        row.alpha_composite(im, (x, 5))
        x += im.width + 10
    parts.append(row)

    # 8x beside vanilla and the accepted lampuka, tonn and sardina buckets
    ours = composite(Image.open(OUT).convert("RGBA"))
    lamp = composite(Image.open(os.path.join(ITEMS, "lampuka_bucket.png")).convert("RGBA"))
    tonn = composite(Image.open(os.path.join(ITEMS, "tonn_bucket.png")).convert("RGBA"))
    sard = composite(Image.open(os.path.join(ITEMS, "sardina_bucket.png")).convert("RGBA"))
    rej = composite(build(REJECTED))
    icons = [("cod", Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")),
             ("salmon", Image.open(os.path.join(VANILLA, "salmon_bucket.png")).convert("RGBA")),
             ("tropical fish", Image.open(os.path.join(VANILLA, "tropical_fish_bucket.png")).convert("RGBA")),
             ("pufferfish", Image.open(os.path.join(VANILLA, "pufferfish_bucket.png")).convert("RGBA")),
             ("lampuka bucket", lamp), ("tonn bucket", tonn), ("sardina bucket", sard),
             ("cerna REJECTED", rej), ("CERNA NEW (in game)", ours),
             ("our layer alone", Image.open(OUT).convert("RGBA")),
             ("cerna item", Image.open(os.path.join(ITEMS, "cerna.png")).convert("RGBA"))]
    parts.append(text(["8x on the slot grey: vanilla cod, salmon, tropical fish, pufferfish | lampuka, tonn, sardina | "
                       "cerna rejected (cernabucket3) | cerna NEW (over cod_bucket) | layer alone | accepted cerna item"]))
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
        row.alpha_composite(im.resize((32, 32), Image.NEAREST), (260 + i * 40, 12))
    parts.append(row)

    lines = ["art/tools/measure.py:"]
    tmp = os.path.join(os.path.dirname(SHEET), "fish_cerna_bucket_measure.tmp.png")
    for n, im in icons[:9]:
        im.save(tmp)
        m = measure(tmp)
        lines.append(f"  {n:18s} coverage {m['coverage']:.2f}  colours {m['colours']:2d}  darkest {float(m['lmin']):.2f}"
                     f"  lightest {float(m['lmax']):.2f}  outline {float(m['edge_l']):.2f}  inside {float(m['interior_l']):.2f}"
                     f"  top-left minus bottom-right {float(m['tl_minus_br']):+.2f}")
    os.remove(tmp)
    parts.append(text(lines, small))

    shots = sorted(glob.glob(os.path.join(SHOTS, "*fish-08*.png")))
    parts.append(text(["In game, hotbar at 3x (art run cernabucket4; slot 1 vanilla cod, last vanilla salmon; the rest are "
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
