"""The awrata (gilthead sea bream, Sparus aurata) as a swimming mob: its 3D model and its texture.

Drawn from the reference photos in art/references/fish_awrata_refonly/ (list.tsv). What makes it an awrata:
  - an oval, deep but laterally flat bream: deeper than the lampuka or sardina, much thinner and lighter than the
    cerna (3 px thick against the cerna's 6), deepest at mid-body with a narrow tail stalk,
  - a steep, rounded forehead that falls in single steps to a small mouth with thick pale lips,
  - silver-grey sides under a blue-grey back, with thin darker lines along the body,
  - a GOLD band across the forehead between the eyes: on the top of the head and on the forehead just above and in
    front of the eye, so it reads from the side and from above,
  - a dark patch at the top of the gill cover, and the cover's edge as a 1 px line two columns behind the eye, with a
    muted red foot: no lone dot of colour near the eye, so nothing reads as a second eye,
  - one long dorsal fin (dark spines in front, softer rays behind) and a forked tail with darker edges.
The palette is the accepted item icon's (art/src/fish_awrata_icon.py PAL), each colour lifted a step (brighter and a
touch richer), because under water the game greys and darkens everything. No face is a flat fill: body texels are
shifted one shade lighter or darker by a fixed hash, so reruns are byte-identical.

Size: the hitbox is 0.7 x 0.45 blocks (11.2 x 7.2 model pixels). Vanilla's models run about 2 times their hitbox
width in length (cod 15 px on 8), so the awrata is 23 px long (18 of body from the lips, 5 of tail), 8 px deep
(11 with the dorsal fin, 13 with every fin) and 3 px thick. Body depth to body length 8 to 18 (0.44), like the
cerna's 10 to 24 (0.42) but on a body half as thick (thickness to depth 0.38 against the cerna's 0.6) and far smaller;
the lampuka is 0.23, the sardina 0.27, the tonn 0.38. One texture pixel per model pixel, like vanilla's fish.

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, a root
child "body" and a "tail_fin" that sways like vanilla cod's. The body is rigid, like cod's.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/AwrataModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/awrata.png    (64 x 32)
With --sheet SCREENSHOT_DIR it also writes the compare sheet art/candidates/fish_awrata_model.png (offline previews,
the accepted items, the other accepted fish models at the same scale, the in-game shots).

Run:  art/.venv/bin/python art/src/fish_awrata_model.py [--sheet SCREENSHOT_DIR]
"""
import colorsys
import glob
import math
import os
import re
import sys
import zipfile

from PIL import Image, ImageDraw

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA_DIR = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "fish")
JAVA = os.path.join(JAVA_DIR, "AwrataModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "awrata.png")
TW, TH = 64, 32


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


def lift(c, v=1.15, s=1.08):
    """One step lighter and a touch richer for the water: brightness x1.15, saturation x1.08 (hue kept)."""
    h, sat, val = colorsys.rgb_to_hsv(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
    r, g, b = colorsys.hsv_to_rgb(h, min(1.0, sat * s), min(1.0, val * v))
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)), 255)


def darker(c, k=0.86):
    return (int(round(c[0] * k)), int(round(c[1] * k)), int(round(c[2] * k)), c[3])


