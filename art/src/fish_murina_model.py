"""The murina (Mediterranean moray, Muraena helena) as a swimming mob: its 3D model, its texture and its eel swimming.

Drawn from the reference photos in art/references/fish_murina_refonly/ (list.tsv; o01-o06 out of water for the true
colour). What makes it a murina:
  - a long, snake-like eel: round in front, flattened from side to side toward the tail;
  - no pectoral fins; one continuous low fin from just behind the head along the back, round the tail tip and forward
    under the belly to the middle of the body, in the same spotted skin as the body;
  - a big head that stands out from a narrower neck: a raised crown behind the eye, a long snout, a wide mouth held
    open (a dark gape running back past the eye), a jutting lower jaw, a small pale eye near the front, high on the
    head, and short tube nostrils at the tip of the snout;
  - violet-brown, densely spotted with cream; the head carries no spots, so the pale eye stays its only bright mark.
The palette is the accepted item icon's (art/src/fish_murina_icon.py PAL), lifted a step because the water greys and
darkens everything. Every face shades from a lit top to a dark underside; no face is a flat fill (a fixed hash shifts
texels one tone, so reruns are byte-identical).

Size: the hitbox is 0.9 x 0.3 blocks. The murina is 32 px long (2 blocks: snout tip z -14 to tail tip z 18), the
longest of the set (cerna 29, cod 15), but only 4 px deep and 3 px thick along the body, and 5 px deep and 4 px thick
at the head. Body depth to length is 4 to 32 (0.13), against the cerna's 0.42 and the sardina's 0.27: a thin eel.
One texture pixel per model pixel, like vanilla's fish.

Swimming: the body is a chain of five sections (head and neck "body", then seg1, seg2, seg3 and the tail), each the
child of the one before. MurinaModel.setupAnim sends a sideways wave down the chain: every section turns a little
more than the one before and a little later, so an S travels from the neck to the tail while the head stays nearly
steady. Each section after the first carries a 1 px collar of its own cross-section (0.05 px smaller all round) that
sits inside the section in front, so the
outside of a bend never opens a gap. The renderer's whole-body wiggle is 0 (MimContentClient), as the wave does it.

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, a root
child "body". There is no root "tail" or "tail_fin": the model moves its own sections.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/MurinaModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/murina.png    (64 x 64)
With --sheet SCREENSHOT_DIR also writes the compare sheet art/candidates/fish_murina_model.png (previews go to the
folder given with --preview DIR).

Run:  art/.venv/bin/python art/src/fish_murina_model.py [--preview DIR] [--sheet SCREENSHOT_DIR]
"""
import colorsys
import glob
import math
import os
import sys
import zipfile

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "fish",
                    "MurinaModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "murina.png")
TW, TH = 64, 64


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


def lift(c, k):
    """One step lighter for the water: brightness scaled by k, saturation kept (hue unchanged)."""
    h, s, v = colorsys.rgb_to_hsv(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
    r, g, b = colorsys.hsv_to_rgb(h, s, min(1.0, v * k))
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)), 255)


# The accepted murina item icon's palette (art/src/fish_murina_icon.py PAL), copied here so the model never drifts.
ICON = {
    "1": "#8c6a6a", "2": "#765660", "3": "#62464e", "4": "#503a40", "5": "#433036",
    "k": "#705660", "o": "#2a1a1f",
    "C": "#e2d09c", "c": "#b49c84", "d": "#806a6c",
    "E": "#f0e8bc", "L": "#866670", "l": "#5c4650", "M": "#200f14",
}
IC = {k: hexc(v) for k, v in ICON.items()}

# Round 2 (critic 2026-11-18: "the darkest fish ... under water a dark grey-blue mass"): every body, fin, jaw and spot
# tone is raised by about this much brightness on top of round 1, keeping its hue; the gape stays near-black.
BRIGHTER = 34


def up(c, d=BRIGHTER):
    """Raise a colour's brightness by d (0-255 scale) with its hue and saturation kept."""
    h, s, v = colorsys.rgb_to_hsv(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
    r, g, b = colorsys.hsv_to_rgb(h, s, min(1.0, v + d / 255.0))
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)), 255)

# body ramp, 0 lightest (the lit top) to 5 darkest (the underside): the icon's five tones each lifted about one step,
# with one more light above them for the top faces
RAMP = [up(c) for c in (lift(IC["1"], 1.36), lift(IC["1"], 1.18), lift(IC["2"], 1.22), lift(IC["3"], 1.26),
                         lift(IC["4"], 1.26), lift(IC["5"], 1.22))]
