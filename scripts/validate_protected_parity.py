#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import re
from pathlib import Path

from _editorial_common import (
    FENCE_RE,
    URL_RE,
    iter_chapter_pairs,
    parse_chapter_selector,
)

EXEC_LABELS = {"python", "py", "go", "golang", "bash", "sh", "shell", "json"}

INLINE_RE = re.compile(r"`([^`\n]+)`")


def executable_fences(text: str):
    out = []
    for m in FENCE_RE.finditer(text):
        info = m.group(3).strip()
        label = info.split()[0].lower() if info else ""
        if label in EXEC_LABELS:
            out.append((info, m.group(4)))
    return out


def protected_inline_tokens(text: str):
    tokens = []
    for token in INLINE_RE.findall(text):
        # Limit this parity check to code-like tokens; ordinary English terms may be
        # intentionally represented differently in Persian prose.
        if (
            any(c in token for c in "_/\\.-{}[]()=:")
            or re.search(r"[a-z][A-Z]", token)
            or re.fullmatch(r"[A-Z][A-Z0-9_-]{1,}", token)
        ):
            tokens.append(token)
    return collections.Counter(tokens)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Validate protected English→Persian technical content parity."
    )
    ap.add_argument("--root", default=".")
    ap.add_argument("--chapters", action="append")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    selected = parse_chapter_selector(args.chapters)
    errors = []
    warnings = []
    checked = 0

    for ch, en_path, fa_path in iter_chapter_pairs(root, selected):
        if not fa_path.exists():
            errors.append(f"ch{ch:02d}: missing Persian counterpart")
            continue
        checked += 1
        en = en_path.read_text(encoding="utf-8")
        fa = fa_path.read_text(encoding="utf-8")

        en_fences = executable_fences(en)
        fa_fences = executable_fences(fa)
        if en_fences != fa_fences:
            errors.append(
                f"ch{ch:02d}: executable fenced blocks differ "
                f"(English={len(en_fences)}, Persian={len(fa_fences)})."
            )

        en_urls = collections.Counter(URL_RE.findall(en))
        fa_urls = collections.Counter(URL_RE.findall(fa))
        for url, count in en_urls.items():
            if fa_urls[url] < count:
                errors.append(
                    f"ch{ch:02d}: protected source URL missing/changed "
                    f"in Persian: {url}"
                )

        en_inline = protected_inline_tokens(en)
        fa_inline = protected_inline_tokens(fa)
        missing_inline = []
        for token, count in en_inline.items():
            if fa_inline[token] < count:
                missing_inline.append(token)
        if missing_inline:
            warnings.append(
                f"ch{ch:02d}: code-like inline tokens occur fewer times in Persian: "
                + ", ".join(sorted(set(missing_inline)))
            )

    for msg in warnings:
        print("WARNING:", msg)
    for msg in errors:
        print("ERROR:", msg)
    print(
        f"protected-parity: checked={checked} errors={len(errors)} "
        f"warnings={len(warnings)}"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
