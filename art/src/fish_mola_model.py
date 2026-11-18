"""The mola mola (ocean sunfish, Mola mola) as a swimming mob: its 3D model and its texture.

Drawn from the reference photos in art/references/fish_mola_refonly/ (list.tsv, Wikimedia Commons, licences there):
mm03, mm05 and mm09 (side views swimming: the disc, the fins far back, the scalloped clavus), mm07 and mm10 (out of
water, for the true colour: grey to grey-brown above, silvery sides, a pale belly with grey mottling), mm04 and mm08
(the small mouth, the eye with its paler ring, the gill opening and the small pectoral fin), mm11 (basking on its side
at the surface) and mm06 (swimming just under the surface). What makes it a sunfish:
  - a tall, flat, round disc that looks cut off behind: 21 px long and 21 tall without the fins, and only
    7 px thick at its thickest, thinning to the dorsal and ventral edges and toward the back;
  - no tail: the clavus, a narrow rim 4 px deep behind the disc, its edge scalloped into four rounded lobes;
  - very tall dorsal and anal fins far back, about 8 to 9 px beyond the disc each (the disc's back squared off, full height to the clavus), slim and leaning back, which scull from side to
    side together (the real fish beats them synchronously, 0.3 to 0.6 times a second: Watanabe and Sato 2008);
  - a small round mouth at the front of the blunt head (a pale lip round a darker opening);
  - small rounded pectoral fins at mid-height, with the gill opening just in front of them (a soft darker crease);
  - an eye ahead of and above the pectoral fin: a small raised bump, dark, in a mid-grey ring (a socket), and the only
    dark thing on the head, so the gill and mouth never read as a second eye or a face;
  - grey-brown above, silver-grey sides, a pale belly with soft grey blotches (out of water, mm07 and mm10).
Size: 26 px long from the mouth to the clavus (1.63 blocks) and 38 px tall fin tip to fin tip (2.38 blocks), a
mature fish at life size, the way the tonn (2 to 4 blocks) and the blue shark (2.69 blocks) are drawn.
No icon exists yet (the model comes first, owner 2026-11-18), so the palette comes from the photos, a step lighter
for the water (house rule).

Parts (the fish model contract, docs/Tools and Process/Art pipeline.md, "Fish models"): "body" (the disc, the eyes,
the mouth), "dorsal_fin" and "anal_fin" (pivoted at their bases, sculled by MolaMolaModel's own animation),
"clavus" (the rim, a slow rudder) and "left_fin" / "right_fin" (the pectorals). Head toward -z, y 24 at the ground
(the anal fin's tip). Its middle is at y 4.5: lying on its side (on land, or basking at the surface) the renderer
shifts it by SIDE_SHIFT so its middle lies over its position.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/MolaMolaModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/mola_mola.png
With --sheet [SCREENSHOT_DIR] it also writes the review sheet art/candidates/fish_mola_model.png.

Run:  art/.venv/bin/python art/src/fish_mola_model.py [--sheet [SCREENSHOT_DIR]]
"""
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
JAVA = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "fish",
                    "MolaMolaModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "mola_mola.png")
TW, TH = 256, 128


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


# --- palette (from the out-of-water photos mm07 and mm10, a step lighter for the water) ---------------------------
PAL = {k: hexc(v) for k, v in {
    "B": "#706b63",   # the back: grey-brown, the top third (critic round 1: the rest 20% lighter; round 2: back darker)
    "U": "#99958b",   # upper side
    "S": "#b2afa7",   # silver side
    "L": "#c6c3ba",   # lower side, a thin band between the side and the belly
    "W": "#dedcd4",   # pale belly, the lower third of the disc
    "w": "#e4e1d8",   # the belly's lit undersides
    "m": "#c3c1b9",   # soft grey blotches on the pale belly (about 12% darker than it)
    "n": "#9c998f",   # blotches on the silver side
    "u": "#636058",   # blotches on the back
    "F": "#7a766d",   # fin, at the base
    "G": "#6c685f",   # fin, mid
    "H": "#5e5a53",   # fin tip
    "f": "#8a867c",   # fin, lit leading edge
    "P": "#a09c93",   # pectoral fin (critic round 2: lighter, so it never pairs with the eye)
    "p": "#8b877e",   # its base
    "E": "#25272a",   # the eye
    "e": "#3b3f45",   # the eye's lit upper half
    "c": "#c8c5bc",   # the clavus's scalloped rim, about 13% lighter than the body (critic round 2)
    "k": "#8f8b82",   # the notches between its lobes
    "R": "#bdbab1",   # a paler ring round the eye, as in mm07 (critic round 2), so it reads as an eye, not a hole
    "g": "#6a655d",   # the gill opening (a soft crease, not the eye's dark)
    "M": "#b3ada2",   # the lip round the mouth
    "O": "#6e6862",   # the mouth's opening (about 35% darker than the body, not the eye's dark)
}.items()}
PAL["."] = (0, 0, 0, 0)
CLEAR = PAL["."]
SIDE_RAMP = ["w", "W", "L", "S", "U", "B"]       # lightest to darkest, for stepping a tone
FIN_RAMP = ["f", "F", "G", "H"]

