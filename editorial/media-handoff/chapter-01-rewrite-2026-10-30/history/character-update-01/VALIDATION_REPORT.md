# Validation report — 2026-10-30

- `/usr/bin/python3 .../scripts/build_packages.py`: exit 0. Created both language editions and two visual contexts; 11 editorial units, 44 proposed action-led shot cards per branch, 66 spoken cues per language, 14 physical character copies.
- `/usr/bin/python3 .../scripts/validate_packages.py`: exit 0, PASS. Checks paired blocks, scene/source coverage, unique IDs, exact once-per-block shot coverage, speaker cast, script/cue text consistency, relative package paths, image decoding/dimensions/alpha, copied-byte hashes, source evidence paths and 203 protected pre-work hashes. See validation-results.json.
- `python3 story-room/scripts/validate_skill_bundle.py .`: exit 0, checked 12 skills, 0 errors.
- `make check PYTHON=.venv/bin/python`: completed exit 0. Lint, Python/Go tests, manuscript/continuity, translations/editorial state, offline experiments, parity and both strict MkDocs builds passed. Complete captured output: make-check.log. Existing Persian heuristic warnings and MkDocs notices remain informational; they do not certify these new scripts.
- Independent machine bilingual/dramatic review: all 114 FA/EN blocks reviewed, six local wording/staging repairs applied, then reread. Verdict GO FOR OWNER READ-THROUGH; see `playscript/chapter-01-final-2026-10-30/BILINGUAL_REVIEW.md`.

## Not validated / unresolved

No timed table read was performed. No new recording, rig, exported film, scene reference, generated motion or lip-sync was produced. All timings remain TBD. Eleven editorial scenes are not eleven clips: multi-phase source beats need reviewed splits, and the long S10 teaching bridge requires modular locally held graphics and measured narration, not a single Flow generation.

Both branches lack selected Chapar/Arash and production-specific sets, props, action poses and exact frames. Paper Puppet has five portrait derivatives pending likeness review; V2 has two garment derivatives pending review. Fourteen copied portraits are documented preparation references, not fourteen newly approved performances. Background alpha was read, not synthesized. External rights verification and account state remain unestablished; no external upload was attempted.

Repository gates validate the book/code workflow, not new screenplay artistic quality, Godot media or final voice/mouth alignment. Final picture/voice review requires actual rendered outputs. The original script, selected artwork, manuscripts, continuity and previous handoff hashes are unchanged. NO external generation/upload/commit/push performed.
