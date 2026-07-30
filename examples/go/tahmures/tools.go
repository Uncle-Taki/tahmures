package tahmures

import (
	"encoding/json"
	"fmt"
)

type ToolDefinition struct {
	Name             string
	Effect           string
	RequiredScopes   []string
	ArgumentContract OutputContract
	RequiresApproval bool
}

type ToolCall struct {
	Name      string
	Arguments map[string]any
}

type ToolDecision struct {
	Allowed bool
	Reason  string
	Call    ToolCall
}

type ToolGate struct {
	definitions map[string]ToolDefinition
}

func NewToolGate(definitions []ToolDefinition) (ToolGate, error) {
	result := ToolGate{definitions: map[string]ToolDefinition{}}
	for _, definition := range definitions {
		if definition.Name == "" || (definition.Effect != "read" && definition.Effect != "write") {
			return ToolGate{}, fmt.Errorf("tools need names and read or write effects")
		}
		if _, exists := result.definitions[definition.Name]; exists {
			return ToolGate{}, fmt.Errorf("tool names must be unique")
		}
		result.definitions[definition.Name] = definition
	}
	return result, nil
}

func (gate ToolGate) Evaluate(call ToolCall, scopes []string, approved bool) ToolDecision {
	definition, exists := gate.definitions[call.Name]
	if !exists {
		return ToolDecision{false, "unknown_tool", call}
	}
	raw, _ := json.Marshal(call.Arguments)
	if !definition.ArgumentContract.Validate(string(raw)).Valid {
		return ToolDecision{false, "invalid_arguments", call}
	}
	granted := map[string]bool{}
	for _, scope := range scopes {
		granted[scope] = true
	}
	for _, scope := range definition.RequiredScopes {
		if !granted[scope] {
			return ToolDecision{false, "insufficient_scope", call}
		}
	}
	if definition.RequiresApproval && !approved {
		return ToolDecision{false, "approval_required", call}
	}
	return ToolDecision{true, "allowed", call}
}

type FixtureToolExecutor struct{}

func (FixtureToolExecutor) Execute(decision ToolDecision) (map[string]any, error) {
	if !decision.Allowed {
		return nil, fmt.Errorf("%s", decision.Reason)
	}
	return map[string]any{"tool": decision.Call.Name, "status": "fixture_executed"}, nil
}
