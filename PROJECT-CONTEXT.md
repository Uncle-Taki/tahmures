# Project Context — Tahmures

This document gives a language model (or a new contributor) complete working
context for the Tahmures repository in a single reading. It describes what the
project is, which skills and tools operate on it, the full directory tree, and
the rules for working here. It is a summary layer only: the canonical,
normative documents are listed in Section 5, and where this file and those
documents disagree, those documents win.

## 1. What This Project Is

**Tahmures — *The Art and Engineering of Speaking with Intelligent
Machines*** is a bilingual, narrative-supported engineering book about prompt
engineering and reliable language-model systems, written by Mehdi Khoshtinat.
Content is licensed CC BY 4.0; code is Apache-2.0.

### Topic and thesis

The book teaches working developers — people who can read and modify code,
use a CLI, and understand basic HTTP/JSON, with no ML theory or prior
prompt-engineering experience assumed — how to build dependable systems on
top of language models. Its core thesis: a failure is rarely just "bad prompt
wording". Before rewording anything, diagnose the true owner of the failure
among requirements, prompt, model, context, retriever, application, tool,
dataset, evaluator, security boundary, and human decision. Language is an
interface; reliability comes from explicit requirements, structured data,
deterministic controls, evaluation, and accountable humans — with prompting
recognised as only one control among many.

### Narrative approach

Every chapter opens with an original short story ("episode") set in the
legendary world of Tahmures the Div-Binder, drawn from Iranian epic
tradition but explicitly **original teaching fiction, not a translation or
adaptation of the *Shahnameh***. The story presents the chapter's engineering
problem before any technical vocabulary appears, then transitions via a
"From Tale to Engineering" bridge. Divs are analogues for language models:
capable, uncertain, literal, occasionally deceptive, and not reliably
aligned. Across the book, Tahmures develops from commander to investigator
to experimenter to system designer to guardian and teacher. Recurring
characters (First Scribe, Keeper of Scripts, Archivist, Gatekeeper,
Messenger), objects (the experiment ledger, the stopping bell, the
Whispering Tablet), and locations are tracked in
`book/narrative-continuity.md`, the narrative source of truth.

### Chapter rhythm

Each chapter follows a fixed contract defined in `meta-prompt.md`: front
matter, then Learning Objectives → The Tale of Tahmures (five subsections:
Setting, Request, Unexpected Result, Discovery, From Tale to Engineering) →
The Engineering Problem → Mental Model → Core Concepts → Prompt Pattern →
Naive Attempt → Failure Analysis → Improved Design → Worked Example →
Experiment → Evaluation → Implementation Lab (Python and Go subsections) →
Failure Modes → Security Considerations → Operational Considerations →
Trade-Offs → When Prompting Is Not the Answer → Exercises → Chapter Summary
→ The Next Tale (a hook to the following chapter) → Citations and Further
Reading. Chapter narratives run 400–900 words; Chapters 7 onward require
3,500–5,500 prose words excluding front matter and fenced code.

### Bilingual structure

- **English is canonical** for technical meaning, written in **British
  English**. All 24 chapters (Parts I–IV, 6 chapters per part) are complete.
- **Persian** (`book/fa/`) is a faithful editorial translation in
  contemporary Iranian Persian with English-heavy developer terminology,
  published as a right-to-left edition with a one-to-one filename mapping to
  the English manuscript. It is governed by `writing_persian_eng_books.md`
  and `book/fa/translation-glossary.md`.

| Part | Site-nav title (English) | Site-nav title (Persian) | Chapters |
| --- | --- | --- | --- |
| I | Language, Intent, and Reliable Instructions | زبان، نیت و دستورهای قابل‌اعتماد | 1–6 |
| II | Prompt Design and Controlled Generation | طراحی پرامپت و تولید کنترل‌شده | 7–12 |
| III | Context, Memory, Tools, and Agents | Context، حافظه، ابزارها و Agentها | 13–18 |
| IV | Evaluation, Security, and Production | ارزیابی، امنیت و محیط عملیاتی | 19–24 |

