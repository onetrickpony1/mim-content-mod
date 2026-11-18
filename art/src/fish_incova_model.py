"""The incova (European anchovy, Engraulis encrasicolus) as a swimming mob: its 3D model and its texture.

The anchovy's last piece; its item icon, bucket and spawn egg are owner-accepted. The owner: anchovies are NOT
sardines (2026-11-18), so the model is built to read differently from the accepted sardina model
(art/src/fish_sardina_model.py), from the photos in art/references/fish_incova_refonly/ (list.tsv):
  - slimmer and rounder in cross-section: a cigar 2 px wide and 2 px deep (square, so it reads round), where the
    sardina is 2 wide and 3 deep (a flattened spindle). Body depth to body length is 2 to 10 (0.20), the sardina's
    3 to 11 (0.27), cod's 4 to 11 (0.36);
  - a long pointed snout overhanging the mouth: a 1 px wide tip, then a 2 px wide snout, both only in the top row,
    on the back's line, so the head ends in a point two pixels in front of the lower jaw;
  - a long underslung mouth: the lower jaw starts under the eye as a narrow (1 px) chin, set in from the cheeks; the
    snout's underside is the grey gape, and a grey mouth line runs from the chin back past the eye, fading behind it (no
    dark pixel under the eye, so it never reads as a second eye);
  - a large eye set far forward: one black texel two pixels behind the snout tip, in the green head, with no pale
    ring or bright pixel touching it;
  - a bright silver band along the flank, one unbroken near-white row from behind the gill cover to the tail stalk;
  - a greenish to blue-green back, darkening along the body to the tail and at the snout's point; seen from above the
    back is the dark blue-green of the icon;
  - no dark spots, no gold gill cover;
  - a forked tail (two lobes and an open notch), a small triangular dorsal fin mid-back, small pelvic and anal fins
    and low pectoral fins, every fin touching the body.
The palette is the accepted item icon's (art/src/fish_incova_icon.py PAL), each colour lifted a step for the water
(the game greys and darkens everything under water); the eye stays black.

Size: the hitbox is 0.35 x 0.2 blocks (5.6 x 3.2 model pixels). The incova is 13 px long (10 of body from the snout
tip, 3 of tail), against the sardina's 14 (11 + 3) and cod's 15; 2 px deep (4 with the dorsal and pelvic fins) and
2 px wide. One texture pixel per model pixel, like vanilla's fish.

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, a root
child "body" and a "tail_fin" that sways like vanilla cod's.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/IncovaModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/incova.png    (32 x 32)
With --sheet SCREENSHOT_DIR also writes the compare sheet art/candidates/fish_incova_model.png (offline previews go
to the folder given with --preview DIR, or art/candidates/tmp_incova).

Run:  art/.venv/bin/python art/src/fish_incova_model.py [--preview DIR] [--sheet SCREENSHOT_DIR]
"""
import colorsys
import glob
import math
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fish_sardina_model as sard  # noqa: E402  (the shared box-UV layout, previews and vanilla cod geometry)

ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "fish",
                    "IncovaModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "incova.png")
TW, TH = 32, 32


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16))


def lift(c, k=1.18, add=0.05, hue=0.0):
    """One step lighter for the water: brightness scaled up a little, saturation kept; hue in degrees."""
    h, s, v = colorsys.rgb_to_hsv(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
    r, g, b = colorsys.hsv_to_rgb((h + hue / 360.0) % 1.0, s, min(1.0, v * k + add))
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)), 255)


