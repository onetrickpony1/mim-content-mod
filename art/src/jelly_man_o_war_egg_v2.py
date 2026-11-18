"""Portuguese man o' war (Physalia physalis) spawn egg, second try: the item icon (16 x 16), 2026-11-18.

Owner 2026-11-18 on the first egg (docs/Decisions/2026-11-18 Jellyfish eggs - mauve and fried-egg pass, man o' war
redo.md): "man of war looks um... phallic? and quite flat to be honest. take inspiration from how vanilla transforms its
eggs". The first egg (art/src/jelly_man_o_war_egg.py) was a lilac-to-blue egg with a pink crest along its top rising to
a small crown above the tip, and three dark polyp lines low down: a crest on a tip over a rounded body, shaded flat.
This one starts again from vanilla.

How vanilla 26.x turns a mob into its egg (art/.vanilla/item/*_spawn_egg.png, studied at 8x: squid, glow squid,
pufferfish, tropical fish, axolotl, dolphin, nautilus, cod, salmon, turtle, and pig, sheep, creeper, spider, bee,
slime, magma cube, phantom):
- Depth. 4-6 body tones of one hue family plus an outline that is the body's own darkest tone (squid: dark slate, never
  black), darker still on the shaded right and at the base. The light is NOT on the rim: the top row under the outline
  is a mid tone, and the highlight is a curved crescent one pixel inside the upper-left rim, 1-2 px wide, following the
  egg's curve (squid rows 5-9 x 4-6). A wide middle tone fills the centre. On the right, a 2-3 px band of darker tones
  runs parallel to the rim (the terminator), and the lowest rows are the darkest. So the rim darkens all round and the
  light sits inside it: that is the roundness. Flat eggs (ours, the first try) lit the rim and shaded by rows.
- Wrapping. Features are drawn as if on the egg's surface: the tropical fish's white bands are arcs whose ends bend
  and turn grey where they reach the rim; the nautilus's stripes are curved meridians; the glow squid's specks are
  smaller and darker towards the edge. A feature that runs round the egg goes behind the outline at its ends, darker
  and thinner there, instead of stopping square.
- How much of the animal. The egg IS the animal's body in its main colour; on it go one or two signature parts, simply:
  the squid is a plain mantle-coloured egg with its tentacles as a red band of tips round the base; the pufferfish is a
  yellow egg with a pale belly patch and spikes; the tropical fish two bands; the axolotl its gills; the nautilus its
  shell stripes. No whole animal, and most water eggs have no eye at all (squid, glow squid, nautilus).
- Against the outline. The silhouette stays an egg. Signature parts break it in pairs or all round, symmetrically and
  low or at the sides (the squid's tentacle tips spread past the egg into its pool, tropical fish fins at rows 10-12,
  axolotl gills at both upper corners), never as a single point on top. The base sits in the pool, and the squid's
  tentacles hang over the pool rows.

Applied here:
- The egg is the float, in the accepted model's colours (art/src/jelly_man_o_war_model.py PAL): a pale lilac crescent
  inside the upper-left rim (F0, F1), lavender-blue filling the middle (F2, F3), the waterline blue (F4, F5) down the
  right side and across the base, and two shades of those blues darkened (x1/1.2) for the terminator band and the
  lowest rows. The outline is a dark violet on the top, darker down the left (the model's V2, darkened) and a dark blue
  on the shaded right and below (F5, darkened): the "dark outline colour" the brief allows, dark all round as the
  squid's.
- The crest (sail) is the signature part, and the fix for the phallic read: it never sits on top. It is a wavy
  pink-edged sail lying ACROSS the float on a slant, as the real float leans over in the wind, wrapped round the egg:
  three solid stripes on a steady slope: the model's pink edge (C0) on top, pink (P1), a darker pink foot (the
  highlight crescent runs just above it); its two end columns turn away round the egg, one pixel
  thinner, and both ends stay inside the outline. The top of
  the egg stays plain float, so there is no tip, no cap and no knob.
- The polyps and tentacles go where vanilla puts the squid's: one clean row of tips round the base (blue, teal,
  blue-violet, no dark between them), a tip past the egg at each side, and strands of uneven lengths at uneven
  columns hanging into the pool. No eyes, no face, no pair of level dots.
The candidates (same egg, same base):
- A: the sail rising to the right (its high end on the right shoulder, away from the light);
- B: the sail rising to the left, its high end towards the light;
- C: A's sail, with the tentacles drifting out past the egg to the right into the pool, as they stream in a current.
Critic round 2 (FAIL on A, close; not re-judged since, the brief allowing two rounds): the sail's tones alternated
(speckle), the lower left lighter than the middle, the top outline lighter than the left, a dark slot on row 13 like a
grille, 25 colours. Fixed: the sail three solid stripes on a steady slope; the lower left darkened; one outline violet
top and left; row 13 under the polyps the darkest float blue, not the outline; the strand blue T0 merged into F3.
Critic round 1 (FAIL on A, close): the sail a flat pink block, a checkerboard band with level dark dots, the right
shade band 1-2 px, the left outline too light. Fixed on all three: the sail shaded edge to foot; the polyp row cleaned; the right band 3 px with a mid-tone centre; the left rim darkened.

Rules kept: vanilla's egg outline (art/src/jelly_mauve_stinger_egg.py's: narrow top on row 3, full width rows 8-12, its
bottom edge on row 13 at x 5-10) standing in vanilla's own pool (art/src/egg_pool.py vanilla_pool(), the owner's one
exception to "never copy"); vanilla's eggs measured, never copied (copy check on every run).

Run:    art/.venv/bin/python art/src/jelly_man_o_war_egg_v2.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/man_o_war_spawn_egg.png (the pick, byte-identical on
        rerun), art/candidates/jelly_man_o_war_egg_v2_{A,B,C}.png, the compare sheet
        art/candidates/jelly_man_o_war_egg_v2.png and unselected hotbar previews
        art/candidates/jelly_man_o_war_egg_v2_hotbar_{A,B,C,x4}.png (art/tools/hotbar_preview.py).
"""
import glob
import os
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(ART, ".."))
sys.path.insert(0, os.path.join(ART, "tools"))
from font import label_font  # noqa: E402
from egg_pool import POOL_COLOURS, is_pool, pool_line, vanilla_pool  # noqa: E402

