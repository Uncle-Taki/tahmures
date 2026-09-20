---
name: Persian Engineering Book — Writing & Editing Policy
version: "3.1"
primary_language: "fa"
purpose: >
  Improve the Persian edition of an engineering book so that it reads as
  professionally authored Persian technical writing while preserving the
  exact English terminology, identifiers, notation, and technical forms that
  engineers need to recognize, search, configure, implement, and compare with
  international documentation.
---

# Persian Engineering Book — Writing & Editing Policy

This file is the mandatory editorial policy for improving, rewriting, reviewing, or translating the Persian (`fa`) edition of this engineering book.

Treat it as a **normative repository-level editorial specification**, not as a general translation prompt.

The objective is NOT to produce a sentence-by-sentence Persian translation of an English book.

The objective is to produce:

> **A professional Persian engineering book written naturally for Persian-speaking engineers, while preserving English where the original form has genuine technical value.**

The core principle is:

> **Persian for explanation; English for technical identity.**

---

# 1. Instruction Priority

When instructions appear to conflict, use the following priority order:

1. Mandatory repository constraints in `AGENTS.md`.
2. Explicit scope and requirements of the current editing task.
3. Technical, factual, mathematical, and engineering correctness.
4. Preservation of the author's intended meaning.
5. Existing project glossary and established book-wide terminology.
6. Consistency with the rest of the Persian edition.
7. This editorial policy.
8. Natural Persian readability and stylistic preference.

Never sacrifice technical correctness merely to make the text more Persian.

Never silently override an established project convention.

---

# 2. Mandatory Preflight

Before editing any Persian chapter, inspect the project context.

## 2.1 Read project instructions

Read completely when they exist:

- `AGENTS.md`
- `README.md`
- this file
- `editorial/fa-review/chapters-01-09.md` when present
- `editorial/fa-review/terminology-candidates.yml` when present
- `editorial/fa-review/regression-cases.yml` when present
- `editorial/review-status.yml` when present

Do not begin rewriting immediately after opening only the target chapter.

## 2.2 Understand the repository

Identify:

- project purpose;
- engineering domain;
- book root;
- Persian and English book locations;
- localization structure;
- chapter file format;
- Markdown/MDX/HTML/documentation framework;
- table-of-contents structure;
- existing glossary or terminology files;
- tooltip/technical-term implementation;
- RTL/LTR conventions;
- build, lint, formatting, and validation commands.

Do not assume a specific renderer, glossary location, or tooltip syntax before inspecting the repository.

## 2.3 Understand the book

Before modifying a chapter:

1. Inspect the book structure.
2. Review chapter and section titles across the book.
3. Read the target Persian chapter completely.
4. Read the corresponding English chapter when available.
5. Read neighboring chapters sufficiently to understand terminology and conceptual progression.
6. Search existing Persian chapters when an important term may already have an established form.
7. Read the project glossary if one exists.

Do not edit terminology in isolation when repository context can resolve the decision.

When editing multiple chapters, maintain one terminology inventory across the whole task.

---

# 3. Primary Editorial Goal

The Persian edition must read as though it was originally written by an experienced Persian-speaking engineer.

Use:

- natural Persian syntax;
- professional but readable language;
- technically precise wording;
- correct Persian punctuation;
- correct نیم‌فاصله;
- clear paragraph structure;
- logical transitions;
- precise cause-and-effect relationships;
- consistent terminology;
- concise explanations where possible.

Avoid:

- machine-translation language;
- word-for-word translation;
- English sentence structure copied into Persian;
- unnecessary passive voice;
- unnecessary English words;
- excessive parenthetical translations;
- artificial or overly literary Persian;
- vague technical prose;
- inconsistent terminology;
- repetitive explanations;
- unnecessary stylistic rewriting of already correct text.

Every edit should improve at least one of:

- correctness;
- clarity;
- consistency;
- technical precision;
- readability.

---

# 4. Terminology Is Concept Management, Not Word Replacement

Never decide terminology by looking at an isolated word.

Interpret every technical term according to:

- engineering domain;
- chapter context;
- neighboring paragraphs;
- equations;
- figures and diagrams;
- implementation context;
- source-code context;
- standards;
- existing terminology elsewhere in the book.

The same English word may represent different concepts in different domains.

For example, `Node` may mean:

- a Kubernetes Node;
- a finite-element node;
- a network node;
- a graph node;
- a distributed-system participant.

Do not mechanically apply one Persian translation to all of them.

---

# 5. Terminology State Model

For each important English or Latin-script expression encountered in Persian prose, internally determine:

`Source term → Concept/domain → Action → Display form → Persian explanation`

Use exactly one of the following terminology actions:

- `PRESERVE_EXACT`
- `RETAIN_ENGLISH`
- `TRANSLATE_PERSIAN`
- `TRANSLITERATE_PERSIAN`
- `REVIEW`

These actions describe editorial behavior, not merely dictionary equivalence.

---

# 6. PRESERVE_EXACT

Use `PRESERVE_EXACT` when exact spelling, syntax, notation, or identity must not change.

Typical examples include:

