#!/usr/bin/env python3
"""Compare aggregate reports produced by the Python and Go CLIs."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def run(command: list[str], output: Path) -> dict:
    environment = os.environ.copy()
    environment.setdefault("GOCACHE", "/tmp/tahmures-go-cache")
    completed = subprocess.run(
        [*command, "--output", str(output)],
        check=False,
        text=True,
        capture_output=True,
        env=environment,
    )
    if completed.returncode:
        raise SystemExit(completed.stderr or completed.stdout)
    return json.loads(output.read_text(encoding="utf-8"))


def main() -> int:
    manifests = sorted(Path("experiments/manifests").glob("ch*.json"))
    with tempfile.TemporaryDirectory(prefix="tahmures-parity-") as directory:
        temporary = Path(directory)
        for manifest in manifests:
            python_report = run(
                [
                    sys.executable,
                    "-m",
                    "tahmures.cli",
                    "run",
                    "--manifest",
                    str(manifest),
                ],
                temporary / "python.json",
            )
            go_report = run(
                [
                    "go",
                    "run",
                    "./examples/go/cmd/tahmures",
                    "run",
                    "--manifest",
                    str(manifest),
                ],
                temporary / "go.json",
            )
            if python_report["variant_summaries"] != go_report["variant_summaries"]:
                raise SystemExit(
                    f"parity failure for {manifest}:\n"
                    f"python={python_report['variant_summaries']}\n"
                    f"go={go_report['variant_summaries']}"
                )
            if python_report["tag_summaries"] != go_report["tag_summaries"]:
                raise SystemExit(
                    f"tag parity failure for {manifest}:\n"
                    f"python={python_report['tag_summaries']}\n"
                    f"go={go_report['tag_summaries']}"
                )
            print(f"{manifest.name}: parity confirmed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
