"""Deterministic context selection with provenance and budget accounting."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass


class ContextBudgetError(ValueError):
    """Raised when mandatory context cannot fit the declared budget."""


@dataclass(frozen=True)
class ContextItem:
    id: str
    text: str
    token_estimate: int
    priority: int
    provenance: str
    mandatory: bool = False
    scope: str = "public"
    trust: str = "data"
    valid_from: int | None = None
    valid_until: int | None = None
    digest: str = ""
    claim_group: str = ""

    def __post_init__(self) -> None:
        if self.token_estimate < 1:
            raise ValueError("token_estimate must be positive")
        if not self.provenance:
            raise ValueError("context provenance cannot be empty")
        if self.trust not in {"instruction", "data"}:
            raise ValueError("context trust must be instruction or data")
        if (
            self.valid_from is not None
            and self.valid_until is not None
            and self.valid_from > self.valid_until
        ):
            raise ValueError("context validity range is inverted")


@dataclass(frozen=True)
class ContextSelection:
    selected: tuple[ContextItem, ...]
    excluded: tuple[ContextItem, ...]
    used_tokens: int
    budget: int


@dataclass(frozen=True)
class ContextPolicy:
    input_budget: int
    reserved_output: int = 0
    scope: str = "public"
    as_of: int = 0


@dataclass(frozen=True)
class ContextExclusion:
    item: ContextItem
    reason: str


@dataclass(frozen=True)
class ContextPackage:
    selected: tuple[ContextItem, ...]
    excluded: tuple[ContextExclusion, ...]
    conflicts: tuple[tuple[str, ...], ...]
    used_tokens: int
    available_budget: int


def select_context(items: tuple[ContextItem, ...], budget: int) -> ContextSelection:
    if budget < 1:
        raise ContextBudgetError("context budget must be positive")
    if len({item.id for item in items}) != len(items):
        raise ContextBudgetError("context item IDs must be unique")
    mandatory = [item for item in items if item.mandatory]
    mandatory_tokens = sum(item.token_estimate for item in mandatory)
    if mandatory_tokens > budget:
        raise ContextBudgetError(
            f"mandatory context needs {mandatory_tokens} tokens; budget is {budget}"
        )
    optional = sorted(
        (item for item in items if not item.mandatory),
        key=lambda item: (-item.priority, item.token_estimate, item.id),
    )
    selected = list(mandatory)
    excluded: list[ContextItem] = []
    used = mandatory_tokens
    for item in optional:
        if used + item.token_estimate <= budget:
            selected.append(item)
            used += item.token_estimate
        else:
            excluded.append(item)
    order = {item.id: index for index, item in enumerate(items)}
    selected.sort(key=lambda item: order[item.id])
    excluded.sort(key=lambda item: order[item.id])
    return ContextSelection(tuple(selected), tuple(excluded), used, budget)


def assemble_context(
    items: tuple[ContextItem, ...], policy: ContextPolicy
) -> ContextPackage:
    available = policy.input_budget - policy.reserved_output
    if available < 1:
        raise ContextBudgetError("reserved output leaves no input budget")
    candidates: list[tuple[ContextItem, str]] = []
    excluded: list[ContextExclusion] = []
    for item in items:
        if item.scope not in {"public", policy.scope}:
            excluded.append(ContextExclusion(item, "scope"))
            continue
        if item.valid_from is not None and policy.as_of < item.valid_from:
            excluded.append(ContextExclusion(item, "not_yet_valid"))
            continue
        if item.valid_until is not None and policy.as_of > item.valid_until:
            excluded.append(ContextExclusion(item, "expired"))
            continue
        digest = item.digest or hashlib.sha256(item.text.encode()).hexdigest()
        candidates.append((item, digest))
    winners: dict[str, int] = {}
    for index, (item, digest) in enumerate(candidates):
        current = winners.get(digest)
        if current is None:
            winners[digest] = index
            continue
        current_item = candidates[current][0]
        item_key = (-int(item.mandatory), -item.priority, item.token_estimate, item.id)
        current_key = (
            -int(current_item.mandatory),
            -current_item.priority,
            current_item.token_estimate,
            current_item.id,
        )
        if item_key < current_key:
            winners[digest] = index
    eligible: list[ContextItem] = []
    for index, (item, digest) in enumerate(candidates):
        if winners[digest] == index:
            eligible.append(item)
        else:
            excluded.append(ContextExclusion(item, "duplicate"))
    selection = select_context(tuple(eligible), available)
    excluded.extend(ContextExclusion(item, "budget") for item in selection.excluded)
    groups: dict[str, list[ContextItem]] = {}
    for item in selection.selected:
        if item.claim_group:
            groups.setdefault(item.claim_group, []).append(item)
    conflicts = tuple(
        tuple(sorted(item.id for item in group))
        for group in groups.values()
        if len({item.text for item in group}) > 1
    )
    return ContextPackage(
        selected=selection.selected,
        excluded=tuple(excluded),
        conflicts=tuple(sorted(conflicts)),
        used_tokens=selection.used_tokens,
        available_budget=available,
    )
