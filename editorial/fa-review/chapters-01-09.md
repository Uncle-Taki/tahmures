# Persian Review Record — Chapters 01–09

## Status

- Project: **Tahmures**
- Review scope: Persian Chapters **01–09**
- Review status: **human-reviewed as a corpus**
- Chapters 10–24: **not yet human-reviewed**
- Purpose of this file:
  1. preserve the human findings from the first nine chapters;
  2. convert those findings into reusable editorial rules;
  3. prevent the same failure classes from appearing in Chapters 10–24;
  4. protect approved Persian improvements from being overwritten by literal retranslation;
  5. create a calibration corpus for future Codex review passes.

This file does **not** claim that every listed issue occurs in every one of Chapters 01–09.
The original review comments were recorded at corpus level rather than with complete
chapter-by-chapter localization. Do not invent chapter locations that were not recorded.

---

## 1. Source-of-truth hierarchy

For Persian editing, use the repository hierarchy defined by `AGENTS.md`,
`book/project-charter.md`, `book/narrative-continuity.md`, `meta-prompt.md`,
`writing_persian_eng_books.md`, and `book/fa/translation-glossary.md`.

This file adds **human review evidence**. It does not replace those repository rules.

When a conflict exists:

1. explicit current user instruction;
2. mandatory repository constraints in `AGENTS.md`;
3. approved project charter and continuity state;
4. technical/factual correctness;
5. canonical English meaning where English is authoritative;
6. human-approved Persian wording recorded here or in later review records;
7. established glossary and book-wide terminology;
8. `writing_persian_eng_books.md`;
9. stylistic preference.

A human-approved Persian sentence must **not** be replaced merely because another
translation resembles the English source more closely.

---

## 2. Review coverage

### 2.1 Reviewed

- Chapters 01–09: reviewed by the author/editor.
- Findings in this file are considered validated failure classes.

### 2.2 Not yet reviewed

- Chapters 10–24 have not yet received human line-by-line review.
- They must therefore be treated as **unreviewed**, not as correct.
- The rules derived from Chapters 01–09 must be applied proactively to Chapters 10–24.
- Applying those rules is a **preventive audit**, not a claim that Chapters 10–24 have
  already passed human review.

### 2.3 Required rollout

For Chapters 10–24:

1. scan for every failure class listed in this document;
2. produce proposed corrections;
3. preserve technical meaning and protected tokens;
4. run deterministic repository validators;
5. mark the chapter as `machine_prechecked`;
6. do **not** mark it `human_reviewed` until the author reviews it.

Recommended review batches:

- Batch A: 10–12
- Batch B: 13–15
- Batch C: 16–18
- Batch D: 19–21
- Batch E: 22–24

---

## 3. Confirmed issue classes

### 3.1 Reference parity between English and Persian

Observed review concern:

> Persian references are fewer than the English version.

Required policy:

- The canonical English chapter determines the minimum citation set for claims shared
  by both editions.
- Persian must not silently lose a citation that supports a canonical technical,
  empirical, historical, or literary claim.
- Compare **citation identity**, not only citation count.
- Prefer set containment:

```text
english_required_citations ⊆ persian_citations
```

- Persian may contain additional Persian-language or edition-specific references when
  justified.
- Equal counts with different sources do **not** constitute parity.
- When English and Persian support different wording, investigate whether:
  - the Persian translation dropped a claim;
  - the English chapter changed after translation;
  - the Persian chapter is stale;
  - a citation was accidentally removed;
  - the editions intentionally differ.

Recommended future validator:

```text
scripts/validate_reference_parity.py
```

The validator should report:
- missing citation keys;
- unexpected citation loss;
- unmatched reference anchors;
- stale reference sections;
- duplicate references;
- references present in one edition but not used in the corresponding claim context.

It should not automatically delete Persian-only references.

---

### 3.2 Reader-facing thematic part names

Observed review concern:

> The four six-chapter divisions should be thematic rather than merely numerical.

Policy:

- Keep internal repository paths (`part-1` ... `part-4`) stable unless a separate
  migration is explicitly approved.