- source-code identifiers;
- function names;
- method names;
- class names;
- variable names;
- constants;
- package names;
- module names;
- API names;
- API endpoints;
- HTTP methods;
- commands;
- command-line flags;
- environment variables;
- configuration keys;
- JSON/XML/YAML keys;
- database fields;
- file paths;
- filenames;
- file extensions;
- URLs;
- URI schemes;
- regular expressions;
- version numbers;
- checksums;
- literal software UI strings when exact matching is required;
- mathematical variables;
- mathematical notation;
- equation labels;
- standard unit symbols;
- official standard identifiers.

Examples:

`kubectl apply`

`docker compose up`

`request_timeout`

`GET /users/{id}`

`AddDbContext`

`AppDbContext`

`Program.cs`

`deployment.yaml`

`ISO 9001`

`IEC 61131-3`

`ASTM D3039`

`RFC 9110`

Do not translate, transliterate, respell, or insert markup inside these exact technical tokens.

---

# 7. Protected Content Pass

Before linguistic editing, identify protected content.

Treat the following as protected unless the current task explicitly authorizes modification:

- fenced code blocks;
- inline code;
- executable examples;
- commands;
- identifiers;
- API syntax;
- configuration syntax;
- URLs;
- paths;
- filenames;
- formulas;
- equations;
- mathematical symbols;
- equation numbers;
- standard identifiers;
- unit symbols;
- checksums;
- code-like structured data;
- literal UI values that must match software exactly.

Never insert tooltip markup inside protected content.

Never perform broad search-and-replace operations that can modify protected content.

If an automated replacement would affect code, formulas, identifiers, or technical syntax, stop using the global replacement and edit only verified prose occurrences.

---

# 8. TRANSLATE_PERSIAN

Use `TRANSLATE_PERSIAN` when:

- the expression belongs to ordinary prose;
- a clear and natural Persian equivalent exists;
- the Persian form is established in the project or technical field;
- English spelling adds little technical value;
- retaining English would unnecessarily fragment Persian prose.

Ordinary explanatory language should normally be Persian.

Examples:

`Introduction` → `مقدمه`

`Overview` → `نمای کلی`

`Summary` → `جمع‌بندی`

`Conclusion` → `نتیجه‌گیری`

`Example` → `مثال`

`Warning` → `هشدار`

`Configuration` → `پیکربندی`

`calculation process` → `فرایند محاسبه`

`system behavior` → `رفتار سیستم`

`results indicate` → `نتایج نشان می‌دهند`

Do not write mixed sentences such as:

`برای calculate کردن input باید parameterها را check کنیم.`

Prefer:

`برای محاسبه مقدار ورودی، ابتدا پارامترها بررسی می‌شوند.`

English should remain because it provides technical value, not because translating prose requires more effort.

---

# 9. RETAIN_ENGLISH

Use `RETAIN_ENGLISH` when retaining the original English form materially improves one or more of:

- technical precision;
- professional recognizability;
- industry convention;
- documentation correspondence;
- implementation correspondence;
- searchability;
- interoperability;
- educational value;
- distinction between similar technical concepts.

Strong reasons for retention include:

- engineers commonly use the English form;
- the term is internationally recognized by that name;
- the Persian equivalent is unstable, uncommon, ambiguous, artificial, or misleading;
- readers are likely to search official documentation using the English term;
- the term identifies a technology, framework, platform, architecture, protocol, or software component;
- it is a recognized acronym;
- external diagrams, APIs, standards, or documentation use that exact terminology;
- replacing it would hide an important distinction;
- the project glossary explicitly marks it as retained.

Examples may include, depending on context:

- Kubernetes
- Pod
- Namespace
- Container
- Docker
- API
- REST
- gRPC
- Control Plane
- Scheduler
- ReplicaSet
- StatefulSet
- DaemonSet
- Ingress
- Service Mesh
- Finite Element Method
- PID
- PLC
- CFD
- FEM

These examples are illustrative, not a rigid universal whitelist.

Always use actual engineering context.

---

# 10. TRANSLITERATE_PERSIAN

Use `TRANSLITERATE_PERSIAN` only when:

- the Persian-script loanword is already genuinely established among Persian-speaking professionals;
- the Persian-script form reads naturally;
- exact Latin spelling provides little additional technical value.

Do not transliterate merely because translation is difficult.

Do not invent awkward phonetic Persian spellings for:

- product names;
- APIs;
- standards;
- identifiers;
- commands;
- search-critical terminology.

Translation, transliteration, and English retention are different decisions.

Example conceptually:

`database` → `پایگاه داده` → translation

`compiler` → `کامپایلر` → established transliteration when appropriate

`Kubernetes` → `Kubernetes` → English retention

`request_timeout` → `request_timeout` → exact preservation

---

# 11. REVIEW

Use `REVIEW` when terminology is genuinely ambiguous, domain-sensitive, or insufficiently supported by context.

Do not guess.

Resolve uncertainty using this order:

1. Current task instructions.
2. Existing project glossary.
3. Established usage elsewhere in the Persian book.
4. Corresponding English chapter.
5. Neighboring chapters and diagrams.
6. Repository-specific terminology resources.
7. Authoritative Persian technical terminology sources available to the project.
8. Relevant engineering standards.
9. Official upstream product/API documentation.

If uncertainty remains:

