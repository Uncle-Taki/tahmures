#!/usr/bin/env python3
"""Fact-check the v4 moustache/underlay geometry before building."""
import numpy as np
from build_lib import V2, V3, load_master, load_v2, load_domain, dilate, erode

m = load_master()
mal = m[..., 3]
mv = mal > 0
dom = load_domain()

mo = load_v2("face/moustache.png")
U = mo[..., 3] > 0
print("v2 moustache alpha: %d px, unique alphas: %s" % (
    U.sum(), sorted(set(mo[..., 3][U].tolist()))))
ys, xs = np.nonzero(U)
print("U bbox: x %d..%d y %d..%d" % (xs.min(), xs.max(), ys.min(), ys.max()))

# per-column bottom edge of U in the mouth centre
for x in range(528, 556, 4):
    col = np.nonzero(U[:, x])[0]
    if len(col):
        print("  x=%d U y %d..%d" % (x, col.min(), col.max()))

# warm px inside U (master r>=150)
warm_U = U & (m[..., 0] >= 150) & (m[..., 0] - m[..., 2] >= 60)
print("warm px inside U:", int(warm_U.sum()))

# lip band / parting line facts
print("\nmaster columns (x=536..544 step 2), y236..254:")
for x in range(536, 546, 2):
    print(" x=%d:" % x, [tuple(m[y, x, :3]) for y in range(236, 255)])

# U overlap with rows >= 238
for ylo in (237, 238, 239, 240):
    print("U px with y >= %d: %d" % (ylo, int((U & (np.arange(mal.shape[0])[:, None] >= ylo)).sum())))

# v3 M and P
M = np.load(V3 + "/code/_M.npy")
P = np.load(V3 + "/code/_P.npy")
print("\nv3 M: %d px" % M.sum())
ys, xs = np.nonzero(M)
print("M bbox: x %d..%d y %d..%d" % (xs.min(), xs.max(), ys.min(), ys.max()))
print("v3 P: %d px, bbox y %d..%d" % (P.sum(), np.nonzero(P)[0].min(), np.nonzero(P)[0].max()))

# crescent zone: warm master px in box, and who covers them
box = np.zeros_like(U)
box[226:252, 500:582] = True
warm = box & mv & (m[..., 0] >= 150) & (m[..., 0] - m[..., 2] >= 60)
print("\nwarm px in box(500-582,226-252): %d" % warm.sum())
print("  of these in U:", int((warm & U).sum()), " in M:", int((warm & M).sum()),
      " in P:", int((warm & P).sum()))
cres = np.zeros_like(U)
cres[230:237, 530:542] = True
w_cres = cres & mv & (m[..., 0] >= 150) & (m[..., 0] - m[..., 2] >= 60)
print("crescent bbox warm px:", int(w_cres.sum()),
      " in U:", int((w_cres & U).sum()), " in M:", int((w_cres & M).sum()))

# nm_alpha coverage of parting line y240
nm = load_v2("mouths/neutral_mouth.png")
nmA = nm[..., 3] > 0
ys, xs = np.nonzero(nmA)
print("\nnm_alpha: %d px bbox x %d..%d y %d..%d" % (nmA.sum(), xs.min(), xs.max(), ys.min(), ys.max()))
row240 = nmA[240, 528:557]
print("nm_alpha at y240 x528-556:", row40 := row240.astype(int).tolist())

# dark px at y237-243 not in nm_alpha or U (would stay in beard as lip remnant)
dark = (m[..., 0] < 90) & (m[..., 1] < 75) & (m[..., 2] < 70) & mv
band = np.zeros_like(U)
band[237:244, 524:561] = True
resid = band & dark & ~nmA & ~U
print("dark lip px y237-243 not covered by nm/U:", int(resid.sum()))

# beard sprite (v2) alpha in mouth area
bd = load_v2("face/beard.png")
bdA = bd[..., 3] > 0
print("v2 beard alpha in crescent:", int((bdA & w_cres).sum()))
print("v2 beard alpha covers warm box px:", int((bdA & warm).sum()))

# CLONE_BLOCK verify
block = m[270:293, 494:604]
print("\nclone block all dark:", bool(((block[..., 0] < 90) & (block[..., 1] < 75) & (block[..., 2] < 70)).all()))

# head_base garment analysis (R1-04)
hb = load_v2("head/head_base.png")
hbA = hb[..., 3] > 0
gold_g = hbA & (hb[..., 0] >= 170) & ((hb[..., 0].astype(int) - hb[..., 2]) >= 140)
ys, xs = np.nonzero(gold_g)
print("\nhead_base garment-gold px (r>=170, r-b>=140): %d, bbox x %d..%d y %d..%d" % (
    gold_g.sum(), xs.min(), xs.max(), ys.min(), ys.max()))
for ylo, yhi in ((0, 320), (320, 400)):
    sel = gold_g & (ys[:, None] * 0 + 1) if False else None
gold_y = {int(y) for y in ys}
import collections
hist = collections.Counter((int(y) // 10) * 10 for y in ys)
print("gold px y-histogram (decade):", dict(sorted(hist.items())))
# center column band
cband = np.zeros_like(U)
cband[300:380, 501:573] = True
print("gold px in center band x501-572 y300-379:", int((gold_g & cband).sum()))

# eroded domain
edom = erode(dom & mv, 1)
print("\neroded domain px:", int(edom.sum()))
print("gold px in eroded domain:", int((gold_g & edom).sum()))

# hair_back gold
hb2 = load_v2("head/hair_back.png")
hA = hb2[..., 3] > 0
g2 = hA & (hb2[..., 0] >= 170) & ((hb2[..., 0].astype(int) - hb2[..., 2]) >= 140)
ys2, xs2 = np.nonzero(g2)
print("hair_back garment-gold px: %d, bbox x %d..%d y %d..%d" % (
    g2.sum(), xs2.min(), xs2.max(), ys2.min(), ys2.max()))
