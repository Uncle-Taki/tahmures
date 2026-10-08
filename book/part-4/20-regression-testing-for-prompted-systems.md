---
title: "Regression Testing for Prompted Systems"
slug: "regression-testing-for-prompted-systems"
chapter: 20
part: "Part IV — Evaluation, Security, and Production"
summary: "Protect known behaviour with versioned case suites, release gates, and explicit regression budgets."
maturity: "draft"
last_reviewed: "2026-09-28"
narrative_episode: "The Command That Won One Trial"
narrative_origin: "original-teaching-fiction"
learning_objectives:
  - "Build versioned prompt-system regression suites"
  - "Classify improvements, regressions, and intended changes"
  - "Gate releases on protected cases and score floors"
prerequisites: [C10, C19]
---

# Regression Testing for Prompted Systems

## Learning Objectives

By the end of this chapter, you can build versioned prompt-system regression suites, classify improvements, regressions, and intended changes, and gate releases on protected cases and score floors. The working claim of the chapter is narrower than it looks: a prompt revision is a system release, and the suite — not anyone's memory — is what makes forgetting old obligations hard.

## The Tale of Tahmures

### The Setting

The First Scribe's experiment ledger filled an entire wall of the Hall of Scripts. Each leaf held a request, the command and its revision, the result, and the council's decision. A new leaf described a caravan question that the latest command had answered badly. Tahmures asked for a revision before the next departure.

### The Request

The Keeper of Scripts changed three lines and tested the command against the caravan question. The answer now named the safe road, preserved the winter restriction, and cited the current map. The single red mark became green. Tahmures approved the revision, pleased that evidence had replaced argument.

### The Unexpected Result

By noon, complaints arrived from the archive, the granary, and the border court. The new wording treated an expired order as current, omitted a ration limit, and answered a sealed question that required abstention. Those cases had passed last week. No one had replayed them because they were not part of the reported defect. The revision had genuinely improved one behaviour; it had also shifted how the command weighed recency, exceptions, and missing evidence. Calling it better or worse in the abstract concealed the changed decisions.

### The Discovery

Tahmures ordered the First Scribe to stop organising the ledger by embarrassment. Cases were given fixed names, expected outcomes, labels, and keepers. Safety and authority cases became protected: a revision could not spend them to gain an average point elsewhere. Every candidate was tried against the same settled cases, the same recorded answers, and the same examiners, with its wording and the governing rules recorded by revision. The report separated repaired cases, regressed cases, those that still passed, and those that still failed. Some changed expectations were legitimate, but they required a recorded decision of the council and review rather than silent relabelling. The council also retained failures discovered in service, once private details were removed. A revised command was no longer a corrected sentence; it was a new issue of the kingdom's working instrument, offered for acceptance. The rehearsed cases did not prove future perfection, but they made forgetting old obligations harder.

They rehearsed the gate with three proposed revisions. The first fixed the caravan and broke a sealed-order case. The second preserved every old case but failed the new one. The third passed both and lowered the quality of two ordinary summaries. Tahmures refused to hide those differences behind one total. The council accepted the third only after deciding that the lower summary score remained above its declared floor. Beside the green mark, the First Scribe wrote what had improved, what had worsened, and who had accepted the trade. Future readers would inherit a decision, not a mysterious green seal.

### From Tale to Engineering

A local fix is not evidence of a safe release. Prompted systems need versioned regression suites that expose both gains and losses, protect disqualifying cases, and preserve the rationale for intended behavioural change.

## The Engineering Problem

The problem this chapter owns is silent forgetting. A prompted system's observable behaviour is the joint product of a prompt, a model, a policy, retrieved data, tools, and the code that assembles them. Change any one of these and you have re-rolled every case the system has ever handled, not just the case someone complained about. The reported defect is one leaf in the ledger; the obligations are the whole wall. A fix tuned until the reported leaf turns green tells you nothing about the archive, the granary, or the border court.

