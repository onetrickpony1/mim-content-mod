"""The petrica (anglerfish, Lophius piscatorius and L. budegassa) as a swimming mob: its 3D model and its texture.

Drawn from the reference photos in art/references/fish_petrica_refonly/ (list.tsv): norway (a landed fish from above,
out of water, for the outline and the true colour), algeria (a Mediterranean L. budegassa at a market, for the olive
tone and the mouth line), frontal and seeteufel (the mouth from the front), insitu and side01 (on the floor in water:
the fringe of skin flaps and the camouflage), hal (a museum fish labelled "Frequent in Maltese waters").
What makes it an anglerfish, and not a ray or a flatfish:
  - a huge, wide, flattened head, 14 px across (16 with the fringe), nearly half the fish's 22 px length, 4 px thick
    in the middle stepping down to 2 px at the rim; the body behind it tapers fast (6, 4, 3 px wide) to a small,
    rounded tail fin that sways;
  - an enormous mouth right across the front: the lower jaw juts 1 px past the upper and the gape is one straight,
    flat dark line from corner to corner (12 px), never curved up (a grin) or down (a sad face), and no teeth;
  - a fringe of small skin flaps along both edges of the head: 1 px tabs, every other texel, in a muted pale brown;
  - small eyes on top of the head, looking up: a near-black pupil on a 1 px bump with a pale ring round it; nothing
    else on the fish is that dark, and the blotches keep away from them;
  - the "fishing rod" (illicium) standing on the snout, leaning forward, with a small dull fleshy flap at its tip
    (this is a mud-floor anglerfish: no glowing lure), and a short second spine behind it;
  - big fan pectoral fins spread flat on the floor behind the head, and a small soft dorsal fin near the tail;
  - mottled brown camouflage on the back (2 px blotches darker and lighter, never 1 px specks), a paler rim, and a
    pale cream belly (dark back, pale belly).
The palette is a step lighter than the photos (water greys and darkens everything).

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): a plain FishModel, head toward -z, y 24 at
the ground, root children "body", "lure", "left_fin", "right_fin" and "tail_fin" (which sways). The renderer gives it
no body wiggle and lays it flat on land (MimContentClient, liesFlat).

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/PetricaModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/petrica.png   (64 x 64)
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
TW, TH = 64, 64
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
        "e": "#c8a070", "E": "#0c0806",        # the ring round the eye, the eye
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
BLOTCH = {"A": (0.18, 0.14), "B": (0.18, 0.14), "C": (0.26, 0.18)}   # chance of a dark, of a pale 2 px blotch
LIFT = {"A": 1.0, "B": 1.3, "C": 1.3}   # A is given at its final colours (round 2)
CLEAR = (0, 0, 0, 0)

# --- the model -------------------------------------------------------------------------------------------------------
# Parts: name -> (parent, pivot (absolute model pixels), (xRot, yRot, zRot)). Cubes: (name, part, (U, V), (x0, y0, z0)
# absolute, (w, h, d)). Absolute: x across, y down (24 = ground), z head (-) to tail (+).
PARTS = {
    "body": (None, (0.0, 22.0, 0.0), (0.0, 0.0, 0.0)),
    # the rod stands just behind the front edge of the head and leans forward over the mouth
    # round 7: right behind the upper lip. After round 8 the rod and its flap stand at the pivot (they had been left
    # 2 px behind it, so the lean lifted them to 9 px, taller than a flat fish's 7 px on land) and lean a little more
    "lure": (None, (0.0, 19.0, -12.5), (0.9, 0.0, 0.0)),
    # the pectoral fans lie flat on the floor behind the head, swept a little back
    "left_fin": (None, (4.5, 22.5, 0.5), (0.0, 0.6, 0.0)),    # round 5: swept back further
    "right_fin": (None, (-4.5, 22.5, 0.5), (0.0, -0.6, 0.0)),
    "tail_fin": (None, (0.0, 22.5, 10.0), (0.0, 0.0, 0.0)),
}
SPECS = [
    # the lower jaw, jutting 1 px past the upper, right across the front
    # round 5: the head 2 px longer (the fish sat smaller than the cerna; the head carries the size)
    ("jaw", "body", (-6.0, 22.0, -14.0), (12, 2, 1)),
    # the head: a 3 px dome in the middle, 2 px shoulders, a 1 px rim (round 1: flatter and wider)
    # round 4: the dome 4 px deep (round 2 asked for the head to be the deepest part; a separate crown cube showed a
    # dark step that read as a second mouth from the front)
    # round 5: 5 px deep, a clear step over the 3 px body behind it
    # round 7: the dome 2 px wider, so the eyes sit nearer the head's edges
    ("head", "body", (-5.0, 19.0, -13.0), (10, 5, 12)),
    ("shoulder_l", "body", (5.0, 21.0, -13.0), (1, 3, 11)),
    ("shoulder_r", "body", (-6.0, 21.0, -13.0), (1, 3, 11)),
    # the rim, its corners cut a step at the front and back (round 5: the head read as a square from above)
    ("rim_l", "body", (6.0, 23.0, -11.0), (2, 1, 7)),
    ("rim_r", "body", (-8.0, 23.0, -11.0), (2, 1, 7)),
    ("rim_lf", "body", (6.0, 23.0, -12.0), (1, 1, 1)),
    ("rim_rf", "body", (-7.0, 23.0, -12.0), (1, 1, 1)),
    ("rim_lb", "body", (6.0, 23.0, -4.0), (1, 1, 1)),
    ("rim_rb", "body", (-7.0, 23.0, -4.0), (1, 1, 1)),
    # the body behind the head, tapering fast to the tail in width (head 16 px, trunk 5, rear 3, stalk 2) and depth
    # (5, 3, 2, 2); round 5: the body behind the head 3 px shorter
    # round 6: a wider middle section (head 16, trunk 9, rear 5, stalk 3) so the head doesn't jump to a stick
    ("trunk", "body", (-4.5, 21.0, -1.0), (9, 3, 4)),
    ("rear", "body", (-2.5, 22.0, 3.0), (5, 2, 4)),
    ("stalk", "body", (-1.5, 22.0, 7.0), (3, 2, 3)),
    # the fringe of skin flaps along both edges of the head and in front of the lower jaw (flat, every other texel)
    # round 3: along the sides only (under the chin it read as a comb of teeth), irregular, 1 or 2 px long
    ("fringe_l", "body", (8.0, 23.5, -11.0), (1, 0, 7)),
    ("fringe_r", "body", (-9.0, 23.5, -11.0), (1, 0, 7)),
    # round 6: small pale tabs along the lower jaw's edge too, irregular (an even row read as teeth in round 3)
    ("fringe_f", "body", (-6.0, 23.5, -15.0), (12, 0, 1)),
    # the small, low soft dorsal fin near the tail
    ("dorsal", "body", (0.0, 21.0, 4.0), (0, 1, 4)),
    # the rod (illicium) and the fleshy flap at its tip
    # round 2: two crossed 1 px planes instead of a cube, so it reads 1 px thin from every side, and shorter
    # round 5: 2 px and leaning further forward (it was the tallest thing from the side)
    ("rod", "lure", (0.0, 17.0, -13.0), (0, 2, 1)),
    ("rod_x", "lure", (-0.5, 17.0, -12.5), (1, 2, 0)),
    ("esca", "lure", (0.0, 16.0, -14.5), (0, 1, 2)),
    # the pectoral fans
    # round 5: at the body's mid height, splayed flat sideways (lower down they hung like legs)
    ("pec_l", "left_fin", (4.5, 22.5, -1.0), (5, 0, 4)),
    ("pec_r", "right_fin", (-9.5, 22.5, -1.0), (5, 0, 4)),
    # the small rounded tail
    # round 3: a fan taller than the stalk, widening backward (a knob on a shaft read badly)
    ("caudal", "tail_fin", (0.0, 20.0, 10.0), (0, 4, 3)),
]


def footprint(size):
    w, h, d = size
    if w == 0:
        return 2 * d, d + h
    if h == 0:
        return d + 2 * w, d
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
# Fin outlines, one character per texel. Vertical planes (w 0): rows y from the top, columns z from the front.
# Flat planes (h 0): rows z from the front, columns x from the body outward.
CAUDAL = [        # rows y 20..23, columns z 10..12: a fan in the body's brown, widening backward, a darker rim
    ".FD",
    "FFD",
    "FFD",
    ".FD",
]
DORSAL = [        # row y 21, columns z 4..7: a low soft fin
    "ffF.",
]
ESCA = [          # row y 16, columns z -14.5..-12.5: a small dull flap
    "QQ",
]
PECTORAL = [      # rows z -1..2 (front to back), columns from the body outward: a thin fan, round 3 in the body's tones
    "rrF..",
    "rFFF.",
    "rFFfD",
    "rFfD.",
]
FRINGE = None     # every other texel, from the hash below


def lifted(c, k):
    h, s, v = colorsys.rgb_to_hsv(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
    r, g, b = colorsys.hsv_to_rgb(h, s, min(1.0, v * k))
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)), 255)


def ramp(pal, shade):
    return pal[str(max(0, min(5, shade)))]


def hash01(*vals):
    return CE.hash01(*vals)


EYES = ((4.5, -8.5), (-4.5, -8.5))   # round 7: near the dome's edges


def near_eye(x, z, r=1.6):
    return any(abs(x - ex) < r and abs(z - ez - 0.5) < r for ex, ez in EYES)


def back_colour(pal, cand, x, z):
    """The back seen from above, the view seen most: mottled brown camouflage in 2 px blotches, the middle of the dome
    a little lighter, the rim a little paler and warmer, a clean pale ring round each eye."""
    for ex, ez in EYES:
        if abs(x - ex) < 0.6 and abs(z - ez) < 0.6:
            return pal["E"]                  # a 1 px pupil (round 7 tried 2 x 2: googly cartoon eyes)
        # round 5: a 2 x 2 eye, the pupil at its outer front corner and a pale socket on the other three
        # round 6: a 1 px ring round the pupil (3 x 3), so it shows under water; in a light skin brown, not cream,
        # because a cream ring made googly cartoon eyes from the front
        if abs(x - ex) < 1.6 and abs(z - ez) < 1.6:
            return pal["e"]                  # a light skin-brown ring (cream or grey rings made cartoon eyes)
        # round 2: a pale rim only beside and behind the eye (no ring in front, which faced the viewer as a face);
        # round 3: only behind it, so head on the eye shows as one small dark dot
        # round 4: no rim at all (from above the front a pale pixel behind the eye read as the white of a cartoon eye)
    ax = abs(x)
    if z < -12 and ax < 6:
        return ramp(pal, 2)                  # the row over the gape plain (round 4: a darker row read as a 2nd mouth)
    snout = (z < -5 and ax < 6) and not near_eye(x, z, 1.6)   # round 8: as far back as the eyes (a dark blotch
                                                             # behind them read as a brow)
    if snout:
        # round 6: no dark marks between the eyes and the mouth (they read as brows and a nose); round 7: a plain
        # patch there read as a face, so it is mottled in the light and mid tones only
        m = hash01(49, int(math.floor(x / 2)), int(math.floor(z / 2)))
        return pal["P"] if m > 0.8 else ramp(pal, 1 if m > 0.55 else 2 if m > 0.2 else 3)
    shade = 3
    if ax < 3.0 and z < 0:
        shade = 2                            # the dome
    if ax > 6.0:
        shade = 2                            # the rim
    if z > 4:
        shade = 3
    if z > 9:
        shade = 4                            # the tail darkens
    if near_eye(x, z, 2.6):
        return ramp(pal, shade)              # nothing but the plain back next to the eyes
    # 2 px blotches: pairs of texels along z, cells of 2 x 2
    # round 3: blotches of two sizes (2 and 3 px cells, staggered) so they never line up into bands
    dark, pale = BLOTCH[cand]
    r = hash01(41, int(math.floor((x + 8) / 2)), int(math.floor((z + 12) / 2)))
    r3 = hash01(45, int(math.floor((x + 9) / 3)), int(math.floor((z + 13) / 3)))
    if r3 < 0.16:
        return pal["B"]
    if r3 > 0.9:
        return pal["P"]
    if r < dark:
        return pal["B"]
    if r > 1 - pale:
        return pal["P"]
    # a soft one-step mottle in 2 px runs
    m = hash01(43, int(math.floor(x * 2)), int(math.floor(z / 2)))
    if m < 0.22:
        shade += 1
    elif m > 0.80:
        shade -= 1
    return ramp(pal, shade)


def side_colour(pal, cand, x, y, z):
    """The flanks of the flat head and body: dark at the top, paling down to the cream belly (countershade)."""
    yi = int(math.floor(y))
    shade = {19: 3, 20: 3, 21: 3, 22: 2, 23: 0}.get(yi, 1)   # the bottom row cream; round 5: lighter flanks
    m = hash01(47, int(math.floor(z / 2)), yi)
    if yi <= 22 and m < 0.2:
        shade += 1
    return ramp(pal, shade)


def body_colour(pal, cand, name, face, x, y, z, cube):
    _, _, _, (x0, y0, z0), (w, h, d) = cube
    if name == "jaw":
        if face == "top":
            return pal["L"]                  # round 3: the lip seen from above (the gape is the row just behind it)
        if face == "north":
            return pal["L"] if y < 23 else ramp(pal, 1)   # the pale lower lip, the chin under it
        if face == "bottom":
            return pal["0"]
        return pal["L"]
    if face == "north" and name in ("head", "shoulder_l", "shoulder_r"):
        if y < 21:
            return ramp(pal, 1)              # the upper lip, over the middle of the gape
        return pal["M"]                      # the gape seen from the front, the one row above the jaw
    if face == "top":
        return back_colour(pal, cand, x, z)
    if face == "bottom":
        return ramp(pal, 0)
    return side_colour(pal, cand, x, y, z)


def plane_colour(pal, name, cube, x, y, z):
    _, _, _, (x0, y0, z0), (w, h, d) = cube
    if name.startswith("fringe"):
        zi = int(math.floor(z))
        # round 5: pale-brown flaps every other texel, 1 px out, so they show from above
        if name == "fringe_f":
            xi = int(math.floor(x))
            return pal["T"] if xi in (-6, -3, -2, 1, 4) else CLEAR
        return pal["T"] if zi % 2 == 0 else CLEAR
    if h == 0:
        grid = PECTORAL
        r = int(math.floor(z - z0))
        c = int(math.floor(x - x0)) if name.endswith("_l") else int(math.floor(x0 + w - x))
        ch = grid[r][c]
    else:
        grid = {"caudal": CAUDAL, "dorsal": DORSAL, "esca": ESCA}[name]
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
                col = pal["R"]
            elif w == 0 or h == 0:
                col = plane_colour(pal, name, cube, x, y, z)
            else:
                col = body_colour(pal, cand, name, face, x, y, z, cube)
            img.putpixel((u, v), col)
    return img


# --- the Java model ---------------------------------------------------------------------------------------------------
def write_java():
    f = CE.f
    lines = []
    for part in ("body", "lure", "left_fin", "right_fin", "tail_fin"):
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
 * The petrica (anglerfish): a huge, wide, flattened head (14 px across, 16 with its fringe of skin flaps, nearly half
 * the 22 px length) with an enormous straight mouth right across the front and the lower jaw jutting out, small eyes
 * on top, the fishing-rod lure (illicium) leaning forward from the snout with a small dull flap at its tip, big fan
 * pectoral fins flat on the floor, and a body tapering fast to a small rounded tail that sways. Mottled brown above,
 * cream below. Head toward -z, the ground at y 24; flat, so it lies flat on land (no wiggle). Texture 64 x 64:
 * textures/entity/fish/petrica.png. Made by art/src/fish_petrica_model.py (don't edit by hand).
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
