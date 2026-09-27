---
title: "Decomposition and Workflows"
slug: "decomposition-and-workflows"
chapter: 9
part: "Part II — Designing Prompted Interactions"
summary: "Split complex work by observable responsibility, explicit dependencies, checkpoints, and terminal states."
maturity: "draft"
last_reviewed: "2026-07-29"
narrative_episode: "The Mountain in One Command"
narrative_origin: "original-teaching-fiction"
learning_objectives:
  - "Decompose tasks into independently verifiable stages"
  - "Validate workflow dependencies, checkpoints, and termination"
  - "Design bounded retries and compensation for partial failure"
prerequisites: [C03, C08]
---

# Decomposition and Workflows


## Learning Objectives

You will turn an opaque multi-step request into a workflow with named
responsibilities, declared inputs and outputs, acyclic dependencies,
checkpoints, and one terminal outcome. You will recognise when decomposition
adds needless coordination and when it creates essential observability.

## The Tale of Tahmures


### The Setting

The mountain messenger’s field diary was recovered from a leather tube beside
the western pass. Its first page carried Tahmures’s command:

> Find the stranded surveyors, determine their condition, choose a safe route,
> deliver provisions, and return with a complete report.

Below it, the messenger had written, “A clear order. I leave at dawn.”

Snow had erased the road markers. Two shepherds disagreed about the surveyors’
camp. The eastern path was shorter; the southern path crossed lower ground.

### The Request

Tahmures had selected a Wandering Div for speed and given it the diary, pack
animals, and authority to purchase supplies. “Complete the mission,” he said.
“Do not trouble the court with every footstep.”

The div reached a fire-blackened campsite, found three sets of tracks, chose
the eastern path, bought food for eight people, and returned before the second
storm. Its report declared the mission mostly successful: the camp located,
route chosen, supplies delivered, survivors counted.

### The Unexpected Result

The surveyors were not there.

The div had found their abandoned first camp. One track led to a hunting party,
another to the surveyors’ relocated shelter, and the third back toward the
valley. Because it counted eight sleeping places, it bought supplies for eight.
Because the eastern path was shortest on an old map, it called the route safe.
It left the food at a stone marker and completed its report.

Every part of the command appeared in the diary with a mark beside it. The
marks concealed the moment at which “located camp” became “located people.”
No intermediate record stated the evidence, and no one had been asked to
approve the route before supplies moved.

### The Discovery

The First Scribe reconstructed the mission on five wooden boards: locate,
assess, route, supply, report. Between the first and second boards he placed a
red cord.

“What must cross this cord?” Tahmures asked.

“A position with evidence, not merely a place that resembles a camp.”

They added an output to every board. *Locate* produced coordinates, observed
signs, source, and uncertainty. *Assess* produced headcount and needs or a
declared inability to assess. *Route* accepted current weather and the verified
position. Before supply, a checkpoint required a human to review any uncertain
location or changing pass. Report became terminal only after delivery evidence
or an explicit failed outcome.

Tahmures objected that messages to court would cost time. The Scribe agreed.
Not every board needed royal approval. Some checks could be local and
deterministic. Only uncertainty beyond a threshold or a changed high-risk fact
crossed the red cord.

The new plan did not promise success. It promised that a false assumption
would have a name, a record, and a place where work could stop.

### From Tale to Engineering

The original command contained all the verbs but none of the intermediate
contracts. Decomposition becomes reliable only when stages expose evidence,
dependencies, checkpoints, failure outcomes, and termination—not when a long
prompt is merely split into smaller prompts.

## The Engineering Problem

Complex tasks combine different responsibilities: gathering facts, making
judgements, selecting plans, changing state, and reporting. A single response
can make the combination look coherent while hiding which premise produced the
result. When something fails, the application cannot resume safely or decide
what must be repeated.

Decomposition introduces observable boundaries. It also introduces state,
coordination, latency, and new failure modes. The problem is to split work
along verifiable responsibilities rather than arbitrary token lengths, then
make transitions application-owned.

## Mental Model

Represent a workflow as a directed acyclic graph. Each node has a stable ID,
purpose, declared inputs, declared outputs, validation, retry policy, and
possibly a checkpoint. An edge means a node depends on a validated output, not
merely that it appears later in a prompt.

```text
locate -> assess -> route -> supply -> report
                     ^ checkpoint
```

