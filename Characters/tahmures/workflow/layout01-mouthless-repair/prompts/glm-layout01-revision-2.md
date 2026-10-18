# GLM bounded revision 2 — CHARACTER_LAYOUT01_MOUTHLESS_REPAIR

MODE = IMPLEMENT_AND_VERIFY

Entry: Codex checked the actual v4 layers and images. Structural checks pass
185/185 and the full repository gate is green. Three visual defects remain.
This is the second and last internal correction round. Preserve passed work;
do not restart extraction or create a new production phase. No Claude call,
provider/API, spending, art approval, Godot, TTS, video, body extraction, mouth
library, manuscripts, metadata, source hashes, skills or commits.

## Inputs and permitted outputs

Read the live `/mehdi-media`, `/mehdi-review`, `/mehdi-context`,
`/mehdi-director`, `/mehdi-narrative`, `/tahmures-narrative`,
`/tahmures-editorial` skills as needed. Read the existing workflow contract,
Model-B architecture, criteria, original handoff, revision-1 handoff and:

- `Characters/tahmures/workflow/layout01-mouthless-repair/reports/codex/verification-02/review.md`;
- its `independent-checks.json`, `structural-check.json`, actual independent
  mouth/neck/head/stress captures and `reviewed-candidate-snapshot.json`;
- v4's actual manifest, exported layers, masks, build sources and GLM report
  `Characters/tahmures/workflow/layout01-mouthless-repair/reports/glm/implementation-02.md`.

Source stays `Characters/tahmures/versions/layout01-v2/source/approved_master.png`,
SHA-256 `3eedfaa5a41965c45a137a74a9137c6e59304a0604f877a81c98870c64dba2e5`.
Preserve the immutable source, ZIP, v2, v3 and every v4 byte. Reviewed v4
manifest hash is `a83ea94b639407da685f1e2de7a570a3daa7a2c5c70f7007c7fe49eeab3d13d0`;
index hash is `1bfe5b5f9d0dbc4a35f81c5ce922cca95ae4daa3f24b01e1f428810e1be1fd08`.

Write only a NEW `Characters/tahmures/versions/layout01-v5/` candidate and
`Characters/tahmures/workflow/layout01-mouthless-repair/reports/glm/implementation-03.md`.
If v5 already exists, stop before overwriting and report it. Copy reusable v4
work with adapted output paths, never stale validation claims. Preserve eyes,
brows, nose, ears, upper hair/diadem, pivots, front-view identity, layer order,
canvas 1086×1448, mouth anchor (540,241), Model B and the two existing states.
The corrected small opening at the actual lip line is accepted for this test;
do not move it back into the beard/chin notch or expand expression scope.

## R2-01 — remove the dark mouthless remnant

Actual location: v4 mouthless A, centre below nose approximately x520–544,
y228–239, crop [480,195,610,285). See Codex
`verification-02/mouth-mouthless-6x.png` and `head-mouthless-1x.png` and GLM
`R1_01_mouthless_crescent.png`. The warm crescent is removed, but a detached
rising black smile-like stroke and broken side marks remain. Counting warm
pixels cannot close this defect.

Minimum repair: refine the local foreground moustache matte/art and adjoining
receiver to form a natural continuous surface in A, without the detached
mouth-like ink. Preserve recognizable moustache shape, nose/upper contour and
palette. The neutral/open patches must restore the visible source-mouth
relationship. Transfer local edge ownership to the patches if necessary, with
honest reconstructed provenance; do not conceal the defect with a rectangle,
full source underlay or flattened facial preview. Do not erase all dark beard
texture merely to satisfy a colour threshold.

Required tests: actual A on light/dark/checker backgrounds at source size and
4–8x; isolated moustache and receiver; a local before/after showing removal of
the dark stroke as well as warm remnants. Recheck B/C source identity. Small
source-faithful changes inside the repaired seam are allowed; pixel-exact
neutral reconstruction is not a substitute for clean independent artwork.

## R2-02 — repair colour/artwork tears in the motion seam

Actual v4 failing examples:

- `previews/stress/patch-neutral-dx0-dy2.png`;
- `previews/stress/moustache-over-neutral-dx0-dy-1.png`;
- corresponding open-test states.

Inspect crop [480,205,605,265), underside of moustache approximately
x490–550, y229–240. Codex's matching `*-8x.png` captures show light skin bars
and fragmented dark edges exposed by the required displacement. These are
opaque image seams: zero transparent holes is insufficient.

