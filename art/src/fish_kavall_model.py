"""The kavall (Atlantic chub mackerel, Scomber colias) as a swimming mob: its 3D model and its texture.

Night job piece 1 of 3 (docs/Decisions/2026-11-18 Night job - the rest of the fish, Claude decides.md). Drawn from the
photos in art/references/fish_kavall_refonly/ (list.tsv; fresh fish out of water for colour). What makes it a kavall:
  - a torpedo body, round in section, pointed at both ends: a short pointed snout, a big eye high on the head,
    the deepest part just behind the gill cover, tapering to a thin tail stalk;
  - a blue-green back crossed by dark wavy "tiger" bars that run down the upper flank (seen from above, chevrons);
  - silver sides and a pale belly (countershaded), with faint grey spots on the lower flank (the chub mackerel's mark,
    which the Atlantic mackerel, pizzintun, lacks);
  - two dorsal fins set well apart, small finlets on the back and belly between them and the tail;
  - a deeply forked tail, dusky olive-yellow like the other fins.
Every colour is a step lighter than the photos, because the game greys and darkens everything under water.

Size: 21 px long (17 of body from the snout tip, 4 of tail), 4 px deep, 3 px wide at the trunk: about 1.3 blocks,
visibly longer and slimmer than vanilla cod (15 px). Model critic rounds: 4 (PASS in round 4). One texture pixel per
model pixel, like vanilla's fish.

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, a root
child "body", "top_fin" (the first dorsal fin) and a "tail_fin" that sways like vanilla cod's.

Candidates (the same model, three paint jobs): A blue-green back with chevron bars; B the same with bolder, darker
bars reaching lower and a cooler steel-blue back; C greener olive back as in the Atlantic photos. CHOSEN is installed.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/KavallModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/kavall.png    (32 x 32)
  art/candidates/kavall_model/  (candidate textures and offline previews)
With --sheet SCREENSHOT_DIR also writes the review sheet art/candidates/fish_kavall_model.png.

Run:  art/.venv/bin/python art/src/fish_kavall_model.py [--sheet SCREENSHOT_DIR]
"""
import colorsys
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
                    "KavallModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "kavall.png")
CAND = os.path.join(ROOT, "art", "candidates", "kavall_model")
TW, TH = 32, 32
CHOSEN = "A"
VANILLA_JAR = "/home/cultar/Apps/Minecraft World/tools/gradle-home/caches/fabric-loom/26.3/minecraft-merged.jar"


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


# Palettes. Keys:
#   H head top (steel blue-green), c cheek silver, E eye, j mouth line, J mouth line fading
#   m back blue-green, k dark bar, M bar where it fades down the flank, g green-silver upper flank
#   s silver, W bright silver, w belly, p faint lower-flank spot
#   F fin lit, f fin, a pale belly fin, T tail lit, t tail shade, P pectoral fin (dusky)
PALETTES = {
    # round 3 (critic): the back greener and duller (it read aqua on land), the bars a mid-dark blue-green so the eye
    # stays the darkest mark, the cheek a pale silver ring round the eye
    "A": {
        "H": "#4a7c72", "c": "#d8dee0", "E": "#0b0d0e", "j": "#7d8b8e", "J": "#a7b3b5",
        "m": "#3c7a6e", "k": "#234a4e", "M": "#557a74", "g": "#9db8b0",
        "s": "#cdd7d8", "W": "#e4ecec", "w": "#fbfcfa", "p": "#a3b0b4",
        "F": "#b4b07e", "f": "#8f8c62", "a": "#b9b98e", "T": "#c2bb7a", "t": "#aaa46a", "u": "#b8b070",
        "P": "#7f9492",
    },
    # B: a cooler steel-blue back, as the Mediterranean market photos
    "B": {
        "H": "#46768a", "c": "#d8dee0", "E": "#0b0d0e", "j": "#7d8a90", "J": "#a7b2b7",
        "m": "#3a6f80", "k": "#1f4452", "M": "#4f6f7c", "g": "#a6bcc1",
        "s": "#c8d2d6", "W": "#e4ebee", "w": "#fafbfa", "p": "#9aa7ad",
        "F": "#aeab80", "f": "#878562", "a": "#b5b48e", "T": "#b2ad76", "t": "#84815a", "u": "#999567",
        "P": "#7a8e96",
    },
    # C: an olive-green back, as the Atlantic photos
    "C": {
        "H": "#5b8270", "c": "#d8dee0", "E": "#0b0d0e", "j": "#7f8a86", "J": "#a9b3ae",
        "m": "#4d7b62", "k": "#2a4a3c", "M": "#5f7a66", "g": "#b0c4b2",
        "s": "#cbd4d1", "W": "#e5ece8", "w": "#fbfbf7", "p": "#a5afac",
        "F": "#bcb47a", "f": "#958e5c", "a": "#bdb98a", "T": "#c0b46e", "t": "#918852", "u": "#a49c60",
        "P": "#839488",
    },
}
CLEAR = (0, 0, 0, 0)

