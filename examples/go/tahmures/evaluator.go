package tahmures

import (
	"encoding/json"
	"fmt"
	"regexp"
	"strings"
)

type Evaluator interface {
	Name() string
	Evaluate(ExperimentCase, GenerationResponse) EvaluationResult
}

type evaluator struct {
	name string
	kind string
}

func (item evaluator) Name() string {
	return item.name
}

func BuildEvaluator(spec EvaluatorSpec) (Evaluator, error) {
	switch spec.Type {
	case "classification", "required_terms", "forbidden_terms", "evidence", "json_fields",
		"json_contract", "workflow_trace", "allowed_choice", "rubric_metadata",
		"context_package", "retrieval_quality", "memory_state", "tool_authorization",
		"agent_trace", "handoff_contract":
		return evaluator{name: spec.Name, kind: spec.Type}, nil
	default:
		return nil, fmt.Errorf("unsupported evaluator type: %s", spec.Type)
	}
}

func (item evaluator) Evaluate(
	testCase ExperimentCase,
	response GenerationResponse,
) EvaluationResult {
	switch item.kind {
	case "classification":
		return item.classification(testCase, response)
	case "required_terms":
		return item.terms(testCase, response, false)
	case "forbidden_terms":
		return item.terms(testCase, response, true)
	case "evidence":
		return item.evidence(testCase, response)
	case "json_fields":
		return item.jsonFields(testCase, response)
	case "json_contract":
		return item.jsonContract(testCase, response)
	case "workflow_trace":
		return item.workflowTrace(testCase, response)
	case "allowed_choice":
		return item.allowedChoice(testCase, response)
	case "context_package":
		return item.contextPackage(testCase, response)
	case "retrieval_quality":
		return item.retrievalQuality(testCase, response)
	case "memory_state":
		return item.memoryState(testCase, response)
	case "tool_authorization":
		return item.toolAuthorization(testCase, response)
	case "agent_trace":
		return item.agentTrace(testCase, response)
	case "handoff_contract":
		return item.handoffContract(testCase, response)
	default:
		return item.rubricMetadata(testCase, response)
	}
}

func responseObject(response GenerationResponse) map[string]any {
	value := map[string]any{}
	_ = json.Unmarshal([]byte(response.Text), &value)
	return value
}

func stringSet(values []string) map[string]bool {
	result := map[string]bool{}
	for _, value := range values {
		result[value] = true
	}
	return result
}

func (item evaluator) contextPackage(testCase ExperimentCase, response GenerationResponse) EvaluationResult {
	value := responseObject(response)
	selected := stringSet(stringSlice(value["selected"]))
	excluded := stringSet(stringSlice(value["excluded"]))
	required := stringSlice(testCase.Expected["required_selected"])
	forbidden := stringSlice(testCase.Expected["forbidden_selected"])
	requiredRate := ratioFound(required, selected)
	forbiddenRate := float64(0)
	if len(forbidden) > 0 {
		forbiddenRate = float64(countFound(forbidden, selected)) / float64(len(forbidden))
	}
	exclusionsReported := countFound(forbidden, excluded) == len(forbidden)
	passed := requiredRate == 1 && forbiddenRate == 0 && exclusionsReported
	return EvaluationResult{item.name, passed, boolFloat(passed), map[string]float64{
		"mandatory_retention": requiredRate, "irrelevant_inclusion": forbiddenRate,
		"exclusion_reporting": boolFloat(exclusionsReported),
	}, fmt.Sprintf("selected=%v; excluded=%v", selected, excluded)}
}

func (item evaluator) retrievalQuality(testCase ExperimentCase, response GenerationResponse) EvaluationResult {
	retrieved := stringSlice(responseObject(response)["retrieved"])
	found := stringSet(retrieved)
	relevant := stringSlice(testCase.Expected["relevant_ids"])
	stale := stringSlice(testCase.Expected["stale_ids"])
	recall := float64(countFound(relevant, found)) / float64(max(1, len(relevant)))
	precision := float64(countFound(retrieved, stringSet(relevant))) / float64(max(1, len(retrieved)))
	rank := 0
	relevantSet := stringSet(relevant)
	for index, id := range retrieved {
		if relevantSet[id] {
			rank = index + 1
			break
		}
	}
	reciprocal := float64(0)
	if rank > 0 {
		reciprocal = 1 / float64(rank)
	}
	staleRate := float64(countFound(stale, found)) / float64(max(1, len(stale)))
	passed := recall == 1 && staleRate == 0
	return EvaluationResult{item.name, passed, boolFloat(passed), map[string]float64{
		"recall_at_k": recall, "precision_at_k": precision,
		"reciprocal_rank": reciprocal, "stale_retrieval": staleRate,
	}, fmt.Sprintf("retrieved=%v", retrieved)}
}

