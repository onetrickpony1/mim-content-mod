"""Bucket of boll (common stingray, Dasyatis pastinaca): the ray layer of the item icon (16 x 16), 2026-11-18.

The bucket is not ours: the item model (models/item/boll_bucket.json) puts the player's own vanilla
minecraft:item/cod_bucket underneath as layer0 and this texture on top as layer1, so the mod ships no Mojang
pixels (STYLE rule 3) and the bucket matches whatever resource pack the player uses. Rows 6-15 are clear, and in
rows 0-5 every opaque pixel of the cod in cod_bucket is covered so no cod shows through (check_cover() on every
run, against art/.vanilla's cod_bucket when it is there). The back-rim outline is checked by
art/src/fish_bucket_rim.py (owner 2026-11-18, keep the back outline). Same method and water shades as the
owner-accepted cerna, cawl, huta kahla and ziemel buckets.

Candidates T to G follow the first brief; N (the pick) follows the owner's later idea, see its grid.
Owner rule: a bucket shows the animal's head rising out of the water, the vanilla way, never the tail or the whole
animal (docs/Decisions/2026-11-18 Cerna bucket - head showing, not the whole fish.md). A ray's head is the front of
its disc, so every candidate shows the front of the disc and its spread wings breaking the surface, wing tips curled
up like the accepted icon's; the back of the disc and the whip tail stay under water.

Colours are the owner-accepted boll item icon's (textures/item/boll.png, candidate C of
art/src/fish_boll_icon_v5.py PAL), same keys, nothing new: o outline, L lit leading edges, H the light on the dome,
1 2 3 the olive-brown back from lit to shade. The water and the rim tone are the shared bucket shades
(art/src/fish_bucket_rim.py). No eyes, no spiracles, no mouth (the icon has none, and the no-face rule). The
exception is N, the owner's own idea: its cream underside tones (W w s) are new, and it shows the nostrils and mouth
the owner asked for, in the icon's 4 and 3; still no eyes.

Candidates (the sheet shows all three):
- T, tilted: the front of the disc rises at the upper left where vanilla's cod head is, its lit leading edge running
  down to the left past the bucket's side and curling up into the near wing tip (0-1, 4-5); the back slopes down
  to the right into the water, and the far wing tip curls up out of the water at the right rim (12-15, 3-5).
- V, wings spread: the ray seen head-on as in the icon, the near wing reaching out of the left side with its tip
  curled up (0, 0-2), the far wing rising to the top right (13-15, 0-3), the dome sinking into the water between.
- I2, the icon's top: the icon's own wings and dome as they sit in the icon (near tip 0-1, 3-5; far wing 12-15,
  0-4), with the snout end of the dome under the water and a 1 px stub where the front wing tip curls up (4, 0-1).
- W5: critic round 1's fix for V, the front half of the ray's diamond rising snout first, wing tips curled up past
  both sides, water under the disc (see the comment at its grid).
- G: critic round 2's fix for W5, the same snout and near wing, the far wing a low flap sloping into the
  water, and blue water in place of W5's dark band under the disc (see the comment at its grid).
Blind reads (one hotbar each, no context): T "a small greyish-brown fish ... not a stingray"; V "could be a
ray/skate"; I2 "a small brown/tan fish"; W5 (three readers) "a grey-blue/silvery fish", "a grey/silvery-blue
fish", "It looks like a ray or flatfish seen from above"; G (three readers) "a fish with a blue-grey/teal body ...
not clearly a stingray", "a bluish-grey fish with a lighter belly", "nothing about it reads as a stingray". W5 is
the best of these, but none read as a ray first.
- N: the owner's new idea after seeing those (2026-11-18): the ray poking up out of the bucket, its pale
  underside to the viewer, with its nostrils (and the mouth below them) near the bottom, just above the water. See
  the comment at its grid. The underside's cream tones are new (the icon shows only the back); the olive rim, the
  nostrils and the mouth use the icon's colours. Blind reads of N: "a white or cream, mushroom-shaped blob ...
  probably a jellyfish", "a white/cream mushroom-like or jellyfish-shaped blob", "a pale, whitish-cream fish or
  similar sea creature".
- N2: critic round 1's fix for N (see the comment at its grid). Blind reads: "a pale, cream/white fish (looks like
  a whitish fish with a darker eye and dark markings on top)", "a white or pale fish".
- N3, the pick: critic round 2's fix for N2 (see the comment at its grid).

Writes: mod/src/main/resources/assets/mimcontent/textures/item/boll_bucket.png (the PICK, byte-identical on rerun)
With --sheet it also writes the review sheet art/candidates/fish_boll_bucket.png (the candidates as players see them,
this layer over vanilla's cod_bucket, at 8x, 2x and 1x beside vanilla's fish buckets, the accepted cerna, cawl,
huta kahla and ziemel buckets and the boll icon; the layers alone; measure.py numbers) and the offline hotbar
previews art/candidates/fish_boll_bucket_hotbar.png and fish_boll_bucket_hotbar_x4.png (GUI scale 2 and 4, unselected).
Run:    art/.venv/bin/python art/src/fish_boll_bucket.py [--sheet]
"""
import os
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fish_bucket_rim import RIM, check_rim  # noqa: E402
from fish_boll_icon_v5 import PAL as ICON  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
ART = os.path.join(ROOT, "art")
ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
OUT = os.path.join(ITEMS, "boll_bucket.png")


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = {
    # water: the shared shades of the accepted buckets (art/src/fish_bucket_rim.py WATER)
    "~": hx("#2a55c4"),
    "v": hx("#1d3c96"),  # shadow on the water beside the ray where it goes under
    "^": hx("#6a92ea"),  # a glint of light on the water
    "#": RIM,            # the bucket's back-rim outline where we cover a cod pixel (vanilla's is #353535)
}
# the boll: the owner-accepted icon's palette (candidate C), same keys
PAL.update({k: ICON[k] for k in "oLH123"})
# candidate N (owner 2026-11-18): the pale underside, cream-white from lit to shade (a ray's belly is near white;
# new tones, since the icon shows only the back), and the nostrils and mouth in the icon's own darkest browns
# (critic round 1 on N: warmer than the first #ece4cc #d8ceb0 #bcb092, further from the bucket's greys; the sheet's
# N now shows these too)
PAL.update({"W": hx("#f2e6c8"), "w": hx("#dccaa2"), "s": hx("#b9a27c"), "n": ICON["4"], "m": ICON["3"]})

