# Claude final independent review — Chapters 01–04 character-narrative refactor

MODE = INDEPENDENT_FINAL_REVIEW

PHASE = CH01_04_CHARACTER_NARRATIVE_REFACTOR

ROLE: Claude is the independent final checker for the completed bounded
character-narrative refactor. GPT has rechecked the two narrative corrections
and the Persian spelling alignment. The human remains the final editorial
authority.

Do not edit manuscripts, records, validators, or skills. Do not change source
hashes, review metadata, or approval state. Do not commit. Write only the
review report requested below.

## 1. Load governing evidence

Read the relevant live skills under `.agents/skills/`, especially
`mehdi-context`, `mehdi-bilingual`, `mehdi-narrative`,
`tahmures-narrative`, `mehdi-review`, and `tahmures-editorial`.

Read these phase records:

- `.agents/tahmures_characters.md`
- `.agents/tahmures_characters_part2.md`
- `.agents/tahmures_character_behaviors_ch01-04.md`
- `.agents/tahmures_character_visual_prompts_ch01-04.md`
- `.zcode/character-refactor-01-04/implementation-report.md`
- `.zcode/character-refactor-01-04/correction-01-report.md`
- `.zcode/character-refactor-01-04/spelling-alignment-report.md`
- `.zcode/character-refactor-01-04/human-signoff-packet.md`
- `.zcode/character-refactor-01-04/gpt-review-01.md`
- `.zcode/character-refactor-01-04/gpt-review-02.md`
- `.zcode/character-refactor-01-04/gpt-review-03.md`
- `book/narrative-continuity.md`

Inspect the live English and Persian story sections and closing hooks of
Chapters 01–04. Inspect only surrounding text needed to verify a story fact,
causal transition, or hook. Do not repeat a complete technical-chapter review.
Inspect the changed validator and focused tests to verify the spelling scope.

The human approved deliberate creative role and chronology adaptations for
this batch. Treat the owner decisions recorded below as binding; do not reject
them for differing from the unadapted mythic chronology. Do check that records
label project fiction honestly and do not present it as a *Shahnameh* event.

## 2. Owner-approved cast and chronology

Use the signoff packet and behavior sheet as the written record of these
choices. Check that the live tales preserve their functions and the
engineering lesson:

- Chapter 01: Shahrasp as First Scribe; Akvan Div as Keeper of Scripts;
  Simurgh as messenger; Black Div as Literal Div; Chapar as courier;
  Garshasp as the named former captain; Arash as present/northern captain and
  Gatekeeper; Div-e Sefid as Mirror Div in the hook.
- Chapter 02: Jamshid is the eastern governor who smiles; Budhasaf is the
  western governor who accuses; Div-e Sefid is the Mirror Div; Shahrasp is the
  First Scribe; Soroush is the Archivist.
- Chapter 03: Arzhang Div advises the council; Jamshid owns the cost ceiling;
  Arash owns the supply-cart requirement; Nariman is the flood-affected
  stakeholder whose fields lost access; Keyumars is the living builder;
  Shahrasp records the requirements; Soroush appears in the hook.
- Chapter 04: Black Div processes the archive request; Soroush is Archivist;
  Jamshid is the former-governor author of the old irrigation letter; Keyumars
  is the king awaited by that letter; Arash owns the sluice action boundary;
  Akvan Div proposes red ink; Shahrasp helps reconstruct the decision table;
  Sam is the orchard keeper.

The chronology is explicit: Keyumars is alive as builder in Chapter 03;
Chapter 04 takes place six years after Keyumars's death. He is Tahmures's
grandfather and is the deceased king in the Chapter 04 lesson. Jamshid's
Chapter 04 life status is unspecified: the text must not imply he is alive or
dead. Jamshid remains the author of the expired letter. Do not conflate these
two roles.

## 3. Review questions

Check whether:

1. Every changed name is the owner-approved mapping, with no role silently
   reassigned or extra named character added.
2. Character actions still carry the same technical causal roles: who supplies
   evidence, who defines requirements, who executes consequential action, who
   preserves records, and who makes the model's mistake.
3. The four tales remain coherent as a cumulative Tahmures narrative, rather
   than four disconnected cast substitutions. Shahrasp, Soroush, Akvan Div,
   Arash, and the other recurring roles remain distinguishable where the
   lesson requires it.
4. Human-approved creative chronology is recorded as project fiction where
   relevant. Do not upgrade Tier-B or Tier-C material to Shahnameh fact.
5. Chapter 04's expired-letter causality remains clear: the letter's awaited
   king is the deceased Keyumars, while Jamshid is its former-governor author
   and has no asserted death status.
6. Persian Chapter 03's Nariman sentence faithfully expresses that the flood
   blocked access to his fields without adding a market destination. A
   separate scene-level market mention is valid if the English scene contains
   it.
7. Persian prose is natural enough and faithful in the changed story passages;
   do not demand literal English sentence architecture.
8. Persian Chapters 01–04 use `طهمورث` in prose and headings. The validator
   requires `## روایت طهمورث` only for Chapters 01–04 and continues to require
   `## روایت تهمورث` for Chapters 05–24. The glossary and later chapters were
   intentionally left unchanged; do not treat this scoped choice as a global
   glossary promotion.
9. Character tooltips accurately describe behavior without claiming that a
   character literally implements software. Account for the documented
   English site-wide tooltip effect and the Persian tooltip collisions/omissions.
10. The signoff packet reflects live text, distinguishes resolved corrections
    from owner preferences, and does not ask the human to re-decide Keyumars's
    death or Jamshid's unspecified status.
11. No human approval, `human_reviewed` state, or current revision date was
    machine-assigned.

Do not reopen findings that GPT explicitly closed unless your live inspection
shows a concrete contradiction. Do not propose broad rewrites or aesthetic
changes. Classify any concern as BLOCKER, NONBLOCKING, or OWNER_DECISION.
Human preference questions belong in the signoff packet; a machine-solvable
source or parity defect does not.

## 4. Validation and hash boundary

The repository has known stale `source_sha256` values because the English
character refactor is awaiting acceptance and human signoff. Do not refresh
them. The current known gate result is 789 passed and 8 stale-hash failures;
do not call it green. The focused spelling-heading tests and strict English
and Persian builds have passed according to the GLM report and GPT recheck.

You may rerun narrow read-only checks if useful, but do not repeat broad
mechanical work solely for its own sake. If running translation validation,
report the stale-hash stop accurately. Distinguish verified test evidence from
visual or language judgments.

## 5. Output

Write only:

`.zcode/character-refactor-01-04/claude-final-review-01.md`

Include:

- verdict and scope;
- passages actually inspected;
- cast/chronology and engineering-role assessment;
- EN/FA parity and Persian naturalness findings;
- spelling-validator boundary;
- continuity, tooltip, and signoff-packet accuracy;
- blockers, nonblocking observations, and genuine human choices;
- validation/hash limitations;
- whether the batch is ready to present to the human for signoff.

Do not claim human approval. Finish with exactly one token:

`CLAUDE_CH01_04_CHARACTER_NARRATIVE_ACCEPTED`

`CLAUDE_CH01_04_CHARACTER_NARRATIVE_REVISION_REQUIRED`

`CLAUDE_CH01_04_CHARACTER_NARRATIVE_OWNER_DECISION_REQUIRED`
