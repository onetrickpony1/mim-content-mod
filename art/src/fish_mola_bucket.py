"""Bucket of mola mola (ocean sunfish, "Pixxiluna"): the fish layer of the item icon (16 x 16), 2026-11-18.

RETIRED 2026-11-19: the mola can't be caught in a bucket (docs/Decisions/2026-11-19 Mola mola - can be found, not
captured; escapes when hurt; basks in the sun.md), so the mod has no mola bucket. The script is kept for history: a
run still checks the candidates and writes the review sheet with --sheet, but no longer installs anything in the mod.

Made on the night job (docs/Decisions/2026-11-18 Night job - the rest of the fish, Claude decides.md): an independent
critic's PASS stands in for the owner's OK tonight; the creative choices are logged in
docs/Creatures and Plants/Night log/mola_mola.md for the owner's morning review.

The bucket is not ours: the item model (models/item/mola_mola_bucket.json) puts the player's own vanilla
minecraft:item/cod_bucket underneath as layer0 and this texture on top as layer1, so the mod ships no Mojang pixels
(STYLE rule 3) and the bucket matches whatever resource pack the player uses. Rows 6-15 are clear, and in rows 0-5
every opaque pixel of the cod in cod_bucket is covered so no cod shows through (check_cover() on every run, against
art/.vanilla's cod_bucket). The back-rim outline is checked by art/src/fish_bucket_rim.py (owner 2026-11-18, keep the
back outline). Same method and water shades as the accepted cerna, boll and skorfna buckets.

Owner rule: a bucket shows the fish's head rising out of the water, never the tail or the whole fish
(docs/Decisions/2026-11-18 Cerna bucket - head showing, not the whole fish.md). For the mola that head is the front of
the tall round grey disc:
- a blunt, rounded brow, lit at the top left (h), grey-brown on top (B) shading to silver (U S) at the water;
- the small beak mouth (q) as a notch on the very front of the outline, below the eye's row, so it sits on the
  silhouette and never inside the face beside the eye (no-face rule);
- one small dark eye (E) with only lit or mid tones round it: no ring, no dark pixel in its 3 x 3 or near it in its
  row (check_eye());
- behind the brow, the tip of the tall, slim dorsal fin standing up out of the water (dark G H with a lit leading
  edge f), the mola's signature; the rest of the disc, the clavus and the anal fin are under water.

Colours are the accepted-for-tonight icon A's (art/src/fish_mola_icon.py PAL: the accepted model's hues a step darker
for out of water), same keys, nothing new. The water and the rim tone are the shared bucket shades
(art/src/fish_bucket_rim.py).
References (photos, reference only): art/references/fish_mola_refonly/ (list.tsv), mm07, mm10 and mm04 above all.

Rounds (night of 2026-11-18, five critic rounds; each candidate's comment below says what changed and why):
1. A, B, C: critic picked B, PASS with fixes -> B2.  2. B2: critic PASS; blind readers with decoy buckets: "grey-green
mottled" fish -> B3, pale and smooth.  3. B3: critic PASS; blind readers: "pale grey flat, broad fish" -> D, a
narrower round dome with the fin apart behind.  4. D: critic PASS; blind readers alone among vanilla items: two
"Bucket of Cod", one saw the fin as a tail -> E, the fin grown out of the dome's back.  5. E: critic PASS, the pick.
Blind reads of E, alone among vanilla items: "Bucket of Mola Mola (Sunfish)" once, a plain grey fish twice.

Wrote (until retired): mod/src/main/resources/assets/mimcontent/textures/item/mola_mola_bucket.png (the PICK,
byte-identical on rerun); that file is now removed from the mod. With --sheet it also writes the review sheet art/candidates/fish_mola_bucket.png (the candidates as players
see them, this layer over vanilla's cod_bucket, at 8x, 2x and 1x beside vanilla's cod and pufferfish buckets and the
accepted cerna, boll and skorfna buckets; the layers alone; measure.py numbers; the offline hotbar previews).
Run:    art/.venv/bin/python art/src/fish_mola_bucket.py [--sheet]
"""
import os
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fish_bucket_rim import OUTLINE, RIM, WATER, check_rim, _dark as rim_dark  # noqa: E402
from fish_mola_icon import PAL as ICON  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
ART = os.path.join(ROOT, "art")
ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
OUT = os.path.join(ITEMS, "mola_mola_bucket.png")


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = {
    # water: the shared shades of the accepted buckets (art/src/fish_bucket_rim.py WATER)
    "~": hx("#2a55c4"),
    "v": hx("#1d3c96"),  # shadow on the water beside the fish where it goes under
    "^": hx("#6a92ea"),  # a glint of light on the water
    "#": RIM,            # the bucket's back-rim outline where we cover a cod pixel (vanilla's is #353535)
}
PAL.update(ICON)  # the icon's keys: h B U n S L W m F G H f c k P p E q O o

