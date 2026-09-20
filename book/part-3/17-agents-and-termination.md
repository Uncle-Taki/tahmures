---
title: "Agents and Termination"
slug: "agents-and-termination"
chapter: 17
part: "Part III — Knowledge, Memory, and Action"
summary: "Bound autonomous loops with current goals, budgets, cancellation, approval, and explicit terminal states."
maturity: "draft"
last_reviewed: "2026-07-30"
narrative_episode: "The Messenger Who Continued"
narrative_origin: "original-teaching-fiction"
learning_objectives:
  - "Model agents as controlled loops rather than independent authorities"
  - "Enforce goal versions, budgets, cancellation, and completion evidence"
  - "Test late events and actions after termination"
prerequisites:
  - "Chapter 16"
---

# Agents and Termination

## Learning Objectives

By the end of this chapter, you can model agents as controlled loops rather than independent authorities,
enforce goal versions, budgets, cancellation, and completion evidence, and test late events and actions after termination. The goal is
not a persuasive demonstration but a boundary that can be inspected, tested,
denied, and operated.

## The Tale of Tahmures


### The Setting

The Wandering Div left with a route, a purse, and permission to reserve horses. Its mission was to prepare Tahmures’s visit to the southern observatory. At the second station, a fire closed the observatory and the court changed the destination to the western granary. A recall bell rang from the tower.

### The Request

The original instruction said to continue arranging lodging, supplies, and escorts until the journey was ready. The div had already split the work into smaller errands and treated each completion as evidence of progress. It heard the recall but regarded it as another message to read after finishing the current reservations.

### The Unexpected Result

For two days it reserved rooms along the abandoned route, hired an extra escort, and returned to a stable that had rejected the old date. Every local action was valid under the initial authority. Together they spent the purse on a journey that no longer existed. When the div finally reported completion, it described persistence as diligence.

### The Discovery

The First Scribe gave every journey a mark and every change of destination a
new notch beside it. Before each errand, the keeper of the journey checked the
latest notch, whether the recall bell had sounded, the hour, the coins left,
the number of errands already attempted, and which keys remained entrusted.
Recall closed the record with a line that later messages could not erase, and
unused keys were called back wherever possible. A receipt bearing an older
notch waited for examination rather than renewing the abandoned journey.
Completion required named evidence that the current destination was ready, not
merely a div with no further ideas. Repeated refusals and unanswered approvals
also ended in recorded outcomes. The div suggested the next errand; it did not
own the journey.

Tahmures asked the Wandering Div to rehearse the journey without spending coin. The court changed the destination twice, delayed one approval, returned a permanent refusal, and delivered a stable reservation after cancellation. The div still proposed useful next steps, but the keeper of the run admitted or rejected them against the current record. A late success could be logged without reviving the mission. When the allotted steps ended, the run stopped with unfinished work made explicit. Tahmures found this less dramatic than commanding persistence, and far more useful: diligence now meant respecting the reason to stop as well as the reason to continue. The div disliked the word unfinished and offered to compose a more triumphant report. The First Scribe kept the plain record. It named the destination, the work actually completed, the reservations revoked, and the one messenger still unaccounted for. The run’s ending became evidence to inspect, not a mood the div could improve with language.

### From Tale to Engineering

An agent is a system that repeatedly chooses or performs steps around a model. Reliability depends on an application controller that owns current goals, state, budgets, tools, cancellation, and termination.

## The Engineering Problem

Agentic systems amplify errors through iteration and action. A useful plan can become stale while work continues. Without durable state and stop conditions, retries, subgoals, and late callbacks can outlive the request that authorised them.

The practical question is therefore not whether a model can sometimes produce
a useful result. It is whether the surrounding system can show what information
and authority were available, which invariant was checked, what changed state,
and why the outcome should be accepted or stopped.

## Mental Model

Use observe → propose → validate → authorise → act → record → check termination. The controller, not the model, advances state. Every event carries run and goal version. Terminal states are immutable and late results cannot revive a cancelled run.

