import json

import pytest
from tahmures.manifest import load_cases, load_manifest


def test_loads_committed_manifest() -> None:
    manifest = load_manifest("experiments/manifests/ch01-prompt-roles.json")
    assert manifest.schema_version == 1
    assert manifest.chapter == 1
    assert len(manifest.prompt_variants) == 2


def test_rejects_unknown_schema(tmp_path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps({"schema_version": 2}), encoding="utf-8")
    with pytest.raises(ValueError, match="schema_version 1"):
        load_manifest(path)


def test_rejects_duplicate_case_ids(tmp_path) -> None:
    path = tmp_path / "cases.jsonl"
    record = {"case_id": "same", "input": {}, "expected": {}}
    path.write_text(
        f"{json.dumps(record)}\n{json.dumps(record)}\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="unique"):
        load_cases(path)
