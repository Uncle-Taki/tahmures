# GLM execution prompt — CH01_04_PERSIAN_TAHMURES_SPELLING_ALIGNMENT

MODE = IMPLEMENT_AND_VERIFY_BOUNDED_CORRECTION

PHASE = CH01_04_PERSIAN_TAHMURES_SPELLING_ALIGNMENT

ENTRY:

`CH01_04_CHARACTER_NARRATIVE_CORRECTION_01` has passed GPT's narrow closure
check for its two prior blockers. Read
`.zcode/character-refactor-01-04/gpt-review-02.md` and
`.zcode/character-refactor-01-04/correction-01-report.md` for evidence and
boundaries.

The owner has now explicitly requested that Persian Chapters 01–04 use
`طهمورث` everywhere, replacing `تهمورث`. This authorizes the scoped spelling
change, including the four tale headings. GLM executes; GPT rechecks; Claude
reviews independently after GPT; the human retains final approval.

Do NOT commit. Do NOT mark human review complete. Do NOT update source hashes
or review metadata.

## 1. Load live context

Read the live relevant skills in `.agents/skills/`, especially
`mehdi-context`, `mehdi-bilingual`, `mehdi-review`, `mehdi-director`,
`tahmures-editorial`, and `tahmures-narrative`. The owner's new instruction
overrides the older note that retro-editing approved chapters was not yet
authorized, but only for the bounded Chapter 01–04 Persian spelling change in
this prompt.

Inspect the current state of the files listed below before editing. Preserve
all unrelated working-tree changes.

## 2. Authorized scope

Edit only the following:

- `book/fa/part-1/01-what-is-a-prompt.md`
- `book/fa/part-1/02-models-meaning-and-uncertainty.md`
- `book/fa/part-1/03-requirements-before-wording.md`
- `book/fa/part-1/04-anatomy-of-a-reliable-prompt.md`
- `scripts/validate_translations.py`
- `examples/python/tests/test_translation_validator.py`
- `.agents/tahmures_character_behaviors_ch01-04.md`
- `.zcode/character-refactor-01-04/human-signoff-packet.md`
- `.zcode/character-refactor-01-04/correction-01-report.md` only to append a
  dated audit note; preserve the original report text.
- `.zcode/character-refactor-01-04/gpt-review-02.md` only if a factual report
  correction is needed.
- `book/narrative-continuity.md` only to add a concise correction/change-log
  entry documenting this scoped spelling alignment.
- `.agents/skills/tahmures-narrative/references/story-world.md` only to update
  its spelling guidance with the new scoped authorization and its boundary.

Do not change English manuscript files, Chapters 05–24, other Persian chapters,
the canonical glossary `book/fa/translation-glossary.md`, media, code outside
the listed validator/test, or any unrelated files. Do not change the actual
Persian tale prose beyond correcting any remaining `تهمورث` occurrence in
these four chapter files. Current search suggests only the four headings
remain.

Do not change `source_sha256`, `last_reviewed`, `last_translated`,
`translation_status`, `editorial/review-status.yml`, or any human-review state.
Persian-only edits do not change the English source hash. The existing hashes
are already stale because the English refactor awaits acceptance; leave them
as-is until the separate post-signoff metadata phase.

## 3. Required spelling result

In Persian Chapters 01–04, every occurrence of the protagonist's name must be
`طهمورث`. This includes these headings:

- `## روایت طهمورث` in Chapters 01, 02, 03, and 04.

Search each full file for both `تهمورث` and `طهمورث`. Confirm no old spelling
remains in the four chapter files. Do not mechanically change unrelated
names, quotations, historical records, code, URLs, or other tokens.

Keep the user-authorized scope explicit: Chapters 05–24 continue to use their
current `تهمورث` spelling, and the canonical translation glossary remains
unchanged in this pass. Do not present this scoped editorial decision as a
book-wide glossary promotion.

## 4. Make the heading validator chapter-aware

`validate_translations.py` currently pins `## روایت تهمورث` in a shared
heading list for all Persian chapters. Update the validator so it requires:

- Chapters 01–04: `## روایت طهمورث`
- Chapters 05–24: `## روایت تهمورث`

Preserve heading order and every other chapter heading rule. Do not make the
new spelling global, because later Persian chapters are outside the authorized
scope. Keep final-chapter closing-heading behavior intact.

