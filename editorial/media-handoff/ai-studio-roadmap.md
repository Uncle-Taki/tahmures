# Tahmures: Codex direction, AI Studio implementation, local acceptance

Prepared 2026-10-18. This is a task roadmap, subordinate to `AGENTS.md`,
`meta-prompt.md`, the project charter, narrative continuity and existing scoped
approval records. It does not replace `workflow/phase-status.json` or grant art,
voice, manuscript or release approval. Earlier upload packs remain historical
handoffs; use the new local recovery baseline for this workflow.

## Roles and the working loop

**Owner:** chooses artistic outcomes, Simurgh's chapter form, reconstructed
surfaces and voice/performance. **Codex:** defines bounded tasks, maintains the
engineering plan, reviews actual diffs, runs local Python/Godot checks and reports
acceptance or specific rework. **Google AI Studio Build agent:** implements the
one assigned task and returns real changed files, evidence and limitations.
The agent cannot approve its own work or impersonate a Codex/owner review.

Use this loop for every task:

1. Codex supplies the exact baseline hash manifest, task, allowed paths and tests.
2. Owner imports that baseline into AI Studio and pastes the task prompt.
3. AI Studio makes one bounded change and returns a patch/export or review branch.
4. Owner brings the actual files/export/branch to this chat, with its response.
5. Codex checks changed paths and hashes, applies into a separate candidate where
   appropriate, runs tests, renders and inspects visual differences.
6. Codex marks the task accepted for its exact scope or returns concrete rework.
   Owner reviews actual art/performance when required. Only then start the next task.

A text answer claiming files exist is not a deliverable. Preserve raw agent
responses as received evidence; never treat a `[file-tag: ...]` as a local file.

## Current baseline and failed-command repairs

The received package is preserved in `godot-character-library-recovery-01.zip`
at the repository root. The maintained local candidate is
`Characters/godot-character-library-recovery-01/`. A second nested extraction and
the root manifest are historical received copies, not active edit targets.

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
| 2 — Joint and prop review | AI Studio: parent/child rig hierarchy, pivots, honest coupled prop assemblies, documented uncovered regions and constrained movement. Reuse accepted Tahmures head. | Actual neutral/reset, supported motion and frame comparisons on light/dark/checker. Owner reviews any reconstructed art and selects Simurgh's chapter form. Unsupported blink/gaze/limb motion stays disabled. |
| 3 — Chapter recovery | AI Studio: new candidate project using real reusable layered rigs, with source-canvas-aware framing and no named-character fallback. Salvage verified timeline/caption code after inspection. | Codex tests all 11 scenes, seek/reset/replay, missing resources, HUD bounds, bilingual layout and 173-second duration plan. Old GLM project remains intact. Garshasp offstage; Div-e Sefid outside the current adaptation. |
| 4 — Complete silent exports | Local Godot execution under Codex review: EN and FA movies plus timed scene samples. AI Studio can supply scripts but must identify unavailable runtime tools. | Probe both actual files for duration/frame count, streams and complete ending. Visually inspect Persian/English captions and scene causality. File presence is not completion. |
| 5 — Voice and performance | Owner supplies recordings/transcripts/cues. AI Studio implements authorized synchronization; Codex runs local audio/caption checks. | Human listening/visual review. No rejected eSpeak, invented speech or unapproved mouth flapping. Two-state proxy and phoneme lip-sync are different scopes. |
| 6 — Final package and publication preparation | Codex reviews a minimal standalone package, rebuild dependencies and documentation. | Required media gates and full repository gate pass; final art/performance approval exists. Only explicitly selected final files are candidates for publication. No automatic commit, push or deployment. |
| 7 — Reuse | Repeat reviewed templates for Chapters 02–04 before scaling to 05–24. | Each chapter has its own narrative/caption/timing evidence and approval; pilot approval does not approve later chapters. |

Phase 1 is the immediate next task. Do not jump from a successful import to Phase 3.
Planning for later phases may proceed while art decisions remain pending.

## Google AI Studio Build mode: practical use

Google's [official Build mode documentation](https://ai.google.dev/gemini-api/docs/aistudio-build-mode)
documents GitHub import, two-way sync and ZIP export. It describes web/Android
previews; it does not establish a Godot runtime in the Build environment.
Use its code-editing capabilities for this existing Godot/Python project.
Do not ask it to regenerate the project as React or invent a successful Godot run.

1. Open Build mode. Use **Add files (+) → Import from GitHub** if an approved
   exchange repository/branch exists; otherwise use accessible source files and
   ask for a real patch/export, not a web scaffold. Verify available import
   features in your account before assuming any ZIP can be unpacked.
2. Paste `ai-studio-task-01.md` and provide `ai-studio-exchange.zip` or the matching
   reviewed source snapshot. Ask it to list actual readable files first.
3. If a GitHub-connected workspace is used, inspect **Settings → GitHub** for its
   repository and branch before syncing. Never sync directly to the book's main
   branch. If safe branch isolation is unavailable, download ZIP/patch results
   and return them here for local review instead.
4. Ask for command outputs only for commands actually run. If Pillow, NumPy or
   Godot are unavailable there, return code, masks/contour data and exact local
   commands; Codex runs them on the workstation. Do not install new dependencies,
   add provider calls or use generated imagery to fill missing surfaces without scope.
5. Return files plus `ai-studio-return-template.md`. Preserve the baseline identity
   and separate technical checks, art acceptance and full repository status.

## GitHub preparation (not performed by this handoff)

The current repository has no configured Git remote. No remote, repository,
commit, branch, push, PR or deployment has been created by this work.
Your request to consider GitHub is a planning request; a destination and explicit
publishing instruction are still needed before external writes.

Recommended exchange: a **private media workbench** or an isolated review branch
such as `codex/character-recovery`, with Codex reviewing every returned diff.
Do not publish the whole dirty book checkout or force an exception to the
owner's final-files-only publication policy. A temporary candidate exchange is a
separate explicit owner decision. Source publication and final book release are
distinct actions.

`prepare_ai_studio_exchange.py` builds a reviewable local snapshot and manifest.
It includes the maintained candidate, original source references, required
approval/index dependencies, selected canonical context and these task documents.
It excludes `.git`, editor caches, raw chat transcripts, old received duplicate
trees, giant upload ZIPs and movie renders. This is a selected snapshot, not a
full checkout. It can run the media candidate checks, not the entire book gate.

Before a future push, Codex will review the exact staged path list against the
snapshot manifest, identify any missing rebuild dependency, and confirm the
target private repository/branch. No `git add .` across this working tree.
Once you authorize the destination, a concrete minimal candidate can be published
without exposing unrelated manuscript edits or replacing historical approvals.

## Next action

Use `ai-studio-task-01.md`: repair **Akvan only**, return real changed files.
Bring its export/patch and response back here. Codex will inspect isolated head,
face, torso, arms and coupled tablet-hold masks and run the next local acceptance
pass before expanding the operation to the rest of the library.
