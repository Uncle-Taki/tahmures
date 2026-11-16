# Codex task — use installed Tahmures story-room skills to strengthen Chapter 01 writing

You are running at the **root of the actual Tahmures GitHub repository**. I want a highly professional dramatic-writing pass for **Chapter 01 — Ancient Tablet** so that the eventual episodic 2D animation has compelling stakes, original layered dialogue, precise dramatic turns and purposeful punch timing. I admire **Bahram Beyzai** as a playwright: be guided by high-level theatrical principles supported by research—myth reexamined, narrative framing, unreliable testimony, ritual, competing voices, questions of power and accountability, performable poetic pressure—**but write genuinely original dialogue and scenes, not an imitation of his distinctive language or any recognizable work**.

## Hard boundaries
- First read all applicable `AGENTS.md`, `meta-prompt.md`, `book/project-charter.md`, `book/narrative-continuity.md`, the **actual canonical English Chapter 01**, current editorial media status, active `english-final-03` production README/timeline/manifests/approval records, and relevant `.agents/skills/tahmures-editorial/` guidance. Check whether newer approved records supersede the known revision; document exact evidence.
- Preserve the distinction between the **canonical manuscript**, **approved media adaptations**, and **unapproved writing proposals**. The current Chapter 01 adaptation uses **Div-e Sefid as messenger**; **Chapar is another courier**. Avoid rewriting character roles, replacing approved dialogue, or moving the shot timing silently.
- I target **11 scenes**, but verify the actual scene count and exact timeline; identify any discrepancy without pretending that 11 is canon. A scene is not an individual short video clip.
- Ancient-world drama uses no modern engineering jargon; preserve the chapter-specific failure, real costs, the correct failure owner, nuance of divs, actual engineering bridge, and next-chapter hook. Keep Tahmures fiction distinct from the *Shahnameh*.
- **LOCAL CANDIDATE WRITING AND SYNCHRONIZED CANDIDATE FLOW HANDOFF ONLY.** Produce a complete updated *candidate* Flow handoff in a new folder. Do not modify source manuscripts, Persian translation, continuity, approved images/voices/Godot media, `timeline.json`, acceptance records or the existing official Flow handoff. Do not call Google Flow or any provider, upload, generate images/video/voices, commit, push or deploy. No new dependencies unless absolutely necessary. No claims of owner artistic approval.

## Skills to use explicitly
Start by reading and invoking `$tahmures-story-room-director` as the coordinating skill. Then open/read the actual `SKILL.md` for each specialist skill before the numbered phases below. If any skill is missing, stop calling it 'installed' and report that, but still deliver source-grounded partial work.

1. `$tahmures-episode-purpose`: extract the central dramatic question, emotional transformation, promise, ethical tension and engineering teaching bridge. Present 2–3 **PROPOSAL** loglines; recommend one with justification.
2. `$tahmures-character-pressure`: map each character's immediate goal, fear, values, knowledge, tactics, contradiction and unique agency. Test nuanced opposition and distinguish Chapar from Div-e Sefid.
3. `$tahmures-causal-architecture`: audit cause/effect, event ownership, escalation, critical reversals and price of choices. Propose the smallest improvements that earn their consequences.
4. `$tahmures-original-iranian-dramaturgy`: apply original, high-level Iranian theatrical/mythic framing without copying any Beyzai phrase, plot or scene. Offer restrained and ceremonial **candidate** approaches only where appropriate.
5. `$tahmures-eleven-scene-blueprint`: inspect actual 11-scene claim versus timeline and produce playable scene cards with objectives, turns, obstacles, entry/exit state, visual beats and source citations.
6. `$tahmures-punch-and-timing`: extract dramatic punch timings from real `timeline.json`/recordings (hook, revelation, reversal, cost, silence, payoff). If precise time is missing, mark **TBD**, not invented timestamps. Seek contrast and build, not a mechanical punch quota.
7. `$tahmures-dialogue-and-subtext`: extract existing lines accurately, diagnose subtext and unique voice, write **two distinct original candidate alternatives** for pivotal exchanges (economical vs ceremonially heightened), include performance and duration implications. Preserve approved recordings and lip-sync signoffs.
8. `$tahmures-visual-sound-storytelling`: convert needless exposition into readable 2D actions, entrances/exits, symbolic objects, rhythmic sound and meaningful silence. Check staging and voice production feasibility.
9. `$tahmures-series-continuity`: report all canon/adaptation/presentation conflicts, language scope, provenance, character identity and future-series promises; never silently fix canonical files.
10. `$tahmures-story-red-team`: independent adversarial review; assess clear cause/effect, emotional cost, agency, power, original dialogue, punch placement, 2D producibility and instruction accuracy. Provide prioritized fix cards and evaluate the revised **proposal** again.