EMPTY = ["................"] * 10

# rows 0-5, columns 0-15; "." is clear (vanilla cod_bucket's own outline or water shows there)
CANDIDATES = {
    # A: the brow rises at the left of the mouth as vanilla's fish do, the back sloping down to the right into the
    # water; the dorsal fin's tip stands up from the slope (x 10-12, rows 0-3) and leans back. Dark grey-brown back B,
    # silver S and pale W lower down at the water line; the beak mouth q juts one pixel at the front (0,4) with a pale
    # lip c behind it, below and well before the eye (5,3).
    "A": [
        "..........oH....",
        "....OOOO..fHo...",
        "..OOhhBBBOfG....",
        ".OhhhEBBUUUF#...",
        "qcLSLSnSLSv~~...",
        ".oWLWPLWv^~~~...",
    ] + EMPTY,
    # B: a taller, rounder, blunt brow that rises to row 0, its front a round wall (x 2, 1, 0 down the rows), so it
    # reads as the top of a big round disc, not a pointed snout or a long low back; the eye high (4,2); the small beak
    # mouth q at the foot of the front (0,4) under a pale lip c; the slim dark fin stands apart behind (x 11-13),
    # leaning back.
    "B": [
        "...OOOOO...oH...",
        "..OhhhBBOo.fHo..",
        ".OhhEhBBBBofG...",
        "OchhBUBnBUUF#...",
        "qcLLSnLSLSLv~...",
        ".oWWWPLWv^~~~...",
    ] + EMPTY,
    # B2, the pick: critic round 1 picked B (PASS with fixes), applied here: the fin's rim pixel at 13,1 is gone so it
    # stands slim and upright rather than swept back like a shark's; the blotch below the eye (5,4) is plain silver
    # so eye, mouth and spot never make a face; the eye meets the body tone B on its right (5,2) instead of sitting
    # in a bright socket; the dome's top and right shoulder (7,0 8,1) take the shaded rim o; one pale lip (1,4) is
    # enough for the beak (1,3 is h); the back before the fin (10,3) is B so the fin stands off the body at 1x.
    "B2": [
        "...OOOOo...oH...",
        "..OhhhBBoo.fH...",
        ".OhhEBBBBBofG...",
        "OhhhBUBnBUBF#...",
        "qcLLSSLSLSLv~...",
        ".oWWWPLWv^~~~...",
    ] + EMPTY,
    # B3, the pick: B2 passed critic round 2, but three blind readers, with decoy buckets beside it, called it a
    # "grey-green mottled" bottom fish (and named the pale tonn the sunfish). So the disc goes pale and smooth, as the
    # out-of-water photos (mm07): the dark grey-brown back B and the blotch n are gone, the back is the icon's upper
    # side U, the middle silver S and lower side L, the water line pale belly W; the dark fin and the dark rim stay,
    # so the pale round head and the slim dark fin read apart at 1x.
    "B3": [
        "...OOOOo...oH...",
        "..OhhhUUoo.fH...",
        ".OhhEUUUUUofG...",
        "OhhLSUSSSUUF#...",
        "qcWLLSLSLSLv~...",
        ".oWWWPWWv^~~~...",
    ] + EMPTY,
    # D, the pick: three more blind readers (decoy buckets beside it) called B3 a "pale grey flat, broad fish": at
    # 12 px wide it read long. D keeps B3's pale smooth colours but makes the head a round dome only 9 px wide (x 0-8)
    # and 6 tall, its shaded right side curving down into the water, and stands the dorsal fin's tip up out of the
    # water BEHIND it (x 10-11, rows 0-3) with water between: the round front of the disc and the tall fin of the
    # brief. The bucket's far rim shows dark between them (9,2). The lower side is one smooth band (7,4 L, critic
    # round 3's note on B3).
    "D": [
        "...OOOo...oH....",
        "..OhhhUo..fH....",
        ".OhhEUUUo#fG....",
        "OhhLSUSSo~FG....",
        "qcWLLSLLov~~~...",
        ".oWWWPWLv^~~~...",
    ] + EMPTY,
    # E, the pick: D passed critic round 4, but two of three blind readers (D alone among vanilla items) called it a
    # cod, one seeing the fin standing apart in the water as a TAIL. So E grows the fin out of the dome's own back:
    # the round head (x 0-9) rises into a slim dark dorsal fin (x 9-11, rows 0-3) that leans back from it, one
    # silhouette like the real fish's profile, never a second thing in the water behind.
    "E": [
        "...OOo....oH....",
        "..OhhhUo.fH.....",
        ".OhhEUUUofG.....",
        "OhhLSUSSUFo#....",
        "qcWLLSLLSov~~...",
        ".oWWWPWLLv^~~...",
    ] + EMPTY,
    # C: a smaller, rounder dome (x 1-8) and the fin a tall thin blade standing straight up behind it (x 9-10), so the
    # two read as separate parts: round head, tall fin.
    "C": [
        ".........oHo....",
        "...OOOOO.fHo....",
        ".OOhhBBOOfGo....",
        "OhhEhBBBUFG#....",
        "qcLSLnSLSSv~~...",
        ".oWWPLWLv^~~~...",
    ] + EMPTY,
}
PICK = "E"

