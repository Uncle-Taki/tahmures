#!/usr/bin/env python3
"""Deterministic local builder for Characters/godot-character-library-recovery-01.

Executes Phase A & Phase B asset generation on the local repository:
1. Verifies SHA-256 hashes of Tahmures approved packages (layout01-v7 and
   layout01-facial-states-01) and all 9 owner-supplied character PNGs in Characters/.
2. Preserves existing RGBA transparency; for RGB inputs performs edge-seeded
   border flood-fill background removal into derived RGBA
   working images, preserving interior pale clothing, white robes (Div-e Sefid),
   eyes, teeth, and fine outlines. Leaves original source PNGs untouched.
3. Exports disjoint full-canvas RGBA component layers for each character so that
   alpha-compositing the exported layers in draw_order_bottom_to_top reproduces
   the derived RGBA cutout bit-for-bit at original resolution (1087x1447 for
   simurgh_human, 1086x1448 for all others) WITHOUT any hidden master image backing.
4. Generates per-layer alpha masks, provenance masks (source vs reconstructed),
   and QA inspection plates on light, dark, and checker backgrounds.

Usage (from repository root /home/mehdi/Project/leela/tahmures):
  From the package directory: /usr/bin/python3 scripts/build_character_library.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

import numpy as np
from library_contract import verify_inputs
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
PKG = HERE.parent
DEFAULT_REPO = PKG.parent.parent


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def remove_bg_border_flood(
    arr: np.ndarray, tol: int = 22
) -> tuple[np.ndarray, np.ndarray]:
    if arr.ndim != 3 or arr.shape[2] not in (3, 4) or tol < 0:
        raise ValueError("Expected RGB/RGBA input and a nonnegative tolerance")
    if arr.shape[2] == 4:
        # Existing transparency is authoritative. Colour flood-fill can enter
        # dark hair/beard outlines through transparent black border pixels.
        rgba = arr.copy()
        foreground = rgba[:, :, 3] > 0
        rgba[~foreground] = 0
        return rgba, foreground
    h, w = arr.shape[:2]
    corners = np.array(
        [arr[0, 0, :3], arr[0, w - 1, :3], arr[h - 1, 0, :3], arr[h - 1, w - 1, :3]],
        dtype=np.int32,
    )
    bg_color = np.median(corners, axis=0).astype(np.int32)
    diff = np.abs(arr[:, :, :3].astype(np.int32) - bg_color).max(axis=2)
    candidate_bg = diff <= tol

    visited = np.zeros((h, w), dtype=bool)
    visited[0, :] = candidate_bg[0, :]
    visited[h - 1, :] = candidate_bg[h - 1, :]
    visited[:, 0] = candidate_bg[:, 0]
    visited[:, w - 1] = candidate_bg[:, w - 1]

    changed = True
    while changed:
        old_sum = int(visited.sum())
        for _ in range(8):
            visited[1:, :] |= visited[:-1, :] & candidate_bg[1:, :]
            visited[:-1, :] |= visited[1:, :] & candidate_bg[:-1, :]
            visited[:, 1:] |= visited[:, :-1] & candidate_bg[:, 1:]
            visited[:, :-1] |= visited[:, 1:] & candidate_bg[:, :-1]
        changed = int(visited.sum()) != old_sum

    fg = ~visited
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    rgba[:, :, :3] = arr[:, :, :3]
    rgba[:, :, 3] = np.where(fg, 255, 0).astype(np.uint8)
    rgba[rgba[:, :, 3] == 0] = 0
    return rgba, fg


def make_qa_plate(rgba: np.ndarray, out_path: Path, label: str) -> None:
    h, w = rgba.shape[:2]
    scale = 0.35
    tw, th = int(w * scale), int(h * scale)
    plate = Image.new("RGB", (tw * 3 + 32, th + 48), (30, 33, 42))
    draw = ImageDraw.Draw(plate)
    draw.text(
        (12, 10),
        f"{label} — Light / Dark / Checker QA (layers only)",
        fill=(235, 238, 244),
    )
    fg_im = Image.fromarray(rgba, "RGBA").resize((tw, th), Image.Resampling.LANCZOS)

    for i, mode in enumerate(["light", "dark", "checker"]):
        bg = Image.new(
            "RGBA",
            (tw, th),
            (244, 241, 232, 255) if mode == "light" else (24, 27, 34, 255),
        )
        if mode == "checker":
            bdraw = ImageDraw.Draw(bg)
            for y in range(0, th, 16):
                for x in range(0, tw, 16):
                    if ((x // 16) + (y // 16)) % 2 == 0:
                        bdraw.rectangle(
                            [x, y, min(tw - 1, x + 15), min(th - 1, y + 15)],
                            fill=(54, 60, 74, 255),
                        )
        bg.alpha_composite(fg_im)
        plate.paste(bg.convert("RGB"), (8 + i * (tw + 8), 36))
    plate.save(out_path)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, default=DEFAULT_REPO)
    args = ap.parse_args()
    repo = args.repo_root.resolve()

    manifest = json.loads(
        (PKG / "character-library-manifest.json").read_text(encoding="utf-8")
    )

    verify_inputs(repo, manifest)

    # Copy approved Tahmures head layers byte-for-byte if present in repo
    poc_head = (
        repo
        / "Characters/tahmures/prototypes/godot-front-view-character-poc-01"
        / "assets/approved-head"
    )
    dst_head = PKG / "assets/approved-head"
    dst_head.mkdir(parents=True, exist_ok=True)
    if poc_head.is_dir():
        for png in sorted(poc_head.glob("*.png")):
            shutil.copy2(png, dst_head / png.name)

    for char_entry in manifest["characters"]:
        cid = char_entry["character_id"]
        src_path = repo / char_entry["source_file"]
        if not src_path.is_file():
            print(f"[ERROR] Missing source file: {src_path}", file=sys.stderr)
            return 1
        actual_sha = sha256_file(src_path)
        if actual_sha != char_entry["sha256"]:
            print(
                f"[ERROR] SHA-256 mismatch for {src_path}: got {actual_sha}",
                file=sys.stderr,
            )
            return 1

        im = Image.open(src_path)
        if (
            list(im.size) != char_entry["dimensions"]
            or im.mode != char_entry["source_mode"]
        ):
            raise ValueError(f"Source canvas/mode mismatch: {cid}")
        arr = np.asarray(im)
        h, w = arr.shape[:2]
        rgba, fg = remove_bg_border_flood(arr)

        cdir = PKG / "characters" / cid
        for sub in ("cutout", "layers", "masks", "provenance", "qa"):
            (cdir / sub).mkdir(parents=True, exist_ok=True)

        Image.fromarray(rgba, "RGBA").save(cdir / "cutout" / f"{cid}_cutout.png")

        # Partition foreground pixels into component layers (last in list = topmost;
        # unassigned foreground pixels go to the primary torso/body core layer so
        # union of layers == derived RGBA cutout with zero holes and zero duplication)
        comps = char_entry["components"]
        assigned = np.zeros((h, w), dtype=bool)
        layer_masks = {}

        # Assign from top of stack to bottom so foreground features claim
        # their pixels first
        for comp in reversed(comps):
            cname = comp["component_id"]
            x0, y0, x1, y1 = comp["search_window"]
            if not (0 <= x0 < x1 <= w and 0 <= y0 < y1 <= h):
                raise ValueError(f"Out-of-canvas component: {cid}/{cname}")
            m = np.zeros((h, w), dtype=bool)
            m[y0:y1, x0:x1] = fg[y0:y1, x0:x1] & (~assigned[y0:y1, x0:x1])
            layer_masks[cname] = m
            assigned |= m

        # Any remaining foreground pixels go into the body/torso core component
        rem = fg & (~assigned)
        if rem.any():
            core_id = (
                comps[2]["component_id"] if len(comps) > 2 else comps[0]["component_id"]
            )
            layer_masks[core_id] |= rem

        # Export each component layer, mask, and provenance mask, and verify
        # recomposition
        recomposed = np.zeros((h, w, 4), dtype=np.uint8)
        draw_order_records = []
        for comp in comps:
            cname = comp["component_id"]
            m = layer_masks[cname]
            layer_rgba = np.zeros((h, w, 4), dtype=np.uint8)
            layer_rgba[m] = rgba[m]
            lpath = cdir / "layers" / f"{cname}.png"
            Image.fromarray(layer_rgba, "RGBA").save(lpath)
            Image.fromarray(layer_rgba[:, :, 3], "L").save(
                cdir / "masks" / f"{cname}.png"
            )
            # All extracted pixels are source-visible pixels
            # (reconstructed mask is all-zero)
            Image.fromarray(np.where(m, 255, 0).astype(np.uint8), "L").save(
                cdir / "provenance" / f"{cname}__source.png"
            )
            Image.fromarray(np.zeros((h, w), dtype=np.uint8), "L").save(
                cdir / "provenance" / f"{cname}__reconstructed.png"
            )

            recomposed[m] = layer_rgba[m]
            draw_order_records.append(
                {
                    "component_id": cname,
                    "pivot_canvas": comp["pivot_canvas"],
                    "tight_alpha_bbox": Image.fromarray(layer_rgba).getbbox(),
                    "local_motion_approved": False,
                    "opaque_pixels": int(m.sum()),
                    "sha256": sha256_file(lpath),
                }
            )

        assert np.array_equal(recomposed, rgba), f"Recomposition mismatch for {cid}"
        make_qa_plate(
            recomposed, cdir / "qa" / f"{cid}_qa_plate.png", f"{cid} ({w}x{h})"
        )

        comp_map = {
            "character_id": cid,
            "source_file": char_entry["source_file"],
            "source_sha256": actual_sha,
            "canvas": [w, h],
            "skeleton_type": char_entry["skeleton_type"],
            "technical_readiness_state": "candidate_partition_needs_anatomical_review",
            "segmentation_method": (
                "provisional_disjoint_search_windows_not_anatomical_segmentation"
            ),
            "supported_states": ["neutral", "idle"],
            "unsupported_states": ["blink", "gaze_left", "gaze_right", "gesture_small"],
            "movement_scope": "whole_rig_translation_only_until_seams_reviewed",
            "human_approved": False,
            "draw_order_bottom_to_top": draw_order_records,
            "sockets": [],
        }
        (cdir / "component-map.json").write_text(
            json.dumps(comp_map, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"[BUILT] {cid:14s} | {len(comps)} layers | recomposition exact = True")

    from prepare_review import prepare_review

    prepare_review(PKG, repo, manifest)
    print(
        "ALL 10 CANDIDATE PARTITIONS BUILT. "
        "ANATOMICAL CUTS AND MOTION STILL REQUIRE REVIEW."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
