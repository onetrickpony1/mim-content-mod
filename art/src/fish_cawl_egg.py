"""Ċawl spawn egg: the item icon (16 x 16), 2026-11-18.

The pool (owner 2026-11-18, "the pool under the egg should be the same as vanilla"; docs/Decisions/2026-11-18 Boll
egg B; egg pools match vanilla.md): the pool drawn in the grid below is our old one. vanilla_pool() swaps it for
vanilla's own pool (art/src/egg_pool.py, the owner's exception to "never copy", for the pool only) before the egg
is written, keeping every body pixel; what is said below about our own pool is its history.

Built the vanilla 26.x way (decisions "2026-11-18 Sardina egg - a representation, not a fat fish" and "2026-11-18 Three
eggs rejected - must be egg-shaped; cawl and shark buckets accepted"): vanilla's EGG outline, standing in its own pool,
with the fish painted ON it. Vanilla's cod egg (art/.vanilla/item/cod_spawn_egg.png) is the template for the outline,
measured row by row, never copied.

The ċawl (Mediterranean damselfish, Chromis chromis) egg follows vanilla's curve row by row: narrow at the top
(6-9 on row 3), widening to 2-13 on rows 8-9 and 1-14 on rows 10-11 (the side fins), 2-13 on row 12, never a ball.
At 1x it reads by:
- a dark chocolate cap over the top, lit on its upper left like vanilla's, shading to the right;
- a lit, rounded head on the left: a dome of highlight (H) over and behind the eye, lit snout and cheek, and a
  shaded chin and throat under the eye (the owner rejected the icon's flat face, 2026-11-18);
- one black eye in a pale ring (H in front, above and behind it), the only black;
- the body shaded down a ramp of 6 tones to the lower right;
- a small pale belly patch low on the front;
- one signature part breaking the outline: the deeply forked tail at the upper right, its two lobe tips lit (q),
  not the palest tone, so they do not read as lone specks.
The outer pixels stay in a mid-dark band (luminance about 45-80), so the egg keeps its outline on the light slot and
does not vanish on the dark one; the light sits inside.
Colours are the accepted ċawl item icon's (art/src/fish_cawl_icon.py PAL), with its four shaded body tones lifted
part way and kept in order (see PAL), plus the pool blues, which are our own (not vanilla's pool, nor the other eggs').
Round 2 (critic, 2026-11-18): the outline follows vanilla's curve low down (rows 8-12 out to 2-13 and 1-14) so it no
longer reads as a sack; the cap is lit at its upper left like vanilla's; the shaded tones are lifted part way so
the cap and shaded side stay visible on the dark slot; the tail tips are toned down from the palest tone so they do
not read as lone specks. Round 1 is kept as art/candidates/fish_cawl_egg_round1.png for the side-by-side.
Photos (reference only): art/references/fish_cawl_refonly/ (list.tsv).

Run:    art/.venv/bin/python art/src/fish_cawl_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/cawl_spawn_egg.png (byte-identical on rerun) and
        art/candidates/fish_cawl_egg.png (compare sheet), with the offline hotbar previews
        art/candidates/fish_cawl_egg_hotbar.png and fish_cawl_egg_hotbar_x4.png (art/tools/hotbar_preview.py).
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

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
OUT_ICON = os.path.join(TEXTURES, "item", "cawl_spawn_egg.png")
OUT_SHEET = os.path.join(ART, "candidates", "fish_cawl_egg.png")
OUT_HOTBAR = os.path.join(ART, "candidates", "fish_cawl_egg_hotbar.png")
OUT_HOTBAR4 = os.path.join(ART, "candidates", "fish_cawl_egg_hotbar_x4.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_cawl_refonly")
ACCEPTED = ["lampuka", "tonn", "sardina", "cerna", "awrata", "murina"]


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAL = {
    # the ċawl: the accepted item icon's colours (art/src/fish_cawl_icon.py PAL)
    "b": hx("#5f4535"),                       # rim on the lit top and left
    "H": hx("#a07c5c"),                       # highlight: the head dome, the eye ring, the belly patch
    "W": hx("#8a6a50"), "1": hx("#735540"),
    # the icon's four shaded body tones (#614636 #4f3a2c #432f23 #36261c), lifted part way and in order (critic,
    # round 2), so the cap and shaded side stay visible on the dark slot without drifting toward the ċerna
    "2": hx("#6e4f3c"), "3": hx("#644938"), "4": hx("#5a4030"), "5": hx("#4f382a"),   # the light ramp, lit to shaded
    "e": hx("#0a0a0a"),                       # the eye (the only black)
    "d": hx("#7a6656"),                       # the lit tip of the left side fin
    "p": hx("#a8968a"),                       # pale: the belly patch
    "q": hx("#8e705d"), "r": hx("#6d5242"), "t": hx("#614434"),  # the tail: lit lobe, shaded lobe, notch
    # the old pool (now swapped for vanilla's): our own ramp of deep blues
    "u": hx("#152a47"), "v": hx("#1f4d7c"), "x": hx("#2b70aa"), "y": hx("#4b95d3"), "z": hx("#9ccdf0"),
    "o": hx("#1d130c"),                       # the egg's shadow on the water
}
# Our own old pool's colours: vanilla_pool() takes them out and puts vanilla's pool in (owner 2026-11-18,
# "the pool under the egg should be the same as vanilla"; art/src/egg_pool.py).
OLD_POOL = {PAL[k] for k in "uvxyz"}

GRID = [
    "................",
    "................",
    "............q...",
    "......b133.rq.q.",
    ".....bW1234rtq..",
    "....b1W1b344....",
    "....2HHW2334....",
    "...bHeHW12344...",
    "..22W3W1223455..",
    "..b33411233445..",
    ".2d32Hp123345r5.",
    ".br42WH12234545.",
    "..344322334455..",
    "..uvoooooooovu..",
    ".uvxyzyxxyzyxvu.",
    "..uvvu.uvvu.vu..",
]


def variant(changes):
    rows = [list(r) for r in GRID]
    for y, x, ch in changes:
        rows[y][x] = ch
    return ["".join(r) for r in rows]


def render(rows):
    assert len(rows) == 16
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), PAL[ch] + (255,))
    return im


def widths(im):
    out = []
    for y in range(16):
        xs = [x for x in range(16) if im.getpixel((x, y))[3] > 0]
        out.append(f"{xs[0]}-{xs[-1]}" if xs else "")
    return out


def measure(paths):
    py = os.path.join(ART, ".venv", "bin", "python")
    res = subprocess.run([py, os.path.join(ART, "tools", "measure.py")] + paths, capture_output=True, text=True)
    lines = []
    for line in res.stdout.splitlines():
        if line.startswith("{"):
            d = eval(line, {"np": __import__("numpy")})  # measure.py prints dicts with numpy floats
            lines.append(f"{d['file']:<26} cover {d['coverage']:.2f}  colours {d['colours']:>2}  dark {d['lmin']:.2f}  "
                         f"light {d['lmax']:.2f}  edge {d['edge_l']:.2f}  inside {d['interior_l']:.2f}  "
                         f"TL-BR {d['tl_minus_br']:+.2f}")
    return lines


def copy_check(icon):
    """Exact-pixel copy check against every vanilla spawn egg (as art/candidates/critic_sardina_egg_v5/check.py).
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
        vcols |= {v.getpixel((x, y))[:3] for x in range(16) for y in range(16) if v.getpixel((x, y))[3] > 0}
    shared = ({c[:3] for c in ours.values()} - POOL_COLOURS) & vcols
    assert not hits, f"copies vanilla pixels besides the pool: {hits}"
    hits.sort(reverse=True)
    most = f"most: {hits[0][0]} in {hits[0][1]}" if hits else "none"
    return [f"same pixel and colour as a vanilla spawn egg, besides its pool: {sum(n for n, _ in hits)} pixels over {len(hits)} eggs ({most})",
            f"our colours (besides the pool) also used by any vanilla spawn egg: {len(shared)}",
            pool_line(icon)]


