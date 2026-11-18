"""Item icon for the tonn (Atlantic bluefin tuna, Thunnus thynnus): the caught fish, like vanilla cod and salmon.

What makes it a tonn (photos and drawings in art/references/fish_tonn_refonly/, list.tsv):
- a thick torpedo body, deepest a third of the way back, tapering to a very thin tail stalk;
- a pointed, conical snout;
- a stiff crescent (lunate) tail, both lobes long and thin, dark blue-black;
- a deep blue-black back and silver-white sides and belly (countershading);
- small yellow finlets with dark edges in a row along the top and bottom of the tail stalk;
- a greyish-yellow second dorsal and anal fin, and a short dark pectoral fin behind the gill.

Pose and light follow vanilla's fish items (measured with art/tools/measure.py, never copied): head lower left, tail
upper right, light from the top left, lit edges a mid tone and shaded edges dark. A tuna's dark back faces that light,
which would make the icon darker on the lit side; the back is drawn as a glossy navy with a cobalt sheen along its
upper edge (the sky reflection seen on live bluefin, tonn_06), and the silver belly takes the shade on its lower right.

Run:  art/.venv/bin/python art/src/fish_tonn_icon.py
Writes mod/.../textures/item/tonn.png (byte-identical on rerun) and art/candidates/fish_tonn_icon.png (compare sheet,
with the in-game hotbar crop from .art-runs/tonnicon2/ if that run exists).
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
OUT_ICON = os.path.join(TEXTURES, "item", "tonn.png")
OUT_SHEET = os.path.join(ART, "candidates", "fish_tonn_icon.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_tonn_refonly")
SHOTS = os.path.join(ROOT, ".art-runs", "tonnicon2", "build", "smoke-run", "screenshots")


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAL = {
    # back: lit edge, cobalt sheen, deep navy, and the bright blue band where the back meets the silver
    "h": hx("#6584b8"), "H": hx("#a0b8dc"), "k": hx("#1f2d52"), "b": hx("#3a5e98"),
    # silver side and belly: white where the light falls, silver, grey and dark grey toward the shaded lower right
    "w": hx("#e8edf1"), "s": hx("#b4bfcb"), "g": hx("#848fa0"), "G": hx("#5a6476"),
    "o": hx("#181e2c"),                       # shaded edge (belly side, under the jaw, lower tail lobe tip)
    "e": hx("#0a0a0a"),                       # eye
    "p": hx("#1f2a44"),                       # pectoral fin
    "f": hx("#7a7a6e"), "F": hx("#a8a07a"),   # second dorsal fin and its tip (greyish yellow)
    "a": hx("#3e4252"), "A": hx("#5c5a4c"),   # anal fin and its tip, in the shade
    "y": hx("#f0c828"), "Y": hx("#a8801a"),   # finlets: lit (top), shaded (bottom)
    "t": hx("#1b2746"), "T": hx("#5677ae"),   # tail (both lobes navy), one lit pixel on the upper lobe
}

# Head lower left (pointed snout at 0,13; eye at 2,11), tail upper right. Round 2 (critic): the body is deepest at
# x 2-5 and tapers on both sides to a 1-2 pixel stalk at 10-11,4-5 (the belly edge steps up diagonally, no vertical
# cut); the crescent lobes are equal and navy, up from the stalk (x 11, tip bent to 12,1) and right (row 4, tip bent to
# 14,3); two finlets each side of the stalk only; the pectoral fin sits under the navy band behind the gill (5,10).
TONN = [
    "................",
    "...........tt...",
    "...........t....",
    "...........T..t.",
    "......F...ytttt.",
    "......f.yhkoY...",
    "......hHkbwo....",
    "....hHHkbwoY....",
    "...hHHkkwso.....",
    "..hHHkbwsoaA....",
    "..hHkpwsgo......",
    ".hekbwsgo.......",
    ".hbwwsgGo.......",
    "hwwsgGoo........",
    ".oooo...........",
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
    for name in ("tonn_02.jpg", "tonn_06.jpg", "tonn_13.jpg", "tonn_04.jpg"):
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
        parts.append(("References (art/references/fish_tonn_refonly, list.tsv)", band))

    # 8x and 1x beside vanilla and the lampuka
    items = [("vanilla cod", os.path.join(VANILLA, "cod.png")),
             ("vanilla salmon", os.path.join(VANILLA, "salmon.png")),
             ("vanilla tropical fish", os.path.join(VANILLA, "tropical_fish.png")),
             ("lampuka (accepted)", os.path.join(TEXTURES, "item", "lampuka.png")),
             ("TONN", None)]
    band = Image.new("RGB", (W, 128 + 90), bg)
    d = ImageDraw.Draw(band)
    for i, (name, p) in enumerate(items):
        im = icon if p is None else Image.open(p).convert("RGBA")
        x0 = 10 + i * 244
        tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
        tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
        band.paste(tile.convert("RGB"), (x0, 22))
        d.text((x0, 2), name, fill=ink, font=small)
        for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
            t = Image.new("RGBA", (16 * s + 8, 16 * s + 8), col + (255,))
            t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
            band.paste(t.convert("RGB"), (x0 + 136 + (j % 2) * 44, 22 + (j // 2) * 46))
    d.text((10, 160), "8x, then 1x and 2x on light and dark grey", fill=ink, font=small)
    parts.append(("The icon at 8x and 1x beside vanilla cod, salmon, tropical fish and our lampuka", band))

    # numbers
    lines = measure([os.path.join(VANILLA, "cod.png"), os.path.join(VANILLA, "salmon.png"),
                     os.path.join(VANILLA, "tropical_fish.png"), os.path.join(TEXTURES, "item", "lampuka.png"),
                     OUT_ICON])
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
    d.text((10, 8), "Tonn (Atlantic bluefin tuna) item icon, textures/item/tonn.png", fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    os.makedirs(os.path.dirname(OUT_SHEET), exist_ok=True)
    out.save(OUT_SHEET)


def main():
    check(TONN)
    icon = render(TONN)
    icon.save(OUT_ICON, optimize=False)
    sheet(icon)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), "and", os.path.relpath(OUT_SHEET, ROOT))


if __name__ == "__main__":
    main()
