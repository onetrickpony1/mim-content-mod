"""Item texture for fenek moqli (Maltese fried rabbit), catalogue D22. Candidates, 2026-11-17.

Rabbit pieces marinated in wine and garlic and fried in olive oil, often served with fried potatoes.

Owner's photos (reference only, never traced): art/references/fenek_moqli_owner/.
What they show:
- a plain white plate (the same kind as the accepted lampuka moqlija, so the fried dishes match);
- several rabbit pieces in a heap, a rich golden to mahogany brown, glossy, with darker caramelised patches;
- pale chunks and slices of garlic stuck on the meat and lying in the oil;
- a leg piece with a pale bone end (the illustration);
- in two photos, golden fried potato slices beside the meat.

The plate is fish.py's plate() at the lampuka moqlija's size and place. The pieces, garlic, bone and potatoes are
hand-placed parts; their light, edges and dark caramelised specks are rules on top (light from the top left).

Round 3 (g to k): the owner, of round 2: "no the closest is e and still its too much like a chicken leg. these words
were key: 'a rabbit hind leg has a meaty lower leg running its whole length, a visible knee, and a thigh that is longer
than it is wide, widest at the hip.'" So these draw the leg as one long, lean shape (hip, thigh, knee, lower leg, bone
tip) spanning most of the plate, with no round ball and no bare bone stick. Silhouettes from photos of rabbit hind legs,
raw and fried (reference only, never traced): art/references/fenek_moqli_refonly/.

Run:  art/.venv/bin/python art/src/fenek_moqli.py
Writes art/candidates/fenek_moqli_{a..l,l2}.png, art/candidates/fenek_moqli_compare.png,
art/candidates/fenek_moqli_legs_1x.png, and installs PICK as
mod/src/main/resources/assets/mimcontent/textures/item/fenek_moqli.png.
"""
import glob
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fish  # noqa: E402
import food_items as F  # noqa: E402

hx, render, check = F.hx, F.render, F.check
OUT, VANILLA, ART = F.OUT, F.VANILLA, F.ART
label_font = F.label_font
ROOT = os.path.dirname(ART)
ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")

KINDS = list("abcdefghijkl") + ["l2", "e3", "e4"]
PICK = "e4"
SHOW = ["e", "e3", "e4"]     # the comparison sheets

PAL = dict(fish.PAL)
PAL.update({
    # fried rabbit: golden to mahogany brown, glossy, darker caramelised patches
    "u": hx("#f0c47a"),   # glossy highlight
    "v": hx("#d8944a"),   # lit meat
    "x": hx("#b8692c"),   # meat
    "z": hx("#8c461a"),   # meat in shade, lit edges
    "Z": hx("#5e2c0e"),   # edges facing away, the gaps between pieces
    "j": hx("#47200a"),   # caramelised dark patches
    # garlic
    "G": hx("#f6efd6"), "H": hx("#d6c494"),
    # bone end
    "N": hx("#efe4c8"), "n": hx("#9a8660"),
    # fried potato slices
    "P": hx("#f6d86a"), "Q": hx("#dcae3c"), "S": hx("#8a5e18"),
    # the plate's outline: two letters (plate() splits the rim by side), both the lampuka moqlija plate's own grey
    # (owner 2026-11-17: "lighter grey, yes matching"; it was #58524a / #635d54, darker than the lampuka plate)
    "X": fish.PAL["R"], "V": fish.PAL["R"],
})

