# Claude — v5 independent visual recheck

MODE = VERIFY_VISUAL_GATE_ONLY

PHASE = CHARACTER_LAYOUT01_MOUTHLESS_REPAIR

## Image-access preflight — before starting the gate

The previous Claude run could not view PNGs. Its report is mechanically useful,
but it did not judge whether the artwork is good or defective. Do not repeat
the same non-visual review and do not infer appearance from pixel counts.

First open the actual approved master and `D_source_comparison.png` listed
below. Confirm that you can perceive their visual content, and briefly describe
two observed visual details and which images were actually viewed. Reading a
filename, manifest, caption, RGB array or OCR output is not visual access.

If the viewer again rejects images or the model cannot view them, **stop the
preflight**. State `IMAGE_ACCESS_PREFLIGHT_BLOCKED`, quote the tool limitation,
and do not run another complete mechanical review or issue a new artwork
verdict. This operational status is not a phase acceptance token. The previous
phase gate remains open. The operator should provide PNG attachments to an
image-capable reviewer before retrying.

## Authority and unchanged submitted package

After image access succeeds, use the live media/review/narrative/editorial
skills and the original `claude-layout01-final-review.md` for authority and
criteria, narrowed to its unadjudicated visual requirements. Keep all assets,
scripts, metadata, accepted media, manuscripts and workflow gates read-only.
No provider, paid call, implementation, art approval, commit or next phase.

Source: `Characters/tahmures/versions/layout01-v2/source/approved_master.png`.
Source SHA-256:
`3eedfaa5a41965c45a137a74a9137c6e59304a0604f877a81c98870c64dba2e5`.

Candidate: `Characters/tahmures/versions/layout01-v5/`.
Manifest SHA-256:
`e4d6b58271d9baf35747b155970341790c77ae14cc11f7c6a44b422b2893fb45`.
File-index SHA-256:
`256dc1dd3f756c6e72171dd65a026a37144a600e862ff984ddd0704ed2ccf1b7`.

Read the actual previous report:
`Characters/tahmures/workflow/layout01-mouthless-repair/reports/claude/final-review-01.md`.
Retain its verified mechanical findings for this unchanged package. Check hash
binding before reuse; any difference invalidates this narrow recheck. No new
full-book gate or repeat 138-file structural audit is necessary if the binding
remains unchanged. Do not rerun the builder or mutate the hash-bound package.

## Required visual evidence

All paths below are candidate-root-relative unless otherwise specified:

1. Actual approved master above, and `previews/plates/D_source_comparison.png`.
2. Raw `previews/mouthless.png`, `neutral.png`, `open_test.png`.
3. `previews/plates/D_head_100_{light,dark,checker}.png`.
4. `previews/plates/D_mouth_zoom.png`,
   `D_mouth_{light,dark,checker}.png` in that same plates directory.
5. `previews/plates/D_neck_zoom.png`,
   `D_neck_{light,dark,checker}.png` in that same directory.
6. Actual component plates `E_moustache.png`, `E_beard.png`, `E_head_base.png`,
   `E_lower_face_neutral.png`, `E_lower_face_open_test.png`, and
   `E_underlay.png` (QA only, not a facial state).
7. Components/masks/provenance sheets `E_components_0..3.png`,
   `E_masks_0..3.png`, `E_provenance_0..3.png` in the plates directory.
8. Stress overview:
   `Characters/tahmures/workflow/layout01-mouthless-repair/reports/codex/completion-03/stress-contact-sheet.png`.
   Then inspect all 18 actual `previews/stress/*.png` at source scale; zoom
   individual high-risk cases, especially patch `dy=+2`, patch `dy=-2` and
   moustache `dy=-1` over both neutral/open states. Use their named plates.

View the images themselves. If using direct attachments, record the original
file path and hash for each attachment; clearly state any required item that
was not supplied or viewed. A contact sheet helps triage but does not replace
individual seam inspection. Do not manufacture comparisons for missing images.

## Exact unresolved visual questions

Review the appearance aspects of L01-03/04/05/06/07/09/11/12/13/14/15/16:

- R2-01: actual mouthless receiver around x520–544,y228–239 has no detached
  rising smile/notch ink or unwanted lip/skin remnant. Preserve moustache/nose
  identity; inspect the surrounding skin/beard boundary.
- R2-02: the shared patch/moustache interface has no torn ink, detached skin
  bars, doubled lips or baked feature outline in the declared independent
  axial offsets. Normal lip movement is not automatically a seam defect.
- R2-03: the repaired neck region x463–606,y326–375, especially the left
  wedge, has coherent hair/skin attachment rather than horizontal bands,
  collar shards or arbitrary filler. Assess actual source-scale significance.
- Forehead/diadem, cheek/jaw/neck, eye/brow alignment, neutral/source identity,
  small-open coherence and exterior edges remain acceptable on three
  backgrounds. Require real layered assembly, not a source-backed preview.

Codex implemented these repairs and is not the independent visual authority.
Do not adopt its PASS claim without inspecting. Do not demand pixel-perfect
neutral identity instead of independently usable local layers. Reconstructed
hidden material and the small open test are intentional; no perspective,
rotation, combined transforms, production speech or Godot readiness is claimed.
Human preference approval remains separate from your independent gate.

## Output after successful preflight

Write only:
`Characters/tahmures/workflow/layout01-mouthless-repair/reports/claude/final-review-02.md`.
Preserve report 01. Include exact package binding, image-access proof, complete
viewed-image inventory, the visual criterion dispositions, R2 closure table,
identity/motion assessment, remaining limits and verdict. Reference the prior
mechanical report; do not claim its evidence was a visual review.

Classify actual findings as BLOCKER, NONBLOCKING or OWNER_ART_DECISION. For a
blocker give file, exact sample/coordinates, observed defect, minimum repair
and required proof. No blind repaint request, broad redesign or new mouth
library. If required visual evidence is still missing after preflight, say so
and withhold acceptance rather than guessing.

When the visual review is actually performed, finish with exactly one original
phase token:

`CLAUDE_LAYOUT01_ACCEPTED`

`CLAUDE_LAYOUT01_REVISION_REQUIRED`

`CLAUDE_LAYOUT01_OWNER_DECISION_REQUIRED`

Acceptance is independent review only. Codex records the actual result, then
explicit human visual approval is still required before freezing/releasing v5.
