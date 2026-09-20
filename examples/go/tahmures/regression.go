package tahmures

import (
	"fmt"
	"sort"
)

type CaseOutcome struct {
	CaseID string
	Passed bool
	Score  float64
	Tags   []string
}
type RegressionPolicy struct {
	ProtectedTags         []string
	AllowedRegressions    int
	MinimumCandidateScore float64
}
type RegressionReport struct {
	Passed                                                         bool
	Fixed, Regressed, StablePass, StableFail, ProtectedRegressions []string
	MeanScoreDelta                                                 float64
}

func CompareRegression(baseline, candidate []CaseOutcome, policy RegressionPolicy) (RegressionReport, error) {
	if policy.AllowedRegressions < 0 || policy.MinimumCandidateScore < 0 || policy.MinimumCandidateScore > 1 {
		return RegressionReport{}, fmt.Errorf("invalid regression policy")
	}
	before, after := map[string]CaseOutcome{}, map[string]CaseOutcome{}
	for _, item := range baseline {
		if item.CaseID == "" || before[item.CaseID].CaseID != "" {
			return RegressionReport{}, fmt.Errorf("case IDs must be non-empty and unique")
		}
		before[item.CaseID] = item
	}
	for _, item := range candidate {
		if item.CaseID == "" || after[item.CaseID].CaseID != "" {
			return RegressionReport{}, fmt.Errorf("case IDs must be non-empty and unique")
		}
		after[item.CaseID] = item
	}
	if len(before) == 0 || len(before) != len(after) {
		return RegressionReport{}, fmt.Errorf("case IDs must match")
	}
	protectedTags := stringSetAny(policy.ProtectedTags)
	fixed, regressed, stablePass, stableFail, protected := []string{}, []string{}, []string{}, []string{}, []string{}
	delta := 0.0
	floor := true
	for id, old := range before {
		now, ok := after[id]
		if !ok {
			return RegressionReport{}, fmt.Errorf("case IDs must match")
		}
		delta += now.Score - old.Score
		if now.Score < policy.MinimumCandidateScore {
			floor = false
		}
		if old.Passed && !now.Passed {
			regressed = append(regressed, id)
			for _, tag := range old.Tags {
				if protectedTags[tag] {
					protected = append(protected, id)
					break
				}
			}
		} else if !old.Passed && now.Passed {
			fixed = append(fixed, id)
		} else if now.Passed {
			stablePass = append(stablePass, id)
		} else {
			stableFail = append(stableFail, id)
		}
	}
	for _, items := range [][]string{fixed, regressed, stablePass, stableFail, protected} {
		sort.Strings(items)
	}
	return RegressionReport{len(regressed) <= policy.AllowedRegressions && len(protected) == 0 && floor, fixed, regressed, stablePass, stableFail, protected, roundSix(delta / float64(len(before)))}, nil
}