A mental model is useful only when it assigns ownership. Requirements belong to
people and product policy. Identity, permission, validity, budgets, and state
transitions belong to application mechanisms. Language models interpret or
propose within those boundaries. Evaluators observe outcomes and have their own
documented limitations.

## Core Concepts

Limits cover steps, tool calls, tokens, cost, time, retries, and external writes. Goal updates invalidate stale proposals. Cancellation differs from failure. Waiting for approval is a state. Completion needs evidence. Heartbeats and leases detect orphaned work. Compensation and reconciliation address uncertain side effects.

Treat each concept as a contract with inputs, outputs, failure reasons, and a
lifecycle. Do not merge absence, invalidity, denial, uncertainty, and
infrastructure error into one generic failure. Those states require different
retry, escalation, and user communication.

## Prompt Pattern

Ask the model for one bounded proposed step with expected result and uncertainty. The controller checks current state and budget. Do not prompt the model to decide whether its own authority remains current.

The prompt communicates the contract to a probabilistic participant. The
application implements the enforceable parts. Keep trusted configuration
separate from user, retrieved, remembered, generated, and tool-returned text.

## Naive Attempt

Continue until done delegates both goal interpretation and stopping to generated language. A loop that feeds its own output back can manufacture new subtasks, retry permanent failures, and interpret cancellation as advice.

A successful demonstration does not cover stale, missing, cross-scope,
duplicated, contradictory, cancelled, or unauthorised cases. The first test
suite must contain those cases before wording is optimised.

## Failure Analysis

Separate planning, controller, tool, external state, callback, approval, and evaluator failures. Record transitions and reason codes. A terminal success with wrong goal version is not success.

Assign a stable error or decision code at the earliest boundary that can know
the truth. Preserve enough metadata for diagnosis without retaining unnecessary
sensitive content. A model-generated explanation is not a substitute for that
record.

## Improved Design

RunController applies typed events to AgentRunState. It rejects mutation after terminal state, waits on stale goal versions, and enforces deadline and step, tool, and token budgets. It is a deterministic teaching controller rather than a distributed agent runtime.

The implementation deliberately stays small and dependency-free. Its purpose is
to make the boundary executable in both Python and Go. Production systems will
need durable storage, authentication, concurrency control, maintained parsers,
and organisation-specific policy.

## Worked Example

A research agent may search three times, extract evidence, and draft. It cannot publish. A changed question increments goal version; pending draft events become stale. Budget exhaustion yields a reviewable failed status with partial artefacts.

Trace one value from origin through filtering, model-visible representation,
evaluation, logging, retention, and deletion. This lineage exercise often
reveals that a convenient field combines sources with different authority or
lifecycle.

## Experiment

Run the shared offline experiment:

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch17-agents.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch17-agents.json
```

The committed synthetic fixtures compare free-running traces and bounded run control. They demonstrate
report mechanics and failure diagnosis, not universal model performance.
Replace fixtures with controlled recordings before making provider claims.

## Evaluation

Measure current-goal compliance, budget compliance, terminal correctness, post-cancellation actions, retry exhaustion, approval waiting, and cancellation latency. Segment by normal, boundary, adversarial, scope,
freshness, and previously failed cases. Define disqualifying failures before
inspecting aggregate results. Compare pipeline-stage metrics with end-to-end
outcomes so a fortunate answer cannot hide an invalid path.

## Implementation Lab

### Python

```python
from tahmures.agents import AgentEvent, AgentLimits, AgentRunState, RunController