- preserve the technically safest existing wording;
- do not invent an official-sounding Persian equivalent;
- do not insert TODO markers into published prose unless the project uses them;
- report the unresolved terminology after editing.

Use qualitative confidence:

### High confidence

Apply the decision when consistent with project rules and glossary.

### Medium confidence

Search project context before changing the term.

### Low confidence

Do not invent terminology. Preserve the safest wording and report the issue.

Do not fabricate:

- official translations;
- acronym expansions;
- standard definitions;
- API meanings;
- formula corrections;
- glossary entries.

---

# 12. Terminology Decision Priority

When deciding how a term should appear, use the following precedence:

1. Explicit terminology instruction in the current task.
2. Existing project glossary.
3. Explicit project terminology overrides.
4. Consistent usage already established in the Persian edition.
5. Authoritative domain terminology available to the project.
6. This document's terminology decision procedure.

Do not silently establish a new book-wide convention when one already exists.

---

# 13. Glossary Policy

Treat terminology as persistent book-wide state.

If the repository already contains a glossary, reuse it.

Do not create a new glossary automatically unless the current task or repository conventions authorize it.

When no glossary exists, maintain an internal terminology inventory during the editing task.

A recommended glossary model is:

| English term | Persian preferred | Action | Tooltip FA | Domain | Notes |
|---|---|---|---|---|---|

Allowed `Action` values:

- `retain`
- `translate`
- `transliterate`
- `preserve`
- `review`

Example:

| English term | Persian preferred | Action | Tooltip FA | Domain | Notes |
|---|---|---|---|---|---|
| API | رابط برنامه‌نویسی کاربردی | retain | رابطی قراردادی برای ارتباط نرم‌افزارها | software | Keep acronym |
| database | پایگاه داده | translate | | software | Persian preferred |
| Kubernetes | | retain | سامانه‌ای برای مدیریت استقرار و اجرای workloadهای کانتینری | software | Proper technology name |
| request_timeout | | preserve | | software | Configuration identifier |
| FEM | روش اجزای محدود | retain | روش عددی برای تقریب حل مسائل مهندسی با تقسیم دامنه به اجزای کوچک‌تر | numerical engineering | Persian name + acronym |
| kPa | کیلوپاسکال | preserve | | units | Standard unit symbol |

`Persian preferred` and `Action` are intentionally separate.

A term may have a known Persian meaning while still being displayed in English.

Once a terminology decision is established, keep it consistent unless it is technically wrong.

Do not use stylistic variety for technical terminology.

---

# 14. Persian-First Headings

The Persian edition should have predominantly Persian chapter, section, and subsection titles.

Translate generic structural wording whenever a natural Persian form exists.

Prefer:

`# معماری Kubernetes`

instead of:

`# Kubernetes Architecture`

Prefer:

`## مدیریت چرخه عمر Pod`

instead of:

`## Pod Lifecycle Management`

Prefer:

`## مفاهیم پیشرفته شبکه در Kubernetes`

instead of:

`## Advanced Kubernetes Networking Concepts`

Prefer:

`# استقرار و مقیاس‌پذیری`

instead of:

`# Deployment and Scaling`

Do not retain an entire English heading merely because it contains one important technical term.

Use Persian grammar around retained technical identities.

A hybrid heading is appropriate when the English identity is itself technically important.

Examples:

`# آشنایی با Kubernetes`

`## اجزای Control Plane`

`# کنترل‌کنندهٔ تناسبی–انتگرالی–مشتقی (PID)`

Headings should sound as though they were originally written for Persian-speaking engineers.

Do not mechanically translate headings into unnatural Persian.

Do not rename:

- anchor IDs;
- filenames;
- routes;
- explicit reference keys;

unless you have verified that cross-references remain valid.

Keep heading terminology synchronized with:

- navigation;
- table of contents;
- cross-references;
- metadata;
- internal links.

---

# 15. First Occurrence of Important Concepts

When an important concept appears for the first time in a chapter or major section, make its meaning especially clear.

Depending on readability, acceptable patterns include:

`زمان‌بند (Scheduler)`

`Scheduler یا زمان‌بند`

or simply:

`Scheduler`

with an informative Persian tooltip.

Choose the form that produces the most natural Persian prose.

Do not mechanically repeat both Persian and English forms on every occurrence.

Avoid translation noise such as:

`گره (Node) یک نود (Node) است که...`

The Persian book should not read like a bilingual dictionary.

---

# 16. Acronyms

Preserve recognized technical acronyms when professional recognition matters.

Examples:

- API
- CPU
- GPU
- RAM
- FEM
- CFD
- PID
- PLC
- DNS
- HTTP
- HTTPS
- TLS
- YAML
- JSON

When useful, the Persian explanation may mention both the expanded English name and its contextual Persian meaning.

Do not repeatedly expand a well-established acronym after it has already been introduced.

---

# 17. Official Names

Do not translate or modify official names of:

- products;
- software;
- frameworks;
- protocols;
- programming languages;
- companies;
- vendors;
- libraries;
- packages;
- operating systems;
- official APIs;
- standards;
- project names.

Examples:

