#!/usr/bin/env python3
"""Layout01 v4 repair — stage 50: manifest.json for the candidate package.

Revision 1 of the layout01 Model-B candidate: same architecture and layer
order as v3; local repairs to the mouthless moustache remnant (R1-01), the
moustache-footprint underdraw (R1-02), the small-open test opening (R1-03),
and the lower-neck garment contamination (R1-04).
"""
import hashlib
import json

import numpy as np
from PIL import Image

from build_lib import V4

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
    "head_base":
        "Three local reconstructions: (1) feature underdraw — solid "
        "interiors (alpha>=252) of the eye/eyebrow/nose footprints (5922 px) "
        "inpainted by Laplacian diffusion from the surrounding master skin "
        "so features can move in a later phase (v3 recipe, unchanged); "
        "(2) R1-02 moustache-footprint underdraw — 1394 px of the moustache "
        "matte U inside the head region filled with diffused skin (boundary "
        "seeded by surrounding master art; invisible dark non-head pixels "
        "in the seed box are added to the diffusion region so ink/beard "
        "colours do not leak); (3) R1-04 lower-neck cleanup — 277 garment "
        "pixels (strict garment gold r>=150 & r-b>=140 & b<=70, blend fringe "
        "r>=120 & r-b>=90 & b<=70, and pale collar trim r>=200 & 30<=r-b<=110 "
        "& g>=185, all y>=300) replaced with strand-continuation diffusion "
        "seeded by the head layer's own kept colours plus hair_back where "
        "the head is transparent. Skin/neck silhouette otherwise follows the "
        "master inside the immutable head domain.",
    "beard":
        "Mouthless receiver: the mouth-content region M (2616 px, bbox "
        "x500-580 y228-269) is filled with beard texture tiled from the "
        "verified all-dark master block y270-293 x494-604; R1-02 adds the "
        "moustache-footprint underdraw — 345 px of U inside the beard region "
        "outside M filled with the same cloned texture so +-1px moustache "
        "offsets reveal clean beard instead of the old feature outline; "
        "304 previously-uncovered domain pixels are recovered master pixels.",
    "moustache":
        "R1-01/R1-02 matte decontamination over the v2 extraction: for every "
        "U pixel above a faithful reconstructed underlay (skin underdraw in "
        "head_base or the patch underdraw), (alpha, RGB) is re-solved so the "
        "pixel composites to the exact master colour over the neutral "
        "underlay and goes dark over the mouthless beard clone (353 px "
        "solved, reconstructed provenance); 2 pure-underlay pixels are "
        "dropped (alpha 0); 29 pixels with no exact ink-blend solution "
        "(err>2, all on the top edge y214-218 over skin) and 1436 ink "
        "pixels are kept as source; pixels above the cloned receiver are "
        "kept verbatim (compositing stays within 2 of the master over the "
        "dark clone). Outer form, palette, and line weight are unchanged.",
    "lower_face_neutral":
        "Master pixels inside the common footprint P, plus R1-02 "
        "moustache-footprint underdraw: 336 px of P inside U filled by "
        "Laplacian diffusion from the surrounding master mouth art (edge "
        "pixels of U outside P are included in the diffusion region as an "
        "invisible buffer so moustache ink does not leak into the fill).",
    "lower_face_open_test":
        "Neutral patch content plus a 59 px restrained lens-shaped opening "
        "at the actual lip parting line (R1-03): for each column x531-553 "
        "the darkest master row in y237..243 (the master's y240 parting "
        "line) is parted — centre row colour = 55% master line colour + 45% "
        "master mouth-interior dark; adjacent rows = 65% gap colour + 35% "
        "underlying master pixel; 3 rows for x536-548, 2 rows for "
        "x531-535/x549-553; pixels inside U or outside P are skipped.",
    "hair_back":
        "R1-04: 6 garment-gold pixels (b<=70 family, y>=300) replaced with "
        "strand-continuation diffusion seeded by surrounding hair_back "
        "strands and head skin.",
    "diadem_gold": "",
    "ear_left": "", "ear_right": "", "eye_left": "", "eye_right": "",
    "eyebrow_left": "", "eyebrow_right": "", "nose": "",
}

