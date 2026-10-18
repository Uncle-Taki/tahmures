"""Verify actual new pose assets, source preservation and decoded animations."""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

P = Path(__file__).resolve().parents[1]
ROOT = P.parents[3]
SOURCE = ROOT / "Characters/tahmures/versions/layout01-v7"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(report_path):
    checks = []

    def check(name, passed, evidence):
        checks.append({"check": name, "pass": bool(passed), "evidence": evidence})

    manifest = json.loads((P / "manifest.json").read_text())
    source_manifest = json.loads((SOURCE / "manifest.json").read_text())
    records = {s["id"]: s for s in source_manifest["sprites"]}
    index = json.loads((SOURCE / "files-sha256.json").read_text())
    changed = [rel for rel, h in index.items() if digest(SOURCE / rel) != h]
    check("frozen_v7_146_files_unchanged", not changed, changed)
    actual = {
        str(p.relative_to(SOURCE))
        for p in SOURCE.rglob("*")
        if p.is_file() and p.name != "files-sha256.json"
    }
    check("frozen_source_inventory_complete", actual == set(index), len(actual))
    master_path = ROOT / source_manifest["source_master_repo_path"]
    check(
        "original_master_hash_unchanged",
        digest(master_path) == source_manifest["source_image_sha256"],
        source_manifest["source_image_sha256"],
    )
    approval = json.loads((ROOT / manifest["source"]["approval"]).read_text())
    check(
        "explicit_human_input_approval_bound",
        approval["actual_response"] == "yes, continue."
        and approval["manifest_sha256"] == digest(SOURCE / "manifest.json")
        and approval["file_index_sha256"] == digest(SOURCE / "files-sha256.json"),
        manifest["source"]["approval"],
    )
    sprites = {
        key: Image.open(SOURCE / rec["path"]).convert("RGBA")
        for key, rec in records.items()
    }
    assets = {}
    for rec in manifest["new_assets"]:
        image = Image.open(P / rec["path"])
        a = np.array(image)
        assets[rec["id"]] = image.convert("RGBA")
        mask = np.array(Image.open(P / rec["mask_path"]))
        source_pixels = np.array(Image.open(P / rec["provenance"]["source_pixel_mask"]))
        rebuilt = np.array(
            Image.open(P / rec["provenance"]["reconstructed_pixel_mask"])
        )
        check(
            rec["id"] + ":full_canvas_rgba",
            image.mode == "RGBA" and image.size == (1086, 1448),
            str(image.size),
        )
        check(
            rec["id"] + ":file_hash",
            digest(P / rec["path"]) == rec["sha256"],
            rec["path"],
        )
        check(
            rec["id"] + ":exact_alpha_mask",
            np.array_equal(mask, a[..., 3]),
            rec["mask_path"],
        )
        check(
            rec["id"] + ":honest_reconstruction",
            not source_pixels.any()
            and set(np.unique(rebuilt)).issubset({0, 255})
            and np.array_equal(rebuilt > 0, a[..., 3] > 0),
            "All new pose art reconstructed; no source-pixel claims",
        )
        check(
            rec["id"] + ":original_pivot",
            rec["pivot"]
            == records[
                rec["id"].replace("_closed", "")
                if rec["id"].startswith("eye_")
                else "eyebrow_left"
            ]["pivot"],
            rec["pivot"],
        )
    check(
        "only_three_new_pose_surfaces",
        set(assets)
        == {"eye_left_closed", "eye_right_closed", "thinking_brow_underlay"},
        list(assets),
    )

    def assemble(state, omit=None):
        spec = manifest["states"][state]
        order = source_manifest["render_groups"][spec["group"]]["layer_order"]
        result = Image.new("RGBA", (1086, 1448))
        for key in order:
            if key == omit:
                continue
            im = (
                assets[spec["replace"][key]]
                if key in spec.get("replace", {})
                else sprites[key]
            )
            move = spec.get("move", {})
            if key == move.get("sprite"):
                shifted = Image.new("RGBA", im.size)
                shifted.paste(im, (move["dx"], move["dy"]))
                im = shifted
            result = Image.alpha_composite(result, im)
            if key == "head_base" and spec.get("auxiliary_after_head_base"):
                result = Image.alpha_composite(
                    result, assets[spec["auxiliary_after_head_base"]]
                )
        return np.array(result)

    states = {state: assemble(state) for state in manifest["states"]}
    domain = (
        np.array(
            Image.open(SOURCE / "masks/visible_head_domain.png").filter(
                ImageFilter.MinFilter(3)
            )
        )
        > 0
    )
    master = np.array(
        Image.open(
            ROOT / "Characters/tahmures/versions/layout01-v2/source/approved_master.png"
        )
    )
    neutral = states["neutral"]
    for state, actual in states.items():
        saved = np.array(Image.open(P / "states" / (state + ".png")))
        check(
            state + ":independent_recomposition",
            np.array_equal(actual, saved),
            "Actual source/prototype layers",
        )
        gaps = int((domain & (master[..., 3] > 0) & (actual[..., 3] == 0)).sum())
        deficits = int(
            (domain & (master[..., 3] >= 250) & (actual[..., 3] < 250)).sum()
        )
        check(
            state + ":head_coverage",
            gaps == 0 and deficits == 0,
            {"gaps": gaps, "alpha_deficits": deficits},
        )
        if state in ["neutral", "open_test", "mouthless"]:
            check(
                state + ":exact_approved_pose",
                np.array_equal(
                    actual, np.array(Image.open(SOURCE / "previews" / (state + ".png")))
                ),
                "No new art in original mouth states",
            )
    blink_allowed = np.zeros(domain.shape, bool)
    for key in ["eye_left", "eye_right"]:
        original = np.array(sprites[key])
        closed = np.array(assets[key + "_closed"])
        blink_allowed |= (original[..., 3] > 0) | (closed[..., 3] > 0)
        white = (
            (original[..., 0] > 210)
            & (original[..., 1] > 210)
            & (original[..., 2] > 210)
            & (original[..., 3] > 0)
        )
        remaining = int(
            (
                white
                & (states["blink_closed"][..., 0] > 210)
                & (states["blink_closed"][..., 1] > 210)
                & (states["blink_closed"][..., 2] > 210)
            ).sum()
        )
        check(
            key + ":no_eye_white_remnant",
            remaining == 0,
            {"remaining_white_pixels": remaining},
        )
        check(
            key + ":complete_feature_receiver",
            np.all(closed[..., 3][original[..., 3] > 0] >= 250),
            "Original eye silhouette covered by new pose patch",
        )
    blink_delta = np.any(states["blink_closed"] != neutral, axis=2)
    check(
        "blink_change_confined_to_eye_surfaces",
        not (blink_delta & ~blink_allowed).any(),
        int(blink_delta.sum()),
    )
    original_brow = np.array(sprites["eyebrow_left"])
    shifted = Image.new("RGBA", (1086, 1448))
    shifted.paste(sprites["eyebrow_left"], (0, -1))
    shifted = np.array(shifted)
    brow_allowed = (
        (original_brow[..., 3] > 0)
        | (shifted[..., 3] > 0)
        | (np.array(assets["thinking_brow_underlay"])[..., 3] > 0)
    )
    thinking_delta = np.any(states["thinking"] != neutral, axis=2)
    check(
        "thinking_change_confined_to_brow_interface",
        not (thinking_delta & ~brow_allowed).any(),
        int(thinking_delta.sum()),
    )
    vacated = (original_brow[..., 3] > 0) & (shifted[..., 3] == 0)
    remaining_dark = int((vacated & (states["thinking"][..., 0] < 100)).sum())
    check(
        "no_baked_brow_in_vacated_strip",
        remaining_dark == 0,
        {"dark_residual_pixels": remaining_dark},
    )

    timeline = manifest["timeline"]
    check(
        "timeline_96_frames_8_seconds",
        len(timeline) == 96
        and sum(c["duration_ms"] for c in timeline) == 8000
        and {c["state"] for c in timeline} == set(states),
        {
            "frames": len(timeline),
            "duration_ms": sum(c["duration_ms"] for c in timeline),
        },
    )
    for kind in ["gif", "webp"]:
        animated = Image.open(P / "previews" / f"facial-states.{kind}")
        check(
            kind + ":decoded_frame_count",
            animated.n_frames == len(timeline),
            animated.n_frames,
        )
        palette = None
        if kind == "gif":
            palette = Image.open(P / "previews/gif-palette.png")
        total = 0
        mismatches = []
        durations = []
        for i, _cue in enumerate(timeline):
            animated.seek(i)
            animated.load()
            duration = animated.info.get("duration", 0)
            total += duration
            durations.append(duration)
            expected = Image.open(P / "frames" / f"frame-{i:03d}.png").convert("RGB")
            if palette is not None:
                expected = expected.quantize(
                    palette=palette, dither=Image.Dither.NONE
                ).convert("RGB")
            if expected.tobytes() != animated.convert("RGB").tobytes():
                mismatches.append(i)
        check(
            kind + ":actual_decoded_pixels",
            not mismatches,
            {
                "mismatch_frames": mismatches,
                "comparison": "lossless RGB"
                if kind == "webp"
                else "shared-palette RGB",
            },
        )
        check(
            kind + ":actual_duration",
            total == 8000 and durations == [cue["duration_ms"] for cue in timeline],
            {"duration_ms": total},
        )
        check(
            kind + ":infinite_preview_loop",
            animated.info.get("loop") == 0,
            animated.info.get("loop"),
        )
    protected = (
        ROOT
        / "Characters/tahmures/workflow/layout01-mouthless-repair"
        / "protected-tracked-files.json"
    )
    changed = [
        f for f, h in json.loads(protected.read_text()).items() if digest(ROOT / f) != h
    ]
    check("protected_book_code_and_metadata_unchanged", not changed, changed)
    check(
        "prototype_not_human_approved",
        manifest["human_approved"] is False
        and manifest["status"] == "PROTOTYPE_CANDIDATE",
        manifest["status"],
    )
    result = {
        "gate": "prototype_technical_checks",
        "pass": all(c["pass"] for c in checks),
        "artistic_approval": False,
        "checks": checks,
    }
    report_path.write_text(json.dumps(result, indent=2) + "\n")
    print(
        json.dumps(
            {
                "pass": result["pass"],
                "passed": sum(c["pass"] for c in checks),
                "failed": [c for c in checks if not c["pass"]],
            },
            indent=2,
        )
    )
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=P / "validation.json")
    main(parser.parse_args().report)
