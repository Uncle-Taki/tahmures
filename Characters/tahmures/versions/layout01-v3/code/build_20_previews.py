#!/usr/bin/env python3
"""Layout01 v3 repair — stage 20: compose states A/B/C, save previews, verify coverage.

Compositions (bottom -> top):
  hair_back, head_base, ear_right, ear_left, beard, [patch], nose, eye_right,
  eye_left, eyebrow_right, eyebrow_left, moustache, diadem_gold
"""
import os
import numpy as np
from PIL import Image

from build_lib import V3, CANVAS, load_master, load_domain, compose, erode

LAYER_ORDER = [
    "hair_back", "head_base", "ear_right", "ear_left", "beard",
    "nose", "eye_right", "eye_left", "eyebrow_right", "eyebrow_left",
    "moustache", "diadem_gold",
]
PATCH_POS = 5  # after beard, before nose


def load_sprite(sid):
    rel = {"head_base": "head/head_base.png", "hair_back": "head/hair_back.png",
           "diadem_gold": "head/diadem_gold.png"}.get(sid)
    if rel is None:
        rel = {"ear_left": "face/ear_left.png", "ear_right": "face/ear_right.png",
               "eye_left": "face/eye_left.png", "eye_right": "face/eye_right.png",
               "eyebrow_left": "face/eyebrow_left.png", "eyebrow_right": "face/eyebrow_right.png",
               "nose": "face/nose.png", "beard": "face/beard.png",
               "moustache": "face/moustache.png",
               "lower_face_neutral": "mouths/lower_face_neutral.png",
               "lower_face_open_test": "mouths/lower_face_open_test.png"}[sid]
    return np.asarray(Image.open(V3 + "/" + rel).convert("RGBA"))


def build_group(patch_id=None):
    ids = list(LAYER_ORDER)
    if patch_id:
        ids.insert(PATCH_POS, patch_id)
    layers = [load_sprite(i) for i in ids]
    return compose(layers), ids


def coverage_report(comp, master, dom, label):
    cal = np.asarray(comp)[..., 3]
    er = erode(dom, 1)
    holes = int((er & (master[..., 3] > 0) & (cal == 0)).sum())
    deficits = int((er & (master[..., 3] >= 250) & (cal < 250)).sum())
    print("%s: eroded-domain holes=%d alpha-deficits=%d" % (label, holes, deficits))
    return holes, deficits


def main():
    os.makedirs(V3 + "/previews", exist_ok=True)
    m = load_master()
    dom = load_domain()

    results = {}
    for patch, name, key in ((None, "mouthless", "A"),
                             ("lower_face_neutral", "neutral", "B"),
                             ("lower_face_open_test", "open_test", "C")):
        comp, ids = build_group(patch)
        comp.save(V3 + "/previews/%s.png" % name)
        holes, deficits = coverage_report(comp, m, dom, "state %s (%s)" % (key, name))
        results[name] = {"holes": holes, "deficits": deficits, "order": ids}

        ca = np.asarray(comp)
        # RGB comparison with the master where both are opaque (per pixel:
        # a pixel counts once, using its largest channel difference)
        both = (ca[..., 3] >= 250) & (m[..., 3] >= 250)
        diff = np.abs(ca[..., :3].astype(int) - m[..., :3].astype(int)).max(axis=2)
        dmax = int(diff[both].max()) if both.any() else 0
        dn = int((diff[both] > 3).sum())
        print("   RGB vs master (both opaque): max=%d, >3 diff px=%d of %d" % (
            dmax, dn, int(both.sum())))
        # where are the diffs?
        if dn:
            bad = both & (diff > 3)
            ys, xs = np.nonzero(bad)
            print("   diff bbox: x %d..%d y %d..%d" % (
                xs.min(), xs.max(), ys.min(), ys.max()))

    # B vs C must differ only inside the patch footprint
    B = np.asarray(Image.open(V3 + "/previews/neutral.png").convert("RGBA"))
    C = np.asarray(Image.open(V3 + "/previews/open_test.png").convert("RGBA"))
    P = np.load(V3 + "/code/_P.npy")
    M = np.load(V3 + "/code/_M.npy")
    opening = np.load(V3 + "/code/_opening.npy")
    bc = (B != C).any(axis=2)
    outside = bc & ~P
    print("B vs C: differing px=%d, outside patch footprint=%d" % (
        int(bc.sum()), int(outside.sum())))
    assert not outside.any(), "B/C differences escape the patch footprint"

    # A must differ from the master only inside the mouth-content region M,
    # C only inside the synthesized opening (B is pixel-exact)
    A = np.asarray(Image.open(V3 + "/previews/mouthless.png").convert("RGBA"))
    for label, arr, allowed in (("A", A, M), ("C", C, opening)):
        both = (arr[..., 3] >= 250) & (m[..., 3] >= 250)
        d = np.abs(arr[..., :3].astype(int) - m[..., :3].astype(int)).max(axis=2)
        bad = both & (d > 3)
        esc = bad & ~allowed
        print("state %s: >3 diff px=%d, escaping intended region=%d" % (
            label, int(bad.sum()), int(esc.sum())))
        assert not esc.any(), label + " differences escape the intended region"

    import json
    with open(V3 + "/code/_compose_meta.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
