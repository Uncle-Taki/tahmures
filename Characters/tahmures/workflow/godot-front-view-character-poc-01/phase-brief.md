# GODOT_FRONT_VIEW_CHARACTER_POC_01 — phase brief

## Current execution responsibility (owner instruction, 2026-10-10)

GLM reached its usage limit. GPT-Codex is now the primary implementer and
technical validator for the remaining bounded phases. Claude receives a
read-only near-final check prompt and does not implement corrections. The human
retains voice, pronunciation, and subjective visual approval. This instruction
supersedes older GLM-primary wording below; prior GLM work remains historical.

## Purpose

Continue the owner's Tahmures character proof of concept with the human-approved
front-view facial-state prototype as its head source. The proof should use one
Godot scene to produce English and Persian exports, with a blink, thinking pose,
pointing beat, spoken sample, and mouth motion synchronized to the speech.
This tests a pipeline; it does not establish final character art or publication
readiness.

## Authority and approved input

Use `Characters/tahmures/prototypes/layout01-facial-states-01/` only at the
manifest/index hashes recorded in
`Characters/tahmures/workflow/approvals/layout01-facial-states-01-human-approval.json`.
The approval covers the reviewed eyelid and brow reconstructions for continued
front-view prototype use. It does not approve a body, arm, hand, pointing pose,
speech-viseme set, or permanent character-art promotion.

Preserve the approved source v7 and all current candidate files. Any body or
pointing elements needed to test the scene must be visibly labeled temporary
prototype stand-ins and must not be added to the canonical character registry.
Keep new geometry and audio in a dedicated prototype directory.

## Proposed proof

- A Godot project with reproducible version and run/export instructions.
- Reuse the approved head components/states; implement deterministic blink,
  thinking, and the existing neutral/open mouth switch.
- Use a temporary torso/arm/hand proxy only if needed to exercise a pointing
  beat; label its provenance and noncanonical status in the project.
- Make the Godot project and visible visual rig first. The owner has auditioned
  the installed eSpeak English and Persian voices and rejected both as too
  poor for narration. Do not use them as deliverable speech.
- After the owner chooses/provides acceptable speech (preferably two short
  human-recorded WAVs), add the English and Persian tracks and check English
  pronunciation of “Tahmures” and natural Persian pronunciation of `طهمورث`.
- Drive the available mouth-state switch from audio timing/envelope and state
  clearly whether the result is amplitude-synchronized or phoneme-level
  lip-sync. Do not describe a two-state flap as full speech visemes.
- Export the same timeline twice, once per audio/language track, with text or
  subtitles rendered from the same scene configuration.

## Toolchain and voice gate

The owner installed Godot 4.7.2, FFmpeg, and eSpeak NG. The observed versions
are recorded in `toolchain-preflight.json`. The target Godot project does not
exist yet, so the project bootstrap must create `project.godot` before any
`--path` command can run. See `GODOT_INSTALL.md` for the difference between a
headless smoke test and opening/running the visible editor scene.

The owner auditioned both eSpeak voices and rejected their quality. Treat voice
selection as a later input decision, not as a blocker to the visual stage. Do
not try more eSpeak settings, substitute tones/silence as speech, or use paid
or remote TTS. GLM should create replaceable EN/FA audio slots and proceed with
visual work; actual audio synchronization and bilingual exports wait for
acceptable human recordings or a separately authorized local voice audition.

## Acceptance evidence

The phase can pass only when a reviewer can run the project and reproduce both
exports; the same scene and event timeline drive each language version; the
approved head is unchanged; the blink/thinking/mouth states are visible and
timed as declared; temporary pointing art is clearly noncanonical; both audio
tracks are real speech with documented voice/tool/version and pronunciation
review; subtitles and audio are aligned; and no paid service is required.

The historical GLM work created the project, approved-head assembly, and visual
motion. GPT-Codex implements and validates the remaining bounded phases.
Claude performs the requested near-final read-only check. Human approval is
required for any new permanent body/arm art and for voice/performance choices.

## Current status

Stage A is implemented and its bounded HUD/layout correction passed GPT-Codex
technical and rendered-frame review. The 18-second visual timeline is accepted
for continued prototyping; the torso, arms, hands, and mark remain temporary.
Stage B0 audio/subtitle interface scaffolding passed Codex validation and
Claude's read-only final check, including the Persian fixture render. Stage B1
remains gated on the owner's recordings, confirmed transcript/subtitle text,
pronunciation review, and mouth-motion choice.
Actual Stage B1 audio integration and exports require owner-provided human-
recorded English and Persian WAVs, verbatim transcript files, and an explicit
choice about whether the existing small-open test state may be used as a
simple speech-motion proxy. Both eSpeak voices remain rejected.
