"""The pixxispad (swordfish, Xiphias gladius) as a swimming mob: its 3D model and its texture.

Drawn from the reference photos in art/references/fish_pixxispad_refonly/ (list.tsv). What makes it a pixxispad:
  - a long, robust, rounded torpedo body, deepest just behind the head, tapering to a thin tail stalk;
  - the sword: the upper jaw drawn out into a long, flat, straight bill, about a third of the body's length, level with
    the body's axis, pale on top, darkest at the root, with darker edges so it shows against the water;
  - a short pointed lower jaw under the root of the sword;
  - a big eye, just above the line of the sword;
  - a tall, rigid, sickle-shaped first dorsal fin standing just behind the head;
  - long sickle pectoral fins set low on the flanks;
  - a huge crescent tail on a slim stalk with a single dark keel on each side;
  - no scales and no pelvic fins; a dark purple-bronze back fading to silvery-brown sides and a pale belly.

Colour: the accepted item icon's palette (art/src/fish_pixxispad_icon.py PAL), each colour lifted one small step in
lightness for the water (the hue and saturation kept), because under water the game greys and darkens everything.
Faces are shaded by a light ramp from the dark back to the pale belly, dithered only where two tones meet, so no face
is a flat fill and there are no random patches.

Rounded forms: every body section is an octagon in cross-section (a core box with a narrower strip on its back and
its belly), and the sections step down in 1 px steps toward the sword and the tail.

Size: the hitbox is 1.3 x 0.6 blocks, like the tonn's width. The model is 44 px long (2.75 blocks): a 12 px sword and
a 32 px body from the forehead to the tips of the tail (the tonn is 39 px, the lampuka 35, vanilla cod 15). The body
is 8 px deep and 6 px thick (the tonn 10 and 7, the lampuka 7 and 3, cod 4 and 2), so it is slimmer than the tonn
and much rounder than the lampuka; with the dorsal fin it stands 15 px tall, with the tail 14 px.

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, a root
child "body", "tail" (the slim back end: it sways gently) holding "tail_fin" (the crescent: it sways more). The sword
is part of "body", so it stays straight and level whatever the tail does.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/PixxispadModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/pixxispad.png    (64 x 64)
Run:   art/.venv/bin/python art/src/fish_pixxispad_model.py
Sheet: art/.venv/bin/python art/src/fish_pixxispad_model.py --sheet [SCREENSHOT_DIR]
       -> art/candidates/fish_pixxispad_model.png
"""
import colorsys
import glob
import math
import os
import re
import sys
import zipfile

from PIL import Image, ImageDraw

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
ART = os.path.join(ROOT, "art")
RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
FISH_JAVA = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "fish")
JAVA = os.path.join(FISH_JAVA, "PixxispadModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "pixxispad.png")
SHEET = os.path.join(ART, "candidates", "fish_pixxispad_model.png")
REFS = os.path.join(ART, "references", "fish_pixxispad_refonly")
TW, TH = 64, 64
CLEAR = (0, 0, 0, 0)


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# The accepted icon's palette (art/src/fish_pixxispad_icon.py PAL), copied so this script stands alone.
ICON = {
    "S": "#c4b4a4", "s": "#9a8a80", "u": "#6e5c5c",                       # sword: lit top, darker, shaded underside
    "H": "#8a7072", "h": "#7a6266", "1": "#664c5c", "2": "#4a3442",       # the back: sheen, rim, purple, dark purple
    "3": "#8c7876", "4": "#a69896", "5": "#ccc2ba",                       # sides: bronze-silver, silver, pale belly
    "g": "#7a6e72", "G": "#54484f", "o": "#24161e",                       # shade toward the belly, dark rim
    "e": "#0a080c", "j": "#7a6670", "p": "#5a4450",                       # eye, lower jaw, pectoral
    "D": "#8a7480", "d": "#5a4450", "T": "#8a7480", "t": "#5e4654",       # dorsal and tail: lit edge, membrane
    "k": "#1c1218",                                                       # keel
}
LIFT = 0.03    # one small step lighter for the water: lightness + 0.03, hue and saturation kept


def lift(h, dl=LIFT):
    r, g, b = (c / 255 for c in hx(h))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb(hh, min(1.0, ll + dl), ss)
    return (round(r * 255), round(g * 255), round(b * 255), 255)


PAL = {k: lift(v) for k, v in ICON.items()}
PAL["e"] = hx(ICON["e"]) + (255,)        # the eye stays as dark as the icon's: the only black on the fish
PAL["k"] = lift(ICON["k"], 0.03)
# two in-between tones the ramp needs (mixed from the icon's own colours, so the hue family holds)


def mixc(a, b, t=0.5):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3)) + (255,)


