---
title: "Retrieval-Augmented Generation"
slug: "retrieval-augmented-generation"
chapter: 14
part: "Part III — Knowledge, Memory, and Action"
summary: "Evaluate retrieval, evidence, and citations as distinct components of grounded generation."
maturity: "draft"
last_reviewed: "2026-07-30"
narrative_episode: "The Correct Answer from the Wrong Tablet"
learning_objectives:
  - "Measure retrieval quality before answer quality"
  - "Preserve chunk identity, scope, freshness, and provenance"
  - "Reject correct-looking answers supported by the wrong evidence"
prerequisites:
  - "Chapter 13"
---

# Retrieval-Augmented Generation

## Learning Objectives

By the end of this chapter, you can measure retrieval quality before answer quality,
preserve chunk identity, scope, freshness, and provenance, and reject correct-looking answers supported by the wrong evidence. The goal is
not a persuasive demonstration but a boundary that can be inspected, tested,
denied, and operated.

## The Tale of Tahmures

*The following is an original fictional episode created for teaching. It is not
a translation, adaptation, or reconstructed passage from the* Shahnameh.

### The Setting

In the map room, a brass pointer rested on the eastern pass. A div had named it safe after searching a cabinet of route tablets. The caravan crossed without incident, and the council celebrated both speed and accuracy. The First Scribe, following the new rules for the council table, asked for the source mark. The tablet came from a survey made before a landslide moved the road.

### The Request

Tahmures asked why the old tablet had been retrieved. It repeated the words “eastern pass,” “safe road,” and the village name more often than the current survey. Its script was cleaner and its copied title longer. The current record described the same pass using a newer district name and ranked second. The div had answered correctly because, by coincidence, workers reopened the old alignment the previous week—a fact found nowhere on the retrieved tablet.

### The Unexpected Result

An adviser argued that a correct answer was sufficient. Tahmures placed a second route question beside it. This time the obsolete map named a bridge that no longer existed. The method of choosing tablets behaved consistently; the world had merely stopped rewarding its mistake. No source mark in the first answer exposed the problem because the response named “the archive” rather than a particular passage. Success on one journey had concealed stale evidence, poor selection, and a path nobody could retrace.

### The Discovery

The Archivist divided finding passages from answering questions. Every copied
passage received a permanent shelf mark, the mark of its parent tablet, the
readers permitted to see it, the dates for which it spoke, and the name of its
source. Before the div wrote a sentence, clerks tried known questions whose
useful passages had already been identified. They barred forbidden and expired
tablets, ordered the remaining candidates, and allowed only a small stack onto
the reading desk. An answer could name only marks present in that stack. When
no current tablet supported a route, declining to choose counted as success.
Tahmures compared how often the needed passage appeared, how much useless
material accompanied it, how early it appeared, and whether every named source
could be inspected. A fortunate arrival no longer earned a perfect mark by
itself.

They repeated the trial with river crossings, winter shelters, and provincial names that had changed. Sometimes the newest tablet was not relevant; sometimes an old tablet remained valid. The Archivist therefore refused a rule that equated age with falsehood. She recorded why a candidate entered the cabinet, why another was barred, and where the first useful passage appeared. Tahmures then asked the div questions for which the cabinet contained no answer. Its most trustworthy response was a plain admission that the evidence was insufficient. The court began to reward that restraint as carefully as a supported route.

### From Tale to Engineering

Retrieval supplies a model with candidate evidence; it does not certify that the evidence is current, authorised, relevant, or sufficient. Reliable RAG evaluates the corpus, retriever, context package, answer, and citations as separate stages.

## The Engineering Problem

Retrieval-augmented generation combines an information-retrieval system with generation. A fluent answer can hide missed evidence, irrelevant chunks, stale documents, inaccessible sources, poor chunking, or unsupported citations. End-to-end correctness alone cannot locate the failure.

The practical question is therefore not whether a model can sometimes produce
a useful result. It is whether the surrounding system can show what information
and authority were available, which invariant was checked, what changed state,
and why the outcome should be accepted or stopped.

