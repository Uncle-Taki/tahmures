---
title: "Production Operations and Drift"
slug: "production-operations-and-drift"
chapter: 23
part: "Part IV — Evaluation, Security, and Production"
summary: "Operate prompted systems with version identity, segmented telemetry, service objectives, drift gates, and rollback."
maturity: "draft"
last_reviewed: "2026-09-28"
narrative_episode: "The Dialect That Changed at Dawn"
narrative_origin: "original-teaching-fiction"
learning_objectives:
  - "Define versioned operational telemetry for prompted systems"
  - "Detect segment-level drift hidden by aggregates"
  - "Design rollback, incident, and change-management procedures"
prerequisites: [C19, C20, C22]
---

# Production Operations and Drift

## Learning Objectives

By the end of this chapter, you can record version-complete telemetry for every run of a prompted system, compare time windows instead of single moments, and detect a failing segment that the kingdom-wide average conceals. The working claim: a prompted system that was verified at launch does not *stay* verified, because models, prompts, policies, and data all change underneath it — and only measurements that name their versions can tell you which change travelled with which symptom.

## The Tale of Tahmures

### The Setting

For seven days the tower of distant provinces recorded every message it translated: the sending province, the seal, the hour, how long each reply took, the rations it cost, and whether a local clerk accepted the result. At dawn on the eighth day, the divs changed their dialect. Most translations remained smooth. The overall acceptance mark moved by less than one stroke in a hundred.

### The Request

Tahmures asked whether the tower's service remained sound. The tower master presented one average for quality, one for delay, and one for cost. All sat inside their painted bands. On that evidence, continuing service was reasonable.

### The Unexpected Result

At the eastern border, negated travel orders began losing their exceptions. That province supplied few messages, so its failures vanished inside the kingdom-wide average. A reserve route, taken when the first failed, also doubled the cost of long records, but short requests concealed it. The tower's keepers knew the name of the dialect the divs used, yet had not recorded its revision beside the command's wording, the governing rules, the shelves consulted, and the body of records. They could see when complaints began but not which change travelled with them. The tower stood ready, and for one small, consequential part of the kingdom it answered fluently and wrongly.

### The Discovery

The First Scribe divided the tower's tallies by task, risk, language, province, length, and known boundary case. Every entry named the batch of work that produced it, and the revision of its dialect, wording, rules, records, and mechanism. The tower's declared standards included disqualifying safety rates as well as averages; a missing examination was not counted as a pass. Quiet rehearsals beside the old dialect, and one small province entrusted with the new one, preceded any wider change. Alarms named the failing part and the revisions that had changed with it. Restoring the old dialect returned a coherent bundle rather than only yesterday's wording. The tower's book of duties separated the divs' own refusals, commands stopped by rule, an absent examiner, stale records, and failing quality. Tahmures learned that reliability in service was a continuing practice of measurement, not the memory of a triumphant first day.

They replayed the seventh day's messages through both dialects without delivering either answer. The new dialect improved short western notices and damaged long eastern negations. The trial province therefore carried only work that could be undone. When its border mark crossed the red line, the tower restored the old dialect together with its matching wording and rules. The next rehearsal silenced the examiner itself. The keepers reported those hours as unknown and narrowed the service rather than calling unexamined messages successful. By sunset, the plain green average had been replaced by a map whose small provinces could no longer disappear. The eastern clerk sent one final note: the corrected exceptions had arrived before the pass closed. Tahmures pinned it beside the smallest segment on the map, where gratitude could not be mistaken for a measure but could remind the tower what its measures protected.

### From Tale to Engineering

A prompted system can drift while aggregate dashboards remain green. Operations require version-complete traces, segmented outcome metrics, explicit service objectives, controlled rollout, and tested rollback.

## The Engineering Problem

Everything before this chapter happened at a point in time: a prompt was written, an experiment ran, a release gate passed. Production is not a point in time. The model provider silently retires a revision; someone edits a policy list; the retrieval index is rebuilt; the traffic mix shifts toward a region the dataset under-sampled. Each change is invisible in the code you deploy, and each can move behaviour while every average you watch stays reassuringly green — because an average is a population statistic, and a small failing segment is precisely the population an average is built to bury.

