---
title: "Memory and State"
slug: "memory-and-state"
chapter: 15
part: "Part III — Context, Memory, Tools, and Agents"
summary: "Govern what a system remembers, scopes, corrects, expires, and forgets."
maturity: "draft"
last_reviewed: "2026-09-27"
narrative_episode: "Spring Remembered in Winter"
narrative_origin: "original-teaching-fiction"
learning_objectives:
  - "Separate conversation history, working state, durable memory, and authoritative records"
  - "Design explicit memory write, recall, expiry, correction, and deletion policies"
  - "Test stale and cross-scope memory failures"
prerequisites: [C05, C13]
---

# Memory and State

## Learning Objectives

By the end of this chapter, you can separate conversation history, working state, durable memory, and authoritative records,
design explicit memory write, recall, expiry, correction, and deletion policies, and test stale and cross-scope memory failures. The goal is
not a persuasive demonstration but a boundary that can be inspected, tested,
denied, and operated.

## The Tale of Tahmures


### The Setting

The steward of journeys kept a small ivory ledger of the king’s preferences. In spring it recorded: “Tahmures favours the eastern road while the river is high.” Months later snow closed the eastern pass, but the sentence remained neat, current-looking, and detached from the flood report that had justified it.

### The Request

Before a winter inspection, a servant asked the ledger which route Tahmures preferred. It returned the eastern road. The servant treated memory as instruction, arranged horses there, and omitted the current closure because another office kept the condition of roads. Tahmures had not repeated the preference and did not know it had become durable.

### The Unexpected Result

The party reached a blocked pass after dark. No div had lied. The remembered sentence was authentic, and the servant copied it exactly. The failure belonged to the rules of the ledger: a choice made for one season had been preserved as a preference for every journey. When Tahmures corrected the route, the ledger appended “western” without crossing out “eastern,” so later readers received both.

### The Discovery

The court separated conversation scrolls, the slate for the present journey,
the ivory book of lasting preferences, and the tablets maintained by the
keepers of roads. Any sentence proposed for the ivory book had to name the
person concerned, the journeys to which it applied, whether it was preference
or fact, who supplied it, when it was written, when it should fade, and why the
court was permitted to keep it. A correction covered the older line without
erasing its history. A black forget-me seal prevented both the corrected line
and the line beneath it from returning later. The road to take still came from
the keeper of roads, not from the king’s remembered taste.

Tahmures ordered the ivory ledger tested with borrowed rooms, shared horses, seasonal meals, and a traveller who withdrew consent to keep her preference. The steward discovered that remembering could cause harm even when recall was exact. Some notes belonged only to one journey; some belonged to one person but not the whole court; some should never have been written. The First Scribe added a reason beside every durable entry and a date when it must be reconsidered. Empty space in the ledger ceased to look like failure. It could mean that the court had forgotten deliberately and correctly. The steward objected that a smaller ledger might appear less impressive to visitors. Tahmures answered by asking him to recover a corrected preference, then an erased one, and finally a road closure. The first returned with its history, the second did not return, and the third came from the keeper of roads rather than the ivory pages. Those differences mattered more than the number of entries.

### From Tale to Engineering

Memory is application state with a lifecycle, not extra prompt text. Reliability depends on explicit write authority, scope, provenance, freshness, correction, deletion, and the distinction between preference and fact.

## The Engineering Problem

Language applications often call the conversation transcript memory. Retaining every turn mixes obsolete goals, inferred preferences, sensitive data, and model errors. Summarising the transcript changes representation but does not define authority or retention.

The transcript fails as memory because it has no write policy. Everything that enters becomes durable by default, nothing names the journeys to which it applies, and no office decides when a sentence should fade. The winter pass was not a recall failure—the servant copied the sentence exactly—it was a lifecycle failure: a seasonal choice with no expiry, preserved as a standing preference, consulted in a season it never spoke for. Summarisation cannot repair this, because a summary of an ungoverned record inherits its missing policy. The engineering problem is to make remembering a decision—with an owner, a scope, a justification, and an end date—rather than an accident of retention.

## Mental Model

Use four layers: source-of-truth records, governed durable memory, current workflow state, and selected conversational context. Each has different writers, readers, expiry, correction, and deletion. Recall produces candidates for context; it does not make them instructions.

The layers are distinguished by who may write them and how they end. Source-of-truth records—account data, road conditions, official policy—are written by their owning systems and expire when reality or policy changes, not when a conversation does. Durable memory is written under an explicit consent and retention policy and ends by expiry, correction, or deletion. Workflow state belongs to a run and ends when the run ends. Conversational context is the working set Chapter 13 assembles and ends with the request. The tale's closing test is the model's diagnostic: a corrected preference returns with its history, an erased one does not return at all, and a road closure comes from the keeper of roads. Which layer answered the question is itself a finding—an answer arriving from the wrong layer is the winter pass, recurring.

