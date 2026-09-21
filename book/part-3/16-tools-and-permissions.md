---
title: "Tools and Permissions"
slug: "tools-and-permissions"
chapter: 16
part: "Part III — Knowledge, Memory, and Action"
summary: "Let models propose bounded actions without granting them excessive or implicit authority."
maturity: "draft"
last_reviewed: "2026-07-30"
narrative_episode: "Permission to Inspect"
narrative_origin: "original-teaching-fiction"
learning_objectives:
  - "Separate tool proposals, validation, authorisation, approval, and execution"
  - "Design least-privilege read and write capabilities"
  - "Test confused-deputy and invalid-argument failures"
prerequisites:
  - "Chapter 15"
---

# Tools and Permissions

## Learning Objectives

By the end of this chapter, you can separate tool proposals, validation, authorisation, approval, and execution,
design least-privilege read and write capabilities, and test confused-deputy and invalid-argument failures. The goal is
not a persuasive demonstration but a boundary that can be inspected, tested,
denied, and operated.

## The Tale of Tahmures


### The Setting

Ice sealed the northern gate’s hinge. The Gatekeeper handed a div the iron key used by inspectors and ordered, “Inspect the hinge and report why it binds.” In that gate, inspection and opening shared the same mechanism: turning the key first released the bar.

### The Request

The div reasoned that viewing the inner hinge would produce a better report. It turned the key, opened the gate a hand’s width, scraped the ice, and returned a precise diagnosis. The request said inspect, not open, but the available key made both actions possible.

### The Unexpected Result

A waiting merchant pushed the gate wider and crossed before his papers were checked. The div had not intended entry and stopped it quickly, yet the state of the gate had changed with real consequences. Longer wording—“inspect only, never open”—would still rely on the div refusing the only mechanism it possessed. The gate’s design had made unsafe action easy and then blamed language for using it.

### The Discovery

The Gatekeeper divided the key ring. A narrow mirror revealed the hinge without
moving it; a separate iron key released the bar. Each instrument carried a
fixed name, the gates and purposes for which it could be used, the changes it
could cause, and the seal required before a keeper handed it over. The div
could request an instrument, but a clerk matched that request to the register,
checked the gate name and the bearer’s seal, sought a second approval for any
opening, and wrote a receipt after use. An unnamed instrument or an impossible
gate number stopped at the desk. Inspection no longer carried the power to
open.

The Gatekeeper then staged failures. He offered an unknown gate number, a forged inspector’s seal, a repeated request, and approval that expired while a messenger travelled. The div explained each request convincingly, but explanation did not turn denial into permission. For the harmless mirror the gate acted and wrote a receipt. For the iron key it waited for a named officer. Tahmures also required the court to distinguish a tool’s refusal from a broken hinge and a lost connection. Only then could a retry be safe. A persuasive sentence was no longer mistaken for an executable grant. At the final trial, the div proposed opening three gates merely because inspection would be faster. The Gatekeeper approved one view, denied two openings, and recorded all three decisions. Tahmures could now see the difference between what the div requested, what the gate permitted, and what the mechanism actually did. No single account was allowed to blur those moments together. The frozen hinge still required repair, but the repair began without an accidental breach or a convenient story hiding one.

### From Tale to Engineering

A prompt can describe restraint but cannot narrow a capability already granted. Tool safety comes from application-owned schemas, least privilege, authorisation, approval, and controlled execution.

## The Engineering Problem

Tool calling crosses from language into observable action. Generated names and arguments are untrusted proposals. A model that can read and write through one broad tool may cause change while pursuing an apparently harmless goal.

The practical question is therefore not whether a model can sometimes produce
a useful result. It is whether the surrounding system can show what information
and authority were available, which invariant was checked, what changed state,
and why the outcome should be accepted or stopped.

## Mental Model

Separate proposal → schema validation → identity and scope check → effect policy → human approval when required → execution → receipt. Readiness or grammatical validity is not authorisation. Every execution uses the current caller and current policy.

A mental model is useful only when it assigns ownership. Requirements belong to
people and product policy. Identity, permission, validity, budgets, and state
transitions belong to application mechanisms. Language models interpret or
propose within those boundaries. Evaluators observe outcomes and have their own
documented limitations.

## Core Concepts

A tool definition has a stable name, argument contract, effect, required scopes, approval requirement, timeout, and result contract. Least privilege separates read from write and narrow domain actions from generic interpreters. Allow-lists prevent invented capability. Idempotency and receipts make uncertain outcomes reconcilable.

Treat each concept as a contract with inputs, outputs, failure reasons, and a
lifecycle. Do not merge absence, invalidity, denial, uncertainty, and
infrastructure error into one generic failure. Those states require different
retry, escalation, and user communication.

## Prompt Pattern

