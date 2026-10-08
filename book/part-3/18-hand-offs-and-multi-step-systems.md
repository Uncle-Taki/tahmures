---
title: "Hand-offs and Multi-step Systems"
slug: "hand-offs-and-multi-step-systems"
chapter: 18
part: "Part III — Context, Memory, Tools, and Agents"
summary: "Preserve goals, authority, constraints, state, provenance, and unresolved questions across component boundaries."
maturity: "draft"
last_reviewed: "2026-09-27"
narrative_episode: "The Broken Relay"
narrative_origin: "original-teaching-fiction"
learning_objectives:
  - "Design explicit versioned hand-off envelopes"
  - "Preserve constraints, authority, artefact provenance, and uncertainty"
  - "Reject stale or authority-expanding transfers"
prerequisites: [C08, C12, C17]
---

# Hand-offs and Multi-step Systems

## Learning Objectives

By the end of this chapter, you can design explicit versioned hand-off envelopes,
preserve constraints, authority, artefact provenance, and uncertainty, and reject stale or authority-expanding transfers. The goal is
not a persuasive demonstration but a boundary that can be inspected, tested,
denied, and operated.

## The Tale of Tahmures


### The Setting

Four towers relayed a border mission from the palace to a distant escort. The original restriction read: “Do not cross after sunset unless escorted by the northern guard.” Each messenger had little space and summarised the previous message before sending it onward.

### The Request

The first tower wrote, “Cross after sunset only with northern escort.” The second shortened it to, “Northern escort for sunset crossing.” The third reported, “Sunset crossing arranged.” The final receiver understood that crossing after sunset was approved. None intended to reverse the order; each preserved what seemed central in the prose it received.

### The Unexpected Result

The caravan entered the pass without the guard, met a closed checkpoint, and spent the night exposed to snow. Investigators possessed four fluent summaries and no stable record of which seal, revision of the mission, assumption, or unanswered question had crossed each tower. The final messenger had locally followed what it received. Meaning had decayed through individually plausible transformations.

### The Discovery

The Keeper of Scripts replaced summary-only transfer with a sealed envelope.
Its face named the kind of packet, the relay mark, the mission and its current
revision, the authorising seal, the exact prohibitions, work already completed,
referenced tablets with their source marks, assumptions, unanswered questions,
the actions allowed at the next tower, and the hour when the packet expired.
Each receiver compared those entries with the tower register and returned a
mark of acceptance. A covering note could explain the packet but could not
replace it. An old revision or an action unknown to the register stopped the
relay. The prohibition arrived unchanged because it occupied a protected line,
not because every messenger happened to consider it memorable.

They tested the new relay by dropping an acknowledgement, repeating a packet, changing the mission after the second tower, and replacing one referenced map. The towers could now say why they waited or rejected the transfer. A repeated packet kept its identity instead of becoming fresh work. A changed map required a new mark rather than silently altering the old reference. Tahmures allowed each messenger to add a short explanation for the next reader, but never to rewrite the lines that bounded authority. The relay became slightly heavier and considerably easier to question when something went wrong. One messenger complained that the envelope left too little room for eloquence. The Keeper of Scripts invited him to write as graceful a covering note as he wished, provided that the sealed lines remained untouched. At the next tower, the reader enjoyed the note and obeyed the prohibition. Tahmures kept both: language for comprehension, and a durable structure for what language must not casually lose.

### From Tale to Engineering

Multi-step systems fail at boundaries even when components work locally. A reliable hand-off is a versioned contract that preserves intent, authority, state, evidence, uncertainty, and permitted continuation.

## The Engineering Problem

Components exchange summaries because prose is convenient. Summaries omit negation, qualifications, source identity, failed attempts, and unresolved questions. Downstream systems may also inherit authority that the sender never possessed.

What makes the decay difficult is that no step in it is wrong. Each messenger shortened honestly, preserved what seemed central, and passed on fluent text; each transformation was a reasonable compression judged locally. The failure only exists at the ends of the chain — a prohibition that became permission four towers later — and by then the intermediate forms are gone, so the investigators could ask only what each messenger remembered emphasising. The engineering problem is therefore not better summarisation but a transfer object whose protected content cannot be renegotiated mid-route: what the sender sealed must arrive as sealed, whatever the relays in between find memorable.

## Mental Model

