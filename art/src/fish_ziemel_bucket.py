"""Bucket of ziemel tal-bahar (seahorse): the seahorse layer of the item icon (16 x 16), redesign 2026-11-18.

The bucket is not ours: the item model (made by art/src/pilot_models.py) puts the player's own vanilla
minecraft:item/cod_bucket underneath as layer0 and this texture on top as layer1, so the mod ships no Mojang
pixels (STYLE rule 3) and the bucket matches whatever resource pack the player uses. Rows 6-15 are clear, and in
rows 0-5 every opaque pixel of the cod in cod_bucket is covered so no cod shows through (check_cover() on every
run, against art/.vanilla's cod_bucket when it is there). Same method and water shades as the owner-accepted
cerna, awrata and murina buckets.

Why a redesign: the owner rejected the head-and-neck design ("seahorse needs a redesign. it cant jsut be the same
head in a bucket idea since it s a seahorse, it came off as a yellow duck. try again", decision note
docs/Decisions/2026-11-18 Seahorse bucket - redesign, not a head in a bucket.md). The fish rule "show the head,
never the tail" does not apply: this bucket shows the WHOLE seahorse, upright, the way vanilla's axolotl and
tadpole buckets show the whole animal.

The pick is the critic's mock-up V10 (art/candidates/critic_ziemel_bucket_v2/), the fix for my concept A, which
the critic marked FIX: a brown blob at 1x and 2x and a duckling or kiwi with a beak from 4x, because the snout came
out of the eye's row from a small round head. V10 has:
- a deep, horse-like head bent forward, the crown on top, one black eye with only mid tones round it;
- a tube snout on the row BELOW the eye, darkest at the tip;
- an open throat, the belly pushed forward and narrowing to an S;
- the tail's curl at the lower left in lighter tones against dark water;
- the bucket's normal back-rim outline behind the neck, with water below it (2026-11-18: the grey far rim the
  maker drew looked wrong to the owner, decision note docs/Decisions/2026-11-18 Buckets - keep the back outline.md).
Colour: the accepted 3D model's brown-ochre ramp (textures/entity/fish/ziemel.png) taken one to two steps darker
and redder toward real Hippocampus guttulatus: five body tones, the lightest (#a97c47) only on the belly. No yellow.

Concepts A, B and C and the rejected design are kept on the sheet. Concept D (a seahorse clinging to the outside
of the bucket) is not used: the owner kept the top strip (rows 6-15 stay clear).
Photos (reference only): art/references/fish_ziemel_refonly/ (list.tsv).

Writes: mod/src/main/resources/assets/mimcontent/textures/item/ziemel_bucket.png (byte-identical on rerun)
With --sheet it also writes the review sheet art/candidates/fish_ziemel_bucket.png and the hotbar previews.
Run:    art/.venv/bin/python art/src/fish_ziemel_bucket.py [--sheet]
"""
import os
import subprocess

from PIL import Image

from fish_bucket_rim import check_rim

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item",
                   "ziemel_bucket.png")


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = {
    # water: the accepted cerna and murina buckets' shades
    "~": hx("#2a55c4"),
    "#": hx("#383838"),  # the bucket's back-rim outline where we cover a cod pixel: our own grey (vanilla's is #353535)
    "v": hx("#1d3c96"),  # shadow on the water by the seahorse, and inside the tail's curl
    "^": hx("#6a92ea"),  # a glint of light on the water by the right rim
    # the far rim the concepts drew (sheet only; the pick has the normal outline): our own greys
    "r": hx("#393939"),  # the rim's outer edge
    "R": hx("#6a6a6a"),  # the inner wall in shade
    "s": hx("#8c8c8c"),  # the rim's top, in shade
    "S": hx("#a2a2a2"),  # the rim's top, lit
    # the ziemel: the accepted model's ramp (#7c5830 ... #eecd86) taken darker and redder, shade to light
    "0": hx("#4c3320"), "1": hx("#62442a"), "2": hx("#7a5634"), "3": hx("#936a3e"), "4": hx("#a97c47"),
    "E": hx("#0a0a0a"),  # the eye: the accepted buckets' eye black
    # the rejected design only (sheet): the model's own ramp, mane and the first version's underwater belly
    "a": hx("#7c5830"), "b": hx("#966c3a"), "c": hx("#b08244"), "d": hx("#c4964f"),
    "e": hx("#d4a85c"), "f": hx("#e2bb6e"), "g": hx("#eecd86"), "m": hx("#aa7840"),
}

