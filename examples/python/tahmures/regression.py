"""Versioned case comparison with protected regression gates."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CaseOutcome:
    case_id: str
    passed: bool
    score: float
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class RegressionPolicy:
    protected_tags: tuple[str, ...] = ()
    allowed_regressions: int = 0
    minimum_candidate_score: float = 0.0


@dataclass(frozen=True)
class RegressionReport:
    passed: bool
    fixed: tuple[str, ...]
    regressed: tuple[str, ...]
    stable_pass: tuple[str, ...]
    stable_fail: tuple[str, ...]
    protected_regressions: tuple[str, ...]
    mean_score_delta: float


def compare_regression(
    baseline: tuple[CaseOutcome, ...],
    candidate: tuple[CaseOutcome, ...],
    policy: RegressionPolicy,
) -> RegressionReport:
    if policy.allowed_regressions < 0 or not 0 <= policy.minimum_candidate_score <= 1:
        raise ValueError("invalid regression policy")
    before = {item.case_id: item for item in baseline}
    after = {item.case_id: item for item in candidate}
    if not before or len(before) != len(baseline) or len(after) != len(candidate):
        raise ValueError("case IDs must be non-empty and unique")
    if set(before) != set(after):
        raise ValueError("baseline and candidate case IDs must match")
    fixed: list[str] = []
    regressed: list[str] = []
    stable_pass: list[str] = []
    stable_fail: list[str] = []
    protected: list[str] = []
    protected_tags = set(policy.protected_tags)
    for case_id in sorted(before):
        old, new = before[case_id], after[case_id]
        if old.passed and not new.passed:
            regressed.append(case_id)
            if set(old.tags) & protected_tags:
                protected.append(case_id)
        elif not old.passed and new.passed:
            fixed.append(case_id)
        elif new.passed:
            stable_pass.append(case_id)
        else:
            stable_fail.append(case_id)
    mean_delta = sum(after[key].score - before[key].score for key in before) / len(
        before
    )
    score_floor = all(
        item.score >= policy.minimum_candidate_score for item in after.values()
    )
    passed = (
        len(regressed) <= policy.allowed_regressions and not protected and score_floor
    )
    return RegressionReport(
        passed,
        tuple(fixed),
        tuple(regressed),
        tuple(stable_pass),
        tuple(stable_fail),
        tuple(protected),
        round(mean_delta, 6),
    )
