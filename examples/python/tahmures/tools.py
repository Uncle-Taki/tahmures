"""Least-privilege validation for inert tool calls."""

from __future__ import annotations

import json
from dataclasses import dataclass

from tahmures.contracts import OutputContract
from tahmures.types import JSONValue


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    effect: str
    required_scopes: tuple[str, ...]
    argument_contract: OutputContract
    requires_approval: bool = False


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, JSONValue]


@dataclass(frozen=True)
class ToolDecision:
    allowed: bool
    reason: str
    call: ToolCall


class ToolGate:
    def __init__(self, definitions: tuple[ToolDefinition, ...]) -> None:
        if len({item.name for item in definitions}) != len(definitions):
            raise ValueError("tool names must be unique")
        if any(item.effect not in {"read", "write"} for item in definitions):
            raise ValueError("tool effects must be read or write")
        self._definitions = {item.name: item for item in definitions}

    def evaluate(
        self,
        call: ToolCall,
        granted_scopes: tuple[str, ...],
        approved: bool = False,
    ) -> ToolDecision:
        definition = self._definitions.get(call.name)
        if definition is None:
            return ToolDecision(False, "unknown_tool", call)
        result = definition.argument_contract.validate(
            json.dumps(call.arguments, sort_keys=True)
        )
        if not result.valid:
            return ToolDecision(False, "invalid_arguments", call)
        if not set(definition.required_scopes) <= set(granted_scopes):
            return ToolDecision(False, "insufficient_scope", call)
        if definition.requires_approval and not approved:
            return ToolDecision(False, "approval_required", call)
        return ToolDecision(True, "allowed", call)


class FixtureToolExecutor:
    def execute(self, decision: ToolDecision) -> dict[str, JSONValue]:
        if not decision.allowed:
            raise PermissionError(decision.reason)
        return {"tool": decision.call.name, "status": "fixture_executed"}
