#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from _editorial_common import (
    extract_citation_ids,
    iter_chapter_pairs,
    parse_chapter_selector,
    strip_fenced,
)

REGISTRY_PATH = Path("editorial/protected-citation-titles.json")
PROTECTED_ANCHOR = "Robertson, Stephen, and Hugo Zaragoza. 2009."
REFERENCE_HEADINGS = {
    "English": "Citations and Further Reading",
    "Persian": "منابع و مطالعهٔ بیشتر",
}


def _normalise_space(text: str) -> str:
    return " ".join(text.split())


def _unique_json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate registry key: {key}")
        result[key] = value
    return result


def load_protected_title_registry(root: Path) -> dict:
    """Load the single approved Chapter 12 reference; malformed policy fails closed."""
    policy = json.loads(
        (root / REGISTRY_PATH).read_text(encoding="utf-8"),
        object_pairs_hook=_unique_json_object,
    )
    if (
        not isinstance(policy, dict)
        or set(policy) != {"schema_version", "references"}
        or type(policy["schema_version"]) is not int
        or policy["schema_version"] != 1
        or not isinstance(policy["references"], list)
        or len(policy["references"]) != 1
    ):
        raise ValueError("expected schema_version 1 and one protected reference")
    reference = policy["references"][0]
    if (
        not isinstance(reference, dict)
        or set(reference)
        != {"chapter", "author_year_anchor", "article_title", "publication_title"}
        or type(reference["chapter"]) is not int
        or reference["chapter"] != 12
        or any(
            not isinstance(reference[key], str) or not _normalise_space(reference[key])
            for key in ("author_year_anchor", "article_title", "publication_title")
        )
    ):
        raise ValueError("invalid protected Chapter 12 reference fields")
    if _normalise_space(reference["author_year_anchor"]) != PROTECTED_ANCHOR:
        raise ValueError("protected reference must anchor Robertson–Zaragoza 2009")
    return reference


def _protected_title_fields(text: str, heading: str, anchor: str) -> tuple[str, str]:
    text = strip_fenced(text)
    headings = list(re.finditer(rf"(?m)^##[ \t]+{re.escape(heading)}[ \t]*$", text))
    if len(headings) != 1:
        raise ValueError("protected reference section must be present and unique")
    section = text[headings[0].end() :]
    section = re.split(r"(?m)^##[ \t]+", section, maxsplit=1)[0]
    # Indented continuation lines, including wrapped italic delimiters, belong
    # to the current entry rather than opening another top-level reference.
    bullets = list(re.finditer(r"(?m)^[-+*][ \t]+", section))
    entries = [
        _normalise_space(
            section[item.end() : bullets[index + 1].start()]
            if index + 1 < len(bullets)
            else section[item.end() :]
        )
        for index, item in enumerate(bullets)
    ]
    count = sum(entry.count(anchor) for entry in entries)
    if count != 1:
        raise ValueError(f"protected author/year anchor count is {count}; expected 1")
    entry = next(entry for entry in entries if anchor in entry)
    if not entry.startswith(anchor):
        raise ValueError("protected author/year anchor must start its reference entry")
    fields = re.match(
        r"^“([^“”]+)”\s+\*([^*]+)\*(?=\s|$)", entry[len(anchor) :].strip()
    )
    if not fields:
        raise ValueError("missing protected article/publication title structure")
    # The existing article convention places a terminal full stop inside quotes.
    article = _normalise_space(_normalise_space(fields[1]).removesuffix("."))
    return article, _normalise_space(fields[2])


def protected_title_errors(en_text: str, fa_text: str, reference: dict) -> list[str]:
    errors = []
    anchor = _normalise_space(reference["author_year_anchor"])
    for language, text in (("English", en_text), ("Persian", fa_text)):
        try:
            article, publication = _protected_title_fields(
                text, REFERENCE_HEADINGS[language], anchor
            )
        except ValueError as error:
            errors.append(f"ch12: {language} {error}")
            continue
        for field, actual in (("article", article), ("publication", publication)):
            expected = _normalise_space(reference[f"{field}_title"])
            if actual != expected:
                errors.append(
                    f"ch12: {language} protected {field} title mismatch: "
                    f"expected {expected!r}, received {actual!r}"
                )
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Validate citation identities and protected reference title fields."
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
    protected_seen = False
    try:
        protected = load_protected_title_registry(root)
    except (OSError, UnicodeError, ValueError) as error:
        errors.append(f"protected-title registry: {error}")
        protected = None

    for ch, en_path, fa_path in iter_chapter_pairs(root, selected):
        if ch == 12:
            protected_seen = True
        if not fa_path.exists():
            errors.append(f"ch{ch:02d}: missing Persian counterpart: {fa_path}")
            continue

        en_text = en_path.read_text(encoding="utf-8")
        fa_text = fa_path.read_text(encoding="utf-8")
        if protected is not None and ch == protected["chapter"]:
            errors.extend(protected_title_errors(en_text, fa_text, protected))
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

    if (
        protected is not None
        and (selected is None or 12 in selected)
        and not protected_seen
    ):
        errors.append("ch12: missing canonical chapter for protected reference")

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
