package tahmures

import "testing"

func TestPhase2Contracts(t *testing.T) {
	template := PromptTemplate{
		TemplateID: "decree-v1",
		Source:     "Send ${allowance} to ${province}",
		Fields: []TemplateField{
			{Name: "allowance", ValueType: "integer", Required: true},
			{Name: "province", ValueType: "string", Required: true},
		},
	}
	rendered, err := template.Render(map[string]any{"allowance": 12, "province": "Ray"})
	if err != nil || rendered.Text != "Send 12 to Ray" {
		t.Fatalf("unexpected render: %#v %v", rendered, err)
	}
	if _, err := template.Render(map[string]any{"allowance": "12", "province": "Ray"}); err == nil {
		t.Fatal("expected template type error")
	}

	contract := OutputContract{Fields: []FieldContract{
		{Name: "id", ValueType: "string", Required: true},
		{Name: "status", ValueType: "string", Required: true, AllowedValues: []any{"current"}},
		{Name: "count", ValueType: "integer", Required: true},
	}}
	if !contract.Validate(`{"id":"T-1","status":"current","count":2}`).Valid {
		t.Fatal("expected contract to pass")
	}
	if contract.Validate(`{"id":"T-1","status":"other","count":2}`).Valid {
		t.Fatal("expected enum contract to fail")
	}

	plan := WorkflowPlan{Steps: []WorkflowStep{
		{ID: "locate", Inputs: []string{"mission"}, Outputs: []string{"position"}},
		{ID: "assess", DependsOn: []string{"locate"}, Inputs: []string{"position"}, Outputs: []string{"condition"}, Checkpoint: true},
		{ID: "report", DependsOn: []string{"assess"}, Inputs: []string{"condition"}, Outputs: []string{"record"}, Terminal: true},
	}}
	ready, err := plan.Ready([]string{"locate"})
	if err != nil || len(ready) != 1 || ready[0].ID != "assess" {
		t.Fatalf("unexpected ready steps: %#v %v", ready, err)
	}

	selection, err := SelectContext([]ContextItem{
		{ID: "task", Text: "task", TokenEstimate: 2, Priority: 10, Provenance: "application", Mandatory: true},
		{ID: "low", Text: "old", TokenEstimate: 3, Priority: 1, Provenance: "archive:L"},
		{ID: "high", Text: "decisive", TokenEstimate: 3, Priority: 9, Provenance: "archive:H"},
	}, 5)
	if err != nil || len(selection.Items) != 2 || selection.Items[1].ID != "high" {
		t.Fatalf("unexpected context selection: %#v %v", selection, err)
	}
}