No component inside the running system remembers those obligations. The model has no memory of last month's expectations, the prompt is whatever it now says, and the operator remembers the incident that was loudest, not the one that was quietest. The failure owner is therefore the release process itself: unless the memory of past obligations is stored outside all of those components, in a form that can be executed against every candidate, it does not exist. This chapter builds that memory and the gate that reads it.

The boundary against Chapter 19 matters here. Evaluation asks whether an answer meets declared criteria; regression testing asks whether a system still meets criteria it demonstrably met before. The first question needs a rubric. The second needs a history, and history cannot be improvised at release time.

## Mental Model

Think of the suite as frozen memory and the gate as a border checkpoint between two versions of the system. Every case in the suite is an obligation with a stable identity, an expected outcome, and an owner. A candidate revision does not argue its way through the checkpoint; it runs every case, and the gate reads the labels.

The gate's arithmetic is deliberately dull. A case that failed and now passes is fixed. A case that passed and now fails is regressed. The rest are stable, in one direction or the other. On top of the labels sit three numbers with different jobs: a count of regressions compared against a budget, a check that no regressed case carries a protected tag, and a floor under every candidate score. The mean score moves too, but it is reported, never consulted.

Two asymmetries keep the model honest. The gate protects the past; it cannot certify the future — a revision can break nothing and still be worthless, which is why a passing gate is a necessary condition for release, never a sufficient one. And the gate is blind to quality drift that does not flip a label: a summary can quietly lose a tenth of a point every release and the classifier will call it stable forever. The floor exists precisely because labels alone are too coarse; the release record exists because numbers alone are too thin.

## Core Concepts

A case is an obligation, not an example. Its `case_id` is stable across releases, its expected outcome is versioned with the policy that justifies it, and its tags say what kind of promise it is. The identity is the anchor for everything else: without it there is no "same case" to compare, only two piles of text. When the suite itself changes — cases added, retired, or re-tagged — that is a new suite version, recorded like any other release.

Classification reads labels, not scores. `fixed`, `regressed`, `stable_pass`, and `stable_fail` are transitions of the `passed` label between baseline and candidate. The score is a separate observation that answers a different question — how well the case was handled, not whether the expected outcome occurred. A fluent answer that names the wrong road can score high and still fail. Keeping those two signals apart is what prevents a quality metric from quietly masquerading as an outcome.

Protected tags mark cases that cannot be spent. A regression on a case tagged `safety`, `authority`, or `abstention` blocks the release regardless of the budget and regardless of the mean. Protection is not a budget line: it is the statement that some obligations are not for sale at any exchange rate. The choice of what to protect is a policy decision, made before any candidate is measured, and visible in the suite version.

The score floor is the only score-based gate. It requires every candidate outcome — including cases that remain fails — to sit at or above a declared minimum. The floor is what catches the slow bleed that labels cannot see: quality dropping release after release without ever flipping a case. Because it applies to all cases, a floor is set per suite, defended in review, and changed like policy, not like a tuning knob.

The regression budget is an honest admission, not a target. `allowed_regressions` says how many unprotected cases a release may newly break, and any use of that allowance belongs in the release record with a named acceptor. A team that never spends its budget has a suite that is either small or lying; a team that always spends it has stopped protecting anything the tags do not name.

Intended change is a policy event, not a relabel. Sometimes the expectation itself must move — a rule changed, a threshold was wrong, the world moved. The legitimate path is a recorded decision that retires or rewrites the case in a new suite version, with the old expectation preserved in history. The illegitimate path is editing the expectation until the candidate passes, which is the suite learning to agree rather than the system learning to behave.

Flaky cases poison the arithmetic. A case whose label flips on its own — the variability Chapter 10 made visible — is a measurement defect, not a regression. Run against deterministic fixtures it still misleads if the underlying behaviour is unstable. The cure is quarantine: move the case out of the gate until its variance is understood, and record why. A gate that reads a coin flip will teach the team to ignore gates.

## Prompt Pattern

