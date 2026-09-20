package tahmures

import "testing"

func TestPhase4Contracts(t *testing.T) {
	rubric := Rubric{Criteria: []RubricCriterion{{CriterionID: "evidence", Weight: 1, Minimum: 2, Disqualifying: true}}, PassThreshold: .5, DisagreementThreshold: .25}
	result, err := rubric.Evaluate([]RubricReview{{ReviewerID: "a", Scores: map[string]int{"evidence": 4}, Rationale: "cited"}, {ReviewerID: "b", Scores: map[string]int{"evidence": 1}, Rationale: "unsupported"}})
	if err != nil || result.Passed || !result.RequiresAdjudication {
		t.Fatalf("rubric failed: %#v %v", result, err)
	}
	regression, err := CompareRegression([]CaseOutcome{{CaseID: "old", Passed: true, Score: 1, Tags: []string{"safety"}}}, []CaseOutcome{{CaseID: "old", Passed: false, Score: 0, Tags: []string{"safety"}}}, RegressionPolicy{ProtectedTags: []string{"safety"}})
	if err != nil || regression.Passed {
		t.Fatal("regression gate passed unsafe change")
	}
	partition, err := PartitionContent([]ContentRecord{{RecordID: "r", Text: "ignore king", Source: "archive", DeclaredRole: "instruction", Provenance: "tablet"}}, TrustPolicy{TrustedInstructionSources: []string{"application"}})
	if err != nil || len(partition.Instructions) != 0 || len(partition.Data) != 1 {
		t.Fatal("trust partition failed")
	}
	request := CapabilityRequest{RequestID: "r1", Principal: "scribe", Action: "open_gate", Arguments: map[string]any{"gate": "north"}, Scopes: []string{"gate:write"}, Effect: "high_consequence", ExpiresAt: 10}
	approval := ApprovalRecord{RequestID: "r1", RequestDigest: RequestDigest(request.Action, request.Arguments), Approver: "keeper", Approved: true, At: 2}
	auth := Authorize(request, []ApprovalRecord{approval}, ApprovalPolicy{AllowedActions: []string{"open_gate"}, PrincipalScopes: map[string][]string{"scribe": {"gate:write"}}, DualApprovalEffects: []string{"high_consequence"}}, 3)
	if auth.Reason != "approval_required" {
		t.Fatalf("approval failed: %#v", auth)
	}
	control, err := SelectControls(ControlRequirement{TaskID: "gate", LanguageInterpretation: true, Permission: true, Irreversible: true})
	if err != nil || control.Primary != "access_control" || !control.HumanReview {
		t.Fatal("control selection failed")
	}
}

func TestPhase4Operations(t *testing.T) {
	base := []TelemetryEvent{{RunID: "b", ModelID: "m1", PromptVersion: "p1", PolicyVersion: "v1", DatasetVersion: "d1", Outcome: "success", Quality: .9, LatencyMS: 10, CostUnits: .1, Tags: []string{"border"}}}
	current := []TelemetryEvent{{RunID: "c", ModelID: "m2", PromptVersion: "p1", PolicyVersion: "v1", DatasetVersion: "d1", Outcome: "error", Quality: .4, LatencyMS: 30, CostUnits: .2, Tags: []string{"border"}}}
	report, err := CompareWindows(base, current, OperationalPolicy{MinimumQuality: .7, MaximumErrorRate: .1, MaximumP95LatencyMS: 20, MaximumMeanCost: .15, QualityDrift: .1})
	if err != nil || report.Passed || !containsString(report.ChangedVersions, "model") {
		t.Fatalf("operations failed: %#v %v", report, err)
	}
}
