# GLM execution prompt — Chapter 01–04 character reference pack

MODE = IMPLEMENT_AND_VERIFY

PHASE = CH01_04_CHARACTER_REFERENCE_PACK

ROLE:

GLM prepares two character-reference files. GPT performs the next independent
review. The human has approved the mappings and name substitutions below, but
has not approved the resulting behavior sheets, visual prompts, generated art,
or rewritten chapter text.

Do not edit English or Persian manuscripts. Do not edit
`book/narrative-continuity.md`, review metadata, glossary, skills, approved
media, code, or experiments. Do not commit, publish, or mark human review
complete. Do not create the chapter-rewrite prompt in this phase.

## 1. Load live context and skills

Read `AGENTS.md`, `book/project-charter.md`, `book/narrative-continuity.md`,
`meta-prompt.md`, and the current English and Persian tale sections of Chapters
01–04. Read both supplied character references:

- `.agents/tahmures_characters.md`
- `.agents/tahmures_characters_part2.md`

Use the live skills under `.agents/skills/`:

- /mehdi-context
- /mehdi-director
- /mehdi-narrative
- /tahmures-narrative
- /mehdi-author
- /mehdi-bilingual
- /mehdi-review
- /tahmures-editorial

The user explicitly approved role and chronology adaptation for this four-
chapter batch. Follow the approved mappings below. The skills’ source-tier and
continuity rules still apply to how the adaptations are described: do not
present a fictional chapter role or event as a fact from Ferdowsi or another
source tradition.

## 2. Exact outputs

Create exactly these two files:

`.agents/tahmures_character_behaviors_ch01-04.md`

`.agents/tahmures_character_visual_prompts_ch01-04.md`

If either output file already exists, stop without overwriting either one and
report the existing path. Do not modify the supplied dossiers. Treat both new
files as **proposed adaptation references pending GPT review**, not as
competing canonical continuity or final visual-art approvals.
`book/narrative-continuity.md` remains the current continuity source until a
later approved manuscript-revision phase updates it.

## 3. Approved cast mapping

Use this mapping as an owner-approved decision. Preserve the distinction
between the mythic source identity and the character’s new project-fiction
role. “Chapter role” below describes this book’s adaptation, not a claim about
the source tradition.

| Chapter(s) | Current story role | Approved adaptation |
|---|---|---|
| 01–04 | Tahmures | Tahmures remains the continuous protagonist. Use `طهمورث` for new Persian narrative work, subject to the live glossary. |
| 01–04 | First Scribe | Shahrasp |
| 01, 04 | Keeper of Scripts | Akvan Div |
| 01, 04 | Literal Div | Black Div |
| 02 | Mirror Div | Div-e Sefid |
| 03 | Council’s Div | Arzhang Div |
| 02, 04 | Archivist | Soroush |
| 01 | Messenger | Simurgh |
| 01 | Courier who brings the tablet | Chapar / `چاپار`, an occupational role, not a mythic proper name |
| 01 | Captain associated with Tahmures’s father | Garshasp |
| 01, 03, 04 and the Chapter 01 illustrative Gatekeeper | Arash as current captain / Gatekeeper |
| 02 | Two governors with competing treaty claims | Jamshid and Budhasaf |
| 03, 04 | Treasurer / former governor who authored the old letter | Jamshid |
| 03, 04 | Builder / deceased king referred to by the old instruction | Keyumars |
| 03 | Flood-affected-person role | Nariman |
| 04 | Orchard-affected-person role | Sam |

Keep crowds and explicitly collective roles—riders, charcoal burners, villagers,
farmers, bridge makers, witnesses, and watch—as collectives unless a live tale
identifies a distinct individual. Do not invent extra names to fill out the
cast. In Chapter 01, record the courier as `Chapar` and the in-hall Messenger
as `Simurgh`; do not merge their separate story actions.

