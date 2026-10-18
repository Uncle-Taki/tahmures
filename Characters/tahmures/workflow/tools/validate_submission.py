#!/usr/bin/env python3
"""Read-only structural gate for a Layout 01 Model-B submission.

Requires Pillow in the media-tool interpreter, not the book runtime.
Does not grant Codex visual, Claude independent, or human artistic approval.
Writes only JSON to stdout; never updates a manifest or phase status.
"""

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter

CANVAS = (1086, 1448)
REQUIRED_GROUPS = ("puppet_core", "puppet_core_neutral", "puppet_core_open_test")
REQUIRED_IDS = {
    "head_base",
    "hair_back",
    "diadem_gold",
    "ear_left",
    "ear_right",
    "eye_left",
    "eye_right",
    "eyebrow_left",
    "eyebrow_right",
    "nose",
    "beard",
    "moustache",
    "lower_face_neutral",
    "lower_face_open_test",
}
PREVIEW_IDS = {"neutral_face_without_mouth", "neutral_mouth"}
PREVIEW_FILES = (
    "previews/default_pose_head_surface_source.png",
    "previews/default_pose_beard_source.png",
    "face/neutral_face_without_mouth.png",
    "previews/layout01_source_head.png",
    "previews/layout01_reconstructed_head.png",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def image_digest(image):
    return hashlib.sha256(image.convert("RGBA").tobytes()).hexdigest()


def local_path(root, relative):
    if not isinstance(relative, str) or Path(relative).is_absolute():
        raise ValueError("Expected candidate-root-relative path")
    result = (root / relative).resolve()
    if not result.is_relative_to(root.resolve()):
        raise ValueError("Path escapes candidate root: " + relative)
    if not result.is_file():
        raise ValueError("Missing file: " + relative)
    return result


def validate(root, baseline):
    checks = []

    def check(name, ok, evidence):
        checks.append({"check": name, "pass": bool(ok), "evidence": evidence})

    manifest = json.loads((root / "manifest.json").read_text())
    baseline_manifest = json.loads((baseline / "manifest.json").read_text())
    baseline_sprites = {s["id"]: s for s in baseline_manifest["sprites"]}
    source = baseline / "source/approved_master.png"
    expected_source = digest(source)
    original = Image.open(source).convert("RGBA")
    check(
        "source_binding",
        manifest.get("source_image_sha256") == expected_source,
        expected_source,
    )
    check(
        "source_reference_path",
        manifest.get("source_master_repo_path")
        == "Characters/tahmures/versions/layout01-v2/source/approved_master.png",
        manifest.get("source_master_repo_path"),
    )
    check("canvas", manifest.get("canvas") == list(CANVAS), manifest.get("canvas"))
    check(
        "mouth_anchor",
        manifest.get("mouth_anchor") == {"x": 540, "y": 241},
        manifest.get("mouth_anchor"),
    )
    check(
        "architecture",
        manifest.get("mouth_architecture") == "B_LOCAL_LOWER_FACE_PATCH",
        manifest.get("mouth_architecture"),
    )
    check(
        "unapproved_candidate",
        manifest.get("status") == "CANDIDATE"
        and manifest.get("human_approved") is False,
        {
            "status": manifest.get("status"),
            "human_approved": manifest.get("human_approved"),
        },
    )
    records = manifest["sprites"]
    ids = [s["id"] for s in records]
    check(
        "ids_unique_and_complete",
        len(ids) == len(set(ids)) and REQUIRED_IDS.issubset(ids),
        ids,
    )
    sprites = {s["id"]: s for s in records}
    parent_errors = []
    for sid, sprite in sprites.items():
        seen = {sid}
        parent = sprite.get("parent")
        while parent is not None:
            if parent not in sprites or parent in seen:
                parent_errors.append(
                    {"sprite": sid, "invalid_or_cyclic_parent": parent}
                )
                break
            seen.add(parent)
            parent = sprites[parent].get("parent")
    check("parents_resolve_without_cycles", not parent_errors, parent_errors)
    banned_pixels = {
        image_digest(Image.open(baseline / name)) for name in PREVIEW_FILES
    }
    banned_pixels.add(image_digest(original))
    images = {}
    for sprite in records:
        sid = sprite["id"]
        path = local_path(root, sprite["path"])
        mask_path = local_path(root, sprite["mask_path"])
        im = Image.open(path)
        mask = Image.open(mask_path)
        check(
            sid + ":rgba_canvas",
            im.mode == "RGBA" and im.size == CANVAS,
            {"mode": im.mode, "size": list(im.size)},
        )
        check(
            sid + ":mask_canvas",
            mask.mode == "L" and mask.size == CANVAS,
            {"mode": mask.mode, "size": list(mask.size)},
        )
        if im.mode != "RGBA" or im.size != CANVAS or mask.size != CANVAS:
            continue
        images[sid] = im
        check(
            sid + ":mask_exact_alpha",
            mask.mode == "L"
            and ImageChops.difference(mask.convert("L"), im.getchannel("A")).getbbox()
            is None,
            "mask_path is exported-alpha mask; selection/provenance masks are separate",
        )
        bbox = im.getchannel("A").getbbox()
        check(
            sid + ":bbox",
            bbox is not None and sprite.get("alpha_bounding_rect") == list(bbox),
            {"actual": bbox, "declared": sprite.get("alpha_bounding_rect")},
        )
        pivot = sprite.get("pivot", {})
        check(
            sid + ":pivot",
            isinstance(pivot.get("x"), (int, float))
            and isinstance(pivot.get("y"), (int, float))
            and 0 <= pivot["x"] < CANVAS[0]
            and 0 <= pivot["y"] < CANVAS[1],
            pivot,
        )
        check(
            sid + ":file_hashes",
            digest(path) == sprite.get("sha256")
            and digest(mask_path) == sprite.get("mask_sha256"),
            str(path),
        )
        check(
            sid + ":not_preview_underlay",
            sid not in PREVIEW_IDS
            and Path(sprite["path"]).parts[0] != "previews"
            and image_digest(im) not in banned_pixels
            and sprite.get("role") == "rig_component",
            sprite["path"],
        )
        prov = sprite["provenance"]
        source_mask = Image.open(local_path(root, prov["source_pixel_mask"])).convert(
            "L"
        )
        rebuilt_mask = Image.open(
            local_path(root, prov["reconstructed_pixel_mask"])
        ).convert("L")
        check(
            sid + ":provenance_canvas",
            source_mask.size == CANVAS and rebuilt_mask.size == CANVAS,
            "both ownership masks use original canvas",
        )
        if source_mask.size != CANVAS or rebuilt_mask.size != CANVAS:
            continue
        alpha = im.getchannel("A")
        source_pixels = list(source_mask.getdata())
        rebuilt_pixels = list(rebuilt_mask.getdata())
        ownership_ok = all(
            s in (0, 255)
            and r in (0, 255)
            and not (s and r)
            and bool(s or r) == bool(a)
            for s, r, a in zip(
                source_pixels, rebuilt_pixels, alpha.getdata(), strict=True
            )
        )
        check(
            sid + ":provenance_partition",
            ownership_ok,
            "binary masks disjoint within this sprite and cover every visible pixel",
        )
        source_rgb_ok = all(
            not s or (p[:3] == q[:3] and 0 < p[3] <= q[3])
            for s, p, q in zip(
                source_pixels, im.getdata(), original.getdata(), strict=True
            )
        )
        check(
            sid + ":source_pixel_claim",
            source_rgb_ok,
            "claimed source pixels have exact source RGB; "
            "extraction may only reduce alpha",
        )
        check(
            sid + ":reconstruction_description",
            not any(rebuilt_pixels)
            or bool(str(prov.get("reconstruction_method", "")).strip()),
            prov.get("reconstruction_method"),
        )

    groups = manifest["render_groups"]
    check("groups_present", all(g in groups for g in REQUIRED_GROUPS), list(groups))
    baseline_domain = baseline / "masks/visible_head_domain.png"
    domain_path = local_path(root, manifest["coverage_domain_path"])
    domain = Image.open(domain_path).convert("L")
    check(
        "domain_not_shrunk",
        digest(domain_path) == digest(baseline_domain),
        "immutable v2 visible_head_domain must be copied verbatim",
    )
    if domain.size != CANVAS:
        raise ValueError("Coverage domain size differs from original canvas")
    interior = domain.filter(ImageFilter.MinFilter(3))
    compose = {}
    for name in REQUIRED_GROUPS:
        group = groups.get(name, {})
        order = group.get("layer_order", [])
        valid = (
            bool(order)
            and len(order) == len(set(order))
            and all(k in images for k in order)
        )
        check(
            name + ":resolves", valid and group.get("type") == "rig_composition", order
        )
        if not valid:
            continue
        allowed_patch = {
            "puppet_core": None,
            "puppet_core_neutral": "lower_face_neutral",
            "puppet_core_open_test": "lower_face_open_test",
        }[name]
        patches = [k for k in order if k.startswith("lower_face_")]
        check(
            name + ":single_patch",
            patches == ([] if allowed_patch is None else [allowed_patch]),
            patches,
        )
        check(
            name + ":moustache_foreground",
            "beard" in order
            and "moustache" in order
            and order.index("beard") < order.index("moustache")
            and (
                allowed_patch is None
                or order.index(allowed_patch) < order.index("moustache")
            ),
            order,
        )
        out = Image.new("RGBA", CANVAS)
        for sid in order:
            out.alpha_composite(images[sid])
        compose[name] = out
        holes = sum(
            d >= 250 and source_alpha > 0 and a == 0
            for d, source_alpha, a in zip(
                interior.getdata(),
                original.getchannel("A").getdata(),
                out.getchannel("A").getdata(),
                strict=True,
            )
        )
        deficits = sum(
            d >= 250 and source_alpha >= 250 and a < 250
            for d, source_alpha, a in zip(
                interior.getdata(),
                original.getchannel("A").getdata(),
                out.getchannel("A").getdata(),
                strict=True,
            )
        )
        check(
            name + ":interior_coverage",
            holes == 0 and deficits == 0,
            {
                "new_fully_transparent": holes,
                "alpha_below_250_where_source_opaque": deficits,
            },
        )
        preview_key = {
            "puppet_core": "mouthless",
            "puppet_core_neutral": "neutral",
            "puppet_core_open_test": "open_test",
        }[name]
        preview = Image.open(
            local_path(root, manifest["previews"][preview_key])
        ).convert("RGBA")
        check(
            name + ":preview_is_actual_assembly",
            preview.size == CANVAS and preview.tobytes() == out.tobytes(),
            "unadorned RGBA full-canvas assembly",
        )
    if "puppet_core_neutral" in compose and "puppet_core_open_test" in compose:
        check(
            "mouth_states_really_differ",
            compose["puppet_core_neutral"].tobytes()
            != compose["puppet_core_open_test"].tobytes(),
            "not two aliases of one image",
        )
    file_index = json.loads((root / "files-sha256.json").read_text())
    file_errors = []
    for relative, expected in file_index.items():
        path = local_path(root, relative)
        if digest(path) != expected:
            file_errors.append(relative)
    actual_files = {
        str(p.relative_to(root))
        for p in root.rglob("*")
        if p.is_file() and p.name != "files-sha256.json"
    }
    check(
        "file_index_complete_and_current",
        not file_errors and set(file_index) == actual_files,
        {
            "hash_errors": file_errors,
            "unindexed": sorted(actual_files - set(file_index)),
            "missing": sorted(set(file_index) - actual_files),
        },
    )
    for sid in ("eye_left", "eye_right", "eyebrow_left", "eyebrow_right"):
        original_pivot = baseline_sprites[sid]["pivot"]
        expected = (original_pivot["x"], original_pivot["y"])
        pivot = sprites.get(sid, {}).get("pivot", {})
        check(
            sid + ":alignment_preserved",
            (pivot.get("x"), pivot.get("y")) == expected,
            pivot,
        )
    return {
        "gate": "structural_only",
        "artistic_approval": False,
        "pass": all(c["pass"] for c in checks),
        "checks": checks,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = validate(args.candidate.resolve(), args.baseline.resolve())
    except (KeyError, ValueError, OSError, TypeError, json.JSONDecodeError) as exc:
        result = {
            "gate": "structural_only",
            "artistic_approval": False,
            "pass": False,
            "error": str(exc),
        }
    print(json.dumps(result, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
