# Optional Qwen review — S05 r01 dusk dialogue staging

Read-only review, following AGENTS.md and RTK. Codex is the local checker;
Qwen availability is not a prerequisite. Do not edit, commit, upload, call a
provider, rewrite source hashes, grant approval or repair automatically.

Review entry:
`Characters/animations/chapter-01-candidate-01/revisions/s05-r01/index.html`.
Use this revision directory for the relative paths below.

Read `README.md`, `manifest.json`, `scene.gd`, `scene.tscn`, `project.godot`,
`preserve-head.gdshader`, `render_s05.py`, `generation-prompt.txt`, both SRT
tracks and `approval-request.json`. Inspect actual original/new Black Div art,
repaired Tahmures asset and dusk plate in `assets/`. Read the canonical Chapter
01 dusk exchange, narrative continuity, board CH01-S05-A and the six S05 cues.

Inspect actual `evidence/delivery-01/{en,fa}/s05-silent.mp4`, contact sheets,
`verification.json`, `ffprobe.json`, `frames/trace.json`, `seek/trace.json` and
`wrong-prop/0000.png`/trace. Full 450-PNG sequences and seek PNGs are local and
Git-ignored; say if unavailable rather than inferring their contents. Read the
fresh `evidence/final-recheck-01.json` and `evidence/make-check.log`. A web model
must receive actual attachments; filenames do not provide filesystem access.

Questions, in order:

1. Does the new Black Div body actually remove the stock bundle/tablet and cloth
   from both hands? Check finger anatomy, empty palms, wetness to the waist,
   boots, silhouette, neck blend and original face. Does he remain earnest,
   capable and uncertain, rather than a malicious monster? Are Tahmures's repaired
   beard and full-body source preserved? New derivative art is **unapproved**.
2. Does the actual dusk plate support every camera position? Check opening
   floor contact and scale; both head bounds clear of the caption band; no
   invented reverse art, sliding feet, furniture collision or unwanted prop.
   Dialogue frames deliberately crop the lower legs. Is the wet waist still
   readable? Name frame/time/coordinate evidence for visual defects.
3. Are all six exact board cues and speaker labels present in both languages,
   including cue gaps? Check FA glyph joins/direction and actual visual layout;
   correct text alone cannot prove pixels or a particular shaping backend.
   Do 15 seconds and the inherited cue durations permit natural reading? Do not
   silently retime or approve spoken pacing without recordings/read-through.
4. Does custody match the canonical scene? The packet is with Simurgh offscreen;
   Black Div has no tablet/packet. No actor substitution, fabricated invasion,
   added watchfires onstage or decorative doors motif. This isolated scene
   does not prove S04/S06 transition continuity in a full chapter.
5. Verify 450 actual 1280×720 frames per language, 15s/30fps silent H.264 streams,
   full decode, manifest/input/runtime binding, all caption samples, five reverse
   seek/replay cycles plus reset equality, stable recursive nodes and fixed actor
   anchors. The camera actually reframes, but **the actors remain static**.
6. Verify the actual wrong-prop fixture contains the old held bundle and fails
   the custody check, with changed body pixels and unchanged source-head ROI.
   This is a controlled regression fixture, not a general visual prop detector.
   Check bad resources, captions, anchors/camera, format, false approval/acting
   claims and output escape fail explicitly. Recheck must bind current PNGs,
   code, art, manifest and movie, then freshly probe and decode the movie.
7. Status must be honest: no new facial acting, joint performance, walk, lip-sync,
   voice or completed S05 performance. Fixed frontal gaze does not act Tahmures's
   realization. Tests and camera attention cannot satisfy the board's
   accepted-facial-state gate. S01/S02 owner review boundaries, Simurgh form,
   voice choice and the existing Persian release blockers remain separate.

Commands from repository root:

```bash
rtk proxy .venv/bin/python Characters/animations/chapter-01-candidate-01/revisions/s05-r01/render_s05.py --language en --output delivery-01/en --validate-only
rtk proxy /usr/bin/python3 Characters/animations/chapter-01-candidate-01/revisions/s05-r01/render_s05.py --language fa --output delivery-01/fa --validate-only
rtk proxy .venv/bin/python Characters/animations/chapter-01-candidate-01/revisions/s05-r01/render_s05.py --language en --output delivery-01/en --recheck-existing
rtk proxy /usr/bin/python3 Characters/animations/chapter-01-candidate-01/revisions/s05-r01/render_s05.py --language fa --output delivery-01/fa --recheck-existing
```

Independent recapture needs a real display: use `--output qwen-en` or `qwen-fa`
and omit the validation/recheck flag. Never overwrite prior output. Mark live
recapture unverified if unavailable. State files/frames/movies actually opened
and commands actually executed; a report saying pass is not your own execution.

Return separate verdicts for **visible art/staging** and **technical
reproducibility**: `READY_FOR_OWNER_ART_STAGING_REVIEW`, `REWORK_REQUIRED` or
`UNVERIFIED`. Also explicitly mark **facial performance NOT_IMPLEMENTED** and
**voice NOT_PRODUCED**. For each issue give severity, concrete evidence,
consequence and bounded repair. Do not dilute a visible defect because it is
disclosed. Suggested output:
`editorial/media-handoff/qwen-chapter-01-s05-r01-review.md`.
