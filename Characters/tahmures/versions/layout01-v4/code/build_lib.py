#!/usr/bin/env python3
"""Layout01 v4 repair — shared build helpers.

All construction is derived from the immutable v2 baseline (master + v2
sprites) and the accepted v3 work. v3 files are only ever READ; every v4
output is written under versions/layout01-v4/.
"""
import numpy as np
from PIL import Image

REPO = "/home/mehdi/Project/leela/tahmures"
V2 = REPO + "/Characters/tahmures/versions/layout01-v2"
V3 = REPO + "/Characters/tahmures/versions/layout01-v3"
V4 = REPO + "/Characters/tahmures/versions/layout01-v4"
MASTER = V2 + "/source/approved_master.png"
CANVAS = (1086, 1448)

REF_SKIN = np.array([247, 176, 112], dtype=np.int32)
REF_GOLD = np.array([200, 135, 55], dtype=np.int32)
REF_DARK = np.array([45, 32, 27], dtype=np.int32)
REF_BLACK = np.array([6, 4, 4], dtype=np.int32)


def load_master():
    return np.asarray(Image.open(MASTER).convert("RGBA")).copy()


def load_v2(rel):
    return np.asarray(Image.open(V2 + "/" + rel).convert("RGBA")).copy()


def load_v3(rel):
    return np.asarray(Image.open(V3 + "/" + rel).convert("RGBA")).copy()


def load_domain():
    return np.asarray(Image.open(V2 + "/masks/visible_head_domain.png").convert("L")) >= 127


def save_rgba(arr, path):
    Image.fromarray(arr, "RGBA").save(path)


def save_mask_L(alpha, path):
    Image.fromarray(alpha.astype(np.uint8), "L").save(path)


def save_binary(mask, path):
    Image.fromarray(np.where(mask, 255, 0).astype(np.uint8), "L").save(path)


def dilate(mask, iterations):
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
    d = {
        "skin": int(np.abs(rgb - REF_SKIN).sum()),
        "gold": int(np.abs(rgb - REF_GOLD).sum()),
        "dark": int(np.abs(rgb - REF_DARK).sum()),
        "black": int(np.abs(rgb - REF_BLACK).sum()),
    }
    return min(d, key=d.get)


def compose(layers):
    """Alpha-composite a list of RGBA numpy arrays (bottom first) via PIL."""
    out = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    for layer in layers:
        out = Image.alpha_composite(out, Image.fromarray(layer, "RGBA"))
    return out


def alpha_bbox(alpha):
    ys, xs = np.nonzero(alpha > 0)
    if len(ys) == 0:
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]


def shifted(arr, dx, dy):
    out = np.zeros_like(arr)
    h, w = arr.shape[:2]
    x0s, x1s = max(0, dx), min(w, w + dx)
    y0s, y1s = max(0, dy), min(h, h + dy)
    if x0s < x1s and y0s < y1s:
        out[y0s:y1s, x0s:x1s] = arr[y0s - dy:y1s - dy, x0s - dx:x1s - dx]
    return out


def diffuse(region, seed_rgb, iterations=4000):
    """Laplacian diffusion of RGB values into `region` from `seed_rgb`.

    seed_rgb: float array (h,w,3) with valid values on non-region pixels
    (region pixels are ignored as seeds). Returns uint8 RGB for the whole
    canvas with region pixels filled by diffusion. Runs on a cropped box
    around the region for speed.
    """
    ys, xs = np.nonzero(region)
    if len(ys) == 0:
        return np.clip(np.round(seed_rgb), 0, 255).astype(np.uint8)
    margin = 4
    y0 = max(0, ys.min() - margin)
    y1 = min(region.shape[0], ys.max() + 1 + margin)
    x0 = max(0, xs.min() - margin)
    x1 = min(region.shape[1], xs.max() + 1 + margin)
    f = region[y0:y1, x0:x1]
    val = seed_rgb[y0:y1, x0:x1].astype(np.float32).copy()
    seed_vals = val[~f]
    val[f] = seed_vals.mean(axis=0) if len(seed_vals) else 128.0
    for _ in range(iterations):
        nv = val.copy()
        nv[1:, :] = (val[1:, :] + val[:-1, :]) / 2
        nv[:-1, :] = (val[:-1, :] + val[1:, :]) / 2
        nv[:, 1:] = (val[:, 1:] + val[:, :-1]) / 2
        nv[:, :-1] = (val[:, :-1] + val[:, 1:]) / 2
        val = np.where(f[..., None], nv, val)
    out = np.clip(np.round(seed_rgb), 0, 255).astype(np.uint8)
    out[y0:y1, x0:x1][f] = np.clip(np.round(val[f]), 0, 255).astype(np.uint8)
    return out
