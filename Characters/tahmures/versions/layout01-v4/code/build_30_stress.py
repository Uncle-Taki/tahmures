#!/usr/bin/env python3
"""Layout01 v4 repair — stage 30: micro-motion stress samples.

Envelope (front-view only, per submission contract):
- each lower-face patch (neutral, open_test) at (0,0), (+2,0), (-2,0), (0,+2), (0,-2);
- moustache independently at (+1,0), (-1,0), (0,+1), (0,-1) over both patch states.

Checks per sample:
- coverage inside the one-pixel eroded immutable domain: zero new fully
  transparent pixels where the master is visible, zero alpha<250 where the
  master alpha is >= 250;
- composition changes confined to the union of the moved sprite's original and
  shifted footprint;
- for patch shifts, the receiver revealed inside M renders as cloned beard
  texture (dark), never as residual master mouth content;
- for moustache shifts (R1-02): the vacated strip must render EXACTLY as the
  unchanged layers beneath (no baked outline, no doubled edge, no halo);
- baseline (0,0) samples byte-identical to the unadorned previews.

This is a limited front-view micro-offset envelope. It is NOT evidence that
perspective turns, rotation, or unrestricted articulation are safe.
"""
import json
import os
import numpy as np
from PIL import Image

from build_lib import V4, CANVAS, load_master, load_domain, compose, erode, shifted

PATCH_OFFSETS = [(0, 0), (2, 0), (-2, 0), (0, 2), (0, -2)]
MOUSTACHE_OFFSETS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

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
    return np.asarray(Image.open(V4 + "/" + REL[sid]).convert("RGBA")).copy()


def build_state(patch_id, patch_dxy, moustache_dxy):
    ids = list(LAYER_ORDER)
    if patch_id:
        ids.insert(PATCH_POS, patch_id)
    layers = {}
    for sid in ids:
        layers[sid] = load_sprite(sid)
    if patch_id and patch_dxy != (0, 0):
        layers[patch_id] = shifted(layers[patch_id], patch_dxy[0], patch_dxy[1])
    if moustache_dxy != (0, 0):
        layers["moustache"] = shifted(layers["moustache"], moustache_dxy[0], moustache_dxy[1])
    return compose([layers[i] for i in ids])


def coverage(comp, master, dom):
    cal = np.asarray(comp)[..., 3]
    er = erode(dom, 1)
    holes = int((er & (master[..., 3] > 0) & (cal == 0)).sum())
    deficits = int((er & (master[..., 3] >= 250) & (cal < 250)).sum())
    return holes, deficits


def underlay_for(patch_id):
    """Composite of all layers except the moustache (the true underlay)."""
    ids = list(LAYER_ORDER)
    ids.remove("moustache")
    if patch_id:
        ids.insert(PATCH_POS, patch_id)
    return np.asarray(compose([load_sprite(i) for i in ids]))


