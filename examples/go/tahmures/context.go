package tahmures

import (
	"crypto/sha256"
	"fmt"
	"sort"
)

type ContextItem struct {
	ID            string
	Text          string
	TokenEstimate int
	Priority      int
	Provenance    string
	Mandatory     bool
	Scope         string
	Trust         string
	ValidFrom     *int
	ValidUntil    *int
	Digest        string
	ClaimGroup    string
}

type ContextSelection struct {
	Items      []ContextItem
	Excluded   []ContextItem
	UsedBudget int
	Budget     int
}

type ContextPolicy struct {
	InputBudget    int
	ReservedOutput int
	Scope          string
	AsOf           int
}

type ContextExclusion struct {
	Item   ContextItem
	Reason string
}

type ContextPackage struct {
	Items           []ContextItem
	Excluded        []ContextExclusion
	Conflicts       [][]string
	UsedBudget      int
	AvailableBudget int
}

func SelectContext(items []ContextItem, budget int) (ContextSelection, error) {
	if budget < 1 {
		return ContextSelection{}, fmt.Errorf("context budget must be positive")
	}
	seen, indexes := map[string]bool{}, map[string]int{}
	selected, optional := []ContextItem{}, []ContextItem{}
	used := 0
	for index, item := range items {
		if item.Scope == "" {
			item.Scope = "public"
		}
		if item.Trust == "" {
			item.Trust = "data"
		}
		if item.ID == "" || seen[item.ID] || item.TokenEstimate < 1 || item.Provenance == "" {
			return ContextSelection{}, fmt.Errorf("context items need unique IDs and valid estimates")
		}
		if item.Trust != "data" && item.Trust != "instruction" {
			return ContextSelection{}, fmt.Errorf("context trust must be instruction or data")
		}
		seen[item.ID], indexes[item.ID] = true, index
		if item.Mandatory {
			selected = append(selected, item)
			used += item.TokenEstimate
		} else {
			optional = append(optional, item)
		}
	}
	if used > budget {
		return ContextSelection{}, fmt.Errorf("mandatory context exceeds the budget")
	}
	sort.Slice(optional, func(i, j int) bool {
		if optional[i].Priority != optional[j].Priority {
			return optional[i].Priority > optional[j].Priority
		}
		if optional[i].TokenEstimate != optional[j].TokenEstimate {
			return optional[i].TokenEstimate < optional[j].TokenEstimate
		}
		return optional[i].ID < optional[j].ID
	})
	excluded := []ContextItem{}
	for _, item := range optional {
		if used+item.TokenEstimate <= budget {
			selected = append(selected, item)
			used += item.TokenEstimate
		} else {
			excluded = append(excluded, item)
		}
	}
	sort.Slice(selected, func(i, j int) bool {
		return indexes[selected[i].ID] < indexes[selected[j].ID]
	})
	sort.Slice(excluded, func(i, j int) bool {
		return indexes[excluded[i].ID] < indexes[excluded[j].ID]
	})
	return ContextSelection{
		Items: selected, Excluded: excluded, UsedBudget: used, Budget: budget,
	}, nil
}

func AssembleContext(items []ContextItem, policy ContextPolicy) (ContextPackage, error) {
	available := policy.InputBudget - policy.ReservedOutput
	if available < 1 {
		return ContextPackage{}, fmt.Errorf("reserved output leaves no input budget")
	}
	if policy.Scope == "" {
		policy.Scope = "public"
	}
	type contextCandidate struct {
		item   ContextItem
		digest string
	}
	candidates := []contextCandidate{}
	excluded := []ContextExclusion{}
	for _, item := range items {
		if item.Scope == "" {
			item.Scope = "public"
		}
		if item.Trust == "" {
			item.Trust = "data"
		}
		if item.Scope != "public" && item.Scope != policy.Scope {
			excluded = append(excluded, ContextExclusion{item, "scope"})
			continue
		}
		if item.ValidFrom != nil && policy.AsOf < *item.ValidFrom {
			excluded = append(excluded, ContextExclusion{item, "not_yet_valid"})
			continue
		}
		if item.ValidUntil != nil && policy.AsOf > *item.ValidUntil {
			excluded = append(excluded, ContextExclusion{item, "expired"})
			continue
		}
		digest := item.Digest
		if digest == "" {
			digest = fmt.Sprintf("%x", sha256.Sum256([]byte(item.Text)))
		}
		candidates = append(candidates, contextCandidate{item: item, digest: digest})
	}
	better := func(left ContextItem, right ContextItem) bool {
		if left.Mandatory != right.Mandatory {
			return left.Mandatory
		}
		if left.Priority != right.Priority {
			return left.Priority > right.Priority
		}
		if left.TokenEstimate != right.TokenEstimate {
			return left.TokenEstimate < right.TokenEstimate
		}
		return left.ID < right.ID
	}
	winners := map[string]int{}
	for index, candidate := range candidates {
		current, exists := winners[candidate.digest]
		if !exists || better(candidate.item, candidates[current].item) {
			winners[candidate.digest] = index
		}
	}
	eligible := []ContextItem{}
	for index, candidate := range candidates {
		if winners[candidate.digest] == index {
			eligible = append(eligible, candidate.item)
		} else {
			excluded = append(excluded, ContextExclusion{candidate.item, "duplicate"})
		}
	}
	selection, err := SelectContext(eligible, available)
	if err != nil {
		return ContextPackage{}, err
	}
	for _, item := range selection.Excluded {
		excluded = append(excluded, ContextExclusion{item, "budget"})
	}
	groups := map[string][]ContextItem{}
	for _, item := range selection.Items {
		if item.ClaimGroup != "" {
			groups[item.ClaimGroup] = append(groups[item.ClaimGroup], item)
		}
	}
	conflicts := [][]string{}
	for _, group := range groups {
		texts, ids := map[string]bool{}, []string{}
		for _, item := range group {
			texts[item.Text] = true
			ids = append(ids, item.ID)
		}
		if len(texts) > 1 {
			sort.Strings(ids)
			conflicts = append(conflicts, ids)
		}
	}
	sort.Slice(conflicts, func(i, j int) bool { return conflicts[i][0] < conflicts[j][0] })
	return ContextPackage{
		Items: selection.Items, Excluded: excluded, Conflicts: conflicts,
		UsedBudget: selection.UsedBudget, AvailableBudget: available,
	}, nil
}
