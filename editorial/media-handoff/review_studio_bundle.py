#!/usr/bin/env python3
"""Compare the received Studio JSON claims with local files without importing it."""

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_reference(reference):
    """The export uses web-root paths; resolve only inside this repository."""
    path = (ROOT / reference.lstrip("/")).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError(f"Reference escapes repository: {reference}")
    return path


def audit(bundle):
    data = json.loads(bundle.read_text())
    missing, bounds, pixels, canvases, sources = [], [], [], [], []
    references = set()
    layers_total = 0
    for rig in data["character_rigs"]:
        char = rig["character"]
        cid = char["character_id"]
        source = local_reference(char["source_file"])
        sources.append(
            {
                "character": cid,
                "path": char["source_file"],
                "exists": source.is_file(),
                "claimed_sha256": char["source_sha256"],
                "actual_sha256": digest(source) if source.is_file() else None,
                "sha256_matches": source.is_file()
                and digest(source) == char["source_sha256"],
            }
        )
        if source.is_file():
            with Image.open(source) as image:
                claimed = char["canvas_dimensions"]
                actual = list(image.size)
                if actual != [claimed["width"], claimed["height"]]:
                    canvases.append(
                        {
                            "character": cid,
                            "claimed": claimed,
                            "actual": actual,
                            "root_canvas_claim": rig["root_transform"]["canvas_size"],
                        }
                    )
        for layer in rig["bones_and_layers"]:
            layers_total += 1
            ident = {"character": cid, "component": layer["component_id"]}
            for kind, reference in layer["texture_assets"].items():
                path = local_reference(reference)
                references.add(str(path.relative_to(ROOT)))
                if not path.is_file():
                    missing.append({**ident, "kind": kind, "path": reference})
            path = local_reference(layer["texture_assets"]["layer_png"])
            if not path.is_file():
                continue
            with Image.open(path) as image:
                alpha = image.convert("RGBA").getchannel("A")
                box = list(alpha.getbbox()) if alpha.getbbox() else None
                count = sum(alpha.histogram()[1:])
            if box != layer["tight_alpha_bbox"]:
                bounds.append(
                    {**ident, "claimed": layer["tight_alpha_bbox"], "actual": box}
                )
            if count != layer["opaque_pixels"]:
                pixels.append(
                    {**ident, "claimed": layer["opaque_pixels"], "actual": count}
                )
    chapter = data["chapter_01_animatic"]
    timing_errors = []
    scene_lookup = {scene["id"]: scene for scene in chapter["scenes"]}
    end = 0
    for scene in chapter["scenes"]:
        if scene["start"] != end or scene["duration"] <= 0:
            timing_errors.append(
                {"scene": scene["id"], "reason": "gap_overlap_or_duration"}
            )
        end = scene["start"] + scene["duration"]
    for kind in ("dialogue_cues", "programmatic_osts"):
        for cue in chapter[kind]:
            scene = scene_lookup.get(cue["scene"])
            if scene is None or not (
                scene["start"]
                <= cue["start"]
                < cue["end"]
                <= scene["start"] + scene["duration"]
            ):
                timing_errors.append({"cue": cue["id"], "reason": "outside_scene"})
    runtime = data["godot_4_3_contracts"]
    runtime_paths = [runtime["scene_file"], runtime["director_script"]]
    active = ROOT / "Characters/godot-character-library-recovery-01"
    runtime_checks = [
        {
            "reference": ref,
            "exists_in_active_project": (active / ref.removeprefix("res://")).is_file(),
        }
        for ref in runtime_paths
    ]
    baseline = json.loads(
        (ROOT / "editorial/media-handoff/ai-studio-baseline.json").read_text()
    )
    changed_non_target = [
        r["path"]
        for r in baseline["protected_non_target_outputs"]
        if not (ROOT / r["path"]).is_file() or digest(ROOT / r["path"]) != r["sha256"]
    ]
    changed_inputs = [
        r["path"]
        for r in baseline["required_inputs"]
        if not (ROOT / r["path"]).is_file() or digest(ROOT / r["path"]) != r["sha256"]
    ]
    return {
        "schema_version": 1,
        "reviewed_on": "2026-10-20",
        "input": str(bundle.relative_to(ROOT)),
        "input_sha256": digest(bundle),
        "input_modified": False,
        "verdict": "SPECIFICATION_ONLY_NOT_ACCEPTED_AS_IMPLEMENTATION_OR_CERTIFICATION",
        "counts": {
            "characters": len(data["character_rigs"]),
            "layers_claimed": layers_total,
            "unique_texture_references": len(references),
            "missing_texture_references": len(missing),
            "bbox_mismatches": len(bounds),
            "pixel_count_mismatches": len(pixels),
            "canvas_mismatches": len(canvases),
            "source_hash_mismatches": sum(not s["sha256_matches"] for s in sources),
            "scenes": len(chapter["scenes"]),
            "dialogue_cues": len(chapter["dialogue_cues"]),
            "osts": len(chapter["programmatic_osts"]),
            "timeline_seconds": end,
        },
        "source_identity_checks": sources,
        "missing_assets": missing,
        "bbox_mismatches": bounds,
        "pixel_count_mismatches": pixels,
        "canvas_mismatches": canvases,
        "timeline_errors": timing_errors,
        "claimed_runtime_paths": runtime_checks,
        "changed_protected_non_target_outputs": changed_non_target,
        "changed_protected_inputs": changed_inputs,
        "claims_not_established_by_this_json": [
            "organic contours and exact recomposition of newly extracted assets",
            "safe joint overlaps and independent prop decoupling",
            "blink/thinking/alert/talking on all ten rigs",
            "Godot/Unity/Spine/PixiJS compatibility",
            "100 percent certification or owner approval",
            "complete scene rendering, background assets, audio and fonts",
        ],
        "semantic_blockers": [
            {
                "path": "chapter_01_animatic.programmatic_osts[9]",
                "finding": (
                    "Requested Result: Count contradicts classify object/name missing "
                    "context; seal_icon implies unsupported authority."
                ),
            },
            {
                "path": "license",
                "finding": (
                    "Proprietary export label conflicts with repository content/code "
                    "licences; do not adopt it."
                ),
            },
            {
                "path": "head_inspection_registry.tahmures",
                "finding": (
                    "Anatomical-left/viewer-right names and receiver-underlay "
                    "draw order "
                    "must follow the accepted rig, not this registry's zIndex order; "
                    "open_test is not phoneme approval."
                ),
            },
            {
                "path": "character_rigs",
                "finding": (
                    "All-ten certification exceeds the Akvan-only assignment and "
                    "contradicts candidate readiness labels; no new contour files or "
                    "execution evidence are delivered here."
                ),
            },
        ],
        "human_approved": False,
        "runtime_import_authorized_by_report": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bundle", type=Path, default=ROOT / "tahmures_complete_studio_bundle.json"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("studio-bundle-review.json"),
    )
    args = parser.parse_args()
    result = audit(args.bundle.resolve())
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(
        json.dumps({"verdict": result["verdict"], "counts": result["counts"]}, indent=2)
    )
    print("Audit completed. This is a review report, not a passing production gate.")


if __name__ == "__main__":
    main()
