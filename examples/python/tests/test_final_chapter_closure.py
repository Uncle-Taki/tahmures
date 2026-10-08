"""D19: the final chapter closes the book instead of teasing a next chapter."""

import hashlib
from pathlib import Path

import pytest

from scripts.validate_chapters import validate
from scripts.validate_translations import (
    CHAPTER_TITLES,
    EPISODE_TITLES,
    FA_CLOSING_HEADING,
    FA_NEXT_TALE_HEADING,
    HEADINGS,
    validate_pair,
)

EN_FINAL = Path("book/part-4/24-beyond-prompting-choosing-the-right-control.md")
EN_PRE_FINAL = Path("book/part-4/23-production-operations-and-drift.md")
FA_FINAL = Path("book/fa/part-4/24-beyond-prompting-choosing-the-right-control.md")
FA_FIRST = Path("book/fa/part-1/01-what-is-a-prompt.md")
EN_FIRST = Path("book/part-1/01-what-is-a-prompt.md")

PERSIAN_SENTENCE = (
    "این روایت آزمون ساختاری اعتبارسنجی است و نگهبانان فصل پایانی را می‌سنجد."
)
ENGLISH_SENTENCE = "This synthetic source body exists only to size the coverage ratio."


def _write_copy(tmp_path: Path, source: Path, text: str) -> Path:
    target = tmp_path / source.name
    target.write_text(text, encoding="utf-8")
    return target


def test_final_chapter_requires_closing_marker(tmp_path: Path) -> None:
    text = EN_FINAL.read_text(encoding="utf-8").replace("<!-- closing -->\n", "")
    with pytest.raises(ValueError, match="final chapter requires the closing marker"):
        validate(_write_copy(tmp_path, EN_FINAL, text))


def test_final_chapter_rejects_next_tale_hook(tmp_path: Path) -> None:
    text = EN_FINAL.read_text(encoding="utf-8").replace(
        "<!-- closing -->", "<!-- closing -->\n\n<!-- next: ch25 -->"
    )
    with pytest.raises(
        ValueError, match="final chapter must not contain a next-tale hook"
    ):
        validate(_write_copy(tmp_path, EN_FINAL, text))


def test_final_chapter_requires_closing_heading(tmp_path: Path) -> None:
    text = EN_FINAL.read_text(encoding="utf-8").replace(
        "## The Practice Continues", "## The Next Tale"
    )
    with pytest.raises(ValueError, match="missing heading ## The Practice Continues"):
        validate(_write_copy(tmp_path, EN_FINAL, text))


def test_non_final_chapter_rejects_closing_marker(tmp_path: Path) -> None:
    text = EN_PRE_FINAL.read_text(encoding="utf-8").replace(
        "<!-- next: ch24 -->", "<!-- next: ch24 -->\n\n<!-- closing -->"
    )
    with pytest.raises(
        ValueError, match="closing marker is reserved for the final chapter"
    ):
        validate(_write_copy(tmp_path, EN_PRE_FINAL, text))


def test_non_final_chapter_still_requires_next_hook(tmp_path: Path) -> None:
    text = EN_PRE_FINAL.read_text(encoding="utf-8").replace("<!-- next: ch24 -->", "")
    with pytest.raises(ValueError, match="missing machine-readable next-tale hook"):
        validate(_write_copy(tmp_path, EN_PRE_FINAL, text))


def test_persian_non_final_chapter_rejects_closing_marker(tmp_path: Path) -> None:
    text = FA_FIRST.read_text(encoding="utf-8").replace(
        "<!-- next: ch02 -->", "<!-- next: ch02 -->\n\n<!-- closing -->"
    )
    with pytest.raises(
        ValueError, match="closing marker is reserved for the final chapter"
    ):
        validate_pair(EN_FIRST, _write_copy(tmp_path, FA_FIRST, text))


