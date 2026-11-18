"""Item icon for the mola mola (ocean sunfish, Mola mola, "Pixxiluna"): the raw fish it drops, like vanilla cod.

The 3D model came first and the owner accepted it (2026-11-18, "all pass"), so the icon takes the model's look and
colours (art/src/fish_mola_model.py, textures/entity/fish/mola_mola.png). The model's palette was made a step lighter
than the photos for the water; out of water in the hotbar that read as a white blob against the slot grey, so the icon
takes the same hues one step darker (each tone about x0.88, back to the out-of-water photos mm07 and mm10) and adds a
dark rim, as our other fish icons do.

What must read at 16x16 (references: art/references/fish_mola_refonly/, list.tsv; reference only):
- a tall round disc that looks cut off behind;
- a tall dorsal fin up and an anal fin down, slim, both set far back (dark grey, a lit leading edge f);
- the clavus behind: a pale rim with scalloped lobes (the silhouette steps in at each notch);
- a small mouth at the front tip (a dark opening q, below the eye's row);
- one small dark eye high on the head, with only a lit pixel before it: no ring, no second dark spot near it, so it
  never makes a face. The pectoral fin is pale (P) and low, away from the eye's row.
- countershading as the model: a grey-brown back, silver sides, a pale belly with soft blotches; light from the top
  left adds a lit sheen (h) on the forehead.

Pose: vanilla's fish lie diagonally, head lower left. A mola is taller than long, so three poses are offered:
- A: side view, upright: the fins straight up and down, the clavus at the right;
- B: a slight diagonal (about 20 degrees, head down to the left), both long fins still clear;
- C: a stronger diagonal (about 40 degrees, nearer vanilla's), the anal fin trailing down to the right.

Run:  art/.venv/bin/python art/src/fish_mola_icon.py
Writes mod/.../textures/item/mola_mola.png (the INSTALLED candidate, byte-identical on rerun),
art/candidates/fish_mola_icon_<X>.png (each candidate at 16x16), art/candidates/fish_mola_icon.png (compare sheet: the
candidates at 1x, 2x and 8x beside vanilla's fish and our accepted fish icons) and the offline hotbar previews
art/candidates/fish_mola_icon_hotbar_<X>.png (the mola unselected among vanilla items, GUI scale 1 and 2, light and
dark backdrops) and fish_mola_icon_hotbar_x4.png. A copy check fails the run if any pixel matches a vanilla item
texture in place and colour.
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

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
OUT_ICON = os.path.join(TEXTURES, "item", "mola_mola.png")
CAND = os.path.join(ART, "candidates")
OUT_SHEET = os.path.join(CAND, "fish_mola_icon.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_mola_refonly")
MODEL_TEX = os.path.join(TEXTURES, "entity", "fish", "mola_mola.png")

INSTALLED = "A"  # waiting for the owner


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# The model's palette (fish_mola_model.py PAL) a step darker for out of water; the keys keep the model's letters.
PAL = {k: hx(v) for k, v in {
    "h": "#8d887e",   # lit sheen on the forehead (top left)
    "B": "#69645b",   # back, grey-brown (model B #706b63)
    "U": "#827d73",   # upper side (model U #99958b)
    "n": "#8e8a80",   # blotch on the silver side
    "S": "#9f9b91",   # silver side (model S #b2afa7)
    "L": "#b5b1a7",   # lower side (model L #c6c3ba)
    "W": "#ccc9bf",   # pale belly (model W #dedcd4)
    "m": "#bab7ad",   # soft blotch on the belly
    "F": "#6b675e",   # fin at the base (model F #7a766d)
    "G": "#5d5951",   # fin, mid (model G #6c685f)
    "H": "#4f4b44",   # fin tip (model H #5e5a53)
    "f": "#7d796f",   # fin, lit leading edge (model f #8a867c)
    "c": "#c0bdb3",   # the clavus's pale rim (model c #c8c5bc)
    "k": "#a29e95",   # the fold where the clavus meets the disc
    "P": "#b0aca2",   # pectoral fin, pale so it never pairs with the eye (model P #a09c93)
    "p": "#8f8b81",   # its base
    "E": "#1e1f21",   # the eye (model E #25272a)
    "q": "#4a4641",   # the mouth's opening (dark brown-grey, not the eye's black)
    "O": "#46423c",   # rim on the lit top-left side
    "o": "#33302b",   # rim on the shaded side
}.items()}

# A: side view, upright. Disc x 2-10, rows 4-13; dorsal rows 0-4 and anal rows 12-15 rise from x 9-10 (far back) and
# lean back to their tips at x 10-11; clavus: fold k at x 11, rim c at x 12, lobes at x 13 on rows 6-7, 9-10 and 12,
# notches on rows 8 and 11 (the outline steps in). Mouth q at the front tip (2,9), two rows below the eye (5,7).
# Critic round 1: the disc's top and bottom rims were straight 4-5 px walls; now they step 2-3 px (5,4 and 4,13 cut,
# 5,5 and 4,12 rim), and the anal fin's base is one pixel broader (8,13).
A = [
    "..........oo....",
    ".........OHo....",
    ".........fGo....",
    "........OfGo....",
    "......OOOfFo....",
    "....OOhBBBFco...",
    "...OhBBBBBBkcco.",
    "..OhhEUBUUUkcco.",
    "..OUUUSUnUSkco..",
    ".OqSSSLSSnSkcco.",
    "..oSLSSPLSLkcco.",
    "..oLWLPpWmLkco..",
    "...oomWWWLFkcco.",
    ".....oooFFGcoo..",
    ".........fGo....",
    ".........oHo....",
]

# B: tilted about 20 degrees, head down to the left; the fins lean back with the body, the clavus steps down the right.
B = [
    ".......OO.......",
    "......OHHo......",
    "......OHGo......",
    "......OfGo......",
    ".....OOfGo......",
    "...OOhBBfco.....",
    "..OhhBBBBkcco...",
    "..OhBBUUUkcco...",
    ".OUBEUnUSSkco...",
    ".OUUSUSSSLkcco..",
    ".OSSSPLSLWkcco..",
    ".OqSPpWWmWWkco..",
    "..oLWWmWWWFkcco.",
    "...ooWWWWofGoo..",
    ".....oooo.ofHo..",
    "...........oo...",
]

# C: tilted about 40 degrees, nearer vanilla's diagonal; the dorsal fin rises up and back to the top left, the anal fin
# trails down to the bottom right.
C = [
    "...oo...........",
    "...OHo..........",
    "...OHGo.........",
    "...OfGo.........",
    "....OfGo........",
    "....OffFooo.....",
    "...OhhBBkcco....",
    "..OhBBBBBkcco...",
    ".OhBBBUUSkco....",
    ".OUBEUUSnSkcco..",
    ".OUUUSSSLLWkcco.",
    ".OqSSSPLWWmWkco.",
    "..oSSPpWWWWFkco.",
    "...oLWWmWWofGoo.",
    "....ooWWWo.ofHHo",
    "......ooo...ooo.",
]

CANDIDATES = {"A": A, "B": B, "C": C}
NOTES = {
    "A": "A: side view, upright, fins straight up and down",
    "B": "B: a slight diagonal (about 20 degrees), head down to the left",
    "C": "C: a stronger diagonal (about 40 degrees), nearer vanilla's",
}

ACCEPTED = ("lampuka", "tonn", "cerna", "boll", "skorfna", "awrata")
VAN_FISH = ("cod", "salmon", "pufferfish", "tropical_fish")


def render(rows):
    assert len(rows) == 16
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), PAL[ch] + (255,))
    return im


def check(name, rows):
    """Warn about stray pixels (no opaque 8-neighbour) and flat outline runs longer than 4 px; return coverage."""
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            if not any(0 <= x + dx < 16 and 0 <= y + dy < 16 and rows[y + dy][x + dx] != "."
                       for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy):
                print(f"warning: {name}: stray pixel at {x},{y}")
        for run in row.replace(".", " ").split():
            if len(run) >= 5 and set(run) <= {"o", "O"}:
                print(f"warning: {name}: flat outline run of {len(run)} in row {y}")
    return sum(1 for r in rows for c in r if c != ".") / 256


def copy_check(name, icon):
    """Exact-pixel copy check against every vanilla item texture: any pixel with vanilla's place and colour fails."""
    ours = {(x, y): icon.getpixel((x, y)) for x in range(16) for y in range(16) if icon.getpixel((x, y))[3] > 0}
    hits, vcols = [], set()
    for f in sorted(glob.glob(os.path.join(VANILLA, "*.png"))):
        v = Image.open(f).convert("RGBA")
        if v.size != (16, 16):
            continue
        same = [p for p, c in ours.items() if v.getpixel(p) == c]
        if same:
            hits.append((len(same), os.path.basename(f)))
        vcols |= {v.getpixel((x, y))[:3] for x in range(16) for y in range(16) if v.getpixel((x, y))[3] > 0}
    shared = {c[:3] for c in ours.values()} & vcols
    n = sum(k for k, _ in hits)
    line = (f"{name}: pixels with a vanilla item's place and colour: {n}"
            + (f" ({', '.join(f'{k} in {f}' for k, f in sorted(hits, reverse=True)[:3])})" if hits else "")
            + f"; our colours also used anywhere in a vanilla item: {len(shared)}")
    return line, n


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


