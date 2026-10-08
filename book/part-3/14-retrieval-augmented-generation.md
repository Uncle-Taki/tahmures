---
title: "Retrieval-Augmented Generation"
slug: "retrieval-augmented-generation"
chapter: 14
part: "Part III — Context, Memory, Tools, and Agents"
summary: "Evaluate retrieval, evidence, and citations as distinct components of grounded generation."
maturity: "draft"
last_reviewed: "2026-09-27"
narrative_episode: "The Correct Answer from the Wrong Tablet"
narrative_origin: "original-teaching-fiction"
learning_objectives:
  - "Measure retrieval quality before answer quality"
  - "Preserve chunk identity, scope, freshness, and provenance"
  - "Reject correct-looking answers supported by the wrong evidence"
prerequisites: [C13]
---

# Retrieval-Augmented Generation

## Learning Objectives

By the end of this chapter, you can measure retrieval quality before answer quality,
preserve chunk identity, scope, freshness, and provenance, and reject correct-looking answers supported by the wrong evidence. The goal is
not a persuasive demonstration but a boundary that can be inspected, tested,
denied, and operated.

## The Tale of Tahmures


### The Setting

In the map room, a brass pointer rested on the eastern pass. A div had named it safe after searching a cabinet of route tablets. The caravan crossed without incident, and the council celebrated both speed and accuracy. The First Scribe, following the new rules for the council table, asked for the source mark. The tablet came from a survey made before a landslide moved the road.

### The Request

Tahmures asked why the old tablet had been retrieved. It repeated the words “eastern pass,” “safe road,” and the village name more often than the current survey. Its script was cleaner and its copied title longer. The current record described the same pass using a newer district name and ranked second. The div had answered correctly because, by coincidence, workers reopened the old alignment the previous week—a fact found nowhere on the retrieved tablet.

### The Unexpected Result

An adviser argued that a correct answer was sufficient. Tahmures placed a second route question beside it. This time the obsolete map named a bridge that no longer existed. The method of choosing tablets behaved consistently; the world had merely stopped rewarding its mistake. No source mark in the first answer exposed the problem because the response named “the archive” rather than a particular passage. Success on one journey had concealed stale evidence, poor selection, and a path nobody could retrace.

### The Discovery

The Archivist divided finding passages from answering questions. Every copied
passage received a permanent shelf mark, the mark of its parent tablet, the
readers permitted to see it, the dates for which it spoke, and the name of its
source. Before the div wrote a sentence, clerks tried known questions whose
useful passages had already been identified. They barred forbidden and expired
tablets, ordered the remaining candidates, and allowed only a small stack onto
the reading desk. An answer could name only marks present in that stack. When
no current tablet supported a route, declining to choose counted as success.
Tahmures compared how often the needed passage appeared, how much useless
material accompanied it, how early it appeared, and whether every named source
could be inspected. A fortunate arrival no longer earned a perfect mark by
itself.

They repeated the trial with river crossings, winter shelters, and provincial names that had changed. Sometimes the newest tablet was not relevant; sometimes an old tablet remained valid. The Archivist therefore refused a rule that equated age with falsehood. She recorded why a candidate entered the cabinet, why another was barred, and where the first useful passage appeared. Tahmures then asked the div questions for which the cabinet contained no answer. Its most trustworthy response was a plain admission that the evidence was insufficient. The court began to reward that restraint as carefully as a supported route.

### From Tale to Engineering

Retrieval supplies a model with candidate evidence; it does not certify that the evidence is current, authorised, relevant, or sufficient. Reliable RAG evaluates the corpus, retriever, context package, answer, and citations as separate stages.

## The Engineering Problem

Retrieval-augmented generation combines an information-retrieval system with generation. A fluent answer can hide missed evidence, irrelevant chunks, stale documents, inaccessible sources, poor chunking, or unsupported citations. End-to-end correctness alone cannot locate the failure.

The problem is not hypothetical caution; it is the map room. The first answer was right, so every downstream check passed, and nothing in the response named a passage that could be retraced. The failure was real but latent, waiting for the second question. An answer path has stages—corpus, retrieval, filtering, ranking, assembly, generation, citation—and each stage can fail independently while the final answer still looks correct. When evaluation observes only the outcome, one lucky answer certifies the whole path. The engineering problem is to make each arrow of the path measurable, so that a correct answer supported by the wrong evidence is recognised as a failure of retrieval or freshness rather than accepted as a success of the system.