func (item evaluator) memoryState(testCase ExperimentCase, response GenerationResponse) EvaluationResult {
	recalled := stringSet(stringSlice(responseObject(response)["recalled"]))
	active := stringSlice(testCase.Expected["active_ids"])
	forbidden := stringSlice(testCase.Expected["forbidden_ids"])
	recall := float64(countFound(active, recalled)) / float64(max(1, len(active)))
	leakage := float64(countFound(forbidden, recalled)) / float64(max(1, len(forbidden)))
	passed := recall == 1 && leakage == 0
	return EvaluationResult{item.name, passed, boolFloat(passed), map[string]float64{
		"active_memory_recall": recall, "forbidden_memory_use": leakage,
	}, fmt.Sprintf("recalled=%v", recalled)}
}

func (item evaluator) toolAuthorization(testCase ExperimentCase, response GenerationResponse) EvaluationResult {
	value := responseObject(response)
	allowed, _ := value["allowed"].(bool)
	expectedAllowed, _ := testCase.Expected["allowed"].(bool)
	reason := stringValue(value["reason"])
	expectedReason := stringValue(testCase.Expected["reason"])
	passed := allowed == expectedAllowed && reason == expectedReason
	return EvaluationResult{item.name, passed, boolFloat(passed), map[string]float64{
		"authorization_accuracy": boolFloat(passed),
		"unauthorized_execution": boolFloat(allowed && !expectedAllowed),
	}, fmt.Sprintf("allowed=%t; reason=%s", allowed, reason)}
}

func (item evaluator) agentTrace(testCase ExperimentCase, response GenerationResponse) EvaluationResult {
	value := responseObject(response)
	status, reason := stringValue(value["status"]), stringValue(value["reason"])
	expectedStatus := stringValue(testCase.Expected["status"])
	expectedReason := stringValue(testCase.Expected["reason"])
	postTerminal, _ := value["post_terminal_actions"].(float64)
	passed := status == expectedStatus && reason == expectedReason && postTerminal == 0
	return EvaluationResult{item.name, passed, boolFloat(passed), map[string]float64{
		"terminal_state_correctness": boolFloat(passed),
		"post_terminal_action_rate":  boolFloat(postTerminal > 0),
	}, fmt.Sprintf("status=%s; reason=%s", status, reason)}
}

func (item evaluator) handoffContract(testCase ExperimentCase, response GenerationResponse) EvaluationResult {
	value := responseObject(response)
	fields := map[string]bool{}
	for name := range value {
		fields[name] = true
	}
	required := stringSlice(testCase.Expected["required_fields"])
	fieldRate := ratioFound(required, fields)
	goalVersion, _ := value["goal_version"].(float64)
	expectedVersion, _ := testCase.Expected["goal_version"].(float64)
	goalValid := goalVersion == expectedVersion
	actions := stringSlice(value["permitted_next_actions"])
	allowed := stringSet(stringSlice(testCase.Expected["allowed_actions"]))
	actionsValid := countFound(actions, allowed) == len(actions)
	authorityValid := stringValue(value["authority"]) != ""
	passed := fieldRate == 1 && goalValid && actionsValid && authorityValid
	return EvaluationResult{item.name, passed, boolFloat(passed), map[string]float64{
		"required_field_coverage": fieldRate, "goal_version_validity": boolFloat(goalValid),
		"authority_preservation": boolFloat(authorityValid),
		"unsafe_action":          boolFloat(!actionsValid),
	}, fmt.Sprintf("fields=%v; actions=%v", fields, actions)}
}

func countFound(required []string, found map[string]bool) int {
	count := 0
	for _, name := range required {
		if found[name] {
			count++
		}
	}
	return count
}

func (item evaluator) jsonContract(
	testCase ExperimentCase,
	response GenerationResponse,
) EvaluationResult {
	required := stringSlice(testCase.Expected["required_fields"])
	requiredSet := map[string]bool{}
	for _, name := range required {
		requiredSet[name] = true
	}
	typeMap, _ := testCase.Expected["field_types"].(map[string]any)
	allowedMap, _ := testCase.Expected["allowed_values"].(map[string]any)
	names := map[string]bool{}
	for name := range requiredSet {
		names[name] = true
	}
	for name := range typeMap {
		names[name] = true
	}
	for name := range allowedMap {
		names[name] = true
	}
	fields := []FieldContract{}
	for name := range names {
		kind := stringValue(typeMap[name])
		if kind == "" {
			kind = "string"
		}
		allowed, _ := allowedMap[name].([]any)
		fields = append(fields, FieldContract{
			Name: name, ValueType: kind, Required: requiredSet[name], AllowedValues: allowed,
		})
	}
	allowExtra, _ := testCase.Expected["allow_extra"].(bool)
	result := (OutputContract{Fields: fields, AllowExtra: allowExtra}).Validate(response.Text)
	reason := "valid"
	if !result.Valid {
		reason = fmt.Sprintf("violations=%v", result.Violations)
	}
	return EvaluationResult{
		Evaluator: item.name, Passed: result.Valid, Score: boolFloat(result.Valid),
		Metrics: map[string]float64{
			"parse_rate":          boolFloat(result.Parsed),
			"structural_validity": boolFloat(result.Valid),
			"invalid_acceptance":  0,
		},
		Reason: reason,
	}
}

