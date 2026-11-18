"""Bucket of pixxispad: the fish layer of the item icon (16 x 16), 2026-11-18.

The bucket is not ours: the item model (made by art/src/pilot_models.py) puts the player's own vanilla
minecraft:item/cod_bucket underneath as layer0 and this texture on top as layer1, so the mod ships no Mojang
pixels (STYLE rule 3) and the bucket matches whatever resource pack the player uses. This file is therefore ONLY
the fish: rows 6-15 are clear, and in rows 1-5 every opaque pixel of the cod in cod_bucket is covered so no cod
shows through (checked by check_cover() on every run, against art/.vanilla's cod_bucket when it is there).
Same method as the owner-accepted cerna, awrata and murina buckets (art/src/fish_cerna_bucket.py and the others),
whose check and water shades it uses.

Laid out the way vanilla shows its live fish in a bucket: only the head and the front of the back rise out of the
water inside the rim, the head at the upper left, the back sloping down to the right into the water. No tail shows.
The sword points up and out to the upper left and breaks the outline past the rim, as vanilla's pufferfish bucket
breaks it with its spines.

The pixxispad (swordfish, Xiphias gladius) is told apart at 1x by:
- the long pale sword, four pixels on the diagonal from the upper jaw (3,3) to the corner (0,0), lit on top, with a
  shaded underside (u, 2,3) at its base so it reads as a flat bill and not a stick;
- the forehead sloping straight into the top of the sword (3,2 / 4,1), as on the fish;
- the one large eye (5,2) just above and behind the sword's base, with only lit or mid tones round it;
- the short pointed lower jaw (j, 3,4) under the sword's base, darker than the sword, so the bill stands apart;
- the purple-bronze back, lit on the forehead (top left), over bronze-silver cheeks and a pale throat, shading to the
  lower right where the fish goes under;
- the front of the tall sickle dorsal fin breaking the water behind the head (10-11, 0-2), a gap of clear sky between
  it and the head so it never reads as an ear.
Colours are the owner-accepted pixxispad item icon's (textures/item/pixxispad.png, art/src/fish_pixxispad_icon.py
PAL), same keys, nothing new; the water where the fish goes under is the cerna bucket's own shades.
Photos (reference only): art/references/fish_pixxispad_refonly/ (list.tsv).

Writes: mod/src/main/resources/assets/mimcontent/textures/item/pixxispad_bucket.png (byte-identical on rerun)
With --sheet it also writes the review sheet art/candidates/fish_pixxispad_bucket.png (references, what players see,
i.e. this layer over vanilla's cod_bucket, at 8x and 1x beside vanilla's fish buckets and the accepted cerna, awrata
and murina buckets, the layer alone, the accepted pixxispad item, measure.py numbers, and offline hotbar previews at
GUI scale 2 and 4).
Run:    art/.venv/bin/python art/src/fish_pixxispad_bucket.py [--sheet]
"""
import os
import subprocess

from PIL import Image

from fish_bucket_rim import check_rim

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item",
                   "pixxispad_bucket.png")


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = {
    # water where the fish goes under: the accepted cerna bucket's shades
    "~": hx("#2a55c4"),
    "#": hx("#383838"),  # the bucket's back-rim outline where we cover a cod pixel: our own grey (vanilla's is #353535)
    "v": hx("#1d3c96"),  # the shadow on the water beside the fish
    "^": hx("#6a92ea"),  # a glint of light on the water
    # the pixxispad: the owner-accepted item icon's palette (art/src/fish_pixxispad_icon.py PAL), same keys
    "S": hx("#c4b4a4"), "u": hx("#6e5c5c"),   # sword: lit top, shaded underside at its base
    "H": hx("#8a7072"), "h": hx("#7a6266"), "1": hx("#664c5c"), "2": hx("#4a3442"),  # purple-bronze back, lit to dark
    "3": hx("#8c7876"), "4": hx("#a69896"), "5": hx("#ccc2ba"),  # bronze-silver cheek, silver, pale throat
    "g": hx("#7a6e72"), "G": hx("#54484f"),   # the throat and back in shade (lower right)
    "e": hx("#0a080c"),                       # the eye (the only black)
    "j": hx("#7a6670"),                       # short pointed lower jaw
    "D": hx("#8a7480"), "d": hx("#5a4450"),   # dorsal fin: lit leading edge, membrane
}

# rows 0-15, columns 0-15; "." is clear
GRID = [
    "S..........D....",
    ".S..hHH1..Dd....",
    "..ShHe11222d....",
    "..uS443122G#....",
    "...j5543Gv~~~...",
    "....G4gGv^~~....",
] + ["................"] * 10

# Shapes tried on the way and dropped (sheet only): the dorsal right behind the head read as an ear.
TRIED = {
    "tried: dorsal at head": [
        "S.........D.....",
        ".S..hHH1.Dd.....",
        "..ShHe112Dd.....",
        "..uS4431222~....",
        "...j5543Gv~~~...",
        "....G4gGv^~~....",
    ] + ["................"] * 10,
    "tried: block dorsal": [
        "S..........D....",
        ".S..hHH1..Dd....",
        "..ShHe1122Dd....",
        "..uS443122G~....",
        "...j5543Gv~~~...",
        "....G4gGv^~~....",
    ] + ["................"] * 10,
}


