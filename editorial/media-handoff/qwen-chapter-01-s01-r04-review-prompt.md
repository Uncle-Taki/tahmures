# Qwen review — S01 r04 wide reading action

Review the next bounded part read-only, following AGENTS.md and RTK. The owner
explicitly accepted **r03 artwork/timing preview**, recorded with exact hashes in
`editorial/media-handoff/chapter-01-owner-acceptance.json`. That acceptance does
not cover new r04 motion, masks or cleanup. The rejected r02 hand close-up must
not return. No manuscript, original art, approval, historical evidence, commit,
upload, provider call or automatic repair is authorized by this review.

Current review entry:
`Characters/animations/chapter-01-candidate-01/s01-review.html`.

Read and inspect actual files under that candidate:

- `revisions/s01-r04/README.md`, `manifest.json`, `s01.gd`, `cleanup.gdshader`,
  `generation-prompt-v2.txt`, `assets/forearm-cleanup-v2.png`,
  `asset-attempts.json`, and `evidence/inspection-only-*.png`.
- `s01-motion.tscn`, `render_s01_motion.py`, its shared `render_s01.py`, and
  inherited `revisions/s01-r03/s01.gd` / `manifest.json`.
- `renders/s01-r04/{en,fa}/verification.json`, `godot-trace.json`, actual silent
  movies, ffprobe results, contact sheets and selected evidence stills. Inspect
  local full sequences/check/negative frames where available.
- `tests/s01_motion_state_test.gd`, actual `revisions/s01-r04/evidence/motion-state-tests-{en,fa}.json` outputs,
  and the r04 delivery/accepted-source check reports when present.
- Accepted `revisions/s01-r03/assets/hall-reading-wide.png`, its preserved
  preview outputs, canonical Chapter 01 setting/continuity, current production
  status, and the scoped owner-acceptance record.

State precisely which files, frames, movies and commands you actually accessed.
A web model needs actual attachments; filenames do not provide filesystem
access. Do not claim execution because a JSON report says pass.

Questions, in priority order:

1. Is the accepted wide composition preserved? No new close hand shot, flat
   material cards, vector body collage, altered face/materials or substituted
   actor/props. A source-textured exposed forearm/crystal should be the only
   moving part. The new cleanup derivative must appear only in the bounded
   local patch. Accepted original files and their hashes must remain intact.
2. Inspect **actual moving edges** at neutral, alignment, mid-scan and settle,
   including inspection-only zooms. Do cuff/skin joins remain connected? Look
   for straight cuts, angular robe seams, old-hand ghosts, double fingers,
   lens halos, wall painted inside the sleeve, misaligned thumb/crystal, or
   occlusion errors. Do not downgrade visible defects merely because disclosed.
   Zoom images are QA evidence, not additional scenes in the movie.
3. Does the wide action communicate one crystal-assisted reading? The exposed
   forearm pivots about the fixed sleeve opening, aligns at 3.5–4.2s, scans once
   right-to-left at 4.2–5.6s, then holds. There is no new eye/blink/head/lip-sync,
   simulated optics or complete anatomical rig. Judge physical/gaze/reading
   clarity from pixels; moving a numeric anchor is insufficient.
4. Recompute grip error, signed travel, monotonicity, settle and fixed anchors.
   Verify actual pixel changes in the arm ROI and zero changes in room, face,
   silk and message-material ROIs. Actual detached-crystal, oscillating and
   whole-picture-slide fixtures must each fail their corresponding check.
   Check that this proves independent movement, not whole-image motion.
5. Verify EN/FA text and layout, all 360 actual 1280×720 captures per edition,
   12s/30fps silent MP4 streams, cue boundaries, direct seek/reset pixel equality,
   five replay states and stable recursive node counts. Exact cue text/times
   must remain unchanged. Do not infer a text-shaping backend from correct RTL.
6. Verify missing/changed resources, bad geometry/anchors/action times,
   unsupported language/fps, altered cues and output containment fail explicitly.
   Recheck should bind current code dependencies, frame hashes, movie hash,
   fresh metadata probe and full decode. Test with the book `.venv` too; the
   current validators use the standard library and installed FFmpeg/Godot.
7. Approval boundaries: r03 art accepted; r04 motion/cleanup pending. Simurgh
   and voice remain unresolved, and the full chapter is unimplemented. Source
   pixels sampled inside a polygon are limited extraction, not anatomical-rig
   approval. Do not revive rejected r02 art or rewrite Persian source hashes.

Commands from repository root:

```bash
rtk proxy .venv/bin/python Characters/animations/chapter-01-candidate-01/render_s01_motion.py --language en --fps 30 --output renders/s01-r04/en --validate-only
rtk proxy /usr/bin/python3 Characters/animations/chapter-01-candidate-01/render_s01_motion.py --language fa --fps 30 --output renders/s01-r04/fa --validate-only
rtk proxy /usr/bin/python3 Characters/animations/chapter-01-candidate-01/render_s01_motion.py --language en --fps 30 --output renders/s01-r04/en --recheck-existing
rtk proxy /usr/bin/python3 Characters/animations/chapter-01-candidate-01/render_s01_motion.py --language fa --fps 30 --output renders/s01-r04/fa --recheck-existing
```

For independent recapture, use `renders/s01-r04/qwen-en` and `qwen-fa`, omitting
the validation/recheck flag. Real display access is required; mark recapture
unverified if unavailable. Never overwrite accepted or existing candidate output.

Return separate verdicts for **visible motion quality** and **technical
reproducibility**. Use `READY_FOR_OWNER_MOTION_REVIEW`, `REWORK_REQUIRED` or
`UNVERIFIED`, with concrete frame/path/coordinate evidence, severity, consequence
and bounded repair for each finding. Explicitly report remaining visual risks
and actual access limits. Tests cannot approve a visibly broken join or unclear
reading. Suggest saving separately as
`editorial/media-handoff/qwen-chapter-01-s01-r04-review.md`.
