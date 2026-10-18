#!/usr/bin/env python3
"""Deterministic generator for the temporary body stand-in art.

GODOT_FRONT_VIEW_CHARACTER_POC_01 — stage A.

Every file written into assets/temporary-body/ by this script is a
TEMPORARY PROTOTYPE PLACEHOLDER — NOT APPROVED CHARACTER ART.

There is no approved Tahmures body, arm, or hand artwork. The pointing
beat needs visible stand-ins, so this script draws simple flat vector
shapes (capsules, ellipses, one polygon) with deterministic math only:

- no random numbers;
- no image input;
- no AI/local image generation;
- no modification of the approved head package;
- pure Python standard library (struct, zlib, math).

Re-running this script always produces byte-identical PNGs, so the
placeholder art can be re-verified against the hashes recorded in
manifest.json.

Colors are flat design constants. The skin tone (248, 179, 116) was
sampled from the approved head_base artwork (cheek patch average) so
the placeholder hand does not clash with the approved face palette;
sampling a color is not extracting or deriving character art.

Output files (relative to this script's parent directory):
  ../assets/temporary-body/torso.png        280 x 340, pivot top-centre
  ../assets/temporary-body/upper_arm.png     40 x  95, pivot top-centre
  ../assets/temporary-body/forearm.png       34 x  85, pivot top-centre
  ../assets/temporary-body/hand_point.png    36 x  66, pivot (18, 8)
  ../assets/temporary-body/point_target.png  48 x  48, pivot centre
  ../assets/temporary-body/placeholders.json sizes, pivots, sha256
"""

import argparse
import hashlib
import json
import math
import os
import struct
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUT_DIR = os.path.join(HERE, "..", "assets", "temporary-body")

# Flat palette (design constants, see module docstring).
ROBE = (63, 74, 99)
ROBE_DARK = (44, 52, 71)
SLEEVE = (58, 68, 92)
SKIN = (248, 179, 116)
GOLD = (232, 184, 75)

SS = 4  # supersampling factor for anti-aliased edges


def write_png(path, width, height, rgba):
    raw = b"".join(
        b"\x00" + bytes(rgba[y * width * 4:(y + 1) * width * 4])
        for y in range(height)
    )

    def chunk(tag, data):
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(png)


def render(width, height, shape_fn):
    """Anti-aliased flat render: shape_fn(x, y) -> (r, g, b) or None."""
    rgba = bytearray(width * height * 4)
    step = 1.0 / SS
    for y in range(height):
        for x in range(width):
            r = g = b = n = 0
            for sy in range(SS):
                yy = y + (sy + 0.5) * step
                for sx in range(SS):
                    colour = shape_fn(x + (sx + 0.5) * step, yy)
                    if colour is not None:
                        r += colour[0]
                        g += colour[1]
                        b += colour[2]
                        n += 1
            if n:
                base = (y * width + x) * 4
                rgba[base + 0] = int(round(r / n))
                rgba[base + 1] = int(round(g / n))
                rgba[base + 2] = int(round(b / n))
                rgba[base + 3] = int(round(255 * n / (SS * SS)))
    return rgba


def capsule(x, y, x0, y0, x1, y1, radius):
    """True when (x, y) is inside a capsule around segment p0->p1."""
    dx, dy = x1 - x0, y1 - y0
    length_sq = dx * dx + dy * dy
    if length_sq == 0.0:
        t = 0.0
    else:
        t = max(0.0, min(1.0, ((x - x0) * dx + (y - y0) * dy) / length_sq))
    px, py = x0 + t * dx, y0 + t * dy
    return (x - px) ** 2 + (y - py) ** 2 <= radius * radius


def ellipse(x, y, cx, cy, rx, ry):
    return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0


def point_in_polygon(x, y, vertices):
    inside = False
    j = len(vertices) - 1
    for i in range(len(vertices)):
        xi, yi = vertices[i]
        xj, yj = vertices[j]
        if (yi > y) != (yj > y):
            cross = (xj - xi) * (y - yi) / (yj - yi) + xi
            if x < cross:
                inside = not inside
        j = i
    return inside


