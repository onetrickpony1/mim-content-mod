"""Item icon for the ċerna (dusky grouper, Epinephelus marginatus): the caught fish, like vanilla cod and salmon.

What makes it a ċerna (photos and a drawing in art/references/fish_cerna_refonly/, list.tsv):
- big and heavy: a deep, bulky body, clearly deeper than the lampuka, tonn and sardina icons, with a big head;
- reddish brown, shaded from the lit back to the dark belly, with irregular pale cream blotches on the flank (none on
  the head);
- a large mouth with a jutting lower jaw (pale lips), and a small eye high on the head;
- a long spiny dorsal fin along the back and a short soft dorsal before the tail stalk;
- pelvic and anal fins in a dark shade, touching the belly outline;
- a rounded tail on a short stalk.

Pose and light follow vanilla's fish items (measured with art/tools/measure.py, never copied): head lower left, tail
upper right, light from the top left, so the back carries a lit edge and the belly side falls into shade.

Run:  art/.venv/bin/python art/src/fish_cerna_icon.py
Writes mod/.../textures/item/cerna.png (byte-identical on rerun) and art/candidates/fish_cerna_icon.png (compare
sheet, with the in-game hotbar crop from .art-runs/cernaicon4/ if that run exists).
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
OUT_ICON = os.path.join(TEXTURES, "item", "cerna.png")
OUT_SHEET = os.path.join(ART, "candidates", "fish_cerna_icon.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_cerna_refonly")
SHOTS = os.path.join(ROOT, ".art-runs", "cernaicon4", "build", "smoke-run", "screenshots")


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# Rework after the owner (2026-11-18): "it needs reworking, it has very hard edges e.g., its mouth, and very flat
# colours". Studied first: vanilla cod, salmon and cooked salmon round every outline with 1-2 pixel steps and a darker
# rim (lighter on the lit back, darkest on the belly), and fill the body with 4-6 mixed shades plus highlights, not
# flat bands; our tonn and lampuka do the same with a light ramp from the top-left back to the bottom-right belly.
PAL = {
    # body light ramp, lit back (top left) to shaded belly (bottom right): 1 lit, 2, 3 mid, 4, 5 deep shade
    "h": hx("#c8956a"),                       # the brightest light on the back, behind the dorsal
    "1": hx("#b27a55"), "2": hx("#a66c4a"), "3": hx("#93593f"), "4": hx("#7a4434"), "5": hx("#5e3228"),
    "k": hx("#7a4632"),                       # rim on the lit back and head (lighter than the belly rim)
    "o": hx("#2e1a14"),                       # rim on the shaded belly side
    "C": hx("#ccac88"), "c": hx("#a8866a"),   # pale blotches: in the light, and partly shaded
    "e": hx("#0a0a0a"),                       # small eye, high on the head (the only black)
    "L": hx("#b07a5e"), "l": hx("#8a5844"),   # lips and jutting lower jaw: lit, shaded
    "M": hx("#4e2a1e"),                       # the corner of the mouth (brown, not black)
    "D": hx("#5a3224"), "f": hx("#8a5440"),   # dorsal fin along the back: dark spines, lit membrane
    "A": hx("#5a3426"),                       # pelvic and anal fins, in the shade
    "T": hx("#9a5e48"), "t": hx("#7a4838"), "u": hx("#4a2a20"),  # rounded tail: lit, mid, shaded rim
}

# Head lower left: a rounded head whose front steps in at both ends like vanilla cod's (x 2 at rows 8-9, x 1 at rows
# 10-13, x 2 at row 14). The mouth opens at the tip: a brown corner (1,12, not black) above the lower lip (1-2,13).
# Small eye at 2,10, high on the head inside the lit rim. Every outline steps by 1-3 pixels. Second rework (critic,
# 2026-11-18): a wider light ramp (1-5, ochre light to deep red-brown shade), one highlight behind the dorsal (h, 6,5),
# darker mottling among the pale blotches (4 at 4,6, 3,8, 5,7, 6,8, 3,10 and 7,5 as 3) so the flank is patchy like the
# real fish, and a shaded blotch low on the flank (5-6,11). The dark mottling in the top left also keeps the
# light direction at +0.17. It tapers to the stalk at 10,4 under the soft dorsal (8-9,3); the anal fin (12,7 and 11,8)
# covers the steepest part of the belly. The rounded tail fan is lit at its upper left and darkens to a rim at its
# outer edge. The long spiny dorsal runs along the back from 2,7 to 7,4; the pelvic fin (9,12 and 8,13) touches the
# belly outline.
CERNA = [
    "............Tt..",
    "...........TTtu.",
    "...........Tttu.",
    "........DD.ttuu.",
    "......Df234tu...",
    "....Dfh3234o....",
    "...f132CC34o....",
    "..D12433c45oA...",
    "..14C34345oA....",
    "..12CC3c45o.....",
    ".ke42334c5o.....",
    ".2233cc55o......",
    ".M334455oA......",
    ".Ll455ooA.......",
    "..oooo..........",
    "................",
]

# The first rework (cernaicon3), which the critic found too close to the rejected one at 1x; kept for the sheet only.
V3_PAL = dict(PAL, **{"1": hx("#aa6b55"), "2": hx("#a0624c"), "3": hx("#93593f"), "4": hx("#7c4a35"), "5": hx("#663c2c")})
V3 = [
    "............Tt..",
    "...........TTtu.",
    "...........Tttu.",
    "........DD.ttuu.",
    "......Df234tu...",
    "....Df12234o....",
    "...f112CC34o....",
    "..D12233c45oA...",
    ".D12C33345oA....",
    ".k12CC3c45o.....",
    ".ke22334c5o.....",
    ".L2334455o......",
    ".M334455oA......",
    "lLl455ooA.......",
    ".loooo..........",
    "................",
]

# The version the owner sent back (2026-11-18, after the critic's fixes), kept only for the compare sheet.
REJECTED_PAL = {
    "h": hx("#a06c50"), "m": hx("#93593f"), "d": hx("#764533"), "g": hx("#553222"), "o": hx("#2a1812"),
    "C": hx("#c4a684"), "e": hx("#0a0a0a"), "M": hx("#3e2418"), "l": hx("#b08060"), "y": hx("#a07a50"),
    "f": hx("#3e2418"), "a": hx("#4a2e20"), "t": hx("#5a3428"),
}
REJECTED = [
    "............tt..",
    "...........tttt.",
    "...........ttttt",
    "........ff.tttt.",
    "......ffhhhtt...",
    "....fffhmmdo....",
    "...fhhmCCmdo....",
    "..fhmmmmCdoa....",
    ".fhmCmmmddgo....",
    ".hmCCmmCddo.....",
    ".hemmmmCdgo.....",
    "hhmmmmddgo......",
    "hMmmdddggo......",
    "lyMddggoao......",
    "lllyoo..........",
    "................",
]


def render(rows, pal=PAL):
    assert len(rows) == 16
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), pal[ch] + (255,))
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
    W = 1600
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    # references
    refs = []
    for name in ("side_1.jpg", "caught_1.jpg", "drawing_1.jpg", "side_4.jpg"):
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
        parts.append(("References (art/references/fish_cerna_refonly, list.tsv)", band))

    # 8x and 1x beside vanilla and the lampuka
    items = [("vanilla cod", os.path.join(VANILLA, "cod.png")),
             ("vanilla salmon", os.path.join(VANILLA, "salmon.png")),
             ("vanilla tropical fish", os.path.join(VANILLA, "tropical_fish.png")),
             ("lampuka (accepted)", os.path.join(TEXTURES, "item", "lampuka.png")),
             ("tonn (accepted)", os.path.join(TEXTURES, "item", "tonn.png")),
             ("sardina (accepted)", os.path.join(TEXTURES, "item", "sardina.png")),
             ("rejected (owner)", "REJECTED"),
             ("rework 1 (cernaicon3)", "V3"),
             ("CERNA", None)]
    band = Image.new("RGB", (W, 128 + 100), bg)
    d = ImageDraw.Draw(band)
    for i, (name, p) in enumerate(items):
        im = icon if p is None else render(REJECTED, REJECTED_PAL) if p == "REJECTED" else render(V3, V3_PAL) if p == "V3" else Image.open(p).convert("RGBA")
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
    parts.append(("The icon at 8x and 1x beside vanilla cod, salmon, tropical fish and our accepted lampuka, tonn and sardina, then the version the owner sent back and the first rework", band))

    # numbers
    lines = measure([os.path.join(VANILLA, "cod.png"), os.path.join(VANILLA, "salmon.png"),
                     os.path.join(VANILLA, "tropical_fish.png"), os.path.join(TEXTURES, "item", "lampuka.png"),
                     os.path.join(TEXTURES, "item", "tonn.png"), os.path.join(TEXTURES, "item", "sardina.png"),
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
    d.text((10, 8), "Ċerna (dusky grouper) item icon, textures/item/cerna.png", fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    os.makedirs(os.path.dirname(OUT_SHEET), exist_ok=True)
    out.save(OUT_SHEET)


def main():
    check(CERNA)
    icon = render(CERNA)
    icon.save(OUT_ICON, optimize=False)
    sheet(icon)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), "and", os.path.relpath(OUT_SHEET, ROOT))


if __name__ == "__main__":
    main()