ALPHA_NOTES = {
    "beard": "alpha equals master alpha inside the beard region; RGB inside "
             "M and the U underdraw reconstructed (cloned texture)",
    "head_base": "alpha equals master alpha inside the domain-bounded region; "
                 "feature-interior, moustache-footprint, and neck-clean RGB "
                 "reconstructed",
    "moustache": "alpha re-solved on 353 px (ink-blend decontamination) and "
                 "zeroed on 2 pure-underlay px; all other pixels keep the v2 "
                 "extraction alpha (253/254), which is <= master alpha",
    "lower_face_open_test": "alpha equals master alpha inside footprint P; "
                            "336 U-underdraw and 59 opening px RGB "
                            "reconstructed",
    "lower_face_neutral": "alpha equals master alpha inside footprint P; "
                          "336 U-underdraw px RGB reconstructed",
    "hair_back": "alpha equals master alpha; 6 garment px RGB reconstructed",
}


def digest(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def bbox_of(mask):
    ys, xs = np.nonzero(mask)
    return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]


def main():
    meta = json.load(open(V4 + "/code/_sprite_meta.json"))
    M = np.load(V4 + "/code/_M.npy")
    P = np.load(V4 + "/code/_P.npy")
    U = np.load(V4 + "/code/_U.npy")
    opening = np.load(V4 + "/code/_opening.npy")
    neck_clean = np.load(V4 + "/code/_neck_clean.npy")
    ink_head = np.load(V4 + "/code/_ink_head.npy")
    ink_beard = np.load(V4 + "/code/_ink_beard.npy")
    patch_ink = np.load(V4 + "/code/_patch_ink.npy")
    mo_rec = np.load(V4 + "/code/_mo_rec.npy")

    records = []
    for sid, rel, (px, py), parent in SPRITES:
        path = V4 + "/" + rel
        mask_path = V4 + "/masks/%s.png" % sid
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
        "version": "layout01-v4",
        "revision": "layout01-v4 is bounded revision 1 of layout01-v3 "
                    "(Codex verification-01 blockers R1-01..R1-04). v3 files "
                    "are unchanged; this candidate supersedes v3 locally: "
                    "mouthless moustache remnant, moustache-footprint "
                    "underdraw, small-open test opening, and lower-neck "
                    "garment cleanup.",
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
        "preview_only_assets": [
            "code/_u_neutral.npy — QA render of the neutral group without "
            "the moustache, used to expose the underlay surface for R1-02 "
            "inspection (plates R1_02_moustache_ghost.png). Not a rig "
            "component and not a facial state."
        ],
        "supported_motion_envelope": {
            "view": "front",
            "description": "Offline micro-offset stress envelope over the "
                           "actual layer files with the static receiver and "
                           "static moustache foreground; moustache-shift "
                           "samples additionally assert the vacated strip "
                           "renders byte-exactly as the moustache-free "
                           "underlay (R1-02).",
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
                "pixels": int(M.sum()), "bbox": bbox_of(M),
                "meaning": "master mouth content replaced by the beard "
                           "receiver (smile line, lips, interior, corner "
                           "strokes); identical to v3",
            },
            "patch_footprint_P": {
                "pixels": int(P.sum()), "bbox": bbox_of(P),
                "meaning": "common stable footprint of both lower-face "
                           "patches; irregular contour traced from M, not a "
                           "rectangle; identical to v3",
            },
            "moustache_footprint_U": {
                "pixels": int(U.sum()), "bbox": bbox_of(U),
                "underdrawn_in": {
                    "head_base (diffused skin)": int(ink_head.sum()),
                    "beard (cloned texture, outside M)": int(ink_beard.sum()),
                    "lower_face patches (art diffusion)": int(patch_ink.sum()),
                },
                "meaning": "R1-02: full v2 moustache matte underdrawn in "
                           "every layer beneath the movable feature so "
                           "+-1px offsets expose clean surfaces",
            },
            "moustache_decontamination": {
                "solved_px": int(mo_rec.sum()),
                "dropped_px": 2,
                "kept_source_px": 1465,
                "meaning": "R1-01: ink-blend pixels re-solved as "
                           "(alpha, RGB) pairs; removes the warm crescent "
                           "in state A over the beard clone",
            },
            "opening": {
                "pixels": int(opening.sum()), "bbox": bbox_of(opening),
                "meaning": "R1-03: synthesized small-open test at the actual "
                           "lip parting line (master y240 line)",
            },
            "neck_cleanup": {
                "pixels": int(neck_clean.sum()), "bbox": bbox_of(neck_clean),
                "hair_back_px": 6,
                "meaning": "R1-04: garment gold / blend fringe / pale trim "
                           "replaced with strand-continuation diffusion",
            },
            "codex_crescent_bbox": [530, 230, 542, 237],
            "clone_block": [270, 293, 494, 604],
            "uncovered_domain_pixels_assigned": 1828,
        },
        "known_limitations": [
            "Structural and programmatic validation only: no Codex visual "
            "acceptance, Claude independent review, or human artistic "
            "approval is claimed.",
            "The implementing model cannot view rendered images; every "
            "visual property in this revision was verified programmatically "
            "(pixel classifiers, masks, composites, diff counts). Codex and "
            "the human retain visual judgement (see previews/plates/).",
            "Front-view micro-offset envelope only (patch (0,0),(+-2,0),"
            "(0,+-2); moustache (+-1,0),(0,+-1)); no perspective turn, "
            "rotation, or arbitrary articulation support is claimed.",
            "lower_face_open_test is one technical small-open test state, "
            "not the start of a viseme library.",
            "Reconstructed (non-master) pixels in this candidate: beard "
            "receiver M (2616 px) plus U underdraw (1394 head_base / 345 "
            "beard / 336 patch), moustache re-solve (353 px), opening "
            "(59 px), neck cleanup (277 + 6 px), and the v3 feature "
            "underdraw (5922 px) retained unchanged.",
            "29 moustache pixels on the top edge (y214-218 over skin) have "
            "no exact ink-blend solution over the reconstructed underlay "
            "and are kept verbatim from the v2 extraction; at rest they "
            "composite within 2 of the master.",
            "2 master pixels at (528,236) and (529,236) are genuine "
            "moustache fringe left in the underlay (adding them to the "
            "movable matte has no exact solution); they are dark-family "
            "and invisible in all three states.",
            "87 dark pixels remain in head_base inside Codex's R1-02 bbox "
            "[486,209,597,238): 86 are diffused skin fills adjacent to "
            "dark beard/strand boundaries plus 1 master stray at (556,209) "
            "retained as source art; none form the old moustache outline "
            "(vacated-strip identity checks pass exactly).",
            "Garment-family gold hidden under the diadem (62 px in "
            "hair_back y89-124, 34 px in head_base y95-99) predates this "
            "revision, is invisible in every composition, and is out of "
            "scope for this bounded repair.",
            "1828 previously-uncovered domain pixels were assigned to "
            "hair_back/diadem_gold/head_base/beard by nearest-palette "
            "rules; the assignment is heuristic and locally editable.",
            "State A intentionally differs from the master inside M and the "
            "moustache footprint (2371 px >3 RGB): that is the mouthless "
            "design plus the R1-02 underdraw, not a defect.",
            "Only the head-domain seams and the four revision-1 zones were "
            "repaired; no body/arm artwork, rig, or animation export exists "
            "in this phase.",
        ],
        "toolchain": {
            "python": "system /usr/bin/python3 (book .venv has no Pillow)",
            "pillow": "10.2.0",
            "numpy": "1.26.4",
            "editable_code": "code/",
        },
    }
    with open(V4 + "/manifest.json", "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("manifest written with %d sprites" % len(records))
    print("repair_regions: M=%d P=%d U=%d (head %d beard %d patch %d) "
          "opening=%d neck=%d mo_rec=%d" % (
              M.sum(), P.sum(), U.sum(), ink_head.sum(), ink_beard.sum(),
              patch_ink.sum(), opening.sum(), neck_clean.sum(), mo_rec.sum()))


if __name__ == "__main__":
    main()