The prompt's honest role in this discipline is reporting, not remembering. A release prompt instructs the system — or the operator — to answer one question against the whole suite: what changed, case by case, and did anything that used to pass now fail. It cannot hold the suite itself. Quoting every expectation into the prompt makes the suite unversioned, unreadable, and negotiable, because model-visible text is a place the model can argue with; an expectation the model can see is an expectation the model can attempt to renegotiate.

The repository's experiment shows the contrast in two lines. The naive variant asks the system to "revise for the reported failure and report whether the change passes" — one case, one claim. The governed variant asks it to "compare the candidate against the complete versioned suite and protected tags" — every case, declared protections, no negotiation. The wording difference is small; the ownership difference is total. In the governed form the prompt names the suite and its policy as things that exist outside the conversation, and the report is checked against them by code.

## Naive Attempt

The naive design is the one-case fix, and it is seductive because its evidence is real. You take the reported failure, change wording until that case passes, watch the red mark turn green, and release. The single-case demonstration genuinely shows the reported defect is fixed. What it shows about the other obligations is nothing at all.

The repository models this failure directly. The `single_case_fix` variant of the chapter experiment answers every gate question the same way — passed, nothing regressed — because it only ever looked at the case it was asked to fix. Against the three recorded cases it scores one third on gate accuracy: it reports the protected regression as a pass, because from where it stands, nothing it measured moved. The variant is not dishonest; it is blind. Blindness that reports confidently is what makes one-case tuning dangerous rather than merely incomplete.

## Failure Analysis

Release failures have a taxonomy, and every entry names a process defect rather than a model defect. An unversioned baseline compares a candidate against a moving target, so "regressed" means only "different from Tuesday". Mutable expectations let the suite learn to pass: each small edit to an expected outcome is recorded nowhere and noticed by no one, until the suite certifies whatever it is shown. Label and score confusion lets a quality gain excuse an outcome loss, or a quality loss hide under a stable label. Unprotected disqualifiers let an average be spent buying back a case that should never have been for sale. A floor set at zero is not a floor. A flaky case inside the gate converts signal into noise. A production incident that never becomes a case is an obligation the system shed without ceremony.

The correct response to a blocked gate is disciplined, because the tempting responses are all corruption. Tuning the candidate until the gate passes is legitimate engineering. Tuning the suite until the gate passes is the mutable-expectation failure wearing a work ethic. Spending budget is legitimate when the trade is recorded and owned. Relabelling an expectation is legitimate only as a policy decision in a new suite version. The gate cannot enforce any of this; it can only make the corruption visible, which is why the release record sits beside the report.

## Improved Design

The improved design makes the gate executable and dull on purpose. Outcomes are typed values — a case identity, a pass label, a score, and tags — and the policy is three declared numbers: which tags are protected, how many unprotected regressions are allowed, and the minimum candidate score. The comparison validates its own preconditions before it judges anything: case identities must be present, unique, and identical in both sets. A candidate measured against a differently-shaped suite is not a regression result; it is an error, and the contract raises one rather than guessing an alignment.

The gate then applies its three conditions in one breath: the regression count within budget, no protected regression, and every candidate score at or above the floor. All three must hold. The report carries the full classification, the protected regressions, and the mean score delta — rounded, reported, and consulted by no gate condition. That last detail is deliberate. A mean that gated releases would make every case fungible, and fungible obligations are the thing the suite exists to prevent.

The design's stated blind spot is the label. Classification sees only whether the expected outcome occurred; the floor sees only the score. Between them sits everything a release decision actually needs a human for: whether the fixed case matters, whether the score drop is drift or noise, whether the budget should be spent. The gate narrows the human question; it does not abolish it.

## Worked Example

The border court keeps a miniature of its release ledger: eight cases, suite version 7, run under a declared policy. The full ledger and the three rehearsed revisions from the tale are reproduced below exactly as the contract computes them.