PAL = {
    "k": up(lift(IC["k"], 1.45)),          # the lit rim of the back fin
    "o": up(lift(IC["o"], 1.5)),           # the shaded rim under the jaw and the belly fin
    "C": up(IC["C"]),                  # cream spots in the light
    "c": up(lift(IC["c"], 1.08)),          # cream spots in the half light
    "d": up(lift(IC["d"], 1.2)),           # spots in the shade
    "E": hexc("#fffbe8"),              # the small pale eye (the icon's, raised so it shows under water)
    "L": up(lift(IC["L"], 1.25)),          # the upper lip and the tube nostrils
    "l": up(lift(IC["l"], 1.25)),          # the lower jaw
    "M": lift(IC["M"], 1.3),           # the open mouth (dark violet, not black)
    "m": lift(IC["M"], 1.9),           # the roof and floor of the mouth near the front, a little lighter
    ".": (0, 0, 0, 0),
}
CLEAR = PAL["."]


# --- the model -------------------------------------------------------------------------------------------------------
# Parts: name -> (parent, pivot (absolute model pixels), (xRot, yRot, zRot)). Each section turns about its front
# joint. Absolute coordinates: x across, y down (24 = ground), z head (-) to tail (+).
PARTS = {
    "body": (None, (0.0, 21.0, 0.0), (0.0, 0.0, 0.0)),
    "seg1": ("body", (0.0, 21.0, 0.0), (0.0, 0.0, 0.0)),
    "seg2": ("seg1", (0.0, 21.0, 5.0), (0.0, 0.0, 0.0)),
    "seg3": ("seg2", (0.0, 21.0, 10.0), (0.0, 0.0, 0.0)),
    "tail": ("seg3", (0.0, 21.0, 14.0), (0.0, 0.0, 0.0)),
}
CHAIN = ("body", "seg1", "seg2", "seg3", "tail")

# Cubes: (name, part, (x0, y0, z0) absolute, (w, h, d)). Texture places are packed automatically below.
SHAPES = [
    # the head, rounded by steps: tube nostrils, the long snout, the upper jaw (the eye on it), a brow step, then the
    # big head with its raised crown; the open mouth (a dark inner block) between the upper jaw and the jutting lower jaw
    ("nose", "body", (-1.0, 19.0, -14.0), (2, 1, 1)),
    ("snout", "body", (-1.0, 19.0, -13.0), (2, 2, 2)),
    ("upjaw", "body", (-1.5, 19.0, -11.0), (3, 2, 3)),
    ("brow", "body", (-1.5, 18.0, -9.0), (3, 1, 1)),
    ("head", "body", (-2.0, 18.0, -8.0), (4, 5, 4)),
    ("mouth", "body", (-1.0, 21.0, -11.0), (2, 1, 3)),
    ("lojaw_tip", "body", (-1.0, 22.0, -12.0), (2, 1, 1)),
    ("lojaw", "body", (-1.5, 22.0, -11.0), (3, 1, 3)),
    ("neck", "body", (-1.5, 19.0, -4.0), (3, 4, 4)),
    ("fin_neck", "body", (0.0, 18.0, -4.0), (0, 1, 4)),
    # the body sections, each with a collar of its own full cross-section reaching into the section in front (drawn
    # 0.05 px smaller all round, so it never shares a face with the section it sits in)
    ("seg1", "seg1", (-1.5, 19.0, 0.0), (3, 4, 5)),
    ("collar1", "seg1", (-1.5, 19.0, -1.0), (3, 4, 1)),
    ("fin_seg1", "seg1", (0.0, 18.0, 0.0), (0, 1, 5)),
    ("seg2", "seg2", (-1.0, 19.0, 5.0), (2, 4, 5)),
    ("collar2", "seg2", (-1.0, 19.0, 4.0), (2, 4, 1)),
    ("fin_seg2", "seg2", (0.0, 18.0, 5.0), (0, 1, 5)),
    ("anal_seg2", "seg2", (0.0, 23.0, 6.0), (0, 1, 4)),
    ("seg3", "seg3", (-1.0, 19.5, 10.0), (2, 3, 4)),
    ("collar3", "seg3", (-1.0, 19.5, 9.0), (2, 3, 1)),
    ("fin_seg3", "seg3", (0.0, 18.5, 10.0), (0, 1, 4)),
    ("anal_seg3", "seg3", (0.0, 22.5, 10.0), (0, 1, 4)),
    # the flattened tail (its first pixel is its collar, inside seg3) and the fin running round its tip
    ("tail", "tail", (-0.5, 20.0, 13.0), (1, 2, 4)),
    ("fin_tail", "tail", (0.0, 19.0, 14.0), (0, 4, 4)),
]
COLLARS = ("collar1", "collar2", "collar3")
HEAD = ("nose", "snout", "upjaw", "brow", "head", "mouth", "lojaw_tip", "lojaw")

