package tahmures

import (
	"encoding/json"
	"os"
	"reflect"
	"testing"
)

type versionAttributionCorpus struct {
	SchemaVersion int `json:"schema_version"`
	Cases         []struct {
		ID       string           `json:"id"`
		Expected map[string]any   `json:"expected"`
		Response string           `json:"response"`
		ResultGo EvaluationResult `json:"result_go"`
	} `json:"cases"`
}

func TestVersionAttributionSharedCompleteResults(t *testing.T) {
	data, err := os.ReadFile("../../shared/version_attribution_cases.json")
	if err != nil {
		t.Fatal(err)
	}
	var corpus versionAttributionCorpus
	if err := json.Unmarshal(data, &corpus); err != nil {
		t.Fatal(err)
	}
	if corpus.SchemaVersion != 1 {
		t.Fatal("unsupported attribution corpus")
	}
	evaluator, err := BuildEvaluator(EvaluatorSpec{Name: "operational_drift", Type: "operational_drift"})
	if err != nil {
		t.Fatal(err)
	}
	for _, c := range corpus.Cases {
		t.Run(c.ID, func(t *testing.T) {
			result := evaluator.Evaluate(ExperimentCase{CaseID: c.ID, Expected: c.Expected}, GenerationResponse{Text: c.Response, ModelID: "fixture"})
			if !reflect.DeepEqual(result, c.ResultGo) {
				t.Fatalf("actual=%#v expected=%#v", result, c.ResultGo)
			}
			if len(result.Metrics) != 3 {
				t.Fatalf("metric keys changed: %v", result.Metrics)
			}
			for _, key := range []string{"drift_decision_accuracy", "finding_recall", "version_attribution"} {
				if _, exists := result.Metrics[key]; !exists {
					t.Fatalf("missing metric %q", key)
				}
			}
		})
	}
}

func TestVersionAttributionNativeExpectedLists(t *testing.T) {
	evaluator, err := BuildEvaluator(EvaluatorSpec{Name: "drift", Type: "operational_drift"})
	if err != nil {
		t.Fatal(err)
	}
	for _, c := range []struct {
		name   string
		wanted any
		actual string
		match  bool
	}{
		{"string_slice_match", []string{"prompt"}, `["prompt"]`, true},
		{"string_slice_missing", []string{"prompt"}, `[]`, false},
		{"string_slice_extras", []string{"prompt"}, `["prompt","temperature"]`, false},
		{"any_slice_match", []any{"prompt"}, `["prompt"]`, true},
		{"string_slice_empty", []string{}, `[]`, true},
		{"any_slice_empty", []any{}, `[]`, true},
		{"nil_string_slice", []string(nil), `[]`, false},
		{"nil_any_slice", []any(nil), `[]`, false},
		{"nil_value", nil, `[]`, false},
		{"non_string_slice", []int{1}, `[]`, false},
		{"mixed_slice", []any{"prompt", 1}, `["prompt"]`, false},
		{"null_element", []any{nil}, `[]`, false},
	} {
		t.Run(c.name, func(t *testing.T) {
			result := evaluator.Evaluate(ExperimentCase{Expected: map[string]any{"passed": true, "findings": []any{}, "changed_versions": c.wanted}}, GenerationResponse{Text: `{"passed":true,"findings":[],"changed_versions":` + c.actual + `}`})
			want := boolFloat(c.match)
			if result.Passed != c.match || result.Score != want || result.Metrics["version_attribution"] != want {
				t.Fatalf("actual=%#v match=%t", result, c.match)
			}
		})
	}
}

func TestVersionAttributionPreservesFindingRecall(t *testing.T) {
	evaluator, err := BuildEvaluator(EvaluatorSpec{Name: "drift", Type: "operational_drift"})
	if err != nil {
		t.Fatal(err)
	}
	for _, c := range []struct {
		name   string
		wanted []any
		actual string
		recall float64
		passed bool
	}{
		{"false_extras", []any{"cost_slo"}, `["cost_slo","invented_finding"]`, 1, true},
		{"partial_credit", []any{"cost_slo", "quality_drift"}, `["cost_slo"]`, .5, false},
	} {
		t.Run(c.name, func(t *testing.T) {
			result := evaluator.Evaluate(ExperimentCase{Expected: map[string]any{"passed": false, "findings": c.wanted, "changed_versions": []any{"prompt"}}}, GenerationResponse{Text: `{"passed":false,"findings":` + c.actual + `,"changed_versions":["prompt"]}`})
			if result.Passed != c.passed || result.Metrics["finding_recall"] != c.recall || result.Metrics["version_attribution"] != 1 {
				t.Fatalf("unrelated finding behavior changed: %#v", result)
			}
		})
	}
}
