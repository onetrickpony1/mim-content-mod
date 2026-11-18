"""Pixxispad spawn egg: the item icon (16 x 16), round 6 of 2026-11-18: a new shape, with the sword as the key.

The pool (owner 2026-11-18, "the pool under the egg should be the same as vanilla"; docs/Decisions/2026-11-18 Boll
egg B; egg pools match vanilla.md): the pool drawn in the grid below is our old one. vanilla_pool() swaps it for
vanilla's own pool (art/src/egg_pool.py, the owner's exception to "never copy", for the pool only) before the egg
is written, keeping every body pixel; what is said below about our own pool is its history.

The owner: "develop a different shape for this one, can be less egg-y. the sword is critical to seeing it as a
swordfish" (docs/Decisions/2026-11-18 Swordfish egg - a different shape, the sword is critical.md). This egg alone may
leave vanilla's egg outline; it must still read as a spawn egg (a stylised egg-like body in its own pool), not as a
whole fish.

What failed before (all owner or blind-read verdicts, kept on the sheet):
- round 1, a whole fish: "a kiwi bird";
- the ball: "looks like a pufferfish since its ball shaped";
- layout D, an egg with a short level sword at eye height: "kind of looks like a bird now";
- round 5 B, the sword painted on the egg: nobody saw it ("grey cone", "shark fin", the blade read as stripes).

So every option here has a LONG, thin, straight sword (5-7 px) standing clear of the body, pale tan (the icon's S) and
darker toward the tip (s), with a dark edge on its underside (u at the root, the darkest part, then the rim o) so it
shows on both the light and the dark hotbar backdrop. The eye always sits below and behind the sword's root, never
above it as a bird's eye sits over its beak. A solid sickle dorsal fin (lit leading edge D, membrane d) stands on the
back; a thin one read as an ear on the blue shark egg.
- A: a long egg tilted head-up, like a torpedo-shaped egg, with the sword running up-left out of its narrow end.
- B: an upright egg leaning forward, the sword angled steeply up-left out of its top, like the fish leaping; the eye
  low and back.
- C: an upright egg in the lower right of the slot, with the sword running at 45 degrees from the top-left corner
  down to its front, as the sword runs on the accepted icon.
- D: a long egg lying level in its pool, with a level sword the length of the egg's front half running out of the
  upper front, and the eye low and back on the side.
Painted on every option, the vanilla 26.x way: a purple-bronze cap lit toward the upper left and darkest on the back,
bronze-silver and silver sides, a pale belly toward the front, shade toward the lower right, one black eye, the egg in
its own pool. Edges step in 1-3 px runs.
Colours: exactly the owner-accepted pixxispad item icon's (art/src/fish_pixxispad_icon.py PAL, same keys, nothing
new), plus the pool, our own ramp of deep open-sea indigo blues (shared with no vanilla egg).
The option written to the mod (CHOSEN) was picked by blind reads; see BLIND_READ.
Photos (reference only): art/references/fish_pixxispad_refonly/ (list.tsv).

Run:    art/.venv/bin/python art/src/fish_pixxispad_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/pixxispad_spawn_egg.png (byte-identical on rerun),
        art/candidates/fish_pixxispad_egg_r6{A,B,C,D}.png, the rejected tries as fish_pixxispad_egg_rejected_*.png,
        art/candidates/fish_pixxispad_egg.png (compare sheet) and the offline hotbar previews
        art/candidates/fish_pixxispad_egg_hotbar{,2,3}.png (GUI scale 2) and _x4.png (scale 4).
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
from egg_pool import POOL as VANILLA_POOL, POOL_COLOURS, is_pool, pool_line, vanilla_pool  # noqa: E402

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
ITEM = os.path.join(TEXTURES, "item")
OUT_ICON = os.path.join(ITEM, "pixxispad_spawn_egg.png")
CAND = os.path.join(ART, "candidates")
OUT_SHEET = os.path.join(CAND, "fish_pixxispad_egg.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_pixxispad_refonly")
PY = os.path.join(ART, ".venv", "bin", "python")
OPT_ICONS = {k: os.path.join(CAND, f"fish_pixxispad_egg_r6{k}.png") for k in "ABCD"}
OLD_KIWI = os.path.join(CAND, "fish_pixxispad_egg_round1.png")  # the first egg, as saved (not regenerated)
OLD_FILES = {"ball": os.path.join(CAND, "fish_pixxispad_egg_rejected.png"),
             "bird": os.path.join(CAND, "fish_pixxispad_egg_rejected_bird.png"),
             "painted": os.path.join(CAND, "fish_pixxispad_egg_rejected_painted.png")}
SHARK = os.path.join(ITEM, "huta_kahla_spawn_egg.png")
OUR_EGGS = sorted(os.path.basename(p)[:-len("_spawn_egg.png")]
                  for p in glob.glob(os.path.join(ITEM, "*_spawn_egg.png"))
                  if not p.endswith("pixxispad_spawn_egg.png"))


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAL = {
    # the pixxispad: the owner-accepted item icon's palette (art/src/fish_pixxispad_icon.py PAL), same keys
    "S": hx("#c4b4a4"), "s": hx("#9a8a80"), "u": hx("#6e5c5c"),  # sword: pale tan, darker tip, dark root underside
    "H": hx("#8a7072"), "h": hx("#7a6266"), "1": hx("#664c5c"), "2": hx("#4a3442"),  # purple-bronze cap, lit to dark
    "3": hx("#8c7876"), "4": hx("#a69896"), "5": hx("#ccc2ba"),  # bronze-silver, silver, pale belly
    "g": hx("#7a6e72"), "G": hx("#54484f"),   # shaded toward the lower right
    "o": hx("#24161e"),                       # shaded rim, and the sword's dark edge
    "e": hx("#0a080c"),                       # the eye (the only black)
    "j": hx("#7a6670"),                       # short lower jaw
    "p": hx("#5a4450"),                       # pectoral fins
    "D": hx("#8a7480"), "d": hx("#5a4450"),   # dorsal fin: lit leading edge, membrane
    "T": hx("#8a7480"), "t": hx("#5e4654"),   # tail: lit, dark
    "k": hx("#1c1218"),                       # keel on the tail stalk
    # the old pool (now swapped for vanilla's): our own deep open-sea indigo ramp
    "a": hx("#1e2560"),
    "b": hx("#2b3c86"),
    "c": hx("#3a55a8"),
    "w": hx("#5579c8"),
    "W": hx("#a4bdf0"),
}
# Our own old pool's colours: vanilla_pool() takes them out and puts vanilla's pool in (owner 2026-11-18,
# "the pool under the egg should be the same as vanilla"; art/src/egg_pool.py).
OLD_POOL = {PAL[k] for k in "abcwW"}
# The swordfish's own pool. Owner 2026-11-18: "for the swordfish fix it by making a full pool under it in the style of
# the vanilla pool", then "swordfish needs a full circular pool under it". Its egg leans to the right (its base on
# row 13 is x 8-13; vanilla's eggs stand on x 5-10), so vanilla's pool in vanilla's place left it hanging off the right
# end with a gap on the left. Instead it gets the whole of vanilla's pool, every pixel of the ring, moved right by
# POOL_SHIFT so it sits under the egg's own base:
# - vanilla's 30 pool pixels and colours (art/src/egg_pool.py), all moved right by 2 (x 4-15). A shift of 3, which
#   would centre it exactly, runs off the slot; 2 takes it to the right edge, as vanilla's dolphin and nautilus
#   pools reach x 15;
# - plus RING_FILL: the 6 pixels where vanilla's own egg stands (row 13, x 5-10, never seen on vanilla), drawn as the
#   far edge of the water in vanilla's pool colours, lit on the left and shading to the right as vanilla's row 13
#   does, so the oval is closed. Only the first of them (x 7 after the shift) shows; the egg covers the rest.
# Where the egg covers pool pixels the egg stays in front, as on vanilla's eggs. The egg itself is unchanged.
_S, _R, _T = (75, 152, 196), (62, 118, 163), (53, 90, 139)
RING_FILL = {(5, 13): _S, (6, 13): _S, (7, 13): _R, (8, 13): _R, (9, 13): _T, (10, 13): _T}
POOL_SHIFT = 2
PIXXISPAD_POOL = {(x + POOL_SHIFT, y): c for (x, y), c in {**VANILLA_POOL, **RING_FILL}.items()}
assert all(0 <= x <= 15 for x, _ in PIXXISPAD_POOL), "the pool must stay inside the slot"


def round_pool(icon):
    """The egg with our old pool taken out and the swordfish's whole round pool put in behind it."""
    im = icon.copy()
    for x in range(16):
        for y in range(16):
            p = im.getpixel((x, y))
            if p[3] and p[:3] in OLD_POOL:
                im.putpixel((x, y), (0, 0, 0, 0))
    for xy, c in PIXXISPAD_POOL.items():
        if im.getpixel(xy)[3] == 0:
            im.putpixel(xy, c + (255,))
    round_pool_line(im)
    return im


