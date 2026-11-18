"""The tird (ornate wrasse, Thalassoma pavo, the green-and-blue male) as a swimming mob: its 3D model and its texture.

Night job piece 1 of 3 (docs/Decisions/2026-11-18 Night job - the rest of the fish, Claude decides.md). Drawn from the
photos in art/references/fish_tird_refonly/ (list.tsv; two of them taken in Malta, at Ċirkewwa and in Gozo). What makes
it a tird:
  - small and slim: a long, low body, 3 px deep, 2 px wide, a short pointed snout with a small mouth;
  - the male's colours (the "peacock" phase, the one with the clearest read at small size): a turquoise-blue head with
    pink-violet lines, then just behind the head a bright turquoise bar and a broad red-orange band over the pectoral,
    then a green body with thin red lines running down it;
  - countershaded: a darker green back, a pale yellow-green belly;
  - a lunate (crescent) tail whose two tips run out long, blue with dark tips;
  - one long low dorsal fin along the back.
The female (green with red-orange bars and a dark spot on the back) is candidate C; it was not chosen because its dark
spot sits close to the eye's look at this size (owner rule: eyes must look different from every other mark).
Every colour is a step lighter than the photos, because the game greys and darkens everything under water.

Size: 13 px long (9 of body from the snout tip, 4 of tail), 3 px deep, 2 px wide: about 0.75 blocks, smaller and
slimmer than vanilla cod. One texture pixel per model pixel, like vanilla's fish.

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, a root
child "body", "top_fin" (the long dorsal fin) and a "tail_fin" that sways like vanilla cod's.

Candidates (the same model): A the male, turquoise head, red-orange shoulder band, green body; B the same with a bluer
head and a deeper red band; C the female phase (green with red-orange bars, a dark spot on the back). CHOSEN is installed.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/TirdModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/tird.png    (32 x 32)
  art/candidates/tird_model/  (candidate textures and offline previews)
With --sheet SCREENSHOT_DIR also writes the review sheet art/candidates/fish_tird_model.png.

Run:  art/.venv/bin/python art/src/fish_tird_model.py [--sheet SCREENSHOT_DIR]
"""
import glob
import math
import os
import sys
import zipfile

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fish_sardina_model as sard  # noqa: E402  (the shared box-UV layout, the offline renderer, vanilla cod geometry)

ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "fish",
                    "TirdModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "tird.png")
CAND = os.path.join(ROOT, "art", "candidates", "tird_model")
TW, TH = 32, 32
CHOSEN = "A"
VANILLA_JAR = "/home/cultar/Apps/Minecraft World/tools/gradle-home/caches/fabric-loom/26.3/minecraft-merged.jar"


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