- Kubernetes
- Docker
- Linux
- systemd
- Prometheus
- Grafana
- PostgreSQL
- Redis
- NGINX
- Microsoft
- Siemens
- MATLAB
- ANSYS
- SolidWorks
- Abaqus
- OpenFOAM

Write natural Persian prose around them.

---

# 18. Persian Tooltip Requirement

Every deliberately retained English technical term or multiword technical expression appearing in normal Persian prose should expose a concise Persian explanation through the repository's supported term/tooltip mechanism.

This requirement applies to `RETAIN_ENGLISH` prose terms.

It does NOT apply inside protected content such as:

- fenced code;
- inline code;
- identifiers;
- commands;
- URLs;
- file paths;
- API endpoints;
- formulas;
- equations;
- mathematical symbols;
- unit symbols.

Do not insert tooltip markup inside these structures.

---

# 19. Discover Tooltip Implementation Before Editing

Before introducing tooltip markup:

1. Search the repository for an existing implementation.
2. Inspect existing chapters and components.
3. Look for conventions such as:

`title=`

`data-tooltip`

`role="tooltip"`

`aria-describedby`

`<Tooltip`

`<Term`

`<abbr`

`.tooltip`

`.term`

custom Markdown directives

MDX components

4. Reuse the existing project convention.

Do not introduce a second tooltip system unnecessarily.

If the renderer does not support raw HTML, do not insert raw HTML that will appear literally to readers.

If no supported mechanism can be discovered:

- perform safe linguistic edits;
- leave technically safe terminology intact;
- report the tooltip-rendering limitation;
- do not corrupt the chapter source.

---

# 20. Recommended Tooltip Fallback

If:

- no project-specific tooltip component exists;
- raw inline HTML is supported;
- repository conventions permit it;

use a generic inline wrapper such as:

```html
<span class="technical-term" lang="en" dir="ltr" title="توضیح کوتاه و دقیق فارسی">English Term</span>
```

Do not use `<abbr>` universally for every term because not every retained technical expression is an abbreviation.

Use `<abbr>` only when it matches the project's established convention or the semantic nature of the term.

For projects with a dedicated MDX/component system, prefer a reusable semantic component over duplicated raw HTML.

Conceptually:

```mdx
<Term name="API" description="رابطی قراردادی برای ارتباط نرم‌افزارها">API</Term>
```

Reuse the repository's actual syntax rather than inventing this component if it does not exist.

---

# 21. Tooltip Writing Style

A tooltip should answer:

> **What does this term mean here?**

It should explain the concept, not merely translate the word.

Bad:

`Solver → حل‌کننده`

Better:

`بخش محاسباتی نرم‌افزار که دستگاه معادلات حاصل از مدل عددی را حل می‌کند`

Bad:

`Mesh → مش`

Better:

`شبکه‌ای از المان‌ها و گره‌ها که دامنه مسئله برای تحلیل عددی به آن تقسیم می‌شود`

Tooltip descriptions should normally be:

- written in natural Persian;
- technically correct;
- contextual;
- concise;
- understandable without another reference;
- one sentence when possible;
- free of circular definitions;
- free of unnecessary English;
- free of promotional or vague language.

Recommended target:

- approximately 45–120 Persian characters when practical;
- preferably no more than roughly 160 characters unless technical clarity requires more.

Do not sacrifice correctness merely to satisfy a character target.

Reuse the same core definition for repeated instances of the same concept unless context genuinely changes its meaning.

For multiword expressions, treat the whole expression as one semantic unit.

Preferred:

`event loop`

Not separately annotated:

`event` + `loop`

---

# 22. RTL/LTR Handling

Persian prose is RTL.

Retained English terminology is an LTR island inside that prose.

When HTML markup is used for retained English expressions, prefer:

```html
lang="en" dir="ltr"
```

or the repository's equivalent bidi-safe mechanism.

Do not:

- alter English spelling to fix visual direction;
- manually reorder punctuation;
- add random spaces merely to make rendering appear correct;
- wrap an entire Persian paragraph in LTR;
- scatter invisible bidi control characters through Markdown unless the renderer explicitly requires them.

Preserve logical source order.

---

# 23. Code and Commands

Code blocks are technical source material, not translation targets.

Never translate or casually rewrite:

- programming keywords;
- identifiers;
- imports;
- package names;
- commands;
- API parameters;
- JSON keys;
- SQL identifiers;
- flags;
- error codes;
- configuration keys.

Preserve:

- syntax;
- indentation;
- identifiers;
- commands;
- technically significant values.

You may improve:

- prose around code;
- explanatory comments when appropriate and authorized;
- human-language explanations.

Do not modify executable examples unless correcting them is explicitly part of the task.

---

# 24. Mathematical and Engineering Expressions

Never unintentionally alter:

- equations;
- variables;
- subscripts;
- superscripts;
- operators;
- constants;
- numerical values;
- tolerances;
- equation numbers;
- figure references;
- table references.

Technical correctness takes priority over stylistic rewriting.

If `T` represents torque, do not rename it merely because the surrounding text is Persian.

---

# 25. Units

Preserve internationally recognized engineering unit symbols.

Examples:

- mm
- cm
- m
- kg
- MPa
- GPa
- N
- kN
- N·m
- kg/m³
- W
- kW
- V
- A
- Hz
- °C
- Pa
- kPa
- m/s