- Prefer changing reader-facing titles/navigation before physically moving files.
- This avoids breaking:
  - MkDocs navigation;
  - links and anchors;
  - experiment mappings;
  - prompts;
  - tests;
  - translation parity;
  - chapter metadata.

The four existing conceptual arcs should be treated as the basis for reader-facing
part titles:

1. Language and intent
2. Prompt design
3. Knowledge, memory, and action
4. Evaluation, security, and production

Exact Persian titles require editorial approval and glossary consistency.

Do not rename directories or slugs as part of ordinary prose revision.

---

### 3.3 English technical terminology retention

Observed review concern:

> Some English terms should remain English in the Persian edition.

Policy:

- The list in `terminology-candidates.yml` is a **candidate registry**, not an
  unconditional whitelist.
- Each occurrence must be classified by concept and context.
- Use the existing project actions:
  - `PRESERVE_EXACT`
  - `RETAIN_ENGLISH`
  - `TRANSLATE_PERSIAN`
  - `TRANSLITERATE_PERSIAN`
  - `REVIEW`
- English retention is justified when it materially improves technical identity,
  searchability, interoperability, implementation correspondence, or professional
  recognizability.
- Ordinary English prose should not remain English merely because it appears in the
  source.
- A retained English noun must still participate in a **natural Persian sentence**.

Example principle:

```text
Persian grammar around retained English terminology.
```

not:

```text
English noun-phrase order copied into Persian.
```

---

### 3.4 Loss of Persian fluency

Confirmed failure mode:

A sentence may contain individually understandable words while the sentence as a
whole is unnatural, semantically distorted, or structurally copied from English.

Human-approved example:

**Before**

> اولویت دستورها policy مربوط به سامانه و متکی بر منبع‌های احراز هویت‌شده است، نه مسابقه‌ای در زبان قانع‌کننده.

**Approved**

> اولویت دستورها policy مربوط به سامانه و متکی بر منبع‌های احراز هویت‌شده است، نه مسابقه‌ای در زبان برای قانع‌ کردن.

Lesson:

- evaluate relation and scope, not word-by-word equivalence;
- do not approve a translation merely because every token can be mapped to the source;
- check whether adjectives, adverbs, complements, and purpose phrases attach to the
  intended head.

---

### 3.5 Compressed English noun phrases rendered unnaturally in Persian

Human-approved example:

**Before**

> کارگاه دبیران مکانیکی حیاطی با سقف شیشهٔ آبی بود. سی دست برنجی بالای سی میز حرکت می‌کردند و میان آن‌ها صندوقی سرو از لوح‌های انبار شرقی قرار داشت.

**Approved**

> کارگاه دبیران مکانیکی حیاطی با سقف شیشهٔ آبی بود. سی دست برنجی بالای سی میز حرکت می‌کردند و میان آن‌ها صندوقی از جنس چوب سرو حاوی لوح‌های انبار شرقی قرار داشت.

Lesson:

- Persian may need an explicit semantic relation such as:
  - `از جنس ...`
  - `حاوی ...`
  - `برای ...`
  - `متعلق به ...`
  - `مربوط به ...`
- do not preserve English-style noun stacking when Persian requires a relationship to
  be stated explicitly;
- adding an explicit relation is acceptable when it preserves the original meaning
  rather than inventing new content.

---

### 3.6 Wrong head–modifier order

Human-approved example:

**Before**

> مجاز مجموعه نوع و وضعیت را نوشتند،

**Approved**

> مجموعه مجاز نوع و وضعیت را نوشتند،

Lesson:

- inspect the head noun and modifier relation;
- verify موصوف/صفت ordering;
- verify مضاف/مضاف‌الیه ordering;
- verify premodifier/postmodifier placement;
- do not assume source-language order survives Persian translation.

---

### 3.7 Broken Persian-English compounds

Observed problematic fragments include:

