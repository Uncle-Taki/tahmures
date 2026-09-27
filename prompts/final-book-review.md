# Final Codex Prompt — Tahmures Whole-Book Editorial Review

## Launch

Start the project Codex with:

```bash
CODEX_HOME="$HOME/.codex-gpt-3" \
codex
```

Then run this task.

---

Use `$tahmures-editorial` as the orchestration workflow.

You are performing a **repository-level editorial, technical, evidence, bilingual, and
quality review of the entire Tahmures book** and are authorized to make safe,
well-supported changes to the repository within the rules below.

Do not merely return recommendations. Inspect the repository, make justified edits,
run the relevant validators/tests, inspect the final diff, and report what changed.

## 1. Authority and preflight

Before editing, read completely:

- `AGENTS.md`
- `README.md`
- `book/project-charter.md`
- `book/narrative-continuity.md`
- `meta-prompt.md`
- `writing_persian_eng_books.md`
- `book/fa/translation-glossary.md`
- `editorial/README.md`
- `editorial/toolchain-lock.md`
- `editorial/review-status.yml`
- `editorial/part-titles.yml`
- `editorial/fa-review/chapters-01-09.md`
- `editorial/fa-review/terminology-candidates.yml`
- `editorial/fa-review/regression-cases.yml`

Also inspect:

- `mkdocs.yml`
- `mkdocs.fa.yml`
- `Makefile`
- relevant validators under `scripts/`
- Python and Go examples;
- experiment manifests, datasets, fixtures, and prompt variants;
- current `git status` and diff.

Preserve unrelated user changes.

Repository instructions override external skills.

Do not commit, push, deploy, or add live provider calls unless explicitly requested.

## 2. Installed tools

Use installed tools only when they materially improve the task.

### ARS-Codex

Use `$academic-research-suite` for:

- evidence audit;
- current factual verification;
- primary-source discovery;
- historical/literary verification;
- empirical/quantitative claims;
- citation-quality audit;
- experiment/reproducibility review.

Do not let ARS silently rewrite chapters during evidence discovery.

If a source or claim cannot be verified, mark it unresolved or qualify the claim.
Never invent a source, quote, DOI, statistic, or bibliographic record.

### Zotero

Use Zotero when available for bibliography/source-of-truth operations.

Prefer verified existing records and citation keys.

If Zotero is unavailable, continue with repository sources and ARS/web verification,
but do not fabricate bibliography data.

### Writer Skills

Use `$scholarly-technical-writing` for technical-book quality and
`$book-drafting-editor` for revision planning when broad revision is needed.

Use `$high-stakes-book-review` only where evidence, security, privacy, legal exposure,
or reader harm warrants it.

External writer skills do not control chapter architecture, project charter, narrative
continuity, or Persian policy.

### Draw.io

Use `$drawio` / `$drawio-academic-skills` only when a missing or weak diagram is a
material pedagogical problem.

Do not create decorative figures just because the tools are installed.

If new figures are outside the practical scope of this pass, record figure candidates
instead of blocking text corrections.

## 3. Establish the baseline

Before modifications:

1. run `git status`;
2. run the current baseline `make check PYTHON=.venv/bin/python`;
3. run `.venv/bin/python scripts/editorial_check.py`;
4. record pre-existing failures separately.

Do not attribute pre-existing failures to your own changes.

## 4. Review the whole book architecture

Review all 24 English chapters and the four-part learning progression for:

- scope and reader promise;
- prerequisite ordering;
- overlap/repetition;
- missing conceptual bridges;
- chapter-to-chapter dependency;
- consistency with the approved project charter;
- narrative progression and continuity;
- mandatory chapter structure;
- evaluation/security/operations coverage.

The current internal directories `part-1`…`part-4` should remain stable.

Evaluate `editorial/part-titles.yml`.

If the proposed thematic titles are accurate and can be applied safely without
changing internal paths/slugs, update reader-facing navigation/index titles in both
English and Persian.

Do not rename directories/routes merely to achieve thematic naming.

## 5. English canonical review — Chapters 01–24

For every English chapter:

### Technical correctness

Check:

- definitions;
- mental models;
- system boundaries;
- prompt/system/application ownership;
- RAG, context, memory, tools, agents, hand-offs, evaluation, security, and production
  concepts;
- claims about model behavior;
- provider neutrality;
- deterministic-control recommendations.

Do not overstate universal behavior from fixtures or model-specific examples.

### Evidence

Classify load-bearing statements as:

- empirical;
- quantitative;
- historical/literary;
- current/product-specific;
- engineering heuristic;
- opinion/teaching simplification.

Use ARS/Zotero/authoritative sources when support is needed.

Prefer primary sources for important technical claims and reliable scholarly/primary
sources for Tahmures/Shahnameh historical or literary claims.

Ensure `Citations and Further Reading` actually supports the chapter.

### Code and experiments

Cross-check chapter descriptions with:

- `examples/python/`
- `examples/go/`
- tests;
- `experiments/manifests/`
- datasets;
- fixtures;
- `prompts/versions/`

Python is canonical. Go must preserve equivalent observable behavior where required.

Do not change code merely to make prose claims true. Determine which side is wrong.

### English prose integrity

Correct when needed:

- ambiguity;
- vague referents;
- adjective attachment/scope;
- adverb attachment/scope;
- inflated or imprecise prose;
- unnecessary absolutes;
- inconsistent terminology;
- broken causal relations;
- unclear examples.

Use British English consistently.

Avoid stylistic churn when prose is already clear and technically correct.

### Narrative

Preserve:

- original teaching-fiction status;
- cultural integrity;
- continuity;
- chapter-specific conflict;
- actual failure owner;
- engineering bridge;
- next-chapter hook.

