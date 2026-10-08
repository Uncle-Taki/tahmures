"""Full-state controller parity, signed-int boundaries and validation order."""

import json
import sys
from dataclasses import asdict, replace
from pathlib import Path

import pytest
from tahmures.agents import AgentEvent, AgentLimits, AgentRunState, RunController

INTEGER_FIELDS = {
    "max_steps",
    "max_tool_calls",
    "max_tokens",
    "deadline",
    "goal_version",
    "steps",
    "tool_calls",
    "tokens",
    "token_cost",
    "at",
}


def decode_integer(value):
    for label, number in (("MaxInt", sys.maxsize), ("MinInt", -sys.maxsize - 1)):
        if value.startswith(label):
            return number + int(value[len(label) :] or "0")
    return int(value)


def decode_fixture(value):
    if isinstance(value, list):
        return [decode_fixture(item) for item in value]
    if isinstance(value, dict):
        return {
            key: decode_integer(item) if key in INTEGER_FIELDS else decode_fixture(item)
            for key, item in value.items()
        }
    return value


CORPUS = json.loads(
    (Path(__file__).parents[2] / "shared/agent_controller_cases.json").read_text()
)
assert CORPUS["schema_version"] == 1
CASES = decode_fixture(CORPUS["cases"])
TRACES = decode_fixture(CORPUS["traces"])


def observe(limits, state, event):
    before = asdict(state)
    try:
        result = RunController(limits).apply(state, event)
    except ValueError as error:
        assert asdict(state) == before
        return {"state": before, "error": str(error)}
    assert asdict(state) == before  # Successful transitions also preserve the input.
    return {"state": asdict(result), "error": ""}


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_shared_controller_case(case):
    actual = observe(
        AgentLimits(**case["limits"]),
        AgentRunState(**case["state"]),
        AgentEvent(**case["event"]),
    )
    assert actual == case["expected"]


@pytest.mark.parametrize("trace", TRACES, ids=lambda trace: trace["id"])
def test_shared_controller_trace(trace):
    state = AgentRunState(**trace["state"])
    limits = AgentLimits(**trace["limits"])
    for entry in trace["entries"]:
        actual = observe(limits, state, AgentEvent(**entry["event"]))
        assert actual == entry["expected"]
        state = AgentRunState(**actual["state"])


def test_rejected_budget_preserves_usage_then_remains_immutable():
    controller = RunController(AgentLimits(5, 2, 100, 10))
    initial = AgentRunState("inspect", 1, steps=1, tool_calls=1, tokens=30)
    rejected = controller.apply(initial, AgentEvent("step", 1, 50, 2, 2))
    assert rejected == replace(initial, status="failed", reason="tool_budget")
    with pytest.raises(ValueError, match="terminal agent states are immutable"):
        controller.apply(rejected, AgentEvent("cancel", 1))


def test_python_empty_status_remains_terminal():
    # Preserve Python's explicit-state API; Go's zero-value convenience is tested there.
    state = AgentRunState("inspect", 1, status="")
    with pytest.raises(ValueError, match="terminal agent states are immutable"):
        RunController(AgentLimits(1, 1, 1, 1)).apply(state, AgentEvent("cancel", 1))


@pytest.mark.parametrize("kind", ("step", "cancel", "complete"))
def test_minimum_positive_limits(kind):
    state = AgentRunState("inspect", 1)
    result = RunController(AgentLimits(1, 1, 1, 1)).apply(
        state, AgentEvent(kind, 1, 1, 1, 1)
    )
    assert (
        result.status
        == {"step": "running", "cancel": "cancelled", "complete": "completed"}[kind]
    )
    if kind == "step":
        assert (result.steps, result.tool_calls, result.tokens) == (1, 1, 1)
    else:
        assert (result.steps, result.tool_calls, result.tokens) == (0, 0, 0)
