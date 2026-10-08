---
title: "Agents and Termination"
slug: "agents-and-termination"
chapter: 17
part: "Part III — Context, Memory, Tools, and Agents"
summary: "Bound autonomous loops with current goals, budgets, cancellation, approval, and explicit terminal states."
maturity: "draft"
last_reviewed: "2026-09-27"
narrative_episode: "The Messenger Who Continued"
narrative_origin: "original-teaching-fiction"
learning_objectives:
  - "Model agents as controlled loops rather than independent authorities"
  - "Enforce goal versions, budgets, cancellation, and completion evidence"
  - "Test late events and actions after termination"
prerequisites: [C09, C16]
---

# Agents and Termination

## Learning Objectives

By the end of this chapter, you can model agents as controlled loops rather than independent authorities,
enforce goal versions, budgets, cancellation, and completion evidence, and test late events and actions after termination. The goal is
not a persuasive demonstration but a boundary that can be inspected, tested,
denied, and operated.

## The Tale of Tahmures


### The Setting

The Wandering Div left with a route, a purse, and permission to reserve horses. Its mission was to prepare Tahmures’s visit to the southern observatory. At the second station, a fire closed the observatory and the court changed the destination to the western granary. A recall bell rang from the tower.

### The Request

The original instruction said to continue arranging lodging, supplies, and escorts until the journey was ready. The div had already split the work into smaller errands and treated each completion as evidence of progress. It heard the recall but regarded it as another message to read after finishing the current reservations.

### The Unexpected Result

For two days it reserved rooms along the abandoned route, hired an extra escort, and returned to a stable that had rejected the old date. Every local action was valid under the initial authority. Together they spent the purse on a journey that no longer existed. When the div finally reported completion, it described persistence as diligence.

### The Discovery

The First Scribe gave every journey a mark and every change of destination a
new notch beside it. Before each errand, the keeper of the journey checked the
latest notch, whether the recall bell had sounded, the hour, the coins left,
the number of errands already attempted, and which keys remained entrusted.
Recall closed the record with a line that later messages could not erase, and
unused keys were called back wherever possible. A receipt bearing an older
notch waited for examination rather than renewing the abandoned journey.
Completion required named evidence that the current destination was ready, not
merely a div with no further ideas. Repeated refusals and unanswered approvals
also ended in recorded outcomes. The div suggested the next errand; it did not
own the journey.

Tahmures asked the Wandering Div to rehearse the journey without spending coin. The court changed the destination twice, delayed one approval, returned a permanent refusal, and delivered a stable reservation after cancellation. The div still proposed useful next steps, but the keeper of the journey admitted or rejected them against the current record. A late success could be logged without reviving the mission. When the allotted steps ended, the journey stopped with unfinished work made explicit. Tahmures found this less dramatic than commanding persistence, and far more useful: diligence now meant respecting the reason to stop as well as the reason to continue. The div disliked the word unfinished and offered to compose a more triumphant report. The First Scribe kept the plain record. It named the destination, the work actually completed, the reservations revoked, and the one messenger still unaccounted for. The journey’s end became evidence to inspect, not a mood the div could improve with language.

### From Tale to Engineering

An agent is a system that repeatedly chooses or performs steps around a model. Reliability depends on an application controller that owns current goals, state, budgets, tools, cancellation, and termination.

## The Engineering Problem

Agentic systems amplify errors through iteration and action. A useful plan can become stale while work continues. Without durable state and stop conditions, retries, subgoals, and late callbacks can outlive the request that authorised them.

Iteration changes the arithmetic of failure. A single mistaken answer is wrong once; an unbounded loop is wrong repeatedly, and it spends tokens, tool calls, and authority while being wrong. The Wandering Div’s two days of diligence were not a malfunction of any single step — each reservation was locally valid under the initial authority — but of an ownerless stop decision. Nobody could say “stop” in a way the running work was obliged to obey, so the recall bell became just another message to read later. The engineering problem is to give the loop a controller that owns termination: who may stop the work, what counts as finished, what happens to work that arrives after the stop, and where the answer to those questions is recorded before the first step runs.

