# Claude — independent Layout 01 final implementation review

MODE = VERIFY_AND_JUDGE

PHASE = CHARACTER_LAYOUT01_MOUTHLESS_REPAIR

You are the independent phase reviewer. GLM stopped during revision-2 analysis
because it reached its limit. The owner explicitly authorized Codex to complete
the existing v5 candidate. Codex both implemented and checked this completion;
your review must supply the independent gate. Neither Codex's opinion nor
machine passes are authority for visual naturalness or human approval.

## 1. Scope and authority

Review only the front-view Layout 01 head and its two Model-B lower-face
patches. No manuscript, metadata, glossary, continuity, skills, accepted media
blueprint or asset edit. No new mouth library, body, Godot rig, audio or video.
Do not invoke providers, spend money, commit, push or mark human approval.
Only your independent report may be written; keep candidate files immutable.

Read `AGENTS.md` and the live `/mehdi-media`, `/mehdi-review`,
`/mehdi-director`, `/mehdi-context`, `/mehdi-narrative`,
`/tahmures-narrative`, `/tahmures-editorial` skills. Read the existing accepted
01–04 continuity bible only where source/role identity is relevant. The owner
selected the imported original raster master as the visual source for this
repair. Do not redesign it to match older conceptual flat-vector candidates
or create a competing character continuity authority.

## 2. Exact input package

Repository-relative paths:

- Approved source: `Characters/tahmures/versions/layout01-v2/source/approved_master.png`.
  SHA-256 `3eedfaa5a41965c45a137a74a9137c6e59304a0604f877a81c98870c64dba2e5`,
  1086×1448 RGBA. Source ZIP:
  `Characters/tahmures/tahmures_sprites_layout01_v2.zip`, SHA-256
  `8dbe2832fe4b7728a954ae8c94ac4ca5ec5864584d7dfbbd8efd19be8e72e1f0`.
- Actual completed candidate: `Characters/tahmures/versions/layout01-v5/`.
  Read `manifest.json`, `files-sha256.json`, `implementation-report.md`,
  `validation-results.json`, `stress-tests.json`, all exported component/
  alpha/provenance PNGs, actual previews and editable completion sources.
- Workflow: `Characters/tahmures/workflow/layout01-mouthless-repair/`:
  `mouth-architecture.md`, `submission-contract.md`,
  `acceptance-criteria.json`, `source-checksums.json`, issued revision-2 prompt.
  The original contract's historical v3 path/version examples apply to the
  same shape in v5, not a request to recreate v3.
- Codex completion/verification:
  `reports/codex/completion-03/review.md`, `criterion-results.json`,
  `structural-check.json`, `independent-checks.json`, `reproducibility.json`,
  `reviewed-candidate-snapshot.json`, `make-check.log`, actual independent
  head/mouth/neck captures and `stress-contact-sheet.png`.
- Actual prior GLM reports: `reports/glm/implementation-01.md` and
  `implementation-02.md`; revision-2 partial transcript:
  `reports/glm/execution-transcript-03.txt`. There is no completed GLM
  implementation-03 report: Codex owns the completion.
- Previous exact defects: `reports/codex/verification-02/review.md` and its
  comparison captures. v4 is prior rejected evidence, never the new result.

Verify the v5 manifest/index digests against the pinned
`completion-03/reviewed-candidate-snapshot.json`, then every indexed asset
hash. If any file differs, stop acceptance and report the changed file. Use
the actual v5 files, not a source-backed pixel-perfect reconstruction.

## 3. Required actual visual inspection

Open images; do not infer quality from RGB counts, manifest claims or prose.

First inspect source and raw `previews/mouthless.png`, `neutral.png`,
`open_test.png` at the same head scale. Then inspect:

- `previews/plates/D_source_comparison.png`;
- `D_head_100_{light,dark,checker}.png`;
- `D_mouth_zoom.png` and `D_mouth_{light,dark,checker}.png`;
- `D_neck_zoom.png` and `D_neck_{light,dark,checker}.png`;
- `E_moustache.png`, `E_beard.png`, `E_head_base.png`, both patch plates;
- `E_components_0..3.png`, `E_masks_0..3.png`, `E_provenance_0..3.png`;
- `E_underlay.png` (QA-only moustache-hidden render, never a rig state);
- all 18 actual `previews/stress/*.png`, their named zoom plates, and the
  Codex stress contact sheet. Inspect concerning cases individually.

Evaluate at source scale and zoom. Tiny source antialiasing is not by itself a
defect; zoom must expose functional seams, not impose impossible raster
perfection. If your interface cannot view images, state that limitation and
do not issue visual acceptance based only on numeric tests.

