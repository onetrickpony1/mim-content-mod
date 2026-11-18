"""Item icon for the murina (Mediterranean moray, Muraena helena): the caught fish, like vanilla cod and salmon.

This icon sets the murina's look and palette; its bucket, spawn egg and model copy it.

What makes it a murina (photos in art/references/fish_murina_refonly/, list.tsv):
- a long, snake-like eel with no pectoral fins, the body tapering from a deep head to a thin tail;
- a continuous low fin along the back and round the tail, the same skin as the body (drawn as the lit back rim that
  runs unbroken from the head round the flattened tail tip);
- a dark violet-brown base, densely mottled with small cream-yellow spots (fewer on the head). Photos out of water
  (o01-o06, m10, m11: caught, stranded or on a market slab) show the true base is a mauve to violet-brown (hue about
  280-355), not the olive-brown seen through water; the sheet shows the sampled swatches;
- a big, broad head that stands out from a slightly narrower neck, with a long dark mouth line, a pointed snout and a
  small pale eye near the front. The tube nostrils are too small for 16 pixels.

Pose: vanilla has no eel. A gentle S along the diagonal, head lower left facing down-left, tail upper right, as our
other fish lie. Alternatives tried (shown on the compare sheet): an S with a flat bottom (read as a boot), a hooked
tail like a fish on the sand (read as a stick) and a loose curl (read as a rope or snake).

Light follows vanilla's fish items (measured with art/tools/measure.py, never copied): from the top left, so the back
carries a lit mid-tone rim and the belly side falls through a 5-tone ramp into a dark rim. The cream spots take the
light too: bright on the lit side, tan in the middle, dull mauve in the shade. The head carries none, so the pale eye
stays the only bright mark on it.

Run:  art/.venv/bin/python art/src/fish_murina_icon.py
Writes mod/.../textures/item/murina.png (byte-identical on rerun) and art/candidates/fish_murina_icon.png (compare
sheet, with an offline hotbar preview from art/tools/hotbar_preview.py).
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
OUT_ICON = os.path.join(TEXTURES, "item", "murina.png")
OUT_SHEET = os.path.join(ART, "candidates", "fish_murina_icon.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_murina_refonly")


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAL = {
    # body light ramp, lit back (top left) to shaded belly (bottom right): a violet-brown taken from photos out of
    # water (owner 2026-11-18: "it seems a bit more purple"), kept as light as round 2 so it holds on the dark slot
    "1": hx("#8c6a6a"), "2": hx("#765660"), "3": hx("#62464e"), "4": hx("#503a40"), "5": hx("#433036"),
    "k": hx("#705660"),                       # lit rim: the back and its low fin, the top of the head
    "o": hx("#2a1a1f"),                       # shaded rim: belly side, under the jaw
    "C": hx("#e2d09c"), "c": hx("#b49c84"), "d": hx("#806a6c"),  # cream mottle: in the light, mid, in the shade
    "E": hx("#f0e8bc"),                       # small pale eye, the only pale mark on the head
    "L": hx("#866670"), "l": hx("#5c4650"),   # upper lip at the snout tip, lower jaw
    "M": hx("#200f14"),                       # the mouth line
}

PAL_ROUND2 = {
    # round 2 (passed by the critic, sent back by the owner), kept only for the compare sheet.
    # body light ramp, lit back (top left) to shaded belly (bottom right): an olive-tinged dark chocolate brown,
    # kept apart from the ċerna's red-brown; lifted after the critic so the lower right holds on the dark slot
    "1": hx("#8c7058"), "2": hx("#765c48"), "3": hx("#624c3a"), "4": hx("#503e30"), "5": hx("#433428"),
    "k": hx("#66503e"),                       # lit rim: the back and its low fin, the top of the head
    "o": hx("#24190f"),                       # shaded rim: belly side, under the jaw
    "C": hx("#dcc68a"), "c": hx("#ab9460"), "d": hx("#7c6a48"),  # cream mottle: in the light, mid, in the shade
    "E": hx("#f0e8bc"),                       # small pale eye, the only pale mark on the head
    "L": hx("#7c624e"), "l": hx("#5e4a3a"),   # upper lip at the snout tip, lower jaw
    "M": hx("#24140f"), "W": hx("#8a7862"),   # the open mouth, and one tooth muted so it can't read as an eye
}

PAL_ROUND1 = {
    # body light ramp, lit back (top left) to shaded belly (bottom right): an olive-tinged dark chocolate brown,
    # kept apart from the ċerna's red-brown
    "1": hx("#806650"), "2": hx("#6a5240"), "3": hx("#564232"), "4": hx("#45352a"), "5": hx("#382b22"),
    "k": hx("#4f3c2e"),                       # lit rim: the back and its low fin, the top of the head
    "o": hx("#1c1510"),                       # shaded rim: belly side, under the jaw
    "C": hx("#dcc68a"), "c": hx("#ab9460"), "d": hx("#7c6a48"),  # cream mottle: in the light, mid, in the shade
    "E": hx("#f0e8bc"),                       # small pale eye
    "L": hx("#8e7460"), "l": hx("#5e4a3a"),   # upper lip at the snout tip, lower jaw
    "M": hx("#24140f"), "W": hx("#c8b896"),   # the open mouth, and one muted tooth in it
}

# Round 3 (owner): the head is its own shape, rows 9-15 at x 0-6: a crown at 2-4,9 above a notch (6,9-10) where the
# neck dips, a pointed snout at 0,12, the eye at 3,11, a dark mouth line along row 13 ending in a lip corner at 4,13,
# and the lower jaw under it. The neck behind it (6-8, rows 10-12) is narrower than the head.
# Round 1-2 notes: snout tip at 0,13 (upper lip L), the mouth open between it and the lower jaw (row 15, its corners rounded) with one muted tooth at 2,14; eye at
# 3,12. The head rises up-right into the neck, the body swings up in a gentle S (lower bend 9-14,8-10, upper bend
# 8-12,3-6) and the tail flattens to a rounded fin tip at 13-15,1-2. Round 2 (critic): a lighter ramp so the lower right holds on the dark slot, spots spread across the body instead of a chain, rounded muzzle and tail tip. Every outline steps by 1-3 pixels.
MURINA = [
    "................",
    ".............kk.",
    "...........kkc2o",
    ".........kk1C3o.",
    "........k1C3do..",
    "........kc244o..",
    "........k1c34o..",
    ".........k1Cdo..",
    ".........kc3c4o.",
    "..kkk...kk1cddo.",
    ".k1122kkk1C24o..",
    "k11E2232c3d4o...",
    "L1222334d45o....",
    ".MMMl34d5o......",
    ".ll345oo........",
    "..ooo...........",
]

# Round 2, passed by the critic and sent back by the owner ("you cannot clearly see that it has a head"), kept only
# for the compare sheet.
MURINA_ROUND2 = [
    "................",
    ".............kk.",
    "...........kkc2o",
    ".........kk1C3o.",
    "........k1C3do..",
    "........kc244o..",
    "........k1c34o..",
    ".........k1Cdo..",
    ".........kc3c4o.",
    "........kk1cddo.",
    ".....kkk1C244o..",
    "..kkk11C2d4o....",
    ".k1E2c3dc45o....",
    "L2223cd5ooo.....",
    "lMWM34ooo.......",
    ".oll............",
]

# Round 1, before the critic's fixes (contrast on the dark slot, spot chain, square muzzle and tail tip, tooth
# reading as an eye), kept only for the compare sheet.
MURINA_ROUND1 = [
    "................",
    ".............kko",
    "...........kkc2o",
    ".........kk1C3o.",
    "........kC23do..",
    "........k1c4o...",
    "........k12c4o..",
    ".........kC3do..",
    ".........k12c4o.",
    "........kkC23do.",
    ".....kkk112c4o..",
    "..kkk11C2d4o....",
    ".k1E2233c45o....",
    "L22233d5ooo.....",
    "lMWM34ooo.......",
    ".lllo...........",
]

# Poses tried and dropped, in the same palette, kept only for the compare sheet.
ALTERNATIVES = {
    "S, flat bottom (a boot)": [
        "................",
        "............kkko",
        "..........kk1co.",
        "........kkC23o..",
        ".......k12c4o...",
        ".......kC234o...",
        ".......k2c4do...",
        "........k1234o..",
        "........kC2c4o..",
        "...kkkkkk2c44o..",
        "..k112C2C33do...",
        ".k1E22223d5o....",
        "L22223c45oo.....",
        "lMWM3d4oo.......",
        ".lllooo.........",
        "................",
    ],
    "hooked tail (a stick)": [
        "............kk..",
        "...........k1Co.",
        "............k2o.",
        "............kco.",
        "...........k1co.",
        "..........k1C4o.",
        "........kk2c4o..",
        ".......k12C34o..",
        ".....kk12c34o...",
        "...kk11C234o....",
        "..k11c2234o.....",
        ".k1E2C3c4o......",
        "L2223445o.......",
        "lMWM45oo........",
        ".lllooo.........",
        "................",
    ],
    "loose curl (a rope)": [
        "................",
        "................",
        "................",
        "......kkkkk.....",
        ".....k1C2c4k....",
        "....k1co..k2o...",
        "....k2o....kCo..",
        "....kc4.....k3o.",
        ".....oo.....kc3o",
        "..k.........k23o",
        ".k1kk......k1C4o",
        "kE2C2kkkkkk12c4o",
        "L22233C22223c4o.",
        "lMWM444c44c44o..",
        ".lloooooooooo...",
        "................",
    ],
}


def render(rows, pal=None):
    pal = pal or PAL
    assert len(rows) == 16
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), pal[ch] + (255,))
    return im


def check(rows):
    """Warn about stray pixels (no opaque 4-neighbour) and spots too near the eye."""
    eye = [(x, y) for y, row in enumerate(rows) for x, ch in enumerate(row) if ch == "E"]
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            if not any(0 <= x + dx < 16 and 0 <= y + dy < 16 and rows[y + dy][x + dx] != "."
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                print(f"warning: stray pixel at {x},{y}")
            if ch in "Ccd" and any(abs(x - ex) <= 1 and abs(y - ey) <= 1 for ex, ey in eye):
                print(f"warning: spot at {x},{y} is next to the eye")


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


# Body boxes (x0, y0, x1, y1) on photos of the fish out of water, where water can't tint the colour.
SAMPLES = {
    "m11.jpg": ((250, 200, 600, 360), "stranded, Tunisia"),
    "m10.jpg": ((450, 250, 800, 330), "stranded, Tunisia"),
    "o01.jpg": ((230, 150, 460, 270), "fresh on shingle, Almeria"),
    "o02.jpg": ((150, 20, 330, 150), "fresh on shingle, Aegean"),
    "o03.jpg": ((210, 90, 400, 150), "in a rock pool, Crete"),
    "o04.jpg": ((240, 200, 272, 290), "live on rock, Gozo (wet, sunlit)"),
    "o05.jpg": ((45, 300, 95, 400), "market slab, Essaouira"),
}


def sample_photos():
    import numpy as np
    out = {}
    for name, (box, note) in SAMPLES.items():
        p = os.path.join(REFS, name)
        if not os.path.exists(p):
            continue
        a = np.array(Image.open(p).convert("RGB").crop(box)).reshape(-1, 3).astype(float)
        lum = a @ [0.2126, 0.7152, 0.0722]
        q = np.percentile(lum, [10, 45, 90, 98])
        cols = [tuple(int(v) for v in np.median(a[(lum > lo) & (lum < hi)], 0))
                for lo, hi in ((q[0], q[1]), (q[1], q[2]), (q[2], q[3]))]
        out[name] = (cols, note)
    return out


def tiles(band, im, x0, y0):
    """The icon at 8x, then 1x and 2x on light and dark grey."""
    tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
    tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
    band.paste(tile.convert("RGB"), (x0, y0))
    for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
        t = Image.new("RGBA", (16 * s + 8, 16 * s + 8), col + (255,))
        t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (x0 + 136 + (j % 2) * 44, y0 + (j // 2) * 46))


def sheet(icon):
    font, small = label_font(16), label_font(13)
    W = 1720
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    # references
    refs = []
    for name in ("o02.jpg", "o01.jpg", "m11.jpg", "o04.jpg", "o05.jpg"):
        p = os.path.join(REFS, name)
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im = im.resize((330, round(330 * im.height / im.width)), Image.LANCZOS)
            refs.append((name, im))
    if refs:
        h = max(im.height for _, im in refs) + 26
        band = Image.new("RGB", (W, h), bg)
        d = ImageDraw.Draw(band)
        for i, (name, im) in enumerate(refs):
            band.paste(im, (10 + i * 340, 22))
            d.text((10 + i * 340, 2), f"{name} (reference only)", fill=ink, font=small)
        parts.append(("References out of water (art/references/fish_murina_refonly, list.tsv; o04 is from Mgarr ix-Xini, Gozo)",
                      band))

    # colour from photos out of water: base (10-45th luminance percentile), mid (45-90th) and spots (90-98th)
    band = Image.new("RGB", (W, 34 * (len(SAMPLES) + 2) + 10), bg)
    d = ImageDraw.Draw(band)
    y = 6
    for name, (rgbs, note) in list(sample_photos().items()) + [
            ("round 2 palette", ([PAL_ROUND2[c] for c in "12345koCcd"], "olive-brown, as seen through water")),
            ("NEW palette", ([PAL[c] for c in "12345koCcd"], "violet-brown base, cream-yellow spots"))]:
        d.text((10, y + 8), name, fill=ink, font=small)
        for j, rgb in enumerate(rgbs):
            d.rectangle((200 + j * 74, y, 200 + j * 74 + 70, y + 28), fill=rgb)
            d.text((200 + j * 74 + 2, y + 30 - 14), "#%02x%02x%02x" % rgb, fill=(255, 255, 255) if sum(rgb) < 380
                   else (0, 0, 0), font=label_font(11))
        d.text((200 + 10 * 74 + 10, y + 8), note, fill=ink, font=small)
        y += 34
    parts.append(("Colour: photos out of water (base, mid, spots) beside the old and new palettes "
                  "(ramp 1-5, lit rim, shaded rim, spots)", band))

    # 8x and 1x beside vanilla and the accepted fish
    items = [("vanilla cod", os.path.join(VANILLA, "cod.png")),
             ("vanilla salmon", os.path.join(VANILLA, "salmon.png")),
             ("lampuka (accepted)", os.path.join(TEXTURES, "item", "lampuka.png")),
             ("tonn (accepted)", os.path.join(TEXTURES, "item", "tonn.png")),
             ("sardina (accepted)", os.path.join(TEXTURES, "item", "sardina.png")),
             ("cerna (being reworked)", os.path.join(TEXTURES, "item", "cerna.png")),
             ("MURINA", None)]
    band = Image.new("RGB", (W, 128 + 60), bg)
    d = ImageDraw.Draw(band)
    for i, (name, p) in enumerate(items):
        im = icon if p is None else Image.open(p).convert("RGBA")
        x0 = 10 + i * 244
        tiles(band, im, x0, 22)
        d.text((x0, 2), name, fill=ink, font=small)
    d.text((10, 160), "8x, then 1x and 2x on light and dark grey", fill=ink, font=small)
    parts.append(("The icon at 8x and 1x beside vanilla cod and salmon and our fish", band))

    # poses tried
    band = Image.new("RGB", (W, 128 + 34), bg)
    d = ImageDraw.Draw(band)
    for i, (name, rows, pal) in enumerate([("NEW: round 3 (head, colour)", MURINA, PAL), ("round 2 (critic passed)", MURINA_ROUND2, PAL_ROUND2),
                                       ("round 1", MURINA_ROUND1, PAL_ROUND1)]
                                      + [(k, v, PAL_ROUND1) for k, v in ALTERNATIVES.items()]):
        x0 = 10 + i * 244
        tiles(band, render(rows, pal), x0, 22)
        d.text((x0, 2), name, fill=ink, font=small)
    parts.append(("New beside rounds 2 and 1 (8x, 1x, 2x), then the poses tried in round 1", band))

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

    # offline hotbar preview (owner 2026-11-18: flat icons need no Minecraft run), at the GUI scale and at 4x
    py = os.path.join(ART, ".venv", "bin", "python")
    tool = os.path.join(ART, "tools", "hotbar_preview.py")
    hb = []
    for suffix, extra in (("", []), ("_x4", ["--scale", "4"])):
        out = os.path.join(ART, "candidates", f"fish_murina_icon_hotbar{suffix}.png")
        subprocess.run([py, tool, out, "mc:cod", "mc:salmon", "mod:cerna", "mod:awrata", "mod:murina", "--select", "4"]
                       + extra, check=True, capture_output=True)
        hb.append(Image.open(out).convert("RGB"))
    band = Image.new("RGB", (W, sum(im.height + 10 for im in hb) + 24), bg)
    y = 4
    for im in hb:
        band.paste(im, (10, y))
        y += im.height + 10
    ImageDraw.Draw(band).text((10, y), "art/tools/hotbar_preview.py: cod, salmon, cerna, awrata, MURINA (selected); "
                              "light and dark backdrops", fill=ink, font=small)
    parts.append(("Hotbar preview (offline, as the game draws flat items)", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Murina (Mediterranean moray) item icon, textures/item/murina.png", fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    os.makedirs(os.path.dirname(OUT_SHEET), exist_ok=True)
    out.save(OUT_SHEET)


def main():
    check(MURINA)
    icon = render(MURINA)
    icon.save(OUT_ICON, optimize=False)
    sheet(icon)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), "and", os.path.relpath(OUT_SHEET, ROOT))


if __name__ == "__main__":
    main()