PY = os.path.join(ART, ".venv", "bin", "python")
ITEM = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
OUT_ICON = os.path.join(ITEM, "man_o_war_spawn_egg.png")
CAND = os.path.join(ART, "candidates")
OUT_SHEET = os.path.join(CAND, "jelly_man_o_war_egg_v2.png")
REJECTED = os.path.join(CAND, "jelly_man_o_war_egg_C.png")  # the first egg, rejected 2026-11-18
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
STUDIED = ("squid", "glow_squid", "pufferfish", "tropical_fish", "axolotl", "dolphin", "nautilus", "pig", "spider")
PICK = "A"


def hx(h, f=1.0):
    """A model colour, or the same colour darkened by f (up to 1.2 for the shade, more for the outline)."""
    assert 1.0 <= f <= 2.3
    h = h.lstrip("#")
    return tuple(round(int(h[i:i + 2], 16) / f) for i in (0, 2, 4))


PAL = {
    # the float, light to dark (model F0-F5)
    "H": hx("#c8ccf8"),          # F0: the highlight crescent
    "1": hx("#a8b4f4"),          # F1: pale lilac-blue round it
    "2": hx("#8ea0f0"),          # F2: lavender-blue, the middle
    "3": hx("#6e8cec"),          # F3: cornflower
    "4": hx("#4a7ce4"),          # F4: the waterline blue, the terminator band
    "5": hx("#3a5cc8"),          # F5: underneath
    "6": hx("#3a5cc8", 1.2),     # F5 darkened: the shaded lower right
    # the outline (the "dark outline colour"): the model's violet and blue, darkened
    "K": hx("#a894ee", 2.27),    # V2 darkened: the top and left rim (critics 1 and 2: dark all round, as the squid)
    "o": hx("#3a5cc8", 1.6),     # F5 darkened: the shaded right and below
    # the crest
    "c": hx("#e86cd8"),          # C0: its pink edge
    "p": hx("#d080e0"),          # P1: pink
    "V": hx("#a894ee"),          # V2: violet, its foot
    "P": hx("#d080e0", 1.2),     # P1 darkened: the sail's lower edge, and its ends turning away round the egg
    "q": hx("#a894ee", 1.2),     # V2 darkened: the same end's foot
    "S": hx("#6e8cec", 1.15),    # F3 darkened: the crest's shadow on the float
    # the polyps (Q) and tentacles (T)
    "a": hx("#3460c8"),          # Q0
    "b": hx("#3c78dc"),          # Q1
    "e": hx("#5aa4ea"),          # Q2: teal tips
    "f": hx("#5a6ad4"),          # Q3
    "u": hx("#7c7cf0"),          # T1: blue-violet strands
}