Minimum repair: design a small stable overlap/underdraw and continuous
foreground/patch interface across the union of existing tested offsets and an
antialias margin. Revisit contour ownership and exposed texture around the
old U/P boundaries, rather than diffusing only the exact old footprint.
Keep proper skin where visible and beard/ink continuous where foreground
should remain. Local mask/overlap refinements are permitted; preserve the
outer jaw/identity, full head-domain mask and explicit layer order. No broad
head redraw or new mouth states.

Required tests: repeat all 18 cases: each patch (0,0), ±2px X/Y; moustache
independently ±1px X/Y over both patch states. Save actual renders, 100% and
4–8x seam crops, plus QA-only moustache-hidden underlays. Show no discontinuous
skin bars, duplicate contour or fragment left by the old feature.

Keep coverage, footprint confinement and vacated-strip checks but describe
their limits correctly: a vacated strip equals its own underlay by ordinary
compositing even if that underlay contains bad artwork. That equality is not
proof of a clean surface. Inspect the actual underdraw and rendered boundaries.
Do not reduce offsets, omit failing samples, blacken valid skin, add an opaque
backing, or claim unrestricted rotation. If this envelope cannot work without
identity change, report the exact conflict and proposed narrow architecture
choice instead of faking a pass.

## R2-03 — replace neck scanline bands with coherent local artwork

Actual location: left neck/hair attachment approximately x467–486, y327–363;
existing repair envelope x467–606, y327–375. See
`verification-02/neck-neutral-4x.png`, source-scale head captures and v4's
`R1_04_neck.png`. Gold recolouring removed the classifier target but left
horizontal bands and a fragment-shaped wedge.

Minimum repair: use a small traced contour and deliberate continuation of the
nearby hair/neck material, matching strand direction, palette, line weight and
shading. No scanline stripes, collar-shaped recoloured islands or jagged join.
Do not redraw all hair, extract body/garment sprites, hide the neck with a
backing or shrink the fixed domain. Record every changed RGB as reconstructed.
If accurate anatomy conflicts with the fixed domain at specific pixels,
report a narrow contract conflict for Codex rather than painting arbitrary
opaque filler. The coverage requirement remains unchanged until such a
decision actually occurs.

Required tests: actual isolated head and affected layers in A/B/C on three
backgrounds, at 100% and 4–6x; show the local contour and provenance before/
after. A gold-pixel count is supplementary, not proof of a smooth surface.

## Required validation and return

Use `/usr/bin/python3`, which already supplies Pillow. Do not change the book
venv or seek an owner decision about the already established interpreter.

```bash
rtk proxy /usr/bin/python3 Characters/tahmures/workflow/tools/validate_submission.py \
  --candidate Characters/tahmures/versions/layout01-v5 \
  --baseline Characters/tahmures/versions/layout01-v2
```

Keep the original contract: actual A/B/C assemblies from exported components,
exact alpha masks, binary/disjoint per-sprite source/reconstruction ownership,
truthful source RGB claims, fixed coverage domain and intrinsic antialiasing,
valid groups/pivots/parents/paths and complete file hashes. Regenerate manifests,
reports and plates for v5. Recheck v2/v3/v4 preservation against the recorded
hashes, protected manuscript/media/tooling scope, `git diff --check` and
`make check PYTHON=.venv/bin/python`. Never alter the supervisor checker or
criteria to manufacture a pass.

In `implementation-03.md` give exactly the three defect dispositions, changed
files/coordinates, reconstruction method, actual validation/render evidence,
remaining limits and explicit image-viewing capability. If image viewing is
unavailable, state visual naturalness remains unverified; do not declare it
proven by RGB or opacity counts. Preserve all already accepted work.

Do not update approval flags or start the next phase. This is correction 2/2:
if an artistic/architecture ambiguity remains, surface it; Codex will not issue
an automatic third iteration. Claude and human review follow only after the
Codex gate passes.

Finish with exactly one:

`GLM_LAYOUT01_REVISION_2_READY_FOR_CODEX`

`GLM_LAYOUT01_REVISION_2_REVISION_REQUIRED`

`GLM_LAYOUT01_REVISION_2_TOOLING_BLOCKED`

`GLM_LAYOUT01_REVISION_2_OWNER_ART_DECISION_REQUIRED`
