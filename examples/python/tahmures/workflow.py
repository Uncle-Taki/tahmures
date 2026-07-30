"""Deterministic workflow-plan validation for decomposition labs."""

from __future__ import annotations

from dataclasses import dataclass


class WorkflowValidationError(ValueError):
    """Raised when a workflow plan cannot be executed safely."""


@dataclass(frozen=True)
class WorkflowStep:
    id: str
    depends_on: tuple[str, ...] = ()
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()
    checkpoint: bool = False
    terminal: bool = False


@dataclass(frozen=True)
class WorkflowPlan:
    steps: tuple[WorkflowStep, ...]

    def validate(self) -> None:
        if not self.steps:
            raise WorkflowValidationError("workflow needs at least one step")
        by_id = {step.id: step for step in self.steps}
        if len(by_id) != len(self.steps):
            raise WorkflowValidationError("workflow step IDs must be unique")
        for step in self.steps:
            unknown = sorted(set(step.depends_on) - set(by_id))
            if unknown:
                raise WorkflowValidationError(
                    f"step {step.id} has unknown dependencies: {unknown}"
                )
            if not step.inputs or not step.outputs:
                raise WorkflowValidationError(
                    f"step {step.id} must declare inputs and outputs"
                )
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(step_id: str) -> None:
            if step_id in visiting:
                raise WorkflowValidationError("workflow dependencies contain a cycle")
            if step_id in visited:
                return
            visiting.add(step_id)
            for dependency in by_id[step_id].depends_on:
                visit(dependency)
            visiting.remove(step_id)
            visited.add(step_id)

        for step_id in by_id:
            visit(step_id)
        if sum(step.terminal for step in self.steps) != 1:
            raise WorkflowValidationError("workflow needs exactly one terminal step")
        if not any(step.checkpoint for step in self.steps):
            raise WorkflowValidationError("workflow needs at least one checkpoint")

    def ready(self, completed_steps: set[str]) -> tuple[WorkflowStep, ...]:
        self.validate()
        known = {step.id for step in self.steps}
        unknown = sorted(completed_steps - known)
        if unknown:
            raise WorkflowValidationError(f"unknown completed steps: {unknown}")
        return tuple(
            step
            for step in self.steps
            if step.id not in completed_steps
            and set(step.depends_on) <= completed_steps
        )
