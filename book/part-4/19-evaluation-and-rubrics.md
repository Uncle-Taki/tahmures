---
title: "Evaluation and Rubrics"
slug: "evaluation-and-rubrics"
chapter: 19
part: "Part IV — Evaluation, Security, and Production"
summary: "Turn preferences into anchored, reviewable evaluation contracts with disqualifiers and adjudication."
maturity: "draft"
last_reviewed: "2026-08-01"
narrative_episode: "The Trial Without Weights"
narrative_origin: "original-teaching-fiction"
learning_objectives:
  - "Design anchored outcome rubrics"
  - "Separate model, system, and evaluator failures"
  - "Handle reviewer disagreement without hiding it in an average"
prerequisites:
  - "Chapter 18"
---

# Evaluation and Rubrics

## Learning Objectives

By the end of this chapter, you can design anchored outcome rubrics, separate model, system, and evaluator failures, and handle reviewer disagreement without hiding it in an average. The chapter treats evaluation as an engineering responsibility with observable decisions, explicit owners, and reproducible evidence.

## The Tale of Tahmures

### The Setting

The western court met beneath a ceiling painted with balanced scales. Two villages claimed the same strip of river land. The Archivist brought survey tablets, flood marks, tax rolls, and three witness accounts. Tahmures asked the Mirror Div and two judges to examine the record independently. The First Scribe prepared a docket with three empty columns headed strong, acceptable, and weak, but no one had agreed what those words meant.

### The Request

Tahmures asked each reviewer to choose the better judgement and explain the choice. It sounded fair: several readers, the same evidence, and reasons written in public. Yet one judge valued fidelity to the oldest tablet, another valued present cultivation, and the Mirror Div valued the account that reconciled the most testimony. None declared those priorities before reading the proposed judgements.

### The Unexpected Result

All three praised different decisions. Each explanation was coherent. The Mirror Div selected a polished settlement that quoted a flood mark from the wrong decade. One judge noticed the error but still called the answer acceptable because its remedy was humane. The other rejected it because any unsupported land boundary was disqualifying. Their three labels averaged to something that looked moderate and told the villages nothing. Worse, the council began debating which reviewer sounded wiser instead of which observable qualities the judgement required.

### The Discovery

Tahmures halted the verdict and asked the judges to write the test before seeing another answer. They named evidence fidelity, coverage of both claims, legal consistency, clarity, and practicability. For each, they described what scores from zero to four meant. An invented boundary failed regardless of the total. Two independent reviews were required; a wide difference triggered adjudication rather than arithmetic concealment. The First Scribe recorded the answer, evidence spans, rubric version, individual scores, and rationale. On replay, the reviewers still differed about practicability, but they agreed exactly where and why. Tahmures saw that evaluation was not a ceremonial number attached after judgement. It was a specification for observable success, with its own errors and authority. The court could now revise either the answer, the rubric, or the evidence without pretending those were the same act.

Before recalling the villages, Tahmures placed two deliberately flawed judgements before the panel. One was eloquent but cited no tablet; the other was awkward yet traceable. The old labels favoured eloquence. The written anchors rejected the unsupported boundary and preserved the traceable answer for revision. Then the judges exchanged seats and scored again. Their remaining difference concerned the cost of moving an irrigation wall, a fact the record did not contain. They marked it unresolved. For the first time, the empty place in the evidence appeared in the verdict instead of being filled by confidence.

### From Tale to Engineering

The court lacked more than a good prompt: it lacked an evaluation contract. Reliable AI work requires anchored criteria, disqualifying failures, reviewer provenance, and an explicit path for uncertainty and disagreement.

## The Engineering Problem

The central problem is not whether a language model can occasionally produce a useful answer. It is whether the complete system can show why a result should be accepted, rejected, escalated, or rolled back. In this chapter the primary failure owner is requirements and evaluator design. Prompt wording influences behaviour, but it cannot replace the application mechanisms that own evidence, identity, permissions, state, release decisions, and consequences.

A production design must specify inputs, trust classes, output state, decision criteria, disqualifying outcomes, and operator action. It must also distinguish a failed model answer from a failed evaluator or an invalid request. Without those distinctions, teams tune visible prose while hidden system behavior remains unmeasured.

## Mental Model

Use an anchored multi-reviewer rubric as the governing mental model. Think in four linked planes: the requirement plane defines success and authority; the language plane interprets or proposes; the control plane validates and permits; the evidence plane records outcomes. Each plane has a version and an owner. The model never grants itself authority by emitting the right words.

The boundary is intentionally asymmetric. Language can help explain a deterministic denial, but its explanation cannot reverse that denial. An evaluator can measure a candidate, but it cannot silently redefine the product requirement. A human can approve an exception only through the policy path that records the exact exception.

## Core Concepts

First, define observable success before optimising prompts. Second, preserve provenance and version identity across the pipeline. Third, encode hard constraints in mechanisms that can enforce them. Fourth, report uncertainty, disagreement, and skipped checks as first-class outcomes. Fifth, segment evaluation by risk and case type, because aggregate success can conceal rare consequential failures.

The educational contracts in this repository use stable reason codes and deterministic ordering. They omit networking, durable identity, cryptographic verification, and distributed transactions. That limitation is deliberate: readers can inspect the decision logic offline, then identify what a production integration must add.