A state machine complements the graph. Steps may be pending, ready, running,
succeeded, failed, cancelled, or waiting for approval. The workflow itself has
terminal states such as completed, failed, or cancelled. “No more model text”
is not a sufficient definition of completion.

## Core Concepts

Decompose by observable responsibility. A useful step has an outcome that can
be inspected independently. “Think more” is not a responsibility. “Extract
candidate route claims with source IDs” is. Keep deterministic transformations
in code and use generation where language interpretation or proposal is
actually needed.

Dependencies should name known step IDs and form no cycle. A step is ready only
when all its dependencies have completed successfully under the workflow’s
policy. A topological order is not enough when external state may change;
preconditions must be checked at execution time.

Intermediate contracts are just as important as final output contracts. If a
route step expects verified coordinates, the locate step must produce them in
a shared type. Free-text hand-offs invite silent reinterpretation.

Checkpoints are deliberate pauses for validation or approval. They are useful
before irreversible action, when uncertainty exceeds a threshold, or when
conditions have changed. A checkpoint does not always require a person:
schema validation, permission checks, and inventory checks can be automated.

Retries must be bounded and classified. Retry a transient timeout, not a
permanent invalid request. Preserve attempt count and causes. Repeating a
non-idempotent action can duplicate purchases or messages.

Compensation addresses completed side effects after a later failure. It is not
always rollback: grain delivered cannot be “undelivered,” but inventory can be
reconciled and stakeholders notified. Design compensation before enabling the
action.

## Prompt Pattern

Ask for a plan proposal in a validated form:

```text
Produce stages with: id, purpose, depends_on, inputs, outputs,
checkpoint, failure_outcome, and terminal.
Use only the allowed stage IDs.
Do not execute the stages.
```

Then let application code validate the graph. If a model proposes an unknown
dependency, cycle, missing contract, or no terminal state, reject the plan.
Execution is a separate component with permissions scoped per stage.

For a fixed workflow, avoid asking a model to rediscover the graph each time.
Encode the graph in code or configuration and use models only inside selected
nodes.

## Naive Attempt

The naive design sends the whole mission and asks for a complete answer. A
slightly different naive design asks the model to list steps, then blindly
executes each listed line. The first is opaque; the second grants generated
text control over orchestration.

Another mistake is splitting one long prompt into five prompts while passing
unvalidated prose between them. This multiplies inference points without
creating contracts. Errors propagate with additional confidence.

## Failure Analysis

Monolithic failures include omitted stages, unsupported transitions, premature
success, and inability to resume. Workflow failures include cycles, missing
dependencies, incompatible hand-offs, stale state, duplicate side effects,
unbounded retries, orphaned runs, and ambiguous terminal states.

The failure owner may be requirements, plan generation, orchestrator code,
tool behavior, external state, or human approval. Logs should make these
distinctions visible. “Agent failed” is rarely a sufficient diagnosis.

Parallel steps add race conditions. Two individually valid actions may conflict
over shared inventory. Long workflows add version drift: a run may begin under
one policy and finish after deployment of another. Pin workflow versions per
run or define explicit migration.

## Improved Design

Start with a task inventory. Mark which operations are deterministic, which
read external state, which cause side effects, and which require judgement.
Define outputs and failure outcomes. Draw dependencies and remove cycles.
Place checkpoints before high-consequence transitions.

Give every run an ID and every step an idempotency key where supported. Persist
state outside the model conversation. Validate inputs again when a step starts.
Use a termination policy covering success, failure, cancellation, deadline,
budget, and approval expiry.

The repository’s `WorkflowPlan` validates unique IDs, known acyclic
dependencies, declared inputs and outputs, at least one checkpoint, and exactly
one terminal step. `ready(completed_steps)` computes eligible work
deterministically. It is educational orchestration logic, not a durable
distributed workflow engine.

## Worked Example

Consider document publication:

1. `extract` produces claims and source spans.
2. `verify` labels each claim supported, contradicted, or unknown.
3. `draft` uses only supported claims.
4. `review` is a human checkpoint for high-impact content.
5. `publish` is terminal and owns the external write.

If verification fails, drafting should not become ready. If publication times
out, retry only with an idempotency key and confirmed status. If review rejects
the draft, the workflow may return to a new draft attempt under a bounded loop
implemented as state transitions, not a dependency cycle in the static plan.

