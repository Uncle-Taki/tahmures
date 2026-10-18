#!/usr/bin/env python3
"""Layout01 v3 repair — analysis stage 6: v2 sprite fidelity + neck region map."""
import numpy as np
from PIL import Image

REPO = "/home/mehdi/Project/leela/tahmures"
V2 = REPO + "/Characters/tahmures/versions/layout01-v2"
MASTER = V2 + "/source/approved_master.png"

SPRITES = [
    "head/hair_back.png", "head/head_base.png", "head/diadem_gold.png",
    "face/ear_left.png", "face/ear_right.png", "face/eye_left.png", "face/eye_right.png",
    "face/eyebrow_left.png", "face/eyebrow_right.png", "face/nose.png",
    "face/beard.png", "face/moustache.png", "mouths/neutral_mouth.png",
]


def main():
    m = np.asarray(Image.open(MASTER).convert("RGBA"))

    print("=== v2 sprite fidelity vs master (where sprite alpha>0) ===")
    for p in SPRITES:
        s = np.asarray(Image.open(V2 + "/" + p).convert("RGBA"))
        sal = s[..., 3]
        vis = sal > 0
        n = int(vis.sum())
        rgb_same = int((np.abs(s[..., :3].astype(int) - m[..., :3].astype(int)).max(axis=2)[vis] == 0).sum())
        alpha_le = int((sal[vis] <= m[..., 3][vis]).sum())
        alpha_eq = int((sal[vis] == m[..., 3][vis]).sum())
        print("%-28s vis=%6d rgb_exact=%6d alpha<=master=%6d alpha==master=%6d" % (
            p, n, rgb_same, alpha_le, alpha_eq))

    # neck region class map
    def warm(px):
        r, g, b, a = int(px[0]), int(px[1]), int(px[2]), int(px[3])
        if a < 8:
            return "."
        if r > 215 and g > 140 and 70 <= b <= 150 and r - b > 70:
            return "S"
        if r > 150 and 90 <= g <= 160 and b < 100 and r - b > 60:
            return "G"
        if r < 70 and g < 70 and b < 70:
            return "#"
        return "?"

    print("\n=== neck region map x430..700 (2px), y270..390 ===")
    for y in range(270, 390, 2):
        row = "".join(warm(m[y, x]) for x in range(430, 700, 2))
        print("%4d %s" % (y, row))

    # domain bbox
    dom = np.asarray(Image.open(V2 + "/masks/visible_head_domain.png").convert("L")) >= 127
    ys, xs = np.nonzero(dom)
    print("\ndomain bbox: x %d..%d y %d..%d" % (xs.min(), xs.max(), ys.min(), ys.max()))
    # master alpha profile below y374
    print("\nmaster alpha rows y370..400 at x=540:", [int(m[y, 540, 3]) for y in range(370, 401, 2)])


if __name__ == "__main__":
    main()
