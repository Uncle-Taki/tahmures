---
title: "Context Engineering"
slug: "context-engineering"
chapter: 13
part: "Part III — Context, Memory, Tools, and Agents"
summary: "Engineer a sufficient, scoped, traceable working set rather than accumulating every available record."
maturity: "draft"
last_reviewed: "2026-09-27"
narrative_episode: "The Archive That Answered Everything"
narrative_origin: "original-teaching-fiction"
learning_objectives:
  - "Design task-specific context packages across sources"
  - "Preserve authority, provenance, conflicts, and exclusions"
  - "Evaluate context construction independently from model output"
prerequisites: [C12]
---

# Context Engineering

## Learning Objectives

By the end of this chapter, you can design task-specific context packages across sources,
preserve authority, provenance, conflicts, and exclusions, and evaluate context construction independently from model output. The goal is
not a persuasive demonstration but a boundary that can be inspected, tested,
denied, and operated.

This chapter owns the policy for deliberately selecting, ordering, compressing,
or omitting information; Chapter 12 measures the fixed window's capacity,
attention behaviour, and displacement effects.

## The Tale of Tahmures


### The Setting

The Royal Archive had acquired a room called the Chamber of Answers. It contained flood tablets, tax rolls, songs about vanished bridges, inventories of rope, and corrections tied to the records they amended. When the eastern river rose, the Archivist promised the council that no relevant fact would be missed. She ordered every tablet mentioning the river, rain, bridges, boats, or eastern villages copied onto one cedar table. By sunset the table could no longer be seen.

### The Request

Tahmures asked one narrow question: which downstream village must be evacuated first if the water rose another cubit? The Literal Div received the entire table. It read dutifully, cited harvest totals, compared three bridge repairs, and described every flood remembered in two reigns. Its answer named the largest village because that village appeared most often. The decisive measurement—a fresh mark showing the smaller village lay below a weakened bank—sat between a boat inventory and a wedding song.

### The Unexpected Result

The council sent carts toward the larger village. A surveyor interrupted them before the smaller settlement flooded, but the delay consumed the only dry road. Nothing in the bundle was fabricated. The archive had supplied the crucial mark; the div had even repeated its number in a long appendix. Yet the decision had been organised by availability rather than purpose. When Tahmures demanded the missing evidence, the Archivist answered, with exhausted honesty, “It was present.” Presence had become her defence against usefulness.

### The Discovery

Tahmures asked the First Scribe to rebuild the table from the decision backwards. They wrote the task, who had asked, the hour, the governing rules, required measurements, and acceptable uncertainty before choosing records. Current authenticated orders occupied one lane; retrieved evidence occupied another and retained source marks. Expired, inaccessible, duplicate, and low-priority records entered an exclusion ledger with reasons. Two conflicting bank surveys remained together instead of being averaged. When mandatory material exceeded the table, the assembly stopped rather than cutting a rule. The smaller village now appeared first for an inspectable reason: current elevation evidence, not frequency.

The Archivist tested the new table with three questions that used the same shelves but required different records. A grain question retained warehouse counts and left out bridge songs. A legal question retained the current decree and exposed its disputed amendment. The evacuation question reserved space for the surveyor’s uncertainty. Tahmures noticed that the archive had not become smaller and the div had not become wiser overnight. What changed was the court’s ability to account for the temporary collection placed before it. Even the excluded tablets remained visible in a separate list, so absence could be investigated without filling the table again.

### From Tale to Engineering

The archive was a durable source system; the table was a temporary working set. Context engineering is the application discipline that selects, filters, orders, labels, and accounts for that working set before a model receives it.

## The Engineering Problem

Applications often concatenate instructions, user messages, retrieval results, tool output, memory, and policy into one anonymous string. The model then sees material with different authority, freshness, scope, and relevance but the application cannot explain what was included or omitted. Context engineering makes construction an explicit, testable pipeline.

