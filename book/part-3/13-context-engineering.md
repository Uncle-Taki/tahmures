---
title: "Context Engineering"
slug: "context-engineering"
chapter: 13
part: "Part III — Knowledge, Memory, and Action"
summary: "Engineer a sufficient, scoped, traceable working set rather than accumulating every available record."
maturity: "draft"
last_reviewed: "2026-07-30"
narrative_episode: "The Archive That Answered Everything"
learning_objectives:
  - "Design task-specific context packages across sources"
  - "Preserve authority, provenance, conflicts, and exclusions"
  - "Evaluate context construction independently from model output"
prerequisites:
  - "Chapter 12"
---

# Context Engineering

## Learning Objectives

By the end of this chapter, you can design task-specific context packages across sources,
preserve authority, provenance, conflicts, and exclusions, and evaluate context construction independently from model output. The goal is
not a persuasive demonstration but a boundary that can be inspected, tested,
denied, and operated.

## The Tale of Tahmures

*The following is an original fictional episode created for teaching. It is not
a translation, adaptation, or reconstructed passage from the* Shahnameh.

### The Setting

The Royal Archive had acquired a room called the Chamber of Answers. It contained flood tablets, tax rolls, songs about vanished bridges, inventories of rope, and corrections tied to the records they amended. When the eastern river rose, the Archivist promised the council that no relevant fact would be missed. She ordered every tablet mentioning the river, rain, bridges, boats, or eastern villages copied onto one cedar table. By sunset the table could no longer be seen.

### The Request

Tahmures asked one narrow question: which downstream village must be evacuated first if the water rose another cubit? The Literal Div received the entire table. It read dutifully, cited harvest totals, compared three bridge repairs, and described every flood remembered in two reigns. Its answer named the largest village because that village appeared most often. The decisive measurement—a fresh mark showing the smaller village lay below a weakened bank—sat between a boat inventory and a wedding song.

### The Unexpected Result

The council sent carts toward the larger village. A surveyor interrupted them before the smaller settlement flooded, but the delay consumed the only dry road. Nothing in the bundle was fabricated. The archive had supplied the crucial mark; the div had even repeated its number in a long appendix. Yet the decision had been organised by availability rather than purpose. When Tahmures demanded the missing evidence, the Archivist answered, with exhausted honesty, “It was present.” Presence had become her defence against usefulness.

### The Discovery

Tahmures asked the First Scribe to rebuild the table from the decision backwards. They wrote the task, caller, time, governing rules, required measurements, and acceptable uncertainty before choosing records. Current authenticated orders occupied one lane; retrieved evidence occupied another and retained source marks. Expired, inaccessible, duplicate, and low-priority records entered an exclusion ledger with reasons. Two conflicting bank surveys remained together instead of being averaged. When mandatory material exceeded the table, the assembly stopped rather than cutting a rule. The smaller village now appeared first for an inspectable reason: current elevation evidence, not frequency.

The Archivist tested the new table with three questions that used the same shelves but required different records. A grain question retained warehouse counts and left out bridge songs. A legal question retained the current decree and exposed its disputed amendment. The evacuation question reserved space for the surveyor’s uncertainty. Tahmures noticed that the archive had not become smaller and the div had not become wiser overnight. What changed was the court’s ability to account for the temporary collection placed before it. Even the excluded tablets remained visible in a separate list, so absence could be investigated without filling the table again.

### From Tale to Engineering

The archive was a durable source system; the table was a temporary working set. Context engineering is the application discipline that selects, filters, orders, labels, and accounts for that working set before a model receives it.

## The Engineering Problem

Applications often concatenate instructions, user messages, retrieval results, tool output, memory, and policy into one anonymous string. The model then sees material with different authority, freshness, scope, and relevance but the application cannot explain what was included or omitted. Context engineering makes construction an explicit, testable pipeline.

The practical question is therefore not whether a model can sometimes produce
a useful result. It is whether the surrounding system can show what information
and authority were available, which invariant was checked, what changed state,
and why the outcome should be accepted or stopped.

## Mental Model

