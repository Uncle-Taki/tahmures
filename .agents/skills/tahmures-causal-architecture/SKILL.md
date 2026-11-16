---
name: tahmures-causal-architecture
description: Strengthen episode causality, inciting incident, escalation, reversals, costly choice, resolution, and aftermath while preserving canonical facts.
---

# Causal dramatic engine

## Non-negotiable source and approval rules
- Work inside the actual Tahmures repo. Read root/nested `AGENTS.md`, `meta-prompt.md`, `book/project-charter.md`, `book/narrative-continuity.md`, and the canonical English chapter relevant to the task. Follow project-local editorial skill and approvals. The English narrative and continuity are canonical for story facts; media adaptations have their own scoped approval.
- For Chapter 01, inspect `editorial/media-handoff/chapter-01-animation-status.json` and the selected revision under `Characters/animations/chapter-01-candidate-01/production/english-final-03/`, including its README, timeline and reviews, and check for documented superseding decisions.
- Do not assume an 11-scene count or change approved duration: verify the real timeline and flag any mismatch. Div-e Sefid serves as messenger in the approved Chapter 01 animation, while Chapar is a distinct courier. Do not merge them.
- Separate every claim or suggestion with labels **CANON**, **APPROVED MEDIA ADAPTATION**, **PROPOSAL**, **CONFLICT**, or **UNKNOWN**. Cite repo paths (and line/section/scene identifiers when available) for source-derived claims. A proposed line or scene is never an approved line or scene.
- Do not modify canonical English/Persian manuscripts, continuity, approved media, approvals, or status records without the owner's explicit permission. Do not create new voice, imagery, provider calls, uploads, commits, pushes, or deployments. Candidate writing stays in a new working folder.
- The episode must remain original teaching fiction distinct from *Shahnameh*: no modern engineering jargon in the ancient-world scene, a concrete chapter-specific failure with consequences, divs as capable and uncertain rather than just evil, a correctly identified failure owner, an explicit engineering bridge, and a hook to the next chapter.

## Procedure
1. Extract the currently documented sequence of events. Mark every link **because/therefore** or **meanwhile/and then**. A long run of `and then` indicates weak causality; do not replace history with fiction without approval.
2. Locate inciting disruption, first irreversible commitment, rising complications, midpoint recontextualization (optional), crisis of incompatible values, decisive action, immediate cost, and the changed state. These are useful diagnostics, not a mandatory Hollywood formula.
3. For each possible twist ask: whose action caused it, what evidence was planted, what existing belief does it overturn, and what physically changes? Surprise without preparation is not a payoff.
4. Separate **technical failure owner** from **dramatic moral blame**. A person may make a defensible decision with a broken process. Do not falsely assign systemic errors to a convenient villain.
5. Preserve a genuine counterargument for at least two sides. If the scene is a trial/testimony/recounting, map competing versions of events and specify what is verified and what remains uncertain; do not invent certainties.
6. Seek one irreversible consequence and one emotionally intelligible sacrifice. Avoid increasing stakes by random catastrophe.
7. Generate two alternative **PROPOSAL** causal maps: restrained and high-tension. Note delta against canon and production feasibility for each. Recommend smallest effective intervention.

## Output
`03_CAUSAL_ENGINE.md` containing event graph, counterfactual test, setup/payoff map, irreversible steps, ending consequence, source references, and a proposed revision order.

## Fail fast
- An unmotivated character changes personality to force a twist.
- A solution uses information introduced only in its solution scene.
- The audience sees no actual loss despite the stated stakes.
- Engineering lesson is announced but not visible in consequences.
