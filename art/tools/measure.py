"""Measure the pixel-art style of 16x16 textures, so the mod's art can match vanilla by numbers.

Usage: python measure.py <png or folder> [...]
Prints, per texture: size, opaque coverage, unique colours, darkest/lightest luminance,
outline darkness (edge pixels vs interior), light direction (top-left vs bottom-right),
and the shade ramps per hue family. Ends with averages over all files given.
"""
import sys, os, colorsys
import numpy as np
from PIL import Image


def lum(rgb):
    r, g, b = [c / 255 for c in rgb[:3]]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def measure(path):
    im = Image.open(path).convert("RGBA")
    a = np.array(im)
    h, w = a.shape[:2]
    if h > w:  # animated strip: first frame
        a = a[:w]
        h = w
    alpha = a[..., 3] > 0
    n = int(alpha.sum())
    if n == 0:
        return None
    cols = {tuple(px) for px in a[alpha][:, :3]}
    L = np.zeros((h, w))
    for y in range(h):
        for x in range(w):
            if alpha[y, x]:
                L[y, x] = lum(a[y, x])
    # edge = opaque pixel with a transparent (or out-of-image) 4-neighbour
    edge = np.zeros_like(alpha)
    for y in range(h):
        for x in range(w):
            if not alpha[y, x]:
                continue
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yy, xx = y + dy, x + dx
                if yy < 0 or xx < 0 or yy >= h or xx >= w or not alpha[yy, xx]:
                    edge[y, x] = True
    interior = alpha & ~edge
    edge_l = L[edge].mean() if edge.any() else float("nan")
    int_l = L[interior].mean() if interior.any() else float("nan")
    # light direction: opaque pixels above/left of the diagonal vs below/right
    yy, xx = np.mgrid[0:h, 0:w]
    tl = alpha & (xx + yy < w - 1)
    br = alpha & (xx + yy > w - 1)
    tl_l = L[tl].mean() if tl.any() else float("nan")
    br_l = L[br].mean() if br.any() else float("nan")
    # hue families (12 bins) with their shade counts
    fam = {}
    for c in cols:
        hh, ll, ss = colorsys.rgb_to_hls(*[v / 255 for v in c])
        key = "grey" if ss < 0.12 else f"h{int(hh * 12) % 12:02d}"
        fam.setdefault(key, []).append(round(ll, 2))
    return dict(
        file=os.path.basename(path), size=f"{w}x{h}", coverage=round(n / (w * h), 2),
        colours=len(cols), lmin=round(L[alpha].min(), 2), lmax=round(L[alpha].max(), 2),
        edge_l=round(edge_l, 2), interior_l=round(int_l, 2),
        tl_minus_br=round(tl_l - br_l, 2),
        ramps={k: len(v) for k, v in sorted(fam.items())},
    )


def main():
    files = []
    for arg in sys.argv[1:]:
        if os.path.isdir(arg):
            files += sorted(os.path.join(arg, f) for f in os.listdir(arg) if f.endswith(".png"))
        else:
            files.append(arg)
    rows = [r for r in (measure(f) for f in files) if r]
    for r in rows:
        print(r)
    if len(rows) > 1:
        keys = ["coverage", "colours", "lmin", "lmax", "edge_l", "interior_l", "tl_minus_br"]
        avg = {k: round(float(np.nanmean([r[k] for r in rows])), 2) for k in keys}
        print("AVERAGE", avg)


if __name__ == "__main__":
    main()