# The fin round the tail tip, rows y 19..22, columns z 14..17: the back fin above, the belly fin below, the rounded tip.
# 'k' lit rim, 'f' mid fin, 'g' shaded fin, 'o' dark rim, '.' clear (the body's tail block covers rows 20-21, z 14-16).
TAIL_FIN = [
    "kkk.",
    "ffff",
    "gggg",
    "ooo.",
]


def hash01(*vals):
    """A repeatable pseudo-random number in [0, 1) from integers (no floating-point maths, so every run is the same)."""
    h = 2166136261
    for v in vals:
        h = ((h ^ (v & 0xffffffff)) * 16777619) & 0xffffffff
    for _ in range(2):          # a full avalanche, so neighbouring texels don't come out alike
        h ^= h >> 16
        h = (h * 0x85ebca6b) & 0xffffffff
        h ^= h >> 13
        h = (h * 0xc2b2ae35) & 0xffffffff
        h ^= h >> 16
    return h / 4294967296.0


def tone(shade, *key):
    """A body tone, shifted one step lighter or darker at random so no face is a flat fill."""
    r = hash01(*key)
    if r < 0.18:
        shade -= 1
    elif r > 0.80:
        shade += 1
    return RAMP[max(0, min(5, shade))]


def spot(shade):
    """The cream spot's colour where the light is `shade` (0 lit .. 5 dark)."""
    if shade <= 2:
        return PAL["C"]
    if shade == 3:
        return PAL["c"]
    return PAL["d"]


FACE_SALT = {"top": 1, "bottom": 2, "north": 3, "south": 4, "west": 5, "east": 6}
EYE = (19, -10)          # (y row, z column) of the eye on both sides of the upper jaw
GAPE = {(21, -8), (21, -7)}  # the corner of the mouth, cut back into the head's side past the eye


def raw_spot(face, xi, yi, zi):
    if zi < -3:
        return False
    return hash01(17, FACE_SALT[face], xi, yi, zi) < (0.16 if zi < -1 else 0.42)


def spotted(face, xi, yi, zi):
    """Is this body texel a cream spot? Dense, fine spots behind the head, thinning out on the neck and never on the
    head, so the eye stays its only bright mark. A spot never follows another along the body, and at most two stand
    one above the other (longer runs read as bars and bands); they touch at the corners, a broken net of spots."""
    return (raw_spot(face, xi, yi, zi) and not raw_spot(face, xi, yi, zi - 1)
            and not (raw_spot(face, xi, yi - 1, zi) and raw_spot(face, xi, yi - 2, zi)))


def half_spot(face, xi, yi, zi):
    """A spot left out to keep the others apart: a paler patch of skin, so the net of spots stays dense."""
    return raw_spot(face, xi, yi, zi) and not spotted(face, xi, yi, zi)


def spot_tone(shade, face, xi, yi, zi):
    """A spot's colour: the cream takes the light, and one spot in four is a step duller, so they don't read as dots."""
    if hash01(19, FACE_SALT[face], xi, yi, zi) < 0.25:
        shade += 1
    return spot(shade)


def side_texel(name, face, x, y, z, y0, h):
    """A texel on a side (west/east), front (north) or back (south) face."""
    yi, zi, xi = int(math.floor(y)), int(math.floor(z)), int(math.floor(x * 2))
    rel = (y - y0) / h                                   # 0 at the top of the block, 1 at its underside
    shade = 1 + int(round(rel * 4 - 0.5)) if h > 1 else 3
    if face in ("north", "south"):
        shade += 1                                       # the steps' ends turn away from the light
    side = face in ("west", "east")
    if name == "mouth":
        return PAL["M"]
    if name == "nose":
        return PAL["L"] if face != "south" else RAMP[2]
    if side and (yi, zi) == EYE and name == "upjaw":
        return PAL["E"]
    if side and name in HEAD and abs(yi - EYE[0]) <= 1 and abs(zi - EYE[1]) <= 1 and (yi, zi) != EYE:
        return RAMP[2]                                   # the eye's 8 neighbours: one even mid tone, no ring
    if side and (yi, zi) in GAPE and name == "head":
        return PAL["M"]
    if face == "north" and name == "head" and yi == 21:
        return PAL["M"]                                  # the gape runs round the corner of the head's front step
    if name in ("snout", "upjaw") and yi == 20:
        return PAL["L"] if face != "south" else RAMP[3]  # the upper lip along the mouth
    if name in ("lojaw", "lojaw_tip"):
        return PAL["L"] if face != "south" else PAL["o"]      # the pale lower lip under the dark gape
    if name in HEAD:
        # the head: plain skin a shade lighter than the body and without spots, so it reads apart from the spotted
        # neck; the texels round the eye stay one even mid tone, so the pale eye shows and nothing beside it does
        return tone(max(0, shade - 1), FACE_SALT[face], xi, yi, zi)
    if name in COLLARS:
        return tone(shade, FACE_SALT[face], xi, yi, zi)   # seen only in a bend: the body's own shade, no spots
    if spotted(face, xi, yi, zi):
        return spot_tone(shade, face, xi, yi, zi)
    if half_spot(face, xi, yi, zi):
        return RAMP[max(0, shade - 2)]
    return tone(shade, FACE_SALT[face], xi, yi, zi)


