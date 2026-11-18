"""The boll (common stingray, Dasyatis pastinaca) as a swimming mob: its 3D model and its texture.

Drawn from the reference photos in art/references/fish_boll_refonly/ (list.tsv): sr20 (three landed rays from above,
for the disc's outline), sr27 and sr28 (rays on a beach, out of water, for the back's true colour), sr23 (the
underside out of water: cream, nostrils, mouth and gill slits), sr04, sr10 and sr30 (the whip tail against the disc),
sr22 and sr26 (swimming, the wings rippling). What makes it a common stingray:
  - a rhombic disc a little wider than long, 20 px wide and 16 long (1.25 x 1 blocks, bigger than life so it reads;
    owner 2026-11-18, "seemingly small"): a bluntly pointed snout (4 px wide at the tip),
    nearly straight front margins running back to rounded outer corners just behind the middle, then gently convex
    rear margins back to the tail root;
  - a gently domed middle: 2 px thick over the head and gut (12 px wide), tapering to 1 px over the outer wings;
  - small raised eyes on top of the dome (1 px bumps: a dark olive pupil on top, a light lid round them) with the
    spiracles just behind, so from above they read as eyes and never as the marks on the underside;
  - a smooth, plain olive-brown back with no spots, shaded from a lit dome and lit leading edges down to the darker
    rear margins and wing corners;
  - a cream underside (seen only from below while it swims, or when it tilts): the mouth a straight slit across,
    the two nostrils close in front of its ends joined by the nasal curtain (one closed bar, never a sad face), five
    gill slits a side (one soft line), shaded from the middle out to the rim;
  - small pelvic lobes beside the tail root;
  - a long thin whip tail, 26 px (1.6 x the disc's length), with a flat, pale spine lying on it about a third of the way along
    and no dorsal fin.
The palette is the owner-accepted icon's (art/src/fish_boll_icon_v5.py PAL, candidate C) lifted x1.15 in brightness
with the hue and saturation kept (house rule: x1.2 at most), and the accepted bucket's (N2) creams for the underside.
The ray lies belly down on the floor and on land, so the back carries most of the shading.

Parts (RayModel's contract, docs/Tools and Process/Art pipeline.md, "Fish models"): "body" (the middle 6 px of the
disc, the eyes, the pelvic lobes), "left_wing" / "right_wing" (the next 3 px), "left_wing_tip" / "right_wing_tip" (the next 2),
"left_wing_edge" / "right_wing_edge" (the outer 2 px, the rounded corners; the optional third ring RayModel ripples
last), "tail" (the whip, pivoted at the back of the disc) and "spine" (on the tail). Every wing ring hinges at the
middle of the 1 px plate, so no gap opens at the joints as the ripple runs out from the body.

Size: 42 px long in all (2.63 blocks), 20 wide (1.25 blocks), 2 thick over the dome (3 at the eyes).

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/BollModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/boll.png
With --sheet [SCREENSHOT_DIR] [OLD_DIR] it also writes the review sheet art/candidates/fish_boll_model.png and the
offline ripple frames art/candidates/fish_boll_model_ripple.png.

Run:  art/.venv/bin/python art/src/fish_boll_model.py [--sheet [SCREENSHOT_DIR [OLD_DIR]]]
"""
import colorsys
import glob
import math
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import fish_awrata_model as AW  # noqa: E402  (the shared model reader and texel walker)

RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA_DIR = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "fish")
JAVA = os.path.join(JAVA_DIR, "BollModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "boll.png")
TW, TH = 128, 128


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


def lift(c, v=1.15, s=1.0):
    """A step lighter for the water: brightness x1.15, hue kept (critic round 1 found x1.15 pale on sand, round 2
    found x1.05 a dark slab beside cod; x1.15 with a wider ramp, back_tone)."""
    h, sat, val = colorsys.rgb_to_hsv(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
    r, g, b = colorsys.hsv_to_rgb(h, min(1.0, sat * s), min(1.0, val * v))
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)), 255)


def mix(a, b, t):
    return tuple(int(round(a[i] * (1 - t) + b[i] * t)) for i in range(3)) + (255,)


