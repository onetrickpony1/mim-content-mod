"""Kavall (chub mackerel, Scomber colias) spawn egg: the item icon (16 x 16), 2026-11-19.

Started by the owner's rule (docs/Decisions/2026-11-18 Approving a step starts the next; skorfna bucket.md): the
kavall's bucket was approved, which starts its egg.

The owner's egg rules, all kept here:
- vanilla's egg outline (docs/Decisions/2026-11-18 Three eggs rejected - must be egg-shaped; cawl and shark buckets
  accepted.md), measured from vanilla 26.x's fish eggs (cod, salmon, pufferfish in art/.vanilla/item, never copied):
  a 4 px top on row 3 widening to 12 px on rows 8-12, its bottom edge on row 13 (x 5-10), and on rows 10-12 the
  one-pixel side flaps at x 1 and 14 that vanilla's fish eggs carry there;
- a stylised egg in the owner's preferred style from the boll (docs/Decisions/2026-11-18 Boll egg B; egg pools match
  vanilla.md): a plain egg in the animal's palette carrying only its key features, never the whole fish squeezed in
  (docs/Decisions/2026-11-18 Sardina egg - a representation, not a fat fish.md). For the kavall those are
  - the dark tiger bars on its blue-green back: oblique 1 px lines in the icon's darkest teal K, wrapping over the
    egg's top and down its side as the back's bars do, the back lit at the upper left (g d) into the shade (e);
  - the silver flank and belly as a pale patch on the lower front, where vanilla's cod egg has its pale patch, lit
    at the left (n m) and rolling into grey (t w) toward the shaded back;
  - the side flaps as its olive-yellow pectoral fins (c i b), the colour of its finlets and tail;
  - in B only, the deeply forked olive-yellow tail poking out over the top right, as the sardina egg's tail does.
- no eye, no face, no pair of level dots; the silver is a patch, not a band across the middle (a band read as a
  Pokéball).
- vanilla's own pool (art/src/egg_pool.py, the owner's exception to "never copy", for the pool only): P in the grids.

Colours: only those of the accepted icon, model texture and bucket (textures/item/kavall.png, entity/fish/kavall.png,
item/kavall_bucket.png; check_colours() fails on any other), plus vanilla's pool. Nothing new.

Candidates (the sheet shows all of them; PICK is written to the mod): see the comments at their grids.

Critic rounds (fresh critics, PASS or FAIL):
- round 1: FAIL, pick B ("The bars read as a checker or net pattern, not wavy tiger bars ... almost the same as the
  incova egg"); B2 made from its fixes (some, like a bluer back, need colours the accepted art does not have).
- round 2: FAIL on B2 ("The bars don't read as bars ... At 1x and in the GUI-2 hotbar it turns into teal noise");
  B3 made from its fixes (solid 2 px bars).
- round 3: PASS on B3 ("the 2-px diagonal bars read as stripes at 1x and in both hotbars"). Its optional polish, not
  done: the outer tail tip a mid olive, the brightest silver one step down.
Blind reads (fresh readers, no context, the egg in slot 4 of a hotbar of vanilla eggs, GUI scale 4), first lines:
- B2: "A teal-green and white egg with a small fin or tail sticking out at the top right. I'd guess a green-backed
  fish, maybe a wrasse or a bream." / "A spawn egg: teal-green on top, white underneath, with a thin yellow spike or
  stalk sticking up from the top right. It reads as a fish, perhaps a mackerel- or dolphinfish-type fish" / "A spawn
  egg in teal-green with a pale white lower half and a thin yellowish stalk curling from the top."
- B3 (the pick): "a spawn egg for a fish. It is a chunky teal or blue-green fish with a pale underside ... it looks
  most like a mackerel- or tuna-type fish, or possibly a grouper." / "a spawn egg for a teal-green fish with a pale
  white belly ... It reads most like a blue-green, mackerel-type fish" / "It looks like a spawn egg for a fish. The
  fish is blue-green on top with a pale white belly ... and reminds me of a mackerel."

Run:    art/.venv/bin/python art/src/fish_kavall_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/kavall_spawn_egg.png (the PICK, byte-identical on
        rerun), art/candidates/fish_kavall_egg.png (the compare sheet: the candidates at 8x, 1x and 2x beside
        vanilla's fish eggs, our accepted fish eggs and the kavall's own icon and bucket) and the offline hotbar
        previews art/candidates/fish_kavall_egg_hotbar.png and fish_kavall_egg_hotbar_x4.png
        (art/tools/hotbar_preview.py, GUI scale 2 and 4, nothing selected).
"""
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
from egg_pool import POOL as VANILLA_POOL, is_pool, pool_line  # noqa: E402