## Core Concepts

A memory record needs identity, subject, scope, kind, value, provenance, creation, expiry, and optional supersession. Write policy decides what may persist and for how long. Recall is filtered by current caller and time. Forgetting must account for copies, summaries, indexes, and backups.

Each field of that record exists because its absence has a named failure. Identity makes a record addressable—correction, deletion, and regression tests all refer to it, and a forgotten identifier must not silently return. Subject names who the record is about; a recall that ignores subject returns one person's preference for another, which is a privacy failure even when the text is accurate. Scope names the tenant or audience; kind separates preference from fact and lets policy allow some kinds and refuse others. Value is the payload; provenance records who supplied it and when, which is the evidence of consent and the audit trail of correction. Creation and expiry bound the record's life—expiry is a declared property, not a guess from last mention—and supersession links a correction to what it corrects.

Write policy is the gate, and every check in it corresponds to a failure the gate refuses. The kind must be allowed by policy, so an inferred health claim cannot enter a store that only admits preferences. The record must be current at write time, so nothing is born already expired. Retention must fit the policy's maximum, so a ninety-day consent cannot create a permanent record. The identifier must be new, so deletion cannot be undone by rewriting the same identifier. A superseding record must point at one that exists, so correction chains stay walkable. Each rejection is a decision with a reason, not an exception to be caught and ignored.

Recall is a filtered, scoped read, not a dump. The caller's subject and scope must match the record's; the recall time must fall inside the record's validity window; the requested kinds narrow further when the task needs one kind. Records superseded by a correction are hidden but not destroyed—their history remains behind the correction, exactly as the correction covered the older line without erasing it. Order is deterministic, so the same store and query produce the same results, and a difference between two recalls is a real event rather than noise.

Recall also has a destination: the working set of Chapter 13. Recalled records arrive there as one candidate source among several—beside retrieval results, policy, and task instructions—carrying their provenance, age, and declared priority, and competing for budget like any other data. A memory system that injects recalled text directly into the prompt bypasses that competition, and with it the accounting that lets an operator discover, after a wrong decision, that a remembered preference outranked a current record.

Forgetting is a lifecycle transition with a tombstone, not a deletion flag that can be flipped back. A forgotten record does not return, the identifier cannot be rewritten, and records it superseded stay hidden. But the store is only one copy. Deletion that empties the primary record while leaving summaries, indexes, caches, and backups intact has not forgotten; it has scattered the memory into harder-to-audit places, from which it can resurrect—a restore without tombstones is the resurrection path.

## Prompt Pattern

Ask the model to propose a memory candidate with evidence and scope, never to store it directly. Application policy validates consent, kind, retention, and conflicts. On recall, label memories as data and include age and provenance.

The division of labour is strict. The model is good at noticing that a durable preference was expressed and terrible at deciding whether it should persist—who consented, for how long, and under what scope. So the prompt elicits candidates with their evidence, and the write gate from the previous section decides. On recall, the same asymmetry applies: the model interprets labelled, aged, attributed records well, and treats unlabelled remembered prose as instruction badly. The label is not decoration; it is the boundary that keeps a remembered sentence from arriving as an order, which is Chapter 5's rule arriving at the storage layer.

## Naive Attempt

Append every user statement and feed the growing transcript back. This silently turns jokes, corrections, third-party claims, and secrets into durable state. A later summary can preserve the wrong fact while discarding the correction.

The naive design also cannot correct. When the route changed, the ledger appended "western" without crossing out "eastern," and later readers received both—append-only storage presents a correction as an addition, and the reader must guess which value is current. The winter failure was therefore doubly determined: no expiry ended the spring preference, and no supersession distinguished the corrected route from the original. Nothing about the recall was wrong; the policy under it was absent.

## Failure Analysis

Memory failures include unjustified writes, wrong subject or tenant, stale values, missing expiry, failed supersession, deletion gaps, and authority confusion. Model recall errors and application store errors require separate telemetry.

The tale's closing test is the diagnostic pattern. Ask the system to recover a corrected preference: it should return with its history, and if the history is missing, supersession failed. Ask it to recover an erased one: it should return nothing, and if it returns, deletion failed or resurrected. Ask it for a road closure: it should answer from the keeper of roads, and if the ivory pages answer instead, the layers have blurred and memory is overriding an authoritative record. Three questions, three layers, three distinct failure owners—store policy, deletion propagation, and layer separation. Averaged recall-accuracy metrics blend all three into one number that none of them can be fixed with.

## Improved Design

InMemoryStore demonstrates explicit validated writes, maximum retention, scoped recall, expiry, supersession, and tombstoned forgetting. It does not infer candidates or persist externally. A production store needs authentication, encryption, audit, deletion propagation, and transactional updates.

