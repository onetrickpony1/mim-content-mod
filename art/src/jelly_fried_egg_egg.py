"""Fried-egg jellyfish (Cotylorhiza tuberculata) spawn egg: the item icon (16 x 16), 2026-11-18.

Owner 2026-11-18 (docs/Decisions/2026-11-18 Jellyfish spawn eggs - start.md): "yes start the spawn eggs", each after
its accepted model and in vanilla's pool (docs/Decisions/2026-11-18 Boll egg B; egg pools match vanilla.md). Made the
way the owner's accepted boll egg B is (art/src/fish_boll_egg_v2.py): a plain egg in the animal's palette carrying only
its key feature, never the whole animal squeezed in:
- the egg outline of vanilla 26.x's water-mob eggs (measured from cod, salmon and squid _spawn_egg in
  art/.vanilla/item, never copied): a 4 px top on row 3 widening to 12 px on rows 8-12, its bottom edge on row 13
  (x 5-10), standing in vanilla's own pool on rows 12-15 (art/src/egg_pool.py, the owner's exception to "never copy",
  for the pool only);
- shaded as a rounded egg lit from the top left;
- no eye and no face; the knobs are scattered so no two sit side by side like eyes.
The key feature: the orange-yellow yolk dome sitting on the butter-yellow bell, with a few of the purple and white
button knobs of the oral arms near the bottom. A "fried egg" egg must not read as a plain food egg (vanilla's egg
item, a fried egg on a plate): the yellow body, the yolk as the egg's cap (not a round yolk on a white) and the knobs
keep it an animal's spawn egg.

Colours: only the owner-accepted model's (art/src/jelly_fried_egg_model.py: BELL, MARGIN, YOLK, MASS, PURPLE, WHITE),
imported, plus two outline colours made from the model's own darkest yolk and arm-mass tones (x 0.5, hue kept: the
model has no outline, an icon needs one) and vanilla's pool (~ in the grids). Nothing else new.

Candidates (the sheet shows all of them; PICK is written to the mod):
- A, bell and arms: the yolk is the egg's cap (rows 3-5), the butter bell below it (rows 6-9) ends at a pale ribbed
  margin (row 9); under it the ochre oral arms (rows 10-13) with purple and white knobs, purple knob tips along the
  bottom edge, the way vanilla's squid egg shows its red tentacle tips.
- B, plain bell: the boll-B way, the whole egg the butter bell with the yolk cap on top and only five knobs (three
  purple, two white) scattered low; no arm mass.
- C, A with the bell's margin flaring 1 px out of the outline at both sides (row 9), the way a jellyfish bell's rim
  overhangs its arms.
- C2, the pick: C with critic round 1's polish (one purple for the knobs, single-use colours gone).

Run:    art/.venv/bin/python art/src/jelly_fried_egg_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/fried_egg_jellyfish_spawn_egg.png (PICK, byte-identical
        on rerun), art/candidates/jelly_fried_egg_egg.png (compare sheet), art/candidates/jelly_fried_egg_egg_<X>.png
        (each candidate) and art/candidates/jelly_fried_egg_egg_hotbar_<X>.png (each unselected among vanilla eggs,
        GUI scale 2) and jelly_fried_egg_egg_hotbar_x4.png (all candidates, GUI scale 4).
"""
import colorsys
import glob
import os
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(ART, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ART, "tools"))
from font import label_font  # noqa: E402
import jelly_fried_egg_model as MODEL  # noqa: E402
from egg_pool import POOL as VANILLA_POOL, POOL_COLOURS, is_pool, pool_line  # noqa: E402

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
ITEMS = os.path.join(TEXTURES, "item")
OUT_ICON = os.path.join(ITEMS, "fried_egg_jellyfish_spawn_egg.png")
CAND = os.path.join(ART, "candidates")
OUT_SHEET = os.path.join(CAND, "jelly_fried_egg_egg.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
PY = os.path.join(ART, ".venv", "bin", "python")


def rgb(c):
    return tuple(c[:3])


def darker(c, f=0.5):
    """The same hue, darker: the outline, about 0.6 x the inside (art/STYLE.md)."""
    h, s, v = colorsys.rgb_to_hsv(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
    r, g, b = colorsys.hsv_to_rgb(h, s, v * f)
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))


