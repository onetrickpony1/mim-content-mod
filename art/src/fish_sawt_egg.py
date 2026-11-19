"""Sawt (lesser weever, Echiichthys vipera) spawn egg: the item icon (16 x 16), 2026-11-19.

Started by the owner's rule (docs/Decisions/2026-11-18 Approving a step starts the next; skorfna bucket.md): the
sawt's bucket was approved, which starts its egg.

The owner's egg rules, all kept here:
- vanilla's egg outline (docs/Decisions/2026-11-18 Three eggs rejected - must be egg-shaped; cawl and shark buckets
  accepted.md), measured from vanilla 26.x's fish eggs (cod, salmon, pufferfish in art/.vanilla/item, never copied):
  a 4 px top on row 3 widening to 12 px on rows 8-12, its bottom edge on row 13 (x 5-10), and on rows 10-12 the
  one-pixel side flaps at x 1 and 14 that vanilla's fish eggs carry there;
- a stylised egg in the owner's preferred style from the boll (docs/Decisions/2026-11-18 Boll egg B; egg pools match
  vanilla.md): a plain egg in the animal's palette carrying only its key features, never the whole fish squeezed in
  (docs/Decisions/2026-11-18 Sardina egg - a representation, not a fat fish.md). For the sawt those are
  - the short jet-black venomous first dorsal fin (m a k) standing on the egg's top, its tallest spine in front;
  - the sandy-gold body, lit at the upper left (j f) into the back's brown (d n) at the lower right, with the cream
    belly (b) at the lower front;
  - in A and C, the fine oblique dark lines (i) on its flank;
  - the side flaps as the pale pectoral (l h) and the square yellow tail with its black edge (Y e a).
- no eye, no face, no pair of level dots (check_marks()); no band straight across the middle (a band read as a
  Pokéball).
- vanilla's own pool (art/src/egg_pool.py, the owner's exception to "never copy", for the pool only): P in the grids.

Colours: only those of the accepted icon, model texture and bucket (textures/item/sawt.png, entity/fish/sawt.png,
item/sawt_bucket.png; check_colours() fails on any other), plus vanilla's pool. Nothing new.

Candidates (the sheet shows all of them; PICK is written to the mod): see the comments at their grids.

Critic rounds (fresh critics, PASS or FAIL):
- round 1: FAIL, pick A ("it reads as an onion or garlic bulb with its stalk, or a fuse on a bomb"); D made from its
  fixes.
- round 2: FAIL on D ("A compact black blob on that shoulder ... reads as an eye or a cap"); E made from its fixes.
- round 3: PASS on E ("E's black is a slanted streak along the upper-left outline"). Its optional polish, not done:
  at most one spine pixel outside the outline, the top spine dark brown rather than black.
Blind reads (fresh readers, no context, the egg in slot 4 of a hotbar of vanilla eggs, GUI scale 4), first lines:
- D: "A pale tan or sand-coloured egg with dark blotches and what looks like an open mouth or head shape at the upper
  left. I read it as a sandy, camouflaged bottom fish, maybe a weever or a stargazer, or possibly a frog or toad." /
  "A spawn egg that is sandy tan with dark brown blotches and a dark eye-like mark near the top left. It reads as a
  mottled bottom fish, such as a grouper, a flatfish or a weever." / "A sandy tan, lumpy spawn egg with dark brown
  blotches near the top. ... It could also be mistaken for a bread roll or a potato".
- E (the pick): "a spawn egg for a sandy, tan creature with darker brown diagonal stripes and a small black tip at the
  top. ... a loaf of bread or a striped sandy-coloured fish, such as a bream" / "a spawn egg for a sand-coloured fish
  (beige or tan) with a dark tip or fin on top and dark streaks across the body. It suggests a sandy-bottom fish such
  as a weever or a flatfish." / "a tan or sandy spawn egg with dark brown diagonal streaks and speckles, and a small
  dark spike at the top left. ... My first guess is a mottled, sand-coloured fish or something that lies on the
  seabed."

Run:    art/.venv/bin/python art/src/fish_sawt_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/sawt_spawn_egg.png (the PICK, byte-identical on
        rerun), art/candidates/fish_sawt_egg.png (the compare sheet: the candidates at 8x, 1x and 2x beside
        vanilla's fish eggs, our accepted fish eggs and the sawt's own icon and bucket) and the offline hotbar
        previews art/candidates/fish_sawt_egg_hotbar.png and fish_sawt_egg_hotbar_x4.png
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

FISH = "sawt"
TITLE = "Sawt (lesser weever) spawn egg"
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


# the icon's and model's colours: the black fin m a k, the outline c (lit) and g (shade; o the egg's bottom edge),
# the gold body j f d n, the lines i, the cream belly b, the fins l h and the yellow tail Y e
PAL = {k: hx(v) for k, v in {
    "m": "#141210", "a": "#2e241a", "k": "#4a3a2a",
    "c": "#8a6c38", "g": "#6e5630", "o": "#6e5630",
    "j": "#e4cc88", "f": "#d4b468", "d": "#b08a48", "n": "#9c7a3e", "i": "#7a5e30", "b": "#f0e6c4",
    "l": "#c4a868", "h": "#b09455", "Y": "#f0c020", "e": "#c89818",
}.items()}
DARK = "makig"  # the marks check_marks() looks at

POOL = [
    "..PPPooooooPPP..",
    "..PPPPPPPPPPPP..",
    "...PPPPPPPPPP...",
]

# the body with the oblique lines (rows 4-12)
LINES = [
    ".....cjjffc.....",
    "....cjjfffdc....",
    "....cjffiddg....",
    "...cjffiddidg...",
    "..cjfdiddiddng..",
    "..cbbjfdiddnng..",
    ".lcbbbjiddnnngY.",
    ".lcbbbjjfdnnnge.",
    ".hcjbbjffdnnnga.",
]

CANDIDATES = {
    # A: the black fin on top, a front spine two pixels proud (6,1) and a second one (8,2) with black membrane
    # between, sloping to the back; the oblique lines on the flank
    "A": ["................",
          "......m.........",
          "......mam.......",
          "......makm......"] + LINES + POOL,
    # B: A's fin as a solid black sail, no lines: a plain gold egg
    "B": ["................",
          "......m.........",
          "......mak.......",
          "......maak......",
          ".....cjjffc.....",
          "....cjjfffdc....",
          "....cjfffddg....",
          "...cjffffdddg...",
          "..cjfffdddddng..",
          "..cbbjffddnnng..",
          ".lcbbbjfddnnngY.",
          ".lcbbbjjfdnnnge.",
          ".hcjbbjffdnnnga.",
          ] + POOL,
    # C: the fin set further forward, over the front shoulder (5,1)-(8,3), with the lines
    "C": ["................",
          ".....m..........",
          ".....mam........",
          ".....mamkc......"] + LINES + POOL,
    # D: critic round 1's fixes (A FAIL: the fin standing on the egg's top read as an onion's stalk or a fuse). The
    # fin lies flat on the upper front shoulder, never above the outline: black spines (5-6,4) (4-6,5), a sand notch
    # (7,4) between them and the trailing spine, its dark trailing edge (7,5) and base (4,6) in k; the egg's top
    # (row 3) is plain again. The tail low on the back side, yellow (13,10 Y; 13,11 e) with its black edge (14,10-11),
    # breaking the outline there; the oblique lines a tone darker (g); the belly cream (3,12 b).
    "D": ["................",
          "................",
          "................",
          "......cccc......",
          ".....mmjffc.....",
          "....mmmkffdc....",
          "....kjffiddg....",
          "...cjffgddgdg...",
          "..cjfdgddgddng..",
          "..cbbjfdgddnng..",
          ".lcbbbjgddnnnYm.",
          ".lcbbbjjfdnnnem.",
          ".hcbbbjffdnnnga.",
          ] + POOL,
    # E: critic round 2's fixes for D (FAIL: the closed black patch on the shoulder read as an eye or a cap): the fin
    # is a long diagonal run hugging the upper-front outline, (4,5) (5-6,4) (7,3), with two spines poking out a little
    # (5,3) (7,2) and the egg's own sand (6,3) between them, so its edge is serrated like rays; its base under it in
    # the line colour g (5-6,5) (7,4), joining it to the body's lines; no light pixel inside or right under the black
    "E": ["................",
          "................",
          ".......m........",
          ".....mfmcc......",
          ".....mmgffc.....",
          "....mggfffdc....",
          "....cjffiddg....",
          "...cjffgddgdg...",
          "..cjfdgddgddng..",
          "..cbbjfdgddnng..",
          ".lcbbbjgddnnnYm.",
          ".lcbbbjjfdnnnem.",
          ".hcbbbjffdnnnga.",
          ] + POOL,
}
OUTSIDE = {"A": {(6, 1), (6, 2), (7, 2), (8, 2)}, "B": {(6, 1), (6, 2), (7, 2), (8, 2)},
           "C": {(5, 1), (5, 2), (6, 2), (7, 2), (5, 3)}, "D": set(), "E": {(7, 2), (5, 3)}}
PICK = "E"

# vanilla's egg outline: (x from, x to) per row; the side flaps at x 1 and 14 on rows 10-12 are part of it
EGG = {3: (6, 9), 4: (5, 10), 5: (4, 11), 6: (4, 11), 7: (3, 12), 8: (2, 13), 9: (2, 13), 10: (1, 14), 11: (1, 14),
       12: (1, 14), 13: (2, 13), 14: (2, 13), 15: (3, 12)}


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
             [f"file:{tmp[n]}" for n in icons] + ["mod:skorfna_spawn_egg", "mod:cawl_spawn_egg", f"mod:{FISH}"])
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
                                  ", ".join(icons) + f"; our skorfna and cawl eggs; {FISH} icon)", fill=ink,
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