## Experiment

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch09-workflows.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch09-workflows.json
```

The fixtures compare monolithic mission prose with a stages array containing
locate, assess, route, supply, and report. The evaluator checks coverage,
dependency order, required checkpoints, and one terminal state. Tags include a
false-route assumption and changing weather.

The recorded workflow is intentionally linear. Extend it with independent
weather and inventory checks, then test readiness after different completed
sets. Add invalid fixtures with unknown dependencies, cycles, missing
checkpoints, and two terminal steps.

## Evaluation

Measure required-stage coverage, dependency validity, checkpoint presence,
unsupported-transition rate, and terminal-state correctness. At runtime also
measure completion rate, time per state, retries, compensation, cancellation
latency, and approval wait time.

Do not optimise stage coverage alone; a plan can mention every stage in an
unsafe order. Evaluate intermediate contract validity and final task outcomes.
Run fault injection at each boundary. The most valuable workflow test often
asks whether the system stops safely when a precondition fails.

## Implementation Lab

### Python

```python
from tahmures.workflow import WorkflowPlan, WorkflowStep

plan = WorkflowPlan((
    WorkflowStep("locate", inputs=("mission",), outputs=("position",)),
    WorkflowStep("assess", ("locate",), ("position",), ("condition",),
                 checkpoint=True),
    WorkflowStep("report", ("assess",), ("condition",), ("record",),
                 terminal=True),
))
plan.validate()
ready = plan.ready({"locate"})
```

Validation raises a typed error before any execution. The caller owns state and
side effects.

### Go

```go
plan := tahmures.WorkflowPlan{Steps: []tahmures.WorkflowStep{
    {ID: "locate", Inputs: []string{"mission"}, Outputs: []string{"position"}},
    {ID: "assess", DependsOn: []string{"locate"},
        Inputs: []string{"position"}, Outputs: []string{"condition"},
        Checkpoint: true},
    {ID: "report", DependsOn: []string{"assess"},
        Inputs: []string{"condition"}, Outputs: []string{"record"},
        Terminal: true},
}}
ready, err := plan.Ready([]string{"locate"})
```

Persist completed states outside this value when building a real runner.

## Failure Modes

Watch for arbitrary over-decomposition, unvalidated prose hand-offs, cycles,
missing terminal states, stale preconditions, duplicate action, unbounded retry,
lost cancellation, and plans that mutate themselves without policy. A model
may propose a convincing plan that references tools it cannot access or should
not receive.

Checkpoints can become ceremonial if approvers lack evidence or routinely
click through. Design the review packet, not just the pause.

## Security Considerations

Scope credentials per step and grant read or write only where required.
Authenticate plan sources and reject generated tool names outside an allow
list. Recheck authorisation at execution, not only plan creation. Treat every
intermediate model output as untrusted until validated.

Cancellation must revoke pending capability where possible. Audit who approved
what, based on which version and evidence.

## Operational Considerations

Use durable state for long runs, deadlines, heartbeat or lease mechanisms, and
recovery after process failure. Pin plan, prompt, and evaluator versions.
Expose state transitions and reasons. Define retention for intermediate data,
which can contain more sensitive detail than final reports.

Capacity planning must include fan-out, retry amplification, and approval
queues. A five-stage workflow can cost more than five calls if failures retry.

Before release, have a reviewer reconstruct one decision from retained evidence. If its active inputs, versions, owner, and reason code cannot be identified, the boundary is not yet operationally auditable.

## Trade-Offs

Decomposition improves observability and targeted recovery but increases
latency, cost, and integration surface. Parallelism reduces elapsed time while
increasing coordination risk. Human checkpoints reduce autonomous risk but
create delay and reviewer burden. Fixed workflows are predictable; generated
plans are adaptable but need stronger validation.

Use the fewest stages that create meaningful verification and control.

A workflow design review can begin with a failure walk rather than a success
diagram. For each step, assume it never starts, times out before producing an
output, produces an invalid output, completes its external side effect but
loses the acknowledgement, or succeeds while its downstream dependency fails.
Write the observable state and permitted next transition for each case. If the
team cannot distinguish “not attempted” from “possibly completed,” retries may
duplicate action.

Review the step boundary against ownership. Two activities belong in separate
steps when they have different permissions, retry behavior, evidence, or
approvers. They need not be separate merely because they use different prompt
paragraphs. Conversely, a single “research and publish” step hides a critical
permission change even if one model can perform both. Split at the boundary
where read-only investigation becomes an external write.

Inputs should reference validated artefacts with stable identities. Passing
“the previous answer” encourages consumers to depend on conversational
position. Pass `location_assessment/v1` with a run ID, source IDs, validation
status, and creation time. Outputs should be immutable once a step succeeds;
corrections create a new attempt or artefact version so the audit trail does
not change beneath downstream work.

Readiness is not authorisation. A step whose dependencies have succeeded may
still be blocked by caller permission, deadline, budget, cancellation, or
freshness. Recheck these conditions immediately before execution. Long approval
waits are especially important: inventory, exchange rates, weather, or policy
may have changed while a human considered the request. Approval can expire or
require revalidation.

Define idempotency from the external system’s perspective. A request ID stored
only in workflow memory cannot prevent duplicate action after a crash unless
the tool or application records it transactionally with the side effect. When
the destination lacks idempotency support, create a reconciliation step that
checks state before retrying. Never assume a timeout means the action did not
happen.

Compensation should name what can actually be restored. A reserved item can
often be released. A published message can be followed by a correction but not
made unread. A disclosed secret cannot be compensated by deleting a log.
Irreversible actions deserve stronger preconditions and approvals rather than
an optimistic rollback label.

Loops require explicit budgets even when the static plan is acyclic. A
draft-review cycle might permit three revisions. Store the count and a terminal
`revision_exhausted` outcome. Do not let a model decide to continue merely
because it can still propose improvements. Bound wall-clock time, inference
cost, tool operations, and external writes as appropriate.

Review parallelism using shared resources. Steps with no graph dependency can
still conflict over inventory, rate limits, files, or user attention. Add
resource locks, reservations, or serialisation outside the language model.
When results race to a join, define whether the join waits for all, a quorum,
the first valid result, or a deadline. Preserve late results according to a
declared policy.

Human checkpoints need an information contract. Show the proposed action,
source evidence, validation results, material uncertainty, cost, and what
approval enables. Avoid a wall of generated explanation that reviewers learn
to skip. Capture approve, reject, request changes, and expiry as distinct
events. Authentication and role checks belong to the approval system, not a
typed name inside model output.

Version migration is another workflow. A run started under `rescue/v1` should
not silently continue with `rescue/v2` step definitions after deployment.
Pin versions or implement a tested migration that maps states and artefacts.
Some active runs are safer to finish under the old version; others must be
cancelled because policy changed. Document that decision before rollout.

Operational dashboards should show counts and age in every state, not only
final success. A growing `waiting_approval` queue may be a capacity problem; a
growing `ready` queue may be a worker problem; repeated invalid output may be a
prompt or model regression. Alert on orphaned leases, deadline breaches,
retry exhaustion, and compensation failure.

Test workflows with deterministic fakes before involving models. Inject each
failure, restart the runner between state writes, deliver duplicate callbacks,
cancel during every step, and change external state before approval completes.
Then add recorded model fixtures for the language nodes. This separation keeps
orchestration bugs from being misdiagnosed as prompt behavior.

The final review asks whether the workflow is needed. If a database query and a
single approved update solve the problem, five language stages add risk
without value. Decomposition is successful when it creates meaningful
verification and recovery boundaries. The number of boxes is not a maturity
metric.

Data lineage should be queryable across the run. Given the final report, an
operator ought to find the exact locate output, its source observations, the
assessment version, route approval, supply tool receipt, and every validator
result. Correlation IDs alone are insufficient if artefacts can be overwritten.
Use immutable references and record which attempt produced the value consumed
downstream.

Budget policy should cover multiple resources. A run may have limits for model
tokens, wall-clock duration, tool calls, monetary spend, retries, and human
review. Check remaining budget before a step starts and reserve enough for
required cleanup or reporting. A Wandering Div that spends the final allowance
on another planning attempt can leave no capacity to record a safe failure.

Deadline behavior needs a state, not an exception lost in logs. Decide whether
running work is cancelled, allowed to finish without starting downstream
action, or escalated. Propagate cancellation to tools that support it and
ignore late callbacks using run and attempt identity. A late successful result
must not revive a run already cancelled under newer requirements.

External events may invalidate the graph’s assumptions. A route closure,
revoked permission, or changed user request can make ready steps obsolete.
Represent relevant assumptions as preconditions with versions. Event handlers
can mark affected steps stale and require reassessment. Do not append the new
fact to a conversation and hope every later prompt interprets it correctly.

Generated planning is especially sensitive to scope creep. Validate not just
graph shape but every proposed capability, data source, and goal. A plan can be
acyclic, complete, and entirely outside the caller’s authority. Compare it
with an allowed workflow vocabulary and reject undeclared side effects.
Generated step descriptions remain untrusted text even after their IDs pass.

Evaluation should include partial success semantics. A rescue workflow that
locates people but cannot deliver supplies has created useful verified state.
The terminal outcome should not call the mission complete, yet operators may
reuse the location under freshness rules. Define which outputs remain valid
after failure and which are invalidated or quarantined.

Service-level objectives can differ by state. Planning may tolerate a minute;
revoking a pending action after cancellation may require seconds. Measure the
tail of approval and retry latency, not just averages. Long-running outliers
often reveal missing deadlines, lost callbacks, or human queues rather than
slow model inference.

Chaos tests should be repeatable and safe. Use fake tools to simulate success
followed by lost acknowledgement, conflicting callbacks, malformed outputs,
and restarts between each persistence operation. Verify invariants: no action
without approval, no dependency consumed before validation, no more than one
terminal result, and bounded attempts. These invariants provide stronger
assurance than a collection of successful end-to-end demonstrations.

Documentation should tell an operator how to pause intake, inspect a run,
retry a safe step, reconcile uncertain side effects, cancel, and resume. If
recovery requires editing database rows or conversation text by hand, the
workflow is not yet operable. Language-model applications need the same
incident discipline as other distributed systems.

Runbooks should include evidence examples for every terminal outcome. An
operator must be able to tell completed from completed-with-warning, rejected,
cancelled, deadline-exceeded, compensation-required, and uncertain-side-effect.
These names are part of the public operational contract. Avoid a generic
`failed` state that makes reconciliation depend on reading unstructured logs.

Ownership should follow steps as well as services. The team responsible for a
model extraction may differ from the team responsible for a payment tool.
Escalation routes, service-level objectives, and on-call access should reflect
that distinction. A single workflow dashboard can unify the run without
pretending one team controls every dependency.

Privacy review must consider intermediate artefacts and failed attempts. A
draft may contain sensitive information excluded from the final response.
Retries multiply copies. Define encryption, access, retention, and deletion for
every step output. Passing all history into later prompts for convenience
widens exposure and makes deletion difficult.

With these controls, decomposition gives Tahmures’s red cord an engineering
equivalent: a visible boundary at which evidence can be inspected and unsafe
continuation can stop. The workflow remains fallible, but its failures become
local enough to diagnose and govern.
That is measurable progress.
It is also the basis for safe recovery.

## When Prompting Is Not the Answer

Encode stable workflows as code, state machines, or a durable workflow engine.
Use transaction and idempotency mechanisms for side effects. Use schedulers for
time-based work and policy engines for permissions.

Prompting may interpret a document or propose candidates inside a stage. It
should not replace reliable orchestration.

## Exercises

1. Decompose a research brief into evidence-bearing stages.
2. Add an invalid cycle and confirm both implementations reject it.
3. Identify which steps need idempotency keys in an ordering workflow.
4. Design cancellation and compensation for a partially sent campaign.
5. Remove one stage from a plan and explain whether observability worsens.

## Chapter Summary

Reliable decomposition creates inspectable responsibilities, not merely
smaller prompts. Workflows need typed hand-offs, acyclic dependencies,
checkpoints, bounded retries, side-effect policy, and explicit terminal states.
Applications own validation and execution; models may propose or perform
bounded language tasks inside those controls.

## The Next Tale

Once the mission was divided, three advisers produced three valid workflow
plans. Each satisfied every declared stage yet chose a different route and
allocation. Tahmures summoned the Many-Voiced Council to decide whether
difference itself was failure.

<!-- next: ch10 -->

## Citations and Further Reading

- van der Aalst, Wil M. P. 2016. *Process Mining: Data Science in Action*. 2nd
  ed. Berlin: Springer.
  [https://doi.org/10.1007/978-3-662-49851-4](https://doi.org/10.1007/978-3-662-49851-4).
- Kleppmann, Martin. 2017. *Designing Data-Intensive Applications*. Sebastopol,
  CA: O’Reilly Media.
- Amazon Web Services. 2026. “REL04-BP04 Make Mutating Operations Idempotent.”
  *AWS Well-Architected Framework*.
