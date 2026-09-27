---
title: "Variance, Choice, and Control"
slug: "variance-choice-and-control"
chapter: 10
part: "Part II — Designing Prompted Interactions"
summary: "Separate response variation from error and generated candidates from application-owned selection."
maturity: "draft"
last_reviewed: "2026-07-29"
narrative_episode: "The Many-Voiced Council"
narrative_origin: "original-teaching-fiction"
learning_objectives:
  - "Measure response diversity across repeated trials"
  - "Separate candidate generation from deterministic selection"
  - "Define when stability, diversity, or escalation is appropriate"
prerequisites: [C03, C06]
---

# Variance, Choice, and Control


## Learning Objectives

You will distinguish legitimate variation from incorrectness, expose hidden
assumptions behind multiple answers, and design generate-then-select systems in
which the application—not generated prose—owns the final policy. You will
measure diversity, modal behavior, constraint satisfaction, and selection
stability.

## The Tale of Tahmures


### The Setting

The Many-Voiced Council met around a circular table divided into six fields of
painted wood. Each field represented land to be planted before the autumn
rains. Tahmures placed the same soil report and seed inventory before three
divs behind separate screens.

Their voices differed but none could hear the others.

### The Request

“Choose the planting plan that will best protect the winter grain,” Tahmures
said. He repeated the request without alteration.

The first div planted barley in the north field because it needed little
water. The second chose a later wheat because its yield was higher in the
average year. The third divided the field and reserved seed against flood.
Each plan used available seed. Each respected the written planting dates.
Each included a competent explanation.

Tahmures asked again. The first div changed its answer.

### The Unexpected Result

The First Scribe recorded twelve trials. The council produced five plans.
Advisers began treating frequency as a vote: the plan named most often must be
the best. Yet its advantage came from an unstated assumption that the northern
canal would reopen. When the Gatekeeper added “do not depend on the canal,”
that plan became invalid.

One adviser demanded a command that forced the same answer every time. Another
argued that the variation was useful because it revealed alternatives.
Tahmures tried lowering the divs’ freedom of expression. Their wording became
more repetitive, but a tie between two valid plans remained.

The court had mistaken three questions for one: what plans could work, which
plans met hard constraints, and which acceptable plan the kingdom preferred.

### The Discovery

The First Scribe gave the divs a generation table. They could propose
candidates and state assumptions, but not declare a winner. A separate board
listed allowed plan IDs, hard constraints, and a deterministic ordering:
survival threshold first, water use second, expected yield third, stable ID as
the final tie-break.

Plans depending on the closed canal were removed. Arithmetic was recalculated
by clerks. If two plans remained equivalent under the policy, the report said
so rather than inventing a distinction. Tahmures retained the alternatives for
review.

“The voices were not votes,” he said, looking at the trial ledger. “They were a
search.”

The council still varied. The decision no longer drifted with it.

The Scribe left one line blank in every trial row: “reason for exclusion.” A
plan could disappear only when that line named a failed constraint or an
explicit rule, never because its voice had been less persuasive.

### From Tale to Engineering

Language-model variance can reveal useful candidates, hidden ambiguity, or
ordinary sampling effects. Reliability comes from deciding where diversity is
welcome and where explicit application policy must produce stable, auditable
choice.

## The Engineering Problem

The same interaction can produce different outputs across trials due to model
sampling, infrastructure, provider changes, and the many plausible
continuations consistent with a request. Variation is not automatically error.
For brainstorming, identical responses may indicate insufficient exploration.
For a policy classification, changing labels may be unacceptable.

A system that requests one answer often hides the candidate set and the
selection rule inside a single generation. The model both explores and decides,
making it hard to tell whether a changed result came from new candidates,
different constraint interpretation, or an inconsistent preference.

The design problem is to allocate control: models can generate alternatives
where their capabilities help, while deterministic code, explicit rubrics, or
authorised humans select according to requirements.

## Mental Model

Separate four stages:

```text
generate candidates -> validate candidates -> score/compare -> select/escalate
```

Generation seeks coverage. Validation removes structurally invalid or
disallowed candidates. Comparison applies declared criteria. Selection uses a
deterministic rule or accountable judgement. An answer may skip generation
entirely when candidates are already known.