# --- the model -------------------------------------------------------------------------------------------------------
# Parts: name -> (parent, pivot (absolute model pixels), zRot). Cubes: (name, part, (U, V) top-left of the used texture
# area, (x0, y0, z0) absolute, (w, h, d)). Absolute: x across, y down (24 = ground), z head (-) to tail (+).
# Round 3 (critic: too deep and boxy, read as a small tuna): 20 px long (16 of body, 4 of tail), 4 px deep, a pointed
# 1 px snout, and a rear that tapers in two steps to a 2 px stalk.
PARTS = {
    "body": (None, (0.0, 21.0, 0.0), 0.0),
    "top_fin": (None, (0.0, 19.0, -5.0), 0.0),
    "tail_fin": (None, (0.0, 21.0, 7.0), 0.0),
    # the small pectoral fins, hinged on the flanks just behind the gill cover, angled down and out
    "right_fin": (None, (-1.5, 21.0, -5.0), -0.9),
    "left_fin": (None, (1.5, 21.0, -5.0), 0.9),
}
# Round 4 (critic: not visibly longer than cod): 21 px long (17 of body, 4 of tail), 4 px deep; the rear tapers from
# below in two steps (3 px, then the 2 px stalk), so the back line runs on straight and the bars stay above the eye's
# row all the way to the tail.
CUBES = [
    # the pointed snout, the head with the big eye, the trunk, the tapering rear and the thin stalk
    ("snout", "body", (22, 7), (-0.5, 20.0, -10.0), (1, 2, 1)),
    ("head", "body", (22, 0), (-1.0, 19.0, -9.0), (2, 4, 3)),
    ("trunk", "body", (0, 0), (-1.5, 19.0, -6.0), (3, 4, 8)),
    ("rear", "body", (0, 12), (-1.0, 19.0, 2.0), (2, 3, 3)),
    ("stalk", "body", (10, 12), (-0.5, 20.0, 5.0), (1, 2, 2)),
    # the first dorsal fin (its own part, as the contract names it), the small second dorsal fin, and under the belly
    # the pelvic fin and the anal fin opposite the second dorsal: thin strips sloping back, never square blocks
    # (round 3, critic: two squares under the belly read as legs)
    ("dorsal1", "top_fin", (24, 12), (0.0, 17.0, -5.0), (0, 2, 3)),
    ("dorsal2", "body", (24, 14), (0.0, 17.0, 1.0), (0, 2, 1)),
    ("anal", "body", (26, 14), (0.0, 23.0, 0.0), (0, 1, 2)),
    ("pelvic", "body", (26, 15), (0.0, 23.0, -4.0), (0, 1, 2)),
    # the finlets: one small nub on the stalk's back and one on its belly, just before the tail
    ("finlets_top", "body", (24, 16), (0.0, 19.0, 6.0), (0, 1, 1)),
    ("finlets_bot", "body", (26, 16), (0.0, 22.0, 6.0), (0, 1, 1)),
    # the deeply forked tail
    ("caudal", "tail_fin", (16, 12), (0.0, 18.0, 7.0), (0, 6, 4)),
    # the pectoral fins
    ("pec_r", "right_fin", (0, 18), (-2.5, 21.0, -5.0), (1, 0, 2)),
    ("pec_l", "left_fin", (2, 18), (1.5, 21.0, -5.0), (1, 0, 2)),
]

# The side of the fish, rows y 19..22, columns z -10..6. '.' where no section reaches.
# Row 19: the steel head, then the back with a thin dark bar every third pixel, starting three pixels behind the eye
#         (the front of the back is plain) and running to the rear.
# Row 20, the eye's row: the snout, the pale cheek ringing the eye behind and below, then a plain green-silver upper
#         flank with no mark in it at all (round 4, critic: bars in this row read as more eyes); the stalk's back teal.
# Row 21: the mouth line's fading end under the snout, the pale cheek, then silver.
# Row 22: the near-white belly (countershading: back, green-silver, silver, white, top to bottom).
SIDE_Z0 = -10
SIDES = {
    "A": {
        19: ".HHHmkmmkmmkmmk..",
        20: "HcEcgggggggggggmm",
        21: "Jcccsssssssssssss",
        22: ".cwwwwwwwwww.....",
    },
}
SIDES["B"] = SIDES["A"]
SIDES["C"] = SIDES["A"]
# The back seen from above: rows x (trunk three columns; head and rear two, which take the outer rows), columns z
# -10..6. Each bar is a thin chevron across the back: the edges at z, the middle a pixel behind, every third pixel.
TOPS = {v: ["HHHHmkmmkmmkmmkmm", "HHHHmmkmmkmmkmmmm", "HHHHmkmmkmmkmmkmm"] for v in PALETTES}
# The belly seen from below: the pale cheek under the snout and head, the white belly, silver under the rear.
BOTTOM = "ccccwwwwwwwwsssss"

