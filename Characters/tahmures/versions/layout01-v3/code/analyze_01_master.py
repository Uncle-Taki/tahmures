#!/usr/bin/env python3
"""Layout01 v3 repair — analysis stage 1: master image structure.

Read-only analysis of the approved master and v2 baseline components.
Writes textual findings to stdout; no source files are modified.
"""
import sys
import numpy as np
from PIL import Image

REPO = "/home/mehdi/Project/leela/tahmures"
V2 = REPO + "/Characters/tahmures/versions/layout01-v2"
MASTER = V2 + "/source/approved_master.png"


def load(path):
    return Image.open(path).convert("RGBA")


def ascii_render(img, box, cols=96, mode="lum"):
    """Render a crop as ASCII (lum) or as mask (#)."""
    crop = img.crop(box)
    w, h = crop.size
    rows = max(1, int(cols * h / w * 0.5))
    small = crop.resize((cols, rows))
    a = np.asarray(small)
    out = []
    if mode == "lum":
        lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]) * (a[..., 3] / 255.0)
        ramp = " .:-=+*#%@"
        for r in lum:
            out.append("".join(ramp[min(9, int(v / 25.6))] for v in r))
    else:
        for r in a[..., 3]:
            out.append("".join("#" if v > 127 else "." for v in r))
    return "\n".join(out)


def color_clusters(a, mask, n=8):
    """Simple: round colors and count the most common in mask."""
    px = a[mask]
    if len(px) == 0:
        return []
    # quantize to 16-step bins
    q = (px[:, :3] // 16 * 16)
    uniq, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
    order = np.argsort(-counts)[:n]
    return [(tuple(int(x) for x in uniq[i]), int(counts[i])) for i in order]


def main():
    m = load(MASTER)
    a = np.asarray(m)
    print("master size:", m.size, "mode:", m.mode)
    alpha = a[..., 3]
    print("alpha stats: min %d max %d, opaque(>=250): %d, partial(1..249): %d, zero: %d" % (
        alpha.min(), alpha.max(), int((alpha >= 250).sum()), int(((alpha > 0) & (alpha < 250)).sum()),
        int((alpha == 0).sum())))
    ys, xs = np.nonzero(alpha)
    print("nonzero-alpha bbox: x %d..%d y %d..%d" % (xs.min(), xs.max(), ys.min(), ys.max()))

    # head domain mask
    dom = np.asarray(Image.open(V2 + "/masks/visible_head_domain.png").convert("L"))
    print("visible_head_domain: unique", np.unique(dom), "count>=127:", int((dom >= 127).sum()))

    # ASCII of the full head area at low res (lum)
    print("\n=== master luminance, head area (x 350..730, y 0..420) ===")
    print(ascii_render(m, (350, 0, 730, 420), cols=96))

    # ASCII alpha of same
    print("\n=== master alpha, head area ===")
    print(ascii_render(m, (350, 0, 730, 420), cols=96, mode="mask"))

    # mouth region detailed ASCII at near-full resolution
    print("\n=== mouth region (x 470..610, y 200..290) luminance, ~2px/col ===")
    print(ascii_render(m, (470, 200, 610, 290), cols=70))

    print("\n=== mouth region tight (x 495..585, y 220..275) luminance ===")
    print(ascii_render(m, (495, 220, 585, 275), cols=90))

    # palette clusters in head domain
    print("\n=== color clusters in visible head domain ===")
    for c, n in color_clusters(a, dom >= 127, n=12):
        print("  rgb%-18s %d" % (str(c), n))

    # skin region palette: sample cheeks (x 480..530, y 160..200)
    print("\n=== color clusters: left cheek sample (x 480..530 y 160..200) ===")
    box = (slice(160, 200), slice(480, 530))
    sub = a[box]
    for c, n in color_clusters(sub, sub[..., 3] > 200, n=6):
        print("  rgb%-18s %d" % (str(c), n))

    # beard palette sample
    print("\n=== color clusters: beard mass sample (x 500..580, y 280..320) ===")
    sub = a[280:320, 500:580]
    for c, n in color_clusters(sub, sub[..., 3] > 200, n=6):
        print("  rgb%-18s %d" % (str(c), n))


if __name__ == "__main__":
    main()
