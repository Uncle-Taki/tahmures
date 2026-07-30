package tahmures

import (
	"encoding/json"
	"fmt"
	"reflect"
)

// OutputContract is deliberately smaller than JSON Schema. It exists so the
// educational examples can make validation ownership visible.
type FieldContract struct {
	Name          string
	ValueType     string
	Required      bool
	AllowedValues []any
}

type ContractViolation struct {
	Path    string `json:"path"`
	Code    string `json:"code"`
	Message string `json:"message"`
}

type ContractResult struct {
	Valid      bool                `json:"valid"`
	Parsed     bool                `json:"parsed"`
	Value      map[string]any      `json:"value,omitempty"`
	Violations []ContractViolation `json:"violations"`
}

type OutputContract struct {
	Fields     []FieldContract
	AllowExtra bool
}

func (item OutputContract) Validate(text string) ContractResult {
	value := map[string]any{}
	if err := json.Unmarshal([]byte(text), &value); err != nil {
		return ContractResult{
			Violations: []ContractViolation{{
				Path: "$", Code: "parse", Message: "output is not a JSON object",
			}},
		}
	}
	violations := []ContractViolation{}
	known := map[string]bool{}
	for _, field := range item.Fields {
		known[field.Name] = true
		actual, present := value[field.Name]
		if !present {
			if field.Required {
				violations = append(violations, ContractViolation{
					Path: field.Name, Code: "required", Message: "required field is missing",
				})
			}
			continue
		}
		if !contractTypeMatches(actual, field.ValueType) {
			violations = append(violations, ContractViolation{
				Path: field.Name, Code: "type",
				Message: fmt.Sprintf("expected %s", field.ValueType),
			})
			continue
		}
		if len(field.AllowedValues) > 0 {
			allowed := false
			for _, candidate := range field.AllowedValues {
				if reflect.DeepEqual(candidate, actual) {
					allowed = true
				}
			}
			if !allowed {
				violations = append(violations, ContractViolation{
					Path: field.Name, Code: "allowed_value",
					Message: "value is outside the allowed set",
				})
			}
		}
	}
	if !item.AllowExtra {
		for name := range value {
			if !known[name] {
				violations = append(violations, ContractViolation{
					Path: name, Code: "extra", Message: "extra field is not allowed",
				})
			}
		}
	}
	return ContractResult{
		Valid: len(violations) == 0, Parsed: true, Value: value, Violations: violations,
	}
}

func contractTypeMatches(value any, kind string) bool {
	switch kind {
	case "string":
		_, ok := value.(string)
		return ok
	case "integer":
		number, ok := value.(float64)
		return ok && number == float64(int64(number))
	case "number":
		_, ok := value.(float64)
		return ok
	case "boolean":
		_, ok := value.(bool)
		return ok
	case "array":
		_, ok := value.([]any)
		return ok
	case "object":
		_, ok := value.(map[string]any)
		return ok
	case "null":
		return value == nil
	default:
		return false
	}
}
