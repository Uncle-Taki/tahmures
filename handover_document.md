# Tahmures continuation handover — GLM 5.3

Snapshot: 2026-10-01 (post-English-freeze metadata reconciliation). Purpose:
continue from the frozen English source toward F01 Persian synchronization.
This document records state and constraints; it does not authorize new work,
replace canonical policy, or provide independent acceptance evidence.

## 1. Current state summary

Tahmures is a bilingual engineering book for working developers. English is
canonical; Python defines canonical teaching behavior; Go preserves equivalent
observable behavior. Experiments run offline.

**Stage:** English source frozen; F01 Persian synchronization is the next
active phase.

Accepted gates (independent of this document):

| Phase | Status |
| --- | --- |
| P0 architecture/de-templating remediation (Chapters 13–24, D17–D23) | ACCEPTED |
| HA-A — Digest serialization and Python/Go parity | ACCEPTED |
| HA-B — Agent accounting and controller parity | ACCEPTED |
| HA-C — Evaluator attribution semantics | ACCEPTED |
| HA-D — English truth and lab presentation | ACCEPTED |
| HA-E — Bibliographic preservation | ACCEPTED |
| HA-F — Independent English technical acceptance | ACCEPTED (`HA_F_TECHNICAL_ACCEPTED`) |
| F09 — Ancient-world narrative register | ACCEPTED (`F09_ACCEPTED`) |
| English source-stability audit and pre-freeze revisions | ACCEPTED |
| Final English freeze (technical-truth corrections + British-English normalization) | ACCEPTED (`ENGLISH_SOURCE_FROZEN`) |

The canonical English source is **frozen for F01 semantic Persian
synchronization**. English content work is closed unless fresh live evidence
proves a regression.

**Repository:** `/home/mehdi/Project/leela/tahmures`.
**Live HEAD:** `f97f9298ac153e222aea8106049fb24b965ea488`.
Substantial P0 and accepted remediation work remains uncommitted. A clean
checkout of HEAD would omit it. Preserve tracked modifications and untracked
files; do not reset, clean, stash, or replace the working tree.

Rechecked at English freeze (2026-10-01):

- All non-F01 gates pass: formatting, lint, Python/Go tests (excluding
  known F01 translation failures), chapter and continuity validation,
  offline experiments, Python/Go parity, strict English and Persian MkDocs
  builds.
- Current Python state at freeze: **28 failed, 752 passed**, classified as
  26 `F01_STALE_SOURCE` + 2 `F01_FIXTURE_COLLATERAL`, 0
  `NON_F01_REGRESSION`.
- **All 24 English/Persian source relationships are stale** (the English
  sources changed under accepted P0/HA/F09/freeze work; hashes were
  deliberately never refreshed).
- Interpretation: `NON_F01_GATES_PASS`; the full repository gate remains red
  solely because F01 is unresolved.

Do not change this state by refreshing hashes. F01 must perform semantic
synchronization first.

**Historical-record warning:** `editorial/high-assurance-decisions.md` records
HA-A and still labels HA-B/HA-C pending. Those status statements are outdated;
the owner accepted all three. Do not use historical report wording to revoke
acceptance or treat reports as runtime evidence.

Canonical references:

- `AGENTS.md` and its referenced RTK instructions
- `book/project-charter.md`
- `meta-prompt.md`
- `book/narrative-continuity.md`
- `book/fa/translation-glossary.md`
- `editorial/review-status.yml` and `editorial/fa-review/` for Persian work

No `project_context.md` exists. Do not invent missing rules.

## 2. Completed work

### HA-A — ACCEPTED

Supported JSON arguments serialize equivalently in Python and Go. Python
remains canonical. Unsupported, nonfinite and unserializable arguments fail
explicitly; the empty-byte digest fallback is removed. Approval semantics are
unchanged: the digest binds **action + arguments only**.

Regression anchors:

- `examples/shared/approval_digest_cases.json`
- `examples/python/tests/test_approval_serialization.py`
- `examples/go/tahmures/approval_serialization_test.go`

The supported argument root is a nonnull object with string keys. Nested values
are supported JSON-domain values. Integer and floating-point kinds remain
significant (`1` and `1.0` differ); Go decoding must preserve them where required.
Refer to the live implementation and HA-A record for serialization/error details.

### HA-B — ACCEPTED

Negative resource increments are rejected. Budgets are checked before
accumulation, overflow is prevented, and rejected counters are preserved.
Python/Go parity was verified. Completion evidence remains outside RunController.

Regression anchors:

