"""Shared parts of the fish spawn-egg scripts written from 2026-11-19 (trilja, hmar, lingwata, mola mola).

Each fish's own script (art/src/fish_<id>_egg.py) holds its palette, its candidate grids and its pick, and calls
run(). This module holds what they share, the same way the earlier egg scripts each did it in full:
- EGG: vanilla's fish-egg outline (measured from cod and salmon _spawn_egg in art/.vanilla/item, never copied): a
  4 px top on row 3 widening to 12 px on rows 8-9, the side flaps at x 1 and 14 on rows 10-12, the bottom edge on
  row 13 (x 5-10), standing in vanilla's own pool (art/src/egg_pool.py, the owner's exception to "never copy", for
  the pool only; P in the grids);
- check_outline(): the outline is filled and nothing but the fish's named signature pixels lies outside it;
- check_marks(): no two dark marks level with each other with lighter body between them (a pair like that reads
  as eyes);
- copy_check(): no pixel of ours has a vanilla spawn egg's colour at the same place, besides vanilla's pool;
- the compare sheet (candidates at 8x, 1x and 2x beside vanilla's fish eggs, our accepted fish eggs and the fish's
  own icon) and the offline hotbar previews (art/tools/hotbar_preview.py, GUI scale 2 and 4).
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

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
ITEMS = os.path.join(TEXTURES, "item")
CAND = os.path.join(ART, "candidates")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")

# the pool rows (13-15): the egg's bottom edge o on row 13, x 5-10; each fish swaps o for its own outline key
POOL_ROWS = [
    "..PPPrrrrrrPPP..",
    "..PPPPPPPPPPPP..",
    "...PPPPPPPPPP...",
]
EGG = {3: (6, 9), 4: (5, 10), 5: (4, 11), 6: (4, 11), 7: (3, 12), 8: (2, 13), 9: (2, 13), 10: (1, 14), 11: (1, 14),
       12: (1, 14), 13: (2, 13), 14: (2, 13), 15: (3, 12)}
# the accepted fish and jellyfish eggs the candidates are compared with
ACCEPTED = ("boll", "cerna", "skorfna", "lampuka", "tonn", "sardina", "awrata", "cawl", "incova", "murina",
            "huta_kahla", "pixxispad", "ziemel", "mauve_stinger", "fried_egg_jellyfish", "man_o_war")


def pool_rows(outline_key):
    return [r.replace("r", outline_key) for r in POOL_ROWS]


def patched(rows, fixes):
    """A copy of a grid with single pixels changed: fixes is {(x, y): key}."""
    rows = list(rows)
    for (x, y), ch in fixes.items():
        rows[y] = rows[y][:x] + ch + rows[y][x + 1:]
    return rows


def check_outline(name, rows, fin):
    """The egg outline is filled, and nothing but the fish's signature pixels (fin) lies outside it."""
    assert len(rows) == 16, (name, len(rows))
    for y, row in enumerate(rows):
        assert len(row) == 16, (name, y, row)
        lo, hi = EGG.get(y, (99, -1))
        for x, ch in enumerate(row):
            inside = lo <= x <= hi
            if (x, y) in fin:
                assert ch != "." and not inside, f"{name}: signature pixel ({x},{y})"
            else:
                assert (ch != ".") == inside, f"{name}: pixel ({x},{y}) breaks the egg outline"


def check_marks(name, rows, dark):
    """No two dark marks (keys in dark, inside the body, rows 4-12, not on the outline) level with each other and
    2-4 px apart with lighter body between: a pair like that reads as eyes."""
    for y in range(4, 13):
        lo, hi = EGG[y]
        if y >= 10:
            lo, hi = lo + 1, hi - 1  # the flaps are not body
        marks = [x for x in range(lo + 1, hi) if rows[y][x] in dark]
        for a in marks:
            for b in marks:
                if 2 <= b - a <= 4 and all(rows[y][x] not in dark for x in range(a + 1, b)):
                    raise AssertionError(f"{name}: dark marks at ({a},{y}) and ({b},{y}) read as a pair of eyes")


