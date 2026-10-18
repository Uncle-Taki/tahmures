#!/usr/bin/env python3
"""Layout01 v3 repair — stage 50: manifest.json for the candidate package."""
import hashlib
import json

from PIL import Image

from build_lib import V3

SPRITES = [
    # id, path, pivot, parent
    ("head_base", "head/head_base.png", (540, 315), None),
    ("hair_back", "head/hair_back.png", (540, 265), "head_base"),
    ("diadem_gold", "head/diadem_gold.png", (530, 80), "head_base"),
    ("ear_left", "face/ear_left.png", (632, 188), "head_base"),
    ("ear_right", "face/ear_right.png", (450, 188), "head_base"),
    ("eye_left", "face/eye_left.png", (579, 160), "head_base"),
    ("eye_right", "face/eye_right.png", (505, 160), "head_base"),
    ("eyebrow_left", "face/eyebrow_left.png", (579, 116), "head_base"),
    ("eyebrow_right", "face/eyebrow_right.png", (501, 116), "head_base"),
    ("nose", "face/nose.png", (548, 186), "head_base"),
    ("beard", "face/beard.png", (538, 240), "head_base"),
    ("moustache", "face/moustache.png", (540, 217), "head_base"),
    ("lower_face_neutral", "mouths/lower_face_neutral.png", (540, 241), "beard"),
    ("lower_face_open_test", "mouths/lower_face_open_test.png", (540, 241), "beard"),
]

METHODS = {
    "head_base": "Feature underdraw: solid interiors (alpha>=252) of the "
                 "eye/eyebrow/nose footprints (5922 px) inpainted by Laplacian "
                 "diffusion from the surrounding master skin so the features "
                 "can be moved in a later phase; soft feature edges keep "
                 "master RGB. Skin/neck silhouette follows the master inside "
                 "the immutable head domain (repairs the v2 rectangular cheek "
                 "cuts and neck gaps).",
    "beard": "Mouthless receiver: the mouth-content region M (2616 px, bbox "
             "x500-580 y228-269) is filled with beard texture tiled from the "
             "verified all-dark master block y270-293 x494-604; all other "
             "beard pixels are master pixels retained from v2 plus 304 "
             "recovered previously-uncovered pixels.",
    "lower_face_open_test": "Small opening (80 px, x531-553 y253-258) "
                            "synthesized from the master palette: interior "
                            "rows are 45% master mouth-line colour + 55% "
                            "master mouth-interior sample; the bottom edge row "
                            "is 75% line + 25% below-line sample.",
    "lower_face_neutral": "",
    "hair_back": "",
    "diadem_gold": "",
    "ear_left": "", "ear_right": "", "eye_left": "", "eye_right": "",
    "eyebrow_left": "", "eyebrow_right": "", "nose": "", "moustache": "",
}

ALPHA_NOTES = {
    "beard": "alpha equals master alpha inside the beard region; RGB inside M "
             "reconstructed (cloned texture)",
    "head_base": "alpha equals master alpha inside the domain-bounded region; "
                 "feature-interior RGB inpainted",
    "lower_face_open_test": "alpha equals master alpha inside footprint P; "
                            "80 opening px RGB synthesized",
    "lower_face_neutral": "alpha equals master alpha inside footprint P",
}


