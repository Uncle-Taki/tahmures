package tahmures

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"math"
	"os"
	"reflect"
	"strconv"
	"testing"
)

// Tagged integers and float bits avoid encoding/json's default float64 coercion.
type approvalTestNode struct {
	Kind    string             `json:"kind"`
	Value   json.RawMessage    `json:"value"`
	Bits    string             `json:"bits"`
	Items   []approvalTestNode `json:"items"`
	Entries []struct {
		Key   string           `json:"key"`
		Value approvalTestNode `json:"value"`
	} `json:"entries"`
}

func (n approvalTestNode) decode(t *testing.T) any {
	t.Helper()
	switch n.Kind {
	case "null":
		return nil
	case "string":
		var value string
		if err := json.Unmarshal(n.Value, &value); err != nil {
			t.Fatal(err)
		}
		return value
	case "boolean":
		var value bool
		if err := json.Unmarshal(n.Value, &value); err != nil {
			t.Fatal(err)
		}
		return value
	case "integer":
		var value string
		if err := json.Unmarshal(n.Value, &value); err != nil {
			t.Fatal(err)
		}
		return json.Number(value)
	case "float64":
		bits, err := strconv.ParseUint(n.Bits, 16, 64)
		if err != nil {
			t.Fatal(err)
		}
		return math.Float64frombits(bits)
	case "array":
		values := make([]any, len(n.Items))
		for i, item := range n.Items {
			values[i] = item.decode(t)
		}
		return values
	case "object":
		values := map[string]any{}
		for _, entry := range n.Entries {
			values[entry.Key] = entry.Value.decode(t)
		}
		return values
	default:
		t.Fatalf("unknown fixture kind %q", n.Kind)
		return nil
	}
}

type approvalTestRequest struct {
	RequestID string           `json:"request_id"`
	Principal string           `json:"principal"`
	Action    string           `json:"action"`
	Arguments approvalTestNode `json:"arguments"`
	Scopes    []string         `json:"scopes"`
	Effect    string           `json:"effect"`
	ExpiresAt int              `json:"expires_at"`
}
type approvalTestRecord struct {
	RequestID     string `json:"request_id"`
	RequestDigest string `json:"request_digest"`
	Approver      string `json:"approver"`
	Approved      bool   `json:"approved"`
	At            int    `json:"at"`
}
type approvalTestResult struct {
	Allowed       bool              `json:"allowed"`
	Reason        string            `json:"reason"`
	ApprovalCount int               `json:"approval_count"`
	Audit         map[string]string `json:"audit"`
}
type approvalTestCorpus struct {
	SchemaVersion int `json:"schema_version"`
	Valid         []struct {
		ID        string           `json:"id"`
		Action    string           `json:"action"`
		Arguments approvalTestNode `json:"arguments"`
		Bytes     string           `json:"canonical_bytes"`
		Digest    string           `json:"digest"`
	} `json:"valid_cases"`
	Invalid []struct {
		ID        string           `json:"id"`
		Action    string           `json:"action"`
		Factory   string           `json:"factory"`
		Arguments approvalTestNode `json:"arguments"`
	} `json:"invalid_cases"`
	Authorization []struct {
		ID        string               `json:"id"`
		Request   approvalTestRequest  `json:"request"`
		Approvals []approvalTestRecord `json:"approvals"`
		Policy    struct {
			AllowedActions      []string            `json:"allowed_actions"`
			PrincipalScopes     map[string][]string `json:"principal_scopes"`
			ApprovalEffects     []string            `json:"approval_effects"`
			DualApprovalEffects []string            `json:"dual_approval_effects"`
		} `json:"policy"`
		Now      int                `json:"now"`
		Expected approvalTestResult `json:"expected"`
	} `json:"authorization_cases"`
}