EMPTY = ["................"] * 10

# The pick: the critic's mock-up V10 (art/candidates/critic_ziemel_bucket_v2/), the fix for concept A. Rows 0-5,
# columns 0-15; "." is clear. Rows 0-2: a deep, horse-like head bent forward, the crown at 5-8 on row 0 (mid tone
# above the eye, no light pixel touching it), the eye at 5,1, the tube snout on row 2 BELOW the eye (1-4), darkest at
# the tip. Rows 3-5: an open throat (the bucket's back outline seen at 3,3), the belly pushed forward and narrowing
# to an S, and the tail's curl at the lower left in lighter tones against dark water (3-4, rows 4-5). Changes from
# V10: 13,4 is left clear (V10 had water there, over the bucket's dark right side, which opened the outline); and
# (2026-11-18, owner: keep the back outline) the grey far rim at 8-12, rows 2-3, is now the normal back-rim outline
# (our #383838 over cod pixels at 8-9,2 and 11,3; clear over vanilla's own dark at 10,2 and 12,3), and the dark
# water outside the bucket at 2,3 and 2,4 is gone (clear; the bucket's own side shows at 2,4).
GRID = [
    ".....3341.......",
    "....3E3320......",
    ".0112321##......",
    "...#4432v~~#....",
    "...3v3320~~~^...",
    "...23321v~~~....",
] + EMPTY

CONCEPTS = {
    # A: the first pick (critic FIX: a brown blob at 1x and 2x, a duckling or kiwi from 4x, because the snout came out
    # of the eye's row from a small round head).
    "A upright (critic FIX)": [
        "......432.......",
        "...1223E31......",
        "...rSSSs321sr...",
        "..rRv~v443211r..",
        "..~~~2v321v~~...",
        "...~~1110~~^....",
    ] + EMPTY,
    # B: the seahorse to the right, its tail reaching over the bucket's right rim and hooking down outside it, the
    # way real ones grip seagrass. Same rim, colours and head as A.
    "B tail on the rim": [
        "........432.....",
        "....12223E31....",
        "...rSSSSs321sr..",
        "..rRv~~~v44321..",
        "..~~~~~~v321110.",
        "...~~^~~~v1~~.0.",
    ] + EMPTY,
    # C: the tail swung back into a ring beside the body (a spiral round a pixel of water).
    "C ring tail": [
        "......432.......",
        "...1223E31......",
        "...rSSSs321sr...",
        "..rRv~v4432v211.",
        "..~~~~v4321v2~0.",
        "...~~~~v2111100.",
    ] + EMPTY,
}

# The design the owner rejected ("came off as a yellow duck"): the head and neck rising out of the water, exactly as
# it was, in the model's own ramp (a-g = its #7c5830 ... #eecd86).
REJECTED = [
    "......fe........",
    "....cdeedb......",
    "...cdeEdcbbam...",
    "aabbcddbvbada~..",
    "...~vcdcbdad~^..",
    "....~dcbdb~~....",
] + EMPTY


# The back-rim outline pixels (art/src/fish_bucket_rim.py) that the seahorse's head and belly cover; every other one stays dark
FISH_OVER_RIM = [(5, 2), (6, 2), (7, 2), (4, 3)]


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
REFS = os.path.join(ART, "references", "fish_ziemel_refonly")
SHOTS = os.path.join(ROOT, ".art-runs", "ziemelmodel2", "build", "smoke-run", "screenshots")
MODEL_TEX = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "entity", "fish",
                         "ziemel.png")
