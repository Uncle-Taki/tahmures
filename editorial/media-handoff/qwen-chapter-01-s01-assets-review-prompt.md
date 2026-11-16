# Qwen review — Part S01-A: minimal reconstructed art

Review the actual S01 candidate assets locally. Read AGENTS.md and its RTK
instruction first. Do not alter manuscript, original art, approval evidence,
historical/raw bundle, accepted POC or rejected project. Do not commit, push,
upload, call providers or repair files in this review. This is a read-only art
and continuity review, not owner approval.

Canonical meaning: `book/part-1/01-what-is-a-prompt.md` (The Setting), its Persian
counterpart and `book/narrative-continuity.md`. Shahrasp reads fine writing on
silk through polished crystal. Clay, folded leather/bronze tube, charcoal-marked
bark and silk are incoming materials. They are not the later found river tablet.
There is no decorative door/handle motif. Simurgh and voice remain unresolved;
neither is needed in this silent S01 unit.

Read these repository paths:

1. `Characters/animations/chapter-01-candidate-01/planning/s01-proof-specification.md`
   and `planning/review-reconciliation.md`.
2. `Characters/animations/chapter-01-candidate-01/README.md`,
   `s01-review-report.md`, `s01-manifest.json` and `build_s01_assets.py`.
3. All SVGs in `Characters/animations/chapter-01-candidate-01/assets/s01/`,
   the vendored font's `FONT-LICENSE.txt`, and `s01.gd`.
4. `Characters/godot-character-library-recovery-01/characters/shahrasp/cutout/shahrasp_cutout.png`
   and `Characters/Shahrasp.png` as identity/style references.
5. `Characters/environments/chapter-01-candidate-01/preview/bg-hall-01.png`.
6. Actual wide/contact/material stills for both languages:
   `Characters/animations/chapter-01-candidate-01/renders/s01/{en,fa}/evidence-{0030,0126,0144,0168,0240}.png`
   and `contact-sheet.jpg`. Expand brace notation to actual paths. Inspect the
   images, not only their filenames or JSON. If images are inaccessible, say so.

Questions to resolve with evidence:

- Is this visibly Shahrasp? Compare actual source face, head seam, proportions,
  robe/sleeve colour, new vector styling and posture. Does the source eye state
  communicate reading adequately? Do not equate source-pixel preservation with
  acceptance of this new pose.
- Are both arms visibly connected in wide view and the tabletop supported?
  Are feet on the painted floor, away from furniture? Does the close insert
  plausibly show these sleeves/hands, without pretending unseen surfaces were
  recovered from the source?
- Does the visible grip actually hold the crystal, including front/back finger
  overlap and alpha edges? Can the audience see fine writing through/under it?
  Numeric matching anchors alone are insufficient. No modern handled lens,
  magical beam, floating crystal or pseudo-Persian text should appear.
- Compare A before 3s, B 3–6.4s and C after 6.4s. Do crystal, silk and hand
  assignment remain consistent? Flag book/reed ghosts, disappearing props,
  disconnected wrist, impossible depth or changes across cuts.
- Are clay, leather/tube, bark and silk distinguishable and physically supported
  at intake? Does any drawing accidentally imply a new plot object or action?
- Check declared provenance, source hashes and font notice. Separate new vector
  reconstruction from source-backed art. Do not infer new character approval.

Output a concise report with verdict `READY_FOR_PROOF_REVIEW`,
`REWORK_REQUIRED` or `UNABLE_TO_VERIFY`, followed by findings with stable IDs,
severity, actual file/frame/coordinate evidence, consequence and smallest
repair. Separate blockers from optional polish. List inspected images and
commands actually run with exits; mark anything not inspected. End with exact
remaining owner choices. Suggest saving the review separately as
`editorial/media-handoff/qwen-chapter-01-s01-assets-review.md`; do not overwrite
the prior board review or modify assets. Codex will verify and repair findings.