Part naming exists in three layers: the site navigations (`mkdocs.yml`,
`mkdocs.fa.yml`) carry the newer reader-facing titles above;
`editorial/part-titles.yml` holds the same naming as an editorial proposal;
and the part-index front matter (`book/part-N/index.md`,
`book/fa/part-N/index.md`) still carries the earlier charter-era titles
("Language, Intent, and Models" / "Designing Prompted Interactions" /
"Knowledge, Memory, and Action" / "Evaluation, Security, and Operations").
Internal `part-1`…`part-4` paths stay stable regardless of title wording.

1. What Is a Prompt?
2. Models, Meaning, and Uncertainty
3. Requirements Before Wording
4. Anatomy of a Reliable Prompt
5. Instruction Hierarchy and Conflict
6. Learning from Examples
7. Reusable Prompt Templates
8. Structured Outputs and Contracts
9. Decomposition and Workflows
10. Variance, Choice, and Control
11. Designing for Creativity
12. Context Windows and Attention
13. Context Engineering
14. Retrieval-Augmented Generation
15. Memory and State
16. Tools and Permissions
17. Agents and Termination
18. Hand-offs and Multi-step Systems
19. Evaluation and Rubrics
20. Regression Testing for Prompted Systems
21. Prompt Injection and Trust Boundaries
22. Approvals, Capabilities, and Consequential Action
23. Production Operations and Drift
24. Beyond Prompting: Choosing the Right Control

### Engineering duality

The book's code is real and runs:

- **Python 3.12 is the canonical implementation**
  (`examples/python/tahmures/`): a dependency-free, provider-neutral
  experiment library (fixture client, manifests, runners, evaluators,
  contracts for templates, workflows, context, retrieval, memory, tools,
  agents, approvals, trust boundaries, regression, operations).
- **Go 1.26 (`examples/go/tahmures/`)** must preserve **equivalent
  observable behaviour** — schemas, reason codes, deterministic ordering,
  report fields, tag summaries, diversity metrics — not line-by-line
  translation. Cross-language parity is checked by `scripts/check_parity.py`.
- **All experiments run offline** against committed synthetic datasets
  (`experiments/datasets/`) and recorded fixtures
  (`experiments/fixtures/`), with no network calls, no paid model APIs, and
  no credentials. Prompt variants live in `prompts/versions/`, typically in
  contrasting good/bad pairs per chapter.
- Fixture results demonstrate behaviour on the committed data; the book must
  not claim they demonstrate universal model behaviour.

### Build and publication

Two strict MkDocs Material builds: `mkdocs.yml` (English, `docs_dir: book/`)
and `mkdocs.fa.yml` (Persian, `docs_dir: book/fa/`, inherits the English
config, RTL stylesheet, Vazirmatn font, tooltips, and an auto-appended
abbreviations snippet from `includes/fa-abbreviations.md`). Both must build
in strict mode as part of acceptance. Generated site output lands in
`site/` and is never edited directly.

## 2. Skills and Tooling Used

### Project-local skill: `tahmures-editorial`

`.agents/skills/tahmures-editorial/` is the repository's editorial
orchestrator — a **router, not a source of truth** — used for repository-level
book review, revision, bilingual parity, Persian quality, evidence audit,
terminology propagation, and final editorial gating. Key properties:

- **Authority precedence** (in repository-defined order): current user/task
  instruction → `AGENTS.md` → `book/project-charter.md` →
  `book/narrative-continuity.md` → `meta-prompt.md` →
  `writing_persian_eng_books.md` → `book/fa/translation-glossary.md` →
  `editorial/fa-review/*` → `editorial/review-status.yml`. External skills
  never override these files.
- **Mandatory preflight** before any edit: inspect `git status` and preserve
  unrelated user changes; read the target chapter and its counterpart
  completely; inspect code, manifests, fixtures, and prompt variants;
  establish the baseline validator state. "Do not rewrite first and inspect
  later."
- **English canonical pass** rules: preserve the chapter contract, British
  English, verify claims against committed artifacts, distinguish evidence
  from heuristic and opinion, provider neutrality, no stylistic churn.