# Palettes. Keys:
#   H head turquoise-blue, h head top (darker), S snout, c cheek (paler turquoise), E eye, L pink-violet head line
#   B the bright turquoise bar behind the head, b its belly end, R the red-orange shoulder band, o its belly end
#   m back green, k a red line on the back, g flank green, r a red line on the flank, w pale belly, X the female's spot
#   F dorsal fin, A anal fin, u tail base, T tail lobe, d dark tail tip, P pectoral fin
PALETTES = {
    # round 1 (maker, first in-game look): the water turned the greens teal and the band maroon, so the greens are
    # yellower and lighter, the band a brighter orange and the bar a lighter turquoise.
    # Model critic round 1 (PASS, with polish): the flank green a brighter yellow-green (k, g, u), the red lines lighter
    # and pinker (r) and the back's line a light tan (k), so the eye stays the only dark pixel; a clean cream belly (w);
    # the pectorals pale green (P).
    # Model critic round 2 (PASS, with fixes): the eye a row lower, inside the head, the only near-black mark; the tail
    # tips a mid blue-grey (d); the red lines a more saturated red-orange (r); the bar near cyan-white (B) and the band
    # warmer (R), so the collar survives the water's tint
    "A": {
        "H": "#4aa6c0", "h": "#3b8aa4", "S": "#5ab0c6", "c": "#7cc6cf", "E": "#0b0d10", "L": "#cc84aa",
        "B": "#b0fcf0", "b": "#c4f8ee", "R": "#ff6a2a", "o": "#f4a874",
        "m": "#56a046", "k": "#c48a5c", "g": "#96d850", "r": "#f06a3c", "w": "#e4f0c4", "X": "#56a046",
        "F": "#56a696", "A": "#76c8c4", "u": "#8ccc50", "T": "#62c4cc", "d": "#4c7c9c", "P": "#9cc890",
    },
    "B": {
        "H": "#3f8ed0", "h": "#3274ac", "S": "#4f9ed4", "c": "#76b8dc", "E": "#0b0d10", "L": "#c876a8",
        "B": "#6ad6dc", "b": "#94e0e0", "R": "#d0502e", "o": "#e0885a",
        "m": "#3a8248", "k": "#86603a", "g": "#5aa84c", "r": "#be5e3a", "w": "#c8dc98", "X": "#3a8248",
        "F": "#4690a0", "A": "#62b0cc", "u": "#529e50", "T": "#58aed4", "d": "#2a4c78", "P": "#56889c",
    },
    "C": {
        "H": "#58a8b4", "h": "#4a8f96", "S": "#62b0b8", "c": "#86c8c4", "E": "#0b0d10", "L": "#c07c90",
        "B": "#7cd8cc", "b": "#a0e0d0", "R": "#d8743e", "o": "#e4a070",
        "m": "#5a9248", "k": "#a06a3a", "g": "#7cb852", "r": "#d4743e", "w": "#d6e2a2", "X": "#2a3a2c",
        "F": "#5e9a7c", "A": "#7cbcac", "u": "#72aa52", "T": "#74bcb0", "d": "#3c6a6a", "P": "#6a9a8c",
    },
}
CLEAR = (0, 0, 0, 0)

# --- the model -------------------------------------------------------------------------------------------------------
# Parts: name -> (parent, pivot (absolute model pixels), zRot). Cubes: (name, part, (U, V) top-left of the used texture
# area, (x0, y0, z0) absolute, (w, h, d)). Absolute: x across, y down (24 = ground), z head (-) to tail (+).
PARTS = {
    "body": (None, (0.0, 21.5, 0.0), 0.0),
    "top_fin": (None, (0.0, 20.0, -3.0), 0.0),
    "tail_fin": (None, (0.0, 21.0, 3.0), 0.0),
    # the small pectoral fins, hinged on the flanks just behind the shoulder band, angled down and out
    "right_fin": (None, (-1.0, 21.5, -2.0), -0.9),
    "left_fin": (None, (1.0, 21.5, -2.0), 0.9),
}
CUBES = [
    # the short pointed snout, the head, the trunk, the belly under its front half (so the rear tapers from below) and
    # the thin stalk (the back line runs on straight)
    ("snout", "body", (22, 0), (-0.5, 21.0, -6.0), (1, 1, 1)),
    ("head", "body", (0, 0), (-1.0, 20.0, -5.0), (2, 3, 2)),
    ("trunk", "body", (0, 6), (-1.0, 20.0, -3.0), (2, 2, 5)),
    ("belly", "body", (8, 0), (-1.0, 22.0, -3.0), (2, 1, 3)),
    ("stalk", "body", (22, 3), (-0.5, 20.0, 2.0), (1, 2, 1)),
    # the long low dorsal fin (its own part, as the contract names it) and the anal fin under the rear
    ("dorsal", "top_fin", (0, 15), (0.0, 19.0, -3.0), (0, 1, 5)),
    ("anal", "body", (0, 17), (0.0, 22.0, 0.0), (0, 1, 2)),
    # the lunate tail
    ("caudal", "tail_fin", (16, 15), (0.0, 18.5, 3.0), (0, 5, 4)),
    # the pectoral fins
    ("pec_r", "right_fin", (0, 20), (-2.0, 21.5, -2.0), (1, 0, 1)),
    ("pec_l", "left_fin", (2, 20), (1.0, 21.5, -2.0), (1, 0, 1)),
]

