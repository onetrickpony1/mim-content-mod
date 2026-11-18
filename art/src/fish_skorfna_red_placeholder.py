"""Placeholder texture for the red skorfna (red scorpionfish, Scorpaena scrofa), 2026-11-18.

The skorfna has two versions on one model (decision "Skorfna - two versions, red and black, as reskins"). Until the
art makers draw the red one, this makes a red-tinted copy of the black one's texture, so the variant can be built and
tested. Not reviewed art: the art maker replaces it at the same path.

Reads   textures/entity/fish/skorfna.png
Writes  textures/entity/fish/skorfna_red.png   (never overwrites it if it already exists)
Run:    art/.venv/bin/python art/src/fish_skorfna_red_placeholder.py
"""
import os
import sys

from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
FISH = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "entity", "fish")
SRC = os.path.join(FISH, "skorfna.png")
OUT = os.path.join(FISH, "skorfna_red.png")


def main():
    if os.path.exists(OUT):
        print("exists, left alone: " + OUT)
        return 0
    img = Image.open(SRC).convert("RGBA")
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            # keep the light and dark of the mottling, turn the colour toward a scorpionfish red
            lum = (r * 299 + g * 587 + b * 114) / 1000
            px[x, y] = (min(255, int(lum * 1.35 + 40)), int(lum * 0.55), int(lum * 0.45), a)
    img.save(OUT)
    print("wrote " + OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