```text
الزامی فیلد
flexible فیلد
نه خودکار درست
میانی رکورد‌ی
از free نثر امن‌تر است
اضافی-فیلد
خام پاسخ
انسان بازبینی
میانی قرارداد مانند نهایی قرارداد مهم
```

Policy:

- these are **review triggers**;
- do not perform blind string replacement;
- determine:
  1. head noun;
  2. modifier;
  3. ezafe relation;
  4. whether English retention is justified;
  5. whether the phrase is technical identity or ordinary prose;
  6. whether punctuation or inline-code markup is affecting perceived order.

High-confidence examples may be reordered when context confirms the intended meaning,
for example a noun followed by an adjective in Persian.

Ambiguous fragments must be reported for review instead of guessed.

---

### 3.8 Untranslated or unexplained English terms

Observed concern:

> Some English words appear without a Persian explanation.

Policy:

- distinguish intentional retention from accidental non-translation.
- For `RETAIN_ENGLISH` prose terms:
  - use the repository's configured tooltip/term mechanism where supported;
  - provide a concise Persian explanation;
  - do not insert tooltip markup into code, identifiers, paths, formulas, commands,
    URLs, or other protected content.
- A retained term with no explanation is acceptable only when:
  - it is already established earlier in the chapter/book;
  - repetition of the explanation would be noisy;
  - the glossary/tooltip mechanism already makes the meaning available.

---

### 3.9 Mixed-language sentence architecture

Observed example:

```text
stageهایی با این field‌ها تولید کن: id، purpose، depends_on، inputs، outputs،
checkpoint، failure_outcome و terminal.
فقط stage ID‌های مجاز را به‌کار ببر.
stageها را اجرا نکن.
```

Failure mode:

- each technical token may be defensible;
- the surrounding Persian grammar can still become fragmented or visually unstable.

Required checks:

- Persian syntax remains the governing sentence structure;
- retained English terms should be delimited consistently;
- pluralization should not create awkward mixed morphology when a clearer Persian
  construction is available;
- code-like identifiers must remain exact;
- do not translate identifiers that are intended to be literal fields;
- distinguish explanatory prose from literal prompt/code content.

A possible restructuring may be proposed by Codex, but it is not considered
human-approved until reviewed.

---

## 4. Persian syntactic and semantic integrity gate

This gate is **mandatory** for every Persian chapter, including Chapters 10–24.

A fluent sentence that is syntactically or semantically malformed **fails** review.

Check all applicable relations:

### 4.1 Noun phrase integrity

- head noun is identifiable;
- adjective modifies the intended noun;
- adjective order is natural;
- ezafe chain is meaningful;
- مضاف and مضاف‌الیه are ordered correctly;
- English technical nouns do not force English noun order into Persian;
- stacked nouns are expanded when Persian needs an explicit relation.

### 4.2 Adjective integrity

Check:

- which noun the adjective modifies;
- whether the adjective is restrictive, descriptive, classificatory, or technical;
- whether adjective scope changed during translation;
- whether multiple adjectives have a natural order;
- whether a retained English adjective should instead become:
  - Persian adjective;
  - English technical label;
  - parenthetical technical identity;
  - tooltip-supported term.

### 4.3 Adverb integrity

Check:

- adverb position;
- adverb scope;
- which verb/adjective/clause it modifies;
- whether negation scope changed;
- whether degree changed;
- whether temporal or frequency meaning changed;
- whether an English adverb was translated into a Persian adjective or vice versa.

### 4.4 Clause integrity

Check preservation of:

- actor;
- action;
- object;
- recipient;
- causal relation;
- condition;
- negation;
- modality;
- uncertainty;
- comparison;
- temporal order;
- quantification;
- exception;
- limitation.

### 4.5 Coordination and lists

Check:

- all coordinated items have compatible grammatical roles;
- list items are parallel;
- conjunction scope is clear;
- a retained identifier list is not accidentally treated as ordinary prose.

### 4.6 Pronoun and reference integrity

Check:

- antecedent is clear;
- Persian pronoun does not point to the wrong noun;
- omitted subjects remain unambiguous;
- demonstratives do not lose the intended technical referent.

