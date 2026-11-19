"""The hmar (grey triggerfish, Balistes capriscus) as a swimming mob: its 3D model and its texture.

Night job piece 1 of 3 (docs/Decisions/2026-11-18 Night job - the rest of the fish, Claude decides.md). Drawn from the
photos in art/references/fish_hmar_refonly/ (list.tsv; the FDA photos of fresh fish out of water for colour). What
makes it a hmar:
  - a deep, laterally flattened body, rhomboid from the side: the forehead slopes up in a long line from a small
    mouth at the snout's tip, the belly runs low and round, and the long soft fins top and bottom make the back
    corners of the diamond;
  - grey to olive-grey, darker on the back, pale cream-grey on the belly (countershaded), with faint darker saddles
    across the back;
  - an eye set high and far back on the head, the only dark mark there (no mouth line, so the eye and mouth can't
    read as a face: the lips are only a paler grey, as on the real fish);
  - the stout first dorsal spine (the "trigger") on its own, a gap, then the long soft dorsal fin, and a matching
    anal fin below, both far back;
  - a lyre-shaped tail with pointed tips above and below.
Every colour is a step lighter than the photos, because the game greys and darkens everything under water.

Size: 17 px long (14 of body from the lips, 3 of tail), 9 px deep at the trunk, 13 px from the trigger's tip to the anal
fin, 3 px thick at the trunk (2 at the head, rear and stalk, 1 at the lips): about 1 block long, a bit smaller than the
cerna and as long as a cod but twice as deep. One texture pixel per model pixel, like vanilla's fish.

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, a root
child "body", "top_fin" (the trigger) and a "tail_fin" that sways like vanilla cod's.

Candidates (the same model, three paint jobs): A olive-grey; B cooler blue-grey, as the aquarium photos; C warmer
brown-grey, as the FDA market photo. CHOSEN is installed.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/HmarModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/hmar.png    (64 x 32)
  art/candidates/hmar_model/  (candidate textures and offline previews)
With --sheet SCREENSHOT_DIR also writes the review sheet art/candidates/fish_hmar_model.png.

Run:  art/.venv/bin/python art/src/fish_hmar_model.py [--sheet SCREENSHOT_DIR]
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
                    "HmarModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "hmar.png")
CAND = os.path.join(ROOT, "art", "candidates", "hmar_model")
TW, TH = 64, 32
CHOSEN = "A"
VANILLA_JAR = "/home/cultar/Apps/Minecraft World/tools/gradle-home/caches/fabric-loom/26.3/minecraft-merged.jar"


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


# Palettes. Keys:
#   H head top, m back, k saddle, K saddle fading down the flank, g upper flank, s flank, w belly, c cheek,
#   l lips (paler, never dark), E eye
#   F fin lit, f fin shade, T the trigger spine, U tail centre, W belly's lowest row, j mouth, V tail edge
PALETTES = {
    "A": {  # olive-grey
        "H": "#6c6a56", "m": "#74725e", "k": "#686654", "K": "#6e6c59", "g": "#9b9881", "s": "#aeaa94",
        "w": "#e0dbc9", "W": "#ebe7d8", "c": "#aaa691", "l": "#b8b39d", "j": "#6e6b5a", "E": "#0e0f0f",
        "F": "#a5a08a", "f": "#c2bda7", "T": "#626052", "U": "#8f8b77", "V": "#76725f",
    },
    "B": {  # cooler blue-grey, as the aquarium photos
        "H": "#646f6d", "m": "#6c7775", "k": "#606a67", "K": "#666f6d", "g": "#94a09d", "s": "#a8b1ad",
        "w": "#dde1db", "W": "#e8ebe6", "c": "#a3aca8", "l": "#b4bbb6", "j": "#68716f", "E": "#0e0f0f",
        "F": "#9ea7a3", "f": "#bcc4c0", "T": "#545b5a", "U": "#88908c", "V": "#6f7774",
    },
    "C": {  # warmer brown-grey, as the FDA photo
        "H": "#726552", "m": "#7c6e5a", "k": "#6c5f4e", "K": "#726556", "g": "#a2937b", "s": "#b3a58d",
        "w": "#e3d8c6", "W": "#ede4d5", "c": "#ae9f88", "l": "#bcae97", "j": "#6f6252", "E": "#0e0f0f",
        "F": "#ab9a80", "f": "#c8b89e", "T": "#5e5345", "U": "#93836c", "V": "#7a6b58",
    },
}
CLEAR = (0, 0, 0, 0)

# --- the model -------------------------------------------------------------------------------------------------------
# Parts: name -> (parent, pivot (absolute model pixels), zRot). Cubes: (name, part, (U, V) top-left of the used texture
# area, (x0, y0, z0) absolute, (w, h, d)). Absolute: x across, y down (24 = ground), z head (-) to tail (+).
PARTS = {
    "body": (None, (0.0, 16.0, 0.0), 0.0),
    "top_fin": (None, (0.0, 12.0, -3.0), 0.0),
    "tail_fin": (None, (0.0, 15.0, 5.0), 0.0),
}
# Round 1 (critic): the small pectoral fins came out as a pale bar under the eye (an eye and a mouth) and as a dark
# dash by the eye on land, so the model has none; the real fish's are small and pale.
# Round 2 (critic: round, like a piranha; the trigger and soft dorsal read as two horns): a diamond. The forehead runs
# down in a straight 1:1 diagonal from the trigger to the small mouth, the belly drops gently to a point under the
# trigger, and from both apexes straight diagonals run back to the stalk.
# The body's side outline per column z -9..5: (top row, bottom row, thickness in x).
# Round 4 (critic: taller than the cerna, too big beside the cod): drawn smaller, 16 px long and 8 deep (was 19 and 9).
COLUMNS = [
    (-7, 16, 17, 1),    # the lips
    (-6, 15, 17, 2),
    (-5, 14, 18, 2),
    (-4, 13, 18, 2),    # the eye
    (-3, 12, 19, 3),    # the deepest point: the trigger above, the belly's point (two pixels, not a nub) below
    (-2, 12, 19, 3),
    (-1, 12, 18, 3),
    (0, 13, 18, 3),
    (1, 13, 18, 2),
    (2, 14, 17, 2),
    (3, 14, 16, 2),     # the stalk
    (4, 14, 16, 2),
]
EXTENT = {z: (t, b) for z, t, b, _ in COLUMNS}


def _body_cubes():
    """One cube per run of equal columns; texture areas packed left to right in rows of the 64 x 32 texture."""
    runs = []
    for z, t, b, w in COLUMNS:
        if runs and runs[-1][1:] == (t, b, w) and runs[-1][0][-1] == z - 1:
            runs[-1][0].append(z)
        else:
            runs.append(([z], t, b, w))
    cubes, u, v, rowh = [], 0, 0, 0
    for i, (zs, t, b, w) in enumerate(runs):
        d, h = len(zs), b - t + 1
        aw, ah = 2 * (d + w), d + h
        if u + aw > TW:
            u, v, rowh = 0, v + rowh, 0
        cubes.append(("body%d" % i, "body", (u, v), (-w / 2.0, float(t), float(zs[0])), (w, h, d)))
        u, rowh = u + aw, max(rowh, ah)
    return cubes, v + rowh


_BODY, _FIN_V = _body_cubes()
CUBES = _BODY + [
    # the long, low soft dorsal and anal fins, far back, mirror images, ending at the tail's base
    # round 3 (maker, from the in-game shot: with low soft fins the trigger looked like a shark's fin): the soft fins
    # are as tall as the trigger at their front and paler than the back, so they make the diamond's back corners
    ("dorsal", "body", (0, _FIN_V), (0.0, 10.0, 0.0), (0, 4, 5)),
    ("anal", "body", (10, _FIN_V), (0.0, 17.0, 0.0), (0, 5, 5)),
    # the lyre tail
    ("caudal", "tail_fin", (20, _FIN_V), (0.0, 11.0, 5.0), (0, 9, 4)),
    # the trigger: one stout spine, solid (seen from every side), two pixels wide at its base, just behind the eye
    # round 3 (critic: a straight post read as a chimney): the spine rakes back, two pixels at its base and one at
    # its tip, with a pixel of membrane behind it stepping down to the back
    ("trigger", "top_fin", (28, _FIN_V), (-0.5, 10.0, -3.0), (1, 2, 1)),
    ("trigger_tip", "top_fin", (32, _FIN_V), (-0.5, 9.0, -2.0), (1, 3, 1)),
    ("membrane", "top_fin", (36, _FIN_V), (0.0, 11.0, -1.0), (0, 1, 1)),
]
EYE = (-4, 14)   # high, one row under the forehead's line, far back from the lips
# Faint saddles: (columns, rows down from the column's top that are dark 'k', then one fading 'K'). None reaches the
# eye's row (y 14) darker than 'K'.
SADDLES = {
    # round 3 (critic): the first saddle moved back from the eye
    # round 4 (critic: the eye got lost among dark squares): two soft bands, none within 2 px of the eye
    "A": [((-1, 0), 1), ((2, 3), 0)],
}
SADDLES["B"] = SADDLES["A"]
SADDLES["C"] = SADDLES["A"]
# Body tone by row, top to bottom (countershading).
ROW_TONE = {12: "m", 13: "m", 14: "g", 15: "s", 16: "s", 17: "w", 18: "w", 19: "W"}


def side_key(variant, z, y):
    top, bot = EXTENT[z]
    if not top <= y <= bot:
        return None
    if (z, y) == EYE:
        return "E"
    if z == -7:
        return "j" if y == bot else "c"          # the lips grey (pale read as a nub); the mouth a mid grey below
    if z <= -4:                                  # the head: crown, then cheek, then pale throat
        if y == top:
            # round 4: next to the eye the crown is plain back grey, so nothing dark touches the eye
            return "m" if abs(z - EYE[0]) <= 1 else "H"
        if y <= 14:
            return "g"                           # the eye's ring: plain upper-flank grey
        if y <= 17:
            return "c"
        return "w"
    for cols, n in SADDLES[variant]:
        if z in cols:
            if y < top + n:
                return "k"
            if y == top + n:
                return "K"
    return ROW_TONE[y]


DORSAL = {  # rows y 10..13, columns z 0..4: tall at the front, then a straight slope down to the stalk; the
    # trailing edge (f) paler, so it reads as fin and not as the body's outline (round 4)
    10: "F....",
    11: "FFf..",
    12: "FFFf.",
    13: "..FFf",
}
ANAL = {  # rows y 17..21, columns z 0..4: the dorsal's mirror image, ending at the same column
    17: "...Ff",
    18: "..FF.",
    19: "FFFf.",
    20: "FFf..",
    21: "F....",
}
CAUDAL = {  # rows y 11..19, columns z 5..8: a solid fan at the base, a concave rear edge, pointed tips
    # round 3 (critic: thin lobes read as antennae): the web fills between the lobes, a shade darker than the body
    11: "...V",
    12: ".UVV",
    13: "UUV.",
    14: "UU..",
    15: "UU..",
    16: "UU..",
    17: "UUV.",
    18: ".UVV",
    19: "...V",
}


def pal(variant):
    return {k: hexc(v) for k, v in PALETTES[variant].items()}


def body_colour(variant, P, name, face, x, y, z, x0, y0, z0, w, h, d):
    zi, yi = int(math.floor(z)), int(math.floor(y))
    if name.startswith("trigger"):
        return P["T"]
    if face == "top":
        k = side_key(variant, zi, EXTENT[zi][0])
        if zi == -7:
            return P["g"]                        # round 4: the snout's top not pale (a pale tip read as a nub from above)
        return P["H" if k in ("E", None) else k]
    if face == "bottom":
        return P["l" if zi == -7 else "W"]
    if face in ("west", "east"):
        k = side_key(variant, zi, yi)
        return P[k or "c"]
    if face == "north":
        if name == "body0":
            return P["j" if yi == 17 else "g"]
        k = side_key(variant, int(math.floor(z0)), yi)
        return P[{"E": "g", None: "H"}.get(k, k)]
    k = side_key(variant, int(math.floor(z0 + d - 1)), yi)
    return P[{"E": "c", None: "m"}.get(k, k)]


def fin_colour(P, name, x, y, z):
    zi, yi = int(math.floor(z)), int(math.floor(y))
    if name == "membrane":
        ch = "f"
    elif name == "dorsal":
        ch = DORSAL[yi][zi]
    elif name == "anal":
        ch = ANAL[yi][zi]
    else:
        ch = CAUDAL[yi][zi - 5]
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


def check_fins_touch():
    """Every fin pixel shares an edge with the body or with another pixel of its fin that does (the rule: every fin
    touches the body, with solid edges)."""
    for rows, zoff, part in ((DORSAL, 0, "dorsal"), (ANAL, 0, "anal")):
        cells = {(zoff + i, y) for y, r in rows.items() for i, ch in enumerate(r) if ch != "."}
        for (z, y) in cells:
            assert not EXTENT[z][0] <= y <= EXTENT[z][1], (part, "fin inside body", z, y)
        touching = {(z, y) for (z, y) in cells if EXTENT[z][0] - 1 == y or EXTENT[z][1] + 1 == y}
        assert touching, part
        grown = set(touching)
        while True:
            more = {c for c in cells - grown if any((c[0] + a, c[1] + b) in grown
                                                     for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
            if not more:
                break
            grown |= more
        assert grown == cells, (part, "loose fin pixels", sorted(cells - grown))


# --- the Java model ---------------------------------------------------------------------------------------------------
def write_java():
    f = sard.f
    lines = []
    for part in ("body", "top_fin", "tail_fin"):
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
 * The hmar (grey triggerfish): a deep, flat-sided rhomboid body in olive-grey with faint darker saddles and a pale
 * belly, a small pale-lipped mouth at the tip of a long sloping snout, an eye set high and far back, the stout trigger
 * spine, long matching soft dorsal and anal fins far back, and a lyre tail with pointed tips that sways as it swims.
 * 17 px long, 9 px deep (13 with the fins), 3 px thick, head toward -z, the ground at y 24.
 * Made by art/src/fish_hmar_model.py (don't edit by hand). Texture: textures/entity/fish/hmar.png (64 x 32).
 */
public class HmarModel extends FishModel {
    public HmarModel(ModelPart root) {
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
        title("Same scale offline, 12x: hmar, vanilla cod")
        row([Image.open(os.path.join(CAND, "scale_vs_cod.png")).convert("RGBA")])
    if shots_dir and os.path.isdir(shots_dir):
        def shot(n):
            found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None
        names = ["fish-hmar-side", "fish-hmar-three-quarter", "fish-hmar-top", "fish-hmar-beside-cod",
                 "fish-hmar-on-land", "fish-hmar-lineup"]
        present = [(n, shot(n)) for n in names]
        present = [(n, i) for n, i in present if i]
        if present:
            title("In the game: side, three-quarter, top; beside vanilla cod, on land, lineup (hmar, cod, cerna, small tonn)")
            row([i for _, i in present[:3]], h=330)
            row([i for _, i in present[3:]], h=330)
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    dest = os.path.join(ROOT, "art", "candidates", "fish_hmar_model.png")
    out.convert("RGB").save(dest)
    print("sheet:", dest)


def main():
    check_fins_touch()
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