# The accepted icon's palette (art/src/fish_incova_icon.py PAL, round 2), copied by value so this file stands alone.
ICON = {
    "h": "#86b89e", "k": "#244c48", "m": "#3f7568",          # back: lit green sheen, dark blue-green, blue-green
    "W": "#f6faf8", "s": "#c3cdd0", "g": "#8c99a1", "o": "#3a4650",   # band, silver, grey, belly rim
    "j": "#4e5a62", "J": "#9aa6ab",                            # the mouth line, dark then fading
    "p": "#dfe5e3",                                            # the pale lower jaw
    "F": "#93b0a6", "f": "#6f8e86",                            # dorsal fin: lit tip, fin
    "a": "#5f6d78",                                            # pelvic and anal fins
    "T": "#7a9a93", "u": "#5f837c", "t": "#4c6763",            # tail: lit upper lobe, base, shaded lower lobe
}
PAL = {key: lift(hexc(v)) for key, v in ICON.items()}
# The back keeps the icon's teal hues (round 2, critic: an extra greener lift read emerald on land, not the icon's
# teal), lifted with a smaller added step than the rest so the darkest back stays within about +15 lightness of the
# icon's (hues within 1 degree of the icon's).
for key in "hmk":
    PAL[key] = lift(hexc(ICON[key]), k=1.18, add=0.02)