---

## 5. Text-integrity priority

Use this editorial priority when revising Persian:

```text
technical correctness
→ factual correctness
→ semantic fidelity
→ syntactic integrity
→ adjective/adverb scope
→ terminology correctness
→ fluency
→ stylistic elegance
```

Never trade an earlier item for a later one.

In particular:

- beautiful but semantically altered prose is unacceptable;
- fluent but grammatically malformed prose is unacceptable;
- technically correct wording with awkward but repairable style should be improved
  without changing meaning;
- stylistic variety is not a reason to vary technical terminology.

---

## 6. Protected-content rule

Before any Persian rewrite, identify and protect:

- fenced code;
- inline code;
- commands;
- identifiers;
- function/method/class names;
- API names;
- configuration keys;
- JSON/YAML/XML keys;
- paths;
- filenames;
- URLs;
- version numbers;
- checksums;
- equations;
- mathematical notation;
- standard identifiers;
- unit symbols;
- literal field names;
- experiment manifest names.

Do not apply global search-and-replace across protected content.

---

## 7. Human-approved wording policy

Human-approved Persian changes in Chapters 01–09 are editorially authoritative
unless one of the following is found:

- factual error;
- technical error;
- grammatical error;
- terminology conflict;
- broken link/reference;
- contradiction with a later explicit user instruction;
- contradiction with canonical project meaning.

Do not revert them simply to match English syntax.

When an English canonical chapter later changes, compare meaning rather than performing
automatic sentence-level replacement.

---

## 8. Preventive application to Chapters 10–24

The following failure classes must be proactively scanned in every unreviewed chapter:

- reference loss;
- literal translation;
- English sentence order copied into Persian;
- wrong موصوف/صفت order;
- wrong مضاف/مضاف‌الیه relation;
- broken ezafe chains;
- wrong adjective scope;
- wrong adverb scope;
- mixed Persian-English compound inversion;
- unexplained retained English;
- inconsistent terminology;
- malformed list coordination;
- ambiguous pronoun/reference;
- semantic relation lost in compressed noun phrase;
- code/identifier corruption;
- accidental modification of numbers, units, or claims.

The result of this sweep should be labelled:

```text
machine_prechecked: true
human_reviewed: false
```

until the author reviews the chapter.

---

## 9. Review output contract

For each chapter review, Codex should return a compact change report with:

1. files changed;
2. high-severity semantic or technical corrections;
3. syntactic-integrity corrections;
4. adjective/adverb-scope corrections;
5. terminology decisions;
6. retained English terms newly introduced;
7. unresolved ambiguous terms;
8. English/Persian reference mismatches;
9. protected-content issues;
10. commands/tests run;
11. remaining human-review items.

Do not paste the full chapter unless explicitly requested.

---

## 10. Severity model

### BLOCKER

- technical meaning changed;
- factual claim changed;
- code/identifier altered;
- citation supporting a canonical claim lost;
- negation/condition/modality reversed;
- mathematical value/unit altered.

### HIGH

- wrong noun/adjective relation;
- wrong ezafe relation;
- wrong adverb scope;
- actor/object relation altered;
- ambiguous mixed-language phrase that changes meaning;
- English technical term mistranslated into a different concept.

### MEDIUM

- literal or awkward Persian;
- inconsistent terminology with meaning still recoverable;
- unexplained retained English;
- unnatural phrase order;
- poor coordination/list parallelism.

### LOW

- punctuation;
- spacing;
- نیم‌فاصله;
- stylistic tightening that does not alter meaning.

---

## 11. Completion rule

A chapter is not complete merely because it reads smoothly.

For Persian chapters, completion requires:

- repository structural validation;
- translation synchronization checks;
- protected-content preservation;
- reference parity check when applicable;
- terminology consistency check;
- syntactic and semantic integrity review;
- adjective/adverb scope review;
- final continuous-prose reread;
- rendered RTL review when relevant;
- `make check` or the appropriate narrower validators.

Human review status must remain distinct from machine validation status.
