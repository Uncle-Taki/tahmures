# Tahmures: Codex direction, AI Studio implementation, local acceptance

**Routing update — 2026-10-20:** the owner asked Codex to take over implementation.
Use [the current Chapter 01 workflow](chapter-01-animation-workflow.md) and its
status/next-task files. The AI Studio procedure below is optional historical
handoff guidance, not a required next step. Background candidates and the beard
alpha repair now exist; older phase descriptions below are dated snapshots.

Prepared 2026-10-18. This is a task roadmap, subordinate to `AGENTS.md`,
`meta-prompt.md`, the project charter, narrative continuity and existing scoped
approval records. It does not replace `workflow/phase-status.json` or grant art,
voice, manuscript or release approval. Earlier upload packs remain historical
handoffs. The owner has pushed the project to a private GitHub repository;
use the repository workflow below as the primary handoff.

## Review update — 2026-10-20

The received `tahmures_complete_studio_bundle.json` is a specification draft,
not the implementation return required by task 01. Its certification flags do
not advance any phase. See `2026-10-20-studio-bundle-review.md` and the measured
`studio-bundle-review.json` for missing assets and metadata/semantic errors.

The corrected `chapter-01-production-plan.json` is the current **planning
candidate** for scenes/cues/environment dependencies; it is not a runtime manifest
or an approved screenplay. The current manuscript/continuity remain canonical.
The owner removed the hall's door-count/handle motif; the ordinary western gate
remains necessary for the role example. Raw/rejected history stays unchanged.

Task 01 (real Akvan extraction) remains pending. In parallel, task 02 produces
one Hall of Scripts environment candidate under `Characters/environments/`.
The brief defines eight reusable sets and all eleven scene mappings. Background
work, props/extras, camera blocking, text/font, audio, Godot implementation and
release evidence have separate bundles and gates. Complete character/set reviews
before a single S01 integration test; do not jump to a full chapter render.

## Roles and the working loop

**Owner:** chooses artistic outcomes, Simurgh's chapter form, reconstructed
surfaces and voice/performance. **Codex:** defines bounded tasks, maintains the
engineering plan, reviews actual diffs, runs local Python/Godot checks and reports
acceptance or specific rework. **Google AI Studio Build agent:** implements the
one assigned task and returns real changed files, evidence and limitations.
The agent cannot approve its own work or impersonate a Codex/owner review.

Use this loop for every task:

1. Codex supplies the repository baseline, protected-file hashes, task, allowed
   paths and tests in `ai-studio-baseline.json`.
2. Owner imports the private repository and branch `main` into AI Studio and
   pastes `ai-studio-start-here.md`. Record the actual imported revision.
3. AI Studio makes one bounded change and returns a patch/export or review branch.
4. Owner brings the actual files/export/branch to this chat, with its response.
5. Codex checks changed paths and hashes, applies into a separate candidate where
   appropriate, runs tests, renders and inspects visual differences.
6. Codex marks the task accepted for its exact scope or returns concrete rework.
   Owner reviews actual art/performance when required. Only then start the next task.

A text answer claiming files exist is not a deliverable. Preserve raw agent
responses as received evidence; never treat a `[file-tag: ...]` as a local file.

## Current baseline and failed-command repairs

The maintained candidate is `Characters/godot-character-library-recovery-01/`.
All 306 distinct required source/approval/index/head inputs were verified as tracked at
media baseline `e2f29bf431f1fffea4902e1276d2a5f6e6fb2660` on branch `main`.
Repository: `https://github.com/Uncle-Taki/tahmures`. The configured SSH remote is
`git@github.com:Uncle-Taki/tahmures.git`. SSH access was checked; repository
visibility is private as reported by the owner.

Ignored received ZIPs, duplicate extractions and transfer trees may exist on the
workstation. They are not required in the imported repository and must not be
requested or reconstructed as prerequisites.

The original builder and validator had unterminated newline string literals.
Those commands now execute. Transparent background RGB is normalized for exact
pixel recomposition while partial source alpha is preserved. Input approval
bindings and indexed files are actually checked. The validator fails on absent
outputs instead of silently skipping them. Generated metadata separates
received claims from local measurements and removes premature integration status.
Godot checks, source-coordinate centering, gallery backgrounds, head framing and
missing-resource behavior have been repaired and exercised locally.

