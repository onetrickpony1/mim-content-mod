"""Item textures for four Maltese bowl dishes (candidates only, 2026-11-17; NOT in the mod).

One shared terracotta bowl (the accepted borma's clay colours, textures/block/borma_side.png) so the four read as a set,
and clearly not vanilla's low dark wooden bowl: orange-red clay, deeper, a pale lip, a small foot.
Two bowl shapes: "a" deep (3/4 view), "b" a lower, wider dish with a cream glaze line on the lip (†: Maltese
earthenware is often glazed inside; unchecked).

Contents (references art/references/stuffat_1-2, aljotta_1, qarnit_1-2, bigilla_1; see SOURCES.tsv):
- Stuffat tal-fenek: dark red-brown tomato-and-wine sauce, rabbit pieces, potato, carrot, peas†.
- Aljotta: fish broth with garlic, herbs and tomato (en Wikipedia "Maltese cuisine"); the Commons photo shows an orange
  broth with pale fish chunks; rice, a lemon wedge and marjoram/mint†.
- Stuffat tal-qarnit: octopus stewed in a dark red sauce; the Commons photos show curled pieces with suckers, green
  olives and capers.
- Bigilla: mashed tic beans (ful ta' Ġirba), olive oil, salt, red pepper, a dip (en Wikipedia "Bigilla"); the Commons
  photo shows a khaki-brown paste with parsley and chilli.

Run:  art/.venv/bin/python art/src/bowls.py
Writes art/candidates/{stuffat_fenek,aljotta,stuffat_qarnit,bigilla}_{a,b}.png and bowls_compare.png.
"""
import math
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import food_items as F  # noqa: E402

hx, render, outline3 = F.hx, F.render, F.outline3

PAL = {
    # terracotta bowl (borma family)
    "o": hx("#7e4028"), "O": hx("#62301c"), "H": hx("#d49a72"), "L": hx("#c27a52"), "l": hx("#b06a46"),
    "m": hx("#a0583a"), "d": hx("#874a33"), "D": hx("#6e3a26"), "g": hx("#efe0b8"),   # g: cream glaze line
    # stuffat tal-fenek
    "1": hx("#96452a"), "2": hx("#7a3420"), "3": hx("#5a2414"),                       # sauce lit / mid / dark
    "r": hx("#a97650"), "R": hx("#7e5434"),                                          # rabbit
    "p": hx("#ecd08a"), "P": hx("#c9a35a"),                                          # potato
    "c": hx("#d9762a"), "e": hx("#6f9a3a"),                                          # carrot, pea
    # aljotta
    "4": hx("#eba25c"), "5": hx("#dc8838"), "6": hx("#bf6a28"),                       # broth
    "f": hx("#f3ede0"), "F": hx("#d5cbb8"), "i": hx("#fbf7ea"),                      # fish, fish shade, rice
    "y": hx("#f4de4c"), "Y": hx("#d4b02a"), "h": hx("#5f8a3a"),                      # lemon, rind, herb
    # stuffat tal-qarnit
    "7": hx("#a83a26"), "8": hx("#8a2a1c"), "9": hx("#661c12"),                       # sauce
    "q": hx("#bc6a84"), "Q": hx("#8a4058"), "s": hx("#f0c4cc"),                      # octopus, shade, suckers
    "v": hx("#8a9a40"), "V": hx("#5a6624"), "k": hx("#4e5e26"),                      # green olive, its shade, caper
    # bigilla
    "a": hx("#ab9a6c"), "b": hx("#8c7c52"), "B": hx("#6c5e3c"),                       # khaki paste lit / mid / shade
    "j": hx("#cdb848"), "x": hx("#c8402a"), "z": hx("#4f8a3a"),                      # oil, chilli, parsley
    "t": hx("#e2c088"), "T": hx("#b48c52"),                                          # galletta
}


def blank():
    return [["."] * 16 for _ in range(16)]


def E(px, py, cx, cy, rx, ry):
    return ((px - cx) / rx) ** 2 + ((py - cy) / ry) ** 2 <= 1


