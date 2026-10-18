#!/usr/bin/env python3
"""Layout01 v3 repair — analysis stage 3: exact RGB sampling of mouth geometry."""
import numpy as np
from PIL import Image
from collections import Counter

REPO = "/home/mehdi/Project/leela/tahmures"
V2 = REPO + "/Characters/tahmures/versions/layout01-v2"
MASTER = V2 + "/source/approved_master.png"


def top_colors(a, x0, x1, y0, y1, n=6):
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, al = a[y, x]
            if al < 8:
                continue
            c[(int(r), int(g), int(b))] += 1
    return c.most_common(n)


def main():
    a = np.asarray(Image.open(MASTER).convert("RGBA"))

    regions = [
        ("philtrum skin (x535-555, y236-246)", 535, 555, 236, 246),
        ("upper-lip skin band left (x508-526, y240-250)", 508, 526, 240, 250),
        ("upper-lip skin band right (x556-574, y240-250)", 556, 574, 240, 250),
        ("black mouth line row y251-253 (x525-560)", 525, 560, 251, 253),
        ("mouth interior (x532-550, y253-261)", 532, 550, 253, 261),
        ("below mouth (x530-552, y262-268)", 530, 552, 262, 268),
        ("beard below mouth (x500-580, y270-300)", 500, 580, 270, 300),
        ("moustache body (x510-570, y222-234)", 510, 570, 222, 234),
        ("moustache left tip (x486-505, y228-238)", 486, 505, 228, 238),
        ("cheek skin left of mouth (x490-505, y238-250)", 490, 505, 238, 250),
        ("skin right of mouth (x576-592, y238-250)", 576, 592, 238, 250),
        ("nose tip (x540-552, y210-220)", 540, 552, 210, 220),
        ("chin area inside beard? (x525-555, y262-266)", 525, 555, 262, 266),
        ("gold diadem band (x480-540, y60-80)", 480, 540, 60, 80),
    ]
    for name, x0, x1, y0, y1 in regions:
        print("== %s" % name)
        for col, cnt in top_colors(a, x0, x1, y0, y1):
            print("   rgb(%3d,%3d,%3d) x%d" % (col[0], col[1], col[2], cnt))
        print()

    # exact rows printed as hex triplets for the vertical strip through mouth
    print("=== vertical strip x=540 (r,g,b,a) y=228..272 ===")
    for y in range(228, 273):
        r, g, b, al = a[y, 540]
        print("  y=%3d  (%3d,%3d,%3d,%3d)" % (y, r, g, b, al))

    print("=== horizontal strip y=242 x=500..580 ===")
    for x in range(500, 581, 2):
        r, g, b, al = a[242, x]
        print("  x=%3d  (%3d,%3d,%3d,%3d)" % (x, r, g, b, al))

    print("=== horizontal strip y=256 x=500..580 ===")
    for x in range(500, 581, 2):
        r, g, b, al = a[256, x]
        print("  x=%3d  (%3d,%3d,%3d,%3d)" % (x, r, g, b, al))


if __name__ == "__main__":
    main()