# The palette of the accepted awrata item icon (art/src/fish_awrata_icon.py PAL), each lifted one step for the water.
ICON = {
    "K": "#4f6477", "b": "#7d91a3",                                   # blue-grey back: dark, lit
    "W": "#e6ecee", "1": "#cdd6db", "2": "#b4bec6", "3": "#9ba7b1", "4": "#83909b", "5": "#6b7783",  # silver ramp
    "O": "#56626e",                                                   # soft dark: the corner of the mouth
    "G": "#e8bf4c", "g": "#c39a42",                                   # the golden forehead band: lit, shaded
    "p": "#68747f", "P": "#46535e",                                   # the gill patch: soft edge, core
    "R": "#b8664a",                                                   # the red-orange touch below the patch
    "L": "#a2aab1",                                                   # thick lips
    "t": "#46535e",                                                   # darker fin and tail edges
}
PAL = {k: lift(hexc(v)) for k, v in ICON.items()}
PAL["l"] = darker(PAL["L"])     # the lower lip, shaded
# the gold band, pushed further (brighter, richer) than the rest: the first in-game run showed the icon's gold, lifted
# like the rest, going a dull olive under the water's blue
# Critic (round 1): that went dark khaki from the side under water; now the icon's hues, lifted toward cream so the
# band stays lighter and warmer than the flank: lit for the top faces and the brow's top row, shaded for the row below
PAL["G"], PAL["g"] = (248, 214, 120, 255), (232, 190, 90, 255)
# the gill cover: a 1 px line (critic, round 1: a lone red texel and a dark one beside it read as a second eye), in a
# tone between the flank and the back, with a muted red touch, 2 px tall, at its foot
PAL["c"], PAL["r"] = (150, 170, 190, 255), (200, 150, 140, 255)
PAL["e"] = hexc("#0a0a0a")      # the eye (the only black, not lifted)
PAL["."] = (0, 0, 0, 0)
CLEAR = PAL["."]
SILVER = [PAL[k] for k in "W12345"]   # body shades, 0 lightest to 5 darkest


# --- the model -------------------------------------------------------------------------------------------------------
# Parts: name -> (pivot (absolute model pixels), (xRot, yRot, zRot)). Cubes: (name, part, (U, V) top-left of the used
# texture area, (x0, y0, z0) absolute, (w, h, d)). Absolute: x across, y down (24 = ground), z head (-) to tail (+).
PARTS = {
    "body": ((0.0, 19.0, 0.0), (0.0, 0.0, 0.0)),
    "tail_fin": ((0.0, 19.0, 7.0), (0.0, 0.0, 0.0)),
    # the pectoral fins: small fans hinged just outside the flank behind the gill cover, back edges turned out
    "right_fin": ((-1.55, 20.0, -5.0), (0.0, -0.4, 0.0)),
    "left_fin": ((1.55, 20.0, -5.0), (0.0, 0.4, 0.0)),
}
CUBES = [
    # the face, stepping up from the small mouth to the steep rounded forehead: lips, snout, face, head
    ("lips", "body", (58, 6), (-1.0, 19.0, -11.0), (2, 2, 1)),
    ("snout", "body", (52, 6), (-1.0, 18.0, -10.0), (2, 4, 1)),
    ("face", "body", (52, 0), (-1.5, 17.0, -9.0), (3, 5, 1)),
    ("brow", "body", (32, 0), (-1.5, 16.0, -8.0), (3, 6, 1)),
    ("head", "body", (56, 11), (-1.5, 16.0, -7.0), (3, 7, 1)),
    # the deep oval trunk, the rear, and the narrow stalk in two steps
    ("trunk", "body", (0, 0), (-1.5, 15.0, -6.0), (3, 8, 5)),
    ("rear", "body", (16, 0), (-1.5, 16.0, -1.0), (3, 6, 4)),
    ("rear2", "body", (32, 10), (-1.0, 17.0, 3.0), (2, 4, 2)),
    ("stalk", "body", (24, 10), (-1.0, 18.0, 5.0), (2, 2, 2)),
    # the long dorsal fin, the anal fin and the pelvic fins, flat planes down the middle
    ("dorsal", "body", (0, 14), (0.0, 13.0, -7.0), (0, 3, 10)),
    ("anal", "body", (22, 17), (0.0, 21.0, -1.0), (0, 3, 5)),
    ("pelvic", "body", (32, 17), (0.0, 23.0, -5.0), (0, 2, 3)),
    # the forked tail
    ("caudal", "tail_fin", (42, 0), (0.0, 14.0, 7.0), (0, 10, 5)),
    # the pectoral fins
    ("pec_r", "right_fin", (38, 17), (-1.55, 20.0, -5.0), (0, 2, 3)),
    ("pec_l", "left_fin", (44, 17), (1.55, 20.0, -5.0), (0, 2, 3)),
]