# The accepted icon's colours (art/src/fish_boll_icon_v5.py PAL), the same keys, and two in-between tones.
ICON = {
    "L": "#b2a580",   # lit leading edges
    "H": "#a39570",   # the light on the dome
    "1": "#8a7d5c",   # olive-brown back, lit
    "2": "#706549",   # mid
    "3": "#574e39",   # shade
    "4": "#433c2d",   # deep shade: the eyes, the end of the whip
    "S": "#c4b794",   # the tail spine
}
# the olive-browns 1 2 3 a touch richer too (critic round 3: they greyed to mauve under water), hue kept
PAL = {k: lift(hexc(v), s=1.1 if k in "123" else 1.0) for k, v in ICON.items()}
PAL["h"] = mix(PAL["H"], PAL["1"], 0.5)     # between the dome light and the lit back
PAL["m"] = mix(PAL["1"], PAL["2"], 0.5)     # between the lit back and the mid
PAL["n"] = mix(PAL["2"], PAL["3"], 0.5)     # between the mid and the shade
PAL["S"] = mix(PAL["1"], PAL["m"], 0.5)      # the spine: a detail on the whip, not a pale band (critic round 2)
# The accepted bucket's creams (art/src/fish_boll_bucket.py, N2: W w s), not lifted (already light), and one deeper
# cream for the gill slits and the rim of the underside.
PAL["W"] = hexc("#f2e6c8")
PAL["w"] = hexc("#dccaa2")
PAL["s"] = hexc("#b9a27c")
PAL["g"] = hexc("#a08c68")
PAL["k"] = PAL["4"]                          # nostrils (the bucket's n, the icon's 4)
PAL["q"] = PAL["3"]                          # the mouth (the bucket's m, the icon's 3)
PAL["e"] = mix(PAL["3"], PAL["4"], 0.3)      # the eye's pupil, on top of the raised bump (a dark olive, not black)
PAL["p"] = PAL["n"]                          # the spiracle opening just behind it
PAL["x"] = mix(PAL["S"], PAL["3"], 0.45)     # the notches of the spine's serrations
PAL["."] = (0, 0, 0, 0)
CLEAR = PAL["."]
BACK_RAMP = ["L", "H", "h", "1", "m", "2", "n", "3", "4"]     # lightest to darkest
BELLY_RAMP = ["W", "w", "s", "g"]

# --- the disc ---------------------------------------------------------------------------------------------------------
# Column c covers x c..c+1 on the left (+x) and -c-1..-c on the right. FRONT/BACK: the disc's z extent (head at -z).
# (critic round 1: mixed 1-2 px runs, not an even staircase; a blunt 4 px snout). Owner 2026-11-18, "seemingly small":
# the disc is 1.25 blocks wide (20 px, 10 columns a side) and 16 long, bigger than life so it reads beside the other
# fish, the way the seahorse is.
NCOL = 10
FRONT = [-10, -10, -9, -8, -8, -7, -6, -5, -4, -2]
BACK = [6, 6, 6, 5, 5, 4, 4, 3, 2, 1]
SNOUT, DISC_LEN = FRONT[0], BACK[0] - FRONT[0]
# where the disc is 2 px thick (the dome over the head and gut), per column: (z0, z1); no 3 px ridge (round 1: a
# raised ridge and a thick tail root read as a tank's turret and gun)
DOME2 = {0: (-9, 5), 1: (-9, 5), 2: (-8, 4), 3: (-6, 3), 4: (-5, 2), 5: (-3, 1)}
DOME3 = {}
RING = {0: "body", 1: "body", 2: "body", 3: "wing", 4: "wing", 5: "wing", 6: "tip", 7: "tip", 8: "edge", 9: "edge"}
HINGE_X = {"wing": 3.0, "tip": 6.0, "edge": 8.0}
PLATE_MID = 23.5          # the wings hinge at the middle of the 1 px plate
# the eyes: raised 1 px bumps on the dome (owner 2026-11-18: the flat eye marks looked like the nostrils and mouth
# below), column 2 each side, with a lighter lid ring round each on the dome and the spiracle just behind
EYE_COL, EYE_Z, SPIRACLE_Z = 2, -6, -5
EYE_XI = (EYE_COL, -EYE_COL - 1)
TAIL_Z = 6.0
SPINE_Z = (15, 19)        # absolute z of the spine on the tail, about a third of the way along
TAIL_END = 32


