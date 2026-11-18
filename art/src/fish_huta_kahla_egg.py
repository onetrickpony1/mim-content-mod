"""Huta kahla (blue shark, Prionace glauca) spawn egg: the item icon (16 x 16), round 2, 2026-11-18.

The pool (owner 2026-11-18, "the pool under the egg should be the same as vanilla"; docs/Decisions/2026-11-18 Boll
egg B; egg pools match vanilla.md): the pool drawn in the grid below is our old one. vanilla_pool() swaps it for
vanilla's own pool (art/src/egg_pool.py, the owner's exception to "never copy", for the pool only) before the egg
is written, keeping every body pixel; what is said below about our own pool is its history.

Round 1 (option A) was rejected by the owner: "the egg doesnt really say shark, just blue blob and yeah it does look
like an ear" (decision "2026-11-18 Blue shark egg - reads as a blue blob, fin like an ear"). Its fin had an upright
leading edge and a bulging back. This round draws the shark's cues fresh, on vanilla's EGG outline, measured from
cod_spawn_egg (never copied), row for row from row 3 to the pool: 6-9, 5-10, 4-11, 4-11, 3-12, 2-13, 2-13, 1-14 x3,
then the pool 2-13, 2-13, 3-12. Head to the left, lit from the top left, one eye, no face.

Options (all on the sheet, each given to a fresh viewer for a blind read at 1x, 2x and 8x):
- A  the rejected round 1, for comparison only;
- B  the "Jaws" dorsal: a solid dark triangle on the crown. Its leading edge rises from the lit dome in a straight
     diagonal, its trailing edge drops straight and sweeps back into a free rear tip, with a notch under it (the
     concave back of a shark's fin). Lit leading edge, indigo body, darkest trailing edge, so it shows on light and
     dark backdrops. The dome under it is lit blue, so the dark fin stands out.
- C  no fin at all: shark markings painted on, three dark gill slits behind the eye, a sharp countershading line
     whose white belly rises toward the snout.
- D  B's dorsal plus a long dark swept-back pectoral blade painted low across the white belly.
- E  (round 2 pick, critic FIX: the fin read as a cat's ear, no dome) the fin set further back on the right shoulder, standing clear of the dome, with the white belly drawn as a
     long wedge rising to a pointed snout (inside the outline, below the eye's row, so it is no beak).
Round 2 blind read: both viewers called B, D and E a shark first; E drew the fewest other readings
(no tuna, swordfish or whale), and its fin stands clear of the dome. A read as a whale, C as a blob.
- E3 the critic's fix exactly (fin tops at row 1): a fresh viewer alone read it as "Whale".
- E4 (round 2b; critic FIX: "a blue fish or dolphin leaping", E4b "a pair of pointed ears"): the dome back at 6-9, a taller fin rising clear of it with a straight leading edge and a free
     rear tip over a gap, gill slits at x7 and x9 (rows 8-9), mid tone M under the dome, the dark wall stepped. A fresh
     viewer alone, at 1x and 2x beside cod, dolphin and pufferfish: "Shark". E4b (no gill slits) also read "Shark".
- F1 (the critic's, E4 with the dome top a step darker), F3 (F1 with a one-point fin and the belly stopped short of
     the rim) and F3n (CHOSEN, F3 without gill slits): each, alone, read "Shark" first, with no ear or second eye.
No pale point in front of the head, no rounded lobe on top, no dolphin beak.

Colours: the shark's are the EXACT palette of the accepted item icon (PAL in art/src/fish_huta_kahla_icon.py,
textures/item/huta_kahla.png); the pool is our own ramp of blues, not vanilla's shared water-mob pool.
Photos (reference only): art/references/fish_huta_kahla_refonly/ (list.tsv).

Run:    art/.venv/bin/python art/src/fish_huta_kahla_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/huta_kahla_spawn_egg.png (byte-identical on rerun),
        art/candidates/fish_huta_kahla_egg.png (compare sheet) and the offline hotbar previews
        art/candidates/fish_huta_kahla_egg_hotbar.png, _hotbar_x4.png and _hotbar_2.png.
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
from egg_pool import POOL_COLOURS, is_pool, pool_line, vanilla_pool  # noqa: E402

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
OUT_ICON = os.path.join(TEXTURES, "item", "huta_kahla_spawn_egg.png")
OUT_SHEET = os.path.join(ART, "candidates", "fish_huta_kahla_egg.png")
OUT_OPTS = os.path.join(ART, "candidates", "fish_huta_kahla_egg_options")
OUT_HOTBAR = os.path.join(ART, "candidates", "fish_huta_kahla_egg_hotbar.png")
OUT_HOTBAR4 = os.path.join(ART, "candidates", "fish_huta_kahla_egg_hotbar_x4.png")
OUT_HOTBAR2 = os.path.join(ART, "candidates", "fish_huta_kahla_egg_hotbar_2.png")
OUT_HOTBAR_OPTS = os.path.join(ART, "candidates", "fish_huta_kahla_egg_hotbar_options_x4.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_huta_kahla_refonly")
PY = os.path.join(ART, ".venv", "bin", "python")


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAL = {
    # the shark: the accepted item icon's colours, exactly
    "D": hx("#7a90dc"),  # lit rim, the dorsal's leading edge
    "T": hx("#6e84d4"),  # lit rim, a step down
    "3": hx("#4a66c0"),  # bright blue side
    "d": hx("#4a5cb4"),  # where the side turns into the back
    "1": hx("#303a86"),  # indigo back, the dorsal's body
    "p": hx("#262e74"),  # darkest indigo: the shaded right rim, the dorsal's trailing edge and tip
    "5": hx("#e8ecf6"),  # white belly
    "6": hx("#a8b0cc"),  # belly turning away
    "g": hx("#6e76a0"),  # belly in shade
    "G": hx("#464e7c"),  # deepest belly shade
    "e": hx("#0a0a16"),  # the eye
    "P": hx("#4a5eb6"),  # pectoral blade
    "k": hx("#323c8c"),  # pectoral trailing edge, gill slits (option C)
    # added in round 2b: the one tone not in the icon's palette, a mid step between T #6e84d4 and 3 #4a66c0. The
    # critic flagged ~25 px of flat 3 under the dome; T there merges with the lit rim and 3 is the flat fill itself.
    "M": hx("#5e78cc"),
    # the old pool (now swapped for vanilla's): our own ramp of blues
    "u": hx("#1f3a68"),
    "v": hx("#2a5890"),
    "w": hx("#3576b0"),
    "x": hx("#5398cc"),
    "y": hx("#86d0f0"),
}
# Our own old pool's colours: vanilla_pool() takes them out and puts vanilla's pool in (owner 2026-11-18,
# "the pool under the egg should be the same as vanilla"; art/src/egg_pool.py).
OLD_POOL = {PAL[k] for k in "uvwxy"}

POOL = [
    "..vxyxwyxwwyxv..",
    "...uuvuuuvuuu...",
]

# A, round 1 (rejected 2026-11-18): the fin off the right shoulder, upright leading edge, read as an ear
ROUND1_A = [
    "................",
    "............p...",
    "...........Dp...",
    "......TDd1.Ddp..",
    ".....TDd111Dp...",
    "....TDd1111p....",
    "....T3dd111p....",
    "...T3e3d1111p...",
    "..T33333d111pp..",
    "..6333333d111p..",
    ".556333333d111p.",
    ".5555633333d11p.",
    ".g5555663dd11pp.",
    "..vwg6gGG1ppwv..",
] + POOL

# B and D: the Jaws dorsal on the crown. Apex (10-11,0), leading edge D down the diagonal 9,1 8,2 7,3 into the lit
# dome, trailing edge p straight down x11 then swept back to the free rear tip at 12,3; the notch at 11-12,4 under
# the tip is the fin's concave back. The dome under it (row 4) is lit blue, so the dark fin stands clear of it.
DORSAL_CROWN = [
    "..........pp....",
    ".........D1p....",
    "........D11p....",
    "......TD111pp...",
    ".....TD33dd.....",
]
# the body below a crown dorsal: the light falls on the upper left, indigo only toward the back rim
BODY = [
    "....TD3333dd....",
    "....T33333d1....",
    "...T3e3333d1p...",
    "..T333333dd11p..",
    "..6333333dd11p..",
    ".55633333d1111p.",
    ".555563333d11pp.",
    ".g5555566Gd11pp.",
    "..vwg66GGG1pwv..",
]
# D: a long swept-back pectoral blade from under the gill (5-7,10) back and down to its tip (10,12)
BELLY_PECTORAL = [
    "..63333P3dd11p..",
    ".5563PPkd31111p.",
    ".555556Pkk3d1pp.",
    ".g555556Gkp11pp.",
    "..vwg66GGG1pwv..",
]
# C: no fin; three gill slits (k, two pixels tall) behind the eye and below its row, a sharp countershading line
MARKINGS = [
    "................",
    "................",
    "................",
    "......TDd1......",
    ".....TD3dd1.....",
    "....TD333dd1....",
    "....T33333d1....",
    "...T3e33333d1...",
    "..T3333k3k3k1p..",
    "..55333k3k3k1p..",
    ".55556333333d1p.",
    ".g555555663dd1p.",
    ".gG5555556Gd11p.",
    "..vwg66GGG1pwv..",
] + POOL
# E: the fin set back on the right shoulder, clear of the dome, and the white belly as a long wedge rising forward
SHOULDER_WEDGE = [
    "...........p....",
    "..........D1....",
    ".........D11p...",
    "........D111pp..",
    ".....TD3dd11....",
    "....TD3333d1....",
    "....T33333d1....",
    "...T3e3333d11...",
    "..T3333333dd1p..",
    "..55633333d11p..",
    ".555556333d111p.",
    ".g555555663d1pp.",
    ".gG555556Gd11pp.",
    "..vwg66GGG1pwv..",
] + POOL

# E fixed (round 2b, the critic's FIX on E: "a single pointed ear, almost cat-like, at 1x", "fish or whale sprites
# more than spawn eggs"). The dome is back (row 3 = 6-9, lit 6-8), the fin rises clear of it from the dome's right
# side with a straight diagonal leading edge (11,0 10,1 9,2 into the lit dome), a trailing edge straight down x11 and a
# free rear tip at 12,3 with nothing under it (11-12,4 empty), so the back is concave. Mid tone M under the dome,
# d dithered at x9-10, the dark wall stepped out to x12 on rows 8-9, two gill slits (1, x7 and x9, rows 8-9, never in
# the eye's row 7), (1,10) belly-shade so the chin is not a dolphin's.
FIN_E4 = [
    "...........p....",
    "..........Dp....",
    ".........D1p....",
    "......DDDd11p...",
]
BODY_E4 = [
    ".....TMMMd1.....",
    "....TDMMM3d1....",
    "....T3MMM3d1....",
    "...T3e333dd1p...",
    "..T3333131dd1p..",
    "..55633131dd1p..",
    ".655556333d111p.",
    ".g555555663d1pp.",
    ".gG555556Gd11pp.",
    "..vwg66GGG1pwv..",
]
# the critic's fix exactly as specified: the fin only up to row 1 (blind read: "Whale... a small tail flick")
FIN_E3 = [
    "................",
    "...........p....",
    "..........D1....",
    "......DDDdD1p...",
]
# E4 without the gill slits, the belly line slanting as in E
BODY_E4B = BODY_E4[:4] + [
    "..T33333d3dd1p..",
    "..55633333dd1p..",
] + BODY_E4[6:]

# Round 3 (critic FIX on E4: "a blue fish or dolphin leaping", E4b "a pair of pointed ears").
# F1, the critic's: E4 with the dome's top row 6-8 a step darker (T), so the dome and the fin's leading edge part.
FIN_F1 = FIN_E4[:3] + ["......TTTd11p..."]
# F3, ours from the critic's idea: F1 with the free rear tip at 12,3 gone, so the fin is ONE point with a straight
# back dropping into the body (nothing under 11,3); and the white belly stopped short of the left edge, so the rim is
# blue all round (2,9 and x1 rows 10-12 become rim tones T, 3, d). F3n is F3 without the gill slits (the critic's
# reader saw them as "a small dark speck ... nostril or second eye at 2x"); it is the pick.
FIN_F3 = FIN_E4[:3] + ["......TTTd1p...."]
BELLY_F3 = [
    "..35633131dd1p..",
    ".T55556333d111p.",
    ".3555555663d1pp.",
    ".dG555556Gd11pp.",
    "..vwg66GGG1pwv..",
]
BODY_F3 = BODY_E4[:4] + ["..T3333131dd1p.."] + BELLY_F3
BODY_F3N = BODY_E4[:4] + ["..T33333d3dd1p..", "..356333d3dd1p.."] + BELLY_F3[1:]

OPTIONS = {
    "A": ROUND1_A,
    "B": DORSAL_CROWN + BODY + POOL,
    "C": MARKINGS,
    "D": DORSAL_CROWN + BODY[:4] + BELLY_PECTORAL + POOL,
    "E": SHOULDER_WEDGE,
    "E3": FIN_E3 + BODY_E4 + POOL,
    "E4": FIN_E4 + BODY_E4 + POOL,
    "E4b": FIN_E4 + BODY_E4B + POOL,
    "F1": FIN_F1 + BODY_E4 + POOL,
    "F3": FIN_F3 + BODY_F3 + POOL,
    "F3n": FIN_F3 + BODY_F3N + POOL,
}
CHOSEN = "F3n"
NOTES = {
    "A": "A: ROUND 1, REJECTED\n(blue blob, fin like an ear)",
    "B": "B: Jaws dorsal on the crown,\nstraight leading edge,\nswept-back rear tip",
    "C": "C: no fin; gill slits and\na sharp countershading\nline painted on",
    "D": "D: B's dorsal plus a long\ndark swept-back pectoral\nblade across the belly",
    "E": "E: round 2 pick, critic FIX:\nfin like a cat's ear, no dome,\nreads as whale or dolphin",
    "E3": "E3: the critic's fix exactly;\nfin tops at row 1\nblind read: whale",
    "E4": "E4: dome back, taller fin,\ngills; critic FIX: dolphin\nleaping, ears (E4b)",
    "F1": "F1 (critic's): E4, dome top\na step darker\nblind read: shark",
    "F3": "F3: F1, one-point fin (no\nrear tip), blue rim all round\nblind read: shark",
    "F3n": "F3n: F3 without the gill\nslits; blind read: shark",
    "E4b": "E4b: E4 without the gill\nslits; blind read: shark",
}
# two fresh viewers' blind reads, word for word (eggs shown unlabelled, shuffled: 1 D, 2 A, 3 E, 4 C, 5 B).
# B, D and E were each read as a shark first by both; E drew the fewest other readings (no tuna, swordfish or whale).
BLIND_READ = {
    "A (egg 2)": ["v1: \"whale (a humpback or sperm whale type)... a little spout or fin sticking up at the back\"",
                  "v2: \"whale or dolphin. The thing on top is split or forked and looks like a blowhole spout or a "
                  "tail fluke, not a fin\""],
    "B (egg 5)": ["v1: \"a shark... Enlarged, it looks like a shark, or possibly a dolphin\"",
                  "v2: \"a shark again... the slanted fin could also suggest a swordfish or a tuna\""],
    "C (egg 4)": ["v1: \"a rounded blue blob, perhaps a whale or a seal, or even a blue slime or helmet\"",
                  "v2: \"a rounded blue blob, maybe a whale or a seal... could also pass for a blue slime\""],
    "D (egg 1)": ["v1: \"a shark (or whale)... could also be a dolphin or orca, or a generic blue fish or whale\"",
                  "v2: \"a shark, or maybe a dolphin... could be mistaken for the vanilla dolphin egg or a tuna\""],
    "E3 alone": ["v3: \"Whale. The egg is a round, dark-blue body with a pale belly, a small tail flick at the right and a "
                 "bulky, heavy shape, which reads as a cartoon whale rather than a slim fish\""],
    "E4 alone": ["v4: \"Shark. It's a blue-grey body with a pale belly, and there's a tall pointed dorsal fin on top that "
                 "makes a shark shape... you could easily mistake it for a dolphin, or for a blue fish like a tuna\""],
    "E4b alone": ["v5: \"Shark. The egg shows a dark blue fish shape with a white belly, a pointed snout and a triangular "
                  "fin on its back... It could also be taken for a dolphin or a tuna\""],
    "F1 alone": ["v6: \"Shark. It has a dark blue back, a white belly and a tall pointed fin rising from the top, which "
                 "together read as a shark seen side-on... nothing that looks like an ear, a second eye or a nostril\""],
    "F3 alone": ["v7: \"Shark. The dark blue back, the white belly and the pointed fin sticking out at the upper right "
                 "make it look like a leaping shark or big sea fish... nothing that looks like an ear, a second eye or a "
                 "nostril\""],
    "F3n alone": ["v8: \"Shark. The egg is dark blue with a pale white underside, and a pointed dorsal-fin tip stands "
                  "up from the top... Nothing clearly looks like an ear or a nostril... I see no second eye\""],
    "E (egg 3)": ["v1: \"a shark, because of the tall pointed dorsal fin and the white belly... could be a dolphin "
                  "or an orca\"",
                  "v2: \"a shark... still looks like a shark with a slightly thinner, more hooked fin\""],
}


def render(rows):
    assert len(rows) == 16
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), PAL[ch] + (255,))
    return im


def widths(im):
    out = []
    for y in range(16):
        xs = [x for x in range(16) if im.getpixel((x, y))[3] > 0]
        out.append(f"{xs[0]}-{xs[-1]}" if xs else "-")
    return out


def measure(paths):
    res = subprocess.run([PY, os.path.join(ART, "tools", "measure.py")] + paths, capture_output=True, text=True)
    lines = []
    for line in res.stdout.splitlines():
        if line.startswith("{"):
            d = eval(line, {"np": __import__("numpy")})  # measure.py prints dicts with numpy floats
            lines.append(f"{d['file']:<26} cover {d['coverage']:.2f}  colours {d['colours']:>2}  dark {d['lmin']:.2f}  "
                         f"light {d['lmax']:.2f}  edge {d['edge_l']:.2f}  inside {d['interior_l']:.2f}  "
                         f"TL-BR {d['tl_minus_br']:+.2f}")
    return lines


def copy_check(icon):
    """Exact-pixel copy check against every vanilla spawn egg (as art/candidates/critic_sardina_egg_v5/check.py).
    Vanilla's own pool pixels are allowed (the owner's exception, art/src/egg_pool.py); any other copied pixel
    fails the run."""
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
    shared = sorted(({c[:3] for c in ours.values()} - POOL_COLOURS) & vcols)
    assert not hits, f"copies vanilla pixels besides the pool: {hits}"
    hits.sort(reverse=True)
    most = f", most {hits[0][0]} in {hits[0][1]}" if hits else ""
    return (f"copied pixels besides vanilla's pool {sum(n for n, _ in hits)} over {len(hits)} vanilla eggs{most}; "
            f"colours shared with vanilla eggs (besides the pool) {len(shared)}; " + pool_line(icon))


HOTBAR_OPTS = ("A", "E4", "F1", "F3", "F3n")


def hotbar(paths):
    tool = os.path.join(ART, "tools", "hotbar_preview.py")
    items = ["mc:cod_spawn_egg", "mc:dolphin_spawn_egg", "mc:pufferfish_spawn_egg", "mod:huta_kahla_spawn_egg",
             "mod:lampuka_spawn_egg", "mod:tonn_spawn_egg", "mod:sardina_spawn_egg", "mod:cerna_spawn_egg",
             "mod:awrata_spawn_egg"]
    subprocess.run([PY, tool, OUT_HOTBAR] + items + ["--select", "3"], check=True, capture_output=True)
    subprocess.run([PY, tool, OUT_HOTBAR4] + items + ["--select", "3", "--scale", "4"], check=True,
                   capture_output=True)
    items2 = ["mc:cod_spawn_egg", "mod:murina_spawn_egg", "mod:huta_kahla_spawn_egg", "mod:huta_kahla",
              "bucket:huta_kahla_bucket"]
    subprocess.run([PY, tool, OUT_HOTBAR2] + items2 + ["--select", "2", "--scale", "2"], check=True,
                   capture_output=True)
    items3 = ["mc:cod_spawn_egg", "mc:dolphin_spawn_egg", "mc:pufferfish_spawn_egg"] + [f"file:{p}" for p in paths
                                                                               if os.path.basename(p)[:-4] in HOTBAR_OPTS]
    subprocess.run([PY, tool, OUT_HOTBAR_OPTS] + items3 + ["--select", "3", "--scale", "4"], check=True,
                   capture_output=True)


def tile_row(band, im, x0, y0):
    """8x on light grey, then 1x and 2x on light and dark grey."""
    t = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
    t.alpha_composite(im.resize((128, 128), Image.NEAREST))
    band.paste(t.convert("RGB"), (x0, y0))
    for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
        t = Image.new("RGBA", (40, 40), col + (255,))
        t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (x0 + j * 44, y0 + 134))


def sheet(icon, options):
    font, small = label_font(16), label_font(13)
    W = 1340
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    refs = []
    for name in ("bs01.jpg", "bs03.jpg", "bs07.jpg", "bs05.jpg"):
        p = os.path.join(REFS, name)
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im = im.resize((320, round(320 * im.height / im.width)), Image.LANCZOS)
            refs.append((name, im))
    if refs:
        h = min(260, max(im.height for _, im in refs)) + 26
        band = Image.new("RGB", (W, h), bg)
        d = ImageDraw.Draw(band)
        for i, (name, im) in enumerate(refs):
            band.paste(im.crop((0, 0, im.width, min(im.height, 260))), (10 + i * 330, 22))
            d.text((10 + i * 330, 2), f"{name} (reference only)", fill=ink, font=small)
        parts.append(("References (art/references/fish_huta_kahla_refonly, list.tsv)", band))

    order = ["A", "E4", CHOSEN, "F1", "F3", "E", "E3", "E4b", "B", "C", "D"]
    band = Image.new("RGB", (W, 236 * 3), bg)
    d = ImageDraw.Draw(band)
    for i, k in enumerate(order):
        x0, y0 = 10 + (i % 5) * 262, (i // 5) * 236
        tile_row(band, options[k], x0, y0 + 60)
        d.multiline_text((x0, y0 + 2), NOTES[k] + ("   << CHOSEN" if k == CHOSEN else ""), fill=ink, font=small)
    parts.append(("The rejected round 1 and the new options (8x; under each: 1x, 2x on light grey, 1x, 2x on dark)",
                  band))

    if BLIND_READ:
        lines = [f"{k}  {q}" for k, qs in BLIND_READ.items() for q in qs]
        band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
        d = ImageDraw.Draw(band)
        for i, line in enumerate(lines):
            d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
        parts.append(("Blind reads by fresh viewers with no context, beside vanilla's cod, dolphin and pufferfish eggs "
                      "(v1-v2 all options at 1x, 2x, 8x; v3-v8 one egg alone at 1x, 2x), word for word", band))

    items = [("vanilla cod egg", os.path.join(VANILLA, "cod_spawn_egg.png")),
             ("vanilla dolphin egg", os.path.join(VANILLA, "dolphin_spawn_egg.png")),
             ("vanilla pufferfish egg", os.path.join(VANILLA, "pufferfish_spawn_egg.png")),
             (f"HUTA KAHLA EGG ({CHOSEN})", None),
             ("huta kahla item icon", os.path.join(TEXTURES, "item", "huta_kahla.png"))]
    items += [(f"{n} egg (accepted)", os.path.join(TEXTURES, "item", f"{n}_spawn_egg.png"))
              for n in ("lampuka", "tonn", "sardina", "cerna", "awrata", "murina")]
    per = 6
    for start in range(0, len(items), per):
        band = Image.new("RGB", (W, 200), bg)
        d = ImageDraw.Draw(band)
        for i, (name, p) in enumerate(items[start:start + per]):
            im = icon if p is None else Image.open(p).convert("RGBA")
            x0 = 10 + i * 220
            tile_row(band, im, x0, 22)
            d.text((x0, 2), name, fill=ink, font=small)
        parts.append(("Beside vanilla's fish eggs and our accepted eggs" if start == 0 else "", band))

    cod = Image.open(os.path.join(VANILLA, "cod_spawn_egg.png")).convert("RGBA")
    lines = ["row:      " + " ".join(f"{y:>5}" for y in range(16)),
             "cod egg:  " + " ".join(f"{w:>5}" for w in widths(cod))]
    lines += [f"{k}:        " + " ".join(f"{w:>5}" for w in widths(im)) for k, im in options.items()]
    lines += measure([os.path.join(VANILLA, n + "_spawn_egg.png") for n in ("cod", "dolphin", "pufferfish")]
                     + [os.path.join(TEXTURES, "item", n + "_spawn_egg.png") for n in ("tonn", "cerna")] + [OUT_ICON])
    lines += [f"copy check {k}: " + copy_check(im) for k, im in options.items()]
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("Outline widths per row (first-last opaque x), art/tools/measure.py and the copy check", band))

    for path, title in ((OUT_HOTBAR_OPTS, "Hotbar preview x4: cod, dolphin, pufferfish, then options "
                                          + ", ".join(HOTBAR_OPTS)),
                        (OUT_HOTBAR4, f"Hotbar preview x4 (cod, dolphin, pufferfish, HUTA KAHLA {CHOSEN}, lampuka, "
                                      "tonn, sardina, cerna, awrata)"),
                        (OUT_HOTBAR, "Hotbar preview at GUI scale (same order)"),
                        (OUT_HOTBAR2, "Hotbar preview x2 (cod egg, murina egg, HUTA KAHLA egg, its icon, its bucket)")):
        im = Image.open(path).convert("RGB")
        if im.width > W - 20:
            im = im.resize((W - 20, round(im.height * (W - 20) / im.width)), Image.NEAREST)
        band = Image.new("RGB", (W, im.height + 8), bg)
        band.paste(im, (10, 4))
        parts.append((title, band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Huta kahla (blue shark) spawn egg, round 2, textures/item/huta_kahla_spawn_egg.png", fill=ink,
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
    options = {k: vanilla_pool(render(v), OLD_POOL) for k, v in OPTIONS.items()}
    icon = options[CHOSEN]
    icon.save(OUT_ICON, optimize=False)
    print("wrote", OUT_ICON)
    os.makedirs(OUT_OPTS, exist_ok=True)
    paths = []
    for k, im in options.items():
        p = os.path.join(OUT_OPTS, f"{k}.png")
        im.save(p, optimize=False)
        paths.append(p)
    hotbar(paths)
    sheet(icon, options)
