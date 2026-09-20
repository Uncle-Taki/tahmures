"""A conservative educational selector for language and hard controls."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ControlRequirement:
    task_id: str
    language_interpretation: bool = False
    structured_output: bool = False
    hard_invariant: bool = False
    authoritative_state: bool = False
    permission: bool = False
    external_mutation: bool = False
    irreversible: bool = False
    subjective_judgement: bool = False


@dataclass(frozen=True)
class ControlDecision:
    primary: str
    supporting: tuple[str, ...]
    human_review: bool
    reasons: tuple[str, ...]


def select_controls(requirement: ControlRequirement) -> ControlDecision:
    if not requirement.task_id:
        raise ValueError("control requirement needs a task ID")
    controls: list[str] = []
    reasons: list[str] = []
    if requirement.language_interpretation:
        controls.append("language_model")
    if requirement.structured_output:
        controls.append("schema_validation")
    if requirement.hard_invariant:
        controls.append("deterministic_code")
        reasons.append("hard_invariant")
    if requirement.authoritative_state:
        controls.append("database_constraint")
        reasons.append("authoritative_state")
    if requirement.permission or requirement.external_mutation:
        controls.append("access_control")
        reasons.append("capability_boundary")
    human = requirement.subjective_judgement or requirement.irreversible
    if human:
        controls.append("human_judgement")
        reasons.append("accountable_judgement")
    if not controls:
        controls.append("deterministic_code")
        reasons.append("default_mechanism")
    priority = (
        "database_constraint",
        "access_control",
        "deterministic_code",
        "human_judgement",
        "schema_validation",
        "language_model",
    )
    primary = next(item for item in priority if item in controls)
    supporting = tuple(item for item in controls if item != primary)
    return ControlDecision(primary, supporting, human, tuple(reasons))
