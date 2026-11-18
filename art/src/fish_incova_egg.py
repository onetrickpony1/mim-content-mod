"""Incova spawn egg: the item icon (16 x 16), round 4 (round 3 redesign with the critic's fixes), 2026-11-18.

The pool (owner 2026-11-18, "the pool under the egg should be the same as vanilla"; docs/Decisions/2026-11-18 Boll
egg B; egg pools match vanilla.md): the pool drawn in the grid below is our old one. vanilla_pool() swaps it for
vanilla's own pool (art/src/egg_pool.py, the owner's exception to "never copy", for the pool only) before the egg
is written, keeping every body pixel; what is said below about our own pool is its history.

The owner rejected the round 2 egg (decision "2026-11-18 Three eggs rejected - must be egg-shaped; cawl and shark
buckets accepted"): "incova egg looks like a pokeball/dolphin mix". Its white band straight across the middle read
as a Pokeball and its pointed snout as a dolphin. This redesign starts from vanilla's EGG outline (measured from
vanilla's cod egg, never copied): a narrow top widening downwards, rows 3 to 12, sitting in its own small pool on
rows 13 to 15. The anchovy's look is painted ON the egg, the vanilla 26.x way:
- a greenish-blue cap in the accepted icon's greens (h T u m k), lit on its upper left and darker to the right,
  coming down lower at the front (round the eye) and at the back than in the middle, so its edge curves like a helmet
  and is never one straight line;
- one black eye high on the front, touched only by mid and dark greens;
- silver sides (s J g) shading to the lower right, with a small pale belly patch (p) at the lower front;
- the silver lateral band only as a short stripe set on the green on the back half (row 8, x 8 to 10), with the cap
  curving down behind it to the right-hand edge: no full-width stripe and no white (it peaks at the pale silver p);
- small shaded side fin flaps low on both sides (rows 10 to 12), so the egg widens downwards like vanilla's;
  no snout, nothing on top.
It reads apart from the accepted sardina egg: a lighter, greener cap (the sardina's is dark teal), grey silver sides
rather than a white lower half, no gold, and no dorsal fin or tail on top.
Round 3's version A (critic: FIX) and options B (no band, a small dorsal flap) and C (band and dorsal flap, no side fins) are kept for the sheet. A won:
it is the only one that shows the anchovy's stripe without a part on top like the sardina's.
Colours are exactly the owner-accepted incova item icon's (art/src/fish_incova_icon.py PAL, same keys, nothing new),
plus the pool: our own ramp of slate-to-azure blues, shared with no vanilla egg and no other egg of ours.
Photos (reference only): art/references/fish_incova_refonly/ (list.tsv).

Run:    art/.venv/bin/python art/src/fish_incova_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/incova_spawn_egg.png (byte-identical on rerun),
        art/candidates/fish_incova_egg.png (compare sheet) and the offline hotbar previews
        art/candidates/fish_incova_egg_hotbar.png (GUI scale 2) and fish_incova_egg_hotbar_x4.png (scale 4).
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
sys.path.insert(0, HERE)
from font import label_font  # noqa: E402
from egg_pool import POOL_COLOURS, is_pool, pool_line, vanilla_pool  # noqa: E402
from fish_incova_icon import PAL as ICON  # noqa: E402

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
OUT_ICON = os.path.join(TEXTURES, "item", "incova_spawn_egg.png")
OUT_SHEET = os.path.join(ART, "candidates", "fish_incova_egg.png")
OUT_HOTBAR = os.path.join(ART, "candidates", "fish_incova_egg_hotbar.png")
OUT_HOTBAR4 = os.path.join(ART, "candidates", "fish_incova_egg_hotbar_x4.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_incova_refonly")
PY = os.path.join(ART, ".venv", "bin", "python")
OUR_EGGS = ("lampuka", "tonn", "sardina", "cerna", "awrata", "murina")  # the owner-accepted eggs


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# The incova: the owner-accepted icon's palette, same keys and values (only those used here).
# Cap ramp, lit to dark: h (lit green sheen), T, u, m, k (dark blue-green back); f the snout tip and dorsal fin,
# F the fin's lit tip; W the silver band, p the pale belly patch, s silver, g grey silver, o shaded rim;
# e the eye; j and J the mouth line; a the side fins.
PAL = {k: ICON[k] for k in "hTumkfFWpsgoejJa"}
PAL.update({
    # the old pool (now swapped for vanilla's): our own ramp of slate-to-azure blues
    "1": hx("#1b3048"),
    "2": hx("#26517a"),
    "3": hx("#3170a0"),
    "4": hx("#4893c0"),
    "5": hx("#8ccde8"),
})
# Our own old pool's colours: vanilla_pool() takes them out and puts vanilla's pool in (owner 2026-11-18,
# "the pool under the egg should be the same as vanilla"; art/src/egg_pool.py).
OLD_POOL = {PAL[k] for k in "12345"}
POOL_KEYS = "12345"

POOL = [
    "..34oooooooo43..",
    ".12455343554321.",
    "..12211.122211..",
]
# The cap: lit top-left (h T), mid greens (u m), dark blue-green (k) at the top and right; the eye at 5,7.
CAP = [
    "................",
    "................",
    "................",
    "......kmmk......",
    ".....mThTuk.....",
    "....mThhTumk....",
    "....muuTuumk....",
    "...muemmuumkk...",
]
CAP_DORSAL = CAP[:2] + [".......Ff......."] + CAP[3:]

# Round 3, option A (critic: FIX, fins at mid-height so it didn't widen downwards, the stripe lost in the belly
# line, a near-straight cap edge), kept only for the sheet.
ROUND3_GRID = CAP + [
    "...mmmmsssmkk...",
    "..aspsJgJsppoa..",
    "..aJppsJgggsoa..",
    "...gJpsJggggo...",
    "....gJJgggoo....",
] + POOL

# Round 4 (chosen, the critic's fixes): the fin flaps moved low (rows 10-12 run 2-13, 1-14, 1-14, so the egg widens
# downwards like vanilla's), the silver stripe on green on row 8 (s s p, x 8-10), and the cap curving down behind it
# on the back (u u m k on row 9, m on row 10), so the cap's edge is a curve and not a straight split.
GRID = CAP + [
    "...mmmmmsspkk...",
    "...spsJgJuumk...",
    "..aJppsJgggmoo..",
    ".aJgJpsJggggoao.",
    ".oaogJJgggooooo.",
] + POOL

# Round 3 options not chosen, kept for the sheet.
OPTION_B = CAP_DORSAL + [   # no band, a small dorsal flap on top
    "...mmmmsssmkk...",
    "..aspsJggJJkoa..",
    "..aJppsJgggJoa..",
    "...gJpsJggggo...",
    "....gJJgggoo....",
] + POOL
OPTION_C = CAP_DORSAL + [   # the band and a dorsal flap, no side fins
    "...mmmmsssmkk...",
    "...spsJgJsppo...",
    "...JppsJgggso...",
    "...gJpsJggggo...",
    "....gJJgggoo....",
] + POOL

# Round 2, REJECTED by the owner ("pokeball/dolphin mix"), kept only for the sheet.
PREV_GRID = [
    "................",
    ".........F......",
    "........Ff......",
    "......hhTmk.....",
    "....hhTummko....",
    "...hTumkkkkko...",
    "...hfumkkkkko...",
    ".fTumemkkkkko...",
    "...jjjjJkkkko...",
    "...WWWWWWWWWo...",
    "..appssssgggoa..",
    "..aspppssgggoa..",
    "....sssgggoo....",
    "..34oooooooo43..",
    ".12455343554321.",
    "..12211.122211..",
]


def render(rows):
    assert len(rows) == 16
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), PAL[ch] + (255,))
    return im


def measure(paths):
    res = subprocess.run([PY, os.path.join(ART, "tools", "measure.py")] + paths, capture_output=True, text=True)
    lines = []
    for line in res.stdout.splitlines():
        if line.startswith("{"):
            d = eval(line, {"np": __import__("numpy")})  # measure.py prints dicts with numpy floats
            lines.append(f"{d['file']:<26} cover {d['coverage']:.2f}  colours {d['colours']:>2}  dark {d['lmin']:.2f}  "
                         f"light {d['lmax']:.2f}  edge {d['edge_l']:.2f}  inside {d['interior_l']:.2f}  "
                         f"TL-BR {d['tl_minus_br']:+.2f}")
    return lines


def colours(im):
    return {im.getpixel((x, y))[:3] for x in range(16) for y in range(16) if im.getpixel((x, y))[3] > 0}


def lum(c):
    return (0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]) / 255


def widths(im):
    """Per-row outline widths (first-last opaque x) from row 3."""
    out = []
    for y in range(3, 16):
        xs = [x for x in range(16) if im.getpixel((x, y))[3] > 0]
        out.append(f"{min(xs)}-{max(xs)}" if xs else "-")
    return " ".join(out)


def eye_check():
    """The brightest pixel touching the eye (8 neighbours): it must stay a mid or dark tone."""
    ys = [y for y, r in enumerate(GRID) if "e" in r]
    y, x = ys[0], GRID[ys[0]].index("e")
    near = [GRID[y + dy][x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dx or dy) and GRID[y + dy][x + dx] != "."]
    top = max(near, key=lambda k: lum(PAL[k]))
    return f"eye at {x},{y}; brightest pixel touching it: '{top}' lightness {lum(PAL[top]):.2f} (eye-ring keys: {''.join(near)})"


def copy_check(icon):
    """Exact-pixel copy check against every vanilla spawn egg (as art/candidates/critic_sardina_egg_v5/check.py),
    and the pool against vanilla's (art/src/egg_pool.py).
    Vanilla's own pool pixels are allowed (the owner's exception, art/src/egg_pool.py); any other copied pixel
    fails the run."""
    ours = {(x, y): icon.getpixel((x, y)) for x in range(16) for y in range(16) if icon.getpixel((x, y))[3] > 0}
    hits, vcols = [], set()
    for f in sorted(glob.glob(os.path.join(VANILLA, "*spawn_egg*.png"))):
        v = Image.open(f).convert("RGBA")
        if v.size != (16, 16):
            continue
        same = [p for p, c in ours.items() if v.getpixel(p) == c and not is_pool(p, c)]
        if same:
            hits.append((len(same), os.path.basename(f)))
        vcols |= colours(v)
    shared = (colours(icon) - POOL_COLOURS) & vcols
    assert not hits, f"copies vanilla pixels besides the pool: {hits}"
    hits.sort(reverse=True)
    most = f"most: {hits[0][0]} in {hits[0][1]}" if hits else "none"
    icon_cols = set(ICON.values())
    return [f"same pixel and colour as a vanilla spawn egg, besides its pool: {sum(n for n, _ in hits)} pixels over {len(hits)} eggs ({most})",
            f"our colours (besides the pool) also used by any vanilla spawn egg: {len(shared)}",
            pool_line(icon),
            f"colours not in the incova icon palette, besides the pool: {len(colours(icon) - POOL_COLOURS - icon_cols)}",
            eye_check()]


def hotbars():
    items = ["mc:cod_spawn_egg", "mod:lampuka_spawn_egg", "mod:tonn_spawn_egg", "mod:sardina_spawn_egg",
             "mod:incova_spawn_egg", "mod:cerna_spawn_egg", "mod:awrata_spawn_egg", "mod:murina_spawn_egg",
             "mod:incova"]
    tool = os.path.join(ART, "tools", "hotbar_preview.py")
    subprocess.run([PY, tool, OUT_HOTBAR] + items + ["--select", "4"], check=True, capture_output=True)
    subprocess.run([PY, tool, OUT_HOTBAR4] + items + ["--select", "4", "--scale", "4"], check=True,
                   capture_output=True)
    return "vanilla cod egg, lampuka, tonn, sardina eggs, INCOVA EGG, cerna, awrata, murina eggs, incova item"


def tile_band(W, items, bg, ink, small):
    band = Image.new("RGB", (W, 128 + 120), bg)
    d = ImageDraw.Draw(band)
    for i, (name, p) in enumerate(items):
        im = p if isinstance(p, Image.Image) else Image.open(p).convert("RGBA")
        x0 = 10 + i * 214
        tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
        tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
        band.paste(tile.convert("RGB"), (x0, 22))
        d.text((x0, 2), name, fill=ink, font=small)
        for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1),
                                      ((40, 40, 40), 2))):
            t = Image.new("RGBA", (40, 40), col + (255,))
            t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
            band.paste(t.convert("RGB"), (x0 + (j % 2) * 44 + (j // 2) * 88, 156))
    d.text((10, 202), "8x, then 1x and 2x on light grey, 1x and 2x on dark grey", fill=ink, font=small)
    return band


def sheet(icon):
    font, small = label_font(16), label_font(13)
    W = 2580
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    refs = []
    for name in ("portugal.jpg", "ifremer1.jpg", "lonja.jpg", "gervais.jpg"):
        p = os.path.join(REFS, name)
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im = im.resize((360, round(360 * im.height / im.width)), Image.LANCZOS)
            refs.append((name, im))
    if refs:
        h = max(im.height for _, im in refs) + 26
        band = Image.new("RGB", (W, h), bg)
        d = ImageDraw.Draw(band)
        for i, (name, im) in enumerate(refs):
            band.paste(im, (10 + i * 370, 22))
            d.text((10 + i * 370, 2), f"{name} (reference only)", fill=ink, font=small)
        parts.append(("References (art/references/fish_incova_refonly, list.tsv)", band))

    bucket = Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")
    bucket.alpha_composite(Image.open(os.path.join(TEXTURES, "item", "incova_bucket.png")).convert("RGBA"))
    row1 = [("vanilla cod egg", os.path.join(VANILLA, "cod_spawn_egg.png")),
            ("vanilla salmon egg", os.path.join(VANILLA, "salmon_spawn_egg.png")),
            ("vanilla tropical fish egg", os.path.join(VANILLA, "tropical_fish_spawn_egg.png")),
            ("vanilla pufferfish egg", os.path.join(VANILLA, "pufferfish_spawn_egg.png")),
            ("round 2, REJECTED", render(PREV_GRID)),
            ("round 3 (A, critic FIX)", render(ROUND3_GRID)),
            ("INCOVA EGG (round 4)", icon),
            ("option B (not chosen)", render(OPTION_B)),
            ("option C (not chosen)", render(OPTION_C)),
            ("incova item icon", os.path.join(TEXTURES, "item", "incova.png")),
            ("incova bucket", bucket)]
    row2 = [("our sardina egg", os.path.join(TEXTURES, "item", "sardina_spawn_egg.png")),
            ("INCOVA EGG", icon)] + \
           [(f"our {n} egg", os.path.join(TEXTURES, "item", n + "_spawn_egg.png")) for n in OUR_EGGS if n != "sardina"]
    parts.append(("The egg at 8x and 1x beside vanilla's fish eggs, the accepted incova item and bucket",
                  tile_band(W, row1, bg, ink, small)))
    parts.append(("The egg beside our accepted eggs (the sardina first: an anchovy is not a sardine)",
                  tile_band(W, row2, bg, ink, small)))

    lines = measure([os.path.join(VANILLA, n + "_spawn_egg.png") for n in ("cod", "salmon", "tropical_fish", "pufferfish")]
                    + [os.path.join(TEXTURES, "item", n + "_spawn_egg.png") for n in OUR_EGGS] + [OUT_ICON])
    lines += copy_check(icon)
    lines.append("row widths from row 3, vanilla cod egg: " + widths(Image.open(os.path.join(VANILLA, "cod_spawn_egg.png"))
                                                                   .convert("RGBA")))
    lines.append("row widths from row 3, incova egg:      " + widths(icon))
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("art/tools/measure.py, the copy check and the eye check", band))

    names = hotbars()
    for path, label in ((OUT_HOTBAR, "GUI scale 2"), (OUT_HOTBAR4, "GUI scale 4")):
        im = Image.open(path).convert("RGB")
        if im.width > W - 20:
            im = im.resize((W - 20, round(im.height * (W - 20) / im.width)), Image.NEAREST)
        band = Image.new("RGB", (W, im.height + 30), bg)
        band.paste(im, (10, 4))
        ImageDraw.Draw(band).text((10, im.height + 8), f"{os.path.relpath(path, ROOT)}  ({names})", fill=ink,
                                  font=small)
        parts.append((f"Offline hotbar preview (art/tools/hotbar_preview.py), {label}", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Incova (European anchovy) spawn egg, textures/item/incova_spawn_egg.png", fill=ink,
           font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    os.makedirs(os.path.dirname(OUT_SHEET), exist_ok=True)
    out.save(OUT_SHEET)
    print("wrote", OUT_SHEET)


if __name__ == "__main__":
    icon = vanilla_pool(render(GRID), OLD_POOL)
    icon.save(OUT_ICON, optimize=False)
    print("wrote", OUT_ICON)
    sheet(icon)
