"""Item icon for the lingwata (common sole, Solea solea): the caught fish, seen from its eyed side like vanilla's cod.

What makes it a sole (photos in art/references/fish_lingwata_refonly/, list.tsv), and not the boll (a ray):
- an oval, tongue-shaped flat body: a blunt round head, widest about a third back, tapering to a small rounded tail
  fan; no wings and no whip tail;
- a lighter fringe fin running all round the edge, with darker ray ticks;
- both eyes on the upper side near the head, close together on a slant (never side by side like a face), each a dark
  pupil with a pale ring, the only near-black pixels;
- the small pectoral fin behind the head with its dark tip;
- sandy brown with darker speckles, lit from the top left like vanilla's fish items.

Pose: head lower left, tail upper right, as vanilla's cod and salmon (measured, never copied).
Colours: the 3D model's (art/src/fish_lingwata_model.py, paint G), out of water: the model's browns before their x1.15
water lift, nudged a step brighter for the hotbar (vanilla foods sit at 0.54 inside luminance).

Candidates (the sheet shows all three; PICK is installed):
- A: the tongue on the diagonal, 1 px light fringe inside a dark outline, the fan tail at the top right.
- B: A a little wider and shorter, so the body inside the fringe has more room for the speckles.
- C: A with the white blind side showing as a 1 px pale rim along the shaded lower right edge.

Run:  art/.venv/bin/python art/src/fish_lingwata_icon.py [--candidate X] [--sheet]
Writes mod/.../textures/item/lingwata.png (byte-identical on rerun); with --sheet also art/candidates/fish_lingwata_icon.png
and the offline hotbar previews art/candidates/fish_lingwata_icon_hotbar.png.
"""
import math
import os
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
ART = os.path.join(ROOT, "art")
ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
OUT = os.path.join(ITEMS, "lingwata.png")
VANILLA = os.path.join(ART, ".vanilla", "item")
PICK = "I"
HOTBAR = ("F", "H", "I")   # the candidates in the hotbar preview (at most 9 slots)


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = {
    "o": hx("#4a3a2a"),   # outline on the shaded lower right
    "k": hx("#6e583f"),   # outline on the lit upper left
    "F": hx("#d2bb92"),   # fringe fin, lit
    "f": hx("#a88f6a"),   # fringe ray ticks, and the fringe in the shade
    "1": hx("#c4a87e"),   # body, lit
    "2": hx("#b0946c"),   # body
    "3": hx("#97795a"),   # body, shade
    "m": hx("#7c624a"),   # speckles
    "e": hx("#1c1714"),   # pupils
    "R": hx("#e2d4b2"),   # the pale ring round each eye
    "p": hx("#3a2c22"),   # the pectoral fin's dark tip
    "T": hx("#a88c66"),   # tail fan
    "t": hx("#806648"),   # tail fan rays and rim
    "W": hx("#e8e0cf"),   # the white blind side (C)
    "g": hx("#8e7c62"),   # fringe in the shade, greyer (D, E)
    "P": hx("#9a8060"),   # the pectoral fin, mid tone (H)
    "Q": hx("#d8c49c"),   # the pectoral fin, pale (I)
    "K": hx("#86704f"),   # outline on the lit upper left (I)
    "O": hx("#3e3022"),   # outline on the shaded lower right (I)
}

SHAPES = {
    "A": dict(head=(1.6, 14.4), tail=(12.6, 3.4), w=4.1, widest=0.33),
    "B": dict(head=(1.8, 14.0), tail=(12.2, 3.8), w=4.6, widest=0.35),
    "C": dict(head=(1.6, 14.4), tail=(12.6, 3.4), w=4.1, widest=0.33),
    # icon round 1: a wider neck into a short fan, the light along the top left edge, a lighter fringe band, the eyes
    # closer on the upper half of the head, the pectoral a 2 px streak toward the lower right edge
    "D": dict(head=(1.6, 14.4), tail=(12.0, 4.0), w=4.1, widest=0.33, taper=0.3, fan=0.16, fan_w=2.4, along=0.15,
              band=True, streak=((0.4, 1.9), (0.5, 1.9))),
    "E": dict(head=(1.8, 14.2), tail=(12.0, 4.0), w=4.4, widest=0.36, taper=0.3, fan=0.16, fan_w=2.6, along=0.15,
              band=True, streak=((0.4, 2.0), (0.5, 2.0))),
}
# the tail fan, at the top right, spreading across the body's axis, rounded, with darker rays
FAN = {(13, 1): "t", (14, 1): "t", (12, 2): "t", (13, 2): "T", (14, 2): "t", (15, 2): "t",
       (12, 3): "T", (13, 3): "t", (14, 3): "T", (15, 3): "t", (13, 4): "t", (14, 4): "t"}