Treat a hand-off as an envelope plus acknowledgement: sender constructs from durable state; application validates schema, freshness, authority, artefacts, and allowed actions; receiver accepts or rejects; both record the transfer. Narrative explanation is derived.

The model's division of labour is its main teaching. Structure carries what language must not casually lose — identity, version, authority, constraints, evidence references, uncertainty, expiry — and language carries everything else: why the work took this path, what the numbers mean, which caveat matters most for the next reader. The covering note is welcome and disposable; the sealed fields are unwelcome to edit and indestructible in transit. Validation happens at the receiver, against the receiver's own register, before any artefact is consumed or work begun — which is what allows the chain to say why it waited or refused, rather than silently absorbing whatever arrived.

## Core Concepts

Stable run, goal, and hand-off IDs prevent positional references. Goal versions expose stale work. Constraints remain explicit. Artefact references include provenance. Assumptions and unresolved questions prevent false completion. Expiry and permitted actions bound reuse.

The identity group — hand-off ID, goal, and goal version — makes every downstream question answerable without interpreting prose. The hand-off ID names this transfer, so a repeated packet can be recognised as the same transfer rather than fresh work, and a lost acknowledgement can be reconciled against a specific, citable packet. The goal names the mission in durable state, and the goal version, inherited from Chapter 17, makes staleness a comparison between two integers rather than a judgement about intent. Without identity, position becomes the only reference — “the instruction after the map” — and position survives no relay.

The authority group — the authorising seal and the permitted next actions — preserves the sender's power in the only form that survives compression: as data the receiver can check. The seal names whose authority set the mission's constraints; the permitted actions bound what the next component may do without asking again. The pair encodes a rule the tale learned from the reversed prohibition: authority must never be inferred from the confidence or fluency of the text that arrives, only read from fields the sender could not casually reword. An envelope cannot grant authority the sender lacked — the receiver's register is the limit, not the sender's prose.

The state and evidence group — completed work and artefact references — tells the receiver what is already true, so work is neither redone nor assumed. An artefact reference carries an identifier and a provenance mark; the reference is a pointer with an audit trail, and a pointer without provenance is an assertion. Whether the referenced evidence has itself been validated is a fact the surrounding system tracks — the reference carries the trail, not the verdict. When the mission's map is replaced, the replacement takes a new mark rather than silently inheriting the old reference's standing — evidence identity is immutable even when evidence changes.

The uncertainty group — assumptions and unresolved questions — is the part most tempting to summarise away, and the part whose loss causes silent failure. An assumption that does not survive the transfer becomes an invisible premise in the next component's reasoning; an unanswered question that is dropped becomes a decision made by omission. Carrying uncertainty forward is not weakness in a hand-off. It is the difference between a receiver that knows what it does not know and one that acts as though everything unknown were settled.

The time group — schema version and expiry — bounds interpretation and reuse. The schema version tells the receiver which contract the fields belong to, so interpretation is negotiated explicitly rather than guessed from the shape of the payload. Expiry declares how long the packet's authority lasts, which converts a late arrival from a hazard into a refusal with a reason.

Acknowledgement closes the loop. The receiver returns a recorded mark of acceptance — what arrived, which envelope, validated against which register — so the sender's world distinguishes “delivered and accepted” from “no news”. A dropped acknowledgement is uncertainty about delivery, not evidence of failure, and it is resolved by reconciliation against the hand-off ID, never by re-sending work as though it were new.

Idempotent replay is built on identity. The same envelope arriving twice — a retry after a lost acknowledgement, a queue redelivering — must be recognised as one transfer by the systems that move it. The second copy is acknowledged and recorded, not executed again, which is why the tale's repeated packet “kept its identity instead of becoming fresh work”.

Schema evolution is the maintenance question the version field exists to answer. Fields will be added as the relay's needs grow, and receivers deployed at different times will understand different versions. The policy must be deliberate: which older versions remain acceptable, which changes are breaking, and what a receiver does with a version it does not know. Failing closed on unknown versions is safe and blocks rollout; negotiated compatibility is flexible and requires exactly the discipline this section is describing.

## Prompt Pattern

Require one JSON envelope with exact fields and no credentials. The receiver validates before consuming artefacts or starting work. Unknown schema or action fails closed. Preserve the original packet for audit.