# The side of the fish, one character per pixel: columns z -11..7, rows y 15..22. '.' = the plain body, shaded by
# row (blue-grey back, a silver sheen under it, darker toward the belly, thin darker lines along the body).
SIDE_Z0, SIDE_Y0 = -11, 15
FEATURES = [
    # z:   1 1
    #      1 0 9 8 7 6 5 4 3 2 1 0 1 2 3 4 5 6 7
    "...................",   # y 15
    "...G.PP............",   # y 16: gold at the forehead's edge; the gill patch, high, behind the eye
    "..Gg.c.............",   # y 17: the gold band above the eye; the gill cover's line starts under the patch
    ".bWeWc.............",   # y 18: the eye row: blue-grey forehead edge, light silver around the eye; the gill line two columns behind
    "LL...c.............",   # y 19: the upper lip; the gill cover's line
    "lO...r.............",   # y 20: the lower lip and the corner of the mouth; a muted red touch at the line's foot
    ".....r.............",   # y 21
    "...................",   # y 22
]
# the plain body by row: (shade index or back colour, is a lengthwise line)
ROWS = {15: ("K", False), 16: ("b", False), 17: (0, False), 18: (2, True), 19: (1, False), 20: (3, True),
        21: (2, False), 22: (3, False)}
LINES_FROM, LINES_TO = -5, 4      # the lines run along the trunk and rear, not on the head or stalk

# Fins, as text: one character per pixel; colours from PAL (digits: the silver ramp). Every fin has a solid rim.
# the long dorsal fin, rows y 13..15, columns z -7..2: dark spines and darker rim in front, softer rays behind
DORSAL_Z0, DORSAL_Y0 = -7, 13
DORSAL = [
    ".tttttt...",
    "tKbKbKbtt.",
    "KKKKKKbbbt",
]
# the forked tail, rows y 14..23, columns z 7..11: lit above, shaded below, dark edges, the fork's notch at 11-12
CAUDAL_Z0, CAUDAL_Y0 = 7, 14
CAUDAL = [
    "...tt",
    "..b3t",
    ".bb3t",
    "bb3t.",
    "b3t..",
    "34t..",
    "344t.",
    ".344t",
    "..44t",
    "...tt",
]
# the anal fin, rows y 21..23, columns z -1..3 (row 21 shows only below rear2)
ANAL_Z0, ANAL_Y0 = -1, 21
ANAL = [
    "3333t",
    "3344t",
    ".ttt.",
]
# the pelvic fins, rows y 23..24, columns z -5..-3
PELVIC_Z0, PELVIC_Y0 = -5, 23
PELVIC = [
    "34t",
    ".t.",
]
# the pectoral fin, rows y 20..21, columns z -5..-3 (before it is turned out): pale, with a mid-grey rim, so it
# never reads as a dark spot on the flank
PEC_Z0, PEC_Y0 = -5, 20
PECTORAL = [
    "234",
    "34.",
]


def hash01(*vals):
    """A repeatable pseudo-random number in [0, 1) from integers (no floating-point maths)."""
    h = 2166136261
    for v in vals:
        h = ((h ^ (v & 0xffffffff)) * 16777619) & 0xffffffff
    h ^= h >> 13
    h = (h * 0x5bd1e995) & 0xffffffff
    h ^= h >> 15
    return h / 4294967296.0


FACE_SALT = {"top": 1, "bottom": 2, "north": 3, "south": 4, "west": 5, "east": 6}


def plain(yi, zi, salt, xi):
    """The plain body at row yi: the back mottled between its two blue-greys, the silver one shade either way (lines
    only ever darker, so they stay readable)."""
    base, line = ROWS[yi]
    r = hash01(salt, xi, yi, zi)
    if base == "K":
        return PAL["b"] if r < 0.25 else PAL["K"]
    if base == "b":
        return PAL["K"] if r < 0.2 else (PAL["2"] if r > 0.88 else PAL["b"])
    if line and not (LINES_FROM <= zi <= LINES_TO):
        line, base = False, base - 1
    if line:
        return SILVER[base]
    if r < 0.15:
        base -= 1
    elif r > 0.92:
        base += 1
    return SILVER[max(0, min(5, base))]