# Fin outlines: one character per pixel, rows by absolute y, columns by absolute z.
DORSAL1_Z0, DORSAL1_Y0 = -5, 17
DORSAL1 = [
    "Ff.",
    "fFf",
]
# the tail: a solid 2 x 2 base on the stalk and two 2 px lobes, each pixel sharing an edge with the next, so it stays
# one shape from every angle (round 4, critic: 1 px corner-touching lobes broke up into floating specks)
CAUDAL_Z0, CAUDAL_Y0 = 7, 18
CAUDAL = [
    "..TT",
    ".TT.",
    "uu..",
    "uu..",
    ".tt.",
    "..tt",
]
# the finlets, column z 6
FINLETS = "f"
# the anal and pelvic strips: dusky olive, a darker tone than the tail so they never read as a pale mark (round 4)
STRIP = "ff"


def pal(variant):
    return {k: hexc(v) for k, v in PALETTES[variant].items()}


def body_colour(variant, P, name, face, x, y, z, x0, y0, z0, w, h, d):
    """The colour of one texel of a body section, from where it sits on the fish. Faces hidden inside the fish get
    the body colour around them, so no stray colour hides anywhere in the texture."""
    side = SIDES[variant]
    zi, yi = int(math.floor(z)), int(math.floor(y))
    col = zi - SIDE_Z0
    if face == "top":
        rows = TOPS[variant]
        xi = int(math.floor(x + 1.5))           # 0..2 across the trunk
        if w < 3:
            xi = 0 if x < 0 else 2
        return P[rows[min(2, max(0, xi))][col]]
    if face == "bottom":
        return P[BOTTOM[col]]
    if face in ("west", "east"):
        ch = side[yi][col]
        return P["c" if ch == "." else ch]
    if face == "north":
        if name == "snout":
            return P["H"] if yi == 20 else P["J"]
        # the ring of each section round the one in front: the side colour of its first column, never the eye's
        ch = side[yi][int(math.floor(z0)) - SIDE_Z0]
        return P[{"E": "c", ".": "H"}.get(ch, ch)]
    # south: the back end of a section, the colour of its last side column
    ch = side[yi][int(math.floor(z0 + d - 1)) - SIDE_Z0]
    return P[{"E": "c", ".": "m"}.get(ch, ch)]


def fin_colour(P, name, x, y, z):
    zi, yi = int(math.floor(z)), int(math.floor(y))
    if name == "dorsal1":
        ch = DORSAL1[yi - DORSAL1_Y0][zi - DORSAL1_Z0]
    elif name == "caudal":
        ch = CAUDAL[yi - CAUDAL_Y0][zi - CAUDAL_Z0]
    elif name in ("finlets_top", "finlets_bot"):
        ch = FINLETS[zi - 6]
    elif name == "dorsal2":
        ch = "f"
    elif name == "anal":
        ch = STRIP[zi]
    elif name == "pelvic":
        ch = STRIP[zi + 4]
    else:
        ch = "P"                               # the pectorals: a dusky mid tone, never a bright or dark spot
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
 * The kavall (chub mackerel): a torpedo with a pointed snout and a big eye, a blue-green back crossed by dark wavy
 * bars, silver sides and a pale belly with faint spots, two dorsal fins set apart, small finlets before a deeply
 * forked olive-yellow tail that sways as it swims. 21 px long, 4 px deep, 3 px wide, head toward -z, the ground at y 24.
 * Made by art/src/fish_kavall_model.py (don't edit by hand). Texture: textures/entity/fish/kavall.png (32 x 32).
 */
public class KavallModel extends FishModel {
    public KavallModel(ModelPart root) {
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
        title("Same scale offline, 12x: kavall, vanilla cod")
        row([Image.open(os.path.join(CAND, "scale_vs_cod.png")).convert("RGBA")])
    if shots_dir and os.path.isdir(shots_dir):
        def shot(n):
            found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None
        names = ["fish-kavall-side", "fish-kavall-three-quarter", "fish-kavall-top", "fish-kavall-beside-cod",
                 "fish-kavall-on-land", "fish-kavall-lineup"]
        present = [(n, shot(n)) for n in names]
        present = [(n, i) for n, i in present if i]
        if present:
            title("In the game: side, three-quarter, top; beside vanilla cod, on land, lineup (kavall, cod, cerna, small tonn)")
            row([i for _, i in present[:3]], h=330)
            row([i for _, i in present[3:]], h=330)
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    dest = os.path.join(ROOT, "art", "candidates", "fish_kavall_model.png")
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
