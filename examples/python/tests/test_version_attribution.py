"""D27 exact-set attribution without changes to other evaluator metrics."""

import json
from dataclasses import asdict
from pathlib import Path

import pytest
from tahmures.evaluators import build_evaluator
from tahmures.types import EvaluatorSpec, ExperimentCase, GenerationResponse

CORPUS = json.loads(
    (Path(__file__).parents[2] / "shared/version_attribution_cases.json").read_text()
)
assert CORPUS["schema_version"] == 1


@pytest.mark.parametrize("case", CORPUS["cases"], ids=lambda case: case["id"])
def test_shared_complete_attribution_result(case):
    evaluator = build_evaluator(EvaluatorSpec("operational_drift", "operational_drift"))
    result = evaluator.evaluate(
        ExperimentCase(case["id"], {}, case["expected"]),
        GenerationResponse(case["response"], "fixture"),
    )
    assert asdict(result) == case["result_python"]
    assert set(result.metrics) == {
        "drift_decision_accuracy",
        "finding_recall",
        "version_attribution",
    }


@pytest.mark.parametrize("invalid", [None, (), ("prompt",), "prompt", {"prompt"}])
def test_malformed_native_expected_attribution(invalid):
    evaluator = build_evaluator(EvaluatorSpec("drift", "operational_drift"))
    result = evaluator.evaluate(
        ExperimentCase(
            "native", {}, {"passed": True, "findings": [], "changed_versions": invalid}
        ),
        GenerationResponse(
            '{"passed":true,"findings":[],"changed_versions":[]}', "fixture"
        ),
    )
    assert not result.passed and result.score == 0.0
    assert result.metrics == {
        "drift_decision_accuracy": 1.0,
        "finding_recall": 1.0,
        "version_attribution": 0.0,
    }


def test_finding_recall_still_allows_false_extras():
    # D27 changes attribution only, not this existing recall contract.
    evaluator = build_evaluator(EvaluatorSpec("drift", "operational_drift"))
    result = evaluator.evaluate(
        ExperimentCase(
            "finding_extras",
            {},
            {
                "passed": False,
                "findings": ["cost_slo"],
                "changed_versions": ["prompt"],
            },
        ),
        GenerationResponse(
            json.dumps(
                {
                    "passed": False,
                    "findings": ["cost_slo", "invented_finding"],
                    "changed_versions": ["prompt"],
                }
            ),
            "fixture",
        ),
    )
    assert result.passed
    assert result.metrics["finding_recall"] == 1.0


def test_partial_finding_credit_is_preserved():
    evaluator = build_evaluator(EvaluatorSpec("drift", "operational_drift"))
    result = evaluator.evaluate(
        ExperimentCase(
            "partial_findings",
            {},
            {
                "passed": False,
                "findings": ["cost_slo", "quality_drift"],
                "changed_versions": ["prompt"],
            },
        ),
        GenerationResponse(
            '{"passed":false,"findings":["cost_slo"],"changed_versions":["prompt"]}',
            "fixture",
        ),
    )
    assert not result.passed and result.score == 0.0
    assert result.metrics["finding_recall"] == 0.5
    assert result.metrics["version_attribution"] == 1.0