# --- geometry (model px; head toward -z, y down, the ground at y 24) ----------------------------------------------
YC = 4.5                       # the disc's middle
SNOUT = -12                    # the front of the first body column
NCOL = 21                      # body columns, z -12 .. 9
# half-height of each column round YC (the disc's outline from the side: a blunt rounded head, then nearly level,
# tapering a little toward the clavus)
# (critic round 1: the disc read 1.3:1; now 21 long and 21 tall, as round as the real fish's)
# (critic round 2: the back squared off, full height to the end, so it looks cut off)
HH = [4.5, 6.5, 7.5, 8.5, 9.5, 9.5] + [10.5] * 15
# half-thickness of each column at its middle (thickest behind the head, thinner at the snout and toward the back)
HT = [1.5, 2.5, 3.0, 3.0, 3.0] + [3.5] * 8 + [3.0] * 4 + [2.5] * 4
BODY_END = SNOUT + NCOL        # z 9: the clavus starts here
EYE_Z, EYE_Y = -6, -1          # the eye bump: z -6..-4, y -1..1 (ahead of and above the pectoral fin)
GILL_Z = -3                    # the gill opening, one column in front of the pectoral fin
PEC = (-2.0, 4.0)              # the pectoral fins' pivot (z, y), on the body's side
PEC_YAW = 0.45                 # they stand out from the body, trailing back
MOUTH = (-13, 2, 2)            # the mouth: z -13..-12, y 2..4, 2 wide, a little below the eye (critic round 2)
# (critic round 1: slimmer, 8 px at the base, one row shorter)
DORSAL = [(1, 9), (1, 9), (1, 9), (2, 9), (3, 9), (3, 9), (4, 9), (5, 9), (5, 9), (6, 9), (7, 9)]
DORSAL_BASE_Y = -4.5           # its first row is y -4.5..-3.5 (sunk into the disc), then up one row each; the half
FIN_DZ = 0.5                   # pixel offsets keep every fin face off the disc's own face planes (no flicker)
FIN_PIVOT_Z = 5.0
CLAVUS_Y = (-3, 12)            # its rows (between the fins' bases)
# each row's back edge: a 1 px rim (z 12) all round, with four soft lobes 2 rows long reaching 1 px further, and the
# ends tucked in (critic round 1: single-pixel knobs read as gear teeth)
CLAVUS_LOBES = [11, 12, 13, 13, 12, 13, 13, 12, 13, 13, 12, 13, 13, 12, 11]
SIDE_SHIFT = 1.501 - YC / 16.0  # lying on its side, its middle over its position
LAND_LIFT = (3.5 + 1.0 + 0.5) / 16.0    # half its thickness with the eye bump, + 0.5 px (FishRenderer's rule)


def col_top(i):
    return YC - HH[i]


def col_bottom(i):
    return YC + HH[i]


def half_width(i, y0):
    """The body's half-thickness in column i at the row y0..y0+1: full in the middle, thinner toward the edges."""
    dy = abs(y0 + 0.5 - YC) / HH[i]
    w = HT[i]
    if dy > 0.85:
        w -= 1.5
    elif dy > 0.6:
        w -= 1.0
    elif dy > 0.35:
        w -= 0.5
    return max(1.5 if i > 0 else 1.0, w)


def mirror_y(y0, h=1):
    """A row y0..y0+h mirrored about the disc's middle: the anal fin is the dorsal fin turned over."""
    return 2 * YC - (y0 + h)


