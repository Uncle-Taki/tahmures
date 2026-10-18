#!/usr/bin/env python3
"""Layout01 v3 repair — analysis stage 5: domain definition and gap ownership."""
import numpy as np
from PIL import Image
from collections import Counter

REPO = "/home/mehdi/Project/leela/tahmures"
V2 = REPO + "/Characters/tahmures/versions/layout01-v2"
MASTER = V2 + "/source/approved_master.png"


def top_colors(a, sel, n=5):
    c = Counter()
    idx = np.nonzero(sel)
    for y, x in zip(idx[0], idx[1]):
        r, g, b, al = a[y, x]
        c[(int(r) // 16 * 16, int(g) // 16 * 16, int(b) // 16 * 16)] += 1
    return c.most_common(n)


def main():
    m = np.asarray(Image.open(MASTER).convert("RGBA"))
    mal = m[..., 3]
    dom = np.asarray(Image.open(V2 + "/masks/visible_head_domain.png").convert("L"))

    print("=== domain vs master alpha ===")
    for t in (1, 64, 127, 128, 250):
        d = dom >= 127
        print("master alpha >= %3d inside domain: %d; outside domain: %d" % (
            t, int((d & (mal >= t)).sum()), int((~d & (mal >= t)).sum())))
    print("domain true total:", int((dom >= 127).sum()))
    print("master alpha==0 inside domain:", int((dom >= 127 & (mal == 0)).sum()) if False else int(((dom >= 127) & (mal == 0)).sum()))

    # compose v2 puppet_core (with neutral_mouth as v2 did) for gap analysis
    order = [
        "head/hair_back.png", "head/head_base.png", "face/ear_right.png", "face/ear_left.png",
        "face/beard.png", "face/nose.png", "face/eye_right.png", "face/eye_left.png",
        "face/eyebrow_right.png", "face/eyebrow_left.png", "face/moustache.png",
        "mouths/neutral_mouth.png", "head/diadem_gold.png",
    ]
    comp = Image.new("RGBA", (1086, 1448), (0, 0, 0, 0))
    for p in order:
        comp = Image.alpha_composite(comp, Image.open(V2 + "/" + p).convert("RGBA"))
    ca = np.asarray(comp)
    cal = ca[..., 3]

    d = dom >= 127
    er = d.copy()
    er[1:, :] &= d[:-1, :]; er[:-1, :] &= d[1:, :]; er[:, 1:] &= d[:, :-1]; er[:, :-1] &= d[:, 1:]

    miss = er & (cal == 0)
    print("\n=== master top colors in each missing band (eroded domain, comp alpha==0) ===")
    bands = [
        ("hair-top", 500, 570, 14, 22),
        ("diadem/forehead L", 436, 500, 80, 124),
        ("diadem/forehead C", 500, 570, 80, 124),
        ("diadem/forehead R", 570, 646, 80, 124),
        ("hair-side R upper", 660, 690, 170, 280),
        ("hair/ear side L", 615, 630, 210, 240),
        ("neck L", 460, 500, 290, 370),
        ("neck C", 500, 590, 300, 370),
        ("neck R", 590, 680, 290, 370),
        ("chin tip", 520, 560, 368, 375),
    ]
    for name, x0, x1, y0, y1 in bands:
        sel = np.zeros_like(miss)
        sel[y0:y1, x0:x1] = True
        sel &= miss
        cnt = int(sel.sum())
        tc = top_colors(m, sel)
        print("%-20s %5d px  master colors: %s" % (name, cnt, tc))

    # what does the composed image have vs master at cheek cut columns?
    print("\n=== cheek cut inspection: v2 comp vs master, x=458..470, y=230..260 ===")
    for y in range(230, 261, 3):
        line = []
        for x in range(458, 471):
            cr, cg, cb, ca_ = ca[y, x]
            mr, mg, mb, ma_ = m[y, x]
            line.append("x%d c(%3d,%3d,%3d,%3d) m(%3d,%3d,%3d,%3d)" % (x, cr, cg, cb, ca_, mr, mg, mb, ma_))
        print("y=%d %s" % (y, " | ".join(line[:4])))
        print("     %s" % " | ".join(line[4:8]))
        print("     %s" % " | ".join(line[8:]))

    # hair_back alpha in right-side band vs master
    hb = np.asarray(Image.open(V2 + "/head/hair_back.png").convert("RGBA"))
    print("\n=== hair_back alpha vs master alpha, x=655..690 ===")
    for y in range(200, 290, 10):
        row = []
        for x in range(655, 690, 5):
            row.append("x%d hb=%3d m=%3d dom=%d" % (x, hb[y, x, 3], m[y, x, 3], 1 if dom[y, x] >= 127 else 0))
        print("y=%d %s" % (y, " ; ".join(row)))

    # vertical profile of master colors at neck center
    print("\n=== master color vertical profile x=540, y=300..380 ===")
    for y in range(300, 381, 4):
        r, g, b, al = m[y, 540]
        print("  y=%3d (%3d,%3d,%3d,%3d) comp_alpha=%3d" % (y, r, g, b, al, cal[y, 540]))

    # what does head_base look like at its edges
    hbrg = np.asarray(Image.open(V2 + "/head/head_base.png").convert("RGBA"))
    print("\n=== head_base alpha edge profile, y=250, x=460..475 and x=610..622 ===")
    for x in list(range(460, 476)) + list(range(610, 623)):
        print("  x=%3d hb_alpha=%3d master=(%3d,%3d,%3d,%3d)" % (x, hbrg[250, x, 3], *m[250, x]))


if __name__ == "__main__":
    main()