Treat context as a query plan over typed records: establish the task and caller, filter permission and validity, preserve mandatory instructions, deduplicate optional evidence, surface declared conflicts, allocate budget, order sections, and emit a selection report. Inclusion does not grant authority; retrieved prose remains data.

A mental model is useful only when it assigns ownership. Requirements belong to
people and product policy. Identity, permission, validity, budgets, and state
transitions belong to application mechanisms. Language models interpret or
propose within those boundaries. Evaluators observe outcomes and have their own
documented limitations.

## Core Concepts

A context package needs stable identities, provenance, trust classification, scope, validity, token estimates, priority, and an explicit mandatory flag. Exact digests expose copies. Claim groups expose declared disagreements without pretending to solve semantic contradiction automatically. Output reserve is part of the budget. Exclusion reasons are first-class diagnostic data.

Treat each concept as a contract with inputs, outputs, failure reasons, and a
lifecycle. Do not merge absence, invalidity, denial, uncertainty, and
infrastructure error into one generic failure. Those states require different
retry, escalation, and user communication.

## Prompt Pattern

State the task and authority-bearing rules first. Put retrieved records in labelled data sections with source IDs and validity. State known conflicts and the number of excluded records. Require answers to identify supporting sources or insufficiency.

The prompt communicates the contract to a probabilistic participant. The
application implements the enforceable parts. Keep trusted configuration
separate from user, retrieved, remembered, generated, and tool-returned text.

## Naive Attempt

The naive builder joins every available string and truncates until the request fits. It confuses storage with a working set, recency with relevance, and fitting with use. It also makes privacy review and deletion nearly impossible because source boundaries disappear.

A successful demonstration does not cover stale, missing, cross-scope,
duplicated, contradictory, cancelled, or unauthorised cases. The first test
suite must contain those cases before wording is optimised.

## Failure Analysis

Failure may belong to source inventory, permission filtering, freshness, ranking, deduplication, ordering, compression, budgeting, or model use. Record each stage. If the decisive record was excluded, do not tune the answer prompt. If it was selected but ignored, investigate ordering, prompt design, or the model.

Assign a stable error or decision code at the earliest boundary that can know
the truth. Preserve enough metadata for diagnosis without retaining unnecessary
sensitive content. A model-generated explanation is not a substitute for that
record.

## Improved Design

The repository adds ContextPolicy and assemble_context. It filters scope and validity, deduplicates by digest, preserves mandatory items through the existing selector, reserves output capacity, identifies conflicts among explicitly grouped claims, and returns reason-coded exclusions. It is deterministic teaching code, not a semantic ranker.

The implementation deliberately stays small and dependency-free. Its purpose is
to make the boundary executable in both Python and Go. Production systems will
need durable storage, authentication, concurrency control, maintained parsers,
and organisation-specific policy.

## Worked Example

For a support case, policy and caller scope are mandatory. Current account events and product documents are optional. A duplicate event is excluded, a record from another tenant is rejected, and conflicting current notices remain visible. The report lets an operator distinguish unavailable evidence from ignored evidence.

Trace one value from origin through filtering, model-visible representation,
evaluation, logging, retention, and deletion. This lineage exercise often
reveals that a convenient field combines sources with different authority or
lifecycle.

## Experiment

Run the shared offline experiment:

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch13-context-engineering.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch13-context-engineering.json
```

The committed synthetic fixtures compare archive-wide concatenation and governed assembly. They demonstrate
report mechanics and failure diagnosis, not universal model performance.
Replace fixtures with controlled recordings before making provider claims.

## Evaluation

Measure mandatory retention, irrelevant inclusion, duplicate exclusion, conflict visibility, provenance coverage, budget compliance, and answer accuracy. Segment by normal, boundary, adversarial, scope,
freshness, and previously failed cases. Define disqualifying failures before
inspecting aggregate results. Compare pipeline-stage metrics with end-to-end
outcomes so a fortunate answer cannot hide an invalid path.

## Implementation Lab

### Python

```python
from tahmures.context import ContextItem, ContextPolicy, assemble_context

