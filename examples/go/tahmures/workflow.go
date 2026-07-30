package tahmures

import (
	"fmt"
	"sort"
)

type WorkflowStep struct {
	ID         string
	DependsOn  []string
	Inputs     []string
	Outputs    []string
	Checkpoint bool
	Terminal   bool
}

type WorkflowPlan struct {
	Steps []WorkflowStep
}

func (item WorkflowPlan) Validate() error {
	steps := map[string]WorkflowStep{}
	terminal := 0
	for _, step := range item.Steps {
		if step.ID == "" {
			return fmt.Errorf("workflow step ID cannot be empty")
		}
		if _, exists := steps[step.ID]; exists {
			return fmt.Errorf("duplicate workflow step ID: %s", step.ID)
		}
		if len(step.Inputs) == 0 || len(step.Outputs) == 0 {
			return fmt.Errorf("workflow step %s must declare inputs and outputs", step.ID)
		}
		steps[step.ID] = step
		if step.Terminal {
			terminal++
		}
	}
	if len(steps) == 0 || terminal != 1 {
		return fmt.Errorf("workflow requires steps and exactly one terminal state")
	}
	for _, step := range item.Steps {
		for _, dependency := range step.DependsOn {
			if _, ok := steps[dependency]; !ok {
				return fmt.Errorf("unknown dependency %s", dependency)
			}
			if dependency == step.ID {
				return fmt.Errorf("step %s depends on itself", step.ID)
			}
		}
	}
	visiting, visited := map[string]bool{}, map[string]bool{}
	var walk func(string) error
	walk = func(id string) error {
		if visiting[id] {
			return fmt.Errorf("workflow contains a dependency cycle")
		}
		if visited[id] {
			return nil
		}
		visiting[id] = true
		for _, dependency := range steps[id].DependsOn {
			if err := walk(dependency); err != nil {
				return err
			}
		}
		delete(visiting, id)
		visited[id] = true
		return nil
	}
	for id := range steps {
		if err := walk(id); err != nil {
			return err
		}
	}
	checkpoint := false
	for _, step := range item.Steps {
		checkpoint = checkpoint || step.Checkpoint
	}
	if !checkpoint {
		return fmt.Errorf("workflow requires at least one checkpoint")
	}
	return nil
}

func (item WorkflowPlan) Ready(completed []string) ([]WorkflowStep, error) {
	if err := item.Validate(); err != nil {
		return nil, err
	}
	known, done := map[string]bool{}, map[string]bool{}
	for _, step := range item.Steps {
		known[step.ID] = true
	}
	for _, id := range completed {
		if !known[id] {
			return nil, fmt.Errorf("unknown completed step: %s", id)
		}
		done[id] = true
	}
	ready := []WorkflowStep{}
	for _, step := range item.Steps {
		if done[step.ID] {
			continue
		}
		ok := true
		for _, dependency := range step.DependsOn {
			ok = ok && done[dependency]
		}
		if ok {
			ready = append(ready, step)
		}
	}
	sort.Slice(ready, func(i, j int) bool { return ready[i].ID < ready[j].ID })
	return ready, nil
}
