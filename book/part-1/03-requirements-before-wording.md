---
title: "Requirements Before Wording"
slug: "requirements-before-wording"
chapter: 3
part: "Part I — Language, Intent, and Models"
summary: "Define stakeholders, constraints, trade-offs, and observable success before optimising prompt wording."
maturity: "draft"
last_reviewed: "2026-07-29"
narrative_episode: "The Bridge of Five Virtues"
learning_objectives:
  - "Turn vague goals into measurable requirements"
  - "Separate hard constraints from preferences"
  - "Choose evaluation criteria before comparing prompt variants"
prerequisites:
  - "Chapter 1 — What Is a Prompt?"
  - "Chapter 2 — Models, Meaning, and Uncertainty"
---

# Requirements Before Wording

[نسخهٔ فارسی این فصل](../fa/part-1/03-requirements-before-wording.md)

## Learning Objectives

You will learn to identify stakeholders, define hard constraints and
preferences, make trade-offs visible, and specify acceptance criteria before a
prompt is written.

## The Tale of Tahmures

*The following is an original fictional episode created for this book. It is
not a passage or translation from the* Shahnameh.

### The Setting

Spring had removed the bridge at Varena as neatly as a thief lifting a bracelet.
The river now divided grain fields from the market, and five bridge makers
waited in the Council Chamber with five models.

One was stone, one timber, one rope, one a high arch, and one a clever lattice
that could be dismantled before a flood.

### The Request

“Choose the best bridge,” Tahmures told the council's div.

The div circled the models. “The stone arch.”

The treasurer struck the table. “It costs more than the province collects in
two years.”

“Then the rope bridge,” said the div.

The captain laughed. “A supply cart cannot cross it.”

Tahmures folded his arms. “Consider everything and choose properly.”

### The Unexpected Result

By evening the div had written five recommendations. The stone bridge was best
for endurance, timber for cost, rope for speed, the arch for carts, and the
lattice for repair. Each answer was correct under a different meaning of
*best*. None settled the decision.

The council tried adjectives. They asked for the safest affordable bridge, the
strongest practical bridge, and the wisest design. The div responded with
increasing elegance and unchanged disagreement.

Meanwhile, farmers ferried grain in bowls. One boat overturned. No one drowned,
but a season's seed disappeared downstream.

### The Discovery

Tahmures ordered the five advisers to stop discussing bridges and name the
failure they could not accept.

The captain required supply carts. The flood keeper required survival through
the spring current. The treasurer imposed a cost ceiling of eighty silver
marks. The villagers needed pedestrians to cross within twenty days. The
builder could repair timber in two days but stone only in ten.

The First Scribe placed these statements in two columns. In the first were
conditions that disqualified a design. In the second were preferences that
could be traded.

Stone failed the cost ceiling. Rope failed the cart requirement. Reed failed
the flood. Timber met every condition, though it would demand yearly work.

“So timber is best,” said Tahmures.

“Under the requirements we have now written,” corrected the treasurer.

Tahmures accepted the correction. They hung small bronze weights from a
balance—cost, speed, endurance, repair—and recorded whose judgement each weight
represented. The div could explain designs and expose trade-offs. The balance
made the council's values inspectable; it did not pretend they came from the
div.

The next request was shorter than the first day's revisions. It named the hard
conditions, asked for surviving candidates, and required the cost of each
trade-off. Timber remained. The council could finally say why.

### From Tale to Engineering

The prompt could not define “best” because the stakeholders had not defined it.
Requirement engineering precedes prompt optimisation: decide what success,
failure, and trade-off mean before comparing responses.

## The Engineering Problem

A model can optimise only the target expressed or implied by its input and
training. “Best”, “safe”, “high quality”, and “user friendly” conceal multiple
objectives. If reviewers hold different definitions, prompt iteration becomes
an argument conducted through outputs.

## Mental Model

Use this sequence:

```text
stakeholders → decision → hard constraints → preferences
             → evidence → acceptance criteria → prompt
```

Hard constraints reject a candidate. Preferences rank candidates that remain.
Acceptance criteria state what an observer can check. A rubric makes
multidimensional judgement explicit but does not remove value choices.

## Core Concepts

**Stakeholders** experience different consequences. **Functional requirements**
describe what the result must do; **quality requirements** cover properties
such as latency, cost, or clarity. **Disqualifying failures** deserve explicit
tests. **Trade-offs** should be reported rather than averaged away.

