package tahmures

import (
	"encoding/json"
	"os"
	"reflect"
	"testing"
)

// Python-derived goldens lock every field, including findings slice order.
func TestOperationsCompleteOrderedParity(t *testing.T) {
	data, err := os.ReadFile("../../shared/operations_order_cases.json")
	if err != nil {
		t.Fatal(err)
	}
	var corpus struct {
		SchemaVersion int `json:"schema_version"`
		Cases         []struct {
			ID       string            `json:"id"`
			Baseline []TelemetryEvent  `json:"baseline"`
			Current  []TelemetryEvent  `json:"current"`
			Policy   OperationalPolicy `json:"policy"`
			Expected OperationalReport `json:"expected"`
		} `json:"cases"`
	}
	if err := json.Unmarshal(data, &corpus); err != nil {
		t.Fatal(err)
	}
	if corpus.SchemaVersion != 1 || len(corpus.Cases) == 0 {
		t.Fatal("invalid operations-order corpus")
	}
	for _, c := range corpus.Cases {
		t.Run(c.ID, func(t *testing.T) {
			for iteration := 0; iteration < 50; iteration++ {
				actual, err := CompareWindows(c.Baseline, c.Current, c.Policy)
				if err != nil {
					t.Fatal(err)
				}
				if !reflect.DeepEqual(actual, c.Expected) {
					t.Fatalf("iteration=%d actual=%#v expected=%#v", iteration, actual, c.Expected)
				}
			}
		})
	}
}
