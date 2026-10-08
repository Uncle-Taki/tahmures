import re
from pathlib import Path

import pytest
from markdown import Markdown

import scripts.validate_translations as translation_validator
from scripts.validate_chapters import validate as validate_chapter
from scripts.validate_translations import validate_pair, validate_persian_terminology

SOURCE = Path("book/part-1/01-what-is-a-prompt.md")
TRANSLATION = Path("book/fa/part-1/01-what-is-a-prompt.md")
SOURCE_10 = Path("book/part-2/10-variance-choice-and-control.md")
TRANSLATION_10 = Path("book/fa/part-2/10-variance-choice-and-control.md")


@pytest.mark.parametrize("chapter", range(1, 25))
def test_committed_persian_translation_passes(chapter: int) -> None:
    part = (
        "part-1"
        if chapter <= 6
        else "part-2"
        if chapter <= 12
        else "part-3"
        if chapter <= 18
        else "part-4"
    )
    source = next(Path(f"book/{part}").glob(f"{chapter:02d}-*.md"))
    translation = Path("book/fa") / part / source.name
    slug, episode = validate_pair(source, translation)
    assert slug
    assert episode


def test_part_three_uses_persian_title_and_preserves_episode() -> None:
    source = Path("book/part-3/13-context-engineering.md")
    translation = Path("book/fa/part-3/13-context-engineering.md")
    slug, episode = validate_pair(source, translation)
    assert slug == "context-engineering"
    assert episode == "The Archive That Answered Everything"


def test_part_four_uses_persian_title_and_episode() -> None:
    source = Path("book/part-4/19-evaluation-and-rubrics.md")
    translation = Path("book/fa/part-4/19-evaluation-and-rubrics.md")
    slug, episode = validate_pair(source, translation)
    assert slug == "evaluation-and-rubrics"
    assert episode == "دادگاه بی‌وزنه"


def test_stale_source_hash_is_rejected(tmp_path: Path) -> None:
    changed = tmp_path / TRANSLATION.name
    changed.write_text(
        re.sub(
            r'^source_sha256: "[0-9a-f]{64}"$',
            f'source_sha256: "{"0" * 64}"',
            TRANSLATION.read_text(encoding="utf-8"),
            count=1,
            flags=re.MULTILINE,
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="source_sha256 is stale"):
        validate_pair(SOURCE, changed)


def test_changed_executable_fence_is_rejected(tmp_path: Path) -> None:
    changed = tmp_path / TRANSLATION.name
    changed.write_text(
        TRANSLATION.read_text(encoding="utf-8").replace(
            "response = client.generate(request)",
            "response = other_client.generate(request)",
            1,
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="executable python fence"):
        validate_pair(SOURCE, changed)


def test_arabic_codepoint_is_rejected(tmp_path: Path) -> None:
    changed = tmp_path / TRANSLATION.name
    changed.write_text(
        TRANSLATION.read_text(encoding="utf-8").replace("می‌توانید", "مي‌توانید", 1),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="Arabic yeh or kaf"):
        validate_pair(SOURCE, changed)


def test_approved_domain_term_is_allowed() -> None:
    validate_persian_terminology(
        "هر case یک ورودی مستقل برای ارزیابی است.",
        Path("example.md"),
    )


def test_approved_domain_term_renders_with_persian_tooltip() -> None:
    rendered = Markdown(extensions=["abbr"]).convert(
        "هر case یک ورودی مستقل است و `case` یک شناسهٔ لفظی است.\n\n"
        "*[case]: مورد آزمایشی؛ یک ورودی مستقل برای اجرا و ارزیابی"
    )
    assert '<abbr title="مورد آزمایشی؛ یک ورودی مستقل برای اجرا و ارزیابی">' in (
        rendered
    )
    assert "<code>case</code>" in rendered


def test_unapproved_ordinary_english_is_rejected() -> None:
    with pytest.raises(ValueError, match=r"unapproved Latin prose terms: production"):
        validate_persian_terminology(
            "این روش برای production آماده نیست.",
            Path("example.md"),
        )


def test_machine_readable_english_is_exempt() -> None:
    validate_persian_terminology(
        (
            "مقدار `production` را بررسی کنید.\n\n"
            "```json\n"
            '{"status": "production"}\n'
            "```\n\n"
            "[منبع](https://example.com/production)"
        ),
        Path("example.md"),
    )


def test_glossary_term_requires_zwnj_before_persian_suffix() -> None:
    with pytest.raises(ValueError, match="need a ZWNJ"):
        validate_persian_terminology(
            "caseها را اجرا کنید.",
            Path("example.md"),
        )
    validate_persian_terminology(
        "case‌ها را اجرا کنید؛ هر case، مستقل است.",
        Path("example.md"),
    )


def _tale_text(text: str) -> str:
    start = text.index("### صحنه")
    end = text.index("### از روایت تا مهندسی")
    short_tale = (
        "### صحنه\n\nمتن کوتاه.\n\n"
        "### درخواست\n\nمتن کوتاه.\n\n"
        "### نتیجهٔ غیرمنتظره\n\nمتن کوتاه.\n\n"
        "### کشف\n\nمتن کوتاه.\n\n"
    )
    return text[:start] + short_tale + text[end:]


def _english_short_tale(text: str) -> str:
    start = text.index("### The Setting")
    end = text.index("### From Tale to Engineering")
    short_tale = (
        "### The Setting\n\nShort text.\n\n"
        "### The Request\n\nShort text.\n\n"
        "### The Unexpected Result\n\nShort text.\n\n"
        "### The Discovery\n\nShort text.\n\n"
    )
    return text[:start] + short_tale + text[end:]


def _chapter_10_exception() -> dict:
    english = SOURCE_10.read_text(encoding="utf-8")
    narrative = english[
        english.index("### The Setting") : english.index("### From Tale to Engineering")
    ]
    persian = TRANSLATION_10.read_text(encoding="utf-8")
    fa_narrative = persian[
        persian.index("### صحنه") : persian.index("### از روایت تا مهندسی")
    ]
    return {
        "persian_tale_word_count": translation_validator._words(fa_narrative),
        "frozen_english_tale_word_count": len(
            translation_validator.ENGLISH_WORD_PATTERN.findall(narrative)
        ),
        "reason": "faithful Persian compression under review",
        "parity_reviewed": True,
        "no_unsupported_addition": True,
    }


def test_english_tale_below_floor_still_fails(tmp_path: Path) -> None:
    changed = tmp_path / SOURCE.name
    changed.write_text(
        _english_short_tale(SOURCE.read_text(encoding="utf-8")), encoding="utf-8"
    )
    with pytest.raises(ValueError, match="expected 400–900"):
        validate_chapter(changed)


def test_persian_tale_below_floor_without_exception_fails(tmp_path: Path) -> None:
    changed = tmp_path / TRANSLATION.name
    changed.write_text(
        _tale_text(TRANSLATION.read_text(encoding="utf-8")), encoding="utf-8"
    )
    with pytest.raises(ValueError, match="expected 400–900"):
        validate_pair(SOURCE, changed)


def test_reviewed_below_floor_persian_tale_passes() -> None:
    slug, episode = validate_pair(SOURCE_10, TRANSLATION_10)
    assert slug == "variance-choice-and-control"
    assert episode == "شورای چندصدا"


def test_tale_length_exception_does_not_bypass_source_hash(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    changed = tmp_path / TRANSLATION_10.name
    changed.write_text(
        re.sub(
            r'^source_sha256: "[0-9a-f]{64}"$',
            f'source_sha256: "{"0" * 64}"',
            TRANSLATION_10.read_text(encoding="utf-8"),
            count=1,
            flags=re.MULTILINE,
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        translation_validator,
        "_tale_length_exceptions",
        lambda root: {"10": _chapter_10_exception()},
    )
    with pytest.raises(ValueError, match="source_sha256 is stale"):
        validate_pair(SOURCE_10, changed)


def test_tale_length_exception_does_not_bypass_executable_fence(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    body = TRANSLATION_10.read_text(encoding="utf-8")
    fence = next(
        block
        for language, block in translation_validator._fences(body)
        if language == "python"
    )
    changed = tmp_path / TRANSLATION_10.name
    changed.write_text(
        body.replace(fence, fence.replace("item.id", "item.name", 1), 1),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        translation_validator,
        "_tale_length_exceptions",
        lambda root: {"10": _chapter_10_exception()},
    )
    with pytest.raises(ValueError, match="executable python fence"):
        validate_pair(SOURCE_10, changed)


def test_tale_length_exception_pins_reviewed_word_count(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    changed = tmp_path / TRANSLATION_10.name
    changed.write_text(TRANSLATION_10.read_text(encoding="utf-8"), encoding="utf-8")
    exception = _chapter_10_exception()
    exception["persian_tale_word_count"] += 1
    monkeypatch.setattr(
        translation_validator,
        "_tale_length_exceptions",
        lambda root: {"10": exception},
    )
    with pytest.raises(ValueError, match="re-review"):
        validate_pair(SOURCE_10, changed)


def test_stale_tale_length_exception_is_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    changed = tmp_path / TRANSLATION.name
    changed.write_text(TRANSLATION.read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.setattr(
        translation_validator,
        "_tale_length_exceptions",
        lambda root: {"1": _chapter_10_exception()},
    )
    with pytest.raises(ValueError, match="stale tale-length exception"):
        validate_pair(SOURCE, changed)
