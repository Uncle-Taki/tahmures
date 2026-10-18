#!/usr/bin/env python3
"""Layout01 v3 repair — shared build helpers.

All construction is derived from the immutable v2 baseline and the approved
master. Source-pixel claims always use exact master RGB with alpha taken from
the master (extraction may only reduce alpha, and here it keeps it equal).
"""
import numpy as np
from PIL import Image

REPO = "/home/mehdi/Project/leela/tahmures"
V2 = REPO + "/Characters/tahmures/versions/layout01-v2"
V3 = REPO + "/Characters/tahmures/versions/layout01-v3"
MASTER = V2 + "/source/approved_master.png"
CANVAS = (1086, 1448)

# Master-derived reference colours for ownership classification of previously
# uncovered pixels (quantised cluster centres from the analysis stage).
REF_SKIN = np.array([247, 176, 112], dtype=np.int32)
REF_GOLD = np.array([200, 135, 55], dtype=np.int32)
REF_DARK = np.array([45, 32, 27], dtype=np.int32)
REF_BLACK = np.array([6, 4, 4], dtype=np.int32)


def load_master():
    return np.asarray(Image.open(MASTER).convert("RGBA")).copy()


def load_v2(rel):
    return np.asarray(Image.open(V2 + "/" + rel).convert("RGBA")).copy()


def load_domain():
    return np.asarray(Image.open(V2 + "/masks/visible_head_domain.png").convert("L")) >= 127


def save_rgba(arr, path):
    Image.fromarray(arr, "RGBA").save(path)


def save_mask_L(alpha, path):
    Image.fromarray(alpha.astype(np.uint8), "L").save(path)


def save_binary(mask, path):
    Image.fromarray(np.where(mask, 255, 0).astype(np.uint8), "L").save(path)


def dilate(mask, iterations):
    """Binary dilation with a 3x3 structuring element."""
    out = mask.copy()
    for _ in range(iterations):
        m = out.copy()
        m[1:, :] |= out[:-1, :]
        m[:-1, :] |= out[1:, :]
        m[:, 1:] |= out[:, :-1]
        m[:, :-1] |= out[:, 1:]
        out = m
    return out


def erode(mask, iterations):
    """Binary erosion with a 3x3 structuring element."""
    out = mask.copy()
    for _ in range(iterations):
        m = out.copy()
        m[1:, :] &= out[:-1, :]
        m[:-1, :] &= out[1:, :]
        m[:, 1:] &= out[:, :-1]
        m[:, :-1] &= out[:, 1:]
        out = m
    return out


def nearest_class(rgb):
    """Return 'skin' | 'gold' | 'dark' | 'black' for an RGB triplet."""
    d = {
        "skin": int(np.abs(rgb - REF_SKIN).sum()),
        "gold": int(np.abs(rgb - REF_GOLD).sum()),
        "dark": int(np.abs(rgb - REF_DARK).sum()),
        "black": int(np.abs(rgb - REF_BLACK).sum()),
    }
    return min(d, key=d.get)


def compose(layers):
    """Alpha-composite a list of RGBA numpy arrays (bottom first)."""
    out = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    for layer in layers:
        out = Image.alpha_composite(out, Image.fromarray(layer, "RGBA"))
    return out


def alpha_bbox(alpha):
    """PIL-compatible alpha getbbox: (left, top, right, bottom), exclusive."""
    ys, xs = np.nonzero(alpha > 0)
    if len(ys) == 0:
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]


def shifted(arr, dx, dy):
    """Return a copy of a full-canvas RGBA array translated by (dx, dy)."""
    out = np.zeros_like(arr)
    h, w = arr.shape[:2]
    x0s, x1s = max(0, dx), min(w, w + dx)
    y0s, y1s = max(0, dy), min(h, h + dy)
    if x0s < x1s and y0s < y1s:
        out[y0s:y1s, x0s:x1s] = arr[y0s - dy:y1s - dy, x0s - dx:x1s - dx]
    return out
