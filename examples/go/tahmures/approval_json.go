package tahmures

// This serializer follows Python 3.12 json.dumps for the approved JSON domain.
// It deliberately does not use encoding/json's UTF-8/HTML or float rendering.
import (
	"encoding"
	"encoding/json"
	"fmt"
	"math"
	"math/big"
	"reflect"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"unicode/utf16"
	"unicode/utf8"
)

type approvalArgumentsError struct{ cause error }

func (e approvalArgumentsError) Error() string { return "invalid approval arguments" }
func (e approvalArgumentsError) Unwrap() error { return e.cause }

var approvalNumberPattern = regexp.MustCompile(`^-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?$`)

// Path-local identities reject cycles while accepting shared acyclic values.
type approvalJSONIdentity struct {
	kind    reflect.Kind
	typeOf  reflect.Type
	pointer uintptr
	length  int
}

func canonicalApprovalJSON(action string, arguments map[string]any) ([]byte, error) {
	if arguments == nil {
		return nil, fmt.Errorf("arguments must be a nonnull object")
	}
	encoded := []byte(`{"action":`)
	var err error
	encoded, err = appendApprovalString(encoded, action)
	if err != nil {
		return nil, err
	}
	encoded = append(encoded, `,"arguments":`...)
	encoded, err = appendApprovalValue(encoded, reflect.ValueOf(arguments), map[approvalJSONIdentity]bool{})
	if err != nil {
		return nil, err
	}
	return append(encoded, '}'), nil
}

func appendApprovalString(dst []byte, value string) ([]byte, error) {
	if !utf8.ValidString(value) {
		return nil, fmt.Errorf("invalid Unicode string")
	}
	dst = append(dst, '"')
	for _, r := range value {
		switch r {
		case '"', '\\':
			dst = append(dst, '\\', byte(r))
		case '\b':
			dst = append(dst, `\b`...)
		case '\f':
			dst = append(dst, `\f`...)
		case '\n':
			dst = append(dst, `\n`...)
		case '\r':
			dst = append(dst, `\r`...)
		case '\t':
			dst = append(dst, `\t`...)
		default:
			if r >= 0x20 && r < 0x7f {
				dst = append(dst, byte(r))
			} else if r <= 0xffff {
				dst = appendApprovalEscape(dst, uint16(r))
			} else {
				high, low := utf16.EncodeRune(r)
				dst = appendApprovalEscape(dst, uint16(high))
				dst = appendApprovalEscape(dst, uint16(low))
			}
		}
	}
	return append(dst, '"'), nil
}

func appendApprovalEscape(dst []byte, value uint16) []byte {
	const digits = "0123456789abcdef"
	return append(dst, '\\', 'u', digits[value>>12], digits[(value>>8)&15], digits[(value>>4)&15], digits[value&15])
}

func approvalFloat(value float64) (string, error) {
	if math.IsInf(value, 0) || math.IsNaN(value) {
		return "", fmt.Errorf("nonfinite number")
	}
	// Both runtimes choose shortest round-trip digits. Python uses scientific
	// notation outside [-4, 15], retaining .0 for integral fixed-point floats.
	scientific := strconv.FormatFloat(value, 'e', -1, 64)
	index := strings.IndexByte(scientific, 'e')
	exponent, err := strconv.Atoi(scientific[index+1:])
	if err != nil {
		return "", err
	}
	if exponent < -4 || exponent >= 16 {
		return scientific, nil
	}
	fixed := strconv.FormatFloat(value, 'f', -1, 64)
	if !strings.Contains(fixed, ".") {
		fixed += ".0"
	}
	return fixed, nil
}

func approvalNumber(value json.Number) (string, error) {
	text := string(value)
	if !approvalNumberPattern.MatchString(text) {
		return "", fmt.Errorf("invalid JSON number %q", text)
	}
	if strings.ContainsAny(text, ".eE") {
		value, err := strconv.ParseFloat(text, 64)
		if err != nil {
			return "", err
		}
		return approvalFloat(value)
	}
	integer, ok := new(big.Int).SetString(text, 10)
	if !ok {
		return "", fmt.Errorf("invalid integer")
	}
	return integer.String(), nil
}