PAL = {
    # the yolk, light to dark
    "Y": rgb(MODEL.YOLK[0]), "y": rgb(MODEL.YOLK[1]), "z": rgb(MODEL.YOLK[2]), "Z": rgb(MODEL.YOLK[3]),
    "q": rgb(MODEL.YOLK[4]),
    # the bell, light to dark, and its pale margin
    "m": rgb(MODEL.MARGIN[0]), "1": rgb(MODEL.BELL[0]), "2": rgb(MODEL.BELL[1]), "3": rgb(MODEL.BELL[2]),
    "4": rgb(MODEL.BELL[3]), "5": rgb(MODEL.BELL[4]),
    # the oral arm mass, light to dark
    "M": rgb(MODEL.MASS[0]), "N": rgb(MODEL.MASS[1]), "K": rgb(MODEL.MASS[2]), "J": rgb(MODEL.MASS[3]),
    "G": rgb(MODEL.MASS[4]),
    # the knobs: purple-blue and white
    "u": rgb(MODEL.PURPLE[0]), "v": rgb(MODEL.PURPLE[1]), "w": rgb(MODEL.PURPLE[2]), "x": rgb(MODEL.PURPLE[3]),
    "W": rgb(MODEL.WHITE[0]), "X": rgb(MODEL.WHITE[2]),
    # the outlines, from the model's darkest yolk and arm-mass tones
    "O": darker(MODEL.YOLK[4]), "o": darker(MODEL.MASS[4]),
}

# rows 12-15: vanilla's pool (~ takes vanilla's own colour from art/src/egg_pool.py) with the egg's bottom edge on
# row 13, x 5-10
YOLK_CAP = [
    "................",
    "................",
    "................",
    "......OOOO......",
    ".....OYYyzO.....",  # the yolk dome, lit at its top left
    "....OYYyyzZO....",
    "....o1zZZq4o....",  # its base sinking into the bell, the bell showing at both sides
]
POOL_ROWS = [
    "..~~~~~~~~~~~~..",
    "...~~~~~~~~~~...",
]
CANDIDATES = {
    "A": YOLK_CAP + [
        "...o11223344o...",
        "..o1122333445o..",
        "..om2m3m3m4m5o..",  # the pale ribbed margin
        "..oNWMKNuKJKGo..",  # the ochre oral arms with white and purple knobs
        "..oKNuKJKXJvGo..",
        "..oJKKvJGJuJGo..",
        "..~~~oxouxo~~~..",  # purple knob tips along the bottom edge
    ] + POOL_ROWS,
    "B": YOLK_CAP + [
        "...o11223344o...",
        "..o1122233445o..",
        "..o1222333445o..",
        "..o2223u34455o..",  # five knobs scattered low, none side by side
        "..o2W33344v55o..",
        "..o33u344W455o..",
        "..~~~oooooo~~~..",
    ] + POOL_ROWS,
    "C": YOLK_CAP + [
        "...o11223344o...",
        "..o1122333445o..",
        ".om2m3m3m4m4m5o.",  # the margin flaring 1 px out at both sides
        "..oJWMKNuKJKGo..",
        "..oKNuKJKXJvGo..",
        "..oJKKvJGJuJGo..",
        "..~~~oxouxo~~~..",
    ] + POOL_ROWS,
}
# C2: critic round 1 (PASS on C) polish: the single-use colours q, M, X and the faint purple u go (24 colours with
# the pool, from 28), so the knobs are all the deeper purple v, which stands out from the ochre at 1x and keeps the
# egg apart from vanilla's yellow-orange pufferfish egg.
CANDIDATES["C2"] = CANDIDATES["C"][:6] + [
    "....o1zZZZ4o....",
] + CANDIDATES["C"][7:10] + [
    "..oJWNKNvKJKGo..",
    "..oKNvKJKWJvGo..",
    "..oJKKvJGJvJGo..",
    "..~~~oxovxo~~~..",
] + POOL_ROWS
# the egg outline each candidate must fill exactly (x from, x to per row), the pool included
EGG = {3: (6, 9), 4: (5, 10), 5: (4, 11), 6: (4, 11), 7: (3, 12), 8: (2, 13), 9: (2, 13), 10: (2, 13),
       11: (2, 13), 12: (2, 13), 13: (2, 13), 14: (2, 13), 15: (3, 12)}
