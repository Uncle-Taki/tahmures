"""Execute a shared experiment manifest with any ModelClient."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from tahmures.client import ModelClient
from tahmures.evaluators import build_evaluator
from tahmures.manifest import (
    load_cases,
    load_fixtures,
    resolve_project_path,
)
from tahmures.types import (
    CaseResult,
    ExperimentReport,
    GenerationRequest,
    Manifest,
    Message,
)


def _macro_f1(expected: list[str], actual: list[str]) -> float:
    labels = sorted(set(expected) | set(actual))
    if not labels:
        return 0.0
    scores: list[float] = []
    for label in labels:
        pairs = tuple(zip(expected, actual, strict=True))
        true_positive = sum(e == label and a == label for e, a in pairs)
        false_positive = sum(e != label and a == label for e, a in pairs)
        false_negative = sum(e == label and a != label for e, a in pairs)
        denominator = (2 * true_positive) + false_positive + false_negative
        scores.append((2 * true_positive / denominator) if denominator else 0.0)
    return sum(scores) / len(scores)


class ExperimentRunner:
    def __init__(
        self, manifest: Manifest, manifest_path: str | Path, client: ModelClient
    ) -> None:
        self.manifest = manifest
        self.manifest_path = Path(manifest_path)
        self.client = client

    def run(self) -> ExperimentReport:
        cases = load_cases(
            resolve_project_path(self.manifest_path, self.manifest.dataset)
        )
        evaluators = tuple(build_evaluator(spec) for spec in self.manifest.evaluators)
        results: list[CaseResult] = []
        for variant in self.manifest.prompt_variants:
            template_path = resolve_project_path(
                self.manifest_path, variant.template_path
            )
            template = template_path.read_text(encoding="utf-8")
            for case in cases:
                for trial in range(1, self.manifest.trials + 1):
                    request = GenerationRequest(
                        messages=(
                            Message(role="developer", content=template),
                            Message(
                                role="user",
                                content=json.dumps(case.input, sort_keys=True),
                            ),
                        ),
                        metadata={
                            "case_id": case.case_id,
                            "variant_id": variant.id,
                            "trial": trial,
                        },
                    )
                    response = self.client.generate(request)
                    evaluations = tuple(
                        evaluator.evaluate(case, response) for evaluator in evaluators
                    )
                    results.append(
                        CaseResult(
                            case_id=case.case_id,
                            variant_id=variant.id,
                            trial=trial,
                            response=response,
                            evaluations=evaluations,
                        )
                    )
        summaries = self._summarise(cases, results)
        tag_summaries = self._summarise_tags(cases, results)
        return ExperimentReport(
            schema_version=1,
            experiment_id=self.manifest.experiment_id,
            client=self.client.name,
            variant_summaries=summaries,
            tag_summaries=tag_summaries,
            case_results=tuple(results),
        )

    def _summarise(self, cases, results) -> dict[str, dict[str, float]]:
        case_by_id = {case.case_id: case for case in cases}
        sums: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
        counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        labels: dict[str, tuple[list[str], list[str]]] = defaultdict(lambda: ([], []))
        for result in results:
            for evaluation in result.evaluations:
                sums[result.variant_id]["pass_rate"] += float(evaluation.passed)
                counts[result.variant_id]["pass_rate"] += 1
                for metric, value in evaluation.metrics.items():
                    sums[result.variant_id][metric] += value
                    counts[result.variant_id][metric] += 1
            expected_label = case_by_id[result.case_id].expected.get("label")
            if isinstance(expected_label, str):
                labels[result.variant_id][0].append(expected_label.casefold())
                labels[result.variant_id][1].append(
                    result.response.text.strip().casefold()
                )
        summaries: dict[str, dict[str, float]] = {}
        for variant, metrics in sums.items():
            summaries[variant] = {
                name: round(value / counts[variant][name], 6)
                for name, value in sorted(metrics.items())
            }
            expected, actual = labels[variant]
            if expected:
                summaries[variant]["macro_f1"] = round(_macro_f1(expected, actual), 6)
            texts = [
                result.response.text
                for result in results
                if result.variant_id == variant
            ]
            frequencies = Counter(texts)
            summaries[variant]["unique_response_count"] = float(len(frequencies))
            summaries[variant]["unique_response_ratio"] = round(
                len(frequencies) / len(texts), 6
            )
            summaries[variant]["modal_response_rate"] = round(
                max(frequencies.values()) / len(texts), 6
            )
        return summaries

    def _summarise_tags(self, cases, results) -> dict[str, dict[str, dict[str, float]]]:
        case_by_id = {case.case_id: case for case in cases}
        sums: dict[str, dict[str, dict[str, float]]] = defaultdict(
            lambda: defaultdict(lambda: defaultdict(float))
        )
        counts: dict[str, dict[str, dict[str, int]]] = defaultdict(
            lambda: defaultdict(lambda: defaultdict(int))
        )
        for result in results:
            for tag in case_by_id[result.case_id].tags:
                for evaluation in result.evaluations:
                    sums[result.variant_id][tag]["pass_rate"] += float(
                        evaluation.passed
                    )
                    counts[result.variant_id][tag]["pass_rate"] += 1
                    for metric, value in evaluation.metrics.items():
                        sums[result.variant_id][tag][metric] += value
                        counts[result.variant_id][tag][metric] += 1
        return {
            variant: {
                tag: {
                    metric: round(value / counts[variant][tag][metric], 6)
                    for metric, value in sorted(metrics.items())
                }
                for tag, metrics in sorted(tags.items())
            }
            for variant, tags in sorted(sums.items())
        }


def fixture_runner(manifest: Manifest, manifest_path: str | Path) -> ExperimentRunner:
    from tahmures.client import FixtureClient

    fixtures = load_fixtures(resolve_project_path(manifest_path, manifest.fixtures))
    return ExperimentRunner(manifest, manifest_path, FixtureClient(fixtures))
