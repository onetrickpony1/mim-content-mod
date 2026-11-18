"""Offline hotbar preview: flat item icons drawn in the real vanilla hotbar at the game's GUI scale.

The game draws a flat item (item icon, spawn egg, layered bucket) as its 16x16 texture scaled up with no
filtering, so this shows exactly what the hotbar shows, without starting Minecraft. 3D models still need
the in-game test (owner decision 2026-11-18, "Icons previewed offline; in-game tests for models and per category").

Usage:
  art/.venv/bin/python art/tools/hotbar_preview.py OUT.png ITEM [ITEM ...] [--scale 4] [--select N]

ITEM forms (up to 9):
  mc:cod                 vanilla item texture (art/.vanilla/item/cod.png)
  mod:lampuka            our item texture (mod resources, textures/item/lampuka.png)
  bucket:cerna_bucket    our layered bucket: the vanilla cod_bucket with our layer on top, as the game draws it
  file:/path/to/x.png    any 16x16 png (e.g. a candidate not yet written to the mod)

The hotbar sprites come from the vanilla client jar into art/.vanilla/gui/ (git-ignored).
The preview is drawn twice, over a light (sky) and a dark (night or cave) backdrop.
"""
import argparse
import os
import sys
from PIL import Image

ART = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
ROOT = os.path.dirname(ART)
VAN = os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla"))
MOD = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
BACKDROPS = [(120, 167, 255, 255), (24, 26, 32, 255)]


def load(spec):
    kind, rest = spec.split(":", 1)
    if kind == "mc":
        path = os.path.join(VAN, "item", rest + ".png")
    elif kind == "mod":
        path = os.path.join(MOD, "item", rest + ".png")
    elif kind == "file":
        path = rest
    elif kind == "bucket":
        base = Image.open(os.path.join(VAN, "item", "cod_bucket.png")).convert("RGBA")
        layer = Image.open(os.path.join(MOD, "item", rest + ".png")).convert("RGBA")
        base.alpha_composite(layer)
        return base
    else:
        sys.exit(f"unknown item form: {spec}")
    if not os.path.exists(path):
        sys.exit(f"missing texture: {path}")
    im = Image.open(path).convert("RGBA")
    return im.crop((0, 0, 16, 16)) if im.size != (16, 16) else im


def hotbar(items, scale, select):
    bar = Image.open(os.path.join(VAN, "gui", "hotbar.png")).convert("RGBA")
    sel = Image.open(os.path.join(VAN, "gui", "hotbar_selection.png")).convert("RGBA")
    w, h = bar.size[0] + 2, sel.size[1]
    out = []
    for bg in BACKDROPS:
        im = Image.new("RGBA", (w, h), bg)
        im.alpha_composite(bar, (1, 1))
        for i, it in enumerate(items):
            im.alpha_composite(it, (1 + 3 + 20 * i, 1 + 3))
        if select is not None:
            im.alpha_composite(sel, (20 * select, 0))
        out.append(im.resize((w * scale, h * scale), Image.NEAREST))
    sheet = Image.new("RGBA", (out[0].width, sum(o.height for o in out) + 8 * scale), (139, 139, 139, 255))
    y = 0
    for o in out:
        sheet.alpha_composite(o, (0, y))
        y += o.height + 8 * scale
    return sheet


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out")
    ap.add_argument("items", nargs="+")
    ap.add_argument("--scale", type=int, default=2, help="GUI scale; the in-game screenshots come out at 2")
    ap.add_argument("--select", type=int, default=None, help="slot index 0-8 to show as selected")
    a = ap.parse_args()
    if len(a.items) > 9:
        sys.exit("the hotbar holds 9 items")
    hotbar([load(s) for s in a.items], a.scale, a.select).save(a.out)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