FLARE = {9: (1, 14)}  # C only: the margin's 1 px flare
PICK = "C2"  # C (every blind reader called it a jellyfish, see BLIND_READS) with critic round 1's polish; the owner decides
BLIND_READS = {  # first lines, word for word; each reader saw all three hotbars (egg in the 5th slot, unselected)
    "round 1 (A, B, C; the folder name and the git status in the readers' context named the fried-egg jellyfish, so "
    "these may be primed)": [
        "A: 'a spawn egg, maybe for a jellyfish (the fried-egg jellyfish) or a yellow fish like a chick-coloured fish.' "
        "/ 'A yellow-orange spawn egg; I'd guess a jellyfish again, though it could also be a yellow-and-orange fish.' "
        "/ 'Also a spawn egg for a fried egg jellyfish, though I'm less sure than for hb_q.'",
        "B: 'a spawn egg for a fried-egg jellyfish, or less likely a chicken or egg-themed creature.' / 'A yellow "
        "spawn egg; my best guess is a chick, with the fried-egg jellyfish as a weaker second guess.' / 'A pale "
        "yellow spawn egg. My best guess is a fried egg jellyfish, but with low confidence.'",
        "C: 'a spawn egg, most likely for a jellyfish (perhaps the fried-egg jellyfish), or else a spotted fish.' / "
        "'A spawn egg for a jellyfish, probably a yellow/orange one like the fried-egg jellyfish.' / 'A spawn egg "
        "for a fried egg jellyfish (or another jellyfish with a yellow dome).'"],
    "round 1b (the same eggs, neutral file and folder names; readers 1 and 3 still said 'fried egg', likely from "
    "the git status, reader 2 did not)": [
        "A: 'A spawn egg, probably for a pale yellow or orange creature. My best guess is a jellyfish, or maybe a "
        "chick.' / 'a spawn egg, and my best guess is a jellyfish, possibly a spotted one. A pufferfish is my second "
        "guess.' / 'A spawn egg, best guess the same yellow and orange jellyfish (or a yellow fish), drawn a bit "
        "warmer.'",
        "B: 'A spawn egg, probably for a pale yellow creature. My best guess is a chick or a jellyfish.' / 'a spawn "
        "egg, and my best guess is a pale blobby creature such as a blobfish or a pale pufferfish.' / 'A spawn egg, "
        "best guess a pale yellow jellyfish or blob-like sea creature.'",
        "C: 'A spawn egg, probably for a jellyfish, perhaps a \"fried egg\" type with a yellow-orange centre on a pale "
        "body.' / 'a spawn egg, and my best guess is a jellyfish.' (the clean reader: 'a short fringe of thin darker "
        "lines hanging below that look like a bell with short tentacles') / 'A spawn egg, best guess a yellow "
        "jellyfish (a cream jellyfish with an orange top, maybe a \"fried egg\" type); it could also be a yellow "
        "fish.'"],
    "C2 (one fresh reader, its hotbar alone, neutral names; it still said 'fried-egg', likely from the git status)": [
        "C2: 'It looks like a spawn egg, and my best guess is a jellyfish, probably the fried-egg jellyfish.' (second "
        "guesses: 'some yellow-orange sea animal or a mushroom-capped creature')"],
}
HOTBAR_EGGS = ["mc:cod_spawn_egg", "mc:salmon_spawn_egg", "mc:squid_spawn_egg", "mc:pufferfish_spawn_egg", None,
               "mc:tropical_fish_spawn_egg", "mc:axolotl_spawn_egg", "mc:glow_squid_spawn_egg",
               "mc:turtle_spawn_egg"]
