# Godot Stage A — Codex validation 01

**Decision:** bounded visual-layout correction required before voice integration.

## What passed

- Godot 4.7.2 project exists at
  `Characters/tahmures/prototypes/godot-front-view-character-poc-01/`,
  with `project.godot` and configured `scenes/main.tscn`.
- The approved facial-state package hashes match the pinned values. The
  project integrity checker independently passed **19/19** checks, including
  the 17 copied head assets, scene resource paths, main-scene config, approved
  face-state switches, timeline keys, placeholder labels, and 71-file project
  manifest.
- I independently ran `scripts/check_integrity.py`: exit 0.
- I independently ran the headless main-scene smoke test with an explicit
  writable log path: exit 0; main scene loaded and reported the first beat.
- `ffprobe` confirms the silent render is MJPEG 1280×720 at 30 fps, 540
  frames, 18.000 seconds. Its stereo PCM track is reported as digital silence,
  not narration.
- I visually inspected the six supplied timeline frames: neutral, blink,
  thinking, point hold, open-test mouth, and return to neutral. The head
  components remain aligned, blink and brow states read, and the pointing
  stand-ins are clearly marked as temporary.
- No narration is present, no eSpeak voice was used, and the project report
  does not claim lip-sync. This matches the owner's voice-quality decision.

## Blocking finding: HUD and character/callout overlap

The rendered layout does not meet the stage-A requirement for readable
state/timing markers that do not obscure the character.

- In all inspected frames, the language/debug line at approximately screen
  y=92 crosses the top hair/diadem area.
- The world-space placeholder labels sit around y=540–616.
- The dynamic StateLabel occupies approximately x=16–1000, y=606–646. Long
  strings such as the thinking and open-test labels draw across the torso and
  collide with the placeholder labels. This is visible in
  `t6.5s-thinking.png` and `t11.0s-point-open-mouth.png`.
- The time/hint/progress-bar area occupies the remaining lower strip, so the
  current layout has no clear separation between character, callouts, and
  debug UI.

This is a bounded layout defect, not a character-art or timing defect.

**Minimum correction:** place the character, temporary-art callouts, language
name, state indicator, and timeline into distinct non-overlapping screen
regions. Keep the state indicator concise (for example, IDLE, BLINK, THINK,
POINT, OPEN TEST, RETURN); move explanatory detail to the project README or
console. Preserve readable temporary-placeholder identification without
drawing text over the figure. Re-render the same key states and update hashes.

## Scope and current limits

The correction must not modify the approved head assets, animation event
times, facial-state design, voice choice, or character registry. Stage B remains
unstarted. It requires acceptable English and Persian recordings or a
separately authorized local voice audition; eSpeak remains rejected.

## Next handoff

Use
`Characters/tahmures/workflow/godot-front-view-character-poc-01/glm-stage-a-layout-revision-01.md`.
After GLM resubmits, GPT rechecks only the layout correction and preservation
of the already passing Stage-A gates. Then the owner can review the clean
visible preview. Voice integration and bilingual export follow once acceptable
voice input exists.

