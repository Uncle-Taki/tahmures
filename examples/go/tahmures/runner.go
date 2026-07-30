package tahmures

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"sort"
	"strings"
)

type ExperimentRunner struct {
	Manifest     Manifest
	ManifestPath string
	Client       Client
}

func (runner ExperimentRunner) Run(ctx context.Context) (ExperimentReport, error) {
	cases, err := LoadCases(ResolveProjectPath(runner.ManifestPath, runner.Manifest.Dataset))
	if err != nil {
		return ExperimentReport{}, err
	}
	evaluators := make([]Evaluator, 0, len(runner.Manifest.Evaluators))
	for _, spec := range runner.Manifest.Evaluators {
		built, buildErr := BuildEvaluator(spec)
		if buildErr != nil {
			return ExperimentReport{}, buildErr
		}
		evaluators = append(evaluators, built)
	}
	results := []CaseResult{}
	for _, variant := range runner.Manifest.PromptVariants {
		templatePath := ResolveProjectPath(runner.ManifestPath, variant.TemplatePath)
		template, readErr := os.ReadFile(templatePath)
		if readErr != nil {
			return ExperimentReport{}, fmt.Errorf("read prompt template: %w", readErr)
		}
		for _, testCase := range cases {
			input, _ := json.Marshal(testCase.Input)
			for trial := 1; trial <= runner.Manifest.Trials; trial++ {
				request := GenerationRequest{
					Messages: []Message{
						{Role: "developer", Content: string(template)},
						{Role: "user", Content: string(input)},
					},
					Parameters: GenerationParameters{
						Temperature:     0,
						MaxOutputTokens: 500,
					},
					Metadata: map[string]any{
						"case_id":    testCase.CaseID,
						"variant_id": variant.ID,
						"trial":      trial,
					},
				}
				response, generateErr := runner.Client.Generate(ctx, request)
				if generateErr != nil {
					return ExperimentReport{}, generateErr
				}
				evaluations := make([]EvaluationResult, 0, len(evaluators))
				for _, check := range evaluators {
					evaluations = append(evaluations, check.Evaluate(testCase, response))
				}
				results = append(results, CaseResult{
					CaseID:      testCase.CaseID,
					VariantID:   variant.ID,
					Trial:       trial,
					Response:    response,
					Evaluations: evaluations,
				})
			}
		}
	}
	return ExperimentReport{
		SchemaVersion:    1,
		ExperimentID:     runner.Manifest.ExperimentID,
		Client:           runner.Client.Name(),
		VariantSummaries: summarise(cases, results),
		TagSummaries:     summariseTags(cases, results),
		CaseResults:      results,
	}, nil
}

func summarise(
	cases []ExperimentCase,
	results []CaseResult,
) map[string]map[string]float64 {
	caseByID := map[string]ExperimentCase{}
	for _, testCase := range cases {
		caseByID[testCase.CaseID] = testCase
	}
	sums := map[string]map[string]float64{}
	counts := map[string]map[string]int{}
	expectedLabels := map[string][]string{}
	actualLabels := map[string][]string{}
	for _, result := range results {
		if sums[result.VariantID] == nil {
			sums[result.VariantID] = map[string]float64{}
			counts[result.VariantID] = map[string]int{}
		}
		for _, evaluation := range result.Evaluations {
			sums[result.VariantID]["pass_rate"] += boolFloat(evaluation.Passed)
			counts[result.VariantID]["pass_rate"]++
			for name, value := range evaluation.Metrics {
				sums[result.VariantID][name] += value
				counts[result.VariantID][name]++
			}
		}
		if label := stringValue(caseByID[result.CaseID].Expected["label"]); label != "" {
			expectedLabels[result.VariantID] = append(
				expectedLabels[result.VariantID],
				strings.ToLower(label),
			)
			actualLabels[result.VariantID] = append(
				actualLabels[result.VariantID],
				strings.ToLower(strings.TrimSpace(result.Response.Text)),
			)
		}
	}
	for variant, metrics := range sums {
		for name, value := range metrics {
			metrics[name] = round6(value / float64(counts[variant][name]))
		}
		if len(expectedLabels[variant]) > 0 {
			metrics["macro_f1"] = round6(
				macroF1(expectedLabels[variant], actualLabels[variant]),
			)
		}
		frequencies := map[string]int{}
		total := 0
		for _, result := range results {
			if result.VariantID == variant {
				frequencies[result.Response.Text]++
				total++
			}
		}
		modal := 0
		for _, count := range frequencies {
			if count > modal {
				modal = count
			}
		}
		metrics["unique_response_count"] = float64(len(frequencies))
		metrics["unique_response_ratio"] = round6(float64(len(frequencies)) / float64(total))
		metrics["modal_response_rate"] = round6(float64(modal) / float64(total))
	}
	return sums
}

func summariseTags(
	cases []ExperimentCase,
	results []CaseResult,
) map[string]map[string]map[string]float64 {
	caseByID := map[string]ExperimentCase{}
	for _, testCase := range cases {
		caseByID[testCase.CaseID] = testCase
	}
	sums := map[string]map[string]map[string]float64{}
	counts := map[string]map[string]map[string]int{}
	for _, result := range results {
		for _, tag := range caseByID[result.CaseID].Tags {
			if sums[result.VariantID] == nil {
				sums[result.VariantID] = map[string]map[string]float64{}
				counts[result.VariantID] = map[string]map[string]int{}
			}
			if sums[result.VariantID][tag] == nil {
				sums[result.VariantID][tag] = map[string]float64{}
				counts[result.VariantID][tag] = map[string]int{}
			}
			for _, evaluation := range result.Evaluations {
				sums[result.VariantID][tag]["pass_rate"] += boolFloat(evaluation.Passed)
				counts[result.VariantID][tag]["pass_rate"]++
				for name, value := range evaluation.Metrics {
					sums[result.VariantID][tag][name] += value
					counts[result.VariantID][tag][name]++
				}
			}
		}
	}
	for variant, tags := range sums {
		for tag, metrics := range tags {
			for name, value := range metrics {
				metrics[name] = round6(value / float64(counts[variant][tag][name]))
			}
		}
	}
	return sums
}

func macroF1(expected, actual []string) float64 {
	labelSet := map[string]bool{}
	for _, label := range expected {
		labelSet[label] = true
	}
	for _, label := range actual {
		labelSet[label] = true
	}
	labels := make([]string, 0, len(labelSet))
	for label := range labelSet {
		labels = append(labels, label)
	}
	sort.Strings(labels)
	if len(labels) == 0 {
		return 0
	}
	total := 0.0
	for _, label := range labels {
		tp, fp, fn := 0, 0, 0
		for index := range expected {
			switch {
			case expected[index] == label && actual[index] == label:
				tp++
			case expected[index] != label && actual[index] == label:
				fp++
			case expected[index] == label && actual[index] != label:
				fn++
			}
		}
		denominator := (2 * tp) + fp + fn
		if denominator > 0 {
			total += float64(2*tp) / float64(denominator)
		}
	}
	return total / float64(len(labels))
}

func round6(value float64) float64 {
	text := fmt.Sprintf("%.6f", value)
	var rounded float64
	fmt.Sscanf(text, "%f", &rounded)
	return rounded
}
