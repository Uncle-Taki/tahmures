# Tahmures Persian Batch Review Prompt

Use `$tahmures-editorial`.

Target Persian chapters: {{CHAPTER_RANGE}}.

These chapters are not human-reviewed unless `editorial/review-status.yml` explicitly
says otherwise.

Read repository authority files and the 01–09 calibration/regression corpus first.

Apply all validated failure classes from Chapters 01–09, including:

- citation identity parity;
- protected-content parity;
- literal-translation detection;
- موصوف/صفت;
- مضاف/مضاف‌الیه and ezafe;
- adjective scope;
- adverb scope;
- actor/action/object and negation/condition/modality/causality/quantity;
- mixed Persian-English grammar;
- terminology candidates;
- tooltip treatment;
- natural Persian word order.

Make safe edits. Flag ambiguous cases instead of guessing.

Do not rewrite human-approved text merely to resemble English.

After editing run:

```bash
.venv/bin/python scripts/editorial_check.py --chapters {{CHAPTER_RANGE}}
make check PYTHON=.venv/bin/python
```

Update review state only to `machine_prechecked` unless the author has actually reviewed
the chapter.

Return a concise change/validation report.
