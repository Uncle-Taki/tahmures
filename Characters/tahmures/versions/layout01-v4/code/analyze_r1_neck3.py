#!/usr/bin/env python3
"""R1-04 definitive: per-layer coverage at the neck bottom & gold strips."""
import numpy as np
import collections
from build_lib import load_master, load_v3, load_domain, erode

m = load_master()
mal = m[..., 3]
mv = mal > 0
dom = load_domain()

hb = load_v3("head/head_base.png")
hair = load_v3("head/hair_back.png")
bd = load_v3("face/beard.png")
A = hb[..., 3] > 0
H = hair[..., 3] > 0
B = bd[..., 3] > 0

print("per-layer bottom edge (min y where layer visible, cols x=500..570 step 10):")
for x in range(500, 571, 10):
    a = np.nonzero(A[:, x])[0]; a = a[a > 340]
    h = np.nonzero(H[:, x])[0]; h = h[h > 340]
    b = np.nonzero(B[:, x])[0]; b = b[b > 340]
    d = np.nonzero(dom[:, x])[0]; d = d[d > 340]
    print(" x=%3d head:%s hair:%s beard:%s dom:%s" % (
        x,
        ("%d..%d" % (a.min(), a.max())) if len(a) else "-",
        ("%d..%d" % (h.min(), h.max())) if len(h) else "-",
        ("%d..%d" % (b.min(), b.max())) if len(b) else "-",
        ("%d..%d" % (d.min(), d.max())) if len(d) else "-"))

print("\nhead_base actual content y369-375, x505-570 (alpha>0 only):")
for y in range(369, 376):
    row = []
    for x in range(505, 571, 5):
        if A[y, x]:
            row.append("x%d:%s" % (x, tuple(hb[y, x, :3])))
    print(" y=%d %s" % (y, row))

print("\nmaster content y369-375, x505-570:")
for y in range(369, 376):
    print(" y=%d" % y, [tuple(m[y, x, :3]) for x in range(505, 571, 5)])

print("\nhair_back content y368-378, x495-580 (alpha>0 only, count per row):")
for y in range(368, 379):
    xs = np.nonzero(H[y, 495:580])[0]
    print(" y=%d hair_back px in x495-579: %d" % (y, len(xs)))

# gold strip vertical profile in head_base (left)
r = hb[..., 0].astype(int); b2 = hb[..., 2].astype(int)
gold = A & (r >= 150) & (r - b2 >= 140)
print("\nleft-strip gold px per row (x460-502):")
for y in range(300, 375):
    n = int(gold[y, 460:502].sum())
    if n:
        xs = np.nonzero(gold[y, 460:502])[0] + 460
        print("  y=%d: %d px (x %d..%d)" % (y, n, xs.min(), xs.max()))

print("\nright-strip gold px per row (x574-615):")
for y in range(300, 375):
    n = int(gold[y, 574:615].sum())
    if n:
        xs = np.nonzero(gold[y, 574:615])[0] + 574
        print("  y=%d: %d px (x %d..%d)" % (y, n, xs.min(), xs.max()))

# what is immediately left/right/above/below the left gold strip (seeds)?
print("\nhead_base colors around left gold strip (x465-500, y330-340), non-gold visible:")
zone = A.copy(); zone[:, :] = False
zone[330:341, 465:500] = True
sel = zone & ~gold
cnt = collections.Counter(tuple(hb[y, x, :3]) for y, x in zip(*np.nonzero(sel)))
for col, n in cnt.most_common(10):
    print("   ", col, n)