EMPTY = ["................"] * 10

# rows 0-5, columns 0-15; "." is clear (vanilla cod_bucket's own outline or water shows there)
CANDIDATES = {
    "T": [
        "....oo..........",
        "...oLHoo........",
        "..oLHHH1o#......",
        ".oLHHH112ov#.oo.",
        "oL1o1H123ov~oL2o",
        "oo.~o1123v~~o3o.",
    ] + EMPTY,
    "V": [
        "o.............oo",
        "oLoooooo.....oLo",
        "oL1LLHH1o#..oL2o",
        ".o11HHH11oooL12o",
        "..oo1H1112223oo.",
        "...~oo11223ov...",
    ] + EMPTY,
    "I2": [
        "...oLo.......oLo",
        "...oLoooo...oL2o",
        "...o1HH11oooL12o",
        "oo.o1HHH1123L1o.",
        "oLoo1H11122322o.",
        "ooLL1112v~~^vo..",
    ] + EMPTY,
    # W5: critic round 1's fix for V (V read as "a tan lump in a bucket with two horns", like the cod bucket: a flat
    # band filling the mouth, 2 px of water, an outline line through the body). The front of the disc rises to a
    # pointed snout (4-6, 0-1) with straight wing edges falling to both sides, the front half of the ray's diamond;
    # lit edge L down the left, the light H on the dome at 3-6 shading 1 2 3 to the lower right, the far wing's top
    # edge lit; both tips curl up past the bucket's sides (0,1) and (15,0), each split from the body by a 1 px notch
    # (2,2) and (13,3); the disc's lower edge ends at row 4 with water under it (row 4 x11-12, row 5 x8-12).
    "W5": [
        "....ooo........o",
        "o..oLHH1o.....oL",
        "oLoLHHH112o..oL2",
        "oLLHH1112223oL2o",
        ".oo11223ooov~oo.",
        "...ooooo~~^~v...",
    ] + EMPTY,
    # G: critic round 2's fix for W5 (W5 read as "a grey/silvery fish": the tall far tip at 12-15, 0-3 looked like a
    # raised tail fin, and the dark band under the disc, row 4 x8-10 and row 5 x3-7, greyed the ray at 1x). W5's
    # snout, lit edge, dome and near wing tip (rows 0-3, left) are kept; the far wing is a low, wide flap sloping into
    # the water, its lit leading edge LL at row 4 x10-11 and its tip curling up only 1-2 px at x15, rows 2-4; the
    # dark band is water now, shadow v where the disc goes under and a glint ^, so the tan ray sits on blue.
    "G": [
        "....ooo.........",
        "o..oLHH1o.......",
        "oLoLHHH112oo...o",
        "oLLHH1112223oooL",
        ".oo1122vv3LL22o2",
        "...~vvv~~v~^~oo.",
    ] + EMPTY,
    # N, the owner's idea (2026-11-18): "have it instead be the stingray poking out of the top with its nostrils (at
    # the bottom of it) visible". The ray stands up out of the bucket, snout up, its pale underside to the viewer: a
    # rounded snout (7-8, 0), the disc widening down to the wing edges spreading past both sides of the bucket (0 and
    # 15, rows 3-4), with a thin olive rim of the back (1 2, the icon's) along the top edges. Lit cream W at the upper
    # left shading through w to s at the lower right. Near the bottom, just above the water: the pair of nostrils
    # (n at 5,4 and 8,4) and the mouth line under them (m, 6-8,5). The rest of the ray is under water. No eyes.
    "N": [
        ".......oo.......",
        "....oo1WW1oo....",
        "..oo2WWWWWwsoo..",
        ".o2WWWWWWWwwsw2o",
        "o2wWWnwWnwwsss2o",
        "...osWmmmwsso...",
    ] + EMPTY,
    # N2, the pick: critic round 1's fix for N (N read as "a mushroom-shaped blob" or a jellyfish: a flat-topped cap
    # over a narrow stem, 1 px nostrils lost at 1x, a cool cream close to the bucket's greys). The wing tips now rise
    # at both ends (0-1 and 14-15, rows 1-3), cut off from the shoulders by a notch at (2,2) and (13,2), so the top
    # edge is an upturned ray shape, not a cap; the tips and shoulders carry the icon's olive back (1 2); the
    # nostrils are 2 px tall (n at x6 and x9, rows 3-4) with the mouth (m, 7-8,5) just under them above the water;
    # lit W at the upper left, w, then s at the lower right; water at (3,5) and (12,5) where the body goes under.
    "N2": [
        ".......oo.......",
        "oo..oo1WW1o...oo",
        "o1.o2WWWWWw2o.2o",
        "oWWWWWnWWnwwwsso",
        ".osWWWnwwnwwsso.",
        "...~oswmmwso~...",
    ] + EMPTY,
    # N3, the pick: critic round 2's fix for N2 (N2 read as "a whitish fish with a darker eye": the raised tips read as
    # horns or ears, the nostrils 3 px apart as one fish's eye, and too little olive let the cream merge into the
    # bucket). No raised tips: a straight wedge from the snout (7-8, 0) to pointed wing tips at x0 and x15, rows 3-4,
    # the front half of the ray's diamond; the icon's olive back (1 2, lit L at 8,1) along both sloping top edges,
    # rows 1-3, a dark edge between the cream and the bucket; the nostrils wide apart (n at x5 and x10, rows 3-4) over
    # a wide mouth slit (m, 6-9,5, s corners) on the waterline, the ray's "face"; shadow v and water ~ at both ends
    # of row 5 where the body goes under.
    "N3": [
        ".......oo.......",
        "....oo12L1oo....",
        ".oo21WWWWWW12oo.",
        "o21WWnWWWWnWw12o",
        "ossWwnwwwwnwwsso",
        "...~vsmmmmsv~...",
    ] + EMPTY,
    # N without the mouth line (sheet only): the nostrils alone
    "N-nomouth": [
        ".......oo.......",
        "....oo1WW1oo....",
        "..oo2WWWWWwsoo..",
        ".o2WWWWWWWwwsw2o",
        "o2wWWnwWnwwsss2o",
        "...oswwwwwsso...",
    ] + EMPTY,
}
PICK = "N2"  # owner 2026-11-18: "actually do n2"

