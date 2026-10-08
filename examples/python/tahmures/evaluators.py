"""Small, inspectable evaluators used by the offline experiments."""

from __future__ import annotations

import json
import re
from typing import Protocol

from tahmures.contracts import FieldContract, OutputContract
from tahmures.types import (
    EvaluationResult,
    EvaluatorSpec,
    ExperimentCase,
    GenerationResponse,
    JSONValue,
)


class Evaluator(Protocol):
    name: str

    def evaluate(
        self, case: ExperimentCase, response: GenerationResponse
    ) -> EvaluationResult: ...


def _strings(value: JSONValue) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        return []
    return list(value)


class ClassificationEvaluator:
    def __init__(self, spec: EvaluatorSpec) -> None:
        self.name = spec.name

    def evaluate(
        self, case: ExperimentCase, response: GenerationResponse
    ) -> EvaluationResult:
        expected = str(case.expected.get("label", "")).strip().casefold()
        actual = response.text.strip().casefold()
        passed = bool(expected) and actual == expected
        return EvaluationResult(
            evaluator=self.name,
            passed=passed,
            score=float(passed),
            metrics={"accuracy": float(passed)},
            reason=f"expected {expected!r}; received {actual!r}",
        )


class TermsEvaluator:
    def __init__(self, spec: EvaluatorSpec, forbidden: bool) -> None:
        self.name = spec.name
        self._forbidden = forbidden

    def evaluate(
        self, case: ExperimentCase, response: GenerationResponse
    ) -> EvaluationResult:
        key = "forbidden_terms" if self._forbidden else "required_terms"
        terms = _strings(case.expected.get(key))
        text = response.text.casefold()
        matches = [term for term in terms if term.casefold() in text]
        if not terms:
            score = 1.0
        elif self._forbidden:
            score = 1.0 - (len(matches) / len(terms))
        else:
            score = len(matches) / len(terms)
        passed = score == 1.0
        return EvaluationResult(
            evaluator=self.name,
            passed=passed,
            score=score,
            metrics={self.name: score},
            reason=f"{'matched' if self._forbidden else 'found'}: {matches}",
        )


class EvidenceEvaluator:
    _citation = re.compile(r"\[([A-Z][A-Z0-9_-]*)\]")

    def __init__(self, spec: EvaluatorSpec) -> None:
        self.name = spec.name

    def evaluate(
        self, case: ExperimentCase, response: GenerationResponse
    ) -> EvaluationResult:
        allowed = set(_strings(case.expected.get("allowed_evidence")))
        citations = set(self._citation.findall(response.text))
        answerable = bool(case.expected.get("answerable", True))
        abstained = any(
            phrase.casefold() in response.text.casefold()
            for phrase in _strings(case.expected.get("abstain_phrases"))
        )
        if answerable:
            passed = bool(citations) and citations <= allowed and not abstained
        else:
            passed = abstained and not citations
        return EvaluationResult(
            evaluator=self.name,
            passed=passed,
            score=float(passed),
            metrics={
                "valid_evidence": float(bool(citations) and citations <= allowed),
                "appropriate_abstention": float(abstained == (not answerable)),
                "unsupported_claim": float(not passed),
            },
            reason=(
                f"citations={sorted(citations)}; answerable={answerable}; "
                f"abstained={abstained}"
            ),
        )


class JSONFieldsEvaluator:
    def __init__(self, spec: EvaluatorSpec) -> None:
        self.name = spec.name

    def evaluate(
        self, case: ExperimentCase, response: GenerationResponse
    ) -> EvaluationResult:
        required = _strings(case.expected.get("required_fields"))
        try:
            value = json.loads(response.text)
            fields = set(value) if isinstance(value, dict) else set()
        except json.JSONDecodeError:
            fields = set()
        score = (
            1.0 if not required else len(fields.intersection(required)) / len(required)
        )
        passed = score == 1.0
        return EvaluationResult(
            evaluator=self.name,
            passed=passed,
            score=score,
            metrics={"output_contract": score},
            reason=f"required={required}; fields={sorted(fields)}",
        )


class JSONContractEvaluator:
    def __init__(self, spec: EvaluatorSpec) -> None:
        self.name = spec.name

    def evaluate(
        self, case: ExperimentCase, response: GenerationResponse
    ) -> EvaluationResult:
        required = _strings(case.expected.get("required_fields"))
        type_map = case.expected.get("field_types", {})
        allowed_map = case.expected.get("allowed_values", {})
        if not isinstance(type_map, dict) or not isinstance(allowed_map, dict):
            raise ValueError("json_contract expectations must be objects")
        names = set(required) | set(type_map) | set(allowed_map)
        fields = []
        for name in sorted(names):
            field_type = type_map.get(name, "string")
            allowed = allowed_map.get(name, [])
            if not isinstance(field_type, str) or not isinstance(allowed, list):
                raise ValueError("invalid json_contract field definition")
            fields.append(
                FieldContract(
                    name=name,
                    value_type=field_type,
                    required=name in required,
                    allowed_values=tuple(allowed),
                )
            )
        contract = OutputContract(
            tuple(fields),
            allow_extra=bool(case.expected.get("allow_extra", False)),
        )
        result = contract.validate(response.text)
        metrics = {
            "parse_rate": float(result.parsed),
            "structural_validity": float(result.valid),
            "invalid_acceptance": float(result.valid and bool(result.violations)),
        }
        return EvaluationResult(
            evaluator=self.name,
            passed=result.valid,
            score=float(result.valid),
            metrics=metrics,
            reason="valid"
            if result.valid
            else "; ".join(v.message for v in result.violations),
        )


class WorkflowTraceEvaluator:
    def __init__(self, spec: EvaluatorSpec) -> None:
        self.name = spec.name

    def evaluate(
        self, case: ExperimentCase, response: GenerationResponse
    ) -> EvaluationResult:
        required = _strings(case.expected.get("required_stages"))
        required_checkpoints = set(_strings(case.expected.get("required_checkpoints")))
        try:
            value = json.loads(response.text)
            stages = value.get("stages", []) if isinstance(value, dict) else []
        except json.JSONDecodeError:
            stages = []
        ids = [
            stage.get("id")
            for stage in stages
            if isinstance(stage, dict) and isinstance(stage.get("id"), str)
        ]
        known: set[str] = set()
        dependencies_valid = True
        terminal_count = 0
        checkpoints: set[str] = set()
        for stage in stages:
            if not isinstance(stage, dict):
                dependencies_valid = False
                continue
            dependencies = stage.get("depends_on", [])
            if not isinstance(dependencies, list) or any(
                not isinstance(item, str) or item not in known for item in dependencies
            ):
                dependencies_valid = False
            stage_id = stage.get("id")
            if isinstance(stage_id, str):
                known.add(stage_id)
                if stage.get("checkpoint") is True:
                    checkpoints.add(stage_id)
            terminal_count += int(stage.get("terminal") is True)
        coverage = (
            1.0 if not required else len(set(ids) & set(required)) / len(required)
        )
        checkpoint_rate = (
            1.0
            if not required_checkpoints
            else len(checkpoints & required_checkpoints) / len(required_checkpoints)
        )
        terminal_valid = terminal_count == 1
        passed = (
            coverage == 1.0
            and dependencies_valid
            and checkpoint_rate == 1.0
            and terminal_valid
        )
        return EvaluationResult(
            evaluator=self.name,
            passed=passed,
            score=float(passed),
            metrics={
                "required_stage_coverage": coverage,
                "dependency_validity": float(dependencies_valid),
                "checkpoint_presence": checkpoint_rate,
                "terminal_state_correctness": float(terminal_valid),
            },
            reason=(
                f"stages={ids}; dependencies_valid={dependencies_valid}; "
                f"terminal_count={terminal_count}"
            ),
        )


class AllowedChoiceEvaluator:
    def __init__(self, spec: EvaluatorSpec) -> None:
        self.name = spec.name

    def evaluate(
        self, case: ExperimentCase, response: GenerationResponse
    ) -> EvaluationResult:
        allowed = set(_strings(case.expected.get("allowed_choices")))
        selected = response.text.strip()
        try:
            value = json.loads(response.text)
            if isinstance(value, dict) and isinstance(value.get("selected"), str):
                selected = value["selected"]
        except json.JSONDecodeError:
            pass
        passed = selected in allowed
        return EvaluationResult(
            evaluator=self.name,
            passed=passed,
            score=float(passed),
            metrics={
                "allowed_choice": float(passed),
                "selection_stability": float(
                    selected == case.expected.get("preferred_choice", selected)
                ),
            },
            reason=f"selected={selected!r}; allowed={sorted(allowed)}",
        )