def part_name(ring, side):
    if ring == "body":
        return "body"
    return "%s_%s" % (side, {"wing": "wing", "tip": "wing_tip", "edge": "wing_edge"}[ring])


# name -> (parent, pivot in absolute model px)
PARTS = {"body": (None, (0.0, PLATE_MID, 0.0))}
for side, sx in (("left", 1), ("right", -1)):
    prev = "body"
    for ring in ("wing", "tip", "edge"):
        n = part_name(ring, side)
        PARTS[n] = (prev, (sx * HINGE_X[ring], PLATE_MID, 0.0))
        prev = n
PARTS["tail"] = (None, (0.0, 23.5, TAIL_Z))
PARTS["spine"] = ("tail", (0.0, 23.0, float(SPINE_Z[0])))
SPINE_Y = 22.95          # the spine: a flat serrated barb lying on the whip (its top is at 23)
PART_ORDER = ["body", "left_wing", "left_wing_tip", "left_wing_edge", "right_wing", "right_wing_tip",
              "right_wing_edge", "tail", "spine"]


def part_abs(part):
    return PARTS[part][1]


def disc_cubes():
    """(name, kind, part, abs origin, size, info). kind 'disc' with info (column, layer)."""
    out = []
    for side, sx in (("left", 1), ("right", -1)):
        for c in range(NCOL):
            part = part_name(RING[c], side)
            x0 = c if sx > 0 else -c - 1
            layers = [(1, FRONT[c], BACK[c])]
            if c in DOME2:
                layers.append((2,) + DOME2[c])
            if c in DOME3:
                layers.append((3,) + DOME3[c])
            for layer, z0, z1 in layers:
                y0 = 24 - layer
                out.append(("%s_c%d_l%d" % (side[0], c, layer), "disc", part, (x0, y0, z0), (1, 1, z1 - z0),
                            (c, layer)))
    # pelvic lobes beside the tail root (not flapping: on the body)
    for sx, side in ((1, "l"), (-1, "r")):
        for (xa, z0, z1) in ((1, 6, 9), (2, 6, 8)):
            x0 = xa if sx > 0 else -xa - 1
            out.append(("%s_pelvic%d" % (side, xa), "pelvic", "body", (x0, 23, z0), (1, 1, z1 - z0), (xa, z0, z1)))
    # the eyes: 1 px bumps on the dome's top (y 22)
    for xi in EYE_XI:
        out.append(("eye_%s" % ("l" if xi > 0 else "r"), "eye", "body", (xi, 21, EYE_Z), (1, 1, 1), None))
    # the whip, lying on the floor: a 2 px wide root, then 1 x 1 to the end
    out.append(("tail_root", "tail", "tail", (-1, 23, TAIL_Z), (2, 1, 5), None))
    out.append(("whip", "tail", "tail", (-0.5, 23, TAIL_Z + 5), (1, 1, int(TAIL_END - TAIL_Z - 5)), None))
    # the spine: a flat barb lying on the whip, not a box (critic round 3; side teeth 1 px out read as a cross)
    out.append(("spine", "spine", "spine", (-0.5, SPINE_Y, SPINE_Z[0]), (1, 0, SPINE_Z[1] - SPINE_Z[0]), None))
    return out


def column_of(x):
    """The column index (0..NCOL-1) of a texel centre's absolute x."""
    return int(math.floor(abs(x)))


def shift(key, steps, ramp):
    i = max(0, min(len(ramp) - 1, ramp.index(key) + steps))
    return ramp[i]


