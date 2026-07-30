package tahmures

import "fmt"

type AgentLimits struct {
	MaxSteps     int
	MaxToolCalls int
	MaxTokens    int
	Deadline     int
}

type AgentEvent struct {
	Kind        string
	GoalVersion int
	TokenCost   int
	ToolCalls   int
	At          int
}

type AgentRunState struct {
	Goal        string
	GoalVersion int
	Status      string
	Steps       int
	ToolCalls   int
	Tokens      int
	Reason      string
}

type RunController struct {
	Limits AgentLimits
}

func (controller RunController) Apply(state AgentRunState, event AgentEvent) (AgentRunState, error) {
	if state.Status == "" {
		state.Status = "running"
	}
	if state.Status != "running" {
		return state, fmt.Errorf("terminal agent states are immutable")
	}
	if event.Kind == "cancel" {
		state.Status, state.Reason = "cancelled", "cancelled"
		return state, nil
	}
	if event.GoalVersion != state.GoalVersion {
		state.Status, state.Reason = "waiting", "stale_goal"
		return state, nil
	}
	if event.At > controller.Limits.Deadline {
		state.Status, state.Reason = "failed", "deadline"
		return state, nil
	}
	if event.Kind == "complete" {
		state.Status, state.Reason = "completed", "completed"
		return state, nil
	}
	if event.Kind != "step" {
		return state, fmt.Errorf("unsupported agent event")
	}
	state.Steps++
	state.ToolCalls += event.ToolCalls
	state.Tokens += event.TokenCost
	switch {
	case state.Steps > controller.Limits.MaxSteps:
		state.Status, state.Reason = "failed", "step_budget"
	case state.ToolCalls > controller.Limits.MaxToolCalls:
		state.Status, state.Reason = "failed", "tool_budget"
	case state.Tokens > controller.Limits.MaxTokens:
		state.Status, state.Reason = "failed", "token_budget"
	}
	return state, nil
}
