"""The lionfish (Pterois miles, the devil firefish, invasive in Malta since 2016) as a swimming mob.

Drawn from the reference photos in art/references/fish_lionfish_refonly/ (list.tsv): lf10 (a specimen out of the water)
for the true colour, lf02, lf06 and lf08 (side views) for the proportions, lf04 (from above) for the fans. What makes it
a lionfish, not its relative the skorfna and not a "spiny fish" like the John Dory:
  - bold vertical bands all over: broad red-brown bands with thin cream-white ones between, on the body, the head and
    every fin; darker on the back, fading to a pale cream belly (countershaded);
  - a row of long, SEPARATE dorsal spines, banded red-brown and white, standing well above the back with clear gaps
    (the skorfna's spines are short and joined by membrane);
  - huge fan pectoral fins hinged behind the head, hanging down and swept back along the flanks, with banded rays and
    a ragged, fringed rim (they droop like fans, never spread level like a bird's wings);
  - a feathery tentacle over each eye, banded, and a small one at the corner of the mouth;
  - a slim, compressed body (3 px thick), a short snout, a round fan tail with rows of bands;
  - the eye the only black mark on the fish, ringed by pale skin; no stripe is broken into dots.
The palette sits a step lighter than the photos (water greys and darkens everything).

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, root
children "body" (with "head_flaps"), "top_fin", "left_fin", "right_fin" and "tail_fin" (which sways). The part names
are the placeholder's.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/LionfishModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/lionfish.png   (64 x 64)
With --preview DIR it writes offline previews of every candidate (side, three-quarter, top, beside cod, cerna, skorfna).

Run:  art/.venv/bin/python art/src/fish_lionfish_model.py [--preview DIR]
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
                    "LionfishModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "lionfish.png")
TW, TH = 64, 64
CANDIDATE = "C"   # the band pattern installed in the mod (the redo's candidates A, B, C: see BANDS)
PALETTE = "D"     # the palette all three band patterns use (the redo's; C is the accepted icon's)


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


# Keys: "d0".."d3" the red-brown bands (d0 the belly's faint pink, d3 the back's darkest), "p0".."p3" the cream bands
# (p0 the belly's whitest, p3 the back's), "E" the eye, "e" the pale skin round it, "M" the mouth line, fins: "F" the
# cream membrane, "R" the red-brown ray bands, "r" a lighter rim band, "S" the spines' dark bands, "s" their pale bands.
# Measured from lf10 (out of the water): bands #8a2a1c #a8402a, cream #e8d2be; in water (lf02, lf06) the bands are
# deeper red-brown #5c2a22 and the cream greyer.
PALETTES = {
    # D (the redo, 2026-11-19, after the owner's "too fat and the colours are very flat"): the creams warmed to peach
    # so they stay warm under the blue water, the dark bands much darker and the red bands a lighter, stronger rust so
    # the two band colours stay apart in the water; a near-white belly. C below stays as the accepted icon's palette.
    "D": {"d0": "#d89a84", "d1": "#4a2014", "d2": "#3e1a10", "d3": "#321610",
          "p0": "#faeee4", "p1": "#f2c8b0", "p2": "#e8b498", "p3": "#c08a6c",
          "E": "#0c0908", "e": "#f6dcc8", "M": "#48180e",
          "F": "#f0cdb4", "R": "#8c3a22", "r": "#c06a48", "S": "#a04428", "s": "#f2d0b8",
          "T": "#8a5a40", "t": "#3a1a10",
          "h0": "#eaa486", "h1": "#c4582e", "h2": "#b04a2a", "h3": "#943a1e"},
    # A: deep red-brown bands on cream, as the lionfish looks under water near Malta
    "A": {"d0": "#e0a894", "d1": "#c46a50", "d2": "#ac5038", "d3": "#8c3e2c",
          "p0": "#f6eee2", "p1": "#eee0cc", "p2": "#e2ceb6", "p3": "#c8ac92",
          "E": "#0c0908", "e": "#f2e4d0", "M": "#5a2018",
          "F": "#e8d8c2", "R": "#9a4430", "r": "#c87a5e", "S": "#9a4430", "s": "#f0e2d0",
          "T": "#a07a5e", "t": "#6e2a1e",
          "h0": "#e4a48c", "h1": "#c4583c", "h2": "#a8442c", "h3": "#883420"},
    # B: brighter brick red (the out-of-water specimen), cream a touch warmer
    "B": {"d0": "#e4a894", "d1": "#c0583e", "d2": "#a8402c", "d3": "#863020",
          "p0": "#f8eee0", "p1": "#f2dcc6", "p2": "#e8ccb0", "p3": "#d0a888",
          "E": "#0c0908", "e": "#f6e2cc", "M": "#601c12",
          "F": "#f0d8c0", "R": "#b04a32", "r": "#d8846a", "S": "#a8402c", "s": "#f6e2cc",
          "T": "#ac7c5c", "t": "#7a2a1a",
          "h0": "#eeac94", "h1": "#d0603e", "h2": "#b84c30", "h3": "#943a22"},
    # C: darker chocolate-brown bands (the Red Sea photos), more contrast
    "C": {"d0": "#c89884", "d1": "#7e3e2c", "d2": "#66301f", "d3": "#4c2216",
          "p0": "#f4ece0", "p1": "#ece0cc", "p2": "#ddc8b0", "p3": "#c0a48a",
          "E": "#0c0908", "e": "#f0e2cc", "M": "#48180e",
          "F": "#e4d4be", "R": "#7c3a2a", "r": "#b47058", "S": "#8a3a28", "s": "#eee0cc",
          "T": "#8c6a52", "t": "#5c3424",
          "h0": "#d8a08a", "h1": "#a85038", "h2": "#8e3e2a", "h3": "#70301e"},
}
CLEAR = (0, 0, 0, 0)
LIFT = 1.12   # a small lift for the water, on top of the step already in the palette

# --- the model -------------------------------------------------------------------------------------------------------
# Parts: name -> (parent, pivot (absolute model pixels), (xRot, yRot, zRot)). Cubes: (name, part, (x0, y0, z0)
# absolute, (w, h, d)). Absolute: x across, y down (24 = ground), z head (-) to tail (+). UVs packed by pack().
PARTS = {
    "body": (None, (0.0, 20.0, 0.0), (0.0, 0.0, 0.0)),
    "head_flaps": ("body", (0.0, 17.0, -5.0), (0.0, 0.0, 0.0)),
    # the spines, leaning back a little from the line of the back
    "top_fin": (None, (0.0, 17.0, -2.0), (-0.22, 0.0, 0.0)),
    # the pectoral fans: hinged on the flank behind the gill cover, hanging down and out (about 45 degrees) and swept
    # back along the body, so from the side they spread behind and below the head like a fan, never level like wings
    "right_fin": (None, (-1.0, 19.0, -3.0), (0.0, -0.3, 0.6)),
    "left_fin": (None, (1.0, 19.0, -3.0), (0.0, 0.3, -0.6)),
    "tail_fin": (None, (0.0, 19.0, 5.0), (0.0, 0.0, 0.0)),
}
SPECS = [
    # the head: a short snout with the mouth, then the head with the eyes, as deep as the body
    ("snout", "body", (-1.0, 18.5, -7.0), (2, 2, 1)),
    ("head", "body", (-1.0, 17.0, -6.0), (2, 4, 3)),
    # the body: compressed like the real fish, 2 px thick and 4 deep, tapering to a slim stalk
    ("trunk", "body", (-1.0, 17.0, -3.0), (2, 4, 4)),
    ("rear", "body", (-1.0, 17.5, 1.0), (2, 3, 3)),
    ("stalk", "body", (-0.5, 18.0, 4.0), (1, 2, 1)),
    # small fins under the body: long pelvic fins under the throat, the anal fin under the rear
    ("pelvic_r", "body", (-0.5, 21.0, -4.0), (0, 2, 3)),
    ("pelvic_l", "body", (0.5, 21.0, -4.0), (0, 2, 3)),
    ("anal", "body", (0.0, 20.5, 1.0), (0, 2, 3)),
    # the low soft dorsal fin behind the spines
    ("soft_dorsal", "body", (0.0, 15.5, 1.0), (0, 2, 3)),
    # the feathery tentacles over the eyes
    ("tent_r", "head_flaps", (-1.0, 15.0, -5.0), (0, 2, 1)),
    ("tent_l", "head_flaps", (1.0, 15.0, -5.0), (0, 2, 1)),
    # the separate venomous spines, tallest at the front; and the low membrane joining their bases
    ("spine_1", "top_fin", (0.0, 11.0, -5.0), (0, 6, 1)),
    ("spine_2", "top_fin", (0.0, 11.0, -3.0), (0, 6, 1)),
    ("spine_3", "top_fin", (0.0, 12.0, -1.0), (0, 5, 1)),
    ("spine_4", "top_fin", (0.0, 13.0, 1.0), (0, 4, 1)),
    ("spine_web", "top_fin", (0.0, 16.0, -5.0), (0, 1, 7)),
    # the fans
    ("pec_r", "right_fin", (-1.0, 19.0, -3.0), (0, 3, 7)),
    ("pec_l", "left_fin", (1.0, 19.0, -3.0), (0, 3, 7)),
    # the round fan tail
    ("caudal", "tail_fin", (0.0, 16.5, 5.0), (0, 5, 3)),
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
# The bands, by z column: None cream, "b" dark chocolate brown, "r" a warmer red. Broad 2 px bands with thin 1 px cream
# lines, as on the real fish, the brown and warm red bands alternating so the print isn't one flat repeat; one dark bar
# runs down the cheek under the eye.
BANDS = {
    "A": {-5: "b", -3: "b", -2: "b", 0: "r", 1: "r", 3: "b", 4: "b"},
    "B": {-5: "b", -3: "r", -2: "r", 0: "b", 1: "b", 3: "r", 4: "r"},
    "C": {-5: "b", -3: "b", -2: "r", 0: "b", 1: "r", 3: "b", 4: "r"},
}
EYE = (18, -5)   # (y, z): high on the head, behind the snout
# rows: 3 the back .. 0 the belly (countershading); the belly row keeps faint pink bands
ROW_TONE = {14: 3, 15: 3, 16: 3, 17: 3, 18: 2, 19: 1, 20: 0}


def shade(c, k):
    return (max(0, min(255, int(round(c[0] * k)))), max(0, min(255, int(round(c[1] * k)))),
            max(0, min(255, int(round(c[2] * k)))), c[3])


def jitter(c, *key):
    """A small texel-to-texel change in brightness (+-5 %), so a band reads as skin, not a flat print."""
    return shade(c, 0.95 + 0.1 * CE.hash01(*key))


def stripe(pal, yi, zi, variant):
    tone = ROW_TONE.get(yi, 0)
    band = BANDS[variant].get(zi)
    if yi >= 20:
        return jitter(pal["p0"], 41, yi, zi)    # the belly row: near white, no bands (countershading)
    if band is None:
        return jitter(pal["p%d" % tone], 41, yi, zi)
    return jitter(pal[("d%d" if band == "b" else "h%d") % tone], 43, yi, zi)


def side_colour(pal, variant, y, z, face):
    yi, zi = int(math.floor(y)), int(math.floor(z))
    if (yi, zi) == EYE:
        return pal["E"] if face in ("west", "east") else pal["e"]
    if (zi == -5 and yi in (17, 19)) or (yi == 18 and zi in (-6, -4)):
        return pal["e"]          # the pale ring round the eye on every side (the cheek bar starts below it)
    if zi == -5 and yi >= 20:
        return pal["h2"]         # the rust bar down the cheek, under the eye (lighter than the eye)
    return stripe(pal, yi, zi, variant)


def top_colour(pal, variant, x, z):
    """The back from above: darker than the flanks, the bands crossing it."""
    zi = int(math.floor(z))
    return jitter(pal["t"], 47, zi, int(x * 2))   # a dark brown top edge along the whole back


def body_colour(pal, variant, name, face, x, y, z, x0, y0, z0, w, h, d):
    yi = int(math.floor(y))
    if name == "snout":
        if face == "top":
            return pal["p3"]
        if face == "bottom":
            return pal["p0"]
        return pal["p2"] if yi == 18 else pal["p1"]
    if face == "top":
        return top_colour(pal, variant, x, z)
    if face == "bottom":
        return pal["p0"]
    if face == "north":
        return side_colour(pal, variant, y, z0, face)
    if face == "south":
        return side_colour(pal, variant, y, z0 + d - 1, face)
    return side_colour(pal, variant, y, z, face)


# Fin outlines, one character per texel, top row first (the plane's own rows and columns, from its corner).
SPINE_TALL = ["s", "S", "s", "S", "s", "S"]          # banded, a pale tip
SPINE_MID = ["s", "S", "s", "S", "s"]
SPINE_LOW = ["s", "S", "s", "S"]
WEB = ["RFRFRFR"]                                      # the low membrane along the back, banded with the spines' bases
TENT = ["R", "s"]                                 # feathery, banded
# the fan: rows from the hinge (top) down, columns z -3..3 (front to back). Cream membrane crossed by red-brown bands
# that run across the rays (diagonal, so they curve round the hinge); the rim is fringed: on the last row only every
# other ray reaches out, in a lighter red-brown (a ragged, feathery edge).
def pectoral_grid(variant):
    """Seen from the side the fan sweeps back from behind the head: row 0 the membrane at the hinge, rows 1 and 2 rays
    banded red-brown and cream, the lower one fringed (every other ray reaching out). Three rows since the redo (it hung
    too low and made the fish look deep)."""
    if variant == "C":
        return ["rrrrrr.",
                "RRsRRsR",
                "R.R.R.."]
    return ["FFFFFF.",
            "RRsRRsR",
            "R.R.R.."]


PECTORAL = {v: pectoral_grid(v) for v in "ABC"}
# the round fan tail, rows y 17..21, columns z 5..7: banded across like the body, the corners cut
CAUDAL = [".F.",
          "RFR",
          "FFF",
          "RFR",
          ".F."]
SOFT_DORSAL = ["FRF", "FRF"]
PELVIC = ["FRF", ".R."]
ANAL = ["FRF", "FR."]


def fin_grid(name, variant):
    if name.startswith("spine_") and name != "spine_web":
        return {"spine_1": SPINE_TALL, "spine_2": SPINE_TALL, "spine_3": SPINE_MID, "spine_4": SPINE_LOW}[name]
    return {"spine_web": WEB, "tent_r": TENT, "tent_l": TENT, "pec_r": PECTORAL[variant],
            "pec_l": PECTORAL[variant], "caudal": CAUDAL, "soft_dorsal": SOFT_DORSAL, "pelvic_r": PELVIC,
            "pelvic_l": PELVIC, "anal": ANAL}[name]


# which face of each fin is turned away from the body (lit) and which toward it (in shadow)
OUTER = {"pec_r": "west", "pec_l": "east", "pelvic_r": "west", "pelvic_l": "east", "tent_r": "west", "tent_l": "east"}


def fin_colour(pal, variant, name, cube, face, y, z):
    """A fin texel: its outline colour, lit along the top and edge nearest the light, shading off toward its far
    edge; a paired fin's face toward the body a step darker than its outer face; the spines' and tail's right side
    (west) a little darker than their left, so a fin reads as a thin solid thing, not a print."""
    _, _, _, (x0, y0, z0), (w, h, d) = cube
    grid = fin_grid(name, variant)
    r, c = int(math.floor(y - y0)), int(math.floor(z - z0))
    ch = grid[r][c]
    if ch == ".":
        return CLEAR
    rows = max(1, len(grid) - 1)
    k = 1.06 - 0.22 * r / rows                 # lit at the top (the tips of the spines, the fan's hinge)
    if name in OUTER:
        k *= 1.0 if face == OUTER[name] else 0.84
    elif face == "west":
        k *= 0.9
    return shade(pal[ch], k)


def lifted(c, k):
    h, s, v = colorsys.rgb_to_hsv(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
    r, g, b = colorsys.hsv_to_rgb(h, s, min(1.0, v * k))
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)), 255)


def draw_texture(variant):
    pal = {k: (hexc(v) if k == "E" else lifted(hexc(v), LIFT)) for k, v in PALETTES[PALETTE].items()}
    img = Image.new("RGBA", (TW, TH), CLEAR)
    owner = {}
    for cube in CUBES:
        name, _, _, (x0, y0, z0), (w, h, d) = cube
        for face, u, v, x, y, z in CE.face_texels(cube):
            assert 0 <= u < TW and 0 <= v < TH, (name, face, u, v)
            assert owner.setdefault((u, v), name) == name, ("texture overlap", name, owner[(u, v)], u, v)
            if w == 0 or h == 0:
                col = fin_colour(pal, variant, name, cube, face, y, z)
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
 * The lionfish (Pterois miles): a slim, compressed body banded all over in red-brown and cream, a row of long separate
 * banded venomous spines, huge fan pectoral fins hanging down and back from behind the head, a feathery tentacle over
 * each eye and a round banded fan tail that sways. 15 px long, 3 px thick, 5 px deep; head toward -z, the ground at
 * y 24. Texture: textures/entity/fish/lionfish.png (64 x 64).
 * Made by art/src/fish_lionfish_model.py (don't edit by hand).
 */
public class LionfishModel extends FishModel {
    public LionfishModel(ModelPart root) {
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
def load_model(script, cubes_attr="CUBES", parts_attr="PARTS"):
    import importlib
    mod = importlib.import_module(script)
    return getattr(mod, cubes_attr), getattr(mod, parts_attr)


def previews(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    cod = CE.vanilla_texture("cod")
    cerna_tex = Image.open(os.path.join(RES, "textures", "entity", "fish", "cerna.png")).convert("RGBA")
    sk_cubes, sk_parts = load_model("fish_skorfna_model")
    sk_tex = Image.open(os.path.join(RES, "textures", "entity", "fish", "skorfna.png")).convert("RGBA")
    rows = []
    for variant in BANDS:
        tex = draw_texture(variant)
        tex.resize((TW * 4, TH * 4), Image.NEAREST).save(os.path.join(out_dir, "texture_%s.png" % variant))
        views = [CE.render(CUBES, PARTS, tex, v, 16) for v in ("side", "three", "top")]
        rows.append(views)
        sheet = Image.new("RGBA", (sum(i.width for i in views) + 80, max(i.height for i in views) + 40),
                          (72, 72, 72, 255))
        x = 20
        for im in views:
            sheet.paste(im, (x, 20), im)
            x += im.width + 20
        sheet.save(os.path.join(out_dir, "preview_%s.png" % variant))
    tex = draw_texture(CANDIDATE)
    scale = [CE.render(CUBES, PARTS, tex, "side", 8)]
    if cod:
        scale.append(CE.render(CE.vanilla_cubes(CE.COD_CUBES), CE.COD_PARTS, cod, "side", 8))
    scale.append(CE.render(sk_cubes, sk_parts, sk_tex, "side", 8))
    scale.append(CE.render(CE.CUBES, CE.PARTS, cerna_tex, "side", 8))
    W = sum(i.width for i in scale) + 20 * len(scale) + 20
    H = max(i.height for i in scale) + 40
    sheet = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    x = 10
    for im in scale:
        sheet.paste(im, (x, H - 20 - im.height), im)
        x += im.width + 20
    sheet.save(os.path.join(out_dir, "scale_vs_cod_skorfna_cerna.png"))


def main():
    tex = draw_texture(CANDIDATE)
    os.makedirs(os.path.dirname(TEXTURE), exist_ok=True)
    tex.save(TEXTURE)
    write_java()
    print("wrote", os.path.relpath(TEXTURE, ROOT), "and", os.path.relpath(JAVA, ROOT))
    args = sys.argv[1:]
    if "--preview" in args:
        out = args[args.index("--preview") + 1]
        previews(out)
        print("previews in", out)


if __name__ == "__main__":
    main()