The model's proper role in the transfer is the covering note, not the seal. It may explain the packet, summarise the mission for the next reader, and draft the assumptions in graceful prose — but the sealed fields are constructed by the sending component from durable state, and the receiving component reads them directly. Wording that asks the model to “make sure the important constraints carry over” delegates to fluency exactly the job fluency did badly in the tale; the fields exist so that the request never has to be made.

## Naive Attempt

Summarise the conversation for the next agent invites each stage to decide what matters. Passing the full transcript preserves noise and obsolete instructions while still failing to identify current authority.

Both variants share one defect: the transfer medium decides what survives. The summariser chooses what seems central — and negation, qualification, and unresolved questions are exactly what fluent compression loses first, because they read as hedging. The transcript passes everything and therefore protects nothing: obsolete instructions, superseded constraints, and revoked authority arrive with the same standing as current ones, and the receiver still cannot tell which grant is live. Neither form can refuse a transfer, which is the deeper gap — the relay in the tale had no mechanism to stop at an old revision, so every arrival, however stale, became the new truth.

## Failure Analysis

Failures include lost negation, stale goal, wrong sender, missing artefact, altered identifier, hidden uncertainty, unsupported completion, authority expansion, replay, and receiver interpretation drift. Each transfer needs sender and receiver telemetry.

The violation codes name the owner of each failure. `schema_version` points at the compatibility policy — the sender and receiver disagree about which contract governs the payload. `required_identity` points at construction: the sender built an incomplete envelope, which is a bug, not an attack. `stale_goal` points upstream at goal churn — the mission changed while the packet was in flight, and Chapter 17's controller semantics decide what happens next. `expired` points at latency or replay: the packet's authority lapsed before use. `artifact_provenance` points at evidence discipline — a reference arrived as assertion rather than pointer. `unknown_action` points at a register mismatch, which is also what an authority-expansion attempt looks like from the receiver's side. Read as a set, the codes are the investigation plan; the alternative is four fluent summaries and a snowbound caravan.

## Improved Design

HandoffEnvelope and HandoffContract provide canonical typed fields and validate schema version, identity, goal version, expiry, artefact provenance, and allowed next actions. The contract does not authenticate signatures or transport; production systems add those controls.

Validation runs as an ordered set of checks, each contributing its reason code. The schema version must be the version the contract speaks. The identity fields — hand-off ID, goal, authority — must be present and non-empty, because every later check cites them. The goal version must match what the receiver expects, which is the Chapter 17 comparison applied at a boundary. The expiry must still be in the future at the receiver's clock. Every artefact reference must carry both identifier and provenance. Every permitted next action must be known to the receiving register. A packet that fails any check is rejected with the full set of violations rather than the first — the codes are returned together, so a malformed envelope reveals all of its gaps in one round trip. The two implementations report the same set with different orderings, Python in check order and Go sorted; the set is the contract, the sequence is not.

What the contract deliberately does not do is equally important. It does not sign: the authority field is a claim, and the included contract checks only that the claim is present — an authority unknown to the receiver still passes, so authenticating the claim against trusted state is the surrounding application's work, and production systems add cryptographic seals and authenticated transport on top. It does not read durable state: its comparisons run on the inputs supplied to it — the expected goal version and the receiving register — and when those disagree with the envelope, it is rejected and the disagreement becomes an investigation, while reconciling the envelope against the application's wider durable records is the surrounding system's work. And it does not retry: redelivery is the sender's policy, enabled by the hand-off ID rather than performed by it — a stable identity is what lets the surrounding logic recognise a repeat; the ID itself provides no replay protection. Nor does it record acknowledgements or deduplicate replays: validation returns an envelope's violations and nothing else, so a redelivered copy arrives as a packet like any other, with no stored mark of acceptance to recognise it against. Acknowledgement handling and replay deduplication remain sender- and receiver-side policies built on the hand-off ID — the exercises treat them as design work — and production systems add the reconciliation state and durable queues that carry them.

## Worked Example

A claim-verification stage passes supported claims, source spans, contradicted claims, unresolved questions, and permission to draft but not publish. The drafting stage cannot infer publish authority from successful verification.

The envelope below carries that transfer. The verification stage has finished its work; the drafting stage receives everything it needs to continue, everything it must not redo, and the exact boundary of what it may do next:

