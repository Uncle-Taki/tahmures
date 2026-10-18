#!/usr/bin/env python3
"""Quick verification of the v4 stage-10 outcome before formal stages."""
import numpy as np
from PIL import Image, ImageFilter
from build_lib import V4, load_master, load_domain, erode, compose

m = load_master()
mal = m[..., 3]
mv = mal > 0
dom = load_domain()

def L(rel):
    return np.asarray(Image.open(V4 + "/" + rel).convert("RGBA")).copy()

hair = L("head/hair_back.png")
head = L("head/head_base.png")
di = L("head/diadem_gold.png")
ears = [L("face/ear_right.png"), L("face/ear_left.png")]
beard = L("face/beard.png")
nose = L("face/nose.png")
eyes = [L("face/eye_right.png"), L("face/eye_left.png")]
brows = [L("face/eyebrow_right.png"), L("face/eyebrow_left.png")]
moust = L("face/moustache.png")
pn = L("mouths/lower_face_neutral.png")
po = L("mouths/lower_face_open_test.png")

base = [hair, head, ears[0], ears[1], beard]
feat = [nose, eyes[0], eyes[1], brows[0], brows[1]]

A = np.asarray(compose(base + feat + [moust, di]))
B = np.asarray(compose(base + [pn] + feat + [moust, di]))
C = np.asarray(compose(base + [po] + feat + [moust, di]))
uA = np.asarray(compose(base + feat + [di]))          # A underlay (no patch, no moustache)
uB = np.asarray(compose(base + [pn] + feat + [di]))  # B underlay (patch, no moustache)

# 1. crescent / warm residue in A
warm = (A[..., 0] >= 140) & (A[..., 0] - A[..., 2] >= 55) & (A[..., 3] > 0)
print("A warm px in crescent bbox [530,230,542,237):", int(warm[230:237, 530:542].sum()))
print("A warm px in wider mouth box x520-560 y226-242:", int(warm[226:242, 520:560].sum()))
ys, xs = np.nonzero(warm[226:242, 520:560])
if len(ys):
    print("  at:", [(int(x)+520, int(y)+226, tuple(A[int(y)+226, int(x)+520, :3])) for y, x in zip(ys, xs)][:20])

# 2. B fidelity vs master (raw count; zone accounting in section 7b)
edom = erode(dom & mv, 1)
sel = edom & (mal >= 250)
d = np.abs(B[..., :3].astype(int) - m[..., :3].astype(int)).max(axis=2)
print("\nB vs master: px>3 in eroded opaque domain (raw):", int((d > 3)[sel].sum()),
      " px>2:", int((d > 2)[sel].sum()), " max:", int(d[sel].max()))

# 3. C vs B confinement
dCB = (C[..., :3] != B[..., :3]).any(axis=2) | (C[..., 3] != B[..., 3])
opening = np.load(V4 + "/code/_opening.npy")
P = np.load(V4 + "/code/_P.npy")
outside = dCB & ~(P)
print("\nC vs B: differing px:", int(dCB.sum()), " outside P:", int(outside.sum()),
      " inside opening:", int((dCB & opening).sum()),
      " inside P not opening:", int((dCB & P & ~opening).sum()))
ys, xs = np.nonzero(dCB & P & ~opening)
if len(ys):
    print("  P-diff not in opening:", [(int(x), int(y)) for y, x in zip(ys, xs)][:12])

# 4. coverage for A, B, C
interior = np.asarray(Image.fromarray(np.where(dom, 255, 0).astype(np.uint8)).filter(ImageFilter.MinFilter(3))) >= 128
for name, img in (("A", A), ("B", B), ("C", C)):
    a = img[..., 3]
    holes = int((interior & (mal > 0) & (a == 0)).sum())
    deficits = int((interior & (mal >= 250) & (a < 250)).sum())
    print("%s coverage: holes=%d deficits=%d" % (name, holes, deficits))

# 5. moustache stress vacated-strip identity (dy=+1 over neutral)
def shift_alpha_only(arr, dx, dy):
    out = np.zeros_like(arr)
    h, w = arr.shape[:2]
    x0s, x1s = max(0, dx), min(w, w + dx)
    y0s, y1s = max(0, dy), min(h, h + dy)
    if x0s < x1s and y0s < y1s:
        out[y0s:y1s, x0s:x1s] = arr[y0s - dy:y1s - dy, x0s - dx:x1s - dx]
    return out

from build_lib import dilate
U = np.load(V4 + "/code/_U.npy")
mo_a = moust[..., 3] > 0
for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
    sm = shift_alpha_only(moust, dx, dy)
    render = np.asarray(compose(base + [pn] + feat + [sm, di]))
    vac = mo_a & ~(sm[..., 3] > 0)
    diff = (render[vac] != uB[vac]).any(axis=-1).sum() if vac.any() else 0
    print("moustache d(%d,%d): vacated px=%d, comp!=underlay px=%d" % (dx, dy, vac.sum(), diff))

# 6. R1-02 recount: dark ink under the moustache footprint in underlay sprites
hb_dark = (head[..., 0] < 90) & (head[..., 1] < 75) & (head[..., 2] < 70) & (head[..., 3] > 0)
bd_dark = (beard[..., 0] < 90) & (beard[..., 1] < 75) & (beard[..., 2] < 70) & (beard[..., 3] > 0)
boxh = np.zeros_like(U); boxh[209:238, 486:597] = True
boxb = np.zeros_like(U); boxb[224:239, 498:585] = True
print("\nR1-02 recount: head_base dark px in Codex bbox:", int((hb_dark & boxh).sum()),
      " (was 1234); beard dark px:", int((bd_dark & boxb).sum()), " (was 818; Codex metric 346)")

# 7. R1-04 recount: garment family in head_base/hair_back neck zone
# (garment gold + blend fringe: b<=70; skin keeps b>=73, darks r<120)
def garment_mask(a):
    r = a[..., 0].astype(int); b = a[..., 2].astype(int)
    return (a[..., 3] > 0) & (r >= 120) & (r - b >= 90) & (b <= 70) & \
        (np.arange(a.shape[0])[:, None] >= 300)
print("R1-04 recount: head_base garment px y>=300:", int(garment_mask(head).sum()),
      " (was 253 strict + 166 fringe = 419)")
print("R1-04 recount: hair_back garment px y>=300:", int(garment_mask(hair).sum()),
      " (was 3 strict + 5 fringe = 8)")

# 7b. B fidelity vs master EXCLUDING the intended repair zones
neck2 = np.load(V4 + "/code/_neck_clean.npy")
strip_zone = np.zeros_like(neck2)
strip_zone[300:370, 460:612] = True
intended = dilate(neck2, 2) | strip_zone
dB = np.abs(B[..., :3].astype(int) - m[..., :3].astype(int)).max(axis=2)
bad_out = (dB > 3) & sel & ~intended
in_zone = (dB > 3) & sel & intended
print("B vs master: px>3 outside intended repair zone:", int(bad_out.sum()),
      " (inside zone, intended:", int(in_zone.sum()), ")")
ys, xs = np.nonzero(bad_out)
if len(ys):
    print("  UNINTENDED at:", [(int(x), int(y), tuple(m[y, x, :3]), tuple(B[y, x, :3]))
                              for y, x in zip(ys, xs)][:20])

# 8. neck visual: colors along the former gold strip
print("\nhead_base left strip after cleanup (x467-500 y330-345 sample):")
for y in range(330, 346, 3):
    print("  y=%d:" % y, [tuple(head[y, x, :3]) for x in range(468, 500, 8)])
