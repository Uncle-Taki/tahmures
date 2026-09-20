#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from _editorial_common import (
    extract_citation_ids,
    iter_chapter_pairs,
    parse_chapter_selector,
)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Validate English→Persian citation identity containment."
    )
    ap.add_argument("--root", default=".")
    ap.add_argument("--chapters", action="append", help="Examples: 1-9, 10,12,14")
    ap.add_argument("--json-report")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    selected = parse_chapter_selector(args.chapters)
    errors = []
    warnings = []
    report = []

    for ch, en_path, fa_path in iter_chapter_pairs(root, selected):
        if not fa_path.exists():
            errors.append(f"ch{ch:02d}: missing Persian counterpart: {fa_path}")
            continue

        en_text = en_path.read_text(encoding="utf-8")
        fa_text = fa_path.read_text(encoding="utf-8")
        en_ids = extract_citation_ids(en_text)
        fa_ids = extract_citation_ids(fa_text)
        missing = sorted(en_ids - fa_ids)

        report.append(
            {
                "chapter": ch,
                "english": str(en_path.relative_to(root)),
                "persian": str(fa_path.relative_to(root)),
                "english_ids": sorted(en_ids),
                "persian_ids": sorted(fa_ids),
                "missing_from_persian": missing,
            }
        )

        if missing:
            errors.append(
                f"ch{ch:02d}: Persian is missing {len(missing)} "
                "recognizable citation identities: " + ", ".join(missing)
            )
        if not en_ids:
            warnings.append(
                f"ch{ch:02d}: no machine-recognizable URL/DOI/citation "
                "key found in English; "
                "manual citation-parity review may still be required."
            )

    if args.json_report:
        Path(args.json_report).write_text(
            json.dumps(
                {"chapters": report, "errors": errors, "warnings": warnings},
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    for msg in warnings:
        print("WARNING:", msg)
    for msg in errors:
        print("ERROR:", msg)

    print(
        f"reference-parity: checked={len(report)} errors={len(errors)} "
        f"warnings={len(warnings)}"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
