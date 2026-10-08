package tahmures

import (
	"encoding/json"
	"math"
	"math/big"
	"os"
	"reflect"
	"strconv"
	"strings"
	"testing"
)

// Integer strings/symbols preserve types and exercise each host's actual MaxInt.
type agentFixtureInteger int

func (n *agentFixtureInteger) UnmarshalJSON(data []byte) error {
	var text string
	if err := json.Unmarshal(data, &text); err != nil {
		return err
	}
	for _, symbol := range []struct {
		name  string
		value int
	}{{"MaxInt", math.MaxInt}, {"MinInt", math.MinInt}} {
		if strings.HasPrefix(text, symbol.name) {
			suffix := text[len(symbol.name):]
			if suffix == "" {
				*n = agentFixtureInteger(symbol.value)
				return nil
			}
			offset, err := strconv.Atoi(suffix)
			if err != nil {
				return err
			}
			*n = agentFixtureInteger(symbol.value + offset)
			return nil
		}
	}
	value, err := strconv.Atoi(text)
	if err != nil {
		return err
	}
	*n = agentFixtureInteger(value)
	return nil
}

type agentFixtureState struct {
	Goal        string              `json:"goal"`
	GoalVersion agentFixtureInteger `json:"goal_version"`
	Status      string              `json:"status"`
	Steps       agentFixtureInteger `json:"steps"`
	ToolCalls   agentFixtureInteger `json:"tool_calls"`
	Tokens      agentFixtureInteger `json:"tokens"`
	Reason      string              `json:"reason"`
}

func (s agentFixtureState) state() AgentRunState {
	return AgentRunState{s.Goal, int(s.GoalVersion), s.Status, int(s.Steps), int(s.ToolCalls), int(s.Tokens), s.Reason}
}

type agentFixtureEvent struct {
	Kind        string              `json:"kind"`
	GoalVersion agentFixtureInteger `json:"goal_version"`
	TokenCost   agentFixtureInteger `json:"token_cost"`
	ToolCalls   agentFixtureInteger `json:"tool_calls"`
	At          agentFixtureInteger `json:"at"`
}

func (e agentFixtureEvent) event() AgentEvent {
	return AgentEvent{e.Kind, int(e.GoalVersion), int(e.TokenCost), int(e.ToolCalls), int(e.At)}
}

type agentFixtureLimits struct {
	MaxSteps     agentFixtureInteger `json:"max_steps"`
	MaxToolCalls agentFixtureInteger `json:"max_tool_calls"`
	MaxTokens    agentFixtureInteger `json:"max_tokens"`
	Deadline     agentFixtureInteger `json:"deadline"`
}

func (l agentFixtureLimits) limits() AgentLimits {
	return AgentLimits{int(l.MaxSteps), int(l.MaxToolCalls), int(l.MaxTokens), int(l.Deadline)}
}

type agentFixtureResult struct {
	State agentFixtureState `json:"state"`
	Error string            `json:"error"`
}
type agentFixtureCorpus struct {
	SchemaVersion int `json:"schema_version"`
	Cases         []struct {
		ID       string             `json:"id"`
		Limits   agentFixtureLimits `json:"limits"`
		State    agentFixtureState  `json:"state"`
		Event    agentFixtureEvent  `json:"event"`
		Expected agentFixtureResult `json:"expected"`
	} `json:"cases"`
	Traces []struct {
		ID      string             `json:"id"`
		Limits  agentFixtureLimits `json:"limits"`
		State   agentFixtureState  `json:"state"`
		Entries []struct {
			Event    agentFixtureEvent  `json:"event"`
			Expected agentFixtureResult `json:"expected"`
		} `json:"entries"`
	} `json:"traces"`
}

func loadAgentCorpus(t *testing.T) agentFixtureCorpus {
	t.Helper()
	data, err := os.ReadFile("../../shared/agent_controller_cases.json")
	if err != nil {
		t.Fatal(err)
	}
	var corpus agentFixtureCorpus
	if err := json.Unmarshal(data, &corpus); err != nil {
		t.Fatal(err)
	}
	if corpus.SchemaVersion != 1 {
		t.Fatal("unsupported agent corpus version")
	}
	return corpus
}

func assertAgentResult(t *testing.T, actual AgentRunState, err error, expected agentFixtureResult) {
	t.Helper()
	message := ""
	if err != nil {
		message = err.Error()
	}
	if actual != expected.State.state() || message != expected.Error {
		t.Fatalf("state=%#v error=%q; want state=%#v error=%q", actual, message, expected.State.state(), expected.Error)
	}
}