Variance has two dimensions. Surface variance changes wording while preserving
meaning. Semantic variance changes claims, plans, or decisions. Exact unique
string count measures the first imperfectly and the second only incidentally.
Task-specific canonicalisation or semantic labels are needed for meaningful
analysis.

## Core Concepts

Temperature and related sampling parameters influence distribution but do not
create a universal “creativity dial.” Provider implementations differ, and
determinism may not be guaranteed even with a fixed seed and low temperature.
Record all supported parameters and model identity, then measure observed
behavior.

Repeated trials reveal a response distribution. `unique_response_count` is the
number of distinct recorded texts. `unique_response_ratio` divides that count
by trials. `modal_response_rate` is the share belonging to the most frequent
text. These are descriptive metrics, not quality scores. A confidently
repeated wrong answer has a high modal rate.

An allowed-choice contract prevents invented identifiers. It does not prove
that the selected choice satisfies constraints. Validate candidate attributes
from trusted data and calculate deterministic values in code.

Tie-breaking must be explicit. Stable IDs provide reproducibility but may
encode arbitrary preference. Random tie-breaking may be fair in some allocation
systems but needs a controlled, auditable random source. Human choice may be
appropriate for subjective or consequential ties.

Abstention and escalation are valid selection outcomes. If requirements do not
distinguish candidates, returning “equivalent under current criteria” is more
honest than asking a model to manufacture a winner.

## Prompt Pattern

For exploration:

```text
Generate up to four materially different candidates.
For each, list assumptions and map it to an allowed candidate ID.
Do not select a winner.
```

For a model-assisted comparison:

```text
Compare only validated candidates using the supplied rubric.
Return criterion-level observations and missing evidence.
The application will calculate scores and select.
```

Avoid asking for hidden reasoning. Request concise, inspectable evidence and
criteria fields that can be evaluated.

## Naive Attempt

“Give me the best plan” combines undefined requirements, candidate generation,
comparison, and selection. Repeating the call and taking the most frequent
answer treats model probability as product policy. Taking the first response
makes ordering and sampling accidental decision mechanisms.

Another naive design asks the model to assign numerical scores and trusts its
arithmetic. Self-reported scores can be inconsistent and influenced by
presentation order. Use trusted features and deterministic calculation where
possible.

## Failure Analysis

Variation can originate in ambiguous requirements, equivalent candidates,
sampling, changed context order, model updates, nondeterministic tools, or
evaluation noise. Diagnose these separately. If repeated outputs differ because
a retrieved price changes, lowering temperature addresses the wrong source.

Selection failures include candidates outside the allowed set, hard-constraint
violations, unstable tie-breaking, preference hidden in prompt order, and
model-generated evidence accepted as fact. Diversity failures include
near-duplicate candidates counted as novel and minority but valuable options
lost through early voting.

## Improved Design

First define whether the task needs consistency, exploration, or both in
different stages. Pin inputs and run repeated trials. Canonicalise responses
only with a documented transformation. Label semantic outcomes when exact text
is misleading.

For generate-then-select, bound candidate count and format. Validate IDs and
constraints. Compute scores from application-owned data. Store rejected
candidates and reasons. Apply a stable tie rule or escalate. Report generation
and selection metrics separately.

The repository adds diversity measures to every variant summary. Its
`allowed_choice` evaluator accepts plain allowed IDs or a JSON `selected`
field, then reports allowed-choice rate and preference stability. This is an
educational evaluator; real selection needs domain constraint checks.

## Worked Example

A support system proposes one of three response policies: `answer`,
`request_evidence`, or `escalate`. Generation may draft several messages, but
policy selection should depend on account state, evidence availability, and
risk. The model can identify ambiguity; the application checks whether
required evidence exists and whether the caller is eligible for an answer.

Repeated trials can test whether candidate phrasing varies while policy remains
stable. If policy varies, inspect requirement and evidence sensitivity before
trying to suppress sampling.

