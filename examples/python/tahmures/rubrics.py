"""Anchored, multi-reviewer rubrics for accountable offline evaluation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RubricCriterion:
    criterion_id: str
    weight: float
    minimum: int
    anchors: tuple[str, str, str, str, str]
    disqualifying: bool = False

    def __post_init__(self) -> None:
        if not self.criterion_id or self.weight <= 0 or not 0 <= self.minimum <= 4:
            raise ValueError("invalid rubric criterion")


@dataclass(frozen=True)
class RubricReview:
    reviewer_id: str
    scores: dict[str, int]
    rationale: str


@dataclass(frozen=True)
class RubricResult:
    passed: bool
    weighted_score: float
    criterion_means: dict[str, float]
    reviewer_scores: dict[str, float]
    disagreement: float
    disqualifying_failures: tuple[str, ...]
    requires_adjudication: bool


class Rubric:
    def __init__(
        self,
        criteria: tuple[RubricCriterion, ...],
        pass_threshold: float,
        disagreement_threshold: float,
    ) -> None:
        if not criteria or len({item.criterion_id for item in criteria}) != len(
            criteria
        ):
            raise ValueError("rubric criteria must be non-empty and unique")
        if not 0 <= pass_threshold <= 1 or not 0 <= disagreement_threshold <= 1:
            raise ValueError("rubric thresholds must be between zero and one")
        self.criteria = criteria
        self.pass_threshold = pass_threshold
        self.disagreement_threshold = disagreement_threshold

    def evaluate(self, reviews: tuple[RubricReview, ...]) -> RubricResult:
        if not reviews or len({item.reviewer_id for item in reviews}) != len(reviews):
            raise ValueError("reviews must have unique reviewer IDs")
        criterion_ids = {item.criterion_id for item in self.criteria}
        for review in reviews:
            if not review.reviewer_id or not review.rationale:
                raise ValueError("review identity and rationale are required")
            if set(review.scores) != criterion_ids:
                raise ValueError("review scores must match rubric criteria exactly")
            if any(
                isinstance(score, bool)
                or not isinstance(score, int)
                or not 0 <= score <= 4
                for score in review.scores.values()
            ):
                raise ValueError("rubric scores must be integers from zero to four")
        total_weight = sum(item.weight for item in self.criteria)
        reviewer_scores = {
            review.reviewer_id: sum(
                review.scores[item.criterion_id] * item.weight for item in self.criteria
            )
            / (4 * total_weight)
            for review in reviews
        }
        criterion_means = {
            item.criterion_id: sum(
                review.scores[item.criterion_id] for review in reviews
            )
            / len(reviews)
            for item in self.criteria
        }
        failures = tuple(
            item.criterion_id
            for item in self.criteria
            if item.disqualifying
            and any(
                review.scores[item.criterion_id] < item.minimum for review in reviews
            )
        )
        weighted = sum(reviewer_scores.values()) / len(reviewer_scores)
        disagreement = max(reviewer_scores.values()) - min(reviewer_scores.values())
        adjudication = bool(failures) or disagreement > self.disagreement_threshold
        return RubricResult(
            passed=weighted >= self.pass_threshold and not adjudication,
            weighted_score=round(weighted, 6),
            criterion_means={k: round(v, 6) for k, v in criterion_means.items()},
            reviewer_scores={k: round(v, 6) for k, v in reviewer_scores.items()},
            disagreement=round(disagreement, 6),
            disqualifying_failures=failures,
            requires_adjudication=adjudication,
        )