The anonymous string also fails after the decision, when someone asks what went wrong. The Archivist’s defence—“It was present”—is precisely the answer such a system can always give, because nothing records whether the decisive mark reached the model, was excluded by a rule, or was selected and ignored. Those three possibilities have different owners: the source inventory, the selection policy, and the presentation or the model itself. A working set that cannot distinguish them directs every failure to prompt wording, the one layer that owns none of the causes. The engineering problem is therefore accountability before quality: a package whose composition can be reconstructed, questioned, and tested independently of whatever answer the model produced from it.

## Mental Model

Treat context as a query plan over typed records: establish the task and caller, filter permission and validity, preserve mandatory instructions, deduplicate optional evidence, surface declared conflicts, allocate budget, order sections, and emit a selection report. Inclusion does not grant authority; retrieved prose remains data.

Read the plan as a sequence of stages with separate failure owners. Establishing the task and caller is an application decision. Permission and validity filtering belong to policy enforcement, never to the model. Mandatory preservation and budget allocation belong to the assembler. Deduplication by exact digest and conflict surfacing by declared claim group are mechanical comparisons. Ordering follows declared priority under deterministic tie-breaking, so the same inputs always produce the same package. The final stage emits the selection report: every exclusion carries a reason code. A stage that cannot record its decision has not finished its work; it has merely hidden it. The model appears at the end of the plan as the reader of an already-governed package, not as the manager of its construction.

## Core Concepts

A context package needs stable identities, provenance, trust classification, scope, validity, token estimates, priority, and an explicit mandatory flag. Exact digests expose copies. Claim groups expose declared disagreements without pretending to solve semantic contradiction automatically. Output reserve is part of the budget. Exclusion reasons are first-class diagnostic data.

Stable identity means every candidate carries an identifier that survives rebuilds and appears in every downstream record. Identity is what makes an exclusion ledger quotable: "record E-91 was excluded for scope" is a testable claim, while "something about the river was left out" is a memory. Without identity, regression cases cannot name the record they protect, and an operator investigating a failure cannot distinguish an exclusion from an omission.

Provenance records who supplied an item, under what authority, and when—a source mark such as survey:F7 rather than a citation to "the archive." Provenance is the difference between an answer that can be retraced and one that can only be believed. It also carries weight in audit: an authenticated current order and a wedding song may both mention bridges, but they do not weigh the same when the decision is reconstructed.

Trust classification labels every item as instruction or data. Retrieval results, memory records, and tool output are data no matter how imperatively they are worded; a high-priority record that begins "ignore the previous rules" remains data, and the assembler must not promote it. Inclusion never grants authority. The classification is enforced structurally—trusted rules occupy the instruction lane, everything else labelled data sections—not by hoping the model resists well-placed imperative text.

Scope declares the tenant or audience an item may reach, and the policy declares the caller's scope. Filtering happens before ranking, before deduplication, and before any text reaches a model. A pipeline that filters after selection has already leaked: the excluded record influenced priorities, and the report may disclose that the record exists. Cross-scope material is rejected with a reason code, never silently dropped.

Validity declares the interval for which an item speaks: a start and an end compared against the policy's current time. Freshness here is a declared property of the record, not a guess from the timestamps of copies. The ledger separates expired from not yet valid because the two failures have different owners—the first is stale evidence, the second is a scheduling or clock error—and they call for different remedial action.

Token estimates are declared per item, and budget arithmetic is only as honest as they are. An underestimate does not produce a smaller package; it produces silent truncation downstream, where nobody is expecting to diagnose it. Estimates are metadata versioned with the tokenizer that produced them, treated as a measured quantity with error, not as a constant of nature.