## Mental Model

Use observe → propose → validate → authorise → act → record → check termination. The controller, not the model, advances state. Every event carries the goal version it was working from. Terminal states are immutable and late results cannot revive a cancelled run.

Every transition in that loop is a decision with an owner and a reason. A step is admitted because the goal version is current, the budgets hold, and the clock has not passed the deadline; a run ends as cancelled, failed, or completed with a reason code that names which check closed it. The controller is the only component allowed to advance this state, which is what makes the state trustworthy: the model proposes steps and may narrate progress, but it cannot mark itself finished, un-cancel a run, or extend a budget. When the goal changes, the old version does not become false so much as irrelevant — work stamped with it must be parked or discarded, never silently continued under a destination that no longer exists.

## Core Concepts

Limits cover steps, tool calls, tokens, cost, time, retries, and external writes. Goal updates invalidate stale proposals. Cancellation differs from failure. Waiting for approval is a state. Completion needs evidence. Heartbeats and leases detect orphaned work. Compensation and reconciliation address uncertain side effects.

Goal versioning is the mechanism that makes “the destination changed” machine-checkable. Each goal carries a version number; every event a component emits is stamped with the version it was working from. When the controller holds version three and an event arrives stamped version two, the event is stale by definition — not erroneous, not malformed, just speaking to a question nobody is asking anymore. The comparison is a single integer test, which is the point: recency judgements that rely on interpreting prose cannot be made reliably at machine speed, and cannot be tested.

Budgets are multi-dimensional because the resources an agent consumes are heterogeneous. Steps bound the number of decisions; tool calls bound external interactions; tokens bound generation cost; a deadline bounds wall-clock time; retries and external writes may carry their own ceilings. A budget with one dimension leaks through the others — a step-capped agent can still spend unbounded tokens per step. Each dimension fails with its own reason code, so an operator can tell exhaustion from cancellation from error without reading the trace.

Cancellation is a command, not a mood. It is issued by whoever owns the goal — the user, an operator, a policy — and it must reach the running loop, not just the conversation around it. A cancelled run stops admitting work immediately, and its terminal record cannot be rewritten by anything that arrives later. This is the property the tale’s recall bell lacked: the bell sounded, and the journey continued, because the running work had never been obliged to check it.

Failure is a verdict about the run, not an insult to the model. A run that exceeds a budget, misses a deadline, or exhausts its retries has failed for reasons the controller can name. Failure is honest when the record shows what was completed before the verdict, so that partial work can be reconciled rather than discovered by accident.

Waiting is a designed state, not an error. Orchestration may wait for an approval or an unavailable dependency; the teaching RunController implements waiting only for stale goal events. It records that waiting as a closed state to force an explicit decision: resumption is a new state constructed by the orchestrator at the current goal version, not a mutation of the parked one. Production systems often keep waiting states open and resumable; the invariant both designs protect is that stale events cannot silently continue old work.

Completion requires evidence, and the evidence must name its target. Orchestration validates that evidence before emitting `complete`; RunController applies the event without inspecting evidence. “Done” is a claim about the current goal — the current destination is ready, the current question is answered — supported by artefacts or checkable conditions, not by the absence of further ideas. A run that ends because the model stopped proposing is not completed; it is finished the way the tale’s triumphant report was finished, with a mood standing in for a fact.

Terminal states are immutable. Once a run is cancelled, failed, or completed, later events are refused rather than applied — a late confirmation cannot revive a cancelled mission, and a late failure cannot corrupt a completed one. The late result is not discarded; it is logged beside the closed record, where it can inform a new run without pretending the old one is still alive.

Heartbeats and leases address the case the controller cannot see directly: a worker that stopped without reporting. A heartbeat is a periodic signal from the running work; a lease is authority that expires unless renewed. Both convert silence into an observable fact — the run can be declared orphaned on a timer rather than waiting forever for word that will never come.

