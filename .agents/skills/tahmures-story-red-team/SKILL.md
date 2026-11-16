---
name: tahmures-story-red-team
description: Perform adversarial dramaturgical review of scene causality, theme, dialogue, pacing, character agency, clarity, animation cost and continuity; produce ranked revisions.
---

# Adversarial story review and table-read room

## Non-negotiable source and approval rules
- Work inside the actual Tahmures repo. Read root/nested `AGENTS.md`, `meta-prompt.md`, `book/project-charter.md`, `book/narrative-continuity.md`, and the canonical English chapter relevant to the task. Follow project-local editorial skill and approvals. The English narrative and continuity are canonical for story facts; media adaptations have their own scoped approval.
- For Chapter 01, inspect `editorial/media-handoff/chapter-01-animation-status.json` and the selected revision under `Characters/animations/chapter-01-candidate-01/production/english-final-03/`, including its README, timeline and reviews, and check for documented superseding decisions.
- Do not assume an 11-scene count or change approved duration: verify the real timeline and flag any mismatch. Div-e Sefid serves as messenger in the approved Chapter 01 animation, while Chapar is a distinct courier. Do not merge them.
- Separate every claim or suggestion with labels **CANON**, **APPROVED MEDIA ADAPTATION**, **PROPOSAL**, **CONFLICT**, or **UNKNOWN**. Cite repo paths (and line/section/scene identifiers when available) for source-derived claims. A proposed line or scene is never an approved line or scene.
- Do not modify canonical English/Persian manuscripts, continuity, approved media, approvals, or status records without the owner's explicit permission. Do not create new voice, imagery, provider calls, uploads, commits, pushes, or deployments. Candidate writing stays in a new working folder.
- The episode must remain original teaching fiction distinct from *Shahnameh*: no modern engineering jargon in the ancient-world scene, a concrete chapter-specific failure with consequences, divs as capable and uncertain rather than just evil, a correctly identified failure owner, an explicit engineering bridge, and a hook to the next chapter.

## Procedure
1. Independently audit draft against purpose, character-pressure, causal engine, scene cards, punch timeline, dialogue score, visual pass, and canonical sources. Do **not** mark a proposal approved merely because another skill suggested it.
2. Run seven stress tests: (a) remove protagonist; (b) remove exposition; (c) reverse the villain's point of view; (d) test a silent viewing; (e) track what audience knows at each beat; (f) verify technical failure owner; (g) simulate 2D production/voice timing.
3. Evaluate 0–4 each for `dramatic question`, `cause/effect`, `character agency`, `opposing values`, `earned turns`, `dialogue differentiation`, `subtext`, `visual/sound meaning`, `pacing`, `continuity and instructional truth`. Define evidence for each score; scores are subjective editorial instruments, never proof.
4. Flag `BLOCKER` (canon/approval breach), `MAJOR` (story logic or inability to follow), `MODERATE` (flat scene, weak turn), and `MINOR` (phrasing). Prioritize fixes by audience impact / scope / evidence / effort.
5. Provide at most five ranked revision cards, with before/after intent, exact affected scenes, source constraints, potential runtime/recording changes, owner decision, and a way to test improvement. Include what works already; do not optimize into uniform formulaic plot.
6. In a table-read scenario, each voice must sound like a different person; judge if listeners can tell who speaks without name labels. If not, identify concrete line-level fixes; do not rewrite approved source silently.
7. Run a second adversarial pass after proposed edits and record remaining uncertainty, rather than self-congratulating or claiming objective perfection.

## Output
`10_STORY_RED_TEAM.md`: evidence matrix, scores with reasons, issue register, top five revisions, acceptance conditions, and `GO FOR OWNER REVIEW` / `NOT READY` / `BLOCKED` — never unearned 'final approved'.