# ---- parts: pieces A B C D (each shaded on its own), g garlic, b bone, p potato ----
# a: a heap of three pieces on the plate, a leg with its bone end pointing to the top right, garlic on top.
# The bone breaks out past the plate's top-right edge, so it reads against the slot and not only on the white rim.
PARTS_A = [
    "................",
    ".............bbb",
    ".............bb.",
    "............bb..",
    ".......AAA.bb...",
    "......AAAAAA....",
    ".....AAAAAAA....",
    ".....AAAgAA.....",
    "....CCCAAABBB...",
    "...CCCCCCBBBBB..",
    "...CCgCCBBBgBB..",
    "....CCCCBBgBB...",
    ".....CC..BBB....",
    "................",
    "................",
    "................",
]
# b: two pieces on the left, golden potato slices on the right (as in two of the photos), garlic on the meat.
PARTS_B = [
    "................",
    "................",
    "................",
    "................",
    ".....AAAA..ppp..",
    "....AAgAAApppp..",
    "....AAAAAApppp..",
    "...CCAAAA..ppp..",
    "...CCCCAA.rrr...",
    "...CCgCCCrrrr...",
    "...CCCCCCrrrr...",
    "....CCCC..rr....",
    "................",
    "................",
    "................",
    "................",
]
# c: four smaller pieces in a heap, garlic on top, no bone: the fenkata platter look.
PARTS_C = [
    "................",
    "................",
    "................",
    "................",
    "......AAA.DDD...",
    ".....AAgAADDDD..",
    ".....AAAAADgDD..",
    "....CCCAAADDD...",
    "...CCCCCBBBB....",
    "...CCgCBBBBBB...",
    "....CCCBBgBBB...",
    ".....CC.BBBB....",
    "................",
    "................",
    "................",
    "................",
]


# ---- round 2 (owner 2026-11-17: "b is the best because it has potatoes, but the rabbit doesnt read as rabbit in any
# of them. closest would be the bone one, but a rabbit leg usually includes the thigh too") ----
# b's plate, potatoes and garlic, with a whole fried hind leg as the main piece: the plump thigh (A) joined at the
# knee to the long, slim lower leg (D), ending in the pale bone end (b), which breaks past the plate's edge.
# A and D are shaded as separate pieces, so a dark line marks the knee. The potatoes sit in front (bottom right), so
# their insides take the shaded yellow. The maps below are drawn with the thigh on the left; fenek_moqli() mirrors them
# (thigh bottom right, bone past the top-left edge, potatoes on the left as in the owner's plate photo), which keeps
# the icon's light on the top left (with the thigh on the left, top-left minus bottom-right came out below zero).
LEGS = {
    # d: thigh lying low on the left, the lower leg rising to the top right, the bone past the plate's top edge
    "d": [
        "............bb..",
        "...........bbb..",
        "..........bb....",
        ".........DDD....",
        "........DDD.....",
        ".......DDD......",
        "......DDD.......",
        "..AAAADD........",
        ".AAAAAAA..ppp...",
        ".AAgAAAA.pppp...",
        ".AAAAAAA.pppp...",
        "..AAgAA.rrrr....",
        "...AAA..rrrr....",
        "........rrr.....",
        "................",
        "................",
    ],
    # e: thigh on the upper left, the lower leg running right, the bone past the plate's right edge; a smaller
    # piece and the potatoes below
    "e": [
        "................",
        "................",
        "................",
        "...AAAA.......bb",
        "..AAAAAA....DDbb",
        "..AAgAAAADDDD...",
        "..AAAAAAADD.....",
        "...AAAAAA.......",
        "....AAAA..ppp...",
        ".........pppp...",
        "....CCC..pppp...",
        "...CCgCC.rrrr...",
        "....CCCrrrrr....",
        "........rrr.....",
        "................",
        "................",
    ],
    # f: d's leg alone, larger, the potatoes in one row along the front
    "f": [
        "............bb..",
        "...........bbb..",
        "..........bb....",
        ".........DDD....",
        "........DDD.....",
        ".......DDD......",
        "...AAADDD.......",
        "..AAAAADD.......",
        ".AAAgAAAA.ppp...",
        ".AAAAAAAApppp...",
        "..AAAAgAApppp...",
        "...AAAAA.rrrr...",
        "....rrr..rrrr...",
        "...rrrr...rr....",
        "................",
        "................",
    ],
}


