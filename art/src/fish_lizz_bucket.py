"""Bucket of lizz (European barracuda, Sphyraena sphyraena): the fish layer of the item icon (16 x 16), night job 2026-11-18.

Layered like every fish bucket: the item model puts the player's own vanilla minecraft:item/cod_bucket underneath as
layer0 and this texture on top, so the mod ships no Mojang pixels (STYLE rule 3). This file is ONLY the fish, the
bucket's back outline where we cover a cod pixel, and our own water: rows 6-15 are clear, every cod pixel in rows 0-5
is covered (check_cover()) and the back-rim outline stays dark except where the head sits in front of it
(check_rim() in art/src/fish_bucket_rim.py). Same method as the accepted incova bucket (fish_incova_bucket.py).

The owner's bucket rules: only the head and the front of the body rise out of the water, never the tail; the back of
the rim stays visible.

The lizz is told apart at 1x by:
- a long, low, pointed head facing left, the lower jaw (J) jutting one pixel past the upper snout, a grey mouth line
  (M) between them, no teeth;
- one black eye with only silver round it (no dark or white pixel below it);
- the dark slate back (B, lit edge h) over silver (S, s) and a white belly (W) diving to the lower right into the
  water, the bars of the icon as one darker back pixel (b).
Colours are the night-accepted lizz item icon's (art/src/fish_lizz_icon.py PAL), same keys; the water is the shared
shades of the other buckets.
Photos (reference only): art/references/fish_lizz_refonly/ (list.tsv).

Candidates: A (the head level, the jaw poking just out of the bucket mouth at the left), B (the head tilted up, the
snout pointing up and left). The installed one is CHOSEN.

Writes: mod/src/main/resources/assets/mimcontent/textures/item/lizz_bucket.png (byte-identical on rerun)
With --sheet also the review sheet art/candidates/fish_lizz_bucket.png and the unselected hotbar previews
art/candidates/fish_lizz_bucket_hotbar_<cand>.png.
Run:    art/.venv/bin/python art/src/fish_lizz_bucket.py [--sheet]
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fish_bucket_rim import OUTLINE, RIM, check_rim  # noqa: E402
from fish_lizz_icon import PAL as ICON  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
ART = os.path.join(ROOT, "art")
ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
OUT = os.path.join(ITEMS, "lizz_bucket.png")
VANILLA = os.path.join(ART, ".vanilla", "item")
PY = os.path.join(ART, ".venv", "bin", "python")
CHOSEN = "A"


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = {
    "~": hx("#2a55c4"),  # water: the shared shades of the accepted buckets
    "v": hx("#1d3c96"),  # shadow on the water beside the fish where it goes under
    "^": hx("#6a92ea"),  # a glint of light on the water
    "#": RIM,            # the back-rim outline where we cover a cod pixel
}
PAL.update({k: ICON[k] for k in "hBbSgWsoeMJ"})
PAL["q"] = hx("#8a979c")  # the mid-grey belly rim against the water (round 2: lighter than the back)

# rows 0-5; "." is clear (cod_bucket's own outline or water shows there)
GRIDS = {
    # A (round 2; critic round 1: the dark back didn't read, the pale crown made a knob): the crown dark slate B B B b
    # on row 0, running on as the back; the upper snout h B on row 1 ending at 2,1, the eye 5,1 between silver S; the
    # lower jaw juts to 0,2 as a silver point (J tip, S S, no dark mouth slit under the eye); behind the gill the body
    # dives to the lower right: dark slate back B and b along the top, silver S, the white belly W and s, and a mid-grey
    # rim q against the water, so the back is the darkest part of the fish.
    "A": [
        "....BBBb........",
        "..hBSeSbB.......",
        "JSSsSSsBB##.....",
        "...#qsWSbBv#....",
        "...~~vqsSbBv~...",
        "....~^~qsSbB....",
    ],
    # B: the head tilted up out of the water, the snout pointing up and left from the bucket's far rim
    "B": [
        "..hBBhh.........",
        ".JMSeSBh........",
        "...sSWsBh##.....",
        "...#osWSbhv#....",
        "...~~vosWBhv~...",
        "....~^~osWBh....",
    ],
}
# The back-rim outline pixels the head covers; every other one stays dark
FISH_OVER_RIM = {"A": [(5, 2), (6, 2), (7, 2), (8, 2), (4, 3)], "B": [(5, 2), (6, 2), (7, 2), (8, 2), (4, 3)]}


def build(cand):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(GRIDS[cand]):
        assert len(row) == 16, (cand, y, len(row))
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


def sheet(layers):
    sys.path.insert(0, os.path.join(ART, "tools"))
    from font import label_font
    from measure import measure
    font, small = label_font(16), label_font(13)
    W = 1500
    parts = []

    def text(lines, f=font):
        im = Image.new("RGBA", (W, len(lines) * (f.size + 6) + 6), (255, 255, 255, 255))
        d = ImageDraw.Draw(im)
        for i, ln in enumerate(lines):
            d.text((10, 4 + i * (f.size + 6)), ln, fill=(0, 0, 0), font=f)
        return im

    def ours_of(n):
        return composite(Image.open(os.path.join(ITEMS, n + ".png")).convert("RGBA"))

    icons = [("cod bucket", Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")),
             ("salmon bucket", Image.open(os.path.join(VANILLA, "salmon_bucket.png")).convert("RGBA")),
             ("incova (accepted)", ours_of("incova_bucket")), ("pixxispad (accepted)", ours_of("pixxispad_bucket"))]
    icons += [("cand %s%s" % (c, " (installed)" if c == CHOSEN else ""), composite(l)) for c, l in layers.items()]
    icons += [("lizz item", Image.open(os.path.join(ITEMS, "lizz.png")).convert("RGBA"))]
    parts.append(text(["Bucket of lizz: 8x on the slot grey beside vanilla and accepted buckets, the candidates over "
                       "cod_bucket, and the lizz item"], small))
    row = Image.new("RGBA", (W, 16 * 8 + 30), (139, 139, 139, 255))
    d = ImageDraw.Draw(row)
    for i, (n, im) in enumerate(icons):
        row.alpha_composite(im.resize((128, 128), Image.NEAREST), (10 + i * 150, 4))
        d.text((10 + i * 150, 134), n, fill=(0, 0, 0), font=small)
    parts.append(row)
    for bg in ((139, 139, 139, 255), (40, 40, 40, 255)):
        row = Image.new("RGBA", (W, 50), bg)
        for i, (n, im) in enumerate(icons):
            row.alpha_composite(im, (10 + i * 22, 17))
            row.alpha_composite(im.resize((32, 32), Image.NEAREST), (230 + i * 40, 9))
        parts.append(row)
    parts.append(text(["The back-rim outline of the installed one (red: stays dark; blue: behind the head)"], small))
    big = composite(layers[CHOSEN]).resize((128, 128), Image.NEAREST)
    d = ImageDraw.Draw(big)
    for (x, y) in OUTLINE:
        d.rectangle((x * 8, y * 8, x * 8 + 7, y * 8 + 7),
                    outline=(40, 80, 255) if (x, y) in FISH_OVER_RIM[CHOSEN] else (230, 30, 30))
    row = Image.new("RGBA", (W, 140), (139, 139, 139, 255))
    row.alpha_composite(big, (10, 6))
    parts.append(row)
    lines = ["art/tools/measure.py (whole bucket as players see it):"]
    tmp = os.path.join(ART, "candidates", "fish_lizz_bucket_measure.tmp.png")
    for n, im in icons[:-1]:
        im.save(tmp)
        m = measure(tmp)
        lines.append(f"  {n:22s} coverage {m['coverage']:.2f}  colours {m['colours']:2d}  darkest {float(m['lmin']):.2f}"
                     f"  lightest {float(m['lmax']):.2f}  top-left minus bottom-right {float(m['tl_minus_br']):+.2f}")
    os.remove(tmp)
    parts.append(text(lines, small))
    out = Image.new("RGBA", (W, sum(p.height for p in parts)), (255, 255, 255, 255))
    y = 0
    for p in parts:
        out.alpha_composite(p, (0, y))
        y += p.height
    dest = os.path.join(ART, "candidates", "fish_lizz_bucket.png")
    out.convert("RGB").save(dest)
    print("sheet:", dest)
    for c, l in layers.items():
        tmpf = os.path.join(ART, "candidates", "tmp_lizz_bucket_%s.png" % c)
        composite(l).save(tmpf)
        subprocess.run([PY, os.path.join(ART, "tools", "hotbar_preview.py"),
                        os.path.join(ART, "candidates", "fish_lizz_bucket_hotbar_%s.png" % c),
                        "mc:cod_bucket", "file:" + tmpf, "mc:salmon_bucket", "bucket:incova_bucket",
                        "bucket:pixxispad_bucket", "mc:tropical_fish_bucket", "--scale", "4"], check=True, capture_output=True)
        os.remove(tmpf)


if __name__ == "__main__":
    layers = {}
    for c in GRIDS:
        layer = build(c)
        print("candidate", c)
        check_cover(layer)
        check_rim(layer, os.path.join(VANILLA, "cod_bucket.png"), FISH_OVER_RIM[c])
        layers[c] = layer
    layers[CHOSEN].save(OUT, optimize=False)
    print("wrote", os.path.relpath(OUT, ROOT), "(candidate %s)" % CHOSEN)
    if "--sheet" in sys.argv[1:]:
        sheet(layers)