# The back-rim outline pixels (art/src/fish_bucket_rim.py OUTLINE) that a candidate's fish covers: every outline
# pixel where the layer holds a fish tone (not clear, not our water, not itself outline-dark). check_rim() then asserts
# every other outline pixel stays dark in the composite.
# Tones dark enough to read as a second eye or a mouth beside the eye (the outline O o is the silhouette and allowed)
DARK = set("EqHG#v")


def fish_over(layer):
    return [p for p in OUTLINE if layer.getpixel(p)[3] and layer.getpixel(p)[:3] not in WATER
            and not rim_dark(layer.getpixel(p))]


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
SHEET = os.path.join(CAND, "fish_mola_bucket.png")
SLOT = (139, 139, 139, 255)


def composite(layer):
    """What players see: our layer over vanilla's cod bucket (review only; vanilla is never written out)."""
    base = Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")
    base.alpha_composite(layer)
    return base


def check_eye(name, grid):
    """The no-second-eye, no-face rule: one eye, nothing dark in its 3 x 3 or within 4 px in its row, and the mouth
    on the outline below the eye's row."""
    eyes = [(x, y) for y, r in enumerate(grid) for x, c in enumerate(r) if c == "E"]
    assert len(eyes) == 1, (name, eyes)
    ex, ey = eyes[0]
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if 0 <= ey + dy < 16 and 0 <= ex + dx < 16:
                c = grid[ey + dy][ex + dx]
                assert not ((dx or dy) and c in DARK), f"{name}: dark {c} beside the eye at {ex + dx},{ey + dy}"
    for x, c in enumerate(grid[ey]):
        assert not (c in DARK and c != "E" and abs(x - ex) <= 4), f"{name}: dark {c} in the eye's row at {x},{ey}"
    for y, r in enumerate(grid):
        for x, c in enumerate(r):
            if c == "q":
                assert y > ey, f"{name}: the mouth must sit below the eye's row"
                assert x == 0 or r[x - 1] == ".", f"{name}: the mouth must be on the front outline"


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


def cand_file(name):
    return os.path.join(CAND, f"fish_mola_bucket_{name}.png")


