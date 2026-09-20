#!/usr/bin/env python3
"""Validate the complete Persian edition against canonical English sources."""

from __future__ import annotations

import hashlib
import re
import unicodedata
from pathlib import Path

CHAPTER_TITLES = {
    1: "پرامپت چیست؟",
    2: "مدل‌ها، معنا و عدم‌قطعیت",
    3: "نیازمندی‌ها پیش از واژه‌پردازی",
    4: "کالبدشناسی یک پرامپت قابل‌اعتماد",
    5: "سلسله‌مراتب دستورها و تعارض",
    6: "یادگیری از مثال‌ها",
    7: "قالب‌های بازاستفاده‌پذیر پرامپت",
    8: "خروجی‌های ساخت‌یافته و قراردادها",
    9: "تجزیه و گردش‌کارها",
    10: "واریانس، انتخاب و کنترل",
    11: "طراحی برای خلاقیت",
    12: "پنجره‌های کانتکست و توجه",
    13: "مهندسی کانتکست",
    14: "تولید تقویت‌شده با بازیابی (RAG)",
    15: "حافظه و وضعیت",
    16: "ابزارها و مجوزها",
    17: "عامل‌ها و خاتمه",
    18: "واگذاری‌ها و سامانه‌های چندمرحله‌ای",
    19: "ارزیابی و معیارنامه‌ها",
    20: "آزمون رگرسیون برای سامانه‌های مبتنی بر پرامپت",
    21: "تزریق پرامپت و مرزهای اعتماد",
    22: "تأییدها، قابلیت‌ها و اقدام‌های پیامددار",
    23: "عملیات محیط تولید و رانش",
    24: "فراتر از پرامپت: انتخاب سازوکار کنترل مناسب",
}
EPISODE_TITLES = {
    1: "سه خوانش",
    2: "آینه و پیمان گمشده",
    3: "پل پنج فضیلت",
    4: "نامه‌ای درون دفتر",
    5: "مُهرها بر فراز مُهرها",
    6: "چهار مثال و مثال پنجم",
    7: "فرمانی با مُهرهای خالی",
    8: "سی فهرست",
    9: "کوه در یک فرمان",
    10: "شورای چندصدا",
    11: "باغی که هرگز نروییده بود",
    12: "فرمانی که آغاز خود را فراموش کرد",
    13: "The Archive That Answered Everything",
    14: "The Correct Answer from the Wrong Tablet",
    15: "Spring Remembered in Winter",
    16: "Permission to Inspect",
    17: "The Messenger Who Continued",
    18: "The Broken Relay",
    19: "دادگاه بی‌وزنه",
    20: "فرمانی که در یک آزمون پیروز شد",
    21: "لوح نجواگر",
    22: "کلیدی که همهٔ درها را گشود",
    23: "گویشی که در سپیده‌دم تغییر کرد",
    24: "قفلی که هیچ جمله‌ای نگهش نداشت",
}
FRONT_MATTER_KEYS = (
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
    "language:",
    "translation_of:",
    "source_sha256:",
    "translation_status:",
    "last_translated:",
)
HEADINGS = (
    "## اهداف یادگیری",
    "## روایت تهمورث",
    "### صحنه",
    "### درخواست",
    "### نتیجهٔ غیرمنتظره",
    "### کشف",
    "### از روایت تا مهندسی",
    "## مسئلهٔ مهندسی",
    "## مدل ذهنی",
    "## مفاهیم اصلی",
    "## الگوی پرامپت",
    "## تلاش خام",
    "## تحلیل شکست",
    "## طراحی بهبودیافته",
    "## مثال حل‌شده",
    "## آزمایش",
    "## ارزیابی",
    "## کارگاه پیاده‌سازی",
    "### Python",
    "### Go",
    "## حالت‌های شکست",
    "## ملاحظات امنیتی",
    "## ملاحظات عملیاتی",
    "## بده‌بستان‌ها",
    "## چه زمانی پرامپت پاسخ مسئله نیست",
    "## تمرین‌ها",
    "## خلاصهٔ فصل",
    "## روایت بعدی",
    "## منابع و مطالعهٔ بیشتر",
)
EXECUTABLE_FENCES = {"python", "go", "bash", "json"}
WORD_PATTERN = re.compile(r"[^\W_]+(?:\u200c[^\W_]+)*", re.UNICODE)
FENCE_PATTERN = re.compile(r"^```([^\n]*)\n(.*?)^```\s*$", re.MULTILINE | re.DOTALL)
HTTP_PATTERN = re.compile(r"https?://[^)\s]+")
INLINE_CODE_PATTERN = re.compile(r"`[^`\n]*`")
HTML_COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)
MARKDOWN_DESTINATION_PATTERN = re.compile(r"\]\([^)]*\)")
LATIN_TERM_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_-])[A-Za-z][A-Za-z0-9]*(?:[-_][A-Za-z0-9]+)*"
    r"(?![A-Za-z0-9_-])"
)
PERSIAN_LETTER_PATTERN = r"[\u0621-\u063a\u0641-\u064a\u0671-\u06d3\u06fa-\u06fc]"
GLOSSARY_DEFINITION_PATTERN = re.compile(r"^\*\[([^\]]+)\]:\s*(.+)$", re.MULTILINE)
GLOSSARY_PATH = Path("includes/fa-abbreviations.md")
REFERENCES_HEADING = "## منابع و مطالعهٔ بیشتر"
ORDINARY_LATIN_TERMS = {
    "allowed",
    "application",
    "caller",
    "check",
    "cost",
    "deterministic",
    "missing",
    "output",
    "production",
    "rate",
    "rejected",
    "result",
    "review",
    "source",
    "stable",
    "status",
    "structured",
    "task",
    "test",
    "validate",
}