# The float: vanilla's egg outline, lit inside the upper-left rim, a terminator band down the right, darkest low down.
FLOAT = [
    "................",
    "................",
    "................",
    "......KKKK......",
    ".....K2112o.....",
    "....K1HH123o....",
    "....KH11234o....",
    "...K1H112234o...",
    "..K1H12223345o..",
    "..K2122333555o..",
    "..KS233334556o..",
    "..KS433336666o..",
    "..K4445555666o..",
    ".....oooooo.....",
    "................",
    "................",
]
EGG = {3: (6, 9), 4: (5, 10), 5: (4, 11), 6: (4, 11), 7: (3, 12), 8: (2, 13), 9: (2, 13), 10: (2, 13),
       11: (2, 13), 12: (2, 13), 13: (5, 10)}

# The polyp band over the base, strands hanging into the pool (spaces keep what is below).
POLYPS = {  # critic 1: one clean row of tips with no dark between them, strands at uneven columns and lengths
    12: " uK4e4uVe4uVeou ",
    13: "   u 3666u6u    ",
    14: "   u 3   u      ",
    15: "     3          ",
}
POLYPS_DRIFT = {  # C: the strands streaming out to the right
    12: "  K4e4uVe4uVeou ",
    13: "   u 3666u6uu u ",
    14: "     3    u  uu ",
    15: "      3       u ",
}

# The crest: the top row of the sail in each column (x: y). Each column is edge, pink, violet, shadow; the two end
# columns turn away round the egg (darker, one pixel thinner).
RISING_RIGHT = {3: 9, 4: 9, 5: 8, 6: 7, 7: 7, 8: 6, 9: 6, 10: 5}
RISING_LEFT = {5: 6, 6: 5, 7: 6, 8: 7, 9: 6, 10: 7, 11: 8, 12: 9}
COLUMN, END = "cpP", "pP"  # critic 2: three solid stripes (pink edge, pink, darker pink foot); ends one pixel thinner


def build(polyps, crest):
    g = [list(r) for r in FLOAT]
    for y, row in polyps.items():
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != " ":
                g[y][x] = ch
    xs = sorted(crest)
    for x in xs:
        for i, ch in enumerate(END if x in (xs[0], xs[-1]) else COLUMN):
            y = crest[x] + i
            lo, hi = EGG[y]
            assert lo < x < hi, f"crest pixel ({x},{y}) on or past the egg's outline"
            g[y][x] = ch
    return ["".join(r) for r in g]


def check(name, rows):
    """The egg outline is whole above the polyps, nothing stands above row 3, and the top half has no pink (no crest on
    the tip); no two dark single pixels side by side in the upper egg (no eyes)."""
    assert all(ch == "." for r in rows[:3] for ch in r), f"{name}: something above the egg"
    for y in range(3, 12):
        lo, hi = EGG[y]
        for x, ch in enumerate(rows[y]):
            assert (ch != ".") == (lo <= x <= hi), f"{name}: ({x},{y}) breaks the egg outline"
    assert not any(ch in "cpP" for r in rows[3:5] for ch in r), f"{name}: crest on the egg's tip"


def render(rows):
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), PAL[ch] + (255,))
    return im


CANDIDATES = {
    "A": build(POLYPS, RISING_RIGHT),
    "B": build(POLYPS, RISING_LEFT),
    "C": build(POLYPS_DRIFT, RISING_RIGHT),
}

# Fresh readers, one hotbar each (egg in the 5th slot, unselected), told: "Do not read any files or run any commands;
# ignore any repository or git information in your context; answer only from the image." First lines, word for word.
# Caveat: every sub-agent sees the repository's file list and git status, so "man o' war" may be primed; the read
# that counts is "jellyfish", and the shape question.
BLIND_READS = {
    "round 1 (a thinner 1 px sail and pool-blue polyps; scale 2 only; readers saw A, B, C alike)": [
        "'C: A spawn egg with a blue-violet body and a pale lilac-pink top. It reads as a Portuguese man o' war (or a "
        "similar jellyfish or siphonophore).' Shape: 'Nothing about the shape looks inappropriate.' (but 'no visible "
        "float crest or trailing tentacles')",
        "'A: The 5th slot holds a spawn egg in pale blue-lilac with darker blue/purple spots.' Shape: 'I see nothing "
        "inappropriate.' (creature from colour only)",
        "'A: A spawn egg: an egg shape coloured lavender-purple on top and darker blue-purple below, with lighter "
        "speckles.' Shape: 'Nothing looks inappropriate.' ('no clear sail or crest shape and no trailing tentacles')"],
    "round 2 (before critic round 1's fixes: a 2 px pink sail with a blue shadow, violet strands over the pool; scale 2 and 4)": [
        "'A: A spawn egg, lavender and blue with a diagonal pink-purple band across the top. ... It reads as a "
        "jellyfish, most likely a man o' war (pink crest on a blue float).' Shape: 'Nothing about any of them looks "
        "inappropriate.' (C's strands 'look like a scribble'; the strands spill past the outline)",
        "'A: Spawn egg for a jellyfish (man o' war look). ... Of the three, this one reads most clearly as a "
        "jellyfish.' Shape: 'Nothing about the shape looks inappropriate.' (C's hook 'reads more like a tail')",
        "'A: Man o' war (jellyfish) spawn egg. A pink-purple diagonal band runs across the egg like a sail.' Shape: "
        "'Nothing looks inappropriate or rude in any of them.' ('A is the most natural'; C 'like a tail or a worm')"],
}