The tale compresses the two failures of the discipline into one morning. First, the *aggregation failure*: eastern border messages failed, but they were few, so the kingdom-wide mark barely moved. Second, the *attribution failure*: operators saw the complaints begin but could not name the change that travelled with them, because the events arriving for analysis said nothing about which model revision, prompt version, policy version, or dataset snapshot produced them. The first failure needs segmentation; the second needs version identity written into every event at the moment it happens, because no amount of after-the-fact archaeology can recover a version that was never recorded.

The failure owner is operations and release engineering — not the model, whose behaviour changed exactly as models do, and not the prompt, which did not change at all. The system's *measurement contract* failed to be sensitive to what mattered and failed to attribute what it sensed. This chapter builds that contract.

## Mental Model

Hold two pictures side by side. The tower master's dashboard is a **thermometer**: one number, one room, no map. The map that replaced it is a **field survey taken in layers**: every plot (event) carries its own coordinates (versions), surveys are compared season to season (window against window, never moment against moment), and each small province (tag) is read separately before the kingdom is summarised.

The survey has a fixed grammar — the same five questions in the same order, every time. What are the *objectives*: the minimum quality, the maximum error rate, the worst tolerable delay, the cost ceiling, and the size of decline that counts as drift? What is in each *window*: a set of events, each stamped with model, prompt, policy, and dataset versions? What does each *segment* say, when events are grouped by tag before averaging? What *changed* between the windows, dimension by dimension? And therefore, what is the *finding*: which objectives were violated, in which segments, alongside which version changes?

The discipline that makes the survey trustworthy is subtraction in a fixed order: objectives are declared before the windows are read, segments are summarised before the kingdom, and attribution (what changed) is reported *beside* the findings (what broke) without pretending to be a causal proof. A changed model riding along with a failing segment is a lead, not a verdict.

## Core Concepts

**The event is version-complete or worthless.** A `TelemetryEvent` records the run id, model id, prompt version, policy version, and dataset version, alongside outcome, a quality score, latency in milliseconds, token counts, cost, and free-form tags. The version fields are not decoration: the comparison refuses to run if any of them is empty on any event, because an unattributable measurement is exactly the tower's original failure. The rule to internalise: *record the version at the moment of the run*, when it costs one field, rather than at the moment of the incident, when it costs an investigation.

**Windows, not moments.** Behaviour is summarised over a set of events — a window — producing a `WindowSummary`: the count, the mean quality, the error rate (the fraction of events whose outcome is not `success`), the 95th-percentile latency, and the mean cost. Comparing a single bad run against a single good one is weather; comparing window against window is climate. The empty window is an error, not a zero: silence is not evidence of health.

**What p95 actually computes.** Latency percentiles have a mechanical definition here: sort the window's latencies and take the value at position `ceil(0.95 × n) − 1`. Two consequences follow, and both are teaching, not trivia. In a window of ten events the position is the *maximum* — the rule keeps selecting the maximum through nineteen events and becomes the second-largest value at exactly twenty, so small windows make the percentile a worst-case check. And because the position is an integer index, the same real-world slowdown can move p95 by zero or by the full gap depending on how many events sit above it. Window size is part of the metric's meaning.

**Objectives are a policy object, declared in advance.** An `OperationalPolicy` carries five knobs: minimum quality, maximum error rate, maximum p95 latency, maximum mean cost, and the quality decline that counts as drift. Declaring them before reading results is the Chapter 19 discipline transplanted to operations: a threshold chosen after seeing the numbers is not a control, it is a description.

**Findings are a fixed vocabulary, not prose.** The comparison emits findings from a closed set: `quality_slo` (window mean below the minimum), `quality_drift` (baseline mean minus current mean exceeding the drift allowance), `error_rate_slo`, `latency_slo`, `cost_slo`, and `tag_quality:<tag>` — one per tag whose own mean quality falls below the minimum. Closed vocabularies are what make findings monitorable and diffable across releases; free-text alarms are what make dashboards ignorable.