def side_colour(y, z, face, x):
    yi, zi = int(math.floor(y)), int(math.floor(z))
    ch = FEATURES[yi - SIDE_Y0][zi - SIDE_Z0]
    if ch == "e" and face not in ("west", "east"):
        ch = "."                        # the eye only on the sides
    if ch != ".":
        return PAL[ch]
    return plain(yi, zi, FACE_SALT[face], int(math.floor(x * 2)))


def body_colour(name, face, x, y, z, x0, y0, z0, w, h, d):
    xi, zi = int(math.floor(x * 2)), int(math.floor(z))
    if face == "top":
        if name == "lips":
            return PAL["L"]
        if name == "face" or name == "brow":
            return PAL["G"]   # the gold band across the forehead
        if name == "snout":
            return PAL["b"]
        r = hash01(7, xi, zi)
        if abs(x) < 0.5:                 # darkest along the spine
            return PAL["b"] if r < 0.2 else PAL["K"]
        return PAL["K"] if r < 0.25 else PAL["b"]
    if face == "bottom":
        if name == "lips":
            return PAL["l"]
        r = hash01(2, xi, zi)
        return SILVER[1] if r < 0.2 else (SILVER[3] if r > 0.85 else SILVER[2])
    if face == "north":
        col = side_colour(y, z0, face, x)
        if name == "face" and abs(x) > 1.0 and col not in (PAL["G"], PAL["g"]):
            return darker(col)          # the cheeks turn away: the face reads round, not square
        return col
    if face == "south":
        return side_colour(y, z0 + d - 1, face, x)
    return side_colour(y, z, face, x)


def fin_colour(name, y, z):
    grids = {"dorsal": (DORSAL, DORSAL_Y0, DORSAL_Z0), "anal": (ANAL, ANAL_Y0, ANAL_Z0),
             "pelvic": (PELVIC, PELVIC_Y0, PELVIC_Z0), "caudal": (CAUDAL, CAUDAL_Y0, CAUDAL_Z0),
             "pec_r": (PECTORAL, PEC_Y0, PEC_Z0), "pec_l": (PECTORAL, PEC_Y0, PEC_Z0)}
    grid, gy, gz = grids[name]
    ch = grid[int(math.floor(y)) - gy][int(math.floor(z)) - gz]
    return SILVER["W12345".index(ch)] if ch in "W12345" else PAL[ch]


# --- texture layout (the vanilla box UV layout) ----------------------------------------------------------------------
def tex_offset(cube):
    """texOffs for a cube whose used texture area starts at (U, V): planes leave out the faces they don't have."""
    _, _, (U, V), _, (w, h, d) = cube
    if w == 0:
        return U, V - d
    if h == 0:
        return U - d, V
    return U, V


def face_texels(u, v, origin, size):
    """Every texel of every face of a box with texOffs (u, v): (face, tu, tv, x, y, z), (x, y, z) the texel's centre
    in the box's own coordinates. Follows ModelPart.Cube: top (u+d, v), bottom (u+d+w, v), west (u, v+d),
    north (u+d, v+d), east (u+d+w, v+d), south (u+2d+w, v+d)."""
    x0, y0, z0 = origin
    w, h, d = size
    x1, y1, z1 = x0 + w, y0 + h, z0 + d
    out = []
    for c in range(w):
        for r in range(d):
            out.append(("top", u + d + c, v + r, x0 + c + 0.5, y0, z1 - r - 0.5))
            out.append(("bottom", u + d + w + c, v + r, x0 + c + 0.5, y1, z1 - r - 0.5))
    for c in range(d):
        for r in range(h):
            out.append(("west", u + c, v + d + r, x0, y0 + r + 0.5, z1 - c - 0.5))
            out.append(("east", u + d + w + c, v + d + r, x1, y0 + r + 0.5, z0 + c + 0.5))
    for c in range(w):
        for r in range(h):
            out.append(("north", u + d + c, v + d + r, x0 + c + 0.5, y0 + r + 0.5, z0))
            out.append(("south", u + 2 * d + w + c, v + d + r, x1 - c - 0.5, y0 + r + 0.5, z1))
    return out


