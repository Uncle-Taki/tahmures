---
title: "Regression Testing for Prompted Systems"
slug: "regression-testing-for-prompted-systems"
chapter: 20
part: "Part IV — Evaluation, Security, and Production"
summary: "Protect known behaviour with versioned case suites, release gates, and explicit regression budgets."
maturity: "draft"
last_reviewed: "2026-08-01"
narrative_episode: "The Command That Won One Trial"
narrative_origin: "original-teaching-fiction"
learning_objectives:
  - "Build versioned prompt-system regression suites"
  - "Classify improvements, regressions, and intended changes"
  - "Gate releases on protected cases and score floors"
prerequisites: [C06, C19]
---

# Regression Testing for Prompted Systems

## Learning Objectives

By the end of this chapter, you can build versioned prompt-system regression suites, classify improvements, regressions, and intended changes, and gate releases on protected cases and score floors. The chapter treats regression testing as an engineering responsibility with observable decisions, explicit owners, and reproducible evidence.

## The Tale of Tahmures

### The Setting

The First Scribe's experiment ledger filled an entire wall of the Hall of Scripts. Each leaf held a request, the command version used, the result, and the council's decision. A new leaf described a caravan question that the latest command had answered badly. Tahmures asked for a revision before the next departure.

### The Request

The Keeper of Scripts changed three lines and tested the command against the caravan question. The answer now named the safe road, preserved the winter restriction, and cited the current map. The single red mark became green. Tahmures approved the revision, pleased that evidence had replaced argument.

### The Unexpected Result

By noon, complaints arrived from the archive, the granary, and the border court. The new wording treated an expired order as current, omitted a ration limit, and answered a sealed question that required abstention. Those cases had passed last week. No one had replayed them because they were not part of the reported defect. The revision had genuinely improved one behaviour; it had also shifted how the command weighed recency, exceptions, and missing evidence. Calling it better or worse in the abstract concealed the changed decisions.

### The Discovery

Tahmures ordered the First Scribe to stop organising the ledger by embarrassment. Cases were given stable identities, expected outcomes, tags, and owners. Safety and authority cases became protected: a revision could not spend them to gain an average point elsewhere. Every candidate ran against the same frozen dataset, fixture recordings, prompt version, policy version, and evaluators. The report separated fixed, regressed, stable-pass, and stable-fail cases. Some changed expectations were legitimate, but they required a policy decision and review rather than silent relabelling. The council also retained failures discovered in production after removing private details. A prompt revision was no longer a corrected sentence; it was a proposed system release. The test suite did not prove future perfection, but it made forgetting old obligations harder.

They rehearsed the gate with three proposed revisions. The first fixed the caravan and broke a sealed-order case. The second preserved every old case but failed the new one. The third passed both and lowered the quality of two ordinary summaries. Tahmures refused to hide those differences behind one total. The council accepted the third only after deciding that the lower summary score remained above its declared floor. Beside the release mark, the First Scribe wrote what had improved, what had worsened, and who had accepted the trade. Future readers would inherit a decision, not a mysterious green seal.

### From Tale to Engineering

A local fix is not evidence of a safe release. Prompted systems need versioned regression suites that expose both gains and losses, protect disqualifying cases, and preserve the rationale for intended behavioural change.

## The Engineering Problem

The central problem is not whether a language model can occasionally produce a useful answer. It is whether the complete system can show why a result should be accepted, rejected, escalated, or rolled back. In this chapter the primary failure owner is release process. Prompt wording influences behaviour, but it cannot replace the application mechanisms that own evidence, identity, permissions, state, release decisions, and consequences.

A production design must specify inputs, trust classes, output state, decision criteria, disqualifying outcomes, and operator action. It must also distinguish a failed model answer from a failed evaluator or an invalid request. Without those distinctions, teams tune visible prose while hidden system behavior remains unmeasured.

## Mental Model

Use a versioned regression gate as the governing mental model. Think in four linked planes: the requirement plane defines success and authority; the language plane interprets or proposes; the control plane validates and permits; the evidence plane records outcomes. Each plane has a version and an owner. The model never grants itself authority by emitting the right words.

