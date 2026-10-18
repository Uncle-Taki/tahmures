# Tahmures Layout 01 — V2 Extraction Report

**Final classification: TAHMURES_LAYOUT01_V2_PARTIAL_MANUAL_REPAIR_REQUIRED**

## Authority and provenance
- Source: `source/approved_master.png` (1086 × 1448, SHA-256 3eedfaa5a41965c45a137a74a9137c6e59304a0604f877a81c98870c64dba2e5).
- The previous rejected ZIP is preserved in `source/REJECTED_layout01_v1_evidence.zip` only as historical evidence; it was not used for segmentation.
- All mask coordinates were redrawn against the approved master image.
- The reconstruction reference uses saved SOURCE-POSE-ONLY underlay PNGs plus independently saved feature PNGs. It matches source pixels, but this does not demonstrate movement-ready geometry.
- An independent editable-layer assembly is saved as `previews/layout01_editable_assembly_with_seams.png`; its remaining seams are NOT concealed.

## Separation approach
- Eyes: connected components of original sclera pigment, followed by tight 3px outer-outline mask.
- Eyebrows: dark-pigment components inside anatomical curved ROIs.
- Gold diadem: gold-pigment segmentation combined with a round emblem contour.
- Hair: dark-pigment segmentation inside traced crown/left/right mass shapes. A separate hair_front is omitted because no clean meaningful strand is present.
- Nose and ears: tight local shape and colour mask extraction; not rectangular cropping.
- Beard and moustache: original dark pigments within separate lower-face regions.
- Neutral mouth: a single original mouth patch for pose reconstruction.
- Neutral mouthless face: separate preview-only composite. Never render it together with the individual components.

## Known remaining artistic limitations
- The approved source is flattened; **pixel-exact reference uses preview-only original-source underlays**. The clean editable underlay has visible seams, so artist repair is mandatory.
- Hair strand/crown and diadem occlusion contours, neck and beard attachment still require zoomed artist QA.
- Swapping or turning eyes reveals smooth skin-gradient reconstruction rather than historically recoverable original pixels.
- The dark lower beard beneath the smile is a locally interpolated reconstruction, not historically recoverable source artwork.
- Mouthless full-head composite is mutually exclusive with the standalone rig layers.
- `hair_front.png` deliberately omitted; proposed temple strips were not independently usable. Hair remains in `hair_back.png`.

## Validation results
- PASS: `source_sha256_matches`
- PASS: `all_sprite_files_exist`
- PASS: `all_masks_exist`
- PASS: `masks_match_exported_sprite_alpha`
- PASS: `all_sprite_rgba_full_canvas`
- PASS: `all_sprite_alpha_nonempty_and_has_transparency`
- PASS: `sprite_bbox_metadata_valid`
- PASS: `all_pivots_in_canvas`
- PASS: `original_source_feature_ownership_exclusive`
- PASS: `mouth_patch_is_not_rectangle`
- PASS: `preview_only_source_pose_layers_match_exactly`
- NOT VERIFIED / FAIL: `riggable_editable_layers_match_exactly`
- PASS: `preview_files_exist`
- NOT VERIFIED / FAIL: `source_art_eyebrow_nose_and_hair_manually_art_directed`
- NOT VERIFIED / FAIL: `rig_rotation_gap_free_confirmed`

- Default reference pixel-comparison mean absolute channel difference: 0.0000.
- Default reference pixels differing by more than 3 channel values: 0.
- Editable puppet-core MAE: 7.9899, pixels differing by more than 3 values: 11475. This editable output FAILS visual acceptance until repaired.
- Visual review images: `previews/layout01_original_vs_reconstruction.png`, `previews/layout01_component_QA.png`, `previews/layout01_mouthless_head.png`.

## Explicit hold before Layout 02
No mouth library or body/arm assets are produced. Await human review.