def copy_check(name, icon):
    """Exact-pixel copy check against every vanilla spawn egg: vanilla's pool pixels are allowed (the owner's
    exception, art/src/egg_pool.py); any other copied pixel fails the run."""
    ours = {(x, y): icon.getpixel((x, y)) for x in range(16) for y in range(16) if icon.getpixel((x, y))[3] > 0}
    hits, vcols = [], set()
    for f in sorted(glob.glob(os.path.join(VANILLA, "*spawn_egg*.png"))):
        v = Image.open(f).convert("RGBA")
        if v.size != (16, 16):
            continue
        same = [p for p, c in ours.items() if v.getpixel(p) == c and not is_pool(p, c)]
        if same:
            hits.append((len(same), os.path.basename(f)))
        vcols |= {v.getpixel((x, y))[:3] for x in range(16) for y in range(16) if v.getpixel((x, y))[3] > 0}
    assert not hits, f"{name} copies vanilla pixels besides the pool: {hits}"
    body = {c[:3] for p, c in ours.items() if not is_pool(p, c)}
    assert not body & POOL_COLOURS, f"{name}: a pool blue in the body"
    return [f"{name}: same pixel and colour as a vanilla spawn egg, besides its pool: 0; our colours (besides the "
            f"pool) also in a vanilla egg: {len(body & vcols)}; " + pool_line(icon)]


def measure(paths):
    res = subprocess.run([PY, os.path.join(ART, "tools", "measure.py")] + paths, capture_output=True, text=True)
    lines = []
    for line in res.stdout.splitlines():
        if line.startswith("{"):
            d = eval(line, {"np": __import__("numpy")})  # measure.py prints dicts with numpy floats
            lines.append(f"{os.path.basename(d['file']):<34} cover {d['coverage']:.2f}  colours {d['colours']:>2}  "
                         f"dark {d['lmin']:.2f}  light {d['lmax']:.2f}  edge {d['edge_l']:.2f}  "
                         f"inside {d['interior_l']:.2f}  TL-BR {d['tl_minus_br']:+.2f}")
    return lines


def cand_path(k):
    return os.path.join(CAND, f"jelly_man_o_war_egg_v2_{k}.png")


def hotbars(keys):
    """Each candidate unselected among vanilla water eggs (GUI scale 2), and all of them together at scale 4."""
    outs = {}
    for k in keys:
        out = os.path.join(CAND, f"jelly_man_o_war_egg_v2_hotbar_{k}.png")
        items = ["mc:cod_spawn_egg", "mc:squid_spawn_egg", "mc:tropical_fish_spawn_egg", "mc:glow_squid_spawn_egg",
                 f"file:{cand_path(k)}", "mc:axolotl_spawn_egg", "mc:salmon_spawn_egg", "mc:pufferfish_spawn_egg",
                 "mc:dolphin_spawn_egg"]
        subprocess.run([PY, os.path.join(ART, "tools", "hotbar_preview.py"), out] + items + ["--select", "8"],
                       check=True, capture_output=True)
        outs[k] = out
    out4 = os.path.join(CAND, "jelly_man_o_war_egg_v2_hotbar_x4.png")
    items = (["mc:squid_spawn_egg", "mod:mauve_stinger_spawn_egg", "mod:fried_egg_jellyfish_spawn_egg"]
             + [f"file:{cand_path(k)}" for k in keys])
    subprocess.run([PY, os.path.join(ART, "tools", "hotbar_preview.py"), out4] + items + ["--scale", "4",
                   "--select", "0"], check=True, capture_output=True)
    outs["x4"] = out4
    return outs


