#!/usr/bin/env python3
"""Validate every completed chapter against the editorial contract."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

FRONT_MATTER_KEYS = [
    "title:",
    "slug:",
    "chapter:",
    "part:",
    "summary:",
    "maturity:",
    "last_reviewed:",
    "narrative_episode:",
    "narrative_origin:",
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

# D19: the final chapter closes the book. Its closing section replaces the
# next-tale heading and uses the closing marker instead of a next-chapter hook.
FINAL_CHAPTER = 24
NEXT_TALE_HEADING = "## The Next Tale"
CLOSING_HEADING = "## The Practice Continues"
CLOSING_MARKER = "<!-- closing -->"

PART_PREFIXES = {
    "part-1": ("Part I", "بخش یک"),
    "part-2": ("Part II", "بخش دو"),
    "part-3": ("Part III", "بخش سه"),
    "part-4": ("Part IV", "بخش چهار"),
}
CHAPTER_REFERENCE_RE = re.compile(r"^C(0[1-9]|1[0-9]|2[0-4])$")


def front_matter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or text.count("---\n") < 2:
        raise ValueError(f"{path}: missing YAML front matter")
    parsed = yaml.safe_load(text.split("---\n", 2)[1])
    if not isinstance(parsed, dict):
        raise ValueError(f"{path}: malformed YAML front matter")
    return parsed


def validate_reference(reference: object, dependent: str, source: Path) -> str:
    if not isinstance(reference, str) or not CHAPTER_REFERENCE_RE.fullmatch(reference):
        raise ValueError(f"{source}: malformed prerequisite reference {reference!r}")
    if int(reference[1:]) >= int(dependent[1:]):
        raise ValueError(f"{source}: forward prerequisite {reference} -> {dependent}")
    return reference


def validate_charter_dependency_graph(
    root: Path, dependencies: dict[object, object]
) -> None:
    charter = root / "book/project-charter.md"
    match = re.search(
        r"## 10\. Learning Dependency Graph\n\n```mermaid\n(.*?)```",
        charter.read_text(encoding="utf-8"),
        re.DOTALL,
    )
    if not match:
        raise ValueError(f"{charter}: missing Mermaid learning dependency graph")
    charter_edges = re.findall(r"\b(C\d{2})\b.*?-->\s*(C\d{2})\b", match.group(1))
    if len(charter_edges) != len(set(charter_edges)):
        raise ValueError(f"{charter}: duplicate dependency edge")
    canonical_edges = {
        (parent, dependent)
        for dependent, parents in dependencies.items()
        for parent in parents
    }
    if set(charter_edges) != canonical_edges:
        missing = sorted(canonical_edges - set(charter_edges))
        unexpected = sorted(set(charter_edges) - canonical_edges)
        raise ValueError(
            f"{charter}: dependency graph disagrees with canonical model; "
            f"missing={missing}, unexpected={unexpected}"
        )


def validate_dependencies(root: Path) -> None:
    graph_path = root / "editorial/chapter-dependencies.yml"
    try:
        graph = yaml.safe_load(graph_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise ValueError(f"{graph_path}: malformed YAML") from error
    if not isinstance(graph, dict) or graph.get("schema_version") != 1:
        raise ValueError(f"{graph_path}: unsupported dependency graph schema")
    dependencies = graph.get("required_prerequisites")
    if not isinstance(dependencies, dict):
        raise ValueError(f"{graph_path}: required_prerequisites must be a mapping")

    expected_ids = {f"C{number:02d}" for number in range(1, 25)}
    if set(dependencies) != expected_ids:
        raise ValueError(
            f"{graph_path}: chapters must be exactly {sorted(expected_ids)}"
        )

    for dependent, parents in dependencies.items():
        if not isinstance(parents, list):
            raise ValueError(f"{graph_path}: {dependent} prerequisites must be a list")
        validated = [
            validate_reference(parent, dependent, graph_path) for parent in parents
        ]
        if len(validated) != len(set(validated)):
            raise ValueError(f"{graph_path}: duplicate prerequisite for {dependent}")
    validate_charter_dependency_graph(root, dependencies)

    for number in range(1, 25):
        chapter_id = f"C{number:02d}"
        relative = next((root / "book").glob(f"part-*/{number:02d}-*.md"), None)
        if relative is None:
            raise ValueError(f"book: missing chapter {chapter_id}")
        chapter_path = relative
        fa_path = root / "book/fa" / chapter_path.relative_to(root / "book")
        if not fa_path.exists():
            raise ValueError(f"{fa_path}: missing Persian counterpart for {chapter_id}")

        expected = dependencies[chapter_id]
        for locale, path in (("English", chapter_path), ("Persian", fa_path)):
            metadata = front_matter(path)
            actual = metadata.get("prerequisites")
            if not isinstance(actual, list):
                raise ValueError(f"{path}: prerequisites must be a YAML list")
            validated = [
                validate_reference(parent, chapter_id, path) for parent in actual
            ]
            if len(validated) != len(set(validated)):
                raise ValueError(f"{path}: duplicate prerequisite metadata")
            if validated != expected:
                missing = sorted(set(expected) - set(validated))
                unexpected = sorted(set(validated) - set(expected))
                raise ValueError(
                    f"{path}: {locale} prerequisite metadata disagrees with canonical "
                    f"graph for {chapter_id}; missing={missing}, "
                    f"unexpected={unexpected}"
                )

        english = front_matter(chapter_path)["prerequisites"]
        persian = front_matter(fa_path)["prerequisites"]
        if english != persian:
            raise ValueError(
                f"{fa_path}: Persian prerequisites diverge from English for "
                f"{chapter_id}"
            )


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
    chapter = re.search(r"^chapter:\s*(\d+)", front_matter, re.MULTILINE)
    if not chapter:
        raise ValueError(f"{path}: chapter must be numeric")
    number = int(chapter.group(1))
    headings = list(HEADINGS)
    if number == FINAL_CHAPTER:
        headings[headings.index(NEXT_TALE_HEADING)] = CLOSING_HEADING
    positions: list[int] = []
    for heading in headings:
        try:
            positions.append(text.index(heading))
        except ValueError as error:
            raise ValueError(f"{path}: missing heading {heading}") from error
    if positions != sorted(positions):
        raise ValueError(f"{path}: chapter headings are out of contract order")
    words = narrative_words(text)
    if not 400 <= words <= 900:
        raise ValueError(f"{path}: narrative has {words} words; expected 400–900")
    if 'narrative_origin: "original-teaching-fiction"' not in front_matter:
        raise ValueError(f"{path}: narrative origin must identify teaching fiction")
    if number == FINAL_CHAPTER:
        if CLOSING_MARKER not in text:
            raise ValueError(f"{path}: final chapter requires the closing marker")
        if "<!-- next: ch" in text:
            raise ValueError(f"{path}: final chapter must not contain a next-tale hook")
    else:
        if "<!-- next: ch" not in text:
            raise ValueError(f"{path}: missing machine-readable next-tale hook")
        if CLOSING_MARKER in text:
            raise ValueError(
                f"{path}: closing marker is reserved for the final chapter"
            )
    if not re.search(r"## Citations and Further Reading\n\n.+", text, re.DOTALL):
        raise ValueError(f"{path}: citations section is empty")
    slug = re.search(r'^slug:\s*"([^"]+)"', front_matter, re.MULTILINE)
    episode = re.search(r'^narrative_episode:\s*"([^"]+)"', front_matter, re.MULTILINE)
    if not slug or not episode:
        raise ValueError(f"{path}: slug and narrative episode must be quoted")
    if 7 <= number <= 24:
        words = prose_words(text)
        if not 3500 <= words <= 5500:
            raise ValueError(f"{path}: prose has {words} words; expected 3,500–5,500")
    return number, slug.group(1), episode.group(1)


def front_matter_title(path: Path) -> str:
    match = re.search(
        r'^title:\s*"([^"]+)"', path.read_text(encoding="utf-8"), re.MULTILINE
    )
    if not match:
        raise ValueError(f"{path}: missing quoted front-matter title")
    return match.group(1)


def index_heading(path: Path) -> str:
    match = re.search(r"^#\s+(.+)$", path.read_text(encoding="utf-8"), re.MULTILINE)
    if not match:
        raise ValueError(f"{path}: missing H1")
    return match.group(1)


def nav_title(config: Path, index_path: str) -> str:
    # MkDocs configuration intentionally contains a Python-tagged formatter
    # callback. BaseLoader is sufficient for the scalar/list/dict nav shape
    # and never constructs that callback.
    nav = yaml.load(config.read_text(encoding="utf-8"), Loader=yaml.BaseLoader).get(
        "nav", []
    )
    for entry in nav:
        if not isinstance(entry, dict):
            continue
        title, children = next(iter(entry.items()))
        if isinstance(children, list) and index_path in children:
            return str(title)
    raise ValueError(f"{config}: no navigation entry for {index_path}")


def validate_part_titles(root: Path) -> None:
    parts = yaml.safe_load(
        (root / "editorial/part-titles.yml").read_text(encoding="utf-8")
    )["parts"]
    for part, titles in parts.items():
        en_prefix, fa_prefix = PART_PREFIXES[part]
        expected_en = f"{en_prefix} — {titles['en']}"
        expected_fa = f"{fa_prefix} — {titles['fa']}"
        index = f"{part}/index.md"
        en_index = root / "book" / index
        fa_index = root / "book/fa" / index
        for path, expected in ((en_index, expected_en), (fa_index, expected_fa)):
            if front_matter_title(path) != expected or index_heading(path) != expected:
                raise ValueError(f"{path}: title and H1 must match {expected!r}")
        if nav_title(root / "mkdocs.yml", index) != expected_en:
            raise ValueError(f"mkdocs.yml: {index} title must match {expected_en!r}")
        if nav_title(root / "mkdocs.fa.yml", index) != expected_fa:
            raise ValueError(f"mkdocs.fa.yml: {index} title must match {expected_fa!r}")


def main() -> int:
    root = Path(".")
    validate_part_titles(root)
    validate_dependencies(root)
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