# cubes: (name, kind, part, abs origin, size, info)
def body_cubes():
    rows = {}
    ymin, ymax = int(min(col_top(i) for i in range(NCOL))), int(max(col_bottom(i) for i in range(NCOL)))
    for y0 in range(ymin, ymax):
        segs = []
        for i in range(NCOL):
            if col_top(i) <= y0 and y0 + 1 <= col_bottom(i):
                w = half_width(i, y0)
                if segs and segs[-1][1] == i and segs[-1][2] == w:
                    segs[-1][1] = i + 1
                else:
                    segs.append([i, i + 1, w])
        rows[y0] = [tuple(s) for s in segs]
    # merge identical segments on consecutive rows into taller boxes
    out, open_ = [], {}
    for y0 in range(ymin, ymax + 1):
        segs = set(rows.get(y0, []))
        for key in list(open_):
            if key not in segs:
                out.append((key, open_.pop(key), y0))
        for s in rows.get(y0, []):
            if s not in open_:
                open_[s] = y0
    cubes = []
    for n, ((i0, i1, w), ya, yb) in enumerate(sorted(out, key=lambda t: (t[1], t[0]))):
        cubes.append(("body%02d" % n, "body", "body", (-w, ya, SNOUT + i0), (int(2 * w), yb - ya, i1 - i0), None))
    return cubes


def all_abs_cubes():
    cubes = body_cubes()
    # the eyes: 1 px bumps on the sides
    w = half_width(EYE_Z - SNOUT, EYE_Y)
    assert w == half_width(EYE_Z + 1 - SNOUT, EYE_Y) == half_width(EYE_Z - SNOUT, EYE_Y + 1)
    cubes.append(("eye_l", "eye", "body", (w, EYE_Y, EYE_Z), (1, 2, 2), None))
    cubes.append(("eye_r", "eye", "body", (-w - 1, EYE_Y, EYE_Z), (1, 2, 2), None))
    # the mouth, in front of the snout
    mz, my, mw = MOUTH
    cubes.append(("mouth", "mouth", "body", (-mw / 2.0, my, mz), (mw, mw, 1), None))
    # the dorsal and anal fins: rows, 2 px thick at the base, then 1
    for k, (z0, z1) in enumerate(DORSAL):
        y0 = DORSAL_BASE_Y - k
        t = 2 if k < 2 else 1
        za = z0 + FIN_DZ
        cubes.append(("dorsal%02d" % k, "fin", "dorsal_fin", (-t / 2.0, y0, za), (t, 1, z1 - z0), (k, za, z1 + FIN_DZ)))
        cubes.append(("anal%02d" % k, "fin", "anal_fin", (-t / 2.0, mirror_y(y0), za), (t, 1, z1 - z0), (k, za, z1 + FIN_DZ)))
    # the clavus: an inner band 2 px thick, then the 1 px rim with its lobes
    for k, y0 in enumerate(range(*CLAVUS_Y)):
        z1 = CLAVUS_LOBES[k]
        cubes.append(("clavus_in%02d" % k, "clavus", "clavus", (-1, y0, BODY_END), (2, 1, 2), (k, z1)))
        if z1 > BODY_END + 2:
            cubes.append(("clavus_rim%02d" % k, "clavus", "clavus", (-0.5, y0, BODY_END + 2), (1, 1, z1 - BODY_END - 2), (k, z1)))
    # the pectoral fins: a small rounded fan, its base at the gill
    pz, py = PEC
    for side, sx in (("left", 1), ("right", -1)):
        x0 = 0 if sx > 0 else -1
        cubes.append(("%s_pec1" % side[0], "pec", "%s_fin" % side, (x0, py - 2, pz), (1, 4, 2), None))
        cubes.append(("%s_pec2" % side[0], "pec", "%s_fin" % side, (x0, py - 1, pz + 2), (1, 2, 1), None))
    return cubes


def pec_x():
    """Where the pectoral fins hinge: on the body's surface at their base."""
    i = int(PEC[0]) - SNOUT
    return half_width(i, int(PEC[1]))