def test_final_chapter_marker_parity_between_editions() -> None:
    english = EN_FINAL.read_text(encoding="utf-8")
    persian = FA_FINAL.read_text(encoding="utf-8")
    assert "## The Practice Continues" in english
    assert FA_CLOSING_HEADING in persian
    assert "<!-- closing -->" in english
    assert "<!-- closing -->" in persian
    assert "<!-- next: ch" not in english
    assert "<!-- next: ch" not in persian


def _synthetic_final_chapter_pair(
    tmp_path: Path, *, closing: bool, next_hook: bool, closing_heading: bool = True
) -> tuple[Path, Path]:
    part = tmp_path / "part-4"
    part.mkdir()
    source = part / "24-test-final-chapter.md"
    source.write_text(
        "---\nchapter: 24\n---\n\n" + "\n\n".join([ENGLISH_SENTENCE] * 70) + "\n",
        encoding="utf-8",
    )
    digest = hashlib.sha256(source.read_bytes()).hexdigest()

    headings = [
        FA_CLOSING_HEADING if heading == FA_NEXT_TALE_HEADING else heading
        for heading in HEADINGS
    ]
    if not closing_heading:
        headings[headings.index(FA_CLOSING_HEADING)] = FA_NEXT_TALE_HEADING

    body = [f"# {CHAPTER_TITLES[24]}\n"]
    narrative = "\n\n".join([PERSIAN_SENTENCE] * 40)
    for heading in headings:
        body.append(f"{heading}\n")
        if heading == "### صحنه":
            body.append(f"{narrative}\n")
        else:
            body.append(f"{PERSIAN_SENTENCE}\n")
        if heading == FA_CLOSING_HEADING and closing:
            body.append("<!-- closing -->\n")
        if heading == FA_CLOSING_HEADING and next_hook:
            body.append("<!-- next: ch25 -->\n")

    front_matter = (
        "---\n"
        f'title: "{CHAPTER_TITLES[24]}"\n'
        'slug: "test-final-chapter"\n'
        "chapter: 24\n"
        'part: "بخش چهار"\n'
        'summary: "آزمون ساختاری فصل پایانی."\n'
        'maturity: "draft"\n'
        'last_reviewed: "2026-09-28"\n'
        f'narrative_episode: "{EPISODE_TITLES[24]}"\n'
        'narrative_origin: "original-teaching-fiction"\n'
        "learning_objectives:\n"
        '  - "آزمون ساختاری فصل پایانی"\n'
        "prerequisites: [C23]\n"
        'language: "fa"\n'
        'translation_of: "part-4/24-test-final-chapter.md"\n'
        f'source_sha256: "{digest}"\n'
        'translation_status: "draft"\n'
        'last_translated: "2026-09-28"\n'
        "---\n\n"
    )
    translation = part / "24-test-final-chapter-fa.md"
    translation.write_text(front_matter + "\n".join(body), encoding="utf-8")
    return source, translation


def test_persian_final_chapter_accepts_closing(tmp_path: Path) -> None:
    source, translation = _synthetic_final_chapter_pair(
        tmp_path, closing=True, next_hook=False
    )
    slug, episode = validate_pair(source, translation)
    assert slug == "test-final-chapter"
    assert episode == EPISODE_TITLES[24]


def test_persian_final_chapter_requires_closing_marker(tmp_path: Path) -> None:
    source, translation = _synthetic_final_chapter_pair(
        tmp_path, closing=False, next_hook=False
    )
    with pytest.raises(ValueError, match="expected closing marker"):
        validate_pair(source, translation)


def test_persian_final_chapter_rejects_next_hook(tmp_path: Path) -> None:
    source, translation = _synthetic_final_chapter_pair(
        tmp_path, closing=True, next_hook=True
    )
    with pytest.raises(ValueError, match="final chapter must not contain a next hook"):
        validate_pair(source, translation)


def test_persian_final_chapter_requires_closing_heading(tmp_path: Path) -> None:
    source, translation = _synthetic_final_chapter_pair(
        tmp_path, closing=True, next_hook=False, closing_heading=False
    )
    with pytest.raises(ValueError, match="missing heading"):
        validate_pair(source, translation)
