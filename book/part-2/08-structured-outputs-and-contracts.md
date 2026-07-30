---
title: "Structured Outputs and Contracts"
slug: "structured-outputs-and-contracts"
chapter: 8
part: "Part II — Designing Prompted Interactions"
summary: "Turn generated text into an explicitly validated interface without confusing valid syntax with correct meaning."
maturity: "draft"
last_reviewed: "2026-07-29"
narrative_episode: "Thirty Catalogues"
learning_objectives:
  - "Define and validate bounded JSON output contracts"
  - "Separate syntactic, structural, semantic, and authority checks"
  - "Choose safely among reject, retry, repair, and escalation"
prerequisites:
  - "Chapter 7"
---

# Structured Outputs and Contracts

[این فصل را به فارسی بخوانید](../fa/part-2/08-structured-outputs-and-contracts.md)

## Learning Objectives

You will design a small machine-checkable output contract, decide which
validation belongs to the application, and distinguish a parsed response from
a trustworthy result. You will also evaluate invalid acceptance, not merely
parse success, and implement matching educational validators in Python and Go.

## The Tale of Tahmures

*The following is an original fictional episode created for teaching. It is not
a translation, adaptation, or reconstructed passage from the* Shahnameh.

### The Setting

The workshop of mechanical scribes occupied a courtyard roofed with blue
glass. Thirty brass hands moved above thirty desks. At the center stood one
cedar chest containing tablets from the eastern storehouse.

The Archivist wanted a catalogue before the chest entered the royal archive.
He assigned one tablet to every scribe and supplied the same four facts: the
record’s mark, its kind, its measure, and whether its authority remained
current.

### The Request

Tahmures asked for “a clear catalogue that any keeper can use.” The workshop
master repeated those words to every brass scribe.

By noon, the desks held thirty elegant answers. One began, “Concerning the
ninth tablet.” Another put the date before the mark. A third used *living* for
current and *sleeping* for expired. Measures appeared as numerals, words,
fractions, and comparisons to jars. Three scribes omitted the mark because the
tablet already displayed it. One copied a decorative title as the record’s
kind.

No catalogue was false in every respect. No two could be joined without a
person interpreting them.

### The Unexpected Result

The Archivist’s import machine rejected twenty-two entries. A clerk repaired
six by hand. The remaining two entered the archive—but one placed “nine” in
the field reserved for the tablet’s mark, and the other called an expired
order current. They were valid lines in the catalogue and wrong records.

The workshop master proposed teaching the import machine all thirty styles.
The Keeper of Scripts asked what would happen with the thirty-first.

Tahmures instead ordered every scribe to use four labels. The next batch looked
uniform, but some returned `measure: "twelve"` while others returned
`measure: 12`. One added a fifth field containing an apology. A damaged tablet
produced `measure: null`; a clerk replaced it with zero so the import would
continue. The catalogue became easier to parse and easier to corrupt
consistently.

### The Discovery

The Keeper drew four gates on a slate. At the first, an entry had to be valid
notation. At the second, it needed every required label with the expected kind
of value. At the third, values had to make sense: a measure could not be
negative, and an expired date could not follow a current claim without review.
At the fourth, the source had to justify the value.

“A line may pass one gate and fail the next,” she said.

They wrote an allowed set for record kinds and status, decided whether absence
meant unknown rather than zero, and rejected unrecognised fields. Damaged
records went to a review basket with their source marks. The import machine no
longer repaired meaning merely to preserve motion.

The thirty scribes did not become identical. They became callers of one
contract, and their disagreements became visible failures instead of
incompatible catalogues.

### From Tale to Engineering

Structure made the archive inspectable, not automatically correct. Model
outputs require layered validation: JSON parsing, field contracts, semantic
rules, provenance checks, and application policy are distinct gates.

## The Engineering Problem

Language models naturally produce text, while applications need values they
can inspect and route. Asking for JSON is useful, but “return JSON” is not a
contract. JSON only defines notation. It does not say that the top level must
be an object, which fields exist, whether an identifier is a string, which
status values are allowed, whether additional fields are safe, or whether two
individually valid values contradict each other.

Even a fully schema-valid response can be factually unsupported. Therefore the
goal is not to transform uncertainty into certainty by adding braces. The goal
is to move detectable failure into an explicit boundary before downstream code
acts.

## Mental Model

