---
name: tahmures-punch-and-timing
description: Locate, measure and improve dramatic punch times: revelation, reversal, decision, threat, emotional turn, ironic beat, purposeful silence and episode hook.
---

# Punch moments and temporal design

In this project **punch time** means a demonstrable **beat landing**, not a joke quota or an arbitrary shock every N seconds. Use waveform/audio time, approved `timeline.json` and scene transitions when available.

## Non-negotiable source and approval rules
- Work inside the actual Tahmures repo. Read root/nested `AGENTS.md`, `meta-prompt.md`, `book/project-charter.md`, `book/narrative-continuity.md`, and the canonical English chapter relevant to the task. Follow project-local editorial skill and approvals. The English narrative and continuity are canonical for story facts; media adaptations have their own scoped approval.
- For Chapter 01, inspect `editorial/media-handoff/chapter-01-animation-status.json` and the selected revision under `Characters/animations/chapter-01-candidate-01/production/english-final-03/`, including its README, timeline and reviews, and check for documented superseding decisions.
- Do not assume an 11-scene count or change approved duration: verify the real timeline and flag any mismatch. Div-e Sefid serves as messenger in the approved Chapter 01 animation, while Chapar is a distinct courier. Do not merge them.
- Separate every claim or suggestion with labels **CANON**, **APPROVED MEDIA ADAPTATION**, **PROPOSAL**, **CONFLICT**, or **UNKNOWN**. Cite repo paths (and line/section/scene identifiers when available) for source-derived claims. A proposed line or scene is never an approved line or scene.
- Do not modify canonical English/Persian manuscripts, continuity, approved media, approvals, or status records without the owner's explicit permission. Do not create new voice, imagery, provider calls, uploads, commits, pushes, or deployments. Candidate writing stays in a new working folder.
- The episode must remain original teaching fiction distinct from *Shahnameh*: no modern engineering jargon in the ancient-world scene, a concrete chapter-specific failure with consequences, divs as capable and uncertain rather than just evil, a correctly identified failure owner, an explicit engineering bridge, and a hook to the next chapter.

## Procedure
1. Build the existing time ledger from approved production timeline, shot IDs, and recordings. Record source, start/end, and uncertainty. Never shift approved cuts or audio without scope approval.
2. Tag beats with an explicit type: `HOOK`, `REVEAL`, `REVERSAL`, `DECISION`, `COST`, `SUBTEXT`, `MOTIF_PAYOFF`, `COMIC_RELEASE`, `SILENCE`, `BRIDGE`, `NEXT_EPISODE_HOOK`. Some scenes legitimately have no high-impact beat.
3. For each proposed punch ask: **setup**, audience expectation before it, actual change in knowledge/power/goal, landing image/line/action, duration of attention before next line, emotional aftershock, dependency on earlier beat.
4. Mark positions in both absolute time `mm:ss.s` and relative `% of episode` **only if verified runtime is known**. For unknown runtime provide ordered sequence with `TBD` timing; no fictitious timestamps.
5. Rate each punch `0-3` impact (not objective truth) with why: `0=no change`, `1=local`, `2=reshapes scene`, `3=reshapes episode`. Look for clusters, repeated same-type beats, excessive exposition before a hook, unsupported last-minute revelation, and no recovery/silence.
6. Try a **contrast pass**: replace one verbal punch with a held reaction or prop close-up; move one revelation earlier to increase dread; end a scene on a costly choice instead of explanation. Mark all timing changes PROPOSED.
7. Run a table read / animatic timing simulation against actual spoken dialogue and physical action. Written words-per-minute is not proof of the final performance; use approved audio timings when possible.

## Output
`06_PUNCH_MAP.csv` (see template), `06_PACING_NOTES.md` with peaks/valleys, absolute and relative time audit, three highest-value candidate improvements, and unresolved approval/time blockers.

## Anti-formula principle
Emotion should accumulate. A long quiet sequence can be the dramatic peak; avoid uniformly spaced twists, unmotivated cliffhangers, and jokes that undercut consequences.