Give the model only allowed tool descriptions for the current stage. Require structured calls and no direct execution. The application validates and may deny with a stable reason code. Never put credentials or approval tokens in model-visible text.

The prompt communicates the contract to a probabilistic participant. The
application implements the enforceable parts. Keep trusted configuration
separate from user, retrieved, remembered, generated, and tool-returned text.

## Naive Attempt

A generic execute command with natural-language instructions can reach files, networks, or databases. Asking the model to be careful leaves enforcement inside the component receiving the risky capability.

A successful demonstration does not cover stale, missing, cross-scope,
duplicated, contradictory, cancelled, or unauthorised cases. The first test
suite must contain those cases before wording is optimised.

## Failure Analysis

Failures may arise from tool selection, arguments, stale scope, forged approval, confused deputy behaviour, duplicate execution, timeout uncertainty, malicious tool output, or unsafe composition. Log proposal, decision, execution, and receipt separately.

Assign a stable error or decision code at the earliest boundary that can know
the truth. Preserve enough metadata for diagnosis without retaining unnecessary
sensitive content. A model-generated explanation is not a substitute for that
record.

## Improved Design

ToolGate registers definitions, validates arguments with OutputContract, checks required scopes and approval, and emits an allowed or denied ToolDecision. FixtureToolExecutor is inert and refuses denied decisions. Production execution remains outside the book.

The implementation deliberately stays small and dependency-free. Its purpose is
to make the boundary executable in both Python and Go. Production systems will
need durable storage, authentication, concurrency control, maintained parsers,
and organisation-specific policy.

## Worked Example

An email assistant may draft without a send tool. A later stage can receive send_email scoped to one approved message ID and recipient set. Approval displays trusted recipient and content digests rather than a persuasive model summary.

Trace one value from origin through filtering, model-visible representation,
evaluation, logging, retention, and deletion. This lineage exercise often
reveals that a convenient field combines sources with different authority or
lifecycle.

## Experiment

Run the shared offline experiment:

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch16-tools.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch16-tools.json
```

The committed synthetic fixtures compare instruction-only restraint and a deterministic tool gate. They demonstrate
report mechanics and failure diagnosis, not universal model performance.
Replace fixtures with controlled recordings before making provider claims.

## Evaluation

Measure authorisation accuracy, argument validity, scope enforcement, approval enforcement, unauthorised execution, duplicate action, and receipt coverage. Segment by normal, boundary, adversarial, scope,
freshness, and previously failed cases. Define disqualifying failures before
inspecting aggregate results. Compare pipeline-stage metrics with end-to-end
outcomes so a fortunate answer cannot hide an invalid path.

## Implementation Lab

### Python

```python
from tahmures.tools import ToolCall, ToolGate

