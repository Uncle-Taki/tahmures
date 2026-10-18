#!/usr/bin/env python3
"""Layout01 v3 repair — stage 10: construct all sprites, masks, provenance.

Architecture B_LOCAL_LOWER_FACE_PATCH:
- beard is the continuous outer beard + mouthless receiver (master pixels
  everywhere except the mouth content region M, which is filled with beard
  texture cloned from a verified all-dark beard block below the mouth);
- lower_face_neutral / lower_face_open_test are swappable patches carrying the
  master mouth pixels (open variant synthesises a restrained small opening);
- head_base is rebuilt from master pixels following the true skin/neck
  silhouette inside the immutable head domain (fixing the v2 rectangular cheek
  cuts and neck gaps), with eye/eyebrow/nose footprints inpainted as feature
  underdraw; no body artwork is extracted;
- hair_back and diadem_gold are extended with previously uncovered master
  pixels (top hair edge, right-side strands, lower hair mass, diadem band);
- ears/eyes/brows/nose/moustache are reused verbatim from v2.
"""
import json
import os
import numpy as np
from PIL import Image

from build_lib import (
    V2, V3, CANVAS, load_master, load_v2, load_domain, save_rgba, save_mask_L,
    save_binary, dilate, erode, nearest_class, alpha_bbox,
)

# verified all-dark beard block used as receiver clone source (checked at runtime)
CLONE_BLOCK = (270, 293, 494, 604)  # y0, y1 (exclusive), x0, x1 (exclusive)