def is_round_pool(xy, colour):
    return PIXXISPAD_POOL.get(xy) == tuple(colour[:3]) and colour[3] == 255


def round_pool_line(icon):
    """Each pixel of the round pool is its colour or behind the egg's body; no pool blue anywhere else."""
    shown = under = 0
    for x in range(16):
        for y in range(16):
            p = icon.getpixel((x, y))
            if (x, y) in PIXXISPAD_POOL:
                assert p[3], f"pool pixel ({x},{y}) is empty"
                if is_round_pool((x, y), p):
                    shown += 1
                else:
                    assert p[:3] not in POOL_COLOURS, f"pool pixel ({x},{y}) has the wrong blue"
                    under += 1
            else:
                assert not (p[3] and p[:3] in POOL_COLOURS), f"pool blue at ({x},{y}), outside the pool"
    return (f"pool: vanilla's whole pool and colours (owner's exception), closed into a ring and moved right by "
            f"{POOL_SHIFT}: {shown} of its {len(PIXXISPAD_POOL)} pixels shown, {under} behind the egg; no pool blue "
            f"anywhere else")


POOL_KEYS = "abcwW"

OPTIONS = {
    # A: a long egg tilted head-up (narrow end upper left at x 5, rows 5-7; blunt end lower right in the pool), the
    # sword running up-left out of the narrow end to the tip at 0,2 (5 px, a 3-in-5 slope); eye at 8,7, three columns
    # behind and two rows below the root.
    "A": [
        "................",
        "................",
        "s...........d...",
        "osS........Dd...",
        ".ooSS....Ddd....",
        "...uuhHHHh11....",
        ".....34HHh1122..",
        ".....454eh1122o.",
        "......55433h122o",
        "......g55433gGGo",
        ".......g4433gGGo",
        "........Gg3gGGo.",
        ".........GgGGo..",
        "......cboooooobc",
        "......bcwWccwWcb",
        ".......abbaabba.",
    ],
    # B: an upright egg leaning forward (top at x 5-8, row 4), the sword angled steeply up-left from the top front to
    # the tip at 1,0, its dark edge on the right; the eye low and back at 7,8.
    "B": [
        ".so.............",
        "..so............",
        "..So.......d....",
        "...Su.....Dd....",
        "....ShHh1Ddd....",
        "....u3HHh1d.....",
        "...443Hh112.....",
        "...5443h1122....",
        "..45543e1122o...",
        "..455543312Go...",
        ".p4554433ggGop..",
        ".pg454433ggGGo..",
        "..oGg4433ggGGo..",
        "..cboooooooobc..",
        "..bcwWccwWcwcb..",
        "...abbaabbaab...",
    ],
    # C: an upright egg in the lower right (rows 5-12, x 4-15 with the fin flaps), the sword at 45 degrees from the
    # top-left corner (0,0) to the egg's upper front (6,6), 7 px; the eye at 10,8.
    "C": [
        "s...............",
        "os..............",
        ".oS..........d..",
        "..oS........Dd..",
        "...uS......Ddd..",
        "....uS..hHh1d...",
        ".....uShHHh12...",
        "......u4Hhh122..",
        "......4543e12o..",
        ".....45543312Go.",
        "....p455443ggGop",
        "....pg54443gGGo.",
        ".....oGg4433gGo.",
        "....cboooooooobc",
        "....bcwWccwWcwcb",
        ".....abbaabbaab.",
    ],
    # D: a long egg lying level in its pool (rows 7-12, x 6-15), a level sword 6 px long on row 8 out of the upper
    # front, dark underneath (row 9); the eye low and back at 10,10, two rows below the sword and five columns behind.
    "D": [
        "................",
        "................",
        "................",
        "................",
        "............d...",
        "..........Ddd...",
        ".........Ddd....",
        "........hHHh112.",
        "sssSSShHHHh11222",
        ".oooou344hh1122o",
        "......4554e3gGGo",
        "......g55443gGGo",
        ".......Gg443gGo.",
        ".....cbooooooobc",
        ".....bcwWccwWcwb",
        "......abbaabbaa.",
    ],
}
LABELS = {"A": "A: tilted long egg, sword up-left", "B": "B: leaning egg, steep sword",
          "C": "C: egg low right, sword corner to corner", "D": "D: long egg lying level, level sword"}