The boundary is intentionally asymmetric. Language can help explain a deterministic denial, but its explanation cannot reverse that denial. An evaluator can measure a candidate, but it cannot silently redefine the product requirement. A human can approve an exception only through the policy path that records the exact exception.

## Core Concepts

First, define observable success before optimising prompts. Second, preserve provenance and version identity across the pipeline. Third, encode hard constraints in mechanisms that can enforce them. Fourth, report uncertainty, disagreement, and skipped checks as first-class outcomes. Fifth, segment evaluation by risk and case type, because aggregate success can conceal rare consequential failures.

The educational contracts in this repository use stable reason codes and deterministic ordering. They omit networking, durable identity, cryptographic verification, and distributed transactions. That limitation is deliberate: readers can inspect the decision logic offline, then identify what a production integration must add.

## Prompt Pattern

Use a prompt to communicate the bounded language task: relevant context, desired proposal, explicit output structure, and the evidence the model should cite. Keep application-owned policy outside quoted or retrieved content. Ask the model to expose uncertainty rather than manufacture certainty. Then validate the response and apply a versioned regression gate before any consequential acceptance or action.

A useful pattern separates `task`, `trusted_policy_reference`, `untrusted_content`, `output_contract`, and `limits`. These labels improve legibility; they do not enforce trust by themselves. The application constructs the fields, rejects unknown or stale versions, and decides which outputs can reach downstream systems.

## Naive Attempt

The naive design asks the model to “be careful,” “follow policy,” or “choose the best answer,” then treats a fluent response as proof. It tests one representative example and changes wording until that example passes. The demonstration may be encouraging, but it says nothing about malformed input, stale state, hostile content, disagreement, provider drift, or an irreversible effect.

This approach also confuses model compliance with system correctness. A fixture can contain the desired sentence while the surrounding application selected unauthorised data or skipped a check. Evaluation must observe the path and consequence, not only the final text.

## Failure Analysis

Failures for regression testing include underspecified requirements, contaminated context, unstable criteria, missing provenance, version mismatch, unchecked authority, optimistic defaults, aggregate masking, and human review without usable evidence. A good taxonomy records whether the source is requirements, data, model, evaluator, application, tool, operator, or policy.

Do not retry every failure. Invalid input should be corrected, denied authority escalated, insufficient evidence abstained, evaluator disagreement adjudicated, transient dependency errors retried within budget, and policy violations stopped. A generic retry can amplify cost or repeat an external effect while leaving the original defect untouched.

## Improved Design

The improved design makes a versioned regression gate executable in Python and Go. Inputs are typed; malformed or duplicate identities are rejected; decisions return stable fields; and tests cover normal, boundary, and adversarial cases. The language model supplies interpretations or candidates only where language is useful. Application code retains the final say over hard constraints.

Start with a narrow policy that the team can explain. Add cases when real failures reveal missing distinctions. Keep evaluator code and expectations under review: a deterministic evaluator can be consistently wrong, and a human rubric can encode bias. Reliability comes from explicit, challengeable contracts rather than from declaring one component authoritative in every domain.

## Worked Example

Suppose a border service receives a natural-language request, retrieved records, and an action proposal. The request is authenticated before model use. Retrieval is scoped and records preserve provenance. The model produces a typed proposal with evidence identifiers. The application validates structure and evidence, applies a versioned regression gate, and either denies, escalates, or records a permitted next step. A trace links every decision to the prompt, model, policy, data, and evaluator versions.

Now change one variable at a time: expire a record, remove evidence, forge a role label, change an argument after approval, or move a rare case into a small tag group. The expected outcome should change for a documented reason. If the system merely produces a different paragraph, the boundary is still too implicit.

## Experiment