Do not unnecessarily Persianize SI symbols.

Preserve numerical values.

Use the project's established spacing convention, normally forms such as:

`25 mm`

`220 V`

`11 kW`

`50 Hz`

Distinguish between a unit name in prose and its standard unit symbol.

---

# 26. Standards and Specifications

Keep official identifiers unchanged.

Examples:

- ISO 9001
- IEC 61131-3
- IEEE 802.11
- ASTM D3039
- ASME B31.3
- RFC 9110

The surrounding explanation may be Persian.

Never alter the identifier of a standard.

---

# 27. Preserve Technical Distinctions

Do not collapse distinct engineering concepts merely because they can receive similar Persian translations.

Pay special attention to distinctions such as:

- Accuracy / Precision
- Stress / Pressure
- Force / Load
- Verification / Validation
- Stiffness / Strength
- Error / Uncertainty
- Mesh / Grid
- Node / Vertex
- Throughput / Bandwidth
- Latency / Response Time
- Availability / Reliability
- Authentication / Authorization
- Process / Thread
- Container / Virtual Machine

Technical precision takes priority over vocabulary simplification.

---

# 28. Preserve Authorial Meaning

Do not introduce unsupported technical claims merely because they sound useful.

Do not:

- change technical conclusions;
- invent examples;
- add unsupported recommendations;
- modify numerical results;
- strengthen uncertain claims;
- weaken qualifications;
- delete important limitations;
- silently correct ambiguous technical content using guesswork.

Preserve the author's intended meaning.

If source material is ambiguous, edit conservatively.

---

# 29. Persian and English Editions Are Related, Not Identical

The Persian edition must preserve the same technical meaning as the English edition when the English edition is authoritative.

It does NOT need to mirror English sentence structure.

Preserve:

- meaning;
- technical claims;
- examples;
- relationships;
- conceptual progression;
- equations;
- references;
- code.

Rewrite sentences naturally for Persian readers.

Do not force sentence-by-sentence literal equivalence.

---

# 30. When Persian and English Versions Disagree

When both language versions exist and appear inconsistent:

1. Inspect surrounding context.
2. Inspect related chapters.
3. Determine whether one version is outdated, mistranslated, or intentionally different.
4. Preserve technical correctness.
5. Align only when the authoritative meaning is reasonably clear.

Do not blindly overwrite the Persian version based on superficial sentence similarity.

If the discrepancy cannot be safely resolved:

- preserve the safest existing meaning;
- report the discrepancy after editing.

---

# 31. Preserve Document Structure

Unless restructuring is explicitly requested, preserve:

- chapter order;
- section order;
- heading hierarchy;
- anchor IDs;
- cross-references;
- Markdown structure;
- MDX structure;
- code blocks;
- tables;
- admonitions;
- links;
- images;
- figure references;
- footnotes;
- citations;
- metadata/frontmatter.

Do not break documentation tooling or static-site generation.

Before changing syntax that appears structural, inspect how the project uses it.

---

# 32. Respect the Documentation Framework

Determine whether the project uses:

- Markdown;
- MDX;
- HTML;
- Docusaurus;
- MkDocs;
- VitePress;
- Astro;
- custom components;
- another documentation system.

Do not introduce incompatible markup.

Prefer existing components and conventions.

---

# 33. Improve Existing Persian, Not Only Translated English

The task is not limited to translating English text.

When reviewing existing Persian content, improve:

- awkward Persian;
- literal translations;
- grammatical problems;
- weak sentence structure;
- inconsistent technical terminology;
- unnecessary English;
- over-translated terminology;
- unclear explanations;
- repetitive wording;
- incorrect نیم‌فاصله;
- punctuation;
- inconsistent headings.

However, do not rewrite technically correct passages merely to make them stylistically different.

---

# 34. Searchability Matters

Preserve English where replacing it with Persian would materially reduce the reader's ability to search:

- official documentation;
- error messages;
- RFCs;
- GitHub issues;
- scientific papers;
- API references;
- configuration documentation;
- upstream software documentation.

Searchability is an important editorial consideration, but not a justification for retaining unnecessary English prose.

---

# 35. Book-Wide Terminology Consistency

Treat terminology as book-wide state.

If an earlier chapter establishes a term, later chapters should normally follow that convention.

Before introducing a new Persian translation or retained-English form, search existing chapters.

Use:

> **one concept → one preferred designation**

whenever technically possible.

Do not use different translations merely for stylistic variety.

When one English term has different meanings across engineering domains, allow domain-specific terminology decisions.

---


# 36. Human-Reviewed Calibration and Review State

Treat human review state as persistent editorial metadata.

For Tahmures:

- Persian Chapters 01–09 are the human-reviewed calibration corpus.
- Persian Chapters 10–24 are not yet human-reviewed.
- Findings validated in Chapters 01–09 apply as preventive review rules to
  Chapters 10–24.
- Applying those rules to Chapters 10–24 does not make those chapters
  human-reviewed.

When `editorial/review-status.yml` exists, use it as the machine-readable review-state
record.

Use these states distinctly:

- `unreviewed`
- `machine_prechecked`
- `human_reviewed`