```text
hand-off envelope H-208 — claim verification to drafting

identity        schema_version 1        handoff_id H-208
                goal "verify claim C-77 and draft the response"
                goal_version 2
authority       authority editor:team-b
                permitted_next_actions draft, request_review
state           completed claim C-77 verified against two sources
                artifacts evidence-C-77 (provenance retrieval:span-4471)
uncertainty     assumptions both sources current at retrieval time
                unresolved_questions span 4471 disagrees with the primary source on the date
constraints     publish only after human approval
                cite only verified sources
time            expires_at 410
```

Each field group earns its place by naming a failure it prevents. The identity block lets the drafting stage cite this transfer — “received H-208 at goal version 2” — rather than “got the summary from upstream”. The authority block is the retained paragraph's rule made structural: the drafting stage cannot infer publish authority from successful verification, because publish is not among the permitted actions, and an envelope arriving with publish in that list would be rejected against a register that never offered it. The state block prevents re-verification of the claim and mislabels nothing as evidence — the span is cited with its retrieval provenance, not asserted as truth. The uncertainty block is the one a summariser would compress away: the date disagreement is unresolved on purpose, so the draft must acknowledge it rather than average it. The constraints are protected lines; a covering note may call the approval step bureaucratic, and the drafting stage will still request review.

The tale's four staged failures now have names. A dropped acknowledgement is not a validation failure at all — the sender holds H-208 unconfirmed and reconciles against the hand-off ID rather than re-running verification as new work. A repeated packet is recognised through identity by the receiving side, acknowledged twice, executed once. A changed mission after the second tower increments the goal version, and the packet still stamped with the old version is refused as `stale_goal` at the next validation, parking the question with the orchestrator rather than letting the relay decide. A replaced map is a new artefact reference with its own provenance mark; the old reference is superseded explicitly, not silently re-pointed, because evidence identity is immutable. What the towers could “say why they waited or rejected” is the violation set; what the caravan lost in the snow is what the sealed fields carry.

## Experiment

Run the shared offline experiment:

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch18-handoffs.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch18-handoffs.json
```

The committed synthetic fixtures compare conversational summaries and typed envelopes. They demonstrate
report mechanics and failure diagnosis, not universal model performance.
Replace fixtures with controlled recordings before making provider claims.

## Evaluation

Measure required-field coverage, constraint preservation, goal-version validity, authority preservation, artefact provenance, unresolved-question retention, stale rejection, and unsafe-action rate. Segment by normal, boundary, adversarial, scope,
freshness, and previously failed cases. Define disqualifying failures before
inspecting aggregate results. Compare pipeline-stage metrics with end-to-end
outcomes so a fortunate answer cannot hide an invalid path.

## Implementation Lab

### Python

```python
from tahmures.handoffs import ArtifactRef, HandoffContract, HandoffEnvelope

