# Tahmures Editorial Gates

## Gate 1 — Repository integrity

Pass when:

- unrelated user changes are preserved;
- generated site files are not edited directly;
- document structure remains valid.

## Gate 2 — Technical integrity

Pass when:

- claims match canonical meaning;
- code/experiment descriptions match repository artifacts;
- numbers, units, formulas, identifiers, and commands are preserved;
- Python/Go equivalence claims are supported.

## Gate 3 — Evidence integrity

Pass when:

- load-bearing factual/empirical/historical claims are supported;
- unverifiable claims are qualified or reported;
- citations are not fabricated;
- Persian does not silently lose evidence for shared canonical claims.

## Gate 4 — English editorial integrity

Pass when:

- terms are defined before abstraction;
- modifier/adjective/adverb scope is clear;
- prose is precise and not inflated;
- British English is consistent;
- mandatory chapter structure remains intact.

## Gate 5 — Persian syntactic and semantic integrity

Pass when:

- Persian is natural;
- no literal English sentence architecture remains where it harms Persian;
- موصوف/صفت is correct;
- مضاف/مضاف‌الیه and ezafe are correct;
- adjective and adverb scope is correct;
- mixed English/Persian phrases obey Persian grammar;
- actor/action/object, negation, condition, modality, causality, comparison, and
  quantity are preserved.

## Gate 6 — Human-review integrity

Pass when:

- Chapters 01–09 human-approved wording is protected;
- Chapters 10–24 are not falsely labelled human-reviewed;
- new human findings are promoted into regression rules when appropriate.

## Gate 7 — Deterministic validation

Pass when applicable validators succeed:

- reference parity;
- protected-content parity;
- Persian editorial regression;
- review-status validation;
- translation synchronization;
- chapter/continuity checks;
- tests/experiments/parity/docs through `make check`.

A model's confidence cannot substitute for a failing deterministic gate.
