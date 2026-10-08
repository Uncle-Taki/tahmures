---
title: "Evaluation and Rubrics"
slug: "evaluation-and-rubrics"
chapter: 19
part: "Part IV — Evaluation, Security, and Production"
summary: "Turn preferences into anchored, reviewable evaluation contracts with disqualifiers and adjudication."
maturity: "draft"
last_reviewed: "2026-09-28"
narrative_episode: "The Trial Without Weights"
narrative_origin: "original-teaching-fiction"
learning_objectives:
  - "Design anchored outcome rubrics"
  - "Separate model, system, and evaluator failures"
  - "Handle reviewer disagreement without hiding it in an average"
prerequisites: [C03, C08, C10]
---

# Evaluation and Rubrics

## Learning Objectives

By the end of this chapter, you can design anchored outcome rubrics, separate model, system, and evaluator failures, and handle reviewer disagreement without hiding it in an average. The docket you produce is a specification in its own right: versioned, reviewable, and as fallible as the answers it judges.

## The Tale of Tahmures

### The Setting

The western court met beneath a ceiling painted with balanced scales. Two villages claimed the same strip of river land. The Archivist brought survey tablets, flood marks, tax rolls, and three witness accounts. Tahmures asked the Mirror Div and two judges to examine the record independently. The First Scribe prepared a docket with three empty columns headed strong, acceptable, and weak, but no one had agreed what those words meant.

### The Request

Tahmures asked each reviewer to choose the better judgement and explain the choice. It sounded fair: several readers, the same evidence, and reasons written in public. Yet one judge valued fidelity to the oldest tablet, another valued present cultivation, and the Mirror Div valued the account that reconciled the most testimony. None declared those priorities before reading the proposed judgements.

### The Unexpected Result

All three praised different decisions. Each explanation was coherent. The Mirror Div selected a polished settlement that quoted a flood mark from the wrong decade. One judge noticed the error but still called the answer acceptable because its remedy was humane. The other rejected it because any unsupported land boundary was disqualifying. Their three labels averaged to something that looked moderate and told the villages nothing. Worse, the council began debating which reviewer sounded wiser instead of which observable qualities the judgement required.

### The Discovery

Tahmures halted the verdict and asked the judges to write the standard of judgement before seeing another answer. They named evidence fidelity, coverage of both claims, legal consistency, clarity, and practicability. For each, they described what scores from zero to four meant. An invented boundary failed regardless of the total. Two independent reviews were required; a wide difference sent the case to adjudication rather than concealing it in arithmetic. The First Scribe recorded the answer, the evidence passages, the rubric's revision, the individual scores, and each reviewer's reasons. When the case was heard again, the reviewers still differed about practicability, but they agreed exactly where and why. Tahmures saw that evaluation was not a ceremonial number attached after judgement. It was a specification for observable success, with its own errors and authority. The court could now revise either the answer, the rubric, or the evidence without pretending those were the same act.

Before recalling the villages, Tahmures placed two deliberately flawed judgements before the panel. One was eloquent but cited no tablet; the other was awkward yet traceable. The old labels favoured eloquence. The written anchors rejected the unsupported boundary and preserved the traceable answer for revision. Then the judges exchanged seats and scored again. Their remaining difference concerned the cost of moving an irrigation wall, a fact the record did not contain. They marked it unresolved. For the first time, the empty place in the evidence appeared in the verdict instead of being filled by confidence.

### From Tale to Engineering

The court lacked more than a good prompt: it lacked an evaluation contract. Reliable AI work requires anchored criteria, disqualifying failures, reviewer provenance, and an explicit path for uncertainty and disagreement.

## The Engineering Problem

When success is subjective or variable, the measuring instrument becomes a load-bearing component, and the court's first docket failed before anyone read a judgement. Three columns — strong, acceptable, weak — carried no agreement about what the words meant, so each reviewer imported a private standard: fidelity to the oldest tablet, present cultivation, reconciliation of testimony. The labels averaged into a number that looked moderate and told the villages nothing, and the council's attention moved from the decision's observable qualities to which reviewer sounded wiser.