# Hand finish on top of the rules, in the icon's own (mirrored) coordinates. d, critic round 2: "at 1x it's still a ball
# on a stick (drumstick)": a 2 px meaty lower leg lit on its upper right, a notch at the knee, and a thigh longer than
# it is wide (24 pixels).
FINISH = {
    # e, owner 2026-11-17: "go back to e and just fix the potatoes". The fried potato slices read golden at 1x: at most
    # one dark pixel in three, only on edges away from the light (the back slice's lower edge marks it off from the
    # front one), the rest lit.
    "e": {
        (4, 8): "P", (5, 8): "P", (6, 8): "P",
        (4, 9): "P", (5, 9): "Q", (6, 9): "Q", (7, 9): "Q",
        (4, 10): "Q", (5, 10): "S", (6, 10): "S", (7, 10): "S",
        (4, 11): "P", (5, 11): "P", (6, 11): "P", (7, 11): "Q",
        (5, 12): "P", (6, 12): "Q", (7, 12): "Q", (8, 12): "Q", (9, 12): "S",
        (6, 13): "S", (7, 13): "S", (8, 13): "S",
    },
    "d": {
        # lower leg
        (7, 3): "v", (8, 3): "Z", (7, 4): "x", (8, 4): "v", (9, 4): "Z", (8, 5): "x", (9, 5): "v", (10, 5): "Z",
        (9, 6): "x", (10, 6): "u", (11, 6): "Z",
        # knee
        (12, 6): "Z", (12, 7): "u", (13, 7): "v",
        # thigh
        (9, 8): "Z", (9, 9): "Z", (10, 9): "x", (9, 10): "q", (10, 10): "Z", (11, 10): "x", (10, 11): "q",
        (11, 11): "Z", (12, 11): "x", (11, 12): "X",
    },
}


# ---- round 3 (owner 2026-11-17, see the top of this file) ----
# Drawn in the icon's own coordinates (not mirrored). A thigh, D lower leg (the same piece: no line at the knee), C and E
# a second piece or leg, b bone tip, g garlic, p and r potato slices. Every leg is about four times longer than it is
# wide: widest at the hip, tapering to a bent knee, then a lower leg two or three pixels thick to the bone tip.
LEGS3 = {
    # g: e's way round (bone top left, hip bottom right). The thigh lies low and long, the lower leg rises steeply from
    # the knee: an elongated Z. Potatoes bottom left.
    "g": [
        "................",
        "..bb............",
        "..bDD...........",
        "...DDD..........",
        "...DDD..........",
        "....DDD.........",
        "....DDDD........",
        ".....DDAAA......",
        ".....DAAAAAAA...",
        "...pp.AAAgAAAAA.",
        "..pppp.AAAAAAAAA",
        "..rrrr...AAAAAAA",
        "...rr..g...AAAA.",
        "................",
        "................",
        "................",
    ],
    # h: the long diagonal the other way, hip bottom left, the bone past the plate's top right; potatoes on the right
    "h": [
        "................",
        ".............bb.",
        "............Dbb.",
        "...........DDD..",
        "..........DDD...",
        "...g.....DDDD...",
        "........DDDD....",
        ".......AADD.....",
        ".....AAAAAAD.pp.",
        "...AAAAgAAAApppp",
        ".AAAAAAAAAA.rrrr",
        "AAAAAAAAAA...rr.",
        "AAAgAAAA........",
        ".AAAA...........",
        "................",
        "................",
    ],
    # i: a shallow boomerang across the plate, hip on the left, the knee low in the middle, the foot rising past the
    # right rim; potatoes in a row in front
    "i": [
        "................",
        "................",
        "................",
        ".AAA............",
        ".AAAAA.......bbb",
        ".AAgAAAA....DDb.",
        ".AAAAAAAA.DDDD..",
        "..AAAAAAAADDD...",
        "....AAAAAADD....",
        "....pp.AAA.pp...",
        "...pppp...pppp..",
        "...rrrr.g.rrrr..",
        "....rr.....rr...",
        "................",
        "................",
        "................",
    ],
    # j: a leg along the top and the saddle (loin) piece in front; potatoes on the right
    "j": [
        "................",
        "................",
        ".AAA............",
        "AAAAAA.......bb.",
        "AAgAAAAA...DDbb.",
        ".AAAAAAADDDDD...",
        "...AAAAADDD.....",
        "............pp..",
        "..CCCCCCCC.pppp.",
        ".CCCCCCCCCCrrrr.",
        ".CCgCCCCCCC.rr..",
        "..CCCCCCCC......",
        "................",
        "................",
        "................",
        "................",
    ],
    # k: a pair of hind legs side by side, as they are sold, both bones past the top right
    "k": [
        "................",
        "............bb..",
        "...........Dbb..",
        "..........DDD...",
        ".........DDD.bb.",
        "......AAADDDDbb.",
        ".....AAAAAAEEE..",
        "...AAAgAAAEEE...",
        "..AAAAAACCEE....",
        ".AAAACCCCCC..pp.",
        ".AAACCCgCCC.pppp",
        "...CCCCCCC..rrrr",
        "..CCCCCC.....rr.",
        "...CCCC.........",
        "................",
        "................",
    ],
}
# l: the critic's round 3 proposal, "g's proportions with i's knee": an L, the lower leg rising almost straight up from
# a clear knee, the long thigh lying along the front of the plate. l2: the same, with the knee's inside corner cut back
# to the plate for a sharper angle.
LEGS3["l"] = [
    "................",
    "..bb............",
    "..bDD...........",
    "...DD...........",
    "...DD...........",
    "...DDD..........",
    "....DD..........",
    "....DDA.....AA..",
    "....DAAAAAAAAAA.",
    "....AAAAAgAAAAA.",
    "..pp.AAAAAAAAAAA",
    ".pppp..AAAAAAAAA",
    ".rrrr....AAgAAA.",
    "..rr.g.....AA...",
    "................",
    "................",
]
LEGS3["l2"] = [r[:6] + "." + r[7:] if i == 7 else r for i, r in enumerate(LEGS3["l"])]
# Potatoes (critic, round 3): at most one dark pixel in three, only on the edges away from the light, the rest lit.
POTATOES_L = {(2, 10): "P", (3, 10): "P",
              (1, 11): "P", (2, 11): "Q", (3, 11): "Q", (4, 11): "S",
              (1, 12): "P", (2, 12): "P", (3, 12): "Q", (4, 12): "S",
              (2, 13): "S", (3, 13): "S"}