PAL["14"] = mixc(PAL["1"], PAL["4"], 0.35)    # where the purple back meets the silver flank
PAL["su"] = mixc(PAL["s"], PAL["u"], 0.5)     # the sword's edge
PAL["dd"] = mixc(PAL["d"], PAL["2"], 0.5)     # the base of the fins, nearest the dark back


# ---------------------------------------------------------------------------------------------------- shape
# A cube: (name, part, (x0, y0, z0), (w, h, d)), absolute model pixels at rest; head toward -z, y down, ground at 24.
# A part: name -> (parent, pivot relative to the parent's pivot (the root's is 0), rotation (x, y, z) in radians).
PEC_Y, PEC_Z, PEC_X = 22.0, -4.5, 3.05
PARTS = {
    "body": (None, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
    "right_fin": (None, (-PEC_X, PEC_Y, PEC_Z), (0.0, -0.3, 0.35)),
    "left_fin": (None, (PEC_X, PEC_Y, PEC_Z), (0.0, 0.3, -0.35)),
    "tail": (None, (0.0, 20.0, 10.0), (0.0, 0.0, 0.0)),
    "tail_fin": ("tail", (0.0, 0.0, 6.0), (0.0, 0.0, 0.0)),
}


def octagon(name, part, z0, d, w, h, cy=20.0):
    """A body section, rounded in cross-section: a core w x h with a strip (w - 2) x 1 on its back and its belly."""
    return [
        (name, part, (-w / 2, cy - h / 2, z0), (w, h, d)),
        (name + "_top", part, (-(w - 2) / 2, cy - h / 2 - 1, z0), (w - 2, 1, d)),
        (name + "_bot", part, (-(w - 2) / 2, cy + h / 2, z0), (w - 2, 1, d)),
    ]


CUBES = [
    # the sword: a flat bill, wider and deeper at its root, narrowing to a fine tip, centred on y 19.5 (the upper jaw)
    ("sword_tip", "body", (-0.5, 19.0, -23.0), (1, 1, 2)),
    ("sword", "body", (-1.0, 19.0, -21.0), (2, 1, 7)),
    ("sword_root", "body", (-1.5, 18.5, -14.0), (3, 2, 3)),
    ("jaw", "body", (-1.0, 20.5, -13.0), (2, 1, 2)),               # the short lower jaw, under the sword's root
]
CUBES += octagon("snout", "body", -11.0, 2, 4, 4)                # y 17..23: the forehead rising from the sword
CUBES += octagon("head", "body", -9.0, 4, 5, 5)                  # y 16.5..23.5
CUBES += octagon("trunk", "body", -5.0, 7, 6, 6)                 # y 16..24: the deepest, just behind the head
CUBES += octagon("mid", "body", 2.0, 4, 6, 5)                    # y 16.5..23.5: the body starts to taper
CUBES += octagon("rear", "body", 6.0, 4, 5, 4)                   # y 17..23
CUBES += [
    # fins: flat planes, their outlines cut by the texture; every one touches the body along its base
    ("dorsal", "body", (0.0, 9.0, -5.0), (0, 7, 6)),               # stands on the trunk's back (y 16), z -5..1
    ("anal", "body", (0.0, 23.0, 6.0), (0, 3, 4)),                 # hangs under the rear (y 23), z 6..10
    ("pec_r", "right_fin", (-PEC_X, PEC_Y, PEC_Z), (0, 5, 8)),
    ("pec_l", "left_fin", (PEC_X, PEC_Y, PEC_Z), (0, 5, 8)),
]
CUBES += octagon("rear2", "tail", 10.0, 3, 4, 2)                 # y 18..22: the narrowing in front of the stalk
CUBES += [
    ("stalk", "tail", (-1.0, 19.0, 13.0), (2, 2, 3)),
    ("keel", "tail", (-2.0, 20.0, 13.0), (4, 0, 3)),               # a flat plate through the stalk: one keel each side
    ("caudal", "tail_fin", (0.0, 13.0, 16.0), (0, 14, 6)),         # the crescent, y 13..27, z 16..22
]

# Fin outlines: rows top to bottom, columns front (-z) to back. L = lit leading edge, m = membrane, b = base (nearest
# the body), k = dark trailing edge, . = clear.
MASKS = {
    # tall rigid sickle, its tip swept back over its short base, a deeply concave trailing edge
    "dorsal": (9.0, -5.0, [
        "....Lk",
        "...Lk.",
        "..Lmk.",
        "..Lmk.",
        ".Lmmk.",
        ".Lmmmk",
        "Lbbbbk",
    ]),
    "anal": (23.0, 6.0, [
        "bbbb",
        ".Lmk",
        "..Lk",
    ]),
    # long, narrow, falcate: the front column touches the flank, the tip trails back and down
    "pec": (PEC_Y, PEC_Z, [
        "LL......",
        "bmLL....",
        ".bmmLL..",
        "..kmmmL.",
        "....kkmL",
    ]),
    # the huge crescent: two long thin lobes swept back from the stalk (rows 6-7 are the stalk's y 19..21)
    "caudal": (13.0, 16.0, [
        ".....L",
        "....Lk",
        "....Lk",
        "...Lk.",
        "..Lmk.",
        ".Lmk..",
        "bbk...",
        "bbk...",
        ".Lmk..",
        "..Lmk.",
        "...Lk.",
        "....Lk",
        "....Lk",
        ".....L",
    ]),
}


# ---------------------------------------------------------------------------------------------------- texture
def hash01(*vals):
    """A repeatable pseudo-random number in [0, 1) from integers (integer maths only, so every run is the same)."""
    h = 2166136261
    for v in vals:
        h = ((h ^ (v & 0xffffffff)) * 16777619) & 0xffffffff
    h ^= h >> 13
    h = (h * 0x5bd1e995) & 0xffffffff
    h ^= h >> 15
    return h / 4294967296.0


# The flank, from the ridge of the back (y 16) to the belly (y 24): dark purple, purple, purple-bronze rim, the meeting
# tone, bronze-silver, silver, pale. Between two stops the texel takes one or the other (a fixed dither), so the tones
# mix where they meet and nowhere else.
RAMP = [(16.0, "2"), (17.6, "2"), (18.6, "1"), (19.7, "h"), (20.5, "3"), (21.7, "4"), (23.0, "5"), (24.0, "5")]
FACE_SALT = {"top": 1, "bottom": 2, "west": 3, "east": 4, "north": 5, "south": 6}


def ramp(y, z, salt, x=0.0):
    yy = min(max(y, RAMP[0][0]), RAMP[-1][0])
    for (y0, a), (y1, b) in zip(RAMP, RAMP[1:]):
        if yy <= y1:
            t = (yy - y0) / (y1 - y0) if y1 > y0 else 0.0
            r = hash01(salt, int(math.floor(z * 2)), int(math.floor(y * 2)), int(math.floor(x * 2)))
            return PAL[b] if r < t else PAL[a]
    return PAL[RAMP[-1][1]]


EYE = {(19, -9), (19, -8), (20, -9), (20, -8)}   # (row centre y floored, z floored) on the head's sides: 2 x 2


def body_colour(name, face, x, y, z, w, h):
    base = name.split("_")[0]
    zi = int(math.floor(z))
    salt = FACE_SALT[face]
    if base in ("sword", "jaw") or name in ("sword_tip", "sword_root"):
        return sword_colour(name, face, x, y, z)
    if face == "top":
        # the back seen from above: dark purple along the ridge, purple toward the sides
        edge = abs(x) > (w / 2 - 1) if w > 2 else False
        if name.endswith("_top"):
            return PAL["1"] if edge else (PAL["1"] if hash01(7, zi, int(x * 2)) > 0.8 else PAL["2"])
        return PAL["2"] if hash01(8, zi, int(x * 2)) > 0.6 else PAL["1"]     # the core's shoulder, beside the strip
    if face == "bottom":
        if name.endswith("_bot"):
            return PAL["5"] if hash01(10, zi, int(x * 2)) > 0.25 else PAL["4"]
        return PAL["4"] if hash01(9, zi, int(x * 2)) > 0.3 else PAL["g"]
    if face in ("west", "east") and base == "head" and (int(math.floor(y)), zi) in EYE:
        return PAL["e"]
    # the back edge of the gill cover: one tone darker, low on the flank, two columns behind the eye
    if face in ("west", "east") and name == "trunk" and zi == -5 and y > 20.5:
        return PAL["g"]
    if base == "stalk" or base == "rear2":
        # the tail stalk darkens toward the tail, like the fish's
        c = ramp(y + 0.6, z, salt, x)
        return c
    return ramp(y, z, salt, x)


def sword_colour(name, face, x, y, z):
    zi = int(math.floor(z))
    if name == "jaw":
        if face == "bottom":
            return PAL["g"]
        if face == "north":
            return PAL["G"]
        return PAL["j"]
    if face == "top":
        # pale along the bill, darkest at the root, a little darker at the very tip
        if name == "sword_root":
            return PAL["su"] if zi >= -12 else PAL["s"]
        if name == "sword_tip":
            return PAL["s"]
        return PAL["s"] if zi >= -15 else PAL["S"]
    if face == "bottom":
        return PAL["u"]
    if face == "north":
        return PAL["su"]
    # the sides: the bill's edge, darker than its top so it outlines the pale bill against the water
    if name == "sword_root":
        return PAL["s"] if y < 19.5 else PAL["u"]
    return PAL["su"] if name == "sword_tip" or zi >= -16 else PAL["s"]


def fin_colour(name, x, y, z):
    key = "pec" if name.startswith("pec") else name
    if name == "keel":
        if abs(x) <= 1.0:
            return CLEAR             # inside the stalk: never seen
        return PAL["k"]
    y0, z0, grid = MASKS[key]
    r, c = int(math.floor(y - y0)), int(math.floor(z - z0))
    ch = grid[r][c] if 0 <= r < len(grid) and 0 <= c < len(grid[r]) else "."
    if ch == ".":
        return CLEAR
    if key == "caudal":
        return {"L": PAL["T"], "m": PAL["t"], "k": mixc(PAL["t"], PAL["2"], 0.45), "b": PAL["t"]}[ch]
    if key == "pec":
        return {"L": PAL["D"], "m": PAL["p"], "k": mixc(PAL["p"], PAL["2"], 0.45), "b": PAL["dd"]}[ch]
    return {"L": PAL["D"], "m": PAL["d"], "k": mixc(PAL["d"], PAL["2"], 0.45), "b": PAL["dd"]}[ch]


# ---------------------------------------------------------------------------------------------------- texture layout
def used_rect(cube):
    """The used part of a cube's UV footprint: (offset inside the footprint, size). Planes have only two faces."""
    _, _, _, (w, h, d) = cube
    if w == 0:
        return (0, d), (2 * d, h)
    if h == 0:
        return (d, 0), (2 * w, d)
    return (0, 0), (2 * d + 2 * w, d + h)


def pack():
    """Shelf packing, tallest first; returns texOffs for each cube."""
    sizes = [used_rect(c)[1] for c in CUBES]
    order = sorted(range(len(sizes)), key=lambda k: (-sizes[k][1], -sizes[k][0], k))
    pos, x, y, shelf = [None] * len(sizes), 0, 0, 0
    for k in order:
        w, h = sizes[k]
        if x + w > TW:
            x, y, shelf = 0, y + shelf, 0
        pos[k] = (x, y)
        x += w
        shelf = max(shelf, h)
    assert y + shelf <= TH, ("texture too small", y + shelf)
    return [(pos[k][0] - used_rect(CUBES[k])[0][0], pos[k][1] - used_rect(CUBES[k])[0][1]) for k in range(len(CUBES))]


def face_texels(cube, uv):
    """Every texel of every face: (face, u, v, x, y, z) with (x, y, z) the texel's centre on the model at rest.
    Follows ModelPart.Cube: top (u+d, v), bottom (u+d+w, v), west (u, v+d), north (u+d, v+d), east (u+d+w, v+d),
    south (u+2d+w, v+d)."""
    _, _, (x0, y0, z0), (w, h, d) = cube
    u, v = uv
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
    uvs = pack()
    img = Image.new("RGBA", (TW, TH), CLEAR)
    owner = {}
    for cube, uv in zip(CUBES, uvs):
        name, _, _, (w, h, d) = cube
        for face, u, v, x, y, z in face_texels(cube, uv):
            assert 0 <= u < TW and 0 <= v < TH, (name, face, u, v)
            assert owner.setdefault((u, v), name) == name, ("texture overlap", name, owner[(u, v)], u, v)
            col = fin_colour(name, x, y, z) if (w == 0 or h == 0) else body_colour(name, face, x, y, z, w, h)
            img.putpixel((u, v), col)
    return img


# ---------------------------------------------------------------------------------------------------- Java
def f(v):
    s = ("%.4f" % v).rstrip("0")
    if s.endswith("."):
        s += "0"
    if s == "-0.0":
        s = "0.0"
    return s + "F"


def part_origin(part):
    parent, pivot, _ = PARTS[part]
    if parent is None:
        return pivot
    px, py, pz = part_origin(parent)
    return (px + pivot[0], py + pivot[1], pz + pivot[2])


def java_source():
    uvs = pack()
    out = [
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
        " * The pixxispad (swordfish): a long, rounded torpedo with a long, flat, straight sword held level with the body, a",
        " * short lower jaw, a big eye, a tall sickle dorsal fin just behind the head, long sickle pectoral fins set low, a",
        " * slim keeled tail stalk and a huge crescent tail; a dark purple-bronze back over silvery-brown sides and a pale",
        " * belly. 44 px long (a 12 px sword and a 32 px body), 8 px deep, 6 px thick, head toward -z, the ground at y 24.",
        " * The sword is part of \"body\", so it never bends; \"tail\" (the stalk) sways gently and \"tail_fin\" more.",
        " * Made by art/src/fish_pixxispad_model.py (don't edit by hand). Texture: textures/entity/fish/pixxispad.png (64 x 64).",
        " */",
        "public class PixxispadModel extends FishModel {",
        "    public PixxispadModel(ModelPart root) {",
        "        super(root);",
        "    }",
        "",
        "    public static LayerDefinition createBodyLayer() {",
        "        MeshDefinition mesh = new MeshDefinition();",
        "        PartDefinition root = mesh.getRoot();",
    ]
    for part, (parent, pivot, rot) in PARTS.items():
        ox, oy, oz = part_origin(part)
        lines = []
        for cube, (u, v) in zip(CUBES, uvs):
            name, cp, (x0, y0, z0), (w, h, d) = cube
            if cp != part:
                continue
            lines.append(f"            /* {name} */ .texOffs({u}, {v}).addBox({f(x0 - ox)}, {f(y0 - oy)}, {f(z0 - oz)}, "
                         f"{f(w)}, {f(h)}, {f(d)})")
        pose = (f"PartPose.offsetAndRotation({f(pivot[0])}, {f(pivot[1])}, {f(pivot[2])}, {f(rot[0])}, {f(rot[1])}, {f(rot[2])})"
                if any(rot) else f"PartPose.offset({f(pivot[0])}, {f(pivot[1])}, {f(pivot[2])})")
        has_child = any(p[0] == part for p in PARTS.values())
        var = f"PartDefinition {part} = " if has_child else ""
        out.append(f"        {var}{parent or 'root'}.addOrReplaceChild(\"{part}\", CubeListBuilder.create()")
        lines[-1] += ","
        out += lines
        out.append(f"            {pose});")
    out += [f"        return LayerDefinition.create(mesh, {TW}, {TH});", "    }", "}", ""]
    return "\n".join(out)


# ---------------------------------------------------------------------------------------------------- offline views
def parse_java(path):
    """Read a generated or vanilla-style model class: parts (name -> parent, pivot, rotation) and cubes with texOffs."""
    src = open(path, encoding="utf-8").read()
    parts, cubes = {}, []
    for m in re.finditer(r'(\w+)\.addOrReplaceChild\("(\w+)", CubeListBuilder\.create\(\)(.*?)PartPose\.(offset|offsetAndRotation)\(([^)]*)\)\);',
                         src, re.S):
        owner, name, body, _, args = m.groups()
        nums = [float(a.strip().rstrip("F")) for a in args.split(",")]
        piv, rot = tuple(nums[:3]), tuple(nums[3:6]) if len(nums) > 3 else (0.0, 0.0, 0.0)
        parts[name] = (None if owner == "root" else owner, piv, rot)
        for c in re.finditer(r"texOffs\((\d+), (\d+)\)\.addBox\(([^)]*)\)", body):
            u, v = int(c.group(1)), int(c.group(2))
            x, y, z, w, h, d = [float(a.strip().rstrip("F")) for a in c.group(3).split(",")]
            cubes.append((name, (u, v), (x, y, z), (int(w), int(h), int(d))))
    return parts, cubes


def rot_zyx(p, rot):
    """ModelPart's rotation: x first, then y, then z (Quaternionf.rotationZYX)."""
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


def to_model(parts, part, p):
    """A point in a part's own space -> model space, through its parents."""
    while part:
        parent, piv, rot = parts[part]
        p = rot_zyx(p, rot)
        p = (p[0] + piv[0], p[1] + piv[1], p[2] + piv[2])
        part = parent
    return p


SHADE = {"top": 1.0, "bottom": 0.5, "west": 0.8, "east": 0.8, "north": 0.7, "south": 0.7}


def render(parts, cubes, texture, view, scale, sub=4):
    """A model drawn orthographically: 'side' (from -x... head to the left), 'top' (from above, head left) or 'three'
    (a front three-quarter from above). Returns (RGBA image, model point -> pixel function) cropped to the fish."""
    yaw, pitch = {"side": (0.0, 0.0), "top": (0.0, 90.0), "three": (35.0, 25.0)}[view]
    cy_, sy_ = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))

    def project(p):
        x, y, z = p
        z2, x2 = z * cy_ - x * sy_, z * sy_ + x * cy_
        y3, d3 = y * cp - x2 * sp, y * sp + x2 * cp
        return z2, y3, d3                     # screen x, screen y, depth (smaller = nearer: the -x side faces us)

    pts = []
    for name, part, (u, v), (x0, y0, z0), (w, h, d) in cubes:
        cube = (name, part, (x0, y0, z0), (w, h, d))
        for face, tu, tv, x, y, z in face_texels(cube, (u, v)):
            col = texture.getpixel((tu % texture.size[0], tv % texture.size[1]))
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
                    pts.append((project(to_model(parts, part, p)), col))
    return pts