def body_texel(name, face, x, y, z, x0, y0, z0, w, h, d):
    yi, zi, xi = int(math.floor(y)), int(math.floor(z)), int(math.floor(x * 2))
    if face == "top":
        if name == "mouth":
            return PAL["M"]
        if name == "lojaw_tip":
            return PAL["m"]                              # the floor of the open mouth, seen at its front
        if name == "lojaw":
            return PAL["M"]
        if name == "nose":
            return PAL["L"]
        if name in HEAD:
            return tone(0 if abs(x) < 1.0 else 1, 1, xi, zi)
        if name in COLLARS:
            return tone(2, 1, xi, zi)
        if spotted(face, xi, yi, zi):
            return spot_tone(1, face, xi, yi, zi)
        return tone(0 if abs(x) < 1.0 else 1, 1, xi, zi)
    if face == "bottom":
        if name in ("snout", "upjaw"):
            return PAL["m"] if name == "snout" else PAL["M"]   # the roof of the open mouth
        if name == "mouth":
            return PAL["M"]
        if name in ("lojaw", "lojaw_tip", "head"):
            return PAL["o"] if hash01(2, xi, zi) < 0.5 else RAMP[5]
        if name in COLLARS:
            return RAMP[5]
        if spotted(face, xi, yi, zi):
            return PAL["d"]
        return tone(5, 2, xi, zi)
    return side_texel(name, face, x, y, z, y0, h)


def fin_texel(name, face, x, y, z, y0, h, d):
    """The low fin: the same spotted skin as the body, lit above (the back fin), shaded below (the belly fin)."""
    yi, zi = int(math.floor(y)), int(math.floor(z))
    salt = FACE_SALT[face]
    if name == "fin_tail":
        ch = TAIL_FIN[yi - 19][zi - 14]
        if ch == ".":
            return CLEAR
        if ch in "fg":
            base = 2 if ch == "f" else 4
            return spot(base) if hash01(23, salt, yi, zi) < 0.2 else tone(base, salt, 7, yi, zi)
        return PAL[ch] if hash01(29, salt, yi, zi) < 0.6 else tone(1 if ch == "k" else 5, salt, 9, yi, zi)
    if name.startswith("fin_"):
        r = hash01(31, salt, zi)
        return PAL["c"] if r < 0.22 else (PAL["k"] if r < 0.6 else tone(1, salt, 3, zi))
    # the belly fin
    r = hash01(37, salt, zi)
    return PAL["d"] if r < 0.18 else (PAL["o"] if r < 0.5 else tone(5, salt, 5, zi))


# --- texture layout (the vanilla box UV layout) ----------------------------------------------------------------------
def footprint(w, h, d):
    """Width and height of a cube's used texture area (planes leave out the faces they don't have)."""
    if w == 0:
        return 2 * d, h
    return 2 * (d + w), d + h


def pack():
    """Shelf packing, tallest first (ties by listing order), in a 64 x 64 sheet: a fixed order, so it never changes."""
    order = sorted(range(len(SHAPES)), key=lambda i: (-footprint(*SHAPES[i][3])[1], i))
    places = {}
    x = y = shelf = 0
    for i in order:
        fw, fh = footprint(*SHAPES[i][3])
        if x + fw > TW:
            x, y, shelf = 0, y + shelf, 0
        places[i] = (x, y)
        x += fw
        shelf = max(shelf, fh)
    assert y + shelf <= TH, "texture too small"
    return [(n, p, places[i], pos, size) for i, (n, p, pos, size) in enumerate(SHAPES)]


CUBES = pack()


def tex_offset(cube):
    """texOffs for a cube whose used texture area starts at (U, V)."""
    _, _, (U, V), _, (w, h, d) = cube
    if w == 0:
        return U, V - d
    return U, V