# The shared bowls, drawn by hand; '?' marks the contents' surface. a: deep, 3/4 view, small foot.
BOWL_A = [
    "................",
    "................",
    "....oooooooo....",
    "..ooHHHHLLLLOO..",
    ".oHH????????LLO.",
    ".oH??????????LO.",
    ".oL??????????lO.",
    ".OLL????????llO.",
    "..OLLLLLllllOO..",
    "..OlllllmmmddO..",
    "...OllmmmmddO...",
    "....OlmmmddO....",
    ".....ODDDDO.....",
    "......OOOO......",
    "................",
    "................",
]
# b: lower and wider, a cream glaze line inside the lip (†), a wider foot.
BOWL_B = [
    "................",
    "................",
    "................",
    "....oooooooo....",
    "..ooggggggggOO..",
    ".oHg????????gLO.",
    ".oH??????????LO.",
    ".oL??????????lO.",
    ".OLg????????glO.",
    ".OLLLLLlllllldO.",
    "..OOllllmmmdOO..",
    "....ODDDDDDO....",
    ".....OOOOOO.....",
    "................",
    "................",
    "................",
]


def bowl(kind):
    """The shared bowl. Returns (grid, zone) where zone[y][x] is True for the contents' surface."""
    rows = BOWL_A if kind == "a" else BOWL_B
    g = [list(r) for r in rows]
    zone = [[c == "?" for c in r] for r in rows]
    return g, zone


def fill(kind, base, pieces):
    """Contents: a surface coloured by 'base' (lit, mid, dark from the top left / inner shadow at the back), then the
    hand-placed pieces {(x, y): ch} (only on the surface)."""
    g, zone = bowl(kind)
    zs = [(x, y) for y in range(16) for x in range(16) if zone[y][x]]
    top = min(y for _, y in zs)
    for x, y in zs:
        back = y == top or not zone[y - 1][x]                 # the inner shadow under the back lip
        g[y][x] = base[2] if back else (base[0] if (x + y) % 5 == 0 and x < 9 else base[1])
    for (x, y), ch in pieces.items():
        if zone[y][x]:
            g[y][x] = ch
    return g


DY = {"a": 0, "b": 1}   # the b bowl's surface sits one row lower


def dish(kind, base, pieces, extra=None):
    """Contents in 'a' coordinates (surface rows 4-7), moved down for the b bowl; extra = pixels drawn over the
    bowl itself (a lemon wedge or a galletta on the rim), also in 'a' coordinates."""
    dy = DY[kind]
    g = fill(kind, base, {(x, y + dy): c for (x, y), c in pieces.items()})
    for (x, y), c in (extra or {}).items():
        g[y + dy][x] = c
    return g


FENEK = {(5, 5): "r", (6, 5): "r", (5, 6): "R", (6, 6): "R", (7, 4): "r", (9, 6): "p", (10, 6): "p", (10, 7): "P",
         (9, 7): "P", (8, 5): "e", (11, 5): "e", (4, 7): "e", (7, 7): "e", (10, 4): "p", (11, 4): "P"}
ALJOTTA = {(5, 5): "f", (6, 5): "f", (6, 6): "F", (9, 6): "f", (10, 6): "F", (8, 4): "f", (4, 6): "i", (7, 6): "i",
           (11, 6): "i", (8, 7): "i", (8, 5): "h", (5, 7): "h", (10, 5): "i"}
LEMON = {(11, 2): "Y", (12, 2): "y", (12, 3): "y", (13, 3): "Y", (11, 3): "y", (13, 4): "Y", (12, 4): "y"}
QARNIT = {(6, 4): "q", (7, 4): "q", (8, 4): "Q", (5, 5): "q", (8, 5): "s", (9, 5): "Q", (5, 6): "s", (6, 6): "q",
          (7, 6): "s", (8, 6): "Q", (10, 6): "v", (11, 6): "V", (11, 5): "v", (4, 6): "k", (10, 7): "k", (6, 7): "q"}
BIGILLA = {(4, 5): "B", (5, 4): "B", (6, 4): "B", (7, 4): "B", (10, 5): "B", (11, 6): "B", (6, 6): "B", (7, 6): "B",
           (8, 6): "B", (9, 6): "B", (6, 5): "j", (7, 5): "j", (8, 5): "j", (9, 4): "x", (5, 6): "z", (10, 7): "z",
           (11, 5): "z", (7, 7): "x", (4, 7): "z"}