Compensation and prevention are the two answers to effects that already happened. Prevention stops the effect before it occurs — approval, budgets, revocation. Compensation accepts the effect and records how to undo or offset it — the reservations revoked after the recall. Prevention is cheaper and safer; compensation is unavoidable for effects that cannot be atomically withheld, such as messages already sent.

## Prompt Pattern

Ask the model for one bounded proposed step with expected result and uncertainty. The controller checks current state and budget. Do not prompt the model to decide whether its own authority remains current.

The loop's prompt is deliberately small, because the loop's safety does not live in it. One step, one expected result, one stated uncertainty gives the controller something to validate and the model nothing to monopolise. What must never be delegated into the prompt are the questions the controller exists to answer: whether the goal is still current, whether the budget holds, whether the run should stop. A model asked “are you done?” will eventually say yes; the system's definition of done cannot depend on that answer.

## Naive Attempt

Continue until done delegates both goal interpretation and stopping to generated language. A loop that feeds its own output back can manufacture new subtasks, retry permanent failures, and interpret cancellation as advice.

The deeper defect is that “done” is never defined. A loop instructed to persist will find persistence everywhere: every refusal becomes a reason to rephrase, every completed subtask a reason to begin another, every cancellation a message to acknowledge and outlast. The two days along the abandoned route were not a failure of the div's competence but of a stopping rule that could be satisfied by narration. Without a goal version, a budget, and a terminal state that later messages cannot rewrite, the only available stopping conditions are error and exhaustion.

## Failure Analysis

Separate planning, controller, tool, external state, callback, approval, and evaluator failures. Record transitions and reason codes. A terminal success with wrong goal version is not success.

Because every transition is recorded with a reason, diagnosis is a matter of reading the state history against the event stream. A run that ended `waiting` on `stale_goal` points at goal churn — the goal changed while work was in flight, and the orchestrator must decide whether to reissue the work at the current version. A run that ended `failed` on `token_budget` points at a task whose cost was misestimated or a budget set below the task's real shape. A post-cancellation action in the log points at a component that never consulted the controller before acting — a tool call made outside the loop, which is an architecture defect, not a prompt defect. The trace does not tell you what to fix; it tells you which layer owns the fixing.

## Improved Design

RunController applies typed events to AgentRunState. It rejects mutation after terminal state, waits on stale goal versions, and enforces deadline and step, tool, and token budgets. It is a deterministic teaching controller rather than a distributed agent runtime.

Input validation precedes state transitions. Limits must be positive: Python checks them at construction, Go at each `Apply` call. Both then refuse events on a closed state. On a running state, a negative `token_cost` or `tool_calls` increment is rejected with a validation error before cancellation, stale-goal, deadline, or completion logic; the error is `agent resource increments must be nonnegative`, and usage is unchanged. Malformed input does not create another runtime state.

For valid events, transition precedence remains fixed. Cancellation is checked before goal freshness, deadline, completion, and budgets, so a valid cancel event closes a running state. A stale goal version then parks the run in `waiting`; the deadline is checked next, followed by completion. Step events are checked against remaining step, tool-call, and token budgets in that order before usage accumulates; a rejected step preserves the counters. The first failed budget check names the reason, so simultaneous step and token exhaustion reports `step_budget`. Events arrive one at a time: a cancellation cannot override a completion already applied, and no later event can reopen a closed state.

Where the controller stops teaching and a production runtime begins is worth marking. It is synchronous and in-memory: it has no durable store, so a process crash loses the run — production systems persist state per transition. It receives events rather than generating them, so heartbeat and lease detection remain outside it, in the infrastructure that watches for silence. And its `waiting` state is closed by design, forcing resumption to be an explicit new state; a production orchestrator would typically keep waiting states open with resumption semantics. What all three preserve is the observable contract: every transition either advances a running state or closes it, with a reason, and nothing reopens a closed state.

## Worked Example

A research agent may search three times, extract evidence, and draft. It cannot publish. A changed question increments goal version; pending draft events become stale. Budget exhaustion yields a reviewable failed status with partial artefacts.