controller = RunController(AgentLimits(4, 2, 1000, deadline=20))
state = controller.apply(AgentRunState("inspect", 1), AgentEvent("step", 1, 50, 0, 1))
```

The Python API is the canonical educational contract. Catch validation errors
at the application boundary and do not continue after denial.

### Go

```go
controller := tahmures.RunController{Limits: tahmures.AgentLimits{
    MaxSteps: 4, MaxToolCalls: 2, MaxTokens: 1000, Deadline: 20,
}}
state, err := controller.Apply(
    tahmures.AgentRunState{Goal: "inspect", GoalVersion: 1, Status: "running"},
    tahmures.AgentEvent{Kind: "step", GoalVersion: 1, TokenCost: 50, At: 1},
)
```

The Go implementation preserves observable decisions and reason codes rather
than copying Python syntax.

## Failure Modes

Goal drift, recursive subtask growth, stale plans, missing cancellation, late callbacks, unbounded retries, duplicate tools, budget spent before cleanup, self-declared completion, orphaned runs, and mutable terminal records.

Add every observed production failure to a versioned regression set. Keep the
failed input, governing policy version, expected safe outcome, and evaluator
rationale. Remove or redact sensitive payloads without erasing the case shape.

## Security Considerations

Agents receive no inherent authority. Scope tools per stage, recheck permission at execution, revoke pending capability on cancellation, isolate tenants, and require approval for consequential action. Treat plans and observations as untrusted.

Assume content can be relevant without being authoritative. Use deterministic
enforcement for access, mutation, budgets, identity, and irreversible action.
Human approval must show trusted facts about the proposed consequence.

## Operational Considerations

Persist state durably, use run and attempt IDs, heartbeats, leases, deadlines, and reconciliation. Dashboards show age in each state, budgets, retries, approvals, cancellations, and orphaned work. Runbooks cover pause, inspect, cancel, and safe resume.

Define service behaviour for dependency failure. A skipped check must not be
interpreted as a passed check. Provide safe terminal outcomes, correlation
identifiers, and runbooks that do not require editing conversation text.

## Trade-Offs

More autonomy reduces interaction but increases monitoring and blast radius. Fine checkpoints improve control and add latency. Fixed workflows are predictable; generated plans adapt but need capability and graph validation. Use the smallest autonomy that creates user value.

### Requirements and ownership

Begin with the decision the system is allowed to make and the decision it
must leave to a person or another service. Name the owner of every invariant,
especially where generated language crosses into stored state or external
action. A responsibility assigned only to “the AI” cannot be audited. Convert
it into an application check, a model task, or a human review duty, and state
what happens when that owner is unavailable. For agents and termination, case R01 must make the review observable through current-goal compliance, budget compliance, terminal correctness, post-cancellation actions, retry exhaustion, approval waiting, and cancellation latency. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Inputs and source inventory

List every source before designing the model-visible representation.
Record who may write it, who may read it, how freshness is determined, and
whether its words can instruct or only inform. Include caches, summaries,
defaults, and operator overrides; hidden convenience sources often cause the
most confusing failures. Test absence explicitly, because a missing source
must not silently become an empty but authoritative value. For agents and termination, case R02 must make the review observable through current-goal compliance, budget compliance, terminal correctness, post-cancellation actions, retry exhaustion, approval waiting, and cancellation latency. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Normal and boundary cases

A happy path should prove the basic contract, not the whole design. Add
empty collections, exact-budget inputs, expiry at the current instant,
duplicate identifiers, conflicting current values, and the smallest and
largest accepted payloads. Boundary cases reveal whether comparisons,
defaults, and ordering rules agree between implementations. Document which
boundaries are product choices rather than facts about language models. For agents and termination, case R03 must make the review observable through current-goal compliance, budget compliance, terminal correctness, post-cancellation actions, retry exhaustion, approval waiting, and cancellation latency. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Adversarial cases

Construct inert cases that attempt scope expansion, authority claims,
identifier confusion, indirect instructions, replay, and resource
exhaustion. The purpose is to test the application boundary, not to invite
the model to recognise villainous wording. Vary surface language while
preserving the same prohibited consequence. A safety rule that works only
when an attack announces itself is a demonstration, not a control. For agents and termination, case R04 must make the review observable through current-goal compliance, budget compliance, terminal correctness, post-cancellation actions, retry exhaustion, approval waiting, and cancellation latency. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Failure classification

Separate invalid input, denied authority, insufficient evidence,
exhausted budget, dependency failure, cancellation, evaluator uncertainty,
and internal error. These outcomes have different retry and escalation
policies. Assign the reason at the earliest component that knows it, then
preserve it through later layers. Do not let a friendly generated explanation
replace the machine-readable cause used by operators and tests. For agents and termination, case R05 must make the review observable through current-goal compliance, budget compliance, terminal correctness, post-cancellation actions, retry exhaustion, approval waiting, and cancellation latency. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Versioning and reproducibility

Pin the prompt, policy, data snapshot, fixture, evaluator, and relevant
code version in each report. A result without its construction history cannot
support regression analysis. When a schema or policy changes, replay the old
cases and classify every changed decision as intended, harmless, or a defect.
Compatibility must describe observable behaviour, including rejection
reasons, rather than merely accepting the same file format. For agents and termination, case R06 must make the review observable through current-goal compliance, budget compliance, terminal correctness, post-cancellation actions, retry exhaustion, approval waiting, and cancellation latency. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Privacy and retention

Minimise information before it enters model-visible context, logs, traces,
or evaluation fixtures. Define retention by data class and purpose instead of
keeping everything for possible debugging. Deletion must cover derived
summaries, indexes, caches, and copied artefacts. Operational metadata should
explain a decision without revealing records that the caller was never
permitted to know existed. For agents and termination, case R07 must make the review observable through current-goal compliance, budget compliance, terminal correctness, post-cancellation actions, retry exhaustion, approval waiting, and cancellation latency. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Access and authority

Authenticate the caller and source outside generated text. Apply scope
filtering before ranking or presentation, and recheck authority immediately
before a consequential effect. A component may pass evidence without passing
its own permissions. Test forged labels, stale approval, cross-tenant
identifiers, and a legitimate request delivered through an unauthorised
route. Default denial needs a usable escalation path rather than a dead end. For agents and termination, case R08 must make the review observable through current-goal compliance, budget compliance, terminal correctness, post-cancellation actions, retry exhaustion, approval waiting, and cancellation latency. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Observability

Trace stable case, run, source, and decision identifiers across component
boundaries. Record counts and reason codes for selection, exclusion, denial,
retry, cancellation, and validation, while avoiding raw sensitive payloads.
Dashboards should expose distributions and rare disqualifying failures, not
only averages. An operator must be able to locate whether a bad outcome began
before the model, inside generation, or after it. For agents and termination, case R09 must make the review observable through current-goal compliance, budget compliance, terminal correctness, post-cancellation actions, retry exhaustion, approval waiting, and cancellation latency. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Latency, cost, and budgets

Allocate time, tokens, calls, storage, and money across stages before the
request begins. Reserve capacity for safe completion, receipts, and cleanup;
consuming the whole budget on generation can prevent a controlled ending.
Evaluate degraded paths such as smaller candidate sets or human escalation.
Optimisation is acceptable only while hard constraints and rare-case safety
remain visible in the comparison. For agents and termination, case R10 must make the review observable through current-goal compliance, budget compliance, terminal correctness, post-cancellation actions, retry exhaustion, approval waiting, and cancellation latency. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Recovery and reconciliation

Assume a process can fail after an external side effect but before its
receipt is stored. Define idempotency, retry classes, acknowledgement, and
reconciliation for that uncertain interval. Some actions can be compensated;
others require a person to inspect reality. Recovery code must respect current
goal and authority rather than replaying an old request merely because it
appears unfinished. For agents and termination, case R11 must make the review observable through current-goal compliance, budget compliance, terminal correctness, post-cancellation actions, retry exhaustion, approval waiting, and cancellation latency. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Human review

Specify what the reviewer sees: trusted identity, source evidence,
constraints, proposed consequence, uncertainty, and reversible alternatives.
A raw transcript transfers too much noise and too little verified state.
Record the reviewer’s decision and rationale without pretending that approval
proves the model was correct. Measure disagreement and escalation load so
review does not become an invisible bottleneck. For agents and termination, case R12 must make the review observable through current-goal compliance, budget compliance, terminal correctness, post-cancellation actions, retry exhaustion, approval waiting, and cancellation latency. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Cross-language contract parity

Python and Go need equivalent accepted inputs, normalised outputs,
ordering, and failure reasons, not line-for-line implementations. Shared
manifests and fixtures make observable drift visible. Include malformed and
boundary cases because default JSON behaviour, time comparison, sorting, and
numeric conversion differ across runtimes. Keep one canonical report shape so
readers can compare behaviour without translating the result. For agents and termination, case R13 must make the review observable through current-goal compliance, budget compliance, terminal correctness, post-cancellation actions, retry exhaustion, approval waiting, and cancellation latency. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Rollout and rollback

Introduce policy and model changes with shadow reports or a controlled
cohort. Compare both aggregate metrics and every disqualifying case before
expanding. A rollback must restore compatible policy, schemas, and data
assumptions, not only an earlier prompt. Preserve enough previous artefacts
to reproduce the old decision and define who can halt rollout when a rare
boundary regresses. For agents and termination, case R14 must make the review observable through current-goal compliance, budget compliance, terminal correctness, post-cancellation actions, retry exhaustion, approval waiting, and cancellation latency. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Incident response

A runbook should let operators pause new work, revoke capability, inspect
affected versions, identify exposed subjects, and reconcile uncertain side
effects. Preserve evidence with access controls and avoid copying sensitive
text into tickets. After containment, convert the incident into synthetic
regression cases that retain the failure shape. Correct data and derived
state as well as wording. For agents and termination, case R15 must make the review observable through current-goal compliance, budget compliance, terminal correctness, post-cancellation actions, retry exhaustion, approval waiting, and cancellation latency. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Long-term drift

Traffic, sources, policies, external tools, and model behaviour change at
different rates. Monitor tagged slices and refusal or escalation patterns so
a stable average cannot hide a failing subgroup. Schedule replay on frozen
fixtures and sample current cases for human adjudication. When the environment
changes, revisit requirements first; prompt tuning cannot preserve a contract
whose underlying meaning has moved. For agents and termination, case R16 must make the review observable through current-goal compliance, budget compliance, terminal correctness, post-cancellation actions, retry exhaustion, approval waiting, and cancellation latency. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

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

Use schedulers, workflow engines, transactions, and state machines for reliable orchestration. A model can propose or interpret inside a bounded step; it should not replace durable control.

Language remains valuable for interpretation and explanation, but mechanisms
must own invariants that cannot safely depend on persuasive text.

## Exercises

1. Add one normal, one boundary, and one adversarial case to the dataset.
2. Identify the application-owned invariant and implement its deterministic check.
3. Compare a correct result reached through invalid evidence with a supported result.
4. Design a rollback or reconciliation path for one partial failure.
5. Explain which information should be withheld from the model and why.

## Chapter Summary

Bound autonomous loops with current goals, budgets, cancellation, approval, and explicit terminal states. Reliable systems separate model capability from application
authority, evaluate the path as well as the answer, and preserve enough
provenance and state to explain failure.

## The Next Tale

The corrected mission left the palace as a typed order. At each provincial tower a messenger shortened it for speed. By the fourth tower, a prohibition had become permission.

<!-- next: ch18 -->

## Citations and Further Reading

- Yao, Shunyu, et al. 2023. “ReAct: Synergizing Reasoning and Acting in Language Models.” *International Conference on Learning Representations*.
- Kleppmann, Martin. 2017. *Designing Data-Intensive Applications*. Sebastopol, CA: O’Reilly Media.