GALLETTA = {(12, 1): "o", (13, 1): "o", (11, 2): "o", (12, 2): "t", (13, 2): "t", (14, 2): "O", (11, 3): "t",
            (12, 3): "t", (13, 3): "T", (14, 3): "O", (11, 4): "T", (12, 4): "t", (13, 4): "T", (14, 4): "O",
            (12, 5): "O", (13, 5): "O"}

CANDS = [(f"{n}_{k}", k, base, pieces, extra) for n, base, pieces, extra in (
    ("stuffat_fenek", "123", FENEK, None), ("aljotta", "456", ALJOTTA, LEMON),
    ("stuffat_qarnit", "789", QARNIT, None), ("bigilla", "abB", BIGILLA, None)) for k in "ab"]
CANDS = [(n, k, b, p, (GALLETTA if n == "bigilla_b" else e)) for n, k, b, p, e in CANDS]
LABELS = {"stuffat_fenek": "Stuffat tal-fenek", "aljotta": "Aljotta", "stuffat_qarnit": "Stuffat tal-qarnit",
          "bigilla": "Bigilla"}


# ---- Accepted (owner 2026-11-17), frozen and installed: fenek v2, aljotta v2, qarnit v3 ----
FENEK_ACCEPTED = [
    "................",
    "................",
    "................",
    "....oooooooo....",
    "..ooggggggggOO..",
    ".oHg333rR3nngLO.",
    ".oH31err2epp3LO.",
    ".oL1c2RR12PPelO.",
    ".OLu2221ec22GlO.",
    ".OLLLLLlllllldO.",
    "..OOllllmmmdOO..",
    "....ODDDDDDO....",
    ".....OOOOOO.....",
    "................",
    "................",
    "................",
]
ALJOTTA_ACCEPTED = [
    "................",
    "................",
    "................",
    "....oooooooYy...",
    "..oogggggggyyY..",
    ".oHg6h66f666yYO.",
    ".oH6hffhh5i56LO.",
    ".oL4i5Fi4fFi5lO.",
    ".OLu5h54i5h5GlO.",
    ".OLLLLLlllllldO.",
    "..OOllllmmmdOO..",
    "....ODDDDDDO....",
    ".....OOOOOO.....",
    "................",
    "................",
    "................",
]
QARNIT_ACCEPTED = [
    "................",
    "................",
    "................",
    "....oooooooo....",
    "..ooggggggggOO..",
    ".oHg9MMM9K99gLO.",
    ".oH9M9SMNepP9LO.",
    ".oLe8S8M78Ke8lO.",
    ".OLueNM78p88GlO.",
    ".OLLLLLlllllldO.",
    "..OOllllmmmdOO..",
    "....ODDDDDDO....",
    ".....OOOOOO.....",
    "................",
    "................",
    "................",
]
INSTALL = (("stuffat_fenek", FENEK_ACCEPTED), ("aljotta", ALJOTTA_ACCEPTED), ("stuffat_qarnit", QARNIT_ACCEPTED))


# ---- Bigilla v4 (owner: "remove the galletta") and galletti, a new item (owner: "make a separate food item for
# galletti (multiple should be in the food's icon)"). Galletti: small round flat Maltese water crackers, pale cream to
# golden, docking holes, toasted blisters (the owner's bigilla photos, art/references/bowls_owner/bigilla/). ----
def bigilla_v4():
    g = v2("AWX", {(4, 6): "X", (5, 5): "X", (10, 6): "X", (11, 7): "X", (5, 6): "J", (6, 6): "J", (7, 6): "J",
                   (8, 6): "z", (9, 6): "z", (8, 7): "z", (10, 7): "z", (6, 8): "z", (11, 6): "z", (5, 7): "z",
                   (9, 5): "x", (7, 8): "x", (9, 7): "x", (4, 8): "W", (10, 8): "W"})
    for (x, y), c in {(5, 6): "E", (6, 6): "J", (7, 6): "W", (6, 7): "E"}.items():
        g[y][x] = c
    return g


