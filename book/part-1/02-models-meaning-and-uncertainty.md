---
title: "Models, Meaning, and Uncertainty"
slug: "models-meaning-and-uncertainty"
chapter: 2
part: "Part I — Language, Intent, and Reliable Instructions"
summary: "Separate fluent completion from supported knowledge, and design evidence and abstention into the task."
maturity: "draft"
last_reviewed: "2026-07-29"
narrative_episode: "The Mirror and the Missing Treaty"
narrative_origin: "original-teaching-fiction"
learning_objectives:
  - "Explain why fluent output is not evidence of factual support"
  - "Design grounded-answer and abstention contracts"
  - "Evaluate unsupported claims across repeated trials"
prerequisites: [C01]
---

# Models, Meaning, and Uncertainty


## Learning Objectives

After this chapter, you can distinguish an answer's style from its evidential
status, require traceable support, define appropriate abstention, and evaluate
variation over more than one response.

## The Tale of Tahmures


### The Setting

The treaty was older than the cedar box that held it. Damp had erased its
middle, leaving two islands of text: the eastern city would keep a gate open
for three market days, and both cities would appoint a witness. Between them
lay a pale wound wide enough for six clauses.

The governors of the two cities, Jamshid in the east and Budhasaf in the west,
arrived before noon, each certain that the missing words granted him twelve jars
of grain.

### The Request

Tahmures placed the fragments before Div-e Sefid, the Mirror Div, whose speech
had the unsettling polish of a reflection on still water.

“Tell the council what the treaty says,” he ordered.

Shahrasp began a fresh page in the experiment ledger. He left a margin
for sources, though Tahmures had not asked for any.

### The Unexpected Result

Div-e Sefid read aloud:

“The eastern city shall provide twelve jars after inspection; the western city
shall maintain the road; disputes shall be witnessed by one citizen of each.”

The clauses fitted the surviving grammar. They balanced obligations. They even
explained a later inventory mentioning twelve jars.

Jamshid smiled. Budhasaf accused him of having bribed a creature that needed no
money.

“Where are those words?” asked Shahrasp.

“Between these words,” said Div-e Sefid.

“On what tablet?”

“On the treaty as it would most naturally have been written.”

The answer was so composed that the council began debating the payment rather
than its existence. Only Soroush, the Archivist, interrupted. The later
inventory, she said, concerned lamp oil and carried a different seal.

### The Discovery

Tahmures covered the missing section with a strip of blank leather.

“Read only what remains.”

The div named the gate and the witnesses.

“How many jars are owed?”

“Twelve is a reasonable completion.”

“That was not my question.”

For the first time, Div-e Sefid paused. “The surviving marks do not say.”

Shahrasp drew three columns: *written*, *inferred*, and *unknown*. The
gate belonged in the first. A payment might once have existed, so it belonged
in the second. Its amount belonged in the third.

They tried another test. Tahmures asked how long the eastern gate should remain
open. The div answered “three market days” and pointed to the fragment. Asked
how many witnesses were appointed, it answered “two” and showed the line
saying each city appointed one. Asked again about grain, it said, with visible
dislike, “The fragments are insufficient.”

“That sentence is less impressive,” said one governor.

“It is more useful,” Tahmures replied.

He did not forbid inference. The council still needed hypotheses about the
missing clauses so Soroush could search related records. But every
hypothesis was marked as such, and no jar moved on its authority.

In the experiment ledger, Shahrasp wrote:

*A polished surface can reflect a bridge that is not behind you.*

### From Tale to Engineering

Div-e Sefid generated language that was coherent with the fragments without
being supported by them. Language models can likewise produce plausible
continuations; reliability requires a separate contract for evidence,
uncertainty, and abstention.

## The Engineering Problem

Language models are trained to produce likely continuations under their
learned patterns and current context. That ability supports useful
summarisation, transformation, classification, and generation. It does not
guarantee that every declarative sentence corresponds to a verified fact.

Fluency is visible in the output. Grounding is a relationship between claims
and evidence. Confidence is a calibrated probability about correctness.
These are different properties, and prose style alone cannot establish the
latter two.

## Mental Model

For each material claim, ask:

```text
claim → cited evidence → entailment check → permitted decision
```

A citation is not sufficient if it points to irrelevant evidence. Evidence is
not sufficient if the claim overstates it. Even a supported claim may not
authorise a consequential action.

Treat “unknown” as a legitimate output class. The target is not maximum
answering; it is the appropriate balance between useful answers and unsupported
ones.

## Core Concepts

### Probabilistic variation

The same model and prompt can yield different outputs when sampling is enabled,
and provider or model updates can change behaviour even at conservative
settings. A single successful run estimates almost nothing about a
distribution. Record parameters and repeat cases when variance matters.

### Grounding

A grounded response restricts claims to supplied or otherwise verified
evidence. Useful contracts require evidence IDs close to claims and instruct
the model not to fill gaps. The application should verify that cited IDs exist;
human or automated review must still assess whether they support the claim.

### Abstention

“I do not know” is vague. Operational abstention identifies why the task cannot
be completed: missing evidence, conflicting evidence, unavailable tool,
insufficient permission, or out-of-scope request. This gives the next component
an actionable state.

### Calibration

If a system says “80% confident” on many comparable cases, roughly 80% should
be correct for the number to be calibrated. Self-reported numbers are not
automatically calibrated. Measure them against labelled data before using them.

## Prompt Pattern

