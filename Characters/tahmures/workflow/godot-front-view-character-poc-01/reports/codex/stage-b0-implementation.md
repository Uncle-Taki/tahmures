# Stage B0 audio/subtitle interface — Codex implementation record

## Outcome

Implemented the bounded Stage B0 input interface and an opt-in bilingual
caption-test mode. Following Claude's first final check, corrected the WAV
block-alignment validation and WebVTT signature/header-separator defects, with
regression coverage. No voice was synthesized, no recording/transcript/subtitle
input was invented as narration, and no audio was played. The installed eSpeak
voices remain rejected. Claude's bounded recheck is pending.

## What changed

- Added `scripts/audio_subtitle_pipeline.gd`: language-specific input paths,
  PCM16 WAV metadata validation, an 18-second limit, and a WebVTT parser that
  retains cue wording while rejecting invalid, empty, overlapping, or out-of-
  order cues. Missing owner inputs return `pending`; no fallback is selected.
- Added `NarrationPlayer` to the scene with `stream = null` and autoplay off.
  Runtime logs report the exact missing input paths. No playback call is wired.
- Added an opt-in `--caption-test` display that reads only test WebVTT fixtures.
  English/Persian fixture captions are explicitly marked as not owner-approved
  narration. This path adds no speech motion and does not change the normal
  scene layout.
- Added focused Godot tests and test-only EN/FA WebVTT fixtures; updated the
  project README, audio input instructions, integrity checker, and manifest.
- Closed Claude findings B0-01 and B0-02: PCM16 WAVs now require
  `nBlockAlign == channels * 2`, and WebVTT validates the exact signature
  boundary plus the mandatory blank-line separation before cues. Tests now
  include zero/wrong block alignment, malformed signature suffix, missing
  header separator, valid metadata header, and optional BOM.
- Updated the workflow roadmap/brief to record the owner's new role model:
  Codex implements and validates; Claude performs the read-only final check;
  the human retains voice and subjective approval.

## Validation evidence

- Godot 4.7.2 focused tests: **30 passed, 0 failed** after the bounded fixes.
- Godot headless normal-scene smoke: exit 0.
- Godot headless Persian caption-test-mode smoke: exit 0; fixture parsed and
  the test mode initialized without audio or speech animation.
- Prototype integrity checker: all checks passed, including the 77-file
  project manifest and original Stage-A output hashes.
- `ffprobe`: accepted Stage-A file remains MJPEG 1280×720, 30 fps, 18 seconds;
  it retains the pre-existing silent stereo PCM track.
- Stage-A AVI SHA-256 remains
  `91bcb60405d0b3a85a0537cf01430962dc218807d4bb40aa82dacc4b25ed8b87`; all six
  sampled frame hashes remain pinned by the checker.
- Repository `make check PYTHON=.venv/bin/python`: passed; 787 Python tests,
  Go tests, editorial/translation checks, experiments, parity, and strict
  English/Persian documentation builds passed. Six existing `Agentها`
  heuristic warnings remain.
- `git diff --check`: passed.

## Visual-render limitation

The current Codex workspace has no usable X11 or Wayland display. A regular
Godot Movie Maker run exits before creating a file; `--headless --write-movie`
selects the dummy rendering backend and fails when it attempts to write frames.
The failed output was removed. Therefore no Godot-generated Stage-B0 PNG/video
exists, and Persian shaping, punctuation, RTL visual order, and caption fit
have **not** been visually verified in this workspace. This remains open for
Claude's recheck. The prior Claude session reported a non-headless launch
capable of Intel/Mesa OpenGL but did not create a frame because its permission
was restricted to a report; the new check prompt permits only derived render
evidence plus the report, without source/code changes. A headless smoke is not
visual evidence.

## Deferred owner decisions

Stage B1 still requires owner-provided English and Persian WAVs, exact
owner-confirmed transcripts and subtitles, the owner's listening/pronunciation
review, and an explicit choice about whether the existing small-open test pose
may be used as a simple audio-driven mouth-motion proxy. The system does not
describe that pose as lip-sync. No human approval or final media acceptance is
claimed here.