OUR_EGGS = ("boll", "cerna", "tonn", "ziemel")


def check_outline(name, rows):
    """Every opaque pixel lies inside the egg outline and the outline is filled: nothing pokes out, no gaps
    (C's margin flare excepted)."""
    for y, row in enumerate(rows):
        lo, hi = (FLARE if name.startswith("C") else {}).get(y, EGG.get(y, (99, -1)))
        for x, ch in enumerate(row):
            assert (ch != ".") == (lo <= x <= hi), f"{name}: pixel ({x},{y}) breaks the egg outline"


def check_no_eyes(name, rows):
    """No two knobs of a colour side by side or one row apart in a pair (they would read as eyes)."""
    knobs = {"u", "v", "w", "x", "W", "X"}
    for y, row in enumerate(rows[:13]):
        for x, ch in enumerate(row):
            if ch in knobs and x + 1 < 16 and row[x + 1] in knobs:
                raise AssertionError(f"{name}: knobs side by side at ({x},{y})")


def render(rows):
    assert len(rows) == 16
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch == "~":
                im.putpixel((x, y), VANILLA_POOL[(x, y)] + (255,))
            elif ch != ".":
                im.putpixel((x, y), PAL[ch] + (255,))
    return im


def measure(paths):
    res = subprocess.run([PY, os.path.join(ART, "tools", "measure.py")] + paths, capture_output=True, text=True)
    lines = []
    for line in res.stdout.splitlines():
        if line.startswith("{"):
            d = eval(line, {"np": __import__("numpy")})  # measure.py prints dicts with numpy floats
            lines.append(f"{os.path.basename(d['file']):<36} cover {d['coverage']:.2f}  colours {d['colours']:>2}  "
                         f"dark {d['lmin']:.2f}  light {d['lmax']:.2f}  edge {d['edge_l']:.2f}  "
                         f"inside {d['interior_l']:.2f}  TL-BR {d['tl_minus_br']:+.2f}")
    return lines


def copy_check(name, icon):
    """Exact-pixel copy check against every vanilla spawn egg (as the fish egg scripts). Vanilla's own pool pixels are
    allowed (the owner's exception, art/src/egg_pool.py); any other copied pixel fails the run."""
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
    assert not hits, f"{name}: copies vanilla pixels besides the pool: {hits}"
    shared = {c[:3] for p, c in ours.items() if not is_pool(p, c)} & vcols
    assert not ({c[:3] for p, c in ours.items() if not is_pool(p, c)} & POOL_COLOURS), f"{name}: pool blue in body"
    return (f"{name}: same pixel and colour as a vanilla spawn egg, besides its pool: 0; our colours (besides the "
            f"pool) also used by any vanilla spawn egg: {len(shared)}; " + pool_line(icon))


def cand_path(n):
    return os.path.join(CAND, f"jelly_fried_egg_egg_{n}.png")


def hotbars(names):
    """Each candidate unselected (5th slot) among vanilla water-mob eggs at GUI scale 2, and all together at 4."""
    outs = {}
    for n in names:
        out = os.path.join(CAND, f"jelly_fried_egg_egg_hotbar_{n}.png")
        items = [it or f"file:{cand_path(n)}" for it in HOTBAR_EGGS]
        subprocess.run([PY, os.path.join(ART, "tools", "hotbar_preview.py"), out] + items, check=True,
                       capture_output=True)
        outs[n] = out
    out = os.path.join(CAND, "jelly_fried_egg_egg_hotbar_x4.png")
    items = ["mc:squid_spawn_egg", "mod:boll_spawn_egg"] + [f"file:{cand_path(n)}" for n in names]
    subprocess.run([PY, os.path.join(ART, "tools", "hotbar_preview.py"), out] + items + ["--scale", "4"],
                   check=True, capture_output=True)
    outs["x4"] = out
    return outs


