"""Ziemel tal-bahar (seahorse) spawn egg: the item icon (16 x 16), 2026-11-18, round 3 (a redesign).

The owner sent round 2 back: "seahorse egg is huge and doesnt read as an egg at all it looks like the whole
seahorse" (decision note "2026-11-18 Three eggs rejected - must be egg-shaped; cawl and shark buckets accepted").
Round 1 before it read as a Dalek or a bird. Round 3 starts from vanilla's EGG outline and paints the seahorse on it,
the vanilla 26.x way and the way our accepted lampuka, tonn, sardina, cerna, awrata and murina eggs do it.
Vanilla's eggs (art/.vanilla/item/*spawn_egg*.png) were measured, never copied.

The outline follows the vanilla cod egg's widths: 6-9, 5-10, 4-11, 4-11, 3-12, 2-12, 2-13, 1-14, 1-14, then the
pool (1-14, 2-13, 2-13, 3-12). Narrow on top, widest low down, taller than wide, the same size as the cod egg.

On it:
- a brown-ochre cap and body, lit top-left to shaded bottom-right in five tones, with a dark shaded rim;
- one black eye at (6,5), with only mid body tones round it: no gold, no light speck, no face;
- two pale bony rings on the lower egg (rows 9 and 11) as arcs on the lit front only (x 2-8), turning into the
  body's shade on the right, so they wrap round the egg and never make a band across it;
- two small signature parts poking out: the coronet as two knobs at the back of the crown ((8,2) and (10,3)) and a
  short straight tube snout at the front (row 6, x 1 to 3) with a flared tip at (1,5) and (1,6), never a hook. Three options were drawn (snout and coronet; coronet and curled
  tail; snout and tail): the snout and coronet one was picked, because the snout under the eye and the coronet on the
  crown together say "horse head", which is what makes a seahorse a seahorse at 1x, while a 3 px tail curl at the side
  reads as a jug handle. The other two stay on the sheet. The critic then sent A back for three fixes (a cone or
  beehive outline, a beak-like hooked snout, barrel bands; art/candidates/critic_ziemel_egg_r3/), made here.

Colour: the owner-accepted bucket's brown-ochre ramp (art/src/fish_ziemel_bucket.py "0" to "4", taken from the
accepted 3D model's texture, darker and redder so it is NOT yellow), one lighter cap highlight of the same hue, and
pale ring tones of the same hue (not yellow). The pool is our own ramp of seagrass-shade blues, not vanilla's
water-mob pool nor any of our other eggs' pools (checked on every run).

Photos (reference only): art/references/fish_ziemel_refonly/ (list.tsv).

Run:    art/.venv/bin/python art/src/fish_ziemel_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/ziemel_spawn_egg.png (byte-identical on rerun) and
        art/candidates/fish_ziemel_egg.png (compare sheet), with the offline hotbar previews
        art/candidates/fish_ziemel_egg_hotbar.png and fish_ziemel_egg_hotbar_x4.png (art/tools/hotbar_preview.py).
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
OUT_ICON = os.path.join(TEXTURES, "item", "ziemel_spawn_egg.png")
OUT_SHEET = os.path.join(ART, "candidates", "fish_ziemel_egg.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_ziemel_refonly")
OUT_HOTBAR = os.path.join(ART, "candidates", "fish_ziemel_egg_hotbar.png")
OUT_HOTBAR4 = os.path.join(ART, "candidates", "fish_ziemel_egg_hotbar_x4.png")
MODEL_SHOT = os.path.join(ROOT, ".art-runs", "ziemelmodel2", "build", "smoke-run", "screenshots",
                          "0072_fish-ziemel-side.png")
OUR_EGGS = ("lampuka", "tonn", "sardina", "cerna", "awrata", "murina")


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAL = {
    # the ziemel: the accepted bucket's ramp (art/src/fish_ziemel_bucket.py), shade to light
    "0": hx("#4c3320"), "1": hx("#62442a"), "2": hx("#7a5634"), "3": hx("#936a3e"), "4": hx("#a97c47"),
    "o": hx("#38251a"),  # shaded rim: the back and under the egg
    "5": hx("#b4864e"),  # the cap's highlight, top-left (same hue as the ramp, not yellow)
    "b": hx("#bc9a72"),  # the pale bony rings, lit (same hue, less saturated: not yellow)
    "c": hx("#a98a66"),  # the rings, half shade
    "d": hx("#8c6f52"),  # the rings, in shade
    "f": hx("#b09070"),  # round 1 only (sheet): its dorsal fin
    "E": hx("#0a0a0a"),  # the eye: the accepted buckets' eye black
    # the pool: our own ramp of seagrass-shade blues
    "p": hx("#1b3448"), "q": hx("#255a78"), "r": hx("#3478a0"), "s": hx("#52a0c4"), "w": hx("#a8dcec"),
}

# Round 3 (2026-11-18): vanilla's egg outline with the seahorse painted on. Option A, the one picked, as first
# drawn (sent back by the critic: too narrow low down, so a cone or beehive; a beak-like hook; barrel bands).
A_FIRST = [
    "................",
    "................",
    ".......4.3......",
    "......5443......",
    ".....554332.....",
    "....44E43321....",
    ".23345443221....",
    ".1.4544332210...",
    "...544433221o...",
    "..4bbbbcccdd1o..",
    "..44333322211o..",
    "..4bbbbccdd21o..",
    "..q4333222110s..",
    "..rqsoooooo0sp..",
    "..qrswsrrwsrqp..",
    "...pqqppqqppq...",
]


def variant(rows, pts):
    g = [list(r) for r in rows]
    for (x, y), c in pts.items():
        g[y][x] = c
    return ["".join(r) for r in g]


# Option A fixed after the critic's review (art/candidates/critic_ziemel_egg_r3/fixA.png):
# - the outline widened to the cod egg's widths low down: row 8 2-12, rows 10-11 1-14, with a dark rim at x 14,
#   and the pool rim widened to match on row 12;
# - the snout straight with a flared tip: no down-turned hook at (1,7) (it read as a beak, "kiwi-like bird");
# - the rings as arcs on the lit front only (pale at x 2-8), x 9-13 in the body's shade tones (full bands read
#   as a barrel);
# - the crown knobs moved back and down to (8,2) and (10,3), so the top no longer reads as a cone's point.
GRID = [
    "................",
    "................",
    "........4.......",
    "......54433.....",
    ".....554332.....",
    ".2..44E43321....",
    ".13345443221....",
    "...4544332210...",
    "..4544433221o...",
    "..4bbbbcc22110..",
    ".4443333222110o.",
    ".44bbbbcc22110o.",
    ".qq4333222110ss.",
    "..rqsoooooo0sp..",
    "..qrswsrrwsrqp..",
    "...pqqppqqppq...",
]

# the two options not picked (sheet only), drawn on A as first drawn
NO_SNOUT = {(1, 6): ".", (2, 6): ".", (3, 6): ".", (1, 7): "."}
TAIL = {(14, 9): "3", (15, 10): "2", (14, 11): "1", (15, 11): "0"}
OPTION_B = variant(A_FIRST, {**NO_SNOUT, **TAIL})  # coronet and curled tail
OPTION_C = variant(A_FIRST, {(7, 2): ".", (9, 2): ".", **TAIL})  # snout and curled tail

# round 2 (rejected by the owner: "looks like the whole seahorse", sheet only)
ROUND2_GRID = [
    "........4.3.....",
    ".......44321....",
    "......4433211...",
    ".....4E3322110..",
    "....433322211o..",
    "2..43333222110..",
    "2333333322210...",
    "2...4333221o....",
    ".....4b3321o....",
    "3b4.4bb43221o...",
    "4o3.44443221o...",
    "22..4bbb43221o..",
    "..2344444322o...",
    "...4oooooooooqs.",
    ".rqsswsrrwrsrsp.",
    "..qpqppqqppqqp..",
]

# round 1 (sent back by the critic, sheet only)
ROUND1_GRID = [
    "................",
    "........342.....",
    ".......43321....",
    "......4332211...",
    ".....43E2211o...",
    "....43332211o...",
    "0..4333222110o..",
    "0113333222110o..",
    "...1244322210o..",
    "...4bbb432211f..",
    "..444444322111f.",
    "..4bbbb432211f..",
    "...4444432210o..",
    "..b4oooooooooqs.",
    ".4p3swsrrwrsrsp.",
    "..32qppqqppqqp..",
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
    """Exact-pixel copy check against every vanilla spawn egg (as art/candidates/critic_sardina_egg_v5/check.py),
    and the pool colours against vanilla and our other eggs."""
    ours = {(x, y): icon.getpixel((x, y)) for x in range(16) for y in range(16) if icon.getpixel((x, y))[3] > 0}
    hits = []
    vcols = set()
    for f in sorted(glob.glob(os.path.join(VANILLA, "*spawn_egg*.png"))):
        v = Image.open(f).convert("RGBA")
        if v.size != (16, 16):
            continue
        same = [p for p, c in ours.items() if v.getpixel(p) == c]
        if same:
            hits.append((len(same), os.path.basename(f)))
        vcols |= {v.getpixel((x, y))[:3] for x in range(16) for y in range(16) if v.getpixel((x, y))[3] > 0}
    shared = {c[:3] for c in ours.values()} & vcols
    hits.sort(reverse=True)
    most = f"most: {hits[0][0]} in {hits[0][1]}" if hits else "none"
    pool = {PAL[k] for k in "pqrsw"}
    egg_cols = set()
    others = sorted(f for f in glob.glob(os.path.join(TEXTURES, "item", "*_spawn_egg.png"))
                    if os.path.basename(f) != "ziemel_spawn_egg.png")
    for f in others:
        e = Image.open(f).convert("RGBA")
        egg_cols |= {e.getpixel((x, y))[:3] for x in range(16) for y in range(16) if e.getpixel((x, y))[3] > 0}
    return [f"same pixel and colour as a vanilla spawn egg: {sum(n for n, _ in hits)} pixels over {len(hits)} eggs ({most})",
            f"our colours also used by any vanilla spawn egg: {len(shared)}",
            f"pool colours also used by vanilla eggs: {len(pool & vcols)}; by our other {len(others)} eggs: "
            f"{len(pool & egg_cols)}"]


def widths(im):
    """Per-row outline widths, 'first-last' of the opaque pixels."""
    out = []
    for y in range(16):
        xs = [x for x in range(16) if im.getpixel((x, y))[3] > 0]
        out.append(f"{min(xs)}-{max(xs)}" if xs else "")
    return out


def width_lines(icon):
    cod = Image.open(os.path.join(VANILLA, "cod_spawn_egg.png")).convert("RGBA")
    rows = [("vanilla cod", cod), ("round 2 (rejected)", render(ROUND2_GRID)), ("A first drawn", render(A_FIRST)),
            ("A FIXED (NEW)", icon)]
    rows += [(n, Image.open(os.path.join(TEXTURES, "item", n + "_spawn_egg.png")).convert("RGBA"))
             for n in ("sardina", "murina")]
    ws = [widths(im) for _, im in rows]
    return [["row"] + [n for n, _ in rows]] + [[str(y)] + [w[y] for w in ws] for y in range(16)]


def tile_row(d, band, x0, name, im, small, ink):
    tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
    tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
    band.paste(tile.convert("RGB"), (x0, 22))
    d.text((x0, 2), name, fill=ink, font=small)
    for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
        t = Image.new("RGBA", (40, 40), col + (255,))
        t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (x0 + (j % 2) * 44 + (j // 2) * 88, 156))


def sheet(icon):
    font, small = label_font(16), label_font(13)
    W = 2600
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    refs = []
    for name in ("g_1.jpg", "g_head.jpg", "h_main.jpg", "g_long.jpg", "h_gervais.jpg"):
        p = os.path.join(REFS, name)
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im = im.resize((round(260 * im.width / im.height), 260), Image.LANCZOS)
            refs.append((name, im))
    if refs:
        band = Image.new("RGB", (W, 260 + 26), bg)
        d = ImageDraw.Draw(band)
        x = 10
        for name, im in refs:
            band.paste(im, (x, 22))
            d.text((x, 2), f"{name} (reference only)", fill=ink, font=small)
            x += im.width + 12
        parts.append(("References (art/references/fish_ziemel_refonly, list.tsv): deep head, tube snout below the "
                      "eye, coronet, body rings, dorsal fin, curled tail", band))

    # the accepted model and bucket
    bucket = Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")
    bucket.alpha_composite(Image.open(os.path.join(TEXTURES, "item", "ziemel_bucket.png")).convert("RGBA"))
    band = Image.new("RGB", (W, 128 + 120), bg)
    d = ImageDraw.Draw(band)
    tile_row(d, band, 10, "accepted bucket", bucket, small, ink)
    tile_row(d, band, 224, "NEW ZIEMEL EGG", icon, small, ink)
    tex = Image.open(os.path.join(TEXTURES, "entity", "fish", "ziemel.png")).convert("RGBA")
    t = Image.new("RGBA", (tex.width * 6, tex.height * 6), (139, 139, 139, 255))
    t.alpha_composite(tex.resize((tex.width * 6, tex.height * 6), Image.NEAREST))
    band.paste(t.convert("RGB"), (440, 22))
    d.text((440, 2), "accepted model texture", fill=ink, font=small)
    if os.path.exists(MODEL_SHOT):
        shot = Image.open(MODEL_SHOT).convert("RGB").crop((340, 130, 510, 350)).resize((170, 220), Image.NEAREST)
        band.paste(shot, (720, 22))
        d.text((720, 2), "accepted model in game (earlier run)", fill=ink, font=small)
    parts.append(("The accepted bucket and 3D model the egg takes its colours from", band))

    items = [(f"vanilla {n.replace('_', ' ')} egg", os.path.join(VANILLA, n + "_spawn_egg.png"))
             for n in ("cod", "salmon", "tropical_fish", "pufferfish", "horse")]
    items += [(f"our {n} egg", os.path.join(TEXTURES, "item", n + "_spawn_egg.png")) for n in OUR_EGGS]
    items += [("NEW ZIEMEL EGG", icon)]
    band = Image.new("RGB", (W, 128 + 120), bg)
    d = ImageDraw.Draw(band)
    for i, (name, p) in enumerate(items):
        im = p if isinstance(p, Image.Image) else Image.open(p).convert("RGBA")
        tile_row(d, band, 10 + i * 214, name, im, small, ink)
    d.text((10, 202), "8x, then 1x and 2x on light grey, 1x and 2x on dark grey", fill=ink, font=small)
    parts.append(("The egg at 8x and 1x beside vanilla's fish eggs (and the horse egg) and our six accepted eggs", band))

    band = Image.new("RGB", (W, 128 + 120), bg)
    d = ImageDraw.Draw(band)
    tile_row(d, band, 10, "round 1 (sent back)", render(ROUND1_GRID), small, ink)
    tile_row(d, band, 224, "round 2 (REJECTED)", render(ROUND2_GRID), small, ink)
    tile_row(d, band, 438, "A as first drawn", render(A_FIRST), small, ink)
    tile_row(d, band, 652, "A FIXED (NEW)", icon, small, ink)
    tile_row(d, band, 866, "B: coronet + tail", render(OPTION_B), small, ink)
    tile_row(d, band, 1080, "C: snout + tail", render(OPTION_C), small, ink)
    notes = ["Round 3 starts from the vanilla cod egg's outline, row for row, standing in its own pool.",
             "The seahorse is painted on: brown-ochre cap and body, one black eye, two pale bony rings",
             "across the lower egg, and two small parts poking out.",
             "A (picked): coronet knobs on top and a short tube snout under the eye: together they say",
             "'horse head' at 1x. B and C swap one part for a 3 px curled tail at the back, which reads",
             "as a jug handle at 1x; C without the coronet reads as a teapot (spout and handle).",
             "A fixed (critic's review): cod's widths low down (row 8 2-12, rows 10-11 1-14), a straight",
             "snout with a flared tip (no beak hook), rings as arcs on the lit front only (no barrel bands),",
             "crown knobs moved to (8,2) and (10,3) so the top is not a cone's point."]
    for i, line in enumerate(notes):
        d.text((1300, 24 + 20 * i), line, fill=ink, font=small)
    parts.append(("Round 1, round 2 (rejected), round 3 option A as first drawn and fixed, options B and C "
                  "(8x, then 1x and 2x)", band))

    lines = width_lines(icon)
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, cells in enumerate(lines):
        for j, cell in enumerate(cells):
            d.text((10 + (0 if j == 0 else 50 + 190 * (j - 1)), 4 + 20 * i), cell, fill=ink, font=label_font(14))
    parts.append(("Outline widths per row (first-last opaque x) beside vanilla's cod egg", band))

    lines = measure([os.path.join(VANILLA, n + "_spawn_egg.png") for n in ("cod", "salmon", "tropical_fish", "pufferfish")]
                    + [os.path.join(TEXTURES, "item", n + "_spawn_egg.png") for n in OUR_EGGS] + [OUT_ICON])
    lines += copy_check(icon)
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("art/tools/measure.py and the copy check", band))

    py = os.path.join(ART, ".venv", "bin", "python")
    items = ["mc:cod_spawn_egg", "mc:chicken_spawn_egg", "mc:parrot_spawn_egg", "mod:sardina_spawn_egg",
             "mod:ziemel_spawn_egg", "mod:cerna_spawn_egg", "mod:awrata_spawn_egg", "mod:murina_spawn_egg",
             "mc:horse_spawn_egg"]
    for out, scale in ((OUT_HOTBAR, 2), (OUT_HOTBAR4, 4)):
        subprocess.run([py, os.path.join(ART, "tools", "hotbar_preview.py"), out] + items +
                       ["--select", "4", "--scale", str(scale)], check=True, capture_output=True)
    for out, scale in ((OUT_HOTBAR, 2), (OUT_HOTBAR4, 4)):
        im = Image.open(out).convert("RGB")
        band = Image.new("RGB", (max(W, im.width + 20), im.height + 30), bg)
        band.paste(im, (10, 4))
        ImageDraw.Draw(band).text((10, im.height + 8), os.path.relpath(out, ROOT) + f"  (GUI scale {scale}: vanilla cod, "
                                  "chicken and parrot eggs; our sardina egg; ZIEMEL EGG (selected); our cerna, awrata, "
                                  "murina eggs; vanilla horse egg)",
                                  fill=ink, font=small)
        parts.append((f"Hotbar preview (art/tools/hotbar_preview.py, GUI scale {scale})", band))

    W = max(W, max(b.width for _, b in parts))
    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Ziemel tal-bahar (seahorse) spawn egg, textures/item/ziemel_spawn_egg.png", fill=ink,
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
    icon = render(GRID)
    icon.save(OUT_ICON, optimize=False)
    print("wrote", OUT_ICON)
    sheet(icon)