# a crease at the inside of the knee; g's potatoes lightened by the same rule
FINISH3 = {"g": {(7, 7): "z", (3, 10): "P", (4, 10): "Q", (2, 11): "Q"}, "h": {(8, 7): "z"}, "k": {(9, 5): "z"},
           "l": POTATOES_L, "l2": POTATOES_L}


def paint_legs(parts, seed):
    """Round 3 shading: each column of a piece is lit on top and in shade below (light from the top left), so a thin
    lower leg reads as a round, glossy limb rather than a dark line. A and D are one piece, C and E another."""
    g = [list(r) for r in parts]

    def at(x, y):
        return g[y][x] if 0 <= x < 16 and 0 <= y < 16 else "."

    def piece(c):
        return ("A", "D", "g") if c in "AD" else ("C", "E", "g")

    out = [["."] * 16 for _ in range(16)]
    for x in range(16):
        y = 0
        while y < 16:
            c = g[y][x]
            if c == ".":
                y += 1
                continue
            if c in "pr":    # fried potato slices, as in paint()
                if at(x + 1, y) != c or at(x, y + 1) != c:
                    out[y][x] = "S"
                elif at(x - 1, y) != c or at(x, y - 1) != c:
                    out[y][x] = "P"
                else:
                    out[y][x] = "Q"
                y += 1
                continue
            if c == "b":     # bone tip: pale, its underside in shade
                out[y][x] = "n" if at(x, y - 1) == "b" else "N"
                y += 1
                continue
            P = piece("A" if c == "g" else c)
            t = y
            while y < 16 and g[y][x] in P:
                y += 1
            n = y - t
            for i in range(n):
                yy = t + i
                if g[yy][x] == "g":
                    out[yy][x] = "G"
                    continue
                if i == n - 1:
                    ch = "Z"
                elif i == 0:
                    ch = "u" if fish.hash01(x, yy, seed) > 0.6 else "v"
                elif i == n - 2 and n >= 4:
                    ch = "z"
                elif i == 1 and n >= 4:
                    ch = "v"
                else:
                    ch = "j" if fish.hash01(x, yy, seed) > 0.85 else "x"
                if yy > 0 and g[yy - 1][x] == "g" and ch in "uvx":
                    ch = "H"     # the garlic's shadow
                out[yy][x] = ch
    return out


