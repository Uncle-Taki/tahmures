# GLM execution prompt — Chapter 01–04 character-narration refactor

MODE = IMPLEMENT_AND_VERIFY

PHASE = CH01_04_CHARACTER_NARRATIVE_REFACTOR

## Roles and approval boundary

GLM performs the bounded reference corrections and narrative implementation.
GPT independently reviews the resulting English/Persian passages and the
continuity update. The human retains final authority over narrative taste,
Persian naturalness, character presentation, and signoff.

The user approved the Chapter 01–04 cast mapping listed below, including the
explicit creative role and chronology adaptations. This authorizes original
project fiction; it does not authorize presenting those chapter roles as
historical or *Shahnameh* events.

Do not commit, publish, generate images, call a provider, mark human review
complete, or modify material outside the listed scope. Do not rewrite technical
sections, examples, code, experiments, citations, or chapter structures.

## 1. Required context and source order

Read `AGENTS.md`, `book/project-charter.md`, `meta-prompt.md`, and
`book/narrative-continuity.md`. Load the live skills under `.agents/skills/`:

- /mehdi-director
- /mehdi-context
- /mehdi-author
- /mehdi-narrative
- /tahmures-narrative
- /mehdi-bilingual
- /mehdi-human-review
- /mehdi-review
- /tahmures-editorial

Read the approved mapping and proposed behavior/tooltips in:

- `.agents/tahmures_character_behaviors_ch01-04.md`
- `.agents/tahmures_character_visual_prompts_ch01-04.md`
- `.agents/tahmures_characters.md`
- `.agents/tahmures_characters_part2.md`

Read the complete English and Persian tale sections and closing hooks for:

- `book/part-1/01-what-is-a-prompt.md`
- `book/fa/part-1/01-what-is-a-prompt.md`
- `book/part-1/02-models-meaning-and-uncertainty.md`
- `book/fa/part-1/02-models-meaning-and-uncertainty.md`
- `book/part-1/03-requirements-before-wording.md`
- `book/fa/part-1/03-requirements-before-wording.md`
- `book/part-1/04-anatomy-of-a-reliable-prompt.md`
- `book/fa/part-1/04-anatomy-of-a-reliable-prompt.md`

English story meaning and the explicit engineering lesson are canonical for the
Persian translation. The human-approved mapping controls the new project-fiction
names. Project rules and continuity control protected structure and series
consistency. Existing human review applies only to the old revision; these edits
must return for renewed GPT and human review.

## 2. Owner decisions — resolved and locked for this batch

The owner has explicitly confirmed both story choices below. Treat them as
fixed inputs; do not reopen them or substitute alternatives during execution.

```text
CH02_GOVERNOR_ASSIGNMENT = JAMSHID_EAST_BUDHASAF_WEST

CH03_CH04_KEYUMARS_TIMELINE = LIVE_BUILDER_WITH_CH04_SIX_YEARS_AFTER_HIS_DEATH
```

Jamshid is the eastern governor who smiles; Budhasaf is the western governor
who accuses the Mirror Div. Keep Keyumars alive as the Chapter 03 builder, then
establish in the Chapter 04 opening that six years have passed since his death.
Jamshid is the Chapter 03 treasurer and is dead by Chapter 04; keep his Chapter
04 letter explicitly historical. Do not invent a cause or exact date for
either death.

## 3. Bounded reference-pack corrections

Before using the character sheets, correct only these recorded defects:

1. In the behavior file and roster, include Div-e Sefid in Chapter 01 because
   the Chapter 01 closing hook names the Mirror Div. Include Soroush in Chapter
   03 because that chapter's closing hook names the Archivist.
2. Update the corresponding chapter tags in the visual-prompt file.
3. Correct Shahrasp's “exact appearances” list: he appears in the four tale
   sections, but not in the Chapter 01 or Chapter 02 closing hooks.
4. Remove “Hushang's generation” from Garshasp's project-fiction description.
   The Chapter 01 text leaves the father unnamed. Preserve Hushang only in the
   explicitly canonical source-genealogy note; do not silently name the father
   Keyumars.
5. Correct the Persian hover copy, keeping it natural and semantically paired:
   - Shahrasp: replace `دیدنی نگه می‌دارد` with natural wording such as
     `روشن و در دسترس نگه می‌دارد`.
   - Arash, Chapter 01: fix the malformed `رسیدی پیام‌رسان` phrase to a natural
     equivalent of “receives the messenger's delivery.”
   - Soroush, Chapter 04: replace unclear `واقعیت بدهند` with a natural
     equivalent of “which records may supply information/facts”; do not imply
     that records guarantee truth or authority.
   - Budhasaf: remove “مورد تأیید مالک” and any other workflow metadata from
     reader-facing tooltip text. Keep the approval/source caveat in the profile.
