"""Item icon for the awrata (gilthead sea bream, Sparus aurata): the caught fish, like vanilla cod and salmon.

What makes it an awrata (photos and a drawing in art/references/fish_awrata_refonly/, list.tsv):
- an oval, deep-bodied but flat bream: deeper than the lampuka and sardina icons, less heavy than the ċerna;
- a silver-grey body with thin dark lines along it, and a slightly darker blue-grey back;
- a GOLDEN band across the forehead between the eyes (the fish is named after it);
- a dark patch at the top of the gill cover, with a red-orange touch below it;
- a steep rounded forehead, a small mouth with thick lips, and a forked tail with darker edges.

Pose and light follow vanilla's fish items (measured with art/tools/measure.py, never copied) and our accepted
lampuka, tonn and sardina: head lower left, tail upper right, light from the top left. The silver runs a light ramp
from a sheen just under the blue-grey back down to the shaded belly, with a dark rim on the belly side.

This icon sets the awrata's look and palette: its bucket, spawn egg and model copy PAL below.

Run:  art/.venv/bin/python art/src/fish_awrata_icon.py
Writes mod/.../textures/item/awrata.png (byte-identical on rerun) and art/candidates/fish_awrata_icon.png (compare
sheet, with an offline hotbar preview from art/tools/hotbar_preview.py, also saved as
art/candidates/fish_awrata_icon_hotbar.png and _hotbar_x4.png).
"""
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
OUT_ICON = os.path.join(TEXTURES, "item", "awrata.png")
OUT_SHEET = os.path.join(ART, "candidates", "fish_awrata_icon.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_awrata_refonly")
HOTBAR = ["mc:cod", "mc:salmon", "mod:lampuka", "mod:tonn", "mod:sardina", "mod:cerna", "mod:awrata"]


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAL = {
    # blue-grey back: the rim where the light falls on it (also the dorsal fin), and the band just inside it
    "K": hx("#4f6477"), "b": hx("#7d91a3"),
    # silver light ramp, from the sheen under the back (W) to the shaded belly (5); 3 and 4 also draw the thin dark
    # lines along the body, one tone darker than the silver around them
    "W": hx("#e6ecee"), "1": hx("#cdd6db"), "2": hx("#b4bec6"), "3": hx("#9ba7b1"), "4": hx("#83909b"),
    "5": hx("#6b7783"),
    "o": hx("#343d47"),                       # rim on the shaded belly side
    "O": hx("#56626e"),                       # softer rim: tail stalk, pelvic and anal fins, mouth corner
    "e": hx("#0a0a0a"),                       # eye (the only black)
    "G": hx("#e8bf4c"), "g": hx("#c39a42"),   # golden forehead band: lit, shaded
    "p": hx("#68747f"), "P": hx("#46535e"),   # dark patch at the top of the gill cover: soft edge, core
    "R": hx("#b8664a"),                       # red-orange touch below the gill patch
    "L": hx("#a2aab1"),                       # thick lips
    "t": hx("#46535e"),                       # darker edges of the forked tail (same tone as the gill patch core)
}

