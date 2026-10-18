# GLM prompt — complete the Chapter 01 Godot scene

> Superseded by the owner's character-first recovery instruction. Do not execute
> this older scene-first task or its permission to substitute named-character
> stand-ins. Use [the revised local Gemini handoff](gemini-local-continuation.md)
> and [the GLM output inspection](2026-10-18-glm-character-review.md). The content
> below is retained as historical task context, not current implementation scope.

Copy the prompt below to GLM with local repository access. This file is a task
handoff; no GLM execution or new production approval is recorded by its creation.

---

MODE = IMPLEMENT_AND_VERIFY

PHASE = CH01_GODOT_VISUAL_SEQUENCE_COMPLETION_01

You are GLM, the implementation agent. Continue the existing Tahmures work and
finish a runnable **Chapter 01 Godot visual sequence**, with all eleven planned
scenes, bilingual text/caption tracks, reusable character staging, controls and
real render evidence. Work through implementation and verification; a plan,
screenplay, isolated character demo or list of suggestions is not the deliverable.

The owner's request authorizes this Chapter 01 implementation candidate. It does
not approve new permanent character art, voice performances, the pending book
revision, publication, provider calls or Git writes. Complete all work supported
by available assets. Missing voice/art approval must be exposed accurately
without preventing a functioning, clearly identified visual animatic.

## 1. Context and source order

Repository: `/home/mehdi/Project/leela/tahmures`.

Read `AGENTS.md` and its RTK reference. Prefix shell commands with `rtk`.
Read relevant live skills under `.agents/skills/`: `mehdi-context`,
`mehdi-media`, `mehdi-narrative`, `tahmures-narrative`, `mehdi-bilingual` and
`mehdi-review`. Respect the charter and editorial contract. This is a bilingual
prompt-engineering book with original myth-inspired teaching fiction, not a
historical reconstruction or an interactive mythology game.

Read these sources before coding:

- `book/part-1/01-what-is-a-prompt.md` and its Persian counterpart
  `book/fa/part-1/01-what-is-a-prompt.md`;
- relevant Chapter 01/cast/prop entries in `book/narrative-continuity.md`;
- `.agents/tahmures_character_behaviors_ch01-04.md`, keeping its draft status
  distinct from the owner's already recorded mappings;
- `.agents/tahmures-media-editor-llm-context.md` and the media roadmap;
- `.zcode/ch01-only-finalization/animation-script/`: both screenplays,
  `dialogue-ledger.md`, `scene-breakdown.yaml`, `screenplay-review.md`;
- `.zcode/ch01-only-finalization/GPT-CH01-animation-screenplay-review.md` and
  `prompts/05-glm-ch01-animation-screenplay-revision-1.md`;
- `.zcode/media-01-04/ch01-video-blueprint.md` and relevant media-bible entries;
- `.zcode/media-production-foundation/scene-schema.md`, its asset-management
  rules, `registry/asset-registry.yaml` and relevant character/location cards;
- `Characters/tahmures/workflow/phase-status.json`, `asset-versions.json`, both
  approval JSONs in `workflow/approvals/`, and
  `editorial/media-handoff/2026-10-18-process-state.md`;
- the actual existing project at
  `Characters/tahmures/prototypes/godot-front-view-character-poc-01/`, especially
  `project.godot`, `scenes/main.tscn`, `scripts/main.gd`,
  `scripts/audio_subtitle_pipeline.gd`, the manifest, integrity checker and
  asset-directory READMEs.

The live chapter and current continuity control names, causal meaning and the
engineering lesson. The older blueprint guides media sequencing; some of its
names/art descriptions predate the adaptation. The screenplay review and bounded
correction brief identify known defects. Historical briefs that say the project
does not exist or B0 is pending do not override actual files and current state.
Do not follow an old scope prohibition as a reason to refuse this new
implementation task; retain its relevant source/approval constraints.

## 2. Preserve the baseline; create one chapter candidate

Inspect Git status and record source hashes before changes. Work under:

```text
Characters/tahmures/prototypes/godot-chapter-01-01/
```

