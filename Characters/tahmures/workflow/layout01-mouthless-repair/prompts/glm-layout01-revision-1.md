# GLM bounded revision 1 — CHARACTER_LAYOUT01_MOUTHLESS_REPAIR

MODE = IMPLEMENT_AND_VERIFY

Entry: Codex reviewed v3 and found four visual blockers despite 185/185
structural passes. Keep the same Model-B local lower-face architecture. This
is correction 1 of at most 2 internal correction rounds, not a new production
phase. Do not call Claude, approve art, create Godot/TTS/video/body assets,
invoke providers, spend money, edit manuscripts/accepted media/skills/criteria,
or commit. Follow the live skills already required by the original handoff.

## Inputs and permitted outputs

Read the original issued handoff and submission contract, plus:

- `Characters/tahmures/workflow/layout01-mouthless-repair/reports/codex/verification-01/review.md`;
- its `structural-check.json`, `independent-checks.json`,
  `moustache-ownership.json`, independent captures and the actual v3 sprites;
- `Characters/tahmures/versions/layout01-v3/manifest.json` and build sources;
- the unchanged master at `versions/layout01-v2/source/approved_master.png`,
  SHA-256 `3eedfaa5a41965c45a137a74a9137c6e59304a0604f877a81c98870c64dba2e5`.

Write a NEW candidate to `Characters/tahmures/versions/layout01-v4/` and the
actual response to `Characters/tahmures/workflow/layout01-mouthless-repair/reports/glm/implementation-02.md`.
Keep every v3 file/hash unchanged. Copy only reusable work into v4, adapt its
version/output paths, and regenerate its reports/manifest/index with truthful
new provenance. Do not copy stale v3 validation claims as v4 results.

Preserve the passed eyes, eyebrows, nose, ears, upper hair/diadem repair,
alignment, and immutable source/domain. Revisions are local to the mouth
interface, its hidden underdraw, and the defective lower-neck join. Do not redo
source extraction or replace the whole head. The two mouth states remain
neutral and one small-open test only.

## R1-01 — remove the mouthless remnant

Location: v3 `previews/mouthless.png`, warm/ink crescent immediately below the
moustache centre at bbox [530,230,542,237), visible in
`verification-01/mouth-mouthless-8x.png`. Both `beard` and `moustache` carry
pixels there; filling only `_M` missed the residue.

Minimum repair: refine the moustache's true feature mask and local receiver so
mouthless A contains no old mouth/skin crescent. Retain the moustache's
recognizable outer form. Use reconstructed beard/skin only where needed, with
updated provenance; the neutral patch must still restore the intended source
mouth relationship. Do not hide it with a rectangle or a flattened preview.

Tests: inspect the entire mouth/moustache interface in A at 100% and 4–8×,
with light/dark/checker backgrounds; show isolated component masks and a local
before/after. Do not claim visual removal based only on the old `_M` mask or
on alpha coverage.

## R1-02 — remove baked moustache outlines beneath the movable feature

Locations: v3 `head_base` has 1,233 dark pixels matching the source moustache
within [486,209,597,238); `beard` has 346 within [498,224,585,239). The builder
does not reconstruct the full moustache movement footprint. A visible doubled
edge appears in ±1px stress samples, notably
`verification-01/stress-moustache-over-neutral-dx0-dy1-8x.png`.

Minimum repair: complete hidden skin/beard beneath the union of the moustache's
tested offsets and an antialias margin. Remove the old feature's baked outline
from underlying surfaces; preserve the real foreground moustache. Do not merely
paste original pixels under it or increase alpha. Exact-dark-colour matches
are supporting evidence, not a rule banning naturally dark beard texture.

Tests: independently shift only moustache by ±1px X/Y over both patch states;
show 100% and enlarged crops without a duplicate old edge, halo or exposed lip
residue. Repeat the patch ±2px X/Y tests and coverage checks. Also provide a
temporary inspection render with moustache hidden to expose the actual
underlying surface; this is QA only, not a new facial-state library.

## R1-03 — make the alternate test a coherent small mouth opening

Location: v3 `lower_face_open_test` modifies approximately x531–553, y253–258
at the central beard/chin notch; the lip curve immediately below moustache
remains unchanged. Compare `verification-01/mouth-neutral-8x.png` and
`mouth-open_test-8x.png`. The dark addition does not clearly part the lips.

Minimum repair: form one restrained opening at the actual lip location, with
consistent adjoining skin/beard geometry inside the same localized Model-B
patch interface. Do not preserve one mouth curve and add a second mouth mark
elsewhere in the beard. Preserve jaw silhouette, moustache identity, palette,
mouth anchor and front-view anatomy. If the source anatomy is genuinely
ambiguous, report the precise ambiguity rather than guessing a new face.

Tests: a clear neutral/open comparison from the actual components at source
scale and zoom; exactly one coherent mouth feature in C; B/C differ only in
the revised patch region. No exaggerated expression or extra mouth states.

## R1-04 — clean the lower-neck component

Locations: isolated head has clothing-colour fragments/collar remnants near
x467–606, y326–374; inspect `verification-01/neck-neutral-6x.png` and source
comparison. `build_10_sprites.py` explicitly routes low gold pixels into
`head_base` to close coverage. Those pixels are garment, not clean head/neck.

Minimum repair: trace and complete a smooth local neck/hair attachment and
remove clothing-colour contamination from the head layer. Keep source identity
and required underdraw; do not extract a torso, redraw the complete hair mass,
or conceal the defect using the original body. Preserve target coverage and
record new hidden artwork as reconstructed. Do not silently shrink the fixed
domain. If these conditions conflict for specific target pixels, report them
to Codex for a narrow contract correction instead of painting arbitrary
opaque filler or falsely declaring a pass.

Tests: isolated A/B/C head and lower-neck components on three backgrounds at
100% and zoom; no gold/garment shards, jagged neck join or new transparent gap.
Show the attachment contour and any reconstructed ownership masks.

## Required regression checks and handoff

Use the system media interpreter; do not alter the book environment:

```bash
rtk proxy /usr/bin/python3 Characters/tahmures/workflow/tools/validate_submission.py \
  --candidate Characters/tahmures/versions/layout01-v4 \
  --baseline Characters/tahmures/versions/layout01-v2
```

The original submission contract still applies: actual raw A/B/C composites,
exact export-alpha masks, honest pixel provenance, full-canvas/pivot/order
integrity, all file hashes, all 18 stress samples, and no source preview backing.
Retain the source's intrinsic antialiasing. Regenerate A–E plates and candidate
test reports only as needed to verify the four corrections. Recheck immutable
source/v2/v3 hashes, protected source scope, `git diff --check`, and the required
repository gate. Do not edit the supervisor checker to get a pass.

In `implementation-02.md` give R1-01–04 dispositions, exact files and coordinates
changed, retained versus reconstructed pixels, actual tests, remaining limits,
and explicit image-viewing limitations if you cannot inspect rendered images.
Do not declare Codex/Claude/human acceptance or start the next phase.

Finish with exactly one:

`GLM_LAYOUT01_REVISION_1_READY_FOR_CODEX`

`GLM_LAYOUT01_REVISION_1_REVISION_REQUIRED`

`GLM_LAYOUT01_REVISION_1_TOOLING_BLOCKED`

`GLM_LAYOUT01_REVISION_1_OWNER_ART_DECISION_REQUIRED`
