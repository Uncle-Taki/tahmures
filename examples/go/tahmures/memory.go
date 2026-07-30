package tahmures

import (
	"fmt"
	"sort"
)

type MemoryPolicy struct {
	AllowedKinds []string
	MaxTTL       int
}

type MemoryRecord struct {
	MemoryID   string
	SubjectID  string
	Scope      string
	Kind       string
	Value      string
	Provenance string
	CreatedAt  int
	ExpiresAt  int
	Supersedes string
}

type MemoryQuery struct {
	SubjectID string
	Scope     string
	AsOf      int
	Kinds     []string
}

type InMemoryStore struct {
	records   map[string]MemoryRecord
	forgotten map[string]bool
}

func NewInMemoryStore() *InMemoryStore {
	return &InMemoryStore{records: map[string]MemoryRecord{}, forgotten: map[string]bool{}}
}

func (store *InMemoryStore) Remember(record MemoryRecord, policy MemoryPolicy, now int) error {
	if record.MemoryID == "" || record.SubjectID == "" || record.Scope == "" ||
		record.Kind == "" || record.Value == "" || record.Provenance == "" {
		return fmt.Errorf("memory fields and provenance are required")
	}
	allowed := false
	for _, kind := range policy.AllowedKinds {
		allowed = allowed || kind == record.Kind
	}
	if !allowed || record.CreatedAt > now || record.ExpiresAt <= now ||
		record.ExpiresAt-record.CreatedAt > policy.MaxTTL {
		return fmt.Errorf("memory violates write policy")
	}
	if _, exists := store.records[record.MemoryID]; exists {
		return fmt.Errorf("memory ID already exists")
	}
	if record.Supersedes != "" {
		if _, exists := store.records[record.Supersedes]; !exists {
			return fmt.Errorf("superseded memory does not exist")
		}
	}
	store.records[record.MemoryID] = record
	return nil
}

func (store *InMemoryStore) Recall(query MemoryQuery) []MemoryRecord {
	superseded, kinds := map[string]bool{}, map[string]bool{}
	for _, kind := range query.Kinds {
		kinds[kind] = true
	}
	for _, record := range store.records {
		if record.Supersedes != "" {
			superseded[record.Supersedes] = true
		}
	}
	result := []MemoryRecord{}
	for id, record := range store.records {
		if store.forgotten[id] || superseded[id] || record.SubjectID != query.SubjectID ||
			record.Scope != query.Scope || record.CreatedAt > query.AsOf ||
			query.AsOf >= record.ExpiresAt || (len(kinds) > 0 && !kinds[record.Kind]) {
			continue
		}
		result = append(result, record)
	}
	sort.Slice(result, func(i, j int) bool {
		if result[i].Kind != result[j].Kind {
			return result[i].Kind < result[j].Kind
		}
		return result[i].MemoryID < result[j].MemoryID
	})
	return result
}

func (store *InMemoryStore) Forget(id string) error {
	if _, exists := store.records[id]; !exists {
		return fmt.Errorf("memory does not exist")
	}
	store.forgotten[id] = true
	return nil
}