def face_texels(cube):
    """Every texel of every face: (face, u, v, x, y, z), with (x, y, z) the texel's centre on the model, absolute.
    The mapping follows ModelPart.Cube: top (u+d, v), bottom (u+d+w, v), west (u, v+d), north (u+d, v+d),
    east (u+d+w, v+d), south (u+2d+w, v+d)."""
    _, _, _, (x0, y0, z0), (w, h, d) = cube
    u, v = tex_offset(cube)
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
        for face, u, v, x, y, z in face_texels(cube):
            assert 0 <= u < TW and 0 <= v < TH, (name, face, u, v)
            assert owner.setdefault((u, v), name) == name, ("texture overlap", name, owner[(u, v)], u, v)
            if w == 0:
                col = fin_texel(name, face, x, y, z, y0, h, d)
            else:
                col = body_texel(name, face, x, y, z, x0, y0, z0, w, h, d)
            img.putpixel((u, v), col)
    return img


# --- the Java model ---------------------------------------------------------------------------------------------------
def f(v):
    s = ("%.4f" % v).rstrip("0")
    if s.endswith("."):
        s += "0"
    if s == "-0.0":
        s = "0.0"
    return s + "F"


# the wave: how far each section of the chain turns (radians, absolute, in the water) and how much later it turns
WAVE_AMP = (0.05, 0.15, 0.26, 0.36, 0.46)
WAVE_LAG = 1.05          # radians of phase between one section and the next: about two thirds of a wave on the body
WAVE_SPEED = 0.33        # radians per tick: one stroke every 19 ticks (about 1 s), slower than cod's


