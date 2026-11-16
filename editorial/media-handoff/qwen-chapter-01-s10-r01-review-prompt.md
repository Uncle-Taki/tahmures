# Optional Qwen review — S10 r01

Read-only review under AGENTS.md and RTK. No repairs, commits, provider calls,
uploads, manuscript changes or approval are authorized. Codex checks locally;
external review availability does not block progress.

Entry: `Characters/animations/chapter-01-candidate-01/revisions/s10-r01/index.html`.
Read that revision's README, manifest, provenance, board snapshot, owner form
selection, approval request, exact prompts, shaders, `scene.gd`, `ripples.gd`,
`render_s10.py` and both subtitle files. Compare canonical Chapter 01 and the
S10 board rows. Inspect actual new art and S06 rider/resident sources.

Open actual EN/FA `evidence/delivery-01/*/s10-silent.mp4`, contact sheets,
verification reports, ffprobe metadata, traces and six `negative-*` captures.
Inspect local primary/seek PNGs where available, plus `evidence/final-recheck.json`
and make-check log. A filename or report does not establish that you opened
pixels, played a movie or executed a command. State actual access precisely.
Web review needs attachments, not filesystem filenames.

Check in order:

1. S10-A floor contact and scale, Tahmures beard/likeness, one new tan rolled
   message/blue cord distinct from the old tablet. Inspect cuff/hand joins at
   local 1s, 2s, 2.7s, 3.5s and 4s: no ghost thumb, detached wrist, double fingers,
   rigid cuts or unsupported receiver grip. Enlarged QA is evidence, not a new
   movie close-up. Numeric contact checks cannot excuse visible defects.
2. Custody passes once at 2s; giver withdraws by 3.5s; receiver/message remain
   stationary. This is limited release, not a complete reach/grip/departure.
   Canon does not name the second carrier: Simurgh is a staging inference.
3. Owner rule: human Simurgh indoors, bird outside. Only indoor human Simurgh
   appears in S10. Earlier exterior human S04/S06 assets need separate repair;
   do not call those reconciled or invent a transformation world rule.
4. S10-B riders approach the near bank, facing their actual travel direction,
   growing in scale, with appropriate ground/water contact and no collisions.
   Whole mounted cutouts are not an articulated horse gait. Inspect water
   ripple placement and foreground rock intersections.
5. All three village identities and S06 resident/lamp selections persist.
   Lamps actually lower, flames fade, calm face patches align without a face
   seam or renewed alarm. Held new faces are not facial animation. Check joins
   and surviving old arm/hand ghosts through motion.
6. Verify both 15s/450-frame/30fps/1280×720 silent H.264 exports, all exact
   EN/FA cue boundaries/gaps and glyph/layout pixels. The long second cue needs
   read-through; no audio timing approval exists. Check five reverse seek
   cycles and reset, stable nodes and actual controls for duplicate message,
   detached wrist, no release, wrong travel, static lamps and alarmed faces.
7. Recheck current runtime/art/source/report/frame/movie hashes, fresh ffprobe,
   full decode and all 450 encoded-frame SSIM comparisons per edition. Invalid
   resources, anchors/times, captions, form rule, formats, false performance or
   approval claims and escaping output must fail. S04's +10s downstream shift
   remains unassembled. No chapter completion or new art acceptance is implied.

Commands from repository root:

```bash
rtk proxy .venv/bin/python Characters/animations/chapter-01-candidate-01/revisions/s10-r01/render_s10.py --language en --output delivery-01/en --validate-only
rtk proxy /usr/bin/python3 Characters/animations/chapter-01-candidate-01/revisions/s10-r01/render_s10.py --language fa --output delivery-01/fa --validate-only
rtk proxy .venv/bin/python Characters/animations/chapter-01-candidate-01/revisions/s10-r01/render_s10.py --language en --output delivery-01/en --recheck-existing
rtk proxy /usr/bin/python3 Characters/animations/chapter-01-candidate-01/revisions/s10-r01/render_s10.py --language fa --output delivery-01/fa --recheck-existing
```

Independent capture needs display access and fresh `--output qwen-en/qwen-fa`
without validation/recheck flags. Never overwrite prior evidence. Bulk PNGs are
Git-ignored; report unavailable evidence honestly.

Return separate visible-quality and technical-reproducibility verdicts:
`READY_FOR_OWNER_MOTION_REVIEW`, `REWORK_REQUIRED` or `UNVERIFIED`. Give severity,
frame/time/path/coordinates, consequence and bounded repair for each finding.
Do not downgrade defects because disclosed. Explicitly state no voice, facial
animation, articulated horse gait or final scene approval. Suggested output:
`editorial/media-handoff/qwen-chapter-01-s10-r01-review.md`.