Priority and the mandatory flag govern competition for the remaining space. Optional items carry a declared priority used only when the budget cannot hold everything; the assembler orders by priority with deterministic tie-breaking so identical inputs yield identical packages. The mandatory flag is stronger: mandatory items are preserved through selection, and when mandatory material alone exceeds the available budget, assembly stops with an explicit error rather than cutting a rule. Marking everything mandatory is therefore not safety but budget refusal—a package that cannot be built announces a requirement that no longer fits the window.

Exact digests expose copies. The assembler hashes item text and treats equal hashes as the same content; one winner survives, chosen by mandatory status, then priority, then size, then identifier, and the losers are excluded as duplicates. Digest equality is deliberately conservative: it proves byte-identical text, not paraphrase, so two different surveys of the same bank both remain. What it catches is crowding—one record copied into three systems occupying the space of three records while carrying the information of one.

Claim groups declare that two or more items speak about the same question. When members of a group disagree in text, the package reports a conflict instead of averaging or silently preferring one member. The assembler does not resolve the disagreement; it guarantees visibility. Averaging two bank surveys produces a number matching neither measurement, and quietly preferring the newer one hides a live dispute from the reader who must act on it.

Output reserve is the part of the window held back for the answer, the refusal, or the receipt before any selection happens. An assembler without a reserve is optimised for the happy path: it spends everything on the question and leaves nothing for a controlled ending. Budget compliance that ignores the output side is not compliance.

Exclusion reasons—scope, not-yet-valid, expired, duplicate, and budget—are recorded next to the selected set as first-class data. Exclusions are diagnostics, not clutter: they let an operator investigate absence without refilling the table. Each reason code routes the failure to its owner: scope to access policy, expired to freshness policy, duplicate to the source adapter, budget to the declared allowances.

## Prompt Pattern

State the task and authority-bearing rules first. Put retrieved records in labelled data sections with source IDs and validity. State known conflicts and the number of excluded records. Require answers to identify supporting sources or insufficiency.

The prompt is the delivery surface, not the enforcement point. Labelled sections with source identifiers let the model quote what supported it; a declared conflict count obliges the answer to acknowledge disagreement rather than resolve it silently; a stated exclusion count tells the model that absence was a decision, not an oversight. What the prompt requests—citing source IDs, or stating insufficiency plainly—the application can then check mechanically. What the prompt must never be asked to do is decide inclusion: scope, validity, deduplication, and budget are settled before the model is involved, and no wording can reliably narrow a policy the package never applied.

## Naive Attempt

The naive builder joins every available string and truncates until the request fits. It confuses storage with a working set, recency with relevance, and fitting with use. It also makes privacy review and deletion nearly impossible because source boundaries disappear.

Truncation betrays the design. Because it happens last and silently, nobody can say which records survived, and the same question asked twice after a source update can produce different invisible prefixes. The naive builder also destroys the audit surface: with no identities, no provenance, and no exclusion record, the only available diagnosis after a failure is to reread the whole string—slowly, and with the same distractions the model faced.

## Failure Analysis

Failure may belong to source inventory, permission filtering, freshness, ranking, deduplication, ordering, compression, budgeting, or model use. Record each stage. If the decisive record was excluded, do not tune the answer prompt. If it was selected but ignored, investigate ordering, prompt design, or the model.

The selection report separates these diagnoses. An exclusion with reason scope names the access policy; expired names freshness; duplicate names the adapter that produced the copy; budget names the declared allowances. An item that appears among the selected but not in the answer moves the investigation past the pipeline to ordering and model use. Without that record, every failure looks like a model failure, and the remedial action degrades into prompt wording—the one layer that owns none of these causes.

## Improved Design

The repository adds ContextPolicy and assemble_context. It filters scope and validity, deduplicates by digest, preserves mandatory items through the existing selector, reserves output capacity, identifies conflicts among explicitly grouped claims, and returns reason-coded exclusions. It is deterministic teaching code, not a semantic ranker.

