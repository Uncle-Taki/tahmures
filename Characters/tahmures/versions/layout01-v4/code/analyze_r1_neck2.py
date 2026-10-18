#!/usr/bin/env python3
"""R1-04 precise: strict garment-gold + pale-trim census in v3 head_base."""
import numpy as np
import collections
from build_lib import V3, load_master, load_v3, load_domain, erode

m = load_master()
mal = m[..., 3]
mv = mal > 0
dom = load_domain()
edom = erode(dom & mv, 1)

hb = load_v3("head/head_base.png")
A = hb[..., 3] > 0
r = hb[..., 0].astype(int)
g = hb[..., 1].astype(int)
b = hb[..., 2].astype(int)

# strict garment gold: r-b >= 140
gold = A & (r >= 150) & (r - b >= 140) & (np.arange(hb.shape[0])[:, None] >= 300)
ys, xs = np.nonzero(gold)
print("strict garment gold (y>=300): %d px" % gold.sum())
if len(ys):
    print("  bbox x %d..%d y %d..%d" % (xs.min(), xs.max(), ys.min(), ys.max()))
    hist = collections.Counter((int(y)//10)*10 for y in ys)
    print("  y-hist:", dict(sorted(hist.items())))
    for xlo, xhi in ((460, 502), (502, 574), (574, 615)):
        print("  x%d-%d: %d" % (xlo, xhi, int(gold[:, xlo:xhi].sum())))
    print("  in eroded domain:", int((gold & edom).sum()))
    print("  colors:", collections.Counter(tuple(hb[y, x, :3]) for y, x in zip(ys, xs)).most_common(12))

# pale collar trim
trim = A & (r >= 200) & ((r - b) >= 30) & ((r - b) <= 110) & (g >= 180) & \
    (np.arange(hb.shape[0])[:, None] >= 360)
ys, xs = np.nonzero(trim)
print("\npale trim (y>=360): %d px" % trim.sum())
if len(ys):
    print("  bbox x %d..%d y %d..%d" % (xs.min(), xs.max(), ys.min(), ys.max()))
    print("  in eroded domain:", int((trim & edom).sum()))
    print("  colors:", collections.Counter(tuple(hb[y, x, :3]) for y, x in zip(ys, xs)).most_common(10))
    hist = collections.Counter((int(y)) for y in ys)
    print("  y-hist:", dict(sorted(hist.items())))

# where does neck skin end vertically in the centre?
skin = A & (r >= 200) & ((r - b) >= 100) & ((r - b) <= 139)
for x in (510, 530, 550, 570):
    col = np.nonzero(skin[:, x])[0]
    col = col[(col >= 340) & (col <= 390)]
    if len(col):
        print("neck-skin column x=%d: y %d..%d" % (x, col.min(), col.max()))

# dark contour presence around the gold strips (diffusion seed availability)
dark = A & (r < 90) & (g < 75) & (b < 70)
for name, sl in (("left strip", (slice(320, 380), slice(460, 502))),
                 ("right strip", (slice(320, 380), slice(574, 615))),
                 ("bottom centre", (slice(368, 380), slice(500, 575)))):
    print("%s: gold=%d trim=%d dark=%d skin=%d total=%d" % (
        name, int(gold[sl].sum()), int(trim[sl].sum()), int(dark[sl].sum()),
        int(skin[sl].sum()), int(A[sl].sum())))

# gold px adjacency: how many gold px touch a dark px?
from build_lib import dilate
gold_d = gold & dilate(dark, 1)
print("\ngold px adjacent to dark:", int(gold_d.sum()), "of", int(gold.sum()))
trim_d = trim & dilate(dark, 1)
print("trim px adjacent to dark:", int(trim_d.sum()), "of", int(trim.sum()))

# check hair strand continuation above the left gold strip
print("\nhead_base colors x460-502 y300-326 (top 8):")
sl = (slice(300, 326), slice(460, 502))
cnt = collections.Counter(tuple(hb[y, x, :3]) for y, x in zip(*np.nonzero(A[sl])))
for col, n in cnt.most_common(8):
    print("   ", col, n)

# master's own gold in the same zone (is master itself garment there?)
mgold = mv & (m[..., 0].astype(int) >= 150) & \
    (m[..., 0].astype(int) - m[..., 2].astype(int) >= 140) & \
    (np.arange(hb.shape[0])[:, None] >= 300)
print("\nmaster strict gold y>=300: %d px" % mgold.sum())
ys, xs = np.nonzero(mgold)
if len(ys):
    print("  bbox x %d..%d y %d..%d" % (xs.min(), xs.max(), ys.min(), ys.max()))

# domain bottom edge in neck columns
dom_ys = np.nonzero(dom[:, 530])[0]
print("\ndomain column x=530: y %d..%d" % (dom_ys.min(), dom_ys.max()))
dom_ys = np.nonzero(dom[:, 480])[0]
print("domain column x=480: y %d..%d" % (dom_ys.min(), dom_ys.max()))

# head_base alpha bottom edge
hb_ys = np.nonzero(A[:, 530])[0]
print("head_base column x=530: y %d..%d" % (hb_ys.min(), hb_ys.max()))
hb_ys = np.nonzero(A[:, 480])[0]
print("head_base column x=480: y %d..%d" % (hb_ys.min(), hb_ys.max()))
