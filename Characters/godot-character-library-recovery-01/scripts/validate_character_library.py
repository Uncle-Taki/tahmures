#!/usr/bin/env python3
"""Fail-closed candidate validation. A pass does not approve anatomical cuts/art."""

import argparse
import sys
from pathlib import Path

import numpy as np
from library_contract import digest, read_json, verify_inputs, write_json
from PIL import Image

PKG = Path(__file__).resolve().parent.parent


def validate(repo, package=PKG):
    manifest = read_json(package / "character-library-manifest.json")
    head = verify_inputs(repo, manifest)
    checks = []
    for name, record in head.items():
        if digest(package / "assets/approved-head" / name) != record["sha256"]:
            raise ValueError("Copied approved head hash mismatch: " + name)
    checks.append("source_hashes_frozen_indexes_approval_bindings_and_17_head_copies")
    from build_character_library import remove_bg_border_flood

    for c in manifest["characters"]:
        cid = c["character_id"]
        d = package / "characters" / cid
        cmap = read_json(d / "component-map.json")
        if cmap["character_id"] != cid or cmap["source_sha256"] != c["sha256"]:
            raise ValueError("Component map identity mismatch: " + cid)
        if cmap.get("human_approved") is not False or cmap["supported_states"] != [
            "neutral",
            "idle",
        ]:
            raise ValueError("Candidate capabilities/approval overstated: " + cid)
        expected, foreground = remove_bg_border_flood(
            np.array(Image.open(repo / c["source_file"]))
        )
        w, h = cmap["canvas"]
        if [w, h] != c["dimensions"]:
            raise ValueError("Canvas mismatch: " + cid)
        out = Image.new("RGBA", (w, h))
        occupied = np.zeros((h, w), dtype=bool)
        if [r["component_id"] for r in cmap["draw_order_bottom_to_top"]] != [
            r["component_id"] for r in c["components"]
        ]:
            raise ValueError("Missing or reordered component: " + cid)
        for r in cmap["draw_order_bottom_to_top"]:
            name = r["component_id"]
            path = d / "layers" / (name + ".png")
            layer = Image.open(path).convert("RGBA")
            array = np.array(layer)
            mask = array[:, :, 3] > 0
            if digest(path) != r["sha256"] or layer.size != (w, h):
                raise ValueError("Layer hash/canvas mismatch: " + str(path))
            bbox = list(layer.getbbox()) if layer.getbbox() else None
            if bbox != r["tight_alpha_bbox"] or int(mask.sum()) != r["opaque_pixels"]:
                raise ValueError("Layer statistics mismatch: " + str(path))
            if np.any(occupied & mask):
                raise ValueError("Duplicated visible pixels: " + str(path))
            occupied |= mask
            if not np.array_equal(
                np.array(Image.open(d / "masks" / (name + ".png"))), array[:, :, 3]
            ):
                raise ValueError("Alpha mask mismatch: " + str(path))
            src = np.array(Image.open(d / "provenance" / (name + "__source.png")))
            rec = np.array(
                Image.open(d / "provenance" / (name + "__reconstructed.png"))
            )
            if not np.array_equal(src > 0, mask) or np.any(rec):
                raise ValueError("Extraction provenance mismatch: " + str(path))
            out = Image.alpha_composite(out, layer)
        cutout = np.array(Image.open(d / "cutout" / (cid + "_cutout.png")))
        if not np.array_equal(np.array(out), cutout) or not np.array_equal(
            cutout, expected
        ):
            raise ValueError("Source/cutout/layer recomposition mismatch: " + cid)
        if not np.array_equal(occupied, foreground):
            raise ValueError("Missing foreground pixels: " + cid)
        for required in [
            package / "scenes/characters" / (cid + ".tscn"),
            d / "qa/component-sheet.png",
            d / "qa/source-versus-layers.png",
            d / "qa" / (cid + "_qa_plate.png"),
        ]:
            if not required.is_file():
                raise ValueError("Missing review output: " + str(required))
        checks.append("source_cutout_layers_masks_provenance_scene:" + cid)
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=PKG.parent.parent)
    parser.add_argument("--package-root", type=Path, default=PKG)
    args = parser.parse_args()
    package = args.package_root.resolve()
    report = {
        "pass": False,
        "human_approved": False,
        "scope": "technical_source_pose_candidate_only",
        "checks": [],
    }
    try:
        report["checks"] = validate(args.repo_root.resolve(), package)
        report["pass"] = True
    except (OSError, ValueError, KeyError, TypeError) as exc:
        report["error"] = str(exc)
        print("[FAIL]", exc, file=sys.stderr)
    write_json(package / "validation.json", report)
    for check in report["checks"]:
        print("[PASS]", check)
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
