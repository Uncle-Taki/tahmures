"""Deterministic summaries and drift findings for synthetic telemetry."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class TelemetryEvent:
    run_id: str
    model_id: str
    prompt_version: str
    policy_version: str
    dataset_version: str
    outcome: str
    quality: float
    latency_ms: int
    input_tokens: int
    output_tokens: int
    cost_units: float
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class OperationalPolicy:
    minimum_quality: float
    maximum_error_rate: float
    maximum_p95_latency_ms: int
    maximum_mean_cost: float
    quality_drift: float


@dataclass(frozen=True)
class WindowSummary:
    count: int
    mean_quality: float
    error_rate: float
    p95_latency_ms: int
    mean_cost: float


@dataclass(frozen=True)
class OperationalReport:
    passed: bool
    baseline: WindowSummary
    current: WindowSummary
    tag_summaries: dict[str, WindowSummary]
    findings: tuple[str, ...]
    changed_versions: tuple[str, ...]


def _summary(events: tuple[TelemetryEvent, ...]) -> WindowSummary:
    if not events:
        raise ValueError("operational windows cannot be empty")
    ordered = sorted(item.latency_ms for item in events)
    p95 = ordered[max(0, math.ceil(0.95 * len(ordered)) - 1)]
    return WindowSummary(
        len(events),
        round(sum(item.quality for item in events) / len(events), 6),
        round(sum(item.outcome != "success" for item in events) / len(events), 6),
        p95,
        round(sum(item.cost_units for item in events) / len(events), 6),
    )


def compare_windows(
    baseline: tuple[TelemetryEvent, ...],
    current: tuple[TelemetryEvent, ...],
    policy: OperationalPolicy,
) -> OperationalReport:
    if not 0 <= policy.minimum_quality <= 1 or not 0 <= policy.maximum_error_rate <= 1:
        raise ValueError("invalid operational quality policy")
    for event in (*baseline, *current):
        if not all(
            (
                event.run_id,
                event.model_id,
                event.prompt_version,
                event.policy_version,
                event.dataset_version,
            )
        ):
            raise ValueError("telemetry version identity is required")
    old, new = _summary(baseline), _summary(current)
    findings: list[str] = []
    if new.mean_quality < policy.minimum_quality:
        findings.append("quality_slo")
    if old.mean_quality - new.mean_quality > policy.quality_drift:
        findings.append("quality_drift")
    if new.error_rate > policy.maximum_error_rate:
        findings.append("error_rate_slo")
    if new.p95_latency_ms > policy.maximum_p95_latency_ms:
        findings.append("latency_slo")
    if new.mean_cost > policy.maximum_mean_cost:
        findings.append("cost_slo")
    tags = sorted({tag for item in current for tag in item.tags})
    by_tag = {
        tag: _summary(tuple(item for item in current if tag in item.tags))
        for tag in tags
    }
    for tag, summary in by_tag.items():
        if summary.mean_quality < policy.minimum_quality:
            findings.append(f"tag_quality:{tag}")
    dimensions = (
        (
            "model",
            {item.model_id for item in baseline},
            {item.model_id for item in current},
        ),
        (
            "prompt",
            {item.prompt_version for item in baseline},
            {item.prompt_version for item in current},
        ),
        (
            "policy",
            {item.policy_version for item in baseline},
            {item.policy_version for item in current},
        ),
        (
            "dataset",
            {item.dataset_version for item in baseline},
            {item.dataset_version for item in current},
        ),
    )
    changed = tuple(name for name, before, after in dimensions if before != after)
    return OperationalReport(not findings, old, new, by_tag, tuple(findings), changed)
