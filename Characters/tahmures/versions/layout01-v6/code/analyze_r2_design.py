#!/usr/bin/env python3
"""Design analysis for the v5 fixes.

A. Under-moustache surface: what should the face look like without the
   moustache? Examine the master's lip/skin surface just below the matte
   bottom per column, and the matte's blend/ink composition per row.

B. Neck: examine the master's hair strand structure around the left wedge
   (above y327, and the right-side attachment) to design a strand
   continuation. Also map where hair_back alpha covers the wedge.
"""
import numpy as np
from PIL import Image

from build_lib import V2, V4


def L(root, rel):
    return np.asarray(Image.open(root + "/" + rel).convert("RGBA")).copy()


m = L(V2, "source/approved_master.png")
mo_v2 = L(V2, "face/moustache.png")
hair = L(V2, "head/hair_back.png")
head_v2 = L(V2, "head/head_base.png")
U = np.load(V4 + "/code/_U.npy")
M = np.load(V4 + "/code/_M.npy")
P = np.load(V4 + "/code/_P.npy")

print("=== A. per-column matte bottom and the content below it ===")
print("x: yb (matte bottom) | master(yb) | master(yb+1) | master(yb+2) | class")
for x in range(490, 590, 4):
    col = np.nonzero(mo_v2[:, x, 3] > 0)[0]
    if not len(col):
        continue
    yb = int(col.max())
    below = [tuple(m[y, x, :3]) for y in (yb + 1, yb + 2, yb + 3)]
    b1 = m[yb + 1, x, :3]
    cls = ("LIP/SKIN" if b1[0] >= 140 else "BEARD/DARK" if b1[0] < 90 else "MID")
    print("x=%d yb=%d mo=%s below=%s %s" % (
        x, yb, tuple(m[yb, x, :3]), below, cls))

print()
print("=== A2. matte px composition: ink vs blend per row (centre x515-560) ===")
for y in range(209, 240):
    n_ink = n_blend = n_bright = 0
    for x in range(515, 561):
        if mo_v2[y, x, 3] > 0:
            r = m[y, x, 0]
            if r < 90:
                n_ink += 1
            elif r >= 140:
                n_bright += 1
            else:
                n_blend += 1
    print("y=%d ink=%d blend=%d bright=%d" % (y, n_ink, n_blend, n_bright))

print()
print("=== A3. master lip surface rows (centre) — the continuation source ===")
for y in range(228, 245):
    row = m[y, 528:557, :3]
    print("y=%d mean=%s" % (y, row.mean(axis=0).round(0)))

print()
print("=== B. master hair structure above the left neck wedge ===")
for y in range(300, 332, 2):
    print("y=%d:" % y, [tuple(m[y, x, :3]) for x in range(458, 496, 4)])

print()
print("=== B2. hair_back alpha coverage over the wedge ===")
for y in range(320, 372, 4):
    xs = [x for x in range(455, 500) if hair[y, x, 3] > 0]
    print("y=%d hair_back alpha>0 x: %s" % (y, ("%d..%d" % (min(xs), max(xs))) if xs else "none"))

print()
print("=== B3. right-side attachment (x582-610) master content ===")
for y in range(326, 370, 6):
    print("y=%d:" % y, [tuple(m[y, x, :3]) for x in range(580, 612, 4)])

print()
print("=== B4. neck skin vs hair edge: master rows y350-368, x460-520 ===")
for y in range(350, 370, 4):
    seg = []
    for x in range(460, 520, 4):
        px = m[y, x, :3]
        seg.append("S" if px[0] >= 140 else ("H" if px[2] > px[0] else "d"))
    print("y=%d %s" % (y, "".join(seg)))

print()
print("=== B5. v2 head_base alpha over the wedge (what head owns there) ===")
for y in range(326, 366, 4):
    xs = [x for x in range(460, 500) if head_v2[y, x, 3] > 0]
    print("y=%d head_base alpha>0: %s" % (y, ("%d..%d" % (min(xs), max(xs))) if xs else "none"))