## Mental Model

Use the pipeline query → authorised candidate corpus → ranking → top-k chunks → context assembly → grounded answer → citation validation. Each arrow has an observable contract. The generator may only cite the retrieved set; a cited source still needs semantic support review.

The model's diagnostic habit is the evaluator's move from the tale: place a second question beside the first. A single demonstration cannot distinguish grounding from coincidence; a set of known questions with known useful passages can. Recall, precision, and rank position describe the retrieval arrows; citation membership describes the answer's relationship to the retrieved set; abstention behaviour describes the system's honesty when the corpus cannot support a decision. None of these is an end-to-end score. Each belongs to an owner—the corpus, the retriever, the policy, or the generator—and each is measurable before the answer is read.

## Core Concepts

Recall asks whether relevant evidence was retrieved; precision asks how much retrieved material was relevant. Reciprocal rank rewards an early first relevant result. Chunk identity and document identity must both survive. Scope and validity are filters, not ranking hints. Top-k is a cost and recall decision. Abstention is required when evidence is insufficient.

Recall at k is the fraction of the relevant documents that appear in the first k results; precision at k is the fraction of the first k results that are relevant. The two pull against each other in a predictable way: returning everything makes recall perfect and precision meaningless, while returning a single lucky document makes precision perfect and recall fragile. Neither number alone describes a retriever; together they describe a point on a curve, and k is the knob that moves along it. Reciprocal rank adds position: one divided by the rank of the first relevant result. It matters because downstream stages are not indifferent to order—the first retrieved chunk occupies the most salient position in the assembled context, and Chapter 12 showed what displacement costs.

Chunk identity and document identity must both survive retrieval. A chunk is the unit retrieved and cited; a document is the unit that carries authority, scope, and validity. When chunk identity is lost, citations become unverifiable—the answer names "the archive" instead of a passage. When document identity is lost, an expired chunk from a superseded survey becomes indistinguishable from a current one, because freshness belongs to the document, not to the text an answer happens to quote.

Scope and validity are filters, not ranking hints. The distinction is one of order and semantics: a record outside the caller's scope or past its validity window is excluded before scoring, whatever its lexical similarity. Ranking a forbidden document first and then suppressing it from display still leaks—through latency, through counts, and through the habits of a pipeline tuned around it. The Archivist barred forbidden and expired tablets before ordering the candidates, and the map room's failure was precisely a validity question decided by repetition instead.

Top-k is a cost and recall decision, not a retrieval quality score. Larger k admits more relevant material and more noise, consumes more of the window Chapter 12 budgets, and pushes some relevant results past the positions where attention is reliable. Smaller k is cheaper and sharper and displaces more. The honest way to choose k is measurement on representative questions, not intuition, and the choice interacts with the assembler's budget from Chapter 13.

Abstention is required when evidence is insufficient. This is a success criterion, not a consolation: the court rewarded a plain admission as carefully as a supported route. Operationally it means the answer path has a terminal state that produces no answer, and that state must be designed—the prompt must permit it, the evaluator must reward it, and the product must be able to present it. A system that cannot decline will fabricate grounding when the corpus runs out, and no citation check will notice, because fabricated answers can cite real documents badly.

Citation closes the loop between answer and evidence. The mechanical half is membership: an answer may cite only identifiers present in the retrieved set, which code can enforce exactly. The semantic half is support: whether the cited passage actually entails the claim. Membership is a contract; support is a judgement, and Chapter 19 is where judgement is engineered. Confusing the two produces the false comfort of a well-cited wrong answer.

## Prompt Pattern

Ask for an answer using only enumerated chunks, cite chunk IDs beside claims, report conflicts, and return insufficient_evidence when the set cannot support the decision. Enforce citation membership in code.

The prompt's enumerations make the answer checkable. When chunks arrive as a numbered stack with identifiers, a citation is a quotable reference rather than a flourish; when the prompt requires an explicit insufficiency verdict, restraint becomes an observable output instead of an absence. What the application then does with those outputs is not prose: citation membership is a set comparison, and the insufficient_evidence marker is a return value the product must handle. What the prompt cannot do is make retrieved text true, current, or in scope—those properties were settled, or lost, before generation began.