The engineering problem is to turn evaluation from a ceremony into a specification. That specification must state which observable qualities define success, which failures disqualify a candidate regardless of other merit, how reviewer disagreement is handled, and who owns each of those choices. It must also keep three failures apart that look identical from the outside: a model that produced a weak answer, a system that supplied stale evidence or skipped a check, and an evaluator that cannot tell the difference. The remedies differ — re-prompting addresses the first, pipeline repair the second, rubric revision the third — and a team that cannot distinguish them will tune prose while the defect lives elsewhere. In this chapter the primary failure owner is requirements and evaluator design: the docket itself.

## Mental Model

Use an anchored multi-reviewer rubric as the governing mental model. Read it as a small decision machine with named, testable parts. Criteria name the observable qualities that matter. Anchors define, for each criterion, what scores from zero to four actually mean, so a number is a claim about the artefact rather than a reviewer's mood. Weights state how heavily each criterion counts. A disqualifying minimum states a floor below which one criterion sinks the whole candidate. The pass threshold states what weighted total accepts. The disagreement threshold states how far apart independent reviews may sit before humans must adjudicate.

The machine runs the same way every time, which is what makes its verdicts challengeable. Each reviewer scores every criterion; each review becomes one weighted score on a shared zero-to-one scale; the reviews are averaged, compared with the threshold, and checked for disqualifiers and disagreement. An average can accept a candidate, but it cannot excuse one: a disqualifier or a wide split routes the candidate to adjudication whatever the mean says. Authority sits in the docket, written before the candidates are read — not in the sensibility of whichever reviewer speaks last.

## Core Concepts

Anchored scores are the difference between a rubric and a ballot. An anchor for the score of two on evidence fidelity — a dispositive claim does not trace to the record — lets a reviewer record a specific, arguable observation; the label acceptable records only a feeling. Anchors also make review transferable: a judge taking another's seat applies the written meaning rather than inherited instinct, which is what the exchanged seats in the tale actually tested.

Weights encode relative importance as a policy decision. The court weighted evidence twice as heavily as coverage and practicability because a boundary settlement that cannot be traced to the record is worthless regardless of its other virtues. The contract normalises each review to a shared zero-to-one scale — the weighted sum divided by the largest achievable sum — so thresholds keep their meaning when criteria are added or reweighted.

A disqualifier is a criterion whose minimum cannot be averaged away. The rule is deliberately strict: if any one reviewer scores a disqualifying criterion below its minimum, the failure is recorded with its criterion identity and the candidate is routed to adjudication even when the mean clears the pass threshold. One strict reviewer can therefore stop a fluent candidate that lenient ones would wave through — the tale's judge who rejected any unsupported boundary, made structural.

Disagreement is data, not noise. The distance between the highest and lowest reviewer totals measures whether the artefact sits near a boundary or the anchors are ambiguous; both are worth knowing, and neither is visible in an average. The designed response is adjudication — a named human reads the scores, rationales, and anchors, then decides — rather than arithmetic concealment.

Reviewer provenance and rubric identity make verdicts auditable. A score is an assertion by an author with a rationale, recorded under a rubric version; strip any of those away and a verdict becomes an unchallengeable number. When the rubric changes, old verdicts do not become wrong — they become incomparable, which is why the version travels with every score.

The evaluator itself is a component with failure modes, and treating it as neutral machinery is the last template to fall away. An instrument can be consistently wrong: anchors that no candidate can fail, a threshold no candidate can clear, a disqualifier that fires on the wrong class of work. Those defects are invisible from inside a single run, because the evaluator is the run's standard of truth. They become visible only when the instrument is itself evaluated — challenged with known-bad candidates it should reject, known-good ones it should accept, and near-threshold cases that expose where its boundaries actually sit. A rubric that has never rejected anything is not a lenient rubric; it is an untested one.

## Prompt Pattern

Ask the model for candidates and evidence, not for verdicts. A prompt in an evaluated pipeline states the bounded task, names the evidence the candidate must cite, and requests an output structure whose claims can be checked against spans. If a model participates in review, it enters as one reviewer among several: a stable identity, scores against the written anchors, a rationale — and no special standing. The pattern fails when the model becomes the machinery itself: a model scoring its own class of output against unwritten standards turns evaluation into self-report with extra steps.

## Naive Attempt