CHOSEN = "A"  # the blind reads: the only option called a swordfish by every reader at both sizes, never a bird

# Owner-rejected eggs, kept only for the compare sheet.
REJECTED = {
    # Round 5 B, the sword painted on: read as "a grey cone / wizard hat" or "a shark fin", the blade as stripes.
    "painted": [
        "................",
        "...........d....",
        "..........dd....",
        "......hHHDd.....",
        ".....hHh112.....",
        "....hHHhe122....",
        "....hHHh1122....",
        "...h3u55112Go...",
        "..h43u533112Go..",
        "..33u5s4443gGo..",
        ".p3uSs3544433gG.",
        ".p3Ss3544433gGp.",
        ".oss44444433ggo.",
        "..cboooooooobc..",
        "..bcwWccwWcwcb..",
        "...abbaabbaab...",
    ],
    # Round 4 layout D: "kind of looks like a bird now" (the level sword at eye height read as a beak).
    "bird": [
        "................",
        "................",
        "...........d....",
        "......1111Dd....",
        ".....1hHHh2.....",
        "....1hHHhh12....",
        "....1Heh1112....",
        "Ssu4333h1112o...",
        "..j44433311gGo..",
        "..455544433gGo..",
        ".p4555544433gGp.",
        ".pg555544433gGp.",
        ".oG44444433ggGo.",
        "..cboooooooobc..",
        "..bcwWccwWcwcb..",
        "...abbaabbaab...",
    ],
    # The ball: "looks like a pufferfish since its ball shaped".
    "ball": [
        "............D...",
        "..........Dd....",
        "..........Dd....",
        "......hHH1Ddd...",
        ".....hHDD2222...",
        "....hHD122222o..",
        "....H1112222Go..",
        "...hHe11222222o.",
        "Ss3uj43333222Go.",
        "....4555443gGGo.",
        "...p4555544ggGop",
        "...pg555444gGop.",
        ".....og444gGo...",
        "...cbboooooobcd.",
        ".abcWwccwWcwWcba",
        "..abba.abbaabba.",
    ],
}
REJECTED_LABELS = {"kiwi": "round 1 file (whole fish: 'kiwi bird')", "ball": "the ball: 'pufferfish'",
                   "bird": "round 4: 'looks like a bird'", "painted": "round 5, sword painted on: 'cone / fin'"}