def write_java():
    lines = []
    for part in CHAIN:
        parent, (px, py, pz), _ = PARTS[part]
        ppiv = PARTS[parent][1] if parent else (0.0, 0.0, 0.0)
        builder = "CubeListBuilder.create()"
        for cube in [c for c in CUBES if c[1] == part]:
            name, _, _, (x0, y0, z0), (w, h, d) = cube
            u, v = tex_offset(cube)
            builder += "\n            /* %s */ .texOffs(%d, %d).addBox(%s, %s, %s, %d.0F, %d.0F, %d.0F%s)" % (
                name, u, v, f(x0 - px), f(y0 - py), f(z0 - pz), w, h, d,
                ", new CubeDeformation(-0.05F)" if name in COLLARS else "")
        pose = "PartPose.offset(%s, %s, %s)" % (f(px - ppiv[0]), f(py - ppiv[1]), f(pz - ppiv[2]))
        lines.append("        PartDefinition %s = %s.addOrReplaceChild(\"%s\", %s,\n            %s);" % (
            part if part != "tail" else "tailPart", parent or "root", part, builder, pose))
    body = "\n".join(lines)
    amps = ", ".join(f(a) for a in WAVE_AMP)
    src = """package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.minecraft.util.Mth;

/**
 * The murina (Mediterranean moray): a long eel, round in front and flattened toward the tail, violet-brown with dense
 * cream spots; a big head with a raised crown, a long snout with tube nostrils, a wide open mouth, a jutting lower jaw
 * and a small pale eye near the front; no pectoral fins, one low fin from behind the head round the tail to mid-belly.
 * 32 px long, 4 px deep and 3 px thick (the head 5 and 4), head toward -z, the ground at y 24.
 * Its own swimming: the body is a chain of five sections (body, seg1, seg2, seg3, tail), each the child of the one
 * before, and a sideways wave runs down it, each section turning further and later than the one in front, so an S
 * travels from the neck to the tail while the head stays nearly still. Out of water the wave is wider and quicker, as
 * vanilla fish flop. The renderer's whole-body wiggle is 0.
 * Made by art/src/fish_murina_model.py (don't edit by hand). Texture: textures/entity/fish/murina.png (%d x %d).
 */
public class MurinaModel extends FishModel {
    /** How far each section turns from the swimming line, in radians, from the head back. */
    private static final float[] AMPLITUDE = {%s};
    private final ModelPart[] sections;

    public MurinaModel(ModelPart root) {
        super(root);
        ModelPart body = root.getChild("body");
        ModelPart seg1 = body.getChild("seg1");
        ModelPart seg2 = seg1.getChild("seg2");
        ModelPart seg3 = seg2.getChild("seg3");
        this.sections = new ModelPart[] {body, seg1, seg2, seg3, seg3.getChild("tail")};
    }

    @Override
    public void setupAnim(LivingEntityRenderState state) {
        super.setupAnim(state);
        float amplitude = state.isInWater ? 1.0F : 1.2F;
        float speed = state.isInWater ? 1.0F : 1.8F;
        float phase = speed * %s * state.ageInTicks;
        float before = 0.0F;
        for (int i = 0; i < sections.length; i++) {
            float angle = amplitude * AMPLITUDE[i] * Mth.sin(phase - i * %s);
            sections[i].yRot = angle - before;
            before = angle;
        }
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
%s
        return LayerDefinition.create(mesh, %d, %d);
    }
}
""" % (TW, TH, amps, f(WAVE_SPEED), f(WAVE_LAG), body, TW, TH)
    with open(JAVA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(src)


# --- offline previews: an orthographic texel splatter with vanilla-like face shading ----------------------------------
SHADE = {"top": 1.0, "bottom": 0.5, "north": 0.8, "south": 0.8, "west": 0.6, "east": 0.6}


def rotate(p, rot):
    """ModelPart order: z, then y, then x (applied to the point in that order)."""
    x, y, z = p
    rx, ry, rz = rot
    if rz:
        c, s = math.cos(rz), math.sin(rz)
        x, y = x * c - y * s, x * s + y * c
    if ry:
        c, s = math.cos(ry), math.sin(ry)
        x, z = x * c + z * s, -x * s + z * c
    if rx:
        c, s = math.cos(rx), math.sin(rx)
        y, z = y * c - z * s, y * s + z * c
    return (x, y, z)


def to_world(parts, part, p):
    """Absolute rest position -> posed position (rotations about each part's rest pivot, the child's first)."""
    while part:
        parent, pivot, rot = parts[part]
        if isinstance(rot, float):
            rot = (0.0, 0.0, rot)
        if any(rot):
            rel = (p[0] - pivot[0], p[1] - pivot[1], p[2] - pivot[2])
            rel = rotate(rel, rot)
            p = (rel[0] + pivot[0], rel[1] + pivot[1], rel[2] + pivot[2])
        part = parent
    return p


def posed(t, amplitude=1.0):
    """PARTS with the swimming wave at phase t (radians), as MurinaModel.setupAnim sets it."""
    out = dict(PARTS)
    before = 0.0
    for i, part in enumerate(CHAIN):
        angle = amplitude * WAVE_AMP[i] * math.sin(t - i * WAVE_LAG)
        parent, pivot, _ = PARTS[part]
        out[part] = (parent, pivot, (0.0, angle - before, 0.0))
        before = angle
    return out


def render(cubes, parts, texture, view, scale, sub=4):
    """Draw a model from 'side' (from -x, head left), 'top' (from above, head left) or 'three' (front three-quarter).
    Returns an RGBA image cropped to the fish, with `scale` screen pixels per model pixel."""
    yaw, pitch = {"side": (0.0, 0.0), "top": (0.0, 90.0), "three": (35.0, 25.0), "other": (180.0, 0.0),
                  "behind": (-25.0, 8.0)}[view]
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))

    def project(p):
        x, y, z = p
        z2, x2 = z * cy + x * sy, -z * sy + x * cy
        y3, d3 = y * cp - x2 * sp, y * sp + x2 * cp
        return z2, y3, d3

    pts = []
    for cube in cubes:
        name, part, _, (x0, y0, z0), (w, h, d) = cube
        for face, u, v, x, y, z in face_texels(cube):
            col = texture.getpixel((u % texture.size[0], v % texture.size[1]))
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
                    pts.append((project(to_world(parts, part, p)), col))
    xs = [q[0][0] for q in pts]
    ys = [q[0][1] for q in pts]
    minx, miny = min(xs) - 1, min(ys) - 1
    wpx = int((max(xs) - minx + 1) * scale) + 1
    hpx = int((max(ys) - miny + 1) * scale) + 1
    img = Image.new("RGBA", (wpx, hpx), CLEAR)
    depth = {}
    r = max(1, int(math.ceil(scale / sub / 2 + 0.5)))
    for (sx, sy_, sd), col in pts:
        px, py = int((sx - minx) * scale), int((sy_ - miny) * scale)
        for ox in range(-r, r):
            for oy in range(-r, r):
                key = (px + ox, py + oy)
                if 0 <= key[0] < wpx and 0 <= key[1] < hpx and sd < depth.get(key, 1e9):
                    depth[key] = sd
                    img.putpixel(key, col + (255,))
    return img