class RubricMetadataEvaluator:
    def __init__(self, spec: EvaluatorSpec) -> None:
        self.name = spec.name

    def evaluate(
        self, case: ExperimentCase, response: GenerationResponse
    ) -> EvaluationResult:
        minima = case.expected.get("rubric_minima", {})
        scores = response.metadata.get("rubric_scores", {})
        if not isinstance(minima, dict) or not isinstance(scores, dict):
            minima, scores = {}, {}
        metrics: dict[str, float] = {}
        passed = bool(minima)
        for criterion, minimum in minima.items():
            score = scores.get(criterion)
            valid = (
                isinstance(minimum, (int, float))
                and not isinstance(minimum, bool)
                and isinstance(score, (int, float))
                and not isinstance(score, bool)
            )
            numeric = float(score) if valid else 0.0
            metrics[f"rubric_{criterion}"] = numeric
            passed = passed and valid and numeric >= float(minimum)
        disagreement = response.metadata.get("reviewer_disagreement", 0.0)
        if isinstance(disagreement, (int, float)) and not isinstance(
            disagreement, bool
        ):
            metrics["reviewer_disagreement"] = float(disagreement)
        metrics["rubric_threshold"] = float(passed)
        return EvaluationResult(
            evaluator=self.name,
            passed=passed,
            score=float(passed),
            metrics=metrics,
            reason=f"committed human scores={scores}; minima={minima}",
        )


def _json_object(text: str) -> dict[str, JSONValue]:
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


class ContextPackageEvaluator:
    def __init__(self, spec: EvaluatorSpec) -> None:
        self.name = spec.name

    def evaluate(
        self, case: ExperimentCase, response: GenerationResponse
    ) -> EvaluationResult:
        value = _json_object(response.text)
        selected = set(_strings(value.get("selected")))
        excluded = set(_strings(value.get("excluded")))
        required = set(_strings(case.expected.get("required_selected")))
        forbidden = set(_strings(case.expected.get("forbidden_selected")))
        required_rate = len(selected & required) / max(1, len(required))
        forbidden_rate = len(selected & forbidden) / max(1, len(forbidden))
        exclusions_reported = forbidden <= excluded
        passed = required_rate == 1 and forbidden_rate == 0 and exclusions_reported
        return EvaluationResult(
            self.name,
            passed,
            float(passed),
            {
                "mandatory_retention": required_rate,
                "irrelevant_inclusion": forbidden_rate,
                "exclusion_reporting": float(exclusions_reported),
            },
            f"selected={sorted(selected)}; excluded={sorted(excluded)}",
        )


class RetrievalQualityEvaluator:
    def __init__(self, spec: EvaluatorSpec) -> None:
        self.name = spec.name

    def evaluate(
        self, case: ExperimentCase, response: GenerationResponse
    ) -> EvaluationResult:
        retrieved = _strings(_json_object(response.text).get("retrieved"))
        relevant = set(_strings(case.expected.get("relevant_ids")))
        stale = set(_strings(case.expected.get("stale_ids")))
        found = set(retrieved)
        recall = len(found & relevant) / max(1, len(relevant))
        precision = len(found & relevant) / max(1, len(found))
        rank = next(
            (
                index
                for index, item in enumerate(retrieved, start=1)
                if item in relevant
            ),
            0,
        )
        reciprocal_rank = 1 / rank if rank else 0.0
        stale_rate = len(found & stale) / max(1, len(stale))
        passed = recall == 1 and stale_rate == 0
        return EvaluationResult(
            self.name,
            passed,
            float(passed),
            {
                "recall_at_k": recall,
                "precision_at_k": precision,
                "reciprocal_rank": reciprocal_rank,
                "stale_retrieval": stale_rate,
            },
            f"retrieved={retrieved}; relevant={sorted(relevant)}",
        )


class MemoryStateEvaluator:
    def __init__(self, spec: EvaluatorSpec) -> None:
        self.name = spec.name

    def evaluate(
        self, case: ExperimentCase, response: GenerationResponse
    ) -> EvaluationResult:
        recalled = set(_strings(_json_object(response.text).get("recalled")))
        active = set(_strings(case.expected.get("active_ids")))
        forbidden = set(_strings(case.expected.get("forbidden_ids")))
        recall = len(recalled & active) / max(1, len(active))
        leakage = len(recalled & forbidden) / max(1, len(forbidden))
        passed = recall == 1 and leakage == 0
        return EvaluationResult(
            self.name,
            passed,
            float(passed),
            {"active_memory_recall": recall, "forbidden_memory_use": leakage},
            f"recalled={sorted(recalled)}",
        )