FISH = "kavall"
TITLE = "Kavall (chub mackerel) spawn egg"
TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
ITEMS = os.path.join(TEXTURES, "item")
OUT_ICON = os.path.join(ITEMS, f"{FISH}_spawn_egg.png")
CAND = os.path.join(ART, "candidates")
OUT_SHEET = os.path.join(CAND, f"fish_{FISH}_egg.png")
OUT_HOTBAR = os.path.join(CAND, f"fish_{FISH}_egg_hotbar.png")
OUT_HOTBAR4 = os.path.join(CAND, f"fish_{FISH}_egg_hotbar_x4.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
SOURCES = [os.path.join(ITEMS, f"{FISH}.png"), os.path.join(TEXTURES, "entity", "fish", f"{FISH}.png"),
           os.path.join(ITEMS, f"{FISH}_bucket.png")]


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


# the icon's colours: the back's darkest teal K (outline over the back, the tiger bars), the slate belly rim O
# (outline over the silver; o the egg's bottom edge), the back lit to shade g d e, the silver n m j t w x v, the
# olive-yellow fins and tail a c i b
PAL = {k: hx(v) for k, v in {
    "K": "#24504f", "O": "#3d4a52", "o": "#3d4a52",
    "g": "#9db8b0", "d": "#599589", "e": "#3c7a6e", "q": "#4a7c72", "l": "#6f8f8c",
    "n": "#f6ffff", "m": "#dfe8e5", "j": "#c9d5d3", "t": "#c3d0ce", "w": "#a3b3b3", "x": "#96a7aa", "v": "#7d8e90",
    "a": "#d2ca84", "c": "#c7be79", "i": "#b8b172", "b": "#9a976a",
}.items()}
DARK = "K"  # the marks check_marks() looks at

POOL = [
    "..PPPooooooPPP..",
    "..PPPPPPPPPPPP..",
    "...PPPPPPPPPP...",
]

# the back with its bars (rows 3-8) over the silver patch on the lower front (rows 9-12)
BODY = [
    "......KKKK......",
    ".....KgddeK.....",
    "....KgdKddKK....",
    "....KgKddKdK....",
    "...KgKddKddKK...",
    "..KdKddKddKdeK..",
    "..OnmmKddKdeeK..",
    ".cOnmmmjKddeeOc.",
    ".iOnmmjjjtdeqOi.",
    ".bOmjjjttwweqOb.",
]

CANDIDATES = {
    # A: three oblique bars, each stepping one pixel forward a row, from the dorsal outline down to the silver
    "A": ["................"] * 3 + BODY + POOL,
    # B: A with the deeply forked olive-yellow tail over the top right (stalk 10-11,3, fork arms 11-12,2 and
    # 10,1 / 13,1)
    "B": ["................",
          "..........a..a..",
          "...........ca...",
          "......KKKKii...."] + BODY[1:] + POOL,
    # C: wavier, more upright bars (each one zig-zags), the bars running on into the shaded back, teal flaps
    "C": ["................"] * 3 + [
        "......KKKK......",
        ".....KgdKeK.....",
        "....KgKddKeK....",
        "....KdKdeKeK....",
        "...KgdKdeKeeK...",
        "..KdgKdKdeKeeK..",
        "..OnmmKdKddKeK..",
        ".lOnmmmjjKdeeOq.",
        ".lOnmmjjjtdeqOq.",
        ".qOmjjjttwweqOq.",
    ] + POOL,
    # B2: critic round 1's fixes for B (FAIL: the bars read as a checker, too close to the incova egg): two bold
    # bars on a plain back, each stepping back one pixel halfway down (6-7,5-8 and 9-10,5-8), a short third one on
    # the shaded side (11,7) (12,8); the fork tips in the darker olive b, the root brighter (a c); the silver patch
    # stepping into grey (t) before the back; two finlet pixels (12,9 i; 12,10 b) on the dark side; the belly's lower
    # right shaded grey (x v)
    "B2": ["................",
           "..........b..b..",
           "...........ca...",
           "......KKKKac....",
           ".....KgddeK.....",
           "....KgKddKeK....",
           "....KdKddKeK....",
           "...KgddKddKKK...",
           "..KdgddKddKeKK..",
           "..OnmmjtdddeiK..",
           ".cOnmmmjtddebOc.",
           ".iOnmmjjjtdeqOi.",
           ".bOmjjjttwxvqOb.",
           ] + POOL,
    # B3: critic round 2's fixes for B2 (FAIL: the bars still read as dots or a net, noise at 1x): the bars are solid
    # 2 px diagonal runs on plain teal, each stepping down and back a pixel a row: the main bar (6-7,5) to (9-10,8),
    # a short one from the dorsal outline (9,4) (10,5) and a short front one (4-5,8) (5,9); the brightest silver only
    # at the belly's upper left, its lowest row in the greys (j t w x v), so it is no white slab
    "B3": ["................",
           "..........b..b..",
           "...........ca...",
           "......KKKKac....",
           ".....KgdeKK.....",
           "....KgKKdeKK....",
           "....KddKKdeK....",
           "...KgdddKKdeK...",
           "..KdKKddeKKeeK..",
           "..OnmKjdddeeiK..",
           ".cOnmmjtddeebOc.",
           ".iOmmjjjtdeeqOi.",
           ".bOjjttwwxvqqOb.",
           ] + POOL,
}
# vanilla's egg outline: (x from, x to) per row; the side flaps at x 1 and 14 on rows 10-12 are part of it
EGG = {3: (6, 9), 4: (5, 10), 5: (4, 11), 6: (4, 11), 7: (3, 12), 8: (2, 13), 9: (2, 13), 10: (1, 14), 11: (1, 14),
       12: (1, 14), 13: (2, 13), 14: (2, 13), 15: (3, 12)}
# the only pixels allowed outside it
OUTSIDE = {"A": set(), "B": {(10, 1), (13, 1), (11, 2), (12, 2), (10, 3), (11, 3)}, "C": set()}
OUTSIDE["B2"] = OUTSIDE["B3"] = OUTSIDE["B"]
PICK = "B3"


def check_outline(name, rows):
    """The egg outline is filled, and nothing but the candidate's own extra parts lies outside it."""
    for y, row in enumerate(rows):
        lo, hi = EGG.get(y, (99, -1))
        for x, ch in enumerate(row):
            inside = lo <= x <= hi
            if (x, y) in OUTSIDE[name]:
                assert ch != "." and not inside, f"{name}: extra pixel ({x},{y})"
            else:
                assert (ch != ".") == inside, f"{name}: pixel ({x},{y}) breaks the egg outline"


def check_marks(name, rows):
    """No lone dark dot inside the body (rows 4-12, off the outline) with another one level with it 2-4 px away:
    a pair like that reads as eyes. A dark pixel touching another dark pixel (8-neighbour) is part of a line."""
    def dark(x, y):
        return 0 <= y < 16 and 0 <= x < 16 and rows[y][x] in DARK

    def lone(x, y):
        return dark(x, y) and not any(dark(x + a, y + b) for a in (-1, 0, 1) for b in (-1, 0, 1) if a or b)

    for y in range(4, 13):
        lo, hi = EGG[y]
        dots = [x for x in range(lo + 1, hi) if lone(x, y)]
        for p in dots:
            for q in dots:
                assert not 2 <= q - p <= 4, f"{name}: dark dots at ({p},{y}) and ({q},{y}) read as a pair of eyes"


def check_colours():
    """Every colour is the accepted icon's, model texture's or bucket's (nothing new)."""
    seen = set()
    for f in SOURCES:
        im = Image.open(f).convert("RGBA")
        seen |= {im.getpixel((x, y))[:3] for x in range(im.width) for y in range(im.height) if im.getpixel((x, y))[3]}
    new = {k: v for k, v in PAL.items() if v not in seen}
    assert not new, f"colours not in the accepted art: {new}"


def render(rows):
    assert len(rows) == 16
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch == "P":
                im.putpixel((x, y), VANILLA_POOL[(x, y)] + (255,))
            elif ch != ".":
                im.putpixel((x, y), PAL[ch] + (255,))
    return im


def measure(paths):
    py = os.path.join(ART, ".venv", "bin", "python")
    res = subprocess.run([py, os.path.join(ART, "tools", "measure.py")] + paths, capture_output=True, text=True)
    lines = []
    for line in res.stdout.splitlines():
        if line.startswith("{"):
            d = eval(line, {"np": __import__("numpy")})  # measure.py prints dicts with numpy floats
            lines.append(f"{d['file']:<30} cover {d['coverage']:.2f}  colours {d['colours']:>2}  dark {d['lmin']:.2f}  "
                         f"light {d['lmax']:.2f}  edge {d['edge_l']:.2f}  inside {d['interior_l']:.2f}  "
                         f"TL-BR {d['tl_minus_br']:+.2f}")
    return lines


def copy_check(name, icon):
    """Exact-pixel copy check against every vanilla spawn egg (as the other fish egg scripts). Vanilla's own pool
    pixels are allowed (the owner's exception, art/src/egg_pool.py); any other copied pixel fails the run."""
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
    shared = {c[:3] for p, c in ours.items() if not is_pool(p, c)} & vcols
    hits.sort(reverse=True)
    most = f"most: {hits[0][0]} in {hits[0][1]}" if hits else "none"
    return (f"{name}: same pixel and colour as a vanilla spawn egg, besides its pool: {sum(n for n, _ in hits)} pixels "
            f"over {len(hits)} eggs ({most}); our colours (besides the pool) also used by any vanilla spawn egg: "
            f"{len(shared)}; {pool_line(icon)}"), sum(n for n, _ in hits)


def tmp_paths(icons):
    return {n: os.path.join(CAND, f"fish_{FISH}_egg_{n}.tmp.png") for n in icons}


# our accepted fish eggs shown beside the candidates (those that exist)
OURS = ["boll", "cerna", "skorfna", "incova", "sardina", "lampuka", "tonn", "awrata", "cawl", "murina"]


def hotbars(icons):
    """Offline hotbar previews, nothing selected: vanilla cod, pufferfish, tropical fish eggs, the candidates, our
    incova and sardina eggs, the fish's own icon."""
    py = os.path.join(ART, ".venv", "bin", "python")
    tmp = tmp_paths(icons)
    for n, im in icons.items():
        im.save(tmp[n])
    items = (["mc:cod_spawn_egg", "mc:pufferfish_spawn_egg", "mc:tropical_fish_spawn_egg"] +
             [f"file:{tmp[n]}" for n in icons] + ["mod:incova_spawn_egg", "mod:sardina_spawn_egg", f"mod:{FISH}"])
    try:
        for out, scale in ((OUT_HOTBAR, 2), (OUT_HOTBAR4, 4)):
            subprocess.run([py, os.path.join(ART, "tools", "hotbar_preview.py"), out] + items[:9] +
                           ["--scale", str(scale)], check=True, capture_output=True)
    finally:
        for p in tmp.values():
            os.remove(p)


def sheet(icons):
    font, small = label_font(16), label_font(13)
    W = 2400
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    def van(n):
        return Image.open(os.path.join(VANILLA, n + ".png")).convert("RGBA")

    def ours(n):
        return Image.open(os.path.join(ITEMS, n + ".png")).convert("RGBA")

    bucket = van("cod_bucket")
    bucket.alpha_composite(ours(f"{FISH}_bucket"))
    items = ([(f"CANDIDATE {n}{' (PICK)' if n == PICK else ''}", im) for n, im in icons.items()] +
             [(f"{FISH} icon (accepted)", ours(FISH)), (f"{FISH} bucket (accepted)", bucket)] +
             [(f"vanilla {n.replace('_', ' ')} egg", van(n + "_spawn_egg"))
              for n in ("cod", "salmon", "pufferfish", "tropical_fish")] +
             [(f"our {n} egg", ours(n + "_spawn_egg")) for n in OURS
              if os.path.exists(os.path.join(ITEMS, n + "_spawn_egg.png"))])
    per = 10
    for start in range(0, len(items), per):
        chunk = items[start:start + per]
        band = Image.new("RGB", (W, 128 + 110), bg)
        d = ImageDraw.Draw(band)
        for i, (name, im) in enumerate(chunk):
            x0 = 10 + i * 236
            tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
            tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
            band.paste(tile.convert("RGB"), (x0, 22))
            d.text((x0, 2), name, fill=ink, font=small)
            for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1),
                                          ((40, 40, 40), 2))):
                t = Image.new("RGBA", (40, 40), col + (255,))
                t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
                band.paste(t.convert("RGB"), (x0 + j * 44, 156))
        d.text((10, 204), "8x, then 1x and 2x on the slot grey, 1x and 2x on dark grey", fill=ink, font=small)
        parts.append((f"The candidates at 8x, 1x and 2x beside the accepted {FISH} icon and bucket, vanilla's fish "
                      "eggs and our accepted fish eggs" if start == 0 else "(continued)", band))

    tmp = tmp_paths(icons)
    for n, im in icons.items():
        im.save(tmp[n])
    lines = measure([os.path.join(VANILLA, n + "_spawn_egg.png") for n in ("cod", "salmon", "pufferfish")]
                    + [os.path.join(ITEMS, n + "_spawn_egg.png") for n in ("boll", "skorfna")] + list(tmp.values()))
    for p in tmp.values():
        os.remove(p)
    lines += [copy_check(n, im)[0] for n, im in icons.items()]
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("art/tools/measure.py and the copy check", band))

    for out, scale in ((OUT_HOTBAR, 2), (OUT_HOTBAR4, 4)):
        im = Image.open(out).convert("RGB")
        band = Image.new("RGB", (W, im.height + 30), bg)
        band.paste(im, (10, 4))
        ImageDraw.Draw(band).text((10, im.height + 8), os.path.relpath(out, ROOT) + f"  (GUI scale {scale}, nothing "
                                  "selected: vanilla cod, pufferfish, tropical fish eggs; CANDIDATES " +
                                  ", ".join(icons) + f"; our incova and sardina eggs; {FISH} icon)", fill=ink,
                                  font=small)
        parts.append((f"Hotbar preview (art/tools/hotbar_preview.py, GUI scale {scale})", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), f"{TITLE}: textures/item/{FISH}_spawn_egg.png", fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    out.save(OUT_SHEET)
    print("wrote", os.path.relpath(OUT_SHEET, ROOT))


if __name__ == "__main__":
    check_colours()
    for n, g in CANDIDATES.items():
        check_outline(n, g)
        check_marks(n, g)
    icons = {n: render(g) for n, g in CANDIDATES.items()}
    for n, im in icons.items():
        line, n_same = copy_check(n, im)
        assert n_same == 0, line
    icons[PICK].save(OUT_ICON, optimize=False)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), f"(candidate {PICK})")
    os.makedirs(CAND, exist_ok=True)
    hotbars(icons)
    sheet(icons)
