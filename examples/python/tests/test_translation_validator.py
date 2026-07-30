from pathlib import Path

import pytest
from markdown import Markdown

from scripts.validate_translations import validate_pair, validate_persian_terminology

SOURCE = Path("book/part-1/01-what-is-a-prompt.md")
TRANSLATION = Path("book/fa/part-1/01-what-is-a-prompt.md")


@pytest.mark.parametrize("chapter", range(1, 13))
def test_committed_persian_translation_passes(chapter: int) -> None:
    part = "part-1" if chapter <= 6 else "part-2"
    source = next(Path(f"book/{part}").glob(f"{chapter:02d}-*.md"))
    translation = Path("book/fa") / part / source.name
    slug, episode = validate_pair(source, translation)
    assert slug
    assert episode


def test_stale_source_hash_is_rejected(tmp_path: Path) -> None:
    changed = tmp_path / TRANSLATION.name
    changed.write_text(
        TRANSLATION.read_text(encoding="utf-8").replace(
            (
                'source_sha256: "39c313c89012e979d6e46b543cc41738'
                'dfc2785872c7f72c27bb7fa7fd51d68b"'
            ),
            f'source_sha256: "{"0" * 64}"',
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
