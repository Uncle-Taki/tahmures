#!/usr/bin/env python3
"""Layout01 v4 repair — stage 10: construct all sprites, masks, provenance.

Revision 1 over v3 (Model B local lower-face patch retained):

R1-01 (mouthless warm crescent under the moustache centre):
  the v2 moustache matte is binary (alpha 253/254) with blend-encoded RGB;
  its warm over-extensions rendered as a skin crescent over the dark beard
  clone in state A. The v4 moustache is decontaminated: pure-skin matte px
  are dropped, ink-blend px are re-solved as (alpha, rgb) so they composite
  to the exact master colour over the neutral underlay AND go dark over the
  mouthless beard clone.

R1-02 (baked moustache outline in underlayers):
  the full moustache footprint U (v2 matte, exact) is underdrawn:
  head_base gets diffused skin, the beard gets clone texture, the neutral
  patch gets art diffusion — so +-1px moustache offsets reveal clean
  surfaces instead of the old ink outline.

R1-03 (incoherent small-open test):
  the opening is formed at the actual lip parting line (darkest row in
  y237..243 per column, the master's y240 line), as a restrained lens-shaped
  gap inside the same patch footprint.

R1-04 (garment colours in the head layer):
  strict garment gold (r>=150, r-b>=140) and pale collar trim
  (r>=200, 30<=r-b<=110, g>=185) pixels in the head_base neck zone and three
  gold pixels in hair_back are replaced with dark strand continuation
  (Laplacian diffusion from the surrounding hair strands, with a one-pixel
  contour blend toward adjacent neck skin). Neck shading skin
  (r-b roughly 100..139) is legitimate master art and is kept.
"""
import json
import os
import numpy as np
from PIL import Image

from build_lib import (
    V2, V3, V4, CANVAS, load_master, load_v2, load_domain, save_rgba,
    save_mask_L, save_binary, dilate, erode, nearest_class, alpha_bbox,
    diffuse, compose,
)

CLONE_BLOCK = (270, 293, 494, 604)  # y0, y1 (exclusive), x0, x1 (exclusive)
M_REF = np.array([45, 32, 27], dtype=np.float64)


def clone_fill(m, ys, xs):
    """Beard texture tiled from the verified all-dark clone block."""
    by0, by1, bx0, bx1 = CLONE_BLOCK
    src_y = by0 + ((ys - 228) % (by1 - by0))
    src_x = np.clip(xs, bx0, bx1 - 1)
    return m[src_y, src_x, :3]


def solve_moustache_px(B0, u):
    """Solve (c, m) so that c*m + (1-c)*u == B0 with m clamped to [0,255].

    Returns (alpha, rgb, err). c is estimated from the red channel (largest
    skin/ink separation) and refined by a local grid search when clamping
    prevents an exact solution.
    """
    B0 = B0.astype(np.float64)
    u = u.astype(np.float64)
    dr = u[0] - M_REF[0]
    if abs(dr) < 20:
        return None
    c0 = (u[0] - B0[0]) / dr
    cands = [c0]
    # per-channel estimates as extra candidates
    for ch in range(3):
        d = u[ch] - M_REF[ch]
        if abs(d) > 20:
            cands.append((u[ch] - B0[ch]) / d)
    lo = max(0.02, min(cands) - 0.12)
    hi = min(0.99, max(cands) + 0.12)
    cands.extend(np.arange(lo, hi + 1e-9, 0.02))
    best = None
    for c in cands:
        c = float(np.clip(c, 0.02, 0.99))
        m = (B0 - (1 - c) * u) / c
        m = np.clip(m, 0, 255)
        comp = c * m + (1 - c) * u
        err = float(np.abs(comp - B0).max())
        if best is None or err < best[2]:
            best = (c, m, err)
    c, m, err = best
    return int(round(255 * c)), np.clip(np.round(m), 0, 255).astype(np.uint8), err


