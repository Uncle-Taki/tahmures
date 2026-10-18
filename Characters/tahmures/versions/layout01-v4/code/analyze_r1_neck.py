#!/usr/bin/env python3
"""R1-04: analyze v3 head_base lower-neck garment contamination."""
import numpy as np
import collections
from build_lib import V2, V3, load_master, load_v2, load_v3, load_domain, dilate, erode

m = load_master()
mal = m[..., 3]
mv = mal > 0
dom = load_domain()
edom = erode(dom & mv, 1)

hb = load_v3("head/head_base.png")
hbA = hb[..., 3] > 0
r = hb[..., 0].astype(int)
g = hb[..., 1].astype(int)
b = hb[..., 2].astype(int)

zone = np.zeros_like(hbA)
zone[320:380, 460:615] = True
sel = hbA & zone
print("head_base visible px in zone y320-379 x460-614:", int(sel.sum()))

# broad gold family: warm, saturated, low blue
goldf = sel & (r >= 150) & (r - b >= 90) & (g < r)
print("gold-family px (r>=150, r-b>=90, g<r):", int(goldf.sum()))
ys, xs = np.nonzero(goldf)
if len(ys):
    print("  bbox x %d..%d y %d..%d" % (xs.min(), xs.max(), ys.min(), ys.max()))
    hist = collections.Counter((int(y)//10)*10 for y in ys)
    print("  y-histogram:", dict(sorted(hist.items())))
    # split by x
    for xlo, xhi in ((460, 500), (500, 575), (575, 615)):
        s2 = goldf[:, xlo:xhi]
        print("  x%d-%d: %d" % (xlo, xhi, int(s2.sum())))

# exact color census of the left strip
print("\nleft strip x460-500 y320-379 colors (top 15):")
ls = hbA.copy(); ls[:, :] = False; ls[320:380, 460:500] = True
cnt = collections.Counter(tuple(hb[y, x, :3]) for y, x in zip(*np.nonzero(ls)))
for col, n in cnt.most_common(15):
    print("   ", col, n)

print("\nright strip x575-615 y320-379 colors (top 15):")
rs = hbA.copy(); rs[:, :] = False; rs[320:380, 575:615] = True
cnt = collections.Counter(tuple(hb[y, x, :3]) for y, x in zip(*np.nonzero(rs)))
for col, n in cnt.most_common(15):
    print("   ", col, n)

print("\ncenter x500-575 y315-335 colors (top 12):")
cs = hbA.copy(); cs[:, :] = False; cs[315:335, 500:575] = True
cnt = collections.Counter(tuple(hb[y, x, :3]) for y, x in zip(*np.nonzero(cs)))
for col, n in cnt.most_common(12):
    print("   ", col, n)

print("\nbottom rows y368-378 x500-575 colors (top 15):")
bs = hbA.copy(); bs[:, :] = False; bs[368:378, 500:575] = True
cnt = collections.Counter(tuple(hb[y, x, :3]) for y, x in zip(*np.nonzero(bs)))
for col, n in cnt.most_common(15):
    print("   ", col, n)

# master reference at same zones
print("\nMASTER left strip x460-500 y320-379 (top 10):")
ms = mv.copy(); ms[:, :] = False; ms[320:380, 460:500] = True
cnt = collections.Counter(tuple(m[y, x, :3]) for y, x in zip(*np.nonzero(ms)))
for col, n in cnt.most_common(10):
    print("   ", col, n)

# who else covers the zone: hair_back, beard
hair = load_v3("head/hair_back.png")
bd = load_v3("face/beard.png")
hA = hair[..., 3] > 0
bdA = bd[..., 3] > 0
print("\ncoverage in zone: hair_back %d, beard %d, head_base %d (of %d domain+vis px)" % (
    (hA & zone).sum(), (bdA & zone).sum(), (hbA & zone).sum(), (zone & dom & mv).sum()))
top = (hA | bdA | hbA) & zone & dom & mv
print("zone px still uncovered by hair/beard/head:", int((zone & dom & mv & ~top).sum()))

# hair_back gold in neck zone
hr = hair[..., 0].astype(int)
hb2 = hair[..., 2].astype(int)
hg = hair[..., 3] > 0
gold_h = hg & (hr >= 150) & (hr - hb2 >= 90)
print("hair_back gold-family px in zone:", int((gold_h & zone).sum()))
ys, xs = np.nonzero(gold_h & zone)
for y, x in zip(ys, xs):
    print("   hair_back gold at x=%d y=%d %s" % (x, y, tuple(hair[y, x, :3])))

# what does master look like where head_base has garment px — sample rows
print("\nmaster rows y370-376 x505-570 (every 5th col):")
for y in range(368, 378):
    print(" y=%d:" % y, [tuple(m[y, x, :3]) for x in range(508, 566, 10)])