# The side of the fish, rows y 20..22, columns z -6..2. '.' where no section reaches.
# Row 20 (the back): the darker head top (round 2: the eye moved down out of it), the turquoise bar, the red-orange band,
#         then the green back with one dulled red line.
# Row 21: the snout, the eye with head colour all round it, the head, the bar and the band, then the flank green with a red line
#         (round 1, critic: one pixel, stepping up to the back's tan pixel behind it, a broken line, not a band).
# Row 22 (the belly, under the head and the front half only): the pale cheek under the eye, the pink-violet head line
#         a pixel behind it (never in the eye's row), the bar's pale end and a clean cream
#         belly (round 1, critic: the pink and salmon there looked dirty).
SIDE_Z0 = -6
SIDES = {
    "A": {
        20: ".hhBRmmkm",
        21: "SEHBRgrgg",
        22: ".cLbww...",
    },
    # the female: no shoulder band, red-orange bars down the green body, one dark spot on the back well behind the head
    "C": {
        20: ".EhmkmXkm",
        21: "SHLgrgrgg",
        22: ".cLwow...",
    },
}
SIDES["B"] = SIDES["A"]
# The back seen from above: two rows (x -1..0 and 0..1), columns z -6..2.
TOPS = {"A": ["ShhBRmmkm", "ShhBRmmkm"], "B": ["ShhBRmmkm", "ShhBRmmkm"], "C": ["ShhmkmXkm", "ShhmkmXkm"]}
# The belly seen from below.
BOTTOM = {"A": "Sccbwwwww", "B": "Sccbwwwww", "C": "ScLwowoww"}

# Fin outlines: one character per pixel, rows by absolute y, columns by absolute z.
DORSAL_Z0 = -3
DORSAL = "FFFFF"
ANAL_Z0 = 0
ANAL = "AA"
# the lunate tail: a 2 px base on the stalk, then the crescent's two long tips, each pixel sharing an edge with the
# next so it stays one shape from every angle; the tips are a darker blue
# (round 1, critic: the tips too long and stiff, like a bracket): 5 rows, the tips a pixel shorter and swept a pixel
# further back, the middle green like the body
CAUDAL_Z0, CAUDAL_Y0 = 3, 18.5
CAUDAL = [
    "..dd",
    ".uT.",
    "uu..",
    ".uT.",
    "..dd",
]


def pal(variant):
    return {k: hexc(v) for k, v in PALETTES[variant].items()}


def body_colour(variant, P, name, face, x, y, z, x0, y0, z0, w, h, d):
    """The colour of one texel of a body section, from where it sits on the fish."""
    side = SIDES[variant]
    zi, yi = int(math.floor(z)), int(math.floor(y))
    col = zi - SIDE_Z0
    if face == "top":
        rows = TOPS[variant]
        xi = 0 if x < 0 else 1
        return P[rows[xi][col]]
    if face == "bottom":
        return P[BOTTOM[variant][col]]
    if face in ("west", "east"):
        ch = side[yi][col]
        return P["c" if ch == "." else ch]
    if face == "north":
        if name == "snout":
            return P["S"]
        # the front of each section round the one in front of it: the side colour of its first column, never the eye's
        ch = side[yi][int(math.floor(z0)) - SIDE_Z0]
        return P[{"E": "h", ".": "H"}.get(ch, ch)]
    # south: the back end of a section, the colour of its last side column
    ch = side[yi][int(math.floor(z0 + d - 1)) - SIDE_Z0]
    return P[{"E": "h", ".": "g"}.get(ch, ch)]


def fin_colour(P, name, x, y, z):
    zi, yi = int(math.floor(z)), int(math.floor(y))
    if name == "dorsal":
        ch = DORSAL[zi - DORSAL_Z0]
    elif name == "anal":
        ch = ANAL[zi - ANAL_Z0]
    elif name == "caudal":
        ch = CAUDAL[int(math.floor(y - CAUDAL_Y0))][zi - CAUDAL_Z0]
    else:
        ch = "P"
    return CLEAR if ch == "." else P[ch]


def draw_texture(variant):
    P = pal(variant)
    img = Image.new("RGBA", (TW, TH), CLEAR)
    owner = {}
    for cube in CUBES:
        name, _, _, (x0, y0, z0), (w, h, d) = cube
        for face, u, v, x, y, z in sard.face_texels(cube):
            assert 0 <= u < TW and 0 <= v < TH, (name, face, u, v)
            assert owner.setdefault((u, v), name) == name, ("texture overlap", name, owner[(u, v)], u, v)
            if w == 0 or h == 0:
                c = fin_colour(P, name, x, y, z)
            else:
                c = body_colour(variant, P, name, face, x, y, z, x0, y0, z0, w, h, d)
            img.putpixel((u, v), c)
    return img


