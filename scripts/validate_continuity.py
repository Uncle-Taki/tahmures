#!/usr/bin/env python3
"""Check the continuity ledger and hook chain for completed chapters."""

import re
from pathlib import Path


def main() -> int:
    continuity = Path("book/narrative-continuity.md")
    if not continuity.exists():
        raise SystemExit("missing book/narrative-continuity.md")
    text = continuity.read_text(encoding="utf-8")
    chapters = sorted(Path("book").glob("part-*/*[0-9]-*.md"))
    episodes: list[str] = []
    numbers: list[int] = []
    for path in chapters:
        chapter_text = path.read_text(encoding="utf-8")
        front_matter = chapter_text.split("---\n", 2)[1]
        number_match = re.search(r"^chapter:\s*(\d+)", front_matter, re.MULTILINE)
        episode_match = re.search(
            r'^narrative_episode:\s*"([^"]+)"', front_matter, re.MULTILINE
        )
        if not number_match or not episode_match:
            raise SystemExit(f"{path}: cannot derive chapter continuity metadata")
        numbers.append(int(number_match.group(1)))
        episodes.append(episode_match.group(1))
    if numbers != list(range(1, len(chapters) + 1)):
        raise SystemExit(f"chapter continuity sequence is not complete: {numbers}")
    if len(episodes) != len(set(episodes)):
        raise SystemExit("duplicate episode titles in completed chapters")
    for number, episode in zip(numbers, episodes, strict=True):
        if text.count(episode) < 1:
            raise SystemExit(f"continuity record missing episode {episode}")
        row_marker = f"| {number:02d} |"
        if row_marker not in text:
            raise SystemExit(f"continuity record missing chapter row {row_marker}")
    for number, path in zip(numbers, chapters, strict=True):
        expected = f"<!-- next: ch{number + 1:02d} -->"
        if expected not in path.read_text(encoding="utf-8"):
            raise SystemExit(f"{path}: expected hook marker {expected}")
    for required in [
        "The First Scribe",
        "Mirror Div",
        "The Archivist",
        "Keeper of Scripts",
        "The Gatekeeper",
        "experiment ledger",
        "mechanical scribes",
        "Many-Voiced",
        "context selection",
        "evidence ledger",
        "ivory memory ledger",
        "divided key ring",
        "recall bell",
        "hand-off envelope",
        "Wandering Div",
    ]:
        if required not in text:
            raise SystemExit(f"continuity record missing pilot element: {required}")
    print("narrative continuity: valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