def draw_texture():
    img = Image.new("RGBA", (TW, TH), CLEAR)
    owner = {}
    for cube in CUBES:
        name, _, _, (x0, y0, z0), (w, h, d) = cube
        u, v = tex_offset(cube)
        for face, tu, tv, x, y, z in face_texels(u, v, (x0, y0, z0), (w, h, d)):
            if w == 0 and face not in ("west", "east"):
                continue
            assert 0 <= tu < TW and 0 <= tv < TH, (name, face, tu, tv)
            assert owner.setdefault((tu, tv), name) == name, ("texture overlap", name, owner[(tu, tv)], tu, tv)
            col = fin_colour(name, y, z) if w == 0 else body_colour(name, face, x, y, z, x0, y0, z0, w, h, d)
            img.putpixel((tu, tv), col)
    return img


# --- the Java model ---------------------------------------------------------------------------------------------------
def f(v):
    s = ("%.4f" % v).rstrip("0")
    if s.endswith("."):
        s += "0"
    if s == "-0.0":
        s = "0.0"
    return s + "F"


def write_java():
    lines = []
    for part in ("body", "tail_fin", "right_fin", "left_fin"):
        (px, py, pz), rot = PARTS[part]
        builder = "CubeListBuilder.create()"
        for cube in [c for c in CUBES if c[1] == part]:
            name, _, _, (x0, y0, z0), (w, h, d) = cube
            u, v = tex_offset(cube)
            builder += "\n            /* %s */ .texOffs(%d, %d).addBox(%s, %s, %s, %d.0F, %d.0F, %d.0F)" % (
                name, u, v, f(x0 - px), f(y0 - py), f(z0 - pz), w, h, d)
        if any(rot):
            pose = "PartPose.offsetAndRotation(%s, %s, %s, %s, %s, %s)" % (
                f(px), f(py), f(pz), f(rot[0]), f(rot[1]), f(rot[2]))
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
 * The awrata (gilthead sea bream): an oval, deep but flat body, silver-grey under a blue-grey back with thin darker
 * lines, a gold band across the forehead between the eyes, a dark patch with a red-orange touch at the top of the gill
 * cover, a steep rounded forehead over a small thick-lipped mouth, one long dorsal fin and a forked tail with darker
 * edges that sways as it swims. 23 px long, 8 px deep, 3 px thick, head toward -z, the ground at y 24.
 * Made by art/src/fish_awrata_model.py (don't edit by hand). Texture: textures/entity/fish/awrata.png (64 x 32).
 */
public class AwrataModel extends FishModel {
    public AwrataModel(ModelPart root) {
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


# --- offline previews: any model read back from its Java file, drawn as an orthographic texel splatter -------------
SHADE = {"top": 1.0, "bottom": 0.5, "north": 0.8, "south": 0.8, "west": 0.6, "east": 0.6}
NUM = r"(-?\d+(?:\.\d+)?)F?"


def parse_java(path):
    """Read a model's createBodyLayer back: [(part, parent, pivot, rot, [(u, v, origin, size)])], and the texture
    size. Handles root children and children of a named PartDefinition (the tonn's and lampuka's 'tail')."""
    src = open(path, encoding="utf-8").read()
    parts = []
    pat = re.compile(r"(?:PartDefinition\s+(\w+)\s*=\s*)?(\w+)\.addOrReplaceChild\(\"(\w+)\",\s*CubeListBuilder\.create\(\)"
                     r"(.*?)PartPose\.(offsetAndRotation|offset)\(([^)]*)\)\);", re.S)
    var_part = {"root": None}
    for m in pat.finditer(src):
        var, parent_var, name, cubes_src, kind, args = m.groups()
        nums = [float(a.strip().rstrip("F")) for a in args.split(",")]
        pivot = tuple(nums[:3])
        rot = tuple(nums[3:6]) if kind == "offsetAndRotation" else (0.0, 0.0, 0.0)
        cubes = []
        for c in re.finditer(r"\.texOffs\((-?\d+),\s*(-?\d+)\)\.addBox\(([^)]*)\)", cubes_src):
            b = [float(a.strip().rstrip("F")) for a in c.group(3).split(",")]
            cubes.append((int(c.group(1)), int(c.group(2)), tuple(b[:3]), (int(b[3]), int(b[4]), int(b[5]))))
        parts.append((name, var_part.get(parent_var), pivot, rot, cubes))
        if var:
            var_part[var] = name
    size = re.search(r"LayerDefinition\.create\(mesh,\s*(\d+),\s*(\d+)\)", src)
    return parts, (int(size.group(1)), int(size.group(2)))


def rot_point(p, rot):
    """ModelPart rotates by rotationZYX(z, y, x): x first, then y, then z."""
    x, y, z = p
    rx, ry, rz = rot
    if rx:
        c, s = math.cos(rx), math.sin(rx)
        y, z = y * c - z * s, y * s + z * c
    if ry:
        c, s = math.cos(ry), math.sin(ry)
        x, z = x * c + z * s, -x * s + z * c
    if rz:
        c, s = math.cos(rz), math.sin(rz)
        x, y = x * c - y * s, x * s + y * c
    return (x, y, z)


def render(model, texture, view, scale, sub=4):
    """Draw a parsed model from 'side' (from -x, head left), 'top' (from above, head left) or 'three' (front
    three-quarter), with `scale` screen pixels per model pixel; cropped to the fish."""
    parts, _ = model
    by_name = {p[0]: p for p in parts}

    def world(part, p):
        while part:
            _, parent, pivot, rot, _ = by_name[part]
            p = rot_point(p, rot)
            p = (p[0] + pivot[0], p[1] + pivot[1], p[2] + pivot[2])
            part = parent
        return p

    yaw, pitch = {"side": (0.0, 0.0), "top": (0.0, 90.0), "three": (35.0, 25.0)}[view]
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))

    def project(p):
        x, y, z = p
        z2, x2 = z * cy + x * sy, -z * sy + x * cy
        return z2, y * cp - x2 * sp, y * sp + x2 * cp

    pts = []
    for name, _, _, _, cubes in parts:
        for u, v, origin, size in cubes:
            for face, tu, tv, x, y, z in face_texels(u, v, origin, size):
                if not (0 <= tu < texture.size[0] and 0 <= tv < texture.size[1]):
                    continue
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
    img = Image.new("RGBA", (wpx, hpx), CLEAR)
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


# vanilla cod and salmon (26.3 CodModel and SalmonModel, as numbers), for scale
COD = ([("p", None, (0, 0, 0), (0, 0, 0), [(0, 0, (-1, 20, 0), (2, 4, 7)), (11, 0, (-1, 20, -3), (2, 4, 3)),
                                          (0, 0, (-1, 20, -4), (2, 3, 1)), (22, 3, (0, 20, 7), (0, 4, 4)),
                                          (20, -6, (0, 19, -1), (0, 1, 6))]),
        ("rf", None, (-1, 23, 0), (0, 0, -0.7854), [(22, 1, (-2, 0, -1), (2, 0, 2))]),
        ("lf", None, (1, 23, 0), (0, 0, 0.7854), [(22, 4, (0, 0, -1), (2, 0, 2))])], (32, 32))
SALMON = ([("p", None, (0, 0, 0), (0, 0, 0), [(0, 0, (-1.5, 17.5, -7.2), (3, 5, 8)), (0, 13, (-1.5, 17.5, 0.8), (3, 5, 8)),
                                             (22, 0, (-1, 18, -10.2), (2, 4, 3)), (20, 10, (0, 17.5, 8.8), (0, 5, 6)),
                                             (2, 1, (0, 15.5, -2.2), (0, 2, 3)), (0, 2, (0, 15.5, -0.2), (0, 2, 4))]),
           ("rf", None, (-1.5, 21.5, -7.2), (0, 0, -0.7854), [(-4, 0, (-2, 0, 0), (2, 0, 2))]),
           ("lf", None, (1.5, 21.5, -7.2), (0, 0, 0.7854), [(0, 0, (0, 0, 0), (2, 0, 2))])], (32, 32))


def vanilla_texture(name):
    for jar in sorted(glob.glob(os.path.join(ROOT, ".art-runs", "*", ".gradle", "loom-cache", "minecraftMaven", "net",
                                             "minecraft", "minecraft-merged-*", "26.3", "*.jar"))):
        with zipfile.ZipFile(jar) as z:
            try:
                with z.open("assets/minecraft/textures/entity/fish/%s.png" % name) as fh:
                    return Image.open(fh).convert("RGBA").copy()
            except KeyError:
                continue
    return None


OTHERS = ("lampuka", "tonn", "sardina", "cerna")


def load_model(fish):
    model = parse_java(os.path.join(JAVA_DIR, fish.capitalize() + "Model.java"))
    tex = Image.open(os.path.join(RES, "textures", "entity", "fish", fish + ".png")).convert("RGBA")
    return model, tex


def extent(model):
    """Length, depth (body boxes only, and with fins) and thickness of a parsed model at rest, in model pixels."""
    pts_body, pts_all = [], []
    by_name = {p[0]: p for p in model[0]}

    def offset(part):
        ox = oy = oz = 0.0
        while part:
            _, parent, pivot, _, _ = by_name[part]
            ox, oy, oz = ox + pivot[0], oy + pivot[1], oz + pivot[2]
            part = parent
        return ox, oy, oz
    for name, _, _, rot, cubes in model[0]:
        if any(rot):
            continue                    # the turned-out side fins don't change the length or depth
        pivot = offset(name)
        for u, v, (x0, y0, z0), (w, h, d) in cubes:
            for c in ((x0, y0, z0), (x0 + w, y0 + h, z0 + d)):
                p = (c[0] + pivot[0], c[1] + pivot[1], c[2] + pivot[2])
                pts_all.append(p)
                if w and h and d:
                    pts_body.append(p)

    def span(pts, i):
        return max(p[i] for p in pts) - min(p[i] for p in pts)
    return span(pts_all, 2), span(pts_body, 1), span(pts_all, 1), span(pts_body, 0), span(pts_body, 2)


# --- the compare sheet ------------------------------------------------------------------------------------------------
def sheet(shots_dir, texture):
    from PIL import ImageFont
    font = ImageFont.load_default()
    W = 1800
    blocks = []
    me = (parse_java(JAVA), texture)

    def title(t):
        im = Image.new("RGBA", (W, 26), (40, 40, 40, 255))
        ImageDraw.Draw(im).text((8, 6), t, fill=(240, 240, 240, 255), font=font)
        blocks.append(im)

    def row(images, h=None, gap=12, align_bottom=False, labels=None):
        if h:
            images = [i.resize((max(1, int(i.width * h / i.height)), h), Image.LANCZOS) for i in images]
        hh = max(i.height for i in images) + (16 if labels else 0)
        im = Image.new("RGBA", (W, hh + 8), (72, 72, 72, 255))
        dr = ImageDraw.Draw(im)
        x = 8
        for n, i in enumerate(images):
            step = max(i.width, 6 * len(labels[n]) if labels else 0) + gap
            if x + i.width > W:
                break
            top = 4 + (hh - (16 if labels else 0) - i.height if align_bottom else 0)
            im.paste(i, (x, top), i)
            if labels:
                dr.text((x, hh - 10), labels[n], fill=(230, 230, 230, 255), font=font)
            x += step
        blocks.append(im)

    ref_dir = os.path.join(ROOT, "art", "references", "fish_awrata_refonly")
    refs = [Image.open(os.path.join(ref_dir, n)).convert("RGBA")
            for n in ("awrata_01.jpg", "awrata_06.jpg", "awrata_09.jpg", "awrata_03.jpg", "awrata_11.jpg",
                      "awrata_08.jpg") if os.path.exists(os.path.join(ref_dir, n))]
    title("References (reference only): out of water for colour, the gold band and gill patch, the fins; in water")
    row(refs[:3], h=240)
    row(refs[3:], h=240)
    title("Offline model, 16x: side, three-quarter, top (vanilla face shading only, no water)")
    row([render(me[0], texture, "side", 16), render(me[0], texture, "three", 16)])
    row([render(me[0], texture, "top", 16)])
    items = [Image.open(os.path.join(RES, "textures", "item", n)).convert("RGBA")
             for n in ("awrata.png", "awrata_bucket.png", "awrata_spawn_egg.png")]
    title("The accepted awrata item icon, bucket and spawn egg (8x), beside the model (side and three-quarter, 8x)")
    row([i.resize((128, 128), Image.NEAREST) for i in items]
        + [render(me[0], texture, "side", 8), render(me[0], texture, "three", 8)], align_bottom=True, gap=24)
    models = [("awrata", me)] + [(n, load_model(n)) for n in OTHERS]
    cod, sal = vanilla_texture("cod"), vanilla_texture("salmon")
    if cod and sal:
        models += [("vanilla cod", (COD, cod)), ("vanilla salmon", (SALMON, sal))]
    labels = []
    for n, (mdl, _) in models:
        ln, dep, depf, thick, blen = extent(mdl)
        labels.append("%s: %d long, %d deep, %d thick" % (n, ln, dep, thick))
    title("Same scale, 6x, side: the awrata beside the accepted lampuka, tonn, sardina, cerna, and vanilla cod and salmon")
    row([render(m[0], m[1], "side", 6) for _, m in models[:3]], align_bottom=True, gap=40, labels=labels[:3])
    row([render(m[0], m[1], "side", 6) for _, m in models[3:]], align_bottom=True, gap=40, labels=labels[3:])
    title("Same scale, 6x, from above (thickness): the same fish in the same order")
    row([render(m[0], m[1], "top", 6) for _, m in models[:3]], align_bottom=True, gap=40, labels=labels[:3])
    row([render(m[0], m[1], "top", 6) for _, m in models[3:]], align_bottom=True, gap=40, labels=labels[3:])
    title("Texture at 6x and 1x (64 x 32)")
    row([texture.resize((TW * 6, TH * 6), Image.NEAREST), texture])
    if shots_dir and os.path.isdir(shots_dir):
        def shot(n):
            found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None

        names = ("fish-awrata-side", "fish-awrata-three-quarter", "fish-awrata-top", "fish-awrata-on-land",
                 "fish-awrata-beside-cod")
        got = [(n, shot(n)) for n in names]
        got = [(n, i) for n, i in got if i]
        if got:
            title("In the game: the awrata alone (side, three-quarter, top, on land), and beside vanilla cod")
            row([i for _, i in got[:3]], h=330)
            row([i for _, i in got[3:]], h=330)
            title("The same, cropped to the fish (beside cod: awrata right, cod left)")
            boxes = {"fish-awrata-beside-cod": (0.04, 0.2, 0.96, 0.7)}
            crops = []
            for n, i in got:
                fx = boxes.get(n, (0.2, 0.2, 0.8, 0.7))
                box = (int(i.width * fx[0]), int(i.height * fx[1]), int(i.width * fx[2]), int(i.height * fx[3]))
                k = 580.0 / (box[2] - box[0])
                crops.append(i.crop(box).resize((580, int((box[3] - box[1]) * k)), Image.NEAREST))
            row(crops[:3])
            row(crops[3:])
        tank = [shot(n) for n in ("fish-03-tank-awrata-lampuka-cerna", "fish-01-tank-all", "fish-06-on-land")]
        tank = [i for i in tank if i]
        if tank:
            title("In the game: the shared tank (awrata, lampuka, cerna, ...), and on land")
            row(tank, h=330)
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    dest = os.path.join(ROOT, "art", "candidates", "fish_awrata_model.png")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    out.convert("RGB").save(dest)
    print("sheet:", dest)
    for l in labels:
        print(" ", l)


def main():
    texture = draw_texture()
    os.makedirs(os.path.dirname(TEXTURE), exist_ok=True)
    texture.save(TEXTURE)
    write_java()
    print("wrote", os.path.relpath(TEXTURE, ROOT), "and", os.path.relpath(JAVA, ROOT))
    args = sys.argv[1:]
    if "--sheet" in args:
        i = args.index("--sheet")
        sheet(args[i + 1] if i + 1 < len(args) else None, texture)


if __name__ == "__main__":
    main()