def tiles(band, im, x0, y0):
    """The icon at 8x, then 1x and 2x on light grey and on the slot's dark grey #2b2b2b."""
    tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
    tile.alpha_composite(im.convert("RGBA").resize((128, 128), Image.NEAREST))
    band.paste(tile.convert("RGB"), (x0, y0))
    for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((43, 43, 43), 1), ((43, 43, 43), 2))):
        t = Image.new("RGBA", (16 * s + 8, 16 * s + 8), col + (255,))
        t.alpha_composite(im.convert("RGBA").resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (x0 + 136 + (j % 2) * 44, y0 + (j // 2) * 46))


def text_band(lines, W, bg, ink):
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    return band


def cand_path(name):
    return os.path.join(CAND, f"fish_mola_icon_{name}.png")


def hotbars(icons):
    """Offline hotbar previews, the mola unselected among vanilla items, at GUI scale 1 and 2 (light and dark)."""
    py = os.path.join(ART, ".venv", "bin", "python")
    tool = os.path.join(ART, "tools", "hotbar_preview.py")
    out = {}
    for name in icons:
        items = ["mc:cod", "mc:apple", "mc:bread", f"file:{cand_path(name)}", "mc:salmon", "mc:carrot",
                 "mc:pufferfish", "mc:cooked_beef", "mc:tropical_fish"]
        ims = []
        for scale in (1, 2):
            tmp = os.path.join(CAND, f"fish_mola_icon_hotbar_{name}_s{scale}.png")
            subprocess.run([py, tool, tmp] + items + ["--scale", str(scale)], check=True, capture_output=True)
            ims.append(Image.open(tmp).convert("RGB"))
            os.remove(tmp)
        w = max(im.width for im in ims) + 16
        both = Image.new("RGB", (w, sum(im.height for im in ims) + 24), (139, 139, 139))
        y = 8
        for im in ims:
            both.paste(im, (8, y))
            y += im.height + 8
        both.save(os.path.join(CAND, f"fish_mola_icon_hotbar_{name}.png"))
        out[name] = both
    x4 = os.path.join(CAND, "fish_mola_icon_hotbar_x4.png")
    subprocess.run([py, tool, x4, "mc:cod", "mod:cerna"] + [f"file:{cand_path(n)}" for n in icons]
                   + ["mc:salmon", "mod:tonn", "mc:pufferfish", "mod:boll"] + ["--scale", "4"],
                   check=True, capture_output=True)
    out["x4"] = Image.open(x4).convert("RGB")
    return out


def sheet(icons, copy_lines):
    font, small = label_font(16), label_font(13)
    W = 2000
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    # references and the accepted model's texture
    band = Image.new("RGB", (W, 290), bg)
    d = ImageDraw.Draw(band)
    x = 10
    for name in ("mm07.jpg", "mm10.jpg", "mm04.jpg", "mm01.jpg"):
        p = os.path.join(REFS, name)
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im.thumbnail((340, 250), Image.LANCZOS)
            band.paste(im, (x, 26))
            d.text((x, 4), f"{name} (reference only)", fill=ink, font=small)
            x += im.width + 12
    tex = Image.open(MODEL_TEX).convert("RGBA")
    tex = tex.resize((tex.width * 2, tex.height * 2), Image.NEAREST)
    t = Image.new("RGBA", tex.size, (139, 139, 139, 255))
    t.alpha_composite(tex)
    band.paste(t.convert("RGB"), (x, 26))
    d.text((x, 4), "accepted model texture (2x)", fill=ink, font=small)
    parts.append(("References (art/references/fish_mola_refonly, list.tsv) and the accepted model's texture", band))

    # palette
    band = Image.new("RGB", (W, 60), bg)
    d = ImageDraw.Draw(band)
    for i, (k, rgb) in enumerate(PAL.items()):
        d.rectangle((10 + i * 90, 4, 10 + i * 90 + 84, 40), fill=rgb)
        d.text((12 + i * 90, 6), k, fill=(255, 255, 255) if sum(rgb) < 380 else (0, 0, 0), font=small)
        d.text((12 + i * 90, 24), "#%02x%02x%02x" % rgb, fill=(255, 255, 255) if sum(rgb) < 380 else (0, 0, 0),
               font=label_font(11))
    parts.append(("Palette: the model's hues a step darker for out of water, plus the rim, eye and mouth", band))

    # candidates beside vanilla and the accepted fish
    items = [(NOTES[n] + (" (installed)" if n == INSTALLED else ""), im) for n, im in icons.items()]
    items += [(f"vanilla {n}", Image.open(os.path.join(VANILLA, f"{n}.png")).convert("RGBA")) for n in VAN_FISH]
    items += [(f"{n} (accepted)", Image.open(os.path.join(TEXTURES, "item", f"{n}.png")).convert("RGBA"))
              for n in ACCEPTED]
    per_row = 8
    rows_n = (len(items) + per_row - 1) // per_row
    band = Image.new("RGB", (W, rows_n * 172 + 24), bg)
    d = ImageDraw.Draw(band)
    for i, (name, im) in enumerate(items):
        x0, y0 = 10 + (i % per_row) * 246, 22 + (i // per_row) * 172
        tiles(band, im, x0, y0)
        d.text((x0, y0 - 20), name[:34], fill=ink, font=small)
    d.text((10, rows_n * 172), "8x, then 1x and 2x on light grey and on the slot's dark grey #2b2b2b", fill=ink,
           font=small)
    parts.append(("The candidates at 8x, 1x and 2x beside vanilla's fish and our accepted fish icons", band))

    # numbers and the copy check
    lines = measure([cand_path(n) for n in icons]
                    + [os.path.join(TEXTURES, "item", f"{n}.png") for n in ACCEPTED]
                    + [os.path.join(VANILLA, f"{n}.png") for n in VAN_FISH])
    lines.append("STYLE.md food ranges: cover 0.29-0.77, colours 6-20, dark 0.0-0.35, light 0.32-0.99, TL-BR +0.01-+0.17")
    lines += copy_lines
    parts.append(("art/tools/measure.py and the copy check", text_band(lines, W, bg, ink)))

    # hotbars
    hb = hotbars(icons)
    names = list(icons) + ["x4"]
    band = Image.new("RGB", (W, sum(hb[n].height + 10 for n in names) + 10), bg)
    y = 4
    for n in names:
        band.paste(hb[n], (10, y))
        ImageDraw.Draw(band).text((hb[n].width + 20, y + 4), f"candidate {n}" if n != "x4" else
                                  "scale 4: cod, cerna, " + ", ".join(icons) + ", salmon, tonn, pufferfish, boll",
                                  fill=ink, font=small)
        y += hb[n].height + 10
    parts.append(("Hotbar preview (offline, as the game draws flat items): the mola unselected in slot 4 among cod, "
                  "apple, bread, salmon, carrot, pufferfish, steak, tropical fish; GUI scale 1 then 2", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Mola mola (ocean sunfish) item icon, textures/item/mola_mola.png", fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    out.save(OUT_SHEET)


def main():
    os.makedirs(CAND, exist_ok=True)
    icons, copy_lines, copied = {}, [], 0
    for name, rows in CANDIDATES.items():
        cov = check(name, rows)
        icons[name] = render(rows)
        line, n = copy_check(name, icons[name])
        print(f"{name}: coverage {cov:.2f}; {line}")
        copy_lines.append("copy check " + line)
        copied += n
        icons[name].save(cand_path(name), optimize=False)
    if copied:
        sys.exit("copy check failed: a pixel matches a vanilla item texture in place and colour")
    icons[INSTALLED].save(OUT_ICON, optimize=False)
    sheet(icons, copy_lines)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), f"(candidate {INSTALLED}) and", os.path.relpath(OUT_SHEET, ROOT))


if __name__ == "__main__":
    main()