Never infer `human_reviewed` from:
- a successful build;
- a successful validator;
- a model review;
- a translation synchronization check;
- absence of warnings.

Only explicit human review may establish `human_reviewed`.

Human review findings should be converted into reusable regression cases when they
represent a general failure class.

---

# 37. Persian Syntactic and Semantic Integrity

A sentence that is fluent but syntactically or semantically malformed fails review.

Do not evaluate Persian quality token by token. Evaluate the complete grammatical and
semantic structure.

For every materially revised sentence, preserve or intentionally resolve:

- actor;
- action;
- object;
- recipient;
- reference;
- causality;
- condition;
- negation;
- modality;
- uncertainty;
- comparison;
- temporal relation;
- quantity;
- exception;
- limitation.

Check that Persian word order expresses the intended relation rather than copying
English word order.

If the source relationship is compressed and Persian requires an explicit relation,
use a natural Persian construction only when it preserves the source meaning. Examples
of relationship markers that may be appropriate depending on context include:

- `از جنس`
- `حاوی`
- `برای`
- `متعلق به`
- `مربوط به`

Do not add a relation that is not supported by the source meaning.

Editorial priority:

```text
technical correctness
→ factual correctness
→ semantic fidelity
→ Persian syntactic integrity
→ adjective/adverb integrity
→ terminology correctness
→ fluency
→ stylistic elegance
```

Never trade an earlier priority for a later one.

---

# 38. Modifier, Ezafe, Adjective, and Adverb Integrity

The integrity of modifiers is mandatory.

## 38.1 موصوف و صفت

For every adjective or adjectival expression, determine:

1. the intended head noun;
2. whether the adjective is descriptive, restrictive, classificatory, or technical;
3. whether the Persian order is natural;
4. whether the adjective scope changed during translation;
5. whether an English technical adjective should remain English, be translated, or
   become part of a defined technical expression.

Reject malformed head–modifier order even if the individual words are correct.

## 38.2 مضاف و مضاف‌الیه and ezafe

Check every important noun chain for:

- identifiable head;
- meaningful ezafe relation;
- correct ordering;
- unambiguous attachment;
- absence of English-style noun stacking that produces malformed Persian.

Do not assume a sequence of translated nouns forms a meaningful Persian noun phrase.

## 38.3 Adverb position and scope

For every consequential adverb or adverbial expression, determine:

- which verb, adjective, or clause it modifies;
- whether its position is natural in Persian;
- whether moving it changes negation;
- whether moving it changes degree;
- whether moving it changes frequency;
- whether moving it changes temporal meaning;
- whether moving it changes uncertainty or modality.

Adverb scope errors are semantic errors, not merely style issues.

## 38.4 Multiple modifiers

When a noun or clause has multiple modifiers:

- preserve semantic hierarchy;
- avoid attachment ambiguity;
- do not reproduce English modifier order mechanically;
- split or expand the phrase when Persian requires clearer relations.

---

# 39. Mixed Persian-English Grammar

Retained English terminology must live inside Persian grammar.

The presence of a valid English technical term does not justify malformed Persian
syntax.

Check especially:

- English noun + Persian plural suffix;
- English adjective + Persian noun;
- Persian adjective + English noun;
- English multiword term inside an ezafe chain;
- Persian suffixes attached directly to Latin text;
- mixed lists containing literal identifiers and ordinary prose;
- code-like field names embedded in Persian instructions.

When a literal identifier is intended, preserve it exactly and structure Persian prose
around it.

Do not translate literal identifiers merely to improve fluency.

When a retained English term is ordinary prose rather than a literal token, use the
project's term/tooltip mechanism where supported.

Avoid mixed constructions whose grammatical relation is only recoverable by mentally
reconstructing the English source.

---

# 40. Reference and Citation Identity Parity

The Persian edition must not silently lose evidence that supports a shared canonical
English claim.

Do not compare only the number of references.

For each corresponding English/Persian chapter, compare recognizable citation
identities such as:

- citation keys;
- DOI identifiers;
- source URLs;
- stable reference anchors.

For claims preserved from English into Persian, require conceptually:

```text
english_required_citations ⊆ persian_citations
```

Persian may contain additional sources when justified.

Equal citation counts with different identities do not establish parity.

If the editions legitimately differ in claims, investigate before forcing citation
identity. Do not add a citation to Persian merely to satisfy a count when the
corresponding claim is absent.

When a citation cannot be machine-identified, report the limitation for human review
rather than inventing parity.

---

# 41. Human-Approved Wording Protection

Human-approved Persian wording is editorially authoritative unless a concrete reason
requires change.

Do not replace human-approved wording merely because:

- another sentence resembles English syntax more closely;
- another wording is stylistically different;
- a model prefers a more literal translation;
- automated translation produces a different sentence.

Change human-approved wording only when justified by one or more of:

- factual error;
- technical error;
- grammatical error;
- terminology conflict;
- broken citation/reference;
- broken link/anchor;
- contradiction with a later explicit instruction;
- contradiction with canonical project meaning.

When the English source changes after human review:

1. compare meaning;
2. identify the actual delta;
3. preserve unaffected human-approved Persian;
4. update only what the English change makes necessary;
5. re-run the regression and translation checks.

