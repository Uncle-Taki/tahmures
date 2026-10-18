#!/usr/bin/env python3
"""Layout01 v3 repair — stage 70: independent local verification.

Re-composes the manifest-declared groups from the delivered component files
two ways — with PIL's alpha compositing (byte-exact against the saved
previews) and with an independent float implementation (must agree within
1/255 per channel) — and confirms masks, provenance, pivots, coverage,
fidelity and the immutable inputs. Results are written to
code/_verify_report.json and must all pass.
"""
import hashlib
import json
import os

import numpy as np
from PIL import Image

from build_lib import V2, V3, REPO, CANVAS, erode

ZIP_PATH = REPO + "/Characters/tahmures/tahmures_sprites_layout01_v2.zip"
MASTER_PATH = V2 + "/source/approved_master.png"
ZIP_SHA = "8dbe2832fe4b7728a954ae8c94ac4ca5ec5864584d7dfbbd8efd19be8e72e1f0"
MASTER_SHA = "3eedfaa5a41965c45a137a74a9137c6e59304a0604f877a81c98870c64dba2e5"
PREVIEW_OF = {
    "puppet_core": "mouthless",
    "puppet_core_neutral": "neutral",
    "puppet_core_open_test": "open_test",
}


def digest(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def compose_pil(paths):
    """RGBA composition via PIL (same engine class the previews were built with)."""
    out = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    for p in paths:
        out = Image.alpha_composite(out, Image.open(p).convert("RGBA"))
    return out


def compose_independent(paths):
    """Independent float64 premultiplied composition (rounding may differ by 1)."""
    out = np.zeros((CANVAS[1], CANVAS[0], 4), dtype=np.uint8)
    for p in paths:
        layer = np.asarray(Image.open(p).convert("RGBA")).astype(np.float64)
        la = layer[..., 3:4] / 255.0
        base = out.astype(np.float64)
        ba = base[..., 3:4] / 255.0
        out_a = la + (1 - la) * ba
        pm = layer[..., :3] * la + base[..., :3] * (1 - la) * ba
        safe = out_a > 0
        rgb = np.where(safe, pm / np.where(safe, out_a, 1), 0)
        out = np.concatenate(
            [np.clip(np.round(rgb), 0, 255),
             np.clip(np.round(out_a * 255), 0, 255)], axis=2
        ).astype(np.uint8)
    return out


def main():
    results = {}

    # immutable inputs unchanged
    results["zip_sha256_unchanged"] = digest(ZIP_PATH) == ZIP_SHA
    results["master_sha256_unchanged"] = digest(MASTER_PATH) == MASTER_SHA
    results["domain_copy_verbatim"] = (
        digest(V3 + "/masks/visible_head_domain.png")
        == digest(V2 + "/masks/visible_head_domain.png"))

    manifest = json.load(open(V3 + "/manifest.json"))
    sprites = {s["id"]: s for s in manifest["sprites"]}

    # masks equal exact alpha; bboxes and pivots as declared
    mask_ok, bbox_ok, pivot_ok = True, True, True
    for sid, s in sprites.items():
        im = Image.open(V3 + "/" + s["path"])
        mask = Image.open(V3 + "/" + s["mask_path"]).convert("L")
        if np.any(np.asarray(mask) != np.asarray(im.getchannel("A"))):
            mask_ok = False
        if list(im.getchannel("A").getbbox()) != s["alpha_bounding_rect"]:
            bbox_ok = False
        p = s["pivot"]
        if not (0 <= p["x"] < CANVAS[0] and 0 <= p["y"] < CANVAS[1]):
            pivot_ok = False
    results["masks_equal_exact_alpha"] = mask_ok
    results["bboxes_match_manifest"] = bbox_ok
    results["pivots_in_canvas"] = pivot_ok

    # provenance partition and source-pixel claims
    master = np.asarray(Image.open(MASTER_PATH).convert("RGBA"))
    prov_ok = True
    for sid, s in sprites.items():
        im = np.asarray(Image.open(V3 + "/" + s["path"]).convert("RGBA"))
        src = np.asarray(
            Image.open(V3 + "/" + s["provenance"]["source_pixel_mask"]).convert("L")) > 127
        rec = np.asarray(
            Image.open(V3 + "/" + s["provenance"]["reconstructed_pixel_mask"]).convert("L")) > 127
        vis = im[..., 3] > 0
        if (src & rec).any() or not np.array_equal(src | rec, vis):
            prov_ok = False
        src_rgb_eq = (im[..., :3] == master[..., :3]).all(axis=2)
        src_alpha_ok = im[..., 3] <= master[..., 3]
        if int((src & ~src_rgb_eq).sum()) or int((src & ~src_alpha_ok).sum()):
            prov_ok = False
    results["provenance_partition_and_source_claims"] = prov_ok

    # groups resolve; recomposition equals the unadorned previews
    groups = manifest["render_groups"]
    comp = {}
    for gname, group in groups.items():
        order = group["layer_order"]
        paths = [V3 + "/" + sprites[i]["path"] for i in order]
        pil_img = compose_pil(paths)
        comp[gname] = np.asarray(pil_img)
        prev = np.asarray(
            Image.open(V3 + "/" + manifest["previews"][PREVIEW_OF[gname]]).convert("RGBA"))
        results["recompose_%s_byte_equal_preview" % gname] = bool(
            pil_img.tobytes() == Image.fromarray(prev, "RGBA").tobytes())
        indep = compose_independent(paths)
        results["recompose_%s_independent_max_channel_diff" % gname] = int(
            np.abs(indep.astype(int) - prev.astype(int)).max())
        results["recompose_%s_sprite_count" % gname] = len(order)

    # B vs C: truly differ, only inside the patch footprint
    P = np.load(V3 + "/code/_P.npy")
    B, C = comp["puppet_core_neutral"], comp["puppet_core_open_test"]
    bc = (B != C).any(axis=2)
    results["B_and_C_truly_differ"] = bool(bc.any())
    results["B_C_diff_confined_to_P"] = not bool((bc & ~P).any())
    results["B_C_diff_px"] = int(bc.sum())

    # fidelity envelope vs master (per-pixel max channel diff > 3)
    both = (B[..., 3] >= 250) & (master[..., 3] >= 250)
    dB = np.abs(B[..., :3].astype(int) - master[..., :3].astype(int)).max(axis=2)
    results["B_pixel_faithful_gt3_px"] = int((dB[both] > 3).sum())

    # coverage in the one-pixel eroded domain for all three states
    dom = np.asarray(
        Image.open(V2 + "/masks/visible_head_domain.png").convert("L")) >= 127
    er = erode(dom, 1)
    for gname, c in comp.items():
        cal = c[..., 3]
        holes = int((er & (master[..., 3] > 0) & (cal == 0)).sum())
        deficits = int((er & (master[..., 3] >= 250) & (cal < 250)).sum())
        results["coverage_%s" % gname] = {"holes": holes, "deficits": deficits}

    # antialiasing preserved at the outer boundary: single-owner silhouette
    # keeps master alpha exactly (composition must not raise it)
    edge = (master[..., 3] > 0) & (master[..., 3] < 250)
    A = comp["puppet_core"]
    results["outer_boundary_alpha_raised_px"] = int(
        (A[..., 3][edge] > master[..., 3][edge]).sum())

    # no banned byte-identical images among rig components
    banned = set()
    for name in ("previews/default_pose_head_surface_source.png",
                 "previews/default_pose_beard_source.png",
                 "face/neutral_face_without_mouth.png",
                 "previews/layout01_source_head.png",
                 "previews/layout01_reconstructed_head.png"):
        banned.add(hashlib.sha256(
            Image.open(V2 + "/" + name).convert("RGBA").tobytes()).hexdigest())
    banned.add(hashlib.sha256(master.tobytes()).hexdigest())
    dup = [sid for sid, s in sprites.items() if hashlib.sha256(
        np.asarray(Image.open(V3 + "/" + s["path"]).convert("RGBA")).tobytes()
    ).hexdigest() in banned]
    results["no_banned_duplicate_components"] = not dup

    # stress evidence present and passing
    stress = json.load(open(V3 + "/stress-tests.json"))
    results["stress_samples_present"] = len(stress["samples"]) == 18 and all(
        os.path.isfile(V3 + "/" + s["path"]) for s in stress["samples"])
    results["stress_all_passed"] = bool(stress["all_passed"])

    # pass criteria
    def passes(key, val):
        if key.endswith("_byte_equal_preview") or key in (
                "zip_sha256_unchanged", "master_sha256_unchanged",
                "domain_copy_verbatim", "masks_equal_exact_alpha",
                "bboxes_match_manifest", "pivots_in_canvas",
                "provenance_partition_and_source_claims",
                "B_and_C_truly_differ", "B_C_diff_confined_to_P",
                "no_banned_duplicate_components", "stress_samples_present",
                "stress_all_passed"):
            return val is True
        if key.endswith("_independent_max_channel_diff"):
            return val <= 1
        if key in ("B_pixel_faithful_gt3_px", "outer_boundary_alpha_raised_px"):
            return val == 0
        if key.startswith("coverage_"):
            return val["holes"] == 0 and val["deficits"] == 0
        return None  # informational only

    ok = True
    for k, v in results.items():
        verdict = passes(k, v)
        if verdict is None:
            print("info:", k, "=", v)
        elif verdict:
            print("ok:", k, "=", v)
        else:
            ok = False
            print("FAIL:", k, "=", v)

    results["all_passed"] = ok
    with open(V3 + "/code/_verify_report.json", "w") as f:
        json.dump(results, f, indent=2)
    assert ok, "verification failed"
    print("stage 70 complete: all independent checks pass")


if __name__ == "__main__":
    main()