**Segmentation is per-tag.** Every event may carry tags, and the report summarises the current window once per tag. Tags are the map's provinces: region, record length, task type, known boundary case — the chapter's experiment uses `east` and `long`. Note the asymmetry the contract is honest about: quality is checked per tag, but latency, cost, and error findings are window-level only. Segmenting those is a natural production extension, not a behaviour this contract has.

**Attribution is reported, not proven.** `changed_versions` lists the dimensions whose version sets differ between windows — model, prompt, policy, dataset. It answers "what changed", which is a necessary input to diagnosis, and deliberately does not answer "what caused the finding". That jump — from co-occurrence to cause — is the operator's judgement, exercised with the replay bench.

## Prompt Pattern

The experiment's two template files stage the contrast in one line each. The naive variant instructs: *"Decide whether the service is healthy from its overall average."* The governed variant instructs: *"Compare versioned windows, SLOs, and tagged segments; report drift and attribution."* The first is the tower master's dashboard as an instruction — it can only return the thermometer's one number. The governed line, by contrast, commissions rather than judges: it names the windows, objectives, segments, and version dimensions, and the surrounding code — not the model — does the comparing.

(SLO — a service-level objective — is the standard name for the declared thresholds in the policy object: the minimums and maximums a service promises to hold. The term earns its keep because it distinguishes the *promise*, which is written down before deployment, from the *measurement*, which the window comparison produces.)

The prompt's honest work in operations is summarisation and triage drafting: turning a finding set into an incident narrative, an operator-readable digest, a runbook suggestion. The record itself — events, windows, findings, changed versions — is typed data produced by code, because a summary that *is* the record cannot be audited, diffed, or replayed.

## Naive Attempt

The aggregate dashboard is the naive design, and its failure mode is precise: it is not *wrong*, it is insensitive by construction. On the chapter's fixture, the `aggregate_only` variant is asked about a window in which the model changed and one region collapsed. It answers `{"passed": true, "findings": [], "changed_versions": []}` — every case, including the failing ones. The same question to `versioned_segments` returns `passed: false`, the failing tags, and the model dimension.

Read the naive answer twice. It reported *healthy* not because nothing happened but because its instrument could only produce one number, and the number was fine. The dashboard was green; the eastern border was fluent and wrong; and the operator had no version trail to check even after complaints arrived. Aggregation is a choice to be blind to minorities, and traffic always has minorities.

## Failure Analysis

Operational failures form a taxonomy, and the runbook's first job is telling them apart — the tale's final discovery insists on separating provider error, policy denial, evaluator outage, data drift, and quality regression, because each has a different owner and a different response.

- **Aggregation masking.** A segment fails inside a green mean. The countermeasure is per-tag summaries and per-tag findings — which exist for quality in this contract and must be extended to other dimensions in production.
- **Missing version identity.** Events arrive without model/prompt/policy/dataset stamps, so symptoms cannot be correlated with changes. The contract refuses such events outright; the operational lesson is that the refusal must happen at ingest, in production telemetry too.
- **Threshold after the fact.** Choosing the quality minimum once you have seen the numbers converts a control into a rationalisation. Declare objectives in the policy, version them, and change them through review.
- **Unevaluated as success.** When the evaluator itself is down, the missing measurement must count as *unknown*, never as a pass — the tale's drill reduced service rather than fake a green mark. A window with no verdict is not a healthy window; it is a hole in the record.
- **Attribution leap.** "The model changed and quality fell" is co-occurrence. The replay bench — re-running the previous window's events through the current configuration — is what converts co-occurrence into evidence, and it is deliberately a *process* in this teaching (the experiment replays committed fixtures), not a contract feature.
- **Rollback of one thing.** Restoring yesterday's prompt while keeping today's incompatible policy or index creates a *new* failure. The unit of rollback is the coherent bundle — model with its prompt, policy, and dataset versions that were validated together.

