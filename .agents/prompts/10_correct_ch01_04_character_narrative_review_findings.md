# GLM bounded correction — Chapter 01–04 character-narrative refactor

MODE = IMPLEMENT_AND_VERIFY_BOUNDED_CORRECTIONS

PHASE = `CH01_04_CHARACTER_NARRATIVE_CORRECTION_01`

ROLE: GLM is the implementation agent. GPT will verify only the findings
listed here. Claude remains the independent final checker after GPT accepts;
the human retains final review authority.

## Entry evidence and authority

Read the current live skills as needed: `/mehdi-context`, `/mehdi-bilingual`,
`/mehdi-narrative`, `/mehdi-review`, `/tahmures-narrative`, and
`/tahmures-editorial`. User decisions and `book/narrative-continuity.md` take
precedence over stale generic skill defaults for this explicitly approved
Chapter 01–04 mapping.

Read:

- `.agents/prompts/09_refactor_ch01_04_character_narrations.md`;
- `.agents/tahmures_character_reference_gpt_review_ch01-04.md`;
- `.agents/tahmures_character_behaviors_ch01-04.md`;
- `.agents/tahmures_character_visual_prompts_ch01-04.md`;
- `.zcode/character-refactor-01-04/gpt-review-01.md`;
- `.zcode/character-refactor-01-04/implementation-report.md`;
- `.zcode/character-refactor-01-04/human-signoff-packet.md`;
- the exact current English/Persian Chapter 03 and 04 tale passages;
- the Chapter 03–04 entries and change log in `book/narrative-continuity.md`;
- `includes/en-character-abbreviations.md` and the appended relevant entries
  in `includes/fa-abbreviations.md`.

Do not revert accepted character mappings or redo the four-chapter refactor.
The bounded changes below are the only manuscript changes authorized.

## Scope

Authorized files for this correction:

- English Chapter 03 and Chapter 04 tale passages only;
- Persian Chapter 03 and Chapter 04 tale passages only;
- `book/narrative-continuity.md` only where Jamshid's Chapter 04 status is
  stated;
- `.agents/tahmures_character_behaviors_ch01-04.md` and
  `.agents/tahmures_character_visual_prompts_ch01-04.md` only where Jamshid's
  Chapter 04 death/status is stated;
- English and Persian tooltip definitions for Jamshid;
- `.zcode/character-refactor-01-04/human-signoff-packet.md`;
- append a dated correction note to
  `.zcode/character-refactor-01-04/implementation-report.md`;
- `.zcode/character-refactor-01-04/correction-01-report.md`.

Do not edit Chapters 01–02, technical sections, exercises, citations, quoted
artefacts, source hashes, review status, glossary, MkDocs configuration,
skills, approved media, code, experiments, or any unrelated file. Do not
commit.

## Correction A — Jamshid's status in Chapter 04

The owner explicitly clarified after the previous GLM report:

> Leave Jamshid's alive/death status unspecified.

Keep the already approved mapping: Jamshid is the Chapter 02 eastern governor,
the Chapter 03 treasurer, and the Chapter 04 former-governor letter's author.
Do not say or imply that he is alive or dead in Chapter 04. This clarification
supersedes the previous draft's `late Jamshid` wording and all machine-authored
claims that the owner had approved his death.

Make the smallest faithful repairs:

- English Chapter 04: change “a letter from the late Jamshid, a former
  governor” to “a letter from Jamshid, a former governor”. Remove any other
  explicit death-status word applied to Jamshid.
- Persian Chapter 04: identify the author as Jamshid, a former governor, and
  remove `درگذشته` wherever it modifies Jamshid.
- Keep “The king it waited for was Keyumars” and the Chapter 04 opening that
  places the scene six years after Keyumars's death. Do not confuse the king
  awaited in the letter with the letter's author.
- Keep the letter's old/expired instruction and the technical point that
  retaining an old record does not give it current authority.
- The original generic wording called the letter author's governor dead. The
  owner's latest instruction controls for this mapped character: replace that
  status wording with the neutral former-governor/letter wording above. Do not
  create a second, anonymous author for the same letter. Keep the record old
  and expired, without stating whether Jamshid is alive or dead.