However, source-pose recomposition is not anatomical segmentation. Rectangular
cuts can split a face or garment incorrectly while reproducing neutral perfectly.
The new character candidates support only neutral and whole-pose idle. The accepted
Tahmures head can be inspected separately. Chapter replacement is still unimplemented.

The full `make check PYTHON=.venv/bin/python` baseline still fails eight tests
because Persian Chapters 01–04 have stale English-source hashes; 789 tests pass.
This is an editorial review/reconciliation dependency, not a reason to alter the
manuscript or lie about the media gate. Complete current-revision human review
and scoped metadata reconciliation on that separate track before release.

## Phases and exit conditions

| Phase | Implementer and deliverable | Codex/owner exit gate |
|---|---|---|
| 0 — Local baseline repair | Codex: repaired scripts, ten generated candidates, validators, real Godot captures and command logs. | Local candidate checks pass; anatomical and editorial limitations remain explicit. Completed for the current baseline. |
| 1 — Anatomical cuts | AI Studio: one character per task, starting with Akvan. Explicit contour masks, correct part ownership, source/derived distinction and component plates. Then the other sources, with both Simurgh forms separate. | Codex checks source preservation, masks, layer-only recomposition and actual isolated parts. Rectangular tiles renamed as limbs do not pass. No synthetic hidden pixels masquerade as source extraction. |
| 1E — Environment design (parallel) | AI Studio task 02: one Hall of Scripts floor plan and editable wide-view candidate, then other views/lighting and the seven additional sets. | Codex checks actual source-character composite, perspective/ground/occlusion/caption regions; owner reviews actual art. No background is complete from a JSON claim. |
| 2 — Joint and prop review | AI Studio: parent/child rig hierarchy, pivots, honest coupled prop assemblies, documented uncovered regions and constrained movement. Reuse accepted Tahmures head. | Actual neutral/reset, supported motion and frame comparisons on light/dark/checker. Owner reviews any reconstructed art and selects Simurgh's chapter form. Unsupported blink/gaze/limb motion stays disabled. |
| 3 — Chapter recovery | AI Studio: new candidate project using real reusable layered rigs, with source-canvas-aware framing and no named-character fallback. Salvage verified timeline/caption code after inspection. | Codex tests all 11 scenes, seek/reset/replay, missing resources, HUD bounds, bilingual layout and 173-second duration plan. Old GLM project remains intact. Garshasp offstage; Div-e Sefid outside the current adaptation. |
| 4 — Complete silent exports | Local Godot execution under Codex review: EN and FA movies plus timed scene samples. AI Studio can supply scripts but must identify unavailable runtime tools. | Probe both actual files for duration/frame count, streams and complete ending. Visually inspect Persian/English captions and scene causality. File presence is not completion. |
| 5 — Voice and performance | Owner supplies recordings/transcripts/cues. AI Studio implements authorized synchronization; Codex runs local audio/caption checks. | Human listening/visual review. No rejected eSpeak, invented speech or unapproved mouth flapping. Two-state proxy and phoneme lip-sync are different scopes. |
| 6 — Final package and publication preparation | Codex reviews a minimal standalone package, rebuild dependencies and documentation. | Required media gates and full repository gate pass; final art/performance approval exists. Only explicitly selected final files are candidates for publication. No automatic commit, push or deployment. |
| 7 — Reuse | Repeat reviewed templates for Chapters 02–04 before scaling to 05–24. | Each chapter has its own narrative/caption/timing evidence and approval; pilot approval does not approve later chapters. |

Phase 1 remains the character task; Phase 1E can proceed independently for set
design. Do not jump from a successful import or export to Phase 3.
Planning for later phases may proceed while art decisions remain pending.

## Google AI Studio Build mode: practical use

Google's [official Build mode documentation](https://ai.google.dev/gemini-api/docs/aistudio-build-mode)
documents GitHub import, two-way sync and ZIP export. It describes web/Android
previews; it does not establish a Godot runtime in the Build environment.
Use its code-editing capabilities for this existing Godot/Python project.
Do not ask it to regenerate the project as React or invent a successful Godot run.

