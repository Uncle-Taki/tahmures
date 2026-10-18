# GODOT_FRONT_VIEW_CHARACTER_POC_01 — Stage-A layout verification

**Gate:** `STAGE_A_HUD_AND_SAFE_LAYOUT_CORRECTION`

**Result:** ACCEPTED for the Stage-A technical/layout gate

**Candidate:** `Characters/tahmures/prototypes/godot-front-view-character-poc-01/`
**Review date:** 2026-10-10

## Assessment

The bounded HUD correction closes the only Stage-A layout blocker. I directly
inspected all six regenerated PNG frames: idle, blink, thinking, point hold,
point with the labeled open-test mouth, and return to neutral. The header and
Persian name stay above/left of the head; the state and progress controls stay
in the lower-left column; the temporary torso and arm notices stay outside the
character silhouette; and the point-mark label is separate from the hand and
ring. No HUD text overlaps the head, body, raised arm, or temporary-art
callouts in the inspected frames.

This accepts the revised Stage-A layout and technical prototype evidence. It
does not approve temporary body/arm artwork as permanent design, a voice, a
speaking-mouth treatment, a finished video, or publication.

## Independent checks

- `scripts/check_integrity.py`: **29/29 passed**, covering pinned inputs, 17
  approved head assets, scene references, timeline, temporary-art labels, 13
  UI rectangles, viewport margins, character/arm/mark exclusion zones,
  pairwise UI separation, and the 71-file manifest.
- `scripts/verify_render.py`: **passed**, including all 8 HUD pixel checks
  across six sampled frames. It rewrote `renders/verification.json`; the
  integrity checker passed again immediately afterward.
- Godot `--quit-after 2`: **exit 0** for English and Persian language-hook
  runs. Both report the same 18-second visual timeline.
- Godot `--import`: **exit 0**. This review environment emitted errors while
  attempting to open a local socket and write global editor settings under
  `/home/mehdi/.config/godot`; resource scanning completed. Treat those as
  sandbox/environment limitations, not a clean-log claim.
- `ffprobe`: the actual preview is 1280×720 MJPEG, 30 fps, 540 frames,
  18.000 seconds, with a stereo 48 kHz PCM track.
- `ffmpeg volumedetect`: mean and maximum are both −91.0 dB, confirming the
  track is engine silence, not narration.
- `git diff --check`: clean. Repository status reports broad `Characters/`
  and unrelated `li*3` as untracked. This review does not attribute every
  file in that existing untracked tree to the current correction.
- `make check PYTHON=.venv/bin/python`: **passed** — 787 Python tests, Go
  tests, lint/format, chapter and continuity checks, translation/editorial
  parity, offline experiments, and both strict documentation builds. The
  existing six `Agentها` heuristic warnings remain; editorial errors are 0.

## Scope and remaining gate

The GLM report and project manifest describe changes confined to the Godot
prototype. The approved facial source remains hash-bound and passes the
project checker. No manuscript, accepted media blueprint, review status,
glossary, or shared implementation change is indicated.

Actual narration integration is not ready to execute yet. The expected
`audio/en/narration.wav` and `audio/fa/narration.wav` do not exist; the folders
contain only their README files. The owner rejected both eSpeak voices, and
they must not be retried or substituted. Stage B1 needs exact owner-confirmed
EN/FA transcripts and an explicit decision about whether the existing
small-open test state may be used as a simple speech-motion proxy. It is not
phoneme artwork and must not be described as lip-sync.

## Decision

**Stage-A layout correction: ACCEPTED.** The next GLM task is a concrete
audio/subtitle-interface scaffolding phase that can proceed without recordings.
Actual narrated exports remain gated on owner-provided recordings, transcripts,
and the mouth-motion choice.
