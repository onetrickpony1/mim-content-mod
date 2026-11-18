"""Bucket of skorfna (scorpionfish): the fish layer of the item icon (16 x 16), black and red, 2026-11-18.

The bucket is not ours: the item models (models/item/skorfna_bucket.json, skorfna_red_bucket.json) put the player's
own vanilla minecraft:item/cod_bucket underneath as layer0 and this texture on top as layer1, so the mod ships no
Mojang pixels (STYLE rule 3) and the bucket matches whatever resource pack the player uses. Rows 6-15 are clear, and
in rows 0-5 every opaque pixel of the cod in cod_bucket is covered so no cod shows through (check_cover() on every
run, against art/.vanilla's cod_bucket when it is there). The back-rim outline is checked by
art/src/fish_bucket_rim.py (owner 2026-11-18, keep the back outline). Same method and water shades as the
owner-accepted cerna, boll and other buckets.

One bucket item, two pictures (owner 2026-11-18, "Skorfna icon D accepted; each colour drops its own item"): the
bucket keeps which version is inside (SkorfnaFish.saveToBucketTag, Variant "black" or "red"), and the item definition
items/skorfna_bucket.json picks the picture by it (a minecraft:select on the client property
mimcontent:bucket_variant, client/BucketVariantProperty.java): skorfna_bucket.png (black, the fallback) or
skorfna_red_bucket.png (red). Both are the same pixels, the black and red palettes of the accepted icon, as the icon's
own red item is.

Owner rule: a bucket shows the fish's head rising out of the water, the vanilla way, never the tail or the whole fish
(docs/Decisions/2026-11-18 Cerna bucket - head showing, not the whole fish.md). For the skorfna that head is the
whole point: big, as wide as the bucket's mouth, with
- the wide, downturned mouth: a dark gape running back and down from the lip, over a pale jutting chin;
- one eye high on the head, with only light or mid tones round it (no dark pixel in its 3 x 3 or in its row near it,
  the no-second-eye rule);
- the frilly skin flaps: pale tassels on the brow over the eye and dangling under the chin (the photos' cirri), kept
  in the icon's light tones, never dark (a dark flap over the eye read as a second eye on the model);
- behind the head, the first dorsal spines standing up out of the water with dark tips, the venomous spines that make
  it a scorpionfish; the rest of the fish is under water.

Colours are the owner-accepted icon's (art/src/fish_skorfna_icon.py palette(): the approved model's palette before
its water lift, same keys), nothing new: 0 pale belly, J chin, h lit rim, 1 2 3 4 mid to dark, B dark saddle, R
red-brown, E eye, M gape, L lip, S spine tips, D dark spine, F membrane, f shaded membrane, W chin flaps. The water and the
rim tone are the shared bucket shades (art/src/fish_bucket_rim.py).
Candidates A and C (long, flat-topped heads) and D (a taller, blunter head); critic round 1 picked D (PASS with
fixes), applied as D2, the pick; critic round 2 on D2: PASS, no fixes. Blind reads of D2 (no context, alone in a
hotbar): black "Bucket of Scorpionfish", "Bucket of Scorpionfish (a bucket of a brown, spiny fish)"; red "Bucket of
Scorpionfish". In game (SMOKE_ONLY=skorfna-bucket, SkorfnaBucketCheck) a bucket holding a red skorfna draws the red
picture and one holding a black skorfna, or none saved, the black.
References (photos, reference only): art/references/fish_skorfna_refonly/ (list.tsv), the head shots above all.

Writes: mod/src/main/resources/assets/mimcontent/textures/item/skorfna_bucket.png and skorfna_red_bucket.png (the
PICK, byte-identical on rerun). With --sheet it also writes the review sheet art/candidates/fish_skorfna_bucket.png
(the candidates as players see them, this layer over vanilla's cod_bucket, black and red, at 8x, 2x and 1x beside
vanilla's cod and pufferfish buckets and the accepted boll, cerna and lampuka buckets; the layers alone; measure.py
numbers) and the offline hotbar previews art/candidates/fish_skorfna_bucket_hotbar.png and
fish_skorfna_bucket_hotbar_x4.png (GUI scale 2 and 4, nothing selected).
Run:    art/.venv/bin/python art/src/fish_skorfna_bucket.py [--sheet]
"""
import os
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fish_bucket_rim import RIM, check_rim, _dark as rim_dark  # noqa: E402
from fish_skorfna_icon import PAL as ICON, PAL_RED as ICON_RED  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
ART = os.path.join(ROOT, "art")
ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
OUT = {"black": os.path.join(ITEMS, "skorfna_bucket.png"), "red": os.path.join(ITEMS, "skorfna_red_bucket.png")}


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


