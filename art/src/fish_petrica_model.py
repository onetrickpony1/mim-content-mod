"""The petrica (anglerfish, Lophius piscatorius and L. budegassa) as a swimming mob: its 3D model and its texture.

Redo of 2026-11-19 (docs/Decisions/2026-11-19 Night fish models - nine pass, John Dory and petrica redo.md): the owner
found the night job's flat pancake "looks absolutely nothing like an anglerfish ... in the water it has a normal fish
shape". This version is drawn from the LIVE fish in aquariums (art/references/fish_petrica_refonly/: aq_angler, the
fish standing on its fins in a Norwegian aquarium, head on; aq_finisterrae1/2, resting on sand; drawing_budegassa, a
side view of a fresh L. budegassa) and keeps the old landed photos (norway, algeria, hal) for colour.
What makes it an anglerfish (the redo's 8th and last critic round, "FAIL (narrowly)"; see the night log):
  - a huge, broad head, 14 px wide and 8 deep, with 1 px bevels at its top and front edges, about half the fish;
  - a very wide straight mouth right across: one dark gape row above the lower jaw, which juts 2 px past the upper
    and is 1 px wider each side, with a pale lip edge and a few short, uneven pale teeth standing on its rim;
  - the body deep behind the head, then narrowing in 3 steps (10, 7, 4, 3 px wide) to a squared tail fin with a
    darker edge; a low soft second dorsal fin near the tail;
  - big pectoral fans on short arms at the sides, swept back and angled out and down;
  - the fishing rod (illicium) on the snout, one 1 px plane, with a ragged fleshy flap at its tip (no glow), and a
    shorter second spine behind it leaning back;
  - ragged skin flaps, light and dark, along the head's lower sides;
  - small dark eyes on top of the head near its edges, half sunk, each with a pale pixel beside and behind it;
  - mottled brown in 2 px blotches, paling to a cream belly (countershade).
On land (out of water) it lies flat on its belly: the renderer squashes it to LAND_SQUASH of its height (MimContentClient,
FishRenderer.withLandSquash; FishShape's flat row and the land hit boxes use the same squash), the landed, flattened look
the owner found close.

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): a plain FishModel, head toward -z, y 24 at
the ground, root children "body", "lure", "left_fin", "right_fin" and "tail_fin" (which sways). No body wiggle.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/PetricaModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/petrica.png   (128 x 64)
With --preview DIR it writes offline previews of every candidate paint (side, three-quarter, top, beside vanilla cod
and the cerna). With --candidate X it installs candidate X instead of the chosen one (for trying them in the game).

Run:  art/.venv/bin/python art/src/fish_petrica_model.py [--preview DIR] [--candidate A|B|C]
"""
import colorsys
import math
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import fish_cerna_model as CE  # noqa: E402  (the shared texel layout and the offline renderer)

RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "fish",
                    "PetricaModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "petrica.png")
TW, TH = 128, 64
CHOSEN = "A"


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


