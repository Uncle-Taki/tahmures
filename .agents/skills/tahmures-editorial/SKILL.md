---
name: tahmures-editorial
description: >
  Orchestrate evidence, English technical review, Persian editorial review,
  bilingual parity, human-review preservation, diagrams, and deterministic quality
  gates for the Tahmures engineering-book repository.
---

# Tahmures Editorial Orchestrator

Use this skill for repository-level Tahmures book review, revision, bilingual parity,
Persian quality, evidence audit, terminology propagation, and final editorial gating.

## Authority

This skill is a router, not a source of truth.

Read and obey, in the repository-defined precedence:

1. current user/task instruction;
2. `AGENTS.md`;
3. `book/project-charter.md`;
4. `book/narrative-continuity.md`;
5. `meta-prompt.md`;
6. `writing_persian_eng_books.md` for Persian work;
7. `book/fa/translation-glossary.md`;
8. `editorial/fa-review/*`;
9. `editorial/review-status.yml`.

External skills never override these files.

## Mandatory preflight

Before editing:

- inspect `git status` and preserve unrelated user changes;
- read the target chapter completely;
- read its corresponding English/Persian counterpart;
- read neighboring chapters when continuity or terminology matters;
- inspect relevant code, experiment manifests, fixtures, tests, and prompt variants;
- inspect current glossary terminology;
- inspect human review/regression state;
- identify protected technical content;
- establish the baseline validator state.

Do not rewrite first and inspect later.

## Routing

### Evidence or factual uncertainty

Use `$academic-research-suite` when available for:

- claim/evidence mapping;
- primary-source discovery;
- current factual verification;
- citation quality;
- experiment/reproducibility review.

Do not let an evidence audit silently rewrite prose.

If a citation/source cannot be verified, mark it unresolved rather than inventing
support.

### Technical manuscript review

Use `$scholarly-technical-writing` when available for:

- conceptual progression;
- reader prerequisites;
- definition quality;
- mathematical/engineering exposition;
- examples;
- exercises;
- evidence placement;
- chapter-level coherence.

Use `$book-drafting-editor` for a controlled revision plan before broad changes.

Use `$high-stakes-book-review` selectively when evidence, security, privacy, legal
exposure, or reader harm makes it useful.

### Bibliography

Use Zotero when available as the bibliographic source of truth.

Never invent a Zotero record, citation key, DOI, quotation, or bibliographic detail.

### Figures

Use `$drawio` / `$drawio-academic-skills` only when a figure materially improves
engineering comprehension.

Keep editable source. Do not create decorative diagrams merely because the tool exists.

## English canonical pass

For English chapters:

- preserve the mandatory chapter contract;
- use British English;
- verify factual, empirical, historical, and literary claims;
- distinguish evidence, heuristic, and opinion;
- preserve provider neutrality;
- verify experiment descriptions against committed artifacts;
- verify Python/Go claims against code and tests;
- preserve narrative continuity;
- fix adjectives, adverbs, modifier scope, ambiguity, and technical prose when needed;
- avoid unnecessary stylistic churn.

Do not change English merely to force easier Persian translation.

## Persian pass

Persian is not a sentence-by-sentence copy of English.

Follow `writing_persian_eng_books.md`.

Always check:

- technical meaning;
- factual meaning;
- actor/action/object relation;
- negation, condition, modality, comparison, causality, and quantity;
- موصوف و صفت;
- مضاف و مضاف‌الیه;
- ezafe chains;
- adjective attachment/scope;
- adverb position/scope;
- mixed Persian-English grammar;
- terminology consistency;
- tooltip treatment;
- bidi integrity;
- protected tokens;
- reference/citation identity parity.

The integrity of text, adjectives, and adverbs is mandatory.

## Human review protection

Chapters 01–09 are the human-reviewed Persian calibration corpus.

Do not retranslate them wholesale.

Use `editorial/fa-review/regression-cases.yml` to detect recurrence and
`terminology-candidates.yml` as contextual candidates, not a whitelist.

Chapters 10–24 are not human-reviewed. Apply the validated failure classes to them
proactively, but do not call them human-reviewed after a machine pass.

## References

For shared canonical claims, Persian must not silently lose English evidence.

Compare citation identity where possible, not only reference count.

Persian may have justified additional references.

## Thematic parts

Prefer reader-facing thematic part names while keeping internal `part-1`…`part-4`
paths stable unless an explicit structural migration is requested.

Use `editorial/part-titles.yml` as a proposal, not an automatic rename command.

## Change discipline

Make targeted changes.

Do not:

- perform repository-wide cosmetic reformatting;
- run blind terminology replacements;
- overwrite unrelated user changes;
- change generated `site/` output directly;
- alter code/experiments merely to make prose claims true;
- commit or push unless explicitly requested.

If prose and implementation disagree, determine which source is wrong; do not silently
change code to match prose.

## Completion

Before calling work complete:

1. run relevant narrow tests while editing;
2. run `scripts/editorial_check.py`;
3. run the project-required `make check PYTHON=.venv/bin/python`;
4. inspect the final diff;
5. report unresolved evidence/terminology issues;
6. report review status honestly.

Read `references/workflow.md` for the end-to-end sequence and `references/gates.md` for
the acceptance gates.