# The back-rim outline pixels (art/src/fish_bucket_rim.py) that the head, its back and its sword cover; every other one stays dark
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


ART = os.path.join(ROOT, "art")
VANILLA = os.path.join(ART, ".vanilla", "item")
ITEMS = os.path.dirname(OUT)
REFS = os.path.join(ART, "references", "fish_pixxispad_refonly")
SHEET = os.path.join(ART, "candidates", "fish_pixxispad_bucket.png")
SLOT = (139, 139, 139, 255)


def hotbars():
    """Offline hotbar previews (art/tools/hotbar_preview.py) at GUI scale 2 and 4."""
    py = os.path.join(ART, ".venv", "bin", "python")
    tool = os.path.join(ART, "tools", "hotbar_preview.py")
    outs = []
    for suffix, scale in (("", "2"), ("_x4", "4")):
        out = os.path.join(ART, "candidates", f"fish_pixxispad_bucket_hotbar{suffix}.png")
        subprocess.run([py, tool, out, "mc:cod_bucket", "mc:pufferfish_bucket", "bucket:cerna_bucket",
                        "bucket:awrata_bucket", "bucket:murina_bucket", "bucket:pixxispad_bucket", "mod:pixxispad",
                        "--select", "5", "--scale", scale],
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
    W = 1900
    parts = []

    def text(lines, f=font, h=None):
        h = h or (len(lines) * (f.size + 6) + 6)
        im = Image.new("RGBA", (W, h), (255, 255, 255, 255))
        d = ImageDraw.Draw(im)
        for i, ln in enumerate(lines):
            d.text((10, 4 + i * (f.size + 6)), ln, fill=(0, 0, 0), font=f)
        return im

    parts.append(text(["Bucket of pixxispad (16 x 16): references, the fish out of water for true colour "
                       "(art/references/fish_pixxispad_refonly, reference only)"]))
    row = Image.new("RGBA", (W, 190), (255, 255, 255, 255))
    x = 10
    for f in ("sw09_2.jpg", "sw01_market.jpg", "sw02_essaouira.jpg", "sw04_drawing.jpg"):
        p = os.path.join(REFS, f)
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGBA")
        im.thumbnail((420, 180))
        row.alpha_composite(im, (x, 5))
        x += im.width + 10
    parts.append(row)

    ours = composite(Image.open(OUT).convert("RGBA"))
    icons = [("cod", Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")),
             ("salmon", Image.open(os.path.join(VANILLA, "salmon_bucket.png")).convert("RGBA")),
             ("tropical fish", Image.open(os.path.join(VANILLA, "tropical_fish_bucket.png")).convert("RGBA")),
             ("pufferfish", Image.open(os.path.join(VANILLA, "pufferfish_bucket.png")).convert("RGBA"))]
    icons += [(f"{n} bucket", composite(Image.open(os.path.join(ITEMS, f"{n}_bucket.png")).convert("RGBA")))
              for n in ("cerna", "awrata", "murina")]
    icons += [("PIXXISPAD (in game)", ours),
              ("our layer alone", Image.open(OUT).convert("RGBA")),
              ("pixxispad item", Image.open(os.path.join(ITEMS, "pixxispad.png")).convert("RGBA"))]
    tried = [(n, composite(build(g))) for n, g in TRIED.items()]
    parts.append(text(["8x on the slot grey: vanilla cod, salmon, tropical fish, pufferfish | accepted cerna, awrata, "
                       "murina buckets | PIXXISPAD (over cod_bucket) | layer alone | accepted pixxispad item | "
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
            row.alpha_composite(im.resize((32, 32), Image.NEAREST), (240 + i * 40, y0 + 9))
    parts.append(row)

    lines = ["art/tools/measure.py (whole composite as players see it):"]
    tmp = os.path.join(os.path.dirname(SHEET), "fish_pixxispad_bucket_measure.tmp.png")
    for n, im in icons[:8]:
        im.save(tmp)
        m = measure(tmp)
        lines.append(f"  {n:20s} coverage {m['coverage']:.2f}  colours {m['colours']:2d}  darkest {float(m['lmin']):.2f}"
                     f"  lightest {float(m['lmax']):.2f}  outline {float(m['edge_l']):.2f}  inside {float(m['interior_l']):.2f}"
                     f"  top-left minus bottom-right {float(m['tl_minus_br']):+.2f}")
    os.remove(tmp)
    parts.append(text(lines, small))

    parts.append(text(["Hotbar preview (art/tools/hotbar_preview.py, offline, as the game draws flat items) at GUI scale 2 "
                       "and 4: vanilla cod and pufferfish buckets, cerna, awrata, murina buckets, PIXXISPAD BUCKET "
                       "(selected), pixxispad item"]))
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