# name -> (parent, pivot (abs), rotation)
PARTS = {
    "body": (None, (0.0, YC, 0.0), (0.0, 0.0, 0.0)),
    "dorsal_fin": (None, (0.0, float(DORSAL_BASE_Y + 1), FIN_PIVOT_Z), (0.0, 0.0, 0.0)),
    "anal_fin": (None, (0.0, float(mirror_y(DORSAL_BASE_Y + 1, 0)), FIN_PIVOT_Z), (0.0, 0.0, 0.0)),
    "clavus": (None, (0.0, YC, float(BODY_END)), (0.0, 0.0, 0.0)),
    "left_fin": (None, (pec_x(), PEC[1], PEC[0]), (0.0, PEC_YAW, 0.0)),
    "right_fin": (None, (-pec_x(), PEC[1], PEC[0]), (0.0, -PEC_YAW, 0.0)),
}
PART_ORDER = ["body", "dorsal_fin", "anal_fin", "clavus", "left_fin", "right_fin"]


def local_cubes():
    """Every cube with its origin relative to its part's pivot (the pectoral fins' cubes are drawn from the hinge)."""
    out = []
    for name, kind, part, (x0, y0, z0), size, info in all_abs_cubes():
        px, py, pz = PARTS[part][1]
        if part.endswith("_fin") and part not in ("dorsal_fin", "anal_fin"):
            # drawn at x 0 (left) or -1 (right) from the hinge
            out.append((name, kind, part, (x0, y0 - py, z0 - pz), size, info, (x0 + px, y0, z0)))
        else:
            out.append((name, kind, part, (x0 - px, y0 - py, z0 - pz), size, info, (x0, y0, z0)))
    return out


# --- texture ----------------------------------------------------------------------------------------------------------
def hash01(*v):
    h = 2166136261
    for a in v:
        h = ((h ^ (int(a) & 0xffffffff)) * 16777619) & 0xffffffff
    return h / 4294967295.0


def blotch(y, z, salt):
    """Soft blotches 2-3 px across: smooth value noise on a 3 px grid (no lone specks)."""
    gy, gz = y / 3.0, z / 3.0
    y0, z0 = math.floor(gy), math.floor(gz)
    fy, fz = gy - y0, gz - z0
    sy, sz = fy * fy * (3 - 2 * fy), fz * fz * (3 - 2 * fz)
    a = hash01(y0, z0, salt) * (1 - sz) + hash01(y0, z0 + 1, salt) * sz
    b = hash01(y0 + 1, z0, salt) * (1 - sz) + hash01(y0 + 1, z0 + 1, salt) * sz
    return a * (1 - sy) + b * sy


def shift(key, steps, ramp):
    return ramp[max(0, min(len(ramp) - 1, ramp.index(key) + steps))]


def side_tone(y, z):
    """The disc's colour at height y (abs) and z: a darker back across the top, silver sides, the pale belly over the
    lower third; the edges between them dithered by the blotch noise (no hard lines), and soft blotches 2-3 px across,
    about 10% darker than the tone under them, scattered over all of it (critic round 1: no stripes)."""
    i = max(0, min(NCOL - 1, int(math.floor(z)) - SNOUT))
    r = (y - YC) / HH[i]                          # -1 at the top edge, +1 at the bottom
    r += (blotch(y, z, 3) - 0.5) * 0.22           # a ragged, dithered edge between the bands
    if r < -0.55:
        key = "B"
    elif r < -0.28:
        key = "U"
    elif r < 0.22:
        key = "S"
    elif r < 0.36:
        key = "L"
    else:
        key = "W"
    if blotch(y * 1.4, z, 7) > 0.66:
        key = {"B": "u", "U": "u", "S": "n", "L": "n", "W": "m"}[key]
    return key


def body_key(cube, face, x, y, z):
    zi, yi = int(math.floor(z)), int(math.floor(y))
    if face in ("east", "west"):
        # a mid-grey ring round the eye bump (an eye socket)
        if (yi in (EYE_Y - 1, EYE_Y + 2) and EYE_Z <= zi <= EYE_Z + 1) or (zi in (EYE_Z - 1, EYE_Z + 2) and EYE_Y <= yi <= EYE_Y + 1):
            return "R"
        # the gill opening: a soft crease, 3 px tall, just in front of the pectoral fin
        if zi == GILL_Z and 3 <= yi <= 5:
            return "g"
        return side_tone(y, z)
    # the steps of the back, belly, forehead and snout: the same colours as the sides there, so the box joins don't
    # show as stripes (the game shades each face by its direction anyway)
    return side_tone(y, z)


def eye_key(cube, face, x, y, z):
    if face in ("east", "west"):
        return "e" if int(math.floor(y)) == EYE_Y else "E"
    return "R"


def mouth_key(cube, face, x, y, z):
    if face == "north":
        return "O"                                 # the small round opening, seen head-on and from the side
    return "M"