# Ramp 0 (pale belly) .. 5 (darkest back), then the features. Measured from the out-of-water photos (norway: back
# #634121 #7c5a3c #876146 #947a61; algeria: olive #85826c #948e79) before the lift for the water.
PALETTES = {
    # A: warm mottled brown, the landed Atlantic fish (norway). Round 1: stronger blotches, a paler belly and lip, a
    # darker gape, a gold-brown ring round the eye, a darker fringe.
    "A": {
        # given at their final values (LIFT 1.0). Round 2: warmer and more saturated; round 5: a third lighter, as
        # under water it still went near-black beside the cod; the darkest marks are only the eyes and the gape
        # round 7: the back's darker tones 10% darker again
        "0": "#d8c8aa", "1": "#c8a070", "2": "#b48a5a", "3": "#94704a", "4": "#7a5a3a", "5": "#604630",
        "B": "#5a3c28", "P": "#e0b878",        # blotches: dark brown, light ochre (round 5: more contrast)
        "e": "#d8c8a0", "E": "#0c0806",        # a pale rim beside and behind the eye (redo round 7), the eye
        "L": "#e0ccac", "M": "#1a120c",        # the pale lower lip, the gape
        "T": "#c8a070",                        # the fringe of skin flaps (round 5: pale brown)
        "F": "#a07a4c", "f": "#886440", "D": "#6e5034", "r": "#b48a5a",   # fins: membrane, shaded, rim, base
        "R": "#9c7850", "Q": "#b48a5a",        # the rod (lighter, round 5), the flap at its tip (skin colour)
    },
    # B: olive brown, the Mediterranean L. budegassa at the market (algeria)
    "B": {
        "0": "#c4bca4", "1": "#a49c80", "2": "#8e866a", "3": "#7a7256", "4": "#665e46", "5": "#544c38",
        "B": "#423a28", "P": "#a89a70",
        "e": "#a8904c", "E": "#100c08",
        "L": "#b0a688", "M": "#2a2418",
        "T": "#544c38",
        "F": "#787054", "f": "#645c44", "D": "#4a4432", "r": "#948c70",
        "R": "#5a5240", "Q": "#b0947c",
    },
    # C: A's brown with more and larger camouflage blotches
    "C": {
        "0": "#c4b296", "1": "#ac8a6a", "2": "#987656", "3": "#80603f", "4": "#684a30", "5": "#523824",
        "B": "#402a1c", "P": "#b08456",
        "e": "#a8844c", "E": "#100b08",
        "L": "#b08d6a", "M": "#2a1c14",
        "T": "#523824",
        "F": "#7a5b3e", "f": "#664a30", "D": "#4e3624", "r": "#97785a",
        "R": "#5e4430", "Q": "#b08a74",
    },
}
BLOTCH = {"A": (0.24, 0.14), "B": (0.18, 0.14), "C": (0.26, 0.18)}   # chance of a dark, of a pale 2 px blotch
LIFT = {"A": 1.0, "B": 1.3, "C": 1.3}   # A is given at its final colours (round 2)
CLEAR = (0, 0, 0, 0)

