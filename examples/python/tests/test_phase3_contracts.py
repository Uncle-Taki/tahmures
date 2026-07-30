import pytest
from tahmures.agents import AgentEvent, AgentLimits, AgentRunState, RunController
from tahmures.context import ContextItem, ContextPolicy, assemble_context
from tahmures.contracts import FieldContract, OutputContract
from tahmures.handoffs import ArtifactRef, HandoffContract, HandoffEnvelope
from tahmures.memory import InMemoryStore, MemoryPolicy, MemoryQuery, MemoryRecord
from tahmures.retrieval import (
    InMemoryRetriever,
    RetrievalRequest,
    RetrievedChunk,
    validate_citations,
)
from tahmures.tools import ToolCall, ToolDefinition, ToolGate


def test_context_assembly_filters_deduplicates_and_finds_conflicts() -> None:
    items = (
        ContextItem("rule", "allow", 2, 9, "policy", True, claim_group="gate"),
        ContextItem("conflict", "deny", 2, 8, "archive", claim_group="gate"),
        ContextItem("copy", "deny", 2, 7, "mirror", digest="same"),
        ContextItem("copy2", "deny again", 2, 6, "mirror", digest="same"),
        ContextItem("private", "secret", 2, 10, "private", scope="tenant-b"),
    )
    package = assemble_context(
        items, ContextPolicy(input_budget=8, reserved_output=2, scope="tenant-a")
    )
    assert [item.id for item in package.selected] == ["rule", "conflict", "copy"]
    assert {item.reason for item in package.excluded} == {"duplicate", "scope"}
    assert package.conflicts == (("conflict", "rule"),)


def test_context_assembly_keeps_mandatory_duplicate() -> None:
    package = assemble_context(
        (
            ContextItem("optional", "same", 1, 100, "cache"),
            ContextItem("rule", "same", 1, 1, "policy", mandatory=True),
        ),
        ContextPolicy(2),
    )
    assert [item.id for item in package.selected] == ["rule"]
    assert [(item.item.id, item.reason) for item in package.excluded] == [
        ("optional", "duplicate")
    ]


def test_retrieval_is_scoped_current_and_citations_are_bounded() -> None:
    expired = 2
    retriever = InMemoryRetriever(
        (
            RetrievedChunk(
                "OLD", "d1", "safe eastern pass", "map", valid_until=expired
            ),
            RetrievedChunk("CUR", "d2", "safe eastern pass", "survey"),
            RetrievedChunk("OTHER", "d3", "safe eastern pass", "private", scope="b"),
        )
    )
    result = retriever.retrieve(
        RetrievalRequest("safe pass", limit=3, scope="a", as_of=3)
    )
    assert [item.chunk_id for item in result] == ["CUR"]
    assert validate_citations("Use it [CUR].", result).valid
    assert not validate_citations("Use it [OLD].", result).valid


def test_memory_expiry_supersession_scope_and_forgetting() -> None:
    store = InMemoryStore()
    policy = MemoryPolicy(("preference",), max_ttl=20)
    old = MemoryRecord("m1", "u1", "a", "preference", "east", "user", 1, 10)
    new = MemoryRecord("m2", "u1", "a", "preference", "west", "user", 2, 15, "m1")
    store.remember(old, policy, now=2)
    store.remember(new, policy, now=2)
    assert [item.memory_id for item in store.recall(MemoryQuery("u1", "a", 3))] == [
        "m2"
    ]
    assert store.recall(MemoryQuery("u1", "b", 3)) == ()
    store.forget("m2")
    assert store.recall(MemoryQuery("u1", "a", 3)) == ()


def test_tool_gate_requires_scope_approval_and_valid_arguments() -> None:
    contract = OutputContract((FieldContract("gate", "string"),))
    gate = ToolGate((ToolDefinition("open", "write", ("gate:write",), contract, True),))
    call = ToolCall("open", {"gate": "north"})
    assert gate.evaluate(call, ("gate:write",)).reason == "approval_required"
    assert gate.evaluate(call, ("gate:write",), approved=True).allowed
    assert gate.evaluate(ToolCall("missing", {}), ()).reason == "unknown_tool"


def test_agent_controller_enforces_goal_budgets_and_terminal_state() -> None:
    controller = RunController(AgentLimits(1, 1, 10, 10))
    state = AgentRunState("travel", 2)
    state = controller.apply(state, AgentEvent("step", 2, 5, 1, 1))
    state = controller.apply(state, AgentEvent("step", 2, 1, 0, 2))
    assert (state.status, state.reason) == ("failed", "step_budget")
    with pytest.raises(ValueError, match="immutable"):
        controller.apply(state, AgentEvent("step", 2))


def test_handoff_rejects_stale_goals_and_unsafe_actions() -> None:
    envelope = HandoffEnvelope(
        1,
        "h1",
        "travel north",
        2,
        "royal-order",
        ("do not cross after sunset",),
        (),
        (ArtifactRef("route", "survey"),),
        (),
        ("escort available?",),
        ("inspect",),
        10,
    )
    contract = HandoffContract(("inspect",))
    assert contract.validate(envelope, 2, 1).valid
    assert "stale_goal" in contract.validate(envelope, 3, 1).violations