def mask_of(sh):
    hx_, hy = sh["head"]
    tx, ty = sh["tail"]
    ax, ay = tx - hx_, ty - hy
    L = math.hypot(ax, ay)
    ux, uy = ax / L, ay / L
    px, py = -uy, ux
    m = {}
    for y in range(16):
        for x in range(16):
            dx, dy = x + 0.5 - hx_, y + 0.5 - hy
            u = (dx * ux + dy * uy) / L
            v = dx * px + dy * py
            if u < 0 or u > 1 + sh.get("fan", 0.0):
                continue
            a = sh["widest"]
            if u > 1:
                w = sh.get("fan_w", 2.0)                 # the short tail fan, joined to the taper (icon round 1)
            elif u < a:
                w = sh["w"] * math.sqrt(max(0.0, 1 - ((a - u) / a) ** 2))
            else:
                w = sh["w"] * (1 - sh.get("taper", 0.42) * ((u - a) / (1 - a)) ** 1.6)
            if abs(v) <= w:
                m[(x, y)] = (u, v)
    return m


def nb(p):
    x, y = p
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def build(cand):
    sh = SHAPES[cand]
    m = mask_of(sh)
    mask = set(m)
    edge = {p for p in mask if any(n not in mask for n in nb(p))}
    fringe = {p for p in mask - edge if any(n in edge for n in nb(p))}
    body = mask - edge - fringe
    grid = {}
    for p in edge:
        x, y = p
        # the lit upper left rim lighter, the shaded lower right darker; C shows the white blind side there
        lit = m[p][1] < 0
        if m[p][0] > 1:
            grid[p] = "t"
            continue
        grid[p] = "k" if lit else ("W" if cand == "C" and m[p][0] > 0.15 and m[p][0] < 0.8 else "o")
    for p in fringe:
        x, y = p
        lit = m[p][1] < 0
        tick = (x + y) % 2 == 0
        if m[p][0] > 1 - 0.02:
            grid[p] = "t" if tick else "T"
            continue
        if sh.get("band"):
            # icon round 1: a lighter, greyer band, lit on the top left, darker on the bottom right, lightly dithered
            grid[p] = ("F" if not (tick and m[p][0] > 0.5) else "f") if lit else ("f" if not tick else "g")
            continue
        grid[p] = ("f" if tick else "F") if lit else ("f" if not tick else "F")
    for p in body:
        u, v = m[p]
        s = (v / sh["w"]) + sh.get("along", 0.6) * u     # light from the top left: v < 0 is the upper left side
        if u > 1:
            grid[p] = "T"
            continue
        grid[p] = "1" if s < -0.15 else ("2" if s < 0.45 else "3")
    for p, k in (FAN.items() if not sh.get("fan") else []):
        if p not in grid:
            grid[p] = k
    # features placed by body coordinates (u along from the head, v across; v < 0 the upper, lit side)
    def at(u, v):
        return min(sorted(body), key=lambda q: (m[q][0] - u) ** 2 * 120 + (m[q][1] - v) ** 2)
    eyes = EYES[cand]
    for e in eyes:
        for n in nb(e):
            if n in body or n in fringe:
                grid[n] = "R"
    for e in eyes:
        grid[e] = "e"
    if sh.get("streak"):
        # icon round 1: a 2 px dark brown streak toward the lower right edge, behind the eyes, not a dot
        for q in (at(*sh["streak"][0]), at(*sh["streak"][1])):
            grid[q] = "p"
    else:
        spot = at(0.58, 1.7)
        grid[spot] = "p"
    for u, v in MARKS[cand]:
        q = at(u, v)
        if grid[q] not in "eRp" and all(grid.get(n) not in ("e",) for n in nb(q)):
            grid[q] = "m"
    return grid


