# Tahmures media phase orchestration

Current phase: `GODOT_FRONT_VIEW_CHARACTER_POC_01` (Stage A project and HUD
layout accepted by GPT-Codex; Stage B0 audio/subtitle interface scaffolding
ready for GLM; actual Stage B1 integration gated on owner-provided EN/FA
recordings, exact transcripts, and mouth-motion choice).
`CHARACTER_LAYOUT01_MOUTHLESS_REPAIR` and `LAYOUT01_FACIAL_STATE_PROTOTYPE_01`
are complete. V7 and the reviewed facial-state prototype have separate,
hash-bound human approvals; the latter is approved for continued prototype use,
not promoted as permanent character art.

## Responsibilities and authorities

Owner instruction, 2026-10-09: **GLM is the low-cost primary implementation
agent; GPT-Codex designs bounded work and independently validates the results.**
GLM performs concrete coding, asset, render, and self-test work. GPT-Codex
reviews actual outputs and evidence, then gives GLM focused corrections when
needed. GPT does not take over routine implementation.

Claude is not part of routine implementation or validation. Use a fresh,
read-only near-final Claude review only when the owner asks. The human retains
subjective visual approval and character freezing. Machine checks, GPT
validation, optional Claude review, and human approval are distinct gates. This
role split does not authorize paid/provider calls, publication, commits or
pushes.

The approved manuscript, `book/narrative-continuity.md`, and accepted 01–04
media blueprints/bible retain story and technical authority. For this component
repair, the owner explicitly selected the imported master as the visual source.
Preserve its existing face, hair, gold diadem, palette and linework; do not use
this mechanical repair to resolve older style-card differences or change canon.

## Durable layout

- `phase-status.json`: single current-state and release-gate record.
- `asset-versions.json`: source/version disposition; no automatic approvals.
- `layout01-mouthless-repair/prompts/`: preserve historical issued handoffs;
  current prompts are near-final read-only review briefs or explicitly requested
  external execution tasks. Do not generate routine GLM correction prompts.
- `layout01-mouthless-repair/reports/{glm,codex,claude}/`: actual agent results.
- `layout01-mouthless-repair/history.jsonl`: dated, append-only task/gate events.
- `layout01-mouthless-repair/{source-checksums,package-inventory}.json`: input
  identity and source preservation evidence.
- `layout01-mouthless-repair/acceptance-criteria.json`: machine/visual/approval
  checks with evidence requirements.
- `tools/validate_submission.py`: read-only structural validator; it cannot
  grant artistic approval.
- `../versions/layout01-v2/`: immutable rejected baseline extracted from ZIP.
- `../versions/layout01-v3/` and `layout01-v4/`: preserved rejected candidates.
- `../versions/layout01-v5/`: face/motion independently passed; neck rejected.
- `../versions/layout01-v6/`: actual neck implementation attributed to Claude;
  preserved as received, with its original package/report hashes.
- `../versions/layout01-v7/`: frozen, human-approved front-view input, bound to
  `approvals/layout01-v7-human-approval.json`; exact reviewed files unchanged.
- `../prototypes/layout01-facial-states-01/`: Codex blink/thinking/state-switch
  prototype. Its reviewed pose art has scoped human approval for continued
  prototype use; it is not permanent production art.

These paths are outside `.zcode/` and eligible for repository storage. Local
durability is not a substitute for backup; commit/push remain owner actions.

## Phase transitions

1. `GLM_IMPLEMENTATION_IN_PROGRESS`: GLM implements the authorized bounded
   task, preserves protected inputs, renders actual evidence, and runs focused
   self-checks.
2. `GPT_VALIDATION_PENDING`: GPT-Codex binds hashes, inspects actual outputs,
   independently runs appropriate checks, and records acceptance or precise
   blockers. A GLM summary alone is not evidence.
3. Concrete blockers return to GLM as a bounded correction list; GPT validates
   the changed package. Escalate genuine owner art/policy choices rather than
   iterating indefinitely.
4. A fresh Claude read-only review is optional for near-final, high-subjectivity
   work and happens only when the owner requests it.
5. Human visual approval remains required for new permanent art and performance
   choices; bind it to the actual final candidate hashes.

The earlier bounded GLM correction limit for Layout 01 remains historical
evidence only. It does not limit new owner-authorized GLM phases.

## Return protocol

Follow [receiving independent review](layout01-mouthless-repair/receive-review-output.md).
Never infer a passed gate from file presence, an agent token, or a correct
pixel-exact source preview. Do not set manuscript review metadata during media
work. Preserve previously rejected versions without putting them in the
approved-asset registry.


The current phase is `GODOT_FRONT_VIEW_CHARACTER_POC_01`. Stage A and the
bounded HUD correction are accepted: GPT independently reran 29 integrity
checks, 8 rendered HUD checks, Godot language-hook smoke tests, and ffprobe on
the silent 18-second render, and visually inspected six keyframes. The active
GLM handoff is
`godot-front-view-character-poc-01/glm-stage-b0-audio-interface-01.md`, which
can implement input and subtitle plumbing without fabricated media. Actual
Stage B1 audio integration waits for paired human-recorded WAVs, exact
transcripts, and the mouth-motion choice. Both eSpeak voices remain rejected.
See `godot-front-view-character-poc-01/ROADMAP.md` for the next steps and
`GODOT_INSTALL.md` for project commands.