If it exists, inspect it and continue only compatible work; do not overwrite an
unrelated candidate. Keep all implementation, corrected local planning files,
tests, reports and render evidence within this candidate. Preserve the original
Godot POC, V2–V7 packages, facial-state package, approval records, historical
screenplays, blueprints, registry and manuscript unchanged.

Reuse the existing working head rig and state assets. Do not restart extraction
or redesign Tahmures. Verify the approval-bound package hashes against the real
JSON records. New candidate files get their own hashes and status; old approvals
do not automatically approve a refactored scene or new artwork.

Prefer one reusable `Tahmures` scene, reusable stage/prop/overlay components,
language resources and one chapter director/timeline. Keep chapter runtime UI
separate from optional debug HUD. Do not scatter eleven standalone projects.
Copy the exact required assets into the candidate with provenance so normal
playback does not need local intermediate-version paths. Source preservation
checks may reference the original packages explicitly.

## 3. Entry corrections — implement locally, then continue

At this handoff the scene YAML contains **11 scenes totaling 149 seconds** and
the supervisory review still says `CH01_ANIMATION_SCREENPLAY_REVISION_REQUIRED`.
Do not call that screenplay production-approved. Build a corrected, traceable
candidate-local scene/cue plan, preserving stable `CH01-S01`–`CH01-S11`, cue and
overlay IDs. Apply the existing review findings before adapting the code:

1. **S06 cause:** visibly show Simurgh arriving and delivering the wrapped
   packet to Arash, followed by Arash sending riders. Do not replace arrival/
   delivery with “Arash reads, therefore dispatches.” Preserve the eleven
   charcoal-burner fires and three villages' fear. Delivery is not authentication.
2. **S10 carrier:** stage Simurgh carrying the corrective second message, per
   the established Messenger role and blueprint. Record this as a staging
   inference; the prose does not name that carrier. Do not invent dialogue,
   decide Simurgh's final bird/human form, or claim a seal grants authority.
3. **Persian:** repair the known malformed production prose locally, including
   `فیروزه‌های بی‌نام`, the doubled reed-sharpening tense and unnatural
   authority/security wording. Preserve source dialogue and the distinctions
   between `چاپاری` at introduction and `چاپار` later; use `طهمورث`.
4. **Style:** the present 2D treatment is a provisional animatic direction,
   not a new series-wide style lock or a replacement for approved art decisions.
5. **S09:** give all eight prompt components equal conceptual weight. No
   primary/subordinate split, no authority-implying seal icons in review questions.
6. **Timing:** use the existing revision brief's 173-second budget as the
   starting point: 12, 16, 10, 15, 15, 17, 31, 15, 20, 15, 7 seconds.
   Use one visual timeline for both languages. Check caption reading time and
   actual rendering; without recorded speech, timing remains provisional for
   narration. Do not cut source lines to force the budget or claim voice timing
   has been tested. Report any justified duration deviation.
7. **Record truth:** distinguish source facts, staging inferences, working
   estimates and human art choices. The media order intentionally places the
   engineering diagram before the second message and ledger ending; it is not
   literal prose order. Div-e Sefid's next-chapter hook is outside this sequence.

Record closure evidence in `planning/review-findings.md`. Do not stop after this
planning correction; proceed to the runnable chapter.

## 4. Scene coverage — no missing beats

| ID | Required visible content |
|---|---|
| CH01-S01 | Establish Hall of Scripts and arriving materials; source-consistent atmosphere. |
| CH01-S02 | Chapar brings the found tablet; show dissolved seal and exact imperative as programmatic text. Chapar is distinct from Simurgh. |
| CH01-S03 | Tahmures asks what the tablet is; three distinct recipients examine it. |
| CH01-S04 | Akvan Div catalogues a record; Simurgh wraps an urgent message; Black Div reads and leaves to act. |
| CH01-S05 | Wet Black Div returns with eleven fires; preserve the source dialogue and Tahmures's realization. |
| CH01-S06 | Simurgh's arrival/delivery, Arash's dispatch, villages' alarm, charcoal burners: real consequences without making a div malicious. |
| CH01-S07 | Longer-wording attempt, Akvan's warning, Tahmures stops the reed, four labels, first three unknown, separate requested-result card. |
| CH01-S08 | Same “Close the western gate” sentence as current task, court evidence and handwriting practice; roles depend on context. |
| CH01-S09 | Engineering bridge: the complete request envelope and all eight components, with the application/security boundary clear. |
| CH01-S10 | Short corrective message, recipient/correction/acknowledgement, Simurgh as inferred carrier, riders returning. |
| CH01-S11 | Shahrasp's ledger line and the episode takeaway/end card. |