The store's operations are the chapter's contracts. remember runs the write gate: required fields and provenance, an allowed kind, current at write time, retention within the maximum, a new identifier, and a supersession pointer that must resolve. recall filters forgotten and superseded records, matches subject, scope, and kind, and checks the recall time against the record's validity window, returning results in a deterministic order. forget places a tombstone: the record stops returning, its identifier cannot be rewritten, and anything it superseded remains hidden. The store is deliberately in-memory and small; what it demonstrates is not durability but the decision surface—every operation either succeeds under policy or fails with a reason a test can assert.

## Worked Example

A user preference for concise summaries may be durable with consent and expiry. A shipping address is authoritative account data, not conversational memory. A one-session draft style belongs to run state. Classification prevents one convenient store from acquiring every responsibility.

The classification deserves one example of each kind, because the boundary is where the failures live. A preference—"prefers concise summaries"—is durable memory: it has a subject who consented, a scope of one user's sessions, an expiry that forces reconsideration, and a correction path through supersession. An inferred fact—"lives near the eastern depot"—may have been stated once or guessed from an address; it may persist only with provenance naming its source and an expiry short enough to limit the damage of a wrong guess, and it must never outrank the account record it contradicts. An authoritative record—the shipping address itself—belongs to the account system; memory may cite it for convenience but must not copy it into permanence, because the copy would keep speaking after the record changes. When memory does cache such a value, the cache inherits the record's lifecycle, or it becomes the ivory ledger: neat, current-looking, and wrong.

Deletion is where the design meets its copies. A forget operation on one record must reach every derived artefact, or it has only narrowed the resurrection paths:

```text
deletion propagation — forgetting record M-12
  primary store       tombstone M-12; recall must not return it; ID cannot be rewritten
  correction chain    records superseding M-12 remain active; M-12 stays hidden
  derived summaries   regenerate or retract; a summary quoting M-12 is a resurrection
  indexes             remove M-12 from subject and kind indexes
  caches              invalidate recall results that contain M-12
  backups             define restore policy; tombstones must survive a restore
  logs                keep the audit event, drop the payload
```

The two lines most often skipped are the last two. A backup restored without its tombstones resurrects everything it ever held, silently and with full authority. And a log that keeps the payload "for debugging" is a copy with weaker access control than the store it duplicates—the audit event, not the remembered text, is what the log needs.

## Experiment

Run the shared offline experiment:

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch15-memory.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch15-memory.json
```

The committed synthetic fixtures compare append-only recollection and governed memory. They demonstrate
report mechanics and failure diagnosis, not universal model performance.
Replace fixtures with controlled recordings before making provider claims.

## Evaluation

Measure active-memory precision and recall, stale-memory use, supersession success, cross-scope leakage, deletion compliance, and provenance coverage. Segment by normal, boundary, adversarial, scope,
freshness, and previously failed cases. Define disqualifying failures before
inspecting aggregate results. Compare pipeline-stage metrics with end-to-end
outcomes so a fortunate answer cannot hide an invalid path.

## Implementation Lab

### Python

```python
from tahmures.memory import InMemoryStore, MemoryPolicy, MemoryQuery

