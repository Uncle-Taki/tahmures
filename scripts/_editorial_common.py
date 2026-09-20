from __future__ import annotations

import re
from pathlib import Path

FENCE_RE = re.compile(r"(?ms)^([ \t]*)(`{3,}|~{3,})([^\n]*)\n(.*?)^\1\2[ \t]*$")
URL_RE = re.compile(r"https?://[^\s<>\]\)\"']+")
DOI_RE = re.compile(r"(?i)\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b")


def chapter_number(path: Path) -> int | None:
    m = re.match(r"(\d{2})-", path.name)
    return int(m.group(1)) if m else None


def iter_chapter_pairs(root: Path, selected: set[int] | None = None):
    for en in sorted(root.glob("book/part-*/*.md")):
        if en.name == "index.md":
            continue
        ch = chapter_number(en)
        if ch is None or (selected is not None and ch not in selected):
            continue
        rel = en.relative_to(root / "book")
        fa = root / "book" / "fa" / rel
        yield ch, en, fa


def parse_chapter_selector(values: list[str] | None) -> set[int] | None:
    if not values:
        return None
    out: set[int] = set()
    for value in values:
        for part in value.split(","):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                a, b = part.split("-", 1)
                out.update(range(int(a), int(b) + 1))
            else:
                out.add(int(part))
    return out


def strip_fenced(text: str) -> str:
    return FENCE_RE.sub("", text)


def line_number(text: str, start: int) -> int:
    return text.count("\n", 0, start) + 1


def citation_section(text: str) -> str:
    # English and Persian may use different translated headings; if an English canonical
    # heading is present use it, otherwise scan the entire chapter.
    m = re.search(r"(?mi)^##\s+Citations and Further Reading\s*$", text)
    return text[m.end() :] if m else text


def extract_citation_ids(text: str) -> set[str]:
    text = strip_fenced(citation_section(text))
    ids: set[str] = set()

    for url in URL_RE.findall(text):
        ids.add("url:" + url.rstrip(".,;:"))

    for doi in DOI_RE.findall(text):
        ids.add("doi:" + doi.lower().rstrip(".,;:"))

    # Pandoc-style citations: [@key; @key2]
    for group in re.findall(r"\[([^\]]*@[^\]]+)\]", text):
        for key in re.findall(r"@([A-Za-z0-9_:.+\-/]+)", group):
            ids.add("cite:" + key)

    # LaTeX-style citations.
    for group in re.findall(r"\\cite[a-zA-Z*]*\{([^}]+)\}", text):
        for key in group.split(","):
            key = key.strip()
            if key:
                ids.add("cite:" + key)

    return ids
