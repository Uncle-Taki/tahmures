# Qwen review — Part S01-B: Godot performance and verification

Independently review the isolated silent S01 proof. Read AGENTS.md/RTK first.
Perform read-only inspection/tests; write no repairs, commit, push, uploads,
provider calls or approval-state changes. Existing reports are claims to verify.
Do not infer owner acceptance or chapter completion. Preserve manuscript,
original artwork, historical raw bundle, accepted POC and rejected project.

Read the canonical Chapter 01 setting and narrative continuity, then:

- `Characters/animations/chapter-01-candidate-01/README.md`
- `Characters/animations/chapter-01-candidate-01/s01-review-report.md`
- `Characters/animations/chapter-01-candidate-01/planning/s01-proof-specification.md`
- `Characters/animations/chapter-01-candidate-01/planning/review-reconciliation.md`
- `Characters/animations/chapter-01-candidate-01/s01-manifest.json`
- `Characters/animations/chapter-01-candidate-01/s01.gd`, `render_s01.py`,
  `project.godot`, `s01.tscn`, `build_s01_assets.py`
- `editorial/media-handoff/chapter-01-animation-status.json`
- Both `Characters/animations/chapter-01-candidate-01/renders/s01/{en,fa}/`
  `verification.json`, `godot-trace.json`, `ffprobe.json`, actual silent movie,
  selected evidence PNGs, boundary/seek/reset captures and negative-fixture
  traces/captures where present. Expand braces to real paths.
- `Characters/animations/chapter-01-candidate-01/evidence/s01-delivery-checks.json`,
  both encoded-movie sample sheets and `render_s01-capture-revision.py` in that
  evidence directory. Original capture-runner hashes refer to that archived
  revision; `image_roi_recheck` records the current runner and feature-bearing
  ROI measurements. Verify those separate hashes rather than assuming the
  capture and later verification code are the same revision.

Verify these independently, recording unavailable evidence as unavailable:

1. 12 seconds / 30fps / 360 actual 1280×720 frames per language, real encoded
   movie streams and absence of audio. Compare recorded hashes with files.
   Movie existence does not imply complete chapter or recorded narration.
2. One complete reading action: approach/alignment, one right-to-left 24px scan
   at 4.2–5.6s, stable settle, material reveal at 6.4s. Static head/eye state is
   a limitation, not newly approved acting. Watch actual motion and both cuts.
3. Grip continuity, signed monotonic progression, static support/silk/backdrop
   anchors, masked image ROIs and negative fixtures. Check that deliberately
   detached crystal, oscillating scan and whole-picture movement each fail the
   relevant measurement. Distinguish computed anchors from visible finger grip.
4. Absolute-time behavior, direct seek vs sequential playback at 2/4.8/6.4/11.9s,
   reset/replay, stable node count, half-open cue boundaries including t=12.
   Verify actual pixels/state, not only functions named seek/reset.
5. All malformed-input cases fail explicitly. Look for hidden fallbacks,
   unsupported language, missing hand/crystal/silk/font, cue changes, invalid
   crop/anchors/time and output-path hazards. Check actual runtime vs validator
   assumptions and stale-report risks.
6. Exact EN/FA cue strings against the board/plan, proper Godot Persian shaping,
   punctuation/ZWNJ, direction, actual line breaks, glyph coverage and bounds.
   Captions must not cover hands. Measured layout is not human readability or
   recording timing approval. Inspect both editions visually.
7. Provenance/source hash integrity, unchanged approved inputs, font licence,
   new-art disclosures. Identify export portability limitations without claiming
   a standalone app was delivered. All commands should use RTK.
8. Review scope/status: no Simurgh decision, voice, full-chapter integration,
   owner signoff or resolved Persian editorial gate should be invented.

Low-cost commands (repository root):

```bash
rtk proxy python3 Characters/animations/chapter-01-candidate-01/render_s01.py --language en --fps 30 --output renders/s01/en --validate-only
rtk proxy python3 Characters/animations/chapter-01-candidate-01/render_s01.py --language fa --fps 30 --output renders/s01/fa --validate-only
rtk proxy ffprobe -v error -show_streams -show_format -of json Characters/animations/chapter-01-candidate-01/renders/s01/en/s01-silent.mp4
rtk proxy ffprobe -v error -show_streams -show_format -of json Characters/animations/chapter-01-candidate-01/renders/s01/fa/s01-silent.mp4
```

For independent recapture use new output directories, never overwrite evidence:

```bash
rtk proxy python3 Characters/animations/chapter-01-candidate-01/render_s01.py --language en --fps 30 --output renders/qwen-s01/en
rtk proxy python3 Characters/animations/chapter-01-candidate-01/render_s01.py --language fa --fps 30 --output renders/qwen-s01/fa
```

This requires real display access and can take several minutes. If unavailable,
state that capture was not reproduced. Do not substitute headless success for
viewport evidence or call expected historical book-gate failures media failures.

Return `TECHNICALLY_VERIFIED_WITH_ART_REVIEW_PENDING`, `REWORK_REQUIRED` or
`UNABLE_TO_VERIFY`, with stable findings: severity, actual path/line/frame,
reproduction/evidence, consequence and bounded repair. List actual commands/exits,
watched clips/inspected frames and unverified claims. Separate pipeline defects,
story/contact blockers, art-review issues and optional polish. State whether
the next chapter part can proceed and what specifically still needs checking.
Suggest saving separately as
`editorial/media-handoff/qwen-chapter-01-s01-proof-review.md`; Codex remains
responsible for reproducing findings and fixes. No review verdict grants owner
art acceptance.
