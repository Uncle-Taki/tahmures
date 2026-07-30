"""Typed hand-off envelopes that preserve intent, authority, and provenance."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ArtifactRef:
    artifact_id: str
    provenance: str


@dataclass(frozen=True)
class HandoffEnvelope:
    schema_version: int
    handoff_id: str
    goal: str
    goal_version: int
    authority: str
    constraints: tuple[str, ...]
    completed: tuple[str, ...]
    artifacts: tuple[ArtifactRef, ...]
    assumptions: tuple[str, ...]
    unresolved_questions: tuple[str, ...]
    permitted_next_actions: tuple[str, ...]
    expires_at: int

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class HandoffResult:
    valid: bool
    violations: tuple[str, ...]


class HandoffContract:
    def __init__(self, allowed_actions: tuple[str, ...]) -> None:
        self._allowed = set(allowed_actions)

    def validate(
        self, envelope: HandoffEnvelope, expected_goal_version: int, now: int
    ) -> HandoffResult:
        violations: list[str] = []
        if envelope.schema_version != 1:
            violations.append("schema_version")
        if not all((envelope.handoff_id, envelope.goal, envelope.authority)):
            violations.append("required_identity")
        if envelope.goal_version != expected_goal_version:
            violations.append("stale_goal")
        if envelope.expires_at <= now:
            violations.append("expired")
        if any(
            not item.artifact_id or not item.provenance for item in envelope.artifacts
        ):
            violations.append("artifact_provenance")
        if not set(envelope.permitted_next_actions) <= self._allowed:
            violations.append("unknown_action")
        return HandoffResult(not violations, tuple(violations))
