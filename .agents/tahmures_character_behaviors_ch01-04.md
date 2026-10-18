# Tahmures — Character Behavior Sheets, Chapters 01–04

**Status:** `DRAFT_ADAPTATION_REFERENCE_PENDING_HUMAN_APPROVAL`
**Phase:** `CH01_04_CHARACTER_NARRATIVE_REFACTOR` (bounded corrections to the `CH01_04_CHARACTER_REFERENCE_PACK` output)
**Date:** 2026-10-10
**Prepared by:** GLM (implementation agent). GPT performed the independent reference review; the bounded corrections it required were applied on 2026-10-10. Next gate: human approval of the adapted names, behavior wording, and tooltip copy. This file does not record that approval.

## What this file is

- A proposed adaptation reference for the approved Chapter 01–04 cast mapping. The
  human approved the name mappings and chronology substitutions recorded here, but
  has **not** approved the resulting behavior sheets, visual prompts, generated art,
  or rewritten chapter text.
- `book/narrative-continuity.md` remains the continuity source of truth until a
  later approved manuscript-revision phase updates it. This file does not compete
  with it and does not authorize any manuscript edit.
- The narration-refactor phase (2026-10-10) applied this mapping to the Chapter 01–04 tale sections, closing hooks, and continuity record in both editions, and implemented the site tooltips. Those manuscript changes are pending renewed GPT and human review; the historical human review of Persian Chapters 01–09 covers the previous revision only.
- A "chapter role" below describes this book's adaptation, never a claim about
  Ferdowsi or another source tradition. The four-chapter episodes remain original
  teaching fiction (`narrative_origin: original-teaching-fiction`).

## Label legend

| Label | Meaning |
|---|---|
| `TIER_A_SHAHNAMEH_EXPLICIT` | Mythic identity explicit in the relevant *Shahnameh* material per the supplied dossier and live skill references. Verse-level citation is still pending for any publication-facing source claim. |
| `TIER_B_LATER_TRADITION` | Identity attested in later or parallel tradition (Avestan, Pahlavi, Rivayat, or unversified legend); not established as a *Shahnameh* verse claim from the supplied references. |
| `UNVERIFIED_SOURCE_LEAD` | Possible identity not established by the supplied references; do not assert it as a source fact. |
| `NOT_APPLICABLE_OCCUPATIONAL_ROLE` | An occupational word, not a mythic person. |
| `TIER_C_PROJECT_FICTION` | The character's appearance, role, and actions in this book's chapters. |
| `UNVERIFIED_SOURCE_DETAIL` | A specific source detail that the supplied references do not establish; kept out of the sheets except as a flagged caution. |
| `GPT_REVIEW_REQUIRED` | Open question deliberately left for the next review gate. |

Every named figure below carries **two separate classifications**: (1) mythic source
identity with tier, and (2) chapter appearance and educational role as
`TIER_C_PROJECT_FICTION`. Tier B or C material never becomes Tier A through
repetition, and no source event is claimed for the adapted episodes.

## 1. Roster summary

| # | English name | Persian (proposed) | Former role in live text (EN / FA) | Chapters | Mythic source tier | Chapter role |
|---|---|---|---|---|---|---|
| 1 | Tahmures | طهمورث | Tahmures / تهمورث | 01–04 | `TIER_A_SHAHNAMEH_EXPLICIT` | Continuous protagonist-learner |
| 2 | Shahrasp | شهراسپ | First Scribe / دبیر نخست | 01–04 | `TIER_A_SHAHNAMEH_EXPLICIT` | First Scribe (keeper of the experiment ledger) |
| 3 | Akvan Div | اکوان دیو | Keeper of Scripts / نگهبان دبیره‌ها | 01, 04 | `TIER_A_SHAHNAMEH_EXPLICIT` (later-cycle div) | Keeper of Scripts |
| 4 | Black Div | دیو سیاه | Literal Div / دیو لفظ‌گرا | 01, 04 | `TIER_A_SHAHNAMEH_EXPLICIT` (unnamed figure; personal identity is adaptation) | Literal Div |
| 5 | Div-e Sefid | دیو سپید | Mirror Div / دیو آینه | 01 (hook), 02 | `TIER_A_SHAHNAMEH_EXPLICIT` (later-cycle div) | Mirror Div |
| 6 | Arzhang Div | ارژنگ دیو | the council's div / دیو شورا | 03 | `TIER_A_SHAHNAMEH_EXPLICIT` (later-cycle div) | Council's Div |
| 7 | Soroush | سروش | Archivist / بایگان | 02, 03 (hook), 04 | `TIER_B_LATER_TRADITION` (Avestan yazata) | Archivist |
| 8 | Simurgh | سیمرغ | Messenger / پیام‌رسان | 01 | `TIER_A_SHAHNAMEH_EXPLICIT` (Zal/Rostam-cycle bird) | Messenger |
| 9 | Arash | آرش | northern/present captain, captain, Gatekeeper / سردار کنونی، فرمانده، دروازه‌بان | 01, 03, 04 (+ Ch01 illustrative Gatekeeper) | `TIER_B_LATER_TRADITION` (border-archer legend) | Current captain / Gatekeeper |
| 10 | Garshasp | گرشاسپ | a captain who served Tahmures's father (offstage) / «یکی از سرداران زمان پدرتان» | 01 | `TIER_B_LATER_TRADITION` | Remembered captain of the prior court |
| 11 | Jamshid | جمشید | eastern governor (02), treasurer (03), former governor letter author (04) / فرماندار، خزانه‌دار، فرماندار پیشین | 02, 03, 04 | `TIER_A_SHAHNAMEH_EXPLICIT` (successor generation) | Governor / treasurer / former governor |
| 12 | Budhasaf | بوداسب | western governor (02) / فرماندار | 02 | `UNVERIFIED_SOURCE_LEAD` | Governor with a competing claim |
| 13 | Keyumars | کیومرث | builder (03), the king dead six years (04) / سازنده، آن شاه | 03, 04 | `TIER_A_SHAHNAMEH_EXPLICIT` (primordial king) | Builder / deceased king |
| 14 | Nariman | نریمان | flood keeper / نگهبان سیلاب | 03 | `TIER_A_SHAHNAMEH_EXPLICIT` (Sistani lineage forebear) | Flood-affected council member (stakeholder) |
| 15 | Sam | سام | orchard keeper / نگهبان میوه‌ستان | 04 | `TIER_A_SHAHNAMEH_EXPLICIT` (Sistani lineage champion) | Orchard-affected person |
| 16 | Chapar | چاپار | courier / پیک | 01 | `NOT_APPLICABLE_OCCUPATIONAL_ROLE` | Courier (short role entry, §3.16) |

## 2. Persian naming status

| English | Proposed Persian | Status |
|---|---|---|
| Tahmures | طهمورث | Applied in this batch by the owner's scoped spelling alignment (2026-10-10): Persian Chapters 01–04 use طهمورث in prose and the four tale headings («روایت طهمورث»); the translation validator enforces the heading per chapter range. Chapters 05–24 and `book/fa/translation-glossary.md` keep تهمورث pending a separate book-wide terminology decision; this is not a glossary promotion. |
| Chapar | چاپار | Settled by the approved mapping (occupational role). |
| Shahrasp | شهراسپ | Recommended project form per GPT review (2026-10-10): شهراسپ is the dossier's main Persian form; شهرسپ appears in the quoted verse and remains a signoff note. No glossary entry exists yet; promotion is out of scope for this batch. |
| Akvan Div | اکوان دیو | `GPT_REVIEW_REQUIRED`. Proposed form from the supplied dossier; no established project form exists. |
| Black Div | دیو سیاه | `GPT_REVIEW_REQUIRED`. Proposed form; the personal identity itself is an adaptation (see §3.4). |
| Div-e Sefid | دیو سپید | `GPT_REVIEW_REQUIRED`. Proposed form from the supplied dossier. |
| Arzhang Div | ارژنگ دیو | `GPT_REVIEW_REQUIRED`. Proposed form from the supplied dossier. |
| Soroush | سروش | `GPT_REVIEW_REQUIRED`. Proposed form; no established project form exists. |
| Simurgh | سیمرغ | `GPT_REVIEW_REQUIRED`. Proposed form from the supplied dossier. |
| Arash | آرش | `GPT_REVIEW_REQUIRED`. Proposed form; no established project form exists. |
| Garshasp | گرشاسپ | `GPT_REVIEW_REQUIRED`. Proposed form from the supplied dossier. |
| Jamshid | جمشید | `GPT_REVIEW_REQUIRED`. Proposed form (standard Persian; no project glossary entry yet). |
| Budhasaf | بوداسب | `GPT_REVIEW_REQUIRED`. Proposed form mirrors the dossier's `Būdasb / بوداسب` note; the underlying identity is unverified (§3.12). |
| Keyumars | کیومرث | `GPT_REVIEW_REQUIRED`. Proposed form from the supplied dossier. |
| Nariman | نریمان | `GPT_REVIEW_REQUIRED`. Proposed form from the supplied dossier. |
| Sam | سام | `GPT_REVIEW_REQUIRED`. Proposed form from the supplied dossier. |

The current Persian live-text role labels (دبیر نخست، نگهبان دبیره‌ها، بایگان، پیام‌رسان، دیو لفظ‌گرا، دیو آینه، دروازه‌بان، خزانه‌دار، فرمانده، نگهبان سیلاب، سازنده، پیک، فرماندار) were inspected directly in both editions; they are recorded per sheet below and must not be mechanically retranslated in a later revision.

## 3. Behavior sheets

### 3.1 Tahmures