# vanilla cod, as measured from the 26.3 client (CodModel), for scale in the previews
COD_PARTS = {"p": (None, (0, 0, 0), 0.0), "rf": (None, (-1, 23, 0), -0.7854), "lf": (None, (1, 23, 0), 0.7854)}
COD_CUBES = [
    ("body", "p", None, (-1, 20, 0), (2, 4, 7), (0, 0)),
    ("head", "p", None, (-1, 20, -3), (2, 4, 3), (11, 0)),
    ("nose", "p", None, (-1, 20, -4), (2, 3, 1), (0, 0)),
    ("tail", "p", None, (0, 20, 7), (0, 4, 4), (22, 3)),
    ("top", "p", None, (0, 19, -1), (0, 1, 6), (20, -6)),
    ("rf", "rf", None, (-3, 23, -1), (2, 0, 2), (22, 1)),
    ("lf", "lf", None, (1, 23, -1), (2, 0, 2), (22, 4)),
]


def vanilla_cubes(spec):
    out = []
    for name, part, _, pos, (w, h, d), (u, v) in spec:
        if w == 0:
            U, V = u, v + d
        elif h == 0:
            U, V = u + d, v
        else:
            U, V = u, v
        out.append((name, part, (U, V), pos, (w, h, d)))
    return out


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


def cerna_model():
    """The accepted cerna model (cubes, parts, texture), for scale."""
    sys.path.insert(0, HERE)
    import fish_cerna_model as cm
    tex = Image.open(cm.TEXTURE).convert("RGBA")
    return cm.CUBES, cm.PARTS, tex


def previews(out_dir, texture):
    os.makedirs(out_dir, exist_ok=True)
    out = {}
    for view in ("side", "other", "top", "three"):
        img = render(CUBES, PARTS, texture, view, 16)
        img.save(os.path.join(out_dir, "murina_%s16.png" % view))
        out[view] = img
    out["wave"] = [render(CUBES, posed(t), texture, "top", 8) for t in (0.0, 1.05, 2.1, 3.15, 4.2)]
    out["land"] = render(CUBES, posed(1.0, 1.2), texture, "top", 8)
    cod = vanilla_texture("cod")
    row = [render(CUBES, PARTS, texture, "side", 8)]
    try:
        cc, cp, ct = cerna_model()
        row.append(render(cc, cp, ct, "side", 8))
    except Exception as e:      # the sheet still shows the rest
        print("cerna not drawn:", e)
    if cod:
        row.append(render(vanilla_cubes(COD_CUBES), COD_PARTS, cod, "side", 8))
    out["scale"] = row
    return out