BLIND_READ = [
    # One fresh helper per option (no context), the six eggs shuffled in a hotbar (light and dark backdrop): first at
    # actual size (1x, "small"), then at 2x ("large"). Answers word for word for our egg's slot.
    "A, reader 1:  1x 'A dark body with a lighter spike. Maybe a swordfish; no other feature reads. Low.'",
    "              2x 'A grey-brown body with a long pointed snout to the right, like a bill. Swordfish, from the long bill. Medium.'",
    "A, reader 2:  1x 'A grey fish with a long snout, maybe a swordfish. It reads as a long grey shape with a red dot. Low.'",
    "              2x 'A swordfish: a dark grey body with a long thin pointed bill and a red eye or gill mark. Medium.'",
    "B, reader 1:  1x 'Possibly a grey rabbit or cat, from the grey body and dark top.'  2x 'A rabbit, from the grey head with two "
    "upright pointed ears with pink insides. Medium.'",
    "C, reader 1:  1x 'Swordfish or narwhal: grey body with a long diagonal spike. Low.'  2x 'Swordfish: grey fish with a long "
    "sword-like bill. Medium. I dropped narwhal.'",
    "C, reader 2:  1x 'Dark grey fish or shark: a dark triangular, finned shape. Low.'  2x 'Narwhal or swordfish: grey body with "
    "a long pale spike pointing up and right. Medium.'",
    "D, reader 1:  1x 'Grey with a long snout to the left, maybe a rat or mouse. Low.'  2x 'Dark grey egg with a long thin grey "
    "snout or tail to the left and a pale spot: rat, or a long fish such as a moray or needlefish. Low-medium.'",
    "Tally: A swordfish 4 of 4; C swordfish 2 of 4 (narwhal twice, shark once); B rabbit; D rat or mouse. Nobody said bird for "
    "any option. A is CHOSEN.",
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
    res = subprocess.run([PY, os.path.join(ART, "tools", "measure.py")] + paths, capture_output=True, text=True)
    lines = []
    for line in res.stdout.splitlines():
        if line.startswith("{"):
            d = eval(line, {"np": __import__("numpy")})  # measure.py prints dicts with numpy floats
            lines.append(f"{d['file']:<34} cover {d['coverage']:.2f}  colours {d['colours']:>2}  dark {d['lmin']:.2f}  "
                         f"light {d['lmax']:.2f}  edge {d['edge_l']:.2f}  inside {d['interior_l']:.2f}  "
                         f"TL-BR {d['tl_minus_br']:+.2f}")
    return lines


def colours(im):
    return {im.getpixel((x, y))[:3] for x in range(16) for y in range(16) if im.getpixel((x, y))[3] > 0}


def copy_check(icon):
    """Exact-pixel copy check against every vanilla spawn egg (as art/candidates/critic_sardina_egg_v5/check.py),
    and the colours against every vanilla egg.
    Vanilla's own pool pixels are allowed (the owner's exception, art/src/egg_pool.py), and on the chosen egg the
    pixels of its round pool (vanilla's pool moved right, PIXXISPAD_POOL); any other copied pixel fails the run."""
    ours = {(x, y): icon.getpixel((x, y)) for x in range(16) for y in range(16) if icon.getpixel((x, y))[3] > 0}
    rnd = all(is_round_pool(xy, icon.getpixel(xy)) or icon.getpixel(xy)[:3] not in POOL_COLOURS
              for xy in PIXXISPAD_POOL) and icon.getpixel((7, 13))[:3] in POOL_COLOURS  # the swordfish's round pool
    allowed = is_round_pool if rnd else is_pool
    hits, vcols = [], set()
    for f in sorted(glob.glob(os.path.join(VANILLA, "*spawn_egg*.png"))):
        v = Image.open(f).convert("RGBA")
        if v.size != (16, 16):
            continue
        same = [p for p, c in ours.items() if v.getpixel(p) == c and not allowed(p, c)]
        if same:
            hits.append((len(same), os.path.basename(f)))
        vcols |= colours(v)
    shared = (colours(icon) - POOL_COLOURS) & vcols
    assert not hits, f"copies vanilla pixels besides the pool: {hits}"
    hits.sort(reverse=True)
    most = f"most: {hits[0][0]} in {hits[0][1]}" if hits else "none"
    own = {PAL[k] for k in PAL} | POOL_COLOURS
    return [f"same pixel and colour as a vanilla spawn egg, besides its pool: {sum(n for n, _ in hits)} pixels over {len(hits)} eggs ({most})",
            f"our colours (besides the pool) also used by any vanilla spawn egg: {len(shared)}",
            f"colours outside the icon palette plus the pool: {len(colours(icon) - own)}",
            round_pool_line(icon) if rnd else pool_line(icon)]


def hotbars(chosen_path):
    """Three hotbars, each at GUI scale 2 and 4. Returns (path, label) pairs."""
    tool = os.path.join(ART, "tools", "hotbar_preview.py")
    accepted = ["lampuka", "tonn", "sardina", "cerna", "awrata", "murina", "incova", "ziemel"]
    kiwi = ["file:" + OLD_KIWI] if os.path.exists(OLD_KIWI) else []
    bars = [
        ("fish_pixxispad_egg_hotbar",
         ["mc:cod_spawn_egg", "mc:pufferfish_spawn_egg", "mc:chicken_spawn_egg", "mc:parrot_spawn_egg",
          "mod:huta_kahla_spawn_egg"] + ["file:" + OPT_ICONS[k] for k in "ABCD"], 5 + "ABCD".index(CHOSEN),
         "vanilla cod, pufferfish, chicken, parrot eggs, our blue shark egg, round 6 options A, B, C, D"),
        ("fish_pixxispad_egg_hotbar2",
         kiwi + ["file:" + OLD_FILES[k] for k in ("ball", "bird", "painted")]
         + ["file:" + chosen_path, "mod:pixxispad", "bucket:pixxispad_bucket", "mc:cod_spawn_egg"],
         len(kiwi) + 3,
         ("round 1, " if kiwi else "") + "the ball, the bird egg, the painted sword (all rejected), "
         f"ROUND 6 {CHOSEN}, the pixxispad item and bucket, vanilla cod egg"),
        ("fish_pixxispad_egg_hotbar3", [f"mod:{n}_spawn_egg" for n in accepted] + ["file:" + chosen_path], 8,
         ", ".join(accepted) + f" eggs (accepted), PIXXISPAD round 6 {CHOSEN}"),
    ]
    out = []
    for name, items, sel, label in bars:
        p2, p4 = os.path.join(CAND, name + ".png"), os.path.join(CAND, name + "_x4.png")
        subprocess.run([PY, tool, p2] + items + ["--select", str(sel)], check=True, capture_output=True)
        subprocess.run([PY, tool, p4] + items + ["--select", str(sel), "--scale", "4"], check=True, capture_output=True)
        out += [(p2, f"GUI scale 2: {label}"), (p4, f"GUI scale 4: {label}")]
    return out


def tiles(im, x0, band, d, name, small):
    d.text((x0, 2), name, fill=(235, 235, 235), font=small)
    for s, col in ((8, (139, 139, 139)), (2, (139, 139, 139)), (1, (139, 139, 139)), (2, (40, 40, 40)), (1, (40, 40, 40))):
        t = Image.new("RGBA", (16 * s + 8, 16 * s + 8), col + (255,))
        t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (x0, 22))
        x0 += t.width + 6
    return x0