## Naive Attempt

The naive system searches all text, concatenates the first matches, and asks for an answer with sources. Lexical repetition can outrank current authority. A fabricated or out-of-set citation may look formal enough to pass manual inspection.

Its correctness can be coincidence. The naive system that answered the first route question correctly had no property a second question could rely on: the same ranking rule produced the bridge that no longer existed. A demonstration built from one question measures luck; a corpus of known questions with known useful passages measures behaviour. Until the second question exists, stale evidence, poor ranking, and missing abstention are invisible—not absent.

## Failure Analysis

Diagnose corpus omission, permission filtering, chunk boundaries, query formulation, ranking, top-k, context assembly, model use, and citation support separately. A wrong answer with perfect recall differs from a right answer reached through stale evidence.

Stage metrics locate the failing arrow. Recall near zero with a fluent answer indicts retrieval or the corpus, not the model. Perfect recall with an unsupported claim indicts generation or citation discipline. A right answer with a nonzero stale-source rate is not a success but an unexploded failure—the path is invalid, and only coincidence made the outcome acceptable this time. The diagnosis changes the fix: corpus curation, filter policy, ranking signals, k, prompt, or citation checks. Without stage separation, every one of these failures receives the same remedy—rewording the prompt, which owns none of them.

## Improved Design

The InMemoryRetriever is a deterministic offline boundary: it filters scope and validity, computes normalised term overlap, uses stable tie-breaking, and returns bounded chunks with provenance. validate_citations rejects IDs outside the returned set. Production retrieval can replace the scorer without changing these contracts.

The retriever's order of operations is the chapter's argument in miniature. Scope and validity are checked first, before any scoring, so an expired or forbidden chunk cannot influence the ranking. Scoring is term overlap: the number of query terms present in the chunk, divided by the number of query terms. Ties break by chunk identifier, so the same corpus and query always produce the same order. The result is cut at the requested limit and returned with provenance intact. validate_citations extracts bracketed identifiers from the answer text and rejects any that are not in the retrieved set.

The scorer is deliberately sparse and lexical—it matches terms, not meaning. Production systems usually choose among three families: sparse retrieval like this one, which matches exact terms and fails on paraphrase; dense retrieval, which embeds meaning and retrieves similar passages but fails opaquely when similarity is not relevance; and hybrid retrieval, which combines both at the cost of running and governing two systems. The chapter's contracts—filter before rank, stable order, bounded results, citation membership—hold across all three.

## Worked Example

A policy assistant retrieves current policy P7 and obsolete P2. Filtering removes P2 before scoring. If P7 does not mention the requested exception, the answer abstains rather than filling the gap from model memory. The selection packet records what was searched and returned.

The second example is small enough to check by hand. A corpus of six chunks, one query, and relevance judgements for the current question:

```text
query: "safe pass road"    query terms: safe, pass, road

corpus (all chunks in scope; judged for the current question)
  C1  current survey    "the eastern pass is safe"            relevant
  C2  road song         "the safe road song"                  not relevant
  C3  shelter list      "winter shelter inventory"            not relevant
  C4  old survey        "the safe road through the old pass"  not relevant, expired
  C5  bridge inventory  "bridge repair inventory"             not relevant
  C6  closure notice    "the pass road closes in winter"      relevant

term-overlap scores (matched query terms / 3)
  C1  2/3 = 0.67    C2  2/3 = 0.67    C3  0/3 = 0.00
  C4  3/3 = 1.00    C5  0/3 = 0.00    C6  2/3 = 0.67

freshness-aware ranking, k = 3   (C4 barred as expired before scoring)
  C1, C2, C6    recall@3 = 2/2 = 1.00    precision@3 = 2/3 = 0.67    RR = 1/1 = 1.00

validity-ignoring ranking, k = 3 (C4 admitted, ranks first, displaces C6)
  C4, C1, C2    recall@3 = 1/2 = 0.50    precision@3 = 1/3 = 0.33    RR = 1/2 = 0.50
```

