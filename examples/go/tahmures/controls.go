package tahmures

import "fmt"

type ControlRequirement struct {
	TaskID                                                                                                                                       string
	LanguageInterpretation, StructuredOutput, HardInvariant, AuthoritativeState, Permission, ExternalMutation, Irreversible, SubjectiveJudgement bool
}
type ControlDecision struct {
	Primary     string
	Supporting  []string
	HumanReview bool
	Reasons     []string
}

func SelectControls(r ControlRequirement) (ControlDecision, error) {
	if r.TaskID == "" {
		return ControlDecision{}, fmt.Errorf("control requirement needs a task ID")
	}
	controls, reasons := []string{}, []string{}
	if r.LanguageInterpretation {
		controls = append(controls, "language_model")
	}
	if r.StructuredOutput {
		controls = append(controls, "schema_validation")
	}
	if r.HardInvariant {
		controls = append(controls, "deterministic_code")
		reasons = append(reasons, "hard_invariant")
	}
	if r.AuthoritativeState {
		controls = append(controls, "database_constraint")
		reasons = append(reasons, "authoritative_state")
	}
	if r.Permission || r.ExternalMutation {
		controls = append(controls, "access_control")
		reasons = append(reasons, "capability_boundary")
	}
	human := r.SubjectiveJudgement || r.Irreversible
	if human {
		controls = append(controls, "human_judgement")
		reasons = append(reasons, "accountable_judgement")
	}
	if len(controls) == 0 {
		controls = append(controls, "deterministic_code")
		reasons = append(reasons, "default_mechanism")
	}
	set := stringSetAny(controls)
	primary := ""
	for _, candidate := range []string{"database_constraint", "access_control", "deterministic_code", "human_judgement", "schema_validation", "language_model"} {
		if set[candidate] {
			primary = candidate
			break
		}
	}
	support := []string{}
	for _, item := range controls {
		if item != primary {
			support = append(support, item)
		}
	}
	return ControlDecision{primary, support, human, reasons}, nil
}
