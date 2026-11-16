---
name: tahmures-flow-handoff-sync
description: Synchronize Tahmures story-room proposals into a complete versioned candidate Google Flow handoff, with per-shot prompts, agent instructions, media maps, review gates and a safe approval-based promotion plan.
---

# Flow handoff sync — candidate packaging and impact propagation

Use when a story revision affects episode intent, a character choice, scene ordering, a dramatic punch, dialogue, props, visuals, audio performance or timing. **This is an execution skill: create and validate files, do not just advise updating contexts.**

## Read before writing
1. Root/nested `AGENTS.md`, `meta-prompt.md`, `book/project-charter.md`, `book/narrative-continuity.md`, canonical chapter, active media revision and its timeline/approval state. Inspect `editorial/media-handoff/` and actual existing Google Flow handoff, including approved visual identity, audio provenance, shot prompt/instruction references and the previously generated local Flow prompt where present.
2. Read the Story Room source ledger and completed outputs: purpose, character pressure, scene map, punch map, dialogue, visual-sound recommendations, continuity and owner decisions. Only sources with explicit approval have production authority; **PROPOSAL is not approval**.
3. For Chapter 01, preserve Div-e Sefid as approved media messenger and Chapar as separate courier. Do not convert an adaptation into manuscript canon or assert English approvals cover Persian media.

## Produce the COMPLETE synchronized candidate handoff now
Working root: `editorial/media-handoff/story-room/chapter-01-candidate-01/flow-handoff-candidate/` or a clearly documented safe candidate equivalent. Create actual files, with a README and: 
- `context/`: episode goal, character objectives and decisions, story/visual continuity, locations and props, source authority, approval constraints.
- `agent-instructions/`: short, actionable updated instructions for story, art style, character identities, subtext and actor performance, shot/tempo/negative constraints; compare with the EXISTING `Tahmures — Veo visual consistency agent instructions`, avoid contradictions, and identify which items the user should manually add/update in Flow only after approval.
- `episode-01/`: scene and shot index keyed to verified timeline, per-shot prompt drafts, action and emotion directions, character/setting/prop refs, start/end frame suggestions, camera and staging, timing, dialogue/audio map and silent beats, continuity carryover, and assembly/edit notes.
- `assets/` and `manifests/`: reference map with exact source files and authorized candidate copies where needed, hashes if possible, blocked/nonapproved items separated; never invent art or represent unapproved files as upload-ready.
- `guides/`: operator procedure using Flow Characters, Uploads, Agent instructions, Frames/Ingredients, suitable models, scenes, and downloaded clips. No assumed automated integration or provider calls.
- `CHANGE_IMPACT_MATRIX.csv`, `HANDOFF_DIFF_AND_PROMOTION.md`, `VALIDATION_REPORT.md`: full change propagation, line/file/scene references, approvals and precise old/new differences.

Do not stop at `12_FLOW_WRITING_HANDOFF.md`; that is an input summary. Ensure that **every changed story beat propagates into all its dependent prompt, agent context, dialogue, audio, shot, image-reference, scene and assembly entries**. If dialogue is still a proposal, retain approved recording separately and mark new audio as approval needed. Do not alter the original timeline or voice.

## Quality gates
- Bidirectional mapping: every candidate shot points to one real/candidate scene and to source anchors; every scene has shot coverage or a stated blocker; every proposed story change has impacted files in the matrix.
- Detect contradictory Flow agent text, stale dialogue, character identity swaps, missing reference assets, invalid media paths, unsourced timestamps, unapproved voice/re-recording, and contradictions with canonical English narrative or approved adaptation.
- When the plan includes alternate script choices, select one coherent *recommended proposal* for the candidate package while retaining the choices for owner review.
- Use statuses `CANON`, `APPROVED MEDIA ADAPTATION`, `PROPOSAL`, `UNKNOWN`, `CONFLICT` and explicit human approval fields. Include exactly what must change after approval.

## Never silently promote
The current run is **candidate-only**: no changes to canonical manuscripts, existing production renders/recordings, `timeline.json`, approvals or the existing official Google Flow handoff. Never run paid generation, send uploads, commit or push. Following explicit scope-specific owner approval, a separate authorized action may generate a new versioned official handoff from the accepted subset; preserve history and revalidate. Do not claim artistic, timing or lip-sync approval from mere technical validation.

## Deliver
Report the created candidate Flow paths, count of mapped scene/shot prompts, updated instruction proposals, missing assets, highest-impact approval decisions, validation results and a copy-paste-ready promotion instruction that is strictly conditional on explicit approval.