def _field(front_matter: str, name: str) -> str:
    match = re.search(rf'^{re.escape(name)}:\s*"([^"]+)"', front_matter, re.MULTILINE)
    if not match:
        raise ValueError(f"missing quoted front matter field {name}")
    return match.group(1)


def _words(text: str) -> int:
    return len(WORD_PATTERN.findall(text))


def _body_without_code(text: str) -> str:
    body = text.split("---\n", 2)[2]
    return FENCE_PATTERN.sub("", body)


def _fences(text: str) -> list[tuple[str, str]]:
    return [
        (match.group(1).strip(), match.group(2))
        for match in FENCE_PATTERN.finditer(text)
    ]


def _glossary_terms() -> set[str]:
    definitions = GLOSSARY_DEFINITION_PATTERN.findall(
        GLOSSARY_PATH.read_text(encoding="utf-8")
    )
    if not definitions:
        raise ValueError(f"{GLOSSARY_PATH}: no abbreviation definitions found")
    terms = [term for term, _ in definitions]
    if len(terms) != len(set(terms)):
        raise ValueError(f"{GLOSSARY_PATH}: duplicate abbreviation definition")
    return set(terms)


def _terminology_prose(text: str) -> str:
    if text.startswith("---\n") and text.count("---\n") >= 2:
        text = text.split("---\n", 2)[2]
    if REFERENCES_HEADING in text:
        text = text.split(REFERENCES_HEADING, 1)[0]
    text = FENCE_PATTERN.sub("", text)
    text = HTML_COMMENT_PATTERN.sub("", text)
    text = INLINE_CODE_PATTERN.sub("", text)
    text = HTTP_PATTERN.sub("", text)
    text = MARKDOWN_DESTINATION_PATTERN.sub("]", text)
    return re.sub(r"^\s*!!!\s+[A-Za-z][A-Za-z0-9_-]*", "", text, flags=re.MULTILINE)


def validate_persian_terminology(text: str, path: Path) -> None:
    if path.name == "translation-glossary.md":
        return
    prose = _terminology_prose(text)
    terms = _glossary_terms()
    attached = sorted(
        term
        for term in terms
        if re.search(
            rf"(?<![A-Za-z0-9_-]){re.escape(term)}{PERSIAN_LETTER_PATTERN}",
            prose,
        )
    )
    if attached:
        joined = ", ".join(attached)
        raise ValueError(
            f"{path}: glossary terms need a ZWNJ before Persian suffixes: {joined}"
        )
    for term in sorted(terms, key=len, reverse=True):
        prose = re.sub(
            rf"(?<![A-Za-z0-9_-]){re.escape(term)}(?![A-Za-z0-9_-])",
            "",
            prose,
        )
    unapproved = sorted(
        set(LATIN_TERM_PATTERN.findall(prose)) & ORDINARY_LATIN_TERMS,
        key=str.casefold,
    )
    if unapproved:
        joined = ", ".join(unapproved)
        raise ValueError(f"{path}: unapproved Latin prose terms: {joined}")


def validate_pair(source: Path, translation: Path) -> tuple[str, str]:
    source_text = source.read_text(encoding="utf-8")
    text = translation.read_text(encoding="utf-8")
    if unicodedata.normalize("NFC", text) != text:
        raise ValueError(f"{translation}: text is not NFC-normalised")
    if any(character in text for character in ("ي", "ك")):
        raise ValueError(f"{translation}: contains Arabic yeh or kaf")
    validate_persian_terminology(text, translation)
    if not text.startswith("---\n") or text.count("---\n") < 2:
        raise ValueError(f"{translation}: missing YAML front matter")
    front_matter = text.split("---\n", 2)[1]
    for key in FRONT_MATTER_KEYS:
        if key not in front_matter:
            raise ValueError(f"{translation}: missing front matter key {key}")

    chapter_match = re.search(r"^chapter:\s*(\d+)", front_matter, re.MULTILINE)
    if not chapter_match:
        raise ValueError(f"{translation}: chapter must be numeric")
    chapter = int(chapter_match.group(1))
    if chapter not in CHAPTER_TITLES:
        raise ValueError(f"{translation}: unexpected Persian chapter {chapter}")
    title = _field(front_matter, "title")
    episode = _field(front_matter, "narrative_episode")
    slug = _field(front_matter, "slug")
    if title != CHAPTER_TITLES[chapter]:
        raise ValueError(f"{translation}: incorrect Persian chapter title")
    if episode != EPISODE_TITLES[chapter]:
        raise ValueError(f"{translation}: incorrect Persian episode title")
    if _field(front_matter, "narrative_origin") != "original-teaching-fiction":
        raise ValueError(f"{translation}: incorrect narrative origin")
    if _field(front_matter, "language") != "fa":
        raise ValueError(f"{translation}: language must be fa")
    part_name = source.parent.name
    if part_name not in {"part-1", "part-2", "part-3", "part-4"}:
        raise ValueError(f"{source}: source must belong to part-1 through part-4")
    expected_source = f"{part_name}/{source.name}"
    if _field(front_matter, "translation_of") != expected_source:
        raise ValueError(f"{translation}: translation_of must be {expected_source}")
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    if _field(front_matter, "source_sha256") != source_hash:
        raise ValueError(f"{translation}: source_sha256 is stale")

    positions = []
    for heading in HEADINGS:
        try:
            positions.append(text.index(heading))
        except ValueError as error:
            raise ValueError(f"{translation}: missing heading {heading}") from error
    if positions != sorted(positions):
        raise ValueError(f"{translation}: Persian headings are out of contract order")
    if f"# {title}\n" not in text:
        raise ValueError(f"{translation}: H1 does not match title")

    narrative = text[text.index("### صحنه") : text.index("### از روایت تا مهندسی")]
    narrative_count = _words(narrative)
    if not 400 <= narrative_count <= 900:
        raise ValueError(
            f"{translation}: narrative has {narrative_count} words; expected 400–900"
        )
    clean_translation = _body_without_code(text)
    clean_source = _body_without_code(source_text)
    persian_letters = len(re.findall(r"[\u0600-\u06ff]", clean_translation))
    latin_letters = len(re.findall(r"[A-Za-z]", clean_translation))
    script_ratio = persian_letters / max(1, persian_letters + latin_letters)
    if script_ratio < 0.60:
        raise ValueError(
            f"{translation}: Persian-script ratio {script_ratio:.3f} is too low"
        )
    coverage_ratio = _words(clean_translation) / max(1, _words(clean_source))
    if not 0.65 <= coverage_ratio <= 1.40:
        raise ValueError(
            f"{translation}: source coverage ratio {coverage_ratio:.3f} is implausible"
        )

    source_fences = _fences(source_text)
    translated_fences = _fences(text)
    if [language for language, _ in source_fences] != [
        language for language, _ in translated_fences
    ]:
        raise ValueError(f"{translation}: fenced-block languages or order changed")
    for index, ((language, source_body), (_, translated_body)) in enumerate(
        zip(source_fences, translated_fences, strict=True), start=1
    ):
        if language in EXECUTABLE_FENCES and source_body != translated_body:
            raise ValueError(
                f"{translation}: executable {language} fence {index} changed"
            )

    source_urls = set(HTTP_PATTERN.findall(source_text))
    translation_urls = set(HTTP_PATTERN.findall(text))
    if not source_urls <= translation_urls:
        raise ValueError(f"{translation}: source citation URLs were removed")
    expected_hook = f"<!-- next: ch{chapter + 1:02d} -->"
    if expected_hook not in text:
        raise ValueError(f"{translation}: expected hook {expected_hook}")
    return slug, episode


def main() -> int:
    for path in sorted(Path("book/fa").rglob("*.md")):
        validate_persian_terminology(path.read_text(encoding="utf-8"), path)

    sources = sorted(
        [
            *Path("book/part-1").glob("0[1-6]-*.md"),
            *Path("book/part-2").glob("0[7-9]-*.md"),
            *Path("book/part-2").glob("1[0-2]-*.md"),
            *Path("book/part-3").glob("1[3-8]-*.md"),
            *Path("book/part-4").glob("19-*.md"),
            *Path("book/part-4").glob("2[0-4]-*.md"),
        ]
    )
    translations = sorted(
        [
            *Path("book/fa/part-1").glob("0[1-6]-*.md"),
            *Path("book/fa/part-2").glob("0[7-9]-*.md"),
            *Path("book/fa/part-2").glob("1[0-2]-*.md"),
            *Path("book/fa/part-3").glob("1[3-8]-*.md"),
            *Path("book/fa/part-4").glob("19-*.md"),
            *Path("book/fa/part-4").glob("2[0-4]-*.md"),
        ]
    )
    if len(sources) != 24 or len(translations) != 24:
        raise SystemExit(
            f"expected 24 source and 24 Persian chapters; "
            f"found {len(sources)} and {len(translations)}"
        )
    if [path.name for path in sources] != [path.name for path in translations]:
        raise SystemExit("Persian/source chapter filenames do not match")
    slugs: set[str] = set()
    episodes: set[str] = set()
    for source, translation in zip(sources, translations, strict=True):
        try:
            slug, episode = validate_pair(source, translation)
        except ValueError as error:
            raise SystemExit(str(error)) from error
        if slug in slugs or episode in episodes:
            raise SystemExit(f"{translation}: duplicate slug or episode title")
        slugs.add(slug)
        episodes.add(episode)
        print(f"{translation}: valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