class ToolAuthorizationEvaluator:
    def __init__(self, spec: EvaluatorSpec) -> None:
        self.name = spec.name

    def evaluate(
        self, case: ExperimentCase, response: GenerationResponse
    ) -> EvaluationResult:
        value = _json_object(response.text)
        expected_allowed = bool(case.expected.get("allowed"))
        expected_reason = str(case.expected.get("reason", ""))
        allowed = value.get("allowed") is True
        reason = str(value.get("reason", ""))
        passed = allowed == expected_allowed and reason == expected_reason
        return EvaluationResult(
            self.name,
            passed,
            float(passed),
            {
                "authorization_accuracy": float(passed),
                "unauthorized_execution": float(allowed and not expected_allowed),
            },
            f"allowed={allowed}; reason={reason}",
        )


class AgentTraceEvaluator:
    def __init__(self, spec: EvaluatorSpec) -> None:
        self.name = spec.name

    def evaluate(
        self, case: ExperimentCase, response: GenerationResponse
    ) -> EvaluationResult:
        value = _json_object(response.text)
        status = str(value.get("status", ""))
        reason = str(value.get("reason", ""))
        post_terminal = int(value.get("post_terminal_actions", 0) or 0)
        passed = (
            status == case.expected.get("status")
            and reason == case.expected.get("reason")
            and post_terminal == 0
        )
        return EvaluationResult(
            self.name,
            passed,
            float(passed),
            {
                "terminal_state_correctness": float(passed),
                "post_terminal_action_rate": float(post_terminal > 0),
            },
            f"status={status}; reason={reason}; post_terminal={post_terminal}",
        )


class HandoffContractEvaluator:
    def __init__(self, spec: EvaluatorSpec) -> None:
        self.name = spec.name

    def evaluate(
        self, case: ExperimentCase, response: GenerationResponse
    ) -> EvaluationResult:
        value = _json_object(response.text)
        required = set(_strings(case.expected.get("required_fields")))
        fields = set(value)
        field_rate = len(fields & required) / max(1, len(required))
        goal_valid = value.get("goal_version") == case.expected.get("goal_version")
        allowed = set(_strings(case.expected.get("allowed_actions")))
        actions = set(_strings(value.get("permitted_next_actions")))
        authority_valid = bool(value.get("authority"))
        passed = (
            field_rate == 1 and goal_valid and actions <= allowed and authority_valid
        )
        return EvaluationResult(
            self.name,
            passed,
            float(passed),
            {
                "required_field_coverage": field_rate,
                "goal_version_validity": float(goal_valid),
                "authority_preservation": float(authority_valid),
                "unsafe_action": float(not actions <= allowed),
            },
            f"fields={sorted(fields)}; actions={sorted(actions)}",
        )