# The back-rim outline pixels (art/src/fish_bucket_rim.py) that each candidate's ray covers; every other one stays dark
FISH_OVER_RIM = {
    "T": [(5, 2), (6, 2), (7, 2), (8, 2), (3, 3), (4, 3), (2, 4), (13, 4), (13, 5)],
    "V": [(5, 2), (6, 2), (7, 2), (8, 2), (3, 3), (4, 3), (11, 3), (12, 3), (2, 4), (13, 4)],
    "I2": [(5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (3, 3), (4, 3), (11, 3), (12, 3), (2, 4), (13, 4),
           (2, 5), (13, 5)],
    "W5": [(5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (3, 3), (4, 3), (11, 3), (12, 3), (2, 4), (13, 4)],
    "N": [(5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (3, 3), (4, 3), (11, 3), (12, 3), (2, 4), (13, 4)],
    "N2": [(5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (3, 3), (4, 3), (11, 3), (12, 3), (2, 4), (13, 4)],
    "N3": [(5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (3, 3), (4, 3), (11, 3), (12, 3), (2, 4), (13, 4)],
    "N-nomouth": [(5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (3, 3), (4, 3), (11, 3), (12, 3), (2, 4), (13, 4)],
    "G": [(5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (3, 3), (4, 3), (11, 3), (12, 3), (2, 4), (13, 4), (13, 5)],
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


VANILLA = os.path.join(ART, ".vanilla", "item")
CAND = os.path.join(ART, "candidates")
SHEET = os.path.join(CAND, "fish_boll_bucket.png")
SLOT = (139, 139, 139, 255)


def composite(layer):
    """What players see: our layer over vanilla's cod bucket (review only; vanilla is never written out)."""
    base = Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")
    base.alpha_composite(layer)
    return base


def hotbars():
    """Offline hotbar previews (art/tools/hotbar_preview.py) at GUI scale 2 and 4, the boll bucket unselected."""
    py = os.path.join(ART, ".venv", "bin", "python")
    tool = os.path.join(ART, "tools", "hotbar_preview.py")
    outs = []
    for suffix, scale in (("", "2"), ("_x4", "4")):
        out = os.path.join(CAND, f"fish_boll_bucket_hotbar{suffix}.png")
        subprocess.run([py, tool, out, "mc:cod_bucket", "mc:apple", "mc:salmon_bucket", "mc:bread",
                        "bucket:boll_bucket", "mc:tropical_fish_bucket", "bucket:cerna_bucket",
                        "mc:pufferfish_bucket", "bucket:huta_kahla_bucket", "--scale", scale],
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

    icon = Image.open(os.path.join(ITEMS, "boll.png")).convert("RGBA")
    designs = [(f"{n}{' (PICK)' if n == PICK else ''}", composite(build(g))) for n, g in CANDIDATES.items()]
    layers = [(f"{n}: layer alone", build(g)) for n, g in CANDIDATES.items()]
    parts.append(text(["Bucket of boll (common stingray), 16 x 16: the candidates as players see them (our layer over "
                       "vanilla's cod_bucket) at 8x, the layers alone, and the accepted boll icon whose palette they use"]))
    row = Image.new("RGBA", (W, 16 * 8 + 30), SLOT)
    d = ImageDraw.Draw(row)
    for i, (n, im) in enumerate(designs + layers + [("boll icon (accepted)", icon)]):
        row.alpha_composite(im.resize((128, 128), Image.NEAREST), (10 + i * 150, 4))
        d.text((10 + i * 150, 134), n, fill=(0, 0, 0), font=small)
    parts.append(row)

    compare = [("cod", van("cod_bucket")), ("salmon", van("salmon_bucket")),
               ("tropical fish", van("tropical_fish_bucket")), ("pufferfish", van("pufferfish_bucket")),
               ("cerna (ours)", ours("cerna_bucket")), ("cawl (ours)", ours("cawl_bucket")),
               ("huta kahla (ours)", ours("huta_kahla_bucket")), ("ziemel (ours)", ours("ziemel_bucket")),
               ("boll icon", icon)] + designs
    parts.append(text(["Beside vanilla's cod, salmon, tropical fish and pufferfish buckets, the accepted cerna, cawl, "
                       "huta kahla and ziemel buckets and the boll icon: 8x"]))
    row = Image.new("RGBA", (W, 16 * 8 + 30), SLOT)
    d = ImageDraw.Draw(row)
    for i, (n, im) in enumerate(compare):
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
            row.alpha_composite(im, (700 + i * 22, y0 + 17))
    parts.append(row)

    lines = ["art/tools/measure.py (whole composite as players see it):"]
    tmp = os.path.join(CAND, "fish_boll_bucket_measure.tmp.png")
    for n, im in compare:
        im.save(tmp)
        m = measure(tmp)
        lines.append(f"  {n:22s} coverage {m['coverage']:.2f}  colours {m['colours']:2d}  darkest {float(m['lmin']):.2f}"
                     f"  lightest {float(m['lmax']):.2f}  outline {float(m['edge_l']):.2f}  inside "
                     f"{float(m['interior_l']):.2f}  top-left minus bottom-right {float(m['tl_minus_br']):+.2f}")
    os.remove(tmp)
    parts.append(text(lines, small))

    parts.append(text(["Hotbar preview (art/tools/hotbar_preview.py, offline, as the game draws flat items) at GUI scale "
                       "2 and 4, nothing selected: cod bucket, apple, salmon bucket, bread, BOLL BUCKET, tropical fish "
                       "bucket, cerna bucket, pufferfish bucket, huta kahla bucket"]))
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


if __name__ == "__main__":
    n = 0
    for name, g in CANDIDATES.items():
        lay = build(g)
        n = check_cover(lay)
        check_rim(lay, os.path.join(VANILLA, "cod_bucket.png"), FISH_OVER_RIM[name])
    print(f"cover ok: all {n} cod pixels covered, 0 pixels identical to vanilla (all candidates)")
    build(CANDIDATES[PICK]).save(OUT, optimize=False)
    print("wrote", os.path.relpath(OUT, ROOT), f"(candidate {PICK})")
    if "--sheet" in sys.argv[1:]:
        sheet()
