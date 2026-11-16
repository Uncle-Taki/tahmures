# Optional review — S02 r03 full silent scene

Read-only review under AGENTS.md/RTK. Qwen availability is optional; Codex has
implemented/captured and locally checked this unit. Do not repair, upload,
commit, push, call providers, edit manuscripts or grant owner approval.

Candidate: Characters/animations/chapter-01-candidate-01/revisions/s02-r03/.
Inspect README, manifest, motion.gd/tscn/project.godot, all three shaders,
render_s02.py, recheck_s02.py, asset-attempts.json, all generated asset prompts,
actual assets and current index.html. Inspect actual EN/FA movies, frames,
traces, seek/reset/replays and negative fixtures under evidence/delivery-02,
inspection-only joins and final-recheck-01.json. Earlier failed inspection and
delivery-01 output is retained and superseded, not active proof.

Owner approved r02 held-pose art/design with exact hashes in
editorial/media-handoff/chapter-01-s02-owner-acceptance.json. That does not approve
new sleeve/body/lower-edge reconstruction, motion or framing. Original r02 art,
old acceptance request, manifests and evidence remain unchanged. New approval
request is motion-specific and still pending. S01 r04 remains separate.

Priority review:

1. Watch actual movies. A: one coherent lowering/release with connected sleeve,
   wrist and finger overlap; tablet stops and empty palm turns down behind the
   counter front. Inspect actual moving edges, not just anchor distances. Look
   for sleeve cap cuts, stationary old sleeve ghosts, fingers baked into clay,
   doubled props, cloth seams or incorrect furniture depth. Do not excuse visible
   defects because disclosed. QA join zooms are not movie shots.
2. B/C: same tablet, seal dissolved/no identifying emblem, cord remnants,
   imperative overlay and unknown prior carrier/recipient. B is an actual-source
   crop x365..621 y290..434, with only sleeve edge at left/head outside, not an
   invented reverse set or restored S01 hand close-up. C returns to wide with
   the tablet still at intake. No Akvan receiver/three-tablet stock substitution,
   no S01 material substitution, no doors motif. Tahmures's cedar-stand action
   remains S03. Beginning already at intake is an explicit staging ellipsis,
   not a rendered walk. Read shot-override.json against canonical sources.
3. Assess the upright tablet support, small action clarity at playback speed,
   sleeve/body cleanup match and cuff/palm occlusion. Hand samples accepted
   pixels; isolated sleeve is reconstructed art with declared affine registration,
   not anatomical extraction. The generated body is used only in a bounded
   registered patch. Face/strap/boots remain source-backed, no new face action.
4. Recompute actual grip error, release separation, placed-tablet settle,
   body anchors and one custody transition. Check actual arm-region changes and
   fixed ROIs (threshold >8) in selected wide states. Camera B intentionally
   changes pixels. Actual detach/whole-slide/duplicate fixture images must
   differ and their traces must fail the named target. Numeric counts alone
   cannot prove object identity or physical support.
5. Both editions: all 480 actual 1280×720 PNGs, 16s/30fps silent single-video
   MP4, fresh probe/full decode, correct EN/FA exact cue text/timing, SRT local
   time origin 12s, caption depth/regions, scene cuts at local 6.5 and 11s,
   five replay/reset/seek pixel equality and recursive node count 20. No text
   backend, audio or full chapter completion inferred.
6. Verify source/dependency/frame/movie bindings and integrity tests: actual
   altered temporary frame/movie copies rejected. 11 malformed inputs rejected;
   unavailable/missing runtime resources must fail explicitly. Production scripts
   are standard-library-only and run with the book .venv. Output is constrained
   to fresh evidence paths; do not overwrite delivery-02 or accepted references.
7. make-check.log: 789 pass / 8 pre-existing stale Persian source-hash failures,
   exit 2, later targets not reached; no auto hash repair. Simurgh/voice remain
   unresolved and new S02 motion/cleanup is owner-pending.

Commands from repository root:

```bash
rtk proxy .venv/bin/python Characters/animations/chapter-01-candidate-01/revisions/s02-r03/render_s02.py --validate-only
rtk proxy .venv/bin/python Characters/animations/chapter-01-candidate-01/revisions/s02-r03/recheck_s02.py --report evidence/external-recheck-01.json
rtk proxy /usr/bin/python3 Characters/animations/chapter-01-candidate-01/revisions/s02-r03/render_s02.py --output evidence/external-delivery-01
```

Use fresh suffixes. Recapture needs actual display access and can take minutes;
headless import is not a frame capture. State exactly what you read, viewed,
executed and decoded, with limits if you cannot view images/video. Return
separate visible-performance and technical verdicts, concrete path/frame/pixel
findings and bounded repairs. Save a new report separately as
editorial/media-handoff/qwen-chapter-01-s02-r03-review.md.