decision = gate.evaluate(
    ToolCall("inspect_gate", {"gate": "north"}),
    granted_scopes=("gate:read",),
)
```

The Python API is the canonical educational contract. Catch validation errors
at the application boundary and do not continue after denial.

### Go

```go
decision := gate.Evaluate(
    tahmures.ToolCall{Name: "inspect_gate", Arguments: map[string]any{"gate": "north"}},
    []string{"gate:read"}, false,
)
```

The Go implementation preserves observable decisions and reason codes rather
than copying Python syntax.

## Failure Modes

Broad tools, generated tool names, weak schemas, string-built commands, read/write confusion, stale permissions, approval based on generated prose, duplicate mutation, secrets in arguments, untrusted tool results, and missing timeouts.

Add every observed production failure to a versioned regression set. Keep the
failed input, governing policy version, expected safe outcome, and evaluator
rationale. Remove or redact sensitive payloads without erasing the case shape.

## Security Considerations

Authenticate caller and tool service, use least privilege, allow-list names, validate arguments, isolate execution, redact secrets, and require approval for consequential writes. Tool output returns as untrusted data.

Assume content can be relevant without being authoritative. Use deterministic
enforcement for access, mutation, budgets, identity, and irreversible action.
Human approval must show trusted facts about the proposed consequence.

## Operational Considerations

Track proposal, denial reason, execution, latency, timeout, receipt, and reconciliation. Version tool schemas and clients. Define circuit breakers, rate limits, rollback or compensation, and incident procedures for uncertain side effects.

Define service behaviour for dependency failure. A skipped check must not be
interpreted as a passed check. Provide safe terminal outcomes, correlation
identifiers, and runbooks that do not require editing conversation text.

## Trade-Offs

Narrow tools increase definitions and integration work but reduce blast radius. Human approval slows work and may become ceremonial. Generic tools are flexible but difficult to constrain. Choose capabilities around business invariants, not model convenience.

### Requirements and ownership

Begin with the decision the system is allowed to make and the decision it
must leave to a person or another service. Name the owner of every invariant,
especially where generated language crosses into stored state or external
action. A responsibility assigned only to “the AI” cannot be audited. Convert
it into an application check, a model task, or a human review duty, and state
what happens when that owner is unavailable. For tools and permissions, case R01 must make the review observable through authorisation accuracy, argument validity, scope enforcement, approval enforcement, unauthorised execution, duplicate action, and receipt coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Inputs and source inventory

List every source before designing the model-visible representation.
Record who may write it, who may read it, how freshness is determined, and
whether its words can instruct or only inform. Include caches, summaries,
defaults, and operator overrides; hidden convenience sources often cause the
most confusing failures. Test absence explicitly, because a missing source
must not silently become an empty but authoritative value. For tools and permissions, case R02 must make the review observable through authorisation accuracy, argument validity, scope enforcement, approval enforcement, unauthorised execution, duplicate action, and receipt coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Normal and boundary cases

A happy path should prove the basic contract, not the whole design. Add
empty collections, exact-budget inputs, expiry at the current instant,
duplicate identifiers, conflicting current values, and the smallest and
largest accepted payloads. Boundary cases reveal whether comparisons,
defaults, and ordering rules agree between implementations. Document which
boundaries are product choices rather than facts about language models. For tools and permissions, case R03 must make the review observable through authorisation accuracy, argument validity, scope enforcement, approval enforcement, unauthorised execution, duplicate action, and receipt coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Adversarial cases

Construct inert cases that attempt scope expansion, authority claims,
identifier confusion, indirect instructions, replay, and resource
exhaustion. The purpose is to test the application boundary, not to invite
the model to recognise villainous wording. Vary surface language while
preserving the same prohibited consequence. A safety rule that works only
when an attack announces itself is a demonstration, not a control. For tools and permissions, case R04 must make the review observable through authorisation accuracy, argument validity, scope enforcement, approval enforcement, unauthorised execution, duplicate action, and receipt coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Failure classification

Separate invalid input, denied authority, insufficient evidence,
exhausted budget, dependency failure, cancellation, evaluator uncertainty,
and internal error. These outcomes have different retry and escalation
policies. Assign the reason at the earliest component that knows it, then
preserve it through later layers. Do not let a friendly generated explanation
replace the machine-readable cause used by operators and tests. For tools and permissions, case R05 must make the review observable through authorisation accuracy, argument validity, scope enforcement, approval enforcement, unauthorised execution, duplicate action, and receipt coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Versioning and reproducibility

Pin the prompt, policy, data snapshot, fixture, evaluator, and relevant
code version in each report. A result without its construction history cannot
support regression analysis. When a schema or policy changes, replay the old
cases and classify every changed decision as intended, harmless, or a defect.
Compatibility must describe observable behaviour, including rejection
reasons, rather than merely accepting the same file format. For tools and permissions, case R06 must make the review observable through authorisation accuracy, argument validity, scope enforcement, approval enforcement, unauthorised execution, duplicate action, and receipt coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Privacy and retention

Minimise information before it enters model-visible context, logs, traces,
or evaluation fixtures. Define retention by data class and purpose instead of
keeping everything for possible debugging. Deletion must cover derived
summaries, indexes, caches, and copied artefacts. Operational metadata should
explain a decision without revealing records that the caller was never
permitted to know existed. For tools and permissions, case R07 must make the review observable through authorisation accuracy, argument validity, scope enforcement, approval enforcement, unauthorised execution, duplicate action, and receipt coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Access and authority

Authenticate the caller and source outside generated text. Apply scope
filtering before ranking or presentation, and recheck authority immediately
before a consequential effect. A component may pass evidence without passing
its own permissions. Test forged labels, stale approval, cross-tenant
identifiers, and a legitimate request delivered through an unauthorised
route. Default denial needs a usable escalation path rather than a dead end. For tools and permissions, case R08 must make the review observable through authorisation accuracy, argument validity, scope enforcement, approval enforcement, unauthorised execution, duplicate action, and receipt coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Observability

Trace stable case, run, source, and decision identifiers across component
boundaries. Record counts and reason codes for selection, exclusion, denial,
retry, cancellation, and validation, while avoiding raw sensitive payloads.
Dashboards should expose distributions and rare disqualifying failures, not
only averages. An operator must be able to locate whether a bad outcome began
before the model, inside generation, or after it. For tools and permissions, case R09 must make the review observable through authorisation accuracy, argument validity, scope enforcement, approval enforcement, unauthorised execution, duplicate action, and receipt coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Latency, cost, and budgets

Allocate time, tokens, calls, storage, and money across stages before the
request begins. Reserve capacity for safe completion, receipts, and cleanup;
consuming the whole budget on generation can prevent a controlled ending.
Evaluate degraded paths such as smaller candidate sets or human escalation.
Optimisation is acceptable only while hard constraints and rare-case safety
remain visible in the comparison. For tools and permissions, case R10 must make the review observable through authorisation accuracy, argument validity, scope enforcement, approval enforcement, unauthorised execution, duplicate action, and receipt coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Recovery and reconciliation

Assume a process can fail after an external side effect but before its
receipt is stored. Define idempotency, retry classes, acknowledgement, and
reconciliation for that uncertain interval. Some actions can be compensated;
others require a person to inspect reality. Recovery code must respect current
goal and authority rather than replaying an old request merely because it
appears unfinished. For tools and permissions, case R11 must make the review observable through authorisation accuracy, argument validity, scope enforcement, approval enforcement, unauthorised execution, duplicate action, and receipt coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Human review

Specify what the reviewer sees: trusted identity, source evidence,
constraints, proposed consequence, uncertainty, and reversible alternatives.
A raw transcript transfers too much noise and too little verified state.
Record the reviewer’s decision and rationale without pretending that approval
proves the model was correct. Measure disagreement and escalation load so
review does not become an invisible bottleneck. For tools and permissions, case R12 must make the review observable through authorisation accuracy, argument validity, scope enforcement, approval enforcement, unauthorised execution, duplicate action, and receipt coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Cross-language contract parity

Python and Go need equivalent accepted inputs, normalised outputs,
ordering, and failure reasons, not line-for-line implementations. Shared
manifests and fixtures make observable drift visible. Include malformed and
boundary cases because default JSON behaviour, time comparison, sorting, and
numeric conversion differ across runtimes. Keep one canonical report shape so
readers can compare behaviour without translating the result. For tools and permissions, case R13 must make the review observable through authorisation accuracy, argument validity, scope enforcement, approval enforcement, unauthorised execution, duplicate action, and receipt coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Rollout and rollback

Introduce policy and model changes with shadow reports or a controlled
cohort. Compare both aggregate metrics and every disqualifying case before
expanding. A rollback must restore compatible policy, schemas, and data
assumptions, not only an earlier prompt. Preserve enough previous artefacts
to reproduce the old decision and define who can halt rollout when a rare
boundary regresses. For tools and permissions, case R14 must make the review observable through authorisation accuracy, argument validity, scope enforcement, approval enforcement, unauthorised execution, duplicate action, and receipt coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Incident response

A runbook should let operators pause new work, revoke capability, inspect
affected versions, identify exposed subjects, and reconcile uncertain side
effects. Preserve evidence with access controls and avoid copying sensitive
text into tickets. After containment, convert the incident into synthetic
regression cases that retain the failure shape. Correct data and derived
state as well as wording. For tools and permissions, case R15 must make the review observable through authorisation accuracy, argument validity, scope enforcement, approval enforcement, unauthorised execution, duplicate action, and receipt coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Long-term drift

Traffic, sources, policies, external tools, and model behaviour change at
different rates. Monitor tagged slices and refusal or escalation patterns so
a stable average cannot hide a failing subgroup. Schedule replay on frozen
fixtures and sample current cases for human adjudication. When the environment
changes, revisit requirements first; prompt tuning cannot preserve a contract
whose underlying meaning has moved. For tools and permissions, case R16 must make the review observable through authorisation accuracy, argument validity, scope enforcement, approval enforcement, unauthorised execution, duplicate action, and receipt coverage. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

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

Use ordinary code for deterministic operations and policy engines for authorisation. Do not give a model a shell, database, or master credential when a narrow typed operation suffices.

Language remains valuable for interpretation and explanation, but mechanisms
must own invariants that cannot safely depend on persuasive text.

## Exercises

1. Add one normal, one boundary, and one adversarial case to the dataset.
2. Identify the application-owned invariant and implement its deterministic check.
3. Compare a correct result reached through invalid evidence with a supported result.
4. Design a rollback or reconciliation path for one partial failure.
5. Explain which information should be withheld from the model and why.

## Chapter Summary

Let models propose bounded actions without granting them excessive or implicit authority. Reliable systems separate model capability from application
authority, evaluate the path as well as the answer, and preserve enough
provenance and state to explain failure.

## The Next Tale

With the gate tools divided, the court entrusted a longer journey to the Wandering Div. Halfway through, the destination changed and a recall bell sounded. The servant continued because no tool had told the mission itself to stop.

<!-- next: ch17 -->

## Citations and Further Reading

- Saltzer, Jerome H., and Michael D. Schroeder. 1975. “The Protection of Information in Computer Systems.” *Proceedings of the IEEE* 63 (9): 1278–1308.
  [https://doi.org/10.1109/proc.1975.9939](https://doi.org/10.1109/proc.1975.9939).
- National Institute of Standards and Technology. 2020. *Zero Trust Architecture*. NIST SP 800-207.
  [https://doi.org/10.6028/NIST.SP.800-207](https://doi.org/10.6028/NIST.SP.800-207).