WATER = {
    # water: the shared shades of the accepted buckets (art/src/fish_bucket_rim.py WATER)
    "~": hx("#2a55c4"),
    "v": hx("#1d3c96"),  # shadow on the water beside the fish where it goes under
    "^": hx("#6a92ea"),  # a glint of light on the water
    "#": RIM,            # the bucket's back-rim outline where we cover a cod pixel (vanilla's is #353535)
}
KEYS = "0JhC12345BREMLSDFfrW"


def palette(icon):
    p = dict(WATER)
    p.update({k: icon[k] for k in KEYS})
    return p


PALS = {"black": palette(ICON), "red": palette(ICON_RED)}

EMPTY = ["................"] * 10

# rows 0-5, columns 0-15; "." is clear (vanilla cod_bucket's own outline or water shows there)
CANDIDATES = {
    # A: the head at the left of the mouth, as vanilla's fish rise, lit from the top left with a darker edge (3) along
    # its front so it stands off the slot grey. The scorpionfish's wide mouth runs right across the face: the upper lip
    # lit (row 3), the dark gape M along row 4 from the lip L (1,4) back to 5,4, its corner turning down at 6,5
    # (downturned), the pale chin J under it with a skin flap W hanging at 2,5. The eye (5,2) sits high with only lit or
    # mid tones round it, a pale brow flap C over it (5,1). Behind the head two dorsal spines with dark tips S stand out
    # of the water (8,0 10,0), joined by membrane F f; the last spine D (11,1) and the back slope into the water (11,3).
    # A red-brown blotch R and a dark saddle B on the flank, away from the eye.
    "A": [
        "........S.S.....",
        "...3hC1DFDFS....",
        "..3hhE12FfFD....",
        ".31h1h2R23B#....",
        ".LMMMM23v~~~~...",
        "..WJJ0Mv^~~~~...",
    ] + EMPTY,
    # C: A, frillier: the brow flap stands a pixel proud of the head (5,0), a flap on the snout (1,2), a pale cheek
    # blotch (6,3), and tassels hanging from the chin (1,5 and 4,5 pale W) as in the head photos.
    "C": [
        ".....C..S.S.....",
        "...3hC1DFDFS....",
        ".C3hhE12FfFD....",
        ".31h1hC2R3B#....",
        ".LMMMM23v~~~~...",
        ".WWJW0Mv^~~~~...",
    ] + EMPTY,
    # D: a taller, rounder head that rises higher out of the water (its crown at row 0, 4-6), so it reads blunt and
    # deep, not long-snouted: the eye at 6,2, the brow flap C on the crown (6,0), a shorter gape M (2-4,4) turning down
    # at 5,5 over the chin J and its flap W; two spines with dark tips (8,0 10,0) and a third, low, at 12,1 before the
    # back sinks (11-12,3).
    "D": [
        "....3hC.S.S.....",
        "...3hhh1DFDFS...",
        "..3h1hE2FfFfD...",
        ".31hh1h2R3B3#...",
        ".LMMM12R3v~~~...",
        "..WJJM3v^~~~~...",
    ] + EMPTY,
    # D2, the pick: critic round 1's fixes for D (PASS with fixes): the light runs from the lit crown down to a mid
    # cheek (4,2 h, 4,3 1) instead of a darker pixel over a lighter one; the chin tassel is the pale 0 (2,5), since in
    # the black palette W is the chin's own colour and the flap vanished; the dark saddle B at 10,3, nearly as dark as
    # the eye beside the rim, read as a spot behind the eye at 1x, so it is mid 3.
    "D2": [
        "....3hC.S.S.....",
        "...3hhh1DFDFS...",
        "..3hhhE2FfFfD...",
        ".31h11h2R333#...",
        ".LMMM12R3v~~~...",
        "..0JJM3v^~~~~...",
    ] + EMPTY,
}
PICK = "D2"

