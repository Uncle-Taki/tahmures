---
name: tahmures-series-continuity
description: Audit an episode draft against Tahmures canon, approved media adaptation, language scope, recurring characters, world rules, artifacts and hooks.
---

# Series continuity and approval audit

## Non-negotiable source and approval rules
- Work inside the actual Tahmures repo. Read root/nested `AGENTS.md`, `meta-prompt.md`, `book/project-charter.md`, `book/narrative-continuity.md`, and the canonical English chapter relevant to the task. Follow project-local editorial skill and approvals. The English narrative and continuity are canonical for story facts; media adaptations have their own scoped approval.
- For Chapter 01, inspect `editorial/media-handoff/chapter-01-animation-status.json` and the selected revision under `Characters/animations/chapter-01-candidate-01/production/english-final-03/`, including its README, timeline and reviews, and check for documented superseding decisions.
- Do not assume an 11-scene count or change approved duration: verify the real timeline and flag any mismatch. Div-e Sefid serves as messenger in the approved Chapter 01 animation, while Chapar is a distinct courier. Do not merge them.
- Separate every claim or suggestion with labels **CANON**, **APPROVED MEDIA ADAPTATION**, **PROPOSAL**, **CONFLICT**, or **UNKNOWN**. Cite repo paths (and line/section/scene identifiers when available) for source-derived claims. A proposed line or scene is never an approved line or scene.
- Do not modify canonical English/Persian manuscripts, continuity, approved media, approvals, or status records without the owner's explicit permission. Do not create new voice, imagery, provider calls, uploads, commits, pushes, or deployments. Candidate writing stays in a new working folder.
- The episode must remain original teaching fiction distinct from *Shahnameh*: no modern engineering jargon in the ancient-world scene, a concrete chapter-specific failure with consequences, divs as capable and uncertain rather than just evil, a correctly identified failure owner, an explicit engineering bridge, and a hook to the next chapter.

## Procedure
1. Build a source-of-truth matrix from canonical English narrative, `book/narrative-continuity.md`, approved episode-specific media records, actual timeline and role manifests.
2. Inspect draft for names, character functions, status, obligations, physical identity, event order, geography, props, abilities/limitations, secrets known, spoken claims, evidence, promises made, and change of state across scenes.
3. Label an intentional animation adaptation separately from the English manuscript and any Persian translation. Never back-port creative candidates into the manuscript silently.
4. For Chapter 01 assert messenger=Div-e Sefid and separate courier=Chapar; compare by role and appearance, not just strings.
5. Identify accidental modern jargon inside the ancient-world sequences and assess the engineering bridge for accuracy and truthful attribution of failure owner.
6. Identify setup/payoff obligations introduced for later episodes; do not prematurely resolve established questions or invent future-canon changes.
7. Review proposed rewrites for art/voice production implications and existing scoped approvals. Mark effects on `timeline.json`, actor recordings, lip sync, environment assets, legal/rights, source hashes.

## Output
`09_CONTINUITY_AUDIT.md`: source citation matrix; PASS/CONFLICT/UNKNOWN/BLOCKED findings by priority; candidate continuity delta requiring owner approval; zero silent canon mutations.

## Gate
No unresolved high-severity contradiction is misrepresented as production-ready.
