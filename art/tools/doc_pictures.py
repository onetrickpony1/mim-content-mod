"""Pictures for docs/Food/Food progress.md: each item icon enlarged 8x, and in-game shots of the placed dishes.

Usage: python doc_pictures.py [screenshots dir]
The icons come from the mod's textures. The in-game shots come from a run of tools/run-art.sh
(default: mod/build/smoke-run/screenshots); shots that are missing are skipped.
Writes docs/Food/images/.
"""
import glob
import os
import sys
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
OUT = os.path.join(ROOT, "docs", "Food", "images")
SHOTS = {  # in-game shot name -> picture name
    "12-ross-il-forn-table": "ingame_ross_il_forn",
    "14-imqarrun-table": "ingame_imqarrun_il_forn",
    "15-timpana-table": "ingame_timpana",
    "16-torta-table": "ingame_torta_lampuki",
    "02-kenur-close-day": "ingame_kenur",
    "04-pots-on-table-day": "ingame_borma",
}


def main(shots_dir):
    os.makedirs(OUT, exist_ok=True)
    for p in sorted(glob.glob(os.path.join(ITEMS, "*.png"))):
        im = Image.open(p).convert("RGBA")
        im = im.crop((0, 0, im.width, im.width))  # first frame of an animated texture
        im.resize((128, 128), Image.NEAREST).save(os.path.join(OUT, os.path.basename(p)))
    for shot, name in SHOTS.items():
        found = sorted(glob.glob(os.path.join(shots_dir, f"*_{shot}.png")))
        if found:
            im = Image.open(found[-1]).convert("RGB")
            im.resize((im.width * 3 // 4, im.height * 3 // 4), Image.LANCZOS).save(os.path.join(OUT, name + ".jpg"), quality=88)
        else:
            print("missing shot", shot)
    print("wrote", OUT)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "mod", "build", "smoke-run", "screenshots"))
