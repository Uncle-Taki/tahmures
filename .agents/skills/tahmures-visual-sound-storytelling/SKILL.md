---
name: tahmures-visual-sound-storytelling
description: Turn dramatic intentions into 2D-animatable actions, props, shot priorities, sound cues and silence rather than explaining the story in dialogue.
---

# Visual and sonic storytelling

## Non-negotiable source and approval rules
- Work inside the actual Tahmures repo. Read root/nested `AGENTS.md`, `meta-prompt.md`, `book/project-charter.md`, `book/narrative-continuity.md`, and the canonical English chapter relevant to the task. Follow project-local editorial skill and approvals. The English narrative and continuity are canonical for story facts; media adaptations have their own scoped approval.
- For Chapter 01, inspect `editorial/media-handoff/chapter-01-animation-status.json` and the selected revision under `Characters/animations/chapter-01-candidate-01/production/english-final-03/`, including its README, timeline and reviews, and check for documented superseding decisions.
- Do not assume an 11-scene count or change approved duration: verify the real timeline and flag any mismatch. Div-e Sefid serves as messenger in the approved Chapter 01 animation, while Chapar is a distinct courier. Do not merge them.
- Separate every claim or suggestion with labels **CANON**, **APPROVED MEDIA ADAPTATION**, **PROPOSAL**, **CONFLICT**, or **UNKNOWN**. Cite repo paths (and line/section/scene identifiers when available) for source-derived claims. A proposed line or scene is never an approved line or scene.
- Do not modify canonical English/Persian manuscripts, continuity, approved media, approvals, or status records without the owner's explicit permission. Do not create new voice, imagery, provider calls, uploads, commits, pushes, or deployments. Candidate writing stays in a new working folder.
- The episode must remain original teaching fiction distinct from *Shahnameh*: no modern engineering jargon in the ancient-world scene, a concrete chapter-specific failure with consequences, divs as capable and uncertain rather than just evil, a correctly identified failure owner, an explicit engineering bridge, and a hook to the next chapter.

## Procedure
1. For every scene ask: what can the audience know from **action, blocking, composition, eyeline, a withheld object, a repeated gesture, sound or silence** before any words?
2. Convert at least one expository exchange into a playable visual action (where source/approval allows), e.g. delay in handing an object, a deliberate positioning choice, or change in witness orientation. Do not manufacture new props as canon.
3. Define strongest scene-entry image and scene-exit image; emotional continuity and motivated eyelines; readable staging in a simple 2D silhouette; staging that can be animated in short, controllable shots.
4. Develop a soundtrack logic: diegetic signal, ritual rhythm, footsteps, distant reaction, approved spoken line, and purposeful silence. New audio assets are **proposed only**, never automatically generated.
5. Produce storyboard-ready **dramatic shot intentions** but do not insert model prompts, image references, or new timing into approved production manifests. Those belong to the downstream Flow handoff after approval.
6. Flag practical risks: crowd scenes, many speaking heads, changing perspective, continuous difficult hands, long lip-sync requirements, repeated characters and props, tight shot continuity. Prioritize close, staged action over gratuitous camera movement.
7. Propose a 30-second read-only muted animatic check: if the audience can't follow what's at stake without narration, specify missing visual evidence; don't invent frames.

## Output
`08_VISUAL_SOUND_PASS.md`: before/after action possibilities, picture-first storytelling, sound/silence beat map, key visual motif, 2D feasibility and Flow-handoff notes.

## Gate
Every added image/action does dramatic work and remains traceable to either canon or an explicitly unapproved proposal.