func loadApprovalCorpus(t *testing.T) approvalTestCorpus {
	t.Helper()
	data, err := os.ReadFile("../../shared/approval_digest_cases.json")
	if err != nil {
		t.Fatal(err)
	}
	var corpus approvalTestCorpus
	if err = json.Unmarshal(data, &corpus); err != nil {
		t.Fatal(err)
	}
	if corpus.SchemaVersion != 1 {
		t.Fatal("unsupported corpus version")
	}
	return corpus
}

func TestApprovalSharedSerialization(t *testing.T) {
	for _, c := range loadApprovalCorpus(t).Valid {
		t.Run(c.ID, func(t *testing.T) {
			arguments := c.Arguments.decode(t).(map[string]any)
			bytes, err := canonicalApprovalJSON(c.Action, arguments)
			if err != nil || string(bytes) != c.Bytes {
				t.Fatalf("bytes=%s want=%s err=%v", bytes, c.Bytes, err)
			}
			digest, err := CheckedRequestDigest(c.Action, arguments)
			if err != nil || digest != c.Digest {
				t.Fatalf("digest=%s want=%s err=%v", digest, c.Digest, err)
			}
			if RequestDigest(c.Action, arguments) != c.Digest {
				t.Fatal("legacy valid-input digest differs")
			}
			sum := sha256.Sum256(bytes)
			if hex.EncodeToString(sum[:]) != c.Digest {
				t.Fatal("golden digest/bytes disagree")
			}
		})
	}
}

func TestApprovalSharedCompleteAuthorization(t *testing.T) {
	for _, c := range loadApprovalCorpus(t).Authorization {
		t.Run(c.ID, func(t *testing.T) {
			r := c.Request
			request := CapabilityRequest{r.RequestID, r.Principal, r.Action, r.Arguments.decode(t).(map[string]any), r.Scopes, r.Effect, r.ExpiresAt}
			var records []ApprovalRecord
			for _, a := range c.Approvals {
				records = append(records, ApprovalRecord{a.RequestID, a.RequestDigest, a.Approver, a.Approved, a.At})
			}
			p := c.Policy
			result := Authorize(request, records, ApprovalPolicy{p.AllowedActions, p.PrincipalScopes, p.ApprovalEffects, p.DualApprovalEffects}, c.Now)
			actual := approvalTestResult{result.Allowed, result.Reason, result.ApprovalCount, result.Audit}
			if !reflect.DeepEqual(actual, c.Expected) {
				t.Fatalf("actual=%#v expected=%#v", actual, c.Expected)
			}
		})
	}
}

func assertInvalidApproval(t *testing.T, action string, arguments map[string]any) {
	t.Helper()
	digest, err := CheckedRequestDigest(action, arguments)
	if digest != "" || err == nil || err.Error() != "invalid approval arguments" || errors.Unwrap(err) == nil {
		t.Fatalf("invalid digest=%q err=%v", digest, err)
	}
	func() {
		defer func() {
			p := recover()
			if e, ok := p.(error); !ok || e.Error() != "invalid approval arguments" {
				t.Fatalf("legacy helper must panic explicitly, got %v", p)
			}
		}()
		RequestDigest(action, arguments)
	}()
	request := CapabilityRequest{"r", "servant", action, arguments, nil, "read", 10}
	sum := sha256.Sum256(nil)
	record := ApprovalRecord{"r", hex.EncodeToString(sum[:]), "steward", true, 1}
	for _, variant := range []string{"normal", "invalid_request", "invalid_effect", "expired"} {
		r := request
		switch variant {
		case "invalid_request":
			r.RequestID = ""
		case "invalid_effect":
			r.Effect = "unknown"
		case "expired":
			r.ExpiresAt = 0
		}
		result := Authorize(r, []ApprovalRecord{record}, ApprovalPolicy{AllowedActions: []string{action}}, 2)
		expected := AuthorizationResult{false, "invalid_arguments", 0, map[string]string{"request_id": r.RequestID, "principal": r.Principal, "action": action, "digest": ""}}
		if !reflect.DeepEqual(result, expected) {
			t.Fatalf("%s: got %#v want %#v", variant, result, expected)
		}
	}
}

