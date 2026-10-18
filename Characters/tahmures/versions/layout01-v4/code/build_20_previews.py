#!/usr/bin/env python3
"""Layout01 v4 repair — stage 20: compose states A/B/C, save previews, verify.

Compositions (bottom -> top), identical to the accepted v3 group orders:
  hair_back, head_base, ear_right, ear_left, beard, [patch], nose, eye_right,
  eye_left, eyebrow_right, eyebrow_left, moustache, diadem_gold

Intended-difference accounting for revision 1:
- B (neutral): master-exact everywhere except the R1-04 neck cleanup zone
  (garment colours replaced by reconstructed strand continuation);
- A (mouthless): additionally differs inside the mouth receiver M, the
  moustache-footprint underdraw (ink_head/ink_beard/patch_ink) and the
  decontaminated moustache edge (R1-01/R1-02);
- C (open_test): differs from B only inside the synthesized lip opening.
"""
import json
import os
import numpy as np
from PIL import Image

from build_lib import (
    V4, CANVAS, load_master, load_domain, compose, erode, dilate,
)

LAYER_ORDER = [
    "hair_back", "head_base", "ear_right", "ear_left", "beard",
    "nose", "eye_right", "eye_left", "eyebrow_right", "eyebrow_left",
    "moustache", "diadem_gold",
]
PATCH_POS = 5  # after beard, before nose

REL = {
    "head_base": "head/head_base.png",
    "hair_back": "head/hair_back.png",
    "diadem_gold": "head/diadem_gold.png",
    "ear_left": "face/ear_left.png",
    "ear_right": "face/ear_right.png",
    "eye_left": "face/eye_left.png",
    "eye_right": "face/eye_right.png",
    "eyebrow_left": "face/eyebrow_left.png",
    "eyebrow_right": "face/eyebrow_right.png",
    "nose": "face/nose.png",
    "beard": "face/beard.png",
    "moustache": "face/moustache.png",
    "lower_face_neutral": "mouths/lower_face_neutral.png",
    "lower_face_open_test": "mouths/lower_face_open_test.png",
}


def load_sprite(sid):
    return np.asarray(Image.open(V4 + "/" + REL[sid]).convert("RGBA"))


def build_group(patch_id=None):
    ids = list(LAYER_ORDER)
    if patch_id:
        ids.insert(PATCH_POS, patch_id)
    layers = [load_sprite(i) for i in ids]
    return compose(layers), ids


def main():
    os.makedirs(V4 + "/previews", exist_ok=True)
    m = load_master()
    mal = m[..., 3]
    dom = load_domain()

    M = np.load(V4 + "/code/_M.npy")
    P = np.load(V4 + "/code/_P.npy")
    U = np.load(V4 + "/code/_U.npy")
    opening = np.load(V4 + "/code/_opening.npy")
    ink_head = np.load(V4 + "/code/_ink_head.npy")
    ink_beard = np.load(V4 + "/code/_ink_beard.npy")
    patch_ink = np.load(V4 + "/code/_patch_ink.npy")
    neck_clean = np.load(V4 + "/code/_neck_clean.npy")

    # intended repair zones (dilated 1px to absorb compositing rounding)
    neck_zone = dilate(neck_clean, 1)
    strip_zone = np.zeros_like(U)
    strip_zone[300:370, 460:612] = True
    neck_zone |= strip_zone
    a_zone = dilate(M | ink_head | ink_beard | patch_ink | U, 1) | neck_zone

    edom = erode(dom & (mal > 0), 1)
    results = {}
    for patch, name, key in ((None, "mouthless", "A"),
                             ("lower_face_neutral", "neutral", "B"),
                             ("lower_face_open_test", "open_test", "C")):
        comp, ids = build_group(patch)
        comp.save(V4 + "/previews/%s.png" % name)
        ca = np.asarray(comp)
        cal = ca[..., 3]

        holes = int((edom & (mal > 0) & (cal == 0)).sum())
        deficits = int((edom & (mal >= 250) & (cal < 250)).sum())
        print("state %s (%s): holes=%d deficits=%d" % (key, name, holes, deficits))
        assert holes == 0 and deficits == 0, key + " coverage failure"

        both = (cal >= 250) & (mal >= 250)
        diff = np.abs(ca[..., :3].astype(int) - m[..., :3].astype(int)).max(axis=2)
        bad = both & (diff > 3)
        allowed = a_zone if key in ("A", "B") else (a_zone | dilate(opening, 1))
        if key == "B":
            allowed = neck_zone
        esc = bad & ~allowed
        print("   RGB vs master: >3 diff px=%d (intended), escaping=%d, max=%d" % (
            int(bad.sum()), int(esc.sum()),
            int(diff[both].max()) if both.any() else 0))
        assert not esc.any(), key + " differences escape the intended zones"
        results[name] = {
            "holes": holes, "deficits": deficits, "order": ids,
            "rgb_diff_gt3_total": int(bad.sum()),
            "rgb_diff_gt3_escaping_intended_zone": int(esc.sum()),
        }

    # B vs C must differ only inside the opening
    B = np.asarray(Image.open(V4 + "/previews/neutral.png").convert("RGBA"))
    C = np.asarray(Image.open(V4 + "/previews/open_test.png").convert("RGBA"))
    bc = (B != C).any(axis=2)
    outside = bc & ~P
    in_open = bc & opening
    in_p_not_open = bc & P & ~opening
    print("B vs C: differing px=%d, outside P=%d, in opening=%d, in P not opening=%d" % (
        int(bc.sum()), int(outside.sum()), int(in_open.sum()), int(in_p_not_open.sum())))
    assert not outside.any(), "B/C differences escape the patch footprint"
    assert int(in_p_not_open.sum()) == 0, "B/C differ inside P outside the opening"
    results["b_vs_c"] = {
        "differing_px": int(bc.sum()),
        "outside_patch_footprint": int(outside.sum()),
        "inside_opening": int(in_open.sum()),
    }

    # state A: no warm residue over the mouthless receiver (R1-01)
    A = np.asarray(Image.open(V4 + "/previews/mouthless.png").convert("RGBA"))
    warm = (A[..., 0] >= 140) & (A[..., 0] - A[..., 2] >= 55) & (A[..., 3] > 0)
    crescent = int(warm[230:237, 530:542].sum())
    clone_zone = M | ink_beard
    warm_clone = int((warm & clone_zone).sum())
    print("state A warm residue: crescent bbox=%d, over clone zone=%d" % (
        crescent, warm_clone))
    assert crescent == 0 and warm_clone == 0, "R1-01 warm residue remains"
    results["r1_01"] = {
        "warm_px_crescent_bbox_530_230_542_237": crescent,
        "warm_px_over_mouthless_receiver": warm_clone,
    }

    with open(V4 + "/code/_compose_meta.json", "w") as f:
        json.dump(results, f, indent=2)
    print("stage 20 complete")


if __name__ == "__main__":
    main()