def main():
    for d in ("head", "face", "mouths", "masks", "provenance", "previews",
              "previews/stress", "previews/plates"):
        os.makedirs(V4 + "/" + d, exist_ok=True)

    m = load_master()
    mal = m[..., 3]
    master_vis = mal > 0
    dom = load_domain()

    v2_sprites = {
        "hair_back": load_v2("head/hair_back.png"),
        "head_base": load_v2("head/head_base.png"),
        "diadem_gold": load_v2("head/diadem_gold.png"),
        "ear_left": load_v2("face/ear_left.png"),
        "ear_right": load_v2("face/ear_right.png"),
        "eye_left": load_v2("face/eye_left.png"),
        "eye_right": load_v2("face/eye_right.png"),
        "eyebrow_left": load_v2("face/eyebrow_left.png"),
        "eyebrow_right": load_v2("face/eyebrow_right.png"),
        "nose": load_v2("face/nose.png"),
        "beard": load_v2("face/beard.png"),
        "moustache": load_v2("face/moustache.png"),
        "neutral_mouth": load_v2("mouths/neutral_mouth.png"),
    }
    covered = np.zeros((CANVAS[1], CANVAS[0]), dtype=bool)
    for s in v2_sprites.values():
        covered |= s[..., 3] > 0

    # ---------------- 1. uncovered pixel assignment (v3 recipe) ----------------
    unc = dom & master_vis & ~covered
    gold_zone = dilate(v2_sprites["diadem_gold"][..., 3] > 0, 4)
    hair_extra = np.zeros_like(unc)
    diadem_extra = np.zeros_like(unc)
    head_extra = np.zeros_like(unc)
    beard_extra = np.zeros_like(unc)
    ys, xs = np.nonzero(unc)
    for y, x in zip(ys, xs):
        cls = nearest_class(m[y, x, :3].astype(np.int32))
        if y <= 40:
            target = "hair" if cls in ("dark", "black") else (
                "diadem" if cls == "gold" else "head")
        elif y <= 130:
            if cls == "gold" or (cls in ("dark", "black") and gold_zone[y, x]):
                target = "diadem"
            elif cls == "skin":
                target = "head"
            else:
                target = "hair"
        elif 215 <= y <= 325 and 455 <= x <= 615:
            target = "beard"
        elif y >= 326 and cls == "gold":
            target = "head"
        elif cls == "skin":
            target = "head"
        elif cls in ("dark", "black"):
            target = "hair"
        else:
            target = "hair" if (x < 470 or x > 612) else "head"
        if target == "hair":
            hair_extra[y, x] = True
        elif target == "diadem":
            diadem_extra[y, x] = True
        elif target == "beard":
            beard_extra[y, x] = True
        else:
            head_extra[y, x] = True
    print("uncovered=%d assignment: hair+%d diadem+%d head+%d beard+%d" % (
        unc.sum(), hair_extra.sum(), diadem_extra.sum(), head_extra.sum(),
        beard_extra.sum()))

    # ---------------- 2. receiver M, patch footprint P, moustache footprint U ----------------
    nm_alpha = v2_sprites["neutral_mouth"][..., 3] > 0
    box = np.zeros_like(nm_alpha)
    box[249:269, 524:561] = True
    darkpx = (m[..., 0] < 90) & (m[..., 1] < 75) & (m[..., 2] < 70) & master_vis
    dark_mass = box & darkpx
    M = nm_alpha | dark_mass
    M = dilate(erode(M, 1), 2) | M
    M = dilate(erode(M, 2), 2) | nm_alpha | dark_mass
    P = dilate(M, 3)
    P[:226, :] = False
    # reproducibility guard: identical to the accepted v3 regions
    assert np.array_equal(M, np.load(V3 + "/code/_M.npy")), "M differs from v3"
    assert np.array_equal(P, np.load(V3 + "/code/_P.npy")), "P differs from v3"
    print("M=%d P=%d (v3-identical)" % (M.sum(), P.sum()))

    U = v2_sprites["moustache"][..., 3] > 0
    print("U=%d" % U.sum())

    # ---------------- 3. hair_back (v3 recipe + R1-04 gold cleanup) ----------------
    hair = v2_sprites["hair_back"].copy()
    hair[..., :3][hair_extra] = m[..., :3][hair_extra]
    hair[..., 3][hair_extra] = mal[hair_extra]
    hr = hair[..., 0].astype(int)
    hb_ = hair[..., 2].astype(int)
    # garment gold and its dark-blend fringe (garment family: b<=70;
    # neck skin keeps b>=73, strand darks stay r<120)
    hair_gold = (hair[..., 3] > 0) & (hr >= 120) & (hr - hb_ >= 90) & (hb_ <= 70) & \
        (np.arange(hair.shape[0])[:, None] >= 300)
    print("hair_back garment px to clean:", int(hair_gold.sum()))

    # ---------------- 4. diadem_gold (v3 recipe, unchanged behaviour) ----------------
    diadem = v2_sprites["diadem_gold"].copy()
    diadem[..., :3][diadem_extra] = m[..., :3][diadem_extra]
    diadem[..., 3][diadem_extra] = mal[diadem_extra]

    # ---------------- 5. head_base ----------------
    # provisional beard region (needed to subtract from head region)
    beard_region = (v2_sprites["beard"][..., 3] > 0) | beard_extra | dilate(M, 4)
    hair_a = hair[..., 3] > 0
    diadem_a = diadem[..., 3] > 0
    head_region = dom & master_vis & ~hair_a & ~beard_region & ~diadem_a
    head = np.zeros((CANVAS[1], CANVAS[0], 4), dtype=np.uint8)
    head[..., :3] = m[..., :3]
    head[..., 3] = np.where(head_region, mal, 0)

    # feature underdraw (v3 recipe: eye/brow/nose solid interiors)
    feat = np.zeros_like(head_region)
    for fid in ("eye_left", "eye_right", "eyebrow_left", "eyebrow_right", "nose"):
        feat |= v2_sprites[fid][..., 3] >= 252
    feat &= head_region
    ys, xs = np.nonzero(feat)
    y0, y1 = max(0, ys.min() - 4), min(CANVAS[1], ys.max() + 5)
    x0, x1 = max(0, xs.min() - 4), min(CANVAS[0], xs.max() + 5)
    val = head[y0:y1, x0:x1, :3].astype(np.float64)
    f = feat[y0:y1, x0:x1]
    boundary = dilate(f, 1) & ~f
    seed = val[boundary].mean(axis=0)
    val[f] = seed
    for _ in range(600):
        nv = val.copy()
        nv[1:, :] = (val[1:, :] + val[:-1, :]) / 2
        nv[:-1, :] = (val[:-1, :] + val[1:, :]) / 2
        nv[:, 1:] = (val[:, 1:] + val[:, :-1]) / 2
        nv[:, :-1] = (val[:, :-1] + val[:, 1:]) / 2
        val = np.where(f[..., None], nv, val)
    head[y0:y1, x0:x1, :3] = np.clip(np.round(val), 0, 255).astype(np.uint8)
    head_reconstructed = feat.copy()

    # R1-02/R1-01: underdraw the moustache footprint in head_base with
    # diffused skin. Boundary values are the surrounding master art; dark
    # non-head-region pixels inside the box are added to the diffusion
    # region (they are invisible in head_base) so ink/beard colours do not
    # leak into the skin fill.
    ink_head = U & head_region
    print("head_base moustache-footprint underdraw px:", int(ink_head.sum()))
    seed_box = np.zeros_like(U)
    seed_box[195:262, 470:614] = True
    dark_m = (m[..., 0] < 100) & (m[..., 1] < 85) & (m[..., 2] < 80) & master_vis
    dark_buffer = seed_box & master_vis & ~head_region & ~hair_a & ~diadem_a & dark_m
    s_region = ink_head | dark_buffer
    s_field = diffuse(s_region, m[..., :3].astype(np.float64))
    head[..., :3][ink_head] = s_field[..., :3][ink_head]
    head_reconstructed |= ink_head
    print("skin underdraw: region=%d (dark buffer %d)" % (s_region.sum(), dark_buffer.sum()))

    # R1-04: garment gold / pale trim cleanup in the neck zone
    r_ = head[..., 0].astype(int)
    g_ = head[..., 1].astype(int)
    b_ = head[..., 2].astype(int)
    ygrid = np.arange(head.shape[0])[:, None]
    vis_head = head[..., 3] > 0
    # strict garment gold: warm saturated AND low absolute blue (neck
    # shading skin shares the r-b range but keeps b >= 73); plus the
    # gold-to-dark blend fringe of the garment strips
    gold_g = vis_head & (ygrid >= 300) & (b_ <= 70) & \
        (((r_ >= 150) & (r_ - b_ >= 140)) | ((r_ >= 120) & (r_ - b_ >= 90)))
    trim_t = vis_head & (r_ >= 200) & (r_ - b_ >= 30) & (r_ - b_ <= 110) & \
        (g_ >= 185) & (ygrid >= 340)
    neck_clean = gold_g | trim_t
    print("neck cleanup: gold=%d trim=%d total=%d (in eroded domain: %d)" % (
        gold_g.sum(), trim_t.sum(), neck_clean.sum(),
        (neck_clean & erode(dom & master_vis, 1)).sum()))
    # strand-continuation diffusion: boundary = the head layer's own kept
    # colours (skin + strand darks) plus hair_back where head is transparent
    zone = np.zeros_like(U)
    zone[290:382, 455:618] = True
    seed_rgb = np.zeros((CANVAS[1], CANVAS[0], 3), dtype=np.float64)
    head_boundary = zone & vis_head & ~neck_clean
    seed_rgb[head_boundary] = head[..., :3][head_boundary]
    hair_boundary = zone & ~vis_head & (hair[..., 3] > 0)
    seed_rgb[hair_boundary] = hair[..., :3][hair_boundary]
    neck_fill = diffuse(neck_clean, seed_rgb)
    head[..., :3][neck_clean] = neck_fill[..., :3][neck_clean]
    head_reconstructed |= neck_clean

    # hair_back gold cleanup (strand diffusion within hair_back)
    if hair_gold.any():
        hz = np.zeros_like(U)
        hz[300:345, 455:500] = True
        srgb = np.zeros((CANVAS[1], CANVAS[0], 3), dtype=np.float64)
        hb_vis = hz & (hair[..., 3] > 0) & ~hair_gold
        srgb[hb_vis] = hair[..., :3][hb_vis]
        hh = hz & (hair[..., 3] == 0) & vis_head
        srgb[hh] = head[..., :3][hh]
        hfill = diffuse(hair_gold, srgb)
        hair[..., :3][hair_gold] = hfill[..., :3][hair_gold]

    # ---------------- 6. beard receiver ----------------
    by0, by1, bx0, bx1 = CLONE_BLOCK
    block = m[by0:by1, bx0:bx1]
    block_dark = (block[..., 0] < 90) & (block[..., 1] < 75) & (block[..., 2] < 70)
    assert block_dark.all(), "clone block contains non-beard pixels"
    beard = np.zeros((CANVAS[1], CANVAS[0], 4), dtype=np.uint8)
    beard[..., :3] = m[..., :3]
    beard[..., 3] = np.where(beard_region, mal, 0)
    # receiver content inside M: beard texture from the verified block
    yy, xx = np.nonzero(M)
    beard[yy, xx, :3] = clone_fill(m, yy, xx)
    # R1-02: underdraw the moustache footprint inside the beard too
    ink_beard = U & beard_region & ~M
    yy, xx = np.nonzero(ink_beard)
    beard[yy, xx, :3] = clone_fill(m, yy, xx)
    beard_reconstructed = M | ink_beard
    print("beard: region=%d M=%d ink_beard=%d" % (
        beard_region.sum(), M.sum(), ink_beard.sum()))

    # ---------------- 7. lower-face patches ----------------
    neutral = np.zeros((CANVAS[1], CANVAS[0], 4), dtype=np.uint8)
    neutral[..., :3] = m[..., :3]
    neutral[..., 3] = np.where(P, mal, 0)

    # R1-02: patch underlay beneath the moustache = art diffusion from the
    # surrounding master art around the mouth. U pixels outside P are added
    # to the diffusion region (invisible in the patch) so the moustache ink
    # above P does not leak into the patch fill.
    patch_ink = P & U
    print("patch moustache-footprint underdraw px:", int(patch_ink.sum()))
    pbox = np.zeros_like(U)
    pbox[222:279, 492:591] = True
    p_buffer = pbox & U & ~P
    p_field = diffuse(patch_ink | p_buffer, m[..., :3].astype(np.float64))
    neutral[..., :3][patch_ink] = p_field[..., :3][patch_ink]

    # R1-03: small-open test — part the lips at the actual parting line
    opent = neutral.copy()
    opening = np.zeros_like(P)
    gap_dark = np.array([8, 6, 6], dtype=np.float64)
    for x in range(531, 554):
        col = m[237:244, x, 0]
        ly = 237 + int(np.argmin(col))
        line_col = m[ly, x, :3].astype(np.float64)
        gap_col = 0.55 * line_col + 0.45 * gap_dark
        if 536 <= x <= 548:
            rows = [ly - 1, ly, ly + 1]
        else:
            rows = [ly, ly + 1]
        for y in rows:
            if y < 226 or y >= CANVAS[1] or not P[y, x] or U[y, x]:
                continue
            if y == ly:
                rgb = gap_col
            else:
                rgb = 0.65 * gap_col + 0.35 * m[y, x, :3].astype(np.float64)
            opent[y, x, :3] = np.clip(np.round(rgb), 0, 255).astype(np.uint8)
            opening[y, x] = True
    print("open patch opening px:", int(opening.sum()))

    # ---------------- 8. moustache decontamination (R1-01/R1-02) ----------------
    # underlay render for the solve: neutral group without the moustache
    under_layers = [hair, head, v2_sprites["ear_right"], v2_sprites["ear_left"],
                    beard, neutral, v2_sprites["nose"], v2_sprites["eye_right"],
                    v2_sprites["eye_left"], v2_sprites["eyebrow_right"],
                    v2_sprites["eyebrow_left"]]
    u_img = compose(under_layers)
    u = np.asarray(u_img, dtype=np.uint8).copy()
    np.save(V4 + "/code/_u_neutral.npy", u)
    edom = erode(dom & master_vis, 1)

    moust = v2_sprites["moustache"].copy()
    mo_src = np.zeros((CANVAS[1], CANVAS[0]), dtype=bool)
    mo_rec = np.zeros((CANVAS[1], CANVAS[0]), dtype=bool)
    kept = dropped = solved = fallback = guarded = 0
    solve_errs = []
    ys, xs = np.nonzero(U)
    for y, x in zip(ys, xs):
        B0 = m[y, x, :3]
        u_px = u[y, x, :3]
        u_a = int(u[y, x, 3])
        faithful = ink_head[y, x] or patch_ink[y, x]
        if u_a < 250 and edom[y, x]:
            guarded += 1
            continue  # keep verbatim (coverage guard)
        if not faithful:
            # underlay beneath is clone texture (not a faithful u0 estimate):
            # keep verbatim; comp over dark clone stays within ~2 of master
            kept += 1
            mo_src[y, x] = True
            continue
        res = solve_moustache_px(B0, u_px)
        if res is None:
            kept += 1
            mo_src[y, x] = True
            continue
        alpha, rgb, err = res
        c = alpha / 255.0
        if err > 2.0:
            # cannot represent as an ink blend over our underlay: keep source
            fallback += 1
            solve_errs.append((int(x), int(y), float(err)))
            mo_src[y, x] = True
            continue
        if c >= 0.97:
            kept += 1
            mo_src[y, x] = True
        elif c <= 0.02 and np.abs(u_px.astype(int) - B0.astype(int)).max() <= 2:
            # pure underlay showing through the old matte: drop only when
            # the reconstructed underlay actually reproduces the master
            moust[y, x, 3] = 0
            dropped += 1
        else:
            moust[y, x, 0] = rgb[0]
            moust[y, x, 1] = rgb[1]
            moust[y, x, 2] = rgb[2]
            moust[y, x, 3] = alpha
            solved += 1
            mo_rec[y, x] = True
    print("moustache: kept=%d dropped=%d solved=%d fallback=%d guarded=%d" % (
        kept, dropped, solved, fallback, guarded))
    if solve_errs:
        print("  fallback px (err):", solve_errs[:12])

    # ---------------- 9. save everything ----------------
    sprites = {
        "head_base": (head, "head/head_base.png"),
        "hair_back": (hair, "head/hair_back.png"),
        "diadem_gold": (diadem, "head/diadem_gold.png"),
        "ear_left": (v2_sprites["ear_left"], "face/ear_left.png"),
        "ear_right": (v2_sprites["ear_right"], "face/ear_right.png"),
        "eye_left": (v2_sprites["eye_left"], "face/eye_left.png"),
        "eye_right": (v2_sprites["eye_right"], "face/eye_right.png"),
        "eyebrow_left": (v2_sprites["eyebrow_left"], "face/eyebrow_left.png"),
        "eyebrow_right": (v2_sprites["eyebrow_right"], "face/eyebrow_right.png"),
        "nose": (v2_sprites["nose"], "face/nose.png"),
        "beard": (beard, "face/beard.png"),
        "moustache": (moust, "face/moustache.png"),
        "lower_face_neutral": (neutral, "mouths/lower_face_neutral.png"),
        "lower_face_open_test": (opent, "mouths/lower_face_open_test.png"),
    }

    meta = {}
    for sid, (arr, rel) in sprites.items():
        save_rgba(arr, V4 + "/" + rel)
        save_mask_L(arr[..., 3], V4 + "/masks/" + sid + ".png")
        vis = arr[..., 3] > 0
        if sid == "beard":
            rec = vis & beard_reconstructed
        elif sid == "head_base":
            rec = vis & head_reconstructed
        elif sid == "hair_back":
            rec = vis & hair_gold
        elif sid == "lower_face_open_test":
            rec = vis & (opening | patch_ink)
        elif sid == "lower_face_neutral":
            rec = vis & patch_ink
        elif sid == "moustache":
            rec = vis & mo_rec
        else:
            rec = np.zeros_like(vis)
        # source claim: exact master RGB and alpha <= master alpha
        rgb_eq = (arr[..., :3] == m[..., :3]).all(axis=2)
        al_le = arr[..., 3] <= mal
        src = vis & ~rec & rgb_eq & al_le
        leftover = vis & ~rec & ~src
        if leftover.any():
            print("  WARNING %s: %d visible px neither source nor rec" % (
                sid, leftover.sum()))
        save_binary(src, V4 + "/provenance/" + sid + "__source.png")
        save_binary(rec, V4 + "/provenance/" + sid + "__reconstructed.png")
        meta[sid] = {
            "visible": int(vis.sum()),
            "source": int(src.sum()),
            "reconstructed": int(rec.sum()),
            "bbox": alpha_bbox(arr[..., 3]),
        }
        print("%-22s vis=%6d src=%6d rec=%5d bbox=%s" % (
            sid, meta[sid]["visible"], meta[sid]["source"],
            meta[sid]["reconstructed"], meta[sid]["bbox"]))

    with open(V2 + "/masks/visible_head_domain.png", "rb") as f:
        dom_bytes = f.read()
    with open(V4 + "/masks/visible_head_domain.png", "wb") as f:
        f.write(dom_bytes)

    np.save(V4 + "/code/_M.npy", M)
    np.save(V4 + "/code/_P.npy", P)
    np.save(V4 + "/code/_U.npy", U)
    np.save(V4 + "/code/_opening.npy", opening)
    np.save(V4 + "/code/_beard_region.npy", beard_region)
    np.save(V4 + "/code/_head_region.npy", head_region)
    np.save(V4 + "/code/_ink_head.npy", ink_head)
    np.save(V4 + "/code/_ink_beard.npy", ink_beard)
    np.save(V4 + "/code/_patch_ink.npy", patch_ink)
    np.save(V4 + "/code/_neck_clean.npy", neck_clean)
    np.save(V4 + "/code/_mo_src.npy", mo_src)
    np.save(V4 + "/code/_mo_rec.npy", mo_rec)
    with open(V4 + "/code/_sprite_meta.json", "w") as f:
        json.dump(meta, f, indent=2)
    print("stage 10 complete")


if __name__ == "__main__":
    main()
