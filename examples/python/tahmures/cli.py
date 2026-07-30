"""Command-line interface for offline Tahmures experiments."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from tahmures.manifest import load_manifest
from tahmures.runner import fixture_runner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tahmures")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run = subparsers.add_parser("run", help="run an experiment manifest")
    run.add_argument("--manifest", required=True, type=Path)
    run.add_argument("--output", type=Path)
    run.add_argument("--client", choices=["fixture"], default="fixture")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        manifest = load_manifest(args.manifest)
        report = fixture_runner(manifest, args.manifest).run()
    except (OSError, ValueError, LookupError) as error:
        print(f"error: {error}")
        return 2
    payload = json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
