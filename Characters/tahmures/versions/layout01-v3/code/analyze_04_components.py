#!/usr/bin/env python3
"""Layout01 v3 repair — analysis stage 4: v2 component inventory and composition gaps."""
import numpy as np
from PIL import Image

REPO = "/home/mehdi/Project/leela/tahmures"
V2 = REPO + "/Characters/tahmures/versions/layout01-v2"
MASTER = V2 + "/source/approved_master.png"

SPRITES = [
    "head/head_base.png",
    "head/hair_back.png",
    "head/diadem_gold.png",
    "face/ear_left.png",
    "face/ear_right.png",
    "face/eye_left.png",
    "face/eye_right.png",
    "face/eyebrow_left.png",
    "face/eyebrow_right.png",
    "face/nose.png",
    "face/beard.png",
    "face/moustache.png",
    "mouths/neutral_mouth.png",
]


def alpha_stats(path):
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im)
    al = a[..., 3]
    nz = al > 0
    n = int(nz.sum())
    if n == 0:
        return im.size, 0, None
    ys, xs = np.nonzero(nz)
    return im.size, n, (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def main():
    m = np.asarray(Image.open(MASTER).convert("RGBA"))
    mal = m[..., 3]

    print("=== component alpha inventory ===")
    for p in SPRITES:
        size, n, bbox = alpha_stats(V2 + "/" + p)
        print("%-32s size=%s nonzero=%6d bbox=%s" % (p, size, n, bbox))

    # compose puppet_core in v2 order
    order = [
        "head/hair_back.png",
        "head/head_base.png",
        "face/ear_right.png",
        "face/ear_left.png",
        "face/beard.png",
        "face/nose.png",
        "face/eye_right.png",
        "face/eye_left.png",
        "face/eyebrow_right.png",
        "face/eyebrow_left.png",
        "face/moustache.png",
        "mouths/neutral_mouth.png",
        "head/diadem_gold.png",
    ]
    comp = Image.new("RGBA", (1086, 1448), (0, 0, 0, 0))
    for p in order:
        layer = Image.open(V2 + "/" + p).convert("RGBA")
        comp = Image.alpha_composite(comp, layer)
    ca = np.asarray(comp)
    cal = ca[..., 3]

    dom = np.asarray(Image.open(V2 + "/masks/visible_head_domain.png").convert("L")) >= 127

    # erode domain by 1px
    er = dom.copy()
    er[1:, :] &= dom[:-1, :]
    er[:-1, :] &= dom[1:, :]
    er[:, 1:] &= dom[:, :-1]
    er[:, :-1] &= dom[:, 1:]

    miss_full = dom & (cal == 0)
    miss_er = er & (cal == 0)
    deficit = er & (cal < 250) & (mal >= 250)
    print("\n=== v2 puppet_core+neutral_mouth composition vs domain ===")
    print("domain px: %d, eroded: %d" % (int(dom.sum()), int(er.sum())))
    print("fully transparent in domain: %d" % int(miss_full.sum()))
    print("fully transparent in eroded: %d" % int(miss_er.sum()))
    print("alpha<250 where master>=250 (eroded): %d" % int(deficit.sum()))

    # where are the missing pixels? print row ranges
    ys, xs = np.nonzero(miss_full)
    if len(ys):
        print("\nmissing-pixel row bands (y, count) every row with misses:")
        rows = np.unique(ys)
        # summarize into bands
        start = rows[0]
        prev = rows[0]
        for r in rows[1:]:
            if r != prev + 1:
                print("  y %d..%d" % (start, prev))
                start = r
            prev = r
        print("  y %d..%d" % (start, prev))
        # x extents per band
        print("\nx-extent of misses per 10-row band:")
        for y0 in range(0, 1448, 10):
            sel = miss_full[y0:y0 + 10]
            c = int(sel.sum())
            if c:
                yy, xx = np.nonzero(sel)
                print("  y %3d-%3d: %5d px, x %d..%d" % (y0, y0 + 9, c, xx.min(), xx.max()))

    # compare composed RGB to master where both opaque
    both = (cal >= 250) & (mal >= 250)
    diff = np.abs(ca[..., :3].astype(int) - m[..., :3].astype(int)).max(axis=2)
    print("\nRGB max-diff>3 where both opaque: %d of %d" % (int((diff[both] > 3).sum()), int(both.sum())))

    # what does beard.png look like in the mouth area — is the smile baked in?
    b = np.asarray(Image.open(V2 + "/face/beard.png").convert("RGBA"))
    print("\n=== beard.png in mouth region x500..580 y225..270 (alpha>200 as 'X') ===")
    for y in range(225, 270, 1):
        row = "".join("X" if b[y, x, 3] > 200 else ("x" if b[y, x, 3] > 0 else ".") for x in range(500, 580, 1))
        print("%4d %s" % (y, row))

    nm = np.asarray(Image.open(V2 + "/mouths/neutral_mouth.png").convert("RGBA"))
    print("\n=== neutral_mouth.png alpha x500..580 y225..270 ===")
    for y in range(225, 270, 1):
        row = "".join("X" if nm[y, x, 3] > 200 else ("x" if nm[y, x, 3] > 0 else ".") for x in range(500, 580, 1))
        print("%4d %s" % (y, row))

    ms = np.asarray(Image.open(V2 + "/face/moustache.png").convert("RGBA"))
    print("\n=== moustache.png alpha x480..600 y205..245 ===")
    for y in range(205, 245, 1):
        row = "".join("X" if ms[y, x, 3] > 200 else ("x" if ms[y, x, 3] > 0 else ".") for x in range(480, 600, 1))
        print("%4d %s" % (y, row))


if __name__ == "__main__":
    main()