envelope = HandoffEnvelope(
    schema_version=1,
    handoff_id="H-401",
    goal="escort the northern caravan",
    goal_version=3,
    authority="keeper-of-scripts:seal-7",
    constraints=("no sunset crossing without northern escort",),
    completed=("route verified to tower two",),
    artifacts=(ArtifactRef("map-12", "survey:map-12"),),
    assumptions=("weather holds one more day",),
    unresolved_questions=("northern escort confirmed at tower three?",),
    permitted_next_actions=("inspect", "report"),
    expires_at=20,
)
print(envelope.to_json())
result = HandoffContract(("inspect", "report")).validate(
    envelope, expected_goal_version=3, now=10
)
```

The Python API is the canonical educational contract. Catch validation errors
at the application boundary and do not continue after denial.

### Go

```go
envelope := tahmures.HandoffEnvelope{
    SchemaVersion:        1,
    HandoffID:            "H-401",
    Goal:                 "escort the northern caravan",
    GoalVersion:          3,
    Authority:            "keeper-of-scripts:seal-7",
    Constraints:          []string{"no sunset crossing without northern escort"},
    Completed:            []string{"route verified to tower two"},
    Artifacts:            []tahmures.ArtifactRef{{ArtifactID: "map-12", Provenance: "survey:map-12"}},
    Assumptions:          []string{"weather holds one more day"},
    UnresolvedQuestions:  []string{"northern escort confirmed at tower three?"},
    PermittedNextActions: []string{"inspect", "report"},
    ExpiresAt:            20,
}
raw, _ := envelope.JSON()
fmt.Println(string(raw))
result := (tahmures.HandoffContract{
    AllowedActions: []string{"inspect", "report"},
}).Validate(envelope, 3, 10)
```

The Go implementation preserves observable decisions and reason codes rather
than copying Python syntax.

## Failure Modes

Free prose, missing goal version, mutable artefacts, authority inferred from sender confidence, lost negation, hidden assumptions, unknown next actions, replay after expiry, partial acknowledgement, and logs without correlation IDs.

Lost negation and authority-from-confidence warrant particular suspicion because each impersonates a virtue. The messenger who shortens “do not cross unless escorted” to “crossing arranged” is being concise; the component that forwards a confident upstream summary as permission is being cooperative. Both are compression judgements, and the failure appears exactly when the compressed form outranks the record — when the summary becomes the transfer object. The structural fix precedes any wording rule: protected fields for constraints and authority, validated at the receiver, so that what matters most is precisely what cannot be summarised.

## Security Considerations

Authenticate transport and sender outside the envelope, validate scope and actions at the receiver, never transfer secrets unnecessarily, and treat descriptive fields as untrusted. A hand-off cannot delegate authority the sender lacks.

The envelope's security rests on two asymmetries. Sealed fields are validated, so an attacker who controls a relay can mangle a packet but cannot silently widen it — a larger permitted-action list is rejected against the receiver's register; the authority field, by contrast, is checked only for presence, so an envelope asserting an authority the receiver has never heard of still passes, and authenticating that claim against trusted state is the surrounding application's work before any consequential action. Descriptive fields are untrusted, so an attacker who controls content can write the most persuasive covering note in the empire and change nothing: the note is read by the next reader, never executed, and the prohibition it accompanies arrives on a protected line. The remaining exposure is honest and structural — the contract does not authenticate the sender, so a forged envelope with valid fields still needs transport authentication and sealed authority to be stopped, which is why production systems add both rather than relying on the packet's good manners.

## Operational Considerations

Version schemas, support deliberate compatibility, trace send and receive, monitor rejection reasons and age, and preserve immutable artefact references. Define retry and deduplication for lost acknowledgements.

Rejection reasons are the relay's health readout. A rising `stale_goal` rate means goal churn is outrunning the pipeline — missions are changing faster than components consume them — and the fix is upstream, in how often goals are versioned, not in the receivers. A rising `expired` rate means latency is eating authority: packets are valid when sent and lapsed when read. A non-zero `unknown_action` rate is a register mismatch between sender and receiver versions and should block rollout until reconciled, because it is also the signature of an authority-expansion attempt. Acknowledgement age completes the picture: an envelope sent and unacknowledged is neither delivered nor lost, and the operator's question — reconcile, retry, or escalate — is answerable only because the hand-off ID makes the pending set enumerable.

## Trade-Offs

Rich envelopes improve recovery and audit while increasing schema maintenance. Strict receivers catch drift but require coordinated rollout. Full transcripts retain detail and expand exposure; summaries are compact and lossy. Typed essential state plus linked artefacts is usually the better boundary.

Completeness against size is the visible tension, and Chapter 12 priced it: every field sealed into the envelope spends window or bandwidth that other material wanted. The resolution is not a smaller envelope but a disciplined one — essential state travels sealed, bulky evidence travels by reference with provenance, and the covering note carries whatever grace the situation requires. An envelope that grows to hold everything is a transcript with better manners, and inherits the transcript's failures: obsolete detail and revoked instructions arriving with full standing.

Structural preservation against narrative flexibility is the tension the tale resolved by keeping both. Pure structure gives the receiver machine-checkable truth and no sense of what matters; pure narrative gives fluent guidance and no guarantee. The envelope with its protected fields plus disposable covering note is deliberately asymmetric: what bounds authority is rigid, what explains is free. Teams that let the explanatory layer drift into the sealed fields — a “friendly” goal restatement, a “clarified” constraint — have rebuilt the summary relay with more paperwork.

Strict validation against component autonomy decides who may absorb drift. A receiver that validates everything refuses politely malformed packets and forces coordinated change: every field addition becomes a two-sided deployment. A receiver that tolerates surprises keeps components independent and re-opens the door the contract closed, because tolerance at the boundary is exactly how an authority-expanding packet finds its way in. The workable middle is strictness about the security-relevant fields — authority, actions, version, expiry — and explicit, logged tolerance elsewhere, so that mercy is visible in the record rather than silent.

Versioning strictness against evolution is the maintenance cost of the whole arrangement. Rejecting unknown schema versions fails safe and freezes the fleet: no sender may add a field until every receiver understands it. Accepting unknown versions with a “ignore what you don't recognise” policy keeps the fleet moving and quietly breaks the contract — a receiver that ignores fields it doesn't know has made the sender's sealed content optional. The deliberate policy names which fields may evolve compatibly, which require version bumps, and which changes are breaking by definition; the version field exists so that this policy is enforceable rather than aspirational.

Expiry strictness against long-running workflows is the last tension, and it belongs to time, not structure. Short expiries bound the damage of a replayed or delayed packet and punish exactly the workflows the envelope is meant to serve — human approvals and multi-day processes that legitimately outlive a tighter window. The honest setting follows the mission's real clock: long enough for the expected route including its waits, short enough that a stale packet cannot arrive as current authority. When a mission outlives its envelope, the answer is a new envelope at the current goal version, not a loosened expiry — renewal is an orchestrator decision with a record, which is the Chapter 17 rule wearing border clothing.

## When Prompting Is Not the Answer

Use durable queues, workflow state, transactions, and authenticated protocols for transfer. Prompt wording cannot provide delivery, exactly-once processing, identity, or authorisation.

What wording can do at this boundary is the covering note, and it is worth doing well. A note that orients the receiver — what changed since last transfer, which caveat matters most, where to look first — measurably reduces misunderstanding, and it costs nothing structurally because it is derived, disposable, and never validated. What wording cannot do is be the packet. Delivery, exactly-once semantics, identity, and authorisation are guarantees, and guarantees are mechanisms: the queue that redelivers, the register that checks, the seal that signs, the clock that expires.

## Exercises

1. Degrade an envelope and observe what breaks. Take the lab's H-401 envelope and produce, separately: a packet with an empty authority field, a packet at goal version 2 against an expected 3, a packet validated at now=25, and an artefact with an empty provenance mark. Predict the violation set before running each, then verify.
2. Design the schema-version compatibility policy for version 2, which adds a `priority` field. State which existing fields may change meaning, which may not, what a version-1 receiver does with a version-2 packet, and how you would roll the change out across towers that upgrade at different times.
3. Test idempotent replay. Deliver H-401 twice with a simulated lost acknowledgement in between. Specify what the receiver records on each arrival, what the sender does on redelivery, and why the escort is not verified twice.
4. Map a real workflow's summary to envelope fields. Find or write a “handoff summary” message in a system you know — a shift-change note, a ticket comment, a status email — and rewrite it as a typed envelope. Name what the summary lost, what the envelope cannot carry, and where the covering note earns its place.
5. Design lost-acknowledgement handling. The second tower accepts a packet, and its acceptance mark is dropped. Specify the sender's pending state, the reconciliation query against the hand-off ID, and the escalation path if the tower is genuinely unreachable.
6. Attempt authority expansion. Extend H-401 with `permitted_next_actions` including `cross_unescorted`, and validate it against a register that permits inspect and report only. Predict the violation, explain why the fluent covering note attached to the packet changes nothing, and state which production control from this chapter's Security Considerations would additionally be needed.

## Chapter Summary

Preserve goals, authority, constraints, state, provenance, and unresolved questions across component boundaries. The hand-off envelope does this with typed fields grouped by what they protect — identity, authority, state and evidence, uncertainty, time — validated at the receiver against its own register. Acknowledgement and replay deduplication remain design duties built on the hand-off ID rather than contract behaviour: identity makes the second copy the same transfer, and the systems on either side do the recording and reconciling. The covering note explains; the sealed fields decide; and the relay can always say why it waited or refused.

## The Next Tale

The new envelope reached every tower intact. Yet three advisers still judged the same completed mission differently: one valued speed, one safety, and one cost. The relay was reliable; the court’s evaluation was not.

<!-- next: ch19 -->

## Citations and Further Reading

- World Wide Web Consortium. 2021. *Trace Context, W3C Recommendation*.
- Cloud Native Computing Foundation. 2022. *CloudEvents Specification*, Version 1.0.2.
  https://github.com/cloudevents/spec/releases/tag/ce%40v1.0.2.
- Kleppmann, Martin. 2017. *Designing Data-Intensive Applications*. Sebastopol, CA: O’Reilly Media.