# --- the model -------------------------------------------------------------------------------------------------------
# Parts: name -> (parent, pivot (absolute model pixels), (xRot, yRot, zRot)). Cubes: (name, part, (U, V), (x0, y0, z0)
# absolute, (w, h, d)). Absolute: x across, y down (24 = ground), z head (-) to tail (+).
LAND_SQUASH = 0.45   # on land its height is squashed to this (the renderer and FishShape); the land check wants <= 7 px
PARTS = {
    "body": (None, (0.0, 20.0, 0.0), (0.0, 0.0, 0.0)),
    # the rod stands on the snout and leans a little forward, its flap above the mouth, not in front of it
    "lure": (None, (0.0, 18.0, -13.0), (0.2, 0.0, 0.0)),
    # the second spine behind it, a thin 1 px spike leaning back (redo round 2: upright, it read as a periscope)
    "spine2": (None, (0.0, 16.0, -10.0), (-0.6, 0.0, 0.0)),
    # the pectoral fins: a broad fan on a visible arm, swept back and angled out and down
    "left_fin": (None, (5.0, 20.0, -1.0), (0.0, 0.4, 0.45)),
    "right_fin": (None, (-5.0, 20.0, -1.0), (0.0, -0.4, -0.45)),
    "tail_fin": (None, (0.0, 21.5, 10.0), (0.0, 0.0, 0.0)),
}
SPECS = [
    # the head: one broad block 14 px wide and 8 deep with 1 px bevels at its top and front edges, so it is a low dome
    # and not stepped tiers (redo rounds 1 to 7: a cube, a crate, a ziggurat, a slab, a stepped box); the lower jaw
    # juts 2 px past it and is 1 px wider each side, with a dark gape between the jaws
    ("head", "body", (-7.0, 17.0, -13.0), (14, 7, 9)),
    ("cap", "body", (-6.0, 16.0, -12.0), (12, 1, 8)),
    ("head_front", "body", (-6.0, 18.0, -14.0), (12, 6, 1)),
    ("jaw", "body", (-8.0, 21.0, -16.0), (16, 3, 2)),
    # the lower teeth: short, uneven 1 px points standing up on the jaw's rim only
    ("teeth", "body", (-7.0, 20.0, -15.5), (14, 1, 0)),
    # the small eyes on top of the head near its edges, set back from the mouth, half sunk
    ("eye_l", "body", (4.0, 15.5, -8.0), (1, 1, 1)),
    ("eye_r", "body", (-5.0, 15.5, -8.0), (1, 1, 1)),
    # the body behind the head, deep, then tapering over 3 steps to a stalk a quarter of the head's width
    # (redo round 7: the whole fish 1.5 times deeper in the water): 10, 7, 4, 3 px wide and 7, 5, 4, 2 deep
    ("trunk", "body", (-5.0, 17.0, -4.0), (10, 7, 5)),
    ("mid", "body", (-3.5, 19.0, 1.0), (7, 5, 4)),
    ("rear", "body", (-2.0, 20.0, 5.0), (4, 4, 3)),
    ("stalk", "body", (-1.5, 21.0, 8.0), (3, 2, 2)),
    # the fringe of skin flaps: ragged 1 px tabs along the head's sides, light and dark, sticking out and hanging down
    ("fringe_l", "body", (7.0, 21.0, -13.0), (1, 0, 9)),
    ("fringe_r", "body", (-8.0, 21.0, -13.0), (1, 0, 9)),
    ("flap_l", "body", (7.5, 21.0, -14.0), (0, 3, 10)),
    ("flap_r", "body", (-7.5, 21.0, -14.0), (0, 3, 10)),
    # the second spine and the low soft second dorsal fin near the tail
    ("spine", "spine2", (0.0, 14.0, -10.5), (0, 2, 1)),
    ("dorsal", "body", (0.0, 17.0, 1.0), (0, 2, 5)),
    # the rod (illicium): one 1 px plane (redo round 7: a crossed plane faced the front as a horn), and a ragged
    # 2 x 2 fleshy flap at its tip (round 7: a block read as a mallet)
    ("rod", "lure", (0.0, 13.0, -13.5), (0, 5, 1)),
    ("esca", "lure", (0.0, 11.0, -14.5), (0, 2, 2)),
    # the pectoral fins: an arm and a broad fan
    ("arm_l", "left_fin", (4.0, 19.0, -2.0), (3, 2, 2)),
    ("arm_r", "right_fin", (-7.0, 19.0, -2.0), (3, 2, 2)),
    ("pec_l", "left_fin", (7.0, 20.0, -3.5), (6, 0, 5)),
    ("pec_r", "right_fin", (-13.0, 20.0, -3.5), (6, 0, 5)),
    # the squared tail fin, wider than the stalk, with a darker edge
    ("caudal", "tail_fin", (0.0, 19.0, 10.0), (0, 5, 4)),
]


def footprint(size):
    w, h, d = size
    if w == 0:
        return 2 * d, d + h
    if h == 0:
        return d + 2 * w, d
    if d == 0:
        return 2 * w, h
    return 2 * d + 2 * w, d + h


def used_corner(size, x, y):
    w, h, d = size
    if w == 0:
        return x, y + d
    if h == 0:
        return x + d, y
    return x, y


def pack(specs):
    """Shelf-pack every cube's used texture area into the 64 x 64 texture, biggest first."""
    order = sorted(specs, key=lambda s: (-footprint(s[3])[1], -footprint(s[3])[0], s[0]))
    uv, x, y, shelf = {}, 0, 0, 0
    for name, _, _, size in order:
        fw, fh = footprint(size)
        if x + fw > TW:
            x, y, shelf = 0, y + shelf + 1, 0
        uv[name] = used_corner(size, x, y)
        x += fw + 1
        shelf = max(shelf, fh)
    assert y + shelf <= TH
    return [(name, part, uv[name], pos, size) for name, part, pos, size in specs]


CUBES = pack(SPECS)

