import json

import pytest
from tahmures.evaluators import build_evaluator
from tahmures.types import (
    EvaluatorSpec,
    ExperimentCase,
    GenerationResponse,
)


def response(text: str) -> GenerationResponse:
    return GenerationResponse(text=text, model_id="fixture-v1")


def test_classification_evaluator() -> None:
    evaluator = build_evaluator(EvaluatorSpec("intent_accuracy", "classification"))
    case = ExperimentCase("one", {}, {"label": "record"})
    assert evaluator.evaluate(case, response("record")).passed
    assert not evaluator.evaluate(case, response("task")).passed


def test_evidence_evaluator_handles_answer_and_abstention() -> None:
    evaluator = build_evaluator(EvaluatorSpec("grounding", "evidence"))
    answerable = ExperimentCase(
        "one",
        {},
        {
            "answerable": True,
            "allowed_evidence": ["E1"],
            "abstain_phrases": ["insufficient evidence"],
        },
    )
    missing = ExperimentCase(
        "two",
        {},
        {
            "answerable": False,
            "allowed_evidence": [],
            "abstain_phrases": ["insufficient evidence"],
        },
    )
    assert evaluator.evaluate(answerable, response("The gate closed [E1].")).passed
    assert evaluator.evaluate(missing, response("Insufficient evidence.")).passed


def test_json_fields_evaluator() -> None:
    evaluator = build_evaluator(EvaluatorSpec("contract", "json_fields"))
    case = ExperimentCase("one", {}, {"required_fields": ["action", "reason"]})
    assert evaluator.evaluate(
        case, response('{"action":"wait","reason":"conflict"}')
    ).passed


@pytest.mark.parametrize(
    ("kind", "expected", "payload"),
    [
        (
            "context_package",
            {"required_selected": ["rule"], "forbidden_selected": ["noise"]},
            {"selected": ["rule"], "excluded": ["noise"]},
        ),
        (
            "retrieval_quality",
            {"relevant_ids": ["CURRENT"], "stale_ids": ["OLD"]},
            {"retrieved": ["CURRENT"]},
        ),
        (
            "memory_state",
            {"active_ids": ["winter"], "forbidden_ids": ["spring"]},
            {"recalled": ["winter"]},
        ),
        (
            "tool_authorization",
            {"allowed": False, "reason": "approval_required"},
            {"allowed": False, "reason": "approval_required"},
        ),
        (
            "agent_trace",
            {"status": "cancelled", "reason": "cancelled"},
            {
                "status": "cancelled",
                "reason": "cancelled",
                "post_terminal_actions": 0,
            },
        ),
        (
            "handoff_contract",
            {
                "required_fields": [
                    "goal_version",
                    "authority",
                    "permitted_next_actions",
                ],
                "goal_version": 3,
                "allowed_actions": ["inspect"],
            },
            {
                "goal_version": 3,
                "authority": "gatekeeper",
                "permitted_next_actions": ["inspect"],
            },
        ),
    ],
)
def test_phase3_evaluators(
    kind: str,
    expected: dict[str, object],
    payload: dict[str, object],
) -> None:
    evaluator = build_evaluator(EvaluatorSpec(kind, kind))
    case = ExperimentCase(kind, {}, expected)
    assert evaluator.evaluate(case, response(json.dumps(payload))).passed
