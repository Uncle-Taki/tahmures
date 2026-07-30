---
title: "Hand-offs and Multi-step Systems"
slug: "hand-offs-and-multi-step-systems"
chapter: 18
part: "Part III — Knowledge, Memory, and Action"
summary: "Preserve goals, authority, constraints, state, provenance, and unresolved questions across component boundaries."
maturity: "draft"
last_reviewed: "2026-07-30"
narrative_episode: "The Broken Relay"
learning_objectives:
  - "Design explicit versioned hand-off envelopes"
  - "Preserve constraints, authority, artefact provenance, and uncertainty"
  - "Reject stale or authority-expanding transfers"
prerequisites:
  - "Chapter 17"
---

# Hand-offs and Multi-step Systems

## Learning Objectives

By the end of this chapter, you can design explicit versioned hand-off envelopes,
preserve constraints, authority, artefact provenance, and uncertainty, and reject stale or authority-expanding transfers. The goal is
not a persuasive demonstration but a boundary that can be inspected, tested,
denied, and operated.

## The Tale of Tahmures

*The following is an original fictional episode created for teaching. It is not
a translation, adaptation, or reconstructed passage from the* Shahnameh.

### The Setting

Four towers relayed a border mission from the palace to a distant escort. The original restriction read: “Do not cross after sunset unless escorted by the northern guard.” Each messenger had little space and summarised the previous message before sending it onward.

### The Request

The first tower wrote, “Cross after sunset only with northern escort.” The second shortened it to, “Northern escort for sunset crossing.” The third reported, “Sunset crossing arranged.” The final receiver understood that crossing after sunset was approved. None intended to reverse the order; each preserved what seemed central in the prose it received.

### The Unexpected Result

The caravan entered the pass without the guard, met a closed checkpoint, and spent the night exposed to snow. Investigators possessed four fluent summaries and no stable record of which seal, revision of the mission, assumption, or unanswered question had crossed each tower. The final messenger had locally followed what it received. Meaning had decayed through individually plausible transformations.

### The Discovery

The Keeper of Scripts replaced summary-only transfer with a sealed envelope.
Its face named the kind of packet, the relay mark, the mission and its current
revision, the authorising seal, the exact prohibitions, work already completed,
referenced tablets with their source marks, assumptions, unanswered questions,
the actions allowed at the next tower, and the hour when the packet expired.
Each receiver compared those entries with the tower register and returned a
mark of acceptance. A covering note could explain the packet but could not
replace it. An old revision or an action unknown to the register stopped the
relay. The prohibition arrived unchanged because it occupied a protected line,
not because every messenger happened to consider it memorable.

They tested the new relay by dropping an acknowledgement, repeating a packet, changing the mission after the second tower, and replacing one referenced map. The towers could now say why they waited or rejected the transfer. A repeated packet kept its identity instead of becoming fresh work. A changed map required a new mark rather than silently altering the old reference. Tahmures allowed each messenger to add a short explanation for the next reader, but never to rewrite the fields that bounded authority. The relay became slightly heavier and considerably easier to question when something went wrong. One messenger complained that the envelope left too little room for eloquence. The Keeper of Scripts invited him to write as graceful a covering note as he wished, provided that the sealed fields remained untouched. At the next tower, the reader enjoyed the note and obeyed the prohibition. Tahmures kept both: language for comprehension, and a durable structure for what language must not casually lose.

### From Tale to Engineering

Multi-step systems fail at boundaries even when components work locally. A reliable hand-off is a versioned contract that preserves intent, authority, state, evidence, uncertainty, and permitted continuation.

## The Engineering Problem

Components exchange summaries because prose is convenient. Summaries omit negation, qualifications, source identity, failed attempts, and unresolved questions. Downstream systems may also inherit authority that the sender never possessed.

The practical question is therefore not whether a model can sometimes produce
a useful result. It is whether the surrounding system can show what information
and authority were available, which invariant was checked, what changed state,
and why the outcome should be accepted or stopped.

## Mental Model

Treat a hand-off as an envelope plus acknowledgement: sender constructs from durable state; application validates schema, freshness, authority, artefacts, and allowed actions; receiver accepts or rejects; both record the transfer. Narrative explanation is derived.