def back_tone(c, z):
    """The back's tone at (x, z): light on the dome over the head, darkening out to the wing corners and back to the
    rear margins; the front margins lit (the light is from the front and above)."""
    zi = int(math.floor(z))
    f0, f1 = FRONT[c], BACK[c]
    r = (c + 0.5) / NCOL                                  # 0 at the middle, 1 at the wing corner
    along = (zi + 0.5 - SNOUT) / float(DISC_LEN)          # 0 at the snout, 1 at the rear of the disc
    v = 0.22 + 0.50 * r * r + 0.30 * max(0.0, along - 0.4) + 0.05 * along
    if c in DOME3 and DOME3[c][0] <= zi < DOME3[c][1]:
        v -= 0.14
    elif c in DOME2 and DOME2[c][0] <= zi < DOME2[c][1]:
        v -= 0.14
    idx = int(round(v * (len(BACK_RAMP) - 1)))
    key = BACK_RAMP[max(1, min(len(BACK_RAMP) - 1, idx))]
    if zi == f0:
        key = shift(key, -1, BACK_RAMP)                   # lit leading edge
    if zi == f1 - 1:
        key = shift(key, 1, BACK_RAMP)                    # the rear margin turns away
    return key


def belly_tone(x, z):
    c = column_of(x)
    zi = int(math.floor(z))
    f0, f1 = FRONT[c], BACK[c]
    xi = int(math.floor(x))
    # the features, as on a real ray's belly (sr23): the mouth a straight slit across, the two nostrils close in front
    # of its ends, joined by the nasal curtain between them, so the four make one closed bar (owner 2026-11-18: the
    # old nostrils over a narrower mouth read as a sad face); five gill slits a side, one soft line further back
    if zi == -8 and xi in (-2, 1):
        return "g"                                        # the nostrils
    if zi == -8 and xi in (-1, 0):
        return "s"                                        # the nasal curtain between them
    if zi == -7 and -2 <= xi <= 1:
        return "g"                                        # the mouth: straight, as wide as the nostrils, no corners
    if -4 <= zi <= 0 and c == 3:
        return "s"                                        # the gill slits a side, one soft line
    r = (c + 0.5) / NCOL
    if c == NCOL - 1 or zi == f1 - 1 or (zi == f0 and c >= 4):
        return "g" if c >= 7 else "s"                     # the rim (not round the snout: no frown outline)
    if r < 0.4:
        return "W"
    if r < 0.75:
        return "w"
    return "s"


def disc_key(cube, face, x, y, z):
    c, layer = cube[5]
    zi = int(math.floor(z))
    if face == "top":
        xi = int(math.floor(x))
        if layer == 2 and xi in EYE_XI and zi == SPIRACLE_Z:
            return "p"                                    # the spiracle, just behind the eye
        if layer == 2 and ((xi in EYE_XI and zi == EYE_Z - 1) or (abs(xi - EYE_XI[0]) == 1 or abs(xi - EYE_XI[1]) == 1)
                           and zi == EYE_Z and xi not in EYE_XI):
            return "L"                                    # the lighter lid ring round the eye
        key = back_tone(c, z)
        if c >= NCOL - 2 and (zi == FRONT[c] or zi == BACK[c] - 1 or c == NCOL - 1):
            key = shift(key, 1, BACK_RAMP)                # a 1 px darker rim round the wing corners (critic round 3)
        return key
    if face == "bottom":
        return belly_tone(x, z) if layer == 1 else "s"
    # the walls: the 1 px rim of the plate is the back's colour a step down (the back curls over the edge); the
    # dome's risers are lit at the front and shaded behind
    base = back_tone(c, z)
    if face == "south":
        return shift(base, 1, BACK_RAMP)
    if face == "north" and layer == 2:
        return shift(base, -1, BACK_RAMP)                 # the dome's front riser lit: no "mouth" line under the eyes
    return base


def eye_key(cube, face, x, y, z):
    """The raised eye: a darker pupil on top, a light lid round its sides."""
    return "e" if face == "top" else "H"


def pelvic_key(cube, face, x, y, z):
    if face == "bottom":
        return "w"
    if face == "top":
        return "n" if int(math.floor(z)) < 6 else "3"
    return "3"


def tail_key(cube, face, x, y, z):
    t = (z - TAIL_Z) / float(TAIL_END - TAIL_Z)     # 0 at the root, 1 at the tip
    top = "2" if t < 0.2 else ("n" if t < 0.5 else ("3" if t < 0.85 else "4"))
    if face == "top":
        return top
    if face == "bottom":
        return "s" if t < 0.3 else ("g" if t < 0.6 else "3")
    if face == "south":
        return "4"
    return shift(top, 1, BACK_RAMP)