- **Persian pass** rules: Persian is not a sentence-by-sentence copy of
  English; technical and factual meaning, actor/action/object relations,
  negation/condition/modality/comparison/causality, ezafe constructions,
  adjective and adverb attachment and scope, mixed Persian–English grammar,
  terminology consistency, bidi integrity, and protected tokens are all
  mandatory checks. Text, adjective, and adverb integrity are quality
  requirements, not stylistic preferences.
- **Human-review protection**: Persian Chapters 01–09 are the human-reviewed
  calibration corpus and must not be retranslated wholesale; Chapters 10–24
  may only be marked `machine_prechecked` by a machine pass, never
  `human_reviewed`.
- **Change discipline**: targeted changes only; no repository-wide
  cosmetic reformatting; no blind terminology replacement; no editing
  generated `site/` output; no altering code or experiments merely to make
  prose claims true; no commits or pushes unless explicitly requested.
- **Completion**: run narrow tests while editing, then
  `scripts/editorial_check.py`, then `make check PYTHON=.venv/bin/python`,
  inspect the final diff, and report unresolved issues honestly.

Its `references/workflow.md` defines the end-to-end editorial sequence
(Phases A–I: baseline validation → book-architecture audit → evidence audit
→ English canonical review → Persian calibration → Persian propagation in
batches → terminology promotion → visual audit → final gates), and
`references/gates.md` defines the seven acceptance gates (repository
integrity, technical integrity, evidence integrity, English editorial
integrity, Persian syntactic/semantic integrity, human-review integrity,
deterministic validation — "a model's confidence cannot substitute for a
failing deterministic gate").

### External Codex skills (routing from `AGENTS.md`)

External skills are subordinate helpers; they never override this
repository's instructions, charter, continuity record, editorial policy,
glossary, human review state, code contracts, or deterministic validators.

| Skill | Used for |
| --- | --- |
| `$academic-research-suite` | Evidence discovery, fact checking, citation audit, primary-source research, experiment/reproducibility review |
| `$scholarly-technical-writing` | Technical-book review and explanation quality |
| `$book-drafting-editor` | Revision planning and controlled manuscript editing before broad changes |
| `$high-stakes-book-review` | Selective deep review where evidence, safety, privacy, legal exposure, or reader harm warrants it |
| `$drawio` / `$drawio-academic-skills` | Editable technical and publication figures, only when a figure materially improves engineering comprehension |
| Zotero | Bibliographic source-of-truth operations when connected; never fabricate records, citation keys, DOIs, or quotations |

External book-architecture or story-bible tools must not be used to create
competing sources of truth; `book/project-charter.md`,
`book/narrative-continuity.md`, and `meta-prompt.md` remain canonical.

The external toolchain is pinned and documented in
`editorial/toolchain-lock.md` (active Codex home `$HOME/.codex-gpt-3`),
installed by `scripts/install_codex_gpt3_tools.sh` and verified by
`scripts/verify_codex_gpt3_tools.sh`.

### Validation and automation scripts (`scripts/`)

| Script | Purpose |
| --- | --- |
| `editorial_check.py` | Runs the full editorial quality-gate suite (orchestrates the `validate_*` scripts) |
| `_editorial_common.py` | Shared helpers: fenced-code regex, URL/DOI regexes, chapter pairing and selection |
| `check_parity.py` | Runs both Python and Go CLIs over every manifest and compares aggregate JSON reports |
| `run_all_experiments.py` | Runs every committed manifest (ch01–ch24) with the offline fixture client |
| `run_experiment.py` | Thin entry point delegating to the canonical Python CLI |
| `validate_chapters.py` | Validates chapter front matter and mandatory heading order against the editorial contract |
| `validate_continuity.py` | Validates the narrative-continuity ledger (complete chapter sequence, unique episode titles) |
| `validate_translations.py` | Validates the Persian edition against English sources (titles, `source_sha256`, synchronisation) |
| `validate_reference_parity.py` | Validates English→Persian citation identity containment |
| `validate_protected_parity.py` | Verifies protected technical content (code fences, URLs, identifiers) is preserved byte-for-byte in Persian |
| `validate_fa_editorial.py` | Applies Persian editorial regression cases and heuristic warnings |
| `validate_editorial_status.py` | Validates `editorial/review-status.yml` review states for all 24 chapters |
| `install_codex_gpt3_tools.sh` / `verify_codex_gpt3_tools.sh` | Install and verify the approved external Codex skills |

### Build targets and CI

Run everything with the existing virtual environment:
`make check PYTHON=.venv/bin/python` (the acceptance gate: formatting, lint,
Python and Go tests, chapter and continuity validation, Persian
synchronisation, editorial validation, all offline experiments,
cross-language parity, and both strict MkDocs builds). Narrower targets:
`make lint|test|validate|validate-translations|experiments|parity|docs|editorial-check`,
each with `PYTHON=.venv/bin/python`. Formatting via `make format`.
Continuous integration (`.github/workflows/ci.yml`) runs `make check` on
Python 3.12 and Go 1.26 for pushes and pull requests.

## 3. Directory Tree

Exhaustive listing (320 files, 52 directories), excluding build and tooling
artifacts: `.git/`, `.venv/`, `site/` (generated MkDocs output),
`__pycache__/`, `.ruff_cache/`, `.pytest_cache/`, `.zcode/`, and
`*.egg-info/`.

```text
.
├── .agents/
│   └── skills/
│       └── tahmures-editorial/        # project-local editorial orchestrator skill
│           ├── SKILL.md
│           └── references/
│               ├── gates.md           # seven acceptance gates
│               └── workflow.md        # phases A–I editorial sequence
├── book/                              # ENGLISH MANUSCRIPT (MkDocs docs_dir) + project docs
│   ├── index.md                       # reader-facing landing page
│   ├── references.md                  # Chicago author-date citations
│   ├── project-charter.md             # approved charter (canonical)
│   ├── narrative-continuity.md        # narrative source of truth (canonical)
│   ├── part-1/                        # 6 chapters + index.md
│   │   ├── index.md
│   │   ├── 01-what-is-a-prompt.md
│   │   ├── 02-models-meaning-and-uncertainty.md
│   │   ├── 03-requirements-before-wording.md
│   │   ├── 04-anatomy-of-a-reliable-prompt.md
│   │   ├── 05-instruction-hierarchy-and-conflict.md
│   │   └── 06-learning-from-examples.md
│   ├── part-2/                        # 6 chapters + index.md
│   │   ├── index.md
│   │   ├── 07-reusable-prompt-templates.md
│   │   ├── 08-structured-outputs-and-contracts.md
│   │   ├── 09-decomposition-and-workflows.md
│   │   ├── 10-variance-choice-and-control.md
│   │   ├── 11-designing-for-creativity.md
│   │   └── 12-context-windows-and-attention.md
│   ├── part-3/                        # 6 chapters + index.md
│   │   ├── index.md
│   │   ├── 13-context-engineering.md
│   │   ├── 14-retrieval-augmented-generation.md
│   │   ├── 15-memory-and-state.md
│   │   ├── 16-tools-and-permissions.md
│   │   ├── 17-agents-and-termination.md
│   │   └── 18-hand-offs-and-multi-step-systems.md
│   ├── part-4/                        # 6 chapters + index.md
│   │   ├── index.md
│   │   ├── 19-evaluation-and-rubrics.md
│   │   ├── 20-regression-testing-for-prompted-systems.md
│   │   ├── 21-prompt-injection-and-trust-boundaries.md
│   │   ├── 22-approvals-capabilities-and-consequential-action.md
│   │   ├── 23-production-operations-and-drift.md
│   │   └── 24-beyond-prompting-choosing-the-right-control.md
│   └── fa/                            # PERSIAN RTL EDITION — mirrors English 1:1
│       ├── index.md
│       ├── translation-glossary.md    # Persian terminology glossary (normative for fa work)
│       ├── stylesheets/rtl.css
│       ├── javascripts/tooltips.js
│       ├── fonts/Vazirmatn-RD-Regular.woff2
│       ├── part-1/ … part-4/          # same 24 chapter filenames as English + index.md each
├── editorial/                         # human editorial state + toolchain policy
│   ├── README.md                      # editorial-system overview
│   ├── INSTALL.md                     # integrating the editorial package
│   ├── toolchain-lock.md              # pinned external Codex toolchain
│   ├── part-titles.yml                # proposed reader-facing part titles
│   ├── review-status.yml              # per-chapter Persian review state
│   └── fa-review/
│       ├── chapters-01-09.md          # human review findings, derived failure classes
│       ├── regression-cases.yml       # Persian regression cases for validate_fa_editorial.py
│       └── terminology-candidates.yml # contextual English-retention candidates
├── examples/
│   ├── python/
│   │   ├── tahmures/                  # CANONICAL Python 3.12 implementation
│   │   │   ├── __init__.py
│   │   │   ├── cli.py                 # command-line interface
│   │   │   ├── client.py              # offline fixture client
│   │   │   ├── runner.py              # experiment runner
│   │   │   ├── manifest.py            # schema_version 1 manifests
│   │   │   ├── types.py
│   │   │   ├── evaluators.py
│   │   │   ├── templates.py           # ch 7 prompt templates
│   │   │   ├── contracts.py           # ch 8 structured outputs
│   │   │   ├── workflow.py            # ch 9 decomposition
│   │   │   ├── controls.py            # ch 10 variance/choice
│   │   │   ├── context.py             # ch 13 context engineering
│   │   │   ├── retrieval.py           # ch 14 RAG
│   │   │   ├── memory.py              # ch 15 memory/state
│   │   │   ├── tools.py               # ch 16 tools/permissions
│   │   │   ├── agents.py              # ch 17 agents/termination
│   │   │   ├── handoffs.py            # ch 18 hand-offs
│   │   │   ├── rubrics.py             # ch 19 rubrics
│   │   │   ├── regression.py          # ch 20 regression testing
│   │   │   ├── trust.py               # ch 21 injection/trust boundaries
│   │   │   ├── approvals.py           # ch 22 approvals/capabilities
│   │   │   └── operations.py          # ch 23 production operations
│   │   └── tests/                     # 8 pytest files
│   │       ├── test_client.py
│   │       ├── test_evaluators.py
│   │       ├── test_manifest.py
│   │       ├── test_phase2_contracts.py
│   │       ├── test_phase3_contracts.py
│   │       ├── test_phase4_contracts.py
│   │       ├── test_runner_cli.py
│   │       └── test_translation_validator.py
│   └── go/
│       ├── cmd/tahmures/main.go       # Go CLI entry point
│       └── tahmures/                  # behaviourally equivalent Go 1.26 package
│           ├── agents.go
│           ├── approvals.go
│           ├── client.go
│           ├── context.go
│           ├── contract.go
│           ├── controls.go
│           ├── evaluator.go
│           ├── handoffs.go
│           ├── manifest.go
│           ├── memory.go
│           ├── operations.go
│           ├── regression.go
│           ├── retrieval.go
│           ├── rubrics.go
│           ├── runner.go
│           ├── template.go
│           ├── tools.go
│           ├── trust.go
│           ├── types.go
│           ├── workflow.go
│           ├── phase2_test.go
│           ├── phase3_test.go
│           ├── phase4_test.go
│           └── runner_test.go
├── experiments/                       # offline experiment assets, one set per chapter
│   ├── manifests/                     # ch01-prompt-roles.json … ch24-beyond-prompting.json (24)
│   ├── datasets/                      # ch01-prompt-roles.jsonl … ch24-beyond-prompting.jsonl (24, synthetic inputs)
│   └── fixtures/                      # ch01-prompt-roles.jsonl … ch24-beyond-prompting.jsonl (24, recorded responses)
├── prompts/
│   ├── final-book-review.md           # whole-book editorial review launch prompt
│   ├── persian-batch-review.md        # parameterised Persian batch-review prompt
│   └── versions/                      # 49 versioned prompt variants, contrasting pairs per chapter
│       ├── ch01-baseline.txt / ch01-explicit.txt
│       ├── ch02-baseline.txt / ch02-evidence-bound.txt
│       ├── ch03-baseline.txt / ch03-decision-brief.txt
│       ├── ch04-blended.txt / ch04-structured.txt
│       ├── ch05-concatenated.txt / ch05-resolved.txt
│       ├── ch06-biased-four-shot.txt / ch06-representative-four-shot.txt / ch06-rule-and-examples.txt
│       ├── ch07-unchecked-substitution.txt / ch07-typed-template.txt
│       ├── ch08-prose-catalogue.txt / ch08-json-contract.txt
│       ├── ch09-monolithic-mission.txt / ch09-checkpointed-workflow.txt
│       ├── ch10-single-answer.txt / ch10-generate-select.txt
│       ├── ch11-unconstrained-novelty.txt / ch11-explore-then-accept.txt
│       ├── ch12-tail-truncation.txt / ch12-priority-selection.txt
│       ├── ch13-concatenate-everything.txt / ch13-engineered-context.txt
│       ├── ch14-unscoped-retrieval.txt / ch14-scoped-retrieval.txt
│       ├── ch15-append-only-memory.txt / ch15-governed-memory.txt
│       ├── ch16-instruction-only-tools.txt / ch16-tool-gate.txt
│       ├── ch17-free-running-agent.txt / ch17-bounded-agent.txt
│       ├── ch18-conversational-handoff.txt / ch18-typed-handoff.txt
│       ├── ch19-preference-only.txt / ch19-anchored-rubric.txt
│       ├── ch20-single-case-fix.txt / ch20-regression-gate.txt
│       ├── ch21-concatenated-content.txt / ch21-typed-trust-boundary.txt
│       ├── ch22-verbal-restriction.txt / ch22-bound-capability.txt
│       ├── ch23-aggregate-only.txt / ch23-versioned-segments.txt
│       └── ch24-prompt-only.txt / ch24-mechanism-first.txt
├── scripts/                           # validation, parity, experiment, editorial automation
│   ├── __init__.py
│   ├── _editorial_common.py
│   ├── editorial_check.py
│   ├── check_parity.py
│   ├── run_all_experiments.py
│   ├── run_experiment.py
│   ├── validate_chapters.py
│   ├── validate_continuity.py
│   ├── validate_translations.py
│   ├── validate_reference_parity.py
│   ├── validate_protected_parity.py
│   ├── validate_fa_editorial.py
│   ├── validate_editorial_status.py
│   ├── install_codex_gpt3_tools.sh
│   └── verify_codex_gpt3_tools.sh
├── includes/
│   └── fa-abbreviations.md            # MkDocs abbreviations for the Persian build
├── fonts/
│   └── Vazirmatn-RD-Regular.woff2     # Persian font (also under book/fa/fonts/)
├── .github/workflows/ci.yml           # CI: make check on Python 3.12 + Go 1.26
├── tests/                             # empty (vestigial; real tests live in examples/python/tests)
├── AGENTS.md                          # repository guide for coding agents
├── README.md                          # human-facing overview and quick start
├── MANIFEST.md                        # sha256 manifest of generated editorial toolchain files
├── meta-prompt.md                     # editorial operating contract (canonical)
├── writing_persian_eng_books.md       # Persian engineering-book writing policy (normative for fa)
├── Makefile                           # root build; includes editorial.mk
├── editorial.mk                       # optional editorial-check and validate-* targets
├── mkdocs.yml                         # English site config (strict, Material)
├── mkdocs.fa.yml                      # Persian site config (inherits mkdocs.yml, RTL)
├── pyproject.toml                     # Python project, pytest/ruff config, pinned dev deps
├── go.mod                             # Go module
├── .python-version / .editorconfig / .gitignore
└── LICENSE-CODE / LICENSE-CONTENT.md  # Apache-2.0 code; CC BY 4.0 content
```

The `.zcode/` directory holds session-planning files for this coding agent,
is gitignored, and is not part of the book.

## 4. How to Work in This Repository

### Normative precedence

When documents conflict, repository-defined order applies (highest first):

1. the current user/task instruction;
2. `AGENTS.md`;
3. `book/project-charter.md`;
4. `book/narrative-continuity.md`;
5. `meta-prompt.md`;
6. `writing_persian_eng_books.md` (for Persian work);
7. `book/fa/translation-glossary.md`;
8. `editorial/fa-review/*`;
9. `editorial/review-status.yml`.

Material contradictions must be recorded, never silently resolved.

### Manuscript rules

- Completed chapters must retain the heading order and front matter from
  `meta-prompt.md`. Narratives must be original teaching fiction, keep the
  ancient-world episode free of modern engineering jargon, contain a
  chapter-specific failure with real consequences, treat divs as capable and
  uncertain rather than simply evil, show the actual failure owner, and end
  with an engineering bridge plus a hook to the next chapter.
- Update `book/narrative-continuity.md` whenever a chapter changes a
  recurring character, object, location, world rule, development step, or
  hook.

### Persian rules

- The English manuscript is canonical for technical meaning. Do not change
  Persian Chapters 1–24 unless translation or Persian editorial work is in
  scope.
- Preserve executable Python, Go, Bash, and JSON fences **byte-for-byte**;
  preserve source URLs, identifiers, paths, API names, manifest names,
  numerical values, and other protected technical tokens.
- Follow `book/fa/translation-glossary.md`, `writing_persian_eng_books.md`,
  and, when present, the `editorial/fa-review/` findings.
- Update `source_sha256` only after the corresponding English source is
  final.
- Persian Chapters 01–09 are `human_reviewed` (the calibration corpus);
  human-approved Persian wording must not be replaced merely to make it
  closer to English sentence structure. Chapters 10–24 are not yet
  human-reviewed; a machine pass marks them `machine_prechecked` at best,
  and the failure classes discovered in 01–09 must be checked proactively.
- A fluent Persian sentence still fails review if it is syntactically or
  semantically malformed — explicitly check noun–adjective agreement,
  ezafe chains, adjective/adverb attachment and scope, subject/object/
  negation/condition/modality/comparison/causality, mixed Persian–English
  noun phrases, and reference/citation identity parity.

### Code and experiment rules

- Keep experiment manifest schema version 1 backward-compatible; use
  dependency-free educational implementations; preserve reason codes,
  deterministic ordering, report fields, tag summaries, and diversity
  metrics across Python and Go; add normal, boundary, malformed, and
  adversarial tests for new contracts; never claim fixture results
  demonstrate universal model behaviour; enforce identity, permissions,
  budgets, state transitions, and irreversible actions in deterministic
  application code rather than prompt prose.

### Change discipline and acceptance

- Make targeted changes. No repository-wide cosmetic reformatting, no blind
  terminology replacement, no overwriting unrelated user changes, no
  editing `site/` output directly, no provider calls, and no commits or
  pushes unless explicitly requested.
- If prose and implementation disagree, determine which source is wrong; do
  not silently change code to match prose (or prose to match code) without
  establishing ground truth against the charter.
- Before handing off implementation work, run and pass:

  ```bash
  make check PYTHON=.venv/bin/python
  ```

  This covers formatting, Python and Go tests, chapter and continuity
  validation, Persian synchronisation, editorial validation, all offline
  experiments, cross-language parity, and both strict MkDocs builds.

## 5. Canonical Documents (Read Before Editing)

This file is a summary. The normative sources, in precedence order:

1. `AGENTS.md` — repository guide: paths, commands, acceptance criteria.
2. `book/project-charter.md` — approved charter: goals, scope, phases,
   security model, cultural integrity policy.
3. `book/narrative-continuity.md` — characters, locations, objects, world
   rules, episode table, hook chain.
4. `meta-prompt.md` — editorial operating contract: chapter contract,
   story contract, quality gate.
5. `writing_persian_eng_books.md` — Persian writing and editing policy.
6. `book/fa/translation-glossary.md` — Persian terminology.
7. `editorial/fa-review/*` — human review findings, regression cases,
   terminology candidates.
8. `editorial/review-status.yml` — per-chapter review state
   (`human_reviewed` / `machine_prechecked` / `unreviewed`).
