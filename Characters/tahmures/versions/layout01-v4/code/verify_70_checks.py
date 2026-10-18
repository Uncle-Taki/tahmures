#!/usr/bin/env python3
"""Layout01 v4 repair — stage 70: independent local verification.

Re-composes the manifest-declared groups from the delivered component files
two ways — with PIL's alpha compositing (byte-exact against the saved
previews) and with an independent float implementation (must agree within
1/255 per channel) — and confirms masks, provenance, pivots, coverage,
fidelity and the immutable inputs. Revision-1 additions: v3-tree integrity
against its own hash index, Codex-metric before/after recounts for
R1-01/R1-02/R1-04, and an independent vacated-strip identity re-check for
R1-02. Results are written to code/_verify_report.json and must all pass.
"""
import hashlib
import json
import os
from pathlib import Path

import numpy as np
from PIL import Image

from build_lib import V2, V3, V4, REPO, CANVAS, erode, dilate, shifted

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


def v3_tree_unchanged():
    """Every v3 file still hashes to what v3's own index recorded."""
    idx = json.load(open(V3 + "/files-sha256.json"))
    bad = [rel for rel, expected in idx.items()
           if digest(V3 + "/" + rel) != expected]
    actual = {str(p.relative_to(V3)) for p in Path(V3).rglob("*")
              if p.is_file() and p.name != "files-sha256.json"}
    return (not bad and actual == set(idx)), len(bad)