func (item evaluator) workflowTrace(
	testCase ExperimentCase,
	response GenerationResponse,
) EvaluationResult {
	required := stringSlice(testCase.Expected["required_stages"])
	requiredCheckpoints := map[string]bool{}
	for _, id := range stringSlice(testCase.Expected["required_checkpoints"]) {
		requiredCheckpoints[id] = true
	}
	document := map[string]any{}
	_ = json.Unmarshal([]byte(response.Text), &document)
	stages, _ := document["stages"].([]any)
	known, found, checkpoints := map[string]bool{}, map[string]bool{}, map[string]bool{}
	dependenciesValid, terminalCount := true, 0
	for _, raw := range stages {
		stage, ok := raw.(map[string]any)
		if !ok {
			dependenciesValid = false
			continue
		}
		id := stringValue(stage["id"])
		if id != "" {
			found[id] = true
		}
		dependencies, ok := stage["depends_on"].([]any)
		if !ok {
			dependenciesValid = false
		}
		for _, rawDependency := range dependencies {
			dependency, ok := rawDependency.(string)
			if !ok || !known[dependency] {
				dependenciesValid = false
			}
		}
		if checkpoint, _ := stage["checkpoint"].(bool); checkpoint {
			checkpoints[id] = true
		}
		if terminal, _ := stage["terminal"].(bool); terminal {
			terminalCount++
		}
		known[id] = true
	}
	coverage := ratioFound(required, found)
	checkpointNames := make([]string, 0, len(requiredCheckpoints))
	for name := range requiredCheckpoints {
		checkpointNames = append(checkpointNames, name)
	}
	checkpointRate := ratioFound(checkpointNames, checkpoints)
	terminalValid := terminalCount == 1
	passed := coverage == 1 && checkpointRate == 1 && dependenciesValid && terminalValid
	return EvaluationResult{
		Evaluator: item.name, Passed: passed, Score: boolFloat(passed),
		Metrics: map[string]float64{
			"required_stage_coverage":    coverage,
			"dependency_validity":        boolFloat(dependenciesValid),
			"checkpoint_presence":        checkpointRate,
			"terminal_state_correctness": boolFloat(terminalValid),
		},
		Reason: fmt.Sprintf("stages=%d; dependencies_valid=%t", len(stages), dependenciesValid),
	}
}

func (item evaluator) allowedChoice(
	testCase ExperimentCase,
	response GenerationResponse,
) EvaluationResult {
	selected := strings.TrimSpace(response.Text)
	document := map[string]any{}
	if json.Unmarshal([]byte(response.Text), &document) == nil {
		if value := stringValue(document["selected"]); value != "" {
			selected = value
		}
	}
	allowed := map[string]bool{}
	for _, value := range stringSlice(testCase.Expected["allowed_choices"]) {
		allowed[value] = true
	}
	passed := allowed[selected]
	preferred := stringValue(testCase.Expected["preferred_choice"])
	stable := preferred == "" || selected == preferred
	return EvaluationResult{
		Evaluator: item.name, Passed: passed, Score: boolFloat(passed),
		Metrics: map[string]float64{
			"allowed_choice": boolFloat(passed), "selection_stability": boolFloat(stable),
		},
		Reason: fmt.Sprintf("selected=%q", selected),
	}
}

func (item evaluator) rubricMetadata(
	testCase ExperimentCase,
	response GenerationResponse,
) EvaluationResult {
	minima, _ := testCase.Expected["rubric_minima"].(map[string]any)
	scores, _ := response.Metadata["rubric_scores"].(map[string]any)
	metrics := map[string]float64{}
	passed := len(minima) > 0
	for criterion, rawMinimum := range minima {
		minimum, minimumOK := rawMinimum.(float64)
		score, scoreOK := scores[criterion].(float64)
		metrics["rubric_"+criterion] = score
		passed = passed && minimumOK && scoreOK && score >= minimum
	}
	if disagreement, ok := response.Metadata["reviewer_disagreement"].(float64); ok {
		metrics["reviewer_disagreement"] = disagreement
	}
	metrics["rubric_threshold"] = boolFloat(passed)
	return EvaluationResult{
		Evaluator: item.name, Passed: passed, Score: boolFloat(passed), Metrics: metrics,
		Reason: fmt.Sprintf("committed human scores=%v; minima=%v", scores, minima),
	}
}