Update `book/narrative-continuity.md` only when an actual continuity state changes.

## 6. Persian Chapters 01–09 — calibration protection pass

These chapters have received human review.

Do **not** retranslate them wholesale.

Treat existing human-approved Persian as authoritative unless there is a concrete:

- factual;
- technical;
- grammatical;
- terminology;
- reference;
- link/anchor;
- or later-explicit-instruction reason to change it.

Audit them for any remaining:

- known regression case;
- citation identity mismatch;
- protected-content mismatch;
- adjective/adverb scope issue;
- ezafe problem;
- mixed English/Persian grammatical problem;
- untranslated term that lacks justified retention/explanation.

Preserve the author's existing manual improvements.

## 7. Persian Chapters 10–24 — propagate solutions from 01–09

These chapters have **not** yet received human line-by-line review.

Apply all validated failure classes discovered in Chapters 01–09.

For every chapter explicitly review:

### Semantic integrity

Preserve:

- actor;
- action;
- object;
- causality;
- negation;
- condition;
- modality;
- uncertainty;
- comparison;
- quantity;
- limitation.

### Persian syntax

Check carefully:

- موصوف و صفت;
- مضاف و مضاف‌الیه;
- ezafe chains;
- head/modifier order;
- adjective attachment and scope;
- adverb position and scope;
- pronoun/reference clarity;
- coordination/list parallelism;
- compressed English noun phrases;
- natural Persian word order.

The integrity of adjectives and adverbs is a high-priority requirement.

A sentence that sounds fluent but has incorrect modifier scope or semantic relations
must be corrected.

### Mixed English/Persian terminology

Use `editorial/fa-review/terminology-candidates.yml` as a candidate registry, not a
blanket whitelist.

For each occurrence decide contextually:

- `PRESERVE_EXACT`
- `RETAIN_ENGLISH`
- `TRANSLATE_PERSIAN`
- `TRANSLITERATE_PERSIAN`
- `REVIEW`

Retained English must still live inside natural Persian grammar.

Preserve literal fields, identifiers, APIs, commands, paths, syntax, and other exact
technical tokens exactly.

Use the existing tooltip mechanism for retained English prose terms when required.

Do not perform blind global search-and-replace.

### Review state

After a successful machine/editorial pass, Chapters 10–24 may be recorded as:

```text
machine_prechecked
```

They must remain:

```text
human_reviewed: false
```

until the author reviews them.

Update `editorial/review-status.yml` only to reflect work actually performed.

## 8. Reference parity

Investigate the current problem that Persian references may be fewer than English.

For shared canonical claims, preserve the supporting citation identity.

Compare:

- URLs;
- DOI identifiers;
- citation keys;
- stable reference identities.

Do not merely equalize counts.

Persian may retain justified additional references.

If the English/Persian claim sets differ, resolve the claim difference before forcing
citation parity.

Run:

```bash
.venv/bin/python scripts/validate_reference_parity.py
```

## 9. Terminology promotion

Review the candidate registry across the entire Persian manuscript.

Do not automatically retain every candidate in English.

When a term's book-wide decision becomes stable:

1. verify actual context across chapters;
2. resolve domain/role ambiguity;
3. update `book/fa/translation-glossary.md`;
4. keep exact identifiers separate from terminology decisions;
5. add or update regression coverage when useful.

## 10. Regression learning

When you find a new issue that generalizes beyond one sentence:

- add a regression case;
- preserve exact bad wording;
- preserve the approved correction if high-confidence and supported;
- use `flag_only` when context is required;
- never encode an ambiguous automatic rewrite.

Do not delete existing human regression cases unless they are demonstrably wrong.

## 11. Validation during work

Use narrow validation while editing.

At minimum run:

```bash
.venv/bin/python scripts/validate_reference_parity.py
.venv/bin/python scripts/validate_protected_parity.py
.venv/bin/python scripts/validate_fa_editorial.py
.venv/bin/python scripts/validate_editorial_status.py
.venv/bin/python scripts/validate_translations.py
```

Then:

```bash
.venv/bin/python scripts/editorial_check.py
```

Finally:

```bash
make check PYTHON=.venv/bin/python
```

Do not claim completion if required deterministic gates fail because of your changes.

If there are pre-existing failures that are outside scope, distinguish them clearly.

## 12. Change discipline

Make targeted changes.

Do not:

- rewrite all prose for stylistic variety;
- alter technically correct code without necessity;
- edit generated `site/` files directly;
- create a second glossary;
- create a second narrative continuity system;
- create a second project charter;
- replace human corrections with literal translation;
- add unverified citations;
- silently strengthen uncertain claims;
- perform mass terminology replacement;
- commit or push.

## 13. Final review

Before finishing:

1. inspect `git diff --check`;
2. inspect the complete diff;
3. verify no unrelated files changed;
4. verify Chapters 01–09 human-approved wording was protected;
5. verify Chapters 10–24 were not falsely labelled human-reviewed;
6. verify citation parity results;
7. verify protected content;
8. verify terminology consistency;
9. verify English/Persian navigation and thematic part titles if changed;
10. run final `make check`.

## 14. Final response

Return a concise but complete report containing:

- English chapters changed;
- Persian chapters changed;
- major technical corrections;
- evidence/citation changes;
- reference parity corrections;
- Persian syntax/modifier/adverb corrections;
- terminology decisions promoted to the glossary;
- unresolved terminology;
- unresolved evidence;
- thematic part-title changes;
- diagrams created or figure candidates;
- code/experiment changes, if any;
- regression cases added;
- Chapters newly marked `machine_prechecked`;
- validation commands run;
- final validation status;
- pre-existing failures that remain.

Do not paste full chapters into the response.
