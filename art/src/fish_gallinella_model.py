"""The gallinella (tub gurnard, Chelidonichthys lucerna) as a swimming mob: its 3D model and its texture.

Night job piece 1 of 3 (docs/Decisions/2026-11-18 Night job - the rest of the fish, Claude decides.md). Drawn from the
photos in art/references/fish_gallinella_refonly/ (list.tsv; market and fresh-caught fish for colour, the views from
above for the wings). What makes it a gurnard:
  - a big, bony, boxy head, as broad as it is deep, with a steep forehead stepping down to a low snout and the eye
    high on the head;
  - a red-orange body that tapers back from the head to a slim stalk: a darker red back with red-brown mottling, an
    orange-pink flank and a pale belly (countershaded);
  - huge fan-like pectoral fins ("wings") spread out sideways from just behind the head: blue-green with darker rays,
    a bright blue rim and a dark navy patch near the base (the tub gurnard's best-known mark);
  - two dorsal fins (a spiny one behind the head, a long low one to the tail), a long low anal fin, a squared tail.
  - The three free finger rays it walks on are left out: at this size they read as legs (night log).
Every colour is a step lighter than the photos, because the game greys and darkens everything under water.

Size: 18 px long (15 of body from the snout tip, 3 of tail), 4 px deep and 4 px wide at the head, 15 px across the
spread wings: 1.13 blocks. One texture pixel per model pixel. Model critic rounds: 5 (PASS in round 5).

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, root
children "body", "top_fin" (the spiny first dorsal), "left_fin" / "right_fin" (the wings) and "tail_fin" (sways).

Candidates (the same model, three paint jobs): A red-orange as the market fish; B a paler pinkish tan with brown spots
as the fish on the boat deck; C A with greener wings. CHOSEN is installed.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/GallinellaModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/gallinella.png    (64 x 64)
  art/candidates/gallinella_model/  (candidate textures and offline previews)
With --sheet SCREENSHOT_DIR also writes the review sheet art/candidates/fish_gallinella_model.png.

Run:  art/.venv/bin/python art/src/fish_gallinella_model.py [--sheet SCREENSHOT_DIR]
"""
import glob
import math
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import fish_cerna_model as CE  # noqa: E402  (the shared texel layout and the offline renderer)

RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "fish",
                    "GallinellaModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "gallinella.png")
CAND = os.path.join(ROOT, "art", "candidates", "gallinella_model")
TW, TH = 64, 64
CHOSEN = "A"


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


# Body ramp 0 (pale belly) .. 5 (darkest back), then the features. Keys:
#   E eye, e the pale skin ring round it, M mouth line, B mottling on the back (red-brown, 2 px patches)
#   wings: r root (body colour), F membrane, f darker ray, D dark patch, d blue in the patch, R rim blue, L rim light
#   fins: Q fin lit, q fin shade, T tail lit, t tail shade
PALETTES = {
    "A": {
        # round 1 critic: under water the red read dull mauve (the water's blue on red); round 2: pushed further to
        # a bright yellow-orange, so the blue tint lands on orange-red, as the fish looks in the sea
        # a red-orange back, a salmon upper flank and a warm cream-pink belly with a hard split along the mid-flank
        # (round 2 critic), so the pale belly still shows through the water's blue
        "0": "#fff0e0", "1": "#fcd8b8", "2": "#fab27e", "3": "#f49058", "4": "#e8703e", "5": "#d85a34",
        "E": "#0b0908", "e": "#e8703e", "M": "#d85a34", "B": "#cc5232", "a": "#fcc8a0",
        "r": "#f49058", "F": "#58b4aa", "G": "#88d6c6", "f": "#5cb2aa", "D": "#4a78c0", "d": "#6a98d8",
        "R": "#4cb0ff", "L": "#94dcff",
        "Q": "#ec7844", "q": "#e06c3c", "T": "#f8925c", "t": "#f08450",
    },
    "B": {
        "0": "#f6e8dc", "1": "#f2c8ae", "2": "#e6a682", "3": "#d4886a", "4": "#bc6c54", "5": "#9c5442",
        "E": "#0b0908", "e": "#f2d2bc", "M": "#a85440", "B": "#8c4636", "a": "#f6d4bc",
        "r": "#e0a080", "F": "#74b4a8", "G": "#98d4c4", "f": "#58968e", "D": "#2a3c6c", "d": "#4a6cae", "R": "#3e94e6",
        "L": "#78c0f4",
        "Q": "#e4a080", "q": "#c88264", "T": "#e08e6c", "t": "#c47054",
    },
    "C": {
        "0": "#f8e6da", "1": "#f6bca2", "2": "#ee9470", "3": "#e07052", "4": "#c8543e", "5": "#a8402f",
        "E": "#0b0908", "e": "#f4c8b0", "M": "#b04838", "B": "#9a3c2c", "a": "#f6d4bc",
        "r": "#e8866a", "F": "#7cba8a", "G": "#a8dcb0", "f": "#5c9a70", "D": "#2a3c6c", "d": "#4a6cae", "R": "#3e94e6",
        "L": "#78c0f4",
        "Q": "#ec8a68", "q": "#d06a4e", "T": "#f49a78", "t": "#e07c5c",
    },
}
CLEAR = (0, 0, 0, 0)