Imagine generated output passing through layered gates:

```text
text -> parse -> structure -> semantics -> evidence -> policy -> action
```

Parsing asks whether notation is valid. Structural validation asks whether the
value has the expected shape, fields, types, and enumerations. Semantic
validation asks whether values make sense together and within the domain.
Evidence validation asks whether claims are supported by permitted sources.
Policy asks whether this valid, supported proposal may be used for the current
caller and action.

Failure at one gate should not be described as failure at another. A retry may
help invalid JSON. It cannot authenticate a source or grant permission.

## Core Concepts

Required fields define what a consumer must receive. Optional fields should
have a precise absence meaning. If `reason` is absent, does that mean no reason
exists, the model omitted it, or the field is inapplicable? Nullability is
separate from optionality: a required field may permit `null` to express known
absence, while an optional field may be omitted.

Types prevent some category mistakes. Booleans should not be encoded as
`"yes"` and `"no"` unless that is the declared enumeration. Identifiers often
remain strings even when composed of digits. Integers and general numbers are
not interchangeable where fractional values are invalid.

Enumerations make closed decisions observable. A status such as
`current|expired|unknown` is safer than free prose when application behavior
depends on it. Include `unknown` or an escalation state when the domain
requires it; forcing every case into positive or negative can manufacture
certainty.

Extra-field policy is a compatibility decision. Rejecting extras catches drift
and accidental disclosure. Allowing extras supports forward evolution but may
let unreviewed values reach permissive consumers. Different trust boundaries
may need different policies.

JSON Schema draft 2020-12 is a mature standard with vocabularies, references,
composition, conditional logic, and precise validation semantics. The
repository’s `OutputContract` is intentionally not an implementation of that
standard. It is a dependency-free teaching tool covering an object, required
fields, basic types, enumerations, and extra fields. Production systems should
use a maintained standards-compliant validator when JSON Schema is the chosen
contract.

Structured generation features offered by a provider may improve conformity.
They do not remove the need to validate at the application boundary. Feature
support, limitations, and failure modes can change across model and provider
versions.

## Prompt Pattern

State the output contract beside the task:

```text
Return exactly one JSON object.
Required fields:
- id: string
- kind: "tablet" or "scroll"
- measure: integer
- status: "current", "expired", or "unknown"
Do not include additional fields or prose.
If the source does not establish measure, use status "unknown" and set the
case aside for review; do not invent zero.
```

This is a communication aid. The application builds the same contract as
executable validation. Keeping prose and code definitions aligned is a
versioning problem. Generate documentation from a canonical schema where
practical, or test the two representations against shared cases.

## Naive Attempt

The naive caller asks, “Return this as JSON,” parses the result, and indexes
fields:

```python
value = json.loads(response.text)
save(value["id"], value["status"])
```

It accepts arrays, extra fields, wrong value types, unknown statuses, and
unsupported claims until downstream code fails—or worse, coerces them.
`json.loads` answers only the first gate.

Another naive approach catches every error and asks the model to “fix the
JSON.” This can turn an observable failure into a plausible but altered record.
A repair model may change values while repairing punctuation.

## Failure Analysis

Syntax failures include truncated JSON, trailing commentary, invalid escaping,
and multiple top-level values. Structural failures include missing fields,
incorrect types, prohibited extra fields, and unknown enumeration values.
Semantic failures include negative measures, impossible date ordering, or a
status inconsistent with other fields.

Grounding failures occur when the object is valid but its content is not
supported. Security failures include an extra field containing sensitive data
or a consumer that treats a model-provided action name as authorised. Consumer
failures occur when different services interpret null, omission, or defaults
differently.

Invalid acceptance rate deserves special attention: how often does the system
accept output that should fail? A low overall error rate can hide catastrophic
acceptance in a rare security tag.

## Improved Design

Define a contract with ownership and version. Validate the raw response before
extracting fields. Preserve the original text for debugging under an
appropriate retention policy. Return a structured list of violations with
paths and codes. Do not expose a partial value as accepted.

Then run domain validators. A catalogue validator might check measure ranges
and cross-field date rules. An evidence validator checks source IDs. Finally,
policy decides whether a validated record is stored automatically or queued
for human review.

Choose failure handling deliberately:

- reject when output is unsafe or retry would hide an important ambiguity;
- retry when failure appears transient and attempts are bounded;
- repair only for transformations proven not to alter meaning;
- escalate when the source or requirements cannot resolve the case.