# --- torso (280 x 340): neck stub + robe, pivot at top-centre (140, 0) ---
ROBE_POLYGON = [
    (14.0, 340.0), (6.0, 250.0), (0.0, 140.0), (6.0, 96.0), (24.0, 68.0),
    (60.0, 60.0), (220.0, 60.0), (256.0, 68.0), (274.0, 96.0), (280.0, 140.0),
    (274.0, 250.0), (266.0, 340.0),
]


def torso_shape(x, y):
    if point_in_polygon(x, y, ROBE_POLYGON):
        if 60.0 <= y <= 78.0:
            return ROBE_DARK  # shoulder trim band
        if abs(x - 140.0) <= 2.0 and 90.0 <= y <= 330.0:
            return ROBE_DARK  # centre fold line
        return ROBE
    if 126.0 <= x <= 154.0 and 0.0 <= y <= 90.0:
        return SKIN  # neck stub, hidden behind the approved beard
    return None


# --- upper arm (40 x 95): sleeve capsule, pivot top-centre (20, 0) ---
def upper_arm_shape(x, y):
    if capsule(x, y, 20.0, 20.0, 20.0, 75.0, 20.0):
        return SLEEVE
    return None


# --- forearm (34 x 85): sleeve capsule with cuff band, pivot (17, 0) ---
def forearm_shape(x, y):
    if capsule(x, y, 17.0, 17.0, 17.0, 68.0, 17.0):
        if 56.0 <= y <= 64.0:
            return ROBE_DARK  # cuff band
        return SLEEVE
    return None


# --- hand (36 x 66): pointing mitten, pivot (wrist) at (18, 8) ---
def hand_shape(x, y):
    if ellipse(x, y, 18.0, 26.0, 13.0, 16.0):
        return SKIN  # palm
    if capsule(x, y, 18.0, 34.0, 18.0, 54.0, 5.0):
        return SKIN  # extended index finger
    if capsule(x, y, 9.0, 32.0, 9.0, 46.0, 5.0):
        return SKIN  # folded fingers
    if ellipse(x, y, 29.0, 20.0, 5.0, 5.0):
        return SKIN  # thumb
    return None


# --- point target (48 x 48): ring + dot scene prop, pivot centre ---
def target_shape(x, y):
    d = math.hypot(x - 24.0, y - 24.0)
    if 13.0 <= d <= 20.0:
        return GOLD  # ring
    if d <= 4.0:
        return GOLD  # centre dot
    return None


SPECS = [
    ("torso.png", 280, 340, (140, 0), torso_shape),
    ("upper_arm.png", 40, 95, (20, 0), upper_arm_shape),
    ("forearm.png", 34, 85, (17, 0), forearm_shape),
    ("hand_point.png", 36, 66, (18, 8), hand_shape),
    ("point_target.png", 48, 48, (24, 24), target_shape),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        default=DEFAULT_OUT_DIR,
        help="output directory (default: the project assets/temporary-body)",
    )
    args = parser.parse_args()
    out_dir = os.path.abspath(args.out)
    os.makedirs(out_dir, exist_ok=True)
    records = []
    for name, width, height, pivot, shape_fn in SPECS:
        rgba = render(width, height, shape_fn)
        path = os.path.join(out_dir, name)
        write_png(path, width, height, rgba)
        digest = hashlib.sha256(open(path, "rb").read()).hexdigest()
        records.append(
            {
                "file": name,
                "size": [width, height],
                "pivot": list(pivot),
                "sha256": digest,
            }
        )
        print(f"{name:20s} {width}x{height} pivot={pivot} sha256={digest}")
    index = {
        "generator": "scripts/generate_temporary_body.py",
        "note": "TEMPORARY PROTOTYPE PLACEHOLDER - NOT APPROVED CHARACTER ART",
        "deterministic": True,
        "inputs": "none (flat vector shapes drawn by deterministic math)",
        "assets": records,
    }
    index_path = os.path.join(out_dir, "placeholders.json")
    with open(index_path, "w") as fh:
        json.dump(index, fh, indent=2)
        fh.write("\n")
    print(f"placeholders.json written with {len(records)} assets to {out_dir}")


if __name__ == "__main__":
    main()