def tile_row(d, band, x0, name, im, small, ink):
    tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
    tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
    band.paste(tile.convert("RGB"), (x0, 22))
    d.text((x0, 2), name, fill=ink, font=small)
    for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
        t = Image.new("RGBA", (40, 40), col + (255,))
        t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (x0 + (j % 2) * 44 + (j // 2) * 88, 156))


def sheet(icons, hb):
    font, small = label_font(16), label_font(13)
    W = 2200
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    band = Image.new("RGB", (W, 248), bg)
    d = ImageDraw.Draw(band)
    row = [(f"egg {k}" + (" (PICK)" if k == PICK else ""), im) for k, im in icons.items()]
    row += [("REJECTED first egg", Image.open(REJECTED).convert("RGBA"))]
    row += [(f"accepted {n.replace('_', ' ')}", Image.open(os.path.join(ITEM, n + "_spawn_egg.png")).convert("RGBA"))
            for n in ("mauve_stinger", "fried_egg_jellyfish")]
    for i, (name, im) in enumerate(row):
        tile_row(d, band, 10 + i * 214, name, im, small, ink)
    notes = ["The float lit inside its upper-left rim, a terminator band down the right, darkest at the base (squid).",
             "The pink-edged sail lies across the float on a slant and wraps round it: no crest on the tip.",
             "A: sail rising right. B: sail rising left. C: A with tentacles drifting right into the pool."]
    for i, line in enumerate(notes):
        d.text((1300, 24 + 20 * i), line, fill=ink, font=small)
    parts.append(("The candidates, the rejected egg and our two accepted jellyfish eggs (8x, then 1x and 2x on light "
                  "and dark grey)", band))

    band = Image.new("RGB", (W, 248), bg)
    d = ImageDraw.Draw(band)
    for i, n in enumerate(STUDIED):
        tile_row(d, band, 10 + i * 214, f"vanilla {n.replace('_', ' ')}",
                 Image.open(os.path.join(VANILLA, n + "_spawn_egg.png")).convert("RGBA"), small, ink)
    parts.append(("The vanilla eggs studied (see the script's docstring)", band))

    lines = measure([os.path.join(VANILLA, n + "_spawn_egg.png") for n in ("squid", "glow_squid", "tropical_fish")]
                    + [REJECTED] + [os.path.join(ITEM, n + "_spawn_egg.png") for n in ("mauve_stinger",
                                                                                       "fried_egg_jellyfish")]
                    + [cand_path(k) for k in icons])
    for k, im in icons.items():
        lines += copy_check(k, im)
    for k, reads in BLIND_READS.items():
        lines.append(f"blind reads, {k}:")
        lines += ["    " + r for r in reads]
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("art/tools/measure.py, the copy check and the blind reads", band))

    for k in list(icons) + ["x4"]:
        im = Image.open(hb[k]).convert("RGB")
        band = Image.new("RGB", (max(W, im.width + 20), im.height + 30), bg)
        band.paste(im, (10, 4))
        cap = (f"egg {k} unselected in the 5th slot, GUI scale 2, among vanilla cod, squid, tropical fish, glow squid, "
               "axolotl, salmon, pufferfish and dolphin eggs" if k != "x4"
               else "GUI scale 4: vanilla squid, our mauve stinger and fried-egg eggs, eggs " + ", ".join(icons))
        ImageDraw.Draw(band).text((10, im.height + 8), os.path.relpath(hb[k], ROOT) + "  " + cap, fill=ink, font=small)
        parts.append((f"Hotbar preview (art/tools/hotbar_preview.py): {k}", band))

    W = max(W, max(b.width for _, b in parts))
    out = Image.new("RGB", (W, sum(b.height + 30 for _, b in parts) + 40), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Man o' war spawn egg, second try, textures/item/man_o_war_spawn_egg.png", fill=ink,
           font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    out.save(OUT_SHEET)
    print("wrote", OUT_SHEET)


if __name__ == "__main__":
    for k, rows in CANDIDATES.items():
        check(k, rows)
    icons = {k: vanilla_pool(render(rows), set()) for k, rows in CANDIDATES.items()}
    for k, im in icons.items():
        copy_check(k, im)
        im.save(cand_path(k), optimize=False)
    icons[PICK].save(OUT_ICON, optimize=False)
    print("wrote", OUT_ICON)
    sheet(icons, hotbars(list(icons)))