# one blend between the icon's blue-green (m) and dark back (k), so the side of the back darkens along the body in
# steps instead of jumping
PAL["M"] = tuple((a + b) // 2 for a, b in zip(PAL["m"], PAL["k"]))
PAL["E"] = (11, 13, 13, 255)          # the eye: the icon's black, not lifted
PAL["."] = (0, 0, 0, 0)
CLEAR = PAL["."]


# --- the model -------------------------------------------------------------------------------------------------------
# Parts: name -> (parent, pivot (absolute model pixels), zRot). Cubes: (name, part, (U, V) top-left of the used texture
# area, (x0, y0, z0) absolute, (w, h, d)). Absolute: x across, y down (24 = ground), z head (-) to tail (+).
PARTS = {
    "body": (None, (0.0, 21.0, 0.0), 0.0),
    "tail_fin": (None, (0.0, 22.0, 5.0), 0.0),
    # hinged on the belly's edges and hanging steeply, close to the flank (seen flatter from the side, never edge-on
    # across the silver band when the fish lies on land)
    "right_fin": (None, (-1.0, 23.0, -1.0), -1.2),
    "left_fin": (None, (1.0, 23.0, -1.0), 1.2),
}
CUBES = [
    # the long pointed snout (top row only): a narrow tip, then the full-width snout with the big eye
    ("tip", "body", (26, 0), (-0.5, 21.0, -5.0), (1, 1, 1)),
    ("snout", "body", (18, 0), (-1.0, 21.0, -4.0), (2, 1, 2)),
    # the narrow chin under the eye: the front of the underslung lower jaw, set back two pixels from the snout tip
    ("chin", "body", (26, 2), (-0.5, 22.0, -3.0), (1, 1, 1)),
    # the head with the jaw and gill cover, the trunk, the narrowing rear and the thin tail stalk
    ("head", "body", (10, 0), (-1.0, 21.0, -2.0), (2, 2, 2)),
    ("trunk", "body", (0, 0), (-1.0, 21.0, 0.0), (2, 2, 3)),
    ("rear", "body", (0, 5), (-0.5, 21.0, 3.0), (1, 2, 1)),
    ("stalk", "body", (4, 5), (-0.5, 21.5, 4.0), (1, 1, 1)),
    # the small dorsal fin mid-back, the pelvic fin under the trunk and the anal fin under the rear
    ("dorsal", "body", (8, 5), (0.0, 19.0, 0.0), (0, 2, 3)),
    ("pelvic", "body", (20, 5), (0.0, 23.0, 0.0), (0, 1, 1)),
    ("anal", "body", (22, 5), (0.0, 23.0, 3.0), (0, 1, 1)),
    # the forked tail
    ("caudal", "tail_fin", (14, 5), (0.0, 20.0, 5.0), (0, 4, 3)),
    # the pectoral fins, low behind the gill cover on the belly's edges, hanging down and a little out
    ("pec_r", "right_fin", (24, 5), (-2.0, 23.0, -1.0), (1, 0, 2)),
    ("pec_l", "left_fin", (26, 5), (1.0, 23.0, -1.0), (1, 0, 2)),
]

# The side of the fish, rows y 21 (the back) and y 22 (the flank), columns z -5..4. One character per pixel.
# Row 21: the snout's point a shade darker as it turns away (M), the green snout and head (m), the eye (E), then the
# back darkening toward the tail (M, k).
# Row 22: under the snout nothing (it overhangs); the mouth line runs in grey (g) from the chin under the eye back past
# the eye, fading behind it (J), never dark enough beside the eye to read as a second one; then the bright silver band (W) to the rear; the stalk is silver (s).
SIDE_Z0 = -5
SIDE = {
    21: "MmEmmmMMkk",
    22: "..ggJWWWWs",
}
# The back seen from above, by z column: green on the snout and head, the dark blue-green back, darkest at the tail.
TOP = "mmmMkkkkkk"
# The belly seen from below: the grey gape under the snout, the pale chin, then the icon's silver-grey (g), so the
# belly shades away from the bright band on the flank (round 2, critic: it was near-white).
BOTTOM = "ggpggggggg"

# Fin outlines, as text: one character per pixel, by absolute z (column) and y (row); '.' is clear.
# the dorsal fin, rows y 19..20, columns z 0..2: a lit leading edge, sloping back to the body
DORSAL_Z0, DORSAL_Y0 = 0, 19
DORSAL = [
    "F..",
    "fFf",
]
# the forked tail, rows y 20..23, columns z 5..7 (z 5 against the stalk): a lit upper lobe, a shaded lower lobe, an
# open notch between them
CAUDAL_Z0, CAUDAL_Y0 = 5, 20
CAUDAL = [
    ".TT",
    "uT.",
    "ut.",
    ".tt",
]


def side_colour(y, z):
    yi, zi = int(math.floor(y)), int(math.floor(z))
    return PAL[SIDE[yi][zi - SIDE_Z0]]


def body_colour(name, face, x, y, z, x0, y0, z0, w, h, d):
    """The colour of one texel of a body section, from where it sits on the fish. Faces that end up inside the fish
    get the colour of the body around them, so no stray colour hides anywhere in the texture."""
    zi = int(math.floor(z))
    col = zi - SIDE_Z0
    if face == "top":
        return PAL[TOP[col]]
    if face == "bottom":
        return PAL[BOTTOM[col]]
    if face in ("west", "east"):
        if name == "stalk":
            return PAL["s"]
        return side_colour(y, z)
    # the ends of each section (north = toward the head, south = toward the tail): the row's colour beside them
    row = int(math.floor(y))
    if name == "stalk":
        return PAL["s"]
    if face == "north":
        if name in ("tip", "snout"):
            return PAL["m"]                       # the point of the snout
        if name == "chin":
            return PAL["J"]                       # the front of the lower jaw
        if name == "head" and row == 22:
            return PAL["J"]                       # the jaw's corners beside the chin
        c = SIDE[row][int(math.floor(z0)) - SIDE_Z0]
        return PAL["m" if c in "E." else c]
    # south: the back end of a section, the colour of its last side column (never the eye's)
    last = z0 + d - 1
    c = SIDE[row][int(math.floor(last)) - SIDE_Z0]
    if c == "E":
        c = "m"
    return PAL[c]


def fin_colour(name, x, y, z):
    """The colour of one fin texel, or CLEAR outside the fin's outline."""
    zi, yi = int(math.floor(z)), int(math.floor(y))
    if name == "dorsal":
        return PAL[DORSAL[yi - DORSAL_Y0][zi - DORSAL_Z0]]
    if name == "caudal":
        return PAL[CAUDAL[yi - CAUDAL_Y0][zi - CAUDAL_Z0]]
    if name in ("pelvic", "anal"):
        return PAL["a"]
    # the pectoral fins: a little lighter at the root, shaded behind
    return PAL["f"] if zi < 0 else PAL["a"]


def draw_texture():
    img = Image.new("RGBA", (TW, TH), CLEAR)
    owner = {}
    for cube in CUBES:
        name, _, _, (x0, y0, z0), (w, h, d) = cube
        for face, u, v, x, y, z in sard.face_texels(cube):
            assert 0 <= u < TW and 0 <= v < TH, (name, face, u, v)
            assert owner.setdefault((u, v), name) == name, ("texture overlap", name, owner[(u, v)], u, v)
            if w == 0 or h == 0:
                c = fin_colour(name, x, y, z)
            else:
                c = body_colour(name, face, x, y, z, x0, y0, z0, w, h, d)
            img.putpixel((u, v), c)
    return img


# --- the Java model ---------------------------------------------------------------------------------------------------
def write_java():
    f = sard.f
    lines = []
    for part in ("body", "tail_fin", "right_fin", "left_fin"):
        parent, (px, py, pz), zrot = PARTS[part]
        builder = "CubeListBuilder.create()"
        for cube in [c for c in CUBES if c[1] == part]:
            name, _, _, (x0, y0, z0), (w, h, d) = cube
            u, v = sard.tex_offset(cube)
            builder += "\n            /* %s */ .texOffs(%d, %d).addBox(%s, %s, %s, %d.0F, %d.0F, %d.0F)" % (
                name, u, v, f(x0 - px), f(y0 - py), f(z0 - pz), w, h, d)
        if zrot:
            pose = "PartPose.offsetAndRotation(%s, %s, %s, 0.0F, 0.0F, %s)" % (f(px), f(py), f(pz), f(zrot))
        else:
            pose = "PartPose.offset(%s, %s, %s)" % (f(px), f(py), f(pz))
        lines.append("        root.addOrReplaceChild(\"%s\", %s,\n            %s);" % (part, builder, pose))
    body = "\n".join(lines)
    src = """package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The incova (anchovy): a slim, round cigar with a long pointed snout overhanging an underslung mouth that reaches
 * back past the big, forward-set eye, a green back over a bright silver band, no spots, a small dorsal fin mid-back
 * and a forked tail that sways as it swims. 13 px long, 2 px deep and wide, head toward -z, the ground at y 24.
 * Made by art/src/fish_incova_model.py (don't edit by hand). Texture: textures/entity/fish/incova.png (32 x 32).
 */
public class IncovaModel extends FishModel {
    public IncovaModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
%s
        return LayerDefinition.create(mesh, %d, %d);
    }
}
""" % (body, TW, TH)
    with open(JAVA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(src)


# --- previews and the compare sheet -----------------------------------------------------------------------------------
def on_bg(img, bg=(72, 72, 72, 255), pad=4):
    out = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), bg)
    out.alpha_composite(img, (pad, pad))
    return out