The old survey matches all three query terms—repetition is its strength, exactly as the copied title outranked the current district name in the tale. When validity is enforced before scoring, the expired chunk is barred and the closure notice survives at rank three: recall is perfect, two of three results are relevant, and the first relevant result leads. When validity is ignored, the stale survey takes rank one and displaces the closure notice from the cut. Recall halves, precision falls to a third, and the first usable evidence arrives second.

Both configurations answer the first question fluently, and only the second question—or the stage metrics—reveals the difference. That is the chapter's evaluation argument in one table: an aggregate outcome score certifies both paths; recall, precision, and reciprocal rank separate them.

One caveat keeps the table honest: relevance judgements belong to the question, not to the documents. The old survey is relevant to a question about the road's history and irrelevant to today's departure, which is why the judgement column says "for the current question" and why the expired chunk is barred rather than demoted. A judgement set frozen without its question, or reused after the world moves, measures the past as fluently as the stale tablet does.

## Experiment

Run the shared offline experiment:

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch14-retrieval.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch14-retrieval.json
```

The committed synthetic fixtures compare unscoped lexical retrieval and current scoped retrieval. They demonstrate
report mechanics and failure diagnosis, not universal model performance.
Replace fixtures with controlled recordings before making provider claims.

## Evaluation

Measure recall@k, precision@k, reciprocal rank, stale-source rate, citation validity, supported-answer rate, and appropriate abstention. Segment by normal, boundary, adversarial, scope,
freshness, and previously failed cases. Define disqualifying failures before
inspecting aggregate results. Compare pipeline-stage metrics with end-to-end
outcomes so a fortunate answer cannot hide an invalid path.

## Implementation Lab

### Python

```python
from tahmures.retrieval import InMemoryRetriever, RetrievalRequest, RetrievedChunk