Update `examples/python/tests/test_translation_validator.py` with focused
regression coverage proving both sides of the boundary: the new heading is
accepted in Chapters 01–04, and the existing heading remains accepted in a
later chapter. Also prove the wrong variant is rejected on each side if the
existing test architecture supports that cleanly. If you need a helper for
expected headings, keep it small and specific to this contract.

Because current Persian source hashes are intentionally stale, test heading
behavior using temporary copies whose temporary front matter has the
calculated source hash. Never write that temporary hash into a repository
chapter. Report the pre-existing/still-expected stale-hash failure separately.

## 5. Keep records truthful

Update the character behavior sheet and signoff packet so they no longer call
the four headings unresolved. Record the owner-authorized scoped spelling
decision accurately:

- Chapters 01–04 Persian tale headings and prose use `طهمورث`.
- Chapters 05–24 and the translation glossary remain `تهمورث` pending a
  separate book-wide terminology decision.
- This correction does not promote a global glossary term or imply renewed
  human approval.

Update the Chapter 01–04 coverage table to show live Persian spelling
`طهمورث` for the protagonist. Keep historical “before” wording in the signoff
ledger where it is needed to explain the change; label it as prior wording,
not current text. Remove the obsolete question asking whether the heading
should remain `روایت تهمورث`.

Update the project-specific narrative skill's spelling note to reflect this
new scoped owner authorization while preserving the boundary above. Do not
change generic bilingual or human-review policy.

Add a brief dated continuity/change-log entry documenting the spelling-only
FA Chapter 01–04 alignment. Do not alter character chronology, roles, plot, or
the accepted Jamshid/Keyumars decisions.

Append an audit note to `correction-01-report.md` if needed so it records this
later scoped spelling correction without rewriting the earlier report's
historical observations.

## 6. Explicitly preserve narrative decisions

The Chapter 04 dead king is already Keyumars:

- Chapter 03: Keyumars is alive as the builder.
- Chapter 04: six years have passed since his death; the letter identifies
  him as the king it awaited.
- Jamshid remains the former-governor author of the letter, with his life
  status in Chapter 04 unspecified.

Do not rename Jamshid as Keyumars or change any of these narrative facts in
this spelling-only pass.

## 7. Validation

Run and report:

- `git diff --check`
- `scripts/validate_chapters.py`
- `scripts/validate_continuity.py`
- `scripts/check_parity.py`
- focused `examples/python/tests/test_translation_validator.py` tests for the
  chapter-aware heading rule
- `scripts/editorial_check.py --chapters 01 --chapters 02 --chapters 03 --chapters 04`
- strict English and Persian builds if the live editorial workflow requires
  them for the changed validator/site text
- `make check PYTHON=.venv/bin/python`, reporting exact results without
  claiming green if it stops on the already-known stale `source_sha256`
  failures.

Do not refresh source hashes to make validation green. Do not change source
files or validators to hide unrelated existing failures.

Self-review questions:

- `FA_CH01_04_ONLY_USES_طهمورث?`
- `CH05_24_HEADING_CONTRACT_UNCHANGED?`
- `VALIDATOR_ACCEPTS_SCOPED_VARIANTS_AND_REJECTS_WRONG_VARIANT?`
- `NO_ENGLISH_OR_NARRATIVE_CHANGE?`
- `GLOSSARY_AND_REVIEW_METADATA_UNCHANGED?`
- `JAMSHID_AND_KEYUMARS_ROLES_UNCHANGED?`
- `SIGNOFF_PACKET_AND_SKILL_GUIDANCE_MATCH_SCOPE?`

## 8. Deliverable and final token

Write `.zcode/character-refactor-01-04/spelling-alignment-report.md` with the
exact files changed, before/after heading text, validator design and tests,
scope checks, remaining glossary boundary, human-review status, and validation
results. Do not mark the review complete or claim human approval.

Finish with exactly one token:

`CH01_04_PERSIAN_TAHMURES_SPELLING_ALIGNMENT_READY_FOR_GPT`

`CH01_04_PERSIAN_TAHMURES_SPELLING_ALIGNMENT_REVISION_REQUIRED`

`CH01_04_PERSIAN_TAHMURES_SPELLING_ALIGNMENT_VALIDATION_BLOCKED`
