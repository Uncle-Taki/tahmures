package tahmures

import (
	"fmt"
	"regexp"
	"sort"
	"strings"
)

type TemplateField struct {
	Name      string
	ValueType string
	Required  bool
	Default   any
}

type RenderedPrompt struct {
	Text       string
	TemplateID string
	Values     map[string]any
}

type PromptTemplate struct {
	TemplateID string
	Source     string
	Fields     []TemplateField
}

var placeholderPattern = regexp.MustCompile(`\$\{([A-Za-z_][A-Za-z0-9_]*)\}`)

func (item PromptTemplate) Render(values map[string]any) (RenderedPrompt, error) {
	fields := map[string]TemplateField{}
	for _, field := range item.Fields {
		if field.Name == "" || fields[field.Name].Name != "" {
			return RenderedPrompt{}, fmt.Errorf("invalid or duplicate template field %q", field.Name)
		}
		fields[field.Name] = field
	}
	unknown := []string{}
	for name := range values {
		if _, ok := fields[name]; !ok {
			unknown = append(unknown, name)
		}
	}
	if len(unknown) > 0 {
		sort.Strings(unknown)
		return RenderedPrompt{}, fmt.Errorf("unknown template variables: %s", strings.Join(unknown, ", "))
	}
	resolved := map[string]any{}
	for name, field := range fields {
		value, present := values[name]
		if !present {
			value, present = field.Default, field.Default != nil
		}
		if !present && field.Required {
			return RenderedPrompt{}, fmt.Errorf("missing template variable: %s", name)
		}
		if present && !templateTypeMatches(value, field.ValueType) {
			return RenderedPrompt{}, fmt.Errorf("template variable %s has wrong type", name)
		}
		if present {
			resolved[name] = value
		}
	}
	text := placeholderPattern.ReplaceAllStringFunc(item.Source, func(match string) string {
		name := placeholderPattern.FindStringSubmatch(match)[1]
		value, ok := resolved[name]
		if !ok {
			return match
		}
		return fmt.Sprint(value)
	})
	if placeholderPattern.MatchString(text) {
		return RenderedPrompt{}, fmt.Errorf("rendered prompt contains unresolved variables")
	}
	return RenderedPrompt{Text: text, TemplateID: item.TemplateID, Values: resolved}, nil
}

func templateTypeMatches(value any, kind string) bool {
	switch kind {
	case "string":
		_, ok := value.(string)
		return ok
	case "integer":
		switch value.(type) {
		case int, int32, int64:
			return true
		default:
			return false
		}
	case "number":
		switch value.(type) {
		case int, int32, int64, float32, float64:
			return true
		default:
			return false
		}
	case "boolean":
		_, ok := value.(bool)
		return ok
	default:
		return false
	}
}
