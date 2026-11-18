"""Bucket of huta kahla (blue shark): the fish layer of the item icon (16 x 16), 2026-11-18.

The bucket is not ours: the item model (made by art/src/pilot_models.py) puts the player's own vanilla
minecraft:item/cod_bucket underneath as layer0 and this texture on top as layer1, so the mod ships no Mojang
pixels (STYLE rule 3) and the bucket matches whatever resource pack the player uses. This file is therefore ONLY
the fish: rows 6-15 are clear, and in rows 1-5 every opaque pixel of the cod in cod_bucket is covered so no cod
shows through (checked by check_cover() on every run, against art/.vanilla's cod_bucket when it is there).
Same method as the owner-accepted cerna, awrata, murina, pixxispad and ziemel buckets, whose check and water shades
it uses; the back-rim outline is checked by art/src/fish_bucket_rim.py (owner 2026-11-18, keep the back outline).

Laid out the way vanilla shows its live fish in a bucket: only the head rises out of the water inside the rim, the
snout at the upper left, the back sloping down to the right into the water. No tail and no whole fish show.

The huta kahla (blue shark, Prionace glauca) is told apart at 1x by:
- the long pointed conical snout, its tip a single pixel at (0,2) out past the bucket's left side, and a flat top
  running straight back from it along row 1, with no crown or forehead dome (round 1's dome over a short snout
  read as a dolphin);
- the one large eye (3,2) three pixels behind the tip, inside the lit blue, with no dark pixel beside it;
- the indigo back (1) over the lit top of the head (D, light from the top left) and the blue side (3), then the
  sharp change to the white underside (5), turning into shade (6, G) where the throat meets the water;
- the triangular first dorsal fin standing up out of the water behind the head (10-12, 0-3) and breaking the
  bucket's outline against the slot, the instant shark cue: a lit leading edge (D, light from the top left like
  the body's) rising to a swept-back tip (11,0), an indigo middle (1) and a dark trailing edge (p). It is a solid
  fin three pixels wide at the far rim, never a line (the owner rejected a thin, long fin on the item icon). It
  stands in front of the far rim at (10,2) and its corner (11,3), as the accepted pixxispad's dorsal does; the rim
  pixel behind its trailing edge (12,3) stays dark. Under the surface it is only a shadow (v, p);
- the water kept apart from the fish: no light water (^) touches the head or the fin (round 1's light ring merged
  with the lit head), only one glint far right (12,5), and a shadow (v) under the white throat keeps that edge
  crisp.
No teeth, no mouth line, no gill slits (at this size they read as a face or extra eyes).
Colours are the owner-accepted huta kahla item icon's (textures/item/huta_kahla.png, art/src/fish_huta_kahla_icon.py
PAL), same keys, nothing new; the water and the rim tone are the shared bucket shades (art/src/fish_bucket_rim.py).
Photos (reference only): art/references/fish_huta_kahla_refonly/ (list.tsv).

Writes: mod/src/main/resources/assets/mimcontent/textures/item/huta_kahla_bucket.png (byte-identical on rerun)
With --sheet it also writes the review sheet art/candidates/fish_huta_kahla_bucket.png (references, what players see,
i.e. this layer over vanilla's cod_bucket, at 8x and 1x beside vanilla's water and cod buckets and the accepted
cerna, awrata, murina, pixxispad and ziemel buckets, the layer alone, the accepted huta kahla item, measure.py
numbers, and offline hotbar previews at GUI scale 2 and 4).
Run:    art/.venv/bin/python art/src/fish_huta_kahla_bucket.py [--sheet]
"""
import os
import subprocess

from PIL import Image

from fish_bucket_rim import RIM, check_rim

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item",
                   "huta_kahla_bucket.png")


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = {
    # water where the fish goes under: the shared bucket water shades (art/src/fish_bucket_rim.py WATER)
    "~": hx("#2a55c4"),
    "v": hx("#1d3c96"),  # the shadow on the water under the head
    "^": hx("#6a92ea"),  # light on the water, ringing the dorsal fin so it stands out
    "#": RIM,  # the bucket's back-rim outline where we cover a cod pixel: the shared tone (vanilla's is #353535)
    # the huta kahla: the owner-accepted item icon's palette (art/src/fish_huta_kahla_icon.py PAL), same keys
    "1": hx("#303a86"), "3": hx("#4a66c0"),   # indigo back (and outline), blue side
    "D": hx("#7a90dc"),                       # lit top of the head
    "5": hx("#e8ecf6"), "6": hx("#a8b0cc"), "G": hx("#464e7c"),  # white underside, turning into shade
    "e": hx("#0a0a16"),                       # the eye (the only near-black)
    "p": hx("#262e74"),                       # dorsal fin: the darkest indigo (the icon's dorsal tip)
}

