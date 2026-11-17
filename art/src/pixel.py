"""Small pixel-art toolkit for 16x16 Minecraft textures.

Textures are built from rules (shape, light, palette ramp, noise, outline), not drawn by hand, so they can be
re-made and tuned. Style numbers come from vanilla (art/STYLE.md, measured by art/tools/measure.py).
"""
import math
import numpy as np
from PIL import Image

N = 16
LIGHT = (-0.55, -0.65, 0.52)  # from the top left, a little towards the viewer (vanilla items: tl-br ~ +0.07)


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def ramp(*hexes):
    return [hexrgb(h) for h in hexes]


def hash01(x, y, seed=0):
    """Deterministic per-pixel noise in [0, 1)."""
    v = math.sin(x * 127.1 + y * 311.7 + seed * 74.7) * 43758.5453
    return v - math.floor(v)


def smooth_noise(x, y, scale, seed=0, period=None):
    """Value noise, bilinear with smoothstep; scale in pixels. With period (in lattice cells) it tiles."""
    gx, gy = x / scale, y / scale
    x0, y0 = math.floor(gx), math.floor(gy)
    fx, fy = gx - x0, gy - y0
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    w = (lambda i: i % period) if period else (lambda i: i)
    a, b = hash01(w(x0), w(y0), seed), hash01(w(x0 + 1), w(y0), seed)
    c, d = hash01(w(x0), w(y0 + 1), seed), hash01(w(x0 + 1), w(y0 + 1), seed)
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def tile_noise(x, y, scale, seed=0):
    """Noise that tiles every 16 px, for block faces that sit side by side. scale must divide 16 (2, 4, 8)."""
    return smooth_noise(x, y, scale, seed, period=N // scale)


class Canvas:
    def __init__(self):
        self.rgba = np.zeros((N, N, 4), dtype=np.uint8)

    def set(self, x, y, rgb, a=255):
        if 0 <= x < N and 0 <= y < N:
            self.rgba[y, x, :3] = rgb
            self.rgba[y, x, 3] = a

    def get(self, x, y):
        return tuple(self.rgba[y, x, :3])

    def opaque(self, x, y):
        return 0 <= x < N and 0 <= y < N and self.rgba[y, x, 3] > 0

    def save(self, path):
        Image.fromarray(self.rgba, "RGBA").save(path)


def shade_dome(mask, cx, cy, rx, ry, height=1.0):
    """Per-pixel light (0..1) for a dome over an ellipse, lit from LIGHT."""
    lx, ly, lz = LIGHT
    ln = math.sqrt(lx * lx + ly * ly + lz * lz)
    lx, ly, lz = lx / ln, ly / ln, lz / ln
    out = np.zeros((N, N))
    for y in range(N):
        for x in range(N):
            if not mask[y, x]:
                continue
            u, v = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
            r2 = min(u * u + v * v, 0.98)
            nz = math.sqrt(1 - r2) * height
            nx, ny = u, v
            nn = math.sqrt(nx * nx + ny * ny + nz * nz)
            out[y, x] = max(0.0, (nx * lx + ny * ly + nz * lz) / nn)
    return out


def pick(r, t):
    """Pick from a ramp (dark -> light) with t in 0..1."""
    i = int(round(max(0.0, min(1.0, t)) * (len(r) - 1)))
    return r[i]


def outline(c, edge_rgb, inner_rgb=None, inner_side=("down", "right")):
    """Vanilla-style outline: every opaque pixel touching transparency takes the edge colour.
    Optionally a second, softer colour on the shadow side (bottom/right) one pixel inside."""
    edges = []
    for y in range(N):
        for x in range(N):
            if not c.opaque(x, y):
                continue
            if any(not c.opaque(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                edges.append((x, y))
    for x, y in edges:
        c.set(x, y, edge_rgb)
    if inner_rgb:
        es = set(edges)
        for x, y in edges:
            for dx, dy, side in ((0, -1, "down"), (-1, 0, "right")):
                if side in inner_side:
                    nx, ny = x + dx, y + dy
                    if c.opaque(nx, ny) and (nx, ny) not in es:
                        c.set(nx, ny, inner_rgb)


def ellipse_mask(cx, cy, rx, ry):
    m = np.zeros((N, N), dtype=bool)
    for y in range(N):
        for x in range(N):
            u, v = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
            m[y, x] = u * u + v * v <= 1.0
    return m
