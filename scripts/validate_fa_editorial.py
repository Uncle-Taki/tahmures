#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit(
        "PyYAML is required by this validator. Activate the project's dev/docs "
        "environment (MkDocs normally provides PyYAML) and retry."
    ) from exc

from _editorial_common import FENCE_RE, line_number, parse_chapter_selector

INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
HTML_TAG_RE = re.compile(r"<[^>]+>")
# The glossary prescribes ZWNJ (U+200C) before Persian suffixes on Latin terms
# (e.g. case\u200cها). Suffixes without ZWNJ (caseها) are genuine violations;
# suffixes with ZWNJ are sanctioned, so only flag the missing-ZWNJ form.
LATIN_SUFFIX_WITHOUT_ZWNJ_RE = re.compile(
    r"\b[A-Za-z][A-Za-z0-9_-]*(?:ها|های|هایی|ها‌ی)\b"
)

# These are warnings only. They intentionally do not attempt automatic correction.
FA_ADJ_BEFORE_LATIN_RE = re.compile(
    r"(?<![\w\u0600-\u06FF])"
    r"(?:خام|مجاز|الزامی|اضافی|میانی|نهایی|خودکار|اصلی|ثانویه)"
    r"\s+[A-Za-z][A-Za-z0-9_-]*"
)
LATIN_BEFORE_FA_NOUN_RE = re.compile(
    r"\b[A-Za-z][A-Za-z0-9_-]*\s+"
    # A Latin technical noun followed by an ezafe-marked Persian stage and its
    # modifier (for example, "interpolation مرحلهٔ دوم") is a sanctioned,
    # grammatically ordered construction rather than a Latin modifier.
    r"(?:فیلد|رکورد|پاسخ|قرارداد|نثر|مجموعه|نوع|وضعیت|مرحله(?![\u0654\u200c]))"
    # Require a complete noun; do not flag the prefix of a Persian predicate
    # such as "requirements پاسخگو".
    r"(?![\u0600-\u06FF\u200c])"
)


MARKDOWN_HEADING_RE = re.compile(r"(?m)^#{1,6}\s+.*$")


def prose_only(text: str) -> str:
    text = FENCE_RE.sub("", text)
    text = INLINE_CODE_RE.sub("", text)
    text = HTML_TAG_RE.sub("", text)
    # Strip markdown headings: a heading's last Latin word followed by body
    # prose is a boundary artifact, not a mixed-language phrase.
    text = MARKDOWN_HEADING_RE.sub("", text)
    return text


def load_cases(root: Path):
    path = root / "editorial/fa-review/regression-cases.yml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data.get("cases", [])


def chapter_files(root: Path, selected: set[int] | None):
    for path in sorted(root.glob("book/fa/part-*/*.md")):
        if path.name == "index.md":
            continue
        m = re.match(r"(\d{2})-", path.name)
        if not m:
            continue
        ch = int(m.group(1))
        if selected is None or ch in selected:
            yield ch, path


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Validate known and heuristic Persian editorial regressions."
    )
    ap.add_argument("--root", default=".")
    ap.add_argument("--chapters", action="append")
    ap.add_argument("--fail-on-warnings", action="store_true")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    selected = parse_chapter_selector(args.chapters)
    cases = load_cases(root)
    errors = []
    warnings = []
    checked = 0

    for ch, path in chapter_files(root, selected):
        checked += 1
        text = path.read_text(encoding="utf-8")
        prose = prose_only(text)

        for case in cases:
            bad = case.get("before")
            if not isinstance(bad, str) or not bad.strip():
                continue
            start = 0
            while True:
                idx = prose.find(bad, start)
                if idx < 0:
                    break
                severity = str(case.get("severity", "medium"))
                msg = (
                    f"ch{ch:02d} {path}: line≈{line_number(prose, idx)} "
                    f"{case.get('id')} {case.get('type')} matched known "
                    "bad/regression text"
                )
                if severity in {"blocker", "high"}:
                    errors.append(msg)
                else:
                    warnings.append(msg)
                start = idx + max(1, len(bad))

        for regex, label in [
            (LATIN_SUFFIX_WITHOUT_ZWNJ_RE, "mixed Latin/Persian morphology"),
            (FA_ADJ_BEFORE_LATIN_RE, "possible Persian adjective before Latin head"),
            (LATIN_BEFORE_FA_NOUN_RE, "possible Latin modifier before Persian noun"),
        ]:
            for m in regex.finditer(prose):
                warnings.append(
                    f"ch{ch:02d} {path}: line≈{line_number(prose, m.start())} "
                    f"{label}: {m.group(0)!r}"
                )

        if re.search(r"\basses\b", prose, flags=re.I):
            warnings.append(
                f"ch{ch:02d} {path}: token 'asses' found; verify whether "
                "the intended term is 'assess'."
            )

    for msg in warnings:
        print("WARNING:", msg)
    for msg in errors:
        print("ERROR:", msg)
    print(
        f"fa-editorial: checked={checked} errors={len(errors)} warnings={len(warnings)}"
    )
    print(
        "disposition: morphology warnings cover only missing-ZWNJ suffixes; "
        "glossary-sanctioned ZWNJ forms and ezafe-ordered mixed phrases are "
        "not flagged"
    )

    if errors:
        return 1
    if warnings and args.fail_on_warnings:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
