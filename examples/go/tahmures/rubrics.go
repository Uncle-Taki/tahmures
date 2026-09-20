package tahmures

import (
	"fmt"
	"math"
)

type RubricCriterion struct {
	CriterionID   string
	Weight        float64
	Minimum       int
	Anchors       [5]string
	Disqualifying bool
}
type RubricReview struct {
	ReviewerID string
	Scores     map[string]int
	Rationale  string
}
type RubricResult struct {
	Passed                         bool
	WeightedScore                  float64
	CriterionMeans, ReviewerScores map[string]float64
	Disagreement                   float64
	DisqualifyingFailures          []string
	RequiresAdjudication           bool
}
type Rubric struct {
	Criteria                             []RubricCriterion
	PassThreshold, DisagreementThreshold float64
}

func (r Rubric) Evaluate(reviews []RubricReview) (RubricResult, error) {
	if len(r.Criteria) == 0 || r.PassThreshold < 0 || r.PassThreshold > 1 || r.DisagreementThreshold < 0 || r.DisagreementThreshold > 1 {
		return RubricResult{}, fmt.Errorf("invalid rubric")
	}
	ids := map[string]bool{}
	totalWeight := 0.0
	for _, c := range r.Criteria {
		if c.CriterionID == "" || c.Weight <= 0 || c.Minimum < 0 || c.Minimum > 4 || ids[c.CriterionID] {
			return RubricResult{}, fmt.Errorf("invalid rubric criterion")
		}
		ids[c.CriterionID] = true
		totalWeight += c.Weight
	}
	if len(reviews) == 0 {
		return RubricResult{}, fmt.Errorf("reviews are required")
	}
	reviewers := map[string]bool{}
	reviewScores := map[string]float64{}
	criterionTotals := map[string]float64{}
	failures := []string{}
	for _, review := range reviews {
		if review.ReviewerID == "" || review.Rationale == "" || reviewers[review.ReviewerID] || len(review.Scores) != len(ids) {
			return RubricResult{}, fmt.Errorf("invalid review")
		}
		reviewers[review.ReviewerID] = true
		weighted := 0.0
		for _, c := range r.Criteria {
			score, ok := review.Scores[c.CriterionID]
			if !ok || score < 0 || score > 4 {
				return RubricResult{}, fmt.Errorf("review scores must match criteria")
			}
			weighted += float64(score) * c.Weight
			criterionTotals[c.CriterionID] += float64(score)
			if c.Disqualifying && score < c.Minimum && !containsString(failures, c.CriterionID) {
				failures = append(failures, c.CriterionID)
			}
		}
		reviewScores[review.ReviewerID] = weighted / (4 * totalWeight)
	}
	means := map[string]float64{}
	for id, total := range criterionTotals {
		means[id] = roundSix(total / float64(len(reviews)))
	}
	weighted, min, max := 0.0, 1.0, 0.0
	for _, score := range reviewScores {
		weighted += score
		if score < min {
			min = score
		}
		if score > max {
			max = score
		}
	}
	weighted = roundSix(weighted / float64(len(reviews)))
	disagreement := roundSix(max - min)
	adjudication := len(failures) > 0 || disagreement > r.DisagreementThreshold
	return RubricResult{weighted >= r.PassThreshold && !adjudication, weighted, means, reviewScores, disagreement, failures, adjudication}, nil
}
func roundSix(value float64) float64 { return math.Round(value*1e6) / 1e6 }
func containsString(values []string, target string) bool {
	for _, v := range values {
		if v == target {
			return true
		}
	}
	return false
}