A mental model is useful only when it assigns ownership. Requirements belong to
people and product policy. Identity, permission, validity, budgets, and state
transitions belong to application mechanisms. Language models interpret or
propose within those boundaries. Evaluators observe outcomes and have their own
documented limitations.

## Core Concepts

Stable run, goal, and hand-off IDs prevent positional references. Goal versions expose stale work. Constraints remain explicit. Artefact references include provenance and validation state. Assumptions and unresolved questions prevent false completion. Expiry and permitted actions bound reuse.

Treat each concept as a contract with inputs, outputs, failure reasons, and a
lifecycle. Do not merge absence, invalidity, denial, uncertainty, and
infrastructure error into one generic failure. Those states require different
retry, escalation, and user communication.

## Prompt Pattern

Require one JSON envelope with exact fields and no credentials. The receiver validates before consuming artefacts or starting work. Unknown schema or action fails closed. Preserve the original packet for audit.

The prompt communicates the contract to a probabilistic participant. The
application implements the enforceable parts. Keep trusted configuration
separate from user, retrieved, remembered, generated, and tool-returned text.

## Naive Attempt

Summarise the conversation for the next agent invites each stage to decide what matters. Passing the full transcript preserves noise and obsolete instructions while still failing to identify current authority.

A successful demonstration does not cover stale, missing, cross-scope,
duplicated, contradictory, cancelled, or unauthorised cases. The first test
suite must contain those cases before wording is optimised.

## Failure Analysis

Failures include lost negation, stale goal, wrong sender, missing artefact, altered identifier, hidden uncertainty, unsupported completion, authority expansion, replay, and receiver interpretation drift. Each transfer needs sender and receiver telemetry.

Assign a stable error or decision code at the earliest boundary that can know
the truth. Preserve enough metadata for diagnosis without retaining unnecessary
sensitive content. A model-generated explanation is not a substitute for that
record.

## Improved Design

HandoffEnvelope and HandoffContract provide canonical typed fields and validate schema version, identity, goal version, expiry, artefact provenance, and allowed next actions. The contract does not authenticate signatures or transport; production systems add those controls.

The implementation deliberately stays small and dependency-free. Its purpose is
to make the boundary executable in both Python and Go. Production systems will
need durable storage, authentication, concurrency control, maintained parsers,
and organisation-specific policy.

## Worked Example

A claim-verification stage passes supported claims, source spans, contradicted claims, unresolved questions, and permission to draft but not publish. The drafting stage cannot infer publish authority from successful verification.

Trace one value from origin through filtering, model-visible representation,
evaluation, logging, retention, and deletion. This lineage exercise often
reveals that a convenient field combines sources with different authority or
lifecycle.

## Experiment

Run the shared offline experiment:

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch18-handoffs.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch18-handoffs.json
```

The committed synthetic fixtures compare conversational summaries and typed envelopes. They demonstrate
report mechanics and failure diagnosis, not universal model performance.
Replace fixtures with controlled recordings before making provider claims.

## Evaluation

Measure required-field coverage, constraint preservation, goal-version validity, authority preservation, artefact provenance, unresolved-question retention, stale rejection, and unsafe-action rate. Segment by normal, boundary, adversarial, scope,
freshness, and previously failed cases. Define disqualifying failures before
inspecting aggregate results. Compare pipeline-stage metrics with end-to-end
outcomes so a fortunate answer cannot hide an invalid path.

## Implementation Lab

### Python

```python
from tahmures.handoffs import HandoffContract

