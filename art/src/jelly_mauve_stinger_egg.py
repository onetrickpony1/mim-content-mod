"""Mauve stinger (Pelagia noctiluca) spawn egg: the item icon (16 x 16), 2026-11-18.

Made the way the accepted eggs are (art/src/fish_cerna_egg.py, fish_boll_egg.py): vanilla's EGG outline (narrow top
on row 3, widening down, full width rows 8-12, its bottom edge on row 13 at x 5-10) standing in vanilla's own pool
(art/src/egg_pool.py, vanilla_pool(): the owner's one exception to "never copy", for the pool only). A stylised egg,
not a whole jellyfish squeezed in (docs/Decisions/2026-11-18 Three eggs rejected - must be egg-shaped; ...), and like
the owner's latest egg (the boll's), a plain egg in the animal's palette carrying its key feature. No eye, no face.
Vanilla's eggs (art/.vanilla/item/*spawn_egg*.png) were measured, never copied (copy check on every run).

Painted on every candidate:
- the egg in the accepted model's see-through pink-mauve (art/src/jelly_mauve_stinger_model.py PAL), lit from the
  top left (hi, b1) down to the deeper mauve of the shaded rim (b3, b4), outlined in the oral arms' deep magenta;
- the mauve stinger's warts (its stinging cells), its key feature: darker mauve dots, each with the model's pale lit
  pixel above it so it reads as a raised bump; that cap is one step up the egg's own ramp, not the model's near-white
  wl, which read as pale spots (critic round 1). They are scattered with no two on one row near the top and none where
  a fish egg puts its eye (upper left), so they cannot read as eyes or a face.
The candidates differ only low down:
- A: six warts alone;
- B: five warts, and a hint of the bell's rim low down: the lower egg turns to the deeper underside (sub), its top
  edge scalloped into lappets. (Pale tentacle strands and frilled oral arms there were tried and dropped: on the
  dark band they read as teeth and a mouth.)
- C (chosen, critic round 1): eight warts, more densely covered, as the animal is.

Colours: the model's own, kept or darkened by at most 1.2x (items are not under water; the model was lifted for the
water): see PAL, each with its model name and factor.

Run:    art/.venv/bin/python art/src/jelly_mauve_stinger_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/mauve_stinger_spawn_egg.png (the chosen candidate,
        byte-identical on rerun), art/candidates/jelly_mauve_stinger_egg_{A,B,C}.png, the compare sheet
        art/candidates/jelly_mauve_stinger_egg.png and unselected hotbar previews
        art/candidates/jelly_mauve_stinger_egg_hotbar_{A,B,C,x4}.png (art/tools/hotbar_preview.py).
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
OUT_ICON = os.path.join(ITEM, "mauve_stinger_spawn_egg.png")
CAND = os.path.join(ART, "candidates")
OUT_SHEET = os.path.join(CAND, "jelly_mauve_stinger_egg.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
CHOSEN = "C"


def hx(h, f=1.0):
    """A model colour darkened by f (1.0 to 1.2: the egg is not under water, the model was lifted for it)."""
    assert 1.0 <= f <= 1.2
    h = h.lstrip("#")
    return tuple(round(int(h[i:i + 2], 16) / f) for i in (0, 2, 4))


PAL = {
    "H": hx("#ffd6f8"),          # hi: the lit top of the dome
    "1": hx("#f8a8f0", 1.04),    # b1: the upper bell
    "2": hx("#f08ae8", 1.06),    # b2: the middle of the bell
    "3": hx("#dc6ed8", 1.08),    # b3: the lower bell
    "4": hx("#c254c4", 1.08),    # b4: the rim in the shade
    "5": hx("#c254c4", 1.2),     # b4, deeper: the shaded lower right
    "k": hx("#b42abc", 1.1),     # core: the outline on the lit top and left
    "o": hx("#9a1aa8", 1.2),     # a0: the outline on the shaded right and below
    "w": hx("#b03cb4", 1.2),     # w1: a wart in the light
    "W": hx("#9a1aa8", 1.1),     # a0: a wart in the shade
    "s": hx("#cc60cc", 1.1),     # sub: the underside of the bell (B)
    "S": hx("#cc60cc", 1.2),     # sub, shaded
}

# The egg: vanilla's egg outline (widths 6-9, 5-10, 4-11, 4-11, 3-12, then 2-13 for rows 8-12), the pool round it.
BASE = [
    "................",
    "................",
    "................",
    "......kkko......",
    ".....kHH11o.....",
    "....kHHH112o....",
    "....kH11122o....",
    "...kH1112223o...",
    "..kH111222233o..",
    "..k1112222334o..",
    "..k1122223344o..",
    "..k2222333445o..",
    "..k2333344455o..",
    ".....oooooo.....",
    "................",
    "................",
]

# Warts: (x, y) of the dark dot; its lit top goes at (x, y - 1). Scattered: none upper left where an eye would be,
# no two on one row in the upper egg.
WARTS = [(8, 5), (10, 7), (6, 8), (4, 10), (9, 11), (11, 12)]
WARTS_MANY = [(7, 4), (9, 6), (5, 8), (11, 9), (8, 10), (3, 11), (12, 11), (6, 12)]
WARTS_RIM = [(8, 5), (10, 7), (6, 8), (4, 9), (11, 9)]  # B: the lower egg is the rim

# B: rows 10-12 become the bell's rim; the scalloped top edge (lappets) on row 10.
RIM_B = [
    "..k2223333445o..",
    "..k3S3S33S4S5o..",
    "..kSSSSSSSSSSo..",
]


# A wart's raised top: one step lighter than the body above the dot (critic round 1: the model's near-white wl cap
# was brighter than the egg's own lit top, so the warts read as pale spots instead of dark ones).
STEP_UP = {"5": "4", "4": "3", "3": "2", "2": "1", "1": "H", "H": "H", "S": "s", "s": "3"}


def build(rows, warts, rim=None):
    rows = list(rows)
    if rim:
        rows[10:13] = rim
    g = [list(r) for r in rows]
    for x, y in warts:
        shade = g[y][x] in "345sS"
        g[y][x] = "W" if shade else "w"
        if g[y - 1][x] in STEP_UP:  # no cap on the outline (a lone pale speck there breaks the egg's edge)
            g[y - 1][x] = STEP_UP[g[y - 1][x]]
    rows = ["".join(r) for r in g]
    for r in rows:
        assert len(r) == 16, r
    return rows


def render(rows):
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), PAL[ch] + (255,))
    return im


CANDIDATES = {
    "A": build(BASE, WARTS),
    "B": build(BASE, WARTS_RIM, RIM_B),
    "C": build(BASE, WARTS_MANY),
}

# Round 1 (before the critic's fixes), three fresh readers, one unselected hotbar each (first lines, word for word). Caveat: every sub-agent sees
# the repository's file list in its context, so a named species ("mauve stinger") may be a leak; "jellyfish" is the read.
BLIND_READS = {
    "A": ['"It looks like a spawn egg, most likely for a pink jellyfish (something like a mauve stinger) or another pink, spotted sea creature."'],
    "B": ['"It\'s most likely a spawn egg for a pink jellyfish, probably the mauve stinger."'],
    "C": ['"It\'s a spawn egg for a pink, spotted sea creature, most likely a jellyfish (a mauve/pink bell covered in small white warts)."'],
    "C round 2 (after critic round 1's fixes, one fresh reader)": [
        '"It\'s a pink, speckled spawn egg, most likely for a pink jellyfish (like a mauve stinger) or some other soft '
        'pink sea creature."', '(asked about a face: "I don\'t see one.")'],
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
    shared = ({c[:3] for c in ours.values()} - POOL_COLOURS) & vcols
    return [f"{name}: same pixel and colour as a vanilla spawn egg, besides its pool: 0; our colours (besides the "
            f"pool) also in a vanilla egg: {len(shared)}; " + pool_line(icon)]


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
    return os.path.join(CAND, f"jelly_mauve_stinger_egg_{k}.png")


def hotbars(keys):
    """Each candidate unselected among vanilla water eggs (GUI scale 2), and all of them together at scale 4."""
    outs = {}
    for k in keys:
        out = os.path.join(CAND, f"jelly_mauve_stinger_egg_hotbar_{k}.png")
        items = ["mc:cod_spawn_egg", "mc:squid_spawn_egg", "mc:tropical_fish_spawn_egg", "mc:glow_squid_spawn_egg",
                 f"file:{cand_path(k)}", "mc:axolotl_spawn_egg", "mc:salmon_spawn_egg", "mc:pufferfish_spawn_egg",
                 "mc:dolphin_spawn_egg"]
        subprocess.run([PY, os.path.join(ART, "tools", "hotbar_preview.py"), out] + items + ["--select", "8"],
                       check=True, capture_output=True)
        outs[k] = out
    out4 = os.path.join(CAND, "jelly_mauve_stinger_egg_hotbar_x4.png")
    items = (["mc:squid_spawn_egg", "mc:glow_squid_spawn_egg", "mod:boll_spawn_egg", "mod:cerna_spawn_egg"]
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
    for i, (k, im) in enumerate(icons.items()):
        tile_row(d, band, 10 + i * 214, f"egg {k}" + (" (CHOSEN)" if k == CHOSEN else ""), im, small, ink)
    notes = ["Vanilla's egg outline in vanilla's own pool; the accepted model's pink-mauve, lit top-left; no eye, no face.",
             "A: six stinging warts (dark mauve dots, each with a pixel one step lighter above: raised).",
             "B: five warts; the lower egg the bell's deeper underside under a scalloped rim (lappets).",
             "C (CHOSEN): eight warts, more densely covered.",
             "Colours: the model's (jelly_mauve_stinger_model.py PAL), kept or darkened by at most 1.2x."]
    for i, line in enumerate(notes):
        d.text((680, 24 + 20 * i), line, fill=ink, font=small)
    parts.append(("The candidates (8x, then 1x and 2x on light and dark grey)", band))

    eggs = [(f"vanilla {n.replace('_', ' ')}", os.path.join(VANILLA, n + "_spawn_egg.png"))
            for n in ("cod", "squid", "glow_squid", "tropical_fish", "pufferfish")]
    eggs += [(f"our {n.replace('_', ' ')}", os.path.join(ITEM, n + "_spawn_egg.png"))
             for n in ("boll", "cerna", "huta_kahla", "ziemel")]
    band = Image.new("RGB", (W, 248), bg)
    d = ImageDraw.Draw(band)
    for i, (name, p) in enumerate(eggs):
        tile_row(d, band, 10 + i * 214, name, Image.open(p).convert("RGBA"), small, ink)
    parts.append(("Vanilla eggs and our accepted eggs, for comparison", band))

    lines = measure([p for _, p in eggs] + [cand_path(k) for k in icons])
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
               else "GUI scale 4: vanilla squid and glow squid eggs, our boll and cerna eggs, eggs " + ", ".join(icons))
        ImageDraw.Draw(band).text((10, im.height + 8), os.path.relpath(hb[k], ROOT) + "  " + cap, fill=ink, font=small)
        parts.append((f"Hotbar preview (art/tools/hotbar_preview.py): {k}", band))

    W = max(W, max(b.width for _, b in parts))
    out = Image.new("RGB", (W, sum(b.height + 30 for _, b in parts) + 40), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Mauve stinger spawn egg, textures/item/mauve_stinger_spawn_egg.png", fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    out.save(OUT_SHEET)
    print("wrote", OUT_SHEET)


if __name__ == "__main__":
    icons = {k: vanilla_pool(render(rows), set()) for k, rows in CANDIDATES.items()}
    for k, im in icons.items():
        copy_check(k, im)
        im.save(cand_path(k), optimize=False)
    icons[CHOSEN].save(OUT_ICON, optimize=False)
    print("wrote", OUT_ICON)
    sheet(icons, hotbars(list(icons)))
