# Tahmures Editorial Workflow

## Phase A — Baseline

1. Read repository authority files.
2. Inspect `git status`.
3. Run baseline validators.
4. Record pre-existing failures.
5. Read review-state metadata.

## Phase B — Book architecture audit

Check:

- reader promise;
- four-part conceptual progression;
- learning dependencies;
- chapter overlap/gaps;
- narrative continuity;
- mandatory heading contract;
- part titles.

Do not move files merely to make thematic titles visible.

## Phase C — Evidence audit

For each chapter, classify claims:

- historical/literary;
- empirical;
- quantitative;
- current/product-specific;
- engineering heuristic;
- opinion/teaching simplification.

Use ARS/Zotero when available.

Prefer primary/authoritative sources for load-bearing claims.

## Phase D — English canonical review

For each English chapter:

1. technical correctness;
2. evidence support;
3. definition/order of concepts;
4. examples and experiment accuracy;
5. Python/Go correspondence;
6. evaluation logic;
7. security/operations claims;
8. adjectives/adverbs/modifier scope;
9. narrative bridge and continuity;
10. citations/further reading.

Make targeted edits.

## Phase E — Persian calibration

For Chapters 01–09:

- preserve human-approved wording;
- scan for residual known failure classes;
- verify citation identity parity;
- verify protected content;
- do not retranslate wholesale.

## Phase F — Persian propagation

For Chapters 10–24:

- apply all validated failure classes;
- review terminology contextually;
- fix syntax and semantic relations;
- preserve exact technical tokens;
- preserve citation support;
- mark only `machine_prechecked`.

Recommended batches: 10–12, 13–15, 16–18, 19–21, 22–24.

## Phase G — Terminology promotion

For each candidate:

1. inspect occurrences across the book;
2. determine concept/domain;
3. compare glossary precedent;
4. decide preserve/retain/translate/transliterate/review;
5. update the canonical glossary only when the decision is stable;
6. add regression coverage where needed.

## Phase H — Visual audit

Identify concepts that genuinely benefit from diagrams.

Prefer editable Draw.io sources.

Do not create new figures during a text-fix pass unless the task explicitly includes
figure creation.

## Phase I — Final gates

Run:

```bash
.venv/bin/python scripts/editorial_check.py
make check PYTHON=.venv/bin/python
```

Inspect the diff and report unresolved items.