def spine_key(cube, face, x, y, z):
    """The flat barb, seen from above (and below): pale, its point darker."""
    zi = int(math.floor(z)) - SPINE_Z[0]
    return "x" if zi == SPINE_Z[1] - SPINE_Z[0] - 1 else "S"


KEYS = {"eye": eye_key, "disc": disc_key, "pelvic": pelvic_key, "tail": tail_key, "spine": spine_key}


# --- texture layout --------------------------------------------------------------------------------------------------
def all_cubes():
    out = []
    for name, kind, part, (x0, y0, z0), size, info in disc_cubes():
        px, py, pz = part_abs(part)
        out.append((name, kind, part, (x0 - px, y0 - py, z0 - pz), size, info, (x0, y0, z0)))
    return out


def layout():
    cubes = all_cubes()
    rects = [(2 * c[4][2] + 2 * c[4][0], c[4][2] + c[4][1]) for c in cubes]
    order = sorted(range(len(cubes)), key=lambda k: (-rects[k][1], -rects[k][0], k))
    pos, x, y, shelf = [None] * len(cubes), 0, 0, 0
    for k in order:
        w, h = rects[k]
        if x + w > TW:
            x, y, shelf = 0, y + shelf, 0
        pos[k] = (x, y)
        x += w
        shelf = max(shelf, h)
    assert y + shelf <= TH, ("texture too small", y + shelf)
    return [(cubes[k], pos[k]) for k in range(len(cubes))]


def draw_texture():
    img = Image.new("RGBA", (TW, TH), CLEAR)
    owner = {}
    for cube, (u, v) in layout():
        name, kind, part, origin, size, info, absorg = cube
        px, py, pz = part_abs(part)
        for face, tu, tv, x, y, z in AW.face_texels(u, v, origin, size):
            assert owner.setdefault((tu, tv), name) == name, ("texture overlap", name, owner[(tu, tv)])
            key = KEYS[kind]((name, kind, part, origin, size, info), face, x + px, y + py, z + pz)
            img.putpixel((tu, tv), PAL[key])
    return img


# --- Java -------------------------------------------------------------------------------------------------------------
def f(v):
    s = ("%.4f" % v).rstrip("0")
    if s.endswith("."):
        s += "0"
    if s == "-0.0":
        s = "0.0"
    return s + "F"


def java_source():
    lines = [
        "package com.maltaminecraft.mimcontent.client.fish;",
        "",
        "import net.minecraft.client.model.geom.ModelPart;",
        "import net.minecraft.client.model.geom.PartPose;",
        "import net.minecraft.client.model.geom.builders.CubeListBuilder;",
        "import net.minecraft.client.model.geom.builders.LayerDefinition;",
        "import net.minecraft.client.model.geom.builders.MeshDefinition;",
        "import net.minecraft.client.model.geom.builders.PartDefinition;",
        "",
        "/**",
        " * The boll (common stingray): a rhombic disc 20 px wide and 16 long (1.25 blocks wide) with a bluntly pointed",
        " * snout and rounded outer corners, gently domed (2 px over the middle, 1 px at the wings), small raised eyes with",
        " * the spiracles behind them, pelvic lobes at the tail root and a 26 px whip tail with a flat pale spine. Plain",
        " * olive-brown back; cream underside with a straight mouth, the nostrils and nasal curtain, and the gill slits.",
        " * Made by art/src/fish_boll_model.py (do not edit by hand); texture textures/entity/fish/boll.png.",
        " * Extends RayModel, which animates it: each wing is three rings (left_wing, left_wing_tip, left_wing_edge),",
        " * each hinged at the middle of the plate, so the ripple runs out from the body to the rounded corners.",
        " */",
        "public class BollModel extends RayModel {",
        "    public BollModel(ModelPart root) {",
        "        super(root);",
        "    }",
        "",
        "    public static LayerDefinition createBodyLayer() {",
        "        MeshDefinition mesh = new MeshDefinition();",
        "        PartDefinition root = mesh.getRoot();",
    ]
    placed = layout()
    for part in PART_ORDER:
        parent, (ax, ay, az) = PARTS[part]
        if parent:
            bx, by, bz = part_abs(parent)
            ox, oy, oz = ax - bx, ay - by, az - bz
        else:
            ox, oy, oz = ax, ay, az
        builder = "CubeListBuilder.create()"
        for (name, _k, cpart, (x0, y0, z0), (w, h, d), _i, _a), (u, v) in placed:
            if cpart != part:
                continue
            builder += "\n            /* %s */ .texOffs(%d, %d).addBox(%s, %s, %s, %s, %s, %s)" % (
                name, u, v, f(x0), f(y0), f(z0), f(w), f(h), f(d))
        has_child = any(p[0] == part for p in PARTS.values())
        var = "PartDefinition %s = " % part if has_child else ""
        lines.append("        %s%s.addOrReplaceChild(\"%s\", %s," % (var, parent or "root", part, builder))
        lines.append("            PartPose.offset(%s, %s, %s));" % (f(ox), f(oy), f(oz)))
    lines += ["        return LayerDefinition.create(mesh, %d, %d);" % (TW, TH), "    }", "}", ""]
    return "\n".join(lines)


