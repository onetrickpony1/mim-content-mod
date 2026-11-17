"""The picture sent to the owner: the in-game food hotbar, then the item textures enlarged beside vanilla.

Usage: python owner_sheet.py <hotbar screenshot> <vanilla item textures dir> <out.png>
"""
import os
import sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from font import label_font

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
MOD = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
ITEMS = [("mc", "bread", "bread"), ("mod", "hobz_malti", "Ħobż tal-Malti"), ("mc", "cookie", "cookie"),
         ("mod", "pastizz_irkotta", "Pastizz tal-Irkotta"), ("mod", "pastizz_pizelli", "Pastizz tal-Piżelli"),
         ("mc", "pumpkin_pie", "pumpkin pie"), ("mc", "baked_potato", "baked potato"), ("mod", "gbejna", "Ġbejna"),
         ("mc", "egg", "egg")]


def main(shot, vanilla, out):
    hot = Image.open(shot).convert("RGBA")
    w, h = hot.size
    hb = hot.crop((w // 2 - 364, h - 88, w // 2 + 364, h))  # the hotbar at gui scale 4
    S = 10
    cell = 16 * S + 24
    W = max(hb.width * 2 + 20, cell * len(ITEMS) + 20)
    H = 36 + hb.height * 2 + 50 + cell + 30
    img = Image.new("RGBA", (W, H), (40, 40, 40, 255))
    d = ImageDraw.Draw(img)
    f, fs = label_font(18), label_font(15)
    d.text((10, 8), "In the game's hotbar: the Maltese foods between vanilla ones", fill=(255, 255, 255, 255), font=f)
    img.paste(hb.resize((hb.width * 2, hb.height * 2), Image.NEAREST), (10, 36))
    y = 36 + hb.height * 2 + 16
    d.text((10, y), "The textures enlarged 10× (ours in gold)", fill=(255, 255, 255, 255), font=f)
    y += 30
    for i, (kind, name, label) in enumerate(ITEMS):
        p = os.path.join(MOD if kind == "mod" else vanilla, name + ".png")
        im = Image.open(p).convert("RGBA").crop((0, 0, 16, 16)).resize((16 * S, 16 * S), Image.NEAREST)
        x = 10 + i * cell
        img.paste(Image.new("RGBA", (16 * S, 16 * S), (139, 139, 139, 255)), (x, y))
        img.alpha_composite(im, (x, y))
        d.text((x, y + 16 * S + 4), label, font=fs,
               fill=(240, 200, 90, 255) if kind == "mod" else (180, 180, 180, 255))
    img.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main(*sys.argv[1:4])