# The back-rim outline pixels (art/src/fish_bucket_rim.py) that each candidate's fish covers; every other one stays
# dark. A covered pixel whose colour is itself outline-dark (the black skorfna's eye, #0c0908) keeps the outline and is
# left out of the list for that palette (fish_over() below).
FISH_OVER_RIM = {
    "A": [(5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (3, 3), (4, 3), (2, 4), (2, 5)],
    "C": [(5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (3, 3), (4, 3), (2, 4), (2, 5)],
    "D": [(5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (3, 3), (4, 3), (11, 3), (2, 4), (2, 5)],
    "D2": [(5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (3, 3), (4, 3), (11, 3), (2, 4), (2, 5)],
}


def fish_over(name, layer):
    return [p for p in FISH_OVER_RIM[name] if not rim_dark(layer.getpixel(p))]


def build(grid, variant="black"):
    pal = PALS[variant]
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(grid):
        assert len(row) == 16, (y, len(row))
        for x, ch in enumerate(row):
            if ch != ".":
                px[x, y] = pal[ch] + (255,)
    return img


VANILLA = os.path.join(ART, ".vanilla", "item")
CAND = os.path.join(ART, "candidates")
SHEET = os.path.join(CAND, "fish_skorfna_bucket.png")
SLOT = (139, 139, 139, 255)


def composite(layer):
    """What players see: our layer over vanilla's cod bucket (review only; vanilla is never written out)."""
    base = Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")
    base.alpha_composite(layer)
    return base


def check_eye(name, grid):
    """The no-second-eye rule: one eye, nothing dark in its 3 x 3 or within 4 px in its row."""
    dark = set("EBSMD#vo")
    eyes = [(x, y) for y, r in enumerate(grid) for x, c in enumerate(r) if c == "E"]
    assert len(eyes) == 1, (name, eyes)
    ex, ey = eyes[0]
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            c = grid[ey + dy][ex + dx]
            assert not ((dx or dy) and c in dark), f"{name}: dark {c} beside the eye at {ex + dx},{ey + dy}"
    for x, c in enumerate(grid[ey]):
        assert not (c in dark and c != "E" and abs(x - ex) <= 4), f"{name}: dark {c} in the eye's row at {x},{ey}"


def check_cover(layer):
    """No cod may show through; rows 6-15 must be clear; no pixel may equal vanilla's at the same place."""
    cod = os.path.join(VANILLA, "cod_bucket.png")
    for y in range(6, 16):
        assert all(layer.getpixel((x, y))[3] == 0 for x in range(16)), f"row {y} not clear"
    if not os.path.exists(cod):
        print("note: art/.vanilla missing, cover not checked")
        return 0
    base = Image.open(cod).convert("RGBA")
    fishy = [(x, y) for y in range(6) for x in range(16)
             if base.getpixel((x, y))[3] and base.getpixel((x, y))[:3] not in ((0x35, 0x35, 0x35), (0x23, 0x4f, 0xcc))]
    shows = [p for p in fishy if layer.getpixel(p)[3] == 0]
    assert not shows, f"cod shows through at {shows}"
    same = []
    for n in ("cod_bucket", "salmon_bucket", "tropical_fish_bucket", "pufferfish_bucket", "axolotl_bucket",
              "tadpole_bucket", "water_bucket", "bucket"):
        p = os.path.join(VANILLA, n + ".png")
        if not os.path.exists(p):
            continue
        v = Image.open(p).convert("RGBA")
        same += [(n, x, y) for y in range(16) for x in range(16)
                 if layer.getpixel((x, y))[3] and layer.getpixel((x, y)) == v.getpixel((x, y))]
    assert not same, f"pixels identical to vanilla: {same}"
    return len(fishy)


def hotbars():
    """Offline hotbar previews (art/tools/hotbar_preview.py) at GUI scale 2 and 4, nothing selected."""
    py = os.path.join(ART, ".venv", "bin", "python")
    tool = os.path.join(ART, "tools", "hotbar_preview.py")
    outs = []
    for suffix, scale in (("", "2"), ("_x4", "4")):
        out = os.path.join(CAND, f"fish_skorfna_bucket_hotbar{suffix}.png")
        subprocess.run([py, tool, out, "mc:cod_bucket", "bucket:skorfna_bucket", "mc:pufferfish_bucket",
                        "bucket:cerna_bucket", "bucket:skorfna_red_bucket", "mc:salmon_bucket", "bucket:boll_bucket",
                        "mod:skorfna", "bucket:lampuka_bucket", "--scale", scale],
                       check=True, capture_output=True)
        outs.append(out)
    return outs


def sheet():
    from PIL import ImageDraw
    sys.path.insert(0, os.path.join(ART, "tools"))
    from font import label_font
    from measure import measure

    font, small = label_font(16), label_font(13)
    W = 2300
    parts = []

    def text(lines, f=font):
        h = len(lines) * (f.size + 6) + 6
        im = Image.new("RGBA", (W, h), (255, 255, 255, 255))
        d = ImageDraw.Draw(im)
        for i, ln in enumerate(lines):
            d.text((10, 4 + i * (f.size + 6)), ln, fill=(0, 0, 0), font=f)
        return im

    def van(n):
        return Image.open(os.path.join(VANILLA, n + ".png")).convert("RGBA")

    def ours(n):
        return composite(Image.open(os.path.join(ITEMS, n + ".png")).convert("RGBA"))

    icons = [("skorfna icon", Image.open(os.path.join(ITEMS, "skorfna.png")).convert("RGBA")),
             ("red icon", Image.open(os.path.join(ITEMS, "skorfna_red.png")).convert("RGBA"))]
    designs = [(f"{n} {v}{' (PICK)' if n == PICK else ''}", composite(build(g, v)))
               for n, g in CANDIDATES.items() for v in ("black", "red")]
    layers = [(f"{n}: layer alone", build(g)) for n, g in CANDIDATES.items()]
    parts.append(text(["Bucket of skorfna (scorpionfish), 16 x 16: the candidates as players see them (our layer over "
                       "vanilla's cod_bucket), black and red, at 8x, the layers alone, and the accepted icons whose "
                       "palettes they use"]))
    allrow = designs + layers + icons
    per = 14
    for start in range(0, len(allrow), per):
        row = Image.new("RGBA", (W, 16 * 8 + 30), SLOT)
        d = ImageDraw.Draw(row)
        for i, (n, im) in enumerate(allrow[start:start + per]):
            row.alpha_composite(im.resize((128, 128), Image.NEAREST), (10 + i * 150, 4))
            d.text((10 + i * 150, 134), n, fill=(0, 0, 0), font=small)
        parts.append(row)

    compare = [("cod", van("cod_bucket")), ("pufferfish", van("pufferfish_bucket")),
               ("salmon", van("salmon_bucket")),
               ("boll (ours)", ours("boll_bucket")), ("cerna (ours)", ours("cerna_bucket")),
               ("lampuka (ours)", ours("lampuka_bucket"))] + icons + designs
    parts.append(text(["Beside vanilla's cod, pufferfish and salmon buckets, the accepted boll, cerna and lampuka "
                       "buckets and the skorfna icons: 8x"]))
    per = 17
    for start in range(0, len(compare), per):
        row = Image.new("RGBA", (W, 16 * 8 + 30), SLOT)
        d = ImageDraw.Draw(row)
        for i, (n, im) in enumerate(compare[start:start + per]):
            x = 10 + i * 124
            row.alpha_composite(im.resize((112, 112), Image.NEAREST), (x, 4))
            d.text((x, 120), n, fill=(0, 0, 0), font=small)
        parts.append(row)
    parts.append(text(["The same at 2x and 1x, on the slot grey and on dark"]))
    row = Image.new("RGBA", (W, 100), SLOT)
    ImageDraw.Draw(row).rectangle((0, 50, W, 100), fill=(40, 40, 40))
    for i, (n, im) in enumerate(compare):
        for y0 in (0, 50):
            row.alpha_composite(im.resize((32, 32), Image.NEAREST), (10 + i * 40, y0 + 9))
            row.alpha_composite(im, (1200 + i * 22, y0 + 17))
    parts.append(row)

    lines = ["art/tools/measure.py (whole composite as players see it):"]
    tmp = os.path.join(CAND, "fish_skorfna_bucket_measure.tmp.png")
    for n, im in compare:
        im.save(tmp)
        m = measure(tmp)
        lines.append(f"  {n:24s} coverage {m['coverage']:.2f}  colours {m['colours']:2d}  darkest {float(m['lmin']):.2f}"
                     f"  lightest {float(m['lmax']):.2f}  outline {float(m['edge_l']):.2f}  inside "
                     f"{float(m['interior_l']):.2f}  top-left minus bottom-right {float(m['tl_minus_br']):+.2f}")
    os.remove(tmp)
    parts.append(text(lines, small))

    parts.append(text(["Hotbar preview (art/tools/hotbar_preview.py, offline, as the game draws flat items) at GUI scale "
                       "2 and 4, nothing selected: cod bucket, SKORFNA BUCKET (black), pufferfish bucket, cerna bucket, "
                       "SKORFNA BUCKET (red), salmon bucket, boll bucket, skorfna icon, lampuka bucket"]))
    for p in hotbars():
        hb = Image.open(p).convert("RGBA")
        row = Image.new("RGBA", (max(W, hb.width + 20), hb.height + 10), (255, 255, 255, 255))
        row.alpha_composite(hb, (10, 5))
        parts.append(row)

    width = max(p.width for p in parts)
    out = Image.new("RGBA", (width, sum(p.height for p in parts)), (255, 255, 255, 255))
    y = 0
    for p in parts:
        out.alpha_composite(p, (0, y))
        y += p.height
    os.makedirs(CAND, exist_ok=True)
    out.convert("RGB").save(SHEET)
    print("wrote", os.path.relpath(SHEET, ROOT))


if __name__ == "__main__":
    n = 0
    for name, g in CANDIDATES.items():
        check_eye(name, g)
        for v in PALS:
            lay = build(g, v)
            n = check_cover(lay)
            check_rim(lay, os.path.join(VANILLA, "cod_bucket.png"), fish_over(name, lay))
    print(f"cover ok: all {n} cod pixels covered, 0 pixels identical to vanilla (all candidates, black and red)")
    for v, path in OUT.items():
        build(CANDIDATES[PICK], v).save(path, optimize=False)
        print("wrote", os.path.relpath(path, ROOT), f"(candidate {PICK}, {v})")
    if "--sheet" in sys.argv[1:]:
        sheet()