# --- checks -----------------------------------------------------------------------------------------------------------
def check_boxes():
    """No two boxes of the disc may overlap, and no two faces facing the same way may share a plane where they meet."""
    cubes = [(c[0], c[6], c[4]) for c in all_cubes()]
    probs = []
    for i in range(len(cubes)):
        a0 = cubes[i][1]
        a1 = tuple(a0[k] + cubes[i][2][k] for k in range(3))
        for j in range(i + 1, len(cubes)):
            b0 = cubes[j][1]
            b1 = tuple(b0[k] + cubes[j][2][k] for k in range(3))
            ov = [min(a1[k], b1[k]) - max(a0[k], b0[k]) for k in range(3)]
            if all(o > 1e-6 for o in ov):
                probs.append(("overlap", cubes[i][0], cubes[j][0]))
                continue
            for k in range(3):
                for side in (0, 1):
                    if abs((a0, a1)[side][k] - (b0, b1)[side][k]) > 1e-6:
                        continue
                    o = [ov[m] for m in range(3) if m != k]
                    if all(q > 1e-6 for q in o):
                        probs.append(("same plane", cubes[i][0], cubes[j][0], "xyz"[k]))
    return probs


# --- offline preview (any yaw and pitch; parts can be turned for the ripple frames) ---------------------------------
SHADE = {"top": 1.0, "bottom": 0.5, "north": 0.8, "south": 0.8, "west": 0.6, "east": 0.6}


def render(model, texture, yaw, pitch, scale, rots=None, sub=3, bg=None):
    parts, _ = model
    rots = rots or {}
    by_name = {p[0]: p for p in parts}

    def world(part, p):
        while part:
            _, parent, pivot, rot, _ = by_name[part]
            p = AW.rot_point(p, rots.get(part, rot))
            p = (p[0] + pivot[0], p[1] + pivot[1], p[2] + pivot[2])
            part = parent
        return p

    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))

    def project(p):
        x, y, z = p
        z2, x2 = z * cy + x * sy, -z * sy + x * cy
        return z2, y * cp - x2 * sp, y * sp + x2 * cp

    pts = []
    for name, _, _, _, cubes in parts:
        for u, v, origin, size in cubes:
            for face, tu, tv, x, y, z in AW.face_texels(u, v, origin, size):
                col = texture.getpixel((tu, tv))
                if col[3] < 128:
                    continue
                k = SHADE[face]
                col = (int(col[0] * k), int(col[1] * k), int(col[2] * k))
                for i in range(sub):
                    for j in range(sub):
                        a, b = (i + 0.5) / sub - 0.5, (j + 0.5) / sub - 0.5
                        if face in ("top", "bottom"):
                            p = (x + a, y, z + b)
                        elif face in ("west", "east"):
                            p = (x, y + a, z + b)
                        else:
                            p = (x + a, y + b, z)
                        pts.append((project(world(name, p)), col))
    xs = [q[0][0] for q in pts]
    ys = [q[0][1] for q in pts]
    minx, miny = min(xs) - 1, min(ys) - 1
    wpx = int((max(xs) - minx + 1) * scale) + 1
    hpx = int((max(ys) - miny + 1) * scale) + 1
    img = Image.new("RGBA", (wpx, hpx), bg or CLEAR)
    depth = {}
    r = max(1, int(math.ceil(scale / sub / 2 + 0.5)))
    px_ = img.load()
    for (sx, sy_, sd), col in pts:
        px, py = int((sx - minx) * scale), int((sy_ - miny) * scale)
        for ox in range(-r, r):
            for oy in range(-r, r):
                key = (px + ox, py + oy)
                if 0 <= key[0] < wpx and 0 <= key[1] < hpx and sd < depth.get(key, 1e9):
                    depth[key] = sd
                    px_[key] = col + (255,)
    return img