6. Describe Nariman's project role as the flood-affected council member or
   stakeholder, not as a separate river-keeping occupation. Preserve his
   requirement that the crossing survive the spring current.
7. In the visual-prompt file, state evidence honestly: GLM checked file identity,
   dimensions, and palette programmatically; it did not visually inspect the
   PNG. Record that GPT visually confirmed the listed visible Tahmures traits
   during the supervisory review. Do not attribute that visual inspection to GLM.

Do not otherwise expand the character sheets, redesign the visual prompts,
research new biography, or change source-tier decisions. Keep the two files
marked as draft adaptation references pending human approval.

## 4. Approved adaptation map

Use these exact English display names. Pair each with its original story
function on first mention so the reader understands the role; after that, use
the personal name naturally. The former role is a project-fiction function, not
a source-tradition claim.

| Live role in Chapters 01–04 | Approved adaptation |
|---|---|
| protagonist | Tahmures |
| First Scribe | Shahrasp |
| Keeper of Scripts | Akvan Div |
| Literal Div | Black Div |
| Mirror Div | Div-e Sefid |
| Council's Div | Arzhang Div |
| Archivist | Soroush |
| Messenger in Chapter 01 | Simurgh |
| courier bringing the tablet | Chapar / `چاپار`, an occupational role, not a proper name |
| captain associated with Tahmures's father | Garshasp |
| present/northern captain and Gatekeeper | Arash |
| two Chapter 02 governors | Jamshid and Budhasaf, using the operator-selected assignment in §2 |
| Treasurer in Chapter 03 | Jamshid |
| builder in Chapter 03 and deceased king in Chapter 04 | Keyumars, using the operator-selected chronology in §2 |
| flood-affected council member in Chapter 03 | Nariman |
| orchard-affected person in Chapter 04 | Sam |

Do not give a name to crowds, witnesses, villagers, bridge makers, farmers, the
watch, apprentice, cities, or other collectives. Keep the Chapter 01 father
unnamed. Use `طهمورث` for new Persian narrative work. Use the proposed Persian
forms in the behavior sheet for the other names, including `شهراسپ` for
Shahrasp, but leave them as batch-level draft forms: do not promote them into
`book/fa/translation-glossary.md` in this phase. The final signoff packet must
list these proposed forms for human confirmation.

Keep source identity and project role distinct. In particular:

- Shahrasp is a source-tradition counselor; his First Scribe function is this
  book's approved adaptation.
- Akvan Div, Div-e Sefid, and Arzhang Div are later-cycle source figures; their
  court jobs in these tales are project fiction.
- Black Div's personal name/identity is an adaptation of an unnamed source
  figure.
- Simurgh's bird identity may inform the project-fiction messenger presentation;
  the role in Tahmures's hall is not a source event.
- Soroush, Arash, Garshasp, Jamshid, Keyumars, Nariman, and Sam must not be
  presented as performing these story occupations in their source traditions.
- Budhasaf remains an approved project-fiction governor with unverified source
  identity; do not merge him with Shahrasp or the scholarly Būdasb hypothesis.

Keep current English pronouns for this batch as adaptation choices: Akvan Div
and Soroush remain she/her as in the existing prose; Shahrasp, Arash, Simurgh,
and the other currently gendered roles retain their current English pronouns.
Do not assert that these project presentations are source-canonical. Persian
must remain natural and need not introduce gender where it is not grammatical.

## 5. Manuscript scope and narrative requirements

Authorized story edits are only the tale sections and their closing hooks in
the eight Chapter 01–04 English/Persian files listed in §1. Do not edit the
chapters' technical prose, exercises, citations, front matter, or adjacent
chapters. Also update `book/narrative-continuity.md` for the changed recurring
names, roles, chronology, and any new transition.

Preserve the existing causal teaching beats and engineering meanings:

- Ch01: ambiguity between intended meaning and written instruction; the
  literal response follows surface wording; the mistaken delivery creates
  consequences; Tahmures learns to label speaker, recipient, occasion, and
  requested result.
- Ch02: Div-e Sefid's fluent completion exceeds available evidence; the failure
  is not explained as malice; written, inferred, and unknown remain distinct;
  abstention is useful.
- Ch03: requirements precede wording; both stone and arch exceed the cost
  ceiling; stakeholders own criteria; Arzhang Div does not invent what “best”
  means.
- Ch04: archive data is not current instruction; formatting does not create
  enforceable authority; the application/Gatekeeper owns consequential action;
  irrelevant material increases exposure; preserve the source's minimisation
  and authority claims.

Do not broaden or modernize the ancient-world tale with engineering jargon.
Keep each chapter's tale within the project's required narrative length and
preserve the explicit bridge to engineering. Do not force every character to
appear in every chapter. Use a character only where the mapping table assigns a
role or where an existing hook already names that role.

