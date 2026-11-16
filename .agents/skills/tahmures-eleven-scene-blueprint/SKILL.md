---
name: tahmures-eleven-scene-blueprint
description: Map an existing or proposed eleven-scene animated episode into playable scene cards with objectives, turns, transitions, sources and production constraints.
---

# Scene cards and episode architecture

## Non-negotiable source and approval rules
- Work inside the actual Tahmures repo. Read root/nested `AGENTS.md`, `meta-prompt.md`, `book/project-charter.md`, `book/narrative-continuity.md`, and the canonical English chapter relevant to the task. Follow project-local editorial skill and approvals. The English narrative and continuity are canonical for story facts; media adaptations have their own scoped approval.
- For Chapter 01, inspect `editorial/media-handoff/chapter-01-animation-status.json` and the selected revision under `Characters/animations/chapter-01-candidate-01/production/english-final-03/`, including its README, timeline and reviews, and check for documented superseding decisions.
- Do not assume an 11-scene count or change approved duration: verify the real timeline and flag any mismatch. Div-e Sefid serves as messenger in the approved Chapter 01 animation, while Chapar is a distinct courier. Do not merge them.
- Separate every claim or suggestion with labels **CANON**, **APPROVED MEDIA ADAPTATION**, **PROPOSAL**, **CONFLICT**, or **UNKNOWN**. Cite repo paths (and line/section/scene identifiers when available) for source-derived claims. A proposed line or scene is never an approved line or scene.
- Do not modify canonical English/Persian manuscripts, continuity, approved media, approvals, or status records without the owner's explicit permission. Do not create new voice, imagery, provider calls, uploads, commits, pushes, or deployments. Candidate writing stays in a new working folder.
- The episode must remain original teaching fiction distinct from *Shahnameh*: no modern engineering jargon in the ancient-world scene, a concrete chapter-specific failure with consequences, divs as capable and uncertain rather than just evil, a correctly identified failure owner, an explicit engineering bridge, and a hook to the next chapter.

## Rules
- **11 scenes is a user target, not a verified canonical fact.** Read actual `timeline.json`, scene manifests, screenplay, audio and status. If count differs, preserve it and produce a comparison, not a silent conversion. Distinguish scene (continuous dramatic unit) from short animation shot.
- A scene starts with an unstable situation and ends with a meaningful change. If a scene merely conveys facts, try visual storytelling or fold it into another scene as a **proposal**.

## Procedure
1. Inventory scene IDs and durations; attach exact source links. Lock approved timing and content.
2. For each scene fill: entrance state, focal character, active want, immediate obstacle, tactics, revelation/pressure, decisive action, **turn** (before -> after), visible stakes, emotional shift, ethical question, setup/payoff, physical action, important prop, dialogue burden, exit image/sound, link into next scene, production/approval status.
3. Summarize a scene in one causal line: `Because X happens, Y tries Z, but W resists; the outcome changes A into B.` Flag scenes that cannot pass.
4. Draw a tension contour; allow breath/quiet after strong turns. Do not prescribe a twist every scene. Ensure at least one scene makes the audience reinterpret an earlier assumption without contradicting source.
5. Specify chapter failure consequence and actual failure owner; ensure the engineering bridge and next hook are placed without breaking the ancient-world register.
6. For each proposed scene change provide smallest patch, source impact, updated durations only as **UNAPPROVED**, and all owner decisions.

## Output
`05_SCENE_BLUEPRINT.md` + copy the `11_SCENE_MATRIX.csv` template to the episode working directory and fill with actual scene rows. When duration or count is unknown use `UNKNOWN`, not invented numbers.

## Acceptance
Every scene produces a new state, each transition has a causal or thematic connection, and all time/approval constraints are visible.
