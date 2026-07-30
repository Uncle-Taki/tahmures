# Tahmures Repository Guide

## Project

Tahmures is a bilingual, narrative-supported engineering book about prompt
engineering and reliable language-model systems.

- English Chapters 1–18 are complete drafts.
- Persian Chapters 1–12 are faithful translations of the canonical English
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
- `scripts/` — validation, parity, and experiment automation
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

## Persian Translation Rules

The English manuscript is canonical. Do not change Persian Chapters 1–12
unless translation work is in scope.

When translating:

- Preserve executable Python, Go, Bash, and JSON fences byte-for-byte.
- Preserve source URLs, identifiers, paths, API names, and manifest names.
- Follow `book/fa/translation-glossary.md`.
- Update `source_sha256` only after the corresponding English source is final.
- Run `scripts/validate_translations.py`.

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
validation, Persian synchronization, all offline experiments, cross-language
parity, and both strict MkDocs builds.