- `examples/shared/agent_controller_cases.json`
- `examples/python/tests/test_agent_accounting.py`
- `examples/go/tahmures/agent_accounting_test.go`

### HA-C — ACCEPTED

`version_attribution` returns 1.0 for valid exact changed-dimension string sets,
otherwise 0.0. Missing dimensions, false extras and malformed attribution fail.
Ordering and duplicate strings are immaterial. Public metric keys, diagnostic
formatting and unrelated evaluator behavior, including `finding_recall`, remain
unchanged.

Regression anchors:

- `examples/shared/version_attribution_cases.json`
- `examples/python/tests/test_version_attribution.py`
- `examples/go/tahmures/version_attribution_test.go`

### HA-D — ACCEPTED

English truth and lab presentation corrections (F02, F04, F05, F08, X01)
were implemented in Chapters 19–22 and independently accepted. The original
finding list is preserved below under §4 as historical record.

### HA-E — ACCEPTED

Bibliographic preservation (F10) was implemented: the canonical BM25 and
Foundations and Trends titles were restored in
`book/fa/part-2/12-context-windows-and-attention.md`, with reference-parity
regression protection. Historical detail is preserved in §4.

### HA-F — ACCEPTED (`HA_F_TECHNICAL_ACCEPTED`)

Independent English technical acceptance completed (read-only, GPT-owned).
Separate inherited bilingual debt from English defects. Subsequent
narrative-register and freeze gates built on this acceptance.

### Post-HA gates — ACCEPTED

- **F09** (`F09_ACCEPTED`): ancient-world narrative register work, including
  the Chapter 08 tale and the Chapter 21 surgical correction.
- **English source-stability audit** and **pre-freeze revisions**: whole-book
  architecture re-audit, bounded technical-truth and copy corrections
  (evidence: `.zcode/english-source-stability-audit.md`,
  `.zcode/english-source-pre-freeze-revision.md`).
- **Final English freeze** (`ENGLISH_SOURCE_FROZEN`): Chapter 18 hand-off
  technical-truth corrections, British-English normalization across the
  manuscript (evidence: `.zcode/english-freeze-final-revision.md`,
  `.zcode/english-freeze-british-cleanup.md`).

Do not modify accepted implementations or the frozen English source.

## 3. Final owner decisions

| Decision | Fixed constraint |
| --- | --- |
| D24 — Approval binding | Digest binds action + arguments only. Request ID, principal, scopes, effect and expiry are not digest-bound. Identity, required scopes, effect classification and supplied approval records are trusted application inputs. |
| D25 — Completion evidence | Orchestration validates evidence, emits `complete`, then RunController applies the transition. No controller evidence validation. |
| D26 — Resource validation | Reject negative increments while preserving existing state-machine semantics. |
| D27 — Attribution | Exact changed-dimension set agreement; malformed attribution fails. Preserve public metric keys. |
| D28 — Capstone | Chapter 24 remains a design/architecture capstone. No integrated runtime. |
| D29 — Serialization | Python canonical for supported valid JSON arguments; Go parity required. Unsupported, nonfinite and unserializable values fail explicitly. |

Scopes use **exact membership**, without wildcard expansion. Reopen a decision
only for demonstrated material repository contradiction; report it to the owner
rather than silently choosing new policy.

## 4. Remaining roadmap — SUPERSEDED (historical record)

> The sections below are the original HA-D/HA-E/HA-F roadmap as written before
> those batches were implemented and accepted. They are retained as history.
> HA-D, HA-E and HA-F are all **ACCEPTED**; nothing in this section remains
> pending. The only remaining roadmap item is **F01 Persian synchronization**
> (see §5).

### HA-D — English truth and lab presentation

Prospective edit allow-list:

- `book/part-4/19-evaluation-and-rubrics.md`
- `book/part-4/20-regression-testing-for-prompted-systems.md`
- `book/part-4/21-prompt-injection-and-trust-boundaries.md`
- `book/part-4/22-approvals-capabilities-and-consequential-action.md`

Required corrections:

- **F02:** Correct relabelling predictions. Changing both request and approval
  IDs while retaining action/arguments can remain allowed. Distinguish unmatched
  approval records from digest mismatches.
- **F04:** Explain trusted application preconditions without strengthening the
  authorizer. Empty requested scopes and caller-supplied read classification
  do not independently establish authenticated identity or required authority.
- **F05:** Correct the `storehouse:*` exercise. It does not grant
  `storehouse:write` under exact membership.