# rows 0-15, columns 0-15; "." is clear
GRID = [
    "...........p....",
    "..1DDD331.D1....",
    "3DDe33331#D1p...",
    ".G5556Gv~~3p#...",
    "...66Gv~~vp~~...",
    "....Gv~~~vv~^...",
] + ["................"] * 10

# Round 1 (critic: FIX, read as a dolphin: a domed crown over a short snout, the fin a dark smudge in the water,
# the light water ring the same blue as the lit head), kept for the old-and-new compare on the sheet
ROUND1 = [
    "....111.........",
    "..1DDD331.......",
    "3DDe33331#......",
    ".G5556Gv~^p#....",
    "...66G~~^1p^~...",
    "....G~~^1pp^~...",
] + ["................"] * 10

# Shapes tried on the way and dropped (sheet only).
TRIED = {
    "critic's mock": [
        "...........1....",
        "..1DDD331.31....",
        "3DDe33331#3p1...",
        ".G5556Gv~^3p#...",
        "...66G~~^1p^~...",
        "....G~~^1pp^~...",
    ] + ["................"] * 10,
    "tried: fin to the floor": [
        "...........p....",
        "..1DDD331.D1....",
        "3DDe33331#D1p...",
        ".G5556Gv~~31#...",
        "...66Gv~~1p~~...",
        "....Gv~~1pp~^...",
    ] + ["................"] * 10,
    "tried: lit fin": [
        "..111...........",
        ".1DDD331........",
        "3D3e33311#......",
        ".G5563G~~^1#....",
        "...66G~~^D1v~...",
        "....G~~^D11v~...",
    ] + ["................"] * 10,
    "tried: tall forehead": [
        "...111..........",
        ".11DD3311.......",
        "3DD3e333G1......",
        ".5556GGv~~1#....",
        "...6Gv~~^D1p^...",
        "....v~~^D1pp~...",
    ] + ["................"] * 10,
}


# The back-rim outline pixels (art/src/fish_bucket_rim.py) that the fish stands in front of: the head and its back
# (5-8,2 and 3-4,3) and the dorsal fin (10,2 and 11,3); every other one stays dark
FISH_OVER_RIM = [(5, 2), (6, 2), (7, 2), (8, 2), (10, 2), (3, 3), (4, 3), (11, 3)]


def build(grid=GRID):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(grid):
        assert len(row) == 16, (y, len(row))
        for x, ch in enumerate(row):
            if ch != ".":
                px[x, y] = PAL[ch] + (255,)
    return img


ART = os.path.join(ROOT, "art")
VANILLA = os.path.join(ART, ".vanilla", "item")
ITEMS = os.path.dirname(OUT)
REFS = os.path.join(ART, "references", "fish_huta_kahla_refonly")
SHEET = os.path.join(ART, "candidates", "fish_huta_kahla_bucket.png")
SLOT = (139, 139, 139, 255)


def hotbars():
    """Offline hotbar previews (art/tools/hotbar_preview.py) at GUI scale 2 and 4."""
    py = os.path.join(ART, ".venv", "bin", "python")
    tool = os.path.join(ART, "tools", "hotbar_preview.py")
    old = os.path.join(ART, "candidates", "fish_huta_kahla_bucket_round1.png")
    composite(build(ROUND1)).save(old)
    outs = []
    for suffix, scale in (("", "2"), ("_x4", "4")):
        out = os.path.join(ART, "candidates", f"fish_huta_kahla_bucket_hotbar{suffix}.png")
        subprocess.run([py, tool, out, "mc:cod_bucket", "bucket:tonn_bucket", "bucket:cerna_bucket",
                        "bucket:murina_bucket", "bucket:pixxispad_bucket", "bucket:ziemel_bucket", "file:" + old,
                        "bucket:huta_kahla_bucket", "mod:huta_kahla", "--select", "7", "--scale", scale],
                       check=True, capture_output=True)
        outs.append(out)
    return outs