SHEET = os.path.join(ART, "candidates", "fish_ziemel_bucket.png")
SLOT = (139, 139, 139, 255)


def hotbars():
    """Offline hotbar previews (art/tools/hotbar_preview.py) at GUI scale 2 and 4."""
    py = os.path.join(ART, ".venv", "bin", "python")
    tool = os.path.join(ART, "tools", "hotbar_preview.py")
    outs = []
    for suffix, scale in (("", "2"), ("_x4", "4")):
        out = os.path.join(ART, "candidates", f"fish_ziemel_bucket_hotbar{suffix}.png")
        subprocess.run([py, tool, out, "mc:cod_bucket", "mc:axolotl_bucket", "bucket:ziemel_bucket",
                        "mc:tadpole_bucket", "bucket:cerna_bucket", "bucket:awrata_bucket", "bucket:murina_bucket",
                        "mc:pufferfish_bucket", "--select", "2", "--scale", scale],
                       check=True, capture_output=True)
        outs.append(out)
    return outs


def composite(layer):
    """What players see: our layer over vanilla's cod bucket (review only; vanilla is never written out)."""
    base = Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")
    base.alpha_composite(layer)
    return base


def sheet():
    import sys
    from PIL import ImageDraw
    sys.path.insert(0, os.path.join(ART, "tools"))
    from font import label_font
    from measure import measure

    font, small = label_font(16), label_font(13)
    W = 1500
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

    parts.append(text(["Bucket of ziemel tal-bahar, REDESIGN (16 x 16). References: Hippocampus guttulatus, upright "
                       "body, pot belly, curled tail, long snout, crown (art/references/fish_ziemel_refonly)"]))
    row = Image.new("RGBA", (W, 190), (255, 255, 255, 255))
    x = 10
    for f in ("g_aquarium.jpg", "g_long.jpg", "g_france.jpg", "h_arrabida.jpg"):
        p = os.path.join(REFS, f)
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGBA")
        im.thumbnail((320, 180))
        row.alpha_composite(im, (x, 5))
        x += im.width + 10
    parts.append(row)

    parts.append(text(["The owner-accepted 3D model, where the palette comes from (ziemelmodel2 run: side, beside cod; "
                       "texture at 6x). The bucket uses its ramp one to two steps darker and redder."]))
    row = Image.new("RGBA", (W, 230), (255, 255, 255, 255))
    x = 10
    for f, box in (("0072_fish-ziemel-side.png", (340, 140, 500, 350)), ("0075_fish-ziemel-beside-cod.png", None)):
        p = os.path.join(SHOTS, f)
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGBA")
        im = im.crop(box) if box else im
        im.thumbnail((360, 220), Image.NEAREST)
        row.alpha_composite(im, (x, 5))
        x += im.width + 10
    if os.path.exists(MODEL_TEX):
        tex = Image.open(MODEL_TEX).convert("RGBA")
        row.alpha_composite(tex.resize((tex.width * 6, tex.height * 6), Image.NEAREST), (x, 5))
    parts.append(row)

    designs = [("REJECTED (yellow duck)", composite(build(REJECTED))),
               ("A upright (critic FIX)", composite(build(CONCEPTS["A upright (critic FIX)"]))),
               ("V10: THE PICK", composite(build())),
               ("B tail on the rim", composite(build(CONCEPTS["B tail on the rim"]))),
               ("C ring tail", composite(build(CONCEPTS["C ring tail"]))),
               ("V10: our layer alone", build())]
    parts.append(text(["The rejected design and the concepts, as players see them (our layer over vanilla's cod_bucket), "
                       "at 8x. Not shown: D (beside the bucket), not used: the owner kept the top strip."]))
    row = Image.new("RGBA", (W, 16 * 8 + 30), SLOT)
    d = ImageDraw.Draw(row)
    for i, (n, im) in enumerate(designs):
        row.alpha_composite(im.resize((128, 128), Image.NEAREST), (10 + i * 200, 4))
        d.text((10 + i * 200, 134), n, fill=(0, 0, 0), font=small)
    parts.append(row)

    parts.append(text(["The same at 2x and 1x, on the slot grey and on dark"]))
    row = Image.new("RGBA", (W, 100), SLOT)
    ImageDraw.Draw(row).rectangle((0, 50, W, 100), fill=(40, 40, 40))
    for i, (n, im) in enumerate(designs[:5]):
        for y0 in (0, 50):
            row.alpha_composite(im.resize((32, 32), Image.NEAREST), (10 + i * 200, y0 + 9))
            row.alpha_composite(im, (60 + i * 200, y0 + 17))
    parts.append(row)

    compare = [("cod", van("cod_bucket")), ("axolotl", van("axolotl_bucket")), ("tadpole", van("tadpole_bucket")),
               ("pufferfish", van("pufferfish_bucket")), ("cerna (ours)", ours("cerna_bucket")),
               ("awrata (ours)", ours("awrata_bucket")), ("murina (ours)", ours("murina_bucket")),
               ("ZIEMEL (V10, pick)", composite(build()))]
    parts.append(text(["The pick beside vanilla's cod, axolotl, tadpole and pufferfish buckets and our accepted cerna, "
                       "awrata and murina buckets: 8x, then 2x and 1x on grey and dark"]))
    row = Image.new("RGBA", (W, 16 * 8 + 30), SLOT)
    d = ImageDraw.Draw(row)
    for i, (n, im) in enumerate(compare):
        row.alpha_composite(im.resize((128, 128), Image.NEAREST), (10 + i * 150, 4))
        d.text((10 + i * 150, 134), n, fill=(0, 0, 0), font=small)
    parts.append(row)
    row = Image.new("RGBA", (W, 100), SLOT)
    ImageDraw.Draw(row).rectangle((0, 50, W, 100), fill=(40, 40, 40))
    for i, (n, im) in enumerate(compare):
        for y0 in (0, 50):
            row.alpha_composite(im.resize((32, 32), Image.NEAREST), (10 + i * 40, y0 + 9))
            row.alpha_composite(im, (360 + i * 22, y0 + 17))
    parts.append(row)

    lines = ["art/tools/measure.py (whole composite as players see it):"]
    tmp = os.path.join(os.path.dirname(SHEET), "fish_ziemel_bucket_measure.tmp.png")
    for n, im in compare + designs[:2] + designs[3:5]:
        im.save(tmp)
        m = measure(tmp)
        lines.append(f"  {n:26s} coverage {m['coverage']:.2f}  colours {m['colours']:2d}  darkest {float(m['lmin']):.2f}"
                     f"  lightest {float(m['lmax']):.2f}  outline {float(m['edge_l']):.2f}  inside "
                     f"{float(m['interior_l']):.2f}  top-left minus bottom-right {float(m['tl_minus_br']):+.2f}")
    os.remove(tmp)
    parts.append(text(lines, small))

    parts.append(text(["Hotbar preview (art/tools/hotbar_preview.py, offline, as the game draws flat items) at GUI scale "
                       "2 and 4: cod, axolotl, ZIEMEL (selected), tadpole, cerna, awrata, murina, pufferfish"]))
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
    os.makedirs(os.path.dirname(SHEET), exist_ok=True)
    out.convert("RGB").save(SHEET)
    print("wrote", os.path.relpath(SHEET, ROOT))


def check_cover(layer, rows_clear=True):
    """No cod may show through; rows 6-15 must be clear; no pixel may equal vanilla's at the same place."""
    cod = os.path.join(VANILLA, "cod_bucket.png")
    if rows_clear:
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
    import sys
    layer = build()
    n = check_cover(layer)
    check_rim(layer, os.path.join(VANILLA, "cod_bucket.png"), FISH_OVER_RIM)
    for name, g in CONCEPTS.items():
        check_cover(build(g))
    print(f"cover ok: all {n} cod pixels covered, 0 pixels identical to vanilla (pick and concepts)")
    layer.save(OUT, optimize=False)
    print("wrote", os.path.relpath(OUT, ROOT))
    if "--sheet" in sys.argv[1:]:
        sheet()