- **F08:** Classify every relevant fence as `RUNNABLE_LAB`,
  `INTEGRATION_FRAGMENT`, or `PSEUDOCODE`. Identify surrounding inputs/hooks,
  including `queue_for_human_review`, regression inputs, `records`/`policy`,
  and the Chapter 21 `modelContext` consumer.
- **X01:** Correct the claim that governed metrics reach 1.0 on both.
  Accuracy targets 1.0; unauthorized execution targets 0.0.

Use local corrections. Preserve tales and architecture. Do not add substantial
setup when explicit integration-fragment context is sufficient.

### HA-E — Bibliographic preservation

**F10:** Restore these exact canonical titles in
`book/fa/part-2/12-context-windows-and-attention.md`:

- `The Probabilistic Relevance Framework: BM25 and Beyond`
- `Foundations and Trends in Information Retrieval`

Current corruption includes `The Probabilistic ارتباط` and
`Information بازیابی`. Compare the complete spans with canonical English.

Add focused regression protection. The existing
`scripts/validate_reference_parity.py` checks recognizable citation identities;
it does not enforce these exact title spans. Specify the smallest validator/test
change in the HA-E plan before implementation; do not build a parallel framework.

This is a narrow bibliography exception to deferred Persian work. Do not
translate other passages, refresh hashes, or change review status.

### HA-F — Independent English technical acceptance

Read-only; owned by GPT-6, independently of the implementing GLM agent.

Verify exact manuscript examples, code/prose correspondence, adversarial cases,
complete Python/Go outputs, experiments, evaluator/approval/agent semantics,
preservation and all validation gates. Separate inherited bilingual debt from
English defects.

Return **PASS** or **REVISION_REQUIRED**. GLM's implementation report cannot
substitute for independent acceptance. Do not edit during this phase.

## 5. Execution order — SUPERSEDED (historical record)

> The original order below (HA-D → HA-E → HA-F) completed and was accepted.
> Post-HA work also completed and was accepted: F09, the English
> source-stability audit and revisions, and the final English freeze
> (`ENGLISH_SOURCE_FROZEN`).

**Current execution position:**

1. **NEXT — F01:** semantic Persian synchronization against the frozen
   English source (all 24 chapter pairs stale; see §1 measurements). Batching
   and sequencing require owner authorization before execution.
2. Post-F01: renewed human review where required (Persian Chapters 01–09
   retain historical `human_reviewed` evidence, but that evidence does not
   certify equivalence to the newly frozen English sources — renewed
   bilingual review is required after targeted resynchronization).
3. Post-F01: final bilingual validation; later publication gates.

Original (completed) order, retained as history:

**HA-D plan → owner approval → implementation → independent verification →
HA-E plan → owner approval → implementation → independent verification → HA-F.**

Advance only after the required gate. Do not automatically begin another batch.

**F01:** Keep bilingual debt visible. Do not translate, refresh source hashes,
or mark human reviewed outside F01. Semantic synchronization now targets the
frozen canonical English source; expose structural/fence debt as well as
stale hashes.

**F09:** COMPLETE (`F09_ACCEPTED`). Tales are preserved. Any future English
narrative edit would reopen the freeze and require owner authorization.

## 6. Constraints and validation

Before each batch:

1. Inspect HEAD, status, tracked diffs and untracked files.
2. Record a revision-bound working-tree baseline.
3. Reproduce relevant findings against exact inputs.
4. Produce a bounded plan and obtain implementation approval where required.

During implementation:

- Make the smallest approved change; no unrelated cleanup or new strategy.
- Preserve unrelated modifications, accepted P0 architecture and HA-A/HA-B/HA-C.
- Preserve tales, titles/slugs/navigation, chapter headings/front matter,
  citation identities and unaffected fences.
- Do not alter contracts, add features, redesign experiments or weaken validators.
- Do not refresh hashes or promote machine work to `human_reviewed`.
- Preserve Persian Chapters 01–09 and the machine/human review distinction.
- Do not commit, push, tag, publish or invoke external providers.

After each logical batch, inspect the actual diff, verify preservation and run
focused checks. After implementation report:

- Files changed and finding-to-file mapping
- Exact reproductions and behavior/prose differences
- Tests and validators, including all failures
- Revision-bound preservation evidence
- Remaining debt and unexpected discoveries

Use the existing virtual environment. Prefix shell commands with `rtk` as
required by the repository's referenced instructions. Principal validation:

```bash
rtk proxy make check PYTHON=.venv/bin/python
```

If the gate stops early, expose the remaining gates:

```bash
rtk proxy make -k check PYTHON=.venv/bin/python
```

Report every failure. Do not hide coverage/fence debt behind the first stale
hash or claim full readiness while required gates remain unresolved. Human and
external publication signoffs cannot be supplied by a machine pass.

## 7. First recommended prompt for GLM 5.3 — SUPERSEDED (historical record)

> The HA-D planning prompt below is retained verbatim as history; HA-D is
> complete and accepted. Do not execute it.
>
> The recommended next prompt is an **F01 planning prompt** (MODE = PLAN,
> F01 batching only, no edits), to be drafted and authorized by the owner
> separately. It should draw its debt measurement from the frozen-English
> baseline (28 failed / 752 passed; all 24 pairs stale) and the F01 readiness
> map in `.zcode/english-source-stability-audit.md`, re-verified against the
> live repository before execution. Do not begin F01 without explicit owner
> authorization.

```text
MODE = PLAN
Agent = GLM 5.3
Batch = HA-D only

Prepare the bounded implementation plan for the existing approved HA-D
roadmap. Do not edit files. Stop after presenting the plan for approval.

Prerequisites:
- Read AGENTS.md and its RTK instructions, book/project-charter.md,
  meta-prompt.md and book/narrative-continuity.md.
- Inspect live HEAD, git status, tracked diffs and untracked files.
- Preserve the dirty working tree. HEAD alone omits accepted work.
- HA-A, HA-B and HA-C are owner-accepted.
- editorial/high-assurance-decisions.md has historical pending-status
  wording; do not reinterpret it as revoking acceptance.

Findings:
F02, F04, F05, F08 and X01 only.

Prospective allowed edit files:
book/part-4/19-evaluation-and-rubrics.md
book/part-4/20-regression-testing-for-prompted-systems.md
book/part-4/21-prompt-injection-and-trust-boundaries.md
book/part-4/22-approvals-capabilities-and-consequential-action.md

All other files are forbidden for modification.
Within allowed files, preserve tales, front matter, headings, titles,
navigation, citation identities and unaffected fences.

Fixed truths:
- Approval digest binds action + arguments only.
- Identity, required scopes, effect classification and approval-record
  provenance are trusted application responsibilities.
- Request-ID filtering is distinct from digest binding.
- Scopes use exact membership; storehouse:* is not a wildcard grant.
- Completion evidence remains outside RunController.
- Chapter 24 remains a design capstone.
- No code, evaluator, experiment or architecture changes.

Required reproduction:
1. Execute the exact Chapter 22 base input.
2. Compare changing only approval request ID; changing both IDs while
   preserving action/arguments; and changing arguments while retaining
   the old digest. Record full authorization results.
3. Reproduce an allow-listed read with an unregistered principal and
   empty requested scopes; document the caller boundary truthfully.
4. Confirm storehouse:* does not grant storehouse:write.
5. Inventory relevant Python/Go fences in Chapters 19–21.
   Classify each as RUNNABLE_LAB, INTEGRATION_FRAGMENT or PSEUDOCODE.
   Identify missing setup, hooks and consumers. Prefer explicit fragment
   context over large new setup.
6. Run:
   rtk proxy .venv/bin/python -m tahmures.cli run \
     --manifest experiments/manifests/ch22-approvals.json
   rtk proxy go run ./examples/go/cmd/tahmures run \
     --manifest experiments/manifests/ch22-approvals.json
   Confirm governed authorization_accuracy=1.0 and
   unauthorized_execution=0.0.

Plan deterministic acceptance:
- Every revised prediction matches its exact executed input.
- Binding claims match D24.
- No wildcard implication remains in the scoped exercise.
- Every relevant fence has honest classification and explicit context.
- Every fence labelled runnable executes with its stated setup.
- Metric direction and values match actual experiment output.
- Unaffected regions and all forbidden files remain unchanged.

Planned implementation validation:
Focused chapter/continuity checks, exact examples, both experiments,
strict documentation builds, make check, and make -k check if needed.
Report inherited F01 failures separately without changing hashes.

Output:
Baseline; reproduced evidence; finding-to-location mapping; exact proposed
corrections; fence classification/setup; allowed changes; preservation;
validation; translation debt; stop conditions.

Stop for material policy contradiction, unexplained baseline divergence,
or a required change outside the four files. Do not invent a resolution.
Do not start HA-E. No commits or external providers.

Finish:
PLAN_READY_FOR_OWNER_REVIEW
or
OWNER_DECISIONS_REQUIRED
```

TAHMURES_FULL_HANDOVER_READY