## Prompt Pattern

Use a prompt to communicate the bounded language task: relevant context, desired proposal, explicit output structure, and the evidence the model should cite. Keep application-owned policy outside quoted or retrieved content. Ask the model to expose uncertainty rather than manufacture certainty. Then validate the response and apply an anchored multi-reviewer rubric before any consequential acceptance or action.

A useful pattern separates `task`, `trusted_policy_reference`, `untrusted_content`, `output_contract`, and `limits`. These labels improve legibility; they do not enforce trust by themselves. The application constructs the fields, rejects unknown or stale versions, and decides which outputs can reach downstream systems.

## Naive Attempt

The naive design asks the model to “be careful,” “follow policy,” or “choose the best answer,” then treats a fluent response as proof. It tests one representative example and changes wording until that example passes. The demonstration may be encouraging, but it says nothing about malformed input, stale state, hostile content, disagreement, provider drift, or an irreversible effect.

This approach also confuses model compliance with system correctness. A fixture can contain the desired sentence while the surrounding application selected unauthorised data or skipped a check. Evaluation must observe the path and consequence, not only the final text.

## Failure Analysis

Failures for evaluation include underspecified requirements, contaminated context, unstable criteria, missing provenance, version mismatch, unchecked authority, optimistic defaults, aggregate masking, and human review without usable evidence. A good taxonomy records whether the source is requirements, data, model, evaluator, application, tool, operator, or policy.

Do not retry every failure. Invalid input should be corrected, denied authority escalated, insufficient evidence abstained, evaluator disagreement adjudicated, transient dependency errors retried within budget, and policy violations stopped. A generic retry can amplify cost or repeat an external effect while leaving the original defect untouched.

## Improved Design

The improved design makes an anchored multi-reviewer rubric executable in Python and Go. Inputs are typed; malformed or duplicate identities are rejected; decisions return stable fields; and tests cover normal, boundary, and adversarial cases. The language model supplies interpretations or candidates only where language is useful. Application code retains the final say over hard constraints.

Start with a narrow policy that the team can explain. Add cases when real failures reveal missing distinctions. Keep evaluator code and expectations under review: a deterministic evaluator can be consistently wrong, and a human rubric can encode bias. Reliability comes from explicit, challengeable contracts rather than from declaring one component authoritative in every domain.

## Worked Example

Suppose a border service receives a natural-language request, retrieved records, and an action proposal. The request is authenticated before model use. Retrieval is scoped and records preserve provenance. The model produces a typed proposal with evidence identifiers. The application validates structure and evidence, applies an anchored multi-reviewer rubric, and either denies, escalates, or records a permitted next step. A trace links every decision to the prompt, model, policy, data, and evaluator versions.

Now change one variable at a time: expire a record, remove evidence, forge a role label, change an argument after approval, or move a rare case into a small tag group. The expected outcome should change for a documented reason. If the system merely produces a different paragraph, the boundary is still too implicit.

## Experiment

Run the shared, provider-neutral fixture experiment:

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch19-evaluation.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch19-evaluation.json
```

The manifest compares a naive variant with the governed design over committed synthetic cases. The `anchored_rubric` evaluator reports observed fixture behavior. These results demonstrate report mechanics and the stated failure cases; they are not evidence that one wording or model behaves universally better. Replace fixtures with controlled recordings before drawing provider-specific conclusions.

## Evaluation

Measure rubric decision accuracy, disqualifier recall, reviewer disagreement, adjudication rate, and evidence coverage. Report per-case outcomes and tag-level summaries alongside aggregates. Define thresholds and disqualifying failures before reading candidate results. Preserve reviewer rationales and evaluator versions. A skipped evaluation is unknown, not passed, and an unavailable safety check should cause the documented safe fallback.

Evaluate the evaluator with disagreements, deliberately malformed cases, and examples near each threshold. Compare proxy metrics with real downstream outcomes. When a proxy ceases to predict the desired consequence, revise the measurement contract rather than optimising harder against the stale proxy.

## Implementation Lab

### Python

```python
from tahmures.rubrics import Rubric

result = rubric.evaluate(reviews)
if result.requires_adjudication:
    queue_for_human_review(result)
```

Python 3.12 is the canonical educational implementation. Validate at the application boundary, preserve reason codes, and do not continue after a denial or required adjudication.

### Go

```go
result, err := rubric.Evaluate(reviews)
if err != nil {
    return err
}
if result.RequiresAdjudication {
    queueForHumanReview(result)
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

Evaluation and Rubrics turns evaluation into an owned system contract. Prompts remain useful for communicating a bounded language task, while an anchored multi-reviewer rubric governs acceptance or action. Reliable practice preserves provenance and versions, separates failure owners, tests boundaries and adversarial cases, reports disagreement, and refuses to let a favourable average erase a disqualifying result.

## The Next Tale

The anchored rubric settled the court's disagreement, but the First Scribe found a darker result in the ledger: the revised command won this trial and failed three older ones.

<!-- next: ch20 -->

## Citations and Further Reading

- Amershi, Saleema, et al. 2019. “Guidelines for Human-AI Interaction.” *CHI 2019*. https://doi.org/10.1145/3290605.3300233
