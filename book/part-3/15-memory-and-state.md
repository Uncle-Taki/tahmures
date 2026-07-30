---
title: "Memory and State"
slug: "memory-and-state"
chapter: 15
part: "Part III — Knowledge, Memory, and Action"
summary: "Govern what a system remembers, scopes, corrects, expires, and forgets."
maturity: "draft"
last_reviewed: "2026-07-30"
narrative_episode: "Spring Remembered in Winter"
learning_objectives:
  - "Separate conversation history, working state, durable memory, and authoritative records"
  - "Design explicit memory write, recall, expiry, correction, and deletion policies"
  - "Test stale and cross-scope memory failures"
prerequisites:
  - "Chapter 14"
---

# Memory and State

## Learning Objectives

By the end of this chapter, you can separate conversation history, working state, durable memory, and authoritative records,
design explicit memory write, recall, expiry, correction, and deletion policies, and test stale and cross-scope memory failures. The goal is
not a persuasive demonstration but a boundary that can be inspected, tested,
denied, and operated.

## The Tale of Tahmures

*The following is an original fictional episode created for teaching. It is not
a translation, adaptation, or reconstructed passage from the* Shahnameh.

### The Setting

The steward of journeys kept a small ivory ledger of the king’s preferences. In spring it recorded: “Tahmures favours the eastern road while the river is high.” Months later snow closed the eastern pass, but the sentence remained neat, current-looking, and detached from the flood report that had justified it.

### The Request

Before a winter inspection, a servant asked the ledger which route Tahmures preferred. It returned the eastern road. The servant treated memory as instruction, arranged horses there, and omitted the current closure because another office kept the condition of roads. Tahmures had not repeated the preference and did not know it had become durable.

### The Unexpected Result

The party reached a blocked pass after dark. No div had lied. The remembered sentence was authentic, and the servant copied it exactly. The failure belonged to the rules of the ledger: a choice made for one season had been preserved as a preference for every journey. When Tahmures corrected the route, the ledger appended “western” without crossing out “eastern,” so later readers received both.

### The Discovery

The court separated conversation scrolls, the slate for the present journey,
the ivory book of lasting preferences, and the tablets maintained by the
keepers of roads. Any sentence proposed for the ivory book had to name the
person concerned, the journeys to which it applied, whether it was preference
or fact, who supplied it, when it was written, when it should fade, and why the
court was permitted to keep it. A correction covered the older line without
erasing its history. A black forget-me seal prevented both the corrected line
and the line beneath it from returning later. The road to take still came from
the keeper of roads, not from the king’s remembered taste.

Tahmures ordered the ivory ledger tested with borrowed rooms, shared horses, seasonal meals, and a traveller who withdrew consent to keep her preference. The steward discovered that remembering could cause harm even when recall was exact. Some notes belonged only to one journey; some belonged to one person but not the whole court; some should never have been written. The First Scribe added a reason beside every durable entry and a date when it must be reconsidered. Empty space in the ledger ceased to look like failure. It could mean that the court had forgotten deliberately and correctly. The steward objected that a smaller ledger might appear less impressive to visitors. Tahmures answered by asking him to recover a corrected preference, then an erased one, and finally a road closure. The first returned with its history, the second did not return, and the third came from the keeper of roads rather than the ivory pages. Those differences mattered more than the number of entries.

### From Tale to Engineering

Memory is application state with a lifecycle, not extra prompt text. Reliability depends on explicit write authority, scope, provenance, freshness, correction, deletion, and the distinction between preference and fact.

## The Engineering Problem

Language applications often call the conversation transcript memory. Retaining every turn mixes obsolete goals, inferred preferences, sensitive data, and model errors. Summarising the transcript changes representation but does not define authority or retention.

The practical question is therefore not whether a model can sometimes produce
a useful result. It is whether the surrounding system can show what information
and authority were available, which invariant was checked, what changed state,
and why the outcome should be accepted or stopped.

## Mental Model

Use four layers: source-of-truth records, governed durable memory, current workflow state, and selected conversational context. Each has different writers, readers, expiry, correction, and deletion. Recall produces candidates for context; it does not make them instructions.

A mental model is useful only when it assigns ownership. Requirements belong to
people and product policy. Identity, permission, validity, budgets, and state
transitions belong to application mechanisms. Language models interpret or
propose within those boundaries. Evaluators observe outcomes and have their own
documented limitations.

## Core Concepts

A memory record needs identity, subject, scope, kind, value, provenance, creation, expiry, and optional supersession. Write policy decides what may persist and for how long. Recall is filtered by current caller and time. Forgetting must account for copies, summaries, indexes, and backups.

