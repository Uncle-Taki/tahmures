#!/usr/bin/env python3
"""Fringe analysis: master colors just outside U; in-U warm/highlight px."""
import numpy as np
import collections
from build_lib import load_master, load_v2, load_v3, dilate

m = load_master()
mo = load_v2("face/moustache.png")
U = mo[..., 3] > 0
mv = m[..., 3] > 0

D = dilate(U, 1) & ~U & mv
print("dilate(U,1)-minus-U px:", int(D.sum()))
ys, xs = np.nonzero(D)
cnt = collections.Counter(tuple(m[y, x, :3]) for y, x in zip(ys, xs))
print("top colors:", cnt.most_common(12))
warm = D & (m[..., 0] >= 150) & (m[..., 0] - m[..., 2] >= 60)
dark = D & (m[..., 0] < 90) & (m[..., 1] < 75) & (m[..., 2] < 70)
mid = D & ~warm & ~dark
print("outside-U adjacent: warm=%d dark=%d mid=%d" % (warm.sum(), dark.sum(), mid.sum()))
# sample mid colors
ys2, xs2 = np.nonzero(mid)
print("sample mid colors:", [tuple(m[y, x, :3]) for y, x in list(zip(ys2, xs2))[:15]])

# warm in-U px: where are they?
W = U & (m[..., 0] >= 150) & (m[..., 0] - m[..., 2] >= 60)
ys3, xs3 = np.nonzero(W)
print("\nin-U warm px: %d, bbox x %d..%d y %d..%d" % (
    W.sum(), xs3.min(), xs3.max(), ys3.min(), ys3.max()))
hist = collections.Counter((int(y)//5)*5 for y in ys3)
print("y-hist:", dict(sorted(hist.items())))
# the 12 px at y>=237
late = U & (np.arange(m.shape[0])[:, None] >= 237)
ys4, xs4 = np.nonzero(late)
print("U px y>=237:", [(int(x), int(y), tuple(m[y, x, :3])) for y, x in zip(ys4, xs4)])

# brightest in-U px (would show as halo when shifted)
bright = U & (m[..., 0] >= 200) & (m[..., 1] >= 150)
print("\nin-U bright px (r>=200,g>=150):", int(bright.sum()))
ys5, xs5 = np.nonzero(bright)
print("  sample:", [(int(x), int(y), tuple(m[y, x, :3])) for y, x in list(zip(ys5, xs5))[:12]])

# how do in-U warm px compare to their local surroundings (are they pure skin)?
# check a vertical profile through the moustache bottom centre
print("\nmaster x=540, y228..242:", [tuple(m[y, 540, :3]) for y in range(228, 243)])
print("U at x=540, y228..242:", [bool(U[y, 540]) for y in range(228, 243)])
print("master x=524, y228..242:", [tuple(m[y, 524, :3]) for y in range(228, 243)])
print("U at x=524, y228..242:", [bool(U[y, 524]) for y in range(228, 243)])