Keep Garshasp offstage as a handwriting reference. Do not add named characters,
dialogue or mythic powers. Tahmures owns the unclear request; neither the
competent divs nor a nonexistent malicious actor owns that interface failure.
Modern diagrams belong in the bridge/overlay space, not ancient dialogue.

This scope is the existing eleven-scene tale plus engineering bridge. It does
not require cramming the entire chapter's labs, exercises and citations into the
episode. If fixture results are optionally shown, cite the committed synthetic
experiment and label `2/3` versus `3/3` as fixture results, not general model proof.

## 5. Available artwork and actual motion

Visually inspect source images and actual renders before claiming alignment.
The head is approved only within its front-view prototype scope. Preserve its
sprite bytes, common canvas, pivots, layer order, filtering and approved blink/
thinking/neutral/open-test state behaviour. Do not paint new faces, fake
perspective by deforming the head, or claim extra expressions exist.

There is no approved permanent torso/arm/hand art. Reuse the clearly identified
temporary rig where useful. Represent other missing cast/locations/props with
deterministic, distinct temporary cutouts, silhouettes or scene graphics based
on the existing roles/cards, recorded in `asset-map.json`. Avoid unapproved
anatomy or mythic claims. Keep Simurgh form-neutral until the owner chooses.
Existing unapproved references remain candidates, not automatically selected art.

Build readable actions: handoff, wrapping/cataloguing, departure, stop, labels
revealing, packet arrival, dispatch and return. Use camera framing and prop/
silhouette movement where unsupported body artwork prevents literal acting.
A row of static text slides with the idle head pasted over every shot is not
completion. Do not use costly generation or invent permanent art to hide gaps.

Provide an optional debug view with scene ID/time/cue and placeholder ownership.
Keep production subtitles readable and the approved head unobstructed. In the
animatic, show a concise preview/temporary-art indication without flooding the
story with implementation prose; the complete per-asset provenance lives in the
report. No debug labels may describe temporary art as final.

## 6. Bilingual text, audio and duration contracts

Keep one semantic timeline and separate EN/FA string/caption resources. Match
source dialogue to the live chapter in each language. Reconcile old narration,
subtitle and overlay files with the corrected scene/cue plan; their presence
does not prove current text or timing. Record source strings and changes in a
candidate-local cue ledger. Do not edit the original files.

Use Godot text nodes with a verified shaping-aware font already available and
proper RTL/bidi behaviour. Render the formula and labels programmatically.
Preserve protected identifiers and punctuation; do not reverse Persian strings
manually or convert exact text into generative-image lettering. Make the four
S07 labels and the S09 formula traceable to their current sources; do not
silently reuse the old S05 overlay `OV-01-04` as S07's four-label plate.

The existing 18-second POC WAV validator is **not** the full chapter contract.
In this candidate, derive allowed audio/cue duration from its declared chapter
timeline. Preserve the original POC validator unchanged. Test chapter boundaries,
cue ordering/overlap, missing tracks, malformed files and language switching.

No owner-confirmed chapter recordings are established by this handoff. Complete
the scene with a **silent animatic mode** and explicitly provisional caption
timing; do not call silence narration or substitute test fixtures for speech.
Keep mouth neutral for spoken cues unless the owner separately authorizes the
existing small-open state as a two-state audio-driven proxy. That is not full
lip-sync. Preserve a non-speaking open-test only where its debug use is clear.

Implement an optional real-audio input route with validated recording and
verbatim cue/transcript inputs. Enable it only when actual supplied inputs and
the needed owner decisions exist. Do not generate voice, use rejected eSpeak,
invoke cloud TTS, purchase services, install new dependencies, or require speech
to complete silent visual playback. List exact input paths/formats needed for
the later narrated export. Missing audio must be a visible pending status,
not a crash or an endless blocker to all visual work.