def main():
    os.makedirs(V4 + "/previews/stress", exist_ok=True)
    m = load_master()
    dom = load_domain()
    M = np.load(V4 + "/code/_M.npy")
    P = np.load(V4 + "/code/_P.npy")
    U = np.load(V4 + "/code/_U.npy")
    moust_a = load_sprite("moustache")[..., 3] > 0

    patch_states = [("lower_face_neutral", "neutral"), ("lower_face_open_test", "open_test")]
    base_comp = {}
    for pid, pname in patch_states:
        base_comp[pname] = np.asarray(
            Image.open(V4 + "/previews/%s.png" % pname).convert("RGBA"))

    samples = []

    def record(name, group, moved, offset, comp, base, allowed):
        path = "previews/stress/%s.png" % name
        comp.save(V4 + "/" + path)
        ca = np.asarray(comp)
        holes, deficits = coverage(comp, m, dom)
        diff = (ca != base).any(axis=2)
        outside = diff & ~allowed
        entry = {
            "name": name,
            "render_group": group,
            "moved_sprite": moved,
            "offset_px": {"x": offset[0], "y": offset[1]},
            "coverage": {
                "new_fully_transparent_interior": holes,
                "alpha_below_250_where_source_opaque": deficits,
            },
            "changed_px_vs_base_state": int(diff.sum()),
            "changes_confined_to_moved_footprint": not bool(outside.any()),
            "path": path,
        }
        print("%-34s holes=%d deficits=%d diff=%5d confined=%s" % (
            name, holes, deficits, entry["changed_px_vs_base_state"],
            entry["changes_confined_to_moved_footprint"]))
        return entry, ca

    # --- patch micro-offsets (10 samples) ---
    for pid, pname in patch_states:
        group = "puppet_core_neutral" if pname == "neutral" else "puppet_core_open_test"
        base = base_comp[pname]
        for dx, dy in PATCH_OFFSETS:
            comp = build_state(pid, (dx, dy), (0, 0))
            name = "patch-%s-dx%d-dy%d" % (pname, dx, dy)
            allowed = P | shifted(P, dx, dy)
            entry, ca = record(name, group, pid, (dx, dy), comp, base, allowed)
            if (dx, dy) == (0, 0):
                entry["byte_identical_to_preview"] = comp.tobytes() == base.tobytes()
            else:
                # receiver continuity: wherever M is revealed (patch moved away),
                # the composition must show cloned dark beard, not old mouth RGB
                revealed = M & ~shifted(P, dx, dy)
                vis = ca[..., 3] > 0
                leak = revealed & vis & ~(
                    (ca[..., 0] < 90) & (ca[..., 1] < 75) & (ca[..., 2] < 70))
                entry["revealed_receiver_px"] = int(revealed.sum())
                entry["revealed_receiver_all_dark"] = not bool(leak.any())
                if leak.any():
                    ys, xs = np.nonzero(leak)
                    entry["revealed_receiver_non_dark_px"] = int(leak.sum())
                    entry["leak_bbox"] = [int(xs.min()), int(ys.min()),
                                          int(xs.max()), int(ys.max())]
            samples.append(entry)

    # --- moustache micro-offsets over both patch states (8 samples) ---
    for pid, pname in patch_states:
        group = "puppet_core_neutral" if pname == "neutral" else "puppet_core_open_test"
        base = base_comp[pname]
        under = underlay_for(pid)
        for dx, dy in MOUSTACHE_OFFSETS:
            comp = build_state(pid, (0, 0), (dx, dy))
            name = "moustache-over-%s-dx%d-dy%d" % (pname, dx, dy)
            allowed = moust_a | shifted(moust_a, dx, dy)
            entry, ca = record(name, group, "moustache", (dx, dy), comp, base, allowed)
            # R1-02 ghost check: in the vacated strip (footprint the moved
            # moustache no longer covers) the render must equal the underlay
            # exactly — no baked outline, no halo, no exposed lip residue
            vacated = moust_a & ~shifted(moust_a, dx, dy)
            mismatch = (ca[vacated] != under[vacated]).any(axis=-1).sum() \
                if vacated.any() else 0
            entry["vacated_strip_px"] = int(vacated.sum())
            entry["vacated_strip_matches_underlay_exactly"] = int(mismatch) == 0
            entry["vacated_strip_mismatched_px"] = int(mismatch)
            if mismatch:
                print("   R1-02 VACATED MISMATCH at d(%d,%d): %d px" % (dx, dy, mismatch))
            samples.append(entry)

    doc = {
        "purpose": "Front-view micro-offset stress evidence for the Model-B "
                   "lower-face patch and static moustache foreground.",
        "revision": "layout01-v4 revision 1: adds the moustache vacated-strip "
                    "identity check (R1-02) over both patch states.",
        "envelope": {
            "lower_face_patch_offsets_px": [
                {"x": x, "y": y} for x, y in PATCH_OFFSETS],
            "moustache_offsets_px": [
                {"x": x, "y": y} for x, y in MOUSTACHE_OFFSETS],
            "patch_states": ["lower_face_neutral", "lower_face_open_test"],
            "receiver": "static mouthless beard receiver (cloned beard texture "
                        "inside mouth-content region M; moustache footprint "
                        "underdrawn in head_base/beard/patch)",
            "sample_count": len(samples),
        },
        "coverage_rule": "Inside the one-pixel eroded immutable visible-head "
                         "domain: zero new fully transparent pixels where the "
                         "master is visible; zero alpha<250 where master alpha "
                         "is >=250. Intrinsic antialiasing preserved; boundary "
                         "pixels are not forced opaque.",
        "confinement_rule": "Composition changes vs the same-state (0,0) base "
                            "must stay inside the union of the moved sprite's "
                            "original and shifted footprint.",
        "vacated_strip_rule": "Where the shifted moustache no longer covers its "
                              "original footprint, the render must equal the "
                              "moustache-free underlay byte-exactly (no baked "
                              "outline, halo, or lip residue).",
        "claims": "Limited front-view micro-offset envelope only. No perspective "
                  "turn, rotation, viseme library, or unrestricted gap-free "
                  "animation is claimed. Whole-head rigidity is not evidence "
                  "that local facial joints are safe.",
        "samples": samples,
        "all_coverage_pass": all(
            s["coverage"]["new_fully_transparent_interior"] == 0
            and s["coverage"]["alpha_below_250_where_source_opaque"] == 0
            for s in samples),
        "all_confined": all(s["changes_confined_to_moved_footprint"] for s in samples),
        "all_receiver_dark": all(
            s.get("revealed_receiver_all_dark", True) for s in samples),
        "all_vacated_strips_exact": all(
            s.get("vacated_strip_matches_underlay_exactly", True) for s in samples),
    }
    doc["all_passed"] = (doc["all_coverage_pass"] and doc["all_confined"]
                         and doc["all_receiver_dark"]
                         and doc["all_vacated_strips_exact"]
                         and all(s.get("byte_identical_to_preview", True)
                                 for s in samples))
    with open(V4 + "/stress-tests.json", "w") as f:
        json.dump(doc, f, indent=2)
    print("samples=%d coverage_pass=%s confined=%s receiver_dark=%s vacated_exact=%s ALL=%s" % (
        len(samples), doc["all_coverage_pass"], doc["all_confined"],
        doc["all_receiver_dark"], doc["all_vacated_strips_exact"], doc["all_passed"]))
    assert doc["all_passed"], "stress envelope failed"
    print("stage 30 complete")


if __name__ == "__main__":
    main()
