package tahmures

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
)

func LoadManifest(path string) (Manifest, error) {
	var manifest Manifest
	data, err := os.ReadFile(path)
	if err != nil {
		return manifest, fmt.Errorf("read manifest: %w", err)
	}
	if err := json.Unmarshal(data, &manifest); err != nil {
		return manifest, fmt.Errorf("decode manifest: %w", err)
	}
	if manifest.SchemaVersion != 1 {
		return manifest, fmt.Errorf("only experiment schema_version 1 is supported")
	}
	if len(manifest.PromptVariants) == 0 || len(manifest.Evaluators) == 0 {
		return manifest, fmt.Errorf("manifest requires prompt variants and evaluators")
	}
	if manifest.Trials == 0 {
		manifest.Trials = 1
	}
	if manifest.Trials < 1 {
		return manifest, fmt.Errorf("trials must be positive")
	}
	seen := map[string]bool{}
	for _, variant := range manifest.PromptVariants {
		if seen[variant.ID] {
			return manifest, fmt.Errorf("prompt variant IDs must be unique")
		}
		seen[variant.ID] = true
	}
	return manifest, nil
}

func LoadCases(path string) ([]ExperimentCase, error) {
	var records []ExperimentCase
	if err := readJSONL(path, func(data []byte) error {
		var item ExperimentCase
		if err := json.Unmarshal(data, &item); err != nil {
			return err
		}
		records = append(records, item)
		return nil
	}); err != nil {
		return nil, err
	}
	if len(records) == 0 {
		return nil, fmt.Errorf("dataset cannot be empty")
	}
	seen := map[string]bool{}
	for _, item := range records {
		if seen[item.CaseID] {
			return nil, fmt.Errorf("dataset case IDs must be unique")
		}
		seen[item.CaseID] = true
	}
	return records, nil
}

func LoadFixtures(path string) ([]FixtureRecord, error) {
	var records []FixtureRecord
	if err := readJSONL(path, func(data []byte) error {
		var item FixtureRecord
		if err := json.Unmarshal(data, &item); err != nil {
			return err
		}
		if item.Response.FinishReason == "" {
			item.Response.FinishReason = "stop"
		}
		if item.Response.ModelID == "" {
			item.Response.ModelID = "fixture-v1"
		}
		if item.Response.Usage == nil {
			item.Response.Usage = map[string]int{}
		}
		if item.Response.Metadata == nil {
			item.Response.Metadata = map[string]any{}
		}
		records = append(records, item)
		return nil
	}); err != nil {
		return nil, err
	}
	seen := map[string]bool{}
	for _, item := range records {
		key := fmt.Sprintf("%s|%s|%d", item.CaseID, item.VariantID, item.Trial)
		if seen[key] {
			return nil, fmt.Errorf("fixture keys must be unique")
		}
		seen[key] = true
	}
	return records, nil
}

func readJSONL(path string, accept func([]byte) error) error {
	file, err := os.Open(path)
	if err != nil {
		return fmt.Errorf("open JSONL %s: %w", path, err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	line := 0
	for scanner.Scan() {
		line++
		if len(scanner.Bytes()) == 0 {
			continue
		}
		if err := accept(scanner.Bytes()); err != nil {
			return fmt.Errorf("decode %s:%d: %w", path, line, err)
		}
	}
	return scanner.Err()
}

func ResolveProjectPath(manifestPath, value string) string {
	if filepath.IsAbs(value) {
		return value
	}
	current, _ := filepath.Abs(filepath.Dir(manifestPath))
	for {
		if _, err := os.Stat(filepath.Join(current, "pyproject.toml")); err == nil {
			return filepath.Join(current, value)
		}
		parent := filepath.Dir(current)
		if parent == current {
			break
		}
		current = parent
	}
	return value
}