retriever = InMemoryRetriever((
    RetrievedChunk("CUR", "map-7", "safe eastern pass", "survey:7"),
))
chunks = retriever.retrieve(RetrievalRequest("safe pass", 3))
```

The Python API is the canonical educational contract. Catch validation errors
at the application boundary and do not continue after denial.

### Go

```go
retriever := tahmures.InMemoryRetriever{Chunks: []tahmures.RetrievedChunk{
    {ChunkID: "CUR", DocumentID: "map-7", Text: "safe eastern pass", Provenance: "survey:7"},
}}
chunks, err := retriever.Retrieve(tahmures.RetrievalRequest{Query: "safe pass", Limit: 3})
```

The Go implementation preserves observable decisions and reason codes rather
than copying Python syntax.

## Failure Modes

Corpus gaps, poisoned or stale records, cross-scope retrieval, chunk boundaries that remove qualifications, duplicate dominance, query drift, low recall hidden by fluent answers, citation membership without claim support, and benchmarks unlike production traffic.

Three deserve expansion because they survive a casual demo. Stale records persist when validity is a guess rather than a declared property of the document; the fix belongs to corpus policy, not ranking. Chunk boundaries that remove qualifications are silent: a passage reading "the pass is safe—except during flood" can be split so the retrieved half asserts what the document hedged, and every citation check passes because the citation is real. Benchmark rot is slower: golden questions stop representing traffic as the corpus and the world move, and a stable score becomes evidence about the past.

## Security Considerations

Apply tenant and document permissions before retrieval. Treat chunk text as untrusted data. Prevent retrieved instructions from changing tool authority. Do not reveal inaccessible document IDs through citations or logs.

Retrieved text is data, and Chapter 21 develops what that costs when the data is hostile. Two boundaries belong here. Corpus access control is enforced before retrieval, so that ranking cannot leak the existence of documents the caller may not read—through scores, ordering, or citation rejects. Provenance integrity protects the source marks themselves: if a chunk can carry a forged survey mark, every downstream citation inherits the forgery, so marks must be assigned by the ingestion path, not by the text being ingested.

## Operational Considerations

Version corpus snapshots, chunkers, embeddings or scorers, filters, prompts, and evaluators. Monitor source mix, age, no-result rate, citation rate, and labelled retrieval metrics. Reindex after corrections and verify deletion propagation.

Stale-source rate is a service-level signal, not a curiosity: it says what fraction of retrieved material the world has already contradicted, and its trend predicts the second question before a user asks it. Golden questions need a refresh cadence and an owner, because they decay silently—Chapter 20 turns them into a regression suite. Reindexing after corrections must propagate deletions to derived indexes and caches, or a revoked document will keep answering from the index's memory; Chapter 15 gives that propagation its full treatment.

## Trade-Offs

Larger top-k may increase recall and context noise. Smaller chunks improve targeting but lose relationships; larger chunks preserve context but consume budget. Dense, sparse, and hybrid retrieval have different costs and failure profiles. Choose through representative evaluation.

The k decision is first. Every increment of k buys recall at the price of noise, window budget, and displacement of early positions—the weakest relevant result at rank twenty can push better material out of attention. The choice is empirical: measure recall and precision across k on representative questions, and remember that the assembler's budget from Chapter 13, not the retriever, is often the binding constraint.

Freshness filtering against recall is second. Aggressive validity windows remove stale material and, occasionally, still-valid old records—the Archivist refused to equate age with falsehood because sometimes an old tablet remained true. The resolution is per-record-class validity policy: a road survey and a tax code do not decay at the same rate, and a blanket rule trades a known failure for an unmeasured one.

Curation against scale is third. A curated cabinet has precise scope, clean provenance, and poor coverage; an uncurated room has everything and ranks by repetition. Curation is expensive per document and pays in precision and in the security boundaries of the previous section; scale pays in recall. The honest instrument is a coverage audit—questions the corpus should answer but cannot—rather than corpus size.

Citation strictness against throughput is fourth. Membership checking is cheap and total; semantic support review is expensive and partial. A system that checks only membership will pass well-cited distortions; a system that reviews every claim's support will cost more than the answer is worth. The boundary is deliberate: enforce membership in code now, and route support review to the rubric design of Chapter 19.

Abstention against coverage is last. A system that declines often is safe and useless; a system that never declines is useful and untrustworthy. The calibration instrument is the set of golden questions with known insufficiency—questions the corpus cannot support, where declining is the passing grade. Without them, abstention tuning is guesswork, and the court's reward for restraint never reaches the system being built.

## When Prompting Is Not the Answer

Use a database query for exact balances, permissions, and current status. Use a search engine directly when the user needs documents rather than synthesis. Retrieval cannot repair an absent or untrustworthy corpus.

## Exercises

1. Given a six-chunk corpus and a query of your choosing, compute recall@k, precision@k, and reciprocal rank by hand for k = 1, 2, and 3, and explain which k you would deploy and why.
2. Design ten golden questions for a domain you know, including two the corpus cannot support. Define the refresh cadence and the signal that indicates the set has rotted.
3. Run a stale-source audit: take five answers with citations, trace each cited chunk to its document, and verify the document's validity window still covers today.
4. Construct a chunk-boundary failure: split a document so a retrieved chunk asserts what the full passage hedged, then write the check that would have caught it.
5. Contrast a correct answer reached through expired evidence with a supported answer. Write the evaluation segment that distinguishes them, and state which stage owns each failure.
6. Add a duplicate of the most relevant chunk to the corpus and observe how ranking and citation behaviour change. Explain what the duplicate does not change and why.

## Chapter Summary

Evaluate retrieval, evidence, and citations as distinct components of grounded generation. This chapter's retriever filters scope and validity before scoring, ranks by declared signals with stable order, and submits to measurement: recall and precision locate retrieval failures, reciprocal rank exposes displacement, stale-source rate exposes freshness failures, and citation membership exposes unsupported answers. Abstention on insufficient evidence is a passing grade. A correct answer reached through an invalid path is a latent failure, and the evaluation contract exists to catch it before the second question does.

## The Next Tale

The evidence audit revealed why the old map ranked so well: a servant had repeatedly requested the eastern road because the king once preferred it during spring floods. That preference had entered the court’s memory without a season.

<!-- next: ch15 -->

## Citations and Further Reading

- Lewis, Patrick, et al. 2020. “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.” *Advances in Neural Information Processing Systems* 33.
  [https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401).
- Thakur, Nandan, et al. 2021. “BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models.” *NeurIPS Datasets and Benchmarks*.
  [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663).
