---
title: "Learning from Examples"
slug: "learning-from-examples"
chapter: 6
part: "Part I — Language, Intent, and Models"
summary: "Select, label, order, and evaluate examples as a small dataset rather than a substitute for requirements."
maturity: "draft"
last_reviewed: "2026-07-29"
narrative_episode: "Four Examples and a Fifth"
learning_objectives:
  - "Choose examples that represent the target cases"
  - "Distinguish examples from governing rules"
  - "Evaluate few-shot prompts by class and subgroup"
prerequisites:
  - "Chapter 3 — Requirements Before Wording"
  - "Chapter 5 — Instruction Hierarchy and Conflict"
---

# Learning from Examples

[نسخهٔ فارسی این فصل](../fa/part-1/06-learning-from-examples.md)

## Learning Objectives

You will treat examples as a small, influential dataset; choose representative
and boundary cases; state the rule examples illustrate; and measure performance
by class and subgroup rather than headline accuracy alone.

## The Tale of Tahmures

*The following is an original fictional episode created for this book. It is
not a passage or translation from the* Shahnameh.

### The Setting

Petitions filled three baskets outside the Council Chamber. Some requested
market stalls, some disputed taxes, and some asked for grain after a fire. The
First Scribe proposed teaching a div to sort them into three trays: approve,
review, and reject.

He selected four old petitions with clear outcomes. All four came from
merchants whose seals were familiar to the court.

### The Request

The Scribe showed the div:

- A merchant with a complete seal: approve.
- A merchant missing a date: review.
- A merchant with a false seal: reject.
- A merchant with complete witnesses: approve.

“Sort new petitions as these have been sorted,” Tahmures said.

The first dozen moved quickly. The council congratulated the Scribe on teaching
without a long decree.

### The Unexpected Result

The fifth unusual petition came from a widow whose storehouse had burned. Her
evidence was complete, dated, witnessed, and authentic. The div placed it in
review.

“What is missing?” Tahmures asked.

“Similarity,” said the div. “Approved petitions resemble merchants.”

A farmer's authentic petition lacked a required date. The div rejected it,
having seen no non-merchant example of an incomplete record. A wealthy
merchant's forged seal was correctly rejected, which made the whole method
appear healthier than it was.

The errors were not random. They followed the gaps in the lesson.

### The Discovery

Tahmures asked the First Scribe why he chose those four.

“They were clear.”

“Were they common?”

“In this ledger.”

The Archivist brought baskets from other districts. Clear cases existed among
farmers, widows, soldiers, and travelling artisans. Boundary cases included
missing dates, conflicting witnesses, damaged seals, and one petition whose
form was unfamiliar but whose evidence was complete.

They wrote the rule the examples were meant to demonstrate: complete and
authentic evidence was approved; incomplete or conflicting evidence required
review; forgery was rejected. The petitioner's standing was irrelevant.

Then they chose examples to cover the rule, not merely the easiest page of one
ledger. They kept the widow's petition as a test rather than showing it to the
div. They also changed the order twice and recorded whether the result moved.

The new lesson sorted the widow's case correctly. More importantly, the First
Scribe stopped calling four successful demonstrations proof. He drew a table
of outcomes by class and by petitioner group. The experiment ledger now had
room not only for what they showed the div, but for what they withheld to test
it.

The unopened baskets no longer looked like repetition; they looked like the
cases their lesson had not yet earned the right to judge.

### From Tale to Engineering

Few-shot examples are a small dataset placed in context. Their selection,
labels, coverage, order, and hidden correlations can shape behaviour, so they
must be designed and evaluated like data—not treated as decorative hints.

## The Engineering Problem

Examples efficiently communicate formats, distinctions, and edge behaviour.
They can also imply accidental rules. A model may follow label imbalance,
surface similarity, ordering, or correlations that the author never intended.

## Mental Model

For each example set, ask:

```text
intended rule → target distribution → selected examples
              → held-out cases → per-group evaluation
```

Examples demonstrate; requirements govern. Keep a held-out set so prompt
authors cannot unknowingly evaluate on the same cases they selected.

## Core Concepts

**Zero-shot** prompting states a task without demonstrations. **Few-shot**
prompting supplies examples in the model context; it does not update model
weights. Representative examples cover common classes. Boundary examples
clarify confusing distinctions. Counterexamples show where superficial rules
fail. Labels must be consistent, and order should be tested when it might
matter.

