"""Protect the anchored Chapter 12 reference, not title copies elsewhere."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))

from validate_reference_parity import main

ROOT = Path(__file__).resolve().parents[3]
ARTICLE = "The Probabilistic Relevance Framework: BM25 and Beyond"
PUBLICATION = "Foundations and Trends in Information Retrieval"
ANCHOR = "Robertson, Stephen, and Hugo Zaragoza. 2009."
ENTRY = f"- {ANCHOR} “{ARTICLE}.” *{PUBLICATION}* 3 (4): 333–389.\n"
EN_PATH = Path("book/part-2/12-context-windows-and-attention.md")
FA_PATH = Path("book/fa/part-2/12-context-windows-and-attention.md")
POLICY_PATH = Path("editorial/protected-citation-titles.json")


@pytest.fixture
def repository(tmp_path):
    for path, heading in [
        (EN_PATH, "Citations and Further Reading"),
        (FA_PATH, "منابع و مطالعهٔ بیشتر"),
    ]:
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"# Context\n\n## {heading}\n\n" + ENTRY)
    registry = tmp_path / POLICY_PATH
    registry.parent.mkdir(parents=True)
    registry.write_bytes((ROOT / POLICY_PATH).read_bytes())
    return tmp_path


def check(root, monkeypatch):
    report = root / "report.json"
    monkeypatch.setattr(
        sys,
        "argv",
        ["reference-parity", "--root", str(root), "--json-report", str(report)],
    )
    code = main()
    return code, json.loads(report.read_text())["errors"]


def mutate(root, path, old, new):
    target = root / path
    text = target.read_text()
    assert text.count(old) == 1
    target.write_text(text.replace(old, new))


def test_exact_valid_reference(repository, monkeypatch):
    assert check(repository, monkeypatch) == (0, [])


def test_line_wrapping_and_whitespace(repository, monkeypatch):
    wrapped = ENTRY.replace(
        "Robertson, Stephen, and Hugo", "Robertson, Stephen,\n  and Hugo"
    )
    wrapped = wrapped.replace("Relevance Framework", "Relevance\n  Framework")
    wrapped = wrapped.replace("Information Retrieval", "Information\n  Retrieval")
    for path in [EN_PATH, FA_PATH]:
        mutate(repository, path, ENTRY, wrapped)
    assert check(repository, monkeypatch) == (0, [])


def test_whitespace_at_title_boundaries(repository, monkeypatch):
    spaced = ENTRY.replace(f"“{ARTICLE}.”", f"“\n  {ARTICLE} .\n  ”")
    spaced = spaced.replace(f"*{PUBLICATION}*", f"*\n  {PUBLICATION}\n  *")
    mutate(repository, FA_PATH, ENTRY, spaced)
    assert check(repository, monkeypatch) == (0, [])


def test_terminal_article_period_is_optional(repository, monkeypatch):
    mutate(repository, FA_PATH, f"{ARTICLE}.”", f"{ARTICLE}”")
    assert check(repository, monkeypatch) == (0, [])


@pytest.mark.parametrize("path", [EN_PATH, FA_PATH], ids=["English", "Persian"])
@pytest.mark.parametrize(
    "old,new,field",
    [
        (ARTICLE, ARTICLE.replace("Relevance", "ارتباط"), "article"),
        (PUBLICATION, PUBLICATION.replace("Retrieval", "بازیابی"), "publication"),
    ],
)
def test_original_corruptions_fail(repository, monkeypatch, path, old, new, field):
    mutate(repository, path, old, new)
    code, errors = check(repository, monkeypatch)
    assert code == 1
    assert any(f"{field} title mismatch" in error for error in errors)


@pytest.mark.parametrize("path", [EN_PATH, FA_PATH])
def test_missing_protected_entry(repository, monkeypatch, path):
    mutate(
        repository,
        path,
        ENTRY,
        "- Another author. 2009. “Another article.” *Journal*.\n",
    )
    code, errors = check(repository, monkeypatch)
    assert code == 1 and any("anchor" in error for error in errors)


@pytest.mark.parametrize("path", [EN_PATH, FA_PATH])
def test_duplicate_anchor(repository, monkeypatch, path):
    mutate(repository, path, ENTRY, ENTRY + ENTRY)
    code, errors = check(repository, monkeypatch)
    assert code == 1 and any("anchor" in error for error in errors)


@pytest.mark.parametrize("title", [ARTICLE, PUBLICATION])
def test_correct_decoy_elsewhere_cannot_mask_corruption(repository, monkeypatch, title):
    mutate(repository, FA_PATH, title, "CORRUPTED TITLE")
    path = repository / FA_PATH
    path.write_text(
        f"The canonical titles are {ARTICLE} and {PUBLICATION}.\n\n" + path.read_text()
    )
    code, errors = check(repository, monkeypatch)
    assert code == 1 and any("title mismatch" in error for error in errors)


def test_correct_decoy_in_another_reference_cannot_mask_corruption(
    repository, monkeypatch
):
    mutate(repository, FA_PATH, ARTICLE, "CORRUPTED TITLE")
    path = repository / FA_PATH
    path.write_text(
        path.read_text() + f"- Other Author. 2010. “{ARTICLE}.” *{PUBLICATION}*.\n"
    )
    assert check(repository, monkeypatch)[0] == 1


def test_additional_legitimate_reference_is_allowed(repository, monkeypatch):
    path = repository / FA_PATH
    path.write_text(
        path.read_text()
        + "- Additional Author. 2020. *An additional reference*. https://example.org/additional\n"
    )
    assert check(repository, monkeypatch) == (0, [])


def test_existing_url_identity_check_is_retained(repository, monkeypatch):
    en, fa = repository / EN_PATH, repository / FA_PATH
    en.write_text(
        en.read_text() + "- Another reference. https://example.org/required\n"
    )
    fa.write_text(fa.read_text() + "- Another reference. https://example.org/changed\n")
    code, errors = check(repository, monkeypatch)
    assert code == 1 and any("recognizable citation identities" in e for e in errors)


@pytest.mark.parametrize(
    "old,new",
    [
        (f"“{ARTICLE}.”", ""),
        (f"*{PUBLICATION}*", ""),
        (f"{ARTICLE}.”", f"{ARTICLE}..”"),
        (ARTICLE, ARTICLE.lower()),
        (PUBLICATION, PUBLICATION + "."),
    ],
)
def test_missing_or_changed_title_structure(repository, monkeypatch, old, new):
    mutate(repository, FA_PATH, old, new)
    assert check(repository, monkeypatch)[0] == 1


@pytest.mark.parametrize(
    "registry",
    [
        None,
        [],
        {},
        {"schema_version": 1},
        {"schema_version": True, "references": []},
        {"schema_version": 2, "references": []},
        {"schema_version": 1, "references": []},
        {"schema_version": 1, "references": "wrong"},
        {"schema_version": 1, "references": [None]},
    ],
)
def test_malformed_registry(repository, monkeypatch, registry):
    (repository / POLICY_PATH).write_text(json.dumps(registry))
    code, errors = check(repository, monkeypatch)
    assert code == 1 and any("registry" in error for error in errors)


@pytest.mark.parametrize(
    "field,value",
    [
        ("chapter", True),
        ("chapter", 13),
        ("author_year_anchor", "Other Author. 2009."),
        ("article_title", None),
        ("article_title", "  "),
        ("publication_title", []),
    ],
)
def test_malformed_registry_entry(repository, monkeypatch, field, value):
    path = repository / POLICY_PATH
    registry = json.loads(path.read_text())
    registry["references"][0][field] = value
    path.write_text(json.dumps(registry))
    assert check(repository, monkeypatch)[0] == 1


@pytest.mark.parametrize(
    "raw", ["{", '{"schema_version":1,"schema_version":1,"references":[]}']
)
def test_invalid_registry_json(repository, monkeypatch, raw):
    (repository / POLICY_PATH).write_text(raw)
    code, errors = check(repository, monkeypatch)
    assert code == 1 and any("registry" in error for error in errors)


def test_missing_registry_fails_closed(repository, monkeypatch):
    (repository / POLICY_PATH).unlink()
    assert check(repository, monkeypatch)[0] == 1


def test_corruption_in_both_editions_still_fails(repository, monkeypatch):
    for path in [EN_PATH, FA_PATH]:
        mutate(repository, path, ARTICLE, "WRONG BUT SHARED TITLE")
    code, errors = check(repository, monkeypatch)
    assert code == 1 and len(errors) == 2


def test_missing_canonical_chapter_fails(repository, monkeypatch):
    (repository / EN_PATH).unlink()
    assert check(repository, monkeypatch)[0] == 1


def test_committed_registry_has_only_approved_titles():
    assert json.loads((ROOT / POLICY_PATH).read_text()) == {
        "schema_version": 1,
        "references": [
            {
                "chapter": 12,
                "author_year_anchor": ANCHOR,
                "article_title": ARTICLE,
                "publication_title": PUBLICATION,
            }
        ],
    }
