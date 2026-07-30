"""Deterministic, scoped retrieval and citation checks for offline teaching."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class RetrievalRequest:
    query: str
    limit: int
    scope: str = "public"
    as_of: int = 0


@dataclass(frozen=True)
class RetrievedChunk:
    chunk_id: str
    document_id: str
    text: str
    provenance: str
    scope: str = "public"
    valid_from: int | None = None
    valid_until: int | None = None
    score: float = 0.0


class Retriever(Protocol):
    def retrieve(self, request: RetrievalRequest) -> tuple[RetrievedChunk, ...]: ...


def _terms(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.casefold()))


class InMemoryRetriever:
    def __init__(self, chunks: tuple[RetrievedChunk, ...]) -> None:
        if len({chunk.chunk_id for chunk in chunks}) != len(chunks):
            raise ValueError("retrieval chunk IDs must be unique")
        self._chunks = chunks

    def retrieve(self, request: RetrievalRequest) -> tuple[RetrievedChunk, ...]:
        if not request.query.strip() or request.limit < 1:
            raise ValueError("retrieval needs a query and positive limit")
        query_terms = _terms(request.query)
        ranked: list[RetrievedChunk] = []
        for chunk in self._chunks:
            if chunk.scope not in {"public", request.scope}:
                continue
            if chunk.valid_from is not None and request.as_of < chunk.valid_from:
                continue
            if chunk.valid_until is not None and request.as_of > chunk.valid_until:
                continue
            terms = _terms(chunk.text)
            score = len(query_terms & terms) / max(1, len(query_terms))
            if score:
                ranked.append(
                    RetrievedChunk(**{**chunk.__dict__, "score": round(score, 6)})
                )
        ranked.sort(key=lambda item: (-item.score, item.chunk_id))
        return tuple(ranked[: request.limit])


@dataclass(frozen=True)
class CitationResult:
    valid: bool
    citations: tuple[str, ...]
    unsupported: tuple[str, ...]


def validate_citations(
    text: str, retrieved: tuple[RetrievedChunk, ...], require_citation: bool = True
) -> CitationResult:
    citations = tuple(sorted(set(re.findall(r"\[([A-Z][A-Z0-9_-]*)\]", text))))
    allowed = {chunk.chunk_id for chunk in retrieved}
    unsupported = tuple(item for item in citations if item not in allowed)
    return CitationResult(
        valid=not unsupported and (bool(citations) or not require_citation),
        citations=citations,
        unsupported=unsupported,
    )
