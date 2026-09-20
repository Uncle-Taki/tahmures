#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], root: Path) -> int:
    print("+", " ".join(cmd), flush=True)
    return subprocess.run(cmd, cwd=root).returncode


def main() -> int:
    ap = argparse.ArgumentParser(description="Run Tahmures editorial quality gates.")
    ap.add_argument("--root", default=".")
    ap.add_argument("--chapters", action="append")
    ap.add_argument("--skip-existing-translation-validator", action="store_true")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    py = sys.executable
    scripts = root / "scripts"

    chapter_args = []
    for value in args.chapters or []:
        chapter_args += ["--chapters", value]

    commands = [
        [py, str(scripts / "validate_editorial_status.py"), "--root", str(root)],
        [
            py,
            str(scripts / "validate_reference_parity.py"),
            "--root",
            str(root),
            *chapter_args,
        ],
        [
            py,
            str(scripts / "validate_protected_parity.py"),
            "--root",
            str(root),
            *chapter_args,
        ],
        [
            py,
            str(scripts / "validate_fa_editorial.py"),
            "--root",
            str(root),
            *chapter_args,
        ],
    ]

    translation = scripts / "validate_translations.py"
    if translation.exists() and not args.skip_existing_translation_validator:
        commands.append([py, str(translation)])

    failures = 0
    for cmd in commands:
        rc = run(cmd, root)
        if rc != 0:
            failures += 1

    print(f"editorial-check: failing_commands={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
