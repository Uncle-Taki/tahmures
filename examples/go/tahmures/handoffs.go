package tahmures

import (
	"encoding/json"
	"sort"
)

type ArtifactRef struct {
	ArtifactID string `json:"artifact_id"`
	Provenance string `json:"provenance"`
}

type HandoffEnvelope struct {
	SchemaVersion        int           `json:"schema_version"`
	HandoffID            string        `json:"handoff_id"`
	Goal                 string        `json:"goal"`
	GoalVersion          int           `json:"goal_version"`
	Authority            string        `json:"authority"`
	Constraints          []string      `json:"constraints"`
	Completed            []string      `json:"completed"`
	Artifacts            []ArtifactRef `json:"artifacts"`
	Assumptions          []string      `json:"assumptions"`
	UnresolvedQuestions  []string      `json:"unresolved_questions"`
	PermittedNextActions []string      `json:"permitted_next_actions"`
	ExpiresAt            int           `json:"expires_at"`
}

func (envelope HandoffEnvelope) JSON() ([]byte, error) {
	return json.Marshal(envelope)
}

type HandoffResult struct {
	Valid      bool
	Violations []string
}

type HandoffContract struct {
	AllowedActions []string
}

func (contract HandoffContract) Validate(
	envelope HandoffEnvelope, expectedGoalVersion int, now int,
) HandoffResult {
	violations := []string{}
	if envelope.SchemaVersion != 1 {
		violations = append(violations, "schema_version")
	}
	if envelope.HandoffID == "" || envelope.Goal == "" || envelope.Authority == "" {
		violations = append(violations, "required_identity")
	}
	if envelope.GoalVersion != expectedGoalVersion {
		violations = append(violations, "stale_goal")
	}
	if envelope.ExpiresAt <= now {
		violations = append(violations, "expired")
	}
	for _, artifact := range envelope.Artifacts {
		if artifact.ArtifactID == "" || artifact.Provenance == "" {
			violations = append(violations, "artifact_provenance")
			break
		}
	}
	allowed := map[string]bool{}
	for _, action := range contract.AllowedActions {
		allowed[action] = true
	}
	for _, action := range envelope.PermittedNextActions {
		if !allowed[action] {
			violations = append(violations, "unknown_action")
			break
		}
	}
	sort.Strings(violations)
	return HandoffResult{Valid: len(violations) == 0, Violations: violations}
}