## 4. Three exact closure questions

### R2-01: mouthless remnant

Does A genuinely have a continuous natural moustache/beard receiver without
the old detached rising black smile/notch stroke or residual lip/skin crescent?
Inspect approximately x520–544,y228–239 and the surrounding interface. Preserve
the recognizable upper moustache/nose relationship. The repaired receiver is
intentional hidden artwork, not a claim of original mouthless source pixels.

### R2-02: shared patch/moustache interface

Do neutral/open insertion and the declared independent offsets remain
coherent, without old baked outlines, doubled lips, detached skin bars or torn
ink inside the moustache? Pay special attention to patch dy=+2, patch dy=-2,
and moustache dy=-1 over both states. Are the slightly changed lower contour
and upper patch overlap still consistent with source identity?

The old vacated-strip comparison is compositing consistency only: a dirty
underlay can pass it. Inspect the actual hidden surfaces and shifted edges.
Likewise, coverage passes do not prove natural geometry. An appropriate
visible lip movement is not automatically a tear. Only independent axial
offsets are claimed; simultaneous transforms/rotation are outside this gate.

### R2-03: neck attachment

Did the horizontal bands and garment-fragment recolouring become coherent
local hair/neck artwork? Inspect x463–606,y326–375, especially the left wedge.
Does the source-scale head retain a clean attachment, source skin and stable
silhouette without gold collar shards or arbitrary filler? The immutable
coverage domain is still retained; assess any silhouette limitation honestly.

## 5. Whole delivered-head integrity

Check all L01-01..18 criteria, without reopening upstream chapters/media:
forehead/diadem/hair coverage, jaw and neck seams, skin/beard boundary, eye/brow
pivots, identity/palette fidelity, natural A/B/C, no rectangles or duplicated
features, real movable components and correct Model-B order
`beard -> lower_face_patch -> moustache`. Require one patch per state;
mouthless has none. No preview-only original-master backing may be in any
puppet group. All source/reconstructed ownership and exact alpha masks must
match actual assets. Reconstructed RGB and increased/modified alpha cannot be
claimed as extracted source pixels.

Neutral v5 deliberately differs locally from the original at the rebuilt
interface. Do not demand pixel identity in place of clean independent layers.
Conversely, do not accept a changed face just because it is easier to animate.
The small-open state is one restrained technical opening at the true lip
line, not a final speech viseme. No omnidirectional head or production rig is
being certified.

## 6. Independent machine verification

From repository root, all shell commands use `rtk`:

```bash
rtk proxy /usr/bin/python3 Characters/tahmures/workflow/tools/validate_submission.py \
  --candidate Characters/tahmures/versions/layout01-v5 \
  --baseline Characters/tahmures/versions/layout01-v2
rtk proxy git diff --check
```

Use `/usr/bin/python3` for Pillow; the book venv is not the media interpreter.
Do not modify the checker or build/finalize scripts to obtain a pass. Do not
execute a builder inside the submitted candidate: it would mutate the package.
For additional recompositions/captures, write only to `/tmp` or your assigned
report directory. Independently resolve layer order, masks, pivots and paths;
reproduce declared offsets where practical. Review the actual full-gate log
and scope/hash snapshots. A fresh full book gate is optional for this read-only
review; it does not replace visual QA.

## 7. Result and allowed output

Write your actual report to:
`Characters/tahmures/workflow/layout01-mouthless-repair/reports/claude/final-review-01.md`.
Include: submitted manifest/index hashes, viewed-image inventory, executed
checks/results, L01 criterion table, R2-01/02/03 closure, identity and motion
assessment, provenance/scope, known limitations, blockers and verdict.

Classify findings as `BLOCKER`, `NONBLOCKING`, or `OWNER_ART_DECISION`.
For each blocker give file/component, source coordinates or exact sample,
defect, minimum correction and required proof. Do not redesign the character
or ask for a full facial-expression library. Human preference approval remains
separate even if your independent review accepts the implementation.

Accept only if the actual delivered head is a clean, usable local front-view
candidate within its explicitly tested limits. If you reject, identify only
the specific remaining defects. If a genuine subjective identity choice is
needed, identify it precisely. Do not edit workflow acceptance/status fields
yourself; Codex will record your actual report afterward. No human art approval,
asset freezing or next-phase implementation is permitted by this prompt.

Finish with exactly one:

`CLAUDE_LAYOUT01_ACCEPTED`

`CLAUDE_LAYOUT01_REVISION_REQUIRED`

`CLAUDE_LAYOUT01_OWNER_DECISION_REQUIRED`
