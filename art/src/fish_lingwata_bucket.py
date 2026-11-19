"""Bucket of lingwata (common sole, Solea solea): the fish layer of the item icon (16 x 16), 2026-11-19.

The bucket is not ours: the item model puts the player's own vanilla minecraft:item/cod_bucket underneath as layer0
and this texture on top as layer1, so the mod ships no Mojang pixels (STYLE rule 3). Rows 6-15 are clear, and in rows
0-5 every opaque pixel of the cod in cod_bucket is covered so no cod shows through (check_cover()). The back-rim
outline is checked by art/src/fish_bucket_rim.py (owner 2026-11-18, keep the back outline).

Owner rule: a bucket shows the animal's head rising out of the water, the vanilla way, never the tail or the whole
animal. A sole's head is the rounded front of its oval: it rises out of the water at the left of the mouth, eyed side
to the viewer, with the lighter fringe fin round its edge and both eyes on one side of it, one above the other on a
slant (never side by side like a face); the rest of the fish is under the water, which covers the cod where the fish
doesn't reach.

Colours: the accepted item icon's (art/src/fish_lingwata_icon.py, candidate I), same keys; the water and the rim tone
are the shared bucket shades (art/src/fish_bucket_rim.py).

Candidates (the sheet shows all three; PICK is installed):
- A: the head rising at the left, tilted like vanilla's cod, the eyes on its upper left side.
- B: A with the head a little wider and taller, so more of the oval shows.
- C: A with the head leaning further over to the left and a glint on the water.
Owner 2026-11-19: A should fill more of the bucket (redo D-H, G passed the critic); then, after seeing G and H, the
sole should stand upright, about 90 degrees (J-Q, see the comments by each; none passed in 3 critic rounds; P is
installed for the owner to judge).

Run:  art/.venv/bin/python art/src/fish_lingwata_bucket.py [--sheet]
Writes mod/.../textures/item/lingwata_bucket.png (byte-identical on rerun); with --sheet also
art/candidates/fish_lingwata_bucket.png and its offline hotbar art/candidates/fish_lingwata_bucket_hotbar.png.
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fish_bucket_rim import check_rim  # noqa: E402
import fish_lingwata_icon as ICON  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
ART = os.path.join(ROOT, "art")
ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
OUT = os.path.join(ITEMS, "lingwata_bucket.png")
VANILLA = os.path.join(ART, ".vanilla", "item")
PICK = "Q"
SHOW = ("G", "M", "P", "Q")   # on the sheet: G (the sideways redo, owner: stand it upright), upright round 2 M, and P, Q


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = dict(ICON.PAL)
PAL.update({
    "~": hx("#2a55c4"),   # water (the shared bucket shade)
    "v": hx("#1d3c96"),   # the shadow on the water beside the fish
    "^": hx("#6a92ea"),   # a glint on the water
    "#": hx("#383838"),   # the back rim where we cover a cod pixel (vanilla's is #353535)
})

# rows 0-5; "." is clear (vanilla shows). K/O the icon's lit and shaded outline, F/f/g the fringe, 1/2/3 the body,
# m a speckle, e the eyes with their pale rings R.
CANDIDATES = {
    "A": ["....KFK.........",
          "...KF1eFK.......",
          "...F1R12gO#.....",
          "..Kfe22m3O~#....",
          "..KfR233gv~^~...",
          "...vgf3gv~~~~...",
          ],
    "B": ["...KFFFK........",
          "..KF11eFK.......",
          "..KF1RR12O#.....",
          "..Kfe2m23gO#....",
          "..KfR2333gv~~...",
          "...vgf33gv~^~...",
          ],
    "C": ["...KFK..........",
          "..KF1eFK........",
          "..F1R1FK##......",
          "..fe22gO~~~#....",
          "..gR33fv~^~~~...",
          "...vgfgv~~^~~...",
          ],
    # Owner 2026-11-19: "lingwata bucket fails it should fill more of the bucket". Redo: the big flat oval rises
    # out of the water and spreads wide across the opening, tilted up so its mottled top side with both eyes faces
    # the viewer; the eyes get their pale rings automatically (ring()). Our accepted buckets cover 27-65 fish pixels in
    # rows 0-5 (boll 65, skorfna 50, kavall 33, cerna 30, marzpan 27); these cover about 60-70.
    # D: tilted like vanilla's cod, the head high at the upper left, the far end dipping into the water at the right.
    "D": ["...KKFFFK.......",
          "..KF11e1FFK.....",
          ".KF1e1112mFFK...",
          ".Kf1112m2233gFK.",
          ".Kg122233m33gfO.",
          "..Og23332gg~vO..",
          ],
    # E: more upright, the oval face-on across the whole opening, its lower half in the water.
    "E": ["....KFFFFK......",
          "..KFF1e11FFK....",
          ".KF111e112fFK...",
          ".Kf1112m2223gK..",
          ".Kg12m22223gfO..",
          "...Og3332m3gO...",
          ],
    # F: D tilted further and wider, from the left edge of the bucket to the right one.
    "F": ["..KKFFFFK.......",
          ".KF11e11FFK.....",
          "KF1e11112mFFK...",
          "Kf11112m22233FK.",
          "Kg1223m22333gfOO",
          ".Og23332m3g~vO..",
          ],
    # Redo round 1 ("a bread roll on a bucket, nothing says which end is the head"): G gives it a head end, the
    # rounder, higher left end with both eyes close together on a slant, and tapers to the right into a small darker
    # tail fan poking past the rim; one smooth oval edge with the lighter fringe inside the outline; mid-brown speckles
    # kept away from the eyes.
    "G": ["..KKFFFK........",
          ".KF1e11FFK......",
          "KF1e1112mFFK....",
          "Kf1112m222gFKt..",
          "Kg12223m33gfOTt.",
          ".Og333223g~~vOt.",
          ],
    # H: G with the head a pixel higher and fuller, fringe ticks along the top, and a wider tail fan.
    "H": [".KKFFfFK........",
          "KF1e11fFFK......",
          "F1e11112FfFK....",
          "f1112m2222gFKtt.",
          "Kg12223m33gfOTTt",
          ".Og333223g~~vOt.",
          ],
    # Owner 2026-11-19: "have the lingwata be like 90 degree vertical in the bucket instead of trying to seat it
    # sideways". The sole stands upright, head up, eyed side to the viewer: the rounded head end with both eyes on a
    # slant near the top, the fringe down both sides, the rest of the body under the water. It stands at the left of
    # the mouth like vanilla's cod (the cod pixels at rows 1-2 x3-7 can only be covered by the fish), water at right.
    # J: 7-8 px wide, the two eyes one above the other with a pale ring between them.
    "J": ["....KFFK........",
          "...KF11eFK......",
          "...Kf111FO#.....",
          "...Kf22e3gO#....",
          "...Kg2m33gOv~...",
          "...Og3m33gOv^...",
          ],
    # K: slimmer, 6 px wide, more water beside it.
    "K": ["....KFFK........",
          "...KF1eFK.......",
          "...Kfe1FO#......",
          "...Kf2mgO~~#....",
          "...Kg23gOv~~~...",
          "...Og3gOv~^~....",
          ],
    # L: fuller, 8 px wide.
    "L": ["....KFFFK.......",
          "...KF111eFK.....",
          "...Kf12e1FO.....",
          "...Kf2m23gO#....",
          "...Kg23m3gOv~...",
          "...Og3333gOv^...",
          ],
    # Upright round 1 ("a round tan lump with two dark dots, like a potato"): M narrows the top to a blunt tongue tip
    # (row 0 two pixels), runs the pale fringe down both sides just inside the outline, puts the eyes on a slant (no
    # pale halo beside them, so they don't read as buttons or a face; "T" is body tan that gets no ring), and spreads
    # the mottles evenly.
    "M": [".....KK.........",
          "....KF1TeO......",
          "...KF11TTFO.....",
          "...KFmTeTFO#....",
          "...KF232m3FOv...",
          "...Og32333gO^...",
          ],
    # N: M one pixel wider at the left from row 3 down, over the rim, to fill more of the bucket.
    "N": [".....KK.........",
          "....KF1TeO......",
          "...KF11TTFO.....",
          "..KF1mTeTFO#....",
          "..KF1232m3FOv...",
          "..Og332333gO^...",
          ],
    # Upright round 2 ("a round tan head with two eyes peeking over the rim, like a hamster"): P is a narrow tongue,
    # 2 px at the top leaning right, 4 at row 1 (the least that covers the cod there), 6 below; a dark mouth-hook
    # pixel at the upper left so the top reads as a snout; the eyes a full pixel apart on a slant, each with one pale
    # pixel beside it; the pale fringe down both sides; lighter mottles; the dark back rim and water to its right.
    "P": ["......KK........",
          "....pTeRO.......",
          "...KFTTFO#......",
          "...KFeRFO~~#....",
          "...KFT3FOv~~~...",
          "...Og32gOv~^~...",
          ],
    # Q: P a pixel wider from row 2 down.
    "Q": ["......KK........",
          "....pTeRO.......",
          "...KFTT1FO#.....",
          "...KFeRTFO~#....",
          "...KFT323FOv~...",
          "...Og3232gOv^...",
          ],
}
def fish_over_rim(rows):
    """The back-rim outline pixels (art/src/fish_bucket_rim.py OUTLINE) that the head itself covers."""
    from fish_bucket_rim import OUTLINE
    return [(x, y) for (x, y) in OUTLINE if y < len(rows) and rows[y][x] not in ".~v^#"]


def ring(rows):
    """Each eye gets a pale ring on the body round it (the icon's R), so no other mark looks like it."""
    g = [list(r) for r in rows]
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch == "e":
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= ny < len(g) and 0 <= nx < 16 and g[ny][nx] in "123":
                        g[ny][nx] = "R"
    return ["".join(r) for r in g]


def build(rows):
    rows = ring(rows)
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != ".":
                img.putpixel((x, y), PAL[ch] + (255,))
    return img


def composite(layer):
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
        p = os.path.join(VANILLA, n + ".png")
        if not os.path.exists(p):
            continue
        v = Image.open(p).convert("RGBA")
        same += [(n, x, y) for y in range(16) for x in range(16)
                 if layer.getpixel((x, y))[3] and layer.getpixel((x, y)) == v.getpixel((x, y))]
    assert not same, f"pixels identical to vanilla: {same}"
    print(f"cover ok: all {len(fishy)} cod pixels covered, 0 pixels identical to vanilla")


def sheet():
    sys.path.insert(0, os.path.join(ART, "tools"))
    from measure import measure
    try:
        from font import label_font
        font = label_font(14)
    except Exception:
        font = None
    W = 1500
    SLOT = (139, 139, 139, 255)
    blocks = []

    def text(t):
        im = Image.new("RGBA", (W, 26), (255, 255, 255, 255))
        ImageDraw.Draw(im).text((8, 5), t, fill=(0, 0, 0), font=font)
        blocks.append(im)

    items = [(n, Image.open(os.path.join(VANILLA, n + ".png")).convert("RGBA"))
             for n in ("cod_bucket", "salmon_bucket", "tropical_fish_bucket")]
    items.append(("boll bucket (accepted)", composite(Image.open(os.path.join(ITEMS, "boll_bucket.png")).convert("RGBA"))))
    items.append(("boll item", Image.open(os.path.join(ITEMS, "boll.png")).convert("RGBA")))
    items.append(("lingwata item", Image.open(os.path.join(ITEMS, "lingwata.png")).convert("RGBA")))
    for c in SHOW:
        tag = " PICK" if c == PICK else (" (rejected)" if c == "A" else "")
        items.append(("lingwata " + c + tag, composite(build(CANDIDATES[c]))))
    text("8x on the slot grey: vanilla cod, salmon, tropical fish buckets | accepted boll bucket and icon | the lingwata "
         "icon | lingwata buckets " + ", ".join(SHOW))
    row = Image.new("RGBA", (W, 160), SLOT)
    d = ImageDraw.Draw(row)
    for i, (n, im) in enumerate(items):
        row.alpha_composite(im.resize((128, 128), Image.NEAREST), (10 + i * 150, 4))
        d.text((10 + i * 150, 136), n, fill=(0, 0, 0), font=font)
    blocks.append(row)
    text("1x and 2x (same order)")
    row = Image.new("RGBA", (W, 60), SLOT)
    for i, (n, im) in enumerate(items):
        row.alpha_composite(im, (10 + i * 20, 20))
        row.alpha_composite(im.resize((32, 32), Image.NEAREST), (240 + i * 40, 12))
    blocks.append(row)
    tmp = os.path.join(ART, "candidates", "fish_lingwata_bucket_measure.tmp.png")
    for n, im in items:
        im.save(tmp)
        r = measure(tmp)
        text(f"{n:26s} coverage {r['coverage']:.2f} colours {r['colours']:2d} darkest {float(r['lmin']):.2f} lightest "
             f"{float(r['lmax']):.2f} outline {float(r['edge_l']):.2f} inside {float(r['interior_l']):.2f} "
             f"tl-br {float(r['tl_minus_br']):+.2f}")
    os.remove(tmp)
    files = []
    for c in SHOW:
        p = os.path.join(ART, "candidates", "fish_lingwata_bucket_%s.png" % c)
        composite(build(CANDIDATES[c])).save(p)
        files.append("file:" + p)
    hb = os.path.join(ART, "candidates", "fish_lingwata_bucket_hotbar.png")
    subprocess.run([sys.executable, os.path.join(ART, "tools", "hotbar_preview.py"), hb, "mc:cod_bucket", "bucket:boll_bucket"]
                   + files + ["mod:lingwata", "mc:salmon_bucket", "--scale", "3"], check=True,
                   stdout=subprocess.DEVNULL)
    text("Offline hotbar (GUI scale 3, unselected): cod bucket, boll bucket, lingwata buckets " + ", ".join(SHOW)
         + ", the lingwata icon, salmon bucket")
    hbi = Image.open(hb).convert("RGBA")
    row = Image.new("RGBA", (W, hbi.height + 10), (255, 255, 255, 255))
    row.alpha_composite(hbi, (10, 5))
    blocks.append(row)
    out = Image.new("RGBA", (W, sum(b.height for b in blocks)), (255, 255, 255, 255))
    y = 0
    for b in blocks:
        out.alpha_composite(b, (0, y))
        y += b.height
    dest = os.path.join(ART, "candidates", "fish_lingwata_bucket.png")
    out.convert("RGB").save(dest)
    print("sheet:", dest)


def main():
    cod = os.path.join(VANILLA, "cod_bucket.png")
    for c, rows in CANDIDATES.items():
        layer = build(rows)
        check_cover(layer)
        check_rim(layer, cod, fish_over_rim(rows))
    build(CANDIDATES[PICK]).save(OUT, optimize=False)
    print("wrote", os.path.relpath(OUT, ROOT), "(candidate %s)" % PICK)
    if "--sheet" in sys.argv[1:]:
        sheet()


if __name__ == "__main__":
    main()