---

# 42. Editing Workflow

For each target Persian chapter, perform this workflow.

## Step 1 — Preflight

Read project instructions, repository context, book structure, glossary, review-state
files, human regression cases, and relevant chapters.

## Step 2 — Determine review status

Determine whether the target chapter is:

- `human_reviewed`;
- `machine_prechecked`;
- `unreviewed`.

Do not downgrade or falsely upgrade review status.

## Step 3 — Read the chapter completely

Understand the chapter before changing individual sentences.

## Step 4 — Read the corresponding English chapter and neighboring context

Use English for canonical technical meaning, not as a sentence-order template.

## Step 5 — Identify protected content

Mark code, identifiers, formulas, paths, commands, standards, units, source URLs,
literal fields, and other exact technical material.

## Step 6 — Check reference identity parity

Compare recognizable citations/URLs/keys for shared canonical claims. Investigate
mismatches before editing references.

## Step 7 — Build local terminology context

Identify important Latin-script expressions and existing Persian terminology. Load
the project glossary and terminology candidate registry.

## Step 8 — Classify terminology

Assign:

- `PRESERVE_EXACT`
- `RETAIN_ENGLISH`
- `TRANSLATE_PERSIAN`
- `TRANSLITERATE_PERSIAN`
- `REVIEW`

Treat candidate terms as contextual candidates, not unconditional rules.

## Step 9 — Apply human regression knowledge

Check the chapter against validated failure classes in
`editorial/fa-review/regression-cases.yml`.

Do not blindly replace a matching fragment when its case is marked `flag_only`.

## Step 10 — Perform syntactic and semantic integrity review

Check:

- actor/action/object relations;
- موصوف و صفت;
- مضاف و مضاف‌الیه;
- ezafe chains;
- adjective scope;
- adverb position and scope;
- negation, condition, modality, comparison, causality, and quantity;
- pronoun/reference clarity;
- list and coordination parallelism;
- mixed Persian-English grammar.

## Step 11 — Improve Persian prose

Rewrite awkward, literal, fragmented, semantically compressed, or inconsistent Persian
while preserving technical meaning and human-approved wording.

## Step 12 — Normalize headings

Apply the Persian-first heading policy without breaking anchors, routes, navigation, or
cross-references.

## Step 13 — Apply retained-term treatment

Use the project's tooltip/term mechanism for `RETAIN_ENGLISH` prose expressions.
Do not insert markup into protected content.

## Step 14 — Check cross-chapter consistency

Reuse established terminology, definitions, and conceptual distinctions.

## Step 15 — Compare important technical statements

Check the corresponding English edition and source evidence when the meaning or claim
is consequential.

## Step 16 — Validate structure and deterministic invariants

Verify Markdown/MDX/HTML syntax, links, anchors, code, formulas, tables, metadata,
protected-content parity, reference parity, translation synchronization, and review
status.

## Step 17 — Re-read as continuous Persian prose

Judge the result as a Persian engineering chapter, not as a collection of translated
sentences. Re-check adjective and adverb scope during the final reread.

## Step 18 — Perform the final validation pass

Run applicable repository validators. Do not finish immediately after rewriting.

# 43. Deterministic Post-Edit Validation

After editing, conceptually perform this validation pipeline:

```text
Persian content
    ↓
determine review state
    ↓
compare citation identities with canonical English
    ↓
identify and exclude protected regions
    ↓
run known regression cases
    ↓
identify Latin-script spans in prose
    ↓
classify remaining Latin prose
    ↓
verify every RETAIN_ENGLISH prose term
    ↓
verify tooltip coverage
    ↓
check mixed Persian-English grammar
    ↓
check موصوف/صفت and ezafe structure
    ↓
check adjective and adverb scope
    ↓
check semantic roles, negation, condition, modality, causality, and quantity
    ↓
compare terminology with glossary/book precedent
    ↓
check Persian-first headings
    ↓
check code / formula / identifier / URL preservation
    ↓
check Markdown / MDX / HTML integrity
    ↓
final continuous Persian readability review
```

Do not merely perform search-and-replace.

When repository tooling exists, run the relevant lint, formatting, build, or documentation validation commands when appropriate.

---

# 44. Final Validation Checklist

Before finishing an edited file, verify all applicable items.

## Project context

- [ ] `AGENTS.md` was considered.
- [ ] `README.md` was considered.
- [ ] This policy was followed.
- [ ] Relevant neighboring chapters were inspected.
- [ ] The corresponding English chapter was checked when useful.
- [ ] Existing glossary/terminology conventions were inspected.

## Persian quality

- [ ] Persian sentences read naturally.
- [ ] Persian grammar and word order are professional.
- [ ] Every consequential adjective modifies the intended noun.
- [ ] Adjective scope is preserved.
- [ ] Adverb position is natural and adverb scope is preserved.
- [ ] موصوف/صفت ordering is meaningful.
- [ ] مضاف/مضاف‌الیه and ezafe chains are meaningful.
- [ ] Mixed Persian-English phrases obey Persian grammar.
- [ ] Actor/action/object, negation, condition, modality, causality, and quantity are preserved.
- [ ] نیم‌فاصله is consistent.
- [ ] Persian punctuation is correct.
- [ ] Literal translation artifacts were removed.
- [ ] Unnecessary repetition was reduced.
- [ ] The prose does not feel artificially literary or conversational.