def fin_key(cube, face, x, y, z):
    k, z0, z1 = cube[5]
    t = k / float(len(DORSAL) - 1)
    key = "F" if t < 0.35 else ("G" if t < 0.75 else "H")
    zi = int(math.floor(z))
    if face in ("east", "west") and z - z0 < 1.0:
        key = shift(key, -1, FIN_RAMP)             # the leading edge, lit
    if face in ("top", "bottom", "north"):
        key = shift(key, -1, FIN_RAMP)
    return key


def clavus_key(cube, face, x, y, z):
    k, z1 = cube[5]
    zi = int(math.floor(z))
    if zi >= z1 - 1 or face == "south":
        # the rim, lighter, with a darker notch where two lobes meet
        notch = z1 == BODY_END + 3 and 0 < k < len(CLAVUS_LOBES) - 1 and CLAVUS_LOBES[k - 1] > z1 and CLAVUS_LOBES[k + 1] > z1
        return "k" if notch else "c"
    return side_tone(y, BODY_END - 0.5)            # the rest matches the body where they join (no seam)


def pec_key(cube, face, x, y, z):
    zi = int(math.floor(z))
    return "p" if zi <= int(PEC[0]) else "P"


KEYS = {"body": body_key, "eye": eye_key, "mouth": mouth_key, "fin": fin_key, "clavus": clavus_key, "pec": pec_key}


def layout():
    cubes = local_cubes()
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
        dx, dy, dz = absorg[0] - origin[0], absorg[1] - origin[1], absorg[2] - origin[2]
        for face, tu, tv, x, y, z in AW.face_texels(u, v, origin, size):
            assert owner.setdefault((tu, tv), name) == name, ("texture overlap", name, owner[(tu, tv)])
            key = KEYS[kind]((name, kind, part, origin, size, info), face, x + dx, y + dy, z + dz)
            img.putpixel((tu, tv), PAL[key])
    return img


# --- Java -------------------------------------------------------------------------------------------------------------
def f(v):
    s = ("%.5f" % v).rstrip("0")
    if s.endswith("."):
        s += "0"
    if s == "-0.0":
        s = "0.0"
    return s + "F"


JAVA_HEAD = '''package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.minecraft.util.Mth;

/**
 * The mola mola (ocean sunfish): a tall, flat round disc 21 px long and 21 tall that looks cut off behind, with no tail but
 * the clavus (a narrow rim with a scalloped edge), very tall dorsal and anal fins far back, small rounded pectoral
 * fins, a small round mouth and a small dark eye in a mid-grey ring. Grey-brown above, silver-grey sides, a pale
 * belly with soft grey blotches. 26 px long and 38 tall fin tip to fin tip (1.63 x 2.38 blocks, life size).
 * Made by art/src/fish_mola_model.py (do not edit by hand); texture textures/entity/fish/mola_mola.png.
 * Its own swimming: the dorsal and anal fins scull from side to side together (both tips to the same side), as the
 * real fish swims; the clavus steers a little and the pectoral fins flutter. The body doesn't wag (its renderer
 * wiggles it under a degree). Basking on its side at the surface (MolaFish), the fins only stir; on land they flap.
 */
public class MolaMolaModel extends FishModel {
    /** The renderer's lift when it lies on its side: half its thickness with the eyes, + 0.5 px (FishShape copies it). */
    public static final float LAND_LIFT = %(lift)s;
    /** Lying on its side, it is moved back along its height by this much, so its middle (y %(yc)s) lies over its position. */
    public static final float SIDE_SHIFT = %(shift)s;
    private final ModelPart dorsal;
    private final ModelPart anal;
    private final ModelPart clavus;
    private final ModelPart leftFin;
    private final ModelPart rightFin;
    private final float finYaw;

    public MolaMolaModel(ModelPart root) {
        super(root);
        this.dorsal = root.getChild("dorsal_fin");
        this.anal = root.getChild("anal_fin");
        this.clavus = root.getChild("clavus");
        this.leftFin = root.getChild("left_fin");
        this.rightFin = root.getChild("right_fin");
        this.finYaw = leftFin.yRot;
    }

    @Override
    public void setupAnim(LivingEntityRenderState state) {
        super.setupAnim(state);
        float t = state.ageInTicks;
        boolean basking = state instanceof FishRenderer.FishRenderState fish && fish.basking;
        float amplitude;
        float rate;
        if (!state.isInWater) {
            amplitude = 0.35F;
            rate = 0.5F;
        } else if (basking) {
            amplitude = 0.08F;
            rate = 0.06F;
        } else {
            // 0.14 radians while still, up to 0.4 swimming; one beat about every 2.2 s (the real fish 0.3 to 0.6 Hz)
            float moving = Mth.clamp(state.walkAnimationSpeed * 2.0F, 0.0F, 1.0F);
            amplitude = 0.14F + 0.26F * moving;
            rate = 0.14F;
        }
        float scull = amplitude * Mth.sin(rate * t);
        // +zRot swings the dorsal fin's tip one way and the anal fin's tip the other, so the anal fin turns the
        // opposite way: both tips go to the same side together
        dorsal.zRot = scull;
        anal.zRot = -scull;
        clavus.yRot = (state.isInWater ? 0.06F : 0.15F) * Mth.sin(0.05F * t + 0.7F);
        float flutter = (basking ? 0.05F : 0.15F) * Mth.sin(0.3F * t);
        // on land they lie nearly flat against the body (critic round 2: one stuck out like a handle)
        float yaw = state.isInWater ? finYaw : 0.25F * finYaw;
        leftFin.yRot = yaw + flutter;
        rightFin.yRot = -yaw - flutter;
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
'''


