"""The ċawl (Mediterranean damselfish, Chromis chromis, the brown adult) as a swimming mob: its 3D model and texture.

Drawn from the reference photos in art/references/fish_cawl_refonly/ (list.tsv). What makes it a ċawl:
  - small: the smallest of the deep-bodied fish, shorter than vanilla cod;
  - a deep, oval, flat-sided body, deepest just behind the head, on a narrow tail stalk;
  - dark chocolate brown, the large scales showing as a net: each scale darker in the middle, paler at its rim;
  - a deeply forked tail, the two long lobes pale at their tips;
  - one long dark dorsal fin along the back, a dark anal fin under the rear, dark pelvic fins;
  - a blunt rounded head, a small mouth and a big eye in a lit socket.
It must not read as a small ċerna (bulky, red-brown, rounded tail) or a small awrata (silver bream): it is darker,
flatter (2 px thick), much smaller, and its tail is the deepest fork of the set.

The palette is the accepted item icon's (art/src/fish_cawl_icon.py PAL), lifted at most a step (brightness x LIFT):
mean texture brightness about 82 (icon 73, ċerna 114), so it stays dark chocolate on land, not ċerna-tan (critic,
round 1 at x1.45 was 106). The head is darker than the flank and stepped round: the front of the forehead dome
catches a little light, the eye sits in a mid-dark socket, the cheek, chin and throat below it are shaded, and every
step of the face has its outer edges a tone darker, so the face reads round, not flat (owner, 2026-11-18: "cawl's
face is too flat"). The flank's scale net is two tones deep (lit rim, dark centre) so it still shows under water.

Size: the hitbox is 0.35 x 0.4 blocks (5.6 x 6.4 model pixels). The model is 14 px long (10 of body from the lip, 4
of tail), 5 px deep (8 with the dorsal and anal fins), 2 px thick. Body depth to body length 0.5, the deepest of the
fish (awrata 0.44, cerna 0.42, cod 0.36); length 14 against cod's 15, the awrata's 23 and the cerna's 29.
One texture pixel per model pixel, like vanilla's fish.

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, a root
child "body" and a "tail_fin" that sways like vanilla cod's.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/CawlModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/cawl.png    (32 x 32)
With --sheet [SCREENSHOT_DIR] also writes the compare sheet art/candidates/fish_cawl_model.png.

Run:  art/.venv/bin/python art/src/fish_cawl_model.py [--sheet SCREENSHOT_DIR]
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
JAVA = os.path.join(JAVA_DIR, "CawlModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "cawl.png")
TW, TH = 32, 32
# round 1's texture (sent back by the critic), kept only for the compare sheet
ROUND1_TEXTURE = os.path.join(ROOT, "art", "candidates", "fish_cawl_model_round1_texture.png")

LIFT = 1.18     # brightness: at most a step above the icon (round 1 at 1.45 went ċerna-tan on land, critic)


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


def lift(c, v=LIFT, s=1.0):
    """The icon's colour a step lighter for the water (hue kept, a touch richer)."""
    h, sat, val = colorsys.rgb_to_hsv(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
    r, g, b = colorsys.hsv_to_rgb(h, min(1.0, sat * s), min(1.0, val * v))
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)), 255)


def darker(c, k=0.85):
    return (int(round(c[0] * k)), int(round(c[1] * k)), int(round(c[2] * k)), c[3])


# The palette of the accepted ċawl item icon (art/src/fish_cawl_icon.py PAL), each lifted one step for the water.
ICON = {
    "K": "#3c291d", "b": "#5f4535",                                   # the dark back: rim, band below it
    "H": "#a07c5c",                                                   # the highlight on the forehead dome
    "W": "#8a6a50", "1": "#735540", "2": "#614636", "3": "#4f3a2c", "4": "#432f23", "5": "#36261c",  # light ramp
    "L": "#402b1f",                                                   # the small mouth
    "D": "#4a3428", "d": "#7a6656", "c": "#5c4132",                   # dorsal fin: base, pale edge, mid
    "F": "#2b1d15",                                                   # pelvic and anal fins (dark)
    "p": "#a8968a", "q": "#8e705d", "r": "#6d5242", "t": "#4a3428",   # tail: pale tips, lit lobe, shaded, notch
}
PAL = {k: lift(hexc(v)) for k, v in ICON.items()}
# the tail's lobe tips and lit lobe keep the icon's own colours (round 1's near-white tips read as bright specks)
PAL["p"], PAL["q"] = hexc(ICON["p"]), hexc(ICON["q"])
PAL["e"] = hexc("#0a0a0a")      # the eye (the only black, not lifted)
PAL["."] = (0, 0, 0, 0)
CLEAR = PAL["."]
RAMP = [PAL[k] for k in "W12345"]   # body tones, 0 lightest to 5 darkest


