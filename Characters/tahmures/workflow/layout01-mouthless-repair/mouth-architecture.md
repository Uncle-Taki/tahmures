# Decision L01-MOUTH-001 — local lower-face patches

Decision: **Model B**, with a static outer beard/jaw and static moustache
foreground. Proposed for GLM implementation; final art remains unapproved.

## Evidence and alternatives

The 1086×1448 master has a small exposed mouth/skin shape integrated with the
beard, tucked immediately below the moustache. v2's `neutral_mouth` (bbox
501,229–580,268) includes skin and black beard-boundary linework. Removing it
reveals an irregular reconstructed beard surface and a smile remnant at the
moustache. A standalone mouth-only PNG cannot reproduce the local skin/beard
transition without rebuilding its surroundings.

Model A (mouthless face + static beard + mouth sprite + moustache) is useful
for a broad skin-only mouth area. Here it encourages oversized skin holes,
beard occlusion or duplicated contour lines. It would require nearly the same
surrounding patch reconstruction while pretending the mouth is independent.

Model B makes that dependency explicit: one local swappable patch carries the
mouth, its immediately surrounding skin, and only the beard geometry needed
for the state. It preserves the character's outer jaw, cheeks and silhouette.
No rectangular concealment surface and no replacement whole-head illustration.

## Composition

Bottom to top, preserving the manifest's explicit group order:

`hair_back -> head_base -> ears -> outer_beard/receiver -> lower_face_patch
 -> nose/eyes/eyebrows -> moustache -> diadem_gold`.

Use existing stable IDs (`beard` for the outer beard/receiver). Patch ordering
must be above `beard` and below `moustache`; nose/features remain appropriately
above local surfaces. Define `puppet_core` as the **mouthless** composition,
`puppet_core_neutral` as the same group plus `lower_face_neutral`, and
`puppet_core_open_test` as the same group plus `lower_face_open_test`. These
groups contain actual rig components only. Source-backed exact previews remain
separate, with `type: preview_only`.

The mouthless receiver has a continuous natural beard/lower-face surface,
with no baked mouth or smile. Neutral and small-open patches share a stable,
irregular footprint bounded to the mouth region; blend only within compatible
skin/beard tones, not across the silhouette. Keep sufficient underdraw beneath
patch and moustache margins for the explicitly tested micro-motion envelope.
Do not enlarge the patch to the full face or erase the beard identity.

Preserve mouth anchor `(540,241)` and source-space coordinates. Character
left/right means anatomical left/right, not viewer left/right. No jaw turn,
perspective turn, or large facial stretch is approved by this phase.

## Provenance and compatibility

Retain source-extracted feature pixels where possible. Newly completed hidden
skin, beard, scalp and neck surfaces are reconstructed artwork. Record their
methods and pixel-ownership masks. Existing v2 reconstructed underdraw cannot
be relabeled original source pixels. Export-alpha masks, extraction selections,
and provenance masks have distinct meanings.

Future rigging can switch one local patch while keeping the moustache/jaw
stable. This phase produces only a neutral patch and one small-open **test**,
not an 18-mouth library, viseme system, body rig, speech track or Godot scene.