# the two eyes on the upper (lit, dorsal) side near the head, one behind the other along the body, 1 px apart
EYES = {"A": [(3, 11), (5, 9)], "B": [(3, 11), (5, 9)], "C": [(3, 11), (5, 9)], "D": [(3, 10), (4, 8)],
        "E": [(3, 10), (4, 8)]}   # pixels
# speckles, by body coordinates, away from the eyes
MARKS = {
    "A": [(0.5, -1.2), (0.62, 0.8), (0.75, -0.5), (0.45, 1.6), (0.85, 0.6), (0.55, 0.0)],
    "B": [(0.5, -1.4), (0.62, 1.0), (0.75, -0.6), (0.45, 1.9), (0.85, 0.7), (0.55, 0.0), (0.68, -1.8)],
    "C": [(0.5, -1.2), (0.62, 0.8), (0.75, -0.5), (0.45, 1.6), (0.85, 0.6), (0.55, 0.0)],
    "D": [(0.55, -1.0), (0.66, 0.6), (0.8, -0.4), (0.5, 0.4), (0.9, 0.5)],
    "E": [(0.55, -1.0), (0.66, 0.6), (0.8, -0.4), (0.5, 0.4), (0.9, 0.5), (0.72, 1.6)],
}


# Icon round 2 ("reads as a sausage"): candidates F and G are drawn from a hand silhouette instead, an oval tongue
# about 2 : 1 with a rounded nose, a 1 px stalk and a flared fan tail at the top right like vanilla's cod (measured,
# not copied). T is the tail, s the stalk. G has a wider fan.
SIL = {
    "F": ["................",
          "............TT..",
          "...........TTTT.",
          "..........TTTT..",
          "......####sTT...",
          ".....#######....",
          "....########....",
          "...#########....",
          "..##########....",
          "..#########.....",
          ".##########.....",
          ".#########......",
          ".########.......",
          ".#######........",
          "..#####.........",
          "................"],
    "G": ["............T...",
          "...........TTT..",
          "...........TTTT.",
          "..........sTTTT.",
          "......####sTT...",
          ".....#######....",
          "....########....",
          "...#########....",
          "..##########....",
          "..#########.....",
          ".##########.....",
          ".#########......",
          ".########.......",
          ".#######........",
          "..#####.........",
          "................"],
    # icon round 3: longer (about 2.2 : 1), narrowing steadily to a small 3 x 3 fan sitting right on the body, no
    # stalk; the lower left corner rounded in 3-2-1 steps
    "H": ["................",
          ".............TT.",
          "............TTTT",
          "...........#TTT.",
          ".........####T..",
          "........#####...",
          ".......######...",
          ".....########...",
          "....#########...",
          "...#########....",
          "..##########....",
          "..#########.....",
          ".#########......",
          ".########.......",
          "..######........",
          "...###.........."],
    # icon round 4 ("a drumstick"): broad, about 2 : 1, no neck at all, the oval flowing into a 3-4 px fan
    "I": ["................",
          "...........TTT..",
          "..........TTTTT.",
          ".........##TTTT.",
          "........######..",
          "......#######...",
          ".....########...",
          "....##########..",
          "...##########...",
          "..###########...",
          "..##########....",
          ".##########.....",
          ".#########......",
          ".########.......",
          "..######........",
          "...###.........."],
}
HAND_I = {"eyes": [(4, 11), (6, 9)], "pec": [((6, 7), "Q"), ((7, 6), "p")],
          "blots": [((8, 8),), ((10, 6),), ((7, 11),), ((9, 9), (10, 8)), ((5, 13),), ((11, 5),)]}
HAND_H = {"eyes": [(4, 11), (6, 9)], "pec": [((8, 11), "P"), ((9, 10), "p")],
          "blots": [((7, 7),), ((9, 6), (10, 5)), ((6, 12),), ((10, 8),), ((8, 9),), ((4, 13), (5, 13))]}
# eyes on the upper (top left) half of the head, one step apart with a pale ring each; the pectoral one dark texel
# behind and below them; three soft 2 x 1 blotches one tone darker
HAND = {"eyes": [(3, 10), (5, 8)], "pec": (7, 11), "blots": [((6, 6), (7, 6)), ((7, 9), (8, 9)), ((4, 12), (5, 12))]}


