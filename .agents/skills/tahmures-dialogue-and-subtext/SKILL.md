---
name: tahmures-dialogue-and-subtext
description: Rewrite episodic dialogue for playable intention, subtext, character-specific voice, rhetorical conflict, listening, silence and voice timing.
---

# Dialogue and subtext laboratory

## Non-negotiable source and approval rules
- Work inside the actual Tahmures repo. Read root/nested `AGENTS.md`, `meta-prompt.md`, `book/project-charter.md`, `book/narrative-continuity.md`, and the canonical English chapter relevant to the task. Follow project-local editorial skill and approvals. The English narrative and continuity are canonical for story facts; media adaptations have their own scoped approval.
- For Chapter 01, inspect `editorial/media-handoff/chapter-01-animation-status.json` and the selected revision under `Characters/animations/chapter-01-candidate-01/production/english-final-03/`, including its README, timeline and reviews, and check for documented superseding decisions.
- Do not assume an 11-scene count or change approved duration: verify the real timeline and flag any mismatch. Div-e Sefid serves as messenger in the approved Chapter 01 animation, while Chapar is a distinct courier. Do not merge them.
- Separate every claim or suggestion with labels **CANON**, **APPROVED MEDIA ADAPTATION**, **PROPOSAL**, **CONFLICT**, or **UNKNOWN**. Cite repo paths (and line/section/scene identifiers when available) for source-derived claims. A proposed line or scene is never an approved line or scene.
- Do not modify canonical English/Persian manuscripts, continuity, approved media, approvals, or status records without the owner's explicit permission. Do not create new voice, imagery, provider calls, uploads, commits, pushes, or deployments. Candidate writing stays in a new working folder.
- The episode must remain original teaching fiction distinct from *Shahnameh*: no modern engineering jargon in the ancient-world scene, a concrete chapter-specific failure with consequences, divs as capable and uncertain rather than just evil, a correctly identified failure owner, an explicit engineering bridge, and a hook to the next chapter.

## Procedure
1. Extract existing dialogue exactly with speaker, scene ID, source/approval and timestamp when present. Do not silently substitute a new script for already approved recorded performance.
2. For each line annotate: literal meaning, **speaker wants listener to do**, tactic, truth withheld, power relation, change in listener, and whether the image could carry the information more efficiently. If line cannot change behavior or expose pressure, propose cutting it.
3. Give each character a differentiated acoustic profile: register, average clause length, rhythm, directness, metaphors grounded in role/world, reaction style, and silence. Prefer **one potent figurative line** followed by plain counterpressure over constant purple prose.
4. Make interaction reciprocal: `A attacks -> B parries -> A changes tactic -> B reveals a cost`, not alternating exposition speeches. Ensure opposing beliefs have credible logic.
5. Write two **PROPOSAL** versions for pivotal exchanges: `natural / economical` and `heightened / ceremonial`. Do not produce a recognizable imitation of Beyzai's wording. Never import actual passages from playwrights.
6. Make the line actor-playable: clear breath units, no impossible simultaneous speaking/action, pauses motivated by thought, no unexplained anachronism. Keep voice and lip-sync constraints explicit.
7. If dialogue is Persian, assess natural syntax, ezafe, modifiers, mixed-language terms, idiomatic rhythm, and line-level meaning **without changing** the official translation unless specifically authorized. For English original, guard against modern engineering jargon in ancient scenes.
8. Audit subtext at pivotal lines. A character saying exactly what they feel is sometimes powerful; do not impose cryptic dialogue on every scene.
9. Compare new proposed dialogue duration to approved clips/audio; preserve existing voice takes, flag re-recording as owner decision, never generate new audio.

## Output
`07_DIALOGUE_SCORE.md`: line-by-line annotated exchange, voice fingerprints, strongest 2–3 revised exchanges, cut/keep rationale, actor directions (sparingly), timing and approval status. Preserve original line alongside each candidate rewrite.
