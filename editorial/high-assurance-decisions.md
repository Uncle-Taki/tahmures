# High-assurance remediation decisions

Owner approvals D24–D29 constrain the high-assurance remediation. This record
does not replace the charter, editorial contracts, or narrative continuity.
Only HA-A is implemented in this batch; HA-B through HA-F remain pending.

## Approved boundaries

| Decision | Approved requirement | Implementation status |
| --- | --- | --- |
| D24 | Approval digests bind action and arguments only. Identity, scopes, effect classification and supplied approval records are trusted application inputs. | Binding preserved by HA-A; manuscript corrections await HA-D. |
| D25 | Orchestration validates completion evidence before emitting `complete`; RunController applies the transition. | No controller changes in HA-A. |
| D26 | Reject negative submitted `token_cost` and `tool_calls` increments. | HA-B pending. |
| D27 | `version_attribution` requires exact changed-dimension agreement; malformed values fail; preserve public metric keys. | HA-C pending. |
| D28 | Chapter 24 remains a design/architecture capstone, without a new integrated runtime. | No capstone changes in HA-A. |
| D29 | Python remains canonical for supported JSON-domain arguments; Go must agree on bytes and digests; unsupported values fail explicitly. | HA-A implementation below. |

## HA-A supported domain

Arguments must be a nonnull object with string keys. Values recursively comprise
Unicode scalar strings, integers, finite floating-point numbers, booleans, null,
arrays and objects. Python uses its ordinary built-in `dict`, `list`, `str`,
`int`, `float`, `bool` and `None` representations. Integer and floating-point
kinds remain distinct: `1` and `1.0` produce different bytes and digests.
Strings preserve code points without Unicode normalisation.

Go accepts native string/bool/integer/finite float values, string-keyed maps,
arrays and slices representing this domain. A `float32` is widened to its exact
float64 value before rendering. Nested nil maps/slices represent null; nil root
arguments are rejected. Shared acyclic references are allowed.

Go `json.Number` preserves number kinds for decoded JSON: integer syntax is
normalised with arbitrary-precision integers; decimal-point or exponent syntax
is parsed as float64. Use `json.Decoder.UseNumber()` when reading JSON inputs
whose integer/float distinction or large integers matter. Ordinary unmarshalling
into `any` loses this distinction before the digest function sees the values;
the serializer cannot recover it. Numbers outside the finite float domain fail.

Unsupported values include nonfinite floats, cyclic containers, non-string
object keys, invalid Unicode, tuples/sets/byte objects and other native objects.
Go structs, pointers, functions, channels, byte slices, `json.RawMessage`,
custom JSON/text marshal hooks and malformed `json.Number` values are rejected.
No new depth, size or integer-width policy is introduced. Existing runtime
serialization failures, including Python runtime limits, fail explicitly.

## Canonical bytes

For supported values, retain Python 3.12's serialization exactly:

```python
json.dumps(
    {"action": action, "arguments": arguments},
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=True,
    allow_nan=False,
).encode("utf-8")
```

SHA-256 hashes those bytes. Object keys sort by Unicode scalar order; there is
no whitespace. Non-ASCII characters use lowercase ASCII `\u` escapes, including
surrogate pairs for non-BMP scalars. HTML-sensitive `<>&` characters remain
literal. Python float rendering preserves negative zero and the integral `.0`,
using scientific notation below decimal exponent -4 or from exponent 16.
This is Python serialization, not a claim of compliance with another canonical
JSON standard.

The payload contains no request ID, principal, scopes, effect or expiry. Changing
those fields does not change the digest. Existing authorization checks and
caller responsibilities still apply; a digest does not authenticate the caller
or verify the provenance of an approval record. Exact scope membership remains
unchanged, without wildcard expansion.

## Errors and compatibility

- Python `request_digest` and `CapabilityRequest.digest` preserve their public
  interfaces. Invalid inputs raise `ValueError("invalid approval arguments")`
  through an internal subclass, with the validation/serialization cause retained.
- Go adds `CheckedRequestDigest(action, arguments) (string, error)`. Invalid
  inputs return an empty digest and a nonnil error whose message is
  `invalid approval arguments`; `errors.Unwrap` exposes the cause.
