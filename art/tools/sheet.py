"""Comparison sheet: the mod's textures enlarged beside the vanilla textures they must sit with.

Usage: python sheet.py <vanilla textures dir> <out.png>
Rows are (label, [paths]); "mod:" paths are in the mod's resources, "mc:" in the vanilla folder.
Block textures are tiled 2x2 so seams show.
"""
import os
import sys
from PIL import Image, ImageDraw

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
MOD = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")

ROWS = [
    ("bread: vanilla bread | ħobż tal-Malti | vanilla baked potato", ["mc:item/bread", "mod:item/hobz_malti", "mc:item/baked_potato"]),
    ("pastry: vanilla cookie | pastizz tal-irkotta | vanilla pumpkin pie", ["mc:item/cookie", "mod:item/pastizz_irkotta", "mc:item/pumpkin_pie"]),
    ("cheese: vanilla egg | ġbejna | vanilla milk bucket", ["mc:item/egg", "mod:item/gbejna", "mc:item/milk_bucket"]),
    ("stone (tiled 2x2): vanilla sandstone | kenur side | kenur top | vanilla furnace side", ["mc:block/sandstone", "mod:block/kenur_side", "mod:block/kenur_top", "mc:block/furnace_side"]),
    ("inside (tiled): kenur soot | kenur ash | kenur ash lit | vanilla campfire log lit", ["mod:block/kenur_soot", "mod:block/kenur_ash", "mod:block/kenur_ash_lit", "mc:block/campfire_log_lit"]),
    ("clay (tiled): vanilla terracotta | borma side | borma top empty | borma top stuffat | vanilla decorated pot side", ["mc:block/terracotta", "mod:block/borma_side", "mod:block/borma_top_empty", "mod:block/borma_top_stuffat", "mc:entity/decorated_pot/decorated_pot_side"]),
]
SCALE = 8
CELL = 16 * SCALE * 2 + 16


def load(spec, vanilla):
    kind, rel = spec.split(":", 1)
    base = MOD if kind == "mod" else vanilla
    p = os.path.join(base, rel + ".png")
    if not os.path.exists(p):
        return None
    im = Image.open(p).convert("RGBA")
    if im.height > im.width:
        im = im.crop((0, 0, im.width, im.width))
    return im.crop((0, 0, 16, 16)) if im.width > 16 else im


def main(vanilla, out):
    W = 16 + CELL * max(len(r[1]) for r in ROWS)
    H = sum(CELL + 30 for _ in ROWS) + 10
    sheet = Image.new("RGBA", (W, H), (139, 139, 139, 255))  # the inventory slot grey
    d = ImageDraw.Draw(sheet)
    y = 10
    for label, specs in ROWS:
        d.text((16, y), label, fill=(20, 20, 20, 255))
        y += 18
        for i, s in enumerate(specs):
            im = load(s, vanilla)
            if im is None:
                continue
            tiled = "block/" in s
            if tiled:
                t = Image.new("RGBA", (32, 32))
                for dx in (0, 16):
                    for dy in (0, 16):
                        t.paste(im, (dx, dy))
                im = t
                big = im.resize((32 * SCALE // 2 * 2, 32 * SCALE // 2 * 2), Image.NEAREST).resize((CELL - 16, CELL - 16), Image.NEAREST)
            else:
                big = im.resize((CELL - 16, CELL - 16), Image.NEAREST)
            x = 16 + i * CELL
            sheet.alpha_composite(big, (x, y))
            d.text((x, y + CELL - 14), s, fill=(10, 10, 10, 255))
        y += CELL + 12
    sheet.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
