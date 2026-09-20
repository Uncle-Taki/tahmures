package tahmures

import (
	"fmt"
	"math"
	"sort"
)

type TelemetryEvent struct {
	RunID, ModelID, PromptVersion, PolicyVersion, DatasetVersion, Outcome string
	Quality                                                               float64
	LatencyMS, InputTokens, OutputTokens                                  int
	CostUnits                                                             float64
	Tags                                                                  []string
}
type OperationalPolicy struct {
	MinimumQuality, MaximumErrorRate float64
	MaximumP95LatencyMS              int
	MaximumMeanCost, QualityDrift    float64
}
type WindowSummary struct {
	Count                  int
	MeanQuality, ErrorRate float64
	P95LatencyMS           int
	MeanCost               float64
}
type OperationalReport struct {
	Passed                    bool
	Baseline, Current         WindowSummary
	TagSummaries              map[string]WindowSummary
	Findings, ChangedVersions []string
}

func summarize(events []TelemetryEvent) (WindowSummary, error) {
	if len(events) == 0 {
		return WindowSummary{}, fmt.Errorf("operational windows cannot be empty")
	}
	latencies := []int{}
	quality, cost, errors := 0.0, 0.0, 0
	for _, event := range events {
		if event.RunID == "" || event.ModelID == "" || event.PromptVersion == "" || event.PolicyVersion == "" || event.DatasetVersion == "" {
			return WindowSummary{}, fmt.Errorf("telemetry version identity is required")
		}
		latencies = append(latencies, event.LatencyMS)
		quality += event.Quality
		cost += event.CostUnits
		if event.Outcome != "success" {
			errors++
		}
	}
	sort.Ints(latencies)
	round := func(v float64) float64 { return math.Round(v*1e6) / 1e6 }
	return WindowSummary{len(events), round(quality / float64(len(events))), round(float64(errors) / float64(len(events))), latencies[int(math.Ceil(.95*float64(len(latencies))))-1], round(cost / float64(len(events)))}, nil
}
func CompareWindows(baseline, current []TelemetryEvent, policy OperationalPolicy) (OperationalReport, error) {
	if policy.MinimumQuality < 0 || policy.MinimumQuality > 1 || policy.MaximumErrorRate < 0 || policy.MaximumErrorRate > 1 {
		return OperationalReport{}, fmt.Errorf("invalid operational quality policy")
	}
	old, err := summarize(baseline)
	if err != nil {
		return OperationalReport{}, err
	}
	now, err := summarize(current)
	if err != nil {
		return OperationalReport{}, err
	}
	findings := []string{}
	if now.MeanQuality < policy.MinimumQuality {
		findings = append(findings, "quality_slo")
	}
	if old.MeanQuality-now.MeanQuality > policy.QualityDrift {
		findings = append(findings, "quality_drift")
	}
	if now.ErrorRate > policy.MaximumErrorRate {
		findings = append(findings, "error_rate_slo")
	}
	if now.P95LatencyMS > policy.MaximumP95LatencyMS {
		findings = append(findings, "latency_slo")
	}
	if now.MeanCost > policy.MaximumMeanCost {
		findings = append(findings, "cost_slo")
	}
	tags := map[string][]TelemetryEvent{}
	for _, e := range current {
		for _, tag := range e.Tags {
			tags[tag] = append(tags[tag], e)
		}
	}
	summaries := map[string]WindowSummary{}
	for tag, events := range tags {
		s, _ := summarize(events)
		summaries[tag] = s
		if s.MeanQuality < policy.MinimumQuality {
			findings = append(findings, "tag_quality:"+tag)
		}
	}
	changed := []string{}
	dimensions := []struct {
		name          string
		before, after map[string]bool
	}{{"model", models(baseline, 0), models(current, 0)}, {"prompt", models(baseline, 1), models(current, 1)}, {"policy", models(baseline, 2), models(current, 2)}, {"dataset", models(baseline, 3), models(current, 3)}}
	for _, d := range dimensions {
		if fmt.Sprint(d.before) != fmt.Sprint(d.after) {
			changed = append(changed, d.name)
		}
	}
	sort.Strings(findings)
	return OperationalReport{len(findings) == 0, old, now, summaries, findings, changed}, nil
}
func models(events []TelemetryEvent, kind int) map[string]bool {
	out := map[string]bool{}
	for _, e := range events {
		v := []string{e.ModelID, e.PromptVersion, e.PolicyVersion, e.DatasetVersion}[kind]
		out[v] = true
	}
	return out
}
