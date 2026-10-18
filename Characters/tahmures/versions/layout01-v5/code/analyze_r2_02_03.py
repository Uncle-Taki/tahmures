#!/usr/bin/env python3
"""R2-02 / R2-03 analysis: seam tears in stress samples; neck bands.

R2-02: v4 patch-neutral-dx0-dy2 and moustache-over-neutral-dx0-dy-1 show
light skin bars and fragmented dark edges at the moustache underside
(x490-550, y229-240). Identify which layer/px produce them.

R2-03: v4 neck repair (x467-606, y327-375) shows horizontal bands and a
fragment-shaped wedge at the left attachment x467-486, y327-363.
"""
import numpy as np
from PIL import Image

from build_lib import V2, V4, compose, shifted


def L(root, rel):
    return np.asarray(Image.open(root + "/" + rel).convert("RGBA")).copy()


m = L(V2, "source/approved_master.png")
moust = L(V4, "face/moustache.png")
patch_n = L(V4, "mouths/lower_face_neutral.png")
beard = L(V4, "face/beard.png")
head = L(V4, "head/head_base.png")
hair = L(V4, "head/hair_back.png")
B = L(V4, "previews/neutral.png")

M = np.load(V4 + "/code/_M.npy")
P = np.load(V4 + "/code/_P.npy")
U = np.load(V4 + "/code/_U.npy")
ink_head = np.load(V4 + "/code/_ink_head.npy")
ink_beard = np.load(V4 + "/code/_ink_beard.npy")
patch_ink = np.load(V4 + "/code/_patch_ink.npy")
neck_clean = np.load(V4 + "/code/_neck_clean.npy")

BASE = ["head/hair_back.png", "head/head_base.png", "face/ear_right.png",
        "face/ear_left.png", "face/beard.png"]
FEAT = ["face/nose.png", "face/eye_right.png", "face/eye_left.png",
        "face/eyebrow_right.png", "face/eyebrow_left.png"]

print("=== R2-02a: patch dy+2 — what changed vs B at the moustache underside ===")
comp_dy2 = np.asarray(compose(
    [L(V4, p) for p in BASE] + [shifted(patch_n, 0, 2)] + [L(V4, p) for p in FEAT]
    + [moust] + [L(V4, "head/diadem_gold.png")]))
d = (comp_dy2 != B).any(axis=2)
ys, xs = np.nonzero(d)
print("changed px:", len(ys), "bbox:", xs.min(), ys.min(), xs.max(), ys.max())
# inside the moustache underside zone
zone = np.zeros_like(d)
zone[229:241, 490:551] = True
print("changed px inside x490-550 y229-240:", int((d & zone).sum()))
# of those, how many are moustache-covered (i.e. the moustache composite
# changed because its underlay moved)?
mz = (d & zone & (moust[..., 3] > 0))
print("  of which under moustache alpha>0:", int(mz.sum()))
# sample the visual change: rows y232-238, columns x500-545
print("sample diffs (dy2 vs B) under moustache, y230-240:")
for y in range(230, 241):
    xs2 = [x for x in range(490, 551) if d[y, x] and moust[y, x, 3] > 0]
    if xs2:
        x0 = xs2[0]
        print("  y=%d n=%d  e.g. x=%d: B=%s dy2=%s mo_a=%d mo_rgb=%s" % (
            y, len(xs2), x0, tuple(B[y, x0, :3]), tuple(comp_dy2[y, x0, :3]),
            moust[y, x0, 3], tuple(moust[y, x0, :3])))

print()
print("=== R2-02b: moustache dy-1 — the vacated strip content ===")
sm = shifted(moust, 0, -1)
comp_mdy = np.asarray(compose(
    [L(V4, p) for p in BASE] + [patch_n] + [L(V4, p) for p in FEAT]
    + [sm] + [L(V4, "head/diadem_gold.png")]))
vac = (moust[..., 3] > 0) & ~(sm[..., 3] > 0)
print("vacated px:", int(vac.sum()))
ys, xs = np.nonzero(vac)
print("vacated bbox:", xs.min(), ys.min(), xs.max(), ys.max())
# what shows in the vacated strip (the patch underdraw) — bottom rows
print("vacated strip rows y>=228, showing patch content (the 'skin bars'):")
for y in range(228, 240):
    xs2 = [x for x in range(485, 598) if vac[y, x]]
    if xs2:
        samples = [(x, tuple(comp_mdy[y, x, :3])) for x in xs2[::max(1, len(xs2)//5)]]
        print("  y=%d n=%d %s" % (y, len(xs2), samples))

print()
print("=== patch underdraw (patch_ink) content statistics ===")
ys, xs = np.nonzero(patch_ink)
vals = patch_n[ys, xs, :3]
print("patch_ink px:", len(ys), "RGB mean:", vals.mean(axis=0).round(1),
      "min:", vals.min(axis=0), "max:", vals.max(axis=0))
bright = (vals[:, 0] >= 140).sum()
print("patch_ink px with r>=140 (skin-like):", int(bright))
dark = (vals[:, 0] < 90).sum()
print("patch_ink px with r<90 (dark):", int(dark))

print()
print("=== R2-03: v4 neck zone — horizontal banding measure ===")
# row-mean luminance inside the left attachment wedge x467-486 y327-363
for name, arr in (("head_base", head), ("state B", B)):
    print(name, "row means (x467-486):")
    out = []
    for y in range(325, 366, 2):
        seg = arr[y, 467:487, :3]
        out.append("y%d:%d" % (y, seg.mean()))
    print("  " + " ".join(out))
print()
print("head_base neck zone column structure at y340 (x462-500):")
print([tuple(head[340, x, :3]) for x in range(462, 500, 3)])
print("master at same:", [tuple(m[340, x, :3]) for x in range(462, 500, 3)])
print()
print("neck_clean px:", int(neck_clean.sum()))
ys, xs = np.nonzero(neck_clean)
print("neck_fill RGB stats: mean", head[ys, xs, :3].mean(axis=0).round(1),
      "std", head[ys, xs, :3].std(axis=0).round(1))
# band detection: row-to-row mean jumps inside the wedge
rows = []
for y in range(328, 363):
    seg = head[y, 467:487, 0].astype(int)
    rows.append(seg.mean())
jumps = [abs(rows[i+1] - rows[i]) for i in range(len(rows)-1)]
print("row-mean jumps >8:", [(328+i, round(jumps[i],1)) for i in range(len(jumps)) if jumps[i] > 8])