func ratioFound(required []string, found map[string]bool) float64 {
	if len(required) == 0 {
		return 1
	}
	count := 0
	for _, name := range required {
		if found[name] {
			count++
		}
	}
	return float64(count) / float64(len(required))
}

func (item evaluator) classification(
	testCase ExperimentCase,
	response GenerationResponse,
) EvaluationResult {
	expected := strings.ToLower(strings.TrimSpace(stringValue(testCase.Expected["label"])))
	actual := strings.ToLower(strings.TrimSpace(response.Text))
	passed := expected != "" && expected == actual
	score := boolFloat(passed)
	return EvaluationResult{
		Evaluator: item.name,
		Passed:    passed,
		Score:     score,
		Metrics:   map[string]float64{"accuracy": score},
		Reason:    fmt.Sprintf("expected %q; received %q", expected, actual),
	}
}

func (item evaluator) terms(
	testCase ExperimentCase,
	response GenerationResponse,
	forbidden bool,
) EvaluationResult {
	key := "required_terms"
	if forbidden {
		key = "forbidden_terms"
	}
	terms := stringSlice(testCase.Expected[key])
	text := strings.ToLower(response.Text)
	matches := []string{}
	for _, term := range terms {
		if strings.Contains(text, strings.ToLower(term)) {
			matches = append(matches, term)
		}
	}
	score := 1.0
	if len(terms) > 0 {
		score = float64(len(matches)) / float64(len(terms))
		if forbidden {
			score = 1 - score
		}
	}
	return EvaluationResult{
		Evaluator: item.name,
		Passed:    score == 1,
		Score:     score,
		Metrics:   map[string]float64{item.name: score},
		Reason:    fmt.Sprintf("matches=%v", matches),
	}
}

var citationPattern = regexp.MustCompile(`\[([A-Z][A-Z0-9_-]*)\]`)

func (item evaluator) evidence(
	testCase ExperimentCase,
	response GenerationResponse,
) EvaluationResult {
	allowed := map[string]bool{}
	for _, value := range stringSlice(testCase.Expected["allowed_evidence"]) {
		allowed[value] = true
	}
	citations := citationPattern.FindAllStringSubmatch(response.Text, -1)
	valid := len(citations) > 0
	for _, match := range citations {
		if !allowed[match[1]] {
			valid = false
		}
	}
	answerable, _ := testCase.Expected["answerable"].(bool)
	abstained := false
	for _, phrase := range stringSlice(testCase.Expected["abstain_phrases"]) {
		if strings.Contains(strings.ToLower(response.Text), strings.ToLower(phrase)) {
			abstained = true
		}
	}
	passed := valid && !abstained
	if !answerable {
		passed = abstained && len(citations) == 0
	}
	return EvaluationResult{
		Evaluator: item.name,
		Passed:    passed,
		Score:     boolFloat(passed),
		Metrics: map[string]float64{
			"valid_evidence":         boolFloat(valid),
			"appropriate_abstention": boolFloat(abstained == !answerable),
			"unsupported_claim":      boolFloat(!passed),
		},
		Reason: fmt.Sprintf(
			"citations=%d; answerable=%t; abstained=%t",
			len(citations),
			answerable,
			abstained,
		),
	}
}

func (item evaluator) jsonFields(
	testCase ExperimentCase,
	response GenerationResponse,
) EvaluationResult {
	required := stringSlice(testCase.Expected["required_fields"])
	value := map[string]any{}
	if err := json.Unmarshal([]byte(response.Text), &value); err != nil {
		value = map[string]any{}
	}
	found := 0
	for _, field := range required {
		if _, ok := value[field]; ok {
			found++
		}
	}
	score := 1.0
	if len(required) > 0 {
		score = float64(found) / float64(len(required))
	}
	return EvaluationResult{
		Evaluator: item.name,
		Passed:    score == 1,
		Score:     score,
		Metrics:   map[string]float64{"output_contract": score},
		Reason:    fmt.Sprintf("required=%v; found=%d", required, found),
	}
}

func stringValue(value any) string {
	text, _ := value.(string)
	return text
}

func stringSlice(value any) []string {
	items, ok := value.([]any)
	if !ok {
		return nil
	}
	result := make([]string, 0, len(items))
	for _, item := range items {
		if text, ok := item.(string); ok {
			result = append(result, text)
		}
	}
	return result
}

func boolFloat(value bool) float64 {
	if value {
		return 1
	}
	return 0
}