## Mental Model

Use the pipeline query → authorised candidate corpus → ranking → top-k chunks → context assembly → grounded answer → citation validation. Each arrow has an observable contract. The generator may only cite the retrieved set; a cited source still needs semantic support review.

A mental model is useful only when it assigns ownership. Requirements belong to
people and product policy. Identity, permission, validity, budgets, and state
transitions belong to application mechanisms. Language models interpret or
propose within those boundaries. Evaluators observe outcomes and have their own
documented limitations.

## Core Concepts

Recall asks whether relevant evidence was retrieved; precision asks how much retrieved material was relevant. Reciprocal rank rewards an early first relevant result. Chunk identity and document identity must both survive. Scope and validity are filters, not ranking hints. Top-k is a cost and recall decision. Abstention is required when evidence is insufficient.

Treat each concept as a contract with inputs, outputs, failure reasons, and a
lifecycle. Do not merge absence, invalidity, denial, uncertainty, and
infrastructure error into one generic failure. Those states require different
retry, escalation, and user communication.

## Prompt Pattern

Ask for an answer using only enumerated chunks, cite chunk IDs beside claims, report conflicts, and return insufficient_evidence when the set cannot support the decision. Enforce citation membership in code.

The prompt communicates the contract to a probabilistic participant. The
application implements the enforceable parts. Keep trusted configuration
separate from user, retrieved, remembered, generated, and tool-returned text.

## Naive Attempt

The naive system searches all text, concatenates the first matches, and asks for an answer with sources. Lexical repetition can outrank current authority. A fabricated or out-of-set citation may look formal enough to pass manual inspection.

A successful demonstration does not cover stale, missing, cross-scope,
duplicated, contradictory, cancelled, or unauthorised cases. The first test
suite must contain those cases before wording is optimised.

## Failure Analysis

Diagnose corpus omission, permission filtering, chunk boundaries, query formulation, ranking, top-k, context assembly, model use, and citation support separately. A wrong answer with perfect recall differs from a right answer reached through stale evidence.

Assign a stable error or decision code at the earliest boundary that can know
the truth. Preserve enough metadata for diagnosis without retaining unnecessary
sensitive content. A model-generated explanation is not a substitute for that
record.

## Improved Design

The InMemoryRetriever is a deterministic offline boundary: it filters scope and validity, computes normalised term overlap, uses stable tie-breaking, and returns bounded chunks with provenance. validate_citations rejects IDs outside the returned set. Production retrieval can replace the scorer without changing these contracts.

The implementation deliberately stays small and dependency-free. Its purpose is
to make the boundary executable in both Python and Go. Production systems will
need durable storage, authentication, concurrency control, maintained parsers,
and organisation-specific policy.

## Worked Example

A policy assistant retrieves current policy P7 and obsolete P2. Filtering removes P2 before scoring. If P7 does not mention the requested exception, the answer abstains rather than filling the gap from model memory. The selection packet records what was searched and returned.

Trace one value from origin through filtering, model-visible representation,
evaluation, logging, retention, and deletion. This lineage exercise often
reveals that a convenient field combines sources with different authority or
lifecycle.

## Experiment

Run the shared offline experiment:

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch14-retrieval.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch14-retrieval.json
```

The committed synthetic fixtures compare unscoped lexical retrieval and current scoped retrieval. They demonstrate
report mechanics and failure diagnosis, not universal model performance.
Replace fixtures with controlled recordings before making provider claims.

## Evaluation

Measure recall@k, precision@k, reciprocal rank, stale-source rate, citation validity, supported-answer rate, and appropriate abstention. Segment by normal, boundary, adversarial, scope,
freshness, and previously failed cases. Define disqualifying failures before
inspecting aggregate results. Compare pipeline-stage metrics with end-to-end
outcomes so a fortunate answer cannot hide an invalid path.

## Implementation Lab

### Python

```python
from tahmures.retrieval import InMemoryRetriever, RetrievalRequest, RetrievedChunk

