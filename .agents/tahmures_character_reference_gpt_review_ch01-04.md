# GPT review — Chapter 01–04 character reference pack

## Assessment

The two GLM files are useful adaptation drafts, not yet a clean input for
manuscript revision. The approved English names are represented, the source
identity and project-fiction role are generally kept separate, and no artwork
or manuscript changes are claimed. A few coverage and tooltip defects need a
bounded correction before the references are used as the basis for a bilingual
narrative rewrite.

## What passed

- The roster covers the approved cast: Tahmures, Shahrasp, Akvan Div, Black Div,
  Div-e Sefid, Arzhang Div, Soroush, Simurgh, Arash, Garshasp, Jamshid,
  Budhasaf, Keyumars, Nariman, Sam, and the occupational role Chapar.
- The new chapter roles are marked as project fiction. Later-cycle figures are
  not presented as participants in Tahmures's source episode. Black Div's
  personal identity is correctly described as an adaptation of an unnamed
  figure. Budhasaf remains separate from Shahrasp and its possible scholarly
  name variant.
- Chapar and Simurgh remain distinct: one brings the found tablet to the hall;
  the other carries a message from the hall to the captain.
- The hover descriptions mostly preserve the engineering distinctions: a
  record is not authority, fluency is not evidence, and a stakeholder does not
  own the council's priorities.
- I opened the approved master at
  `Characters/tahmures/versions/layout01-v2/source/approved_master.png` and
  visually confirmed the described dark clean outlines, large expressive eyes,
  wavy dark hair and beard, gold diadem with round sun medallion, blue robe with
  gold motifs, ivory tunic, and burgundy sash. Its SHA-256 is
  `3eedfaa5a41965c45a137a74a9137c6e59304a0604f877a81c98870c64dba2e5`.
  GLM's pixel checks are useful for palette evidence, but they were not visual
  inspection. The prompts appropriately translate the reported Rick and Morty
  influence into broad original design traits and prohibit copying that show.
- The phase report states that no art was generated and no manuscript,
  continuity, glossary, or review-status file was changed. The current Git
  status is consistent with the two new reference files being untracked,
  alongside earlier untracked user materials.

## Bounded corrections required

| File | Finding | Minimum correction |
|---|---|---|
| `.agents/tahmures_character_behaviors_ch01-04.md` | Chapter 01's closing hook names the Keeper and Mirror Div; the Mirror Div is missing from its Chapter 01 appearance list. Chapter 03's closing hook names the Archivist; Soroush is missing Chapter 03. | Include those hook appearances in the roster, profiles, and coverage table. |
| `.agents/tahmures_character_visual_prompts_ch01-04.md` | Chapter tags omit Div-e Sefid's Chapter 01 hook and Soroush's Chapter 03 hook. | Bring their chapter tags into line with the corrected behavior file. |
| `.agents/tahmures_character_behaviors_ch01-04.md` | Shahrasp's “exact appearances” says he appears in the Chapter 01 and 02 hooks; neither hook contains the Scribe. | Remove those hook claims and list only the appearances actually present. |
| `.agents/tahmures_character_behaviors_ch01-04.md` | Garshasp's project-fiction description says “Hushang's generation.” This carries the old project mapping into the new adaptation. | Describe the “prior court” without naming the father. Preserve Hushang only when explicitly stating canonical source genealogy; Keyumars remains the approved project character for the builder/deceased-king roles. |
| Behavior-sheet tooltip text | Persian contains a malformed Arash sentence (`رسیدی پیام‌رسان`), an unnatural Shahrasp phrase (`دیدنی نگه می‌دارد`), an unclear Soroush phrase (`واقعیت بدهند`), and owner/process metadata inside Budhasaf's reader-facing tooltip. | Correct those Persian lines naturally and keep approval/source-process notes in the editorial sheet, outside reader-facing tooltip copy. Recheck EN/FA meaning. |
| `.agents/tahmures_character_visual_prompts_ch01-04.md` §0 | GLM reports no image-viewing capability, while the file's “verified traits” wording can read as visual confirmation by GLM. | State that GLM checked bytes/palette programmatically and that the visible traits were independently confirmed by GPT during this review. Do not imply GLM visually inspected the image. |
| Nariman role description | The live tale calls the role “flood keeper,” while the owner described the mapping as an affected-person role. | Keep the chapter's stakeholder function and record the intended “flood-affected council member” description; do not invent a separate river-keeping job. |

The displayed duplicate snippets noticed during an earlier inspection were caused
by overlapping output ranges; the files themselves do not contain those
duplicates. The Chapter 01 Tahmures coverage row also appears only once.

## Decisions carried into the narration phase

Two details were not determined by the approved name-pair mapping and affected
the story itself. The owner has now resolved both for this batch:

1. **Resolved by the owner:** Jamshid is the eastern governor (who smiles), and
   Budhasaf is the western governor (who accuses the Mirror Div).
2. Keep Keyumars alive as the Chapter 03 builder, and state that Chapter 04
   takes place six years after his death. Jamshid's Chapter 04 letter is an
   older record and he is dead by then. This preserves the approved roles
   without changing the engineering lesson.

The prior court/captain reference in Chapter 01 remains unnamed in the source
text. Do not silently identify Tahmures's father as Keyumars; the approved
Keyumars mapping concerns the builder/deceased-king roles. Canonical source
notes may still state that Ferdowsi names Hushang as Tahmures's father.

For this batch, preserve the existing English pronouns as project-fiction
presentation unless the owner changes them during signoff. Simurgh may use the
source-supported bird form as the current visual-prompt proposal; its messenger
role in this tale remains project fiction. Persian spellings in the reference
pack are proposed draft forms, not canonical glossary promotion. `شهراسپ` is
the recommended project form because it is the main Persian form in the supplied
dossier; retain a signoff note about the `شهرسپ` variant.

## Decision and next action

**Bounded revision required before the character pack can be treated as a clean
narration input.** The story-refactor prompt includes these corrections as its
entry step. Both owner decisions are now recorded as fixed inputs; the prompt
applies them consistently to the manuscripts and continuity record. It also
preserves existing review metadata until the revised text receives GPT and
human review.
