package tahmures

import (
	"context"
	"testing"
)

func TestCommittedManifestRuns(t *testing.T) {
	path := "../../../experiments/manifests/ch01-prompt-roles.json"
	manifest, err := LoadManifest(path)
	if err != nil {
		t.Fatal(err)
	}
	fixtures, err := LoadFixtures(ResolveProjectPath(path, manifest.Fixtures))
	if err != nil {
		t.Fatal(err)
	}
	report, err := (ExperimentRunner{
		Manifest:     manifest,
		ManifestPath: path,
		Client:       NewFixtureClient(fixtures),
	}).Run(context.Background())
	if err != nil {
		t.Fatal(err)
	}
	if report.VariantSummaries["explicit"]["accuracy"] != 1 {
		t.Fatalf("expected explicit accuracy 1, got %#v", report.VariantSummaries)
	}
}

func TestFixtureClientRejectsMissingRecord(t *testing.T) {
	client := NewFixtureClient(nil)
	_, err := client.Generate(context.Background(), GenerationRequest{
		Messages: []Message{{Role: "user", Content: "input"}},
		Metadata: map[string]any{
			"case_id":    "missing",
			"variant_id": "baseline",
			"trial":      1,
		},
	})
	if err == nil {
		t.Fatal("expected missing fixture error")
	}
}

func TestEvaluators(t *testing.T) {
	check, err := BuildEvaluator(EvaluatorSpec{Name: "intent", Type: "classification"})
	if err != nil {
		t.Fatal(err)
	}
	result := check.Evaluate(
		ExperimentCase{Expected: map[string]any{"label": "record"}},
		GenerationResponse{Text: "record"},
	)
	if !result.Passed {
		t.Fatalf("expected classification to pass: %#v", result)
	}
}
