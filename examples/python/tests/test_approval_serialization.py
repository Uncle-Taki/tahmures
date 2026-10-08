"""Typed, shared Python-oracle corpus and malformed-input approval checks."""

import hashlib
import json
import struct
from dataclasses import asdict, replace
from pathlib import Path

import pytest
from tahmures import approvals as module
from tahmures.approvals import (
    ApprovalPolicy,
    ApprovalRecord,
    CapabilityRequest,
    authorize,
    request_digest,
)

CORPUS = json.loads(
    (Path(__file__).parents[2] / "shared/approval_digest_cases.json").read_text()
)
assert CORPUS["schema_version"] == 1


def decode_node(node):
    kind = node["kind"]
    if kind == "null":
        return None
    if kind in {"string", "boolean"}:
        return node["value"]
    if kind == "integer":
        return int(node["value"])
    if kind == "float64":
        return struct.unpack(">d", bytes.fromhex(node["bits"]))[0]
    if kind == "array":
        return [decode_node(item) for item in node["items"]]
    if kind == "object":
        return {item["key"]: decode_node(item["value"]) for item in node["entries"]}
    raise AssertionError(f"unknown fixture kind: {kind}")


@pytest.mark.parametrize("case", CORPUS["valid_cases"], ids=lambda case: case["id"])
def test_shared_serialization(case):
    arguments = decode_node(case["arguments"])
    # Independent runtime oracle also catches corrupt/stale committed goldens.
    oracle = json.dumps(
        {"action": case["action"], "arguments": arguments},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    assert oracle == case["canonical_bytes"].encode("ascii")
    assert module._canonical_request_bytes(case["action"], arguments) == oracle
    assert request_digest(case["action"], arguments) == case["digest"]
    assert hashlib.sha256(oracle).hexdigest() == case["digest"]


@pytest.mark.parametrize(
    "case", CORPUS["authorization_cases"], ids=lambda case: case["id"]
)
def test_shared_complete_authorization(case):
    fields = case["request"] | {
        "arguments": decode_node(case["request"]["arguments"]),
        "scopes": tuple(case["request"]["scopes"]),
    }
    policy = case["policy"]
    result = authorize(
        CapabilityRequest(**fields),
        tuple(ApprovalRecord(**record) for record in case["approvals"]),
        ApprovalPolicy(
            tuple(policy["allowed_actions"]),
            {
                principal: tuple(scopes)
                for principal, scopes in policy["principal_scopes"].items()
            },
            tuple(policy["approval_effects"]),
            tuple(policy["dual_approval_effects"]),
        ),
        case["now"],
    )
    assert asdict(result) == case["expected"]


def invalid_arguments(case):
    factory = case.get("factory")
    if factory in {"surrogate_value", "surrogate_key", "surrogate_action"}:
        return decode_node(case["arguments"])
    if factory == "cycle_object":
        value = {}
        value["self"] = value
        return value
    if factory == "cycle_array":
        value = []
        value.append(value)
        return {"value": value}
    if factory == "non_string_key":
        return {"value": {1: "one"}}
    return decode_node(case["arguments"])


def assert_invalid(arguments, action="open_storehouse"):
    with pytest.raises(ValueError, match="^invalid approval arguments$") as error:
        request_digest(action, arguments)
    assert error.value.__cause__ is not None
    request = CapabilityRequest("r", "servant", action, arguments, (), "read", 10)
    policy = ApprovalPolicy((action,), {})
    record = ApprovalRecord("r", hashlib.sha256(b"").hexdigest(), "steward", True, 1)
    # Malformed serialization precedes every ordinary authorization check.
    for change in ({}, {"request_id": ""}, {"effect": "unknown"}, {"expires_at": 0}):
        current = replace(request, **change)
        result = authorize(current, (record,), policy, 2)
        assert asdict(result) == {
            "allowed": False,
            "reason": "invalid_arguments",
            "approval_count": 0,
            "audit": {
                "request_id": current.request_id,
                "principal": current.principal,
                "action": action,
                "digest": "",
            },
        }


@pytest.mark.parametrize("case", CORPUS["invalid_cases"], ids=lambda case: case["id"])
def test_shared_invalid(case):
    assert_invalid(invalid_arguments(case), case.get("action", "open_storehouse"))


@pytest.mark.parametrize("value", [(), b"bytes", {1, 2}, object()])
def test_native_non_json_values(value):
    assert_invalid({"value": value})


def test_shared_references_are_not_cycles():
    shared = [{"text": "گندم"}]
    assert request_digest("a", {"x": shared, "y": shared}) == request_digest(
        "a", {"x": [{"text": "گندم"}], "y": [{"text": "گندم"}]}
    )


def test_binding_stays_action_and_arguments_only():
    request = CapabilityRequest("r", "servant", "a", {"n": 1}, (), "read", 10)
    for fields in (
        {"request_id": "new"},
        {"principal": "other"},
        {"scopes": ("more",)},
        {"effect": "write"},
        {"expires_at": 20},
    ):
        assert replace(request, **fields).digest == request.digest
    assert replace(request, action="b").digest != request.digest
    assert replace(request, arguments={"n": 1.0}).digest != request.digest
    assert replace(request, arguments={"n": 1, "extra": False}).digest != request.digest


def test_serialization_failure_keeps_cause(monkeypatch):
    cause = TypeError("serialization failed")

    def failed_encoder(*args, **kwargs):
        raise cause

    monkeypatch.setattr(module.json, "dumps", failed_encoder)
    with pytest.raises(ValueError, match="^invalid approval arguments$") as error:
        request_digest("a", {})
    assert error.value.__cause__ is cause
    request = CapabilityRequest("r", "servant", "a", {}, (), "read", 10)
    assert (
        authorize(request, (), ApprovalPolicy(("a",), {}), 2).reason
        == "invalid_arguments"
    )


def test_unexpected_digest_error_is_not_a_denial(monkeypatch):
    def broken_hash(*args, **kwargs):
        raise ValueError("unexpected hash failure")

    monkeypatch.setattr(module.hashlib, "sha256", broken_hash)
    request = CapabilityRequest("r", "servant", "a", {}, (), "read", 10)
    with pytest.raises(ValueError, match="unexpected hash failure"):
        authorize(request, (), ApprovalPolicy(("a",), {}), 2)