Invoke `$tahmures-flow-handoff-sync` to regenerate all dependent *candidate* Google Flow contexts and prompts from the selected writing proposal; then return to `$tahmures-story-room-director` to assemble the integrated deliverables and owner-review gates.

## Outputs to CREATE, not just outline
Create a non-destructive candidate package at `editorial/media-handoff/story-room/chapter-01-candidate-01/` unless the existing repo has a better safe candidate location. Prefer the installed `story-room/templates/` files. Make at least:
- `README.md` (scope, status, how to review and approve)
- `00_SOURCE_LEDGER.md` (real source citations, authority, actual scene count/duration, approval evidence)
- `01_EPISODE_PURPOSE.md`
- `02_CHARACTER_PRESSURE.md`
- `03_CAUSAL_ENGINE.md`
- `04_DRAMATURGY_OPTIONS.md`
- `05_SCENE_BLUEPRINT.md` and `11_SCENE_MATRIX.csv`
- `06_PUNCH_MAP.csv` and `06_PACING_NOTES.md`
- `07_DIALOGUE_SCORE.md` and `07_CANDIDATE_SCRIPT.md`
- `08_VISUAL_SOUND_PASS.md`
- `09_CONTINUITY_AUDIT.md`
- `10_STORY_RED_TEAM.md`
- `11_OWNER_DECISIONS.md` (concise approve/reject questions, individually actionable)
- `12_FLOW_WRITING_HANDOFF.md` (shot-writing intent and per-shot source mapping)
- `flow-handoff-candidate/` (complete synchronized candidate Flow package, instructions, prompts, assets mapping, guides, impact matrix, and promotion/approval plan)

Where a concrete rewrite is blocked because of owner approval or uncertain timing, still produce the source-grounded diagnosis and clearly labeled options. Use explicit **CANON**, **APPROVED MEDIA ADAPTATION**, **PROPOSAL**, **UNKNOWN**, and **CONFLICT** tags in all artifacts.

## Creative standards
Make the story **dramatic first, instructional second**. Evidence over rhetoric; consequence over declaration; active decision over coincidence; ambiguity over simplistic villains; observed conflict over history lecture. The dialogue must be performable, specific to character, and usually economical; heightened language is reserved for motivated peaks. Test how the scene works without audio as well as with approved dialogue. Do not alter future-chapter continuity casually. Avoid formulaic 'beats at exactly 30%, 50%, 90%' and do not manufacture twists to fill a chart.


## Mandatory new phase — synchronize ALL Google Flow handoff contexts (candidate now; approved revision only after owner authorization)
**This phase is required in the SAME Codex run as the story-room improvement.** Read the previous Google Flow handoff prompt (if present), the actual current Flow handoff in the repository, `editorial/media-handoff/`, and the active production revision. Invoke `$tahmures-flow-handoff-sync` after story red-team and before final reporting. Do not stop after `12_FLOW_WRITING_HANDOFF.md`: it is an input to a comprehensive synchronized handoff, not the complete deliverable.