def raster(pts, scale, box=None):
    xs = [q[0][0] for q in pts]
    ys = [q[0][1] for q in pts]
    minx, miny, maxx, maxy = box or (min(xs) - 1, min(ys) - 1, max(xs) + 1, max(ys) + 1)
    wpx, hpx = int((maxx - minx) * scale) + 1, int((maxy - miny) * scale) + 1
    img = Image.new("RGBA", (wpx, hpx), CLEAR)
    px_ = img.load()
    depth = {}
    r = max(1, int(math.ceil(scale / 8 + 0.5)))
    for (sx, sy, sd), col in pts:
        cx, cy = int((sx - minx) * scale), int((sy - miny) * scale)
        for ox in range(-r, r):
            for oy in range(-r, r):
                key = (cx + ox, cy + oy)
                if 0 <= key[0] < wpx and 0 <= key[1] < hpx and sd < depth.get(key, 1e9):
                    depth[key] = sd
                    px_[key] = col + (255,)
    return img


def own_model():
    uvs = pack()
    parts = {k: (p, piv, rot) for k, (p, piv, rot) in PARTS.items()}
    cubes = []
    for cube, uv in zip(CUBES, uvs):
        name, part, (x0, y0, z0), size = cube
        ox, oy, oz = part_origin(part)
        cubes.append((name, part, uv, (x0 - ox, y0 - oy, z0 - oz), size))
    return parts, cubes


