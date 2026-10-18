#!/usr/bin/env python3
"""Layout01 v3 repair — analysis stage 7: trace the mouth patch geometry precisely.

Outputs the exact footprint data used by the build:
- skin oval mask (warm-skin pixels in the mouth box)
- lip line curve (near-black pixels)
- interior dark region below the line
- proposed M (mouth content) and P (patch footprint = M + 3px margin)
"""
import numpy as np
from PIL import Image

REPO = "/home/mehdi/Project/leela/tahmures"
V2 = REPO + "/Characters/tahmures/versions/layout01-v2"
MASTER = V2 + "/source/approved_master.png"

BOX = (495, 224, 586, 274)  # x0, y0, x1, y1 analysis box


def is_skin(px):
    r, g, b, a = int(px[0]), int(px[1]), int(px[2]), int(px[3])
    return a > 0 and r >= 190 and g >= 120 and b <= 165 and r - b >= 60 and g < r


def is_dark(px):
    r, g, b, a = int(px[0]), int(px[1]), int(px[2]), int(px[3])
    return a > 0 and r < 90 and g < 75 and b < 70


def is_black_line(px):
    r, g, b, a = int(px[0]), int(px[1]), int(px[2]), int(px[3])
    return a > 0 and r < 45 and g < 40 and b < 40


def main():
    m = np.asarray(Image.open(MASTER).convert("RGBA"))
    x0, y0, x1, y1 = BOX

    print("=== mouth box map: s=skin #=dark @=blackline .=other, x%d..%d y%d..%d ===" % BOX)
    for y in range(y0, y1):
        row = []
        for x in range(x0, x1):
            px = m[y, x]
            if is_black_line(px):
                row.append("@")
            elif is_skin(px):
                row.append("s")
            elif is_dark(px):
                row.append("#")
            else:
                row.append(".")
        print("%4d %s" % (y, "".join(row)))

    # lip line trace: for each x find black pixels y in 246..256
    print("\n=== lip line y-extents per x (black pixels in y 244..258) ===")
    for x in range(522, 562):
        ys = [y for y in range(244, 259) if is_black_line(m[y, x])]
        print("  x=%d: %s" % (x, ys))

    # v2 neutral_mouth alpha in the box
    nm = np.asarray(Image.open(V2 + "/mouths/neutral_mouth.png").convert("RGBA"))
    print("\n=== v2 neutral_mouth alpha (X=alpha>0) in box ===")
    for y in range(y0, y1):
        row = "".join("X" if nm[y, x, 3] > 0 else "." for x in range(x0, x1))
        print("%4d %s" % (y, row))


if __name__ == "__main__":
    main()