def hotbars():
    """Offline hotbar previews (art/tools/hotbar_preview.py) at GUI scale 2 and 4, nothing selected."""
    py = os.path.join(ART, ".venv", "bin", "python")
    tool = os.path.join(ART, "tools", "hotbar_preview.py")
    outs = []
    # nine slots: the pick, then the other candidates of the B line (B, B2) and A
    cands = [f"file:{cand_file(n)}" for n in [PICK] + [n for n in ("D", "B3", "B2") if n != PICK]]
    for suffix, scale in (("", "2"), ("_x4", "4")):
        out = os.path.join(CAND, f"fish_mola_bucket_hotbar{suffix}.png")
        subprocess.run([py, tool, out, "mc:cod_bucket", cands[0], "mc:pufferfish_bucket", "bucket:cerna_bucket"]
                       + cands[1:] + ["bucket:boll_bucket", "bucket:skorfna_bucket",
                                      "--scale", scale], check=True, capture_output=True)
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

    icon = ("mola icon A", Image.open(os.path.join(ITEMS, "mola_mola.png")).convert("RGBA"))
    designs = [(f"{n}{' (PICK)' if n == PICK else ''}", composite(build(g))) for n, g in CANDIDATES.items()]
    layers = [(f"{n}: layer alone", build(g)) for n, g in CANDIDATES.items()]
    parts.append(text(["Bucket of mola mola (ocean sunfish), 16 x 16: the candidates as players see them (our layer "
                       "over vanilla's cod_bucket) at 8x, the layers alone, and the icon whose palette they use"]))
    allrow = designs + layers + [icon]
    row = Image.new("RGBA", (W, 16 * 8 + 30), SLOT)
    d = ImageDraw.Draw(row)
    for i, (n, im) in enumerate(allrow):
        row.alpha_composite(im.resize((128, 128), Image.NEAREST), (10 + i * 150, 4))
        d.text((10 + i * 150, 134), n, fill=(0, 0, 0), font=small)
    parts.append(row)

    compare = [("cod", van("cod_bucket")), ("pufferfish", van("pufferfish_bucket")),
               ("cerna (ours)", ours("cerna_bucket")), ("boll (ours)", ours("boll_bucket")),
               ("skorfna (ours)", ours("skorfna_bucket")), icon] + designs
    parts.append(text(["Beside vanilla's cod and pufferfish buckets, the accepted cerna, boll and skorfna buckets and "
                       "the mola icon: 8x"]))
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
    tmp = os.path.join(CAND, "fish_mola_bucket_measure.tmp.png")
    for n, im in compare:
        im.save(tmp)
        m = measure(tmp)
        lines.append(f"  {n:24s} coverage {m['coverage']:.2f}  colours {m['colours']:2d}  darkest {float(m['lmin']):.2f}"
                     f"  lightest {float(m['lmax']):.2f}  outline {float(m['edge_l']):.2f}  inside "
                     f"{float(m['interior_l']):.2f}  top-left minus bottom-right {float(m['tl_minus_br']):+.2f}")
    os.remove(tmp)
    parts.append(text(lines, small))

    parts.append(text(["Hotbar preview (art/tools/hotbar_preview.py, offline, as the game draws flat items) at GUI scale "
                       "2 and 4, nothing selected: cod bucket, MOLA " + PICK + " (the pick, slot 2), pufferfish and cerna "
                       "buckets, the other mola candidates D, B3 and B2, boll and skorfna buckets"]))
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
    out.convert("RGB").save(SHEET)
    print("wrote", os.path.relpath(SHEET, ROOT))


if __name__ == "__main__":
    n = 0
    os.makedirs(CAND, exist_ok=True)
    for name, g in CANDIDATES.items():
        check_eye(name, g)
        lay = build(g)
        n = check_cover(lay)
        check_rim(lay, os.path.join(VANILLA, "cod_bucket.png"), fish_over(lay))
        composite(lay).save(cand_file(name), optimize=False)
    print(f"cover ok: all {n} cod pixels covered, 0 pixels identical to vanilla (all candidates)")
    # retired 2026-11-19 (no mola bucket in the mod): the pick is no longer written to OUT
    print("retired: the mola has no bucket; nothing installed (pick was candidate", PICK + ")")
    if "--sheet" in sys.argv[1:]:
        sheet()
