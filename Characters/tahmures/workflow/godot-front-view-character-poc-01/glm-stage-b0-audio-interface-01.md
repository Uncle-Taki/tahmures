# GLM execution prompt — Stage B0 audio and subtitle interface

MODE = IMPLEMENT_AND_VERIFY
PHASE = `GODOT_FRONT_VIEW_CHARACTER_POC_01_STAGE_B0_AUDIO_INTERFACE_01`
IMPLEMENTER = GLM
TECHNICAL REVIEWER = GPT-Codex
HUMAN = voice, wording, and visual-performance authority

GLM is the primary implementation agent. Implement this bounded, input-free
scaffolding task. GPT-Codex will independently validate the artifacts. Claude
is not part of this phase unless the owner separately requests near-final
review.

## 1. Authority and scope

Read `AGENTS.md`, the current workflow README and phase status, this phase's
brief/roadmap/install guide, the latest Codex verification report, and the live
Godot project README, manifest, validation record, scene, and scripts.

Project: `Characters/tahmures/prototypes/godot-front-view-character-poc-01/`
The Stage-A layout is accepted. Preserve its 18-second timeline, six approved
face-state sprites/poses, safe HUD layout, head source pixels, and temporary
body/arm labels. Do not edit manuscripts, continuity, accepted media blueprints,
glossary, review metadata, source hashes, approval records, shared tools, or
approved facial-state packages. Do not commit or publish.

This is interface scaffolding only. It does not integrate real speech or
produce bilingual narrated videos. Do not use providers, cloud TTS, paid
services, voice cloning, synthesized speech, silent audio stand-ins, or eSpeak.
The owner auditioned and rejected both installed eSpeak voices.

## 2. Record the current input state

Check whether these future owner inputs exist, but do not require them for this
scaffolding phase:

- `audio/en/narration.wav` and `audio/fa/narration.wav`
- `audio/en/narration.txt` and `audio/fa/narration.txt`
- owner instruction on whether `lower_face_open_test` may act as a simple
  two-state speech-motion proxy

The current expected state is that they are absent. Do not create any of these
files or infer transcript text. Record presence/absence in the GLM report.

## 3. Implement the replaceable audio-input interface

Make only the minimum changes needed inside the Godot project to establish and
test a future audio path:

- `-- --language=en|fa` selects a language configuration containing the
  documented WAV and transcript paths.
- Add an audio loader/player path that stays disabled and reports
  `narration: pending` when either language's WAV is absent. Missing or invalid
  input must not crash or silently fall back to eSpeak, silence, or the other
  language.
- Validate future WAV metadata and report precise failures for unsupported
  formats, empty files, or durations outside the documented timeline. Keep
  owner source files immutable; later conversions must go to derived paths.
- Keep the normal Stage-A preview behavior unchanged when no voice files
  exist. The existing silent AVI and six Stage-A frames remain untouched and
  must still match their current manifest hashes.
- Add only configuration/docs/tests needed for the interface. No permanent
  body art, new facial artwork, extra visemes, or canonical registry assets.

## 4. Subtitle interface and RTL proof

Add a small deterministic subtitle-cue reader for one documented text format
(prefer WebVTT unless the existing project has a better local convention).
The reader must preserve cue text exactly, validate time ranges and ordering,
and select the matching language file. When a transcript/cue file is absent,
show no caption and report the missing input clearly.

Test parsing with in-memory fixtures; do not save invented narration or test
audio into the project. For visual RTL/font QA, create a separate clearly
labeled test-only render or frame under `renders/stage-b0/`. It may use the
already documented suggested line
`طهمورث مکث کرد، به پرسش اندیشید و به نشانه اشاره کرد.` solely as a
`TEST FIXTURE — NOT OWNER-APPROVED NARRATION`. Do not place that fixture in the
normal scene timeline, audio folder, subtitles, or Stage-A render. Check Arabic
shaping, logical/visual bidi order, punctuation, safe margins, and any
Latin/Persian mixing. Inspect the actual generated PNG. Keep the subtitle
position outside the head/face and disclose if body overlap is part of the
temporary test layout.

Do not make captions obscure approved face states, or compromise the accepted
HUD safe layout. Keep `طهمورث` as the Persian spelling in new media. A test-only
fixture does not constitute voice, translation, or human approval.

## 5. Mouth-motion boundary

Keep the neutral mouth as the default. The existing `lower_face_open_test` is
an approved small-open test state, not an established speaking pose. Do not
animate it as speech in this phase. Do not create or imply lip-sync. The later
audio phase may use it only if the owner explicitly authorizes a simple
two-state speech proxy; otherwise mouth motion stays static. No new mouth art
or visemes are allowed here.

## 6. Scope, evidence, and tests

Keep all changed project code, input-contract docs, tests, and the test-only
caption frame inside the Godot project. Keep the GLM report at:

`Characters/tahmures/workflow/godot-front-view-character-poc-01/reports/glm/stage-b0-audio-interface-01.md`

The report must state files changed, input availability, interface behavior,
test coverage, actual Persian-frame inspection, and exact deferred requirements
for real recording integration. Distinguish the test fixture from narration.

Run and record:

- Godot `--headless --path <project> --import` and scene smoke tests for EN/FA;
- focused tests for language selection, missing audio, invalid audio metadata,
  cue parsing, missing transcript, and exact cue preservation;
- the project integrity checker, updated narrowly for newly authorized files;
- Stage-A render verification without overwriting the accepted AVI/frames;
- `ffprobe`/hash checks proving the Stage-A AVI remains unchanged and silent;
- `git diff --check` and a precise scope/status listing.

Do not run the full book gate unless shared book files or shared code changed.
Do not change the project manifest to conceal unlisted files; list all genuine
project additions and their hashes.

## 7. Exit criteria and later phase

This Stage B0 phase passes only if the project remains runnable with no audio,
the new loader reports missing input safely, cue parsing is deterministic,
Persian sample rendering is actually inspected and readable, and accepted
Stage-A output is preserved byte-for-byte.

The later Stage B1 phase requires owner-provided human-recorded EN/FA WAVs,
verbatim owner-confirmed transcripts, and an explicit mouth-motion decision.
Only then may GLM integrate real audio, align subtitles, and create two
language exports. Voice quality and pronunciation still require the owner's
actual listening approval. No synthetic audio is authorized by this prompt.

Finish with exactly one status token:

`GODOT_STAGE_B0_AUDIO_INTERFACE_READY_FOR_GPT`

`GODOT_STAGE_B0_REVISION_REQUIRED`

`GODOT_STAGE_B0_TOOLING_BLOCKED`

`GODOT_STAGE_B0_OWNER_DECISION_REQUIRED`