def previews(out_dir, texture):
    os.makedirs(out_dir, exist_ok=True)
    out = {}
    for view in ("side", "top", "three"):
        img = sard.render(CUBES, PARTS, texture, view, 16)
        img.save(os.path.join(out_dir, "incova_%s16.png" % view))
        out[view] = img
    sar_tex = Image.open(sard.TEXTURE).convert("RGBA")
    cod = sard.vanilla_texture("cod")
    row = [sard.render(CUBES, PARTS, texture, "side", 12), sard.render(sard.CUBES, sard.PARTS, sar_tex, "side", 12)]
    top = [sard.render(CUBES, PARTS, texture, "top", 12), sard.render(sard.CUBES, sard.PARTS, sar_tex, "top", 12)]
    three = [sard.render(CUBES, PARTS, texture, "three", 12),
             sard.render(sard.CUBES, sard.PARTS, sar_tex, "three", 12)]
    if cod:
        cc = sard.vanilla_cubes(sard.COD_CUBES)
        row.append(sard.render(cc, sard.COD_PARTS, cod, "side", 12))
        top.append(sard.render(cc, sard.COD_PARTS, cod, "top", 12))
        three.append(sard.render(cc, sard.COD_PARTS, cod, "three", 12))
    out["scale"], out["scale_top"], out["scale_three"] = row, top, three
    return out


