# Tahmures Repository Guide

## Project

Tahmures is a bilingual, narrative-supported engineering book about prompt
engineering and reliable language-model systems.

- English Chapters 1–24 are complete drafts.
- Persian Chapters 1–24 are faithful translations of the canonical English
  manuscript.
- Python 3.12 is the canonical implementation.
- Go 1.26 must preserve equivalent observable behaviour.
- Experiments run offline with committed synthetic datasets and fixtures.
- `meta-prompt.md` is the editorial operating contract.
- `book/project-charter.md` is the approved project charter.

Do not add provider calls, deployment, commits, or pushes unless explicitly
requested.

## Important Paths

- `book/` — English manuscript and project documentation
- `book/fa/` — Persian RTL edition
- `book/narrative-continuity.md` — narrative source of truth
- `examples/python/tahmures/` — canonical Python contracts
- `examples/go/tahmures/` — behaviourally equivalent Go contracts
- `experiments/` — manifests, JSONL datasets, and recorded fixtures
- `prompts/versions/` — experiment prompt variants
- `scripts/` — validation, parity, experiment, and editorial automation
- `editorial/` — human editorial state, review findings, terminology candidates, and toolchain policy
- `.agents/skills/tahmures-editorial/` — project-local Codex editorial orchestrator
- `mkdocs.yml` and `mkdocs.fa.yml` — English and Persian sites

## Development Commands

Use the existing virtual environment when available:

```bash
make check PYTHON=.venv/bin/python
```

Useful narrower commands:

```bash
make lint PYTHON=.venv/bin/python
make test PYTHON=.venv/bin/python
make validate PYTHON=.venv/bin/python
make validate-translations PYTHON=.venv/bin/python
make experiments PYTHON=.venv/bin/python
make parity PYTHON=.venv/bin/python
make docs PYTHON=.venv/bin/python
make editorial-check PYTHON=.venv/bin/python
```

Format Python and Go with:

```bash
make format PYTHON=.venv/bin/python
```

## Manuscript Rules

Every completed English chapter must retain the heading order and front matter
defined in `meta-prompt.md`. Narratives must:

- Be original teaching fiction, clearly distinguished from the *Shahnameh*.
- Keep the ancient-world episode free of modern engineering jargon.
- Contain a chapter-specific failure with real consequences.
- Treat divs as capable and uncertain rather than simply evil.
- Show the actual failure owner, which may be the requirements, application,
  data, tool, evaluator, model, or human decision-maker.
- End with an explicit engineering bridge and a hook to the next chapter.

Update `book/narrative-continuity.md` whenever a chapter changes a recurring
character, object, location, world rule, development step, or hook.

English Chapters 7 onward require 3,500–5,500 prose words excluding front
matter and fenced code. Chapter narratives require 400–900 words.

## Persian Translation and Editorial Rules

The English manuscript is canonical for technical meaning. Do not change Persian
Chapters 1–24 unless translation or Persian editorial work is in scope.

When translating or editing Persian:

- Preserve executable Python, Go, Bash, and JSON fences byte-for-byte.
- Preserve source URLs, identifiers, paths, API names, manifest names, numerical
  values, units, and other protected technical tokens.
- Follow `book/fa/translation-glossary.md`.
- Follow `writing_persian_eng_books.md`.
- Read `editorial/fa-review/chapters-01-09.md`,
  `editorial/fa-review/terminology-candidates.yml`, and
  `editorial/fa-review/regression-cases.yml` when they exist.
- Update `source_sha256` only after the corresponding English source is final.
- Run `scripts/validate_translations.py` and the editorial validators.

### Persian review state

- Persian Chapters 01–09 have received human review and form the calibration
  corpus for Persian editorial quality.
- Persian Chapters 10–24 have not yet received human line-by-line review.
- The failure classes discovered in Chapters 01–09 must be checked proactively
  in Chapters 10–24.
- A machine pass may mark Chapters 10–24 as `machine_prechecked`; it must not
  describe them as `human_reviewed`.
- Human-approved Persian wording must not be replaced merely to make it closer to
  English sentence structure.

### Persian integrity requirements

A Persian sentence fails review if it is fluent but syntactically or semantically
malformed. Explicitly check:

- موصوف و صفت;
- مضاف و مضاف‌الیه and ezafe chains;
- adjective attachment and scope;
- adverb position and scope;
- subject, object, negation, condition, modality, comparison, and causality;
- mixed Persian/English noun phrases;
- natural Persian word order around retained English technical terms;
- reference/citation identity parity for shared canonical claims.

Text integrity, adjective correctness, and adverb correctness are mandatory quality
requirements, not optional stylistic preferences.

## External Codex Skills and Plugins

External skills are subordinate helpers. They never override this repository's
instructions, charter, continuity record, editorial policy, glossary, human review
state, code contracts, or deterministic validators.

Approved routing:

- `$academic-research-suite` — evidence discovery, fact checking, citation audit,
  primary-source research, and experiment/reproducibility review.
- `$scholarly-technical-writing` — technical-book review and explanation quality.
- `$book-drafting-editor` — revision planning and controlled manuscript editing.
- `$high-stakes-book-review` — selective deep review where evidence, safety, privacy,
  legal exposure, or reader harm warrants it.
- `$drawio` and `$drawio-academic-skills` — editable technical and publication figures.
- Zotero — bibliographic source-of-truth operations when connected.

Do not use external book-architecture or story-bible tools to create competing sources
of truth. `book/project-charter.md`, `book/narrative-continuity.md`, and
`meta-prompt.md` remain canonical.

## Editorial Validation

Run the editorial checks directly with:

```bash
.venv/bin/python scripts/editorial_check.py
```

or, after the root Makefile includes `editorial.mk`:

```bash
make editorial-check PYTHON=.venv/bin/python
```

Editorial validation includes reference identity parity, protected-content parity,
Persian regression checks, and review-state validation. Heuristic Persian warnings
must be inspected; known blocker/high-severity regression failures must be fixed.


## Code and Experiment Rules

- Keep experiment manifest schema version 1 backward-compatible.
- Use dependency-free educational implementations unless a dependency change
  is explicitly approved.
- Preserve reason codes, deterministic ordering, report fields, tag summaries,
  and diversity metrics across Python and Go.
- Add normal, boundary, malformed, and adversarial tests for new contracts.
- Do not claim fixture results demonstrate universal model behaviour.
- Enforce identity, permissions, budgets, state transitions, and irreversible
  actions in deterministic application code rather than prompt prose.

## Acceptance

Before handing off implementation work, run:

```bash
make check PYTHON=.venv/bin/python
```

This must pass formatting, Python and Go tests, chapter and continuity
validation, Persian synchronization, editorial validation, all offline
experiments, cross-language parity, and both strict MkDocs builds.