These four name substitutions were explicitly requested and approved by the
human: Fereydun → Budhasaf; Rostam → Arash; Hushang → Keyumars; Goudarz →
Garshasp. Preserve the exact approved English spellings. For Persian spelling,
follow an established project form where one exists; otherwise mark the
transliteration `GPT_REVIEW_REQUIRED` and list a proposed spelling without
silently treating it as settled.

## 4. Source tiers and adaptation record

For every named figure, record two separate classifications:

1. **Mythic source identity:** use `TIER_A_SHAHNAMEH_EXPLICIT`,
   `TIER_B_LATER_TRADITION`, `UNVERIFIED_SOURCE_LEAD`, or
   `NOT_APPLICABLE_OCCUPATIONAL_ROLE`. Support the classification with the
   supplied dossier’s source note and the live narrative skill references.
   Do not treat the dossier alone as proof of a precise literary claim.
2. **Chapter appearance and role:** mark the four-chapter episode and assigned
   educational role as `TIER_C_PROJECT_FICTION`, except where a specific
   source event is genuinely being retold. These chapters remain original
   teaching fiction.

At minimum, explicitly record that Shahrasp is a named counselor in the
Tahmures tradition but “First Scribe” is this project’s adaptation; Akvan Div,
Div-e Sefid, Arzhang Div, Soroush, Simurgh, Garshasp, Arash, Jamshid, Keyumars,
Nariman, and Sam have source identities or cycles that must not be conflated
with their new chapter occupations; and the personal identity given to the
Black Div is an adaptation of a figure described without a personal name.
Record that Chapar is a Persian occupational name, not a mythic person.

**Budhasaf source caution:** the supplied dossier mentions `Būdasb / بوداسب`
only as one scholar’s proposed alternative form for Shahrasp’s name; it does
not establish a separate mythic governor named `Budhasaf`. Keep the human’s
approved `Budhasaf` as a distinct Chapter 02 project-fiction character and do
not merge him with Shahrasp or claim a source identity without verified
evidence. Mark that identity `UNVERIFIED_SOURCE_LEAD`; include the dossier’s
possible name collision as a GPT review note. Do not change the approved name.

The owner has approved deliberate chronology shifts for the listed cast. Record
each shift plainly, including later-cycle figures appearing in Tahmures’s
teaching stories and Jamshid/Keyumars taking the assigned administrative or
story roles. Keyumars precedes Tahmures in the dossier’s chronology; his
approved role as the builder and deceased king is project fiction. Do not
“correct” the mapping back to canonical chronology, and do not state that the
adapted events occurred in the source epic.

If a source detail cannot be verified from the supplied reference or the live
skill references, label it `UNVERIFIED_SOURCE_DETAIL`; do not fill gaps with
invented biography, powers, family relations, dialogue, or quotations.

## 5. Character-sheet format

Create one main behavior sheet per named character and a short role entry for
Chapar.
Use these fields consistently:

- approved display name in English and Persian;
- former Chapter 01–04 role/name and exact chapter appearances;
- mythic source identity, source tier, and concise source basis;
- project-fiction role and explicit chronology adaptation;
- chapter-by-chapter observable behavior and agency;
- the engineering lesson carried in each appearance;
- a short English and natural Persian hover description for each relevant
  chapter role;
- stable personality, voice, and behavioral boundaries that avoid flattening
  divs into generic villains or making heroes omniscient;
- relationship/continuity notes and unresolved items for GPT review.

The behavior must be concrete enough for a later writer to use without
reconstructing the mapping. Describe what a character does and what that action
teaches. Keep the character’s authority distinct from the engineering concept:
a record keeper does not validate truth by title; a messenger does not prove
sender or authority; an actor’s seal or label does not enforce permission; a
Div’s mistake does not make every failure a Div’s fault; a champion who voices
a requirement does not set the council’s priorities.

Use these proposed hover notes as the approved functional starting points;
GLM may make them natural and concise in Persian, but must preserve their
meaning:

- **Black Div / Literal Div:** “Follows surface wording while exposing missing
  role and authority structure.”
- **Div-e Sefid / Mirror Div:** “Can produce a fluent, plausible account that
  goes beyond the available evidence.” Do not imply the source character is
  malicious by default.
- **Arzhang Div / Chapter 03 council Div:** “Offers a candidate before the
  requirements are clear; cannot decide what ‘best’ means for the council.”
- **Akvan Div / Keeper of Scripts:** “Classifies and organizes written forms;
  a label does not make text authoritative.”
- **Shahrasp / First Scribe:** “Keeps observations, sources, and decisions
  visible so Tahmures can examine and revise his judgment.” This is the
  project role, not a source claim that Shahrasp was a scribe.
- **Soroush / Archivist:** “Preserves provenance and points back to source
  records; preservation alone does not make an old instruction current.”
- **Simurgh / Messenger:** “Carries information between people; delivery does
  not establish its intended recipient or authority.”
- **Chapar / courier:** “Carries a record; delivery alone does not determine
  its intended recipient, purpose, or authority.”
- **Nariman / Chapter 03 flood-affected person:** “Voices the need for a
  crossing that survives the spring flood; he does not set the council’s
  priorities.”
- **Sam / Chapter 04 orchard-affected person:** “Makes visible who bears the
  cost when an outdated record is acted on; his concern does not make old text
  current.”
- **Arash / captain or Gatekeeper:** “Represents the consequential actor;
  action still requires current authority supplied by the governing system.”
- **Jamshid and Budhasaf / Chapter 02 governors:** “Present competing claims;
  neither claim is established by confidence or status alone.”
- **Garshasp / captain associated with Tahmures’s father:** “A remembered
  captain from the prior court; a familiar name does not establish the source
  or authority of a command.”
- **Keyumars / Chapter 03 builder and Chapter 04 deceased king:** “An older
  figure whose plans and records remain part of the story; age or prestige
  does not make an instruction current.”
- **Budhasaf / Chapter 02 governor:** “Presents a competing claim; the name is
  an approved project-fiction choice whose separate mythic identity is
  unverified.”

For Tahmures, Keyumars, Garshasp, Jamshid, Budhasaf, Nariman, Sam, and any
other character whose role is adapted, give a chapter-specific tooltip too. Do not
invent a teaching behavior that is not present in the live passage; identify
the intended behavior as an adaptation proposal when it has not yet appeared
in text.

## 6. Bilingual and tooltip handling

Inspect the current English and Persian passages rather than translating the
old role labels mechanically. Keep English/Persian identity and chapter-function
notes semantically equivalent and natural. Use the glossary’s Persian forms;
do not silently normalize previously reviewed manuscript spellings.

The Persian site currently has abbreviation/tooltips support. Record the
proposed tooltip text as content only; do not edit MkDocs configuration,
JavaScript, glossary, or manuscript markup in this phase. Note that matching
English-site tooltip support may need a later scoped implementation decision.
Ensure the sheet’s notes remain readable as ordinary text if hover is
unavailable on touch screens.

## 7. Visual-generation prompt file

Create `.agents/tahmures_character_visual_prompts_ch01-04.md` with one
standalone image-generation prompt and a negative prompt for every named
character in the behavior file, including Tahmures, plus one role-based prompt
for Chapar. Do **not** call an image-generation service or create image files
in this phase. These are prompt drafts for later human-supervised generation;
they do not approve, freeze, or add assets to the registry.

Inspect the actual user-approved Tahmures master:

`Characters/tahmures/versions/layout01-v2/source/approved_master.png`

Expected SHA-256:
`3eedfaa5a41965c45a137a74a9137c6e59304a0604f877a81c98870c64dba2e5`.