def tile_row(items, d, band, y0):
    for i, (name, im) in enumerate(items):
        x0 = 10 + i * 214
        tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
        tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
        band.paste(tile.convert("RGB"), (x0, y0 + 20))
        d.text((x0, y0), name, fill=(235, 235, 235), font=label_font(13))
        for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
            t = Image.new("RGBA", (40, 40), col + (255,))
            t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
            band.paste(t.convert("RGB"), (x0 + j * 44, y0 + 154))


def sheet(icon):
    font, small = label_font(16), label_font(13)
    W = 2160
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    refs = []
    for name in ("cawl_02.jpg", "cawl_04.jpg", "cawl_06.jpg", "cawl_07.jpg", "cawl_13_drawing.jpg"):
        p = os.path.join(REFS, name)
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im = im.resize((310, round(310 * im.height / im.width)), Image.LANCZOS)
            refs.append((name, im))
    if refs:
        h = max(im.height for _, im in refs) + 26
        band = Image.new("RGB", (W, h), bg)
        d = ImageDraw.Draw(band)
        for i, (name, im) in enumerate(refs):
            band.paste(im, (10 + i * 320, 22))
            d.text((10 + i * 320, 2), f"{name} (reference only)", fill=ink, font=small)
        parts.append(("References (art/references/fish_cawl_refonly, list.tsv)", band))

    band = Image.new("RGB", (W, 210), bg)
    d = ImageDraw.Draw(band)
    old = os.path.join(ART, "candidates", "fish_cawl_egg_round1.png")
    tiles = [("round 1 (critic: FIX)", Image.open(old).convert("RGBA"))] if os.path.exists(old) else []
    tiles += [("ROUND 2 (this)", icon),
              ("vanilla cod egg", Image.open(os.path.join(VANILLA, "cod_spawn_egg.png")).convert("RGBA")),
              ("our cerna egg", Image.open(os.path.join(TEXTURES, "item", "cerna_spawn_egg.png")).convert("RGBA"))]
    tile_row(tiles, d, band, 2)
    parts.append(("Round 1 and round 2 at 8x, then 1x and 2x on light and dark grey (round 1 options B and C were "
                  "dropped: a crest adds nothing at 1x, a side tail widens the middle)", band))

    items = [("vanilla cod egg", os.path.join(VANILLA, "cod_spawn_egg.png"))]
    items += [(f"our {n} egg", os.path.join(TEXTURES, "item", n + "_spawn_egg.png")) for n in ACCEPTED]
    items += [("NEW CAWL EGG", None), ("cawl item icon", os.path.join(TEXTURES, "item", "cawl.png"))]
    band = Image.new("RGB", (W, 210), bg)
    d = ImageDraw.Draw(band)
    tile_row([(n, icon if p is None else Image.open(p).convert("RGBA")) for n, p in items], d, band, 2)
    parts.append(("The chosen egg beside vanilla's cod egg, our accepted eggs and the accepted cawl item icon", band))

    cod = Image.open(os.path.join(VANILLA, "cod_spawn_egg.png")).convert("RGBA")
    wc, wo = widths(cod), widths(icon)
    lines = ["row   cod egg   cawl egg"] + [f"{y:>3}   {wc[y]:<8}  {wo[y]}" for y in range(2, 16)]
    lines += [""] + measure([os.path.join(VANILLA, "cod_spawn_egg.png")] +
                            [os.path.join(TEXTURES, "item", n + "_spawn_egg.png") for n in ACCEPTED] + [OUT_ICON])
    lines += copy_check(icon)
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("Outline widths per row (rows 13-15 are the pool), art/tools/measure.py and the copy check", band))

    py = os.path.join(ART, ".venv", "bin", "python")
    hb = ["mc:cod_spawn_egg"] + [f"mod:{n}_spawn_egg" for n in ACCEPTED] + ["mod:cawl_spawn_egg", "mod:cawl"]
    for out, scale in ((OUT_HOTBAR, 2), (OUT_HOTBAR4, 4)):
        subprocess.run([py, os.path.join(ART, "tools", "hotbar_preview.py"), out] + hb +
                       ["--select", "7", "--scale", str(scale)], check=True, capture_output=True)
        im = Image.open(out).convert("RGB")
        band = Image.new("RGB", (W, im.height + 30), bg)
        band.paste(im, (10, 4))
        ImageDraw.Draw(band).text((10, im.height + 8), os.path.relpath(out, ROOT) + f"  (GUI scale {scale}: vanilla cod "
                                  "egg; our lampuka, tonn, sardina, cerna, awrata, murina eggs; CAWL EGG (selected); "
                                  "cawl item icon)", fill=ink, font=small)
        parts.append((f"Hotbar preview (art/tools/hotbar_preview.py, GUI scale {scale})", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Ċawl (Mediterranean damselfish) spawn egg, textures/item/cawl_spawn_egg.png", fill=ink,
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