**Approved display name.** English: Tahmures. Persian: طهمورث (applied in Chapters 01–04 prose and tale headings by the owner's scoped spelling alignment, 2026-10-10; Chapters 05–24 and the glossary keep تهمورث — see §2).

**Former role and exact appearances.** The named protagonist of all four tales (Chapter 01 "The Three Readings", 02 "The Mirror and the Missing Treaty", 03 "The Bridge of Five Virtues", 04 "The Letter Inside the Ledger"); named in both editions throughout.

**Mythic source identity, tier, basis.** Tahmuras, third Pishdadian king, son and successor of Hushang, binder of the divs, who learns writing from the spared divs — `TIER_A_SHAHNAMEH_EXPLICIT`, supported by the supplied dossier (Tahmures episode, including quoted verses and the div-binding and writing motifs) and by the live skill canon reference. The dossier's later-tradition additions (Merv/Shiraz founder attributions, death stories, unnamed-wife material) are Tier B and are not used here.

**Project-fiction role and chronology adaptation.** Tahmures remains the continuous protagonist: a fallible ruler-learning engineer whose victories are investigative, not martial. In this book he never solves a failure through unexplained magic or arbitrary command (fictional-world rule 5). No chronology shift is needed for Tahmures himself; the shifts concern the figures around him (recorded per sheet).

**Chapter-by-chapter observable behavior and agency.**

- **Ch01:** Sets the river tablet on a cedar stand and asks three hall servants "Tell me what this is", expecting three descriptions of one object. His first remedy — ordering the First Scribe to lengthen the instruction — is stopped mid-reed when the Keeper warns that *means* would still carry too much weight. He then places four empty labels (*speaker*, *recipient*, *occasion*, *requested result*), recognizes that the fourth belongs to him rather than to the tablet, and has the real request written on a separate sealed card. He tests the method on other records and sends a second, shorter message north that names the recipient, corrects the rumour, and asks for acknowledgement.
- **Ch02:** Places the torn treaty before the Mirror Div and orders "Tell the council what the treaty says" — an answer-seeking request. On seeing the fluent completion take over the debate, he covers the missing section with blank leather and narrows the task ("Read only what remains", "How many jars are owed?", "That was not my question"). He runs further tests (gate days, witnesses, grain), accepts "The fragments are insufficient" as the useful answer, forbids nothing — inference is still allowed as marked hypothesis — and lets no jar move on a hypothesis's authority.
- **Ch03:** Asks the council's div to "Choose the best bridge", then escalates wording ("Consider everything and choose properly") before recognizing the wording was never the owner of the failure. He orders the five advisers to stop discussing bridges and name the failure they cannot accept, accepts the treasurer's public correction of his own conclusion, hangs named bronze weights on the balance so the council's values are inspectable, and issues a final request that names hard conditions, asks for surviving candidates, and requires the cost of each trade-off.
- **Ch04:** Gives the Literal Div a sealed tablet plus an archive bundle with the instruction to preserve every right granted after the last great flood. When Jamshid's expired letter is executed as current, he confronts both the div ("I gave you that as a record") and the Archivist, then reconstructs the bundle with the First Scribe through three questions (current task / may supply facts / authority today). He adopts the black cord, the *evidence, not command* labels, and separate current seals for renewed grants, tests the arrangement with a decoy market notice, and keeps Jamshid's letter as evidence without authority.

**Engineering lesson per appearance.**

- Ch01: a prompt is the whole structured interaction; grammar does not fix a text's role; test role labels before judging answers.
- Ch02: fluency is not evidence; separate written, inferred, and unknown; abstention is a useful output.
- Ch03: requirements precede wording; hard constraints disqualify, preferences rank; evaluation criteria belong to the stakeholders.
- Ch04: context is not instruction; packaging and authority boundaries are separate from prose quality.

**Hover descriptions (tooltip text — content only; readable as plain text).**

| Role | English | Persian |
|---|---|---|
| General | Ruler and learner who examines his own request and its setting before blaming those who answered. | فرمانروا و شاگردی که پیش از سرزنش پاسخ‌دهندگان، درخواست و چیدمان خودش را می‌کاود. |
| Ch01 | Discovers that grammar alone does not fix a text's role; labels speaker, recipient, occasion, and requested result. | درمی‌یابد که دستور زبان به‌تنهایی نقش متن را تعیین نمی‌کند؛ گوینده، گیرنده، موقعیت و نتیجهٔ درخواستی را برچسب می‌زند. |
| Ch02 | Separates what is written, inferred, and unknown, and accepts "insufficient evidence" as a useful answer. | نوشته‌شده، استنباط‌شده و نامعلوم را از هم جدا می‌کند و «شواهد کافی نیست» را پاسخی مفید می‌داند. |
| Ch03 | Finds that the council, not the wording, must define "best"; separates hard constraints from preferences. | درمی‌یابد که تعریف «بهترین» با شوراست، نه با واژه‌ها؛ شرط‌های سخت را از ترجیح‌ها جدا می‌کند. |
| Ch04 | Separates the current request from archived evidence so old words stay preserved without authority. | درخواست جاری را از شواهد بایگانی جدا می‌کند تا واژه‌های کهنه حفظ شوند، اما اختیار نگیرند. |

**Personality, voice, boundaries.** Direct, exact, increasingly questioning. He gives orders freely but learns to interrogate his own requests first. He is never omniscient: his initial instructions in all four chapters contain the chapter's seed defect. He does not blame divs by default and does not credit himself with automatic truth.

**Relationships and continuity.** Increasingly treats the First Scribe (Shahrasp) as an experimental partner; respects the Keeper (Akvan Div) for structural questions, the Archivist (Soroush) for provenance, and the Gatekeeper (Arash) for refusing unsafe action — consistent with the continuity record's long arc, here at its Part I stage.

**Unresolved items.** Persian spelling transition resolved for this batch (owner-authorized scoped alignment, 2026-10-10): Chapters 01–04 use طهمورث in prose and the four tale headings, and the translation validator is chapter-aware. Chapters 05–24 and the glossary keep تهمورث pending a separate book-wide terminology decision (§2).

### 3.2 Shahrasp — First Scribe

**Approved display name.** English: Shahrasp. Persian: شهراسپ (`GPT_REVIEW_REQUIRED`, see §2).

**Former role and exact appearances.** "The First Scribe" / «دبیر نخست» — Chapters 01, 02, 03, 04, in every tale section. He is not named in any of the four closing hooks (the Chapter 01 hook names the Keeper and the Mirror Div; Chapter 02's the two governors; Chapter 03's the Archivist; Chapter 04's the Gatekeeper).

**Mythic source identity, tier, basis.** Shahrasp is a **named counselor (pure *dastur*/vizier) of Tahmures in the Tahmures episode of the *Shahnameh*** — `TIER_A_SHAHNAMEH_EXPLICIT`, supported by the supplied dossier (which quotes the introduction of his name and his piety) and by the live skill canon reference, which explicitly allows him to counsel, warn, and test the king. **"First Scribe" is this project's adaptation**: the source tradition names him a counselor, not a scribe, and the live skill guidance warns against collapsing occupational roles into Shahrasp. The owner's approved mapping nevertheless assigns the First Scribe function to him for this batch; that decision is recorded here without presenting it as a source claim.

**Project-fiction role and chronology adaptation.** He is Tahmures's continuous recorder: prompts, predictions, variants, outcomes, corrections. He is a contemporary of Tahmures in the source episode, so no chronology shift is required — only the occupational adaptation from counselor to keeper of the experiment ledger.

**Chapter-by-chapter observable behavior and agency.**

- **Ch01:** Ordered to lengthen the ambiguous instruction, he sharpens his reed and is stopped. He adds the experiment ledger's first rule: *"Before judging the answer, record what each piece of language is doing here."*
- **Ch02:** On his **own initiative** ("though Tahmures had not asked for any") he leaves a source margin on the fresh ledger page. He challenges the Mirror Div directly ("Where are those words?", "On what tablet?"), then draws the three columns *written*, *inferred*, *unknown* and places the gate, the payment, and the amount in them. He closes the chapter's ledger line: *"A polished surface can reflect a bridge that is not behind you."*
- **Ch03:** Places the five advisers' statements into two columns — conditions that disqualify a design, and preferences that can be traded.
- **Ch04:** Reconstructs the archive table exactly; when asked "Which object states the current task?", he points to the seal.

**Engineering lesson per appearance.** Ch01: experiment tracking begins before judgment. Ch02: evidence bookkeeping (source margins, claim-status columns) is what makes grounding enforceable. Ch03: requirements become inspectable when sorted into hard constraints versus preferences. Ch04: reconstruction of what was actually bundled is the first debugging step.

**Hover descriptions (tooltip text — content only).**

| Role | English | Persian |
|---|---|---|
| General (approved starting point) | Keeps observations, sources, and decisions visible so Tahmures can examine and revise his judgment. This is the project role, not a source claim that Shahrasp was a scribe. | مشاهده‌ها، منبع‌ها و تصمیم‌ها را روشن و در دسترس نگه می‌دارد تا طهمورث بتواند داوری خود را بررسی و بازنگری کند. (این نقشِ پروژه است، نه ادعای منبع دربارهٔ شهراسپ.) |
| Ch01 | Opens the experiment ledger with the rule: record what each piece of language is doing before judging the answer. | دفتر آزمایش را با این قاعده آغاز می‌کند: پیش از داوری دربارهٔ پاسخ، ثبت کن هر قطعهٔ زبان چه می‌کند. |
| Ch02 | Adds a source margin and the written/inferred/unknown columns that separate polish from evidence. | حاشیهٔ منبع و ستون‌های نوشته‌شده، استنباط‌شده و نامعلوم را می‌افزاید تا صیقل از شاهد جدا شود. |
| Ch03 | Sorts the advisers' statements into disqualifying conditions and tradable preferences. | گفته‌های مشاوران را به شرط‌های ردکننده و ترجیح‌های قابل‌معامله تفکیک می‌کند. |
| Ch04 | Rebuilds the archive bundle exactly and points to the seal that carries the current task. | بستهٔ بایگانی را دقیقاً بازسازی می‌کند و به مُهری اشاره می‌کند که وظیفهٔ جاری را بیان می‌کند. |

**Personality, voice, boundaries.** Quiet, precise, mildly persistent. He records rather than rules: his power is making revision possible, not deciding outcomes. He does not validate truth by title — a record in his ledger is an observation, not a verdict.

**Relationships and continuity.** Becomes Tahmures's experimental partner across Part I (continuity record: ledger introduced in Ch01, source columns in Ch02, requirements in Ch03, bundle reconstruction in Ch04). His later-book development (Part II experimental partner, Part III system trace, Part IV release record) is untouched by this mapping.

**Unresolved items.** Persian spelling شهراسپ vs شهرسپ (§2). English text currently uses he/him for the First Scribe; Shahrasp's source identity is male, so no pronoun conflict arises, but the later revision must keep pronoun handling deliberate (see §6.4).

### 3.3 Akvan Div — Keeper of Scripts

**Approved display name.** English: Akvan Div. Persian: اکوان دیو (`GPT_REVIEW_REQUIRED`).

**Former role and exact appearances.** "Keeper of Scripts" / «نگهبان دبیره‌ها» — Chapter 01 (examines and catalogues the river tablet) and Chapter 04 (proposes red ink); also named in the Chapter 01 closing hook (opens the torn treaty).

**Mythic source identity, tier, basis.** Akvan Div is a **named div of the later Rostam/Kay Khosrow cycle of the *Shahnameh*** (per the supplied dossier: the div by the hidden spring whom Rostam defeats) — `TIER_A_SHAHNAMEH_EXPLICIT` as a named later-cycle div; verse-level citation pending. **His source identity and cycle must not be conflated with the Keeper of Scripts occupation**: nothing in the source tradition makes him a curator of scripts, and that chapter role is `TIER_C_PROJECT_FICTION`. This is a deliberate owner-approved **chronology shift**: a div of a later epic cycle appears in Tahmures's reign as a hall functionary.

**Project-fiction role.** Examiner of syntax, representation, labels, and structured expression (continuity record: "Grammar suggests but does not establish role. Formatting can communicate a boundary but cannot enforce authority.").

**Chapter-by-chapter observable behavior and agency.**

- **Ch01:** Examines the marks; enters the tablet in the catalogue under *Military Records: Northern Frontier*; explains "It is an old command. The hand resembles a captain who served your father" — a resemblance-based attribution offered as classification, not authentication. Independently warns, eyebrow raised, that the proposed longer instruction "still leaves *means* to carry a large burden."
- **Ch04:** Proposes red ink to mark current authority; the proposal is rejected on practical grounds (several scripts have no red), not on authority grounds.

**Engineering lesson per appearance.** Ch01: classification is a hypothesis about role; labels and hand-shape resemblance do not authenticate a source. Ch04: a representation convention only works if every consumer can render it — marking schemes must survive the whole system.

**Hover descriptions (tooltip text — content only).**

| Role | English | Persian |
|---|---|---|
| General (approved starting point) | Classifies and organizes written forms; a label does not make text authoritative. | دبیره‌ها را طبقه‌بندی و سامان می‌دهد؛ برچسب، متن را صاحب‌اختیار نمی‌کند. |
| Ch01 | Catalogues the river tablet as a military record and warns that "means" still carries too much weight. | لوح رود را در فهرست اسناد نظامی ثبت می‌کند و هشدار می‌دهد که واژهٔ «معنا» هنوز بار سنگینی بر دوش دارد. |
| Ch04 | Proposes red ink to mark authority; the marking fails where scripts have no red. | جوهر قرمز را برای نشان‌گذاری اختیار پیشنهاد می‌کند؛ نشانه‌گذاری آن‌جا می‌شکند که دبیره‌ای قرمز ندارد. |

**Personality, voice, boundaries.** Orderly, dryly skeptical, professionally careful. Not a villain and not a mere clerk: her classifications shape what the court can see, and she knows their limits. She never claims her catalogue entries prove authority.

**Relationships and continuity.** Continuity record lists the Keeper in Chapters 1, 4, 7, 8, 18; within this batch, 01 and 04. Structural counterpart to the Archivist (form versus provenance).

**Unresolved items.** The original English text used **she/her** for the Keeper of Scripts. GPT review (2026-10-10) directed keeping the existing English pronouns as project-fiction presentation for this batch; the revised chapters keep she/her, pending human signoff (§6.4).

### 3.4 Black Div — Literal Div

**Approved display name.** English: Black Div. Persian: دیو سیاه (`GPT_REVIEW_REQUIRED`).

**Former role and exact appearances.** "Literal Div" / «دیو لفظ‌گرا» — Chapter 01 (reads the tablet, crosses the river, counts the watchfires) and Chapter 04 (prepares and delivers the canal order; later passes the labelled-bundle tests).

**Mythic source identity, tier, basis.** The *Shahnameh*'s Tahmures episode describes a **black div at the front of the rebel host against Tahmures, without giving him a personal name** — `TIER_A_SHAHNAMEH_EXPLICIT` for the unnamed figure's presence in the episode (per the supplied dossier's dedicated entry, which explicitly records that the poem supplies no name, lineage, motive, or independent fate). **The personal identity given to the Black Div here — a named hall servant with the Literal Div function — is an adaptation of a figure described without a personal name** (`TIER_C_PROJECT_FICTION`), not a claim that Ferdowsi named or characterized him. Nothing in his behavior, personality, or visual design may be attributed to the source.

**Project-fiction role.** Follows surface wording while exposing missing role and authority structure (continuity record; also appears in Chapter 13, outside this batch). Explicitly **not** portrayed as malicious.

**Chapter-by-chapter observable behavior and agency.**

- **Ch01:** Reads the sentence twice and leaves without speaking — then, on his own reading of the imperative, returns at dusk soaked to the waist having crossed the river: "There are eleven watchfires." Pressed, he answers "The tablet said to count them" / "The tablet asked for a count." The eleven fires are charcoal burners; the false alarm is caused by the missing role labels, not by lies.
- **Ch04:** Before dawn he delivers "a beautiful tablet" directing the Gatekeeper to send the first water to the old garden — executing an expired record that was bundled without role labels. Challenged, he defends his reading: "You gave me a pile… It told me to use the records. This record told its reader where to send the water." After the black-cord arrangement, he **passes every test**: he reports the market notice ("Carry this tablet immediately to the northern gate") as history without carrying it away, reports the expired canal order without applying it, and returns an undated, unreadably sealed grant for review rather than guessing.

**Engineering lesson per appearance.** Ch01: an imperative inside unlabeled data will be followed by a literal agent; the defect is the interface, not the div. Ch04: instruction/data separation, provenance labels, and a defined escalation state ("return for review") repair the failure without changing the div.

**Hover descriptions (tooltip text — content only).**

| Role | English | Persian |
|---|---|---|
| General (approved starting point) | Follows surface wording while exposing missing role and authority structure. | به ظاهر واژه‌ها پایبند است و نبودِ ساختار نقش و اختیار را آشکار می‌کند. |
| Ch01 | Counts eleven watchfires across the river because the tablet said to count them; the missing role labels did the rest. | چون لوح گفته بود آتش‌ها را بشمار، از رود گذشت و یازده آتش شمرد؛ بقیهٔ ماجرا نبودِ برچسب‌های نقش بود. |
| Ch04 | Turns a pile of records into an order, then reports imperative notices as history once roles are labelled. | از توده‌ای از اسناد فرمان می‌سازد؛ اما وقتی نقش‌ها برچسب خوردند، اعلان‌های امری را به‌عنوان تاریخ گزارش می‌کند. |

**Personality, voice, boundaries.** Earnest, literal, industrious, oddly literal-minded proud. He is neither trickster nor villain: the same agent that caused both failures also passes all three later tests once structure exists. A Div's mistake does not make every failure a Div's fault — in both chapters the primary owner is elsewhere (interface design; context packaging plus action boundary).

**Relationships and continuity.** Continuity record lists the Literal Div in Chapters 1, 4, 13; within this batch, 01 and 04. His Ch04 improvement shows the arrangement working, which the later-book continuity (Ch13 return) can build on.

**Unresolved items.** None specific beyond the Persian spelling and the global name-collision caution: he must never be equated with Ahriman or described as the *named* commander of the source rebellion (the source figure is unnamed).

### 3.5 Div-e Sefid — Mirror Div

**Approved display name.** English: Div-e Sefid. Persian: دیو سپید (`GPT_REVIEW_REQUIRED`).

**Former role and exact appearances.** "Mirror Div" / «دیو آینه» — Chapters 01 (closing hook only) and 02 (restores the treaty's missing middle).

**Mythic source identity, tier, basis.** Div-e Sefid is the **White Div of Mazandaran of the later Rostam cycle** (per the supplied dossier: the div who blinds and holds Kay Kavus until Rostam's labor defeats him) — `TIER_A_SHAHNAMEH_EXPLICIT` as a named later-cycle div; verse citation pending. **His source identity and cycle must not be conflated with the Mirror Div occupation**: the fluent-completion function is `TIER_C_PROJECT_FICTION`, and nothing in the source episode is retold here. Owner-approved **chronology shift**: a later-cycle div appears in Tahmures's reign as the court's mirror.

**Project-fiction role.** Produces exceptionally coherent completion without guaranteeing support (continuity record). **Do not imply the source character is malicious by default** — in this chapter he is a capable, uncertain language-producer, not a deceiver.

**Chapter-by-chapter observable behavior and agency.**

- **Ch01 (closing hook):** Named as the figure who, when the Keeper opens the damp-eaten treaty, says the missing promises are obvious and writes them before anyone asks how it knows — the teaser that plants Chapter 02's fluent-completion failure.
- **Ch02:** Reads aloud six clauses that fit the surviving grammar, balance the obligations, and even explain a later inventory — then defends them with "Between these words" and "On the treaty as it would most naturally have been written." When Tahmures covers the wound with blank leather and asks what remains, he names the gate and the witnesses. Asked how many jars are owed, he first offers "Twelve is a reasonable completion" — then, for the first time, pauses: "The surviving marks do not say." Under the evidence-bound tests he answers "three market days" and "two" with fragment in hand, and about grain says, with visible dislike, "The fragments are insufficient."

**Engineering lesson.** Fluent, plausible completion can exceed the available evidence; the same capable system can distinguish written, inferred, and unknown when the interaction requires it. The failure owner is the answer-seeking request plus missing evidence, not the div's character.

**Hover descriptions (tooltip text — content only).**

| Role | English | Persian |
|---|---|---|
| General (approved starting point) | Can produce a fluent, plausible account that goes beyond the available evidence. | می‌تواند روایتی روان و باورپذیر بسازد که از شواهد موجود فراتر می‌رود. |
| Ch02 | Reads the treaty's missing clauses as if written, then names what the surviving marks do not say. | بندهای گمشدهٔ پیمان را چنان می‌خواند که گویی نوشته شده‌اند؛ سپس می‌گوید نشان‌های باقی‌مانده چه نمی‌گویند. |

**Personality, voice, boundaries.** Composed, articulate, slightly vain about polish ("unsettling polish of a reflection on still water"), visibly reluctant to abstain — reluctance is style, not deceit. He is not the owner of the near-authorization of the disputed payment; the council's debate and the answer-seeking request are.

**Relationships and continuity.** Continuity record: Mirror Div, Chapter 2 only; "Can distinguish written, inferred, and unknown claims when the interaction requires it." This sheet keeps that capability visible so a later chapter may reuse it without re-villainizing him.

**Unresolved items.** Persian spelling (§2). The English text refers to the Mirror Div as "it" ("Asked again about grain, it said…"); GPT review (2026-10-10) directed keeping the existing pronouns as project-fiction presentation for this batch, so the revised chapter keeps *it*, pending human signoff (§6.4).

### 3.6 Arzhang Div — Council's Div

**Approved display name.** English: Arzhang Div. Persian: ارژنگ دیو (`GPT_REVIEW_REQUIRED`).

**Former role and exact appearances.** "the council's div" / «دیو شورا» — Chapter 03 only.

**Mythic source identity, tier, basis.** Arzhang Div is the **demon-king of Mazandaran of Rostam's labors** (per the supplied dossier: ruler of Mazandaran's divs whom Rostam defeats) — `TIER_A_SHAHNAMEH_EXPLICIT` as a named later-cycle div; verse citation pending. **His source identity and cycle must not be conflated with the council-adviser occupation**: the role is `TIER_C_PROJECT_FICTION`. Owner-approved **chronology shift**: a later-cycle div appears in Tahmures's council.

**Project-fiction role.** Offers candidates and exposes trade-offs; cannot own the council's definition of success. **Avoid assuming that every failure is caused by evil intent** — his chapter failure belongs to the requirements owner (the council), not to him.

**Chapter-by-chapter observable behavior and agency.**

- **Ch03:** Circles the five models and answers "The stone arch" before any criterion exists. Challenged on cost, he switches to "the rope bridge" — a direct response to the latest objection. By evening he has written five recommendations, each correct under a different meaning of *best* (stone: endurance; timber: cost; rope: speed; arch: carts; reed: repair). Pressed with escalating adjectives he responds "with increasing elegance and unchanged disagreement." Once constraints exist, he can explain designs and expose trade-offs; the bronze balance, not the div, carries the council's values.

**Engineering lesson.** A model optimizes only the target expressed or implied by its input; "best" concealed five objectives. Candidate generation and trade-off explanation are genuinely useful; selection requires stakeholder-owned criteria.

**Hover descriptions (tooltip text — content only).**

| Role | English | Persian |
|---|---|---|
| General (approved starting point) | Offers a candidate before the requirements are clear; cannot decide what "best" means for the council. | پیش از روشن‌شدن نیازمندی‌ها گزینه‌ای پیشنهاد می‌دهد؛ نمی‌تواند برای شورا معنای «بهترین» را تعیین کند. |
| Ch03 | Answers "the stone arch" before any criterion exists, then writes five correct recommendations under five meanings of best. | پیش از هر معیاری «قوس سنگی» را پاسخ می‌دهد؛ سپس زیر پنج معنای «بهترین»، پنج توصیهٔ درست می‌نویسد. |

**Personality, voice, boundaries.** Eager, helpful, rhetorically brilliant, faintly pleased with his own fluency. Not a villain: his "failure" is doing exactly what was asked of an undefined target. He never claims authority over the council's values.

**Relationships and continuity.** Single-chapter role in this batch. Distinct from the Many-Voiced Council of Chapter 10 (variance) — Arzhang's lesson is requirements, not variance.

**Unresolved items.** Persian spelling (§2).

### 3.7 Soroush — Archivist

**Approved display name.** English: Soroush. Persian: سروش (`GPT_REVIEW_REQUIRED`).

**Former role and exact appearances.** "The Archivist" / «بایگان» — Chapters 02, 03 (closing hook only), and 04; in Chapter 02 she interrupts the treaty debate, the Chapter 03 hook names her as the keeper of past orders, and in Chapter 04 she brings the records and defends keeping the expired order.

**Mythic source identity, tier, basis.** Soroush (Sraoša) is an **Avestan yazata of hearing, obedience, and ritual vigilance** — `TIER_B_LATER_TRADITION`. The supplied dossier records that his Tahmures-connected role (informing Jamshid about the king's body) belongs to a **later Zoroastrian telling, absent from the *Shahnameh*'s Tahmures episode**; no *Shahnameh* presence for him was verified from the supplied references. **His source identity must not be conflated with the Archivist occupation**, and nothing about the yazata is retold here. The owner's approved mapping places him as a human court archivist in Tahmures's reign — a deliberate **nature and chronology adaptation** (`TIER_C_PROJECT_FICTION`).

**Project-fiction role.** Preserves context, provenance, and the reasons behind past decisions (continuity record: "Records may remain valuable after their instructions expire; selection and authority must be represented separately.").

**Chapter-by-chapter observable behavior and agency.**

- **Ch02:** Is the **only** council member to interrupt the payment debate: the later inventory that seemed to confirm twelve jars concerns lamp oil and carries a different seal. (The narrative also notes the council still needs hypotheses "so the Archivist could search related records.")
- **Ch04:** Brings the water ledgers among which the expired letter sits. Challenged ("Why keep an expired command?"), answers: "Because it explains the past. Burn every old order and the ledger will preserve decisions without causes." When Tahmures asks which objects may supply facts, she touches the records.

**Engineering lesson per appearance.** Ch02: an irrelevant-but-plausible record must be rejected on content and provenance, not on how well it fits a completion. Ch04: preservation is not authorization — archives keep causes, and expiry semantics must be represented separately from preservation.

**Hover descriptions (tooltip text — content only).**

| Role | English | Persian |
|---|---|---|
| General (approved starting point) | Preserves provenance and points back to source records; preservation alone does not make an old instruction current. | خاستگاه اسناد را حفظ می‌کند و به خودِ منبع ارجاع می‌دهد؛ صرفِ نگه‌داشتن، فرمانی قدیمی را جاری نمی‌کند. |
| Ch02 | Interrupts the council to show the later inventory is about lamp oil and carries a different seal. | بحث شورا را قطع می‌کند تا نشان دهد سند متأخر دربارهٔ روغن چراغ است و مُهر متفاوتی دارد. |
| Ch04 | Keeps the expired order because it explains the past, and shows which records may supply facts. | فرمان منقضی را نگه می‌دارد چون گذشته را توضیح می‌دهد و نشان می‌دهد کدام اسناد می‌توانند اطلاعات بدهند. |

**Personality, voice, boundaries.** Quiet, exact, quietly firm under pressure from the king himself. She does not validate truth by title: keeping a record is a statement about evidence, never about authority.

**Relationships and continuity.** Continuity record lists the Archivist in Chapters 2, 4, 6, 8, 12–15, 19, 21; within this batch, 02 and 04. Form/provenance counterpart to the Keeper of Scripts.

**Unresolved items.** The original English text used **she/her** for the Archivist. GPT review (2026-10-10) directed keeping the existing English pronouns as project-fiction presentation for this batch; the revised chapters keep she/her, pending human signoff (§6.4). Persian spelling (§2).

### 3.8 Simurgh — Messenger

**Approved display name.** English: Simurgh. Persian: سیمرغ (`GPT_REVIEW_REQUIRED`).

**Former role and exact appearances.** "The Messenger" / «پیام‌رسان» — Chapter 01 only (checks the tablet, wraps it, carries it north).

**Mythic source identity, tier, basis.** The Simurgh is the **mythical wise bird of the *Shahnameh*'s Zal/Rostam cycle** (per the supplied dossier: nurtured Zal, aids Rostam) — `TIER_A_SHAHNAMEH_EXPLICIT` as a *Shahnameh* bird; verse citation pending; **not part of the Tahmures episode**. The dossier's "timeless being" framing is a research suggestion, not a source claim. **The source identity must not be conflated with the Messenger occupation**: placing the Simurgh in Tahmures's hall is `TIER_C_PROJECT_FICTION` with an owner-approved **chronology/framing shift**.

**Project-fiction role.** Carries context and exposes what changes across recipients (continuity record: "In Chapter 1, treats an unidentified record as an urgent current message, contributing to the frontier alarm.").

**Chapter-by-chapter observable behavior and agency.**

- **Ch01:** Examines the tablet's weight and the remains of its cord — a physical, provenance-minded check that still cannot recover sender or recipient. On his own judgment ("It is an urgent message. I will take it to the present captain.") he wraps it in oilcloth and departs. His arrival is what causes the northern captain to send riders, and by midnight three villages believe an invasion has begun.

**Engineering lesson.** Delivery does not establish a message's intended recipient or authority; a transfer step changes a text's function, and a reasonable reading by a capable courier can still produce a false alarm when the interface omits role labels.

**Hover descriptions (tooltip text — content only).**

| Role | English | Persian |
|---|---|---|
| General (approved starting point) | Carries information between people; delivery does not establish its intended recipient or authority. | اطلاعات را میان مردم جابه‌جا می‌کند؛ رساندنِ پیام، گیرندهٔ موردنظر یا اختیارش را اثبات نمی‌کند. |
| Ch01 | Weighs the tablet, wraps it as an urgent message, and carries it to the present captain; the transfer changed its function. | لوح را وزن می‌کند، آن را پیامی فوری می‌پیچد و نزد سردار کنونی می‌برد؛ جابه‌جایی، کارکردش را عوض کرد. |

**Personality, voice, boundaries.** Competent, decisive, dutiful — and that is precisely the lesson: nothing about him is careless. He is not blamed for the alarm; the missing speaker/recipient labels are. He does not prove sender or authority by carrying a tablet well.

**Relationships and continuity.** Continuity record lists the Messenger in Chapters 1 and 18; within this batch, Chapter 01 only. Distinct from Chapar the courier (§3.16): in the live Chapter 01 text the courier delivers the tablet **to the hall**, while the Messenger carries it **from the hall to the captain** — two separate story actions that must not be merged.

**Unresolved items.** **Form decision:** GPT review (2026-10-10) accepted the source-supported bird form as the current visual-prompt proposal, while the messenger role in this tale remains project fiction; the revised prose keeps the live text's non-committal presentation (no bird description in the tale — he checks weight, wraps oilcloth, travels). Final form confirmation belongs to human signoff (§6.5). Persian spelling (§2).

### 3.9 Arash — current captain / Gatekeeper

**Approved display name.** English: Arash. Persian: آرش (`GPT_REVIEW_REQUIRED`).

**Former role and exact appearances.**

- Chapter 01: "the present captain" / "the northern captain" / «سردار کنونی» / «سردار شمالی» (receives the delivery, sends riders); **plus the illustrative Gatekeeper** / «دروازه‌بان» in the Discovery section's "Close the western gate" example.
- Chapter 03: "the captain" / «فرمانده» (laughs at the rope bridge; requires supply carts).
- Chapter 04: "the Gatekeeper" / «دروازه‌بان» (receives the div's order and opens the gate; proposes destroying expired orders; is bound to the current-seal rule).

**Mythic source identity, tier, basis.** Arash is the **legendary archer who marked Iran's border** in Iranian legendary tradition — `TIER_B_LATER_TRADITION`. The supplied dossier places him in a post-Zahhak era, states his chronology is "not securely synchronized across all legendary traditions," and cites **no *Shahnameh* verse**; any Tier A claim would require verse-level verification first (`GPT_REVIEW_REQUIRED` note, not a silent upgrade). **His source identity must not be conflated with the captain/Gatekeeper occupations**, and the border-arrow story is not retold: the chapter roles are `TIER_C_PROJECT_FICTION` under an owner-approved chronology shift. He is not given a bow or archery in any chapter role.

**Project-fiction role.** The consequential actor: controls gates and sluices, and challenges language-only safety (continuity record for the Gatekeeper function: "Clear words and convincing seals do not replace authenticated authority.").

**Chapter-by-chapter observable behavior and agency.**

- **Ch01 (captain):** On the Messenger's arrival with an unlabeled tablet read as urgent, sends riders into the hills — a plausible military response with real consequences (three villages believe an invasion has begun).
- **Ch01 (illustrative Gatekeeper):** In the classification example, "Close the western gate" is a current task **when sent by the Gatekeeper to the watch** — the same words are evidence in a trial and ink in an apprentice's practice.
- **Ch03 (captain):** Laughs — "A supply cart cannot cross it" — and supplies the hard requirement that supply carts must cross.
- **Ch04 (Gatekeeper):** Opens the gate while Tahmures sleeps, on the strength of the div's beautiful tablet — a well-formed order without a current seal. Proposes destroying expired orders (rejected: it destroys evidence). Is then told to move no sluice without a current seal.

**Engineering lesson per appearance.** Ch01: a consequential actor's plausible reading of an unlabeled message multiplies the cost of interface defects; authority comes from sender and route, not from the message's form. Ch03: a champion who voices a requirement does not set the council's priorities — his cart requirement is one constraint among five. Ch04: action requires current authority supplied by the governing system; prose quality is not authorization, and the remedy is a mechanism (current seal), not a scolding.

**Hover descriptions (tooltip text — content only).**

| Role | English | Persian |
|---|---|---|
| General (approved starting point) | Represents the consequential actor; action still requires current authority supplied by the governing system. | کنشگرِ پیامدساز است؛ اقدام همچنان به اختیار جاری‌ای نیاز دارد که از سامانهٔ حکمرانی برسد. |
| Ch01 (captain) | Receives the courier's delivery as an urgent message and sends riders — a plausible reading with real consequences. | تحویل پیام‌رسان را می‌پذیرد، آن را پیامی فوری می‌گیرد و سواران را به تپه‌ها می‌فرستد — تفسیری معقول با پیامدی واقعی. |
| Ch01 (illustrative Gatekeeper) | In the gate example, "Close the western gate" is a current task only when the Gatekeeper sends it to the watch. | در مثال دروازه، «دروازهٔ غربی را ببند» تنها وقتی وظیفهٔ جاری است که دروازه‌بان آن را برای نگهبانان بفرستد. |
| Ch03 | Requires that supply carts can cross, and rejects the rope bridge on that ground. | عبور ارابهٔ تدارکات را لازم می‌داند و پل طنابی را از همین دلیل رد می‌کند. |
| Ch04 | Opens the sluice on a well-formed tablet, then is bound to move nothing without a current seal. | دریچه را با لوحی خوش‌ساخت باز می‌کند؛ سپس مقید می‌شود هیچ دریچه‌ای را بدون مُهر جاری جابه‌جا نکند. |

**Personality, voice, boundaries.** Dutiful, quick, decisive; respectful of well-formed orders and therefore vulnerable to them. He is not careless — the Ch04 failure is the missing current-seal check at the action boundary, not his diligence.

**Relationships and continuity.** The continuity record introduces the Gatekeeper "indirectly in Chapter 4" and "centrally in Chapter 5"; the mapping extends the same function to the Chapter 01 illustrative Gatekeeper and to the Chapter 01/03 captain roles, which the owner approved for this batch. The later-book Gatekeeper arc (divided key ring, trust partitions, exact approvals) is untouched.

**Unresolved items.** The revision renders the Chapter 01 northern captain, the Chapter 01 illustrative Gatekeeper, the Chapter 03 captain, and the Chapter 04 Gatekeeper as one named figure (Arash), following the approved mapping; confirm at human signoff. Verse verification if any source claim about Arash is ever made. Persian spelling (§2).

### 3.10 Garshasp — remembered captain of the prior court

**Approved display name.** English: Garshasp. Persian: گرشاسپ (`GPT_REVIEW_REQUIRED`).

**Former role and exact appearances.** "a captain who served your father" / «یکی از سرداران زمان پدرتان» — Chapter 01 only, **offstage**: known solely through the Keeper's handwriting attribution. No dialogue, no action, no on-page presence.

**Mythic source identity, tier, basis.** Garshasp is an ancient champion of Iranian tradition — the Avestan Kərəsāspa dragon-slaying tradition and later epic genealogies — `TIER_B_LATER_TRADITION`. The supplied dossier's own Persian and English entries **contradict each other on his family relations** (father of Fariburz vs father of Faramarz vs kinsman of Sam), and cite no *Shahnameh* verse; all genealogical details are therefore `UNVERIFIED_SOURCE_DETAIL` and are deliberately not used here — the chapter role needs none of them. A *Shahnameh* genealogical presence, if claimed later, requires verse verification.

**Project-fiction role and chronology adaptation.** A remembered captain from the court of Tahmures's father, invoked as the likely hand behind an old command. (The Chapter 01 text leaves the father unnamed; the canonical source genealogy — Ferdowsi names Hushang as Tahmures's father — is recorded only in the source note in §3.1, not in the story.) This is an owner-approved project chronology choice (`TIER_C_PROJECT_FICTION`); it must not be presented as a sourced fact about any epic reign.

**Chapter-by-chapter observable behavior and agency.**

- **Ch01:** None on stage. The Keeper catalogues the tablet as an old command because "the hand resembles a captain who served your father." The resemblance is offered and consumed as classification support — nothing more.

**Engineering lesson.** A familiar name (or handwriting) does not establish the source or authority of a command; attribution by resemblance is a hypothesis, not authentication.

**Hover descriptions (tooltip text — content only).**

| Role | English | Persian |
|---|---|---|
| Ch01 (approved starting point) | A remembered captain from the prior court; a familiar name does not establish the source or authority of a command. | سرداری به‌یادماندنی از دربار پیشین؛ نامِ آشنا، منبع یا اختیار یک فرمان را اثبات نمی‌کند. |

**Personality, voice, boundaries.** No voice in this batch. Any future on-page portrayal must not import the source champion's dragon-slaying biography.

**Relationships and continuity.** Connects Tahmures's reign to the prior court; a natural anchor if a later chapter needs inherited precedent. Not in the current continuity record; adding him there belongs to the future approved revision, not this file.

**Unresolved items.** Whether he is ever shown on page (flashback/art) is an open editorial choice; his dossier genealogy contradictions are recorded for GPT awareness. Persian spelling (§2).

### 3.11 Jamshid — governor, treasurer, former governor

**Approved display name.** English: Jamshid. Persian: جمشید (`GPT_REVIEW_REQUIRED`).

**Former role and exact appearances.**

- Chapter 02: the eastern governor of the "two governors" / «دو فرماندار» with competing treaty claims (owner-fixed assignment, 2026-10-10: Jamshid is the eastern governor who smiles at the Mirror Div's completion).
- Chapter 03: "the treasurer" / «خزانه‌دار» (strikes the table; sets the cost ceiling; corrects the king).
- Chapter 04: "a former governor's letter" / «نامهٔ فرمانداری پیشین» — the author of the old irrigation order. The original live text called him "the dead governor"; per the owner clarification (2026-10-10) his life status at the chapter's present is unspecified, so the revision names him only as a former governor.

**Mythic source identity, tier, basis.** Jamshid is **Tahmuras's son and successor in the *Shahnameh*'s sequence** — `TIER_A_SHAHNAMEH_EXPLICIT` (supplied dossier quotes the succession; the live skill canon reference confirms and notes that his youth at Tahmures's court would already be fiction). The Avestan brother-variant is a separate tradition, not used. **His source identity must not be conflated with the governor/treasurer occupations**: placing the successor-generation figure as a contemporary administrator in Tahmures's reign is an owner-approved **chronology shift** (`TIER_C_PROJECT_FICTION`), and no source event is retold.

**Project-fiction role and chronology adaptation.** A confident administrative figure across three chapters: claimant (02), requirements owner for cost (03), and author of an instruction that outlived its authority (04). The owner clarified (2026-10-10): Jamshid's life status at Chapter 04 is unspecified — the tales neither state nor imply that he is alive or dead; the letter is simply an old record whose words survive without current authority. (An earlier draft of this sheet stated he was dead by Chapter 04; that wording was removed.) The Chapter 03 → Chapter 04 gap of at least six years belongs to Keyumars's owner-approved timeline (§3.13), not to any claim about Jamshid.

**Chapter-by-chapter observable behavior and agency.**

- **Ch02:** Arrives before noon "certain that the missing words granted him twelve jars of grain." Under the owner-fixed assignment he is the eastern governor who smiles at the Mirror Div's completion; Budhasaf (§3.12) makes the bribery accusation. The live text's unattributed "less impressive" line is deliberately left unattributed in the revision.
- **Ch03:** Strikes the table — "It costs more than the province collects in two years." Imposes the cost ceiling of eighty silver marks. Publicly corrects his king: "So timber is best" — "Under the requirements we have now written." Helps hang the bronze weights recording whose judgement each represents.
- **Ch04:** Author of "Send the western water first to the cypress garden. Continue until the king returns from the southern road." — an instruction whose trigger condition silently expired; the letter is preserved because it explains an unusual allotment.

**Engineering lesson per appearance.** Ch02: a competing claim is not established by confidence or status alone. Ch03: requirements ownership includes the discipline of correcting the requester, and "best under the requirements we have now written" is the correct form of a recommendation. Ch04: an instruction's authority expires with its conditions even when its words survive; conditional commands need expiry semantics.

**Hover descriptions (tooltip text — content only).**

| Role | English | Persian |
|---|---|---|
| Ch02 governor (approved starting point, shared with Budhasaf) | Present competing claims; neither claim is established by confidence or status alone. | ادعاهای رقیب مطرح می‌کنند؛ هیچ‌یک از دو ادعا صرفاً با اطمینان یا جایگاه اثبات نمی‌شود. |
| Ch03 treasurer | As treasurer, sets the cost ceiling and corrects the king: best means "under the requirements we have now written." | به‌عنوان خزانه‌دار سقف هزینه را تعیین می‌کند و شاه را اصلاح می‌کند: بهترین یعنی «زیر نیازمندی‌هایی که اکنون نوشته‌ایم». |
| Ch04 former governor | The former governor whose old water letter is kept as evidence long after its authority expired. | فرماندار پیشینی که نامهٔ قدیمی‌اش دربارهٔ آب، مدت‌ها پس از انقضای اختیارش همچنان به‌عنوان شاهد نگه داشته شده است. |

**Personality, voice, boundaries.** Self-assured, prosperous, sharp with numbers, unexpectedly rigorous about the limits of his own conclusions. Not a fraud in Chapter 04 — his letter was legitimate when written; the failure is the missing expiry representation.

**Relationships and continuity.** His Ch03 correction scene is the model for stakeholder-owned criteria that the bronze balance formalizes; Chapter 04's letter is the concrete artefact the black-cord arrangement eventually labels. In the source tradition he is Tahmures's successor; that relationship is **not** asserted inside the fiction in this batch (the tales never state it), and whether to hint it is a later revision decision.

**Unresolved items.** East/west assignment resolved by the owner (eastern, the one who smiles); Chapter 04 life status left unspecified by the owner (2026-10-10) — the tale names him only as "a former governor". Persian spelling (§2).

### 3.12 Budhasaf — governor with a competing claim

**Approved display name.** English: Budhasaf. Persian: بوداسب (`GPT_REVIEW_REQUIRED`).

**Former role and exact appearances.** The western governor of the "two governors" / «دو فرماندار» — Chapter 02 only (owner-fixed assignment, 2026-10-10: Budhasaf is the western governor who accuses the Mirror Div).

**Mythic source identity, tier, basis.** `UNVERIFIED_SOURCE_LEAD`. The supplied dossier mentions `Būdasb / بوداسب` **only as one scholar's proposed alternative form for Shahrasp's name** (Vasheghani Farahani's hypothesis that *Shahrasp* may be a later form of *Budasb*); it does **not** establish a separate mythic governor named Budhasaf. Per the owner's instruction: keep the approved `Budhasaf` as a distinct Chapter 02 project-fiction character, do not merge him with Shahrasp, and do not claim a source identity without verified evidence. **Name-collision caution for GPT review:** readers of the scholarly literature may associate the name with that hypothesis; the book must never present this Budhasaf as "the minister Budhasb" or as Shahrasp under another name. His entire Chapter 02 existence is `TIER_C_PROJECT_FICTION`.

**Project-fiction role.** Presents a competing treaty claim with equal confidence and equal lack of evidence.

**Chapter-by-chapter observable behavior and agency.**

- **Ch02:** Arrives before noon certain the missing words granted him twelve jars. Under the owner-fixed assignment he is the western governor who accuses the Mirror Div "of having bribed a creature that needed no money," while Jamshid smiles at the fluent completion. The live text also has "one governor" call the abstention "less impressive," which the revision leaves unattributed.

**Engineering lesson.** Two confident, status-bearing claimants with the same missing evidence produce a dispute, not a fact; the remedy is evidence boundaries and marked hypotheses, not choosing the more convincing claimant.

**Hover descriptions (tooltip text — content only).**

| Role | English | Persian |
|---|---|---|
| Ch02 | Presents a competing claim; neither claim is established by confidence or status alone. | ادعایی رقیب مطرح می‌کند؛ هیچ‌یک از دو ادعا صرفاً با اطمینان یا جایگاه اثبات نمی‌شود. |
| Ch02 governor pair (approved, shared with Jamshid) | Present competing claims; neither claim is established by confidence or status alone. | ادعاهای رقیب مطرح می‌کنند؛ هیچ‌یک از دو ادعا صرفاً با اطمینان یا جایگاه اثبات نمی‌شود. |

**Personality, voice, boundaries.** As confident as his counterpart; no more entitled. He must remain visually and textually distinct from Shahrasp (see the visual-prompt file).

**Relationships and continuity.** Single-chapter role. No relation to Shahrasp may be implied.

**Unresolved items.** East/west assignment resolved by the owner (western, the one who accuses); the standing name-collision caution above; Persian spelling (§2). The approval and source-status caveat (project-fiction choice, unverified separate mythic identity) lives in this profile, not in reader-facing tooltip copy.

### 3.13 Keyumars — builder, deceased king

**Approved display name.** English: Keyumars. Persian: کیومرث (`GPT_REVIEW_REQUIRED`).

**Former role and exact appearances.**

- Chapter 03: "the builder" / «سازنده» — one of the five advisers (repairs timber in two days, stone only in ten).
- Chapter 04: "That king" / «آن شاه» — the king, dead six years, whose awaited return anchors the expired letter ("Continue until the king returns from the southern road").

**Mythic source identity, tier, basis.** Keyumars is the **first king of the Pishdadian line at the opening of the *Shahnameh*** (supplied dossier: "first human and first king of Iran in Zoroastrian myth and the Shahnameh") — `TIER_A_SHAHNAMEH_EXPLICIT` for the kingship claim, verse citation pending; the dossier's Avestan cosmological details (Gayōmart, Mount Alburz, Homā, Siamak) are Tier B and are not used. **Keyumars precedes Tahmures in the dossier's chronology; his approved role as the Chapter 03 builder and the Chapter 04 deceased king is project fiction** — an explicit, owner-approved **chronology shift**. Source-genealogy caution: the supplied dossier makes Keyumars Hushang's grandfather (Keyumars → Siamak → Hushang), and the live canon reference makes Tahmures Hushang's son; read literally, those links place Keyumars as Tahmures's great-grandfather. No source event is retold, and his on-page presence (Ch03) plus posthumous reference (Ch04) must not be described as occurring in the source epic.

**Project-fiction role and chronology adaptation.** Ch03: the voice of repairability — his practice times turn "ease of repair" from an adjective into a measurable requirement. Ch04: the dead king whose name and prestige remain attached to an instruction that long outlived its authority. The owner fixed the timeline (2026-10-10): Keyumars is alive as the Chapter 03 builder, and Chapter 04 opens by establishing that six years have passed since his death. No cause or exact date of death is invented. **Locked relationship (owner decision, 2026-10-10, `TIER_C_PROJECT_FICTION`):** in this book's fiction, Keyumars is Tahmures's direct grandfather — an owner-authorized adaptation that deliberately compresses the source genealogy (see the great-grandfather caution above); it is not a *Shahnameh* fact, is not stated on-page in Chapters 01–04, and requires no tale edit.

**Chapter-by-chapter observable behavior and agency.**

- **Ch03:** Present at the council; his capability statement ("could repair timber in two days but stone only in ten") becomes one of the inputs that disqualify stone on maintenance grounds once the two columns exist.
- **Ch04:** No agency — dead six years. The letter's condition ("until the king returns") silently expired with him; the garden he knew became an orchard.

**Engineering lesson per appearance.** Ch03: operational constraints (repair time, maintenance burden) belong in requirements, supplied by the people who do the work. Ch04: age, prestige, or royal origin does not make an instruction current; conditional commands inherit expiry from their conditions.

**Hover descriptions (tooltip text — content only).**

| Role | English | Persian |
|---|---|---|
| General (approved starting point) | An older figure whose plans and records remain part of the story; age or prestige does not make an instruction current. | چهره‌ای کهن که طرح‌ها و اسنادش در داستان می‌مانند؛ قدمت یا اعتبار، فرمانی را جاری نمی‌کند. |
| Ch03 | Supplies the repair times — timber in two days, stone in ten — that turn repairability into a requirement. | زمان تعمیر را می‌دهد — چوب در دو روز، سنگ در ده روز — و تعمیرپذیری را به نیازمندی بدل می‌کند. |
| Ch04 | The king whose awaited return anchored an instruction that outlived its authority. | شاهِ درگذشته‌ای که انتظار بازگشتش، فرمانی بر جای گذاشت که از اختیارش دوام بیشتری یافت. |

**Personality, voice, boundaries.** In Ch03, a practical elder craftsman's voice: concrete numbers, no rhetoric. In Ch04, deliberately voiceless — his silence is the point (instructions cannot be re-asked of the dead; that is why expiry must be explicit).

**Relationships and continuity.** The Chapter 04 letter (authored by Jamshid, the former governor) awaits this king's return; together they instantiate "old, prestigious, expired." Recorded in the current continuity entry (`book/narrative-continuity.md`): the Chapter 03 builder and Chapter 04 posthumous-king roles, the locked six-year chronology, and the owner-locked Tier-C grandfather relationship to Tahmures.

**Unresolved items.** The internal sequencing flagged for GPT review (living Chapter 03 builder vs king dead six years in Chapter 04) was resolved by the owner on 2026-10-10: Keyumars is the living Chapter 03 builder, and Chapter 04 opens six years after his death; the Chapter 03 closing hook now signals the intervening years. Persian spelling (§2).

### 3.14 Nariman — flood-affected council member

**Approved display name.** English: Nariman. Persian: نریمان (`GPT_REVIEW_REQUIRED`).

**Former role and exact appearances.** "The flood keeper" / «نگهبان سیلاب» in the live text — Chapter 03 only, one of the five advisers. The project role is the flood-affected council member (a stakeholder whose fields the flood cut off), not a separate river-keeping occupation; the revised tale names him Nariman and keeps his requirement that the crossing survive the spring current.

**Mythic source identity, tier, basis.** Nariman is a **forebear of the Sistani champion lineage (father of Sam) in the *Shahnameh*'s epic material** — `TIER_A_SHAHNAMEH_EXPLICIT` for the lineage claim per the supplied dossier; verse citation pending; the dossier gives no stories that this book uses. **His source identity and cycle must not be conflated with the flood-keeper occupation**: an owner-approved **chronology shift** places the later-lineage forebear as a contemporary council voice (`TIER_C_PROJECT_FICTION`).

**Project-fiction role.** The flood-affected council member who voices the stakeholder requirement the bridge must survive; he is a farmer affected by the flood, not the keeper of a river office.

**Chapter-by-chapter observable behavior and agency.**

- **Ch03:** States the failure he cannot accept: the crossing must survive the spring current. His requirement is one voice among five; it disqualifies the reed design but does not set the council's priorities.

**Engineering lesson.** Requirement elicitation means collecting each stakeholder's unacceptable failure; a single legitimate need constrains the solution without owning the decision.

**Hover descriptions (tooltip text — content only).**

| Role | English | Persian |
|---|---|---|
| Ch03 (approved starting point) | Voices the need for a crossing that survives the spring flood; he does not set the council's priorities. | نیاز به گذری را بیان می‌کند که از سیلاب بهاری جان سالم به در ببرد؛ اما اولویت‌های شورا را او تعیین نمی‌کند. |

**Personality, voice, boundaries.** Plain, river-worn practicality. He states his need once and does not inflate it into a ranking.

**Relationships and continuity.** Single-chapter role; the spring flood is also the chapter's inciting event (it removed the old bridge). In the source lineage he is Sam's father — within this batch Sam appears in Chapter 04 with no stated relation; whether to hint the lineage is a later editorial choice, not asserted here.

**Unresolved items.** The live label "flood keeper" (نگهبان سیلاب) was replaced in the revision by the flood-affected council-member framing (owner-approved correction, 2026-10-10); his spring-current requirement is unchanged. Persian spelling (§2).

### 3.15 Sam — orchard keeper

**Approved display name.** English: Sam. Persian: سام (`GPT_REVIEW_REQUIRED`).

**Former role and exact appearances.** "the astonished orchard keeper" / «نگهبان شگفت‌زدهٔ میوه‌ستان» — Chapter 04 only.

**Mythic source identity, tier, basis.** Sam is a **named champion of the Sistani lineage (father of Zal, Rostam's grandfather) in the *Shahnameh*'s epic material** — `TIER_A_SHAHNAMEH_EXPLICIT` for the broad identity. **Caution:** the supplied dossier's Persian and English entries **contradict each other on his family relations** (the Persian entry calls him "son of Zal" and "stepfather of Rostam," which conflicts with the English entry's "grandfather of Rostam, father of Zāl, son of Nariman"); all specific relations are therefore `UNVERIFIED_SOURCE_DETAIL` and are not used — the chapter role needs none. **His source identity and cycle must not be conflated with the orchard-keeper occupation**: an owner-approved **chronology shift** places the epic champion as a provincial orchard keeper (`TIER_C_PROJECT_FICTION`); no source event is retold.

**Project-fiction role.** The person who bears the cost when an outdated record is acted on.

**Chapter-by-chapter observable behavior and agency.**

- **Ch04:** When the diverted water arrives at the old cypress garden (now an orchard), he obeys the flow of events and digs channels his trees do not need, astonished. He receives water that isn't his to use while a village's upper fields go dry.

**Engineering lesson.** Outdated instructions have real, asymmetric victims: the orchard keeper's wasted labor and the dry village's lost day are both consequences of missing expiry semantics; his concern does not make old text current, and his loss does not by itself prove the rule either — the seal dates do.

**Hover descriptions (tooltip text — content only).**

| Role | English | Persian |
|---|---|---|
| Ch04 (approved starting point) | Makes visible who bears the cost when an outdated record is acted on; his concern does not make old text current. | نشان می‌دهد هزینهٔ به‌کاربستن سندی ازکارافتاده بر دوش کیست؛ دغدغهٔ او متن قدیمی را جاری نمی‌کند. |

**Personality, voice, boundaries.** Hard-working, uncomplaining, bewildered by privilege he did not ask for. Not a complainer-archetype and not a claimant: his scene is cost made visible, not grievance as argument.

**Relationships and continuity.** Single-chapter role; the orchard is the letter's "cypress garden" transformed by time — a small continuity anchor (place meaning changed while the words stayed).

**Unresolved items.** Dossier contradiction on his source relations (recorded above for GPT awareness; unused). Persian spelling (§2).

### 3.16 Chapar — courier (short role entry)

**Role, not a person's mythic identity.** "Chapar" / «چاپار» is a **Persian occupational name for a courier, not a mythic person** — `NOT_APPLICABLE_OCCUPATIONAL_ROLE`. The approved mapping records the Chapter 01 courier under this label; it does not create a new named mythic character, and no source identity is claimed for him.

**Former role and exact appearances.** "a courier" / «پیکی» — Chapter 01 only: on a wet morning he brings the tablet found beside the northern river to the Hall of Scripts. He does not know who carried it or whom it was meant to reach.

**Observable behavior and agency.** Delivers a found object with an honest account of its unknown provenance — the chapter's cleanest demonstration that a physical hand-off carries no routing metadata.

**Engineering lesson.** Carries a record; delivery alone does not determine its intended recipient, purpose, or authority.

**Hover descriptions (tooltip text — content only).**

| Role | English | Persian |
|---|---|---|
| Ch01 (approved starting point) | Carries a record; delivery alone does not determine its intended recipient, purpose, or authority. | سندی را می‌آورد؛ صرفِ رساندن، گیرنده، هدف یا اختیار آن را تعیین نمی‌کند. |

**Continuity note.** Keep his actions distinct from the Messenger (Simurgh): the courier brings the tablet **to the hall**; the Messenger takes it **from the hall to the captain**. Do not merge them.

## 4. Coverage table

Built by comparing both language editions of all four live tale sections (including each chapter's closing hook, which reuses the mapped recurring roles). Status `MAPPED` = owner-approved mapping applied; `GPT_REVIEW_REQUIRED` = open collision or assignment; `COLLECTIVE—NO NEW NAME` = background collective.

| Chapter | English role (live text) | Persian role/name (live text) | Approved mapping | Status |
|---|---|---|---|---|
| 01 | Tahmures | طهمورث | Tahmures | MAPPED |
| 01 | The First Scribe | دبیر نخست | Shahrasp | MAPPED |
| 01 | Keeper of Scripts | نگهبان دبیره‌ها | Akvan Div | MAPPED |
| 01 | The Messenger | پیام‌رسان | Simurgh | MAPPED |
| 01 | Literal Div | دیو لفظ‌گرا | Black Div | MAPPED |
| 01 | Courier who brings the tablet | پیک | Chapar (occupational role) | MAPPED |
| 01 | Captain who served Tahmures's father (offstage) | «یکی از سرداران زمان پدرتان» | Garshasp | MAPPED |
| 01 | Present / northern captain | سردار کنونی / سردار شمالی | Arash | MAPPED |
| 01 | Gatekeeper (illustrative example only) | دروازه‌بان | Arash | MAPPED |
| 01 | Mirror Div (closing hook only) | دیو آینه | Div-e Sefid | MAPPED — hook appearance added by GPT-review correction |
| 01 | Charcoal burners (eleven fires) | زغال‌سازان | — | COLLECTIVE—NO NEW NAME |
| 01 | Riders sent into the hills | سواران | — | COLLECTIVE—NO NEW NAME |
| 01 | Three villages | سه روستا | — | COLLECTIVE—NO NEW NAME |
| 01 | The watch (illustrative example) | نگهبانان | — | COLLECTIVE—NO NEW NAME |
| 01 | Apprentice practising letters (illustrative example) | شاگرد | — | COLLECTIVE—NO NEW NAME |
| 02 | Tahmures | طهمورث | Tahmures | MAPPED |
| 02 | Mirror Div | دیو آینه | Div-e Sefid | MAPPED |
| 02 | First Scribe | دبیر نخست | Shahrasp | MAPPED |
| 02 | Eastern governor | فرماندار شرقی | Jamshid | MAPPED — owner-fixed assignment (2026-10-10): Jamshid smiles |
| 02 | Western governor | فرماندار غربی | Budhasaf | MAPPED — owner-fixed assignment (2026-10-10): Budhasaf accuses |
| 02 | Archivist | بایگان | Soroush | MAPPED |
| 02 | The council | شورا | — | COLLECTIVE—NO NEW NAME |
| 02 | Eastern and western cities (treaty parties) | شهر شرقی / شهر غربی | — | NOT CAST — places/parties; no name |
| 02 | Treaty witnesses ("one citizen of each", inside quoted treaty text) | شاهد (متن پیمان) | — | COLLECTIVE—NO NEW NAME |
| 03 | Tahmures | طهمورث | Tahmures | MAPPED |
| 03 | The council's div | دیو شورا | Arzhang Div | MAPPED |
| 03 | Treasurer | خزانه‌دار | Jamshid | MAPPED |
| 03 | Captain | فرمانده | Arash | MAPPED |
| 03 | Flood keeper | نگهبان سیلاب | Nariman | MAPPED — revised as flood-affected council member (§3.14) |
| 03 | Builder | سازنده | Keyumars | MAPPED — owner-fixed timeline: alive in Ch03, Ch04 six years after his death |
| 03 | Archivist (closing hook only) | بایگان | Soroush | MAPPED — hook appearance added by GPT-review correction |
| 03 | Villagers | روستاییان | — | COLLECTIVE—NO NEW NAME |
| 03 | Five bridge makers | پنج پل‌ساز | — | COLLECTIVE—NO NEW NAME |
| 03 | Farmers ferrying grain | کشاورزان | — | COLLECTIVE—NO NEW NAME |
| 03 | First Scribe | دبیر نخست | Shahrasp | MAPPED |
| 03 | The council | شورا | — | COLLECTIVE—NO NEW NAME |
| 04 | Tahmures | طهمورث | Tahmures | MAPPED |
| 04 | Literal Div | دیو لفظ‌گرا | Black Div | MAPPED |
| 04 | Archivist | بایگان | Soroush | MAPPED |
| 04 | Former governor, author of the old letter | فرماندار پیشین | Jamshid | MAPPED — life status at Ch04 unspecified (owner clarification, correction-01) |
| 04 | The king dead six years | آن شاه | Keyumars | MAPPED — owner-fixed timeline (§3.13) |
| 04 | Gatekeeper | دروازه‌بان | Arash | MAPPED |
| 04 | Keeper of Scripts | نگهبان دبیره‌ها | Akvan Div | MAPPED |
| 04 | First Scribe | دبیر نخست | Shahrasp | MAPPED |
| 04 | Orchard keeper | نگهبان میوه‌ستان | Sam | MAPPED |
| 04 | Two villages | دو روستا | — | COLLECTIVE—NO NEW NAME |
| 04 | Farmers sleeping beside the sluice | کشاورزان | — | COLLECTIVE—NO NEW NAME |

No unexpected named character appears in either edition of the four tales. Every named or individually functional role above appears exactly once in the roster (§1) with all applicable chapters listed.

## 5. Collective background roles

Riders, charcoal burners, villagers, farmers, bridge makers, witnesses, the watch, the council, and the apprentice are collectives or generic illustrative roles. They keep `COLLECTIVE—NO NEW NAME` status: no individual in these groups is promoted to a named character, and no extra names are invented to fill out the cast. The two cities of the Chapter 02 treaty are parties/places, not cast members.

## 6. Cross-cutting unresolved items for GPT review

1. **Ch02 governor assignment (§3.11, §3.12).** **Resolved by the owner (2026-10-10):** Jamshid is the eastern governor (the one who smiles); Budhasaf is the western governor (the one who accuses the Mirror Div). The unattributed "less impressive" line stays unattributed.
2. **Keyumars internal sequencing (§3.13).** **Resolved by the owner (2026-10-10):** Keyumars is the living Chapter 03 builder; Chapter 04 opens six years after his death. No cause or date of death invented.
3. **Jamshid Chapter 04 life status (§3.11).** **Resolved by the owner (2026-10-10):** unspecified. An earlier draft of this batch stated he was dead by Chapter 04; the owner clarified that the tales must not state or imply his life status, and that wording was removed from the tales, this sheet, the continuity record, and the tooltips. He remains the former-governor author of the expired letter; the at-least-six-year Chapter 03 → 04 gap belongs to Keyumars's timeline (§3.13).
4. **Pronouns and presentation (§3.3, §3.5, §3.7, §3.8).** The current English text genders the Keeper of Scripts and the Archivist as *she*, the First Scribe as *he*, and the Mirror Div as *it*. GPT review (2026-10-10) directed: preserve the existing English pronouns as project-fiction presentation for this batch unless the owner changes them at signoff; Persian needs no pronoun change. The revised chapters keep she/her (Akvan Div, Soroush), he/him (Shahrasp, Simurgh, Black Div — normalized to *he* in Chapter 04, which the live text had as *it*), and *it* (Div-e Sefid).
5. **Simurgh form (§3.8).** GPT review (2026-10-10): the source-supported bird form is the current visual-prompt proposal; the messenger role in this tale remains project fiction. The revised prose keeps the live text's non-committal presentation (no bird description in the tale).
6. **Shahrasp Persian spelling.** GPT review (2026-10-10) recommends شهراسپ (the dossier's main Persian form) as the project form; the شهرسپ variant remains a signoff note. Glossary promotion is out of scope for this batch.
7. **Tahmures Persian spelling.** **Resolved (2026-10-10, owner-authorized scoped alignment):** Chapters 01–04 use طهمورث in Persian prose and the four tale headings («روایت طهمورث»); the translation validator now enforces the tale heading per chapter range (01–04 طهمورث, 05–24 تهمورث). Chapters 05–24 and the translation glossary keep تهمورث pending a separate book-wide terminology decision; this is not a glossary promotion.
8. **Nariman live label.** **Resolved (2026-10-10):** the revision uses the flood-affected council-member framing (§3.14).
9. **Budhasaf name-collision caution (§3.12).** Keep distinct from Shahrasp and from the scholarly Būdasb hypothesis at all times.
10. **Verse verification.** Tier A labels for the later-cycle figures (Akvan Div, Div-e Sefid, Arzhang Div, Simurgh, Nariman, Sam, Keyumars, Jamshid) rest on the supplied dossier's episode-level claims; verse-level citations are pending and required before any publication-facing source claim. Arash and Garshasp remain Tier B pending verification (§3.9, §3.10); Sam's and Garshasp's dossier entries contain internal contradictions (recorded, unused).
11. **Black Div provenance.** His personal identity and any visual design are adaptations of an unnamed source figure and must never be attributed to Ferdowsi (§3.4; visual-prompt file).
12. **English-site tooltip support.** **Implemented in the narration-refactor phase (2026-10-10):** both sites now carry the character tooltips; see §7.

## 7. Tooltip handling note (content and implementation)

- Both sites now carry the character hover notes: the Persian site through the existing `abbr` extension and `includes/fa-abbreviations.md`, and the English site through the `abbr` extension and `includes/en-character-abbreviations.md` added in the narration-refactor phase (2026-10-10). Reader-facing tooltip copy is the functional sentence from each sheet's general note; approval and source-status caveats stay in this file, outside the tooltips.
- Site tooltips auto-apply to every occurrence of a name (including headings and mentions outside the tales), not only the first mention. `آرش` and `سام` have **no** Persian abbreviations: the definitions would collide with «آرشیو» and «سامانه» in the translation validator. Their notes remain available in this sheet and in the plain prose.
- Every hover note is written to remain fully readable as ordinary text on touch screens or anywhere hover is unavailable.
- The Persian spellings in the abbreviations file are batch-level draft forms pending human confirmation; they are not glossary promotions.
