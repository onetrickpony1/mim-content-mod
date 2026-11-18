"""Skorfna (scorpionfish) spawn egg: the item icon (16 x 16), 2026-11-18.

Started by the owner's rule (docs/Decisions/2026-11-18 Skorfna bucket accepted.md: "skorfna approved", the bucket D2;
approving a piece starts the next). One egg for both colours, black and red (they are reskins of one mob,
docs/Decisions/2026-11-18 Skorfna - two versions, red and black, as reskins.md), so the egg is the black skorfna,
the default: the mottled brown "this colour".

The owner's egg rules, all kept here:
- vanilla's egg outline (docs/Decisions/2026-11-18 Three eggs rejected - must be egg-shaped; cawl and shark buckets
  accepted.md), measured from vanilla 26.x's fish eggs (cod, salmon, pufferfish in art/.vanilla/item, never copied):
  a 4 px top on row 3 widening to 12 px on rows 8-12, its bottom edge on row 13 (x 5-10), and on rows 10-12 the
  one-pixel side flaps at x 1 and 14 that vanilla's fish eggs carry there; nothing else breaks the outline but the
  dorsal spines on top;
- a stylised egg, not the whole fish squeezed in (docs/Decisions/2026-11-18 Sardina egg - a representation, not a
  fat fish.md), in the owner's preferred style from the boll (docs/Decisions/2026-11-18 Boll egg B; egg pools match
  vanilla.md): a plain egg in the animal's palette carrying only its key features. For the skorfna those are
  - the spiny dorsal fin with dark tips: a comb of dark spines D joined by the pale membrane r, standing on the
    egg's top, the spine tips S one pixel proud of it (the way vanilla's pufferfish egg puts its spikes round the
    top of its outline);
  - the mottled brown camouflage: the egg lit from the top left (C 1 2 3 4), with dark saddles in 4 and red-brown
    patches R, never two dark marks level with each other (no pair of eye-like dots), and the pale belly 0 J on the
    lower front, where vanilla's cod egg has its pale patch;
  - the side flaps as the big fan pectorals in fin browns F f D;
  - in C only, the pale skin-flap tassels (the photos' cirri) on those flaps, in the icon's pale 0 and C.
- no eye, no face, no pair of level dots.
- vanilla's own pool (art/src/egg_pool.py, the owner's exception to "never copy", for the pool only): P in the grids.

Colours: only the accepted icon D's (art/src/fish_skorfna_icon.py PAL, the approved model's black palette before
its water lift; the bucket D2, art/src/fish_skorfna_bucket.py, uses the very same keys), plus vanilla's pool. The
outline o is the icon's own (its B, the darkest brown). Nothing new. The red skin is not used: a red patch on a
brown egg read as a second, red fish, and the owner asked for one egg, not two.

Candidates (the sheet shows all of them; PICK is written to the mod):
- A, tall front spine: the dorsal comb steps down from front (left) to back: the first spine two pixels over the
  egg's top (6,1), the second one (8,2), the last on the shoulder (10,3), membrane r between them.
- B, low comb: three spine tips level on row 2 (6, 8, 10) over a band of dark spines and pale membrane that is the
  egg's own top edge (row 3), so the outline stays a rounded egg top.
- C, B with tassels: the pectoral flaps carry the pale skin tassels (1,10 pale 0, 1,11 C on the front; 14,10 C on
  the back), as the bucket's pale chin flaps.

- D, wide comb: four level spine tips (5, 7, 9, 11 on row 2) over a 7 px band of spines and membrane; critic round 1
  PASS with fixes (the back spine hung past the shoulder over nothing, the flat 7 px top read as a crown).
- D2, the PICK: D with both critics' fixes (see its grid): the back spine drops onto the shoulder, the front corner
  is membrane; critic round 2: PASS after its one fix.
The tassels (C) read at 1x as stray light pixels on the flaps (critic round 1), so the pick has none.

Blind reads (fresh readers, no context, the egg alone in a hotbar of vanilla eggs at GUI scale 2 and/or 4):
- round 1, A B C (darker body; the readers could not tell them apart): "A spawn egg, brown with darker brown
  blotches and a pointed top. I can't tell which creature it is for." / "A spawn egg in mottled brown and tan,
  probably for a scorpionfish" / "Most likely a bucket holding a creature, but I can't tell which creature."
- round 2, D2: "It looks like a creature item, most likely a spawn egg or a mob-in-water item ... My best guess is
  a mottled bottom fish such as a scorpionfish" / "A spawn egg, probably for some brown sea creature, but I can't
  tell which one." / "Probably a spawn egg (or an egg-type creature item). I can't name the creature with
  confidence; my best guess is something brown and lumpy, like an octopus or a scorpionfish."

Run:    art/.venv/bin/python art/src/fish_skorfna_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/skorfna_spawn_egg.png (the PICK, byte-identical on
        rerun), art/candidates/fish_skorfna_egg.png (the compare sheet: the candidates at 8x, 1x and 2x beside
        vanilla's fish and squid eggs and our accepted boll, cerna, lampuka and jellyfish eggs) and the offline hotbar
        previews art/candidates/fish_skorfna_egg_hotbar.png and fish_skorfna_egg_hotbar_x4.png
        (art/tools/hotbar_preview.py, GUI scale 2 and 4, nothing selected).
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
from fish_skorfna_icon import PAL as ICON  # noqa: E402  (accepted icon D, the bucket's keys too)
from egg_pool import POOL as VANILLA_POOL, is_pool, pool_line  # noqa: E402

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
ITEMS = os.path.join(TEXTURES, "item")
OUT_ICON = os.path.join(ITEMS, "skorfna_spawn_egg.png")
CAND = os.path.join(ART, "candidates")
OUT_SHEET = os.path.join(CAND, "fish_skorfna_egg.png")
OUT_HOTBAR = os.path.join(CAND, "fish_skorfna_egg_hotbar.png")
OUT_HOTBAR4 = os.path.join(CAND, "fish_skorfna_egg_hotbar_x4.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")

# the icon's keys: body ramp C (lit) 1 2 3 4 5 (shade), red-brown R, pale belly 0 J, fins S (spine tips) D (spines,
# flap shade) F f (membrane, flaps) r (pale membrane); the outline o is the icon's darkest brown B
PAL = {k: ICON[k] for k in "C012345RJSDFfr"}
PAL["o"] = ICON["B"]

POOL = [
    "..PPPooooooPPP..",
    "..PPPPPPPPPPPP..",
    "...PPPPPPPPPP...",
]

# the egg below its top edge (rows 4-12): lit at the upper left, saddles 4 at (9,5-7) and (5-6,8-9), never level,
# red-brown R patches between them, the pale belly 0 J at the lower front, the side flaps on rows 10-12
BODY = [
    ".....oCC12o.....",
    "....oCC1142o....",
    "....oC1RR42o....",
    "...oCC111442o...",
    "..oCC441112R3o..",
    "..o0C14R21123o..",
    ".Fo000J1R1123of.",
    ".Fo0000J1R234oD.",
    ".DoJ000J12334oD.",
]

CANDIDATES = {
    "A": [
        "................",
        "......S.........",
        "......DrS.......",
        "......DrDrS.....",
    ] + [BODY[0][:10] + "D" + BODY[0][11:]] + BODY[1:] + POOL,
    "B": [
        "................",
        "................",
        "......S.S.S.....",
        "......DrDrD.....",
    ] + BODY + POOL,
    "C": [
        "................",
        "................",
        "......S.S.S.....",
        "......DrDrD.....",
    ] + BODY[:6] + [".0o000J1R1123oC.", ".Co0000J1R234oD."] + BODY[8:] + POOL,
    "D": [
        "................",
        "................",
        ".....S.S.S.S....",
        ".....DrDrDrD....",
    ] + BODY + POOL,
    # D2, the pick: critic round 1's fixes for D (PASS with fixes): the back spine no longer hangs past the shoulder
    # (11,2 cleared; its tip S at 11,3 and its shaft D at 11,4 rest on the egg), so the comb slopes down to the tail;
    # the front corner (5,3) is membrane r, rounding the top-left back to an egg shoulder under the front tip.
    # Critic round 2: PASS with one fix, applied: (11,4) is the shaded membrane f, not D, so x 11 is no 4 px straight
    # dark wall and the back spine is a dark tip over membrane like the front one.
    "D2": [
        "................",
        "................",
        ".....S.S.S......",
        ".....rrDrDrS....",
        ".....oCC12of....",
    ] + BODY[1:] + POOL,
}
# vanilla's egg outline: (x from, x to) per row; the side flaps at x 1 and 14 on rows 10-12 are part of it
EGG = {3: (6, 9), 4: (5, 10), 5: (4, 11), 6: (4, 11), 7: (3, 12), 8: (2, 13), 9: (2, 13), 10: (1, 14), 11: (1, 14),
       12: (1, 14), 13: (2, 13), 14: (2, 13), 15: (3, 12)}
# the only pixels allowed outside it: the dorsal comb on top
FIN = {"A": {(6, 1), (6, 2), (7, 2), (8, 2), (10, 3)}, "B": {(6, 2), (8, 2), (10, 2), (10, 3)}}
FIN["C"] = FIN["B"]
FIN["D"] = {(5, 2), (7, 2), (9, 2), (11, 2), (5, 3), (10, 3), (11, 3)}
FIN["D2"] = {(5, 2), (7, 2), (9, 2), (5, 3), (10, 3), (11, 3), (11, 4)}
PICK = "D2"


def check_outline(name, rows):
    """The egg outline is filled, and nothing but the dorsal comb lies outside it."""
    for y, row in enumerate(rows):
        lo, hi = EGG.get(y, (99, -1))
        for x, ch in enumerate(row):
            inside = lo <= x <= hi
            if (x, y) in FIN[name]:
                assert ch != "." and not inside, f"{name}: fin pixel ({x},{y})"
            else:
                assert (ch != ".") == inside, f"{name}: pixel ({x},{y}) breaks the egg outline"


def check_marks(name, rows):
    """No two dark marks (4, D or S inside the body, rows 4-12, x 3-12) level with each other and 2-4 px apart
    with lighter body between: a pair like that reads as eyes."""
    for y in range(4, 13):
        dark = [x for x in range(3, 13) if rows[y][x] in "4DS" and x not in EGG.get(y, (0, 0))]
        for a in dark:
            for b in dark:
                if 2 <= b - a <= 4 and all(rows[y][x] not in "4DS" for x in range(a + 1, b)):
                    raise AssertionError(f"{name}: dark marks at ({a},{y}) and ({b},{y}) read as a pair of eyes")


def render(rows):
    assert len(rows) == 16
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch == "P":
                im.putpixel((x, y), VANILLA_POOL[(x, y)] + (255,))
            elif ch != ".":
                im.putpixel((x, y), PAL[ch] + (255,))
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
    """Exact-pixel copy check against every vanilla spawn egg (as the other fish egg scripts). Vanilla's own pool
    pixels are allowed (the owner's exception, art/src/egg_pool.py); any other copied pixel fails the run."""
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


def tmp_paths(icons):
    return {n: os.path.join(CAND, f"fish_skorfna_egg_{n}.tmp.png") for n in icons}


def hotbars(icons):
    """Offline hotbar previews, nothing selected: vanilla cod, pufferfish, tropical fish eggs, the candidates, our
    boll and cerna eggs, the accepted skorfna icon."""
    py = os.path.join(ART, ".venv", "bin", "python")
    tmp = tmp_paths(icons)
    for n, im in icons.items():
        im.save(tmp[n])
    items = (["mc:cod_spawn_egg", "mc:pufferfish_spawn_egg", "mc:tropical_fish_spawn_egg"] +
             [f"file:{tmp[n]}" for n in icons] + ["mod:boll_spawn_egg", "mod:cerna_spawn_egg", "mod:skorfna"])
    try:
        for out, scale in ((OUT_HOTBAR, 2), (OUT_HOTBAR4, 4)):
            subprocess.run([py, os.path.join(ART, "tools", "hotbar_preview.py"), out] + items[:9] +
                           ["--scale", str(scale)], check=True, capture_output=True)
    finally:
        for p in tmp.values():
            os.remove(p)


def sheet(icons):
    font, small = label_font(16), label_font(13)
    W = 2400
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    def van(n):
        return Image.open(os.path.join(VANILLA, n + ".png")).convert("RGBA")

    def ours(n):
        return Image.open(os.path.join(ITEMS, n + ".png")).convert("RGBA")

    bucket = van("cod_bucket")
    bucket.alpha_composite(ours("skorfna_bucket"))
    items = ([(f"CANDIDATE {n}{' (PICK)' if n == PICK else ''}", im) for n, im in icons.items()] +
             [("vanilla cod egg", van("cod_spawn_egg")), ("vanilla salmon egg", van("salmon_spawn_egg")),
              ("vanilla pufferfish egg", van("pufferfish_spawn_egg")),
              ("vanilla tropical fish egg", van("tropical_fish_spawn_egg")), ("vanilla squid egg", van("squid_spawn_egg")),
              ("our boll egg", ours("boll_spawn_egg")), ("our cerna egg", ours("cerna_spawn_egg")),
              ("our lampuka egg", ours("lampuka_spawn_egg")), ("our mauve stinger egg", ours("mauve_stinger_spawn_egg")),
              ("our fried-egg jelly egg", ours("fried_egg_jellyfish_spawn_egg")),
              ("our man o' war egg", ours("man_o_war_spawn_egg")),
              ("skorfna icon D (accepted)", ours("skorfna")), ("skorfna bucket D2 (accepted)", bucket)])
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
        parts.append(("The candidates at 8x, 1x and 2x beside vanilla's fish and squid eggs, our accepted boll, cerna, "
                      "lampuka and jellyfish eggs, the accepted skorfna icon and bucket" if start == 0
                      else "(continued)", band))

    tmp = tmp_paths(icons)
    for n, im in icons.items():
        im.save(tmp[n])
    lines = measure([os.path.join(VANILLA, n + "_spawn_egg.png") for n in ("cod", "salmon", "pufferfish")]
                    + [os.path.join(ITEMS, n + "_spawn_egg.png") for n in ("boll", "cerna")] + list(tmp.values()))
    for p in tmp.values():
        os.remove(p)
    lines += [copy_check(n, im)[0] for n, im in icons.items()]
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("art/tools/measure.py and the copy check", band))

    for out, scale in ((OUT_HOTBAR, 2), (OUT_HOTBAR4, 4)):
        im = Image.open(out).convert("RGB")
        band = Image.new("RGB", (W, im.height + 30), bg)
        band.paste(im, (10, 4))
        ImageDraw.Draw(band).text((10, im.height + 8), os.path.relpath(out, ROOT) + f"  (GUI scale {scale}, nothing "
                                  "selected: vanilla cod, pufferfish, tropical fish eggs; CANDIDATES " +
                                  ", ".join(icons) + "; our boll and cerna eggs; skorfna icon)", fill=ink, font=small)
        parts.append((f"Hotbar preview (art/tools/hotbar_preview.py, GUI scale {scale})", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Skorfna (scorpionfish) spawn egg: textures/item/skorfna_spawn_egg.png, one egg for both colours",
           fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    out.save(OUT_SHEET)
    print("wrote", os.path.relpath(OUT_SHEET, ROOT))


if __name__ == "__main__":
    for n, g in CANDIDATES.items():
        check_outline(n, g)
        check_marks(n, g)
    icons = {n: render(g) for n, g in CANDIDATES.items()}
    for n, im in icons.items():
        line, n_same = copy_check(n, im)
        assert n_same == 0, line
    icons[PICK].save(OUT_ICON, optimize=False)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), f"(candidate {PICK})")
    os.makedirs(CAND, exist_ok=True)
    hotbars(icons)
    sheet(icons)