class PhaseFourPolicyEvaluator:
    """Compare structured policy outcomes while exposing chapter-specific metrics."""

    def __init__(self, spec: EvaluatorSpec) -> None:
        self.name = spec.name
        self.kind = spec.type

    def evaluate(
        self, case: ExperimentCase, response: GenerationResponse
    ) -> EvaluationResult:
        value = _json_object(response.text)
        expected = case.expected
        if self.kind == "anchored_rubric":
            keys = ("passed", "requires_adjudication", "disqualified")
            metrics = {
                "rubric_decision_accuracy": float(
                    all(value.get(k) == expected.get(k) for k in keys)
                ),
                "adjudication_accuracy": float(
                    value.get("requires_adjudication")
                    == expected.get("requires_adjudication")
                ),
            }
        elif self.kind == "regression_gate":
            regressions = set(_strings(value.get("regressed")))
            expected_regressions = set(_strings(expected.get("regressed")))
            keys = ("passed",)
            metrics = {
                "gate_accuracy": float(value.get("passed") == expected.get("passed")),
                "regression_detection": float(regressions == expected_regressions),
            }
        elif self.kind == "trust_boundary":
            keys = ()
            metrics = {
                "trusted_instruction_accuracy": float(
                    set(_strings(value.get("instructions")))
                    == set(_strings(expected.get("instructions")))
                ),
                "untrusted_override_rate": float(
                    bool(
                        set(_strings(value.get("instructions")))
                        & set(_strings(expected.get("untrusted_ids")))
                    )
                ),
                "quarantine_accuracy": float(
                    set(_strings(value.get("rejected")))
                    == set(_strings(expected.get("rejected")))
                ),
            }
        elif self.kind == "approval_policy":
            keys = ("allowed", "reason")
            metrics = {
                "authorization_accuracy": float(
                    all(value.get(k) == expected.get(k) for k in keys)
                ),
                "unauthorized_execution": float(
                    bool(value.get("allowed")) and not bool(expected.get("allowed"))
                ),
            }
        elif self.kind == "operational_drift":
            keys = ("passed",)
            metrics = {
                "drift_decision_accuracy": float(
                    value.get("passed") == expected.get("passed")
                ),
                "finding_recall": _set_match_rate(
                    _strings(expected.get("findings")), _strings(value.get("findings"))
                ),
                "version_attribution": _version_attribution(
                    expected.get("changed_versions"), value.get("changed_versions")
                ),
            }
        else:
            keys = ("primary", "human_review")
            metrics = {
                "control_selection_accuracy": float(
                    all(value.get(k) == expected.get(k) for k in keys)
                ),
                "prompt_as_hard_control": float(
                    value.get("primary") == "language_model"
                    and bool(expected.get("hard_control", False))
                ),
            }
        key_match = all(value.get(key) == expected.get(key) for key in keys)
        passed = (
            key_match
            and all(
                metric == 1.0
                for name, metric in metrics.items()
                if name
                not in {
                    "untrusted_override_rate",
                    "unauthorized_execution",
                    "prompt_as_hard_control",
                }
            )
            and all(
                metrics.get(name, 0.0) == 0.0
                for name in (
                    "untrusted_override_rate",
                    "unauthorized_execution",
                    "prompt_as_hard_control",
                )
                if name in metrics
            )
        )
        return EvaluationResult(
            self.name,
            passed,
            float(passed),
            metrics,
            f"expected={expected}; received={value}",
        )


def _version_attribution(expected: JSONValue, actual: JSONValue) -> float:
    """Exact string-set agreement; malformed arrays cannot count as empty sets."""
    if not isinstance(expected, list) or not isinstance(actual, list):
        return 0.0
    if not all(
        isinstance(item, str) for values in (expected, actual) for item in values
    ):
        return 0.0
    return float(set(expected) == set(actual))


def _set_match_rate(expected: list[str], actual: list[str]) -> float:
    wanted, found = set(expected), set(actual)
    return 1.0 if not wanted else len(wanted & found) / len(wanted)


def build_evaluator(spec: EvaluatorSpec) -> Evaluator:
    if spec.type == "classification":
        return ClassificationEvaluator(spec)
    if spec.type == "required_terms":
        return TermsEvaluator(spec, forbidden=False)
    if spec.type == "forbidden_terms":
        return TermsEvaluator(spec, forbidden=True)
    if spec.type == "evidence":
        return EvidenceEvaluator(spec)
    if spec.type == "json_fields":
        return JSONFieldsEvaluator(spec)
    if spec.type == "json_contract":
        return JSONContractEvaluator(spec)
    if spec.type == "workflow_trace":
        return WorkflowTraceEvaluator(spec)
    if spec.type == "allowed_choice":
        return AllowedChoiceEvaluator(spec)
    if spec.type == "rubric_metadata":
        return RubricMetadataEvaluator(spec)
    if spec.type == "context_package":
        return ContextPackageEvaluator(spec)
    if spec.type == "retrieval_quality":
        return RetrievalQualityEvaluator(spec)
    if spec.type == "memory_state":
        return MemoryStateEvaluator(spec)
    if spec.type == "tool_authorization":
        return ToolAuthorizationEvaluator(spec)
    if spec.type == "agent_trace":
        return AgentTraceEvaluator(spec)
    if spec.type == "handoff_contract":
        return HandoffContractEvaluator(spec)
    if spec.type in {
        "anchored_rubric",
        "regression_gate",
        "trust_boundary",
        "approval_policy",
        "operational_drift",
        "control_selection",
    }:
        return PhaseFourPolicyEvaluator(spec)
    raise ValueError(f"unsupported evaluator type: {spec.type}")