Record attempts and do not let retry loops continue indefinitely.

## Worked Example

An extraction system returns:

```json
{"id":"T-4","kind":"tablet","measure":0,"status":"current"}
```

The object passes a basic contract. Yet the source said “measure illegible.”
Mapping illegible to zero is a semantic and provenance error. An improved
contract might represent `measure` as nullable and require
`measure_status: known|unknown`. Evidence spans or source IDs can make the
claim auditable. The application then routes unknown measures to review.

This redesign changes the data model, not just the prompt. That is often the
correct response to repeated ambiguity.

## Experiment

Run both implementations:

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch08-output-contracts.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch08-output-contracts.json
```

The synthetic cases compare prose catalogue responses with strict JSON
objects. The evaluator checks parsing, required fields, basic types, allowed
values, and extra-field policy. The ambiguous-measure case demonstrates a
limitation: converting “about nine” to integer nine may pass structure while
remaining semantically debatable.

Extend the dataset with malformed JSON, missing status, boolean-as-integer,
unknown enumeration, prohibited extra fields, and source contradictions.

## Evaluation

Report parse rate, structural validity, semantic validity, retry or repair
rate, and invalid acceptance rate. Keep them separate. A system can improve
parse rate while worsening invalid acceptance through aggressive coercion.

Segment by failure class and business consequence. Set disqualifying thresholds
for dangerous invalid acceptance. Measure latency and cost added by retries,
and compare human-review volume. Use a held-out set containing plausible values
that are structurally valid but semantically wrong.

## Implementation Lab

### Python

```python
from tahmures.contracts import FieldContract, OutputContract

contract = OutputContract((
    FieldContract("id", "string"),
    FieldContract("kind", "string", allowed_values=("tablet", "scroll")),
    FieldContract("measure", "integer"),
    FieldContract("status", "string",
                  allowed_values=("current", "expired", "unknown")),
))
result = contract.validate(response_text)
if not result.valid:
    for violation in result.violations:
        print(violation.path, violation.code)