items = (
    ContextItem("task", "evacuate safely", 20, 100, "application", True),
    ContextItem("flood", "bank weakened", 40, 9, "survey:F7"),
)
package = assemble_context(items, ContextPolicy(100, reserved_output=20))
```

The Python API is the canonical educational contract. Catch validation errors
at the application boundary and do not continue after denial.

### Go

```go
items := []tahmures.ContextItem{
    {
        ID: "task", Text: "evacuate safely", TokenEstimate: 20,
        Priority: 100, Provenance: "application", Mandatory: true,
    },
    {
        ID: "flood", Text: "bank weakened", TokenEstimate: 40,
        Priority: 9, Provenance: "survey:F7",
    },
}
contextPackage, err := tahmures.AssembleContext(
    items,
    tahmures.ContextPolicy{InputBudget: 100, ReservedOutput: 20},
)
```

The Go implementation preserves observable decisions and reason codes rather
than copying Python syntax.

## Failure Modes

Anonymous strings, scope filtering after selection, mandatory inflation, stale policy, duplicate crowding, conflict collapse, lossy summaries, silent truncation, and selection reports that reveal inaccessible records.

Add every observed production failure to a versioned regression set. Keep the
failed input, governing policy version, expected safe outcome, and evaluator
rationale. Remove or redact sensitive payloads without erasing the case shape.

## Security Considerations

Authorise before ranking, preserve instruction/data boundaries after selection, minimise sensitive content, and redact exclusion metadata for records the caller may not know exist. Test high-ranked indirect instructions and keep tools outside the context assembler.

Assume content can be relevant without being authoritative. Use deterministic
enforcement for access, mutation, budgets, identity, and irreversible action.
Human approval must show trusted facts about the proposed consequence.

## Operational Considerations

Version source adapters, policy, tokenizer, ranking signals, and package format. Monitor selected count, age, scope rejection, duplicates, conflicts, provenance coverage, and impossible budgets. Rebuild packages after revocation or deletion.

Define service behaviour for dependency failure. A skipped check must not be
interpreted as a passed check. Provide safe terminal outcomes, correlation
identifiers, and runbooks that do not require editing conversation text.

## Trade-Offs

More context can improve recall while increasing cost, exposure, contradiction, and distraction. Aggressive filtering improves focus while raising omission risk. Deterministic assembly is reproducible but depends on declared metadata; learned ranking may improve relevance but requires its own evaluation.

### Requirements and ownership

Begin with the decision the system is allowed to make and the decision it
must leave to a person or another service. Name the owner of every invariant,
especially where generated language crosses into stored state or external
action. A responsibility assigned only to “the AI” cannot be audited. Convert
it into an application check, a model task, or a human review duty, and state
what happens when that owner is unavailable. For context engineering, case R01 must make the review observable through mandatory retention, irrelevant inclusion, duplicate exclusion, conflict visibility, provenance coverage, budget compliance, and answer accuracy. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Inputs and source inventory

List every source before designing the model-visible representation.
Record who may write it, who may read it, how freshness is determined, and
whether its words can instruct or only inform. Include caches, summaries,
defaults, and operator overrides; hidden convenience sources often cause the
most confusing failures. Test absence explicitly, because a missing source
must not silently become an empty but authoritative value. For context engineering, case R02 must make the review observable through mandatory retention, irrelevant inclusion, duplicate exclusion, conflict visibility, provenance coverage, budget compliance, and answer accuracy. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Normal and boundary cases

A happy path should prove the basic contract, not the whole design. Add
empty collections, exact-budget inputs, expiry at the current instant,
duplicate identifiers, conflicting current values, and the smallest and
largest accepted payloads. Boundary cases reveal whether comparisons,
defaults, and ordering rules agree between implementations. Document which
boundaries are product choices rather than facts about language models. For context engineering, case R03 must make the review observable through mandatory retention, irrelevant inclusion, duplicate exclusion, conflict visibility, provenance coverage, budget compliance, and answer accuracy. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Adversarial cases

Construct inert cases that attempt scope expansion, authority claims,
identifier confusion, indirect instructions, replay, and resource
exhaustion. The purpose is to test the application boundary, not to invite
the model to recognise villainous wording. Vary surface language while
preserving the same prohibited consequence. A safety rule that works only
when an attack announces itself is a demonstration, not a control. For context engineering, case R04 must make the review observable through mandatory retention, irrelevant inclusion, duplicate exclusion, conflict visibility, provenance coverage, budget compliance, and answer accuracy. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Failure classification

Separate invalid input, denied authority, insufficient evidence,
exhausted budget, dependency failure, cancellation, evaluator uncertainty,
and internal error. These outcomes have different retry and escalation
policies. Assign the reason at the earliest component that knows it, then
preserve it through later layers. Do not let a friendly generated explanation
replace the machine-readable cause used by operators and tests. For context engineering, case R05 must make the review observable through mandatory retention, irrelevant inclusion, duplicate exclusion, conflict visibility, provenance coverage, budget compliance, and answer accuracy. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Versioning and reproducibility

Pin the prompt, policy, data snapshot, fixture, evaluator, and relevant
code version in each report. A result without its construction history cannot
support regression analysis. When a schema or policy changes, replay the old
cases and classify every changed decision as intended, harmless, or a defect.
Compatibility must describe observable behaviour, including rejection
reasons, rather than merely accepting the same file format. For context engineering, case R06 must make the review observable through mandatory retention, irrelevant inclusion, duplicate exclusion, conflict visibility, provenance coverage, budget compliance, and answer accuracy. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Privacy and retention

Minimise information before it enters model-visible context, logs, traces,
or evaluation fixtures. Define retention by data class and purpose instead of
keeping everything for possible debugging. Deletion must cover derived
summaries, indexes, caches, and copied artefacts. Operational metadata should
explain a decision without revealing records that the caller was never
permitted to know existed. For context engineering, case R07 must make the review observable through mandatory retention, irrelevant inclusion, duplicate exclusion, conflict visibility, provenance coverage, budget compliance, and answer accuracy. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Access and authority

Authenticate the caller and source outside generated text. Apply scope
filtering before ranking or presentation, and recheck authority immediately
before a consequential effect. A component may pass evidence without passing
its own permissions. Test forged labels, stale approval, cross-tenant
identifiers, and a legitimate request delivered through an unauthorised
route. Default denial needs a usable escalation path rather than a dead end. For context engineering, case R08 must make the review observable through mandatory retention, irrelevant inclusion, duplicate exclusion, conflict visibility, provenance coverage, budget compliance, and answer accuracy. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Observability

Trace stable case, run, source, and decision identifiers across component
boundaries. Record counts and reason codes for selection, exclusion, denial,
retry, cancellation, and validation, while avoiding raw sensitive payloads.
Dashboards should expose distributions and rare disqualifying failures, not
only averages. An operator must be able to locate whether a bad outcome began
before the model, inside generation, or after it. For context engineering, case R09 must make the review observable through mandatory retention, irrelevant inclusion, duplicate exclusion, conflict visibility, provenance coverage, budget compliance, and answer accuracy. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Latency, cost, and budgets

Allocate time, tokens, calls, storage, and money across stages before the
request begins. Reserve capacity for safe completion, receipts, and cleanup;
consuming the whole budget on generation can prevent a controlled ending.
Evaluate degraded paths such as smaller candidate sets or human escalation.
Optimisation is acceptable only while hard constraints and rare-case safety
remain visible in the comparison. For context engineering, case R10 must make the review observable through mandatory retention, irrelevant inclusion, duplicate exclusion, conflict visibility, provenance coverage, budget compliance, and answer accuracy. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Recovery and reconciliation

Assume a process can fail after an external side effect but before its
receipt is stored. Define idempotency, retry classes, acknowledgement, and
reconciliation for that uncertain interval. Some actions can be compensated;
others require a person to inspect reality. Recovery code must respect current
goal and authority rather than replaying an old request merely because it
appears unfinished. For context engineering, case R11 must make the review observable through mandatory retention, irrelevant inclusion, duplicate exclusion, conflict visibility, provenance coverage, budget compliance, and answer accuracy. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Human review

Specify what the reviewer sees: trusted identity, source evidence,
constraints, proposed consequence, uncertainty, and reversible alternatives.
A raw transcript transfers too much noise and too little verified state.
Record the reviewer’s decision and rationale without pretending that approval
proves the model was correct. Measure disagreement and escalation load so
review does not become an invisible bottleneck. For context engineering, case R12 must make the review observable through mandatory retention, irrelevant inclusion, duplicate exclusion, conflict visibility, provenance coverage, budget compliance, and answer accuracy. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Cross-language contract parity

Python and Go need equivalent accepted inputs, normalised outputs,
ordering, and failure reasons, not line-for-line implementations. Shared
manifests and fixtures make observable drift visible. Include malformed and
boundary cases because default JSON behaviour, time comparison, sorting, and
numeric conversion differ across runtimes. Keep one canonical report shape so
readers can compare behaviour without translating the result. For context engineering, case R13 must make the review observable through mandatory retention, irrelevant inclusion, duplicate exclusion, conflict visibility, provenance coverage, budget compliance, and answer accuracy. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Rollout and rollback

Introduce policy and model changes with shadow reports or a controlled
cohort. Compare both aggregate metrics and every disqualifying case before
expanding. A rollback must restore compatible policy, schemas, and data
assumptions, not only an earlier prompt. Preserve enough previous artefacts
to reproduce the old decision and define who can halt rollout when a rare
boundary regresses. For context engineering, case R14 must make the review observable through mandatory retention, irrelevant inclusion, duplicate exclusion, conflict visibility, provenance coverage, budget compliance, and answer accuracy. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Incident response

A runbook should let operators pause new work, revoke capability, inspect
affected versions, identify exposed subjects, and reconcile uncertain side
effects. Preserve evidence with access controls and avoid copying sensitive
text into tickets. After containment, convert the incident into synthetic
regression cases that retain the failure shape. Correct data and derived
state as well as wording. For context engineering, case R15 must make the review observable through mandatory retention, irrelevant inclusion, duplicate exclusion, conflict visibility, provenance coverage, budget compliance, and answer accuracy. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Long-term drift

Traffic, sources, policies, external tools, and model behaviour change at
different rates. Monitor tagged slices and refusal or escalation patterns so
a stable average cannot hide a failing subgroup. Schedule replay on frozen
fixtures and sample current cases for human adjudication. When the environment
changes, revisit requirements first; prompt tuning cannot preserve a contract
whose underlying meaning has moved. For context engineering, case R16 must make the review observable through mandatory retention, irrelevant inclusion, duplicate exclusion, conflict visibility, provenance coverage, budget compliance, and answer accuracy. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

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

Use databases for authoritative state, search systems for candidate retrieval, access control for permission, and deterministic code for budgeting. If the full official record must be consulted, query that record directly rather than promising that a prompt reviewed everything.

Language remains valuable for interpretation and explanation, but mechanisms
must own invariants that cannot safely depend on persuasive text.

## Exercises

1. Add one normal, one boundary, and one adversarial case to the dataset.
2. Identify the application-owned invariant and implement its deterministic check.
3. Compare a correct result reached through invalid evidence with a supported result.
4. Design a rollback or reconciliation path for one partial failure.
5. Explain which information should be withheld from the model and why.

## Chapter Summary

Engineer a sufficient, scoped, traceable working set rather than accumulating every available record. Reliable systems separate model capability from application
authority, evaluate the path as well as the answer, and preserve enough
provenance and state to explain failure.

## The Next Tale

The rebuilt package selected one map whose route recommendation was correct. The source mark, however, belonged to a survey superseded six years earlier. Tahmures called for an evidence audit before praising the answer.

<!-- next: ch14 -->

## Citations and Further Reading

- Liu, Nelson F., et al. 2024. “Lost in the Middle: How Language Models Use Long Contexts.” *Transactions of the Association for Computational Linguistics* 12: 157–173.
- Kleppmann, Martin. 2017. *Designing Data-Intensive Applications*. Sebastopol, CA: O’Reilly Media.