func TestApprovalSharedInvalid(t *testing.T) {
	for _, c := range loadApprovalCorpus(t).Invalid {
		t.Run(c.ID, func(t *testing.T) {
			action := c.Action
			if action == "" {
				action = "open_storehouse"
			}
			if c.ID == "surrogate_action" {
				action = string([]byte{0xed, 0xa0, 0x80})
			}
			var arguments map[string]any
			switch c.Factory {
			case "surrogate_value":
				arguments = map[string]any{"value": string([]byte{0xed, 0xa0, 0x80})}
			case "surrogate_key":
				arguments = map[string]any{string([]byte{0xed, 0xa0, 0x80}): 1}
			case "surrogate_action":
				arguments = map[string]any{}
			case "cycle_object":
				arguments = map[string]any{}
				arguments["self"] = arguments
			case "cycle_array":
				value := make([]any, 1)
				value[0] = value
				arguments = map[string]any{"value": value}
			case "non_string_key":
				arguments = map[string]any{"value": map[int]string{1: "one"}}
			default:
				if value := c.Arguments.decode(t); value != nil {
					arguments = value.(map[string]any)
				}
			}
			assertInvalidApproval(t, action, arguments)
		})
	}
}

type approvalCustomJSON string

func (approvalCustomJSON) MarshalJSON() ([]byte, error) { panic("custom hook must not run") }

func TestApprovalNativeInvalid(t *testing.T) {
	n := 1
	for i, value := range []any{make(chan int), func() {}, struct{ X int }{1}, &n, []byte("bytes"), json.RawMessage(`{}`), approvalCustomJSON("text"), json.Number("NaN"), json.Number("01"), json.Number("1e999"), json.Number(""), json.Number("1.")} {
		t.Run(fmt.Sprint(i), func(t *testing.T) { assertInvalidApproval(t, "a", map[string]any{"value": value}) })
	}
}

func TestApprovalNativeNumbersAndContainers(t *testing.T) {
	for _, pair := range [][2]any{{1, json.Number("1")}, {uint64(math.MaxUint64), json.Number("18446744073709551615")}, {json.Number("-0"), 0}, {json.Number("1e0"), 1.0}, {json.Number("-0.0"), math.Copysign(0, -1)}, {float32(1.25), 1.25}, {[]int{1, 2}, [2]int{1, 2}}, {map[string]int{"a": 1}, map[string]any{"a": 1}}} {
		left := RequestDigest("a", map[string]any{"value": pair[0]})
		right := RequestDigest("a", map[string]any{"value": pair[1]})
		if left != right {
			t.Fatalf("native normalization differs: %#v", pair)
		}
	}
	shared := []any{map[string]any{"text": "گندم"}}
	if _, err := CheckedRequestDigest("a", map[string]any{"x": shared, "y": shared}); err != nil {
		t.Fatal("shared acyclic values rejected", err)
	}
	if RequestDigest("a", map[string]any{"n": 1}) == RequestDigest("a", map[string]any{"n": 1.0}) {
		t.Fatal("numeric kinds collapsed")
	}
	if RequestDigest("a", map[string]any{"n": 1}) == RequestDigest("a", map[string]any{"n": 1, "extra": false}) {
		t.Fatal("extra argument ignored")
	}
}

type approvalPointerHook string

func (*approvalPointerHook) MarshalJSON() ([]byte, error) { panic("pointer hook must not run") }

type approvalTextHook string

func (approvalTextHook) MarshalText() ([]byte, error) { panic("text hook must not run") }

func TestApprovalCustomHooksAndUnsupportedKeys(t *testing.T) {
	for i, value := range []any{approvalPointerHook("x"), approvalTextHook("x"), map[approvalPointerHook]int{"x": 1}, map[approvalTextHook]int{"x": 1}, uintptr(1)} {
		t.Run(fmt.Sprint(i), func(t *testing.T) { assertInvalidApproval(t, "a", map[string]any{"value": value}) })
	}
}