Run the shared, provider-neutral fixture experiment:

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch20-regression.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch20-regression.json
```

The manifest compares a naive variant with the governed design over committed synthetic cases. The `regression_gate` evaluator reports observed fixture behavior. These results demonstrate report mechanics and the stated failure cases; they are not evidence that one wording or model behaves universally better. Replace fixtures with controlled recordings before drawing provider-specific conclusions.

## Evaluation

Measure fixed-case count, regression count, protected regressions, candidate score floor, and mean score delta. Report per-case outcomes and tag-level summaries alongside aggregates. Define thresholds and disqualifying failures before reading candidate results. Preserve reviewer rationales and evaluator versions. A skipped evaluation is unknown, not passed, and an unavailable safety check should cause the documented safe fallback.

Evaluate the evaluator with disagreements, deliberately malformed cases, and examples near each threshold. Compare proxy metrics with real downstream outcomes. When a proxy ceases to predict the desired consequence, revise the measurement contract rather than optimising harder against the stale proxy.

## Implementation Lab

### Python

```python
from tahmures.regression import compare_regression

report = compare_regression(baseline, candidate, policy)
if not report.passed:
    block_release(report.regressed)
```

Python 3.12 is the canonical educational implementation. Validate at the application boundary, preserve reason codes, and do not continue after a denial or required adjudication.

### Go

```go
report, err := tahmures.CompareRegression(baseline, candidate, policy)
if err != nil {
    return err
}
if !report.Passed {
    blockRelease(report.Regressed)
}
```

The Go implementation preserves observable decisions, ordering, and failure meanings. Equivalence concerns behavior and report fields, not a line-for-line translation of Python syntax.

## Failure Modes

Common failures include one-case tuning, mutable expectations, unversioned policy, trust inferred from formatting, implicit permission, stale approvals, averages without segments, logs without correlation IDs, and reviews without anchors. Another subtle failure is declaring the control successful because the final answer happened to be safe even though the path violated the contract.

Keep a failure ledger. For every incident, record the smallest reproducible case, the actual owner, the safe expected outcome, the affected versions, and the decision about retention. Add the case to the appropriate suite without retaining unnecessary private content.

## Security Considerations

Treat all user, retrieved, remembered, generated, and tool-returned text as untrusted unless the application assigns a narrower trusted role. Never place secrets in prompts merely because the model was told not to reveal them. Authenticate outside text, constrain capabilities, recheck authority at action time, and log receipts for consequential effects.

Security evaluation must include legitimate content that resembles an attack, so defences do not reduce to deleting suspicious phrases. It must also include indirect and split instructions, forged labels, stale credentials, replay, confused-deputy paths, and denial-of-service budgets. The safest output cannot repair an already excessive credential.

## Operational Considerations

Record model, prompt, policy, schema, dataset, evaluator, and code versions. Monitor outcomes, denials, abstentions, evaluator availability, latency, cost, and rare disqualifying failures by segment. Use shadow evaluation and canary release where possible. Roll back coherent bundles, because restoring a prompt alone while retaining an incompatible policy or index can create a new failure.

Document service behavior during provider, retrieval, evaluator, and storage outages. Bound retries and preserve idempotency. Operators need runbooks that use stable controls, not emergency edits to conversation text. Reconcile uncertain external effects before retrying them.

## Trade-Offs

Explicit controls add schemas, policy maintenance, evaluation work, and operational latency. They also make failures local, inspectable, and recoverable. Strict rejection can reduce availability; permissive fallback can violate safety or authority. Human review adds judgement and accountability while introducing delay, inconsistency, and reviewer load. The right design states these costs and decides which risk it accepts.


### Requirements and ownership

Start with the decision and its consequence. Name who owns the requirement, who may change it, and which component can observe whether it was satisfied. A duty assigned only to “the model” has no stable enforcement point. Split it into model interpretation, application policy, deterministic checks, evaluator observations, and accountable human decisions. Record what happens when any owner is unavailable. Hard constraints and disqualifying outcomes must remain visible even when an aggregate score improves.

### Inputs, sources, and boundaries

Inventory every input, including defaults, caches, retrieved passages, memories, tool results, policy files, and operator overrides. For each source, record provenance, freshness, scope, authority, sensitivity, and retention. Relevant text is not automatically trusted instruction. Absence is not an empty authoritative value. The model-visible representation should preserve the distinctions the application will need later for validation, explanation, and incident analysis.

### Normal, boundary, and adversarial cases

A happy path only shows that the pieces can cooperate once. Add empty inputs, duplicates, exact limits, expiry at the current instant, conflicting current values, malformed structures, stale versions, and partial dependencies. Add inert adversarial cases for forged authority, indirect instructions, replay, scope expansion, identifier confusion, and resource exhaustion. Vary surface wording while keeping the prohibited consequence constant; phrase recognition is not a security boundary.

### Failure taxonomy

Do not collapse invalid input, insufficient evidence, denied authority, evaluator disagreement, exhausted budget, dependency failure, cancellation, and internal error into “failed.” These states have different owners, retry rules, and user messages. Assign a stable reason code at the earliest component that can know the truth. Preserve it through later stages even when generated prose offers a friendlier explanation.

### Versioning and reproducibility

Pin the model identity, prompt, policy, data snapshot, fixture, evaluator, code, and schema in every consequential report. A score without this construction history cannot support comparison. When expectations change, retain the old case and document why the new label is an intended policy revision. Compatibility means preserving observable decisions and reason codes, not merely parsing the same file.

### Privacy and retention

Minimise content before it enters a model, trace, log, fixture, or review queue. Retain by purpose and data class, not because debugging may someday be useful. Deletion must include summaries, embeddings, caches, copied artefacts, and evaluation extracts. Prefer stable identifiers and counts in telemetry; an operator should diagnose a boundary without gaining access to the underlying record.

### Access and authority

Authenticate identities outside generated text. Filter scope before retrieval and recheck it immediately before external action. A component may pass evidence without passing its own authority. Default denial needs a usable escalation route, or operators will build unsafe bypasses. Test forged labels, stale approvals, legitimate requests from unauthorised routes, and credentials whose capability exceeds the described task.

### Observability

Trace case, run, source, decision, and version identifiers across boundaries. Record selection, exclusion, denial, retry, abstention, cancellation, and validation counts without logging unnecessary payloads. Dashboards need distributions and rare disqualifying events, not averages alone. An incident responder should be able to locate whether the bad outcome began in requirements, input construction, generation, evaluation, application code, a tool, or human review.

### Latency, cost, and budgets

Allocate tokens, time, calls, money, storage, and review attention before execution. Reserve capacity for validation, safe termination, receipts, and cleanup. Measure cost by successful, policy-compliant outcome rather than generation alone. Test degraded modes explicitly. A cheaper fallback is not acceptable if it silently skips the control that made the normal path safe.

### Recovery and reconciliation

Define retry, idempotency, rollback, compensation, and reconciliation for every state-changing boundary. A timeout does not reveal whether an effect occurred. Receipts and request identities must allow the caller to learn the truth without repeating an irreversible action. Recovery paths deserve the same authorization and evaluation as the normal path.

### Human review and appeal

Human review is a designed component, not a decorative final glance. Show reviewers the evidence, uncertainty, policy version, proposed consequence, and alternatives they need. Prevent automation bias with independent anchors and an appeal route. Track disagreement and overrides as diagnostic signals. A named approver remains accountable; the model's confidence cannot substitute for that responsibility.

### Change management

Treat prompts, policies, evaluators, retrieval configuration, tool contracts, and models as deployable versions. Review changes, replay suites, compare segments, canary releases, and retain a coherent rollback bundle. A change that improves one metric can still violate authority, privacy, or cost constraints. Document accepted residual risk and the person authorised to accept it.

### Data quality and coverage

Evaluation is bounded by the cases and labels it contains. Sample across ordinary traffic, rare but consequential segments, changing language, missing fields, and historically failed cases. Inspect whether synthetic data preserves the decision shape without being mistaken for production prevalence. Review labels independently and retain uncertainty where experts disagree. Coverage should answer which risks were examined, not claim that unseen behavior has been eliminated.

### Evaluator governance

Evaluators are production logic when their scores block releases or actions. Give them owners, tests, versions, access limits, and rollback plans. Measure false acceptance and false rejection, and audit deterministic rules as carefully as model-based judges. Never let a model's self-reported score stand in for external evaluation. When human judgement is required, preserve reviewer identity, rationale, anchors, and adjudication rather than only the final number.

### Documentation and evidence

Keep a compact decision record beside each contract: purpose, non-goals, trusted sources, hard invariants, thresholds, reason codes, known limitations, and escalation owner. Examples are useful evidence only when their fixtures and versions are preserved. Documentation should let a new operator predict the safe outcome of a boundary case before running it. If prose and executable policy disagree, the enforced policy must be visible and the discrepancy treated as a defect.

### Adoption and maintenance

The smallest enforceable boundary that a team can maintain is safer than an elaborate design no one understands. Introduce controls with migration paths, observe rejection reasons, and distinguish genuine user friction from blocked unsafe behavior. Budget time for refreshing cases, reviewing drift, rotating credentials, and retiring obsolete policy. Reliability decays when a control has no owner after launch, even if its initial implementation was correct.

### Counterfactual and ablation tests

Remove or alter one control at a time to learn which outcome it actually protects. Replace current evidence with stale evidence, widen a capability, suppress a disqualifier, or hide a version field. A useful test should fail for the predicted reason. If removing a supposed safeguard changes nothing, it may be ceremonial or its evaluator may be blind. Counterfactual tests also prevent teams from crediting prompt wording for safety supplied by an unseen application rule.

### Residual risk and decision records

No test suite closes an open world. After controls pass, state what remains uncertain: unseen inputs, provider changes, reviewer bias, integration defects, or consequences outside telemetry. Estimate impact and detectability, name the risk owner, and set a review date. Acceptance is a governance decision supported by evidence, not a mathematical declaration that failure is impossible. This record lets later incidents challenge the assumptions that were actually made.

### End-to-end acceptance

Component tests are necessary and insufficient. Run representative requests through authentication, context construction, generation, validation, policy, action simulation, and reporting. Verify not only the answer but the absence of prohibited side effects and the presence of receipts. Inject failures between stages: lose an acknowledgement, time out after a proposed mutation, or make an evaluator unavailable. The safe terminal state should remain predictable. Compare end-to-end outcomes with component metrics so a fortunate final answer cannot hide a violated boundary, and a correctly blocked request is not mislabelled as poor model quality. Before release, have someone outside the implementation team reconstruct one decision from the retained evidence. If that person cannot identify the active versions, authority, sources, and reason code, the system is not yet auditable enough for its claimed consequence.


## When Prompting Is Not the Answer

Prompting is not the enforcement mechanism for identity, permission, uniqueness, arithmetic invariants, transaction isolation, rate limits, expiry, deletion, or irreversible approval. Use access control, database constraints, deterministic code, schedulers, queues, and accountable human processes. Use a model where interpretation, synthesis, classification, or explanation benefits from learned language patterns.

The mature question is not “Can a prompt do this?” but “Which component can own this requirement and prove its outcome?” If the answer names only language, redesign the boundary before polishing the sentence.

## Exercises

1. Add one normal, one boundary, one malformed, and one adversarial case to the chapter manifest. Predict the safe reason code before running it.
2. Identify a disqualifying outcome that an average could hide. Add a protected tag or hard policy for it.
3. Trace one value from source through model-visible context, evaluation, action, logging, retention, and deletion.
4. Exchange a report with a partner and review the evaluator rather than the model answer. Which expectation is least defensible?
5. Design the safe degraded behavior when the chapter's governing control is unavailable.

## Chapter Summary

Regression Testing for Prompted Systems turns regression testing into an owned system contract. Prompts remain useful for communicating a bounded language task, while a versioned regression gate governs acceptance or action. Reliable practice preserves provenance and versions, separates failure owners, tests boundaries and adversarial cases, reports disagreement, and refuses to let a favourable average erase a disqualifying result.

## The Next Tale

While adding a failed archive case to the suite, the Archivist unfolded a tablet whose first line addressed not Tahmures, but the reader of the tablet itself.

<!-- next: ch21 -->

## Citations and Further Reading

- Ribeiro, Marco Tulio, Tongshuang Wu, Carlos Guestrin, and Sameer Singh. 2020. “Beyond Accuracy: Behavioral Testing of NLP Models with CheckList.” *ACL 2020*. https://doi.org/10.18653/v1/2020.acl-main.442