def main():
    for d in ("head", "face", "mouths", "masks", "provenance"):
        os.makedirs(V3 + "/" + d, exist_ok=True)

    m = load_master()
    mal = m[..., 3]
    master_vis = mal > 0
    dom = load_domain()

    # ---------------- v2 sprites ----------------
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

    # ---------------- 1. uncovered pixel assignment ----------------
    unc = dom & master_vis & ~covered
    print("uncovered domain pixels vs v2 sprites:", int(unc.sum()))

    gold_zone = dilate(v2_sprites["diadem_gold"][..., 3] > 0, 4)
    hair_extra = np.zeros_like(unc)
    diadem_extra = np.zeros_like(unc)
    head_extra = np.zeros_like(unc)
    beard_extra = np.zeros_like(unc)
    ys, xs = np.nonzero(unc)
    for y, x in zip(ys, xs):
        cls = nearest_class(m[y, x, :3].astype(np.int32))
        if y <= 40:
            # crown hair above the diadem band
            target = "hair" if cls in ("dark", "black") else (
                "diadem" if cls == "gold" else "head")
        elif y <= 130:
            # diadem band: gold elements and their outlines/shadows; hair shows
            # between the elements; forehead skin sits under the band edges
            if cls == "gold" or (cls in ("dark", "black") and gold_zone[y, x]):
                target = "diadem"
            elif cls == "skin":
                target = "head"
            else:
                target = "hair"
        elif 215 <= y <= 325 and 455 <= x <= 615:
            target = "beard"
        elif y >= 326 and cls == "gold":
            # neck-side garment/ornament pixels; no garment sprite in this phase
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
    print("assignment: hair+%d diadem+%d head+%d beard+%d" % (
        hair_extra.sum(), diadem_extra.sum(), head_extra.sum(), beard_extra.sum()))

    # ---------------- 2. mouth content region M and patch footprint P ----------------
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
    print("M px:", int(M.sum()), "P px:", int(P.sum()))
    ys, xs = np.nonzero(M)
    print("M bbox: x %d..%d y %d..%d" % (xs.min(), xs.max(), ys.min(), ys.max()))

    skin = (m[..., 0] >= 190) & (m[..., 1] >= 120) & (m[..., 2] <= 165) & \
        (m[..., 0] - m[..., 2] >= 60) & (m[..., 1] < m[..., 0]) & master_vis
    mouth_box = np.zeros_like(skin)
    mouth_box[228:268, 500:582] = True
    missing_skin = skin & mouth_box & ~M
    print("mouth skin pixels not in M:", int(missing_skin.sum()))

    # ---------------- 3. hair_back ----------------
    hair = v2_sprites["hair_back"].copy()
    hair[..., :3][hair_extra] = m[..., :3][hair_extra]
    hair[..., 3][hair_extra] = mal[hair_extra]
    print("hair_back: %d -> %d px" % (
        int((v2_sprites["hair_back"][..., 3] > 0).sum()), int((hair[..., 3] > 0).sum())))

    # ---------------- 4. diadem_gold ----------------
    diadem = v2_sprites["diadem_gold"].copy()
    diadem[..., :3][diadem_extra] = m[..., :3][diadem_extra]
    diadem[..., 3][diadem_extra] = mal[diadem_extra]
    print("diadem_gold: %d -> %d px" % (
        int((v2_sprites["diadem_gold"][..., 3] > 0).sum()), int((diadem[..., 3] > 0).sum())))

    # ---------------- 5. beard receiver ----------------
    beard_region = (v2_sprites["beard"][..., 3] > 0) | beard_extra | dilate(M, 4)
    # verify the clone block is entirely dark beard (no skin/gold leakage)
    by0, by1, bx0, bx1 = CLONE_BLOCK
    block = m[by0:by1, bx0:bx1]
    block_dark = (block[..., 0] < 90) & (block[..., 1] < 75) & (block[..., 2] < 70)
    assert block_dark.all(), "clone block contains non-beard pixels"
    beard = np.zeros((CANVAS[1], CANVAS[0], 4), dtype=np.uint8)
    beard[..., :3] = m[..., :3]
    beard[..., 3] = np.where(beard_region, mal, 0)
    # receiver content inside M: beard texture tiled from the verified block
    yy, xx = np.nonzero(M)
    src_y = by0 + ((yy - 228) % (by1 - by0))
    src_x = np.clip(xx, bx0, bx1 - 1)
    beard[yy, xx, :3] = m[src_y, src_x, :3]
    beard_source = beard_region & ~M
    print("beard: region %d px (source %d, reconstructed %d)" % (
        int(beard_region.sum()), int(beard_source.sum()), int(M.sum())))

    # ---------------- 6. head_base (domain-bounded skin/neck underlay) ----------------
    hair_a = hair[..., 3] > 0
    beard_a = beard[..., 3] > 0
    diadem_a = diadem[..., 3] > 0
    head_region = dom & master_vis & ~hair_a & ~beard_a & ~diadem_a
    head = np.zeros((CANVAS[1], CANVAS[0], 4), dtype=np.uint8)
    head[..., :3] = m[..., :3]
    head[..., 3] = np.where(head_region, mal, 0)
    print("head_base: region %d px" % int(head_region.sum()))

    # feature underdraw: inpaint the solid interiors of eye/brow/nose
    # footprints with Laplacian diffusion seeded from the surrounding master
    # skin. Soft feature edges (alpha < 252) keep master RGB in head_base so
    # the feature sprite's own antialiased alpha composites to the exact
    # master colour; solid interiors bleed at most 0.8% of the underlay.
    feat = np.zeros_like(head_region)
    for fid in ("eye_left", "eye_right", "eyebrow_left", "eyebrow_right", "nose"):
        feat |= v2_sprites[fid][..., 3] >= 252
    feat &= head_region
    print("feature underdraw region:", int(feat.sum()))
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
    print("head_base reconstructed (feature underdraw):", int(head_reconstructed.sum()))

    # ---------------- 7. lower-face patches ----------------
    neutral = np.zeros((CANVAS[1], CANVAS[0], 4), dtype=np.uint8)
    neutral[..., :3] = m[..., :3]
    neutral[..., 3] = np.where(P, mal, 0)

    opent = neutral.copy()
    opening = np.zeros_like(P)
    for x in range(531, 554):
        ly = None
        for y in range(249, 255):
            if m[y, x, 0] < 45 and m[y, x, 1] < 40 and m[y, x, 2] < 40:
                ly = y
                break
        if ly is None:
            ly = 252
        t = (x - 542) / 11.5
        d = int(round(5.5 * max(0.0, 1.0 - t * t)))
        if d <= 0:
            continue
        line_col = np.array(m[ly, x, :3], dtype=np.float64)
        for k in range(1, d + 1):
            y = ly + k
            if not (0 <= y < CANVAS[1]) or not P[y, x]:
                continue
            opening[y, x] = True
            if k < d:
                src_y = min(CANVAS[1] - 1, y + 12)
                interior = m[src_y, x, :3].astype(np.float64)
                deep = 0.45 * line_col + 0.55 * interior
                opent[y, x, :3] = np.clip(np.round(deep), 0, 255).astype(np.uint8)
            else:
                below = m[min(CANVAS[1] - 1, y + 1), x, :3].astype(np.float64)
                edge = 0.75 * line_col + 0.25 * below
                opent[y, x, :3] = np.clip(np.round(edge), 0, 255).astype(np.uint8)
    print("open patch opening pixels:", int(opening.sum()))

    # ---------------- 8. save everything ----------------
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
        "moustache": (v2_sprites["moustache"], "face/moustache.png"),
        "lower_face_neutral": (neutral, "mouths/lower_face_neutral.png"),
        "lower_face_open_test": (opent, "mouths/lower_face_open_test.png"),
    }

    def source_mask_of(arr):
        a = arr[..., 3] > 0
        rgb_eq = (arr[..., :3] == m[..., :3]).all(axis=2)
        al_le = arr[..., 3] <= mal
        return a & rgb_eq & al_le

    meta = {}
    for sid, (arr, rel) in sprites.items():
        save_rgba(arr, V3 + "/" + rel)
        save_mask_L(arr[..., 3], V3 + "/masks/" + sid + ".png")
        vis = arr[..., 3] > 0
        if sid == "beard":
            rec = vis & M
        elif sid == "head_base":
            rec = vis & head_reconstructed
        elif sid == "lower_face_open_test":
            rec = vis & opening
        else:
            rec = np.zeros_like(vis)
        src = vis & ~rec
        save_binary(src, V3 + "/provenance/" + sid + "__source.png")
        save_binary(rec, V3 + "/provenance/" + sid + "__reconstructed.png")
        meta[sid] = {
            "visible": int(vis.sum()),
            "source": int(src.sum()),
            "reconstructed": int(rec.sum()),
            "bbox": alpha_bbox(arr[..., 3]),
        }
        print("%-22s vis=%6d src=%6d rec=%5d bbox=%s" % (
            sid, meta[sid]["visible"], meta[sid]["source"], meta[sid]["reconstructed"],
            meta[sid]["bbox"]))

    with open(V2 + "/masks/visible_head_domain.png", "rb") as f:
        dom_bytes = f.read()
    with open(V3 + "/masks/visible_head_domain.png", "wb") as f:
        f.write(dom_bytes)

    np.save(V3 + "/code/_M.npy", M)
    np.save(V3 + "/code/_P.npy", P)
    np.save(V3 + "/code/_opening.npy", opening)
    np.save(V3 + "/code/_beard_region.npy", beard_region)
    np.save(V3 + "/code/_head_region.npy", head_region)
    with open(V3 + "/code/_sprite_meta.json", "w") as f:
        json.dump(meta, f, indent=2)
    print("stage 10 complete")


if __name__ == "__main__":
    main()