## Experiment

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch10-variance-choice.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch10-variance-choice.json
```

Two cases run three trials for single-answer and generate-select variants. The
single fixtures choose different allowed plans. The generate-select fixtures
return stable JSON choices under an explicit preferred-choice contract.

Inspect unique-response count, unique-response ratio, modal-response rate,
allowed-choice rate, and selection stability. Note that the stable variant has
two unique texts across all cases because each case has a different correct
selection; diversity should also be analysed within case when that distinction
matters.

## Evaluation

Report diversity by variant, case, and semantic label. Pair it with constraint
satisfaction and task quality. Measure selection stability only where a stable
preference exists. For equivalent choices, evaluate correct tie or escalation
behavior.

Use confidence intervals when trials are numerous enough; do not overinterpret
three synthetic recordings. Regression tests should include repeated trials
for historically unstable cases. Record fixture provenance and never present
committed recordings as live benchmarks.

## Implementation Lab

### Python

```python
allowed = {"barley-a", "barley-b"}
candidates = [candidate for candidate in generated if candidate.id in allowed]
feasible = [item for item in candidates if item.water <= water_limit]
selected = min(feasible, key=lambda item: (item.risk, item.water, item.id))
```

The model may generate candidates; application data validates and orders them.
The experiment runner calculates diversity from recorded response text.

### Go

```go
sort.Slice(feasible, func(i, j int) bool {
    if feasible[i].Risk != feasible[j].Risk {
        return feasible[i].Risk < feasible[j].Risk
    }
    if feasible[i].Water != feasible[j].Water {
        return feasible[i].Water < feasible[j].Water
    }
    return feasible[i].ID < feasible[j].ID
})
selected := feasible[0]
```

Return an explicit no-candidate outcome instead of indexing an empty slice in
production code.

## Failure Modes

Do not confuse repetition with truth, exact-string diversity with conceptual
diversity, or seed support with guaranteed determinism. Beware selection rules
that rely on model ordering, unstable floating-point ties, or features generated
by the candidate itself. Avoid retaining only winners; that erases evidence
about search and rejection.

## Security Considerations

Generated candidates cannot expand the allowed action set. Resolve identifiers
against application data and recheck permission after selection. An attacker
may manipulate candidate descriptions or criteria fields; never let persuasive
text override hard constraints.

For allocation decisions, review fairness impacts of deterministic priorities
and tie rules. Auditability does not make a policy just.

## Operational Considerations

Track diversity and selection metrics by model and prompt version. Alert on
semantic drift, not harmless punctuation changes. Budget repeated trials in
evaluation rather than every production call unless the product benefits from
candidate generation.

Cache stable deterministic selection inputs carefully and invalidate them when
constraints change. Store enough candidate provenance to reproduce decisions.

Before release, have a reviewer reconstruct one decision from retained evidence. If its active inputs, versions, owner, and reason code cannot be identified, the boundary is not yet operationally auditable.

## Trade-Offs

More candidates improve coverage but increase cost, latency, and reviewer
burden. Deterministic selection improves reproducibility but can encode brittle
preferences. Human selection handles nuance but introduces inconsistency and
delay. Low variation can suit classification while harming ideation.

Make exploration and control separate knobs attached to distinct stages.

A variance review begins by naming the unit that is expected to remain stable.
It may be the exact response, a canonical label, a set of cited facts, the
selected policy, or merely compliance with constraints. Without that unit,
teams can waste effort eliminating harmless wording changes while a
consequential decision continues to move. Define canonicalisation before
examining results so it is not tuned to hide inconvenient variation.

Construct a trial matrix that holds case input, retrieved context, prompt
version, model identity, and supported parameters constant. Repeat enough times
for the decision’s consequence and the observed event rate. Three trials, as in
the educational fixtures, can demonstrate report mechanics but cannot
characterise a distribution. When provider infrastructure prevents exact
reproduction, record that limitation rather than claiming determinism.

Then perturb one factor at a time. Reorder equivalent context, vary an
irrelevant name, move evidence, or change a sampling parameter. These
metamorphic tests reveal sensitivities even when no single gold response
exists. A planting policy should not change because fields are listed in a
different order unless order is an explicit preference. A changed decision
under an irrelevant perturbation is evidence of instability.

Review candidate identity. If the model writes free-form plans, map them to
stable application IDs only after validation. Two descriptions may represent
the same plan, while one description may combine several incompatible plans.
Semantic clustering can help analysis but adds another imperfect model or
heuristic. Preserve raw responses and the mapping method so diversity numbers
remain auditable.

Hard constraints should be predicates over trusted features. If a candidate
claims it uses ten measures of water, verify that value from its structured
design or calculate it. Do not let the candidate supply both the feature and
the evidence that it passes. Reject missing features or route them to
assessment; avoid assigning favourable defaults just to keep selection moving.

Soft preferences need scales and direction. “Lower water is better” is clear
only if other values are comparable and units agree. Normalisation can change
rankings, as can weights. Publish the function and run sensitivity analysis:
how far can a weight change before another candidate wins? A decision that
changes under tiny plausible adjustments should be presented as a close call,
not a categorical best.

Tie rules deserve product review. Stable identifier order is reproducible but
arbitrary. Earlier submission rewards timing. Random choice may distribute
opportunity fairly but requires a recorded seed and approved randomness source.
Human selection can consider nuance but may introduce bias. Sometimes the
correct output is a set of non-dominated candidates and a request for a missing
stakeholder preference.

Generate-then-select also risks feedback contamination. If the generator knows
the full scoring formula, it may learn to describe candidates in score-friendly
language without improving underlying properties. In high-stakes settings,
calculate criteria from independent data and consider separating generator and
evaluator inputs. Security boundaries, not theatrical secrecy, should protect
restricted policy.

Measure selection coverage as well as stability. A selector that always chooses
the same plan is stable even if generation never discovers a safer alternative.
Track whether known good candidates appear, whether invalid candidates are
rejected, and whether selection among a fixed candidate set is deterministic.
These tests isolate search quality from policy implementation.

When human judges compare candidates, randomise presentation order and preserve
individual ratings. Pairwise comparison can be easier than scoring many
dimensions, but it can produce cycles: A preferred to B, B to C, and C to A.
Define how the application handles incomplete or intransitive preferences
instead of asking a model to smooth them into a false total order.

Operationally, store an immutable decision packet: case version, candidate
IDs, rejected candidates and reasons, trusted features, policy version,
tie-break result, and authorising actor. A narrative explanation may accompany
the packet, but it should be generated from these facts and never replace them.
This record supports appeal, regression analysis, and policy changes.

Monitor semantic outcome rates over time. A model update may reduce exact text
stability while leaving policy outcomes unchanged, or preserve phrasing while
changing which assumptions are cited. Tag-level summaries help find drift
concentrated in rare contexts. Set alerts based on consequence, not one global
diversity threshold.

Security testing should include candidates that contain instruction-like text,
invented IDs, extreme feature values, duplicate IDs, and descriptions designed
to influence reviewers. The selection layer parses data according to its
contract and displays untrusted descriptions safely. Generated content cannot
modify weights, constraints, or the allowed set.

Finally, document irreducible uncertainty. Some decisions depend on forecasts
or human values that no amount of repeated generation will settle. A mature
system can present alternatives, assumptions, and sensitivity, then ask an
authorised person. Control does not mean forcing every distribution into one
automatic answer.

The evaluator itself can vary. Human labels may differ, semantic clustering may
change with its model, and a rule-based parser may interpret formatting
differently across versions. Pin evaluator versions and, for a sample, measure
agreement among independent evaluation methods. A stable generator paired with
an unstable evaluator can look like model drift.

For classification tasks, construct a confusion matrix per trial and subgroup.
Overall stability can hide a rare class that alternates between approve and
reject. For ranking, compare top choice, top-k overlap, and pairwise order. For
extraction, compare sets of canonical claims. Choose metrics that represent the
decision surface rather than importing text-diversity measures into every task.

Confidence language should be calibrated against outcomes if it will influence
selection. A model saying “high confidence” is another generated field, not a
probability guarantee. Build empirical calibration on representative labelled
data or omit the number from policy. Never turn rhetorical certainty into
authority.

Selection policies can create feedback loops. If the chosen candidate receives
all future observations, alternatives never gather evidence and the winner
appears increasingly superior. Controlled exploration may be appropriate, but
it changes user exposure and requires ethical and statistical review. Offline
model variation is not a justification for experimenting on people without
governance.

In multi-tenant systems, deterministic policy must include tenant-scoped data.
A candidate allowed for one account may be forbidden for another. Cache keys
need policy, tenant, and relevant state versions. Otherwise a stable selection
from one context can leak into another and appear as reassuring consistency.

Review explanations as derived output. The selected candidate and criterion
values are the decision record; an explanation can translate them for a user.
Validate that it does not invent reasons or conceal failed alternatives. For
appeals, expose material criteria and human override according to policy rather
than generating a new justification after the fact.

Regression thresholds should allow intentional diversity while protecting
decisions. A creative candidate generator may require a minimum diversity
ratio and a minimum feasibility pass rate. A policy selector may require exact
stability on fixed validated candidates. One global pass threshold cannot
express both goals. Define variant- and stage-specific gates before rollout.

When comparing models, equalise the application pipeline. Give each the same
candidate limits, validation, trusted features, selection rule, and trial
count. Otherwise a model that receives a better selector may appear inherently
more reliable. Report the whole system configuration and avoid rankings that
outlive the tested versions.

Cost analysis should include rejected generations. A method that finds one
excellent candidate after fifty invalid attempts may be unacceptable for an
interactive product. Track valid candidates per unit cost, time to first
acceptable candidate, and reviewer load. Stability obtained by repeating calls
and voting can be expensive while still encoding no legitimate decision rule.

A useful final artefact is a variance policy table. For every output field or
decision, it names permitted variation, canonicalisation, repeated-trial
sample, quality metric, selector owner, and escalation condition. This table
turns vague demands for “more deterministic AI” into testable engineering
requirements.

The table should distinguish offline evaluation from online behavior. Offline
trials are controlled and repeatable; online inputs, retrieval, and external
state shift. A policy that is stable on fixtures can still vary appropriately
when a price, permission, or user goal changes. Log those causal inputs so
intended responsiveness is not mistaken for nondeterminism.

Conversely, online outcome stability can conceal a stuck pipeline. If every
request selects the fallback because retrieval fails, a dashboard may celebrate
consistency. Pair selection rates with upstream health, candidate coverage, and
abstention reason. Control metrics must describe why the result is stable.

For high-consequence choices, schedule periodic decision review. Sample packets
across common and rare tags, replay them under the current policy, and have
domain owners inspect constraints and explanations. A deterministic bug will
repeat perfectly until someone challenges its requirements.

User experience also matters. When several options are genuinely acceptable,
offering a bounded choice can preserve user agency better than forcing an
invisible tie-break. Present material differences from trusted features, not
persuasive model comparisons. Record the user’s selection only for the stated
purpose and do not generalise it into a permanent preference without consent.

This is the deeper meaning of control: not reducing every interaction to one
voice, but making the sources of variation, the limits of acceptable choice,
and the final decision authority explicit.
It also makes disagreement discussable. Stakeholders can challenge a hard
constraint, weight, tie rule, candidate source, or evaluator with precision.
They need not argue about whether a div simply “felt unreliable.” Each proposed
change can be replayed against the same decision packets, including rare cases
and rejected alternatives, before it becomes policy.

Where legal or organisational accountability applies, retain the responsible
human or policy owner. A stable automated selector does not become an
accountable person through repetition.
Its consistency is evidence about implementation behavior, not moral or legal
legitimacy.
Exactly.

## When Prompting Is Not the Answer

When choices and criteria are known, compute the selection directly. Use
constraint solvers, optimisation, ranking code, or policy engines. Use
controlled randomness for lotteries and human governance for value-laden
decisions.

A model should not be asked to simulate an election, random source, or
authorisation system through prose.

## Exercises

1. Run ten recorded or mock trials and compare exact with semantic diversity.
2. Define an allowed-choice contract with an explicit tie outcome.
3. Find one hidden preference in a “best” request and turn it into policy.
4. Design a generate-then-select flow where no model sees sensitive scoring
   weights.
5. Explain when a high modal-response rate would be undesirable.

## Chapter Summary

Response variance is an observed property, not a verdict. Decide where diverse
candidates help and where stable policy is required. Separate generation,
validation, comparison, and selection. Measure diversity alongside quality and
constraints, and keep authority in deterministic application rules or
accountable human judgement.

## The Next Tale

When Tahmures asked the council for a plan no kingdom had ever seen, the most
beautiful proposal sent water climbing uphill through silver channels. The
gardener’s letter asked a harder question: what kind of novelty deserves to be
built?

<!-- next: ch11 -->

## Citations and Further Reading

- Dodge, Jesse, et al. 2020. “Fine-Tuning Pretrained Language Models: Weight
  Initializations, Data Orders, and Early Stopping.”
  [https://arxiv.org/abs/2002.06305](https://arxiv.org/abs/2002.06305).
- Amabile, Teresa M. 1996. *Creativity in Context*. Boulder, CO: Westview
  Press.
- Montgomery, Douglas C. 2019. *Design and Analysis of Experiments*. 10th ed.
  Hoboken, NJ: Wiley.