// Reject hooks without invoking them, including pointer-receiver hooks on
// values and hooks on map keys. Native JSON primitives need no custom codec.
func approvalHasCustomHook(value reflect.Value) bool {
	jsonHook := reflect.TypeFor[json.Marshaler]()
	textHook := reflect.TypeFor[encoding.TextMarshaler]()
	for _, kind := range []reflect.Type{value.Type(), reflect.PointerTo(value.Type())} {
		if kind.Implements(jsonHook) || kind.Implements(textHook) {
			return true
		}
	}
	return false
}

func appendApprovalValue(dst []byte, value reflect.Value, active map[approvalJSONIdentity]bool) ([]byte, error) {
	if !value.IsValid() {
		return append(dst, "null"...), nil
	}
	if value.Kind() == reflect.Interface {
		if value.IsNil() {
			return append(dst, "null"...), nil
		}
		return appendApprovalValue(dst, value.Elem(), active)
	}
	if number, ok := value.Interface().(json.Number); ok {
		text, err := approvalNumber(number)
		if err != nil {
			return nil, err
		}
		return append(dst, text...), nil
	}
	if approvalHasCustomHook(value) {
		return nil, fmt.Errorf("custom JSON hooks are unsupported")
	}
	switch value.Kind() {
	case reflect.Bool:
		return strconv.AppendBool(dst, value.Bool()), nil
	case reflect.String:
		return appendApprovalString(dst, value.String())
	case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
		return strconv.AppendInt(dst, value.Int(), 10), nil
	case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64:
		return strconv.AppendUint(dst, value.Uint(), 10), nil
	case reflect.Float32, reflect.Float64:
		text, err := approvalFloat(value.Float())
		if err != nil {
			return nil, err
		}
		return append(dst, text...), nil
	case reflect.Map, reflect.Slice, reflect.Array:
		if value.Kind() == reflect.Map && value.Type().Key().Kind() != reflect.String {
			return nil, fmt.Errorf("JSON object keys must be strings")
		}
		if value.Kind() == reflect.Slice && value.Type().Elem().Kind() == reflect.Uint8 {
			return nil, fmt.Errorf("byte slices are unsupported")
		}
		if value.Kind() != reflect.Array {
			if value.IsNil() {
				return append(dst, "null"...), nil
			}
			identity := approvalJSONIdentity{value.Kind(), value.Type(), uintptr(value.UnsafePointer()), value.Len()}
			if active[identity] {
				return nil, fmt.Errorf("cyclic JSON value")
			}
			active[identity] = true
			defer delete(active, identity)
		}
		if value.Kind() == reflect.Map {
			dst = append(dst, '{')
			keys := value.MapKeys()
			sort.Slice(keys, func(i, j int) bool { return keys[i].String() < keys[j].String() })
			for i, key := range keys {
				if approvalHasCustomHook(key) {
					return nil, fmt.Errorf("custom object key hooks are unsupported")
				}
				if i > 0 {
					dst = append(dst, ',')
				}
				var err error
				dst, err = appendApprovalString(dst, key.String())
				if err != nil {
					return nil, err
				}
				dst = append(dst, ':')
				dst, err = appendApprovalValue(dst, value.MapIndex(key), active)
				if err != nil {
					return nil, err
				}
			}
			return append(dst, '}'), nil
		}
		dst = append(dst, '[')
		for i := 0; i < value.Len(); i++ {
			if i > 0 {
				dst = append(dst, ',')
			}
			var err error
			dst, err = appendApprovalValue(dst, value.Index(i), active)
			if err != nil {
				return nil, err
			}
		}
		return append(dst, ']'), nil
	default:
		return nil, fmt.Errorf("unsupported JSON value: %s", value.Kind())
	}
}