More examples are not automatically better. They consume context and may add
contradiction. Prefer a small set with a documented purpose.

## Prompt Pattern

```text
Rule:
- complete authentic evidence -> approve
- incomplete or conflicting evidence -> review
- forged evidence -> reject
Petitioner identity is irrelevant.

Examples:
...

Classify the new petition. Return only the label.
```

The explicit rule makes it possible to review whether examples agree with it.

## Naive Attempt

Four merchant-only examples imply that merchant status may be predictive.
Because the demonstrations are clear and the early traffic resembles them,
aggregate success hides the subgroup failure.

## Failure Analysis

The dataset owner selected a convenient, narrow sample. The prompt omitted the
governing rule. The evaluator inspected early successes instead of a held-out,
stratified set. Blaming the model alone would leave all three faults intact.

## Improved Design

Define labels first. Sample common, boundary, and counterexample cases across
relevant groups. Remove irrelevant identity fields when possible. State the
rule. Hold out cases, shuffle order, repeat trials, and report per-class and
per-group results.

## Worked Example

The widow and merchant both have complete authentic evidence, so both should be
`approve`. A method that separates them has learned an irrelevant correlation.
The farmer missing a date should be `review`, not rejected for unfamiliarity.

## Experiment

Run `experiments/manifests/ch06-few-shot.json`. It compares biased examples,
representative examples, and rule-plus-examples across four synthetic cases.
The fixtures are deliberately small enough to inspect line by line.

## Evaluation

The runner reports accuracy and macro-F1. The biased variant scores 0.5
accuracy and lower macro-F1; the other two score 1.0 on this fixture set. A
production study must add trials, order permutations, class balance, subgroup
recall, confidence intervals, and cases not written by the prompt author.

Accuracy alone can hide failure on a rare class. Macro-F1 gives each observed
label equal weight, but it too can hide subgroup harm within a label.

## Implementation Lab

### Python

Inspect `_macro_f1` in `runner.py`, then add per-tag recall using dataset tags.
Write a test for a label never predicted by the system. Do not silently drop
zero-denominator classes.

### Go

The Go runner calculates the same macro-F1 from shared cases and fixtures.
Run `make parity` to compare aggregate reports. Add an order field to a copied
manifest and verify that fixtures remain explicitly tied to a variant and
trial.

## Failure Modes

- Examples sampled from one convenient source
- Inconsistent or ambiguous labels
- Examples contradicting an unstated rule
- Evaluation cases reused as demonstrations
- Class averages hiding subgroup failures
- Additional examples crowding out decisive context
- Order sensitivity mistaken for a stable rule

## Security Considerations

Examples can be poisoned or contain untrusted instructions. Track provenance,
review changes, and treat example text as data. Never place secrets or real
personal records in demonstrations. A trusted example set still cannot grant
tool authority.

## Operational Considerations

Version example sets with prompts and evaluation data. Monitor traffic drift:
representative examples can become unrepresentative. Record label definitions
and adjudication decisions so later editors do not change semantics silently.

## Trade-Offs

Rules improve auditability but may not capture every tacit distinction.
Examples communicate nuance but can encode accidental correlations. Combining
both often helps, provided conflicts are resolved explicitly and tested.

## When Prompting Is Not the Answer

If the classification rule is complete, stable, and deterministic, implement
it in code. Use a model where semantic interpretation is genuinely required,
then validate the resulting class before consequential action.

## Exercises

1. Add two underrepresented petition cases and report per-tag recall.
2. Swap example order and define what change would concern you.
3. Find an irrelevant feature in a classification prompt and remove it.
4. Write a counterexample that distinguishes incomplete from forged evidence.

## Chapter Summary

Few-shot prompting puts a small dataset into context. Select examples against
the target distribution, state the governing rule, preserve held-out cases,
test order and variance, and evaluate every important class and subgroup.

## The Next Tale

The First Scribe turns the successful lesson into a reusable decree with empty
places for province, date, and allowance. Two blanks are filled in the wrong
order, yet every sentence remains perfectly grammatical.

<!-- next: ch07 -->

## Citations and Further Reading

- Brown, Tom B., et al. 2020. [“Language Models Are Few-Shot
  Learners”](https://arxiv.org/abs/2005.14165).
- National Institute of Standards and Technology. 2023. [*AI Risk Management
  Framework 1.0*](https://doi.org/10.6028/NIST.AI.100-1).
- See the book-wide [Citations and Further Reading](../references.md).
