#!/usr/bin/env python3
"""Validate every completed chapter against the editorial contract."""

from __future__ import annotations

import re
from pathlib import Path

FRONT_MATTER_KEYS = [
    "title:",
    "slug:",
    "chapter:",
    "part:",
    "summary:",
    "maturity:",
    "last_reviewed:",
    "narrative_episode:",
    "learning_objectives:",
    "prerequisites:",
]
HEADINGS = [
    "## Learning Objectives",
    "## The Tale of Tahmures",
    "### The Setting",
    "### The Request",
    "### The Unexpected Result",
    "### The Discovery",
    "### From Tale to Engineering",
    "## The Engineering Problem",
    "## Mental Model",
    "## Core Concepts",
    "## Prompt Pattern",
    "## Naive Attempt",
    "## Failure Analysis",
    "## Improved Design",
    "## Worked Example",
    "## Experiment",
    "## Evaluation",
    "## Implementation Lab",
    "### Python",
    "### Go",
    "## Failure Modes",
    "## Security Considerations",
    "## Operational Considerations",
    "## Trade-Offs",
    "## When Prompting Is Not the Answer",
    "## Exercises",
    "## Chapter Summary",
    "## The Next Tale",
    "## Citations and Further Reading",
]


def narrative_words(text: str) -> int:
    start = text.index("### The Setting")
    end = text.index("### From Tale to Engineering")
    return len(re.findall(r"\b[\w’'-]+\b", text[start:end]))


def prose_words(text: str) -> int:
    body = text.split("---\n", 2)[2]
    body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    return len(re.findall(r"\b[\w’'-]+\b", body))


def validate(path: Path) -> tuple[int, str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or text.count("---\n") < 2:
        raise ValueError(f"{path}: missing YAML front matter")
    front_matter = text.split("---\n", 2)[1]
    for key in FRONT_MATTER_KEYS:
        if key not in front_matter:
            raise ValueError(f"{path}: missing front matter key {key}")
    positions: list[int] = []
    for heading in HEADINGS:
        try:
            positions.append(text.index(heading))
        except ValueError as error:
            raise ValueError(f"{path}: missing heading {heading}") from error
    if positions != sorted(positions):
        raise ValueError(f"{path}: chapter headings are out of contract order")
    words = narrative_words(text)
    if not 400 <= words <= 900:
        raise ValueError(f"{path}: narrative has {words} words; expected 400–900")
    if "original fictional episode" not in text:
        raise ValueError(f"{path}: missing original-fiction notice")
    if "<!-- next: ch" not in text:
        raise ValueError(f"{path}: missing machine-readable next-tale hook")
    if not re.search(r"## Citations and Further Reading\n\n.+", text, re.DOTALL):
        raise ValueError(f"{path}: citations section is empty")
    slug = re.search(r'^slug:\s*"([^"]+)"', front_matter, re.MULTILINE)
    episode = re.search(r'^narrative_episode:\s*"([^"]+)"', front_matter, re.MULTILINE)
    if not slug or not episode:
        raise ValueError(f"{path}: slug and narrative episode must be quoted")
    chapter = re.search(r"^chapter:\s*(\d+)", front_matter, re.MULTILINE)
    if not chapter:
        raise ValueError(f"{path}: chapter must be numeric")
    number = int(chapter.group(1))
    if 7 <= number <= 18:
        words = prose_words(text)
        if not 3500 <= words <= 5500:
            raise ValueError(f"{path}: prose has {words} words; expected 3,500–5,500")
    return number, slug.group(1), episode.group(1)


def main() -> int:
    chapters = sorted(Path("book").glob("part-*[0-9]/*[0-9]-*.md"))
    if not chapters:
        raise SystemExit("no completed chapter files found")
    slugs: set[str] = set()
    episodes: set[str] = set()
    numbers: list[int] = []
    for path in chapters:
        try:
            number, slug, episode = validate(path)
        except ValueError as error:
            raise SystemExit(str(error)) from error
        if slug in slugs or episode in episodes:
            raise SystemExit(f"{path}: duplicate slug or episode")
        numbers.append(number)
        slugs.add(slug)
        episodes.add(episode)
        print(f"{path}: valid")
    expected = list(range(1, max(numbers) + 1))
    if numbers != expected:
        raise SystemExit(f"chapter sequence must be {expected}; found {numbers}")
    manifests = sorted(Path("experiments/manifests").glob("ch*.json"))
    manifest_numbers = []
    for path in manifests:
        match = re.match(r"ch(\d+)-", path.name)
        if not match:
            raise SystemExit(f"{path}: manifest name lacks chapter prefix")
        manifest_numbers.append(int(match.group(1)))
    if sorted(manifest_numbers) != numbers:
        raise SystemExit(
            "completed chapters and manifests must have one-to-one coverage: "
            f"chapters={numbers}, manifests={sorted(manifest_numbers)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
