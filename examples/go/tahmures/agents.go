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
	// Python validates limits at construction. The Go value API must check
	// them on every call before any normalization or control transition.
	limits := controller.Limits
	if limits.MaxSteps < 1 || limits.MaxToolCalls < 1 || limits.MaxTokens < 1 || limits.Deadline < 1 {
		return state, fmt.Errorf("agent limits must be positive")
	}
	if state.Status != "" && state.Status != "running" {
		return state, fmt.Errorf("terminal agent states are immutable")
	}
	if event.TokenCost < 0 || event.ToolCalls < 0 {
		return state, fmt.Errorf("agent resource increments must be nonnegative")
	}
	if state.Status == "" {
		state.Status = "running"
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
	// Charge only accepted steps. A rejected event must retain all counters.
	switch {
	case state.Steps >= limits.MaxSteps:
		state.Status, state.Reason = "failed", "step_budget"
		return state, nil
	case agentBudgetExceeded(state.ToolCalls, event.ToolCalls, limits.MaxToolCalls):
		state.Status, state.Reason = "failed", "tool_budget"
		return state, nil
	case agentBudgetExceeded(state.Tokens, event.TokenCost, limits.MaxTokens):
		state.Status, state.Reason = "failed", "token_budget"
		return state, nil
	}
	state.Steps++
	state.ToolCalls += event.ToolCalls
	state.Tokens += event.TokenCost
	return state, nil
}

func agentBudgetExceeded(used, increment, limit int) bool {
	// Limits are positive and increments nonnegative. The unsigned difference
	// represents remaining capacity without signed overflow, even for imported
	// negative counters; this adds no new validation policy for existing state.
	return used > limit || uint(increment) > uint(limit)-uint(used)
}