def text_band(lines, W, bg, ink, size=14):
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(size))
    return band


def sheet(icon, opts, old):
    font, small = label_font(16), label_font(13)
    W = 2200
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    refs = []
    for name in ("sw01_market.jpg", "sw02_essaouira.jpg", "sw04_drawing.jpg", "sw06_inat.jpg"):
        p = os.path.join(REFS, name)
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im = im.resize((360, round(360 * im.height / im.width)), Image.LANCZOS)
            refs.append((name, im))
    if refs:
        h = max(im.height for _, im in refs) + 26
        band = Image.new("RGB", (W, h), bg)
        d = ImageDraw.Draw(band)
        for i, (name, im) in enumerate(refs):
            band.paste(im, (10 + i * 370, 22))
            d.text((10 + i * 370, 2), f"{name} (reference only)", fill=ink, font=small)
        parts.append(("References (art/references/fish_pixxispad_refonly, list.tsv)", band))

    for row in (list("AB"), list("CD")):
        band = Image.new("RGB", (W, 128 + 36), bg)
        d = ImageDraw.Draw(band)
        x0 = 10
        for k in row:
            x0 = tiles(opts[k], x0, band, d, LABELS[k] + ("  (CHOSEN)" if k == CHOSEN else ""), small) + 60
        parts.append((f"Round 6 options {' and '.join(row)} at 8x, then 2x and 1x on light, 2x and 1x on dark", band))
    keys = [k for k in ("kiwi", "ball", "bird", "painted") if k in old]
    for pair in (keys[:2], keys[2:]):
        band = Image.new("RGB", (W, 128 + 36), bg)
        d = ImageDraw.Draw(band)
        x0 = 10
        for k in pair:
            x0 = tiles(old[k], x0, band, d, "rejected: " + REJECTED_LABELS[k], small) + 60
        parts.append(("The earlier owner-rejected tries, same scales", band))

    if BLIND_READ:
        parts.append(("Blind reads: one fresh helper per option, no context, 1x and 2x beside vanilla's chicken, parrot, "
                      "cod and pufferfish eggs and our blue shark egg (answers word for word)",
                      text_band(BLIND_READ, W, bg, ink)))

    bucket = Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")
    bucket.alpha_composite(Image.open(os.path.join(ITEM, "pixxispad_bucket.png")).convert("RGBA"))
    rows = [
        [("vanilla cod egg", os.path.join(VANILLA, "cod_spawn_egg.png")),
         ("vanilla pufferfish egg", os.path.join(VANILLA, "pufferfish_spawn_egg.png")),
         ("vanilla chicken egg", os.path.join(VANILLA, "chicken_spawn_egg.png")),
         ("vanilla parrot egg", os.path.join(VANILLA, "parrot_spawn_egg.png")),
         ("our blue shark egg", SHARK),
         (f"PIXXISPAD EGG ({CHOSEN})", icon),
         ("pixxispad item icon", os.path.join(ITEM, "pixxispad.png")),
         ("pixxispad bucket", bucket)],
        [(f"our {n} egg", os.path.join(ITEM, n + "_spawn_egg.png"))
         for n in ("lampuka", "tonn", "sardina", "cerna", "awrata", "murina", "incova", "ziemel")]
        + [(f"PIXXISPAD EGG ({CHOSEN})", icon)],
    ]
    for r, items in enumerate(rows):
        band = Image.new("RGB", (W, 128 + 120), bg)
        d = ImageDraw.Draw(band)
        for i, (name, p) in enumerate(items):
            im = p if isinstance(p, Image.Image) else Image.open(p).convert("RGBA")
            x0 = 10 + i * 214
            tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
            tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
            band.paste(tile.convert("RGB"), (x0, 22))
            d.text((x0, 2), name, fill=ink, font=small)
            for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1),
                                          ((40, 40, 40), 2))):
                t = Image.new("RGBA", (40, 40), col + (255,))
                t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
                band.paste(t.convert("RGB"), (x0 + (j % 2) * 44 + (j // 2) * 88, 156))
        d.text((10, 202), "8x, then 1x and 2x on light grey, 1x and 2x on dark grey", fill=ink, font=small)
        parts.append(("The chosen egg beside vanilla's eggs, our blue shark egg and the accepted pixxispad item and "
                      "bucket" if r == 0 else "The chosen egg beside our accepted eggs", band))

    lines = measure([os.path.join(VANILLA, n + "_spawn_egg.png") for n in ("cod", "pufferfish", "chicken", "parrot")]
                    + [SHARK] + [OPT_ICONS[k] for k in "ABCD"])
    for k in "ABCD":
        lines += [f"option {k}: " + c for c in copy_check(opts[k])]
    parts.append(("art/tools/measure.py and the copy check (no vanilla pixel copied)", text_band(lines, W, bg, ink)))

    for path, label in hotbars(OPT_ICONS[CHOSEN]):
        im = Image.open(path).convert("RGB")
        if im.width > W - 20:
            im = im.resize((W - 20, round(im.height * (W - 20) / im.width)), Image.NEAREST)
        band = Image.new("RGB", (W, im.height + 30), bg)
        band.paste(im, (10, 4))
        ImageDraw.Draw(band).text((10, im.height + 8), os.path.relpath(path, ROOT), fill=ink, font=small)
        parts.append((f"Offline hotbar preview (art/tools/hotbar_preview.py), {label}", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Pixxispad (swordfish) spawn egg, round 6: a new shape, the sword clear of the body, "
           "textures/item/pixxispad_spawn_egg.png", fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    os.makedirs(os.path.dirname(OUT_SHEET), exist_ok=True)
    out.save(OUT_SHEET)
    print("wrote", OUT_SHEET)


if __name__ == "__main__":
    opts = {k: vanilla_pool(render(g), OLD_POOL) for k, g in OPTIONS.items()}
    opts[CHOSEN] = round_pool(render(OPTIONS[CHOSEN]))  # the chosen egg stands in its own round pool
    for k, im in opts.items():
        im.save(OPT_ICONS[k])
    old = {}
    if os.path.exists(OLD_KIWI):
        old["kiwi"] = Image.open(OLD_KIWI).convert("RGBA")
    for k, g in REJECTED.items():
        old[k] = render(g)
        old[k].save(OLD_FILES[k])
    icon = opts[CHOSEN]
    icon.save(OUT_ICON, optimize=False)
    print("wrote", OUT_ICON)
    if "--icons-only" not in sys.argv:
        sheet(icon, opts, old)
