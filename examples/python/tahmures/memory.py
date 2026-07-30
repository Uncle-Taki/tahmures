"""Explicit, scoped, expiring in-memory records for the memory chapter."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MemoryPolicy:
    allowed_kinds: tuple[str, ...]
    max_ttl: int


@dataclass(frozen=True)
class MemoryRecord:
    memory_id: str
    subject_id: str
    scope: str
    kind: str
    value: str
    provenance: str
    created_at: int
    expires_at: int
    supersedes: str = ""


@dataclass(frozen=True)
class MemoryQuery:
    subject_id: str
    scope: str
    as_of: int
    kinds: tuple[str, ...] = ()


class InMemoryStore:
    def __init__(self) -> None:
        self._records: dict[str, MemoryRecord] = {}
        self._forgotten: set[str] = set()

    def remember(self, record: MemoryRecord, policy: MemoryPolicy, now: int) -> None:
        if not all(
            (
                record.memory_id,
                record.subject_id,
                record.scope,
                record.kind,
                record.value,
                record.provenance,
            )
        ):
            raise ValueError("memory fields and provenance are required")
        if record.kind not in policy.allowed_kinds:
            raise ValueError("memory kind is not allowed")
        if record.created_at > now or record.expires_at <= now:
            raise ValueError("memory is not current at write time")
        if record.expires_at - record.created_at > policy.max_ttl:
            raise ValueError("memory exceeds maximum retention")
        if record.memory_id in self._records:
            raise ValueError("memory ID already exists")
        if record.supersedes and record.supersedes not in self._records:
            raise ValueError("superseded memory does not exist")
        self._records[record.memory_id] = record

    def recall(self, query: MemoryQuery) -> tuple[MemoryRecord, ...]:
        superseded = {
            record.supersedes for record in self._records.values() if record.supersedes
        }
        return tuple(
            sorted(
                (
                    record
                    for record in self._records.values()
                    if record.memory_id not in self._forgotten
                    and record.memory_id not in superseded
                    and record.subject_id == query.subject_id
                    and record.scope == query.scope
                    and record.created_at <= query.as_of < record.expires_at
                    and (not query.kinds or record.kind in query.kinds)
                ),
                key=lambda item: (item.kind, item.memory_id),
            )
        )

    def forget(self, memory_id: str) -> None:
        if memory_id not in self._records:
            raise ValueError("memory does not exist")
        self._forgotten.add(memory_id)