## 7. Runtime, rendering and verification

Implement deterministic chapter playback, scene selection/seek, pause/resume,
restart and explicit `en`/`fa` selection. Restart/seek must reset actors, props,
captions and audio state so there is no residue from a previous scene. Fail
clearly on unsupported language/resource configuration. Keep controls concise.

Use installed Godot (last observed `4.7.2.stable.official.ed1daf0bf`) and local
FFmpeg/ffprobe. Verify actual versions. No dependency changes or replacement
renderer project is required.

Before editing, run the baseline integrity check:

```bash
rtk proxy python3 Characters/tahmures/prototypes/godot-front-view-character-poc-01/scripts/check_integrity.py
```

For the chapter candidate:

- Run headless import and main-scene smoke checks; inspect actual exit codes.
- Test all eleven scenes, reset/seek boundaries, bilingual cues, missing audio,
  malformed cue/audio inputs and deterministic timing at representative frames.
- Render actual EN and FA silent animatics, preferably 1280×720 at 30 fps, to
  candidate-local outputs. Use Godot Movie Maker or a documented deterministic
  Godot-frame-plus-FFmpeg route. Do not run an entire long movie headlessly and
  call it visually verified because the process exited zero.
- Inspect keyframes from every scene and both language tracks, including long
  Persian lines, four labels and the eight-component diagram. Check real glyph
  shaping, text clipping, safe areas, actor alignment and action legibility.
- Probe actual files for duration, dimensions/frame rate and stream metadata.
  Call a silent engine audio stream silence. Do not claim intelligible narration.
- Compare source hashes afterward; the original head/art/POC inputs must remain
  unchanged. Keep meaningful checks in candidate-local test/validation scripts.
- Run `rtk proxy git diff --check` and the repository-required
  `rtk proxy make check PYTHON=.venv/bin/python` before handoff. Last known full
  gate: 789 tests passed, eight failed due to stale Chapters 01–04 Persian
  source hashes; later stages were not reached. Report actual current results.
  Do not refresh book hashes or weaken validators to hide unrelated failures.

If a real renderer/display/tool constraint prevents a step, first complete the
remaining supported work, then report the exact command, error and smallest
required external action. Never fabricate screenshots, renders or test passes.
Do not stop after reporting a generic “assets missing” or a tooling assumption.

## 8. Required outputs and honest completion

The candidate must contain:

- `project.godot`, reusable character/prop/overlay scenes and a runnable chapter
  director covering all eleven scenes;
- required assets with provenance and placeholder/final distinction;
- corrected planning/cue records, EN/FA language resources and caption files;
- audio-input contract and functioning silent preview mode;
- actual rendered previews and representative keyframes when the toolchain runs;
- focused tests, `validation.json` with actual results, and SHA-256 input/output
  records; no reused approval hash for new bytes;
- `README.md` with exact launch, scene-select, language and export commands;
- `implementation-report.md` with completed work, review-finding closure,
  genuine test/render evidence, changed paths, pre-existing failures and remaining
  owner art/voice decisions.

Keep all intermediate work local. Do not stage, commit, push, publish, clean
history or delete `.godot/`. Only final versions will later be selected for Git.
Do not change the canonical media phase-status record to claim acceptance; keep
the chapter candidate's status local and prepare evidence for review. Do not
claim an independent Claude/GPT check happened or grant human approval.

Finish implementation and your self-check rather than returning a plan. Use
one accurate final status:

```text
CH01_GODOT_VISUAL_SEQUENCE_READY_FOR_REVIEW
```

Use that only when the complete eleven-scene candidate runs and its reported
checks/render evidence support the claim. It means a visual animatic candidate,
not final character art, human-approved narration, or publication acceptance.
List any narration/permanent-art gates separately.

If concrete technical work remains incomplete, use:

```text
CH01_GODOT_VISUAL_SEQUENCE_INCOMPLETE
```

State exactly what works, what failed, and the next executable repair. Do not
describe a partial character demo or silent placeholder sequence as the final
narrated Chapter 01 release.
