#!/usr/bin/env python3
"""R1-02: measure baked dark-moustache ink in v3 head_base/beard vs U."""
import numpy as np
from build_lib import load_master, load_v2, load_v3

m = load_master()
mo = load_v2("face/moustache.png")
U = mo[..., 3] > 0

hb = load_v3("head/head_base.png")
bd = load_v3("face/beard.png")

def dark(a):
    return (a[..., 0] < 90) & (a[..., 1] < 75) & (a[..., 2] < 70) & (a[..., 3] > 0)

box_h = np.zeros_like(U); box_h[209:238, 486:597] = True
box_b = np.zeros_like(U); box_b[224:239, 498:585] = True

d_h = dark(hb) & box_h
d_b = dark(bd) & box_b
print("head_base dark px in Codex bbox:", int(d_h.sum()), "(Codex: 1233)")
print("  of which in U:", int((d_h & U).sum()), " outside U:", int((d_h & ~U).sum()))
print("beard dark px in Codex bbox:", int(d_b.sum()), "(Codex: 346)")
print("  of which in U:", int((d_b & U).sum()), " outside U:", int((d_b & ~U).sum()))

# head_base visible px in the bbox at all
vis_h = (hb[..., 3] > 0) & box_h
print("head_base visible in bbox:", int(vis_h.sum()), " U∩visible:", int((vis_h & U).sum()))
vis_b = (bd[..., 3] > 0) & box_b
print("beard visible in bbox:", int(vis_b.sum()), " U∩visible:", int((vis_b & U).sum()))

# where are the out-of-U dark px in head_base? (sample)
ys, xs = np.nonzero(d_h & ~U)
if len(ys):
    print("out-of-U head_base dark bbox: x %d..%d y %d..%d" % (
        xs.min(), xs.max(), ys.min(), ys.max()))
    import collections
    print("  y-hist:", dict(sorted(collections.Counter((int(y)//5)*5 for y in ys).items())))

# do the out-of-U dark px match the moustache sprite's exact colors?
mo_cols = set(tuple(mo[y, x, :3]) for y, x in zip(*np.nonzero(U)))
match = sum(1 for y, x in zip(ys, xs) if tuple(hb[y, x, :3]) in mo_cols)
print("out-of-U dark px exactly matching a moustache-sprite color:", match, "of", len(ys))

# U split across underlay sprites in v4 plan
hair = load_v3("head/hair_back.png")
di = load_v3("head/diadem_gold.png")
bdA = bd[..., 3] > 0
hA = hair[..., 3] > 0
dA = di[..., 3] > 0
hbA = hb[..., 3] > 0
print("\nU over: head_base %d, beard %d, hair %d, diadem %d, none %d" % (
    (U & hbA & ~bdA & ~hA).sum(), (U & bdA).sum(), (U & hA & ~bdA).sum(),
    (U & dA).sum(), (U & ~hbA & ~bdA & ~hA & ~dA).sum()))