# Reshaped after the critic (2026-11-18): the first version shared 0.85 of its outline with the ċerna and was widest
# at the head, so it read as "a silver ċerna". Now an oval bream, deepest at mid-body (11 px across the diagonal at
# u = x-y from -3 to 1), with a smaller head (7-9) and a narrower stalk; coverage 0.38 against the ċerna's 0.43.
# The back rises in a soft hump behind the head (rows 5-6 step out to x 5 and 4) and steps down to the stalk at 10,3.
# Head lower left: the small mouth sits at the tip (lip 2,12, corner 3,13). The eye (4,10) sits high on the head.
# The golden band runs over the forehead just above the eye (4,9 lit, 3,9 shaded where it meets the rim), with light
# silver (3,10) in front of the eye, so it reads as a mark across the head, not a beak or a crown. The gill patch is
# one joined diagonal stroke behind and above the eye, never touching it: a soft smudge (5,8 core, 6,8 edge), its
# core running down to 6,9 and ending in the red-orange foot at 7,9, touching the stroke (at 7,10, in the eye's row,
# the critic found it read as a second eye). Thin lines run along the body on the
# diagonals x+y = 15 (b, the lightest dark, on the lit silver) and 17-18 (one tone darker than the silver around).
# The forked tail: an upper lobe straight up (11-12, 0-2) and a lower lobe to the right (13-14, 2-3), mirrored about
# the body axis with the notch at 13,1, light at the base and dark at the edges. Pelvic (11,11) and anal (13,8)
# fins break the belly outline so no edge runs straight for more than 3 pixels there.
# Owner 2026-11-18, on accepting it: "move the icon one pixel down so it doesnt touch the edges at the top". The grid
# below is shifted down 1 px; the pixel positions in the notes above are from before the shift (add 1 to y).
AWRATA = [
    "................",
    "...........tt...",
    "...........4t...",
    "...........34tt.",
    "..........K334t.",
    ".......KKb2O....",
    ".....KKbW13o....",
    "....KbWW1b24o...",
    "....Kb1Wb244o...",
    "...KbPpb2345oO..",
    "...gG1PR435o....",
    "..K1e122345o....",
    "..K1224345oO....",
    "..L23445oo......",
    "...Ooooo........",
    "................",
]

