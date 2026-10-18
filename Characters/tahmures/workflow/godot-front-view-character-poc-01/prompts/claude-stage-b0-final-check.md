# Claude read-only final check — Godot Stage B0 audio/subtitle interface

MODE = VERIFY_IMPLEMENTATION_AND_VISUAL_EVIDENCE
PHASE = GODOT_FRONT_VIEW_CHARACTER_POC_01_STAGE_B0_AUDIO_INTERFACE
ROLE = independent final checker only

GPT-Codex implemented this bounded phase because GLM reached its usage limit.
The human requested Codex implementation followed by a Claude final check.
Review the actual repository files and evidence; do not rely only on the
implementation report. Do not edit project/code/manifests, run formatters that
write, repair defects, synthesize/play narration, modify approved media, or
commit. You may write only:

`Characters/tahmures/workflow/godot-front-view-character-poc-01/reports/claude/stage-b0-final-check-02.md`

For genuine visual verification, you may also create only these derived
evidence files outside the Godot project (they do not change source, code, or
its manifest):

- `Characters/tahmures/workflow/godot-front-view-character-poc-01/reports/claude/evidence/stage-b0-fa-caption-test.avi`
- `Characters/tahmures/workflow/godot-front-view-character-poc-01/reports/claude/evidence/stage-b0-fa-caption-test.png`

The human owns voice quality, pronunciation, transcript wording, and subjective
visual approval. This check cannot approve those decisions.

## Read-only review inputs

Read:

- `.agents/skills/mehdi-context/SKILL.md`
- `.agents/skills/mehdi-media/SKILL.md`
- `.agents/skills/mehdi-bilingual/SKILL.md`
- `.agents/skills/mehdi-review/SKILL.md`
- `.agents/skills/tahmures-editorial/SKILL.md`
- `.agents/skills/tahmures-narrative/SKILL.md`
- `Characters/tahmures/workflow/godot-front-view-character-poc-01/phase-brief.md`
- `Characters/tahmures/workflow/godot-front-view-character-poc-01/ROADMAP.md`
- `Characters/tahmures/workflow/godot-front-view-character-poc-01/reports/codex/stage-b0-implementation.md`
- `Characters/tahmures/workflow/godot-front-view-character-poc-01/reports/claude/stage-b0-final-check.md` (the first-check findings)
- the live Godot project README, manifest, Stage-B0 audio helper/tests/fixtures,
  `scripts/main.gd`, `scripts/check_integrity.py`, and `scenes/main.tscn`
- `renders/stage-b0/README.md`

Stage A is accepted and protected. Its render hash is
`91bcb60405d0b3a85a0537cf01430962dc218807d4bb40aa82dacc4b25ed8b87` and its six
key-frame hashes are pinned in `scripts/check_integrity.py`.

## Review questions

1. Does `audio_subtitle_pipeline.gd` safely distinguish unsupported language,
   missing files, invalid PCM WAV metadata, and invalid WebVTT? Does it retain
   cue text faithfully, check order/duration, and avoid rewriting inputs?
2. Do the focused tests exercise valid/invalid WAVs, missing inputs, exact
   Persian text, malformed/overlapping cues, PCM block alignment, strict
   WebVTT signature boundaries, and header/cue separation? Re-run the command:

       godot --headless --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --script res://scripts/tests/audio_subtitle_pipeline_test.gd

3. Is `NarrationPlayer` genuinely inert (null stream, autoplay off, no playback
   path)? Are the installed eSpeak voices still excluded? Confirm no owner WAV,
   transcript, or WebVTT files were added.
4. Does normal Stage-A behavior remain unchanged apart from nonvisual
   diagnostic logging and the inert player node? Confirm the approved timeline,
   head assets, mouth pose, and no-speech boundary remain intact.
5. Is caption test mode explicit opt-in only, sourced from marked test fixtures,
   and unmistakably not approved narration? Does Persian use the intended
   font-fallback list and RTL text/layout direction?
6. Does the integrity checker pass and preserve the accepted AVI/frame hashes?
   Confirm current manifest hash bindings and inspect `git diff --check` output.

## Required visual check

The Codex workspace lacked usable X11/Wayland, and headless Movie Maker could
not produce frames. A prior Claude session reported that non-headless Godot
could launch with Intel/Mesa OpenGL, but no frame was created because its
write permission allowed only the report. This recheck explicitly allows the
two evidence artifacts above. If a real Godot rendering/display backend is
available, render and extract a frame:

    mkdir -p Characters/tahmures/workflow/godot-front-view-character-poc-01/reports/claude/evidence
    godot --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --write-movie Characters/tahmures/workflow/godot-front-view-character-poc-01/reports/claude/evidence/stage-b0-fa-caption-test.avi --fixed-fps 30 --quit-after 30 -- --language=fa --caption-test
    ffmpeg -y -ss 0.5 -i Characters/tahmures/workflow/godot-front-view-character-poc-01/reports/claude/evidence/stage-b0-fa-caption-test.avi -frames:v 1 Characters/tahmures/workflow/godot-front-view-character-poc-01/reports/claude/evidence/stage-b0-fa-caption-test.png

If a clip is produced, inspect the actual extracted PNG and retain the clip and
frame only at the two permitted paths above. Verify shaping,
logical/visual RTL order, punctuation, safe margins, readability, face
visibility, and the `NOT OWNER-APPROVED NARRATION` notice. Also verify that the
test frame is from Godot and that the accepted Stage-A AVI/frames were not
overwritten. Do not use a browser mockup or headless control-tree smoke as a
substitute. If your environment cannot render/view it, record the visual gate
as blocked and withhold full phase acceptance. Do not create mock or synthetic
substitute evidence.

## Scope and output

Do not reopen character-art or voice decisions. Stage B1 remains gated on
owner-provided paired human recordings, verbatim owner-confirmed EN/FA text and
subtitles, owner listening/pronunciation approval, and an explicit
mouth-motion-proxy choice. This stage does not authorize speech animation,
lip-sync, voice generation, or exports.

In the permitted report, state the actual files and commands examined, test and
integrity results, Stage-A preservation, whether genuine Godot Persian visual
evidence was inspected, limitations, and only concrete blockers. Separate
technical acceptance from visual evidence and human approval.

The bounded fixes should reject both counterexamples in the first Claude
report: PCM16 `nBlockAlign` inconsistent with channel/bit depth, and malformed
`WEBVTTgarbage` or cue timing without a blank header separator.

Finish with exactly one:

`GODOT_STAGE_B0_ACCEPTED_FOR_OWNER_INPUTS`

`GODOT_STAGE_B0_REVISION_REQUIRED`

`GODOT_STAGE_B0_TOOLING_BLOCKED`

`GODOT_STAGE_B0_OWNER_DECISION_REQUIRED`