- In `book/narrative-continuity.md`, the behavior sheet, the relevant tooltip,
  signoff packet, and any current report summary, state only the approved
  Chapter 02–03 roles and Chapter 04 letter authorship. Record that Jamshid's
  life status at Chapter 04 is unspecified. Remove statements that say he is
  late/dead or that this was an owner-approved decision.
- Preserve the initial implementation report as an audit record; append a
  correction note explaining that its earlier death claim was superseded by
  the owner's clarification. Correct the current human signoff packet so it
  asks no question about Jamshid's life status.

Do not remove Keyumars's explicitly owner-approved chronology: Keyumars is
alive as the Chapter 03 builder, and Chapter 04 is six years after his death.

## Correction B — Persian Nariman sentence

In Persian Chapter 03, the current wording says the flood cut Nariman's fields
off “from the market” (`از بازار`). English says only that the flood cut off
his fields and does not mention a market. Remove this unsupported detail while
keeping natural Persian and the same stakeholder requirement. A suitable
minimal direction is to express that the flood blocked access to his fields,
for example:

`نریمان، که سیلاب راه دسترسی به کشتزارهایش را بسته بود، پایداری در جریان بهاری را می‌خواست.`

You may make a small grammatical improvement, but do not add a destination,
occupation, or new engineering requirement.

## Signoff packet and tooltip scope disclosure

Update the packet's C03-4 entry to show the corrected Persian and its
source-faithful reason. Update C04-3/C04-10 and the owner-choice summary so
they no longer call Jamshid late/deceased or claim that his death was owner
approved.

The English `pymdownx.snippets` include is auto-appended site-wide. Exact
`Tahmures` occurrences in later chapters therefore receive the new Tahmures
tooltip even though their manuscript source is untouched. Disclose this effect
in the human signoff packet as an optional scope preference. Do not edit later
chapters or change MkDocs architecture in this bounded correction.

## Preserve approved work

Keep the owner-confirmed decisions exactly:

```text
CH02_GOVERNOR_ASSIGNMENT = JAMSHID_EAST_BUDHASAF_WEST
CH03_CH04_KEYUMARS_TIMELINE = LIVE_BUILDER_WITH_CH04_SIX_YEARS_AFTER_HIS_DEATH
JAMSHID_CH04_LIFE_STATUS = UNSPECIFIED
```

Keep the character mapping, approved narrative functions, all previously
accepted English/Persian lines, and the separate project-fiction/source-tier
distinctions. Do not edit skill files in this correction. After human signoff,
the stale Tahmures narrative skill guidance can be reconciled as a separate
knowledge-maintenance phase.

## Validation and self-review

Run `git diff --check`, chapter validation, continuity validation, experiment
parity, the four-chapter reference/protected/Persian editorial checks, and
strict English/Persian builds. Run translation validation and `make check`
and report the exact current stale-`source_sha256` failures; do not refresh the
four Persian hashes before GPT acceptance and subsequent human signoff. Do not
claim the full gate is green if hash-related failures stop it.

Verify specifically:

- `CH04_JAMSHID_STATUS_UNSPECIFIED?`
- `NO_LATE_OR_DECEASED_CLAIM_ABOUT_JAMSHID?`
- `KEYUMARS_SIX_YEAR_TIMELINE_PRESERVED?`
- `CH03_FA_NARIMAN_NO_UNSUPPORTED_MARKET?`
- `CH03_NARIMAN_REQUIREMENT_AND_EN_FA_MEANING_PRESERVED?`
- `SIGNOFF_PACKET_MATCHES_LIVE_TEXT_AND_OWNER_DECISIONS?`
- `CONTINUITY_AND_CHARACTER_SHEETS_MATCH_CURRENT_TEXT?`
- `NO_SOURCE_HASH_OR_REVIEW_STATUS_CHANGE?`

Report changed files, exact before/after lines, validation results, remaining
human choices, and what GPT should inspect. Do not mark human review complete.

Finish with exactly one token:

`CH01_04_CHARACTER_NARRATIVE_CORRECTION_READY_FOR_GPT`

`CH01_04_CHARACTER_NARRATIVE_CORRECTION_REVISION_REQUIRED`

`CH01_04_CHARACTER_NARRATIVE_CORRECTION_VALIDATION_BLOCKED`