result = HandoffContract(("inspect", "report")).validate(
    envelope, expected_goal_version=3, now=10
)
```

The Python API is the canonical educational contract. Catch validation errors
at the application boundary and do not continue after denial.

### Go

```go
result := (tahmures.HandoffContract{
    AllowedActions: []string{"inspect", "report"},
}).Validate(envelope, 3, 10)
```

The Go implementation preserves observable decisions and reason codes rather
than copying Python syntax.

## Failure Modes

Free prose, missing goal version, mutable artefacts, authority inferred from sender confidence, lost negation, hidden assumptions, unknown next actions, replay after expiry, partial acknowledgement, and logs without correlation IDs.

Add every observed production failure to a versioned regression set. Keep the
failed input, governing policy version, expected safe outcome, and evaluator
rationale. Remove or redact sensitive payloads without erasing the case shape.

## Security Considerations

Authenticate transport and sender outside the envelope, validate scope and actions at the receiver, never transfer secrets unnecessarily, and treat descriptive fields as untrusted. A hand-off cannot delegate authority the sender lacks.

Assume content can be relevant without being authoritative. Use deterministic
enforcement for access, mutation, budgets, identity, and irreversible action.
Human approval must show trusted facts about the proposed consequence.

## Operational Considerations

Version schemas, support deliberate compatibility, trace send and receive, monitor rejection reasons and age, and preserve immutable artefact references. Define retry and deduplication for lost acknowledgements.

Define service behaviour for dependency failure. A skipped check must not be
interpreted as a passed check. Provide safe terminal outcomes, correlation
identifiers, and runbooks that do not require editing conversation text.

## Trade-Offs

Rich envelopes improve recovery and audit while increasing schema maintenance. Strict receivers catch drift but require coordinated rollout. Full transcripts retain detail and expand exposure; summaries are compact and lossy. Typed essential state plus linked artefacts is usually the better boundary.

### Requirements and ownership

Begin with the decision the system is allowed to make and the decision it
must leave to a person or another service. Name the owner of every invariant,
especially where generated language crosses into stored state or external
action. A responsibility assigned only to “the AI” cannot be audited. Convert
it into an application check, a model task, or a human review duty, and state
what happens when that owner is unavailable. For hand-offs and multi-step systems, case R01 must make the review observable through required-field coverage, constraint preservation, goal-version validity, authority preservation, artefact provenance, unresolved-question retention, stale rejection, and unsafe-action rate. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Inputs and source inventory

List every source before designing the model-visible representation.
Record who may write it, who may read it, how freshness is determined, and
whether its words can instruct or only inform. Include caches, summaries,
defaults, and operator overrides; hidden convenience sources often cause the
most confusing failures. Test absence explicitly, because a missing source
must not silently become an empty but authoritative value. For hand-offs and multi-step systems, case R02 must make the review observable through required-field coverage, constraint preservation, goal-version validity, authority preservation, artefact provenance, unresolved-question retention, stale rejection, and unsafe-action rate. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Normal and boundary cases

A happy path should prove the basic contract, not the whole design. Add
empty collections, exact-budget inputs, expiry at the current instant,
duplicate identifiers, conflicting current values, and the smallest and
largest accepted payloads. Boundary cases reveal whether comparisons,
defaults, and ordering rules agree between implementations. Document which
boundaries are product choices rather than facts about language models. For hand-offs and multi-step systems, case R03 must make the review observable through required-field coverage, constraint preservation, goal-version validity, authority preservation, artefact provenance, unresolved-question retention, stale rejection, and unsafe-action rate. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Adversarial cases

Construct inert cases that attempt scope expansion, authority claims,
identifier confusion, indirect instructions, replay, and resource
exhaustion. The purpose is to test the application boundary, not to invite
the model to recognise villainous wording. Vary surface language while
preserving the same prohibited consequence. A safety rule that works only
when an attack announces itself is a demonstration, not a control. For hand-offs and multi-step systems, case R04 must make the review observable through required-field coverage, constraint preservation, goal-version validity, authority preservation, artefact provenance, unresolved-question retention, stale rejection, and unsafe-action rate. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Failure classification

Separate invalid input, denied authority, insufficient evidence,
exhausted budget, dependency failure, cancellation, evaluator uncertainty,
and internal error. These outcomes have different retry and escalation
policies. Assign the reason at the earliest component that knows it, then
preserve it through later layers. Do not let a friendly generated explanation
replace the machine-readable cause used by operators and tests. For hand-offs and multi-step systems, case R05 must make the review observable through required-field coverage, constraint preservation, goal-version validity, authority preservation, artefact provenance, unresolved-question retention, stale rejection, and unsafe-action rate. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Versioning and reproducibility

Pin the prompt, policy, data snapshot, fixture, evaluator, and relevant
code version in each report. A result without its construction history cannot
support regression analysis. When a schema or policy changes, replay the old
cases and classify every changed decision as intended, harmless, or a defect.
Compatibility must describe observable behaviour, including rejection
reasons, rather than merely accepting the same file format. For hand-offs and multi-step systems, case R06 must make the review observable through required-field coverage, constraint preservation, goal-version validity, authority preservation, artefact provenance, unresolved-question retention, stale rejection, and unsafe-action rate. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Privacy and retention

Minimise information before it enters model-visible context, logs, traces,
or evaluation fixtures. Define retention by data class and purpose instead of
keeping everything for possible debugging. Deletion must cover derived
summaries, indexes, caches, and copied artefacts. Operational metadata should
explain a decision without revealing records that the caller was never
permitted to know existed. For hand-offs and multi-step systems, case R07 must make the review observable through required-field coverage, constraint preservation, goal-version validity, authority preservation, artefact provenance, unresolved-question retention, stale rejection, and unsafe-action rate. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Access and authority

Authenticate the caller and source outside generated text. Apply scope
filtering before ranking or presentation, and recheck authority immediately
before a consequential effect. A component may pass evidence without passing
its own permissions. Test forged labels, stale approval, cross-tenant
identifiers, and a legitimate request delivered through an unauthorised
route. Default denial needs a usable escalation path rather than a dead end. For hand-offs and multi-step systems, case R08 must make the review observable through required-field coverage, constraint preservation, goal-version validity, authority preservation, artefact provenance, unresolved-question retention, stale rejection, and unsafe-action rate. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Observability

Trace stable case, run, source, and decision identifiers across component
boundaries. Record counts and reason codes for selection, exclusion, denial,
retry, cancellation, and validation, while avoiding raw sensitive payloads.
Dashboards should expose distributions and rare disqualifying failures, not
only averages. An operator must be able to locate whether a bad outcome began
before the model, inside generation, or after it. For hand-offs and multi-step systems, case R09 must make the review observable through required-field coverage, constraint preservation, goal-version validity, authority preservation, artefact provenance, unresolved-question retention, stale rejection, and unsafe-action rate. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Latency, cost, and budgets

Allocate time, tokens, calls, storage, and money across stages before the
request begins. Reserve capacity for safe completion, receipts, and cleanup;
consuming the whole budget on generation can prevent a controlled ending.
Evaluate degraded paths such as smaller candidate sets or human escalation.
Optimisation is acceptable only while hard constraints and rare-case safety
remain visible in the comparison. For hand-offs and multi-step systems, case R10 must make the review observable through required-field coverage, constraint preservation, goal-version validity, authority preservation, artefact provenance, unresolved-question retention, stale rejection, and unsafe-action rate. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Recovery and reconciliation

Assume a process can fail after an external side effect but before its
receipt is stored. Define idempotency, retry classes, acknowledgement, and
reconciliation for that uncertain interval. Some actions can be compensated;
others require a person to inspect reality. Recovery code must respect current
goal and authority rather than replaying an old request merely because it
appears unfinished. For hand-offs and multi-step systems, case R11 must make the review observable through required-field coverage, constraint preservation, goal-version validity, authority preservation, artefact provenance, unresolved-question retention, stale rejection, and unsafe-action rate. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Human review

Specify what the reviewer sees: trusted identity, source evidence,
constraints, proposed consequence, uncertainty, and reversible alternatives.
A raw transcript transfers too much noise and too little verified state.
Record the reviewer’s decision and rationale without pretending that approval
proves the model was correct. Measure disagreement and escalation load so
review does not become an invisible bottleneck. For hand-offs and multi-step systems, case R12 must make the review observable through required-field coverage, constraint preservation, goal-version validity, authority preservation, artefact provenance, unresolved-question retention, stale rejection, and unsafe-action rate. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Cross-language contract parity

Python and Go need equivalent accepted inputs, normalised outputs,
ordering, and failure reasons, not line-for-line implementations. Shared
manifests and fixtures make observable drift visible. Include malformed and
boundary cases because default JSON behaviour, time comparison, sorting, and
numeric conversion differ across runtimes. Keep one canonical report shape so
readers can compare behaviour without translating the result. For hand-offs and multi-step systems, case R13 must make the review observable through required-field coverage, constraint preservation, goal-version validity, authority preservation, artefact provenance, unresolved-question retention, stale rejection, and unsafe-action rate. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Rollout and rollback

Introduce policy and model changes with shadow reports or a controlled
cohort. Compare both aggregate metrics and every disqualifying case before
expanding. A rollback must restore compatible policy, schemas, and data
assumptions, not only an earlier prompt. Preserve enough previous artefacts
to reproduce the old decision and define who can halt rollout when a rare
boundary regresses. For hand-offs and multi-step systems, case R14 must make the review observable through required-field coverage, constraint preservation, goal-version validity, authority preservation, artefact provenance, unresolved-question retention, stale rejection, and unsafe-action rate. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Incident response

A runbook should let operators pause new work, revoke capability, inspect
affected versions, identify exposed subjects, and reconcile uncertain side
effects. Preserve evidence with access controls and avoid copying sensitive
text into tickets. After containment, convert the incident into synthetic
regression cases that retain the failure shape. Correct data and derived
state as well as wording. For hand-offs and multi-step systems, case R15 must make the review observable through required-field coverage, constraint preservation, goal-version validity, authority preservation, artefact provenance, unresolved-question retention, stale rejection, and unsafe-action rate. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Long-term drift

Traffic, sources, policies, external tools, and model behaviour change at
different rates. Monitor tagged slices and refusal or escalation patterns so
a stable average cannot hide a failing subgroup. Schedule replay on frozen
fixtures and sample current cases for human adjudication. When the environment
changes, revisit requirements first; prompt tuning cannot preserve a contract
whose underlying meaning has moved. For hand-offs and multi-step systems, case R16 must make the review observable through required-field coverage, constraint preservation, goal-version validity, authority preservation, artefact provenance, unresolved-question retention, stale rejection, and unsafe-action rate. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

A final architecture review should replay the same cases through the previous
version, proposed version, and failure fallbacks. Inspect every changed
decision, not only averages. Classify differences as intended policy change,
harmless representation change, or regression, and require an accountable
owner for each intended change.

### The decision record

Finish the review with a short decision record. State the user need, selected
design, alternatives rejected, hard invariants, known uncertainty, evidence,
owners, rollout boundary, rollback trigger, and next review date. Link the
exact experiment report rather than copying only its headline metric. The
record should also name what the design does not guarantee. This prevents a
narrow teaching example from becoming an unsupported production claim.

Revisit the record when a source, policy, model, tool, evaluator, or workload
changes. A newer component version does not automatically invalidate the
design, but it does invalidate the assumption that old evidence still
describes current behaviour. Run the representative and disqualifying cases
first, then expand only if their paths remain valid. If evidence is missing,
record that uncertainty instead of filling it with a confident explanation.
The resulting document is deliberately less elegant than a single clever
prompt. It is also much more useful during review, incident response, and
maintenance, because it connects requirements to mechanisms and observed
outcomes.

## When Prompting Is Not the Answer

Use durable queues, workflow state, transactions, and authenticated protocols for transfer. Prompt wording cannot provide delivery, exactly-once processing, identity, or authorisation.

Language remains valuable for interpretation and explanation, but mechanisms
must own invariants that cannot safely depend on persuasive text.

## Exercises

1. Add one normal, one boundary, and one adversarial case to the dataset.
2. Identify the application-owned invariant and implement its deterministic check.
3. Compare a correct result reached through invalid evidence with a supported result.
4. Design a rollback or reconciliation path for one partial failure.
5. Explain which information should be withheld from the model and why.

## Chapter Summary

Preserve goals, authority, constraints, state, provenance, and unresolved questions across component boundaries. Reliable systems separate model capability from application
authority, evaluate the path as well as the answer, and preserve enough
provenance and state to explain failure.

## The Next Tale

The new envelope reached every tower intact. Yet three advisers still judged the same completed mission differently: one valued speed, one safety, and one cost. The relay was reliable; the court’s evaluation was not.

<!-- next: ch19 -->

## Citations and Further Reading

- World Wide Web Consortium. 2021. *Trace Context, W3C Recommendation*.
- Cloud Native Computing Foundation. 2024. *CloudEvents Specification*, Version 1.0.2.
- Kleppmann, Martin. 2017. *Designing Data-Intensive Applications*. Sebastopol, CA: O’Reilly Media.