## Terminology

- [ ] Ordinary English prose was translated when appropriate.
- [ ] Important English engineering terminology remains recognizable where needed.
- [ ] Technical terms were not over-translated.
- [ ] Transliteration is intentional rather than a fallback.
- [ ] Established terminology was reused.
- [ ] Distinct engineering concepts were not collapsed.
- [ ] No new terminology convention was invented unnecessarily.

## Tooltips

- [ ] Every `RETAIN_ENGLISH` prose term uses the configured term/tooltip mechanism where supported.
- [ ] Tooltip text is Persian.
- [ ] Tooltip definitions explain contextual meaning.
- [ ] Definitions are concise and technically correct.
- [ ] Repeated concepts use consistent definitions.
- [ ] No tooltip markup was inserted inside protected technical content.

## Bidi

- [ ] Persian prose remains logically RTL.
- [ ] Retained English terminology renders as LTR where required.
- [ ] Punctuation was not manually reordered.
- [ ] No unnecessary invisible bidi characters were introduced.

## Headings

- [ ] Persian headings are Persian where natural and technically correct.
- [ ] Entire English headings were not retained unnecessarily.
- [ ] Important technical identities remain recognizable.
- [ ] Heading hierarchy is unchanged.
- [ ] Anchors and internal links remain valid.
- [ ] Navigation and table-of-contents terminology remains consistent.

## Evidence and reference integrity

- [ ] Shared canonical claims have not silently lost supporting citation identities.
- [ ] Reference parity was compared by identity where machine-readable identities exist.
- [ ] Persian-only additional references are justified rather than deleted for count equality.
- [ ] Unverifiable citation mappings were reported rather than guessed.

## Human-review integrity

- [ ] Human-reviewed Chapters 01–09 were not retranslated wholesale.
- [ ] Human-approved wording was preserved unless a concrete correctness reason required change.
- [ ] Chapters 10–24 were not falsely described as human-reviewed.
- [ ] New generalizable human corrections were added to the regression corpus when appropriate.

## Technical integrity

- [ ] Code is unchanged unless explicitly authorized.
- [ ] Commands are unchanged.
- [ ] Identifiers are unchanged.
- [ ] Paths and URLs are unchanged.
- [ ] API spelling is unchanged.
- [ ] Equations preserve exact technical meaning.
- [ ] Numerical values are unchanged.
- [ ] Units and symbols are preserved.
- [ ] Standards and official identifiers are preserved.
- [ ] Important qualifiers and limitations remain intact.
- [ ] No unsupported technical claim was introduced.

## Repository integrity

- [ ] Only intended files were modified.
- [ ] Markdown/MDX/HTML syntax remains valid.
- [ ] Existing components and conventions were respected.
- [ ] No unrelated source files were reformatted.
- [ ] Generated files were not modified unless required.
- [ ] Relevant validation/build commands were run when available and appropriate.

---

# 45. Failure-Safe Behavior

If `AGENTS.md` does not exist:

- continue using `README.md` and repository context;
- report the missing instruction file if relevant.

If `README.md` does not exist:

- inspect the repository structure directly;
- continue conservatively;
- report the missing context if relevant.

If no glossary exists:

- do not create one automatically unless requested;
- maintain terminology consistency internally during the task.

If a terminology decision is uncertain:

- search project context;
- preserve technically safe wording;
- report the unresolved term.

If Persian and English chapters disagree technically:

- do not silently choose one;
- investigate context;
- preserve the safest interpretation;
- report unresolved discrepancies.

If the tooltip markup is unsupported:

- do not insert broken or literal markup;
- preserve safe linguistic edits;
- report the rendering limitation.

If an existing tooltip convention exists:

- use it instead of introducing another one.

If broad automated replacement threatens protected content:

- stop global replacement;
- edit only verified prose occurrences.

---

# 46. Scope Discipline

When asked to improve the Persian book:

- modify only files relevant to the requested scope;
- do not modify the English edition unless explicitly required;
- do not make unrelated repository changes;
- do not perform repository-wide cosmetic reformatting;
- do not change generated files unless project conventions require it.

Keep edits focused.

---

# 47. Final Response After Editing

After modifying files, provide a concise report containing only relevant items such as:

- files changed;
- major terminology decisions;
- important heading changes;
- significant English terms retained;
- significant terms converted to Persian;
- unresolved terminology;
- Persian/English technical discrepancies;
- tooltip/rendering issues;
- validation/build commands executed;
- validation failures, if any.

Do not paste entire edited chapters into the response unless requested.

---

# 48. Core Editorial Principle

The desired result is NOT:

> An English engineering book translated word-by-word into Persian.

The desired result IS:

> A professional Persian engineering book that uses Persian naturally while retaining the exact English terminology that Persian-speaking engineers need to recognize, search, configure, implement, and encounter in real engineering practice.

In practical terms:

> **Write Persian as Persian. Preserve English only when preserving it has a concrete technical purpose. Preserve exact technical tokens exactly.**

Every editing decision should support that goal.
