# Tahmures Editorial System

This directory stores **human editorial state and policy evidence**, not generated site
output.

## Files

- `fa-review/chapters-01-09.md` — human findings from Persian Chapters 01–09 and the
  failure classes derived from them.
- `fa-review/terminology-candidates.yml` — contextual English-retention candidates.
  This is not a blanket whitelist and does not replace `book/fa/translation-glossary.md`.
- `fa-review/regression-cases.yml` — human-approved and flag-only Persian regression
  cases used by `scripts/validate_fa_editorial.py`.
- `review-status.yml` — distinguishes `human_reviewed`, `machine_prechecked`, and
  `unreviewed`.
- `part-titles.yml` — proposed reader-facing thematic names while keeping internal
  `part-1`…`part-4` paths stable.
- `toolchain-lock.md` — approved external Codex tools, roles, installation method, and
  precedence rules.
- `INSTALL.md` — installation and repository-integration instructions.

## Review-state rule

Chapters 01–09 are the human calibration corpus.

Chapters 10–24 are **not** human-reviewed. The known failure classes from 01–09 must be
applied proactively to them, but a Codex or validator pass may only establish
`machine_prechecked`.

## Promotion workflow for terminology

```text
human observation
→ terminology-candidates.yml
→ contextual verification
→ explicit approval
→ book/fa/translation-glossary.md
→ validator/regression update when appropriate
```

## Regression workflow

When human review finds a generalizable failure:

1. preserve the exact bad wording;
2. preserve the approved correction when one exists;
3. classify severity;
4. add the case to `regression-cases.yml`;
5. run `scripts/validate_fa_editorial.py`;
6. apply the failure class to unreviewed chapters;
7. do not convert an ambiguous `flag_only` case into an automatic replacement.

## Validation

Direct:

```bash
.venv/bin/python scripts/editorial_check.py
```

With Makefile integration:

```bash
make editorial-check PYTHON=.venv/bin/python
```

Heuristic warnings require review. Exact blocker/high-severity regression occurrences
must be fixed before completion.