def render(rows, pal):
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == "P":
                im.putpixel((x, y), VANILLA_POOL[(x, y)] + (255,))
            elif ch != ".":
                im.putpixel((x, y), tuple(pal[ch][:3]) + (255,))
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
    """Exact-pixel copy check against every vanilla spawn egg. Vanilla's own pool pixels are allowed (the owner's
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
    shared = {c[:3] for p, c in ours.items() if not is_pool(p, c)} & vcols
    hits.sort(reverse=True)
    most = f"most: {hits[0][0]} in {hits[0][1]}" if hits else "none"
    return (f"{name}: same pixel and colour as a vanilla spawn egg, besides its pool: {sum(n for n, _ in hits)} pixels "
            f"over {len(hits)} eggs ({most}); our colours (besides the pool) also used by any vanilla spawn egg: "
            f"{len(shared)}; {pool_line(icon)}"), sum(n for n, _ in hits)


def _tmp(fish, icons):
    return {n: os.path.join(CAND, f"fish_{fish}_egg_{n}.tmp.png") for n in icons}


def hotbars(fish, icons, outs):
    """Offline hotbar previews, nothing selected: vanilla cod, salmon, pufferfish eggs, the candidates, our boll and
    skorfna eggs, the fish's own icon."""
    py = os.path.join(ART, ".venv", "bin", "python")
    tmp = _tmp(fish, icons)
    for n, im in icons.items():
        im.save(tmp[n])
    items = (["mc:cod_spawn_egg", "mc:salmon_spawn_egg", "mc:pufferfish_spawn_egg"] + [f"file:{tmp[n]}" for n in icons]
             + ["mod:boll_spawn_egg", "mod:skorfna_spawn_egg", f"mod:{fish}"])
    try:
        for out, scale in outs:
            subprocess.run([py, os.path.join(ART, "tools", "hotbar_preview.py"), out] + items[:9] +
                           ["--scale", str(scale)], check=True, capture_output=True)
    finally:
        for p in tmp.values():
            os.remove(p)


def sheet(fish, title, icons, pick, outs, out_sheet):
    font, small = label_font(16), label_font(13)
    W = 2400
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    def van(n):
        return Image.open(os.path.join(VANILLA, n + ".png")).convert("RGBA")

    def ours(n):
        return Image.open(os.path.join(ITEMS, n + ".png")).convert("RGBA")

    items = ([(f"CANDIDATE {n}{' (PICK)' if n == pick else ''}", im) for n, im in icons.items()] +
             [(f"{fish} icon (accepted)", ours(fish))] +
             [(f"vanilla {n} egg", van(n + "_spawn_egg")) for n in ("cod", "salmon", "pufferfish", "tropical_fish",
                                                                    "squid")] +
             [(f"our {n} egg", ours(n + "_spawn_egg")) for n in ACCEPTED])
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
        parts.append((f"The candidates at 8x, 1x and 2x beside the accepted {fish} icon, vanilla's fish and squid eggs "
                      "and our accepted fish and jellyfish eggs" if start == 0 else "(continued)", band))

    tmp = _tmp(fish, icons)
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

    for out, scale in outs:
        im = Image.open(out).convert("RGB")
        band = Image.new("RGB", (W, im.height + 30), bg)
        band.paste(im, (10, 4))
        ImageDraw.Draw(band).text((10, im.height + 8), os.path.relpath(out, ROOT) + f"  (GUI scale {scale}, nothing "
                                  "selected: vanilla cod, salmon, pufferfish eggs; CANDIDATES " + ", ".join(icons) +
                                  f"; our boll and skorfna eggs; {fish} icon)", fill=ink, font=small)
        parts.append((f"Hotbar preview (art/tools/hotbar_preview.py, GUI scale {scale})", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), title, fill=ink, font=label_font(20))
    y = 40
    for t, b in parts:
        d.text((10, y), t, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    out.save(out_sheet)
    print("wrote", os.path.relpath(out_sheet, ROOT))


def run(fish, title, pal, candidates, fin, dark, pick, script):
    """Check every candidate, write the pick to the mod, then the hotbar previews and the compare sheet."""
    for n, g in candidates.items():
        check_outline(n, g, fin[n])
        check_marks(n, g, dark)
    icons = {n: render(g, pal) for n, g in candidates.items()}
    for n, im in icons.items():
        line, n_same = copy_check(n, im)
        assert n_same == 0, line
    out_icon = os.path.join(ITEMS, f"{fish}_spawn_egg.png")
    icons[pick].save(out_icon, optimize=False)
    print("wrote", os.path.relpath(out_icon, ROOT), f"(candidate {pick})")
    os.makedirs(CAND, exist_ok=True)
    base = os.path.splitext(os.path.basename(script))[0]
    outs = ((os.path.join(CAND, base + "_hotbar.png"), 2), (os.path.join(CAND, base + "_hotbar_x4.png"), 4))
    hotbars(fish, icons, outs)
    sheet(fish, title, icons, pick, outs, os.path.join(CAND, base + ".png"))
    return icons
