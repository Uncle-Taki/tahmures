"""Source-owned instruction authority for untrusted content boundaries."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ContentRecord:
    record_id: str
    text: str
    source: str
    declared_role: str
    provenance: str


@dataclass(frozen=True)
class TrustPolicy:
    trusted_instruction_sources: tuple[str, ...]
    rejected_sources: tuple[str, ...] = ()


@dataclass(frozen=True)
class TrustFinding:
    record_id: str
    reason: str


@dataclass(frozen=True)
class TrustPartition:
    instructions: tuple[ContentRecord, ...]
    data: tuple[ContentRecord, ...]
    rejected: tuple[ContentRecord, ...]
    findings: tuple[TrustFinding, ...]


def partition_content(
    records: tuple[ContentRecord, ...], policy: TrustPolicy
) -> TrustPartition:
    if len({item.record_id for item in records}) != len(records):
        raise ValueError("content record IDs must be unique")
    trusted = set(policy.trusted_instruction_sources)
    denied = set(policy.rejected_sources)
    instructions: list[ContentRecord] = []
    data: list[ContentRecord] = []
    rejected: list[ContentRecord] = []
    findings: list[TrustFinding] = []
    for record in records:
        if not all((record.record_id, record.text, record.source, record.provenance)):
            raise ValueError(
                "content identity, text, source, and provenance are required"
            )
        if record.declared_role not in {"instruction", "data"}:
            raise ValueError("content role must be instruction or data")
        if record.source in denied:
            rejected.append(record)
            findings.append(TrustFinding(record.record_id, "source_rejected"))
        elif record.declared_role == "instruction" and record.source in trusted:
            instructions.append(record)
        else:
            data.append(record)
            if record.declared_role == "instruction":
                findings.append(TrustFinding(record.record_id, "authority_downgraded"))
    return TrustPartition(
        tuple(instructions), tuple(data), tuple(rejected), tuple(findings)
    )
