#!/usr/bin/env bash
set -euo pipefail

CODEX_HOME="${CODEX_HOME:-$HOME/.codex-gpt-3}"
SOURCES="$HOME/.local/share/codex-skill-sources"

echo "Using CODEX_HOME=$CODEX_HOME"
mkdir -p "$CODEX_HOME/skills" "$SOURCES"

if ! command -v codex >/dev/null 2>&1; then
  echo "ERROR: codex command not found" >&2
  exit 1
fi

echo "== ARS-Codex marketplace =="
CODEX_HOME="$CODEX_HOME" \
codex plugin marketplace add Imbad0202/academic-research-skills-codex --ref main \
  || echo "Marketplace may already exist; continuing."

echo "== ARS-Codex plugin =="
CODEX_HOME="$CODEX_HOME" \
codex plugin add ars-codex@ars-codex

clone_or_update() {
  local repo="$1"
  local dest="$2"
  if [ -d "$dest/.git" ]; then
    git -C "$dest" pull --ff-only
  else
    git clone "$repo" "$dest"
  fi
}

echo "== Writer Skills =="
clone_or_update \
  https://github.com/wnsdy95/writer-skills.git \
  "$SOURCES/writer-skills"

for skill in scholarly-technical-writing book-drafting-editor high-stakes-book-review; do
  src="$SOURCES/writer-skills/skills/$skill"
  if [ ! -f "$src/SKILL.md" ]; then
    echo "ERROR: missing Writer Skill: $src/SKILL.md" >&2
    exit 1
  fi
  ln -sfn "$src" "$CODEX_HOME/skills/$skill"
done

echo "== Draw.io Skills =="
clone_or_update \
  https://github.com/bahayonghang/drawio-skills.git \
  "$SOURCES/drawio-skills"

for skill in drawio drawio-academic-skills; do
  src="$SOURCES/drawio-skills/skills/$skill"
  if [ ! -f "$src/SKILL.md" ]; then
    echo "ERROR: missing Draw.io skill: $src/SKILL.md" >&2
    exit 1
  fi
  ln -sfn "$src" "$CODEX_HOME/skills/$skill"
done

echo
echo "Installed/updated core non-Zotero tools in: $CODEX_HOME"
echo "Zotero is intentionally not installed by this script; install/enable it in the Codex plugin UI."
echo
echo "Open a NEW Codex session with:"
echo "  CODEX_HOME=\"$CODEX_HOME\" \\"
echo "  codex"