def build_hand(cand):
    rows = SIL[cand]
    hand = {"H": HAND_H, "I": HAND_I}.get(cand, HAND)
    body = {(x, y) for y, r in enumerate(rows) for x, c in enumerate(r) if c in "#s"}
    tail = {(x, y) for y, r in enumerate(rows) for x, c in enumerate(r) if c == "T"}
    allm = body | tail
    edge = {p for p in body if any(n not in allm for n in nb(p))}
    fringe = {p for p in body - edge if any(n in edge for n in nb(p))}
    inner = body - edge - fringe
    grid = {}
    for (x, y) in edge:
        lit = (x - 1, y) not in allm or (x, y - 1) not in allm
        if cand == "I":
            # icon round 4: the upper left rim lighter, the lower right one tone darker
            grid[(x, y)] = "K" if (lit and x + y < 15) else "O"
            continue
        grid[(x, y)] = "k" if lit and not ((x + 1, y) not in allm or (x, y + 1) not in allm) else ("k" if lit and x + y < 13 else "o")
    for (x, y) in fringe:
        lit = x + y < 13 or (x - 1, y) in edge and grid[(x - 1, y)] == "k" or (x, y - 1) in edge and grid[(x, y - 1)] == "k"
        tick = (x + y) % 2 == 0
        if cand == "I":
            # icon round 4: a band one tone lighter than the body edge, broken by darker ray pixels
            grid[(x, y)] = ("f" if (x + 2 * y) % 3 == 0 else "F") if lit else ("g" if (x + 2 * y) % 3 == 0 else "f")
        elif cand == "H":
            # icon round 3: the fringe band all round, two alternating tones for the rays
            grid[(x, y)] = ("g" if tick else "F") if lit else ("g" if tick else "f")
        else:
            grid[(x, y)] = ("f" if tick else "F") if lit else ("g" if tick else "f")
    for (x, y) in inner:
        side = x + y                         # across the body: a smaller x + y is the lit upper left side
        lo, hi = {"H": (14, 16), "I": (13, 16)}.get(cand, (13, 15))
        grid[(x, y)] = "1" if side <= lo else ("2" if side <= hi else "3")
    for (x, y) in tail:
        out = any(n not in allm for n in nb((x, y)))
        grid[(x, y)] = "t" if out or (x + y) % 2 == 0 else "T"
    for blot in hand["blots"]:
        for q in blot:
            if q in inner:
                grid[q] = "m"
    if isinstance(hand["pec"], list):
        for q, k in hand["pec"]:
            grid[q] = k
    else:
        grid[hand["pec"]] = "p"
    for e in hand["eyes"]:
        for n in nb(e):
            if n in inner or n in fringe:
                grid[n] = "R"
    for e in hand["eyes"]:
        grid[e] = "e"
    return grid


def image(cand):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for (x, y), k in (build_hand(cand) if cand in SIL else build(cand)).items():
        img.putpixel((x, y), PAL[k] + (255,))
    return img


def ascii_grid(cand):
    g = build_hand(cand) if cand in SIL else build(cand)
    return ["".join(g.get((x, y), ".") for x in range(16)) for y in range(16)]


def check_copy(img):
    same = []
    for n in ("cod", "salmon", "tropical_fish", "pufferfish", "cooked_cod", "cooked_salmon"):
        p = os.path.join(VANILLA, n + ".png")
        if not os.path.exists(p):
            continue
        v = Image.open(p).convert("RGBA")
        same += [(n, x, y) for y in range(16) for x in range(16)
                 if img.getpixel((x, y))[3] and img.getpixel((x, y)) == v.getpixel((x, y))]
    assert not same, f"pixels identical to vanilla: {same}"