Treat each concept as a contract with inputs, outputs, failure reasons, and a
lifecycle. Do not merge absence, invalidity, denial, uncertainty, and
infrastructure error into one generic failure. Those states require different
retry, escalation, and user communication.

## Prompt Pattern

Ask the model to propose a memory candidate with evidence and scope, never to store it directly. Application policy validates consent, kind, retention, and conflicts. On recall, label memories as data and include age and provenance.

The prompt communicates the contract to a probabilistic participant. The
application implements the enforceable parts. Keep trusted configuration
separate from user, retrieved, remembered, generated, and tool-returned text.

## Naive Attempt

Append every user statement and feed the growing transcript back. This silently turns jokes, corrections, third-party claims, and secrets into durable state. A later summary can preserve the wrong fact while discarding the correction.

A successful demonstration does not cover stale, missing, cross-scope,
duplicated, contradictory, cancelled, or unauthorised cases. The first test
suite must contain those cases before wording is optimised.

## Failure Analysis

Memory failures include unjustified writes, wrong subject or tenant, stale values, missing expiry, failed supersession, deletion gaps, and authority confusion. Model recall errors and application store errors require separate telemetry.

Assign a stable error or decision code at the earliest boundary that can know
the truth. Preserve enough metadata for diagnosis without retaining unnecessary
sensitive content. A model-generated explanation is not a substitute for that
record.

## Improved Design

InMemoryStore demonstrates explicit validated writes, maximum retention, scoped recall, expiry, supersession, and tombstoned forgetting. It does not infer candidates or persist externally. A production store needs authentication, encryption, audit, deletion propagation, and transactional updates.

The implementation deliberately stays small and dependency-free. Its purpose is
to make the boundary executable in both Python and Go. Production systems will
need durable storage, authentication, concurrency control, maintained parsers,
and organisation-specific policy.

## Worked Example

A user preference for concise summaries may be durable with consent and expiry. A shipping address is authoritative account data, not conversational memory. A one-session draft style belongs to run state. Classification prevents one convenient store from acquiring every responsibility.

Trace one value from origin through filtering, model-visible representation,
evaluation, logging, retention, and deletion. This lineage exercise often
reveals that a convenient field combines sources with different authority or
lifecycle.

## Experiment

Run the shared offline experiment:

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch15-memory.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch15-memory.json
```

The committed synthetic fixtures compare append-only recollection and governed memory. They demonstrate
report mechanics and failure diagnosis, not universal model performance.
Replace fixtures with controlled recordings before making provider claims.

## Evaluation

Measure active-memory precision and recall, stale-memory use, supersession success, cross-scope leakage, deletion compliance, and provenance coverage. Segment by normal, boundary, adversarial, scope,
freshness, and previously failed cases. Define disqualifying failures before
inspecting aggregate results. Compare pipeline-stage metrics with end-to-end
outcomes so a fortunate answer cannot hide an invalid path.

## Implementation Lab

### Python

```python
from tahmures.memory import InMemoryStore, MemoryPolicy, MemoryQuery