# --- the Java model ---------------------------------------------------------------------------------------------------
def write_java():
    f = sard.f
    lines = []
    for part in ("body", "top_fin", "tail_fin", "right_fin", "left_fin"):
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
 * The tird (ornate wrasse, the male): small and slim, a turquoise-blue head with pink-violet lines, a bright turquoise
 * bar and a red-orange band behind the head, a green body with thin red lines and a pale belly, a long low dorsal fin
 * and a lunate tail with dark-tipped points that sways as it swims. 13 px long, 3 px deep, 2 px wide, head toward
 * -z, the ground at y 24.
 * Made by art/src/fish_tird_model.py (don't edit by hand). Texture: textures/entity/fish/tird.png (32 x 32).
 */
public class TirdModel extends FishModel {
    public TirdModel(ModelPart root) {
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


# --- previews and the review sheet ------------------------------------------------------------------------------------
def vanilla_png(path):
    try:
        with zipfile.ZipFile(VANILLA_JAR) as z, z.open(path) as fh:
            return Image.open(fh).convert("RGBA").copy()
    except (OSError, KeyError):
        return None


def on_bg(img, bg=(72, 72, 72, 255), pad=4):
    out = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), bg)
    out.alpha_composite(img, (pad, pad))
    return out


def hstack(images, gap=20, bg=(72, 72, 72, 255), bottom=True):
    H = max(i.height for i in images)
    out = Image.new("RGBA", (sum(i.width for i in images) + gap * (len(images) - 1), H), bg)
    x = 0
    for i in images:
        out.alpha_composite(i, (x, H - i.height if bottom else (H - i.height) // 2))
        x += i.width + gap
    return out


def write_candidates():
    os.makedirs(CAND, exist_ok=True)
    cod = vanilla_png("assets/minecraft/textures/entity/fish/cod.png")
    for v in PALETTES:
        tex = draw_texture(v)
        tex.save(os.path.join(CAND, "texture_%s.png" % v))
        views = [on_bg(sard.render(CUBES, PARTS, tex, view, 16)) for view in ("side", "three", "top")]
        hstack(views, bottom=False).save(os.path.join(CAND, "preview_%s.png" % v))
    if cod:
        cc = sard.vanilla_cubes(sard.COD_CUBES)
        row = [on_bg(sard.render(CUBES, PARTS, draw_texture(CHOSEN), "side", 12)),
               on_bg(sard.render(cc, sard.COD_PARTS, cod, "side", 12))]
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
    if os.path.exists(os.path.join(CAND, "scale_vs_cod.png")):
        title("Same scale offline, 12x: tird, vanilla cod")
        row([Image.open(os.path.join(CAND, "scale_vs_cod.png")).convert("RGBA")])
    if shots_dir and os.path.isdir(shots_dir):
        def shot(n):
            found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None
        names = ["fish-tird-side", "fish-tird-three-quarter", "fish-tird-top", "fish-tird-beside-cod",
                 "fish-tird-on-land", "fish-tird-lineup"]
        present = [(n, shot(n)) for n in names]
        present = [(n, i) for n, i in present if i]
        if present:
            title("In the game: side, three-quarter, top; beside vanilla cod, on land, lineup (tird, cod, cerna, small tonn)")
            row([i for _, i in present[:3]], h=330)
            row([i for _, i in present[3:]], h=330)
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    dest = os.path.join(ROOT, "art", "candidates", "fish_tird_model.png")
    out.convert("RGB").save(dest)
    print("sheet:", dest)


def main():
    texture = draw_texture(CHOSEN)
    os.makedirs(os.path.dirname(TEXTURE), exist_ok=True)
    texture.save(TEXTURE)
    write_java()
    write_candidates()
    print("wrote", os.path.relpath(TEXTURE, ROOT), "and", os.path.relpath(JAVA, ROOT), "candidates in",
          os.path.relpath(CAND, ROOT))
    args = sys.argv[1:]
    if "--sheet" in args:
        sheet(args[args.index("--sheet") + 1])


if __name__ == "__main__":
    main()
