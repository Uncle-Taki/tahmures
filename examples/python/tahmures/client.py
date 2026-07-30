"""Model client boundary and deterministic fixture implementation."""

from __future__ import annotations

from typing import Protocol

from tahmures.types import FixtureRecord, GenerationRequest, GenerationResponse


class ModelClient(Protocol):
    """The only operation required from a model provider."""

    @property
    def name(self) -> str: ...

    def generate(self, request: GenerationRequest) -> GenerationResponse: ...


class FixtureClient:
    """Return committed responses by case, variant, and trial."""

    def __init__(self, fixtures: tuple[FixtureRecord, ...]) -> None:
        self._fixtures = {
            (record.case_id, record.variant_id, record.trial): record.response
            for record in fixtures
        }

    @property
    def name(self) -> str:
        return "fixture"

    def generate(self, request: GenerationRequest) -> GenerationResponse:
        try:
            key = (
                str(request.metadata["case_id"]),
                str(request.metadata["variant_id"]),
                int(request.metadata["trial"]),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(
                "fixture requests require case_id, variant_id, trial"
            ) from error
        try:
            return self._fixtures[key]
        except KeyError as error:
            raise LookupError(f"no fixture response for {key}") from error
