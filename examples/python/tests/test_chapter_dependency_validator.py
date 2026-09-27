import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))

from validate_chapters import validate_reference


def test_chapter_dependency_reference_requires_canonical_notation() -> None:
    assert validate_reference("C01", "C02", Path("graph.yml")) == "C01"
    with pytest.raises(ValueError, match="malformed prerequisite"):
        validate_reference("Chapter 1", "C02", Path("graph.yml"))


def test_chapter_dependency_reference_rejects_forward_edge() -> None:
    with pytest.raises(ValueError, match="forward prerequisite"):
        validate_reference("C03", "C03", Path("graph.yml"))
