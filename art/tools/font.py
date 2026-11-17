"""A label font with the Maltese letters (ċ ġ għ ħ ż, capitals too).

Pillow's built-in default font only covers basic Latin, so Ħ, Ż, Ġ came out as boxes in the review pictures.
Every picture that writes text uses label_font() instead.
"""
import os
from PIL import ImageFont

CANDIDATES = [
    "/usr/share/fonts/noto/NotoSans-Regular.ttf",
    "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/TTF/DejaVuSans.ttf",
]


def label_font(size=14):
    for p in CANDIDATES:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    raise SystemExit("no font with Maltese letters found; install one of: " + ", ".join(CANDIDATES))