- Go's existing `RequestDigest(action, arguments) string` signature is retained.
  It panics with that error for invalid inputs. Applications accepting untrusted
  inputs should use the checked interface.
- Both authorizers handle these serialization rejections without a panic or
  escaping exception: `allowed=false`, `reason="invalid_arguments"`,
  `approval_count=0`. The audit retains `request_id`, `principal`, `action`,
  and `digest`; an empty audit digest means serialization was unavailable.
  Invalid serialization precedes ordinary authorization checks, preserving the
  previous placement of digest construction. Unexpected programming/hash
  failures are not converted into authorization denials.
- No serialization failure is hashed, and there is no legacy-digest fallback.

Supported Python digests retain their bytes. Go digests change where its old
encoding disagreed with Python, notably Unicode, HTML-sensitive strings and
floating-point values. Previously accepted unsupported values now fail.
Consequently an approval issued with an affected old Go digest can return
`digest_mismatch` after the fix. Any such approval must be reissued through the
trusted approval workflow; do not rewrite old records or accept both digests.
The teaching contracts have no persistent approval store or migration facility.
Application deployments must account for their own outstanding records.

## Evidence and gate scope

`examples/shared/approval_digest_cases.json` is a schema-version-1 **test corpus**,
separate from experiment manifests. Tagged integer strings and float64 bits
preserve numeric types. Its goldens come from the Python runtime, not generated
arithmetic or the Go implementation. Python tests independently recalculate
the bytes and hashes; Go tests compare the complete same corpus results.

Coverage includes 296 valid byte/digest cases (256 seeded finite float patterns),
10 portable invalid cases, native unsupported inputs, error provenance and
precedence, shared references and 28 complete authorization results. The latter
retain the exact Chapter 22 inputs and metadata-binding boundaries, expiry,
scope and approval edge cases. An independent temporary probe additionally
compared 100,000 finite float64 digests against Python without mismatches.
These are concrete test results, not proof over every possible input.

HA-A does not correct English prose or lab presentation (HA-D), agent behavior
(HA-B), evaluator behavior (HA-C), bibliography (HA-E), or establish English
technical acceptance (HA-F). It creates no manuscript or translation edits.
F01 bilingual debt remains deferred: Chapters 13–24 already have stale source
hashes and the baseline full check has 14 related failing Python tests. Hashes
must not be refreshed merely to pass validation. F09 narrative work remains a
separate later batch. Machine work does not confer human review.

## HA-A validation record — 2026-09-29

Reviewed baseline HEAD: `f97f9298ac153e222aea8106049fb24b965ea488`, including
pre-existing uncommitted P0 work and the unrelated handover path edit. The two
approval modules matched HEAD before remediation. No commit was created.

- Focused Python serialization and phase-4 contracts: **371 passed**.
- Go contract tests and repository lint: **passed**.
- Exact Chapter 22 Python and Go fences (only language entry-point wrappers):
  **allowed, reason `allowed`, approval count 1**; both audit digests were
  `430568876febfe9d576e1036439a9ba11da9b246d3f1b66cafbdbc6ac1cd1acf`.
- `make check PYTHON=.venv/bin/python`: **failed on existing F01 debt**.
  Python totals were **436 passed, 14 failed**, compared with the baseline
  **94 passed, 14 failed**; the added 342 HA-A tests passed.
- `make -k check PYTHON=.venv/bin/python`: continued the remaining gates.
  Go tests, lint, chapter/continuity validation, all 24 offline experiments,
  experiment parity and both strict documentation builds passed. Translation
  validation and editorial-check failed on the existing stale Chapter 13 hash.
  Protected-content parity also reported nine existing translation warnings;
  a build or machine pass does not resolve this semantic debt.
- Preservation: hashes of all 321 pre-existing source files were recorded before
  editing. Only the two allowed approval modules changed; the other **319**
  remained byte-for-byte identical. Five new files complete the seven-file HA-A
  allow-list. Chapters, narratives, translation hashes and review states were
  untouched. No validator was weakened.

The overall publishing gate remains open. HA-A completion does not authorise
HA-B or later batches and does not constitute an English freeze or human review.
