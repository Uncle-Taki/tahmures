#!/usr/bin/env python3
"""R2-01 analysis: locate the detached dark stroke in v4 state A.

State A = hair, head, ears, beard (receiver), features, moustache, diadem —
no patch. Codex reports a rising black smile-like stroke and broken side
marks at approx x520-544, y228-239 over the beard receiver.
"""
import numpy as np
from PIL import Image

from build_lib import V2, V4, compose


def L(root, rel):
    return np.asarray(Image.open(root + "/" + rel).convert("RGBA")).copy()


m = L(V2, "source/approved_master.png")
A = L(V4, "previews/mouthless.png")
moust = L(V4, "face/moustache.png")
mo_v2 = L(V2, "face/moustache.png")

order = ["head/hair_back.png", "head/head_base.png", "face/ear_right.png",
         "face/ear_left.png", "face/beard.png", "face/nose.png",
         "face/eye_right.png", "face/eye_left.png",
         "face/eyebrow_right.png", "face/eyebrow_left.png",
         "head/diadem_gold.png"]
underA = np.asarray(compose([L(V4, p) for p in order]))

print("=== state A: dark px per row, x500-570 ===")
for y in range(222, 248):
    xs = [x for x in range(500, 570)
          if A[y, x, 3] > 0 and A[y, x, 0] < 90 and A[y, x, 1] < 75 and A[y, x, 2] < 70]
    print("y=%d: %d dark px%s" % (y, len(xs), ("  x=%d..%d" % (min(xs), max(xs))) if xs else ""))

print()
print("=== attribution grid x515-549 (M=mo-dark m=mo U=under-dark .=under) ===")
for y in range(224, 242):
    line = []
    for x in range(515, 550):
        ma = moust[y, x, 3]
        mr = moust[y, x, :3]
        u = underA[y, x, :3]
        if ma > 0 and mr[0] < 90 and mr[1] < 75 and mr[2] < 70:
            line.append("M")
        elif ma > 0:
            line.append("m")
        elif u[0] < 90 and u[1] < 75 and u[2] < 70:
            line.append("U")
        else:
            line.append(".")
    print("y=%d %s" % (y, "".join(line)))

print()
print("=== where do dark A px come from? (x510-556, y226-240) ===")
n_mo = n_un = 0
for y in range(226, 241):
    for x in range(510, 556):
        a = A[y, x]
        if a[3] > 0 and a[0] < 90 and a[1] < 75 and a[2] < 70:
            if moust[y, x, 3] > 0:
                n_mo += 1
            else:
                n_un += 1
print("dark px from moustache sprite:", n_mo, " from underlay:", n_un)

print()
print("=== moustache sprite dark px below y226 (the suspected notch ink) ===")
ys, xs = np.nonzero((moust[..., 3] > 0) & (moust[..., 0] < 90)
                    & (moust[..., 1] < 75) & (moust[..., 2] < 70))
sel = ys >= 226
print("count:", int(sel.sum()), "bbox:",
      (xs[sel].min(), ys[sel].min(), xs[sel].max(), ys[sel].max()) if sel.any() else None)
for y in range(224, 242):
    c = int(((moust[:, :, 3] > 0) & (moust[:, :, 0] < 90)
             & (moust[:, :, 1] < 75) & (moust[:, :, 2] < 70))[y, 505:570].sum())
    print("  y=%d moustache dark px (x505-570): %d" % (y, c))

print()
print("=== master: true content at the suspect zone ===")
for y in range(228, 242):
    print("y=%d master x536-544:" % y, [tuple(m[y, x, :3]) for x in range(536, 545, 2)])

print()
print("=== v2 moustache matte bottom profile ===")
for x in range(505, 580, 5):
    col = np.nonzero(mo_v2[:, x, 3] > 0)[0]
    if len(col):
        lows = [int(y) for y in col if y >= 224]
        print("x=%d: bottom rows >=224: %s" % (x, lows))