retriever = InMemoryRetriever((
    RetrievedChunk("CUR", "map-7", "safe eastern pass", "survey:7"),
))
chunks = retriever.retrieve(RetrievalRequest("safe pass", 3))
```

The Python API is the canonical educational contract. Catch validation errors
at the application boundary and do not continue after denial.

### Go

```go
retriever := tahmures.InMemoryRetriever{Chunks: []tahmures.RetrievedChunk{
    {ChunkID: "CUR", DocumentID: "map-7", Text: "safe eastern pass", Provenance: "survey:7"},
}}
chunks, err := retriever.Retrieve(tahmures.RetrievalRequest{Query: "safe pass", Limit: 3})
```

The Go implementation preserves observable decisions and reason codes rather
than copying Python syntax.

## Failure Modes

Corpus gaps, poisoned or stale records, cross-scope retrieval, chunk boundaries that remove qualifications, duplicate dominance, query drift, low recall hidden by fluent answers, citation membership without claim support, and benchmarks unlike production traffic.

Add every observed production failure to a versioned regression set. Keep the
failed input, governing policy version, expected safe outcome, and evaluator
rationale. Remove or redact sensitive payloads without erasing the case shape.

## Security Considerations

Apply tenant and document permissions before retrieval. Treat chunk text as untrusted data. Prevent retrieved instructions from changing tool authority. Do not reveal inaccessible document IDs through citations or logs.

Assume content can be relevant without being authoritative. Use deterministic
enforcement for access, mutation, budgets, identity, and irreversible action.
Human approval must show trusted facts about the proposed consequence.

## Operational Considerations

Version corpus snapshots, chunkers, embeddings or scorers, filters, prompts, and evaluators. Monitor source mix, age, no-result rate, citation rate, and labelled retrieval metrics. Reindex after corrections and verify deletion propagation.

Define service behaviour for dependency failure. A skipped check must not be
interpreted as a passed check. Provide safe terminal outcomes, correlation
identifiers, and runbooks that do not require editing conversation text.

## Trade-Offs

Larger top-k may increase recall and context noise. Smaller chunks improve targeting but lose relationships; larger chunks preserve context but consume budget. Dense, sparse, and hybrid retrieval have different costs and failure profiles. Choose through representative evaluation.

### Requirements and ownership

Begin with the decision the system is allowed to make and the decision it
must leave to a person or another service. Name the owner of every invariant,
especially where generated language crosses into stored state or external
action. A responsibility assigned only to “the AI” cannot be audited. Convert
it into an application check, a model task, or a human review duty, and state
what happens when that owner is unavailable. For retrieval-augmented generation, case R01 must make the review observable through recall@k, precision@k, reciprocal rank, stale-source rate, citation validity, supported-answer rate, and appropriate abstention. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Inputs and source inventory

List every source before designing the model-visible representation.
Record who may write it, who may read it, how freshness is determined, and
whether its words can instruct or only inform. Include caches, summaries,
defaults, and operator overrides; hidden convenience sources often cause the
most confusing failures. Test absence explicitly, because a missing source
must not silently become an empty but authoritative value. For retrieval-augmented generation, case R02 must make the review observable through recall@k, precision@k, reciprocal rank, stale-source rate, citation validity, supported-answer rate, and appropriate abstention. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Normal and boundary cases

A happy path should prove the basic contract, not the whole design. Add
empty collections, exact-budget inputs, expiry at the current instant,
duplicate identifiers, conflicting current values, and the smallest and
largest accepted payloads. Boundary cases reveal whether comparisons,
defaults, and ordering rules agree between implementations. Document which
boundaries are product choices rather than facts about language models. For retrieval-augmented generation, case R03 must make the review observable through recall@k, precision@k, reciprocal rank, stale-source rate, citation validity, supported-answer rate, and appropriate abstention. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Adversarial cases

Construct inert cases that attempt scope expansion, authority claims,
identifier confusion, indirect instructions, replay, and resource
exhaustion. The purpose is to test the application boundary, not to invite
the model to recognise villainous wording. Vary surface language while
preserving the same prohibited consequence. A safety rule that works only
when an attack announces itself is a demonstration, not a control. For retrieval-augmented generation, case R04 must make the review observable through recall@k, precision@k, reciprocal rank, stale-source rate, citation validity, supported-answer rate, and appropriate abstention. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Failure classification

Separate invalid input, denied authority, insufficient evidence,
exhausted budget, dependency failure, cancellation, evaluator uncertainty,
and internal error. These outcomes have different retry and escalation
policies. Assign the reason at the earliest component that knows it, then
preserve it through later layers. Do not let a friendly generated explanation
replace the machine-readable cause used by operators and tests. For retrieval-augmented generation, case R05 must make the review observable through recall@k, precision@k, reciprocal rank, stale-source rate, citation validity, supported-answer rate, and appropriate abstention. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Versioning and reproducibility

Pin the prompt, policy, data snapshot, fixture, evaluator, and relevant
code version in each report. A result without its construction history cannot
support regression analysis. When a schema or policy changes, replay the old
cases and classify every changed decision as intended, harmless, or a defect.
Compatibility must describe observable behaviour, including rejection
reasons, rather than merely accepting the same file format. For retrieval-augmented generation, case R06 must make the review observable through recall@k, precision@k, reciprocal rank, stale-source rate, citation validity, supported-answer rate, and appropriate abstention. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Privacy and retention

Minimise information before it enters model-visible context, logs, traces,
or evaluation fixtures. Define retention by data class and purpose instead of
keeping everything for possible debugging. Deletion must cover derived
summaries, indexes, caches, and copied artefacts. Operational metadata should
explain a decision without revealing records that the caller was never
permitted to know existed. For retrieval-augmented generation, case R07 must make the review observable through recall@k, precision@k, reciprocal rank, stale-source rate, citation validity, supported-answer rate, and appropriate abstention. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Access and authority

Authenticate the caller and source outside generated text. Apply scope
filtering before ranking or presentation, and recheck authority immediately
before a consequential effect. A component may pass evidence without passing
its own permissions. Test forged labels, stale approval, cross-tenant
identifiers, and a legitimate request delivered through an unauthorised
route. Default denial needs a usable escalation path rather than a dead end. For retrieval-augmented generation, case R08 must make the review observable through recall@k, precision@k, reciprocal rank, stale-source rate, citation validity, supported-answer rate, and appropriate abstention. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Observability

Trace stable case, run, source, and decision identifiers across component
boundaries. Record counts and reason codes for selection, exclusion, denial,
retry, cancellation, and validation, while avoiding raw sensitive payloads.
Dashboards should expose distributions and rare disqualifying failures, not
only averages. An operator must be able to locate whether a bad outcome began
before the model, inside generation, or after it. For retrieval-augmented generation, case R09 must make the review observable through recall@k, precision@k, reciprocal rank, stale-source rate, citation validity, supported-answer rate, and appropriate abstention. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Latency, cost, and budgets

Allocate time, tokens, calls, storage, and money across stages before the
request begins. Reserve capacity for safe completion, receipts, and cleanup;
consuming the whole budget on generation can prevent a controlled ending.
Evaluate degraded paths such as smaller candidate sets or human escalation.
Optimisation is acceptable only while hard constraints and rare-case safety
remain visible in the comparison. For retrieval-augmented generation, case R10 must make the review observable through recall@k, precision@k, reciprocal rank, stale-source rate, citation validity, supported-answer rate, and appropriate abstention. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Recovery and reconciliation

Assume a process can fail after an external side effect but before its
receipt is stored. Define idempotency, retry classes, acknowledgement, and
reconciliation for that uncertain interval. Some actions can be compensated;
others require a person to inspect reality. Recovery code must respect current
goal and authority rather than replaying an old request merely because it
appears unfinished. For retrieval-augmented generation, case R11 must make the review observable through recall@k, precision@k, reciprocal rank, stale-source rate, citation validity, supported-answer rate, and appropriate abstention. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Human review

Specify what the reviewer sees: trusted identity, source evidence,
constraints, proposed consequence, uncertainty, and reversible alternatives.
A raw transcript transfers too much noise and too little verified state.
Record the reviewer’s decision and rationale without pretending that approval
proves the model was correct. Measure disagreement and escalation load so
review does not become an invisible bottleneck. For retrieval-augmented generation, case R12 must make the review observable through recall@k, precision@k, reciprocal rank, stale-source rate, citation validity, supported-answer rate, and appropriate abstention. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Cross-language contract parity

Python and Go need equivalent accepted inputs, normalised outputs,
ordering, and failure reasons, not line-for-line implementations. Shared
manifests and fixtures make observable drift visible. Include malformed and
boundary cases because default JSON behaviour, time comparison, sorting, and
numeric conversion differ across runtimes. Keep one canonical report shape so
readers can compare behaviour without translating the result. For retrieval-augmented generation, case R13 must make the review observable through recall@k, precision@k, reciprocal rank, stale-source rate, citation validity, supported-answer rate, and appropriate abstention. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Rollout and rollback

Introduce policy and model changes with shadow reports or a controlled
cohort. Compare both aggregate metrics and every disqualifying case before
expanding. A rollback must restore compatible policy, schemas, and data
assumptions, not only an earlier prompt. Preserve enough previous artefacts
to reproduce the old decision and define who can halt rollout when a rare
boundary regresses. For retrieval-augmented generation, case R14 must make the review observable through recall@k, precision@k, reciprocal rank, stale-source rate, citation validity, supported-answer rate, and appropriate abstention. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Incident response

A runbook should let operators pause new work, revoke capability, inspect
affected versions, identify exposed subjects, and reconcile uncertain side
effects. Preserve evidence with access controls and avoid copying sensitive
text into tickets. After containment, convert the incident into synthetic
regression cases that retain the failure shape. Correct data and derived
state as well as wording. For retrieval-augmented generation, case R15 must make the review observable through recall@k, precision@k, reciprocal rank, stale-source rate, citation validity, supported-answer rate, and appropriate abstention. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

### Long-term drift

Traffic, sources, policies, external tools, and model behaviour change at
different rates. Monitor tagged slices and refusal or escalation patterns so
a stable average cannot hide a failing subgroup. Schedule replay on frozen
fixtures and sample current cases for human adjudication. When the environment
changes, revisit requirements first; prompt tuning cannot preserve a contract
whose underlying meaning has moved. For retrieval-augmented generation, case R16 must make the review observable through recall@k, precision@k, reciprocal rank, stale-source rate, citation validity, supported-answer rate, and appropriate abstention. Define at least one disqualifying outcome; do not allow a favourable aggregate to cancel it.

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

Use a database query for exact balances, permissions, and current status. Use a search engine directly when the user needs documents rather than synthesis. Retrieval cannot repair an absent or untrustworthy corpus.

Language remains valuable for interpretation and explanation, but mechanisms
must own invariants that cannot safely depend on persuasive text.

## Exercises

1. Add one normal, one boundary, and one adversarial case to the dataset.
2. Identify the application-owned invariant and implement its deterministic check.
3. Compare a correct result reached through invalid evidence with a supported result.
4. Design a rollback or reconciliation path for one partial failure.
5. Explain which information should be withheld from the model and why.

## Chapter Summary

Evaluate retrieval, evidence, and citations as distinct components of grounded generation. Reliable systems separate model capability from application
authority, evaluate the path as well as the answer, and preserve enough
provenance and state to explain failure.

## The Next Tale

The evidence audit revealed why the old map ranked so well: a servant had repeatedly requested the eastern road because the king once preferred it during spring floods. That preference had entered the court’s memory without a season.

<!-- next: ch15 -->

## Citations and Further Reading

- Lewis, Patrick, et al. 2020. “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.” *Advances in Neural Information Processing Systems* 33.
- Thakur, Nandan, et al. 2021. “BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models.” *NeurIPS Datasets and Benchmarks*.
