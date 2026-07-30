"""Deterministic agent-run budgets, cancellation, and terminal-state control."""

from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class AgentLimits:
    max_steps: int
    max_tool_calls: int
    max_tokens: int
    deadline: int


@dataclass(frozen=True)
class AgentEvent:
    kind: str
    goal_version: int
    token_cost: int = 0
    tool_calls: int = 0
    at: int = 0


@dataclass(frozen=True)
class AgentRunState:
    goal: str
    goal_version: int
    status: str = "running"
    steps: int = 0
    tool_calls: int = 0
    tokens: int = 0
    reason: str = ""


class RunController:
    def __init__(self, limits: AgentLimits) -> None:
        if (
            min(
                limits.max_steps,
                limits.max_tool_calls,
                limits.max_tokens,
                limits.deadline,
            )
            < 1
        ):
            raise ValueError("agent limits must be positive")
        self.limits = limits

    def apply(self, state: AgentRunState, event: AgentEvent) -> AgentRunState:
        if state.status != "running":
            raise ValueError("terminal agent states are immutable")
        if event.kind == "cancel":
            return replace(state, status="cancelled", reason="cancelled")
        if event.goal_version != state.goal_version:
            return replace(state, status="waiting", reason="stale_goal")
        if event.at > self.limits.deadline:
            return replace(state, status="failed", reason="deadline")
        if event.kind == "complete":
            return replace(state, status="completed", reason="completed")
        if event.kind != "step":
            raise ValueError("unsupported agent event")
        steps = state.steps + 1
        tools = state.tool_calls + event.tool_calls
        tokens = state.tokens + event.token_cost
        if steps > self.limits.max_steps:
            return replace(state, status="failed", reason="step_budget")
        if tools > self.limits.max_tool_calls:
            return replace(state, status="failed", reason="tool_budget")
        if tokens > self.limits.max_tokens:
            return replace(state, status="failed", reason="token_budget")
        return replace(state, steps=steps, tool_calls=tools, tokens=tokens)