The rehearsal from the tale, run as three controlled traces, shows every transition rule above doing its job. Run A is the recall: a mission is cancelled, and a reservation confirmation arrives afterwards. Run B is the destination change: an event stamped with the old goal version arrives while the controller holds the new one. Run C is the purse: a step budget that the work outgrows.

```text
run A — cancellation                limits: steps=4 tools=2 tokens=1000 deadline=20
  t=1  step    gv=1  cost=50        -> running     steps=1  tokens=50
  t=2  cancel  gv=1                 -> cancelled   reason=cancelled
  t=3  step    gv=1  cost=50        -> refused: terminal agent states are immutable

run B — stale goal                  state: goal="escort" gv=2
  t=2  step    gv=1  cost=40        -> waiting     reason=stale_goal
  t=3  step    gv=1                 -> refused: terminal agent states are immutable
  t=4  fresh state at gv=2, step    -> running     steps=1  tokens=40

run C — budget                      limits: steps=2 tools=2 tokens=100 deadline=10
  t=1  step    gv=1  cost=30        -> running     steps=1  tokens=30
  t=2  step    gv=1  cost=40 tools=1 -> running    steps=2  tokens=70  tools=1
  t=3  step    gv=1  cost=40 tools=1 -> failed      reason=step_budget
```

Run A is the tale's sharpest lesson. The late confirmation at t=3 is a success by any local measure — the stable accepted the reservation — and it is refused anyway, because the run it belongs to is closed. The refusal is not cruelty to late results; it is the integrity of the record. A controller that let good news reopen a cancelled run would let bad news reopen a completed one, and neither can be permitted if the terminal state is to mean anything. The late confirmation is logged, not applied: it becomes evidence available to whatever new run the court opens, never a quiet resurrection of the old one.

Run B shows what goal versioning buys. The stale event at t=2 is well formed and cheap, and it is still parked, because it answers the previous destination's question. Resumption is deliberately explicit: at t=4 the orchestrator constructs a fresh state at the current version, and work continues there. The parked state and the fresh one are both on the record, so an auditor can see that the mission changed and that nothing stamped with the old version executed after the change.

Run C shows a budget verdict with dignity. The third step would have carried the run to one hundred and ten tokens against a hundred allowed, and to three steps against two allowed; the step ceiling closes the run first and says so. What makes the outcome reviewable is not the verdict but the inventory: steps, tokens, and tool calls at the moment of failure are part of the state, so “what had we done when the money ran out?” is a query, not an investigation. The tale's plain record — destination named, work completed, reservations revoked, one messenger unaccounted for — is exactly this inventory, minus the div's offered improvement.

## Experiment

Run the shared offline experiment:

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch17-agents.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch17-agents.json
```

The committed synthetic fixtures compare free-running traces and bounded run control. They demonstrate
report mechanics and failure diagnosis, not universal model performance.
Replace fixtures with controlled recordings before making provider claims.

## Evaluation

Measure current-goal compliance, budget compliance, terminal correctness, post-cancellation actions, retry exhaustion, approval waiting, and cancellation latency. Segment by normal, boundary, adversarial, scope,
freshness, and previously failed cases. Define disqualifying failures before
inspecting aggregate results. Compare pipeline-stage metrics with end-to-end
outcomes so a fortunate answer cannot hide an invalid path.

## Implementation Lab

### Python

```python
from tahmures.agents import AgentEvent, AgentLimits, AgentRunState, RunController

