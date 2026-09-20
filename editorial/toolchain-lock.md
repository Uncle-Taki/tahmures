# Tahmures Codex Toolchain Lock

## Active Codex home

For this project, use:

```bash
CODEX_HOME="$HOME/.codex-gpt-3" \
codex
```

Every Codex CLI install/update/list command in this file targets the same home.

External tools are subordinate helpers. They never override `AGENTS.md`,
`book/project-charter.md`, `book/narrative-continuity.md`, `meta-prompt.md`,
`writing_persian_eng_books.md`, the glossary, human review state, or deterministic
validators.

## Approved tools

### Core

- ARS-Codex / `$academic-research-suite`
  - evidence discovery;
  - fact checking;
  - primary-source research;
  - citation audit;
  - experiment/reproducibility review.
- Zotero
  - bibliographic source of truth;
  - citation-key/BibTeX operations;
  - source-library search.
- `$scholarly-technical-writing`
  - technical-book review;
  - explanation quality;
  - conceptual progression.
- `$book-drafting-editor`
  - revision planning;
  - controlled manuscript editing.
- `$drawio`
  - editable engineering diagrams.
- `$drawio-academic-skills`
  - publication-facing diagram review/export workflow.
- project-local `$tahmures-editorial`
  - routing and Tahmures-specific orchestration.

### Selective

- `$high-stakes-book-review` — evidence/safety/privacy/legal/reader-harm review where
  relevant.
- `gwagjiug/technical-writing` — optional English review only after separately
  accepting its licensing implications.
- individual K-Dense skills — on demand only.

### Disabled by default

- Quill as book manager;
- external book-project architect;
- external book-structure designer;
- external fiction story-bible manager;
- full K-Dense bundle;
- mechanical-engineering-research-skill;
- diagram-design when Draw.io is sufficient.

## ARS-Codex installation

Add the marketplace:

```bash
CODEX_HOME="$HOME/.codex-gpt-3" \
codex plugin marketplace add Imbad0202/academic-research-skills-codex --ref main
```

Install the plugin payload:

```bash
CODEX_HOME="$HOME/.codex-gpt-3" \
codex plugin add ars-codex@ars-codex
```

Verify:

```bash
CODEX_HOME="$HOME/.codex-gpt-3" \
codex plugin list
```

Then open a **new** conversation:

```bash
CODEX_HOME="$HOME/.codex-gpt-3" \
codex
```

Expected skill:

```text
academic-research-suite
```

The marketplace-add command alone is not the plugin installation step.

## Writer Skills installation

Stable source checkout:

```bash
mkdir -p "$HOME/.local/share/codex-skill-sources"

git clone https://github.com/wnsdy95/writer-skills.git \
  "$HOME/.local/share/codex-skill-sources/writer-skills"
```

If already cloned:

```bash
git -C "$HOME/.local/share/codex-skill-sources/writer-skills" pull --ff-only
```

Expose only selected skills:

```bash
mkdir -p "$HOME/.codex-gpt-3/skills"

ln -sfn \
  "$HOME/.local/share/codex-skill-sources/writer-skills/skills/scholarly-technical-writing" \
  "$HOME/.codex-gpt-3/skills/scholarly-technical-writing"

ln -sfn \
  "$HOME/.local/share/codex-skill-sources/writer-skills/skills/book-drafting-editor" \
  "$HOME/.codex-gpt-3/skills/book-drafting-editor"

ln -sfn \
  "$HOME/.local/share/codex-skill-sources/writer-skills/skills/high-stakes-book-review" \
  "$HOME/.codex-gpt-3/skills/high-stakes-book-review"
```

Do not expose book-architecture/story-bible skills by default.

## Draw.io Skills installation

Stable source checkout:

```bash
git clone https://github.com/bahayonghang/drawio-skills.git \
  "$HOME/.local/share/codex-skill-sources/drawio-skills"
```

If already cloned:

```bash
git -C "$HOME/.local/share/codex-skill-sources/drawio-skills" pull --ff-only
```

Expose both sibling skills so the academic overlay can resolve the base skill:

```bash
ln -sfn \
  "$HOME/.local/share/codex-skill-sources/drawio-skills/skills/drawio" \
  "$HOME/.codex-gpt-3/skills/drawio"

ln -sfn \
  "$HOME/.local/share/codex-skill-sources/drawio-skills/skills/drawio-academic-skills" \
  "$HOME/.codex-gpt-3/skills/drawio-academic-skills"
```

The normal offline/publication workflow does not require a Draw.io MCP server.

## Zotero

Launch the correct Codex home:

```bash
CODEX_HOME="$HOME/.codex-gpt-3" \
codex
```

Install/enable Zotero from the Codex plugin UI available in that session.

After installation, start a new conversation and verify Zotero readiness before relying
on it for bibliography work.

Do not fabricate a bibliography if Zotero or another source database is unavailable.

## Skill verification

Inspect the custom skill directory:

```bash
find "$HOME/.codex-gpt-3/skills" -maxdepth 2 -name SKILL.md -print | sort
```

Verify ARS plugin state:

```bash
CODEX_HOME="$HOME/.codex-gpt-3" \
codex plugin list
```

Then start:

```bash
CODEX_HOME="$HOME/.codex-gpt-3" \
codex
```

and run `/skills`.

Expected project-relevant skills include:

```text
academic-research-suite
scholarly-technical-writing
book-drafting-editor
high-stakes-book-review
drawio
drawio-academic-skills
tahmures-editorial
```

The project-local `tahmures-editorial` skill is discovered from the repository's
`.agents/skills/` tree when supported by the active Codex build.

## Role boundaries

### ARS

May:
- research;
- verify;
- audit evidence;
- review experiments.

Must not:
- become the book architecture source of truth;
- translate Persian by itself;
- override human-approved Persian;
- silently rewrite whole chapters during an evidence audit.

### Writer Skills

May:
- review;
- diagnose;
- plan revisions;
- improve technical explanation when asked.

Must not:
- replace the mandatory chapter contract;
- create a second project charter;
- create a second narrative continuity system.

### Draw.io

May:
- create/edit technical figures;
- keep editable `.drawio` source;
- produce publication exports.

Do not create figures merely because the tool is installed.

### Zotero

May:
- manage bibliographic records;
- provide citation keys;
- verify library presence.

The manuscript remains in the repository.

## Review propagation

```text
Chapters 01–09
= human-reviewed calibration corpus

Chapters 10–24
= unreviewed target corpus
```

Apply validated 01–09 failure classes to 10–24 immediately, but record only
`machine_prechecked` until human review occurs.

## Final acceptance

External skill output is advisory until repository checks pass.

Direct editorial checks:

```bash
.venv/bin/python scripts/editorial_check.py
```

Full project acceptance:

```bash
make check PYTHON=.venv/bin/python
```

Do not commit or push unless explicitly requested.