VIEWS = {"side": (0, 0), "three": (35, 25), "top": (0, 90), "below": (0, -90), "front": (90, 20), "bank": (60, -30)}


def ripple_rots(t, flap=0.32, lag=0.9):
    """RayModel's ripple at tick t (swimming)."""
    phase = 0.25 * t
    wing = flap * math.sin(phase)
    tip = 1.3 * flap * math.sin(phase - lag)
    edge = 1.3 * flap * math.sin(phase - 2 * lag)
    r = {}
    for side, s in (("left", 1), ("right", -1)):
        r[side + "_wing"] = (0, 0, s * wing)
        r[side + "_wing_tip"] = (0, 0, s * tip)
        r[side + "_wing_edge"] = (0, 0, s * edge)
    return r


def sheet(shots_dir, old_dir, texture):
    from PIL import ImageFont
    font = ImageFont.load_default()
    W = 1800
    blocks = []
    me = AW.parse_java(JAVA)
    BG = (72, 72, 72, 255)

    def title(t):
        im = Image.new("RGBA", (W, 26), (40, 40, 40, 255))
        ImageDraw.Draw(im).text((8, 6), t, fill=(240, 240, 240, 255), font=font)
        blocks.append(im)

    def row(images, h=None, gap=16, labels=None):
        images = [i for i in images if i is not None]
        if h:
            images = [i.resize((max(1, int(i.width * h / i.height)), h), Image.LANCZOS) for i in images]
        hh = max(i.height for i in images) + (16 if labels else 0)
        im = Image.new("RGBA", (W, hh + 8), BG)
        dr = ImageDraw.Draw(im)
        x = 8
        for n, i in enumerate(images):
            if x + i.width > W:
                break
            im.paste(i, (x, 4 + (hh - (16 if labels else 0) - i.height)), i)
            if labels:
                dr.text((x, hh - 10), labels[n], fill=(230, 230, 230, 255), font=font)
            x += max(i.width, 6 * len(labels[n]) if labels else 0) + gap
        blocks.append(im)

    ref_dir = os.path.join(ROOT, "art", "references", "fish_boll_refonly")
    refs = [Image.open(os.path.join(ref_dir, n)).convert("RGBA")
            for n in ("sr20.jpg", "sr27.jpg", "sr28.jpg", "sr23.jpg", "sr10.jpg", "sr26.jpg")
            if os.path.exists(os.path.join(ref_dir, n))]
    title("References (reference only): landed rays from above (outline, colour out of water), the underside out of "
          "water, the whip tail, swimming")
    row(refs, h=220)
    items = [Image.open(os.path.join(RES, "textures", "item", n)).convert("RGBA")
             for n in ("boll.png", "boll_bucket.png", "boll_spawn_egg.png")]
    base = Image.open(os.path.join(ROOT, "art", ".vanilla", "item", "cod_bucket.png")).convert("RGBA")
    bucket = base.copy()
    bucket.alpha_composite(items[1])
    items[1] = bucket
    title("The accepted icon (C), bucket (N2) and spawn egg (B) at 8x, beside the model from above and from below "
          "(offline, 8x, no water)")
    row([i.resize((128, 128), Image.NEAREST) for i in items]
        + [render(me, texture, *VIEWS["top"], 8), render(me, texture, *VIEWS["below"], 8)])
    title("Offline model, 12x: three-quarter, side, front")
    row([render(me, texture, *VIEWS["three"], 12), render(me, texture, *VIEWS["side"], 12),
         render(me, texture, *VIEWS["front"], 12)])
    title("Offline: palette (icon C lifted x1.15, the bucket's creams) and the texture at 4x")
    sw = Image.new("RGBA", (len(PAL) * 34, 46), BG)
    d = ImageDraw.Draw(sw)
    for i, (k, c) in enumerate(PAL.items()):
        d.rectangle((i * 34, 0, i * 34 + 30, 30), fill=c)
        d.text((i * 34 + 10, 32), k, fill=(240, 240, 240, 255), font=font)
    row([sw, texture.resize((TW * 4, TH * 4), Image.NEAREST)])
    if old_dir and os.path.isdir(old_dir):
        old = (AW.parse_java(os.path.join(old_dir, "BollModel.java")),
               Image.open(os.path.join(old_dir, "boll.png")).convert("RGBA"))
        title("Old (placeholder) vs new, offline 8x: three-quarter and from above")
        row([render(old[0], old[1], *VIEWS["three"], 8), render(me, texture, *VIEWS["three"], 8),
             render(old[0], old[1], *VIEWS["top"], 8), render(me, texture, *VIEWS["top"], 8)],
            labels=["old", "new", "old", "new"])
    if shots_dir and os.path.isdir(shots_dir):
        def shot(n):
            found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None
        names = ("fish-boll-side", "fish-boll-three-quarter", "fish-boll-top", "fish-boll-beside-cod",
                 "fish-boll-below", "fish-boll-below-close", "fish-boll-on-land", "fish-boll-sizes", "fish-boll-sizes-low")
        got = [shot(n) for n in names]
        title("In the game: side, three-quarter, top / beside cod, from below, from below close / on land, then the "
              "sizes on dry sand: discs 1.5, 1.25 (installed) and 1.0 blocks, beside a vanilla cod and a 3-block tonn")
        row(got[:3], h=330)
        row(got[3:6], h=330)
        row(got[6:], h=330)
        if old_dir and os.path.isdir(old_dir):
            def oshot(n):
                found = sorted(glob.glob(os.path.join(old_dir, "*" + n + ".png")))
                return Image.open(found[-1]).convert("RGBA") if found else None
            title("In the game, old (placeholder) above, new below: three-quarter, top, on land")
            row([oshot(n) for n in ("fish-boll-three-quarter", "fish-boll-top", "fish-boll-on-land")], h=300)
            row([shot(n) for n in ("fish-boll-three-quarter", "fish-boll-top", "fish-boll-on-land")], h=300)
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), BG)
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    dest = os.path.join(ROOT, "art", "candidates", "fish_boll_model.png")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    out.convert("RGB").save(dest)
    print("sheet:", dest)
    # the ripple, offline: nine frames of one beat while swimming (0.32 radians), from the front
    frames = [render(me, texture, 90, 12, 9, rots=ripple_rots(t), bg=BG) for t in range(0, 25, 3)]
    fw, fh = max(f_.width for f_ in frames), max(f_.height for f_ in frames)
    strip = Image.new("RGBA", (fw * 3, fh * 3), BG)
    for i, f_ in enumerate(frames):
        strip.paste(f_, ((i % 3) * fw, (i // 3) * fh))
    dest2 = os.path.join(ROOT, "art", "candidates", "fish_boll_model_ripple.png")
    strip.convert("RGB").save(dest2)
    print("ripple:", dest2)


def main():
    probs = check_boxes()
    for p in probs:
        print("problem:", p)
    assert not probs
    texture = draw_texture()
    os.makedirs(os.path.dirname(TEXTURE), exist_ok=True)
    texture.save(TEXTURE)
    with open(JAVA, "w", encoding="utf-8") as fh:
        fh.write(java_source())
    print("wrote", os.path.relpath(TEXTURE, ROOT), "and", os.path.relpath(JAVA, ROOT))
    args = sys.argv[1:]
    if "--sheet" in args:
        i = args.index("--sheet")
        rest = args[i + 1:]
        sheet(rest[0] if rest else None, rest[1] if len(rest) > 1 else None, texture)


if __name__ == "__main__":
    main()