```text
Suite: border-court v7 (8 cases)
Policy: protected_tags = (safety, authority, abstention)
        allowed_regressions = 1
        minimum_candidate_score = 0.70

Baseline (suite v7 as released):
  caravan_routing           routing     fail  0.52
  sealed_order              authority   pass  0.81
  ration_limit              safety      pass  0.83
  expired_decree            authority   pass  0.78
  abstain_sealed_question   abstention  pass  0.80
  granary_summary           summary     pass  0.78
  border_summary            summary     pass  0.76
  market_report             summary     pass  0.74

Revision R1 — fix the caravan routing case:
  caravan_routing  fail 0.52 -> pass 0.88
  sealed_order     pass 0.81 -> fail 0.75
  report: passed = False
    fixed                 = (caravan_routing,)
    regressed             = (sealed_order,)
    protected_regressions = (sealed_order,)
    stable_fail           = ()
    mean_score_delta      = +0.0375

Revision R2 — conservative rewording:
  caravan_routing  fail 0.52 -> fail 0.72
  report: passed = True
    fixed                 = ()
    regressed             = ()
    protected_regressions = ()
    stable_fail           = (caravan_routing,)
    mean_score_delta      = +0.025

Revision R3 — caravan fix with lighter summaries:
  caravan_routing  fail 0.52 -> pass 0.88
  granary_summary  pass 0.78 -> pass 0.72
  border_summary   pass 0.76 -> pass 0.71
  report: passed = True
    fixed                 = (caravan_routing,)
    regressed             = ()
    protected_regressions = ()
    stable_fail           = ()
    mean_score_delta      = +0.03125
```

Every case not named in a revision's report is `stable_pass`, in the contract's alphabetical report order — six cases in R1, seven in R2 and R3, since `sealed_order` joins them whenever it is not regressing. The three reports deserve slow reading, because each one teaches a different refusal.

R1 is blocked while every number looks healthy. The budget was respected — one regression, one allowed. The floor held — the lowest candidate score is 0.74. The mean improved by nearly four hundredths, more than any other revision achieved. The gate blocks it anyway, because `sealed_order` carries the `authority` tag and protection is not a budget line. Remove that single tag from the suite and the identical numbers pass: the difference between a blocked release and a silently broken sealed order is one tag, chosen before any candidate was measured. That is the entire argument for declaring protections in policy rather than noticing them in incidents.

R2 passes the gate and is still declined. Nothing regressed, the floor held, and the caravan case — the reason the revision existed — remains a fail at 0.72: better written, still the wrong road, which is the label and score saying exactly what each is for. The gate certified that the revision broke no promise. It said nothing about whether the revision kept its purpose, because that is not a question a gate can answer. Releasing R2 would have been legal and useless; the council declined it on purpose, and the gate's pass mark is visibly not a release decision.

R3 passes with a debt attached. The caravan is fixed, nothing regressed, and two summary cases lost six and five hundredths of score without flipping a label — the classifier never saw it. The floor did: border_summary landed at 0.71 against a floor of 0.70, one hundredth from blocking the release. The council accepted the trade, and the acceptance is a record — what improved, what worsened, who accepted — because a release that quietly trades quality for a fix is the same ledger organised by embarrassment, one release later.

## Experiment

Run the shared, provider-neutral fixture experiment:

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch20-regression.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch20-regression.json
```

The manifest compares the two prompt variants over three committed synthetic cases. `old_safety` records a candidate that fixes a new route while regressing a protected sealed order. `safe_candidate` records a change with no regressions. `score_floor` records a candidate whose labels are intact but whose quality drops below the declared floor — a gate failure with an empty regression list, which is the floor earning its keep. The `single_case_fix` variant answers all three with the same confident pass, scoring one third on gate accuracy and two thirds on regression detection; the `regression_gate` variant reports each case as recorded, scoring full marks on both. These results demonstrate report mechanics over the stated cases; they are not evidence that any particular wording behaves universally better. Replace fixtures with controlled recordings before drawing provider-specific conclusions.

## Evaluation

Measure what the included evaluator actually reports. The `regression_gate` evaluator compares a reported gate decision against the recorded expectation and returns two metrics: `gate_accuracy`, whether the pass decision matched, and `regression_detection`, whether the reported regression set matched. Detection is the harsher metric and the one that matters — a gate that reports the right overall verdict for the wrong case list has not protected anything. Alongside the evaluator, the contract itself surfaces the full classification, protected regressions, and mean score delta for each comparison, which are the numbers a release record needs.

What the evaluator does not do is also part of the contract. It does not measure floor behaviour except through cases that encode it, it does not track flakiness across runs, and it does not attribute a regression to a cause. Production suites extend this with per-tag budgets, automatic bisection to the smallest breaking change, and variance tracking across repeated trials; those extensions are not implemented by the included evaluator and are recorded as deferred work, not as claims about it. Define thresholds and protected tags before reading candidate results, and treat a skipped suite run as unknown, not passed.

## Implementation Lab

### Python

**INTEGRATION_FRAGMENT.** Before this comparison, construct `baseline` and `candidate` as tuples of `CaseOutcome` values for the same case identities, and `policy` as a `RegressionPolicy`. Supply `block_release(regressed)` to stop the application's release path. This fragment demonstrates the gate call; it omits outcome collection and the surrounding release workflow.

```python
from tahmures.regression import compare_regression