func TestAgentSharedCases(t *testing.T) {
	for _, c := range loadAgentCorpus(t).Cases {
		t.Run(c.ID, func(t *testing.T) {
			controller := RunController{Limits: c.Limits.limits()}
			state, event := c.State.state(), c.Event.event()
			beforeState, beforeLimits := state, controller.Limits
			actual, err := controller.Apply(state, event)
			assertAgentResult(t, actual, err, c.Expected)
			if state != beforeState || controller.Limits != beforeLimits {
				t.Fatal("input mutated")
			}
		})
	}
}

func TestAgentSharedTraces(t *testing.T) {
	for _, trace := range loadAgentCorpus(t).Traces {
		t.Run(trace.ID, func(t *testing.T) {
			controller := RunController{Limits: trace.Limits.limits()}
			state := trace.State.state()
			for _, entry := range trace.Entries {
				actual, err := controller.Apply(state, entry.Event.event())
				assertAgentResult(t, actual, err, entry.Expected)
				state = actual
			}
		})
	}
}

func TestAgentZeroValueCompatibility(t *testing.T) {
	state := AgentRunState{Goal: "inspect", GoalVersion: 1}
	valid := RunController{Limits: AgentLimits{1, 1, 1, 1}}
	for _, kind := range []string{"step", "cancel", "complete"} {
		r, err := valid.Apply(state, AgentEvent{Kind: kind, GoalVersion: 1, TokenCost: 1, ToolCalls: 1, At: 1})
		if err != nil {
			t.Fatal(err)
		}
		want := state
		switch kind {
		case "step":
			want.Status = "running"
			want.Steps, want.ToolCalls, want.Tokens = 1, 1, 1
		case "cancel":
			want.Status, want.Reason = "cancelled", "cancelled"
		case "complete":
			want.Status, want.Reason = "completed", "completed"
		}
		if r != want {
			t.Fatalf("zero-value compatibility: got %#v want %#v", r, want)
		}
	}
	for _, kind := range []string{"step", "cancel", "complete"} {
		r, err := valid.Apply(state, AgentEvent{Kind: kind, TokenCost: -1})
		if err == nil || err.Error() != "agent resource increments must be nonnegative" || r != state {
			t.Fatalf("negative input altered zero state: %#v %v", r, err)
		}
		r, err = (RunController{}).Apply(state, AgentEvent{Kind: kind})
		if err == nil || err.Error() != "agent limits must be positive" || r != state {
			t.Fatalf("invalid limits altered zero state: %#v %v", r, err)
		}
	}
}

func TestAgentBudgetBoundaryMatrix(t *testing.T) {
	// Independent mathematical expectations avoid computing signed sums that
	// would reproduce the original overflow bug inside the test oracle.
	for _, limit := range []int{1, 2, math.MaxInt - 1, math.MaxInt} {
		for _, used := range []int{0, 1, limit - 1, limit, math.MaxInt} {
			for _, increment := range []int{0, 1, 2, math.MaxInt} {
				for _, resource := range []string{"tokens", "tools"} {
					c := RunController{Limits: AgentLimits{2, limit, limit, 10}}
					state := AgentRunState{Goal: "inspect", GoalVersion: 1, Status: "running"}
					event := AgentEvent{Kind: "step", GoalVersion: 1, At: 1}
					if resource == "tokens" {
						state.Tokens, event.TokenCost = used, increment
					} else {
						state.ToolCalls, event.ToolCalls = used, increment
					}
					sum := new(big.Int).Add(big.NewInt(int64(used)), big.NewInt(int64(increment)))
					exceeds := sum.Cmp(big.NewInt(int64(limit))) > 0
					result, err := c.Apply(state, event)
					if err != nil {
						t.Fatal(err)
					}
					want := state
					if exceeds {
						want.Status = "failed"
						if resource == "tokens" {
							want.Reason = "token_budget"
						} else {
							want.Reason = "tool_budget"
						}
					} else {
						want.Steps = 1
						if resource == "tokens" {
							want.Tokens += increment
						} else {
							want.ToolCalls += increment
						}
					}
					if !reflect.DeepEqual(result, want) {
						t.Fatalf("%s limit=%d used=%d increment=%d: got %#v want %#v", resource, limit, used, increment, result, want)
					}
				}
			}
		}
	}
}