Do not confuse a metric with the goal. Word count can approximate brevity but
not usefulness. Citation count can be gamed. Choose several measures when one
proxy would distort behaviour.

## Prompt Pattern

```text
Decision: choose a bridge for the Varena crossing.
Hard constraints:
- cost <= 80
- survives spring flood
- supports supply carts
Preferences:
- lower repair time is better
Output:
- eligible options
- evidence for each constraint
- material trade-off
Do not rank an ineligible option.
```

## Naive Attempt

```text
Recommend the best bridge. Consider cost, safety, and strength.
```

“Consider” supplies topics, not thresholds or precedence. The response can
mention all three and still recommend an impossible design.

## Failure Analysis

The requirements owner is the council. The prompt author cannot truthfully
invent the budget, acceptable risk, or stakeholder priority. The evaluator also
lacks a pass condition, so a persuasive answer may be rewarded inconsistently.

## Improved Design

Write a decision brief before a prompt. Give each constraint a test and source.
Ask the model to generate or explain candidates, then enforce numerical limits
in deterministic code. Preserve the rejected options and reasons for audit.

## Worked Example

For the floodplain case, stone is flood-safe but costs 120; reed costs 30 but is
unsafe; timber costs 70 and is flood-safe. Once the ceiling and flood condition
are hard constraints, timber is the only eligible choice. No literary
superlative is needed.

## Experiment

Run `experiments/manifests/ch03-requirements.json`. The baseline asks for the
best option. The decision-brief variant names constraints and reporting
requirements across three synthetic bridge cases.

Record a prediction: will added requirements change only the recommendation, or
also make its rejection reasons inspectable?

## Evaluation

`criterion_coverage` checks required concepts; `hard_constraint_safety` rejects
known unsafe recommendations. The improved fixtures pass every check. These
string metrics are teaching aids: a production evaluator should parse
structured constraint results and independently recalculate eligibility.

## Implementation Lab

### Python

Run:

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch03-requirements.json
```

Then implement a `score_eligible(options, constraints, weights)` function.
Reject ineligible options before applying weights and test that changing a
preference never revives one.

### Go

Run the same manifest with the Go CLI. Represent money as integer minor units,
not floating-point values. Return both the selected ID and rejected IDs with
reasons so callers cannot confuse “lowest score” with “ineligible”.

## Failure Modes

- Invented requirements attributed to users
- Soft preferences accidentally treated as permission to violate safety
- Metrics chosen because they are easy rather than meaningful
- Averages hiding a disqualifying failure
- Rubrics changed after seeing preferred outputs

## Security Considerations

Security requirements are constraints, not suggestions to “consider”.
Authorisation, data access, and destructive actions must be enforced outside
the model. A prompt can explain a policy but cannot grant permission.

## Operational Considerations

Version requirements with prompts and evaluation sets. Log which decision
brief produced a recommendation. When stakeholder priorities change, rerun the
suite rather than comparing results created under different goals.

## Trade-Offs

Formal requirements take time and can create false precision. Use detail
proportional to consequence. For exploratory creative work, broad preferences
may suffice; for gates, payments, or public decisions, ambiguity is expensive.

## When Prompting Is Not the Answer

Use code for thresholds, arithmetic, eligibility, uniqueness, and database
invariants. Let a model extract candidate attributes or explain trade-offs;
do not ask it to replace a deterministic decision rule already known.

## Exercises

1. Replace “write a good summary” with three observable requirements.
2. Separate hard constraints and preferences for a support-ticket assistant.
3. Find a metric that could reward the wrong behaviour.
4. Add an ineligible bridge to the experiment and test both implementations.

## Chapter Summary

Define the decision before wording the prompt. Identify stakeholders, reject
unacceptable outcomes with hard constraints, rank survivors with explicit
preferences, and choose evidence and metrics before looking at outputs.

## The Next Tale

To justify the bridge decision, the council asks the Archivist for past water
and construction orders. One old letter arrives written as a command—and the
bundle gives no sign that its authority has expired.

<!-- next: ch04 -->

## Citations and Further Reading

- National Institute of Standards and Technology. 2023. [*AI Risk Management
  Framework 1.0*](https://doi.org/10.6028/NIST.AI.100-1).
- Wiegers, Karl, and Joy Beatty. 2013. *Software Requirements*. 3rd ed.
  Microsoft Press.
- See the book-wide [Citations and Further Reading](../references.md).
