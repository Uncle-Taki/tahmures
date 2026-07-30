package tahmures

import (
	"encoding/json"
	"testing"
)

func integer(value int) *int { return &value }

func TestPhase3ContextRetrievalAndMemory(t *testing.T) {
	items := []ContextItem{
		{ID: "rule", Text: "allow", TokenEstimate: 2, Priority: 9, Provenance: "policy", Mandatory: true, ClaimGroup: "gate"},
		{ID: "conflict", Text: "deny", TokenEstimate: 2, Priority: 8, Provenance: "archive", ClaimGroup: "gate"},
		{ID: "private", Text: "secret", TokenEstimate: 2, Priority: 10, Provenance: "private", Scope: "b"},
	}
	pack, err := AssembleContext(items, ContextPolicy{InputBudget: 6, Scope: "a"})
	if err != nil || len(pack.Items) != 2 || len(pack.Conflicts) != 1 {
		t.Fatalf("unexpected context package: %#v %v", pack, err)
	}
	duplicatePack, err := AssembleContext([]ContextItem{
		{
			ID: "optional", Text: "same", TokenEstimate: 1,
			Priority: 100, Provenance: "cache",
		},
		{
			ID: "rule", Text: "same", TokenEstimate: 1,
			Priority: 1, Provenance: "policy", Mandatory: true,
		},
	}, ContextPolicy{InputBudget: 2})
	if err != nil || len(duplicatePack.Items) != 1 ||
		duplicatePack.Items[0].ID != "rule" {
		t.Fatalf("mandatory duplicate was not preserved: %#v %v", duplicatePack, err)
	}
	retriever := InMemoryRetriever{Chunks: []RetrievedChunk{
		{ChunkID: "OLD", Text: "safe pass", Provenance: "map", ValidUntil: integer(2)},
		{ChunkID: "CUR", Text: "safe pass", Provenance: "survey"},
	}}
	found, err := retriever.Retrieve(RetrievalRequest{Query: "safe pass", Limit: 2, AsOf: 3})
	if err != nil || len(found) != 1 || found[0].ChunkID != "CUR" {
		t.Fatalf("unexpected retrieval: %#v %v", found, err)
	}
	if !ValidateCitations("Use [CUR].", found, true).Valid {
		t.Fatal("expected valid citation")
	}
	store := NewInMemoryStore()
	policy := MemoryPolicy{AllowedKinds: []string{"preference"}, MaxTTL: 20}
	if err := store.Remember(MemoryRecord{
		MemoryID: "m1", SubjectID: "u", Scope: "a", Kind: "preference",
		Value: "east", Provenance: "user", CreatedAt: 1, ExpiresAt: 10,
	}, policy, 2); err != nil {
		t.Fatal(err)
	}
	if len(store.Recall(MemoryQuery{SubjectID: "u", Scope: "b", AsOf: 3})) != 0 {
		t.Fatal("memory crossed scope")
	}
}

func TestPhase3ToolAgentAndHandoff(t *testing.T) {
	gate, err := NewToolGate([]ToolDefinition{{
		Name: "open", Effect: "write", RequiredScopes: []string{"gate:write"},
		RequiresApproval: true,
		ArgumentContract: OutputContract{Fields: []FieldContract{
			{Name: "gate", ValueType: "string", Required: true},
		}},
	}})
	if err != nil {
		t.Fatal(err)
	}
	call := ToolCall{Name: "open", Arguments: map[string]any{"gate": "north"}}
	if gate.Evaluate(call, []string{"gate:write"}, false).Reason != "approval_required" {
		t.Fatal("approval was not required")
	}
	controller := RunController{Limits: AgentLimits{MaxSteps: 1, MaxToolCalls: 1, MaxTokens: 10, Deadline: 10}}
	state, err := controller.Apply(
		AgentRunState{Goal: "travel", GoalVersion: 2, Status: "running"},
		AgentEvent{Kind: "step", GoalVersion: 2, TokenCost: 5, ToolCalls: 1, At: 1},
	)
	if err != nil || state.Steps != 1 {
		t.Fatal("agent step failed")
	}
	envelope := HandoffEnvelope{
		SchemaVersion: 1, HandoffID: "h1", Goal: "travel", GoalVersion: 2,
		Authority: "royal", Artifacts: []ArtifactRef{{ArtifactID: "route", Provenance: "survey"}},
		PermittedNextActions: []string{"inspect"}, ExpiresAt: 10,
	}
	result := (HandoffContract{AllowedActions: []string{"inspect"}}).Validate(envelope, 2, 1)
	if !result.Valid {
		t.Fatalf("unexpected handoff failure: %#v", result)
	}
}

func TestPhase3Evaluators(t *testing.T) {
	tests := []struct {
		kind     string
		expected map[string]any
		payload  map[string]any
	}{
		{"context_package", map[string]any{
			"required_selected": []any{"rule"}, "forbidden_selected": []any{"noise"},
		}, map[string]any{"selected": []string{"rule"}, "excluded": []string{"noise"}}},
		{"retrieval_quality", map[string]any{
			"relevant_ids": []any{"CURRENT"}, "stale_ids": []any{"OLD"},
		}, map[string]any{"retrieved": []string{"CURRENT"}}},
		{"memory_state", map[string]any{
			"active_ids": []any{"winter"}, "forbidden_ids": []any{"spring"},
		}, map[string]any{"recalled": []string{"winter"}}},
		{"tool_authorization", map[string]any{
			"allowed": false, "reason": "approval_required",
		}, map[string]any{"allowed": false, "reason": "approval_required"}},
		{"agent_trace", map[string]any{
			"status": "cancelled", "reason": "cancelled",
		}, map[string]any{
			"status": "cancelled", "reason": "cancelled", "post_terminal_actions": 0,
		}},
		{"handoff_contract", map[string]any{
			"required_fields": []any{"goal_version", "authority", "permitted_next_actions"},
			"goal_version":    float64(3),
			"allowed_actions": []any{"inspect"},
		}, map[string]any{
			"goal_version": float64(3), "authority": "gatekeeper",
			"permitted_next_actions": []string{"inspect"},
		}},
	}
	for _, test := range tests {
		t.Run(test.kind, func(t *testing.T) {
			check, err := BuildEvaluator(EvaluatorSpec{Name: test.kind, Type: test.kind})
			if err != nil {
				t.Fatal(err)
			}
			encoded, err := json.Marshal(test.payload)
			if err != nil {
				t.Fatal(err)
			}
			result := check.Evaluate(
				ExperimentCase{CaseID: test.kind, Expected: test.expected},
				GenerationResponse{Text: string(encoded)},
			)
			if !result.Passed {
				t.Fatalf("expected passing evaluation: %#v", result)
			}
		})
	}
}
