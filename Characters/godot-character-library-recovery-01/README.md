# Local character recovery candidate

Canonical working directory: `Characters/godot-character-library-recovery-01/`
inside `/home/mehdi/Project/leela/tahmures`.

The root-level ZIP, nested `godot-character-library-recovery-01/Characters/...`
directory and root-level manifest are received Gemini artifacts. They are
preserved as evidence, not maintained working copies. Edit this directory only.

## What actually works

- Ten source PNG hashes, two complete approval-bound indexes (146 + 128 files),
  and all 17 accepted head copies are verified before generation.
- Local cutouts, disjoint candidate partitions, masks, source/reconstruction
  provenance, actual component measurements, and source/edge review plates exist.
- Ten reusable Godot scenes load the exported layers. Their neutral composite
  matches each derived cutout exactly. No whole-image backing hides missing parts.
- Whole-pose idle/reset is supported. Independent limb/head motion, blinking,
  gaze and lip-sync are not supported by these provisional new body partitions.
- `H` in the gallery opens the separate previously accepted Tahmures head,
  including its existing blink and single-left-brow thinking test. Its original
  artwork bytes and external approval scope are preserved. The full-body source
  pose candidate and accepted head inspector are deliberately distinct results.
- Missing required resources fail explicitly. Local regression tests exercise
  successful loading, reset, unsupported states and missing resources.

## What still fails visual readiness

Gemini supplied **rectangular search windows**, not anatomical masks. Exact
recomposition proves pixel accounting; it does not prove anatomical separation,
safe joints, prop ownership or valid movement. For example, the received Tahmures
neck region is fully claimed by other windows, and Akvan's eye window contains a
large face rectangle while the prop zone contains much of the torso. These are
candidate partitions, not completed puppets. See every `qa/component-sheet.png`.

The received manifest's claimed measurements/remediations are retained under
`received_*` fields. Actual local layer counts/bounds/hashes are in
`characters/*/component-map.json`. No new art, final character, scene integration
or performance approval is recorded by these checks. Both Simurgh variants
remain separate and the chapter form is undecided.

## Reproduce locally

From the repository root, using existing system Pillow/NumPy and Godot:

```bash
rtk proxy /usr/bin/python3 Characters/godot-character-library-recovery-01/scripts/build_character_library.py
rtk proxy /usr/bin/python3 Characters/godot-character-library-recovery-01/scripts/validate_character_library.py
rtk proxy /usr/bin/python3 Characters/godot-character-library-recovery-01/scripts/tests/test_library_contract.py
rtk proxy godot --headless --path Characters/godot-character-library-recovery-01 --import
rtk proxy godot --headless --path Characters/godot-character-library-recovery-01 --script scripts/tests/rig_contract_test.gd --quit-after 20
rtk proxy godot --path Characters/godot-character-library-recovery-01
```

Gallery: `[`/`]` changes character; `B` cycles real dark/light/checker backgrounds;
`S` toggles whole-pose idle (or thinking in the head inspector); `H` opens/closes
the accepted-head inspector; `R` resets.

One evidence-producing command, with a display for actual viewport captures:

```bash
rtk proxy /usr/bin/python3 Characters/godot-character-library-recovery-01/scripts/run_local_checks.py --build --render --repository-check
```

Without `--render`, runtime tests are headless and no new visual-render proof is
claimed. Logs and `evidence/local-checks.json` distinguish expected negative-test
exits, media candidate checks and the full repository gate. Godot needs access to
its normal user-data/config directories and display; a sandbox denial is an
execution-environment failure, not an art defect. No new installation is needed.

`stage_recovery_patch.py` now produces a **plan only**. The received version
deleted an existing recovery directory, treated any validation file as approval,
and replaced silhouettes with whole-image textures. Those actions could not
deliver the claimed layered-scene integration and have been removed. Nothing
edits the rejected chapter candidate or silently advances to Phase C.

## Review evidence

- `previews/local-character-library-review-gallery.png`: actual local layer composites.
- `previews/godot/`: actual Godot viewport captures, separate from received artwork.
- `characters/*/qa/`: source comparisons, edge plates and component sheets.
- `validation.json`: technical candidate validation only.
- `evidence/local-checks.json`: actual commands and results.

The full repository check currently has the pre-existing eight stale-Persian-hash
failures (789 passing tests). This candidate does not refresh manuscript hashes,
alter review state, weaken validators or imply the full gate passed.

Next: `editorial/media-handoff/ai-studio-roadmap.md` and
`editorial/media-handoff/ai-studio-task-01.md`.