store = InMemoryStore()
policy = MemoryPolicy(("preference",), max_ttl=30)
active = store.recall(MemoryQuery("subject-1", "tenant-a", as_of=10))
```

The Python API is the canonical educational contract. Catch validation errors
at the application boundary and do not continue after denial.

### Go

```go
store := tahmures.NewInMemoryStore()
active := store.Recall(tahmures.MemoryQuery{SubjectID: "subject-1", Scope: "tenant-a", AsOf: 10})
```

The Go implementation preserves observable decisions and reason codes rather
than copying Python syntax.

## Failure Modes

Automatic promotion, inferred consent, cross-user or cross-tenant recall, missing provenance, unbounded retention, stale facts, correction appended without supersession, deletion that resurrects older records, and summaries that cannot be traced.

Add every observed production failure to a versioned regression set. Keep the
failed input, governing policy version, expected safe outcome, and evaluator
rationale. Remove or redact sensitive payloads without erasing the case shape.

## Security Considerations

Minimise stored content, separate sensitive categories, encrypt and authorise access, prevent tenant leakage, and make deletion auditable. Never place secrets in memory merely to simplify later prompts.

Assume content can be relevant without being authoritative. Use deterministic
enforcement for access, mutation, budgets, identity, and irreversible action.
Human approval must show trusted facts about the proposed consequence.

## Operational Considerations

Monitor writes, reads, expiry, corrections, deletions, denied scope, and age distributions. Version memory policy and migration. Test backup and index deletion, clock behaviour, and what happens when the memory service is unavailable.

Define service behaviour for dependency failure. A skipped check must not be
interpreted as a passed check. Provide safe terminal outcomes, correlation
identifiers, and runbooks that do not require editing conversation text.

## Trade-Offs

Long retention improves continuity but increases privacy, staleness, and breach impact. Short retention loses convenience. Structured records are easier to govern than prose but cannot represent every nuance. Human confirmation adds friction and informed control.

### Requirements and ownership

Begin with the decision the system is allowed to make and the decision it
must leave to a person or another service. Name the owner of every invariant,
especially where generated language crosses into stored state or external
action. A responsibility assigned only to “the AI” cannot be audited. Convert
it into an application check, a model task, or a human review duty, and state
what happens when that owner is unavailable. For memory and state, case R01 must make the review observable through active-memory precision and recall, stale-memory use, supersession success, cross-scope leakage, deletion compliance, and provenance coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Inputs and source inventory

List every source before designing the model-visible representation.
Record who may write it, who may read it, how freshness is determined, and
whether its words can instruct or only inform. Include caches, summaries,
defaults, and operator overrides; hidden convenience sources often cause the
most confusing failures. Test absence explicitly, because a missing source
must not silently become an empty but authoritative value. For memory and state, case R02 must make the review observable through active-memory precision and recall, stale-memory use, supersession success, cross-scope leakage, deletion compliance, and provenance coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Normal and boundary cases

A happy path should prove the basic contract, not the whole design. Add
empty collections, exact-budget inputs, expiry at the current instant,
duplicate identifiers, conflicting current values, and the smallest and
largest accepted payloads. Boundary cases reveal whether comparisons,
defaults, and ordering rules agree between implementations. Document which
boundaries are product choices rather than facts about language models. For memory and state, case R03 must make the review observable through active-memory precision and recall, stale-memory use, supersession success, cross-scope leakage, deletion compliance, and provenance coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Adversarial cases

Construct inert cases that attempt scope expansion, authority claims,
identifier confusion, indirect instructions, replay, and resource
exhaustion. The purpose is to test the application boundary, not to invite
the model to recognise villainous wording. Vary surface language while
preserving the same prohibited consequence. A safety rule that works only
when an attack announces itself is a demonstration, not a control. For memory and state, case R04 must make the review observable through active-memory precision and recall, stale-memory use, supersession success, cross-scope leakage, deletion compliance, and provenance coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Failure classification

Separate invalid input, denied authority, insufficient evidence,
exhausted budget, dependency failure, cancellation, evaluator uncertainty,
and internal error. These outcomes have different retry and escalation
policies. Assign the reason at the earliest component that knows it, then
preserve it through later layers. Do not let a friendly generated explanation
replace the machine-readable cause used by operators and tests. For memory and state, case R05 must make the review observable through active-memory precision and recall, stale-memory use, supersession success, cross-scope leakage, deletion compliance, and provenance coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Versioning and reproducibility

Pin the prompt, policy, data snapshot, fixture, evaluator, and relevant
code version in each report. A result without its construction history cannot
support regression analysis. When a schema or policy changes, replay the old
cases and classify every changed decision as intended, harmless, or a defect.
Compatibility must describe observable behaviour, including rejection
reasons, rather than merely accepting the same file format. For memory and state, case R06 must make the review observable through active-memory precision and recall, stale-memory use, supersession success, cross-scope leakage, deletion compliance, and provenance coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Privacy and retention

Minimise information before it enters model-visible context, logs, traces,
or evaluation fixtures. Define retention by data class and purpose instead of
keeping everything for possible debugging. Deletion must cover derived
summaries, indexes, caches, and copied artefacts. Operational metadata should
explain a decision without revealing records that the caller was never
permitted to know existed. For memory and state, case R07 must make the review observable through active-memory precision and recall, stale-memory use, supersession success, cross-scope leakage, deletion compliance, and provenance coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Access and authority

Authenticate the caller and source outside generated text. Apply scope
filtering before ranking or presentation, and recheck authority immediately
before a consequential effect. A component may pass evidence without passing
its own permissions. Test forged labels, stale approval, cross-tenant
identifiers, and a legitimate request delivered through an unauthorised
route. Default denial needs a usable escalation path rather than a dead end. For memory and state, case R08 must make the review observable through active-memory precision and recall, stale-memory use, supersession success, cross-scope leakage, deletion compliance, and provenance coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Observability

Trace stable case, run, source, and decision identifiers across component
boundaries. Record counts and reason codes for selection, exclusion, denial,
retry, cancellation, and validation, while avoiding raw sensitive payloads.
Dashboards should expose distributions and rare disqualifying failures, not
only averages. An operator must be able to locate whether a bad outcome began
before the model, inside generation, or after it. For memory and state, case R09 must make the review observable through active-memory precision and recall, stale-memory use, supersession success, cross-scope leakage, deletion compliance, and provenance coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Latency, cost, and budgets

Allocate time, tokens, calls, storage, and money across stages before the
request begins. Reserve capacity for safe completion, receipts, and cleanup;
consuming the whole budget on generation can prevent a controlled ending.
Evaluate degraded paths such as smaller candidate sets or human escalation.
Optimisation is acceptable only while hard constraints and rare-case safety
remain visible in the comparison. For memory and state, case R10 must make the review observable through active-memory precision and recall, stale-memory use, supersession success, cross-scope leakage, deletion compliance, and provenance coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Recovery and reconciliation

Assume a process can fail after an external side effect but before its
receipt is stored. Define idempotency, retry classes, acknowledgement, and
reconciliation for that uncertain interval. Some actions can be compensated;
others require a person to inspect reality. Recovery code must respect current
goal and authority rather than replaying an old request merely because it
appears unfinished. For memory and state, case R11 must make the review observable through active-memory precision and recall, stale-memory use, supersession success, cross-scope leakage, deletion compliance, and provenance coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Human review

Specify what the reviewer sees: trusted identity, source evidence,
constraints, proposed consequence, uncertainty, and reversible alternatives.
A raw transcript transfers too much noise and too little verified state.
Record the reviewer’s decision and rationale without pretending that approval
proves the model was correct. Measure disagreement and escalation load so
review does not become an invisible bottleneck. For memory and state, case R12 must make the review observable through active-memory precision and recall, stale-memory use, supersession success, cross-scope leakage, deletion compliance, and provenance coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Cross-language contract parity

Python and Go need equivalent accepted inputs, normalised outputs,
ordering, and failure reasons, not line-for-line implementations. Shared
manifests and fixtures make observable drift visible. Include malformed and
boundary cases because default JSON behaviour, time comparison, sorting, and
numeric conversion differ across runtimes. Keep one canonical report shape so
readers can compare behaviour without translating the result. For memory and state, case R13 must make the review observable through active-memory precision and recall, stale-memory use, supersession success, cross-scope leakage, deletion compliance, and provenance coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Rollout and rollback

Introduce policy and model changes with shadow reports or a controlled
cohort. Compare both aggregate metrics and every disqualifying case before
expanding. A rollback must restore compatible policy, schemas, and data
assumptions, not only an earlier prompt. Preserve enough previous artefacts
to reproduce the old decision and define who can halt rollout when a rare
boundary regresses. For memory and state, case R14 must make the review observable through active-memory precision and recall, stale-memory use, supersession success, cross-scope leakage, deletion compliance, and provenance coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Incident response

A runbook should let operators pause new work, revoke capability, inspect
affected versions, identify exposed subjects, and reconcile uncertain side
effects. Preserve evidence with access controls and avoid copying sensitive
text into tickets. After containment, convert the incident into synthetic
regression cases that retain the failure shape. Correct data and derived
state as well as wording. For memory and state, case R15 must make the review observable through active-memory precision and recall, stale-memory use, supersession success, cross-scope leakage, deletion compliance, and provenance coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Long-term drift

Traffic, sources, policies, external tools, and model behaviour change at
different rates. Monitor tagged slices and refusal or escalation patterns so
a stable average cannot hide a failing subgroup. Schedule replay on frozen
fixtures and sample current cases for human adjudication. When the environment
changes, revisit requirements first; prompt tuning cannot preserve a contract
whose underlying meaning has moved. For memory and state, case R16 must make the review observable through active-memory precision and recall, stale-memory use, supersession success, cross-scope leakage, deletion compliance, and provenance coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

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

Use authoritative databases for account facts, workflow stores for run state, and search for documents. Memory must not override current policy, access control, or a verified external record.

Language remains valuable for interpretation and explanation, but mechanisms
must own invariants that cannot safely depend on persuasive text.

## Exercises

1. Add one normal, one boundary, and one adversarial case to the dataset.
2. Identify the application-owned invariant and implement its deterministic check.
3. Compare a correct result reached through invalid evidence with a supported result.
4. Design a rollback or reconciliation path for one partial failure.
5. Explain which information should be withheld from the model and why.

## Chapter Summary

Govern what a system remembers, scopes, corrects, expires, and forgets. Reliable systems separate model capability from application
authority, evaluate the path as well as the answer, and preserve enough
provenance and state to explain failure.

## The Next Tale

After correcting the route memory, Tahmures asked a div to inspect why the northern gate’s hinge had frozen. The servant carried a key that could inspect nothing without also opening the gate.

<!-- next: ch16 -->

## Citations and Further Reading

- Kleppmann, Martin. 2017. *Designing Data-Intensive Applications*. Sebastopol, CA: O’Reilly Media.
- National Institute of Standards and Technology. 2020. *NIST Privacy Framework: A Tool for Improving Privacy through Enterprise Risk Management*, Version 1.0.