def java_model(path):
    parts, cubes = parse_java(path)
    return parts, [(n, n, uv, pos, size) for n, uv, pos, size in cubes]


# vanilla cod (CodModel, 26.3) with its real texOffs, part-local, for scale
COD = ({"body": (None, (0, 22, 0), (0, 0, 0)), "head": (None, (0, 22, 0), (0, 0, 0)), "nose": (None, (0, 22, -3), (0, 0, 0)),
        "right_fin": (None, (-1, 23, 0), (0, 0, -0.7854)), "left_fin": (None, (1, 23, 0), (0, 0, 0.7854)),
        "tail_fin": (None, (0, 22, 7), (0, 0, 0)), "top_fin": (None, (0, 20, 0), (0, 0, 0))},
       [("body", "body", (0, 0), (-1, -2, 0), (2, 4, 7)), ("head", "head", (11, 0), (-1, -2, -3), (2, 4, 3)),
        ("nose", "nose", (0, 0), (-1, -2, -1), (2, 3, 1)),
        ("right_fin", "right_fin", (22, 1), (-2, 0, -1), (2, 0, 2)), ("left_fin", "left_fin", (22, 4), (0, 0, -1), (2, 0, 2)),
        ("tail_fin", "tail_fin", (22, 3), (0, -2, 0), (0, 4, 4)), ("top_fin", "top_fin", (20, -6), (0, -1, -1), (0, 1, 6))])


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