```

Add domain validation after this basic contract. Do not call the educational
class a JSON Schema validator.

### Go

```go
contract := tahmures.OutputContract{Fields: []tahmures.FieldContract{
    {Name: "id", ValueType: "string", Required: true},
    {Name: "kind", ValueType: "string", Required: true,
        AllowedValues: []any{"tablet", "scroll"}},
    {Name: "measure", ValueType: "integer", Required: true},
}}
result := contract.Validate(responseText)
if !result.Valid {
    // route violations; do not consume result.Value
}
```

Both implementations expose parsing separately from validity and produce
inspectable violations.

## Failure Modes

Beware schema prose that differs from executable validation, automatic
coercion, ambiguous nulls, ignored extra fields, unbounded retry, lossy repair,
and consumers that bypass validation. Another failure is applying one contract
to all versions while fixtures were recorded under another.

Structured output may increase confidence beyond evidence. Review interfaces
should not style a valid unsupported object as verified.

## Security Considerations

Set size and nesting limits before parsing untrusted output. Avoid dynamically
loading types or executing values. Treat URLs, file paths, tool names, and code
inside valid fields as untrusted data. Allow-list consequential actions in the
application and recheck caller permission.

Redact secrets in validation logs. Prohibited extra fields can signal attempted
exfiltration and should be observable without preserving the sensitive value.

## Operational Considerations

Track validity by template, model, contract version, and tag. Alert on changes
in field-level violations. Roll out schema changes with consumer compatibility
tests. Decide whether old reports are revalidated or remain attached to the
contract version used originally.

Bound retries and expose exhaustion as a terminal status. A repair service is
another component with its own contract, cost, and failure modes.

## Trade-Offs

Strict contracts improve interoperability but reduce expressive freedom.
Flexible fields tolerate evolution but demand stronger semantic validation.
Provider-enforced structure may reduce syntax failures but increases provider
coupling. A standards-compliant validator adds dependency and schema
complexity, while a small validator is easier to teach but unsuitable for
claims of full conformance.

Choose the simplest contract that faithfully represents downstream decisions.

A practical contract review starts from each consumer rather than from the
model prompt. List the decisions the consumer makes, the fields used for those
decisions, and the consequences of a field being missing, malformed, stale, or
wrong. This prevents a schema from growing into a catalogue of interesting
model output that no application needs. It also exposes fields that deserve a
stronger source than generation.

For every field, write an example value and at least one counterexample. If a
field is `string`, ask whether whitespace-only text is valid, whether length is
bounded, and whether a stable identifier would be safer. If a field is
`integer`, decide whether booleans, floating values such as `2.0`, negative
values, or numbers outside the application’s exact range pass. Basic JSON
types cannot carry all domain meaning.

Enumerations require an evolution policy. Adding a value can break consumers
that assume an exhaustive set. Removing a value can make stored historical
records invalid under a new contract. Decide whether unknown future values are
rejected, mapped to an explicit `other`, or retained for a newer consumer.
Never silently map an unfamiliar consequential status to a permissive default.

Null and omission should be reviewed with concrete truth tables. Suppose
`delivery_date` is absent. The source may not contain a date, extraction may
have failed, the concept may be inapplicable, or the model may have omitted the
field. One null cannot communicate all four states. A companion status field
or a tagged union can make the difference explicit. More expressive structure
may seem verbose, but ambiguity otherwise moves into undocumented consumer
code.

Cross-field constraints deserve their own test table. A `status` of `expired`
may require an expiry date; a current record may prohibit one in the past. A
minimum cannot exceed a maximum. A selected action may require a nonempty
evidence list. These rules can be expressed in full JSON Schema in some cases,
but complex domain checks often remain clearer in ordinary code. The important
point is to assign them an owner and run them after structural validation.

Build a corpus of malformed and deceptive responses. Include fenced JSON,
leading commentary, duplicate keys, extreme nesting, huge strings, unusual
Unicode, extra fields that resemble instructions, and correct structure with
incorrect evidence IDs. Parser behavior around duplicate keys varies; if the
domain cares, define and enforce a policy before normal deserialization loses
the duplicate information.

Review repair with a semantic preservation test. Removing a Markdown fence is
often low risk if the exact enclosed bytes are preserved. Adding a missing
comma may be safe in a narrow case but ambiguous in another. Converting
`"twelve"` to `12`, inventing a missing status, or deleting an unknown field
changes meaning. Label these transformations as model retry or human
correction, not syntax repair. Preserve the original and repaired forms and
the transformation identity.

Retry policies should classify errors. A truncated response caused by an
output limit may justify a revised limit or a smaller requested object. An
unknown enumeration may reflect contract drift and will repeat indefinitely.
A semantic contradiction should usually escalate or return to the source. Add
jitter and backoff only for transient infrastructure failures; they do not
improve deterministic validation errors.

Contract versioning must cover producers and consumers. During a rolling
deployment, a new producer may emit a field before all consumers understand
it. A strict extra-field policy will reject that response, which is safer than
misuse but still an outage if unplanned. Compatibility testing can use
consumer-driven examples: each consumer publishes records it must accept and
records it must reject. Promote the new contract only after both old and new
paths behave deliberately.

Observability should aggregate violation codes by field and version. A spike in
`measure:wrong_type` may indicate a prompt or provider change. A spike in
`status:not_allowed` may indicate a source-system vocabulary change. Sampled
raw output can assist diagnosis but creates privacy and injection risks; apply
redaction, access controls, and retention limits. Metrics should not include
high-cardinality sensitive values as labels.

Finally, review downstream authority. A valid object describing
`{"action":"open_gate"}` is a proposal. The action name must resolve through an
allow list, its arguments require validation, and the current caller needs
permission. High-impact actions may require confirmation using a representation
derived from trusted application data rather than model prose. Structural
validity is a prerequisite for safe consumption, never the final approval.

These review steps are intentionally more extensive than the prompt itself.
That imbalance is normal. Reliable structured output is primarily an interface
engineering problem. The prompt communicates the interface to a probabilistic
producer; the application contract, tests, and policy make it real.

When designing nested records, validate at the narrowest meaningful path.
Reporting only “object invalid” forces operators to inspect raw text and gives
evaluators no useful categories. A path such as
`$.items[2].expiry_date` plus a stable code such as `date_order` supports
metrics, user feedback, and targeted retry. Keep human-readable messages
separate from stable codes so wording can change without breaking consumers.

Arrays introduce additional semantics: minimum and maximum length, uniqueness,
ordering, and item identity. If the model returns two records with the same
ID, a generic type validator will accept both. The application must decide
whether duplicates are invalid, merged, or retained as conflicting
observations. If order affects priority, say so; otherwise consumers should not
infer importance from model-generated order.

Numbers deserve special care across languages. JSON represents numbers without
separate integer syntax rules at every consumer, while language runtimes decode
them differently. Large identifiers can lose precision when treated as
floating-point values. Monetary values need decimal or integer-minor-unit
representation and domain validation. Cross-language parity tests should
include numeric boundaries rather than only small friendly values.

Dates and times are strings at the JSON layer. Define format, timezone, and
whether an interval endpoint is inclusive. Validate impossible calendar dates
and daylight-saving behavior with a maintained time library. A model can emit a
perfectly formatted date that never occurred or is unsupported by the source;
format validity and evidence remain distinct.

Error reporting can itself become a contract. An API might return
`accepted=false`, violations, attempt count, and retry eligibility. The caller
should never infer retry eligibility from message prose. If invalid output is
shown to a user for correction, distinguish model-produced content from
trusted interface labels and escape it for the display context.

Property-based testing is useful for validators. Generate objects that vary one
dimension—field presence, type, enumeration, extra key, depth—and assert the
expected code. Mutation testing can remove a check and verify that tests fail.
Fuzz parsers with size limits in place. These techniques test the application
contract independently of any model.

For model evaluation, build contrast pairs. One response is malformed but
factually correct; another is structurally perfect but unsupported. A robust
report should show syntax success for the latter and evidence failure, while
the former fails before evidence consumption. If one binary score treats them
as identical, diagnosis becomes harder even when both are rejected.

Human review interfaces should display violations and source evidence without
encouraging manual normalisation of every failure. Track correction categories.
Frequent human conversion of the same field indicates the schema, source
mapping, or prompt needs redesign. Manual repair is operational data, not a
free compatibility layer.

Finally, rehearse consumer failure. If the validator service is unavailable,
does the application fail closed or bypass it? If logs cannot be written, does
the action continue? If a schema registry returns an unknown version, is there
a permissive fallback? Reliability design includes these infrastructure paths.
For consequential consumption, “validation skipped” must not be equivalent to
“validation passed.”

Contract ownership should appear in the repository beside the definition.
Name the producing component, consuming services, domain reviewer, and
deprecation policy. Without an owner, permissive workarounds accumulate because
no team can approve a breaking correction. A compact ownership record turns
schema failures into routable engineering work.
It also clarifies who decides whether a failed record is rejected, retried,
repaired, or escalated.
Ownership makes that decision timely and reviewable.

## When Prompting Is Not the Answer

Use deterministic serializers to produce JSON and maintained validators to
check it. Use database constraints for uniqueness and referential integrity.
Use domain code for ranges, accounting identities, and state transitions.

If the desired output can be computed directly from trusted structured input,
skip generation entirely.

## Exercises

1. Design a contract that distinguishes unknown, absent, and inapplicable.
2. Write five structurally valid but semantically invalid catalogue objects.
3. Define a retry policy with a maximum attempt count and terminal outcome.
4. Decide whether extra fields should be allowed in a public API and justify
   the compatibility trade-off.
5. Add provenance fields without implying that a cited source supports the
   claim automatically.

## Chapter Summary

JSON is notation, not trust. Reliable consumers validate syntax, structure,
semantics, evidence, and policy in distinct stages. Contracts need versioning,
clear null and extra-field rules, inspectable violations, bounded failure
handling, and tests for invalid acceptance. The included validator teaches a
small subset; JSON Schema draft 2020-12 is the appropriate standard to study
for full schema work.

## The Next Tale

The unified catalogue revealed a rescue order whose location, route, supplies,
and reporting requirements could not be completed in one accountable act.
Tahmures sent a messenger toward the mountain with a single command—and no
place to record which assumption failed.

<!-- next: ch09 -->

## Citations and Further Reading

- JSON Schema. 2022. “JSON Schema Specification, Draft 2020-12.”
  https://json-schema.org/specification.
- Bray, Tim. 2017. “The JavaScript Object Notation (JSON) Data Interchange
  Format.” RFC 8259. https://www.rfc-editor.org/rfc/rfc8259.
- Kleppmann, Martin. 2017. *Designing Data-Intensive Applications*. Sebastopol,
  CA: O’Reilly Media.
