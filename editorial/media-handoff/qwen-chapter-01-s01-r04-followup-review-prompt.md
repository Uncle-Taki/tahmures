# Qwen review — S01 r04 review reconciliation

Review this bounded follow-up read-only, following AGENTS.md and RTK. Read the
received `qwen-chapter-01-s01-r04-review.md` without changing it. Its heading
identifies Qwen (GLM implementation); do not count it as two independent reviews.
The owner accepted r03 artwork/timing only. r04 motion/cleanup remains pending.

Candidate root: `Characters/animations/chapter-01-candidate-01/`.

Inspect:

- `verify_s01_r04_review.py` and its existing production imports
  `render_s01.py` / `render_s01_motion.py`.
- `revisions/s01-r04/review-followup/reconciliation.md`, `verification.json`,
  `make-check.log`, and `reading-excerpt-{en,fa}.mp4`.
- Actual `renders/s01-r04/{en,fa,qwen-en,qwen-fa}` frames and movies, plus
  corresponding accepted r03 frames. Do not treat report assertions as execution.
- `s01-review.html`, r04 README, current production status and scoped
  `editorial/media-handoff/chapter-01-owner-acceptance.json`.

Questions:

1. Does the evidence utility compare every actual delivered frame with the
   corresponding accepted frame, require the declared 1280×720 dimensions,
   and exclude only half-open rectangle (795,190)–(905,330)? Check all eight
   mask-boundary mutations: pixels just outside must fail; inside may differ.
   Does it verify frame hashes and current capture dependencies before claiming
   720 passing pairs? Evaluate what the excluded region cannot prove.
2. Are the existing reviewer recaptures actually byte-identical (720 PNGs and
   both movies), or merely described that way in JSON? No new Godot recapture
   is claimed by this follow-up. Check fresh probes and full movie decode.
3. Confirm the evidence correction: r04 validate-only executes 15 cases but
   calls base.validate, not base.negative_cases. The follow-up explicitly runs
   the separate inherited r03 negative suite. Verify both counts and actual
   results; do not repeat the original report's combined-execution overclaim.
4. Are the review excerpts full wide frames from source interval 3.3–6.4s,
   93 silent frames each, with no new performance, close-up or production edit?
   Watch the full movies too if vision/playback access is available. Assess
   cuff joins, wall blend, occlusion and reading clarity independently of tests.
5. Are original artwork, r03 approval-bound files, r04 capture dependencies,
   full movies and the received review preserved? Does status keep r04 owner
   approval false and leave Simurgh/voice unresolved? Do not infer approval
   from this review or from static image inspection.
6. Check the recorded make check failure: 789 pass / 8 stale Persian-source
   hash failures, later targets not reached. No source hashes should be repaired
   by this media task. Production runners must remain stdlib-only; Pillow is
   required only by the new standalone offline image-QA utility.

Independent evidence reproduction from repository root, to a fresh directory:

```bash
rtk proxy /usr/bin/python3 Characters/animations/chapter-01-candidate-01/verify_s01_r04_review.py --output revisions/s01-r04/review-followup/qwen-followup-01
```

Choose another fresh suffix if that directory already exists. This writes only
new QA evidence/excerpts under review-followup, not accepted or captured output.
No provider call, repair, manuscript edit, approval edit, upload, commit or push.
Do not overwrite received reviews or existing outputs.

State exactly what you read, ran, decoded and visually viewed. Return separate
technical and visible-quality verdicts: READY_FOR_OWNER_MOTION_REVIEW,
REWORK_REQUIRED or UNVERIFIED. Supply concrete path/frame/coordinate evidence
for each actionable finding. A clean numeric comparison cannot approve the
excluded cuff/hand patch or clarity at playback speed. Save a new report as
`editorial/media-handoff/qwen-chapter-01-s01-r04-followup-review.md` if authorized
by the review environment; never replace the received r04 review.