# --- painting ----------------------------------------------------------------------------------------------------------
# Fin outlines, one character per texel. Vertical planes along z (w 0): rows y from the top, columns z from the front.
# Vertical planes across (d 0): rows y from the top, columns x from the body outward.
CAUDAL = [        # rows y 19..24, columns z 10..14: a squared fan with a darker trailing edge
    "FrFD",
    "rFrD",
    "FfFD",
    "rFrD",
    "FrfD",
]
DORSAL = [        # rows y 17..19, columns z 1..6: a low soft fin
    ".fFf.",
    "fFFFf",
]
SPINE = ["2", "3"]   # in the head's own browns (redo round 5: dark, from above it read as a mouth line)
ESCA = [".T", "TQ"]   # the rod's ragged fleshy flap
PECTORAL = [      # rows z from the front, columns from the arm outward: a solid mid-brown blade with a darker fringe
    "FFFD..",         # of rays at its outer edge (round 4: pale, they read as blobs; round 5: a checker read as
    "FFFFD.",         # pinecones)
    "FFFFFD",
    "FFFFD.",
    "FFDD..",
]
TEETH = (0xe8, 0xe0, 0xd0, 255)
TEETH_X = (-6, -3, -2, 2, 5)                    # x of the lower teeth (irregular; redo round 6: even ones read as a ruler)
LIP = (0xc9, 0xa5, 0x8a, 255)                   # a dull pinkish tan (redo round 5: near-white read as a tray)


def lifted(c, k):
    h, s, v = colorsys.rgb_to_hsv(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
    r, g, b = colorsys.hsv_to_rgb(h, s, min(1.0, v * k))
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)), 255)


def ramp(pal, shade):
    return pal[str(max(0, min(5, shade)))]


def hash01(*vals):
    return CE.hash01(*vals)


EYES = ((4.5, -7.5), (-4.5, -7.5))   # the eyes (eye_l, eye_r)


def mottle(pal, cand, shade, x, z, salt=0):
    """2 and 3 px blotches, darker and lighter, over a soft one-step mottle."""
    dark, pale = BLOTCH[cand]
    r = hash01(41 + salt, int(math.floor((x + 8) / 2)), int(math.floor((z + 16) / 2)))
    r3 = hash01(45 + salt, int(math.floor((x + 9) / 3)), int(math.floor((z + 17) / 3)))
    if r < dark * 0.8:                             # 2 px blotches only (redo round 2: 3 px ones read as plates)
        return pal["B"]
    if r3 > 0.92 or r > 1 - pale:
        return pal["P"]
    m = hash01(43 + salt, int(math.floor(x * 2)), int(math.floor(z / 2)))
    return ramp(pal, shade + (1 if m < 0.22 else -1 if m > 0.8 else 0))


def near_eye(x, z, r):
    return any(abs(x - ex) < r and abs(z - ez) < r for ex, ez in EYES)


def top_colour(pal, cand, name, x, z):
    for ex, ez in EYES:
        if abs(x - ex) < 0.6 and abs(z - ez) < 0.6:
            return pal["E"]                            # under the raised eye
    for ex, ez in EYES:
        dx, dz = x - ex, z - ez
        if name in ("cap", "head") and ((abs(dz) < 0.6 and 0.4 < abs(dx) < 1.6 and dx * ex > 0) or
                                        (abs(dx) < 0.6 and 0.4 < dz < 1.6)):
            return pal["e"]                            # a pale rim: one pixel outside and one behind each eye
                                                       # (redo round 7: gold bars read as drawer handles)                                # a gold rim behind each eye, on top only (redo round 3: a
                                                       # full ring, seen from the front, made googly cartoon eyes)
    if name == "head_front":
        return ramp(pal, 2)                            # the bevel over the mouth
    shade = 3 if z < 7 else 4
    if name == "cap" and abs(x) < 2.6 and z < -5:
        return ramp(pal, 1 if hash01(53, int(math.floor(x / 2)), int(math.floor(z / 2))) > 0.6 else 2)
                                                   # between the eyes only light marks (a dark blotch there read as
                                                   # a nose, redo round 2)
    if near_eye(x, z, 2.6) or z < -12:
        return ramp(pal, shade - (1 if z < -12 else 0))   # plain next to the eyes and over the snout (a dark mark
                                                          # there reads as a nose or brows from the front)
    return mottle(pal, cand, shade, x, z)


def side_colour(pal, cand, x, y, z):
    """Flanks: mottled brown at the top, paling down to the cream belly (countershade)."""
    yi = int(math.floor(y))
    if yi >= 23:
        return ramp(pal, 0)
    if yi >= 22:
        return ramp(pal, 1)
    if yi >= 21:
        return ramp(pal, 2 if hash01(57, int(math.floor(z / 2)), yi) < 0.7 else 1)   # the paler lower flank
    shade = 3 if yi <= 19 else 2
    return mottle(pal, cand, shade, yi * 1.0, z, 7)