GAL = {"o": hx("#76562a"), "O": hx("#543c1a"), "h": hx("#faeecc"), "l": hx("#f0daa6"), "m": hx("#e0c288"),
       "d": hx("#c9a466"), "D": hx("#a98248"), "b": hx("#b8834a"), "k": hx("#6a4a22")}   # b toasted blister, k hole


def cracker(cx, cy, rx, ry, depth=0, holes=(), blisters=()):
    """One galletta: a flat round cracker lit from the top left, a thin side when depth > 0."""
    g = [["."] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            u, v = (x + .5 - cx) / rx, (y + .5 - cy) / ry
            if u * u + v * v <= 1:
                k = -0.55 * u - 0.55 * v
                g[y][x] = "h" if k > 0.45 else "l" if k > 0.0 else "m" if k > -0.45 else "d"
            elif depth and v > 0 and any(u * u + ((y + .5 - j - cy) / ry) ** 2 <= 1 for j in range(1, depth + 1)):
                g[y][x] = "D"
    g = outline3(g)
    g = [["o" if c == "#" and (x + y) < cx + cy else "O" if c == "#" else c for x, c in enumerate(r)]
         for y, r in enumerate(g)]
    for x, y in holes:
        if g[y][x] in "hlmd": g[y][x] = "k"
    for x, y in blisters:
        if g[y][x] in "hlmd": g[y][x] = "b"
    return g


def galletti_a():
    """Three galletti from above, overlapping like a fanned hand: round, pale, docking holes, toasted blisters."""
    back = cracker(5.2, 5.6, 4.6, 4.4, holes=[(4, 4), (6, 4), (4, 6), (6, 6)], blisters=[(3, 5)])
    mid = cracker(11.0, 6.4, 4.4, 4.2, holes=[(10, 5), (12, 5), (10, 7), (12, 7)], blisters=[(13, 6)])
    front = cracker(7.8, 10.6, 4.6, 4.2, holes=[(6, 10), (8, 9), (10, 10), (8, 11)], blisters=[(6, 12), (10, 12)])
    return over(over(back, mid), front)


def galletti_b():
    """A little stack of three seen at three-quarter (each a thin cracker on the one below, slightly offset)."""
    bot = cracker(8.8, 9.4, 6.4, 2.6, depth=1)
    mid = cracker(7.4, 7.2, 6.2, 2.5, depth=1)
    top = cracker(8.4, 4.8, 6.0, 2.6, depth=1, holes=[(6, 4), (8, 4), (10, 4), (7, 5), (9, 5), (11, 5), (5, 5)],
                  blisters=[(4, 4), (12, 5)])
    return over(over(bot, mid), top)


PAL.update({"C": hx("#5c3e4c"), "I": hx("#7c5a68")})   # bigilla v5: paste shade / mid, more purple (critic)


def bigilla_v5():
    return [[{"X": "C", "W": "I"}.get(c, c) for c in r] for r in bigilla_v4()]


GAL2 = {"o": hx("#6e4a22"), "O": hx("#5a3a1a"), "s": hx("#4a3418"), "h": hx("#f4e4bc"), "l": hx("#ead39c"),
        "t": hx("#d4a862"), "k": hx("#b8945a")}
DISC = [".#####.", "#######", "#######", "#######", "#######", "#######", ".#####."]
DISC_ROUND = ["..###..", ".#####.", "#######", "#######", "#######", ".#####.", "..###.."]   # alternative, rounder


def galletti_v2(disc=None):
    """Critic r1: three clean round discs (7x7, cut corners): back-left, back-right, front on top; a dark seam only
    where a disc lies over another; four mid-tan docking holes each; toasted lower-right edge; light top-left."""
    g = [["."] * 16 for _ in range(16)]
    for cx, cy in ((5, 5), (10, 5), (8, 10)):
        x0, y0 = cx - 3, cy - 3
        inside = {(x0 + i, y0 + j) for j, r in enumerate(disc or DISC) for i, c in enumerate(r) if c == "#"}
        new = {}
        for x, y in inside:
            edge = any((x + dx, y + dy) not in inside for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if edge:
                new[(x, y)] = "s" if g[y][x] != "." else ("O" if (x - cx) + (y - cy) > 0 else "o")
            else:
                inner_edge = any((x + dx, y + dy) not in inside for dx, dy in ((2, 0), (0, 2), (1, 1)))
                new[(x, y)] = "t" if inner_edge and (x - cx) + (y - cy) > 0 else ("h" if (x - cx) + (y - cy) < -1 else "l")
        for hx_, hy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            new[(cx + hx_, cy + hy)] = "k"
        for (x, y), c in new.items():
            g[y][x] = c
    return g


# Bigilla v6 (owner: "too purple, its more brown than purple"). Paste sampled from the owner's photos (medians
# #5d5249, #65554b, #7f715e; light/dark quartiles #47352b-#9a8773): a clearly brown one and one with a faint cool cast.
PAL.update({"<": hx("#9a7a5e"), "^": hx("#765a44"), ">": hx("#54402e"),     # v6a: lit, mid, shade
            "{": hx("#8e766a"), "~": hx("#6e5a50"), "}": hx("#4e3e38")})    # v6b


def bigilla_v6(variant):
    m = {"A": "<", "I": "^", "C": ">"} if variant == "a" else {"A": "{", "I": "~", "C": "}"}
    return [[m.get(c, c) for c in r] for r in bigilla_v5()]


GAL3 = dict(GAL2, o=hx("#8c6634"), O=hx("#482e14"), t=hx("#c08c44"), k=hx("#cca86c"))   # critic r3 colours


def galletti_v3():
    """The round version (critic's pick) in GAL3, moved down one row."""
    return [["."] * 16] + galletti_v2(DISC_ROUND)[:15]


def over(back, front):
    g = [r[:] for r in back]
    for y in range(16):
        for x in range(16):
            if front[y][x] != ".":
                g[y][x] = front[y][x]
    return g

# ---- Accepted (owner 2026-11-17), frozen and installed: bigilla v6b, galletti v3 ----
BIGILLA_ACCEPTED = [
    "................",
    "................",
    "................",
    "....oooooooo....",
    "..ooggggggggOO..",
    ".oHg}}}}}x}}gLO.",
    ".oH}}EJ~zz}z}LO.",
    ".oL{~zE~zxz}~lO.",
    ".OLu~~zx~~~~GlO.",
    ".OLLLLLlllllldO.",
    "..OOllllmmmdOO..",
    "....ODDDDDDO....",
    ".....OOOOOO.....",
    "................",
    "................",
    "................",
]
GALLETTI_ACCEPTED = [
    "................",
    "................",
    "................",
    "....ooo..ooo....",
    "...ohhloohhlo...",
    "..ohklkshklktO..",
    "..ohlllshllltO..",
    "..olklkslklktO..",
    "...otttsssttO...",
    "....OOshhlsO....",
    ".....ohklktO....",
    ".....ohllltO....",
    ".....olklktO....",
    "......otttO.....",
    ".......OOO......",
    "................",
]


def main():
    ims = []
    for name, kind, base, pieces, extra in CANDS:
        rows = ["".join(r) for r in dish(kind, base, pieces, extra)]
        F.check(name, rows)
        im = render(rows, PAL)
        im.save(os.path.join(F.OUT, name + ".png"))
        ims.append((LABELS[name[:-2]] + " " + kind, im))
    for v in ("bowl", "mushroom_stew", "rabbit_stew", "beetroot_soup"):
        ims.append(("vanilla " + v, Image.open(os.path.join(F.VANILLA, v + ".png")).convert("RGBA")))
    F.compare(ims).save(os.path.join(F.OUT, "bowls_compare.png"))
    main_v2()
    for item, rows in INSTALL:
        render(rows, PAL).save(os.path.join(F.MOD_ITEMS, item + ".png"))
    render(BIGILLA_ACCEPTED, PAL).save(os.path.join(F.MOD_ITEMS, "bigilla.png"))
    render(GALLETTI_ACCEPTED, GAL3).save(os.path.join(F.MOD_ITEMS, "galletti.png"))
    render(["".join(r) for r in bigilla_v4()], PAL).save(os.path.join(F.OUT, "bigilla_v4.png"))
    big = render(["".join(r) for r in bigilla_v5()], PAL)
    big.save(os.path.join(F.OUT, "bigilla_v5.png"))
    ims = [("Bigilla v5", big)]
    for n, make, pal in (("galletti_a", galletti_a, GAL), ("galletti_b", galletti_b, GAL), ("galletti_v2", galletti_v2, GAL2),
                         ("galletti_v2_round", lambda: galletti_v2(DISC_ROUND), GAL2)):
        rows = ["".join(r) for r in make()]
        F.check(n, rows)
        im = render(rows, pal)
        im.save(os.path.join(F.OUT, n + ".png"))
        if n.startswith("galletti_v2"):
            ims.append(("Galletti " + n[9:].replace("_", " "), im))
    for item, lbl in (("stuffat_fenek", "Stuffat tal-fenek"), ("aljotta", "Aljotta"), ("stuffat_qarnit", "Stuffat tal-qarnit")):
        ims.append((lbl, Image.open(os.path.join(F.MOD_ITEMS, item + ".png")).convert("RGBA")))
    for v in ("cookie", "bread"):
        ims.append(("vanilla " + v, Image.open(os.path.join(F.VANILLA, v + ".png")).convert("RGBA")))
    F.compare(ims).save(os.path.join(F.OUT, "bigilla_galletti.png"))
    g3 = render(["".join(r) for r in galletti_v3()], GAL3)
    g3.save(os.path.join(F.OUT, "galletti_v3.png"))
    v6 = []
    for v in "ab":
        im = render(["".join(r) for r in bigilla_v6(v)], PAL)
        im.save(os.path.join(F.OUT, f"bigilla_v6{v}.png"))
        v6.append((f"Bigilla v6{v}", im))
    fin = v6 + [("Galletti v3", g3)] + [i for i in ims if not i[0].startswith(("Bigilla", "Galletti"))]
    F.compare(fin).save(os.path.join(F.OUT, "bigilla_galletti_final.png"))
    print("wrote", len(CANDS), "bowl candidates, bowls_compare.png, the v2 set and bowls_final.png")


# ---- v2 (critic round 1 + the owner's photos art/references/bowls_owner/, which override the Commons ones) ----
# All four in bowl b. Owner's photos: fenek in a terracotta dish, red-brown sauce, rabbit, potato, carrot, peas, bay;
# aljotta orange-red broth, white fish, rice, lots of parsley, lemon; qarnit dark red sauce, dark red-purple curled
# tentacles with suckers, potato, peas, black olives; bigilla a purple-brown/grey-brown bean paste (not the critic's
# pinkish-brown), olive oil, plenty of parsley and red chilli, galletti.
PAL.update({"G": hx("#c9b08a"), "u": hx("#d8c49a"),                       # glaze line in shade (critic)
            "n": hx("#4a6a30"),                                           # bay leaf
            "M": hx("#8e2e40"), "N": hx("#5e1a28"), "S": hx("#e2aab0"),   # octopus as in the owner's photos
            "K": hx("#2b2622"),                                           # black olive
            "A": hx("#8a6c66"), "W": hx("#6e5250"), "X": hx("#503c3a"),   # bigilla paste: lit, mid, shade
            "J": hx("#d6b04a")})                                          # olive oil


def v2(base, pieces, extra=None):
    g = fill("b", base, pieces)
    for (x, y), c in (extra or {}).items():
        g[y][x] = c
    g[8][12], g[8][3] = "G", "u"
    return g


def stuffat_fenek_v2():
    return v2("123", {(7, 5): "r", (8, 5): "R", (6, 6): "r", (7, 6): "r", (6, 7): "R", (7, 7): "R", (10, 6): "p",
                      (11, 6): "p", (10, 7): "P", (11, 7): "P", (4, 7): "c", (9, 8): "c", (5, 6): "e", (9, 6): "e",
                      (8, 8): "e", (12, 7): "e", (10, 5): "n", (11, 5): "n"})


def aljotta_v2():
    p = {(x, y + 1): c for (x, y), c in ALJOTTA.items()}
    p.update({(5, 5): "h", (10, 8): "h", (7, 6): "h", (4, 6): "h"})
    return v2("456", p, {(x, y + 1): c for (x, y), c in LEMON.items()})


def stuffat_qarnit_v2():
    """A curled tentacle (a C round a dark centre, pale suckers on its inner side), potato, peas, black olives."""
    return v2("789", {(5, 7): "M", (5, 6): "M", (6, 5): "M", (7, 5): "M", (8, 6): "N", (7, 7): "N", (6, 7): "S",
                      (6, 6): "S", (7, 6): "9", (10, 6): "p", (11, 6): "P", (9, 8): "p", (4, 8): "e", (11, 7): "e",
                      (9, 6): "e", (10, 7): "K", (9, 5): "K", (3, 7): "e"})


def bigilla_v2():
    return v2("AWX", {(4, 6): "X", (5, 5): "X", (10, 6): "X", (11, 7): "X", (5, 6): "J", (6, 6): "J", (7, 6): "J",
                      (8, 6): "z", (9, 6): "z", (8, 7): "z", (10, 7): "z", (6, 8): "z", (11, 6): "z", (5, 7): "z",
                      (9, 5): "x", (7, 8): "x", (9, 7): "x", (4, 8): "W", (10, 8): "W"},
              {**{(x, y + 1): c for (x, y), c in GALLETTA.items()}, (12, 6): "X", (13, 6): "L"})


PAL["E"] = hx("#b89a3e")   # oil, pooled darker


def bigilla_v3():
    """Critic r2: the oil as a pooled drizzle."""
    g = bigilla_v2()
    for (x, y), c in {(5, 6): "E", (6, 6): "J", (7, 6): "W", (6, 7): "E"}.items():
        g[y][x] = c
    return g


def stuffat_qarnit_v3():
    """Critic r2: the tentacle as a C-curl (outer arc, suckers on the inner curve, a dark curled tip)."""
    g = stuffat_qarnit_v2()
    for (x, y), c in {(5, 6): "9", (5, 7): "9", (6, 6): "8", (6, 7): "8", (5, 5): "9"}.items():
        g[y][x] = c
    for x, y in ((4, 6), (5, 5), (6, 5), (7, 6), (7, 7), (6, 8)):
        g[y][x] = "M"
    g[6][6] = g[7][5] = "S"
    g[8][5] = "N"
    return g


FINAL = (("stuffat_fenek_v2", "Stuffat tal-fenek v2"), ("aljotta_v2", "Aljotta v2"),
         ("stuffat_qarnit_v3", "Stuffat tal-qarnit v3"), ("bigilla_v3", "Bigilla v3"))


V2 = (("stuffat_fenek_v2", stuffat_fenek_v2), ("aljotta_v2", aljotta_v2), ("stuffat_qarnit_v2", stuffat_qarnit_v2),
      ("bigilla_v2", bigilla_v2), ("stuffat_qarnit_v3", stuffat_qarnit_v3), ("bigilla_v3", bigilla_v3))


def main_v2():
    made = {}
    for name, make in V2:
        rows = ["".join(r) for r in make()]
        F.check(name, rows)
        made[name] = render(rows, PAL)
        made[name].save(os.path.join(F.OUT, name + ".png"))
    ims = [(lbl, made[n]) for n, lbl in FINAL]
    for v in ("bowl", "mushroom_stew", "rabbit_stew", "beetroot_soup"):
        ims.append(("vanilla " + v, Image.open(os.path.join(F.VANILLA, v + ".png")).convert("RGBA")))
    F.compare(ims).save(os.path.join(F.OUT, "bowls_final.png"))


def show_zone(kind):
    g, zone = bowl(kind)
    return ["".join("#" if zone[y][x] else ("." if g[y][x] == "." else "+") for x in range(16)) for y in range(16)]


if __name__ == "__main__" and "--zones" in sys.argv:
    for k in "ab":
        print("\n".join(show_zone(k)))
        print()
    sys.exit()
if __name__ == "__main__":
    main()