The user reports that this ChatGPT-created reference was designed with a Rick
and Morty influence. Use the master itself as Tahmures’s identity anchor and
derive an original, reusable visual language from its visible traits. GPT
observed: clean dark outlines; expressive, simplified cartoon facial shapes;
large readable eyes; controlled cel-like shading; dark wavy hair and beard; a
gold diadem with a central sun medallion; a deep blue robe with repeating gold
motifs; an ivory tunic; and a burgundy sash. Verify these against the image.
Keep Tahmures recognizable and do not redesign his face, palette, diadem,
beard, or clothing identity in the prompt.

Translate the stated influence into general visual descriptors. Do not ask an
image model to copy the Rick and Morty series, its characters, logos, exact
model sheets, or signature designs. Do not insert Rick, Morty, or unrelated
franchise imagery. For other figures, use a coherent original 2D cartoon
language compatible with the master while giving each a distinct silhouette,
face, palette accent, costume, and prop. Keep all costumes and settings
Iranian-inspired project fiction, not claimed historical reconstruction.

For every prompt, include:

- character name and approved chapter role;
- whether the art choice is source-supported or `UNLOCKED_ARTISTIC_CHOICE`;
- one clear view/composition suitable for a reference sheet;
- face, silhouette, costume, palette, expression, pose, and distinctive prop
  where supported or explicitly labelled as a design proposal;
- shared series line, shading, and color-language constraints derived from the
  approved Tahmures master;
- constraints against modern clothing/technology, European-medieval costume
  clichés, duplicate Tahmures features, gratuitous villain coding, embedded
  text, watermarks, logos, or unapproved characters;
- a separate negative prompt and a note that the image is a candidate requiring
  human selection.

Do not invent source-canonical costume, facial features, weapons, powers, or
colors where the dossier is silent. Mark those as unlocked art choices. The
prompt for `Black Div` must not imply that his personal name or visual design
comes from Ferdowsi. The prompt for `Budhasaf` must preserve its unverified
source status and not depict him as Shahrasp. For Div-e Sefid and Arzhang Div,
avoid assuming that every failure is caused by evil intent. Chapar’s prompt
should depict a Persian courier role, not a newly invented named mythic figure.

## 8. Bilingual and tooltip handling

## 9. Required coverage and self-check

Before returning, compare the behavior sheets against all four live tale
sections in both languages. Account for every named character and role in a coverage table
with `Chapter`, `English role`, `Persian role/name`, `approved mapping`, and
`status`. For collective background actors, record `COLLECTIVE—NO NEW NAME`.
If an unexpected named character or collision appears, do not invent a mapping;
list it as `GPT_REVIEW_REQUIRED`.

Check:

- every approved mapping appears exactly once in the roster, with all
  applicable chapters listed;
- English and Persian names are consistent and pronounceable;
- source tier and fictional chapter role are separate;
- adaptations and chronology changes are explicit;
- every character has a bounded behavior and functional hover note;
- no tooltip implies a technical capability absent from the engineering lesson;
- no source quotation, biography, or historical claim was invented;
- every named profile has a corresponding individual visual prompt, and Chapar
  has the role-based visual prompt;
- visual prompts use the approved master as Tahmures’s reference, describe an
  original compatible visual language, and do not imply generated art exists;
- Budhasaf’s source-name ambiguity is explicit and remains distinct from
  Shahrasp;
- no manuscript, continuity, metadata, glossary, or other file changed.

Run `rtk proxy git diff --check`. A full manuscript/build gate is not required
for these reference-only files. Report both output paths, coverage results,
unresolved source/name/pronoun/art questions, and any scope issue in your final
response. Do not claim GPT acceptance, generated artwork, or human approval.

Finish with exactly one token:

`CH01_04_CHARACTER_REFERENCE_PACK_READY_FOR_GPT`

`CH01_04_CHARACTER_REFERENCE_PACK_REVISION_REQUIRED`

`CH01_04_CHARACTER_REFERENCE_PACK_OWNER_DECISION_REQUIRED`
