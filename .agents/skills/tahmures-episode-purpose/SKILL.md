---
name: tahmures-episode-purpose
description: Extract or refine an episode dramatic purpose, theme, audience experience, teaching bridge, dramatic question and ending promise before writing scenes.
---

# Episode purpose and promise

Use this skill FIRST, before scenes or dialogue. It diagnoses **what the episode is about**, not just its plot synopsis. Avoid turning instructional outcomes into character speeches.

## Non-negotiable source and approval rules
- Work inside the actual Tahmures repo. Read root/nested `AGENTS.md`, `meta-prompt.md`, `book/project-charter.md`, `book/narrative-continuity.md`, and the canonical English chapter relevant to the task. Follow project-local editorial skill and approvals. The English narrative and continuity are canonical for story facts; media adaptations have their own scoped approval.
- For Chapter 01, inspect `editorial/media-handoff/chapter-01-animation-status.json` and the selected revision under `Characters/animations/chapter-01-candidate-01/production/english-final-03/`, including its README, timeline and reviews, and check for documented superseding decisions.
- Do not assume an 11-scene count or change approved duration: verify the real timeline and flag any mismatch. Div-e Sefid serves as messenger in the approved Chapter 01 animation, while Chapar is a distinct courier. Do not merge them.
- Separate every claim or suggestion with labels **CANON**, **APPROVED MEDIA ADAPTATION**, **PROPOSAL**, **CONFLICT**, or **UNKNOWN**. Cite repo paths (and line/section/scene identifiers when available) for source-derived claims. A proposed line or scene is never an approved line or scene.
- Do not modify canonical English/Persian manuscripts, continuity, approved media, approvals, or status records without the owner's explicit permission. Do not create new voice, imagery, provider calls, uploads, commits, pushes, or deployments. Candidate writing stays in a new working folder.
- The episode must remain original teaching fiction distinct from *Shahnameh*: no modern engineering jargon in the ancient-world scene, a concrete chapter-specific failure with consequences, divs as capable and uncertain rather than just evil, a correctly identified failure owner, an explicit engineering bridge, and a hook to the next chapter.

## Procedure
1. Identify the chapter's engineering concept, its specific failure, accountable failure owner, and actual consequence **from source**, not a guess. Distinguish author intention from what is currently dramatized.
2. State six different things: **external objective** (what someone physically seeks), **dramatic question** (what viewers need answered), **inner wound/need** (testable inference), **thematic tension** (two defensible values in collision), **audience feeling shift** (entry -> exit), and **learning transfer** (one-sentence bridge). Do not collapse these into a slogan.
3. Form an episode promise: `When [inciting disruption], [protagonist] must [difficult action], or [specific loss]; in choosing, they reveal [tension], and the audience comes to understand [failure/lesson]`. Treat this as a working hypothesis.
4. Name one **unanswered ethical question** and a **tangible motif/object** already supported by canon; propose new motifs only as candidates. Check why the viewer should care about a person rather than an abstract lesson.
5. Trace a **causal demonstration** of the engineering concept: dramatic error -> observable damage -> changed decision -> earned insight. The bridge explains the principle later; characters do not give an engineering lecture in ancient scenes.
6. Produce 2–3 competing episode promises; rank by emotional pressure, fidelity to source, clarity, animation feasibility, and original dramatic complexity. Choose one recommended **PROPOSAL**, not approved canon.

## Output
Write `01_EPISODE_PURPOSE.md` using `story-room/templates/01_EPISODE_PURPOSE.md`. Provide source ledger, six dimensions, competing loglines, core question, before/after audience experience, what must NOT change, and owner decisions.

## Failure checks
- If every character can be exchanged without changing the story, the episode lacks a human center.
- If the theme can be delivered as a lecture without plot loss, there is insufficient dramatization.
- If the story resolves with magic information and no costly decision, rewrite the objective/pressure.
- Never claim that a single theme is objectively correct; present evidence and a reasoned choice.
