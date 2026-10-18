# Layout 01 v3 submission contract

Candidate root: `Characters/tahmures/versions/layout01-v3/`.
All paths below are candidate-root-relative except `source_master_repo_path`.
Use JSON and real files; do not supply a report in place of sprites.

## Required files

- `manifest.json`, `files-sha256.json`, `validation-results.json`.
- Full-canvas RGBA components under `head/`, `face/`, and `mouths/`.
- Export-alpha masks under `masks/` (L-mode, exact exported alpha).
- Binary pixel-ownership masks under `provenance/`, separating retained source
  pixels from reconstructed pixels **within each sprite**. Layer overlap is
  permitted and necessary; do not impose global no-overlap between sprites.
- Immutable copy of v2 `masks/visible_head_domain.png` as the coverage domain.
- Editable local reconstruction/mask code or SVG/Bezier sources under `code/`.
- `previews/{mouthless,neutral,open_test}.png`: unadorned transparent full-canvas
  assemblies rendered from the declared sprite groups, without source underlay.
- Comparison/inspection plates A–E at 100% and enlarged head crops, on
  checkerboard, light and dark backgrounds; images of actual masks/components.
- `previews/stress/` and `stress-tests.json`: baseline and micro-motion samples,
  their transforms, coverage checks and limitation envelope.
- `implementation-report.md`: changed locations, architecture, provenance,
  actual tests, remaining defects, and no human-approval claim.

## Manifest shape

```json
{
  "schema_version": "3.0.0",
  "version": "layout01-v3",
  "character_id": "tahmures",
  "display_name_fa": "طهمورث",
  "status": "CANDIDATE",
  "human_approved": false,
  "source_master_repo_path": "Characters/tahmures/versions/layout01-v2/source/approved_master.png",
  "source_image_sha256": "3eedfaa5a41965c45a137a74a9137c6e59304a0604f877a81c98870c64dba2e5",
  "canvas": [1086, 1448],
  "coordinate_convention": "top-left origin; +x right, +y down; character-perspective left/right",
  "mouth_architecture": "B_LOCAL_LOWER_FACE_PATCH",
  "mouth_anchor": {"x": 540, "y": 241},
  "coverage_domain_path": "masks/visible_head_domain.png",
  "sprites": [],
  "render_groups": {},
  "previews": {"mouthless": "previews/mouthless.png", "neutral": "previews/neutral.png", "open_test": "previews/open_test.png"},
  "supported_motion_envelope": {},
  "known_limitations": []
}
```

Required sprite IDs: `head_base`, `hair_back`, `diadem_gold`, `ear_left`,
`ear_right`, `eye_left`, `eye_right`, `eyebrow_left`, `eyebrow_right`, `nose`,
`beard`, `moustache`, `lower_face_neutral`, `lower_face_open_test`.
Each sprite has `id`, `role: rig_component`, `path`, `mask_path`, `sha256`,
`mask_sha256`, `alpha_bounding_rect: [left,top,right,bottom]` (right/bottom
exclusive), `pivot: {x,y}`, `parent`, and `provenance`.

`provenance` contains `source_pixel_mask`, `reconstructed_pixel_mask`,
`reconstruction_method`, and any alpha/edge modifications. Both ownership masks
are binary full-canvas PNGs, disjoint within that sprite, and their union equals
its nonzero-alpha support. Pixels called original retain exact master RGB;
their alpha may only be reduced for extraction. Any altered RGB is labeled
reconstructed, including decontaminated edges. Hash every delivered file in
`files-sha256.json` except that hash index itself.

Groups `puppet_core`, `puppet_core_neutral`, `puppet_core_open_test` each have
`type: rig_composition` and one explicit `layer_order` of unique sprite IDs.
The array is authoritative. Do not supply contradictory z-index sorting.
Only one lower-face patch may be visible in each state; mouthless has none.
Keep v2's `neutral_mouth` and `neutral_face_without_mouth` out of all rig groups.
If original-pose pixel references are retained, list them separately as
`preview_only`; neither their files nor renamed copies may be rig components.

Eye pivots remain left `(579,160)`, right `(505,160)`; brow pivots left
`(579,116)`, right `(501,116)`. Reuse unmodified feature images when possible.

## Tests and limits

Render from the group and actual component files, never the approved master.
Assert the three unadorned previews equal those computed assemblies. Within a
one-pixel eroded immutable visible-head domain, require zero new fully
transparent pixels wherever the master is visible, and zero alpha-below-250
deficits wherever the master alpha is at least 250. The master itself has
partly transparent antialiased pixels: do not force those to become opaque or
shrink the domain to hide defects. Exterior edge quality is assessed visually.

Deliver micro-motion stress samples: each mouth patch at `(0,0)`, `(+2,0)`,
`(-2,0)`, `(0,+2)`, `(0,-2)`; moustache independently at `(+1,0)`, `(-1,0)`,
`(0,+1)`, `(0,-1)` over the two patch states. Use the same receiver/outer beard.
Do not move the patch or moustache outside a safe designed seam. All samples
must remain opaque in the head interior and visually coherent at source size
and zoom. If that conservative envelope cannot work without identity changes,
report the exact failing sample for a bounded architectural decision; do not
claim unrestricted gap-free animation. Whole-head rigid motion is not evidence
that local facial joints are safe.

The supplied supervisor checker is deliberately structural only. Surface
naturalness, no residual smile, beard/moustache edges, duplicate features,
identity fidelity and seam quality still require independent visual inspection.
