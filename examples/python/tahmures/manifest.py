"""Load and validate the shared JSON v1 experiment files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tahmures.types import (
    EvaluatorSpec,
    ExperimentCase,
    FixtureRecord,
    GenerationResponse,
    Manifest,
    PromptVariant,
)


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read JSON file {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise ValueError(f"cannot read JSONL file {path}: {error}") from error
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"invalid JSON at {path}:{number}: {error}") from error
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{number} must contain a JSON object")
        records.append(value)
    return records


def load_manifest(path: str | Path) -> Manifest:
    raw = _read_json(Path(path))
    if raw.get("schema_version") != 1:
        raise ValueError("only experiment schema_version 1 is supported")
    variants = tuple(
        PromptVariant(id=item["id"], template_path=item["template_path"])
        for item in raw.get("prompt_variants", [])
    )
    evaluators = tuple(
        EvaluatorSpec(
            name=item["name"],
            type=item["type"],
            threshold=float(item.get("threshold", 1.0)),
        )
        for item in raw.get("evaluators", [])
    )
    if not variants:
        raise ValueError("manifest needs at least one prompt variant")
    if len({variant.id for variant in variants}) != len(variants):
        raise ValueError("prompt variant IDs must be unique")
    if not evaluators:
        raise ValueError("manifest needs at least one evaluator")
    trials = int(raw.get("trials", 1))
    if trials < 1:
        raise ValueError("trials must be positive")
    return Manifest(
        schema_version=1,
        chapter=int(raw["chapter"]),
        experiment_id=str(raw["experiment_id"]),
        description=str(raw["description"]),
        dataset=str(raw["dataset"]),
        fixtures=str(raw["fixtures"]),
        prompt_variants=variants,
        evaluators=evaluators,
        trials=trials,
    )


def load_cases(path: str | Path) -> tuple[ExperimentCase, ...]:
    records = _read_jsonl(Path(path))
    cases = tuple(
        ExperimentCase(
            case_id=str(item["case_id"]),
            input=dict(item["input"]),
            expected=dict(item["expected"]),
            tags=tuple(item.get("tags", [])),
        )
        for item in records
    )
    if not cases:
        raise ValueError("dataset cannot be empty")
    if len({case.case_id for case in cases}) != len(cases):
        raise ValueError("dataset case IDs must be unique")
    return cases


def load_fixtures(path: str | Path) -> tuple[FixtureRecord, ...]:
    records = _read_jsonl(Path(path))
    fixtures = tuple(
        FixtureRecord(
            case_id=str(item["case_id"]),
            variant_id=str(item["variant_id"]),
            trial=int(item["trial"]),
            response=GenerationResponse(
                text=str(item["response"]["text"]),
                model_id=str(item["response"].get("model_id", "fixture-v1")),
                finish_reason=str(item["response"].get("finish_reason", "stop")),
                usage={
                    key: int(value)
                    for key, value in item["response"].get("usage", {}).items()
                },
                metadata=dict(item["response"].get("metadata", {})),
            ),
        )
        for item in records
    )
    keys = [(item.case_id, item.variant_id, item.trial) for item in fixtures]
    if len(set(keys)) != len(keys):
        raise ValueError("fixture keys must be unique")
    return fixtures


def resolve_project_path(manifest_path: str | Path, value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate
    current = Path(manifest_path).resolve().parent
    for parent in (current, *current.parents):
        if (parent / "pyproject.toml").exists():
            return parent / candidate
    return Path.cwd() / candidate
