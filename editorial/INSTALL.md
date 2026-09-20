# Tahmures Editorial/Skill Installation Guide

## 1. Copy the generated files

Copy this package into the root of the Tahmures repository, preserving paths.

Important root-level replacements:

- `AGENTS.md`
- `writing_persian_eng_books.md`

New paths include:

- `.agents/skills/tahmures-editorial/`
- `editorial/`
- `scripts/validate_*.py`
- `scripts/editorial_check.py`
- `editorial.mk`
- `prompts/final-book-review.md`

Before replacing the two existing root policy files, review the diff.

## 2. Add Makefile integration

The current Makefile was not supplied when this package was generated, so the package
does not guess its structure.

Add this one line near the end of the repository's root `Makefile`:

```make
-include editorial.mk
```

This exposes:

```bash
make editorial-check PYTHON=.venv/bin/python
make validate-reference-parity PYTHON=.venv/bin/python
make validate-protected-parity PYTHON=.venv/bin/python
make validate-fa-editorial PYTHON=.venv/bin/python
make validate-editorial-status PYTHON=.venv/bin/python
```

The direct Python commands also work without modifying the Makefile.

## 3. Install Codex tools into `.codex-gpt-3`

You can run:

```bash
bash scripts/install_codex_gpt3_tools.sh
```

The script:

- targets `$HOME/.codex-gpt-3`;
- installs ARS-Codex;
- clones/updates Writer Skills;
- exposes only the selected writer skills;
- clones/updates Draw.io Skills;
- exposes `drawio` and `drawio-academic-skills`;
- does not install optional licensing-sensitive `technical-writing`;
- does not install Zotero automatically.

Verify:

```bash
bash scripts/verify_codex_gpt3_tools.sh
```

## 4. Install Zotero interactively

Launch:

```bash
CODEX_HOME="$HOME/.codex-gpt-3" \
codex
```

Use the plugin UI in that Codex home to install/enable Zotero, then restart the
conversation.

## 5. Baseline repository validation

Before large edits:

```bash
make check PYTHON=.venv/bin/python
```

Then run the new editorial checks:

```bash
.venv/bin/python scripts/editorial_check.py
```

Record pre-existing failures before editing so Codex does not attribute them to the new
workflow.

## 6. Calibrate on Chapters 01–09

Do not rewrite them wholesale.

Run the final prompt in calibration/review mode and confirm that the new system:

- preserves human-approved changes;
- catches known regression patterns;
- does not introduce new literal translations;
- does not change code/identifiers;
- does not lose citations.

## 7. Apply to Chapters 10–24

Process in review batches:

- 10–12
- 13–15
- 16–18
- 19–21
- 22–24

The final prompt is written to allow a whole-book pass, but smaller batches are safer
for human review and terminology drift control.

After a machine pass, Chapters 10–24 remain non-human-reviewed until the author reviews
them.

## 8. Thematic part titles

`editorial/part-titles.yml` contains proposed reader-facing thematic names.

Apply them to MkDocs navigation/index pages only after inspecting the current
`mkdocs.yml`, `mkdocs.fa.yml`, part index pages, anchors, and cross-references.

Do not rename `part-1`…`part-4` directories as part of this editorial migration.

## 9. Final prompt

Use:

```text
prompts/final-book-review.md
```

Start Codex with:

```bash
CODEX_HOME="$HOME/.codex-gpt-3" \
codex
```

Then paste the prompt body or tell Codex to read and execute that file.