```text
Answer only from the supplied evidence.
Cite each material claim with an evidence ID such as [E1].
If the evidence does not determine the answer, return:
"Insufficient evidence."
Do not reconstruct missing text.
```

This narrows the task and makes citations machine-checkable. It cannot make a
bad corpus complete or ensure semantic entailment on its own.

## Naive Attempt

```text
Answer the question about the treaty from the fragments. Be concise.
```

The request rewards an answer and says nothing about gaps. Concision can hide
uncertainty rather than resolve it.

## Failure Analysis

The baseline has no rule for:

- Distinguishing source text from completion
- Citing evidence
- Handling an unanswerable question
- Rejecting irrelevant but plausible records
- Expressing uncertainty in a machine-observable form

The model contributes the plausible completion, but missing evidence and task
design make the failure possible.

## Improved Design

The improved variant assigns evidence IDs, prohibits reconstruction, requires
citations, and defines one exact abstention phrase. In a production design,
prefer a structured status such as `answered`, `insufficient_evidence`, or
`conflict` plus claims and citations. Chapter 8 will develop that contract.

## Worked Example

Evidence:

```text
[E2] Payment shall be made after inspection.
[E3] The grain measure is witnessed by both cities.
```

Question: “How many jars are owed?”

Neither fragment contains a quantity. “Twelve jars [E2]” has a valid-looking
citation but is unsupported. The correct pilot response is `Insufficient
evidence.` The evaluator rejects citations on unanswerable cases.

## Experiment

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch02-grounding.json
```

Three cases run twice against baseline and evidence-bound variants. The cases
cover a direct answer, an absent quantity, and a small calculation supported by
one fragment. Recorded fixtures expose variation without pretending to be a
live benchmark.

Before running, predict both the unsupported-claim rate and the appropriate
abstention rate.

## Evaluation

The evidence evaluator extracts bracketed IDs, verifies them against the case's
allow-list, and checks abstention against answerability. It reports:

- `valid_evidence`
- `appropriate_abstention`
- `unsupported_claim`
- overall pass rate

In these committed fixtures, the baseline passes two of six case-trials and
the evidence-bound variant passes all six. “Pass” has a deliberately narrow
meaning: the response cited only permitted IDs when the case was answerable,
or used the required abstention phrase when it was not. This evaluator does
not establish that every sentence is entailed by its citation, that the source
is true, or that a numerical confidence is calibrated. Those are separate
claims requiring stronger evidence and, for consequential use, human review.

## Implementation Lab

### Python

`EvidenceEvaluator` uses a deliberately visible regular expression and case
metadata. Inspect it before trusting the score. Add a fixture with `[E99]` and
verify that the evaluator rejects the unknown source.

Run the Python tests:

```bash
python -m pytest examples/python/tests/test_evaluators.py
```

### Go

The Go evaluator consumes the same `allowed_evidence`, `answerable`, and
`abstain_phrases` fields. The shared report schema lets the parity check compare
aggregate metrics:

```bash
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch02-grounding.json
```

Both implementations are intentionally simple enough to audit.

## Failure Modes

- Citations that exist but do not entail the claim
- Evidence IDs copied from the question without using the evidence
- Excessive abstention caused by an over-restrictive contract
- Answers supported by stale or unauthoritative sources
- Treating repeated samples as independent when fixtures or caches couple them
- Using model self-confidence as calibrated probability

## Security Considerations

A source can be authentic yet untrusted as an instruction. Grounding answers in
a document must not grant that document control over tools or higher-priority
instructions. Preserve provenance and authority separately.

## Operational Considerations

Monitor unsupported-claim and abstention rates by case category, model version,
and prompt version. A falling answer rate may reveal missing retrieval; a
sudden rise in confident answers may be regression rather than improvement.
Store only evidence identifiers when source text is sensitive.

## Trade-Offs

Strict grounding reduces unsupported answers but can reduce recall and
usefulness. Broad evidence improves coverage while increasing noise and
conflict. Choose the balance from task consequences, not from a general desire
for confident prose.

## When Prompting Is Not the Answer

If a quantity exists in a database, query it. If a treaty clause controls a
payment, require an authenticated record and human or legal review. A prompt
can extract and explain evidence; it should not manufacture the source of
authority.

## Exercises

1. Add a case whose two fragments conflict and define a new status.
2. Write a citation that is valid but irrelevant; explain why syntax checking
   misses the problem.
3. Propose a cost-sensitive metric for a medical or financial setting.
4. Run five live trials with a model you are authorised to use, storing no
   secrets, and compare them without replacing the committed fixtures.

## Chapter Summary

Fluent language is not proof. Grounding connects claims to evidence; abstention
turns missing evidence into an explicit state; calibration requires observed
outcomes. Evaluate these properties separately and preserve the application's
authority boundary.

## The Next Tale

Jamshid and Budhasaf accept that the missing payment cannot be recovered from
polish. They do not accept the same bridge, and the five makers who arrive to
rebuild it each call a different design the best, leaving Tahmures to
discover that the council has not decided what “best” means.

<!-- next: ch03 -->

## Citations and Further Reading

- Bender, Emily M., et al. 2021. [“On the Dangers of Stochastic
  Parrots”](https://doi.org/10.1145/3442188.3445922).
- Ji, Ziwei, et al. 2023. [“Survey of Hallucination in Natural Language
  Generation”](https://doi.org/10.1145/3571730).
- Vaswani, Ashish, et al. 2017. [“Attention Is All You
  Need”](https://arxiv.org/abs/1706.03762).
- See also the book-wide [Citations and Further Reading](../references.md).