Apply the names in the closing hooks too: Chapter 01's treaty hook names Akvan
Div/Keeper of Scripts and Div-e Sefid/Mirror Div; Chapter 03's old-letter hook
names Soroush/Archivist. Keep Chapter 04's Gatekeeper hook coherent with Arash.
Do not leave an obsolete role-only reference in a hook after its mapped name is
introduced.

## 6. Hover descriptions

The owner wants concise engineering-behavior notes available by hovering over
character names, similar to term explanations. Use the corrected behavior sheet
as the source of tooltip wording. Keep each note concise, useful, and free of
workflow metadata such as “approved by the owner.” Preserve the sheet's complete
plain-text descriptions for readers who do not use hover.

Persian already has `abbr` and `includes/fa-abbreviations.md`. English currently
does not. Add the smallest reversible support needed for both editions:

- add the `abbr` Markdown extension to `mkdocs.yml` and a dedicated
  `includes/en-character-abbreviations.md` include;
- keep the existing Persian extension and add character-name definitions to
  `includes/fa-abbreviations.md`;
- define only names used in this four-chapter batch; each note must match the
  behavior sheet and preserve EN/FA meaning;
- do not place prose explanations inside protected identifiers, code fences, or
  unrelated glossary terms;
- do not alter site JavaScript, theme, or unrelated abbreviations.

Use the supported abbreviation syntax after the character's first clear
introduction in the narrative. Check that the title text renders in both builds
and that each story remains understandable when the hover is unavailable. Do
not claim hover operation on devices/browsers unless the generated site was
inspected.

## 7. Bilingual integrity and review status

Revise English narrative first, then translate the changed story into Persian
using natural Persian syntax rather than matching English sentence structure.
Preserve all facts, agency, certainty, causality, and role distinctions. Use the
approved name forms consistently and check ezafe, pronouns, agreement, and
mixed-script display. Do not mechanically translate source-identity notes into
the story.

Do not modify `editorial/review-status.yml`, set `human_reviewed: true`, or
update final review dates. The current Persian `source_sha256` values refer to
the previous English revision. Do not refresh them while GLM's English remains
unaccepted; report the expected hash-staleness check honestly. GPT must accept
the revised English first. A separate, later metadata reconciliation updates
the source hashes and review truth, and only explicit human signoff may mark the
current Persian revision human-reviewed.

Prepare a compact signoff packet so the human can review this bounded batch
without rereading four chapters. For each changed passage include a note ID,
old wording/role, new wording/name, source/engineering meaning, and disposition.
List proposed Persian spellings, any unresolved presentation choice, the new
timeline transition, and the tooltip behavior as human-signoff items.

## 8. Required outputs

Update only the two reference files in §3, the eight scoped chapter files, and
`book/narrative-continuity.md`, plus the minimal Markdown/abbreviation files
named in §6. Write implementation evidence to:

- `.zcode/character-refactor-01-04/implementation-report.md`
- `.zcode/character-refactor-01-04/human-signoff-packet.md`

The report must state the owner choices received, files changed, narrative
word counts, source/fiction boundary, continuity changes, tooltip implementation
and rendering evidence, source-hash state, review-state preservation, and all
validation results. Do not claim human signoff.

## 9. Validation

Run the project-required checks with the repository environment:

```bash
rtk proxy git diff --check
rtk proxy .venv/bin/python scripts/validate_translations.py
rtk proxy .venv/bin/python scripts/editorial_check.py --chapters 01 --chapters 02 --chapters 03 --chapters 04
rtk proxy make check PYTHON=.venv/bin/python
```

Do not change validators to obtain a pass. If translation validation reports
only the expected stale source hashes, report those exact failures and do not
update hashes prematurely. Run strict English and Persian builds and visually
inspect the rendered tale hooks and character tooltips, especially Persian RTL.
Report each actual result; do not label a check green if it was not run.

## 10. Final self-review

Before returning, verify:

- all approved character names appear in the correct mapped story roles;
- Chapter 01 and Chapter 03 closing-hook coverage is corrected in both the
  reference files and manuscripts;
- both owner-confirmed decisions in §2 were followed exactly;
- no source tradition was rewritten to match project fiction;
- source-tier claims remain outside the tale unless the source itself supports
  them;
- Tahmures remains fallible and learns cumulatively;
- technical causality and failure owners are unchanged;
- EN/FA story meaning and tooltip notes match;
- no unrelated chapter or status/hash metadata changed.

Finish with exactly one token:

`CH01_04_CHARACTER_NARRATIVE_REFACTOR_READY_FOR_GPT`

`CH01_04_CHARACTER_NARRATIVE_REFACTOR_REVISION_REQUIRED`

`CH01_04_CHARACTER_NARRATIVE_REFACTOR_OWNER_DECISION_REQUIRED`

`CH01_04_CHARACTER_NARRATIVE_REFACTOR_VALIDATION_BLOCKED`