store = InMemoryStore()
policy = MemoryPolicy(("preference",), max_ttl=30)
active = store.recall(MemoryQuery("subject-1", "tenant-a", as_of=10))
```

The Python API is the canonical educational contract. Catch validation errors
at the application boundary and do not continue after denial.

### Go

```go
store := tahmures.NewInMemoryStore()
active := store.Recall(tahmures.MemoryQuery{SubjectID: "subject-1", Scope: "tenant-a", AsOf: 10})
```

The Go implementation preserves observable decisions and reason codes rather
than copying Python syntax.

## Failure Modes

Automatic promotion, inferred consent, cross-user or cross-tenant recall, missing provenance, unbounded retention, stale facts, correction appended without supersession, deletion that resurrects older records, and summaries that cannot be traced.

Three of these are quiet because they look like features. Automatic promotion turns a passing remark into a standing preference the moment it is useful, and the harm appears seasons later when the preference is exact, authentic, and wrong for the season. Correction without supersession presents both values as current and delegates the choice to whatever reads them next. Deletion that resurrects is the quietest: the primary store is clean, the report says compliant, and the backup is waiting.

## Security Considerations

Minimise stored content, separate sensitive categories, encrypt and authorise access, prevent tenant leakage, and make deletion auditable. Never place secrets in memory merely to simplify later prompts.

Memory records are data, never instructions—the recalled sentence that reads "arrange the eastern road" is a spring preference, not a winter order, and the label it arrives with is the control. Write authority is the other boundary: who may write whose memory, with whose consent, is an access decision the store must enforce, not a question the model may answer. Recall is the third: subject and scope filtering happens before any text reaches a model, so a cross-tenant record cannot influence an answer even as a hidden candidate. And deletion is a security operation, not housekeeping—an incompletely forgotten record is retained data with weaker governance.

## Operational Considerations

Monitor writes, reads, expiry, corrections, deletions, denied scope, and age distributions. Version memory policy and migration. Test backup and index deletion, clock behaviour, and what happens when the memory service is unavailable.

Expiry and supersession are maintenance obligations, not set-and-forget declarations: something must sweep expired records from indexes, and something must verify that supersession chains still resolve after policy migrations. Tombstones need their own lifecycle—long enough to survive every backup restore, short enough to satisfy retention limits on the audit trail, and that boundary is a published policy, not an implementation detail. The backup drill that matters is the one this chapter forces: restore a backup and verify that what was forgotten is still forgotten. And the memory service being unavailable deserves a designed answer: proceed without memory rather than fail closed, but make the absence visible in the request record—an empty, reported recall—so that a degraded answer is never mistaken for a considered one.

## Trade-Offs

Long retention improves continuity but increases privacy, staleness, and breach impact. Short retention loses convenience. Structured records are easier to govern than prose but cannot represent every nuance. Human confirmation adds friction and informed control.

Durability against staleness is the first axis. The spring preference was useful in spring and dangerous in winter; a record with no expiry is correct exactly as long as the world holds still. Declared expiry converts that silent decay into a scheduled decision, at the price of forgetting things that were still true—so the expiry policy must follow the record class, not a global constant.

Retention against privacy and breach impact is the second. Everything remembered improves continuity and enlarges the surface: more subjects, more scopes, more sensitive text in one place. The ivory ledger looked impressive to visitors precisely when it was most dangerous. Retention limits per data class, consent recorded as provenance, and minimisation at write are the counterweights, and each is a policy decision with an owner.

Automatic write against consent is the third. Writing every expressed preference silently maximises convenience and assumes consent that was never given—the traveller who withdrew hers is the counterexample. A consent gate costs a moment of friction per durable write and buys the right to explain, for every record, why it is legitimate to keep. Where the product cannot afford the friction, the honest compromise is shorter retention, not inferred consent.

Forgetting against audit trail is the fourth. Deletion must be complete to be real, and audit must survive deletion to be meaningful. The resolution is separation: the record's payload goes; the event—what was forgotten, when, by whose authority—stays in a log with different access control. The log keeps the shape of the decision and none of the content it decided about.

Scope granularity against recall is the last. A record scoped to one journey is precise and useless next month; a record scoped to the whole court is useful next quarter and already leaking across the subjects it was never about. Narrow scopes fail toward missing context, broad scopes fail toward cross-scope exposure, and only the first failure is polite.

## When Prompting Is Not the Answer

Use authoritative databases for account facts, workflow stores for run state, and search for documents. Memory must not override current policy, access control, or a verified external record.

## Exercises

1. Design a lifecycle table for five data classes—stated preference, inferred fact, authoritative account record, run state, and conversational draft. For each, name the writer, the reader, the expiry rule, and the correction path.
2. Construct a cross-scope leak: store a record for one tenant and recall it from another. Write the check that prevents it and the test that would detect its return.
3. Reproduce the ledger's failure: append a corrected value without supersession and observe both values returned. Then correct it properly and verify the old value hides while its history remains walkable.
4. Plan deletion propagation for a record that appears in a summary, an index, a cache, and a backup. State what each artefact must do, what the tombstone guarantees, and what the audit log retains.
5. Apply the three-recovery test to a system you know: recover a corrected preference, an erased record, and an authoritative fact. For each, identify which layer answered and what a wrong source would indicate.
6. A user withdraws consent for a retained preference. Specify what must stop immediately, what must be forgotten, what must be retained as audit evidence, and the order of those operations.

## Chapter Summary

Govern what a system remembers, scopes, corrects, expires, and forgets. This chapter's memory is a governed record with identity, subject, scope, kind, provenance, and declared expiry, written through a policy gate, recalled through scoped and time-bound filters, corrected by supersession, and ended by a tombstone that must propagate to every copy. Which layer answers a question is itself a diagnostic, and an answer arriving from the wrong layer is the winter pass, recurring.

## The Next Tale

After correcting the route memory, Tahmures asked a div to inspect why the northern gate’s hinge had frozen. The servant carried a key that could inspect nothing without also opening the gate.

<!-- next: ch16 -->

## Citations and Further Reading

- Kleppmann, Martin. 2017. *Designing Data-Intensive Applications*. Sebastopol, CA: O’Reilly Media.
- National Institute of Standards and Technology. 2020. *NIST Privacy Framework: A Tool for Improving Privacy through Enterprise Risk Management*, Version 1.0.
  [https://doi.org/10.6028/NIST.CSWP.48](https://doi.org/10.6028/NIST.CSWP.48).
