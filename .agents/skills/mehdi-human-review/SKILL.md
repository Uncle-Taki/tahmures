---
name: mehdi-human-review
description: Reconcile human editorial notes against a canonical source, prepare supervised bilingual repairs and human signoff, then reconcile review metadata only after explicit human approval.
---

# Human-review reconciliation

Use this skill when a human supplies notes on translated or localized chapters.
It owns the review lifecycle, not initial translation or general authoring.
Read project authority files and `$mehdi-context`; use `$mehdi-bilingual`,
`$mehdi-narrative`, or `$mehdi-review` for relevant specialist questions.

## Authority

- Human notes are evidence of intent, observed problems, and preferences. A
  question is not automatically an edit instruction.
- The current canonical source controls technical meaning. Project rules,
  glossary, continuity, and protected-content contracts control their domains.
  Proposed human wording does not authorize semantic drift.
- Human-approved wording is precedent for the revision it covered. New human
  notes deserve direct consideration; provisional machine patterns are weaker
  evidence. Neither overrides canonical meaning or project rules.
- The machine prepares repairs. A supervisor accepts machine repair quality and
  resolves risky boundaries. Only the human grants final human signoff.

In the Tahmures workflow, GLM performs the bulk note ledger, targeted edits,
self-review, validation, and packet preparation. GPT handles source conflicts,
policy decisions, risky technical boundaries, skill architecture, and narrow
supervisory acceptance without repeating the whole GLM pass. The human decides
editorial preferences, approves naturalness, and signs off the final revision.

## Reconcile a batch

1. Identify human input, target chapters, canonical-source revision, review
   metadata, and working-tree baseline. Read notes in context and compare the
   corresponding source before changing translation.
2. Give every note a stable ID. Classify it as `DIRECT_FIX`,
   `GRAMMAR_OR_NATURALNESS`, `SOURCE_MEANING_QUESTION`, `TERMINOLOGY`,
   `PROTECTED_TOKEN`, `RTL_OR_MIXED_SCRIPT`, `NARRATIVE_LOCALIZATION`,
   `HUMAN_PREFERENCE`, or `CROSS_CHAPTER_DECISION`; use multiple classes if
   needed.
3. Keep a complete ledger: original note, location, class, source meaning,
   action and reason, before/after or unchanged evidence, and disposition:
   `RESOLVED`, `RESOLVED_ALREADY_PRESENT`, `PARTIALLY_ADOPTED_WITH_REASON`,
   `REJECTED_AS_SOURCE_UNFAITHFUL`, `DEFERRED_CROSS_CHAPTER_DECISION`, or
   `NEEDS_HUMAN_CONFIRMATION`. Account for questions and duplicates too.
4. Make targeted, source-faithful repairs. Improve target-language grammar,
   modifier and adverb scope, verbs, word order, and readability (including
   ezafe where the target is Persian) without copying source-language sentence
   architecture or replacing sound human-approved prose. If proposed wording
   drops a technical condition, preserve it in a natural repair and explain
   non-adoption in the signoff packet.
5. Classify Latin spans before editing: protected identifier, schema/field,
   code, bibliographic title, established technical term with explanation, or
   ordinary English prose. Preserve protected bytes; ordinarily translate or
   explain reader-facing prose. Do not apply a global Latin-word rule.
6. Inspect logical and rendered RTL order, arrows, labels, fences, and
   copy/paste. Bidi controls are an optional local technique: balance them,
   keep them out of protected tokens and executable fences, and check
   maintainability. Do not universalize a technique from one batch.
7. Before localizing a story name or object, check continuity, glossary, and
   recurring identity. In Tahmures, route such a note through
   `$tahmures-narrative` alongside `$mehdi-narrative`; preserve events and
   metaphor boundaries. The human still approves editorial preference.
8. Inspect the diff, run focused translation/protected-content/editorial checks
   and the project-required gate, then self-review every disposition. Passing
   validators do not prove semantic or rendered quality.

## Supervisory check and human signoff

Prepare a compact, note-indexed packet: original note, before/after, source
meaning or reason, disposition, and precise human question if unresolved.
Include rendered RTL evidence where needed. Expose partial or rejected proposed
wording so the human can assess changed passages without rereading unrelated
chapters.

The supervisor checks ledger completeness, risky source/technical decisions,
protected content, diff scope, rendered mixed-script text, validation, and
whether genuine preferences remain with the human. Supervisory acceptance
means **machine repairs are ready for human signoff**, not human approval.
Neither machine role may mark `human_reviewed` during reconciliation.

## After explicit human approval

1. Record dated, chapter-and-revision-specific human approval evidence and
   any requested final corrections. Confirm later corrections with the human
   before claiming approval of that revision.
2. In a separate metadata step, update review status, dates, and provenance
   only as supported by the project schema and approval evidence. Historical
   review does not automatically certify later content.
3. Consolidate observations as `SAFE_TO_REUSE` (repeated or explicitly
   human-approved as reusable guidance), `PROVISIONAL` (single-batch inference),
   `CHAPTER_SPECIFIC`, or `REQUIRES_MORE_HUMAN_EVIDENCE`. Prior patterns inform
   later batches but never outrank new notes, source, or project rules.
4. Keep terminology as candidates first. Promote to the canonical glossary
   only after human approval, cross-chapter evidence, and consistency review.
   Add regression checks for stable machine-checkable rules.
5. Rerun validation and continue the next batch. Once all chapters have
   current human approval, route terminology consolidation, process-metadata
   reconciliation, visual audit, whole-book bilingual review, publication
   gates, publisher work, and final supervisory acceptance. Commit or publish
   only with explicit authorization.

Target-language-only edits do not change the canonical source hash. Never refresh a
hash merely to pass validation or equate a current hash with human approval.
