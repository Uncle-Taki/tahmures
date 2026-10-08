"""Exact, expiring approval records for consequential fixture actions."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass

from tahmures.types import JSONValue


class _InvalidApprovalArguments(ValueError):
    """The checked serialization boundary rejected an unsupported argument."""


def _validate_json_value(value: JSONValue, active: set[int]) -> None:
    kind = type(value)
    if kind is str:
        value.encode("utf-8")  # Reject surrogate code points; do not normalise text.
    elif kind is float:
        if not math.isfinite(value):
            raise ValueError("nonfinite number")
    elif kind in (int, bool, type(None)):
        return
    elif kind in (dict, list):
        identity = id(value)
        if identity in active:
            raise ValueError("cyclic JSON value")
        active.add(identity)
        try:
            if kind is dict:
                for key, item in value.items():
                    if type(key) is not str:
                        raise TypeError("JSON object keys must be strings")
                    key.encode("utf-8")
                    _validate_json_value(item, active)
            else:
                for item in value:
                    _validate_json_value(item, active)
        finally:
            active.remove(identity)
    else:
        raise TypeError("unsupported JSON value")


def _canonical_request_bytes(action: str, arguments: dict[str, JSONValue]) -> bytes:
    try:
        if type(action) is not str or type(arguments) is not dict:
            raise TypeError("action must be a string and arguments a nonnull object")
        _validate_json_value(action, set())
        _validate_json_value(arguments, set())
        return json.dumps(
            {"action": action, "arguments": arguments},
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError, OverflowError, RecursionError) as error:
        raise _InvalidApprovalArguments("invalid approval arguments") from error


def request_digest(action: str, arguments: dict[str, JSONValue]) -> str:
    """Bind action and JSON-domain arguments using canonical Python bytes.

    Unsupported inputs raise ValueError; request metadata is not digest-bound.
    """
    return hashlib.sha256(_canonical_request_bytes(action, arguments)).hexdigest()


@dataclass(frozen=True)
class CapabilityRequest:
    request_id: str
    principal: str
    action: str
    arguments: dict[str, JSONValue]
    scopes: tuple[str, ...]
    effect: str
    expires_at: int

    @property
    def digest(self) -> str:
        return request_digest(self.action, self.arguments)


@dataclass(frozen=True)
class ApprovalRecord:
    request_id: str
    request_digest: str
    approver: str
    approved: bool
    at: int


@dataclass(frozen=True)
class ApprovalPolicy:
    allowed_actions: tuple[str, ...]
    principal_scopes: dict[str, tuple[str, ...]]
    approval_effects: tuple[str, ...] = ("write",)
    dual_approval_effects: tuple[str, ...] = ()


@dataclass(frozen=True)
class AuthorizationResult:
    allowed: bool
    reason: str
    approval_count: int
    audit: dict[str, str]


def authorize(
    request: CapabilityRequest,
    approvals: tuple[ApprovalRecord, ...],
    policy: ApprovalPolicy,
    now: int,
) -> AuthorizationResult:
    audit = {
        "request_id": request.request_id,
        "principal": request.principal,
        "action": request.action,
        "digest": "",
    }
    try:
        audit["digest"] = request.digest
    except _InvalidApprovalArguments:
        return AuthorizationResult(False, "invalid_arguments", 0, audit)
    if not all((request.request_id, request.principal, request.action)):
        return AuthorizationResult(False, "invalid_request", 0, audit)
    if request.effect not in {"read", "write", "high_consequence"}:
        return AuthorizationResult(False, "invalid_effect", 0, audit)
    if now >= request.expires_at:
        return AuthorizationResult(False, "request_expired", 0, audit)
    if request.action not in policy.allowed_actions:
        return AuthorizationResult(False, "unknown_action", 0, audit)
    granted = set(policy.principal_scopes.get(request.principal, ()))
    if not set(request.scopes) <= granted:
        return AuthorizationResult(False, "insufficient_scope", 0, audit)
    relevant = [item for item in approvals if item.request_id == request.request_id]
    if any(item.request_digest != audit["digest"] for item in relevant):
        return AuthorizationResult(False, "digest_mismatch", 0, audit)
    approved = [item for item in relevant if item.approved and item.at <= now]
    approvers = {item.approver for item in approved}
    if len(approvers) != len(approved):
        return AuthorizationResult(False, "duplicate_approver", len(approvers), audit)
    required = 0
    if request.effect in policy.dual_approval_effects:
        required = 2
    elif request.effect in policy.approval_effects:
        required = 1
    if len(approvers) < required:
        return AuthorizationResult(False, "approval_required", len(approvers), audit)
    return AuthorizationResult(True, "allowed", len(approvers), audit)
