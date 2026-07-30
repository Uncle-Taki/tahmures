"""Shared request, response, and experiment value types."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

JSONValue = str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]


@dataclass(frozen=True)
class Message:
    role: str
    content: str

    def __post_init__(self) -> None:
        if self.role not in {"system", "developer", "user", "assistant", "tool"}:
            raise ValueError(f"unsupported message role: {self.role}")
        if not self.content:
            raise ValueError("message content cannot be empty")


@dataclass(frozen=True)
class GenerationParameters:
    temperature: float = 0.0
    max_output_tokens: int = 500
    seed: int | None = None


@dataclass(frozen=True)
class GenerationRequest:
    messages: tuple[Message, ...]
    parameters: GenerationParameters = field(default_factory=GenerationParameters)
    metadata: dict[str, JSONValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.messages:
            raise ValueError("a generation request needs at least one message")


@dataclass(frozen=True)
class GenerationResponse:
    text: str
    model_id: str
    finish_reason: str = "stop"
    usage: dict[str, int] = field(default_factory=dict)
    metadata: dict[str, JSONValue] = field(default_factory=dict)


@dataclass(frozen=True)
class PromptVariant:
    id: str
    template_path: str


@dataclass(frozen=True)
class EvaluatorSpec:
    name: str
    type: str
    threshold: float = 1.0


@dataclass(frozen=True)
class Manifest:
    schema_version: int
    chapter: int
    experiment_id: str
    description: str
    dataset: str
    fixtures: str
    prompt_variants: tuple[PromptVariant, ...]
    evaluators: tuple[EvaluatorSpec, ...]
    trials: int = 1


@dataclass(frozen=True)
class ExperimentCase:
    case_id: str
    input: dict[str, JSONValue]
    expected: dict[str, JSONValue]
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class FixtureRecord:
    case_id: str
    variant_id: str
    trial: int
    response: GenerationResponse


@dataclass(frozen=True)
class EvaluationResult:
    evaluator: str
    passed: bool
    score: float
    metrics: dict[str, float]
    reason: str


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    variant_id: str
    trial: int
    response: GenerationResponse
    evaluations: tuple[EvaluationResult, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExperimentReport:
    schema_version: int
    experiment_id: str
    client: str
    variant_summaries: dict[str, dict[str, float]]
    tag_summaries: dict[str, dict[str, dict[str, float]]]
    case_results: tuple[CaseResult, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "experiment_id": self.experiment_id,
            "client": self.client,
            "variant_summaries": self.variant_summaries,
            "tag_summaries": self.tag_summaries,
            "case_results": [result.to_dict() for result in self.case_results],
        }