def body_colour(pal, cand, name, face, x, y, z, cube):
    yi = int(math.floor(y))
    xi = int(math.floor(x))
    if name.startswith("eye"):
        return pal["E"] if face in ("top", "north", "east" if x > 0 else "west") else ramp(pal, 2)
    if face == "north" and name == "head_front":
        # the gape: one thin dark row right across, just above the jutting lower jaw; the upper lip above it
        return ramp(pal, 2) if yi < 20 else pal["M"]
    if face == "north" and name in ("head", "cap"):
        return ramp(pal, 2)
    if face == "north" and name == "jaw":
        if yi == 21:
            return LIP                                 # the pale lip edge only (redo round 6: a pale jaw read as a tray)
        if yi == 22 and xi in (-5, 0, 5):
            return pal["T"]                            # a few pale-brown skin flaps under the lip
        return ramp(pal, 3 if yi == 22 else 2)         # the jaw's brown body
    if face == "top" and name == "jaw":
        if abs(x) > 7:
            return ramp(pal, 3)                        # the jaw's sides, brown
        return LIP if z < -15 else pal["M"]            # the lip edge, and the near-black mouth slot

    if face == "top":
        return top_colour(pal, cand, name, x, z)
    if face == "bottom":
        return ramp(pal, 0)
    if name.startswith("arm"):
        return ramp(pal, 2)
    return side_colour(pal, cand, x, y, z)


def plane_colour(pal, name, cube, x, y, z):
    _, _, _, (x0, y0, z0), (w, h, d) = cube
    if name.startswith("fringe"):
        zi = int(math.floor(z))
        tabs = (-12, -10, -8, -6) if x > 0 else (-13, -11, -8, -5)   # 4 a side, light and dark
        if zi not in tabs:
            return CLEAR
        return pal["T"] if tabs.index(zi) % 2 == 0 else ramp(pal, 4)
    if name.startswith("flap"):
        zi, yi = int(math.floor(z)), int(math.floor(y))
        hang = {-13: 22, -11: 23, -10: 22, -8: 23, -6: 22, -5: 23} if x > 0 else {-14: 23, -12: 22, -9: 23, -8: 22, -6: 23}
        if zi in hang and yi >= hang[zi]:
            return pal["T"] if zi % 2 == 0 else ramp(pal, 4)
        return CLEAR
    if h == 0 and name.startswith("pec"):
        r = int(math.floor(z - z0))
        c = int(math.floor(x - x0)) if name.endswith("_l") else int(math.floor(x0 + w - x))
        ch = PECTORAL[r][c]
    else:
        if name == "teeth":
            return TEETH if int(math.floor(x)) in TEETH_X else CLEAR
        grid = {"caudal": CAUDAL, "dorsal": DORSAL, "esca": ESCA, "spine": SPINE}[name]
        r, c = int(math.floor(y - y0)), int(math.floor(z - z0))
        ch = grid[r][c]
    return CLEAR if ch == "." else pal[ch]


def draw_texture(cand):
    pal = {k: (hexc(v) if k in ("E", "M") else lifted(hexc(v), LIFT[cand])) for k, v in PALETTES[cand].items()}
    img = Image.new("RGBA", (TW, TH), CLEAR)
    owner = {}
    for cube in CUBES:
        name, _, _, (x0, y0, z0), (w, h, d) = cube
        for face, u, v, x, y, z in CE.face_texels(cube):
            assert 0 <= u < TW and 0 <= v < TH, (name, face, u, v)
            assert owner.setdefault((u, v), name) == name, ("texture overlap", name, owner[(u, v)], u, v)
            if name in ("rod", "rod_x"):
                col = ramp(pal, 1)                 # a light rod: dark, it read as a nose from the front
            elif w == 0 or h == 0 or d == 0:
                col = plane_colour(pal, name, cube, x, y, z)
            else:
                col = body_colour(pal, cand, name, face, x, y, z, cube)
            img.putpixel((u, v), col)
    return img