The naive design is the docket with empty columns: strong, acceptable, weak, and a request that reviewers be fair. It fails twice. First, undefined labels let every reviewer import a private standard, so the scores measure the reviewers rather than the artefact — the averaged total looked moderate precisely because it averaged three different questions. Second, tuning against one representative case turns evaluation into wording revision: the command changes until the embarrassing example passes, and nothing is learned about the cases nobody happened to mention. A fluent candidate that cites no record sails through, because fluency is the only quality the instrument can see.

## Failure Analysis

Failures for evaluation include unanchored review, hidden disagreement, disqualifiers buried by averages, mutable expectations, evaluator drift across versions, proxy gaming, and unexamined model-as-judge. A workable taxonomy names the owner before choosing the remedy. The same rejected output can be a model failure — fluent fabrication the pipeline should have caught; a system failure — the retriever supplied a stale map or the validator was skipped; or an evaluator failure — the anchors cannot distinguish a traced claim from a confident one. The remedies differ: re-prompt or retrain the first, repair the pipeline for the second, and revise the rubric for the third — a versioned, reviewed act, not a wording change. Collapsing the three into a single notion of quality sends every investigation to the prompt.

Do not retry an adjudication. An evaluator failure is fixed by revising the instrument and re-running the record under the new version; a requirements failure is renegotiated with the people who own success; a disagreement is routed to the adjudicator, not averaged until it disappears.

## Improved Design

The improved design makes the anchored rubric executable in Python and Go. A rubric criterion carries a stable identifier, a positive weight, a minimum score, the five anchor definitions, and the disqualifying flag. A rubric takes the criteria, the pass threshold, and the disagreement threshold. Reviews carry a reviewer identity, a score per criterion, and a rationale; evaluation refuses reviews with duplicate or anonymous reviewers, missing rationales, scores that do not match the criteria exactly, or values outside zero to four. The result reports the weighted mean, per-criterion means, per-reviewer scores, the disagreement distance, the disqualifying failures by criterion, and the adjudication decision; a candidate passes only when the mean reaches the threshold and no adjudication is required.

The contract has boundaries worth naming. Disagreement is one overall distance between reviewer totals, not a per-criterion analysis; the per-criterion means are reported, and locating where reviewers split is the analyst's work with those numbers. The contract judges committed reviews — it does not generate them, keep reviewers independent, or verify that cited spans exist in the record. Those obligations belong to the process around the instrument and to the pipeline that produced the evidence in the first place.

## Worked Example

The replay from the tale, run as a docket. The court's rubric carries three criteria — evidence fidelity weighted double and disqualifying, coverage, practicability — with anchors written before the judgements were read:

```text
court docket — western court, replay of the two flawed judgements
rubric v2 — weights: evidence_fidelity 2 (disqualifying, min 3), coverage 1, practicability 1
thresholds: pass >= 0.75 · adjudicate when reviewer disagreement > 0.20

anchors — evidence_fidelity: 0 fabricated span · 1 real span, misread · 2 dispositive claim
  untraced · 3 every dispositive claim traces · 4 traces, conflicts surfaced
anchors — coverage: 0 one claim unheard · 1 named, undeveloped · 2 developed with evidence ·
  3 strongest evidence on both sides · 4 edge cases addressed
anchors — practicability: 0 unworkable · 1 needs facts the record lacks · 2 costs asserted,
  unevidenced · 3 costs evidenced · 4 costed and phased

judgement A — eloquent, cites no tablet
  reviewer        evidence  coverage  practicability   weighted
  first-judge         3        4           4           14/16 = 0.875
  second-judge        2        4           4           12/16 = 0.750
  criterion mean    2.5      4.0         4.0           mean 0.8125 · disagreement 0.125

  decision: mean clears the pass threshold, but evidence_fidelity sits below its minimum on
  one review → disqualifying failure → adjudication, not acceptance

judgement B — awkward, traceable
  reviewer        evidence  coverage  practicability   weighted
  first-judge         4        3           2           13/16 = 0.8125
  second-judge        4        3           1           12/16 = 0.750
  criterion mean    4.0      3.0         1.5           mean 0.78125 · disagreement 0.0625

  decision: no disqualifier, disagreement within threshold → passed, with practicability
  flagged: the irrigation-wall cost is a fact the record does not contain
```

The arithmetic is small enough to check by hand. Each review's weighted score is the sum of score times weight — for the first judge on judgement A, three on evidence at weight two, four on coverage, four on practicability — divided by the largest achievable sum, four times the total weight of four: fourteen sixteenths, 0.875. The second judge's two on evidence yields twelve sixteenths, 0.75.

