# Tahmures

*The Art and Engineering of Speaking with Intelligent Machines*

Tahmures is a practical, narrative-supported book about designing, evaluating,
and operating reliable language-model interactions. The completed Parts I–IV
contain twenty-four chapters, shared offline experiments, and equivalent Python
and Go implementations.

The chapter stories are original teaching fiction inspired by the legendary
figure of Tahmures in Iranian epic tradition. They are not translations,
adaptations, or reconstructed passages from Ferdowsi's *Shahnameh*.

All twenty-four chapters are also available as a first-class Persian edition
with an RTL MkDocs build. The Persian manuscript is a
faithful editorial translation; code and offline experiment assets remain
shared with the English edition.

## Quick start

Requirements:

- Python 3.12
- Go 1.26
- Make

Create an isolated Python environment and install the pinned project tools:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev,docs]"
```

Run every completed-chapter quality gate:

```bash
make check
```

Build or preview the book:

```bash
make docs
make serve
make serve-en
make serve-fa
```

`make serve` builds both editions and serves English at
`http://127.0.0.1:8000/` and Persian at `http://127.0.0.1:8000/fa/`.
Use `make serve-en` or `make serve-fa` for a language-specific preview with
live reload.

Run one experiment with either implementation:

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch01-prompt-roles.json

go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch01-prompt-roles.json
```

All committed experiments use synthetic data and recorded fixtures. They make
no network calls and require no model-provider credentials.

## Project map

- `book/` — manuscript, references, and narrative continuity
- `book/fa/` — complete Persian manuscript and translation glossary
- `examples/python/` — canonical provider-neutral experiment library
- `examples/go/` — behaviourally equivalent Go implementation
- `experiments/` — shared manifests, datasets, and response fixtures
- `prompts/` — versioned prompt variants used by the experiments
- `scripts/` — content validation and experiment entry points

The editorial rules live in `meta-prompt.md`; the approved direction and
delivery phases live in `book/project-charter.md`.

## Character work with Google AI Studio

For the private-repository workflow on branch `main`, start with the
[AI Studio handoff](editorial/media-handoff/README.md). It contains the starting
prompt, phase roadmap, protected-input baseline and task return contract.
Codex reviews actual implementation files and local Godot results before the
next phase proceeds.

## Licences

Book prose and other content are licensed under CC BY 4.0. Source code is
licensed under Apache-2.0. See `LICENSE-CONTENT.md` and `LICENSE-CODE`.
