# GLM — CHARACTER_LAYOUT01_MOUTHLESS_REPAIR

MODE = IMPLEMENT_AND_VERIFY

You are GLM, the bulk implementation agent. Codex is the technical supervisor;
Claude performs one independent final phase review after Codex acceptance;
the human owns final visual approval. Implement only the bounded repair below.
Do not call Claude, invoke providers, spend money, commit, push, or approve art.

## 1. Live context and exact inputs

Read the live `/mehdi-director`, `/mehdi-context`, `/mehdi-media`,
`/mehdi-review`, `/mehdi-narrative`, `/tahmures-narrative`, and
`/tahmures-editorial` skills in `.agents/skills/`. Read `AGENTS.md`, the accepted
`.zcode/media-01-04/media-continuity-bible.md`, the Chapter 01 blueprint only
where needed, and these durable workflow files:

- `Characters/tahmures/workflow/README.md`;
- `Characters/tahmures/workflow/phase-status.json`;
- `Characters/tahmures/workflow/layout01-mouthless-repair/mouth-architecture.md`;
- `Characters/tahmures/workflow/layout01-mouthless-repair/submission-contract.md`;
- `Characters/tahmures/workflow/layout01-mouthless-repair/acceptance-criteria.json`;
- `Characters/tahmures/workflow/layout01-mouthless-repair/source-checksums.json`;
- `Characters/tahmures/workflow/layout01-mouthless-repair/reports/codex/initial-diagnosis.md`.

Exact package: `Characters/tahmures/tahmures_sprites_layout01_v2.zip`, SHA-256
`8dbe2832fe4b7728a954ae8c94ac4ca5ec5864584d7dfbbd8efd19be8e72e1f0`.
The supplied filename is not suffixed `(1)` in this live repository. Inspect
its real inventory; do not invent a path or use a similarly named file.

Its verified unchanged contents are extracted at
`Characters/tahmures/versions/layout01-v2/`. Read `manifest.json`,
`extraction_report.md`, `validation_results.json`, all `head/`, `face/`,
`mouths/`, `masks/` images and relevant `previews/`.

The owner-approved master for this task is
`Characters/tahmures/versions/layout01-v2/source/approved_master.png`;
1086×1448, SHA-256
`3eedfaa5a41965c45a137a74a9137c6e59304a0604f877a81c98870c64dba2e5`.
Inspect it visually before editing. Its actual face, beard, hair, gold diadem
and colour/linework govern this repair; do not redesign it to fit older flat
vector candidates or silently revise continuity/story documents.

`source/REJECTED_layout01_v1_evidence.zip` is historical evidence, not a source
of replacement artwork. v2 is also an intermediate/rejected editable asset.
Its pixel-exact `original_pose_pixel_reference` uses preview-only underlays.
That reconstruction is not proof of a movement-ready puppet.

## 2. Preserve baseline and output scope

Inspect `git status` and record pre-existing files. Preserve the ZIP, loose
imported PNGs/report, extracted v2, source and workflow criteria/checksums.

Write repaired output only to `Characters/tahmures/versions/layout01-v3/`
and the actual implementation report to
`Characters/tahmures/workflow/layout01-mouthless-repair/reports/glm/implementation-01.md`.
If the candidate directory already contains a result, stop before overwriting
it and report its identity; obtain a new version path from Codex.

Do not change manuscripts, translations, source hashes, review status,
accepted media blueprints/bible, glossary, implementation, experiments,
character registry, skills, workflow gates, supervisor tooling or acceptance
criteria. No body/arm extraction, full Godot rig, animation export, TTS,
chapter video, mouth library, or other character/chapter assets in this phase.

## 3. Implement Model B, not a forced standalone mouth

Use **a localized swappable lower-face patch** carrying the mouth, adjacent
skin and necessary local beard shape. Keep static outer beard/jaw and a static
moustache foreground. Only `lower_face_neutral` and `lower_face_open_test`
are required. The alternate small-open state is a technical test, not the
start of an 18-state library.

Preserve the original mouth anchor `(540,241)` and full-canvas coordinates.
The original mouth patch spans approximately x=501–579, y=229–267; inspect
actual contours and trace the final small irregular interface rather than
using this bbox as a rectangle. The receiver must remain continuous beneath
the patch and moustache. Neutral/open variants should have a common stable
footprint and a narrow tone-compatible seam inside skin/beard, not at the
outer jaw. Do not extend the patch over eyes, nose, forehead or neck.

Mouthless composition: no patch, no original smile, no residual lip line or
unexpected skin-coloured hole in the beard. Make its surface visually natural
for this bearded character. Neutral composition: reproduce the original
recognizable mouth/skin/beard relationship. Alternate: a restrained small
opening, consistent palette and line weight, without duplicated lips or
moustache; no exaggerated grin or changed jaw identity.

Render order must be explicit, with `beard -> lower_face_patch -> moustache`.
Other features remain correctly stacked. Use the required Model-B group
definitions from `submission-contract.md`; do not retain contradictory z-index
sorting. Never include `neutral_face_without_mouth`, original source surfaces,
or renamed preview underlays as actual puppet components.

## 4. Repair adjoining seams only where necessary

Codex inspected visible gaps at the diadem/forehead, irregular vertical cheek
cuts and jagged neck/hair joins. Complete the hidden skin/scalp/neck and beard
underdraw with deliberate contour geometry and small overlapping coverage.
Retain original feature pixels, eye/brow alignment, nose/ear shapes, diadem
emblem, hair outline and colour wherever possible. The immutable original
head-domain mask is the coverage target; do not shrink it to make tests pass.