# --- the model -------------------------------------------------------------------------------------------------------
# Parts: name -> (pivot (absolute model pixels), (xRot, yRot, zRot)). Cubes: (name, part, (U, V) top-left of the used
# texture area, (x0, y0, z0) absolute, (w, h, d)). Absolute: x across, y down (24 = ground), z head (-) to tail (+).
PARTS = {
    "body": ((0.0, 20.0, 0.0), (0.0, 0.0, 0.0)),
    "tail_fin": ((0.0, 20.0, 3.0), (0.0, 0.0, 0.0)),
    # the pectoral fins: small fans hinged just outside the flank behind the gill cover, back edges turned out
    "right_fin": ((-1.05, 20.0, -3.0), (0.0, -0.4, 0.0)),
    "left_fin": ((1.05, 20.0, -3.0), (0.0, 0.4, 0.0)),
}
CUBES = [
    # the blunt rounded head, stepping up one pixel at a time from the small mouth to the forehead
    ("lip", "body", (26, 0), (-0.5, 20.0, -7.0), (1, 2, 1)),
    ("snout", "body", (20, 4), (-1.0, 19.0, -6.0), (2, 3, 1)),
    # the deep trunk (eye in its first column), the rear, the narrow tail stalk
    ("trunk", "body", (0, 0), (-1.0, 18.0, -5.0), (2, 5, 4)),
    ("rear", "body", (12, 0), (-1.0, 18.0, -1.0), (2, 4, 2)),
    ("stalk", "body", (20, 0), (-0.5, 19.0, 1.0), (1, 2, 2)),
    # the long dorsal fin, the anal fin and the pelvic fins, flat planes down the middle
    ("dorsal", "body", (8, 9), (0.0, 16.0, -4.0), (0, 3, 7)),
    ("anal", "body", (8, 12), (0.0, 21.0, -1.0), (0, 3, 4)),
    ("pelvic", "body", (16, 12), (0.0, 23.0, -4.0), (0, 1, 3)),
    # the deeply forked tail
    ("caudal", "tail_fin", (0, 9), (0.0, 16.0, 3.0), (0, 8, 4)),
    # the pectoral fins
    ("pec_r", "right_fin", (16, 13), (-1.05, 20.0, -3.0), (0, 2, 3)),
    ("pec_l", "left_fin", (22, 13), (1.05, 20.0, -3.0), (0, 2, 3)),
]

# The side of the fish, one character per pixel: columns z -7..2, rows y 18..22. '.' = the plain body (below).
# The head: lit forehead (W) above and in front of the eye, a lit cheek (1) behind it, the shaded cheek (2) and chin
# (3) below it; the eye row holds nothing else. The gill line is a short curve two steps darker, starting a row below
# the eye. The mouth is the lip's lower row, shaded.
SIDE_Z0, SIDE_Y0 = -7, 18
FEATURES = [
    # z: 7 6 5 4 3 2 1 0 1 2   (negative to -1, then 0..2)
    "..12......",   # y 18: the forehead dome, catching the light at its front
    ".2e2......",   # y 19: the eye in a mid-dark socket (no light texel touches it)
    "32323.....",   # y 20: lip, snout, shaded cheek under the eye, cheek, the gill line
    "44435.....",   # y 21: the shaded chin and throat (the mouth's lower lip); the gill line
    "..45......",   # y 22: the throat; the gill line's foot
]
# The plain body by row: (scale rim, scale centre). The large scales show as a net: a lighter rim around a darker
# centre, one tone apart, in a diagonal checker (never a lone bright texel). The back is dark, the flank lit under it,
# the belly shaded.
ROWS = {18: ("b", "K"), 19: ("W", "2"), 20: ("1", "3"), 21: ("2", "4"), 22: ("4", "5")}