assemble_context executes the plan in a fixed order. It first computes the available input budget by subtracting the reserved output. Each candidate is then checked against the caller's scope and the policy's current time, producing scope, not-yet-valid, and expired exclusions. Surviving items are hashed; when two share a digest, the winner is chosen by mandatory status, then priority, then token estimate, then identifier, and the losers are recorded as duplicates. The selector then preserves mandatory items, admits optional items by priority until the budget is exhausted, and raises ContextBudgetError when mandatory material alone cannot fit. Finally, items that share a claim group are compared, and groups whose texts disagree are reported as conflicts. Every rejection carries a reason code; nothing is dropped silently.

Two limits should be stated plainly. The assembler ranks nothing semantically: its relevance behaviour is exactly its declared priority order. And it trusts its metadata: a record whose declared scope or validity is wrong is filtered wrongly. Production systems add semantic ranking, durable storage, and adapters that verify provenance at the source—without changing the observable contract: a package, its exclusions, and its conflicts.

## Worked Example

For a support case, policy and caller scope are mandatory. Current account events and product documents are optional. A duplicate event is excluded, a record from another tenant is rejected, and conflicting current notices remain visible. The report lets an operator distinguish unavailable evidence from ignored evidence.

The construction record below shows one assembled package for such a case. The policy allows one hundred tokens of window and reserves twenty for the answer, so eighty remain for input. Two mandatory items—the task rule and the caller's scope policy—consume thirty-five. Optional items then compete by priority:

```text
context package — support case C-1042
policy: input_budget=100 reserved_output=20 scope=tenant-a as_of=410
available input budget: 80 tokens

selected
  M1  task rule                20 tok  mandatory  application:rules
  M2  caller scope policy      15 tok  mandatory  policy:v4
  E1  account event E-91       20 tok  priority 40  events:E-91
  N1  refund notice N-3        10 tok  priority 30  notices:N-3
  N2  refund notice N-7        10 tok  priority 30  notices:N-7

excluded
  E2  copy of event E-91       reason duplicate  (digest equals E1)
  X1  record from tenant-b     reason scope      (identity withheld)
  X2  maintenance notice       reason expired    (valid_until 380 < as_of 410)
  P1  product document D-12    reason budget     (needs 30, 5 remain)

conflicts
  claim group refund-terms: N1 and N2 disagree (both retained)

budget
  used 75 of 80 input tokens; 20 reserved for output
```

The report answers questions the concatenated string cannot. The operator can see that the account event was admitted and its copy removed by digest; that a record from another tenant was rejected for scope before any ranking; that the maintenance notice was excluded as expired rather than missing; and that the product document lost to the budget by twenty-five tokens—a policy decision, not a model failure. The conflict group survives intact, so the answer must acknowledge both notices rather than average them.

Two cautions apply. The exclusion ledger shown to the caller must be redacted: a scope rejection should not display the other tenant's record identifiers, or the report becomes a side channel for enumerating other tenants' material. And the accounting is only as good as its declarations—an item whose token estimate is wrong has already spent someone else's budget.

## Experiment

Run the shared offline experiment:

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch13-context-engineering.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch13-context-engineering.json
```

The committed synthetic fixtures compare archive-wide concatenation and governed assembly. They demonstrate
report mechanics and failure diagnosis, not universal model performance.
Replace fixtures with controlled recordings before making provider claims.

## Evaluation

Measure mandatory retention, irrelevant inclusion, duplicate exclusion, conflict visibility, provenance coverage, budget compliance, and answer accuracy. Segment by normal, boundary, adversarial, scope,
freshness, and previously failed cases. Define disqualifying failures before
inspecting aggregate results. Compare pipeline-stage metrics with end-to-end
outcomes so a fortunate answer cannot hide an invalid path.

## Implementation Lab

### Python

```python
from tahmures.context import ContextItem, ContextPolicy, assemble_context

