"""Item icon for the boll (common stingray, Dasyatis pastinaca): the caught fish, like vanilla cod. Round 5.

Round 5 starts again from the owner's angle picture, art/references/fish_boll_owner/angle_ref_1.png (the owner on
round 4: "it's not the angle i asked for at all"). That picture is used for its angle and composition only; no pixel of
it is used in the icon. The compare sheet shows it small and as a 16x16 downscale, for comparing the silhouette.

The angle, read from the owner's picture:
- seen from the front and a little above: the ray glides toward the viewer, turned slightly to the right, and its back
  (top surface) faces the viewer;
- the wings spread wide to both sides like a gliding bird seen head-on, so the shape is wide and short. The near wing
  reaches out to the far left, its tip curling up (0,7); the far wing rises to the top right, its tip curling up
  (14-15,3). Each wing has a dark outline and a lit leading edge L;
- the body is a broad rounded dome in the middle, with a soft light patch H where it catches the light (top left);
- the head is at the front, bottom centre: a rounded snout lobe (7-9,12-13);
- the tail rises behind the body at the top left. It is a common stingray's thin whip (2 px: lit side L, dark side o)
  with the spine S on it, never the cartoon's short spike.

Kept a common stingray, not the picture's cartoon manta: no cephalic horns, no eyes, no blush, no mouth line or smile
(an earlier test with two eyes read as "a cooking pot"). The back is a smooth plain olive-brown. The caught-fish photos
(art/references/fish_boll_refonly/ sr01, sr02, on a kitchen hob) sample a saturated olive-yellow (#84713b); a critic
found a khaki-yellow too yellow, so the palette keeps the hue and takes about half the saturation, leaning
olive-brown.

Candidates (all share the palette):
- A: the picture's proportions; the whip rises almost straight up from the top left of the back, as in the picture;
- B: the wings raised higher into a V (far tip at row 2), a smaller dome, and a long whip trailing up-left;
- C: A's body with B's long up-left whip.

Run:  art/.venv/bin/python art/src/fish_boll_icon_v5.py
Writes mod/.../textures/item/boll.png (the INSTALLED candidate, byte-identical on rerun),
art/candidates/fish_boll_icon_v5.png (compare sheet), art/candidates/fish_boll_icon_v5_<X>.png (each candidate, 16x16)
and the offline hotbar previews art/candidates/fish_boll_icon_v5_hotbar_<X>.png (the boll unselected, among vanilla
items, at GUI scale 1 and 2 over the light and dark backdrops) and fish_boll_icon_v5_hotbar_x4.png.
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
OUT_ICON = os.path.join(TEXTURES, "item", "boll.png")
CAND = os.path.join(ART, "candidates")
OUT_SHEET = os.path.join(CAND, "fish_boll_icon_v5.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_boll_refonly")
OWNER_REF = os.path.join(ART, "references", "fish_boll_owner", "angle_ref_1.png")

INSTALLED = "C"  # owner 2026-11-18: "lets go with candidate C"


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAL = {
    "o": hx("#1e1a10"),                       # thick dark outline, all round
    "L": hx("#b2a580"),                       # lit leading edges of the wings, lit side of the whip
    "H": hx("#a39570"),                       # the soft light patch on the dome
    "1": hx("#8a7d5c"), "2": hx("#706549"),   # olive-brown back: lit, mid
    "3": hx("#574e39"), "4": hx("#433c2d"),   # shade toward the lower right, the crease where the far wing meets the dome
    "S": hx("#c4b794"),                       # the tail spine, on the whip
}

# A and C share the body (rows 5-13); only the whip differs.
BODY = [
    ".....oLooo..oL2o",
    ".....o111oooL12o",
    "oo..o1HH1123L12o",
    "oLoo1HHH1123122o",
    "oL1111H1122323o.",
    ".ooLL11112223o..",
    "...ooL112233o...",
    ".....ooL23oo....",
    ".......ooo......",
    "................",
    "................",
]

CANDIDATES = {
    "A": [
        "................",
        "................",
        ".....oo.........",
        "....oLo.......oo",
        "....SLo......oLo",
    ] + BODY,
    "B": [
        "................",
        "................",
        "..oo..........oo",
        "..oLo........oLo",
        "...SLo......oL2o",
        "....oLooo..oL12o",
        "....o1H11ooL122o",
        "o..o1HH1123122o.",
        "oooo1HHH11232o..",
        "oLL11HH11223o...",
        ".ooLL11123o.....",
        "...ooL1223o.....",
        ".....ooL3o......",
        ".......oo.......",
        "................",
        "................",
    ],
    "C": [
        "................",
        "..oo............",
        "..oLo...........",
        "...SLo........oo",
        "....oLo......oLo",
    ] + BODY,
}

# Round 2, candidate A2 (critic: FAIL on A, it read as a teapot or gravy boat at 1x: the stubby near wing the spout,
# the curled far wing the handle, the whip the lid knob; a grey smudge on the dark slot). Fixes, all in A2:
# - the near wing is as big as the far wing: it sweeps out from the body at (4,8)-(4,10) to a tip at (0,7), curling up
#   to (0,6)-(1,6), and (1-3,8-10) is filled with body tones so it reads as a broad flap, not a spout;
# - the photos' olive at near-full saturation (sr01/sr02 samples #6a5728 #84713b #a08752), with 12 tones;
# - the dome centre is the brightest point (W at 6,7 7,7 6,8), stepping down toward (10,10); the wing interiors are a
#   step darker than the dome;
# - the outline is soft (o) on the lit top and left edges and hard (O) only on the bottom and right;
# - the whip is a 1 px tapering line from the back (6,5) up to (5,3) and a dark tip at (4,2), with no pale speck;
# - the pale underside P shows at the curled wing tips (14,4) and (1,8); the snout is one rounded point (8,13).
PAL_A2 = {
    "O": hx("#1e1a10"),                       # hard outline, bottom and right edges
    "o": hx("#3d3218"),                       # soft outline, lit top and left edges
    "W": hx("#b8a064"),                       # dome light, the brightest point
    "h": hx("#ac9459"),                       # lit leading edges, the dome around the light
    "1": hx("#a08752"), "m": hx("#957d45"),
    "2": hx("#8a7438"), "n": hx("#7a6530"),
    "3": hx("#6a5728"),                       # also the whip
    "4": hx("#554620"),
    "5": hx("#43381a"),                       # shadow, the whip's tip
    "P": hx("#d6caa0"),                       # pale underside at the curled wing tips
}

CANDIDATES["A2"] = [
    "................",
    "................",
    "....5...........",
    ".....3........oO",
    ".....3.......oPO",
    ".....o3ooo..oh3O",
    "oo...o1h1ooohm3O",
    "ohooo1WWh1m32m3O",
    "oPmm1hWh1m23234O",
    "Oh2221h1m2n334O.",
    ".Ohhm1mm2n345O..",
    "..OOOh1m2n34O...",
    ".....OOO2OOO....",
    "........O.......",
    "................",
    "................",
]

PALS = {"A2": PAL_A2}

NOTES = {
    "A2": "A2: round 2 on A: broad near wing, saturated olive, bright dome centre, soft lit outline, 1 px whip",
    "A": "A: the picture's proportions, whip rising straight up at the top left",
    "B": "B: wings raised into a V, smaller dome, long whip up-left",
    "C": "C: A's body, long whip trailing up-left",
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


def check(name, rows):
    """Warn about stray pixels (no opaque 8-neighbour) and flat outline runs longer than 3 px."""
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            if not any(0 <= x + dx < 16 and 0 <= y + dy < 16 and rows[y + dy][x + dx] != "."
                       for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy):
                print(f"warning: {name}: stray pixel at {x},{y}")
        for run in row.replace(".", " ").split():
            if len(run) >= 4 and set(run) == {"o"}:
                print(f"warning: {name}: flat outline run of {len(run)} in row {y}")
    return sum(1 for r in rows for c in r if c != ".") / 256


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


def owner_ref_16():
    """The owner's picture cropped to the ray (its dark outline's box) and box-downscaled to 16x16: comparison only."""
    import numpy as np
    im = Image.open(OWNER_REF).convert("RGB")
    a = np.array(im).astype(int)
    ys, xs = np.where(a.sum(2) < 150)
    crop = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    s = max(crop.size)
    sq = Image.new("RGB", (s, s), (160, 210, 230))
    sq.paste(crop, ((s - crop.size[0]) // 2, (s - crop.size[1]) // 2))
    return sq.resize((16, 16), Image.BOX)


def sample_photos():
    import numpy as np
    out = {}
    for name, box in (("sr01.jpg", (250, 250, 700, 550)), ("sr02.jpg", (100, 150, 850, 600))):
        p = os.path.join(REFS, name)
        if not os.path.exists(p):
            continue
        a = np.array(Image.open(p).convert("RGB").crop(box)).reshape(-1, 3).astype(float)
        lum = a @ [0.2126, 0.7152, 0.0722]
        q = np.percentile(lum, [5, 35, 65, 95])
        out[name] = [tuple(int(v) for v in np.median(a[(lum >= lo) & (lum <= hi)], 0))
                     for lo, hi in ((q[0], q[1]), (q[1], q[2]), (q[2], q[3]))]
    return out


def tiles(band, im, x0, y0):
    """The icon at 8x, then 1x and 2x on light grey and on the dark slot grey #2b2b2b."""
    tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
    tile.alpha_composite(im.convert("RGBA").resize((128, 128), Image.NEAREST))
    band.paste(tile.convert("RGB"), (x0, y0))
    for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((43, 43, 43), 1), ((43, 43, 43), 2))):
        t = Image.new("RGBA", (16 * s + 8, 16 * s + 8), col + (255,))
        t.alpha_composite(im.convert("RGBA").resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (x0 + 136 + (j % 2) * 44, y0 + (j // 2) * 46))


ACCEPTED = ("cerna", "huta_kahla", "tonn", "lampuka", "awrata", "murina", "cawl")
VAN_FISH = ("cod", "salmon")


def text_band(lines, W, bg, ink):
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    return band


def hotbars(icons):
    """Offline hotbar previews, the boll unselected among vanilla items, at GUI scale 1 and 2 (light and dark)."""
    py = os.path.join(ART, ".venv", "bin", "python")
    tool = os.path.join(ART, "tools", "hotbar_preview.py")
    out = {}
    for name in icons:
        items = ["mc:cod", "mc:apple", "mc:bread", f"file:{os.path.join(CAND, f'fish_boll_icon_v5_{name}.png')}",
                 "mc:salmon", "mc:carrot", "mc:pufferfish", "mc:cooked_beef", "mc:tropical_fish"]
        ims = []
        for scale in (1, 2):
            tmp = os.path.join(CAND, f"fish_boll_icon_v5_hotbar_{name}_s{scale}.png")
            subprocess.run([py, tool, tmp] + items + ["--scale", str(scale)], check=True, capture_output=True)
            ims.append(Image.open(tmp).convert("RGB"))
            os.remove(tmp)
        w = max(im.width for im in ims) + 16
        both = Image.new("RGB", (w, sum(im.height for im in ims) + 24), (139, 139, 139))
        y = 8
        for im in ims:
            both.paste(im, (8, y))
            y += im.height + 8
        path = os.path.join(CAND, f"fish_boll_icon_v5_hotbar_{name}.png")
        both.save(path)
        out[name] = both
    x4 = os.path.join(CAND, "fish_boll_icon_v5_hotbar_x4.png")
    subprocess.run([py, tool, x4, "mc:cod", "mod:cerna"]
                   + [f"file:{os.path.join(CAND, f'fish_boll_icon_v5_{n}.png')}" for n in icons]
                   + ["mc:salmon", "mod:tonn", "mc:pufferfish", "--scale", "4"], check=True, capture_output=True)
    out["x4"] = Image.open(x4).convert("RGB")
    return out


def sheet(icons):
    font, small = label_font(16), label_font(13)
    W = 2000
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    # the owner's picture, small, and its 16x16 downscale (comparison only), beside each candidate at 8x
    own = Image.open(OWNER_REF).convert("RGB")
    own.thumbnail((300, 250), Image.LANCZOS)
    ref16 = owner_ref_16()
    band = Image.new("RGB", (W, 290), bg)
    d = ImageDraw.Draw(band)
    band.paste(own, (10, 26))
    d.text((10, 4), "owner's picture (angle only)", fill=ink, font=small)
    band.paste(ref16.resize((128, 128), Image.NEAREST), (330, 26))
    d.text((330, 4), "its 16x16 downscale, comparison only", fill=ink, font=small)
    for i, (name, im) in enumerate(icons.items()):
        x0 = 560 + i * 160
        t = Image.new("RGBA", (128, 128), (160, 210, 230, 255))
        t.alpha_composite(im.resize((128, 128), Image.NEAREST))
        band.paste(t.convert("RGB"), (x0, 26))
        d.text((x0, 4), f"candidate {name}" + (" (installed)" if name == INSTALLED else ""), fill=ink, font=small)
    for i, name in enumerate(icons):
        d.text((560, 166 + i * 20), NOTES[name], fill=ink, font=small)
    parts.append(("The angle: the owner's picture beside the candidates (same backdrop colour)", band))

    # colour: photo samples beside the palette
    samples = sample_photos()
    band = Image.new("RGB", (W, 34 * (len(samples) + 1) + 10), bg)
    d = ImageDraw.Draw(band)
    y = 6
    for name, rgbs in list(samples.items()) + [("PALETTE", [PAL[c] for c in "LH1234oS"]), ("PALETTE A2", [PAL_A2[c] for c in "Wh1m2n345oOP"])]:
        d.text((10, y + 8), name, fill=ink, font=small)
        for j, rgb in enumerate(rgbs):
            d.rectangle((200 + j * 74, y, 200 + j * 74 + 70, y + 28), fill=rgb)
            d.text((200 + j * 74 + 2, y + 16), "#%02x%02x%02x" % rgb,
                   fill=(255, 255, 255) if sum(rgb) < 380 else (0, 0, 0), font=label_font(11))
        y += 34
    d.text((900, 14), "photos: caught rays out of water (dark, mid, light); palette L H 1 2 3 4 o S: the photos' hue "
                      "at about half the saturation", fill=ink, font=small)
    parts.append(("Colour: sr01 and sr02 samples beside the palette", band))

    # each candidate at 8x, 1x, 2x beside vanilla and the accepted fish
    items = [(f"candidate {n}", im) for n, im in icons.items()]
    items += [(f"vanilla {n}", Image.open(os.path.join(VANILLA, f"{n}.png")).convert("RGBA")) for n in VAN_FISH]
    items += [(f"{n} (accepted)", Image.open(os.path.join(TEXTURES, "item", f"{n}.png")).convert("RGBA"))
              for n in ACCEPTED]
    per_row = 8
    rows_n = (len(items) + per_row - 1) // per_row
    band = Image.new("RGB", (W, rows_n * 170 + 24), bg)
    d = ImageDraw.Draw(band)
    for i, (name, im) in enumerate(items):
        x0, y0 = 10 + (i % per_row) * 244, 22 + (i // per_row) * 170
        tiles(band, im, x0, y0)
        d.text((x0, y0 - 20), name, fill=ink, font=small)
    d.text((10, rows_n * 170), "8x, then 1x and 2x on light grey and on the slot's dark grey #2b2b2b", fill=ink,
           font=small)
    parts.append(("The candidates at 8x, 1x and 2x beside vanilla cod and salmon and the accepted fish", band))

    # numbers
    lines = measure([os.path.join(CAND, f"fish_boll_icon_v5_{n}.png") for n in icons]
                    + [os.path.join(TEXTURES, "item", f"{n}.png") for n in ACCEPTED]
                    + [os.path.join(VANILLA, f"{n}.png") for n in VAN_FISH])
    lines.append("accepted fish coverage 0.26-0.43; STYLE.md food ranges: colours 6-20, dark 0.0-0.35, "
                 "light 0.32-0.99, TL-BR +0.01-+0.17")
    parts.append(("art/tools/measure.py", text_band(lines, W, bg, ink)))

    # hotbars
    hb = hotbars(icons)
    ims = [hb[n] for n in icons] + [hb["x4"]]
    band = Image.new("RGB", (W, max(sum(im.height + 10 for im in ims[:-1]), 1) + ims[-1].height + 40), bg)
    y = 4
    for n, im in zip(list(icons) + ["x4"], ims):
        band.paste(im, (10, y))
        ImageDraw.Draw(band).text((im.width + 20, y + 4), f"candidate {n}" if n != "x4" else
                                  "scale 4: cod, cerna, " + ", ".join(icons) + ", salmon, tonn, pufferfish", fill=ink,
                                  font=small)
        y += im.height + 10
    parts.append(("Hotbar preview (offline, as the game draws flat items): the boll unselected in slot 4 among cod, "
                  "apple, bread, salmon, carrot, pufferfish, steak, tropical fish; GUI scale 1 then 2", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Boll (common stingray) item icon, round 5: the owner's angle, textures/item/boll.png", fill=ink,
           font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    out.save(OUT_SHEET)


def main():
    os.makedirs(CAND, exist_ok=True)
    icons = {}
    for name, rows in CANDIDATES.items():
        cov = check(name, rows)
        print(f"{name}: coverage {cov:.2f}")
        icons[name] = render(rows, PALS.get(name))
        icons[name].save(os.path.join(CAND, f"fish_boll_icon_v5_{name}.png"), optimize=False)
    icons[INSTALLED].save(OUT_ICON, optimize=False)
    sheet(icons)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), f"(candidate {INSTALLED}) and", os.path.relpath(OUT_SHEET, ROOT))


if __name__ == "__main__":
    main()
