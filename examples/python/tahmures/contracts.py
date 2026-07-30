"""A small educational JSON output contract validator.

This module intentionally implements a narrow object contract. It is not a
complete JSON Schema implementation.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class FieldContract:
    name: str
    value_type: str
    required: bool = True
    allowed_values: tuple[Any, ...] = ()


@dataclass(frozen=True)
class ContractViolation:
    path: str
    code: str
    message: str


@dataclass(frozen=True)
class ContractResult:
    valid: bool
    parsed: bool
    value: dict[str, Any] | None
    violations: tuple[ContractViolation, ...]


@dataclass(frozen=True)
class OutputContract:
    fields: tuple[FieldContract, ...]
    allow_extra: bool = False
    _types: dict[str, type] = field(
        default_factory=lambda: {
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool,
            "array": list,
            "object": dict,
            "null": type(None),
        },
        init=False,
        repr=False,
        compare=False,
    )

    def validate(self, text: str) -> ContractResult:
        try:
            value = json.loads(text)
        except json.JSONDecodeError as error:
            violation = ContractViolation("$", "invalid_json", str(error))
            return ContractResult(False, False, None, (violation,))
        if not isinstance(value, dict):
            violation = ContractViolation("$", "wrong_type", "expected JSON object")
            return ContractResult(False, True, None, (violation,))
        violations: list[ContractViolation] = []
        definitions = {field.name: field for field in self.fields}
        for name, definition in definitions.items():
            if name not in value:
                if definition.required:
                    violations.append(
                        ContractViolation(name, "missing", "required field is absent")
                    )
                continue
            expected = self._types.get(definition.value_type)
            if expected is None:
                raise ValueError(f"unknown contract type: {definition.value_type}")
            actual = value[name]
            if definition.value_type == "integer":
                type_matches = isinstance(actual, int) and not isinstance(actual, bool)
            elif definition.value_type == "number":
                type_matches = isinstance(actual, expected) and not isinstance(
                    actual, bool
                )
            else:
                type_matches = isinstance(actual, expected)
            if not type_matches:
                violations.append(
                    ContractViolation(
                        name,
                        "wrong_type",
                        f"expected {definition.value_type}",
                    )
                )
            elif definition.allowed_values and actual not in definition.allowed_values:
                violations.append(
                    ContractViolation(
                        name,
                        "not_allowed",
                        f"value {actual!r} is not allowed",
                    )
                )
        if not self.allow_extra:
            for name in sorted(set(value) - set(definitions)):
                violations.append(
                    ContractViolation(name, "extra", "additional field is not allowed")
                )
        return ContractResult(not violations, True, value, tuple(violations))