def java_source():
    lines = [JAVA_HEAD % {"lift": f(LAND_LIFT), "shift": f(SIDE_SHIFT), "yc": YC}]
    placed = layout()
    for part in PART_ORDER:
        parent, (ax, ay, az), (rx, ry, rz) = PARTS[part]
        builder = "CubeListBuilder.create()"
        for (name, _k, cpart, (x0, y0, z0), (w, h, d), _i, _a), (u, v) in placed:
            if cpart != part:
                continue
            builder += "\n            /* %s */ .texOffs(%d, %d).addBox(%s, %s, %s, %s, %s, %s)" % (
                name, u, v, f(x0), f(y0), f(z0), f(w), f(h), f(d))
        if (rx, ry, rz) == (0.0, 0.0, 0.0):
            pose = "PartPose.offset(%s, %s, %s)" % (f(ax), f(ay), f(az))
        else:
            pose = "PartPose.offsetAndRotation(%s, %s, %s, %s, %s, %s)" % (f(ax), f(ay), f(az), f(rx), f(ry), f(rz))
        lines.append("        root.addOrReplaceChild(\"%s\", %s,\n            %s);\n" % (part, builder, pose))
    lines.append("        return LayerDefinition.create(mesh, %d, %d);\n    }\n}\n" % (TW, TH))
    return "".join(lines)


# --- checks -----------------------------------------------------------------------------------------------------------
def check_boxes():
    """No two faces facing the same way may share a plane where they overlap (they would flicker). Fins are allowed
    to sink into the body (hidden), but not to share a face plane with it; at rest the pectorals are left out (they
    stand out at an angle)."""
    cubes = [(c[0], c[6], c[4]) for c in local_cubes() if not c[2].endswith("_fin") or c[2] in ("dorsal_fin", "anal_fin")]
    body = [c for c in local_cubes() if c[2] == "body"]
    probs = []
    for i in range(len(cubes)):
        a0 = cubes[i][1]
        a1 = tuple(a0[k] + cubes[i][2][k] for k in range(3))
        for j in range(i + 1, len(cubes)):
            b0 = cubes[j][1]
            b1 = tuple(b0[k] + cubes[j][2][k] for k in range(3))
            ov = [min(a1[k], b1[k]) - max(a0[k], b0[k]) for k in range(3)]
            same_part = cubes[i][0][:4] == cubes[j][0][:4]
            if all(o > 1e-6 for o in ov) and same_part:
                probs.append(("overlap", cubes[i][0], cubes[j][0]))
                continue
            for k in range(3):
                for side in (0, 1):
                    if abs((a0, a1)[side][k] - (b0, b1)[side][k]) > 1e-6:
                        continue
                    o = [ov[m] for m in range(3) if m != k]
                    if all(q > 1e-6 for q in o):
                        probs.append(("same plane", cubes[i][0], cubes[j][0], "xyz"[k]))
    assert body
    return probs


def measure():
    zs = [c[6][2] for c in local_cubes()] + [c[6][2] + c[4][2] for c in local_cubes()]
    ys = [c[6][1] for c in local_cubes()] + [c[6][1] + c[4][1] for c in local_cubes()]
    return min(zs), max(zs), min(ys), max(ys)