def main():
    results = {}

    # immutable inputs unchanged
    results["zip_sha256_unchanged"] = digest(ZIP_PATH) == ZIP_SHA
    results["master_sha256_unchanged"] = digest(MASTER_PATH) == MASTER_SHA
    results["domain_copy_verbatim"] = (
        digest(V4 + "/masks/visible_head_domain.png")
        == digest(V2 + "/masks/visible_head_domain.png"))
    v3_ok, v3_bad = v3_tree_unchanged()
    results["v3_tree_unchanged"] = v3_ok
    results["v3_tree_mismatched_files"] = v3_bad

    manifest = json.load(open(V4 + "/manifest.json"))
    sprites = {s["id"]: s for s in manifest["sprites"]}

    # masks equal exact alpha; bboxes and pivots as declared
    mask_ok, bbox_ok, pivot_ok = True, True, True
    for sid, s in sprites.items():
        im = Image.open(V4 + "/" + s["path"])
        mask = Image.open(V4 + "/" + s["mask_path"]).convert("L")
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

    # eye/brow pivots byte-equal to the v2 baseline manifest (alignment)
    base_manifest = json.load(open(V2 + "/manifest.json"))
    base_sprites = {s["id"]: s for s in base_manifest["sprites"]}
    align_ok = True
    for sid in ("eye_left", "eye_right", "eyebrow_left", "eyebrow_right"):
        if sprites[sid]["pivot"] != base_sprites[sid]["pivot"]:
            align_ok = False
    results["eye_brow_pivots_match_v2"] = align_ok

    # provenance partition and source-pixel claims
    master = np.asarray(Image.open(MASTER_PATH).convert("RGBA"))
    prov_ok = True
    for sid, s in sprites.items():
        im = np.asarray(Image.open(V4 + "/" + s["path"]).convert("RGBA"))
        src = np.asarray(
            Image.open(V4 + "/" + s["provenance"]["source_pixel_mask"]).convert("L")) > 127
        rec = np.asarray(
            Image.open(V4 + "/" + s["provenance"]["reconstructed_pixel_mask"]).convert("L")) > 127
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
        paths = [V4 + "/" + sprites[i]["path"] for i in order]
        pil_img = compose_pil(paths)
        comp[gname] = np.asarray(pil_img)
        prev = np.asarray(
            Image.open(V4 + "/" + manifest["previews"][PREVIEW_OF[gname]]).convert("RGBA"))
        results["recompose_%s_byte_equal_preview" % gname] = bool(
            pil_img.tobytes() == Image.fromarray(prev, "RGBA").tobytes())
        indep = compose_independent(paths)
        results["recompose_%s_independent_max_channel_diff" % gname] = int(
            np.abs(indep.astype(int) - prev.astype(int)).max())
        results["recompose_%s_sprite_count" % gname] = len(order)

    # B vs C: truly differ, only inside the patch footprint / opening
    P = np.load(V4 + "/code/_P.npy")
    opening = np.load(V4 + "/code/_opening.npy")
    B, C = comp["puppet_core_neutral"], comp["puppet_core_open_test"]
    bc = (B != C).any(axis=2)
    results["B_and_C_truly_differ"] = bool(bc.any())
    results["B_C_diff_confined_to_P"] = not bool((bc & ~P).any())
    results["B_C_diff_equals_opening"] = bool(np.array_equal(bc, opening))
    results["B_C_diff_px"] = int(bc.sum())

    # fidelity envelope vs master: differences confined to intended zones
    M = np.load(V4 + "/code/_M.npy")
    U = np.load(V4 + "/code/_U.npy")
    ink_head = np.load(V4 + "/code/_ink_head.npy")
    ink_beard = np.load(V4 + "/code/_ink_beard.npy")
    patch_ink = np.load(V4 + "/code/_patch_ink.npy")
    neck_clean = np.load(V4 + "/code/_neck_clean.npy")
    neck_zone = dilate(neck_clean, 1)
    strip_zone = np.zeros_like(U)
    strip_zone[300:370, 460:612] = True
    neck_zone |= strip_zone
    a_zone = dilate(M | ink_head | ink_beard | patch_ink | U, 1) | neck_zone
    zones = {"A": a_zone, "B": neck_zone,
             "C": a_zone | dilate(opening, 1)}
    comp_states = {"A": comp["puppet_core"], "B": B, "C": C}
    for key, c in comp_states.items():
        both = (c[..., 3] >= 250) & (master[..., 3] >= 250)
        d = np.abs(c[..., :3].astype(int) - master[..., :3].astype(int)).max(axis=2)
        bad = both & (d > 3)
        esc = bad & ~zones[key]
        results["fidelity_%s_gt3_px" % key] = int(bad.sum())
        results["fidelity_%s_escaping_intended_zone" % key] = int(esc.sum())

    # coverage in the one-pixel eroded domain for all three states
    dom = np.asarray(
        Image.open(V2 + "/masks/visible_head_domain.png").convert("L")) >= 127
    er = erode(dom, 1)
    for gname, c in comp.items():
        cal = c[..., 3]
        holes = int((er & (master[..., 3] > 0) & (cal == 0)).sum())
        deficits = int((er & (master[..., 3] >= 250) & (cal < 250)).sum())
        results["coverage_%s" % gname] = {"holes": holes, "deficits": deficits}

    # antialiasing preserved at the outer boundary
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
        np.asarray(Image.open(V4 + "/" + s["path"]).convert("RGBA")).tobytes()
    ).hexdigest() in banned]
    results["no_banned_duplicate_components"] = not dup

    # stress evidence present and passing
    stress = json.load(open(V4 + "/stress-tests.json"))
    results["stress_samples_present"] = len(stress["samples"]) == 18 and all(
        os.path.isfile(V4 + "/" + s["path"]) for s in stress["samples"])
    results["stress_all_passed"] = bool(stress["all_passed"])

    # ---------------- R1 before/after Codex-metric recounts ----------------
    recount = {}

    # R1-01: warm crescent in state A
    warm = lambda arr: ((arr[..., 0] >= 140)
                        & (arr[..., 0] - arr[..., 2] >= 55) & (arr[..., 3] > 0))
    A3 = np.asarray(Image.open(V3 + "/previews/mouthless.png").convert("RGBA"))
    recount["r1_01_warm_crescent_v3"] = int(
        warm(A3)[230:237, 530:542].sum())
    recount["r1_01_warm_crescent_v4"] = int(warm(A)[230:237, 530:542].sum())
    recount["r1_01_warm_over_clone_zone_v4"] = int(
        (warm(A) & (M | ink_beard)).sum())

    # R1-02: dark px in the underlayers inside Codex's bboxes
    # (same classifier as check_stage10.py: dark = r<90, g<75, b<70, visible)
    def dark_in(bbox, arr):
        x0, y0, x1, y1 = bbox
        sub = arr[y0:y1, x0:x1]
        dark = (sub[..., 3] > 0) & (sub[..., 0] < 90) & (sub[..., 1] < 75) \
            & (sub[..., 2] < 70)
        return int(dark.sum())

    head3 = np.asarray(Image.open(V3 + "/head/head_base.png").convert("RGBA"))
    head4 = np.asarray(Image.open(V4 + "/head/head_base.png").convert("RGBA"))
    recount["r1_02_head_base_dark_in_codex_bbox_v3"] = dark_in(
        [486, 209, 597, 238], head3)
    recount["r1_02_head_base_dark_in_codex_bbox_v4"] = dark_in(
        [486, 209, 597, 238], head4)
    beard3 = np.asarray(Image.open(V3 + "/face/beard.png").convert("RGBA"))
    beard4 = np.asarray(Image.open(V4 + "/face/beard.png").convert("RGBA"))
    recount["r1_02_beard_dark_in_codex_bbox_v3"] = dark_in(
        [498, 224, 585, 239], beard3)
    recount["r1_02_beard_dark_in_codex_bbox_v4"] = dark_in(
        [498, 224, 585, 239], beard4)
    # supporting evidence: of v4's 87 dark head_base px, how many share an
    # exact v2-moustache RGB (Codex's original matching metric)
    mo_v2 = np.asarray(Image.open(V2 + "/face/moustache.png").convert("RGBA"))
    mo_colors = {(int(r), int(g), int(b)) for r, g, b, a in mo_v2.reshape(-1, 4)
                 if a > 0}
    sub = head4[209:238, 486:597]
    dark = (sub[..., 3] > 0) & (sub[..., 0] < 90) & (sub[..., 1] < 75) \
        & (sub[..., 2] < 70)
    exact = sum(1 for yy, xx in zip(*np.nonzero(dark))
                if (int(sub[yy, xx, 0]), int(sub[yy, xx, 1]),
                    int(sub[yy, xx, 2])) in mo_colors)
    recount["r1_02_head_base_dark_exact_moustache_color_v4"] = int(exact)

    # R1-02: independent vacated-strip identity re-check over both states
    LAYER_ORDER = [
        "hair_back", "head_base", "ear_right", "ear_left", "beard",
        "nose", "eye_right", "eye_left", "eyebrow_right", "eyebrow_left",
        "moustache", "diadem_gold",
    ]
    REL = {sid: sprites[sid]["path"] for sid in sprites}
    moust_a = np.asarray(
        Image.open(V4 + "/" + REL["moustache"]).convert("RGBA"))[..., 3] > 0
    strip_ok = True
    strip_detail = {}
    for pid in ("lower_face_neutral", "lower_face_open_test"):
        ids = [i for i in LAYER_ORDER if i != "moustache"]
        ids.insert(5, pid)
        under = np.asarray(
            compose_pil([V4 + "/" + REL[i] for i in ids]))
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ids2 = list(LAYER_ORDER)
            ids2.insert(5, pid)
            layers = {i: np.asarray(
                Image.open(V4 + "/" + REL[i]).convert("RGBA")).copy()
                for i in ids2}
            layers["moustache"] = shifted(layers["moustache"], dx, dy)
            out = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
            for i in ids2:
                out = Image.alpha_composite(
                    out, Image.fromarray(layers[i], "RGBA"))
            ca = np.asarray(out)
            vacated = moust_a & ~shifted(moust_a, dx, dy)
            mm = int((ca[vacated] != under[vacated]).any(axis=-1).sum())
            strip_detail["%s_d(%d,%d)" % (pid, dx, dy)] = mm
            if mm:
                strip_ok = False
    results["r1_02_vacated_strip_identity_all_offsets"] = strip_ok
    results["r1_02_vacated_strip_mismatched_px"] = strip_detail

    # R1-04: garment family in head/hair layers (same classifier as
    # check_stage10.py: gold + blend fringe, b<=70, y>=300)
    def garment(arr):
        r_ = arr[..., 0].astype(int)
        b_ = arr[..., 2].astype(int)
        vis = arr[..., 3] > 0
        ygrid = np.arange(arr.shape[0])[:, None]
        return int((vis & (r_ >= 120) & (r_ - b_ >= 90) & (b_ <= 70)
                    & (ygrid >= 300)).sum())

    hair3 = np.asarray(Image.open(V3 + "/head/hair_back.png").convert("RGBA"))
    hair4 = np.asarray(Image.open(V4 + "/head/hair_back.png").convert("RGBA"))
    recount["r1_04_head_base_garment_v3"] = garment(head3)
    recount["r1_04_head_base_garment_v4"] = garment(head4)
    recount["r1_04_hair_back_garment_v3"] = garment(hair3)
    recount["r1_04_hair_back_garment_v4"] = garment(hair4)
    results["r1_before_after_recounts"] = recount

    # pass criteria
    def passes(key, val):
        if key.endswith("_byte_equal_preview") or key in (
                "zip_sha256_unchanged", "master_sha256_unchanged",
                "domain_copy_verbatim", "v3_tree_unchanged",
                "masks_equal_exact_alpha",
                "bboxes_match_manifest", "pivots_in_canvas",
                "eye_brow_pivots_match_v2",
                "provenance_partition_and_source_claims",
                "B_and_C_truly_differ", "B_C_diff_confined_to_P",
                "B_C_diff_equals_opening", "no_banned_duplicate_components",
                "stress_samples_present", "stress_all_passed",
                "r1_02_vacated_strip_identity_all_offsets"):
            return val is True
        if key.endswith("_independent_max_channel_diff"):
            return val <= 1
        if key in ("outer_boundary_alpha_raised_px",
                   "fidelity_A_escaping_intended_zone",
                   "fidelity_B_escaping_intended_zone",
                   "fidelity_C_escaping_intended_zone",
                   "v3_tree_mismatched_files"):
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
    with open(V4 + "/code/_verify_report.json", "w") as f:
        json.dump(results, f, indent=2)
    assert ok, "verification failed"
    print("stage 70 complete: all independent checks pass")


if __name__ == "__main__":
    main()