# The first version, sent back by the critic for sharing the ċerna's build; kept only for the compare sheet.
AWRATA_BEFORE = [
    "...........tt...",
    "...........4t...",
    "...........34tt.",
    "..........K334t.",
    "......KbKb2O....",
    ".....KKbW23o....",
    "....KbWW2324o...",
    "...Kbp1W3234o...",
    "..Kb1Pp32345oO..",
    "..bg12p3345o....",
    ".KGe13R345o.....",
    ".K1232345oO.....",
    ".L233445o.......",
    ".O3445oo........",
    "..Looo..........",
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
    W = 1260
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    # references
    refs = []
    for name in ("awrata_02.jpg", "awrata_06.jpg", "awrata_08.jpg", "awrata_09.jpg"):
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
            d.text((10 + i * 308, 2), f"{name} (reference only)", fill=ink, font=small)
        parts.append(("References (art/references/fish_awrata_refonly, list.tsv)", band))

    # 8x and 1x beside vanilla and our fish
    items = [("vanilla cod", os.path.join(VANILLA, "cod.png")),
             ("vanilla salmon", os.path.join(VANILLA, "salmon.png")),
             ("lampuka (accepted)", os.path.join(TEXTURES, "item", "lampuka.png")),
             ("tonn (accepted)", os.path.join(TEXTURES, "item", "tonn.png")),
             ("sardina (accepted)", os.path.join(TEXTURES, "item", "sardina.png")),
             ("ċerna (rework)", os.path.join(TEXTURES, "item", "cerna.png")),
             ("awrata before", "BEFORE"),
             ("AWRATA", None)]
    band = Image.new("RGB", (W, 128 + 100), bg)
    d = ImageDraw.Draw(band)
    for i, (name, p) in enumerate(items):
        im = icon if p is None else render(AWRATA_BEFORE) if p == "BEFORE" else Image.open(p).convert("RGBA")
        x0 = 10 + i * 156
        tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
        tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
        band.paste(tile.convert("RGB"), (x0, 22))
        d.text((x0, 2), name, fill=ink, font=small)
        for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
            t = Image.new("RGBA", (16 * s + 8, 16 * s + 8), col + (255,))
            t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
            band.paste(t.convert("RGB"), (x0 + (0, 26, 70, 96)[j], 154))
    d.text((10, 206), "8x, then 1x and 2x on light and dark grey", fill=ink, font=small)
    parts.append(("The icon at 8x and 1x beside vanilla cod and salmon, our lampuka, tonn, sardina and ċerna, and the "
                  "awrata before the reshape", band))

    # outline overlap with the ċerna (shared opaque pixels over all opaque pixels of either)
    def mask(im):
        return {(x, y) for y in range(16) for x in range(16) if im.getpixel((x, y))[3]}
    cerna = mask(Image.open(os.path.join(TEXTURES, "item", "cerna.png")).convert("RGBA"))
    rows = []
    for name, im in (("lampuka", Image.open(os.path.join(TEXTURES, "item", "lampuka.png")).convert("RGBA")),
                     ("tonn", Image.open(os.path.join(TEXTURES, "item", "tonn.png")).convert("RGBA")),
                     ("sardina", Image.open(os.path.join(TEXTURES, "item", "sardina.png")).convert("RGBA")),
                     ("awrata before", render(AWRATA_BEFORE)), ("awrata", icon)):
        m = mask(im)
        rows.append(f"{name}: {len(m & cerna) / len(m | cerna):.2f}")
    band = Image.new("RGB", (W, 28), bg)
    ImageDraw.Draw(band).text((10, 4), "   ".join(rows), fill=ink, font=label_font(14))
    parts.append(("Outline overlap with the ċerna (intersection over union of the opaque pixels)", band))

    # palette
    band = Image.new("RGB", (W, 60), bg)
    d = ImageDraw.Draw(band)
    for i, (k, c) in enumerate(PAL.items()):
        x0 = 10 + i * 66
        d.rectangle((x0, 4, x0 + 28, 32), fill=c)
        d.text((x0, 36), f"{k} #{c[0]:02x}{c[1]:02x}{c[2]:02x}", fill=ink, font=label_font(11))
    parts.append(("Palette (the bucket, egg and model copy these)", band))

    # numbers
    lines = measure([os.path.join(VANILLA, "cod.png"), os.path.join(VANILLA, "salmon.png"),
                     os.path.join(TEXTURES, "item", "lampuka.png"), os.path.join(TEXTURES, "item", "tonn.png"),
                     os.path.join(TEXTURES, "item", "sardina.png"), os.path.join(TEXTURES, "item", "cerna.png"),
                     OUT_ICON])
    lines.append("STYLE.md food ranges: cover 0.29-0.77, colours 6-20, dark 0.0-0.35, light 0.32-0.99, TL-BR +0.01-+0.17")
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("art/tools/measure.py", band))

    # hotbar preview (offline, art/tools/hotbar_preview.py: the flat icon drawn in the vanilla hotbar at GUI scale 4)
    preview = os.path.join(ART, "candidates", "fish_awrata_icon_hotbar_x4.png")
    subprocess.run([os.path.join(ART, ".venv", "bin", "python"), os.path.join(ART, "tools", "hotbar_preview.py"),
                    preview] + HOTBAR + ["--select", "6", "--scale", "4"], check=True, capture_output=True)
    im = Image.open(preview).convert("RGB")
    if im.width > W - 20:
        im = im.resize((W - 20, round(im.height * (W - 20) / im.width)), Image.NEAREST)
    band = Image.new("RGB", (W, im.height + 30), bg)
    band.paste(im, (10, 4))
    ImageDraw.Draw(band).text((10, im.height + 8), os.path.relpath(preview, ROOT), fill=ink, font=small)
    parts.append(("Hotbar preview (art/tools/hotbar_preview.py, GUI scale 4, on light and dark)", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Awrata (gilthead sea bream) item icon, textures/item/awrata.png", fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    os.makedirs(os.path.dirname(OUT_SHEET), exist_ok=True)
    out.save(OUT_SHEET)


def main():
    check(AWRATA)
    icon = render(AWRATA)
    icon.save(OUT_ICON, optimize=False)
    subprocess.run([os.path.join(ART, ".venv", "bin", "python"), os.path.join(ART, "tools", "hotbar_preview.py"),
                    os.path.join(ART, "candidates", "fish_awrata_icon_hotbar.png")] + HOTBAR + ["--select", "6"],
                   check=True, capture_output=True)
    sheet(icon)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), "and", os.path.relpath(OUT_SHEET, ROOT))


if __name__ == "__main__":
    main()