# --- offline preview --------------------------------------------------------------------------------------------------
SHADE = {"top": 1.0, "bottom": 0.5, "north": 0.8, "south": 0.8, "west": 0.6, "east": 0.6}
VIEWS = {"side": (0, 0), "other": (180, 0), "three": (35, 20), "top": (0, 90), "front": (90, 10), "back": (-90, 10)}


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


def scull_rots(t, amp=0.4, rate=0.14):
    s = amp * math.sin(rate * t)
    return {"dorsal_fin": (0, 0, s), "anal_fin": (0, 0, -s)}


def sheet(shots_dir, texture):
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

    def row(images, h=None, gap=16):
        images = [i for i in images if i is not None]
        if not images:
            return
        if h:
            images = [i.resize((max(1, int(i.width * h / i.height)), h), Image.LANCZOS) for i in images]
        hh = max(i.height for i in images)
        im = Image.new("RGBA", (W, hh + 8), BG)
        x = 8
        for i in images:
            if x + i.width > W:
                break
            im.paste(i, (x, 4 + hh - i.height), i)
            x += i.width + gap
        blocks.append(im)

    ref_dir = os.path.join(ROOT, "art", "references", "fish_mola_refonly")
    refs = [Image.open(os.path.join(ref_dir, n)).convert("RGBA")
            for n in ("mm03.jpg", "mm05.jpg", "mm07.jpg", "mm10.jpg", "mm11.jpg", "mm06.jpg")
            if os.path.exists(os.path.join(ref_dir, n))]
    title("References (reference only, Wikimedia Commons): side views, out of water (true colour), basking on its side")
    row(refs, h=220)
    title("Offline model, 8x: side, other side, three-quarter, front, top")
    row([render(me, texture, *VIEWS["side"], 8), render(me, texture, *VIEWS["other"], 8), render(me, texture, *VIEWS["three"], 8)])
    row([render(me, texture, *VIEWS["front"], 8), render(me, texture, *VIEWS["top"], 8), render(me, texture, *VIEWS["back"], 8)])
    title("Offline: sculling, from the front (both fin tips swing to the same side), 6 frames of one beat")
    row([render(me, texture, 90, 10, 5, rots=scull_rots(t), bg=BG) for t in range(0, 45, 8)])
    title("Palette and texture at 3x")
    sw = Image.new("RGBA", (len(PAL) * 34, 46), BG)
    d = ImageDraw.Draw(sw)
    for i, (k, c) in enumerate(PAL.items()):
        d.rectangle((i * 34, 0, i * 34 + 30, 30), fill=c)
        d.text((i * 34 + 10, 32), k, fill=(240, 240, 240, 255), font=font)
    row([sw])
    row([texture.resize((TW * 3, TH * 3), Image.NEAREST)])
    if shots_dir and os.path.isdir(shots_dir):
        def shot(n):
            found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None
        title("In the game: side, three-quarter, front, top")
        row([shot(n) for n in ("fish-mola-side", "fish-mola-three-quarter", "fish-mola-front", "fish-mola-top")], h=300)
        title("In the game: beside a cod, a 3-block tonn and the blue shark; basking at the surface; on land")
        row([shot(n) for n in ("fish-mola-sizes", "fish-mola-sizes-low", "fish-mola-basking", "fish-mola-basking-above")], h=300)
        title("In the game: sculling, from in front")
        row([shot("fish-mola-scull-%d" % i) for i in range(5)], h=240)
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), BG)
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    dest = os.path.join(ROOT, "art", "candidates", "fish_mola_model.png")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    out.convert("RGB").save(dest)
    print("sheet:", dest)


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
    z0, z1, y0, y1 = measure()
    print("wrote", os.path.relpath(TEXTURE, ROOT), "and", os.path.relpath(JAVA, ROOT))
    print("size: %.1f px long (z %.1f..%.1f), %.1f px tall (y %.1f..%.1f); land lift %.5f, side shift %.5f"
          % (z1 - z0, z0, z1, y1 - y0, y0, y1, LAND_LIFT, SIDE_SHIFT))
    args = sys.argv[1:]
    if "--sheet" in args:
        rest = args[args.index("--sheet") + 1:]
        sheet(rest[0] if rest else None, texture)


if __name__ == "__main__":
    main()