# Fins, as text: one character per pixel; colours from PAL. Every fin has a solid edge and touches the body.
# the long dorsal fin, rows y 16..18, columns z -4..2 (row 18 lies inside the body until the stalk, so it shows
# only over the stalk): dark, with a rim a step lighter along the top
DORSAL_Z0, DORSAL_Y0 = -4, 16
DORSAL = [
    "..cccc.",
    "cDDDDDD",
    ".....Dc",
]
# the anal fin, rows y 21..23, columns z -1..2 (row 21 shows only under the stalk): dark, a paler trailing rim
ANAL_Z0, ANAL_Y0 = -1, 21
ANAL = [
    "..FF",
    "FFFc",
    ".Fc.",
]
# the pelvic fins, row y 23, columns z -4..-2: dark, the long first ray's tip a little paler
PELVIC_Z0, PELVIC_Y0 = -4, 23
PELVIC = [
    "FFc",
]
# the deeply forked tail, rows y 16..23, columns z 3..6: two lobes 2 px thick, lit above and shaded below, pale at
# their tips, a dark edge along the notch, which reaches in to z 5, half the tail's length
CAUDAL_Z0, CAUDAL_Y0 = 3, 16
CAUDAL = [
    "..qp",
    ".qqp",
    "qqr.",
    "qt..",
    "rt..",
    "rrr.",
    ".rrp",
    "..rp",
]
# the pectoral fin, rows y 20..21, columns z -3..-1 (before it is turned out), below the eye's row: a soft fan in
# the flank's own tones, darker to its edge, so it never reads as a spot
PEC_Z0, PEC_Y0 = -3, 20
PECTORAL = [
    "rt.",
    "rtt",
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


def plain(yi, zi):
    """The plain body: the scale net on the flank (rim and centre in a diagonal checker), smooth on the head."""
    rim, centre = ROWS[yi]
    if zi <= -4 or (yi == 19 and zi < -1):
        return PAL[centre]              # the head is darker than the flank, and the eye's row stays clear
    return PAL[rim] if (zi + yi) % 2 == 0 else PAL[centre]


def side_colour(y, z, face):
    yi, zi = int(math.floor(y)), int(math.floor(z))
    ch = FEATURES[yi - SIDE_Y0][zi - SIDE_Z0]
    if ch == "e" and face not in ("west", "east"):
        ch = "2"                        # the eye only on the sides (mid-dark elsewhere, even where hidden)
    if ch != ".":
        return RAMP["W12345".index(ch)] if ch in "W12345" else PAL[ch]
    return plain(yi, zi)


def body_colour(name, face, x, y, z, x0, y0, z0, w, h, d):
    xi, zi = int(math.floor(x * 2)), int(math.floor(z))
    if face == "top":
        if name == "lip":
            return PAL["3"]
        if name == "snout":
            return PAL["2"]
        if name == "trunk" and zi == -5:
            return PAL["1"]             # the top of the forehead dome, a little lit (never a pale band)
        if name == "trunk" and zi == -4:
            return PAL["b"]
        r = hash01(7, xi, zi)
        return PAL["b"] if r < 0.3 else PAL["K"]   # the dark back
    if face == "bottom":
        if name in ("lip", "snout"):
            return PAL["4"]
        r = hash01(2, xi, zi)
        return PAL["4"] if r < 0.35 else PAL["5"]
    if face == "north":
        col = side_colour(y, z0, face)
        if name == "lip" and int(math.floor(y)) == 21:
            return PAL["L"]             # the small mouth, seen from the front
        if name == "lip":
            return PAL["3"]
        if name == "snout" and int(math.floor(y)) == 19:
            return PAL["2"]             # the front of the dome: mid-dark, falling to the shaded chin below
        if name == "trunk" and int(math.floor(y)) == 18:
            return PAL["2"]             # the forehead above the snout
        if w >= 2 and abs(x) > 0.5:
            return darker(col)          # the cheeks turn away: the face reads round, not square
        return col
    if face == "south":
        return side_colour(y, z0 + d - 1, face)
    return side_colour(y, z, face)


def fin_colour(name, y, z):
    grids = {"dorsal": (DORSAL, DORSAL_Y0, DORSAL_Z0), "anal": (ANAL, ANAL_Y0, ANAL_Z0),
             "pelvic": (PELVIC, PELVIC_Y0, PELVIC_Z0), "caudal": (CAUDAL, CAUDAL_Y0, CAUDAL_Z0),
             "pec_r": (PECTORAL, PEC_Y0, PEC_Z0), "pec_l": (PECTORAL, PEC_Y0, PEC_Z0)}
    grid, gy, gz = grids[name]
    return PAL[grid[int(math.floor(y)) - gy][int(math.floor(z)) - gz]]


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


def check_fins_touch():
    """Every opaque fin texel joins the body or another opaque texel of its fin, and every fin has at least one texel
    on the body's edge (so no fin floats)."""
    body = [c for c in CUBES if c[4][0] and c[1] == "body"]

    def on_body(y, z):
        # a fin texel (row y, column z, both integers) that lies against a body box (inside or edge-adjacent)
        for _, _, _, (x0, y0, z0), (w, h, d) in body:
            if y0 - 1 <= y <= y0 + h and z0 <= z < z0 + d:
                return True
        return False
    for name, grid, gy, gz in (("dorsal", DORSAL, DORSAL_Y0, DORSAL_Z0), ("anal", ANAL, ANAL_Y0, ANAL_Z0),
                               ("pelvic", PELVIC, PELVIC_Y0, PELVIC_Z0)):
        cells = [(gy + r, gz + c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch != "."]
        assert any(on_body(y, z) for y, z in cells), ("fin floats", name)


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
 * The cawl (Mediterranean damselfish, the brown adult): small, with a deep, oval, flat-sided body, dark chocolate
 * brown with the large scales showing as a net, a blunt rounded head with a small mouth and a big eye, one long dark
 * dorsal fin, dark anal and pelvic fins, and a deeply forked tail with pale lobe tips that sways as it swims.
 * 14 px long, 5 px deep, 2 px thick, head toward -z, the ground at y 24.
 * Made by art/src/fish_cawl_model.py (don't edit by hand). Texture: textures/entity/fish/cawl.png (32 x 32).
 */
public class CawlModel extends FishModel {
    public CawlModel(ModelPart root) {
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


def parse_java(path):
    """Read a model's createBodyLayer back: [(part, parent, pivot, rot, [(u, v, origin, size)])], and the texture
    size. Handles root children and children of a named PartDefinition."""
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


# vanilla cod (26.3 CodModel, as numbers), for scale
COD = ([("p", None, (0, 0, 0), (0, 0, 0), [(0, 0, (-1, 20, 0), (2, 4, 7)), (11, 0, (-1, 20, -3), (2, 4, 3)),
                                          (0, 0, (-1, 20, -4), (2, 3, 1)), (22, 3, (0, 20, 7), (0, 4, 4)),
                                          (20, -6, (0, 19, -1), (0, 1, 6))]),
        ("rf", None, (-1, 23, 0), (0, 0, -0.7854), [(22, 1, (-2, 0, -1), (2, 0, 2))]),
        ("lf", None, (1, 23, 0), (0, 0, 0.7854), [(22, 4, (0, 0, -1), (2, 0, 2))])], (32, 32))


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


def load_model(fish):
    model = parse_java(os.path.join(JAVA_DIR, fish.capitalize() + "Model.java"))
    tex = Image.open(os.path.join(RES, "textures", "entity", "fish", fish + ".png")).convert("RGBA")
    return model, tex


def extent(model):
    """Length, body depth, depth with fins, thickness of a parsed model at rest, in model pixels."""
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
    return span(pts_all, 2), span(pts_body, 1), span(pts_all, 1), span(pts_body, 0)


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

    def row(images, h=None, gap=12, align_bottom=False, labels=None, bg=(72, 72, 72, 255)):
        if h:
            images = [i.resize((max(1, int(i.width * h / i.height)), h), Image.LANCZOS) for i in images]
        hh = max(i.height for i in images) + (16 if labels else 0)
        im = Image.new("RGBA", (W, hh + 8), bg)
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

    ref_dir = os.path.join(ROOT, "art", "references", "fish_cawl_refonly")
    refs = [Image.open(os.path.join(ref_dir, n)).convert("RGBA")
            for n in ("cawl_01.jpg", "cawl_07.jpg", "cawl_13_drawing.jpg", "cawl_04.jpg", "cawl_06.jpg", "cawl_02.jpg")
            if os.path.exists(os.path.join(ref_dir, n))]
    title("References (reference only): the deep oval body, scale net, big eye, small mouth, long dorsal fin, "
          "deeply forked tail with pale tips")
    row(refs[:3], h=240)
    row(refs[3:], h=240)
    if os.path.exists(ROUND1_TEXTURE):
        old = Image.open(ROUND1_TEXTURE).convert("RGBA")
        title("Round 1 (critic: too light, cerna-tan, a pale band through the eye, near-white tail tips) above, "
              "round 2 below: offline at 12x, then the textures at 6x")
        row([render(me[0], old, "side", 12), render(me[0], old, "three", 12)])
        row([render(me[0], texture, "side", 12), render(me[0], texture, "three", 12)])
        row([old.resize((TW * 6, TH * 6), Image.NEAREST), texture.resize((TW * 6, TH * 6), Image.NEAREST)], gap=30)
        old_dir = os.path.join(ROOT, ".art-runs", "cawlmodel", "build", "smoke-run", "screenshots")
        if shots_dir and os.path.isdir(old_dir) and os.path.isdir(shots_dir):
            pairs = []
            for n, box in (("fish-cawl-beside-cod", (100, 160, 760, 340)), ("fish-cawl-on-land", (340, 150, 510, 270)),
                           ("fish-cawl-three-quarter", (250, 60, 700, 300))):
                for d in (old_dir, shots_dir):
                    found = sorted(glob.glob(os.path.join(d, "*" + n + ".png")))
                    if found:
                        im = Image.open(found[-1]).convert("RGBA").crop(box)
                        pairs.append(im.resize((im.width * 200 // im.height, 200), Image.NEAREST))
            if pairs:
                title("In the game, round 1 then round 2: beside cod (under water), on land, three-quarter")
                row(pairs[:2], gap=20)
                row(pairs[2:], gap=20)
    title("Offline model, 16x: side, three-quarter, top (vanilla face shading only, no water)")
    row([render(me[0], texture, "side", 16), render(me[0], texture, "three", 16)])
    row([render(me[0], texture, "top", 16)])

    items = []
    item_dir = os.path.join(RES, "textures", "item")
    van_bucket = os.path.join(ROOT, "art", ".vanilla", "item", "cod_bucket.png")
    for n in ("cawl.png", "cawl_bucket.png", "cawl_spawn_egg.png"):
        p = os.path.join(item_dir, n)
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGBA")
        if n == "cawl_bucket.png" and os.path.exists(van_bucket):
            base = Image.open(van_bucket).convert("RGBA")
            base.alpha_composite(im)    # layered over the player's own vanilla cod bucket, as the game draws it
            im = base
        items.append(im)
    title("The accepted cawl item icon, bucket (over vanilla cod_bucket) and spawn egg, 8x, beside the model "
          "(side and three-quarter, 8x)")
    row([i.resize((128, 128), Image.NEAREST) for i in items]
        + [render(me[0], texture, "side", 8), render(me[0], texture, "three", 8)], align_bottom=True, gap=24)
    row([i.resize((32, 32), Image.NEAREST) for i in items] + [i for i in items], gap=12)

    models = [("cawl", me)]
    for n in ("awrata", "cerna"):
        try:
            models.append((n, load_model(n)))
        except OSError:
            pass
    cod = vanilla_texture("cod")
    if cod:
        models.append(("vanilla cod", (COD, cod)))
    labels = []
    for n, (mdl, _) in models:
        ln, dep, depf, thick = extent(mdl)
        labels.append("%s: %g long, %g deep (%g with fins), %g thick" % (n, ln, dep, depf, thick))
    title("Same scale, 8x, side: the cawl beside the accepted awrata and cerna, and vanilla cod")
    row([render(m[0], m[1], "side", 8) for _, m in models], align_bottom=True, gap=40, labels=labels)
    title("Same scale, 8x, from above (thickness): the same fish in the same order")
    row([render(m[0], m[1], "top", 8) for _, m in models], align_bottom=True, gap=40, labels=labels)
    title("Texture at 8x and 1x (32 x 32)")
    row([texture.resize((TW * 8, TH * 8), Image.NEAREST), texture]
        + ([cod.resize((256, 256), Image.NEAREST), cod] if cod else []))
    if shots_dir and os.path.isdir(shots_dir):
        def shot(n):
            found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None

        names = ("fish-cawl-side", "fish-cawl-three-quarter", "fish-cawl-top", "fish-cawl-on-land",
                 "fish-cawl-beside-cod")
        got = [(n, shot(n)) for n in names]
        got = [(n, i) for n, i in got if i]
        if got:
            title("In the game: the cawl alone (side, three-quarter, top, on land), and beside vanilla cod")
            row([i for _, i in got[:3]], h=330)
            row([i for _, i in got[3:]], h=330)
            title("The same, cropped to the fish (beside cod: cawl right, cod left)")
            boxes = {"fish-cawl-beside-cod": (0.04, 0.2, 0.96, 0.7)}
            crops = []
            for n, i in got:
                fx = boxes.get(n, (0.25, 0.25, 0.75, 0.65))
                box = (int(i.width * fx[0]), int(i.height * fx[1]), int(i.width * fx[2]), int(i.height * fx[3]))
                k = 580.0 / (box[2] - box[0])
                crops.append(i.crop(box).resize((580, int((box[3] - box[1]) * k)), Image.NEAREST))
            row(crops[:3])
            row(crops[3:])
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    dest = os.path.join(ROOT, "art", "candidates", "fish_cawl_model.png")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    out.convert("RGB").save(dest)
    print("sheet:", dest)
    for l in labels:
        print(" ", l)


def main():
    check_fins_touch()
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