def view(model, texture, v, scale, box=None):
    parts, cubes = model
    return raster(render(parts, [(n, p, uv, pos, s) for n, p, uv, pos, s in cubes], texture, v, scale), scale, box)


# ---------------------------------------------------------------------------------------------------- sheet
def sheet(shots_dir):
    sys.path.insert(0, os.path.join(ART, "tools"))
    from font import label_font
    font, small = label_font(18), label_font(14)
    bg, ink, head = (52, 52, 56), (235, 235, 235), (250, 210, 120)
    W = 1900
    blocks = []

    def band(images, labels=None, h=None, gap=16, bottom=True):
        hh = h or max(i.height for i in images)
        b = Image.new("RGB", (W, hh + 24), bg)
        d = ImageDraw.Draw(b)
        x = 10
        for k, im in enumerate(images):
            y = 22 + (hh - im.height if bottom else 0)
            b.paste(im.convert("RGB") if im.mode != "RGBA" else im, (x, y), im if im.mode == "RGBA" else None)
            if labels:
                d.text((x, 2), labels[k], fill=ink, font=small)
            x += im.width + gap
        return b

    tex = Image.open(TEXTURE).convert("RGBA")
    me = own_model()

    # references
    refs, names = [], []
    for n in ("sw09_2.jpg", "sw10_linn.jpg", "sw04_drawing.jpg", "sw06_inat.jpg"):
        p = os.path.join(REFS, n)
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im.thumbnail((440, 280))
            refs.append(im)
            names.append(n + " (reference only)")
    blocks.append(("References (art/references/fish_pixxispad_refonly, list.tsv)", band(refs, names)))

    # the accepted icon, bucket and egg beside the model
    item = os.path.join(RES, "textures", "item")
    vb = Image.open(os.path.join(ART, ".vanilla", "item", "cod_bucket.png")).convert("RGBA")
    bucket = vb.copy()
    bucket.alpha_composite(Image.open(os.path.join(item, "pixxispad_bucket.png")).convert("RGBA"))
    flats = [Image.open(os.path.join(item, "pixxispad.png")).convert("RGBA"), bucket,
             Image.open(os.path.join(item, "pixxispad_spawn_egg.png")).convert("RGBA")]
    ims = []
    for fl in flats:
        t = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
        t.alpha_composite(fl.resize((128, 128), Image.NEAREST))
        ims.append(t)
    side8 = view(me, tex, "side", 8)
    three8 = view(me, tex, "three", 8)
    blocks.append(("The accepted icon, bucket and spawn egg (8x) beside the model (offline, side and three-quarter, 8 px a pixel)",
                   band(ims + [side8, three8], ["icon (accepted)", "bucket (accepted)", "egg (accepted)", "model, side",
                                                "model, three-quarter"])))

    # the model at the same scale as the accepted tonn and lampuka and vanilla cod
    row, labels = [], []
    tonn_tex = Image.open(os.path.join(RES, "textures", "entity", "fish", "tonn.png")).convert("RGBA")
    lam_tex = Image.open(os.path.join(RES, "textures", "entity", "fish", "lampuka.png")).convert("RGBA")
    cod_tex = vanilla_texture("cod")
    models = [("PIXXISPAD", me, tex), ("tonn (accepted)", java_model(os.path.join(FISH_JAVA, "TonnModel.java")), tonn_tex),
              ("lampuka (accepted)", java_model(os.path.join(FISH_JAVA, "LampukaModel.java")), lam_tex)]
    if cod_tex is not None:
        models.append(("vanilla cod", COD, cod_tex))
    for lab, m, t in models:
        row.append(view(m, t, "side", 6))
        labels.append(lab)
    blocks.append(("Same scale (6 screen px a model pixel), side views", band(row, labels)))
    row = [view(m, t, "top", 6) for _, m, t in models]
    blocks.append(("Same scale, from above", band(row, [l for l, _, _ in models], bottom=False)))
    row = [view(m, t, "three", 6) for _, m, t in models]
    blocks.append(("Same scale, three-quarter", band(row, [l for l, _, _ in models])))

    # the texture
    t8 = Image.new("RGBA", (TW * 6, TH * 6), (200, 200, 200, 255))
    t8.alpha_composite(tex.resize((TW * 6, TH * 6), Image.NEAREST))
    ic = Image.new("RGBA", (16 * 6, 16 * 6), (200, 200, 200, 255))
    ic.alpha_composite(flats[0].resize((96, 96), Image.NEAREST))
    sw = Image.new("RGB", (560, 30 * 3 + 10), bg)
    d = ImageDraw.Draw(sw)
    for i, (lab, keys, pal) in enumerate((("icon", "21h345", {k: hx(ICON[k]) for k in ICON}),
                                         ("model", "21h345", PAL),
                                         ("model fins/sword", "DdTtSs", PAL))):
        d.text((4, 8 + i * 30), lab, fill=ink, font=small)
        for j, k in enumerate(keys):
            d.rectangle((150 + j * 66, 4 + i * 30, 210 + j * 66, 28 + i * 30), fill=pal[k][:3])
    blocks.append(("Texture (64 x 64 at 6x), the icon at 6x, and the icon's ramp beside the lifted model ramp",
                   band([t8, ic, sw], ["pixxispad.png", "icon", "palette"], bottom=False)))

    # in-game crops
    if shots_dir and os.path.isdir(shots_dir):
        names = {n.split("_", 1)[-1]: n for n in sorted(os.listdir(shots_dir))}
        want = ["fish-pixxispad-side.png", "fish-pixxispad-three-quarter.png", "fish-pixxispad-top.png",
                "fish-pixxispad-beside-cod.png", "fish-pixxispad-on-land.png", "fish-04-tank-tonn-murina-ziemel.png"]
        got = [(k, Image.open(os.path.join(shots_dir, names[k])).convert("RGB")) for k in want if k in names]
        for i in range(0, len(got), 2):
            grp = got[i:i + 2]
            ims = []
            for _, s in grp:
                s = s.copy()
                s.thumbnail((920, 520))
                ims.append(s)
            blocks.append(("In game: " + ", ".join(k[:-4] for k, _ in grp), band(ims, [k[:-4] for k, _ in grp])))

    H = sum(b.height + 34 for _, b in blocks) + 44
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 10), "Pixxispad (swordfish) 3D model and entity texture", fill=ink, font=label_font(22))
    y = 44
    for title, b in blocks:
        d.text((10, y), title, fill=head, font=font)
        out.paste(b, (0, y + 28))
        y += b.height + 34
    out.save(SHEET)
    print("wrote", os.path.relpath(SHEET, ROOT))


def stats():
    """Mean luminance of the opaque texels: the model's texture against the icon's."""
    def mean_l(im):
        px = [p for p in im.convert("RGBA").get_flattened_data() if p[3] > 0]
        return sum(0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2] for p in px) / len(px)
    icon = Image.open(os.path.join(RES, "textures", "item", "pixxispad.png"))
    return mean_l(Image.open(TEXTURE)), mean_l(icon)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--sheet":
        sheet(sys.argv[2] if len(sys.argv) > 2 else None)
        return
    draw_texture().save(TEXTURE)
    with open(JAVA, "w", encoding="utf-8") as fh:
        fh.write(java_source())
    t, i = stats()
    print("wrote", os.path.relpath(TEXTURE, ROOT), "and", os.path.relpath(JAVA, ROOT),
          "; mean luminance texture %.0f, icon %.0f" % (t, i))


if __name__ == "__main__":
    main()