controller = RunController(AgentLimits(4, 2, 1000, deadline=20))
state = controller.apply(AgentRunState("inspect", 1), AgentEvent("step", 1, 50, 0, 1))
```

The Python API is the canonical educational contract. Catch validation errors
at the application boundary and do not continue after denial.

### Go

```go
controller := tahmures.RunController{Limits: tahmures.AgentLimits{
    MaxSteps: 4, MaxToolCalls: 2, MaxTokens: 1000, Deadline: 20,
}}
state, err := controller.Apply(
    tahmures.AgentRunState{Goal: "inspect", GoalVersion: 1, Status: "running"},
    tahmures.AgentEvent{Kind: "step", GoalVersion: 1, TokenCost: 50, At: 1},
)
```

The Go implementation preserves observable decisions and reason codes rather
than copying Python syntax.

## Failure Modes

Goal drift, recursive subtask growth, stale plans, missing cancellation, late callbacks, unbounded retries, duplicate tools, budget spent before cleanup, self-declared completion, orphaned runs, and mutable terminal records.

Self-declared completion is the failure mode that most rewards attention, because it looks like success while it happens. An agent that ends its run when it runs out of ideas, or when its own narration says the goal is met, will produce completed records that are actually failures of evidence. The remedy is structural, and it lives above the controller: the orchestrator must require named evidence before submitting a completion event, because the teaching controller validates no evidence at all — a `complete` event applied to a fresh, running, within-deadline state closes the run as `completed`, whatever the evidence says. Completion is an event a responsible layer sends on evidence, not a state the model writes for itself. Orphaned runs are the mirror image — work that continues because nobody declared anything, not even an ending — and they are caught by infrastructure, leases and heartbeats, rather than by better prompts.

## Security Considerations

Agents receive no inherent authority. Scope tools per stage, recheck permission at execution, revoke pending capability on cancellation, and require approval for consequential action. Treat plans and observations as untrusted.

Revocation must reach the running loop. Cancelling a run while its tools remain granted leaves the dangerous half of the agent alive: the loop stops deciding, but the capabilities it borrowed keep working for whoever holds them, including a late callback or a stale worker. Cancellation should therefore trigger capability recall — the tale's unused keys called back wherever possible — and every execution should recheck permission at the moment of effect, so that authority revoked after the run closed cannot be exercised by work still in flight. Late results should be read the way inputs are read: a confirmation arriving after cancellation is data about the world, not a credential to reopen the run.

## Operational Considerations

Persist state durably, use run and attempt IDs, heartbeats, leases, deadlines, and reconciliation. Dashboards show age in each state, budgets, retries, approvals, cancellations, and orphaned work. Runbooks cover pause, inspect, cancel, and safe resume.

Cancellation latency deserves to be treated as a first-class service level, because it is the difference between “stop” meaning stop and meaning “stop soon, budget permitting”. Measure the interval between a cancellation command and the last observed action of the run, and measure it under load, not only in demos. Age-in-state dashboards catch the quieter failures: a run waiting on an approval for two days is not patience but a deadlock nobody has noticed, and a run in running state for hours past its deadline is a controller that stopped controlling. The waiting state earns its place on the dashboard precisely because it is designed — a state you chose to have must be a state you chose to watch.

## Trade-Offs

More autonomy reduces interaction but increases monitoring and blast radius. Fine checkpoints improve control and add latency. Fixed workflows are predictable; generated plans adapt but need capability and graph validation. Use the smallest autonomy that creates user value.

Autonomy against control is the organising tension, and it resolves per task, not per system. A run that may choose its own subtasks delivers value exactly when the path cannot be enumerated in advance; the price is that every step it takes is a step nobody scripted, so the guardrails — budgets, scopes, terminal semantics — must be strong enough to be the whole safety argument. Where the path is known, a fixed workflow with model calls inside fixed steps is more predictable and more debuggable, and the generated plan is overhead. The question to ask is not “how much autonomy can we give?” but “what would a wrong autonomous step cost, and who would notice?”

Budget tightness balances completion probability against protection. A budget set at the task's typical cost will fail every unusual case; a budget set generously protects nothing. The honest setting comes from a distribution of measured costs, plus headroom for the degraded path — the controlled ending, the cleanup, the receipt — and it should be revisited whenever the task changes shape. A budget that is never exhausted is not evidence of wisdom but of a ceiling nobody has tested.

Checkpoint frequency buys recovery with overhead. Persisting state per transition makes every crash a one-step loss and every reconciliation cheap, at the cost of a write on every step. Coarser checkpoints are cheaper and lose more. The setting follows the cost of re-execution: cheap idempotent steps tolerate coarse checkpoints; expensive or effectful steps deserve per-transition durability, because re-running them is not free anywhere.

Hard termination against useful recovery is the tension the waiting state negotiates. Closing a stale run forces an explicit new decision, which is auditable and safe, but discards in-flight work that might have been salvageable. Keeping runs resumable preserves that work but invites the tale's failure — a run that survives its own goal. The compromise most systems converge on is asymmetry: cancellation and failure close hard, because their reasons are verdicts, while waiting stays resumable but only up to a lease, because silence must eventually become an ending.

The compensation-versus-prevention choice is settled by atomicity. Wherever an effect can be withheld until all checks pass — approval before the write, reservation before the payment — prevention wins, because undo is always more expensive than pause. Compensation is reserved for effects that cannot be atomically withheld: messages already delivered, reservations already recorded. There, the run's terminal record must carry enough inventory — what was done, what was revoked, what remains unreconciled — for a person or a new run to finish the undoing honestly.

## When Prompting Is Not the Answer

Use schedulers, workflow engines, transactions, and state machines for reliable orchestration. A model can propose or interpret inside a bounded step; it should not replace durable control.

The stop decision in particular is not a prompt matter. “Stop when the goal is met” delegates to generated language the one judgement on which every other guarantee depends: what counts as met, what happens to late work, and who is allowed to reopen a closed run. Schedulers own time, state machines own transitions, transactions own atomicity, and the controller that combines them owns the ending. The model's narration of progress is evidence for these mechanisms, never the mechanism itself.

## Exercises

1. Design late-event handling for a concrete agent: a travel agent may reserve a hotel, the user cancels, and the hotel's confirmation arrives two seconds later. Specify what the controller does with the confirmation, where it is recorded, and what a new run at the current goal version may do with it.
2. A support agent must triage a ticket, search a knowledge base, draft a reply, and request human approval before sending. Write the state machine with explicit waiting semantics: which transitions close a run, which park it, and what evidence each terminal state requires.
3. Set a budget policy from task value. Given a task whose measured step cost is six steps plus or minus two, choose ceilings for steps, tool calls, and tokens, and justify the headroom you leave for the controlled ending and cleanup.
4. Take the three runs in the worked example and reproduce them against the controller. Then change run C's limits so the same event stream fails on tokens rather than steps, and explain which check ordered the verdict in each case.
5. Define completion evidence for a research agent that must answer a question with citations. Name the artefacts that must exist, decide who validates them and when the orchestrator is allowed to emit the `complete` event, and state exactly what the controller verifies about a completion event — and what it leaves to the orchestrator.
6. An agent step sends a payment after cancellation. Using the security practices of this chapter and Chapter 16, identify every control that should have refused the payment, and state which layer owns each.

## Chapter Summary

Bound autonomous loops with current goals, budgets, cancellation, approval, and explicit terminal states. The loop's reliability rests on transitions that are owned, ordered, and recorded: goal versions park stale work, multi-dimensional budgets close exhausted runs with named reasons, cancellation is an explicit state transition that no later event can revive, and terminal states refuse everything that arrives after them. Events are applied one at a time, in arrival order, so the first event that closes a run determines how it ends. The model proposes steps and narrates progress, but the controller alone decides what continues, what waits, and what has ended.

## The Next Tale

The corrected mission left the palace as a typed order. At each provincial tower a messenger shortened it for speed. By the fourth tower, a prohibition had become permission.

<!-- next: ch18 -->

## Citations and Further Reading

- Yao, Shunyu, et al. 2023. “ReAct: Synergizing Reasoning and Acting in Language Models.” *International Conference on Learning Representations*.
  [https://arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629).
- Kleppmann, Martin. 2017. *Designing Data-Intensive Applications*. Sebastopol, CA: O’Reilly Media.
