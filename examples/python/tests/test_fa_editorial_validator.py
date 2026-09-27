import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))

from validate_fa_editorial import LATIN_BEFORE_FA_NOUN_RE


def test_ezafe_ordered_latin_stage_is_not_a_mixed_phrase_warning() -> None:
    assert LATIN_BEFORE_FA_NOUN_RE.search("interpolation مرحلهٔ دوم") is None


def test_unordered_latin_stage_remains_a_mixed_phrase_warning() -> None:
    assert LATIN_BEFORE_FA_NOUN_RE.search("interpolation مرحله بعدی")


def test_persian_predicate_prefix_is_not_a_mixed_phrase_warning() -> None:
    assert LATIN_BEFORE_FA_NOUN_RE.search("requirements پاسخگو نیست") is None


def test_complete_persian_noun_remains_a_mixed_phrase_warning() -> None:
    assert LATIN_BEFORE_FA_NOUN_RE.search("requirements پاسخ ندارد")