### A. Generate a complete, usable candidate Flow handoff NOW
Build `editorial/media-handoff/story-room/chapter-01-candidate-01/flow-handoff-candidate/`, using the repository's existing naming and layout where applicable. Physically create updated documents (not just a suggestion to update them later):
- `README.md` — version, candidate status, operator quick start, blockers, and exact pointers to the existing production handoff.
- `context/` — episode purpose, story/logline, character motivations and subtext, canon vs approved adaptation vs proposals, visual style, locations, props, continuity and scene-to-scene states. Respect the authoritative manuscript/continuity and actual source files.
- `agent-instructions/` — **candidate** Flow Agent instruction blocks for story intent, identity/style consistency, performance/subtext, dramatic pacing, silence, negative constraints and authority/approval boundaries; explicitly reconcile the existing `Tahmures — Veo visual consistency agent instructions` rather than installing a competing style bible.
- `episode-01/` — real source-backed scene index, individual shot briefs/prompts, start/end frame instructions, shot-to-character/background/prop references, dialogue/audio cue maps, reveal/decision/silence/punch placements, duration implications, transition logic, shot QA, and assembly plan. Derive scene IDs/times from the actual timeline; unapproved new timings are `PROPOSED`/`TBD`.
- `assets/` and `manifests/` — safe copies or links only to authorized existing reference images, shot-to-asset mapping, content hashes where feasible, missing/needs-approval list; never generate or replace visual source art by assumption.
- `guides/` — updated, actionable human Google Flow operating instructions (create/reuse Characters, upload references, install/reconcile Agent instructions, create frames, choose model per shot, generate/iterate, integrate approved audio, assemble/export, return downloaded media to repo). Distinguish documented UI capability from unverified UI specifics.
- `CHANGE_IMPACT_MATRIX.csv` — **one row for each proposed story/dialogue/shot change**, with story source ID, prior value, proposed value, downstream context/character/shot/dialogue/timing/asset/Flow-prompt files, approval status, owner decision, and validation status.
- `HANDOFF_DIFF_AND_PROMOTION.md` — exact file-by-file proposed changes versus the existing Flow handoff, conflicts, migration steps, and owner sign-off checklist.
- `VALIDATION_REPORT.md` — broken paths, unapproved references, inconsistent dialogue, timeline mismatch, duplicate/conflicting agent instructions, missing shots, audio and lip-sync implications, plus tests actually run.

Reuse/reconcile any prior Google Flow handoff instead of fabricating a parallel source of truth. Mark *every* candidate file **NOT APPROVED FOR PRODUCTION / NOT AUTHORIZED FOR FLOW GENERATION** until the applicable story, media, visuals, dialogue and timing approvals are recorded. Do not portray revisions to canonical script or approved media as already accepted. If the story-room proposes multiple alternatives, choose one **RECOMMENDED PROPOSAL** per shot for a coherent working package, retaining alternatives and explicit decision points.

### B. Strict synchronization checks
Trace every proposed change across this chain: **episode goal → character decision → scene turn → punch timestamp → dialogue and voice implications → visual actions → frames/references → Flow shot prompt → scene assembly → continuity**. All scene IDs, cast roles, props, location names, and quoted dialogue should align with the source ledger or carry an explicit PROPOSAL tag. Verify consistency of Div-e Sefid vs Chapar; preserve English/Persian approval scopes. If a story beat exceeds the existing audio/timeline duration, report the constraint and candidate options; never stretch an approved timeline or replace approved recordings silently. Where no source supports an image, add a blocker rather than an invented upload-ready file.

### C. Owner-approved promotion is a separate, explicit action
For the current run, create the synchronized *candidate* package without altering the official Flow handoff or canonical/approved media. If and only if the user has already explicitly approved specific changes with a verifiable recorded scope, additionally prepare a **new versioned official Flow handoff revision** using only those approved changes; never silently overwrite historical or existing approved files. Otherwise, stop at candidate files, record approvals needed and provide the precise follow-up Codex command for promotion after the owner reviews the candidate. Never make paid provider calls, upload to Flow, or spend credits merely because a writing proposal passed a test.

## Verify and report
- Validate the installed skill bundle with `python3 story-room/scripts/validate_skill_bundle.py .` if present; run repo editorial/read-only or scoped checks where relevant, without modifying production outputs. If `make check PYTHON=.venv/bin/python` is feasible, report whether you actually ran it and the result; don't pretend it validates artistic quality.
- Ensure every proposed scene change has an actual source/approval label and production impact, and that all time fields match source or read TBD. Distinguish source voice recordings from approved mouth alignment.
- Final response: exact created paths including `flow-handoff-candidate/`, number of Flow prompts/shot briefs updated, changes propagated to Agent instructions and dialogue/asset/timing maps, actual source-backed scene count, known vs proposed length, 3 most important dramatic improvements, a one-paragraph explanation of Beyzai-informed **original** craft, a concise owner approval and promotion checklist, checks run/results, and explicit statement that canon / existing official Flow handoff / existing approved media / providers / commits / pushes were untouched.

**Perform the local file work now. Do not ask me to restate repo facts. Do not stop with a plan; deliver candidate drafts and audits based on the evidence currently available.**
