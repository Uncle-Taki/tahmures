# Facial-state prototype — Codex implementation report

Phase: `LAYOUT01_FACIAL_STATE_PROTOTYPE_01`. Date: 2026-10-09.
Executor: **Codex**. Input: explicit owner-approved frozen v7. The preceding
mouthless-repair phase is complete; this new prototype is not yet independently
reviewed or human-approved.

## Actual result

Built a working, deterministic Python layer-switching harness with five
rendered states: exact v7 neutral, reconstructed closed-eyelid blink,
conservative thinking/brow pose, exact v7 small-open test, and exact v7
mouthless receiver. Exported **96 720×720 PNG frames**, an **8-second silent
looping GIF**, a lossless animated WebP and source-scale/zoom inspection sheets.

Two closed-eye patches include reconstructed skin underdraw and editable SVG
eyelid arcs. They replace the entire original eye feature instead of covering
only its pupil. A separate local skin receiver supports the anatomical-left
brow's one-pixel upward shift without leaving the old brow ink behind. Eyes,
other brow, nose, jaw, diadem, hair and all original mouth art remain fixed.
New pixels are explicitly reconstructed; no recovered source-pixel claim is
made. New alpha and ownership masks are separate and exact.

The preview holds/cycles individual states with two brief blinks. It does not
combine new expression transforms, interpolate speech, synchronise audio or
demonstrate a full runtime rig. Fixed framing and a QA progress cursor make
the preview inspectable. Thinking is deliberately subtle and labeled as a
one-pixel brow test, not final character acting.

## Verification actually performed

`code/validate.py`: **51 PASS, 0 FAIL**. It checks the complete approved v7
inventory, original-master hash, explicit approval binding, assets/pivots,
exact alpha and all-reconstructed ownership, actual independent composition,
protected head coverage, approved pose equality, no eye-white residue,
full eye-footprint receiver coverage, no baked brow in the vacated strip,
changed-region confinement, 96-frame/eight-second timeline, and every decoded
GIF/WebP frame and duration. GIF pixels are checked against the saved shared
palette; WebP pixels are exact lossless RGB matches to frame PNGs. New pose art
remains `PROTOTYPE_CANDIDATE`, `human_approved: false`.

The actual renderer was rerun: all prototype output bytes reproduce identically
in the same recorded environment. Workflow evidence:
`Characters/tahmures/workflow/layout01-facial-states-01/reproducibility.json`.
Ruff lint/format checks pass for both new scripts. `git diff --check` is clean.
Full repository gate exit 0, **787 Python tests**, Go, editorial/translation,
offline experiments, parity and both strict builds pass. Known six canonical
Persian `Agentها` warnings remain outside this scope.

Codex visually inspected the actual state contact sheet, eye/brow zoom and
isolated eye surfaces. Closed eyes show a natural local skin field and single
eyelid stroke rather than pupils, white discs or circular outlines. The
thinking underlay exposes no duplicate old brow. Exact neutral/mouth states
and lower-head silhouette remain the approved v7 output. This is producer QA,
not independent or human approval of the new art.

## Scope and environment

V7's 146 indexed files and the approved master remain unchanged; protected
book/code/editorial metadata is unchanged. No provider call, paid service,
dependency installation, Godot, body/arm/pointing sprite, mouth library, TTS,
audio track, MP4, chapter video, publication, commit or push. Runtime uses
existing system Python, Pillow 10.2.0/NumPy 1.26.4 and DejaVu Sans. Neither
ffmpeg nor Godot was available; GIF/WebP require neither.

The source v7 owner approval does not automatically approve the newly created
eyelids or brow receiver. A fresh near-final Claude check follows, then record
any required human visual signoff before canonical promotion or further scope.
Codex remains responsible for corrections; Claude reviews read-only.

LAYOUT01_FACIAL_STATE_PROTOTYPE_01_READY_FOR_CLAUDE
