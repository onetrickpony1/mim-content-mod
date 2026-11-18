"""Item icon for the sardina (European sardine, Sardina pilchardus): the caught fish, like vanilla cod and salmon.

What makes it a sardina (photos and drawings in art/references/fish_sardina_refonly/, list.tsv):
- small and slim: a spindle-shaped body, clearly slimmer than the cod icon, tapering to a thin tail stalk;
- a dark blue-green back over bright silver sides and a white belly;
- a row of a few dark spots along the upper flank, just behind the gill cover;
- a gold-tinged gill cover behind a big eye;
- a deeply forked tail, a single small dorsal fin mid-back, small pelvic and anal fins.

Pose and light follow vanilla's fish items (measured with art/tools/measure.py, never copied): head lower left, tail
upper right, light from the top left. The dark back faces that light, so its outer edge is drawn as a lit teal edge
(the sheen on a sardine's back) with the dark blue-green band just inside it, and the shade falls on the belly side.

Run:  art/.venv/bin/python art/src/fish_sardina_icon.py
Writes mod/.../textures/item/sardina.png (byte-identical on rerun) and art/candidates/fish_sardina_icon.png (compare
sheet, with the in-game hotbar crop from .art-runs/sardinaicon3/ if that run exists).
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
OUT_ICON = os.path.join(TEXTURES, "item", "sardina.png")
OUT_SHEET = os.path.join(ART, "candidates", "fish_sardina_icon.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_sardina_refonly")
SHOTS = os.path.join(ROOT, ".art-runs", "sardinaicon3", "build", "smoke-run", "screenshots")


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAL = {
    # back: a lit teal edge where the light falls on it, then the dark blue-green back band
    "h": hx("#8cc6be"), "k": hx("#24525e"),
    # silver side: white just under the back, silver, grey toward the shaded belly, dark outline on the belly
    "w": hx("#eef3f2"), "s": hx("#b4c2c9"), "g": hx("#7e8e99"), "o": hx("#2f3a45"),
    "d": hx("#5f7684"),                       # the row of dark spots along the upper flank (softer than the eye)
    "e": hx("#0a0a0a"),                       # eye
    "y": hx("#dcbc62"), "Y": hx("#a88a44"),   # gold-tinged gill cover: lit, shaded
    "f": hx("#4a7076"),                       # dorsal fin (on the lit back)
    "a": hx("#5f6d78"),                       # pelvic and anal fins (in the shade)
    "T": hx("#587a80"),                       # forked tail, both lobes one tone
}

# Head lower left (snout at 1,12-13; big eye at 3,11 with the gold gill cover behind it), tail upper right.
# The body tapers to a 2 pixel stalk at 9-10,4-5 (belly edge steps up, no vertical cut) and forks at 10,4 into two
# equal lobes in one tone, mirrored about the body axis: up to 11,1 and right to 13,3, with the notch (11,3) open.
# Two soft spots at 7,9 and 9,7 behind the gill, kept lighter than the eye and off its row so they don't read as a
# face. Pelvic (7-8,11-12) and anal (10-11,8-9) fins touch the belly outline.
# Owner 2026-11-18: "just a bit slimmer". The mid body (rows 7-10) is one pixel shallower than before, so the body is
# about 4 px deep against the tonn's 5; coverage drops to 0.27, under the STYLE minimum, by the owner's direction.
SARDINA = [
    "................",
    "...........T....",
    "..........TT....",
    "..........T.TT..",
    ".........hTTT...",
    "........hkg.....",
    "......fhkwso....",
    ".....fhkwdo.....",
    ".....hkwsgoa....",
    "....hkwdgoa.....",
    "...hkwsgo.......",
    "..heysgoa.......",
    ".hwwYgoa........",
    ".hwssgo.........",
    "..oooo..........",
    "................",
]

# The critic-passed version before the owner asked for a slimmer fish (2026-11-18), kept only for the compare sheet.
SARDINA_BEFORE = [
    "................",
    "...........T....",
    "..........TT....",
    "..........T.TT..",
    ".........hTTT...",
    "........hkg.....",
    "......fhkwso....",
    ".....fhkwdgo....",
    ".....hkwssgoa...",
    "....hkwdsgoa....",
    "...hkwssgo......",
    "..heysgoa.......",
    ".hwwYgoa........",
    ".hwssgo.........",
    "..oooo..........",
    "................",
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


def check(rows):
    """Warn about stray pixels (no opaque 4-neighbour)."""
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            if not any(0 <= x + dx < 16 and 0 <= y + dy < 16 and rows[y + dy][x + dx] != "."
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                print(f"warning: stray pixel at {x},{y}")


def measure(paths):
    py = os.path.join(ART, ".venv", "bin", "python")
    res = subprocess.run([py, os.path.join(ART, "tools", "measure.py")] + paths, capture_output=True, text=True)
    lines = []
    for line in res.stdout.splitlines():
        if line.startswith("{"):
            d = eval(line, {"np": __import__("numpy")})  # measure.py prints dicts with numpy floats
            lines.append(f"{d['file']:<18} cover {d['coverage']:.2f}  colours {d['colours']:>2}  dark {d['lmin']:.2f}  "
                         f"light {d['lmax']:.2f}  edge {d['edge_l']:.2f}  inside {d['interior_l']:.2f}  "
                         f"TL-BR {d['tl_minus_br']:+.2f}")
    return lines


def sheet(icon):
    font, small = label_font(16), label_font(13)
    W = 1240
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    # references
    refs = []
    for name in ("side_1.jpg", "sardina_galicia.jpg", "side_3_italy.jpg", "drawing_gervais.jpg"):
        p = os.path.join(REFS, name)
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im = im.resize((300, round(300 * im.height / im.width)), Image.LANCZOS)
            refs.append((name, im))
    if refs:
        h = max(im.height for _, im in refs) + 26
        band = Image.new("RGB", (W, h), bg)
        d = ImageDraw.Draw(band)
        for i, (name, im) in enumerate(refs):
            band.paste(im, (10 + i * 308, 22))
            d.text((10 + i * 308, 2), f"reference {name} (reference only)", fill=ink, font=small)
        parts.append(("References (art/references/fish_sardina_refonly, list.tsv)", band))

    # 8x and 1x beside vanilla and the lampuka
    items = [("vanilla cod", os.path.join(VANILLA, "cod.png")),
             ("vanilla salmon", os.path.join(VANILLA, "salmon.png")),
             ("vanilla tropical fish", os.path.join(VANILLA, "tropical_fish.png")),
             ("lampuka (accepted)", os.path.join(TEXTURES, "item", "lampuka.png")),
             ("tonn (accepted)", os.path.join(TEXTURES, "item", "tonn.png")),
             ("sardina before", "BEFORE"),
             ("SARDINA", None)]
    band = Image.new("RGB", (W, 128 + 100), bg)
    d = ImageDraw.Draw(band)
    for i, (name, p) in enumerate(items):
        im = icon if p is None else render(SARDINA_BEFORE) if p == "BEFORE" else Image.open(p).convert("RGBA")
        x0 = 10 + i * 176
        tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
        tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
        band.paste(tile.convert("RGB"), (x0, 22))
        d.text((x0, 2), name, fill=ink, font=small)
        for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
            t = Image.new("RGBA", (16 * s + 8, 16 * s + 8), col + (255,))
            t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
            band.paste(t.convert("RGB"), (x0 + (0, 26, 70, 96)[j], 154))
    d.text((10, 206), "8x, then 1x and 2x on light and dark grey", fill=ink, font=small)
    parts.append(("The icon at 8x and 1x beside vanilla cod, salmon, tropical fish and our lampuka and tonn, and the sardina before the owner's slimmer request", band))

    # numbers
    lines = measure([os.path.join(VANILLA, "cod.png"), os.path.join(VANILLA, "salmon.png"),
                     os.path.join(VANILLA, "tropical_fish.png"), os.path.join(TEXTURES, "item", "lampuka.png"),
                     os.path.join(TEXTURES, "item", "tonn.png"), OUT_ICON])
    lines.append("STYLE.md food ranges: cover 0.29-0.77, colours 6-20, dark 0.0-0.35, light 0.32-0.99, TL-BR +0.01-+0.17")
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("art/tools/measure.py", band))

    # in-game hotbar crop
    shot = sorted(glob.glob(os.path.join(SHOTS, "*fish-07*.png")))
    if shot:
        im = Image.open(shot[0]).convert("RGB")
        w, h = im.size
        # the hotbar: 182x22 GUI pixels at the bottom centre; the GUI scale is the largest that fits (at most 4)
        gui = max(1, min(4, w // 320, h // 240))
        crop = im.crop((w // 2 - 92 * gui, h - 23 * gui, w // 2 + 92 * gui, h))
        scale = max(1, (W - 20) // crop.width)
        crop = crop.resize((crop.width * scale, crop.height * scale), Image.NEAREST)
        band = Image.new("RGB", (W, crop.height + 30), bg)
        band.paste(crop, (10, 4))
        ImageDraw.Draw(band).text((10, crop.height + 8), os.path.relpath(shot[0], ROOT), fill=ink, font=small)
        parts.append(("In game: hotbar (fish-07), items", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Sardina (European sardine) item icon, textures/item/sardina.png", fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    os.makedirs(os.path.dirname(OUT_SHEET), exist_ok=True)
    out.save(OUT_SHEET)


def main():
    check(SARDINA)
    icon = render(SARDINA)
    icon.save(OUT_ICON, optimize=False)
    sheet(icon)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), "and", os.path.relpath(OUT_SHEET, ROOT))


if __name__ == "__main__":
    main()