Read judgement A against the old docket. Its mean of 0.8125 clears the 0.75 pass threshold, and its disagreement of 0.125 sits inside the 0.20 tolerance; the preference-era court would have accepted it, and the polished settlement would have gone to the villages. The written anchors refuse it anyway: evidence fidelity is disqualifying with a minimum of three, the second judge scored two, and no tablet supports the boundary. One sub-minimum score on one disqualifying criterion routes the whole candidate to adjudication. That is the tale's sharpest sentence made mechanical: an invented boundary fails regardless of the total.

Judgement B is the mirror lesson. It clears no column gracefully — the drafting is awkward, the costs asserted — but every dispositive claim traces, no disqualifier fires, and the reviewers sit close enough that no adjudication is needed, so it passes at 0.78125. What the result adds, and the old labels could not, is direction. The criterion means show practicability at 1.5, and the anchor at one — needs facts the record lacks — names the irrigation-wall cost the record does not contain. The empty place in the evidence appears in the verdict instead of being filled by confidence.

Both rows also record what replay demands: reviewer identities, individual scores, rationales, and the rubric version. Two judges exchanging seats and reproducing a verdict is possible only because the standard travelled with the record.

## Experiment

Run the shared, provider-neutral fixture experiment:

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch19-evaluation.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch19-evaluation.json
```

The manifest compares preference-only review with the anchored design over three committed synthetic cases: `unsupported`, a fluent claim without record evidence, expected to disqualify; `split_review`, two reviewers far enough apart to require adjudication without any disqualifier; `anchored_pass`, criteria met with cited evidence. The `anchored_rubric` evaluator compares the reported decision — passed, requires adjudication, disqualified — against committed expectations and reports `rubric_decision_accuracy` and `adjudication_accuracy`; the runner adds per-variant and per-tag summaries. The committed fixtures demonstrate the decision mechanics and the stated failure cases; they are not evidence that one wording or model behaves universally better.

## Evaluation

Measure what the included evaluator actually reports: `rubric_decision_accuracy`, whether the recorded decision matches expectations, and `adjudication_accuracy`, whether the adjudication routing matched. The rubric contract itself surfaces the disagreement distance, the disqualifying failures by criterion, per-criterion means, and per-reviewer scores — the numbers an adjudicator reads. Production suites extend this with disqualifier recall against known-bad candidates, adjudication rate and its trend, and evidence coverage of the test set; those extensions are not implemented by the included evaluator and are recorded as deferred work, not as claims about it. Define thresholds and disqualifying failures before reading candidate results, and treat a skipped evaluation as unknown, not passed.

## Implementation Lab

### Python

**INTEGRATION_FRAGMENT.** This constructs the rubric and reviews, then routes the result. Supply `queue_for_human_review(result)` as the application's adjudication hook; queue storage and the human decision are omitted. The call is reached for these reviews because evidence fidelity is disqualifying.

```python
from tahmures.rubrics import Rubric, RubricCriterion, RubricReview

rubric = Rubric(
    criteria=(
        RubricCriterion(
            criterion_id="evidence_fidelity",
            weight=2.0,
            minimum=3,
            anchors=(
                "fabricated span",
                "real span, misread",
                "dispositive claim untraced",
                "every dispositive claim traces",
                "traces, conflicts surfaced",
            ),
            disqualifying=True,
        ),
        RubricCriterion(
            criterion_id="coverage",
            weight=1.0,
            minimum=2,
            anchors=(
                "one claim unheard",
                "named, undeveloped",
                "developed with evidence",
                "strongest evidence on both sides",
                "edge cases addressed",
            ),
        ),
        RubricCriterion(
            criterion_id="practicability",
            weight=1.0,
            minimum=2,
            anchors=(
                "unworkable",
                "needs facts the record lacks",
                "costs asserted, unevidenced",
                "costs evidenced",
                "costed and phased",
            ),
        ),
    ),
    pass_threshold=0.75,
    disagreement_threshold=0.2,
)

reviews = (
    RubricReview(
        reviewer_id="first-judge",
        scores={"evidence_fidelity": 3, "coverage": 4, "practicability": 4},
        rationale="humane remedy; drafting fluent",
    ),
    RubricReview(
        reviewer_id="second-judge",
        scores={"evidence_fidelity": 2, "coverage": 4, "practicability": 4},
        rationale="no tablet supports the boundary",
    ),
)