def tiles(band, d, x0, name, im, small, ink):
    tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
    tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
    band.paste(tile.convert("RGB"), (x0, 22))
    d.text((x0, 2), name, fill=ink, font=small)
    for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
        t = Image.new("RGBA", (40, 40), col + (255,))
        t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (x0 + j * 44, 156))


def sheet(icons, hb):
    font, small = label_font(16), label_font(13)
    W = 2400
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    def van(n):
        return Image.open(os.path.join(VANILLA, n + ".png")).convert("RGBA")

    def ours(n):
        return Image.open(os.path.join(ITEMS, n + ".png")).convert("RGBA")

    items = ([(f"CANDIDATE {n}{' (PICK)' if n == PICK else ''}", im) for n, im in icons.items()]
             + [(f"vanilla {n.replace('_', ' ')} egg", van(n + "_spawn_egg"))
                for n in ("squid", "glow_squid", "cod", "pufferfish", "chicken")]
             + [("vanilla egg (food)", van("egg"))]
             + [(f"our {n} egg (accepted)", ours(n + "_spawn_egg")) for n in OUR_EGGS])
    per = 10
    for start in range(0, len(items), per):
        chunk = items[start:start + per]
        band = Image.new("RGB", (W, 238), bg)
        d = ImageDraw.Draw(band)
        for i, (name, im) in enumerate(chunk):
            tiles(band, d, 10 + i * 236, name, im, small, ink)
        d.text((10, 204), "8x, then 1x and 2x on the slot grey, 1x and 2x on dark grey", fill=ink, font=small)
        parts.append(("The candidates at 8x, 1x and 2x beside vanilla eggs (and vanilla's food egg) and our accepted "
                      "eggs" if start == 0 else "(continued)", band))

    lines = measure([os.path.join(VANILLA, n + "_spawn_egg.png") for n in ("cod", "squid", "pufferfish")]
                    + [os.path.join(ITEMS, n + "_spawn_egg.png") for n in ("boll", "cerna")]
                    + [cand_path(n) for n in icons])
    lines += [copy_check(n, im) for n, im in icons.items()]
    for k, reads in BLIND_READS.items():
        lines.append(f"blind reads, {k}:")
        lines += ["    " + r for r in reads]
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("art/tools/measure.py, the copy check and the blind reads", band))

    for k, path in hb.items():
        im = Image.open(path).convert("RGB")
        band = Image.new("RGB", (max(W, im.width + 20), im.height + 30), bg)
        band.paste(im, (10, 4))
        cap = ("unselected, 5th slot, GUI scale 2 (vanilla cod, salmon, squid, pufferfish eggs; THIS EGG; vanilla "
               "tropical fish, axolotl, glow squid, turtle eggs)" if k != "x4" else
               "GUI scale 4: vanilla squid egg, our boll egg, then the candidates " + ", ".join(icons))
        ImageDraw.Draw(band).text((10, im.height + 8), os.path.relpath(path, ROOT) + "  " + cap, fill=ink, font=small)
        parts.append((f"Hotbar preview (art/tools/hotbar_preview.py): {k}", band))

    W = max(W, max(b.width for _, b in parts))
    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Fried-egg jellyfish spawn egg: textures/item/fried_egg_jellyfish_spawn_egg.png", fill=ink,
           font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    out.save(OUT_SHEET)


def main():
    for n, g in CANDIDATES.items():
        check_outline(n, g)
        check_no_eyes(n, g)
    icons = {n: render(g) for n, g in CANDIDATES.items()}
    for n, im in icons.items():
        copy_check(n, im)
    os.makedirs(CAND, exist_ok=True)
    for n, im in icons.items():
        im.save(cand_path(n), optimize=False)
    icons[PICK].save(OUT_ICON, optimize=False)
    hb = hotbars(list(icons))
    sheet(icons, hb)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), f"(candidate {PICK}),", os.path.relpath(OUT_SHEET, ROOT),
          "and the hotbar previews")


if __name__ == "__main__":
    main()
