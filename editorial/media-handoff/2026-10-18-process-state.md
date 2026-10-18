# Tahmures process state — 2026-10-18

## Current owner priority: prepare the supplied character set first

The owner rejected GLM's new chapter candidate because its named characters are
abstract stand-ins rather than the artwork supplied in `Characters/`. The
latest [inspection and recovery order](2026-10-18-glm-character-review.md) and
updated Gemini prompts supersede the proposed scene-refactor-first/scene-first
next tasks below. Prepare Tahmures and all nine newly supplied reference images
as reusable character packages, including both Simurgh variants; visually check
the complete set before chapter assembly continues. This is the new owner task
priority, not a retroactive change to historical phase approvals.

The inspection found 140 additional non-cache files in the new
`godot-chapter-01-01` candidate and nine owner reference PNGs against the earlier
inventory. Its actual renders measured about 156.47 seconds EN / 18 seconds FA
against a declared 173-second chapter plan. The original head POC's acceptance
does not certify that candidate. Preserve both source artwork and the rejected
candidate; no cleanup or rig/scene implementation was performed by this update.

This is a dated reading of existing records and files, not a second phase-status
registry or a new approval. The live media state remains
`Characters/tahmures/workflow/phase-status.json`. The book's charter, continuity
record, editorial contract and review policy retain their authority.

## What is complete, and what “complete” means

| Workstream | Current state | Meaning |
|---|---|---|
| Book foundations | Established | Bilingual technical book, 24 draft chapters, original myth-inspired teaching fiction, canonical English technical meaning, offline Python/Go examples. Draft completion is not publication approval. |
| Chapters 01–04 character/narrative adaptation | Machine review closed; current human signoff pending | Latest stored handoff is `.zcode/character-refactor-01-04/gpt-review-05.md`. Existing historical review does not approve the changed revisions. |
| Persian Chapters 01–09 | Historical human review exists | Chapters 01–04 have since changed and need current-revision signoff. |
| Persian Chapters 10–24 | No recorded human line-by-line review | Machine prechecks cannot confer human-review status. |
| V2 source / V3–V5 candidates | Preserved baseline and development history | The V2 master is the selected visual source; extracted/rejected puppets are not approved final art. |
| V6 | Preserved neck implementation input | Replaced by V7 for continued use; still consumed by V7's packaging/rebuild code. |
| V7 head repair | Completed and approved for a scoped next prototype | The head-repair phase is complete. This does not make the whole Tahmures character final or publication-ready. |
| Facial-state prototype | Completed; approved for continued front-view prototyping | Closed eyelids, thinking-brow receiver and neutral/open-test/mouthless states. No permanent full-body or speech-viseme approval. |
| Godot Stage A | Implemented and technically accepted | One 18-second silent timeline: idle, blink, thinking, temporary pointing and return. Full-canvas head sprites are assembled in the scene. |
| Godot Stage B0 | Implemented; recorded Codex/Claude acceptance | WAV/transcript/WebVTT input contract and test captions exist. Narration playback and audio-driven mouth motion are not implemented by this stage. |
| Godot Stage B1 | Waiting for owner inputs | Both EN/FA WAVs, verbatim transcript files and matching subtitle files are absent on inspection. A mouth-motion decision is also outstanding. |
| Final character and narrated pilot | Not complete | Current torso/arms/hands are mathematical placeholders, not extracted or approved body art. |

Live media state:

```text
GODOT_FRONT_VIEW_CHARACTER_POC_01
STAGE_B0_ACCEPTED_STAGE_B1_OWNER_INPUT_REQUIRED
```

V7 and facial-package manifest/index hashes match their separate human approval
records on this inspection. Their frozen internal manifests still say
`CANDIDATE`/`human_approved: false`: approval was recorded externally without
mutating the approved bytes. Do not “fix” those old fields in place.

## Remaining workflows and dependencies

1. **Reusable character structure (proposed visual continuation).** The current
   demo has a working rig inside `scenes/main.tscn`. A useful Gemini task is to
   prepare/extract a reusable character scene in a separate candidate, preserving
   the accepted appearance and keeping the demonstration HUD/timeline separate.
   This is the bounded task proposed by the accompanying prompts; it has not
   been implemented or promoted by this status report. It needs no voice files.
2. **Real body/arm/hand assets.** Inspect the master to distinguish visible source
   pixels from occluded/missing surfaces; prepare a component/cut/pivot plan.
   New or reconstructed body art needs its own review. Keep placeholders
   explicitly labelled until approved replacements exist. A working head rig
   must not be described as a complete chopped full-body character.
