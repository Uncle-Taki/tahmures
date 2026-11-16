# AI Studio handoff — existing private GitHub repository

Repository: [`Uncle-Taki/tahmures`](https://github.com/Uncle-Taki/tahmures).
The working/import branch is **main**. The owner has authorized completing the
repository update. No second repository is needed.

After the handoff update is published, open Google AI Studio
Build mode, import that repository/branch, and paste
[`ai-studio-start-here.md`](ai-studio-start-here.md).

## Current review — 2026-10-20

For the remaining work through completed bilingual animation, use the
[current Codex production workflow](chapter-01-animation-workflow.md),
[production status](chapter-01-animation-status.json) and
[next bounded task](chapter-01-next-task.md). These replace the older requirement
to hand the next implementation task to AI Studio. Codex now continues locally.

The [34-shot static storyboard](../../Characters/animations/chapter-01-candidate-01/planning/index.html),
asset/action matrix and S01 proof specification are now prepared. The next unit
is [S01 implementation](chapter-01-s01-implementation-task.md); planning imagery
does not claim performed contact actions, voice or artistic approval.

The owner supplied `tahmures_complete_studio_bundle.json`. The
[acceptance review](2026-10-20-studio-bundle-review.md) rejects its all-ten
certification claims as unsupported. Task 01 still needs actual Akvan masks/code
and runtime evidence; no new rig approval or chapter implementation is inferred.

Use the [corrected chapter planning candidate](chapter-01-production-plan.json),
[environment brief](chapter-01-environment-brief.md) and
[Hall design task](ai-studio-task-02-environments.md) for the missing setting work.
The door-count/handle detail has been removed from the current English/Persian
opening and future planning. The raw export and rejected scenes remain historical.

## Generate Chapter 01 backgrounds in Gemini web

**Current continuation:** the owner requested Codex take over after Gemini quota
was exhausted. The [local library](../../Characters/environments/chapter-01-candidate-01/README.md)
now contains 25 image candidates, two blank stages, provenance and Godot previews.
The manual workflow below remains an alternative, not the current execution status.

Start with [the exact upload workflow](gemini-background-workflow.md) and
[the collected reference pack](gemini-background-reference-pack/START-HERE.md).
The pack includes copied source images, prompt documents, one-shot launchers
and a hash manifest; the adjacent ZIP is a local transport convenience.

Use the [Gemini / Argon / Nano Banana master prompt](gemini-background-master-prompt.md),
[25 individual shot prompts](gemini-background-shot-prompts.md) and
[download/review queue](gemini-background-queue.json). The master lists the actual
reference images to attach and includes an optional text-only Argon direction
step. Generate and select the hall master first, then reuse it across views.
The queue covers all eleven scenes; two diagram/end-card stages use editable
code-native graphics separately. Queue entries now record actual candidate files.

This owner-run image workflow is separate from the code/SVG-only AI Studio
task 02. Flat generated images are candidates for local review and layer
preparation; they do not yet fulfil the full environment package contract.

## Current handoff files

| File | Purpose |
|---|---|
| [Starting prompt](ai-studio-start-here.md) | Paste into the imported AI Studio project. |
| [Roadmap](ai-studio-roadmap.md) | Roles, phases, GitHub-based loop and exit gates. |
| [Baseline manifest](ai-studio-baseline.json) | Fixed media commit/tree, required tracked inputs and other characters' protected output hashes. |
| [Task 01](ai-studio-task-01.md) | Akvan anatomical extraction only. |
| [Return template](ai-studio-return-template.md) | Actual revision, changed files, tests, limitations and review request. |

The fixed media baseline is `e2f29bf431f1fffea4902e1276d2a5f6e6fb2660`.
The published handoff revision is newer. Record both;
do not revert away the new instructions just to match the earlier commit.

The active project is `Characters/godot-character-library-recovery-01/` at the
repository root. Its README contains local build, validation, Godot test and
gallery commands. All 306 distinct required source/approval/index/head inputs were
confirmed tracked when this handoff was prepared. The manifest records their
actual baseline bytes; AI Studio must verify its imported inputs.

AI Studio implements one task; Codex reviews actual files, runs local checks and
inspects actual Godot output; the owner reviews new art and performance. Passing
source-pose tests does not approve anatomical cuts or chapter integration.

## Historical and optional material

`gemini-web-continuation.md`, `gemini-local-continuation.md` and
`glm-chapter-01-godot-completion.md` are historical handoffs. Their earlier
Drive/ZIP and phase instructions do not select the current task. Dated audits
record observations at the time of each inspection.

The ignored ZIPs, split movie chunks, received duplicate extractions and
`ai-studio-exchange/` directory are local transfer backups. AI Studio does not
need them to work on the imported repository. `prepare_ai_studio_exchange.py`
remains an optional offline fallback, not the primary collaboration path.

The configured SSH remote is `git@github.com:Uncle-Taki/tahmures.git`; remote
access was checked. GitHub visibility is private as reported by the owner.
The current repository update is owner-authorized; the AI Studio task itself
does not authorize further automatic commits, pushes, merges or deployments.
