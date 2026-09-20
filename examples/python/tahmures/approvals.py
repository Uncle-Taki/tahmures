"""Exact, expiring approval records for consequential fixture actions."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from tahmures.types import JSONValue


def request_digest(action: str, arguments: dict[str, JSONValue]) -> str:
    payload = json.dumps(
        {"action": action, "arguments": arguments},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode()).hexdigest()


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
        "digest": request.digest,
    }
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
    if any(item.request_digest != request.digest for item in relevant):
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
