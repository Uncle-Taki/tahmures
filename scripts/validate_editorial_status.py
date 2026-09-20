#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit(
        "PyYAML is required; activate the project dev/docs environment."
    ) from exc


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Validate Tahmures Persian human/machine review state."
    )
    ap.add_argument("--root", default=".")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    path = root / "editorial/review-status.yml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    chapters = data.get("chapters", {})
    errors = []

    for ch in range(1, 25):
        key = f"{ch:02d}"
        if key not in chapters:
            errors.append(f"missing chapter {key} in review-status.yml")
            continue
        fa = chapters[key].get("persian", {})
        human = bool(fa.get("human_reviewed"))
        status = fa.get("status")

        if ch <= 9:
            if not human or status != "human_reviewed":
                errors.append(
                    f"chapter {key}: expected human_reviewed calibration status"
                )
        else:
            if human or status == "human_reviewed":
                errors.append(
                    f"chapter {key}: must not be marked human_reviewed "
                    "before author review"
                )
            if status not in {"unreviewed", "machine_prechecked"}:
                errors.append(f"chapter {key}: invalid Persian status {status!r}")

    for msg in errors:
        print("ERROR:", msg)
    print(f"editorial-status: chapters=24 errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