def neighbours(x, y):
    return ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))


def paint(parts, seed, low_potatoes=False):
    """Shade the parts into palette letters (a 16x16 grid, "." where the plate shows through)."""
    g = [list(r) for r in parts]

    def at(x, y):
        return g[y][x] if 0 <= x < 16 and 0 <= y < 16 else "."

    out = [["."] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            c = g[y][x]
            if c == ".":
                continue
            if c == "b":     # bone: pale, its lower-right side in shade
                out[y][x] = "n" if at(x + 1, y) != "b" and at(x, y + 1) != "b" else "N"
                continue
            if c == "g":     # garlic chunk: one pale pixel
                out[y][x] = "G"
                continue
            if c in "pr":    # fried potato slices (p and r: two slices, so they keep an edge between them)
                if at(x + 1, y) != c or at(x, y + 1) != c:
                    out[y][x] = "S"
                elif at(x - 1, y) != c or at(x, y - 1) != c:
                    out[y][x] = "P"
                else:
                    out[y][x] = "Q" if low_potatoes or at(x + 2, y) != c or at(x, y + 2) != c else "P"
                continue
            # a rabbit piece: garlic sits on top, so it counts as the same piece for the edges
            same = lambda a, b: at(a, b) in (c, "g")  # noqa: E731
            away = not same(x + 1, y) or not same(x, y + 1)       # an edge facing the bottom right
            lit = not same(x - 1, y) or not same(x, y - 1)        # an edge facing the top left
            if away:
                out[y][x] = "Z"
            elif lit:
                out[y][x] = "x" if (at(x - 1, y) in "ABCD" or at(x, y - 1) in "ABCD") else "v"
            else:
                up, lf = same(x, y - 2), same(x - 2, y)
                if not up or not lf:
                    out[y][x] = "u" if (x + y) % 3 == 0 else "v"     # just inside the lit edge: glossy
                elif not same(x + 2, y) or not same(x, y + 2):
                    out[y][x] = "x"
                else:
                    out[y][x] = "v"
                h = fish.hash01(x, y, seed)
                if h > 0.90 and out[y][x] in "vx":
                    out[y][x] = "j"
    # garlic shade: a chunk's lower-right neighbour on the meat takes the dark edge, so the chunk stands up
    for y in range(16):
        for x in range(16):
            if g[y][x] == "g" and 0 <= y + 1 < 16 and g[y + 1][x] in "ABCD":
                out[y + 1][x] = "H" if out[y + 1][x] in "uv" else out[y + 1][x]
    return out


def plate():
    """The lampuka moqlija's plate, its outline a step darker on the side away from the light (the vanilla outline
    is about 0.6 of the inside's brightness; the white plate's own grey outline is too light for that)."""
    g = fish.plate(8.3, 7.5, 7.4, 6.4)
    for y in range(16):
        for x in range(16):
            if g[y][x] == "R":
                s = (x - 8.3) + (y - 7.5)
                g[y][x] = "X" if s > 2 else "V"
    return g


def fenek_moqli(kind):
    plate_ = plate()
    if kind == "a":
        g = fish.lay(plate_, paint(PARTS_A, 5))
    elif kind == "b":
        g = fish.lay(plate_, paint(PARTS_B, 7))
    elif kind == "c":
        g = fish.lay(plate_, paint(PARTS_C, 11))
    elif kind in ON_PLATE:
        return on_plate(kind)
    elif kind in LEGS3:
        g = fish.lay(plate_, paint_legs(LEGS3[kind], 7))
        for (x, y), c in FINISH3.get(kind, {}).items():
            g[y][x] = c
    else:
        g = fish.lay(plate_, paint(fish.shift([r[::-1] for r in LEGS[kind]], 1, 0), 7, low_potatoes=True))
        for (x, y), c in FINISH.get(kind, {}).items():
            g[y][x] = c
    return ["".join(r) for r in g]


# ---- e on the plate (owner 2026-11-17: "the protatoes arent even on the plate and same with that tiny piece of
# rabbit") ----
# e's leg, pixel for pixel, with the potatoes and the small piece moved inside the plate's rim. In the icon's own
# coordinates: C the small piece, g garlic on it, p and r the two potato slices (r in front).
ON_PLATE = {
    # e3: the potatoes tucked in front of the leg, the small piece on the left
    "e3": [
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "....CC..........",
        "...CgCC.........",
        "...CCCC..pppp...",
        "....CC.rrrrpp...",
        ".......rrrr.....",
        "................",
        "................",
        "................",
        "................",
    ],
    # e4: the potatoes on the free left side, the small piece under the leg
    "e4": [
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "...ppp..........",
        "..pppp..........",
        "...rrrr.CCCC....",
        "....rrrCCgCC....",
        ".......CCCC.....",
        "................",
        "................",
        "................",
        "................",
    ],
}


def golden(g, parts):
    """The fried potato slices: at most one dark pixel in three, only on the edges away from the light (lower edges
    first, from the bottom right), the rest lit (P on the top and left edges, Q inside)."""
    cells = [(x, y) for y in range(16) for x in range(16) if parts[y][x] in "pr"]

    def at(x, y):
        return parts[y][x] if 0 <= x < 16 and 0 <= y < 16 else "."

    low = sorted([(x, y) for x, y in cells if at(x, y + 1) != parts[y][x]], key=lambda c: (-c[0] - c[1], -c[0]))
    right = sorted([(x, y) for x, y in cells if at(x + 1, y) != parts[y][x] and (x, y) not in low],
                   key=lambda c: (-c[0] - c[1], -c[0]))
    dark = set((low + right)[:len(cells) // 3])
    for x, y in cells:
        c = parts[y][x]
        if (x, y) in dark:
            g[y][x] = "S"
        elif at(x - 1, y) != c or at(x, y - 1) != c:
            g[y][x] = "P"
        else:
            g[y][x] = "Q"


def on_plate(kind):
    e = fenek_moqli("e")
    leg = fish.shift([r[::-1] for r in LEGS["e"]], 1, 0)
    g = [list(r) for r in plate()]
    for y in range(16):
        for x in range(16):
            if leg[y][x] in "ADbg" and not (leg[y][x] == "g" and leg[y + 1][x] == "C"):
                g[y][x] = e[y][x]
    parts = ON_PLATE[kind]
    piece = paint(["".join(c if c in "Cg" else "." for c in r) for r in parts], 7)
    g = fish.lay(g, piece)
    golden(g, parts)
    return ["".join(r) for r in g]


# ---- output ----
HOTBAR = [("rabbit", "v", "rabbit"), ("cooked rabbit", "v", "cooked_rabbit"), ("cooked chicken", "v", "cooked_chicken"),
          ("cooked porkchop", "v", "cooked_porkchop"), ("lampuka moqlija", "m", "lampuka_moqlija"),
          ("stuffat tal-fenek", "m", "stuffat_fenek"), ("rabbit stew", "v", "rabbit_stew"),
          ("baked potato", "v", "baked_potato")]


def ensure():
    os.makedirs(OUT, exist_ok=True)
    made = {}
    for k in KINDS:
        rows = fenek_moqli(k)
        check(f"fenek_moqli_{k}", rows)
        im = render(rows, PAL)
        im.save(os.path.join(OUT, f"fenek_moqli_{k}.png"))
        made[k] = im
    made[PICK].save(os.path.join(ITEMS, "fenek_moqli.png"))
    return made


def compare(made):
    font = label_font(14)
    items = [(f"fenek moqli {k}", made[k]) for k in SHOW]
    for n, src, f in HOTBAR:
        folder = VANILLA if src == "v" else ITEMS
        items.append((n, Image.open(os.path.join(folder, f + ".png")).convert("RGBA")))
    cols = 6
    cell, ch = 8 * 16 + 70, 8 * 16 + 40
    nrows = (len(items) + cols - 1) // cols
    hot = sorted(glob.glob(os.path.join(OUT, "ingame_fenek_moqli", "*crop*.png")))
    hot_im = Image.open(hot[0]).convert("RGBA") if hot else None
    W = max(cell * cols + 20, (hot_im.width + 20) if hot_im else 0)
    H = nrows * ch + 20 + 30 + 40 + ((hot_im.height + 30) if hot_im else 0)
    sheet = Image.new("RGBA", (W, H), (139, 139, 139, 255))
    d = ImageDraw.Draw(sheet)
    for i, (n, im) in enumerate(items):
        x0, y0 = 10 + (i % cols) * cell, 10 + (i // cols) * ch
        sheet.alpha_composite(im.resize((128, 128), Image.NEAREST), (x0, y0))
        sheet.alpha_composite(im, (x0 + 136, y0))
        sheet.alpha_composite(im.resize((32, 32), Image.NEAREST), (x0 + 136, y0 + 24))
        d.text((x0, y0 + 130), n, fill=(255, 255, 255, 255), font=font)
    # a 1x and a 2x row in hotbar order (the picked candidate in the third slot, as in game)
    y = 10 + nrows * ch
    n = len(SHOW)
    order = items[n:n + 2] + [items[SHOW.index(PICK)]] + items[n + 2:]
    d.text((10, y), f"hotbar order, 1x and 2x (pick {PICK})", fill=(255, 255, 255, 255), font=font)
    for i, (_, im) in enumerate(order):
        sheet.alpha_composite(im, (10 + i * 20, y + 20))
        sheet.alpha_composite(im.resize((32, 32), Image.NEAREST), (200 + i * 36, y + 20))
    y += 70
    if hot_im:
        d.text((10, y), "in game (hotbar): " + os.path.basename(hot[0]), fill=(255, 255, 255, 255), font=font)
        sheet.alpha_composite(hot_im, (10, y + 22))
    sheet.convert("RGB").save(os.path.join(OUT, "fenek_moqli_compare.png"))


def legs_1x(made):
    """A quick read: the candidates beside e, cooked rabbit, the lampuka moqlija and cooked chicken, at 1x and 3x."""
    font = label_font(14)
    items = [(k, made[k]) for k in SHOW]
    items += [("rabbit", Image.open(os.path.join(VANILLA, "cooked_rabbit.png")).convert("RGBA")),
              ("lampuka", Image.open(os.path.join(ITEMS, "lampuka_moqlija.png")).convert("RGBA")),
              ("chicken", Image.open(os.path.join(VANILLA, "cooked_chicken.png")).convert("RGBA"))]
    step = 3 * 16 + 14
    sheet = Image.new("RGBA", (20 + step * len(items), 10 + 24 + 10 + 48 + 26), (139, 139, 139, 255))
    d = ImageDraw.Draw(sheet)
    for i, (n, im) in enumerate(items):
        x0 = 10 + i * step
        sheet.alpha_composite(im, (x0, 10))
        sheet.alpha_composite(im.resize((48, 48), Image.NEAREST), (x0, 44))
        d.text((x0, 96), n, fill=(255, 255, 255, 255), font=font)
    sheet.convert("RGB").save(os.path.join(OUT, "fenek_moqli_legs_1x.png"))


def e_onplate(made):
    """e before and after the move onto the plate, at 8x and 1x."""
    font = label_font(14)
    keys = ["e"] + list(ON_PLATE)
    sheet = Image.new("RGBA", (20 + 140 * len(keys), 10 + 128 + 8 + 16 + 8 + 22), (139, 139, 139, 255))
    d = ImageDraw.Draw(sheet)
    for i, k in enumerate(keys):
        x0 = 10 + 140 * i
        sheet.alpha_composite(made[k].resize((128, 128), Image.NEAREST), (x0, 10))
        sheet.alpha_composite(made[k], (x0, 146))
        d.text((x0 + 24, 144), "e (before)" if k == "e" else k, fill=(255, 255, 255, 255), font=font)
    sheet.convert("RGB").save(os.path.join(OUT, "fenek_moqli_e_onplate.png"))


def main():
    made = ensure()
    compare(made)
    legs_1x(made)
    e_onplate(made)
    for k, im in made.items():
        print(f"fenek_moqli_{k}", "vertical centre", round(fish.vcentre(im), 2))


if __name__ == "__main__":
    main()