Preferred methods: verified masks, Pillow/OpenCV if available, editable SVG
or hand-traced Bezier shapes, colour sampling and bounded local interpolation
or inpainting when it actually suits this line art. Use available `python3`
with Pillow for media tooling; the book `.venv` currently lacks Pillow.
No global dependency or project-runtime change is authorized. A tool limitation
is reported honestly; it does not permit paid/provider generation or repeatedly
redrawing the full head.

Reconstruct only missing hidden/removed artwork needed by the layers. No flat
rectangular cover over the mouth. No broad blur that destroys ink lines. No
fake original-pixel attribution: modified RGB, inpainted skin/beard and newly
drawn contours are reconstructed, even if sampled from the original palette.
Record reusable editable sources and masks so a later correction is local.

## 5. Manifest, masks and provenance

Implement the complete `submission-contract.md` manifest. All components
remain full-canvas RGBA at 1086×1448. Keep anatomical left/right semantics.
Export each `mask_path` as an L-mode copy of the sprite's exact alpha; do not
confuse binary extraction selections with antialiased exported alpha.

Per sprite, provide disjoint binary source-pixel/reconstructed-pixel ownership
masks covering its visible support and an honest reconstruction method. Source
claims must match the master RGB exactly; alpha may only be reduced during
extraction. Keep overlap between different sprites where hidden coverage is
needed. Record pivots, alpha bboxes (right/bottom exclusive), parent IDs,
files/hashes, layer order and unapproved candidate status. Include actual
limitations and no unsupported claim of unrestricted gap-free rotation.

`original_pose_pixel_reference` may remain a separately marked preview-only
comparison if useful; it must not be the basis of the delivered puppet render.
No original-master backing image, same image under a new name, or flattened
face composite may enter any `puppet_core*` group.

## 6. Functional previews A–E

Build each directly from exported components and the manifest:

- **A mouthless:** clean actual puppet with no mouth remnant or preview underlay.
- **B neutral:** identical puppet with only the neutral lower-face patch inserted.
- **C alternate:** identical puppet with only the small-open test patch inserted.
- **D source comparison:** original approved head versus A/B/C, same scale and
  alignment, labelled truthfully; show where reconstruction changed pixels.
- **E layer inspection:** actual separate components, exact alpha masks,
  provenance masks, patch receiver/interface and layer order.

Supply unadorned full-canvas transparent A/B/C files at the manifest paths and
separate readable checkerboard/light/dark inspection plates at source scale
and 2–4× head zoom. Do not place annotations into the raw composition files.

## 7. Machine and visual tests

Run the supervisor's read-only structural checker from repository root:

```bash
rtk proxy python3 Characters/tahmures/workflow/tools/validate_submission.py \
  --candidate Characters/tahmures/versions/layout01-v3 \
  --baseline Characters/tahmures/versions/layout01-v2
```

Save stdout/exit status in the candidate test report. Do not modify the checker
to obtain a pass; report any contract/tool defect to Codex.

Also implement and run local stress tests from actual layers: neutral and
small-open patches at zero and ±2px X/Y offsets, plus moustache independently
at ±1px X/Y over both patch states. Preserve source head-domain coverage;
assert zero new fully transparent interior pixels wherever the master is
visible and zero alpha-below-250 deficits wherever the master alpha is at least
250, inside its one-pixel eroded domain. Preserve intrinsic antialiasing; do not
force the source's partly transparent boundary pixels to become opaque.
Record transform values and render
all stress samples. Report failed poses rather than adjusting/deleting the
target domain. This is a limited front-view test envelope, not a claim that
turning the character in perspective or arbitrary articulation is supported.

Verify every file/hash/path, mask/alpha equality, pivot, and group resolution.
Verify source/master/ZIP remain unchanged. Recompose groups independently and
compare with unadorned A/B/C bytes. Check that B and C truly differ and only
the intended patch changes; keep nose/eyes/brows/diadem aligned.

Inspect actual images yourself: forehead/diadem seam; jaw/neck continuity;
clean skin/beard boundary; no residual smile in A; no rectangle; no skin holes
in beard; moustache location; natural B/C; no duplicated features; light/dark
edge quality. State exactly what was visually inspected. A structure-only pass
is not artistic approval. Do not claim 100% source-pixel matching for repaired
hidden surfaces, or general rig safety based on the exact source preview.

Run `git diff --check` and `make check PYTHON=.venv/bin/python` as required by
the project; report any unrelated baseline failure without editing its source.
Scope is only this head and its tests/records, not a manuscript repair task.

## 8. Handoff

Deliver all contract files, actual sprites/masks, editable repair sources,
previews A–E, stress evidence and hashes. In the GLM report state:
inputs/checksums; selected architecture; exact repairs and coordinates;
retained versus reconstructed artwork; groups and overlap strategy; actual
machine/visual test outcomes; remaining defects/limits; exact files produced;
and recommended Codex review targets.

Do not update phase-status acceptance flags, declare Claude acceptance, request
human freezing, or start the next phase. Codex will inspect the actual result
and generate a numbered bounded correction if needed. Claude is engaged only
after Codex technical pass; human visual approval still follows.

Finish with exactly one token:

`GLM_LAYOUT01_MOUTHLESS_REPAIR_READY_FOR_CODEX`

`GLM_LAYOUT01_MOUTHLESS_REPAIR_REVISION_REQUIRED`

`GLM_LAYOUT01_MOUTHLESS_REPAIR_TOOLING_BLOCKED`

`GLM_LAYOUT01_MOUTHLESS_REPAIR_OWNER_ART_DECISION_REQUIRED`