def digest(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    meta = json.load(open(V3 + "/code/_sprite_meta.json"))
    records = []
    for sid, rel, (px, py), parent in SPRITES:
        path = V3 + "/" + rel
        mask_path = V3 + "/masks/%s.png" % sid
        im = Image.open(path)
        assert im.mode == "RGBA" and im.size == (1086, 1448)
        bbox = list(im.getchannel("A").getbbox())
        assert bbox == meta[sid]["bbox"], (sid, bbox, meta[sid]["bbox"])
        prov = {
            "source_pixel_mask": "provenance/%s__source.png" % sid,
            "reconstructed_pixel_mask": "provenance/%s__reconstructed.png" % sid,
            "reconstruction_method": METHODS[sid],
            "alpha_edge_modifications": ALPHA_NOTES.get(
                sid, "none; alpha equals master alpha"),
        }
        records.append({
            "id": sid,
            "role": "rig_component",
            "path": rel,
            "mask_path": "masks/%s.png" % sid,
            "sha256": digest(path),
            "mask_sha256": digest(mask_path),
            "alpha_bounding_rect": bbox,
            "pivot": {"x": px, "y": py},
            "parent": parent,
            "provenance": prov,
        })

    core = [
        "hair_back", "head_base", "ear_right", "ear_left", "beard",
        "nose", "eye_right", "eye_left", "eyebrow_right", "eyebrow_left",
        "moustache", "diadem_gold",
    ]
    manifest = {
        "schema_version": "3.0.0",
        "version": "layout01-v3",
        "character_id": "tahmures",
        "display_name_fa": "طهمورث",
        "status": "CANDIDATE",
        "human_approved": False,
        "source_master_repo_path":
            "Characters/tahmures/versions/layout01-v2/source/approved_master.png",
        "source_image_sha256":
            "3eedfaa5a41965c45a137a74a9137c6e59304a0604f877a81c98870c64dba2e5",
        "canvas": [1086, 1448],
        "coordinate_convention":
            "top-left origin; +x right, +y down; character-perspective left/right",
        "mouth_architecture": "B_LOCAL_LOWER_FACE_PATCH",
        "mouth_anchor": {"x": 540, "y": 241},
        "coverage_domain_path": "masks/visible_head_domain.png",
        "sprites": records,
        "render_groups": {
            "puppet_core": {
                "type": "rig_composition",
                "layer_order": core,
                "preview": "previews/mouthless.png",
            },
            "puppet_core_neutral": {
                "type": "rig_composition",
                "layer_order": core[:5] + ["lower_face_neutral"] + core[5:],
                "preview": "previews/neutral.png",
            },
            "puppet_core_open_test": {
                "type": "rig_composition",
                "layer_order": core[:5] + ["lower_face_open_test"] + core[5:],
                "preview": "previews/open_test.png",
            },
        },
        "previews": {
            "mouthless": "previews/mouthless.png",
            "neutral": "previews/neutral.png",
            "open_test": "previews/open_test.png",
        },
        "preview_only_assets": [],
        "supported_motion_envelope": {
            "view": "front",
            "description": "Offline micro-offset stress envelope over the "
                           "actual layer files with the static receiver and "
                           "static moustache foreground.",
            "lower_face_patch_offsets_px": [
                {"x": 0, "y": 0}, {"x": 2, "y": 0}, {"x": -2, "y": 0},
                {"x": 0, "y": 2}, {"x": 0, "y": -2}],
            "moustache_offsets_px": [
                {"x": 1, "y": 0}, {"x": -1, "y": 0}, {"x": 0, "y": 1},
                {"x": 0, "y": -1}],
            "patch_states_tested": ["lower_face_neutral",
                                    "lower_face_open_test"],
            "sample_count": 18,
            "stress_evidence": "stress-tests.json and previews/stress/",
            "claims": "Limited front-view micro-offset envelope only. No "
                      "perspective turn, rotation, viseme library, or "
                      "unrestricted gap-free animation is claimed. "
                      "Whole-head rigidity is not evidence that local "
                      "facial joints are safe.",
        },
        "repair_regions": {
            "mouth_content_region_M": {
                "pixels": 2616, "bbox": [500, 228, 581, 270],
                "meaning": "master mouth content replaced by the beard "
                           "receiver (smile line, lips, interior, corner "
                           "strokes)"},
            "patch_footprint_P": {
                "pixels": 3217, "bbox": [497, 226, 585, 274],
                "meaning": "common stable footprint of both lower-face "
                           "patches; irregular contour traced from M, not a "
                           "rectangle"},
            "opening": {
                "pixels": 80, "bbox": [531, 253, 554, 259],
                "meaning": "synthesized small-open test state"},
            "clone_block": [270, 293, 494, 604],
            "uncovered_domain_pixels_assigned": 1828,
        },
        "known_limitations": [
            "Structural validation only: no Codex visual acceptance, Claude "
            "independent review, or human artistic approval is claimed.",
            "Front-view micro-offset envelope only (patch (0,0),(+-2,0),(0,+-2); "
            "moustache (+-1,0),(0,+-1)); no perspective turn, rotation, or "
            "arbitrary articulation support is claimed.",
            "lower_face_open_test is one technical small-open test state, not "
            "the start of a viseme library.",
            "The mouthless receiver inside M (2616 px) and the open-state "
            "opening (80 px) are reconstructed pixels, not master pixels.",
            "head_base carries hidden inpainted feature underdraw (5922 px) "
            "that only becomes visible if features move in a later phase.",
            "1828 previously-uncovered domain pixels were assigned to "
            "hair_back/diadem_gold/head_base/beard by nearest-palette rules; "
            "the assignment is heuristic and locally editable.",
            "State A intentionally differs from the master inside M (2045 px "
            ">3 RGB): that is the mouthless design, not a defect.",
            "Exterior edge quality, seam naturalness, and identity fidelity "
            "require independent visual inspection (see previews/plates/).",
            "Only the head-domain seams noted by Codex were repaired; no "
            "body/arm artwork, rig, or animation export exists in this phase.",
        ],
        "toolchain": {
            "python": "system /usr/bin/python3 (book .venv has no Pillow)",
            "pillow": "10.2.0",
            "numpy": "1.26.4",
            "editable_code": "code/",
        },
    }
    with open(V3 + "/manifest.json", "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("manifest written with %d sprites" % len(records))


if __name__ == "__main__":
    main()
