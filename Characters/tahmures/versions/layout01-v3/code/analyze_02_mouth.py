#!/usr/bin/env python3
"""Layout01 v3 repair — analysis stage 2: color-class probing of the mouth region.

Classifies master pixels into palette classes and prints scanline maps so the
actual mouth / moustache / beard geometry can be traced without subjective
colour guessing. Read-only.
"""
import numpy as np
from PIL import Image

REPO = "/home/mehdi/Project/leela/tahmures"
V2 = REPO + "/Characters/tahmures/versions/layout01-v2"
MASTER = V2 + "/source/approved_master.png"

# palette classes
SKIN = "S"      # warm skin
SKIN_D = "s"    # darker skin shade
GOLD = "G"
GOLD_D = "g"
WHITE = "W"     # near white (eye whites, highlights)
DARK = "#"      # beard/hair dark brown-black
INK = "@"       # pure black line
EMPTY = "."     # transparent
OTHER = "?"


def classify(px):
    r, g, b, a = int(px[0]), int(px[1]), int(px[2]), int(px[3])
    if a < 8:
        return EMPTY
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    if r > 215 and g > 215 and b > 215:
        return WHITE
    if abs(r - 32) <= 14 and abs(g - 32) <= 20 and b < 64 and r < 64:
        return DARK
    if r < 40 and g < 40 and b < 40:
        return INK
    if r > 180 and 120 <= g <= 200 and b <= 150 and r - b > 60:
        return GOLD if lum > 150 else "g"
    if r > 215 and 140 <= g <= 200 and 70 <= b <= 145 and r - b > 70:
        return SKIN if lum > 160 else SKIN_D
    return OTHER


def region_map(a, x0, x1, y0, y1, step=1):
    out = []
    for y in range(y0, y1, step):
        row = "".join(classify(a[y, x]) for x in range(x0, x1, step))
        out.append("%4d %s" % (y, row))
    header = "     " + "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(x0, x1, step))
    return header + "\n" + "\n".join(out)


def main():
    m = Image.open(MASTER).convert("RGBA")
    a = np.asarray(m)

    print("=== class map: mouth region x 480..610, y 205..290 (1px) ===")
    print(region_map(a, 480, 610, 205, 290))

    print("\n=== class map: wider lower face x 440..650, y 200..380 (2px) ===")
    print(region_map(a, 440, 650, 200, 380, step=2))

    # vertical scan through mouth anchor x=540
    print("\n=== vertical scan x=536..545 (majority class), y 190..300 ===")
    for y in range(190, 300):
        votes = {}
        for x in range(536, 546):
            c = classify(a[y, x])
            votes[c] = votes.get(c, 0) + 1
        top = sorted(votes.items(), key=lambda kv: -kv[1])[:3]
        print("%4d %s" % (y, top))

    # horizontal scan through y=241 (mouth anchor)
    print("\n=== horizontal scan y=238..246 (majority class per x), x 480..610 ===")
    for y in range(238, 247):
        votes = {}
        for x in range(480, 610):
            c = classify(a[y, x])
            votes[c] = votes.get(c, 0) + 1
        top = sorted(votes.items(), key=lambda kv: -kv[1])[:4]
        print("%4d %s" % (y, top))


if __name__ == "__main__":
    main()