def sheet():
    import sys
    from PIL import ImageDraw
    sys.path.insert(0, os.path.join(ART, "tools"))
    from font import label_font
    from measure import measure

    font, small = label_font(16), label_font(13)
    W = 2300
    parts = []

    def text(lines, f=font, h=None):
        h = h or (len(lines) * (f.size + 6) + 6)
        im = Image.new("RGBA", (W, h), (255, 255, 255, 255))
        d = ImageDraw.Draw(im)
        for i, ln in enumerate(lines):
            d.text((10, 4 + i * (f.size + 6)), ln, fill=(0, 0, 0), font=f)
        return im

    parts.append(text(["Bucket of huta kahla (blue shark, 16 x 16): references, landed sharks for true colour, one live shark for the head "
                       "(art/references/fish_huta_kahla_refonly, reference only)"]))
    row = Image.new("RGBA", (W, 190), (255, 255, 255, 255))
    x = 10
    for f in ("bs03.jpg", "bs05.jpg", "bs07.jpg", "bs11.jpg"):
        p = os.path.join(REFS, f)
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGBA")
        im.thumbnail((420, 180))
        row.alpha_composite(im, (x, 5))
        x += im.width + 10
    parts.append(row)

    ours = composite(Image.open(OUT).convert("RGBA"))
    icons = [("water", Image.open(os.path.join(VANILLA, "water_bucket.png")).convert("RGBA")),
             ("cod", Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA"))]
    icons += [(f"{n} bucket", composite(Image.open(os.path.join(ITEMS, f"{n}_bucket.png")).convert("RGBA")))
              for n in ("tonn", "cerna", "awrata", "murina", "pixxispad", "ziemel")]
    icons += [("HUTA KAHLA (in game)", ours), ("round 1 (FIX)", composite(build(ROUND1))),
              ("our layer alone", Image.open(OUT).convert("RGBA")),
              ("huta kahla item", Image.open(os.path.join(ITEMS, "huta_kahla.png")).convert("RGBA"))]
    tried = [(n, composite(build(g))) for n, g in TRIED.items()]
    parts.append(text(["8x on the slot grey: vanilla water, cod | accepted tonn, cerna, awrata, murina, pixxispad, ziemel "
                       "buckets | HUTA KAHLA round 2 (over cod_bucket) | round 1 | layer alone | accepted huta kahla item | "
                       "shapes tried and dropped"]))
    row = Image.new("RGBA", (W, 16 * 8 + 30), SLOT)
    d = ImageDraw.Draw(row)
    for i, (n, im) in enumerate(icons + tried):
        row.alpha_composite(im.resize((128, 128), Image.NEAREST), (10 + i * 145, 4))
        d.text((10 + i * 145, 134), n, fill=(0, 0, 0), font=small)
    parts.append(row)

    parts.append(text(["1x and 2x, on the slot grey and on dark (same order)"]))
    row = Image.new("RGBA", (W, 100), SLOT)
    ImageDraw.Draw(row).rectangle((0, 50, W, 100), fill=(40, 40, 40))
    for i, (n, im) in enumerate(icons):
        for y0 in (0, 50):
            row.alpha_composite(im, (10 + i * 20, y0 + 17))
            row.alpha_composite(im.resize((32, 32), Image.NEAREST), (300 + i * 40, y0 + 9))
    parts.append(row)

    lines = ["art/tools/measure.py (whole composite as players see it):"]
    tmp = os.path.join(os.path.dirname(SHEET), "fish_huta_kahla_bucket_measure.tmp.png")
    for n, im in icons[:10] + icons[11:]:
        im.save(tmp)
        m = measure(tmp)
        lines.append(f"  {n:20s} coverage {m['coverage']:.2f}  colours {m['colours']:2d}  darkest {float(m['lmin']):.2f}"
                     f"  lightest {float(m['lmax']):.2f}  outline {float(m['edge_l']):.2f}  inside {float(m['interior_l']):.2f}"
                     f"  top-left minus bottom-right {float(m['tl_minus_br']):+.2f}")
    os.remove(tmp)
    parts.append(text(lines, small))

    parts.append(text(["Hotbar preview (art/tools/hotbar_preview.py, offline, as the game draws flat items) at GUI scale 2 "
                       "and 4: vanilla cod bucket, tonn, cerna, murina, pixxispad, ziemel buckets, huta kahla round 1, "
                       "HUTA KAHLA BUCKET round 2 (selected), huta kahla item"]))
    for p in hotbars():
        hb = Image.open(p).convert("RGBA")
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
    for n in ("cod_bucket", "salmon_bucket", "tropical_fish_bucket", "pufferfish_bucket", "water_bucket", "bucket"):
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
