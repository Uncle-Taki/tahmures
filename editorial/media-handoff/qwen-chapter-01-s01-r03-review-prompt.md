# Qwen review — S01 r03 owner-rejection repair

Review this bounded repair independently. Read AGENTS.md and RTK instructions.
The owner **rejected r02 art**, specifically the flat incoming-material display
and the hand close-up. Prior technical passes do not override that rejection.
Do not alter source art, manuscript, approvals, rejected evidence or review
reports. No commits, uploads, provider calls or fixes during this review.

Current entry point:
`Characters/animations/chapter-01-candidate-01/s01-review.html`.

Read actual current files:

- Candidate `README.md`, `s01-review-report.md`, `render_s01.py`, `s01.tscn`.
- `revisions/s01-r03/manifest.json`, `s01.gd`, `shot-override.json`,
  `assets/hall-reading-wide.png` and `review-input-hashes.json` under that
  candidate directory.
- `renders/s01-r03/en/` and `renders/s01-r03/fa/`: actual movies,
  `verification.json`, `godot-trace.json`, `ffprobe.json`, contact sheets,
  `evidence-{0030,0144,0240,0357}.png` and local frames/checks if present.
- `editorial/media-handoff/chapter-01-animation-status.json`, canonical English
  Chapter 01/The Setting and narrative continuity.
- Original `Characters/Shahrasp.png` and existing hall plate as references.
- Prior `qwen-chapter-01-s01-assets-review.md` and
  `qwen-chapter-01-s01-proof-review.md` as historical reviews only.

If reviewing in a web chat, attach the actual images/movies/docs. Paths alone do
not provide access. State exactly what you inspected and what is unavailable.

Review priorities:

1. **Owner feedback first:** no rejected full-frame hand insert, flat vector
   robe/limb collage, upright material cards, block stands, or old captioned
   demonstration panels in active runtime/review page. Archived files are not
   active alternatives. Confirm the actual Godot entry loads r03.
2. **Actual art:** inspect full-resolution wide frames. Are identity, neck,
   downward gaze, single pair of arms, costume, desk height/perspective, feet,
   finger/crystal contact and natural shading coherent? Do not treat a pretty
   overview or machine pass as art acceptance. Flag concrete visible defects.
3. **Materials:** can the viewer distinguish clay, folded leather with bronze
   tube, rough charcoal-marked bark and draped silk resting on the existing
   intake counter? In particular, does the small impressed clay object read as
   a message record or merely a seal? Do not certify identities from filenames.
   No modern envelope, floating object, illegible pseudo-language presented as
   exact text, or found river tablet substitution is permitted.
4. **Honest scope:** r03 is a static illustrated wide scene with timed captions.
   It has NO independent reading scan, articulated hands, gaze animation,
   arrival/handoff, audio or full-chapter integration. The old scan/grip tests
   are retired and cannot pass this revision. The future performed reading
   requirement must remain open; no whole-picture motion may pretend to meet it.
5. **Runtime:** exact cue strings/times, proper Godot RTL rendering, readable
   captions clear of hands, 360 real frames per language, seek/reset/five replays,
   actual 12s/30fps silent movies. Test current commands with both interpreters.
   Do not infer a specific shaping backend such as RAQM from correct pixels.
6. **Qwen technical findings:** no mandatory Pillow import in the current runner;
   recheck must verify movie hash, reprobe metadata and fully decode the movie.
   Check modified movie/frame handling and stale revision evidence. Output must
   stay in `renders/s01-r03/`, protecting historical rejected outputs.
7. **Integrity:** originals and both prior review files remain unchanged. New
   AI-generated art/provenance is disclosed, not called approved or pixel-exact.
   No Simurgh/voice decision, human approval, completed reading performance or
   repaired Persian editorial hashes may be invented.

Low-cost commands from repository root:

```bash
rtk proxy .venv/bin/python Characters/animations/chapter-01-candidate-01/render_s01.py --language en --fps 30 --output renders/s01-r03/en --validate-only
rtk proxy /usr/bin/python3 Characters/animations/chapter-01-candidate-01/render_s01.py --language fa --fps 30 --output renders/s01-r03/fa --validate-only
rtk proxy /usr/bin/python3 Characters/animations/chapter-01-candidate-01/render_s01.py --language en --fps 30 --output renders/s01-r03/en --recheck-existing
rtk proxy /usr/bin/python3 Characters/animations/chapter-01-candidate-01/render_s01.py --language fa --fps 30 --output renders/s01-r03/fa --recheck-existing
```

For independent recapture use fresh directories such as
`renders/s01-r03/qwen-en` and `renders/s01-r03/qwen-fa`; omit recheck/validate-only.
Real desktop display access is required. Mark recapture unavailable if blocked.
Do not overwrite owner evidence or delete files outside your own scratch.

Return two separate verdicts: `VISUAL_REWORK_REQUIRED` / `READY_FOR_OWNER_REVIEW`
and `TIMING_PIPELINE_PASS` / `REWORK_REQUIRED` / `UNVERIFIED`. Neither verdict
approves art or a finished reading animation. Give stable findings with severity,
actual file/frame/coordinate, visible evidence, consequence and bounded repair.
State which original owner notes are addressed, which remain, and which prior
Qwen findings are superseded. List actual commands/exits and inspected frames.
Do not downgrade a visible defect to optional polish just because disclosed.
Suggest saving separately as
`editorial/media-handoff/qwen-chapter-01-s01-r03-review.md`.
