package tahmures

import (
	"fmt"
	"regexp"
	"sort"
	"strings"
)

type RetrievalRequest struct {
	Query string
	Limit int
	Scope string
	AsOf  int
}

type RetrievedChunk struct {
	ChunkID    string
	DocumentID string
	Text       string
	Provenance string
	Scope      string
	ValidFrom  *int
	ValidUntil *int
	Score      float64
}

type Retriever interface {
	Retrieve(RetrievalRequest) ([]RetrievedChunk, error)
}

type InMemoryRetriever struct {
	Chunks []RetrievedChunk
}

var retrievalTerm = regexp.MustCompile(`[a-z0-9]+`)

func termSet(text string) map[string]bool {
	result := map[string]bool{}
	for _, term := range retrievalTerm.FindAllString(strings.ToLower(text), -1) {
		result[term] = true
	}
	return result
}

func (retriever InMemoryRetriever) Retrieve(request RetrievalRequest) ([]RetrievedChunk, error) {
	if strings.TrimSpace(request.Query) == "" || request.Limit < 1 {
		return nil, fmt.Errorf("retrieval needs a query and positive limit")
	}
	seen := map[string]bool{}
	for _, chunk := range retriever.Chunks {
		if chunk.ChunkID == "" || seen[chunk.ChunkID] {
			return nil, fmt.Errorf("retrieval chunk IDs must be unique")
		}
		seen[chunk.ChunkID] = true
	}
	if request.Scope == "" {
		request.Scope = "public"
	}
	query := termSet(request.Query)
	ranked := []RetrievedChunk{}
	for _, chunk := range retriever.Chunks {
		scope := chunk.Scope
		if scope == "" {
			scope = "public"
		}
		if scope != "public" && scope != request.Scope {
			continue
		}
		if chunk.ValidFrom != nil && request.AsOf < *chunk.ValidFrom {
			continue
		}
		if chunk.ValidUntil != nil && request.AsOf > *chunk.ValidUntil {
			continue
		}
		found := 0
		for term := range termSet(chunk.Text) {
			if query[term] {
				found++
			}
		}
		if found > 0 {
			chunk.Score = float64(found) / float64(max(1, len(query)))
			ranked = append(ranked, chunk)
		}
	}
	sort.Slice(ranked, func(i, j int) bool {
		if ranked[i].Score != ranked[j].Score {
			return ranked[i].Score > ranked[j].Score
		}
		return ranked[i].ChunkID < ranked[j].ChunkID
	})
	if len(ranked) > request.Limit {
		ranked = ranked[:request.Limit]
	}
	return ranked, nil
}

type CitationResult struct {
	Valid       bool
	Citations   []string
	Unsupported []string
}

func ValidateCitations(text string, retrieved []RetrievedChunk, required bool) CitationResult {
	allowed := map[string]bool{}
	for _, chunk := range retrieved {
		allowed[chunk.ChunkID] = true
	}
	found := map[string]bool{}
	for _, match := range citationPattern.FindAllStringSubmatch(text, -1) {
		found[match[1]] = true
	}
	citations, unsupported := []string{}, []string{}
	for id := range found {
		citations = append(citations, id)
		if !allowed[id] {
			unsupported = append(unsupported, id)
		}
	}
	sort.Strings(citations)
	sort.Strings(unsupported)
	return CitationResult{
		Valid:     len(unsupported) == 0 && (len(citations) > 0 || !required),
		Citations: citations, Unsupported: unsupported,
	}
}
