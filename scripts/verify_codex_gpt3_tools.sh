#!/usr/bin/env bash
set -euo pipefail

CODEX_HOME="${CODEX_HOME:-$HOME/.codex-gpt-3}"

echo "Using CODEX_HOME=$CODEX_HOME"
echo

echo "== Plugin list =="
CODEX_HOME="$CODEX_HOME" \
codex plugin list || true

echo
echo "== User skills =="
if [ -d "$CODEX_HOME/skills" ]; then
  find "$CODEX_HOME/skills" -maxdepth 2 -type f -name SKILL.md -print | sort
  find "$CODEX_HOME/skills" -maxdepth 2 -type l -print | sort
else
  echo "No skill directory: $CODEX_HOME/skills"
fi

echo
echo "== ARS payload search =="
find "$CODEX_HOME" -type f -path '*/academic-research-suite/SKILL.md' -print 2>/dev/null || true

echo
echo "Start a new session and run /skills:"
echo "  CODEX_HOME=\"$CODEX_HOME\" \\"
echo "  codex"