1. Use `https://github.com/Uncle-Taki/tahmures` in AI Studio after the
   repository update is pushed. Use **Add files (+) → Import from GitHub**
   and grant the interface access to the intended private repository if needed.
2. Select branch **main** where branch selection is available. Verify the imported
   files and branch in the interface; do not silently accept another branch.
   If the interface cannot select/retain main, use its branch/ref import option
   if provided, or return file patches without syncing. Never claim isolation
   merely because a prompt mentions a branch.
3. Paste `ai-studio-start-here.md`. The agent must read this roadmap, the baseline
   manifest, task 01 and return template before editing. No Drive links, five-part
   ZIP upload or `EXCHANGE-MANIFEST.json` is required for this primary workflow.
4. Record the actual imported revision separately from the fixed media baseline.
   A newer commit containing these handoff documents is expected after you push
   them. Compare protected file hashes; do not force AI Studio back to the older
   commit and lose the new instructions. If Git history is exposed, verify the
   media baseline is an ancestor. If it is not exposed, report that limit and
   verify accessible file bytes instead.
5. Ask for command outputs only for commands actually run. If Pillow, NumPy,
   RTK or Godot is unavailable, state the missing executable and return actual
   code/masks/contour data with exact workstation commands. Do not install new
   dependencies or claim a web/Android preview validated the Godot project.
6. Return the changed files/patch and `ai-studio-return-template.md`. If the owner
   separately instructs GitHub sync, verify its actual target branch first and
   record result commit(s). This handoff authorizes implementation, not automatic
   commits, pushes, merges or deployment. Codex reviews actual results locally
   before any next phase is assigned.

## Repository baseline and review contract

- Repository: `https://github.com/Uncle-Taki/tahmures`.
- Working/import branch: **main**, the branch already present in this checkout.
- Fixed media baseline: `e2f29bf431f1fffea4902e1276d2a5f6e6fb2660`.
- Exact baseline tree and required input/non-target output SHA-256 values:
  `editorial/media-handoff/ai-studio-baseline.json`.
- Import the published handoff revision. It differs from the fixed media
  baseline because it includes the newer workflow instructions.

The existing private repository is the collaboration source. There is no need
for another repository, a new exchange project or a separate upload archive.
The remote is configured as `origin` at
`git@github.com:Uncle-Taki/tahmures.git`. The owner authorized completing the
repository update. This authorizes the current handoff publication; future
AI Studio commits, pushes, merges and deployments still need their own instruction.

Keep `.gitignore` in force: transfer ZIPs, duplicate trees, Godot caches, rejected
movies and disposable logs stay local. Preserve tracked sources, Godot metadata,
required frozen dependencies and selected approval evidence. Do not restore
ignored content simply to match an old upload inventory or use `git add -f`.
A missing required tracked file must be reported by its exact path.

For task 01, the source/approval inputs and other nine characters' output hashes
are protected. The baseline file is review evidence and is outside AI Studio's
edit scope. Do not rewrite that baseline to make an accidental change disappear.
Codex compares changed paths and hashes, runs focused checks, captures actual
Godot output, inspects the anatomy, and reports technical acceptance/rework.
The owner still decides new art, occlusion reconstruction and performance.

The earlier `ai-studio-exchange.zip` and `prepare_ai_studio_exchange.py` are
optional offline fallbacks. Their old snapshots are not the authority for a newer
repository revision. A fallback export needs its own manifest and actual source
revision; never mix it silently with a GitHub import. The current repository is
complete enough to run the media checks on a suitable local workstation. The
book gate remains a separate check with its recorded editorial baseline failures.

## Next action

Import the updated repository branch **main**, and paste
`ai-studio-start-here.md`. Task 01 repairs **Akvan only** and returns real changed files.
Task 02 may proceed separately for one hall set, under its own allowed paths.
Bring each actual export/patch and response back here. Codex will inspect isolated head,
face, torso, arms and coupled tablet-hold masks and run the next local acceptance
pass before expanding the operation to the rest of the library.