result = rubric.evaluate(reviews)
if result.requires_adjudication:
    queue_for_human_review(result)
```

The Python API is the canonical educational contract. Construct the rubric before
evaluating reviews, and treat a result that requires adjudication as a routing
decision rather than a score.

### Go

**INTEGRATION_FRAGMENT.** Place this inside an application function that can return an error, with the repository package imported as `tahmures`. Provide `queueForHumanReview(result)` to receive the adjudication result. The fragment shows evaluation and routing, leaving queue persistence and adjudication to the application.

```go
rubric := tahmures.Rubric{
	Criteria: []tahmures.RubricCriterion{
		{
			CriterionID:   "evidence_fidelity",
			Weight:        2,
			Minimum:       3,
			Anchors:       [5]string{"fabricated span", "real span, misread", "dispositive claim untraced", "every dispositive claim traces", "traces, conflicts surfaced"},
			Disqualifying: true,
		},
		{
			CriterionID: "coverage",
			Weight:      1,
			Minimum:     2,
			Anchors:     [5]string{"one claim unheard", "named, undeveloped", "developed with evidence", "strongest evidence on both sides", "edge cases addressed"},
		},
		{
			CriterionID: "practicability",
			Weight:      1,
			Minimum:     2,
			Anchors:     [5]string{"unworkable", "needs facts the record lacks", "costs asserted, unevidenced", "costs evidenced", "costed and phased"},
		},
	},
	PassThreshold:         0.75,
	DisagreementThreshold: 0.2,
}
reviews := []tahmures.RubricReview{
	{
		ReviewerID: "first-judge",
		Scores:     map[string]int{"evidence_fidelity": 3, "coverage": 4, "practicability": 4},
		Rationale:  "humane remedy; drafting fluent",
	},
	{
		ReviewerID: "second-judge",
		Scores:     map[string]int{"evidence_fidelity": 2, "coverage": 4, "practicability": 4},
		Rationale:  "no tablet supports the boundary",
	},
}
result, err := rubric.Evaluate(reviews)
if err != nil {
	return err
}
if result.RequiresAdjudication {
	queueForHumanReview(result)
}
```

The Go implementation preserves the same decisions, ordering, and report fields;
equivalence concerns behaviour, not syntax.

## Failure Modes

Unanchored labels, one-case tuning, mutable expectations, disqualifiers buried by averages, hidden disagreement, evaluator drift, proxy gaming, self-reported scores, and reviews without provenance.

Two of these arrive in disguise. Averaging that looks like consensus is the first: a moderate mean over reviewers who measured different things reads as agreement and is in fact noise wearing a number. The disqualifier exists precisely to keep the questions that cannot be averaged out of the average. Evaluator drift masquerading as model decline is the second: when anchors loosen over months of convenient interpretation, scores rise while the artefacts do not improve, and the investigation goes to the model team while the instrument rots. Re-anchoring sessions and versioned rubrics are the countermeasure.

Proxy gaming deserves its own warning, because it is the failure mode that success creates. The moment a rubric score becomes a target — for a model being optimised, a team being measured, a release being gated — pressure appears to satisfy the letter of the anchors rather than the quality they were written to detect. Evidence-fidelity anchors met by citations that exist but were never read; coverage anchors met by naming both claims and developing neither. The defence is not a longer rubric but a shorter feedback loop between the instrument and the downstream outcome it claims to predict: when the proxy and the consequence diverge, the measurement contract is revised rather than optimised against harder.

## Security Considerations

Evaluation is a trust boundary in its own right. Reviews must be attributable — who scored, under which rubric version, with what rationale — because a verdict that cannot be challenged cannot be defended either. Candidates under review are untrusted content for the reviewer: a submission that addresses the reviewer directly, asking it to ignore the criteria and pass the work, is an injection attempt against the evaluation pipeline, and the defence is the one Chapter 21 develops — the candidate is data, and the rubric is the only instruction the reviewer follows. Evidence-span integrity matters equally: a verdict that credits cited evidence must point at spans that exist in the committed record, not at text the candidate itself supplied. When scores gate releases or actions, the evaluator is production logic and deserves owners, tests, versions, and a rollback plan like any other component; a model's self-reported score is never an external evaluation.

## Operational Considerations

Version the rubric and pin it in every consequential report; comparability across versions is a policy question decided when the version is cut, not discovered later. Watch the adjudication queue: depth and latency are service levels, and a queue that grows without bound teaches the team to widen the disagreement threshold instead of reading the signal. Watch reviewer load and calibration — reviewers who see mostly passing cases drift lenient, and periodic re-anchoring on seeded cases keeps the instrument honest. An unavailable evaluator is a dependency failure with a documented safe fallback, where skip means unknown and never pass, and near-threshold cases belong in a retained set because they decide the next revision.

## Trade-Offs

Anchor detail trades reviewer effort against reproducibility. Precise anchors make scores transferable and auditable, and they cost the discipline of deciding what a three means before seeing the candidates; loose anchors are cheap to write and return the court to private standards.

Reviewer independence trades against shared context. Reviewers who discuss a candidate converge quickly and lose the disagreement signal; reviewers who work in isolation preserve it and duplicate effort. The court's rule — anchors written first, reviews recorded independently — buys the signal at the price of coordination.

Disagreement sensitivity trades against adjudication cost. A tight threshold catches ambiguous artefacts early and fills the adjudication queue; a loose one keeps the queue short and lets borderline candidates through on the mean. The threshold is a policy decision about which error is worse, and it belongs in the rubric version, not in the adjudicator's discretion.

Rubric versioning trades improvement against longitudinal comparability. Every re-anchoring makes the instrument better and the trend line shorter; a team that re-anchors monthly cannot honestly plot a year of scores on one axis. The record must say which version produced which number.

Hard disqualifiers trade simplicity against nuance. A single minimum on one criterion is blunt — it cannot express near-misses — and that bluntness is exactly what makes it hard to argue away. Reserve disqualifiers for failures no amount of other merit should offset.

## When Prompting Is Not the Answer

Prompting can elicit a candidate, a self-assessment, or even a suggested score, and only the first of those is evaluation. Acceptance thresholds, disqualifiers, adjudication routing, reviewer provenance, and rubric versioning are mechanisms: they live in code and process, and they decide. A model may serve as one reviewer with recorded provenance; it cannot be the rubric, the threshold, or the adjudicator of record, because a specification that lives in a prompt cannot be pinned, diffed, replayed, or held accountable for its verdicts.

## Exercises

1. Write anchors for a new criterion — safety of tone for a support assistant — defining all five scores and choosing a minimum. Decide whether it should be disqualifying, and defend the decision in terms of what an average could hide.
2. Construct a candidate whose mean clears a 0.75 pass threshold while one reviewer scores a disqualifying criterion below its minimum. Run it through the lab rubric, then argue for and against the disqualifier from the perspective of the candidate's author.
3. Design the adjudication path: what the adjudicator sees — scores, rationales, anchors, evidence spans — what they may decide, and what they must record. Keep the adjudicator from simply re-averaging the scores they were given.
4. A system's acceptance rate fell ten points after a model upgrade. List three explanations — model, pipeline, evaluator — and the evidence you would gather before changing anything.
5. Evaluate the evaluator: commit three near-threshold cases and one malformed review — missing rationale, out-of-range score, criterion mismatch — and verify each is refused or routed as designed.
6. A team proposes replacing two human reviewers with one model reviewer to cut latency. Write the governance conditions under which that is acceptable, and the provenance the model reviewer must carry.

## Chapter Summary

Evaluation becomes reliable when the instrument is a specification rather than a ceremony. Anchored criteria make scores claims about the artefact; weights and thresholds make acceptance a policy; disqualifiers make some failures unaverageable; disagreement routes to adjudication instead of disappearing into the mean. Reviewer provenance and rubric versioning keep verdicts challengeable across time, and the separation of model, system, and evaluator failures sends each defect to the owner who can fix it. The court that writes the test before seeing the answer has converted taste into engineering.

## The Next Tale

The anchored rubric settled the court's disagreement, but the First Scribe found a darker result in the ledger: the revised command won this trial and failed three older ones.

<!-- next: ch20 -->

## Citations and Further Reading

- Amershi, Saleema, et al. 2019. “Guidelines for Human-AI Interaction.” *CHI 2019*. https://doi.org/10.1145/3290605.3300233
