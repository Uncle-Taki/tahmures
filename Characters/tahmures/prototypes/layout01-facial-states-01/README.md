# Layout 01 facial-state prototype

Input: human-approved, frozen **layout01-v7**, with explicit approval in
`Characters/tahmures/workflow/approvals/layout01-v7-human-approval.json`.
Codex implements and verifies this prototype. Claude supplies only the
near-final independent check; new pose art is not human-approved yet.

## Actual outputs

- `previews/facial-states.gif`: 8-second, 96-frame, silent looping preview.
- `previews/facial-states.webp`: same preview with exact lossless RGB frames.
- `previews/state-contact-sheet.png`: all five rendered states at source scale.
- `previews/eye-brow-zoom.png`: neutral, closed eyelids and one-pixel brow test.
- `states/*.png`: raw full-canvas transparent state assemblies.
- `frames/frame-000.png` through `frame-095.png`: actual 720×720 preview frames.
- `assets/`, `masks/`, `provenance/`: two reconstructed closed-eye patches and
  one local thinking-brow receiver; exact alpha and reconstruction ownership.
- `manifest.json`, `validation.json`, `files-sha256.json`: references, timeline,
  test evidence and complete package binding.

The neutral, mouthless and small-open states are exact approved v7 assemblies.
Only the closed eyelids and thinking receiver are new artwork. The thinking
pose is deliberately subtle: anatomical-left eyebrow rises one pixel while
eyes, nose, mouth and head remain fixed. Blinks replace both eye surfaces,
including a local skin receiver, rather than covering pupils alone. These are
reconstructed prototype assets, not recovered original pixels or final visemes.

## Reproduce and validate

From repository root, using the existing system Pillow/NumPy:

```bash
rtk proxy /usr/bin/python3 Characters/tahmures/prototypes/layout01-facial-states-01/code/render.py
rtk proxy /usr/bin/python3 Characters/tahmures/prototypes/layout01-facial-states-01/code/validate.py
```

The renderer checks the approved source approval/hashes, reads immutable v7,
and writes only this prototype. The validator independently recomposes actual
states and decodes **every** GIF/WebP frame to verify pixels and 8-second timing.
GIF uses one shared palette; WebP is exact RGB. Index the final package after
any rebuild; a changed package needs renewed review, not a stale hash claim.

Runtime: system Python, Pillow 10.2.0, NumPy 1.26.4 and existing DejaVu Sans.
No provider, TTS, paid service, installation or book dependency change. No
ffmpeg or Godot binary was present; neither is required for this GIF/WebP
prototype. It is not an MP4 export, full Godot rig or narrated video.

## Limits

Front view and independent state tests only. No combined expression transforms,
rotation/perspective, body/arms/pointing, speech phonemes or lip synchronization.
The small-open patch is the existing technical test. The eight-second state
cycle is pipeline evidence, not natural speech or a finished scene. Camera and
cropping stay fixed; the progress cursor is a QA playback indicator.

Source approval does not approve the new eyelid/receiver art. Keep this package
`PROTOTYPE_CANDIDATE` until the near-final independent check and any required
human visual signoff are recorded. No publication or commit occurred.