def sheet():
    sys.path.insert(0, os.path.join(ART, "tools"))
    from measure import measure
    W = 1500
    SLOT = (139, 139, 139, 255)
    blocks = []
    font = None
    try:
        from font import label_font
        font = label_font(14)
    except Exception:
        pass

    def text(t):
        im = Image.new("RGBA", (W, 26), (255, 255, 255, 255))
        ImageDraw.Draw(im).text((8, 5), t, fill=(0, 0, 0), font=font)
        blocks.append(im)

    vanilla = [(n, Image.open(os.path.join(VANILLA, n + ".png")).convert("RGBA"))
               for n in ("cod", "salmon", "tropical_fish", "pufferfish")]
    boll = ("boll (accepted)", Image.open(os.path.join(ITEMS, "boll.png")).convert("RGBA"))
    cands = [(c, image(c)) for c in HOTBAR]
    row_items = vanilla + [boll] + [("lingwata " + c + (" PICK" if c == PICK else ""), im) for c, im in cands]
    text("8x on the slot grey: vanilla cod, salmon, tropical fish, pufferfish | the accepted boll | lingwata " + ", ".join(HOTBAR) + " (earlier rounds: A-E by fish_lingwata_icon.py --candidate)")
    row = Image.new("RGBA", (W, 160), SLOT)
    d = ImageDraw.Draw(row)
    for i, (n, im) in enumerate(row_items):
        row.alpha_composite(im.resize((128, 128), Image.NEAREST), (10 + i * 150, 4))
        d.text((10 + i * 150, 136), n, fill=(0, 0, 0), font=font)
    blocks.append(row)
    text("1x and 2x (same order)")
    row = Image.new("RGBA", (W, 60), SLOT)
    for i, (n, im) in enumerate(row_items):
        row.alpha_composite(im, (10 + i * 20, 20))
        row.alpha_composite(im.resize((32, 32), Image.NEAREST), (240 + i * 40, 12))
    blocks.append(row)
    ref = os.path.join(ART, "references", "fish_lingwata_refonly")
    refs = [Image.open(os.path.join(ref, n)).convert("RGBA") for n in ("solea1.jpg", "solea.jpg", "plate1.jpg")
            if os.path.exists(os.path.join(ref, n))]
    text("References (reference only)")
    row = Image.new("RGBA", (W, 200), (255, 255, 255, 255))
    x = 10
    for im in refs:
        im.thumbnail((400, 190))
        row.alpha_composite(im, (x, 5))
        x += im.width + 10
    blocks.append(row)
    tmp = os.path.join(ART, "candidates", "fish_lingwata_icon_measure.tmp.png")
    lines = []
    for n, im in row_items:
        im.save(tmp)
        r = measure(tmp)
        lines.append(f"{n:22s} coverage {r['coverage']:.2f} colours {r['colours']:2d} darkest {float(r['lmin']):.2f} "
                     f"lightest {float(r['lmax']):.2f} outline {float(r['edge_l']):.2f} inside {float(r['interior_l']):.2f} "
                     f"tl-br {float(r['tl_minus_br']):+.2f}")
    os.remove(tmp)
    for ln in lines:
        text(ln)
    hb = os.path.join(ART, "candidates", "fish_lingwata_icon_hotbar.png")
    files = []
    for c, im in cands:
        p = os.path.join(ART, "candidates", "fish_lingwata_icon_%s.png" % c)
        im.save(p)
        if c in HOTBAR:
            files.append("file:" + p)
    subprocess.run([sys.executable, os.path.join(ART, "tools", "hotbar_preview.py"), hb, "mc:cod", "mod:boll"] + files
                   + ["mc:salmon", "mc:tropical_fish", "bucket:boll_bucket", "--scale", "3"], check=True,
                   stdout=subprocess.DEVNULL)
    text("Offline hotbar (GUI scale 3, unselected): cod, boll, lingwata " + ", ".join(HOTBAR) + ", salmon, tropical fish, boll bucket")
    hbi = Image.open(hb).convert("RGBA")
    row = Image.new("RGBA", (W, hbi.height + 10), (255, 255, 255, 255))
    row.alpha_composite(hbi, (10, 5))
    blocks.append(row)
    out = Image.new("RGBA", (W, sum(b.height for b in blocks)), (255, 255, 255, 255))
    y = 0
    for b in blocks:
        out.alpha_composite(b, (0, y))
        y += b.height
    dest = os.path.join(ART, "candidates", "fish_lingwata_icon.png")
    out.convert("RGB").save(dest)
    print("sheet:", dest)


def main():
    args = sys.argv[1:]
    cand = args[args.index("--candidate") + 1] if "--candidate" in args else PICK
    img = image(cand)
    check_copy(img)
    img.save(OUT)
    print("installed", cand, "->", os.path.relpath(OUT, ROOT))
    if "--ascii" in args:
        for c in list(SHAPES) + list(SIL):
            print(c)
            print("\n".join(ascii_grid(c)))
    if "--sheet" in args:
        sheet()


if __name__ == "__main__":
    main()