3. **Voice prerequisites.** Supply one selected recording per language, exact
   transcript and matching WebVTT cues. Current contract is PCM16 WAV, mono or
   stereo, 22.05–96 kHz, nonempty, within the 18-second timeline; 48 kHz mono is
   preferred. Existing eSpeak voices were rejected. No cloud/synthetic voice is
   authorized by this handoff.
4. **Mouth choice.** Keep neutral or explicitly authorize the existing small-open
   test sprite as a simple two-state audio-driven proxy. That proxy is not
   phoneme-accurate lip-sync; a proper viseme library is separate art work.
5. **Stage B1 integration.** Once inputs exist, load the selected track, preserve
   exact subtitle text, align playback/captions and implement only the chosen
   mouth behaviour. Both languages use the same character-action timeline.
6. **Paired exports and review.** Render actual EN/FA clips, verify streams,
   duration, timing, Persian shaping/RTL and appearance, then obtain human
   listening/visual approval. Independent review remains a distinct recorded
   check when requested; Gemini must not impersonate a completed Claude review.
7. **Production packaging.** After final art/rig/performance decisions, prepare
   one clearly identified final package with its required assets, code and
   concise evidence. Ensure its documented build/validation does not silently
   depend on excluded local intermediate versions. Only final versions are to
   be selected for Git; no commit/push is authorized by these prompts.
8. **Narrative/editorial track, separate from rig work.** Complete human review
   of the current Chapters 01–04 signoff packet, make any requested corrections,
   then perform separately authorized revision-specific metadata/hash
   reconciliation and rerun the full gate. Continue remaining Persian human
   review, terminology consolidation, bilingual/visual/publication gates as
   documented in the editorial workflow. Character work must not edit the book
   to bypass this queue.
9. **Larger media programme.** The recorded direction is a reusable Chapter 01
   pilot, then Chapters 02–04, then later chapters. That roadmap is a plan; the
   current scene is not a completed chapter video. No readiness claim is made
   here for all existing chapter blueprints or narration drafts.

The immediate audio blocker does not prevent scene reuse/refactoring or the
body-component planning task. It does prevent claiming narrated exports are
ready.

### Chapter 01 scene handoff clarification

The subsequent Chapter 01 handoff inspection found an existing eleven-scene
screenplay under `.zcode/ch01-only-finalization/animation-script/`, totaling
149 seconds in its current YAML. Its supervisory review still records
`CH01_ANIMATION_SCREENPLAY_REVISION_REQUIRED`; the bounded correction brief
proposes a 173-second budget and fixes causality, Persian wording, diagram
hierarchy and status reporting. These draft narration/subtitle resources are
distinct from the missing owner-recorded POC voice inputs.

The [GLM chapter-scene prompt](glm-chapter-01-godot-completion.md) carries those
corrections into a new candidate-local plan and requests the complete visual
sequence. It does not mark the screenplay approved or mean that chapter Godot
implementation has already happened. The existing POC's 18-second audio limit
must not be reused unchanged as the full chapter's duration contract.

## Where to trust current status

Use the live `workflow/phase-status.json`, scoped approvals and later evidence
over historical prompts, old READMEs and completed-phase snapshots. Older texts
still say the project does not exist, V7 awaits approval, GLM must implement, or
Stage B0 is pending. Those describe earlier moments. This user now requests a
Gemini handoff; that changes the requested executor, not the approved art scope.

## `.godot/` clarification

Keep `.godot/` locally and ignored during normal work. It holds generated import
data and editor state. Deletion is optional for stale-import troubleshooting or
disk cleanup, with Godot closed; it is not needed to prepare a Git commit.
Godot rebuilds imported resources afterward, and some editor-local state may
reset. The cache here is about 3.15 MiB, so there is little space pressure.
Source assets, `project.godot`, scenes, scripts, `.import` and `.uid` metadata are
distinct. See [Godot's import documentation](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html).

## Verification scope

This inspection confirmed the current files and approval bindings, absence of
all six expected EN/FA narration inputs, and installed Godot
`4.7.2.stable.official.ed1daf0bf` / ffprobe `6.1.1-3ubuntu5`. The static Godot
integrity checker was rerun. No new GUI/art/audio approval was performed.

The previous triage's `make check` result was 789 passed / eight stale-hash
failures, after passing lint/format checks. The full gate was not rerun for this
documentation handoff. A historical `repository_gate_passed: true` in a media
record does not override that later failing working-tree baseline.
