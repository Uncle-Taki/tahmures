// Package tahmures implements the provider-neutral offline experiment contract.
package tahmures

type Message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type GenerationParameters struct {
	Temperature     float64 `json:"temperature"`
	MaxOutputTokens int     `json:"max_output_tokens"`
	Seed            *int    `json:"seed,omitempty"`
}

type GenerationRequest struct {
	Messages   []Message            `json:"messages"`
	Parameters GenerationParameters `json:"parameters"`
	Metadata   map[string]any       `json:"metadata"`
}

type GenerationResponse struct {
	Text         string         `json:"text"`
	ModelID      string         `json:"model_id"`
	FinishReason string         `json:"finish_reason"`
	Usage        map[string]int `json:"usage"`
	Metadata     map[string]any `json:"metadata"`
}

type PromptVariant struct {
	ID           string `json:"id"`
	TemplatePath string `json:"template_path"`
}

type EvaluatorSpec struct {
	Name      string  `json:"name"`
	Type      string  `json:"type"`
	Threshold float64 `json:"threshold"`
}

type Manifest struct {
	SchemaVersion  int             `json:"schema_version"`
	Chapter        int             `json:"chapter"`
	ExperimentID   string          `json:"experiment_id"`
	Description    string          `json:"description"`
	Dataset        string          `json:"dataset"`
	Fixtures       string          `json:"fixtures"`
	PromptVariants []PromptVariant `json:"prompt_variants"`
	Evaluators     []EvaluatorSpec `json:"evaluators"`
	Trials         int             `json:"trials"`
}

type ExperimentCase struct {
	CaseID   string         `json:"case_id"`
	Input    map[string]any `json:"input"`
	Expected map[string]any `json:"expected"`
	Tags     []string       `json:"tags"`
}

type FixtureRecord struct {
	CaseID    string             `json:"case_id"`
	VariantID string             `json:"variant_id"`
	Trial     int                `json:"trial"`
	Response  GenerationResponse `json:"response"`
}

type EvaluationResult struct {
	Evaluator string             `json:"evaluator"`
	Passed    bool               `json:"passed"`
	Score     float64            `json:"score"`
	Metrics   map[string]float64 `json:"metrics"`
	Reason    string             `json:"reason"`
}

type CaseResult struct {
	CaseID      string             `json:"case_id"`
	VariantID   string             `json:"variant_id"`
	Trial       int                `json:"trial"`
	Response    GenerationResponse `json:"response"`
	Evaluations []EvaluationResult `json:"evaluations"`
}

type ExperimentReport struct {
	SchemaVersion    int                                      `json:"schema_version"`
	ExperimentID     string                                   `json:"experiment_id"`
	Client           string                                   `json:"client"`
	VariantSummaries map[string]map[string]float64            `json:"variant_summaries"`
	TagSummaries     map[string]map[string]map[string]float64 `json:"tag_summaries"`
	CaseResults      []CaseResult                             `json:"case_results"`
}