report = compare_regression(baseline, candidate, policy)
if not report.passed:
    block_release(report.regressed)
```

Python 3.12 is the canonical educational implementation. Construct baseline and candidate as typed outcomes with matching case identities, and policy as a `RegressionPolicy`, and let the comparison — not the surrounding prose — decide whether the release may proceed.

### Go

**INTEGRATION_FRAGMENT.** Here `baseline` and `candidate` are existing `[]tahmures.CaseOutcome` values, and `policy` is a `tahmures.RegressionPolicy`. Import the repository package as `tahmures`, enclose the code in a function returning an error, and supply `blockRelease(regressed)`. Measurement and deployment are outside this gate fragment.

```go
report, err := tahmures.CompareRegression(baseline, candidate, policy)
if err != nil {
    return err
}
if !report.Passed {
    blockRelease(report.Regressed)
}
```

The Go implementation preserves the same validation, classification order, gate conditions, and report fields. Equivalence concerns behaviour, not syntax.

## Failure Modes

The suite is a component, and it fails like one. Mutable expectations are the canonical failure: the suite is edited until it agrees with the candidate, and the gate becomes a mirror. Protected sprawl is its quieter sibling — when everything is protected, the budget is meaningless and every release becomes an all-or-nothing vote, which teaches teams to route around the gate. A stale suite passes candidates against obligations the product no longer has, and blocks candidates against obligations nobody remembers creating. A theatrical suite runs green on every pull request while its cases were last reviewed when the system was a prototype. A flaky case inside the gate manufactures regressions and fixes at random, and a team burned by two false alarms will ignore the third, real one. None of these failures appear in the gate's own report, which is why the suite needs the same ownership, review, and version discipline as the code it judges.

## Security Considerations

The suite is a trust boundary, and it is attacked through its expectations. An expected label is standing authority: whoever can edit what `sealed_order` is expected to do can turn a blocked release into a passing one without touching the candidate. Guard expectation edits with the same review as policy edits, record who changed them and why, and treat an expectation change that lands in the same commit as the candidate it permits as an incident. Protected tags carry the same weight — the R1 counterfactual showed that removing one tag silently converts a blocked release into a passed one, so tag changes are policy events, not cleanup.

The suite is also where adversarial coverage lives, and it must be designed against phrase recognition. An injection case that always uses the same wording tests the fixture, not the system: reword the attack between suite versions while keeping the prohibited outcome identical, so a green case reports a refusal that survived rephrasing rather than a phrase the fixture happens to match. Include legitimate content that resembles an attack, or the suite will teach the system to refuse safe requests. And keep the regression suite itself out of model-visible context: expectations the model can read are expectations it can optimise against, which converts the memory of obligations into a map for evading them.

## Operational Considerations

The suite has a lifecycle that someone must own. Cases are added when production incidents are converted — private details removed, smallest reproducible form retained — and retired when the obligation dies, with both events recorded in suite versions. Every candidate runs the whole suite before release; a suite that runs only on Fridays protects only Friday's obligations. The gate report and its acceptance record are retained beside the release: what improved, what worsened, who accepted the trade, under which prompt, policy, suite, and evaluator versions. That bundle is what makes rollback coherent — restoring a prompt while keeping an incompatible policy or suite version is a new release, untested — and it is the artefact Chapter 23 will need when drift has to be diagnosed after the fact. Budget maintenance time for the suite itself; a control with no owner after launch decays exactly like the code it was meant to check.

## Trade-Offs

Suite size buys coverage and costs maintenance: every case must stay correct, owned, and meaningful as the system moves, and a suite of thousands of stale cases protects less than a suite of eighty live ones. Protection strictness trades against iteration speed in the most literal way this book will show — one tag was the difference between R1 blocked and R1 shipped — so the protected set must be argued about in policy review, not grown by inertia. Floor height trades false rejections against slow bleed: a floor of 0.70 admitted border_summary at 0.71 and would have blocked it at 0.69, and no number is simultaneously safe and convenient. The regression budget trades honesty against safety — an allowance that is never spent suggests the suite is too small to find the trades, and one that is always spent suggests the tags are carrying all the protection. Deterministic fixtures make classification meaningful and reality less represented: the variability Chapter 10 measured does not disappear because the gate is deterministic, so flaky behaviour must be quarantined rather than averaged away, and each quarantined case is a small hole in the memory the suite exists to be.

## When Prompting Is Not the Answer

Memory is not a language task. No wording can recall last month's obligations, compare two runs of a case the conversation never saw, hold a floor under a score, or make a protected tag mean anything. Instructing the model to "be careful not to break existing behaviour" moves nothing, because careful is not an observation. The suite, the policy, and the gate are executable institutional memory owned by the release process; the prompt's role ends at reporting against them. If the design's answer to "how do we not forget" is a sentence in the prompt, the design has already forgotten.

## Exercises

1. Before running any code, predict the full report — every classification list, the protected regressions, the mean delta, and the pass decision — for a fourth revision of the border-court suite in which `expired_decree` moves pass to fail at 0.77 and nothing else changes. Then verify with `compare_regression`.
2. Remove `authority` from the policy's protected tags and re-run revision R1. Explain, in terms a release manager would accept, why the gate now passes and what obligation was traded for the caravan fix.
3. Design a floor for the miniature suite: choose a value, justify it against the baseline scores, and construct a revision that passes every label condition yet fails your floor. Identify which case your floor catches first and why.
4. The council decides that `sealed_order`'s expectation must change because the sealing law itself changed. Write the decision record that makes this an intended policy revision rather than a silent relabel, including what happens to the old case in suite history.
5. A production incident arrives: the system answered a sealed border question with the sealed contents. Convert it into a suite case — case identity, expected outcome, tags, and the private details you would strip — and state which existing case it is closest to and why it is still worth its own identity.
6. One summary case flips labels on roughly one run in three with no code change between runs. Using Chapter 10's variability vocabulary, write the quarantine rule: what leaves the gate, what is recorded, what evidence would readmit the case, and why leaving it in would be worse.

## Chapter Summary

Regression testing for prompted systems is the discipline of keeping promises on purpose. A suite of stable, versioned, owned cases records what the system has obligated itself to do; label-based classification exposes what a candidate fixed and broke; protected tags and score floors mark the obligations that cannot be spent; and the gate turns all of it into a release decision that a mean cannot buy. The gate protects the past and certifies nothing about the future — a passing release may still be useless, and a blocked one may be one tag away from shipping — which is why the acceptance record, not the pass mark, is the artefact future readers inherit.

## The Next Tale

While adding a failed archive case to the suite, the Archivist unfolded a tablet whose first line addressed not Tahmures, but the reader of the tablet itself.

<!-- next: ch21 -->

## Citations and Further Reading

- Ribeiro, Marco Tulio, Tongshuang Wu, Carlos Guestrin, and Sameer Singh. 2020. “Beyond Accuracy: Behavioral Testing of NLP Models with CheckList.” *ACL 2020*. https://doi.org/10.18653/v1/2020.acl-main.442
