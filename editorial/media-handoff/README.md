# AI Studio handoff — existing private GitHub repository

Repository: [`Uncle-Taki/tahmures`](https://github.com/Uncle-Taki/tahmures).
The working/import branch is **main**. The owner has authorized completing the
repository update. No second repository is needed.

After the handoff update is published, open Google AI Studio
Build mode, import that repository/branch, and paste
[`ai-studio-start-here.md`](ai-studio-start-here.md).

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