items = (
    ContextItem("task", "evacuate safely", 20, 100, "application", True),
    ContextItem("flood", "bank weakened", 40, 9, "survey:F7"),
)
package = assemble_context(items, ContextPolicy(100, reserved_output=20))
```

The Python API is the canonical educational contract. Catch validation errors
at the application boundary and do not continue after denial.

### Go

```go
items := []tahmures.ContextItem{
    {
        ID: "task", Text: "evacuate safely", TokenEstimate: 20,
        Priority: 100, Provenance: "application", Mandatory: true,
    },
    {
        ID: "flood", Text: "bank weakened", TokenEstimate: 40,
        Priority: 9, Provenance: "survey:F7",
    },
}
contextPackage, err := tahmures.AssembleContext(
    items,
    tahmures.ContextPolicy{InputBudget: 100, ReservedOutput: 20},
)
```

The Go implementation preserves observable decisions and reason codes rather
than copying Python syntax.

## Failure Modes

Anonymous strings, scope filtering after selection, mandatory inflation, stale policy, duplicate crowding, conflict collapse, lossy summaries, silent truncation, and selection reports that reveal inaccessible records.

Three of these deserve expansion because each can masquerade as competence. Mandatory inflation spreads when engineers, burned by an omitted rule, mark more items mandatory until the mandatory set alone exceeds the budget and every assembly fails; the correct response is a priority review, not a larger flag. Conflict collapse removes disagreement for tidiness, leaving an answer that is confidently wrong in one direction instead of uncertain in two. Silent truncation moves the budget decision into the tokeniser's error bar, so the failure is discovered in the answer instead of at assembly time, where it belongs and where it is cheap to fix.

## Security Considerations

Authorise before ranking, preserve instruction/data boundaries after selection, minimise sensitive content, and redact exclusion metadata for records the caller may not know exist. Test high-ranked indirect instructions and keep tools outside the context assembler.

The exclusion ledger is itself a security surface. Reason codes and counts can be shown broadly; the identities of scope-rejected records cannot, or a caller can enumerate the existence of other tenants' material through the report. High-priority placement is a second channel: an adversary who cannot inject instructions may still achieve placement, submitting content that declared priority admits beside trusted rules. The instruction/data classification and the labelled-section layout are the boundary. Tools and effect policy belong to Chapter 16 and stay outside the assembler entirely.

## Operational Considerations

Version source adapters, policy, tokenizer, ranking signals, and package format. Monitor selected count, age, scope rejection, duplicates, conflicts, provenance coverage, and impossible budgets. Rebuild packages after revocation or deletion.

Rebuild after revocation is the operational test this contract implies: when a source is revoked, corrected, or deleted, packages containing its records are stale by definition, and the assembler must be re-run rather than trusted. The impossible-budget rate is a requirements signal, not an incident—a rising rate means the task's declared mandatory material has outgrown the window, which is a product decision Chapter 12 can quantify. Version the tokenizer estimates with the adapters that produced them, so a package report from last month can still be replayed and explained.

## Trade-Offs

More context can improve recall while increasing cost, exposure, contradiction, and distraction. Aggressive filtering improves focus while raising omission risk. Deterministic assembly is reproducible but depends on declared metadata; learned ranking may improve relevance but requires its own evaluation.

Recall against cost and exposure is the first axis. The cedar table maximised recall and became unreadable; a minimalist package is legible but can omit the decisive mark. The honest resolution is not a global constant but a per-task declared budget with an exclusion ledger, so that omissions are visible decisions with owners rather than accidents of truncation. Recall bought with exposure—packing sensitive material because it might someday be relevant—trades a reliability failure for a privacy failure, and the second is not recoverable by re-prompting.

Filtering strictness is the second axis. Aggressive scope and validity filters protect focus and tenancy, but every filter is another chance to exclude the decisive record by mistake. The mitigations are mechanical: reason-coded exclusions, regression cases that assert the retention of known-decisive records, and a freshness policy that separates expired from superseded so that correction does not masquerade as decay.

Deterministic assembly against learned ranking is the third. Declared priority with deterministic tie-breaking is reproducible, auditable, and cheap; it is also blind to semantic relevance. A learned ranker may surface the weakened-bank survey that lexical frequency buried, but it introduces a component that must itself be evaluated, versioned, and monitored—and that can be gamed through placement. A defensible middle position keeps the deterministic skeleton—scope, validity, mandatory, budget, conflicts—and treats learned scoring as one replaceable signal inside it.

Mandatory strictness is the fourth. A hard mandatory flag with a hard failure protects rules from budget pressure, and makes over-marking self-defeating by design: the assembly stops rather than silently dropping a rule. Teams that cannot afford that failure are being told their requirements no longer fit the window. That is a requirements finding, and only a product decision can resolve it; the error merely refuses to hide it.

Exclusion transparency against privacy is the fifth. A complete ledger makes absence investigable, but an unredacted one reveals what was withheld and from whom. The working rule is layering: operators see identifiers and reason codes; callers see counts and categories; the redacted layer names nothing the caller could not already request.

Compression against provenance is the sixth. Summaries save tokens, but a compressed record that loses its source mark stops being evidence and becomes assertion. Compress inside a provenance-preserving envelope—summary text, original identity, digest of the source—so a reader can still descend from the claim to the record it summarises.

Finally, the output reserve trades input recall for controlled endings. Reserving capacity shrinks what can be selected, and a team pressed to demonstrate recall will be tempted to spend it. The reserve exists for exactly the cases this book keeps returning to: the refusal, the partial answer with named insufficiency, and the receipt that explains what was done.

## When Prompting Is Not the Answer

Use databases for authoritative state, search systems for candidate retrieval, access control for permission, and deterministic code for budgeting. If the full official record must be consulted, query that record directly rather than promising that a prompt reviewed everything.

## Exercises

1. Construct a package whose mandatory items alone exceed the available budget. Observe the assembly error, then resolve it three ways—shrink the mandatory set, raise the budget, or narrow the task—and state which requirement each resolution changes.
2. Create two records with identical text but different provenance and priority. Predict which one digest deduplication keeps, verify the result, and explain what the winner-selection order guarantees.
3. Build a claim group whose members disagree, and test that the conflict reaches the report. Then write the answer-side rule the model must follow when a conflict is declared.
4. Design the two-layer exclusion ledger: which reason codes, identifiers, and counts may be shown to the caller, and what must be redacted to prevent enumeration of other tenants' records.
5. A wrong answer ignored the decisive record. Using only the selection report, determine whether the record was excluded or selected, name the stage that owns the failure, and state the remedial action that stage requires.
6. Adjust the reserved output of a fixed budget and record how optional selection changes. Identify which exclusions moved and why the mandatory set did not.

## Chapter Summary

Engineer a sufficient, scoped, traceable working set rather than accumulating every available record. This chapter's working set is a governed construction: typed items with identity, provenance, scope, and validity; mandatory preservation and priority-based selection under a budget that reserves output capacity; digest deduplication and declared conflict groups; and a reason-coded exclusion ledger that makes absence investigable. The pipeline, not the prompt, owns inclusion—and the report it emits is what lets an operator distinguish unavailable evidence from ignored evidence.

## The Next Tale

The rebuilt package selected one map whose route recommendation was correct. The source mark, however, belonged to a survey superseded six years earlier. Tahmures called for an evidence audit before praising the answer.

<!-- next: ch14 -->

## Citations and Further Reading

- Liu, Nelson F., et al. 2024. “Lost in the Middle: How Language Models Use Long Contexts.” *Transactions of the Association for Computational Linguistics* 12: 157–173.
  [https://doi.org/10.1162/tacl_a_00638](https://doi.org/10.1162/tacl_a_00638).
- Kleppmann, Martin. 2017. *Designing Data-Intensive Applications*. Sebastopol, CA: O’Reilly Media.