## Improved Design

The teaching contract makes the survey executable: `compare_windows(baseline, current, policy)` validates the policy ranges, refuses any event lacking version identity, summarises each window, summarises the current window per tag, emits findings from the closed vocabulary, and lists changed version dimensions. The report is a `passed` flag plus the two window summaries, the tag summaries, the findings tuple, and the attribution tuple. It is deterministic and offline: same windows, same policy, same report — which is what makes it a gate rather than an opinion.

What sits deliberately outside the contract, as *process around it*: canary and shadow execution (routing a small, reversible slice of traffic to the candidate before wider release — the tale's trial province carried only work that could be undone), the replay bench, coherent-bundle rollback, kill switches, and alert routing. The contract provides the evidence these processes consume: the canary's red line is a `tag_quality` finding; the rollback decision reads `changed_versions`; the runbook's branches are keyed to the findings vocabulary. In production these are schedulers and pipelines; here they are described so the reader knows exactly where the deterministic part ends and the operational discipline begins.

## Worked Example

Rebuild the tale's morning as one report. The policy: minimum quality 0.80, maximum error rate 0.10, maximum p95 latency 900 ms, maximum mean cost 6.0 units, drift allowance 0.05. The baseline window holds ten events from the old dialect (`dial-v1`): eight short western notices and two long eastern orders, all successes, quality from 0.86 to 0.91, latencies 600–810 ms, costs 4.7–5.6. The current window holds ten events from the new dialect (`dial-v2`): the western notices slightly *improved* (0.89–0.93), the two eastern orders degraded to 0.56 and 0.58 with costs of 8.9 and 9.1.

The comparison returns this report:

```text
passed:          False
baseline:        count=10  mean_quality=0.884  error_rate=0.0  p95=810   mean_cost=5.1
current:         count=10  mean_quality=0.842  error_rate=0.0  p95=890   mean_cost=5.8
findings:        tag_quality:east, tag_quality:long
changed_versions: model
tag summaries:   east  count=2  mean_quality=0.57  mean_cost=9.0
                 long  count=2  mean_quality=0.57  mean_cost=9.0
                 west  count=8  mean_quality=0.91  mean_cost=5.0
                 short count=8  mean_quality=0.91  mean_cost=5.0
```

Walk the diagnosis the way the tower learned to. The aggregate is *green*: current mean quality 0.842 sits above the 0.80 minimum, the drift from 0.884 is 0.042 — under the 0.05 allowance — no errors, p95 890 under the 900 ceiling, mean cost 5.8 under 6.0. The thermometer would have reported health, and the naive variant of the experiment does exactly that. The findings come entirely from the segments: `tag_quality:east` and `tag_quality:long` both fire, because the same two failing events carry both tags — the collapse is visible through the region lens and the record-length lens, and each lens names a different suspicion (a border dialect issue, or a long-context issue). Attribution says the model dimension changed. The eastern cost doubling hides one level deeper: no finding fires for it (cost findings are window-level, and the western majority absorbs 5.8 < 6.0), but the tag summaries expose it — eastern mean cost 9.0 against the western 5.0 — which is why the report carries summaries, not just findings, and why operators read both.

Now vary one thing at a time, as in every prior chapter. Compare the baseline with itself: `passed: True`, no findings, no changed dimensions — the healthy control. Tighten the drift allowance to 0.03 and the same windows add `quality_drift`: the aggregate's 0.042 decline was real, just under the default radar — threshold selection *is* sensitivity selection. Move the two eastern events up to quality 0.75 and the findings remain: the tag mean, 0.75, is still below the 0.80 minimum, so `tag_quality:east` and `tag_quality:long` keep firing while the aggregate window stays green. Raise them to exactly 0.80 and the tags fall silent — the comparison is `< minimum_quality`, not `<=`, so at the boundary itself the segment disappears while every window-level number stays green, and the failure is now too small to see at all. That is the window-size lesson: ten-event windows see only collapses, not erosion. These are the knobs and their meanings; choosing them is the trade-off section's subject.

## Experiment

Run the shared, provider-neutral fixture experiment:

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch23-operations.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch23-operations.json
```

The manifest compares `aggregate_only` with `versioned_segments` over three committed cases. `regional_drift` is the worked example's shape — a tag-level quality failure with a model change; the naive variant passes it, the governed variant reports `passed: false`, findings `["tag_quality:border"]`, and `changed_versions: ["model"]`. `cost_drift` is the aggregate cost ceiling crossed after a prompt change; the naive variant again reports health, the governed variant reports `cost_slo` with `changed_versions: ["prompt"]`. `healthy` is the control both variants pass. The `operational_drift` evaluator reports three metrics: `drift_decision_accuracy` (did the reported pass/fail match the contract's), `finding_recall` (what fraction of the expected findings the report named), and `version_attribution` (did valid changed-dimension sets agree exactly). Across the committed cases the governed variant scores 1.0 on all three metrics; the naive variant misses both failures entirely. These results demonstrate the report mechanics and the staged failure modes; they are not evidence that any particular wording or provider behaves universally, and controlled recordings should replace the fixtures before provider-specific conclusions.

## Evaluation

Measure what the included evaluator reports: `drift_decision_accuracy`, `finding_recall`, and `version_attribution`, per variant, against the expected reports in the dataset. The window summaries, tag summaries, `findings`, and `changed_versions` are operational contract fields verified by unit tests over `compare_windows`. The evaluator separately scores reported findings and version attribution against the dataset expectations; its metric keys are not fields emitted by the operational contract.

`version_attribution` is exact changed-dimension set agreement: expected and received `changed_versions` must both be present JSON arrays of strings, and their sets must be equal for 1.0; every other case scores 0.0. Order and duplicate string occurrences do not change equality. False extras, missing or wrong-only dimensions, missing/null/wrong-type values, and mixed-element arrays fail. An empty expected set agrees only with a valid empty received set, so fabricated attribution on a healthy case fails. By contrast, `finding_recall` measures coverage of expected findings; it remains recall-like and does not itself penalise every false-extra finding. Production extensions — sensitivity curves per threshold, alert precision and fatigue rates, canary kill accuracy — are operational telemetry you must build; record them as evaluator extensions if they are to gate releases, rather than describing them into existence. The Chapter 20 rule applies unchanged: an operational gate is an evaluator with a version and an owner, and a skipped evaluation is unknown, not passed.

## Implementation Lab

### Python

```python
from tahmures.operations import (
    OperationalPolicy,
    TelemetryEvent,
    compare_windows,
)

policy = OperationalPolicy(
    minimum_quality=0.80,
    maximum_error_rate=0.10,
    maximum_p95_latency_ms=900,
    maximum_mean_cost=6.0,
    quality_drift=0.05,
)

def event(model, run, quality, latency, cost, tags):
    return TelemetryEvent(
        run_id=run,
        model_id=model,
        prompt_version="px-9",
        policy_version="pol-3",
        dataset_version="ds-12",
        outcome="success",
        quality=quality,
        latency_ms=latency,
        input_tokens=900,
        output_tokens=400,
        cost_units=cost,
        tags=tags,
    )


west = ("west", "short")
east = ("east", "long")

baseline = (
    event("dial-v1", "r-b0", 0.87, 610, 4.8, west),
    event("dial-v1", "r-b1", 0.88, 640, 5.0, west),
    event("dial-v1", "r-b2", 0.86, 600, 4.7, west),
    event("dial-v1", "r-b3", 0.89, 655, 5.1, west),
    event("dial-v1", "r-b4", 0.90, 670, 5.2, west),
    event("dial-v1", "r-b5", 0.87, 620, 4.9, west),
    event("dial-v1", "r-b6", 0.88, 630, 5.0, west),
    event("dial-v1", "r-b7", 0.91, 660, 5.3, west),
    event("dial-v1", "r-b8", 0.88, 790, 5.4, east),
    event("dial-v1", "r-b9", 0.90, 810, 5.6, east),
)

current = (
    event("dial-v2", "r-c0", 0.90, 590, 4.8, west),
    event("dial-v2", "r-c1", 0.91, 610, 5.0, west),
    event("dial-v2", "r-c2", 0.89, 600, 4.7, west),
    event("dial-v2", "r-c3", 0.92, 630, 5.1, west),
    event("dial-v2", "r-c4", 0.93, 640, 5.2, west),
    event("dial-v2", "r-c5", 0.90, 615, 4.9, west),
    event("dial-v2", "r-c6", 0.91, 620, 5.0, west),
    event("dial-v2", "r-c7", 0.92, 650, 5.3, west),
    event("dial-v2", "r-c8", 0.56, 870, 8.9, east),
    event("dial-v2", "r-c9", 0.58, 890, 9.1, east),
)

report = compare_windows(baseline, current, policy)
print(report.passed)
print(report.findings)
print(report.changed_versions)
print(report.tag_summaries["east"].mean_quality)
```

These are the worked example's ten events per window, built through a small helper so the pattern stays visible: eight western readings holding steady, two eastern readings collapsing. Run the comparison and confirm the report matches the artefact above. Then change one knob at a time: the drift allowance, the eastern qualities, the model id. Python 3.12 is the canonical educational implementation.

### Go

```go
policy := tahmures.OperationalPolicy{
	MinimumQuality:      0.80,
	MaximumErrorRate:    0.10,
	MaximumP95LatencyMS: 900,
	MaximumMeanCost:     6.0,
	QualityDrift:        0.05,
}

newEvent := func(model, run string, quality float64, latency int, cost float64, tags []string) tahmures.TelemetryEvent {
	return tahmures.TelemetryEvent{
		RunID: run, ModelID: model,
		PromptVersion: "px-9", PolicyVersion: "pol-3", DatasetVersion: "ds-12",
		Outcome: "success", Quality: quality, LatencyMS: latency,
		InputTokens: 900, OutputTokens: 400, CostUnits: cost,
		Tags: tags,
	}
}

west := []string{"west", "short"}
east := []string{"east", "long"}

baseline := []tahmures.TelemetryEvent{
	newEvent("dial-v1", "r-b0", 0.87, 610, 4.8, west),
	newEvent("dial-v1", "r-b1", 0.88, 640, 5.0, west),
	newEvent("dial-v1", "r-b2", 0.86, 600, 4.7, west),
	newEvent("dial-v1", "r-b3", 0.89, 655, 5.1, west),
	newEvent("dial-v1", "r-b4", 0.90, 670, 5.2, west),
	newEvent("dial-v1", "r-b5", 0.87, 620, 4.9, west),
	newEvent("dial-v1", "r-b6", 0.88, 630, 5.0, west),
	newEvent("dial-v1", "r-b7", 0.91, 660, 5.3, west),
	newEvent("dial-v1", "r-b8", 0.88, 790, 5.4, east),
	newEvent("dial-v1", "r-b9", 0.90, 810, 5.6, east),
}

current := []tahmures.TelemetryEvent{
	newEvent("dial-v2", "r-c0", 0.90, 590, 4.8, west),
	newEvent("dial-v2", "r-c1", 0.91, 610, 5.0, west),
	newEvent("dial-v2", "r-c2", 0.89, 600, 4.7, west),
	newEvent("dial-v2", "r-c3", 0.92, 630, 5.1, west),
	newEvent("dial-v2", "r-c4", 0.93, 640, 5.2, west),
	newEvent("dial-v2", "r-c5", 0.90, 615, 4.9, west),
	newEvent("dial-v2", "r-c6", 0.91, 620, 5.0, west),
	newEvent("dial-v2", "r-c7", 0.92, 650, 5.3, west),
	newEvent("dial-v2", "r-c8", 0.56, 870, 8.9, east),
	newEvent("dial-v2", "r-c9", 0.58, 890, 9.1, east),
}

report, err := tahmures.CompareWindows(baseline, current, policy)
if err != nil {
	return err
}
fmt.Println(report.Passed)
fmt.Println(report.Findings)
fmt.Println(report.ChangedVersions)
fmt.Println(report.TagSummaries["east"].MeanQuality)
```

The Go implementation reports identical fields and refuses the same invalid inputs; equivalence concerns observable behaviour, not syntax.

## Failure Modes

Beyond the failure analysis taxonomy, watch for these recurring shapes:

- **The dashboard that replaced thinking.** A green aggregate becomes the argument for doing nothing. The worked example is the counterexample printed as a report: every window-level number healthy, one segment collapsed.
- **Version sprawl.** Events are stamped, but with a dozen ad-hoc labels; "v2-final" and "v2" compare as different dimensions. Version strings are a contract too — format them once, enforce them at ingest.
- **Tag design by accident.** Tags that mirror the majority population (most traffic is western and short) detect nothing about the minority. Choose tags from *risk* — the boundary cases Chapter 20 protects are exactly the tags an operational window should carry.
- **Threshold cargo cult.** Minimums copied from another system's policy, never revisited, eventually describe a service that no longer exists. Thresholds need owners and review dates, like any other control.
- **The unmonitored monitor.** The evaluator's own outage is a failure mode of the gate, not of the system — the tale's drill treats an evaluator-down window as *unknown* and reduces service. Instrument the instrumentation.

## Security Considerations

Telemetry is an attack surface with a clipboard. Version fields are trusted inputs here — a component that lies about its model id poisons attribution, so in production the ingest path must authenticate event sources and treat telemetry as untrusted data crossing a trust boundary, in exactly the Chapter 21 sense. Quality scores arrive from evaluators that can be wrong or captured; a hostile or buggy evaluator that scores its own output green is the operations layer's version of the self-grading model, and Chapter 19's evaluator governance applies. Cost and latency fields are the easiest to manipulate quietly, and they drive rollback decisions — protect the path from measurement to automated action with the same approval discipline Chapter 22 gives consequential action: an automated rollback triggered by forged telemetry is a denial-of-service weapon pointed at your own release. Finally, events carry content-adjacent data (tags, run ids); minimise payloads, and keep the eastern clerk's note out of the metrics — gratitude is not a metric, and neither is a customer's name.

## Operational Considerations

Two design decisions dominate this layer's day-to-day quality, and both are easy to overlook, so they get explicit treatment here.

**Window size.** The statistics above are exact but unforgiving: with ten events, p95 *is* the maximum and a single outlier decides the latency finding; with a hundred, the same outlier moves the percentile by less. Small windows see collapses and miss erosion; large windows see erosion and bury collapses that age out slowly. Practical guidance: size windows by event count, not clock time, when traffic is bursty; keep two window scales (a fast one for alarms, a slow one for trends); and never let a segment's window shrink below the count where its percentile means anything — a two-event tag has a mean and a story, not a percentile.

**Threshold selection.** Every knob in the policy is a sensitivity choice: tighten the drift allowance and you catch slow erosions while paging operators for noise; loosen it and you sleep through the tale's morning. Ground each threshold in a consequence (the eastern order's exception loss), pick it from a replay of known-bad windows rather than from intuition, version it in the policy object, and re-derive it whenever the traffic mix shifts. A threshold without a remembered failure it was tuned against is a painted band on a thermometer.

## Trade-Offs

**Sensitivity versus alert fatigue.** A gate that fires on every wobble trains operators to ignore it; one that fires only on collapses misses erosion. The closed findings vocabulary is the mitigation — monotone, diffable, rankable — but the threshold positions remain a judgement about how much noise your operators can metabolise.

**Canary size versus risk exposure.** A one-percent canary risks almost nothing and sees almost nothing (a rare border failure may not appear in it at all); a broad canary sees much and harms much. The tale's rule is the compromise: canaries receive *reversible* work only, so the exposure is measured in annoyance rather than damage.

**Rollback speed versus diagnostic preservation.** Rolling back the coherent bundle immediately stops the bleeding and destroys the incident scene — current-window events stop arriving for the diagnosis. Preserve the evidence first: export the failing windows, tag them, and let the replay bench keep them reproducible before the bundle is restored.

**Version pinning versus improvement speed.** Pinning every dimension (model, prompt, policy, dataset) makes behaviour reproducible and improvements impossible; floating with upstream revisions ships improvements and unattributable regressions simultaneously. The middle path is deliberate, reviewed unpinning — one dimension at a time, with the window comparison watching the seam.

**Telemetry detail versus storage and privacy cost.** Version-complete, tag-rich, per-event records make diagnosis precise and storage expensive; sampled aggregates are cheap and blind. The event schema here is deliberately minimal for teaching; production choices about what to keep, sample, or drop are retention policy, and Chapter 22's receipt discipline applies — retain by purpose, not by fear.

## When Prompting Is Not the Answer

The record is not a conversation. An operational state — which versions served which window, which segments failed, what changed between baseline and current — is typed data with an invariant: it must be complete, ordered, and diffable after the fact, and no generated summary can stand in for it, because a summary is exactly the thing that changes when you re-read it. A model belongs in this layer at the edges: drafting the incident narrative from findings, triaging which runbook branch a finding suggests, explaining a report to a stakeholder. The events, windows, findings, and attribution are produced by deterministic code, because the question an incident asks — *what exactly changed, and where exactly did it hurt* — has answers that must not depend on how a paragraph was worded that morning. If your monitoring story is a daily model-generated summary of how things seem, the morning the dialect changes, the summary will be the only thing still reading green.

## Exercises

1. Reproduce the worked example, then construct the *invisible failure*: modify the two eastern events until no finding fires while the window stays green, and note the quality level at which the segment disappears. Use that boundary to justify a window size and a tag design for a system you operate.
2. The report shows `changed_versions: ("model", "prompt")` and `findings: ("tag_quality:border",)`. Write the three diagnostic hypotheses this evidence supports, the replay experiment that would distinguish them, and what the runbook should say while the replay runs.
3. Design the tags for a real system you know: list the risk-bearing segments (region, language, record length, task type, known boundary cases), and identify which of them would be minorities too small for their own window. Propose how the fast/slow window pair covers each.
4. Your team wants an automated rollback: any window report with `passed: false` restores the previous coherent bundle. Using Chapter 22's vocabulary, specify what the rollback action is (effect class, digest of what exactly is being reverted, who or what approves it, what expiry a rollback authorisation needs), and what must be preserved before it executes.
5. The evaluator that produces the quality scores goes down for an hour. Specify precisely what the window comparison should report for events processed during that hour, what the policy says about `passed`, and how your answer differs from scoring those events as successes.

## Chapter Summary

Production reliability is a measurement practice, not a launch memory. The mechanism of this chapter is the versioned, segmented window comparison: every event stamped with the model, prompt, policy, and dataset that produced it; windows summarised and compared against objectives declared in advance; quality findings raised per tag so a small province cannot disappear into the kingdom's mean; and changed dimensions reported beside the findings as attribution, not as verdict. Around the deterministic core sit the operational disciplines the contract deliberately leaves as process — canary and shadow traffic, the replay bench, coherent-bundle rollback, and runbooks keyed to the findings vocabulary. The tower's final map is the chapter's image: not one green stroke but a layered survey in which the smallest failing segment stays visible, every measurement names its versions, and the question "healthy?" always decomposes into "healthy for whom, over which window, after what change".

## The Next Tale

When the rollback ended, Tahmures asked the council a harder question: which duties had they assigned to language that should never have depended on language at all?

<!-- next: ch24 -->

## Citations and Further Reading

- Sculley, D., et al. 2015. “Hidden Technical Debt in Machine Learning Systems.” *NeurIPS 2015*. https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems
