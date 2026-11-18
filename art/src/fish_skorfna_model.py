"""The skorfna (scorpionfish) as a swimming mob: one 3D model and two textures in the same UV layout.

  skorfna.png      the black scorpionfish (Scorpaena porcus, Skorfna sewda): mottled dark brown and blackish over a
                   reddish tan, darker saddles across the back, a paler belly, banded fins and tail;
  skorfna_red.png  the red scorpionfish (Scorpaena scrofa, Cippullazza): red to orange-red with darker red-brown
                   mottling, a pale pinkish belly and many small skin flaps on the chin (paint only).
The owner (2026-11-18): "skorfna should just have two versions the red and this colour and they should be reskins of
each other". Both textures share every UV, so the variant code only swaps the texture.

Drawn from the reference photos in art/references/fish_skorfna_refonly/ (list.tsv): black_specimen_side for the
proportions, black_caught_1-3 (on a net, out of water) for the black one's colour, red_market (a market stall) for the
red one's, the rest (in water) for the shape of the head, cirri and fins. What makes it a scorpionfish, not a ball and
not a grouper:
  - long, not round: 15 px from the lip to the tail's edge, 5 px deep at the head (3.0 : 1), 8 px with the spines;
  - a big, broad head, a third of the length (5 px of 15 behind the lip), the broadest part of the fish (6 px across
    the spiny gill covers); the snout steps in at the top and the chin steps back under a 1 px lip, and the gape runs
    from the lip's corners back and down (a wide downturned mouth);
  - high eyes, at the top edge of the head, under a small fleshy flap (cirrus) over each eye ("head_flaps");
  - a body that tapers behind the head, in width (6, 4, 3, 2) and depth (5, 4, 3, 2), to a slim stalk, then a rounded
    fan tail with a dark band;
  - one long dorsal fin from over the gill cover to the stalk: three separate dark spines 3 px tall with 1 px gaps, a
    notch, then a soft rounded rear lobe;
  - big rounded fan pectoral fins hinged on the flank behind the head and spread out sideways, with a darker band and
    rim; small pelvic fins under the throat and a small anal fin, all touching the body.
The shape was reworked through three critic rounds (2026-11-18): the taper, the snout, a dorsal that reads as one fin,
pectorals that read as fans and not legs, and no dark pixels near the eye but the eye.
The palette sits a step lighter than the photos (water greys and darkens everything). No face is a flat fill: rows run
from a dark back to a pale belly, blotches are 2 px wide (never lone 1 px dots) and darker saddles cross the back.

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, root
children "body" (with "head_flaps"), "top_fin", "left_fin", "right_fin" and "tail_fin" (which sways). The part names
are the placeholder's, which SkorfnaFish and the renderer expect.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/SkorfnaModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/skorfna.png       (64 x 64)
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/skorfna_red.png   (64 x 64)
With --preview DIR it writes offline previews (side, three-quarter, top, beside vanilla cod and the cerna).

Run:  art/.venv/bin/python art/src/fish_skorfna_model.py [--preview DIR]
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
                    "SkorfnaModel.java")
TEXTURES = {
    "black": os.path.join(RES, "textures", "entity", "fish", "skorfna.png"),
    "red": os.path.join(RES, "textures", "entity", "fish", "skorfna_red.png"),
}
TW, TH = 64, 64


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


# Body ramp 0 (pale belly) .. 5 (darkest back); then the features. Measured from the out-of-water photos and lifted a
# step for the water (black: black_caught_1 body #2e1c18 #47251c #503428 #644938 #826850, pale spots #b29e88; red:
# red_market #803833 #ba4e3f #d27067, belly #cfadb8 #d8a0a3).
PALETTES = {
    "black": {
        # the photos' dark brown, lifted only as far as the water needs; only the belly stays pale
        "0": "#c4a88c", "1": "#8e6648", "2": "#76503a", "3": "#5e3e2e", "4": "#4a3024", "5": "#38241c",
        "C": "#a88466",                 # the few lighter flaps (never cream)
        "B": "#2e1c16", "R": "#7a3e2c",  # blotches: dark brown, red-brown
        "e": "#8e6648",                 # the skin round the eye
        "E": "#0c0908",                 # the eye
        "L": "#8e6648", "J": "#a88262", "M": "#4a2c22",   # the lip and chin in the body's light tone, the gape
        "F": "#7e5a40", "f": "#654532", "D": "#3e281e", "r": "#a2805e",   # fins: membrane, shaded, bands, light base
        "S": "#2e1c16",                 # dorsal spines and their tips
        "K": "#3e281e", "k": "#76503a",  # the cirri: dark tip, mid tone
        "W": "#a88262",                 # chin flaps (the red one's; the black keeps the chin colour)
    },
    "red": {
        # scarlet (hue about 5-8 degrees), darker red-brown mottling, cream-pink blotches, a pale pink belly
        "0": "#f4cfc8", "1": "#e8786a", "2": "#d85a4a", "3": "#c0443a", "4": "#a03430", "5": "#7c2826",
        "C": "#eeb4a8",
        "B": "#6a2622", "R": "#8a3a2e",
        "e": "#e8786a",
        "E": "#140a08",
        "L": "#d85a4a", "J": "#eca090", "M": "#7c2a26",
        "F": "#d8604e", "f": "#b84a3e", "D": "#7c2826", "r": "#f0a090",
        "S": "#6a2622",
        "K": "#7c2826", "k": "#c0443a",
        "W": "#f8dcd4",
    },
}
CLEAR = (0, 0, 0, 0)

# --- the model -------------------------------------------------------------------------------------------------------
# Parts: name -> (parent, pivot (absolute model pixels), (xRot, yRot, zRot)). Cubes: (name, part, (U, V) top-left of
# the used texture area, (x0, y0, z0) absolute, (w, h, d)). Absolute: x across, y down (24 = ground), z head (-) to
# tail (+). The UVs are packed by pack() below.
PARTS = {
    "body": (None, (0.0, 21.0, 0.0), (0.0, 0.0, 0.0)),
    "head_flaps": ("body", (0.0, 19.0, -5.0), (0.0, 0.0, 0.0)),
    "top_fin": (None, (0.0, 18.0, -4.0), (0.0, 0.0, 0.0)),
    # the pectoral fans: broad plates hinged along the flank just behind the gill cover, spread out sideways (about 35
    # degrees below level) and swept a little back, so their outer edge stays above the belly line
    "right_fin": (None, (-2.0, 19.0, -2.0), (0.0, -0.3, 0.95)),
    "left_fin": (None, (2.0, 19.0, -2.0), (0.0, 0.3, -0.95)),
    "tail_fin": (None, (0.0, 21.0, 5.0), (0.0, 0.0, 0.0)),
}
SPECS = [
    # the head: the upper lip (1 px, so the snout's top and the chin both step back under and over it), the snout
    # (its top row set 1 px further back, so the forehead rises in steps), the bony crown between the eyes, the broad
    # gill covers
    ("lip", "body", (-2.0, 21.0, -7.0), (4, 1, 1)),
    ("head_front", "body", (-2.5, 20.0, -6.0), (5, 3, 2)),
    ("head_top", "body", (-2.5, 19.0, -5.0), (5, 1, 1)),
    ("crown", "body", (-1.5, 18.0, -5.0), (3, 1, 1)),
    ("head_back", "body", (-3.0, 18.0, -4.0), (6, 5, 2)),
    # the body, tapering in width and depth to the slim stalk: 6 x 5 at the head, 4 x 4, 3 x 3, 2 x 2
    ("trunk", "body", (-2.0, 18.0, -2.0), (4, 4, 3)),
    ("rear", "body", (-1.5, 19.0, 1.0), (3, 3, 2)),
    ("stalk", "body", (-1.0, 20.0, 3.0), (2, 2, 2)),
    # small fins under the body: pelvic fins under the throat, the anal fin under the rear
    ("pelvic_r", "body", (-1.5, 22.0, -4.0), (0, 2, 2)),
    ("pelvic_l", "body", (1.5, 22.0, -4.0), (0, 2, 2)),
    ("anal", "body", (0.0, 21.0, 1.0), (0, 2, 2)),
    # the cirri: a fleshy flap standing on the brow over each eye
    ("cirrus_r", "head_flaps", (-2.5, 17.0, -5.0), (0, 2, 1)),
    ("cirrus_l", "head_flaps", (2.5, 17.0, -5.0), (0, 2, 1)),
    # the long dorsal fin, one plane from behind the head to the stalk
    ("dorsal", "top_fin", (0.0, 15.0, -5.0), (0, 5, 10)),
    # the pectoral fans
    ("pec_r", "right_fin", (-2.0, 19.0, -2.0), (0, 4, 4)),
    ("pec_l", "left_fin", (2.0, 19.0, -2.0), (0, 4, 4)),
    # the rounded fan tail
    ("caudal", "tail_fin", (0.0, 18.5, 5.0), (0, 5, 3)),
]


def footprint(size):
    """The texture area a cube needs, including the unused rows (or columns) that keep its texOffs non-negative."""
    w, h, d = size
    if w == 0:
        return 2 * d, d + h
    if h == 0:
        return d + 2 * w, d
    return 2 * d + 2 * w, d + h


def used_corner(size, x, y):
    """Where a cube's used area starts, for the packed area at (x, y): planes skip their unused rows or columns."""
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
ROW_SHADE = {17: 4, 18: 4, 19: 3, 20: 3, 21: 2, 22: 1, 23: 0}
# The side of the fish: features by (y, z) texel (letters are PALETTE keys; '-' / '+' one shade darker / lighter)
FEAT = {
    (19, -5): "E",                                  # the eye, high on the head, under the cirrus
    (20, -5): "e", (20, -6): "e", (19, -4): "e",    # warm tan skin round it
    (21, -7): "L", (21, -6): "M", (22, -5): "M",    # the lip; the gape, a line sloping back and down from its corner
    (22, -6): "J",                                  # the chin, stepped back 1 px under the lip
    (19, -3): "-", (20, -3): "-", (21, -3): "-",    # the gill cover's rim
}
SADDLES_SIDE = {(y, z) for y in (18, 19, 20) for z in (-2, -1)} | {(y, z) for y in (19, 20, 21) for z in (2, 3)} | {
    (20, 4), (21, 4)}

# Fin outlines, one character per texel, top row first (the plane's own rows and columns, from its corner)
def dorsal_grid():
    """The dorsal fin, rows y 15..19, columns z -5..4, one continuous plane from over the gill cover to the stalk:
    five spines (every other column, dark with darker tips) standing 1 px proud of a mid-brown membrane that fills
    between them; tallest at the head end and stepping down about 1 px every 3 px toward the tail. Rows under the back
    are hidden in the body."""
    back = {-5: 18, -4: 18, -3: 18, -2: 18, -1: 18, 0: 18, 1: 19, 2: 19, 3: 20, 4: 20}   # the body's top
    top = {-5: 15, -4: 16, -3: 15, -2: 16, -1: 16, 0: 17, 1: 17, 2: 18, 3: 18, 4: 19}
    spines = (-5, -3, -1, 1, 3)
    rows = []
    for y in range(15, 20):
        row = ""
        for z in range(-5, 5):
            if y < top[z]:
                row += "."
            elif y >= back[z]:
                row += "f"                      # hidden in the body
            elif z in spines:
                row += "S" if y == top[z] else "D"
            else:
                row += "F" if y == top[z] else "f"
        rows.append(row)
    return rows


DORSAL = dorsal_grid()
# the pectoral fan, rows from the hinge (y 19) down, columns z -2..1 (front to back): a light base at the root, a
# darker band parallel to the rim, then the darker rim along the back and lower edges, the outer corners cut
PECTORAL = [
    "rrF.",
    "rFfD",
    "FffD",
    ".DD.",
]
# the rounded tail, rows y 18.5..23.5, columns z 5..7: the corners cut, a dark band across the middle
CAUDAL = [
    ".F.",
    "fDF",
    "fDr",
    "fDF",
    ".F.",
]
PELVIC = ["12", "21"]
ANAL = ["21", "12"]
# the cirrus over each eye, rows y 17..18, column z -5: a small fleshy flap in the body's mid tone, dark at the tip
CIRRUS = [
    "k",
    "K",
]
FINS = {"dorsal": DORSAL, "pec_r": PECTORAL, "pec_l": PECTORAL, "caudal": CAUDAL, "pelvic_r": PELVIC,
        "pelvic_l": PELVIC, "anal": ANAL, "cirrus_r": CIRRUS, "cirrus_l": CIRRUS}


LIFT = {"black": 1.18, "red": 1.06}   # the in-game check: the water still read them darker than vanilla cod


def lifted(c, k):
    h, s, v = colorsys.rgb_to_hsv(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
    r, g, b = colorsys.hsv_to_rgb(h, s, min(1.0, v * k))
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)), 255)


def ramp(pal, shade):
    return pal[str(max(0, min(5, shade)))]


def hash01(*vals):
    return CE.hash01(*vals)


def mottle(base, yi, zi, salt):
    """Blotchy mottling in 2 px patches (never a lone 1 px dot): the patch's shift comes from the pair of texels."""
    r = hash01(salt, yi, zi // 2)
    if r < 0.22:
        return base - 1
    if r > 0.78:
        return base + 1
    return base


def blotch(yi, zi, salt):
    """Irregular blotches 1-3 px long: a texel starts one, or carries on the one in front of it."""
    def start(z):
        return hash01(salt, yi, z) < 0.2
    if start(zi) or (start(zi - 1) and hash01(salt + 1, yi, zi) < 0.6) or (
            start(zi - 2) and hash01(salt + 1, yi, zi - 1) < 0.6 and hash01(salt + 2, yi, zi) < 0.4):
        return "R" if hash01(salt + 3, yi, zi - (zi % 2)) < 0.4 else "B"
    return None


def side_colour(pal, variant, y, z, face):
    yi, zi = int(math.floor(y)), int(math.floor(z))
    row = ROW_SHADE[yi]
    ch = FEAT.get((yi, zi), ".")
    if ch == "E" and face not in ("west", "east"):
        ch = "e"
    if variant == "red" and yi == 22 and zi in (-4, -3):
        return pal["W"]          # the red one's chin flaps: a pale fringe along the jaw and throat
    if ch in pal:
        return pal[ch]
    near_eye = yi <= 20 and zi <= -3
    if not near_eye and yi <= 21:
        b = blotch(yi, zi, 21)
        if b:
            return pal[b]
        if variant == "red" and hash01(31, yi, zi // 2) < 0.14:
            return pal["C"]      # the red one's cream-pink blotches, 2 px
    shade = row + (1 if ch == "-" else -1 if ch == "+" else 0)
    if (yi, zi) in SADDLES_SIDE:
        shade += 1
    if ch == "." and yi != 19:   # the eye's row stays plain (no dots beside the eye)
        shade = mottle(shade, yi, zi, 11)
    return ramp(pal, shade)


SADDLES = (-2, -1, 2, 3)     # z columns where the dark saddles cross the back


def top_colour(pal, variant, x, z):
    """The back seen from above, the view seen most: lit from the top left (the fish's right flank and the head end
    lighter), 4-6 mottled tones, saddles across the back, and on the head a few skin-flap blotches."""
    xi, zi = int(math.floor(x * 2)), int(math.floor(z))
    shade = 2 + (1 if x > -0.5 else 0) + (1 if x > 1.5 else 0) + (1 if zi >= 1 else 0)
    if zi in SADDLES:
        shade += 1
    r = hash01(7, xi, zi)
    if r < 0.2:
        shade -= 1
    elif r > 0.8:
        shade += 1
    if zi <= -3:
        f = hash01(9, xi, zi)
        if f < 0.18:
            return pal["R"]      # skin flaps on the bony head
        if f > 0.86:
            return pal["C"] if variant == "red" else pal["k"]
    return ramp(pal, shade)


def body_colour(pal, variant, name, face, x, y, z, x0, y0, z0, w, h, d):
    if name == "lip":
        if face in ("north", "top", "bottom"):
            return pal["L"]
    if name == "head_front" and face == "north":
        # the face behind the lip: the gape's corners either side of the lip, the chin below it
        yi = int(math.floor(y))
        if yi == 22:
            if variant == "red" and int(math.floor(x * 2)) % 2 == 0:
                return pal["W"]      # the red one's chin flaps
            return pal["J"]
        if yi == 21:
            return pal["M"]          # only the corners show, beside the lip
        return pal["e"]
    if face == "top":
        return top_colour(pal, variant, x, z)
    if face == "bottom":
        if variant == "red" and z < -3:
            return pal["W"] if int(math.floor(x * 2) + math.floor(z)) % 2 == 0 else ramp(pal, 0)
        return ramp(pal, mottle(0, int(math.floor(x * 2)), int(math.floor(z)), 3))
    if face == "north":
        return side_colour(pal, variant, y, z0, face)
    if face == "south":
        return side_colour(pal, variant, y, z0 + d - 1, face)
    return side_colour(pal, variant, y, z, face)


def fin_colour(pal, name, cube, y, z):
    _, _, _, (x0, y0, z0), _ = cube
    grid = FINS[name]
    r, c = int(math.floor(y - y0)), int(math.floor(z - z0))
    ch = grid[r][c]
    return CLEAR if ch == "." else pal[ch]


def draw_texture(variant):
    pal = {k: (hexc(v) if k == "E" else lifted(hexc(v), LIFT[variant])) for k, v in PALETTES[variant].items()}
    img = Image.new("RGBA", (TW, TH), CLEAR)
    owner = {}
    for cube in CUBES:
        name, _, _, (x0, y0, z0), (w, h, d) = cube
        for face, u, v, x, y, z in CE.face_texels(cube):
            assert 0 <= u < TW and 0 <= v < TH, (name, face, u, v)
            assert owner.setdefault((u, v), name) == name, ("texture overlap", name, owner[(u, v)], u, v)
            if w == 0 or h == 0:
                col = fin_colour(pal, name, cube, y, z)
            else:
                col = body_colour(pal, variant, name, face, x, y, z, x0, y0, z0, w, h, d)
            img.putpixel((u, v), col)
    return img


# --- the Java model ---------------------------------------------------------------------------------------------------
def write_java():
    f = CE.f
    lines = []
    for part in ("body", "head_flaps", "top_fin", "right_fin", "left_fin", "tail_fin"):
        parent, (px, py, pz), rot = PARTS[part]
        builder = "CubeListBuilder.create()"
        for cube in [c for c in CUBES if c[1] == part]:
            name, _, _, (x0, y0, z0), (w, h, d) = cube
            u, v = CE.tex_offset(cube)
            builder += "\n            /* %s */ .texOffs(%d, %d).addBox(%s, %s, %s, %d.0F, %d.0F, %d.0F)" % (
                name, u, v, f(x0 - px), f(y0 - py), f(z0 - pz), w, h, d)
        ox, oy, oz = px, py, pz
        if parent:
            ppx, ppy, ppz = PARTS[parent][1]
            ox, oy, oz = px - ppx, py - ppy, pz - ppz
        if any(rot):
            pose = "PartPose.offsetAndRotation(%s, %s, %s, %s, %s, %s)" % (f(ox), f(oy), f(oz), f(rot[0]), f(rot[1]),
                                                                           f(rot[2]))
        else:
            pose = "PartPose.offset(%s, %s, %s)" % (f(ox), f(oy), f(oz))
        target = parent or "root"
        prefix = "PartDefinition body = " if part == "body" else ""
        lines.append("        %s%s.addOrReplaceChild(\"%s\", %s,\n            %s);" % (prefix, target, part, builder,
                                                                                  pose))
    src = """package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The skorfna (scorpionfish): long and tapering, not round, with a big broad spiny head (a third of the length), a wide
 * downturned mouth, high eyes under fleshy flaps, a long spiny dorsal fin with a notch, big fan pectoral fins splayed to
 * prop it on the floor, a slim stalk and a rounded banded tail that sways. 15 px long, 5 px deep (8 with the spines),
 * 6 px across the head; head toward -z, the ground at y 24. One model for both kinds: textures/entity/fish/skorfna.png
 * (the black scorpionfish) and skorfna_red.png (the red one) share every UV (64 x 64).
 * Made by art/src/fish_skorfna_model.py (don't edit by hand).
 */
public class SkorfnaModel extends FishModel {
    public SkorfnaModel(ModelPart root) {
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
def previews(out_dir, textures):
    os.makedirs(out_dir, exist_ok=True)
    cod = CE.vanilla_texture("cod")
    cerna_tex = Image.open(os.path.join(RES, "textures", "entity", "fish", "cerna.png")).convert("RGBA")
    rows = []
    for variant, tex in textures.items():
        views = [CE.render(CUBES, PARTS, tex, v, 16) for v in ("side", "three", "top")]
        for v, im in zip(("side", "three", "top"), views):
            im.save(os.path.join(out_dir, "skorfna_%s_%s16.png" % (variant, v)))
        rows.append(views)
    scale = [CE.render(CUBES, PARTS, textures["black"], "side", 8), CE.render(CUBES, PARTS, textures["red"], "side", 8)]
    if cod:
        scale.append(CE.render(CE.vanilla_cubes(CE.COD_CUBES), CE.COD_PARTS, cod, "side", 8))
    scale.append(CE.render(CE.CUBES, CE.PARTS, cerna_tex, "side", 8))
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
    sheet.save(os.path.join(out_dir, "skorfna_sheet.png"))
    for variant, tex in textures.items():
        tex.resize((TW * 4, TH * 4), Image.NEAREST).save(os.path.join(out_dir, "skorfna_%s_tex4.png" % variant))


def main():
    textures = {}
    for variant, path in TEXTURES.items():
        tex = draw_texture(variant)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tex.save(path)
        textures[variant] = tex
    write_java()
    print("wrote", ", ".join(os.path.relpath(p, ROOT) for p in TEXTURES.values()), "and", os.path.relpath(JAVA, ROOT))
    args = sys.argv[1:]
    if "--preview" in args:
        out = args[args.index("--preview") + 1]
        previews(out, textures)
        print("previews in", out)


if __name__ == "__main__":
    main()
