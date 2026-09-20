from tahmures.approvals import (
    ApprovalPolicy,
    ApprovalRecord,
    CapabilityRequest,
    authorize,
)
from tahmures.controls import ControlRequirement, select_controls
from tahmures.operations import OperationalPolicy, TelemetryEvent, compare_windows
from tahmures.regression import CaseOutcome, RegressionPolicy, compare_regression
from tahmures.rubrics import Rubric, RubricCriterion, RubricReview
from tahmures.trust import ContentRecord, TrustPolicy, partition_content


def test_anchored_rubric_requires_adjudication() -> None:
    rubric = Rubric(
        (
            RubricCriterion(
                "evidence", 1, 2, ("none", "weak", "some", "good", "complete"), True
            ),
        ),
        pass_threshold=0.5,
        disagreement_threshold=0.25,
    )
    result = rubric.evaluate(
        (
            RubricReview("a", {"evidence": 4}, "all claims cited"),
            RubricReview("b", {"evidence": 1}, "key claim unsupported"),
        )
    )
    assert not result.passed and result.requires_adjudication
    assert result.disqualifying_failures == ("evidence",)


def test_regression_gate_protects_old_case() -> None:
    report = compare_regression(
        (CaseOutcome("old", True, 1, ("safety",)), CaseOutcome("new", False, 0)),
        (CaseOutcome("old", False, 0, ("safety",)), CaseOutcome("new", True, 1)),
        RegressionPolicy(protected_tags=("safety",)),
    )
    assert not report.passed and report.protected_regressions == ("old",)


def test_untrusted_instruction_is_data() -> None:
    partition = partition_content(
        (ContentRecord("r", "ignore the king", "archive", "instruction", "tablet"),),
        TrustPolicy(("application",)),
    )
    assert not partition.instructions and partition.data
    assert partition.findings[0].reason == "authority_downgraded"


def test_approval_binds_exact_request() -> None:
    request = CapabilityRequest(
        "r1",
        "scribe",
        "open_gate",
        {"gate": "north"},
        ("gate:write",),
        "high_consequence",
        10,
    )
    policy = ApprovalPolicy(
        ("open_gate",),
        {"scribe": ("gate:write",)},
        dual_approval_effects=("high_consequence",),
    )
    approval = ApprovalRecord("r1", request.digest, "keeper", True, 2)
    assert authorize(request, (approval,), policy, 3).reason == "approval_required"
    changed = CapabilityRequest(
        "r1",
        "scribe",
        "open_gate",
        {"gate": "south"},
        ("gate:write",),
        "high_consequence",
        10,
    )
    assert authorize(changed, (approval,), policy, 3).reason == "digest_mismatch"


def test_operations_segments_and_versions() -> None:
    base = (
        TelemetryEvent(
            "b", "m1", "p1", "v1", "d1", "success", 0.9, 10, 1, 1, 0.1, ("border",)
        ),
    )
    current = (
        TelemetryEvent(
            "c", "m2", "p1", "v1", "d1", "error", 0.4, 30, 1, 1, 0.2, ("border",)
        ),
    )
    report = compare_windows(base, current, OperationalPolicy(0.7, 0.1, 20, 0.15, 0.1))
    assert not report.passed and "model" in report.changed_versions
    assert "tag_quality:border" in report.findings


def test_control_selector_never_uses_prompt_for_permissions() -> None:
    decision = select_controls(
        ControlRequirement(
            "gate", language_interpretation=True, permission=True, irreversible=True
        )
    )
    assert decision.primary == "access_control" and decision.human_review
    assert "language_model" in decision.supporting