def sheet(shots_dir, texture, prev_dir):
    from PIL import ImageFont
    pv = previews(prev_dir, texture)
    try:
        sys.path.insert(0, os.path.join(ROOT, "art", "tools"))
        from font import label_font
        font = label_font(15)
    except Exception:  # noqa: BLE001
        font = ImageFont.load_default()
    W = 1800
    blocks = []

    def title(t):
        im = Image.new("RGBA", (W, 28), (40, 40, 40, 255))
        ImageDraw.Draw(im).text((8, 5), t, fill=(240, 240, 240, 255), font=font)
        blocks.append(im)

    def row(images, h=None, gap=14, align_bottom=False, bg=(72, 72, 72, 255)):
        if h:
            images = [i.resize((max(1, int(i.width * h / i.height)), h), Image.LANCZOS) for i in images]
        hh = max(i.height for i in images)
        im = Image.new("RGBA", (W, hh + 8), bg)
        x = 8
        for i in images:
            if x + i.width > W:
                break
            im.alpha_composite(i, (x, 4 + (hh - i.height if align_bottom else (hh - i.height) // 2)))
            x += i.width + gap
        blocks.append(im)

    ref_dir = os.path.join(ROOT, "art", "references", "fish_incova_refonly")
    refs = [Image.open(os.path.join(ref_dir, n)).convert("RGBA")
            for n in ("gervais.jpg", "side.jpg", "portugal.jpg", "ifremer1.jpg", "lonja.jpg")
            if os.path.exists(os.path.join(ref_dir, n))]
    if refs:
        title("References (reference only): Gervais plate, side view, fresh catch on a beach, fresh at market (x2)")
        row(refs[:2], h=220)
        row(refs[2:], h=220)

    items = os.path.join(RES, "textures", "item")
    acc = []
    for n in ("incova", "incova_spawn_egg"):
        p = os.path.join(items, n + ".png")
        if os.path.exists(p):
            acc.append(Image.open(p).convert("RGBA"))
    cod_bucket = os.path.join(ROOT, "art", ".vanilla", "item", "cod_bucket.png")
    bp = os.path.join(items, "incova_bucket.png")
    if os.path.exists(bp):
        b = Image.open(bp).convert("RGBA")
        if os.path.exists(cod_bucket):
            base = Image.open(cod_bucket).convert("RGBA")
            base.alpha_composite(b)
            b = base
        acc.insert(1, b)
    title("Accepted pieces (icon, bucket, spawn egg) at 8x, beside the model's side view and its texture at 8x")
    row([on_bg(a.resize((128, 128), Image.NEAREST), (139, 139, 139, 255)) for a in acc]
        + [on_bg(pv["side"]), on_bg(texture.resize((TW * 8, TH * 8), Image.NEAREST), (139, 139, 139, 255))])

    title("Offline model, 16x: side, three-quarter, top (vanilla face shading only)")
    row([on_bg(pv["side"]), on_bg(pv["three"]), on_bg(pv["top"])])
    title("Same scale, 12x: incova (hitbox 0.35 x 0.2), the accepted sardina (0.4 x 0.25), vanilla cod (0.5 x 0.3)")
    row([on_bg(i) for i in pv["scale"]], align_bottom=True, gap=50)
    row([on_bg(i) for i in pv["scale_three"]], align_bottom=True, gap=50)
    row([on_bg(i) for i in pv["scale_top"]], gap=50)
    sar_tex = Image.open(sard.TEXTURE).convert("RGBA")
    title("Texture at 8x and 1x: incova and sardina (32 x 32)")
    row([on_bg(texture.resize((TW * 8, TH * 8), Image.NEAREST), (139, 139, 139, 255)), on_bg(texture, (139, 139, 139, 255)),
         on_bg(sar_tex.resize((TW * 8, TH * 8), Image.NEAREST), (139, 139, 139, 255)), on_bg(sar_tex, (139, 139, 139, 255))])

    if shots_dir and os.path.isdir(shots_dir):
        def shot(n):
            found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None

        names = ("fish-incova-side", "fish-incova-three-quarter", "fish-incova-top", "fish-incova-on-land",
                 "fish-incova-beside-cod")
        present = [(n, shot(n)) for n in names]
        present = [(n, i) for n, i in present if i]
        if present:
            title("In the game: the incova alone (side close-up, three-quarter, top), on land, and beside vanilla cod")
            row([i for _, i in present[:3]], h=330)
            row([i for _, i in present[3:]], h=330)
            title("The same, cropped to the fish (beside cod: incova left, cod right)")
            boxes = {"fish-incova-beside-cod": (0.06, 0.25, 0.94, 0.6)}
            crops = []
            for n, i in present:
                fx = boxes.get(n, (0.3, 0.25, 0.7, 0.6))
                box = (int(i.width * fx[0]), int(i.height * fx[1]), int(i.width * fx[2]), int(i.height * fx[3]))
                k = 580.0 / (box[2] - box[0])
                crops.append(i.crop(box).resize((580, int((box[3] - box[1]) * k)), Image.NEAREST))
            row(crops[:3])
            row(crops[3:])
        sar = [shot(n) for n in ("fish-sardina-side", "fish-sardina-beside-cod")]
        sar = [s for s in sar if s]
        if sar and present:
            title("In the game, same camera distance: incova side (left) and the accepted sardina side (right)")
            inc = dict(present).get("fish-incova-side")
            if inc:
                fx = (0.3, 0.25, 0.7, 0.6)
                pair = []
                for i in (inc, sar[0]):
                    box = (int(i.width * fx[0]), int(i.height * fx[1]), int(i.width * fx[2]), int(i.height * fx[3]))
                    k = 580.0 / (box[2] - box[0])
                    pair.append(i.crop(box).resize((580, int((box[3] - box[1]) * k)), Image.NEAREST))
                row(pair)

    # round 1 (critic: FIX, the back too green and the belly too white), kept beside the new version
    old_dir = os.path.join(ROOT, "art", "candidates", "fish_incova_model_round1")
    old_tex = os.path.join(old_dir, "incova.png")
    if os.path.exists(old_tex):
        old = Image.open(old_tex).convert("RGBA")
        title("Round 1 (left of each pair) and round 2 (right): offline side and three-quarter at 12x, textures at 8x")
        row([on_bg(sard.render(CUBES, PARTS, old, "side", 12)), on_bg(sard.render(CUBES, PARTS, texture, "side", 12)),
             on_bg(sard.render(CUBES, PARTS, old, "three", 12)), on_bg(sard.render(CUBES, PARTS, texture, "three", 12))],
            gap=30)
        row([on_bg(old.resize((TW * 8, TH * 8), Image.NEAREST), (139, 139, 139, 255)),
             on_bg(texture.resize((TW * 8, TH * 8), Image.NEAREST), (139, 139, 139, 255))], gap=30)
        if shots_dir and os.path.isdir(shots_dir):
            boxes = {"fish-incova-side": (0.3, 0.25, 0.7, 0.6), "fish-incova-beside-cod": (0.06, 0.25, 0.94, 0.6),
                     "fish-incova-on-land": (0.42, 0.42, 0.66, 0.6)}
            for n, fx in boxes.items():
                pair = []
                for d in (old_dir, shots_dir):
                    found = sorted(glob.glob(os.path.join(d, "*" + n + ".png")))
                    if found:
                        i = Image.open(found[-1]).convert("RGBA")
                        box = (int(i.width * fx[0]), int(i.height * fx[1]), int(i.width * fx[2]), int(i.height * fx[3]))
                        k = 860.0 / (box[2] - box[0])
                        pair.append(i.crop(box).resize((860, int((box[3] - box[1]) * k)), Image.NEAREST))
                if len(pair) == 2:
                    title("In the game, %s: round 1 (left), round 2 (right)" % n[len("fish-incova-"):].replace("-", " "))
                    row(pair)
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    dest = os.path.join(ROOT, "art", "candidates", "fish_incova_model.png")
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
        sheet(args[args.index("--sheet") + 1], texture, prev or os.path.join(ROOT, "art", "candidates", "tmp_incova"))
    elif prev:
        previews(prev, texture)
        print("previews in", prev)


if __name__ == "__main__":
    main()