# --- the Java model ---------------------------------------------------------------------------------------------------
def write_java():
    f = CE.f
    lines = []
    for part in ("body", "lure", "spine2", "left_fin", "right_fin", "tail_fin"):
        parent, (px, py, pz), rot = PARTS[part]
        builder = "CubeListBuilder.create()"
        for cube in [c for c in CUBES if c[1] == part]:
            name, _, _, (x0, y0, z0), (w, h, d) = cube
            u, v = CE.tex_offset(cube)
            builder += "\n            /* %s */ .texOffs(%d, %d).addBox(%s, %s, %s, %d.0F, %d.0F, %d.0F)" % (
                name, u, v, f(x0 - px), f(y0 - py), f(z0 - pz), w, h, d)
        if any(rot):
            pose = "PartPose.offsetAndRotation(%s, %s, %s, %s, %s, %s)" % (f(px), f(py), f(pz), f(rot[0]), f(rot[1]),
                                                                           f(rot[2]))
        else:
            pose = "PartPose.offset(%s, %s, %s)" % (f(px), f(py), f(pz))
        lines.append("        root.addOrReplaceChild(\"%s\", %s,\n            %s);" % (part, builder, pose))
    src = """package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The petrica (anglerfish): a huge, broad head about half the fish, with a very wide straight mouth, the lower jaw
 * jutting out and teeth along both jaws; small eyes on top; the fishing-rod lure leaning forward from the snout with a
 * dull flap at its tip and a second spine behind it; a fringe of skin flaps along the head; big fleshy pectoral fins on
 * arms reaching to the floor; the body tapering to a slim tail stalk and a squared tail fin that sways. Mottled brown
 * above, cream below. Head toward -z, the ground at y 24. No body wiggle; on land it lies flat on its belly, squashed
 * (FishRenderer.withLandSquash). Texture 128 x 64: textures/entity/fish/petrica.png. Made by
 * art/src/fish_petrica_model.py (don't edit by hand).
 */
public class PetricaModel extends FishModel {
    public PetricaModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
%s
        return LayerDefinition.create(mesh, %d, %d);
    }
}
""" % ("\n".join(lines), TW, TH)
    with open(JAVA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(src)


# --- offline previews -------------------------------------------------------------------------------------------------
def previews(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    cod = CE.vanilla_texture("cod")
    cerna_tex = Image.open(os.path.join(RES, "textures", "entity", "fish", "cerna.png")).convert("RGBA")
    rows = []
    for cand in sorted(PALETTES):
        tex = draw_texture(cand)
        views = [CE.render(CUBES, PARTS, tex, v, 12) for v in ("side", "three", "top")]
        rows.append(views)
        tex.resize((TW * 4, TH * 4), Image.NEAREST).save(os.path.join(out_dir, "petrica_%s_tex4.png" % cand))
    scale = [CE.render(CUBES, PARTS, draw_texture(CHOSEN), "top", 8)]
    if cod:
        scale.append(CE.render(CE.vanilla_cubes(CE.COD_CUBES), CE.COD_PARTS, cod, "top", 8))
    scale.append(CE.render(CE.CUBES, CE.PARTS, cerna_tex, "top", 8))
    W = max(sum(i.width for i in r) + 20 * len(r) for r in rows + [scale])
    H = sum(max(i.height for i in r) + 20 for r in rows + [scale])
    sheet = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    y = 0
    for r in rows + [scale]:
        x, hh = 10, max(i.height for i in r)
        for im in r:
            sheet.paste(im, (x, y + hh - im.height), im)
            x += im.width + 20
        y += hh + 20
    sheet.save(os.path.join(out_dir, "petrica_sheet.png"))


def main():
    args = sys.argv[1:]
    cand = args[args.index("--candidate") + 1] if "--candidate" in args else CHOSEN
    tex = draw_texture(cand)
    os.makedirs(os.path.dirname(TEXTURE), exist_ok=True)
    tex.save(TEXTURE)
    write_java()
    print("wrote candidate", cand, "to", os.path.relpath(TEXTURE, ROOT), "and", os.path.relpath(JAVA, ROOT))
    if "--preview" in args:
        out = args[args.index("--preview") + 1]
        previews(out)
        print("previews in", out)


if __name__ == "__main__":
    main()