# --- the compare sheet ------------------------------------------------------------------------------------------------
def sheet(shots_dir, texture, prev_dir):
    from PIL import ImageFont
    pv = previews(prev_dir, texture)
    font = ImageFont.load_default()
    W = 1800
    blocks = []

    def title(t):
        im = Image.new("RGBA", (W, 26), (40, 40, 40, 255))
        ImageDraw.Draw(im).text((8, 6), t, fill=(240, 240, 240, 255), font=font)
        blocks.append(im)

    def row(images, h=None, gap=12, align_bottom=False):
        if h:
            images = [i.resize((max(1, int(i.width * h / i.height)), h), Image.LANCZOS) for i in images]
        hh = max(i.height for i in images)
        im = Image.new("RGBA", (W, hh + 8), (72, 72, 72, 255))
        x = 8
        for i in images:
            if x + i.width > W:
                break
            im.paste(i, (x, 4 + (hh - i.height if align_bottom else 0)), i)
            x += i.width + gap
        blocks.append(im)

    ref_dir = os.path.join(ROOT, "art", "references", "fish_murina_refonly")
    refs = [Image.open(os.path.join(ref_dir, n)).convert("RGBA")
            for n in ("m12.jpg", "m18.jpg", "m07.jpg", "o01.jpg", "o03.jpg", "o05.jpg")
            if os.path.exists(os.path.join(ref_dir, n))]
    title("References (reference only): in the water (head, open mouth, eel body); out of the water (true violet-brown)")
    row(refs[:3], h=260)
    row(refs[3:], h=260)
    old_dir = os.path.join(ROOT, "art", "candidates", "fish_murina_model_round1")
    if os.path.isdir(old_dir):
        def old(n):
            p = os.path.join(old_dir, n)
            return Image.open(p).convert("RGBA") if os.path.exists(p) else None

        def new_shot(n):
            found = sorted(glob.glob(os.path.join(shots_dir or "", "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None

        title("ROUND 2 (right / below) against round 1 (left / above): one step lighter, full collars in the joints, "
              "brighter eye, gentler wave on land")
        o_side, n_side = old("side8.png"), render(CUBES, PARTS, texture, "side", 8)
        o_tex = old("texture.png")
        row([i for i in (o_side, n_side) if i], align_bottom=True, gap=40)
        if o_tex:
            row([o_tex.resize((256, 256), Image.NEAREST), o_tex, texture.resize((256, 256), Image.NEAREST), texture],
                gap=24)
        for n, box, k in (("fish-murina-beside-cod", (60, 150, 820, 280), 1), ("fish-murina-beside-cod",
                          (60, 150, 820, 280), 2), ("fish-murina-side", (150, 140, 700, 300), 2),
                          ("fish-murina-on-land", (200, 170, 650, 270), 2)):
            pair = [old(n + ".png"), new_shot(n)]
            if all(pair):
                crops = [p.crop(box) for p in pair]
                crops = [c.resize((c.width * k, c.height * k), Image.NEAREST) for c in crops]
                title("In the game, %dx: %s, round 1 above, round 2 below" % (k, n))
                row([crops[0]])
                row([crops[1]])
    title("Offline model, 16x, at rest: left side, right side (vanilla face shading only)")
    row([pv["side"]])
    row([pv["other"]])
    title("Offline model, 16x: three-quarter from the front, and from above")
    row([pv["three"], pv["top"]])
    title("The swimming wave from above (8x), five moments one third of a stroke apart: an S runs from neck to tail; "
          "last: out of water (1.2x wider)")
    row(pv["wave"] + [pv["land"]], gap=24)
    title("Same scale, 8x: murina (hitbox 0.9 x 0.3), the accepted cerna (0.9 x 0.6), vanilla cod (0.5 x 0.3)")
    row(pv["scale"], align_bottom=True, gap=40)
    items = [Image.open(os.path.join(RES, "textures", "item", n)).convert("RGBA")
             for n in ("murina.png", "murina_bucket.png", "murina_spawn_egg.png")
             if os.path.exists(os.path.join(RES, "textures", "item", n))]
    title("The accepted murina item icon, bucket and spawn egg (8x), beside the model (side, 8x)")
    row([i.resize((128, 128), Image.NEAREST) for i in items] + [render(CUBES, PARTS, texture, "side", 8)],
        align_bottom=True, gap=24)
    cod = vanilla_texture("cod")
    title("Texture at 4x and 1x: murina (64 x 64); vanilla cod (32 x 32) at 8x and 1x")
    row([texture.resize((TW * 4, TH * 4), Image.NEAREST), texture]
        + ([cod.resize((256, 256), Image.NEAREST), cod] if cod else []))
    if shots_dir and os.path.isdir(shots_dir):
        def shot(n):
            found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None

        names = ("fish-murina-side", "fish-murina-three-quarter", "fish-murina-top", "fish-murina-on-land",
                 "fish-murina-beside-cod")
        have = [(n, shot(n)) for n in names]
        have = [(n, i) for n, i in have if i]
        if have:
            title("In the game: the murina alone (side, three-quarter, top, on land), and beside vanilla cod")
            row([i for _, i in have[:3]], h=330)
            row([i for _, i in have[3:]], h=330)
            title("The same, cropped to the fish (beside cod: murina left, cod right)")
            boxes = {"fish-murina-beside-cod": (0.04, 0.2, 0.96, 0.7)}
            crops = []
            for n, i in have:
                fx = boxes.get(n, (0.12, 0.2, 0.88, 0.75))
                box = (int(i.width * fx[0]), int(i.height * fx[1]), int(i.width * fx[2]), int(i.height * fx[3]))
                k = 580.0 / (box[2] - box[0])
                crops.append(i.crop(box).resize((580, int((box[3] - box[1]) * k)), Image.NEAREST))
            row(crops[:3])
            row(crops[3:])
        imgs = [shot(n) for n in ("fish-04-tank-tonn-murina-ziemel", "fish-01-tank-all")]
        imgs = [i for i in imgs if i]
        if imgs:
            title("In the game: the shared tank")
            row(imgs, h=330)
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    dest = os.path.join(ROOT, "art", "candidates", "fish_murina_model.png")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    out.convert("RGB").save(dest)
    print("sheet:", dest)


def main():
    texture = draw_texture()
    os.makedirs(os.path.dirname(TEXTURE), exist_ok=True)
    texture.save(TEXTURE)
    write_java()
    print("wrote", os.path.relpath(TEXTURE, ROOT), "and", os.path.relpath(JAVA, ROOT))
    args = sys.argv[1:]
    prev = args[args.index("--preview") + 1] if "--preview" in args else None
    if "--sheet" in args:
        sheet(args[args.index("--sheet") + 1], texture, prev or os.path.join(ROOT, "art", "candidates", "tmp_murina"))
    elif prev:
        p = previews(prev, texture)
        print("previews in", prev)


if __name__ == "__main__":
    main()