# --- the model -------------------------------------------------------------------------------------------------------
# Parts: name -> (parent, pivot (absolute model pixels), (xRot, yRot, zRot)). Cubes: (name, part, (x0, y0, z0)
# absolute, (w, h, d)); the UVs are packed by pack(). Absolute: x across, y down (24 = ground), z head (-) to tail (+).
WING_TILT = 0.4   # round 3 critic: angled down and out about 23 degrees, so the fan shows from the side too; hinged
# high on the flank, so its tips stay level with the belly (never hanging below it, round 1) and both show from above
PARTS = {
    "body": (None, (0.0, 21.0, 0.0), (0.0, 0.0, 0.0)),
    "top_fin": (None, (0.0, 19.0, -3.0), (0.0, 0.0, 0.0)),
    "right_fin": (None, (-1.5, 20.5, -4.0), (0.0, 0.0, -WING_TILT)),
    "left_fin": (None, (1.5, 20.5, -4.0), (0.0, 0.0, WING_TILT)),
    "tail_fin": (None, (0.0, 21.5, 6.0), (0.0, 0.0, 0.0)),
}
SPECS = [
    # the head: the low snout, the forehead one step up, then the boxy bony head, as broad as it is deep
    ("snout", "body", (-1.5, 20.0, -9.0), (3, 2, 1)),
    ("head", "body", (-2.0, 18.0, -8.0), (4, 5, 4)),
    # the body, tapering in width and depth to the slim stalk: 4 x 5 at the head, 3 x 4, 2 x 3, 1 x 2 (round 1 critic:
    # the head is now clearly the tallest part, and the forehead slopes down in steps to the snout)
    ("trunk", "body", (-1.5, 19.0, -4.0), (3, 4, 4)),
    ("rear", "body", (-1.0, 20.0, 0.0), (2, 3, 4)),
    ("stalk", "body", (-0.5, 20.5, 4.0), (1, 2, 2)),
    # the long low second dorsal fin and the long low anal fin
    ("dorsal2", "body", (0.0, 19.0, 0.0), (0, 1, 4)),
    ("anal", "body", (0.0, 23.0, 0.0), (0, 1, 4)),
    # the spiny first dorsal, one low fin on the back behind the head (round 1 critic: two posts read as ears)
    ("dorsal1", "top_fin", (0.0, 18.0, -3.0), (0, 1, 4)),
    # the wings: flat fans hinged on the flank behind the head, spread out sideways
    ("wing_r", "right_fin", (-7.5, 20.5, -4.0), (6, 0, 7)),
    ("wing_l", "left_fin", (1.5, 20.5, -4.0), (6, 0, 7)),
    # the squared tail
    ("caudal", "tail_fin", (0.0, 19.0, 6.0), (0, 5, 3)),
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
    """Shelf-pack every cube's used texture area into the texture, biggest first."""
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
ROW_SHADE = {17: 4, 18: 4, 19: 4, 20: 4, 21: 2, 22: 0, 23: 0}   # round 3: the back's red runs on along
# the top of the slim stalk to the tail, so the tail never looks cut off in water
# The side of the fish: features by (y, z) texel
FEAT = {
    (19, -6): "E",                                  # the eye, high on the head, in plain head colour (round 1 critic:
}                                                   # pale skin beside it read as more marks in its row)
GILL = {(20, -4), (21, -4)}                         # the gill cover's edge, one shade darker


# A wing seen from above, rows z -4..2 (front to back), columns from the body out (0 = the root): a short root along
# the flank, the fan widening out and back to a rounded rim. Round 1 critic: calm bands (teal inside, a lighter
# blue-green middle, the bright blue rim on the outer edge only) and one compact dark navy patch. Round 5: the patch is an
# irregular mid-blue blotch (never navy, never as dark as the eye) with a paler blue fleck, at the inner rear of the fan
# by the body, as on the real fish: never a neat square in the middle of the fan, where it read as an eyespot.
WING = [
    "rFGR..",
    "rFGGR.",
    "rFGGGR",
    "rDGGGR",
    "rDDGGR",
    ".DdGR.",
    "..RR..",
]
# the spiny first dorsal, rows y 17..18, columns z -4..-1: tallest at the front, stepping down
# round 2 critic: every fin low, so the head stays the highest point. The spiny first dorsal, row y 18, columns z -3..0,
# level with the top of the head; the second dorsal a 1 px strip along the lower back (row y 19, z 0..3); the anal fin
# a 1 px pale strip (row y 23, z 0..3).
DORSAL1 = ["QqQq"]
DORSAL2 = ["qQqQ"]
ANAL = ["aaaa"]
# the tail, rows y 19..23, columns z 6..8: one orange, a shallow 1 px nick in the middle of the trailing edge (a
# 2 px notch read as a bracket)
CAUDAL = [
    "tTT",
    "tTT",
    "tT.",
    "tTT",
    "tTT",
]
FINS = {"dorsal1": DORSAL1, "dorsal2": DORSAL2, "anal": ANAL, "caudal": CAUDAL}


def ramp(pal, shade):
    return pal[str(max(0, min(5, shade)))]


def side_colour(pal, y, z, face):
    yi, zi = int(math.floor(y)), int(math.floor(z))
    ch = FEAT.get((yi, zi))
    if ch == "E" and face not in ("west", "east"):
        ch = "e"
    if ch:
        return pal[ch]
    shade = ROW_SHADE[yi]
    if (yi, zi) in GILL:
        shade += 1
    # red-brown mottling on the upper flank behind the head, in 2 px patches, well behind the eye (never in its row near it)
    if yi in (19, 20) and zi >= 0 and CE.hash01(5, yi, zi // 2) < 0.22:
        return pal["B"] if yi == 19 else ramp(pal, 4)
    return ramp(pal, shade)


def top_colour(pal, x, z):
    """The back from above, the view a swimmer sees most: a darker red back down the middle, lighter toward the
    flanks, red-brown mottling in 2 px patches behind the head; the bony head plain."""
    xi, zi = int(math.floor(x + 2)), int(math.floor(z))
    edge = x < -1.0 or x > 1.0
    shade = 4 if not edge else 3
    if zi >= 4:
        return ramp(pal, 3)          # the slim stalk's back: plain and lighter (round 2: it read as a brown rod)
    if zi >= -3 and CE.hash01(9, xi, zi // 2) < 0.28:
        return pal["B"]
    if zi <= -4 and xi in (0, 3):
        shade = 3
    return ramp(pal, shade)


def body_colour(pal, name, face, x, y, z, x0, y0, z0, w, h, d):
    if face == "top":
        return top_colour(pal, x, z)
    if face == "bottom":
        return ramp(pal, 0)
    if face == "north":
        if name == "snout":
            return ramp(pal, 3) if int(math.floor(y)) == 20 else ramp(pal, 2)
        return side_colour(pal, y, z0, face)
    if face == "south":
        return side_colour(pal, y, z0 + d - 1, face)
    return side_colour(pal, y, z, face)


def fin_colour(pal, name, cube, x, y, z):
    _, _, _, (x0, y0, z0), (w, h, d) = cube
    if name in ("wing_r", "wing_l"):
        r = int(math.floor(z - z0))
        c = int(math.floor(x - x0)) if name == "wing_l" else int(math.floor(x0 + w - x))
        ch = WING[r][c]
    else:
        grid = FINS[name]
        ch = grid[int(math.floor(y - y0))][int(math.floor(z - z0))]
    return CLEAR if ch == "." else pal[ch]


def draw_texture(variant):
    pal = {k: hexc(v) for k, v in PALETTES[variant].items()}
    img = Image.new("RGBA", (TW, TH), CLEAR)
    owner = {}
    for cube in CUBES:
        name, _, _, (x0, y0, z0), (w, h, d) = cube
        for face, u, v, x, y, z in CE.face_texels(cube):
            assert 0 <= u < TW and 0 <= v < TH, (name, face, u, v)
            assert owner.setdefault((u, v), name) == name, ("texture overlap", name, owner[(u, v)], u, v)
            if w == 0 or h == 0:
                col = fin_colour(pal, name, cube, x, y, z)
            else:
                col = body_colour(pal, name, face, x, y, z, x0, y0, z0, w, h, d)
            img.putpixel((u, v), col)
    return img


# --- the Java model ---------------------------------------------------------------------------------------------------
def write_java():
    f = CE.f
    lines = []
    for part in ("body", "top_fin", "right_fin", "left_fin", "tail_fin"):
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
 * The gallinella (tub gurnard): a big boxy bony head with a steep forehead and the eye high up, a red-orange body
 * tapering to a slim stalk, huge fan-like pectoral "wings" spread out sideways (blue-green, a bright blue rim, a dark
 * navy patch), a spiny first dorsal, long low second dorsal and anal fins, and a squared tail that sways.
 * 18 px long, 4 px deep, 15 px across the wings; head toward -z, the ground at y 24.
 * Made by art/src/fish_gallinella_model.py (don't edit by hand). Texture: textures/entity/fish/gallinella.png (64 x 64).
 */
public class GallinellaModel extends FishModel {
    public GallinellaModel(ModelPart root) {
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


# --- previews and the review sheet ------------------------------------------------------------------------------------
def on_bg(img, bg=(72, 72, 72, 255), pad=4):
    out = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), bg)
    out.alpha_composite(img, (pad, pad))
    return out


def hstack(images, gap=20, bg=(72, 72, 72, 255)):
    H = max(i.height for i in images)
    out = Image.new("RGBA", (sum(i.width for i in images) + gap * (len(images) - 1), H), bg)
    x = 0
    for i in images:
        out.alpha_composite(i, (x, H - i.height))
        x += i.width + gap
    return out


def write_candidates():
    os.makedirs(CAND, exist_ok=True)
    for v in PALETTES:
        tex = draw_texture(v)
        tex.save(os.path.join(CAND, "texture_%s.png" % v))
        views = [on_bg(CE.render(CUBES, PARTS, tex, view, 16)) for view in ("side", "three", "top")]
        hstack(views).save(os.path.join(CAND, "preview_%s.png" % v))
    cod = CE.vanilla_texture("cod")
    row = [on_bg(CE.render(CUBES, PARTS, draw_texture(CHOSEN), "side", 12))]
    if cod:
        row.append(on_bg(CE.render(CE.vanilla_cubes(CE.COD_CUBES), CE.COD_PARTS, cod, "side", 12)))
    hstack(row).save(os.path.join(CAND, "scale_vs_cod.png"))


def sheet(shots_dir):
    from PIL import ImageFont
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

    def row(images, h=None, gap=14):
        if h:
            images = [i.resize((max(1, int(i.width * h / i.height)), h), Image.LANCZOS) for i in images]
        hh = max(i.height for i in images)
        im = Image.new("RGBA", (W, hh + 8), (72, 72, 72, 255))
        x = 8
        for i in images:
            if x + i.width > W:
                break
            im.alpha_composite(i, (x, 4 + (hh - i.height) // 2))
            x += i.width + gap
        blocks.append(im)

    title("Candidates A, B, C (offline, 16x: side, three-quarter, top); chosen: " + CHOSEN)
    for v in PALETTES:
        row([Image.open(os.path.join(CAND, "preview_%s.png" % v)).convert("RGBA")])
    if shots_dir and os.path.isdir(shots_dir):
        def shot(n):
            found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None
        names = ["fish-gallinella-side", "fish-gallinella-three-quarter", "fish-gallinella-top",
                 "fish-gallinella-beside-cod", "fish-gallinella-on-land", "fish-gallinella-lineup"]
        present = [i for i in (shot(n) for n in names) if i]
        if present:
            title("In the game: side, three-quarter, top; beside vanilla cod, on land, lineup")
            row(present[:3], h=330)
            row(present[3:], h=330)
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    dest = os.path.join(ROOT, "art", "candidates", "fish_gallinella_model.png")
    out.convert("RGB").save(dest)
    print("sheet:", dest)


def main():
    texture = draw_texture(CHOSEN)
    os.makedirs(os.path.dirname(TEXTURE), exist_ok=True)
    texture.save(TEXTURE)
    write_java()
    write_candidates()
    print("wrote", os.path.relpath(TEXTURE, ROOT), "and", os.path.relpath(JAVA, ROOT))
    args = sys.argv[1:]
    if "--sheet" in args:
        sheet(args[args.index("--sheet") + 1])


if __name__ == "__main__":
    main()
