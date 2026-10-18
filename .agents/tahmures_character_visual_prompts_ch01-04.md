# Tahmures — Character Visual-Generation Prompts, Chapters 01–04

**Status:** `PROMPT_DRAFTS_FOR_HUMAN_SUPERVISED_GENERATION`
**Phase:** `CH01_04_CHARACTER_NARRATIVE_REFACTOR` (bounded corrections to the `CH01_04_CHARACTER_REFERENCE_PACK` output)
**Date:** 2026-10-10. GPT reviewed the reference pack; the bounded corrections it required were applied on 2026-10-10. The prompts remain drafts pending human approval of the designs.

## What this file is

- One standalone image-generation prompt and a negative prompt for every named
  character in `.agents/tahmures_character_behaviors_ch01-04.md`, plus one
  role-based prompt for Chapar. **No image-generation service was called and no
  image files were created in this phase.**
- These are prompt drafts for later human-supervised generation. Generating from
  them does not approve, freeze, or add any asset to the registry. Every output is
  a **candidate requiring human selection**.
- The approved master (below) is Tahmures's identity anchor. For every other
  figure, the prompts describe an **original 2D cartoon language compatible with
  the master**, with a distinct silhouette, face, palette accent, costume, and prop
  per character. All costumes and settings are Iranian-inspired **project fiction**,
  not claimed historical reconstruction.
- Where the supplied dossier is silent about a figure's appearance, the design is
  marked `UNLOCKED_ARTISTIC_CHOICE` and is a design proposal, not a source claim.
  No source-canonical costume, facial features, weapons, powers, or colors were
  invented and attributed to tradition.

## 0. Verified master reference

- **Path:** `Characters/tahmures/versions/layout01-v2/source/approved_master.png`
- **Expected SHA-256:** `3eedfaa5a41965c45a137a74a9137c6e59304a0604f877a81c98870c64dba2e5`
- **Verification performed programmatically by GLM (no visual inspection):** GLM checked
  file identity and palette programmatically only — SHA-256 recomputed and matched;
  1086 × 1448 RGBA PNG confirmed; palette and layout measured by pure-Python pixel
  analysis (dominant deep blue ≈ `#113366` in robe regions, ivory ≈ `#ffeebb`,
  burgundy ≈ `#772222` concentrated in the torso band, gold ≈ `#dd9933` at the
  crown and distributed across the robe, near-black outline/hair colors, warm skin
  tone); structure corroborated by `Characters/tahmures/extraction_report.md`
  (sclera/eye components, dark hair masses, beard and moustache pigments,
  `diadem_gold` sprite with round emblem contour) and
  `Characters/tahmures/versions/layout01-v2/manifest.json` (`head/diadem_gold.png`).
  GLM did **not** view the image; these checks are not visual confirmation.
- **Visible traits (visually confirmed by GPT during the supervisory review of the
  reference pack):** clean dark outlines;
  expressive, simplified cartoon facial shapes; large readable eyes; controlled
  cel-like shading; dark wavy hair and beard; a gold diadem with a central round
  sun medallion; a deep blue robe with repeating gold motifs; an ivory tunic; and a
  burgundy sash.
- **Influence handling (owner-reported):** the ChatGPT-created master was designed
  with a Rick and Morty influence. That influence is translated here into **general
  visual descriptors only**: bold clean line work, simplified geometric facial
  construction, large expressive eyes, flat cel-like shading, modern animation
  readability. **Do not** ask any image model to copy the Rick and Morty series,
  its characters, its logo, its exact model sheets, or its signature designs, and
  do not insert Rick, Morty, or any unrelated franchise imagery.

## 1. Shared series constraints (embedded in every prompt)

Every prompt below is standalone and embeds these constraints, derived from the
approved master:

- **Style:** 2D flat-color cartoon character illustration; clean uniform dark
  outlines; simplified expressive cartoon facial construction; large readable
  eyes; controlled cel-like shading with flat color areas and minimal gradients;
  limited palette; confident simplified shapes.
- **Composition:** single character, full body, standing, front-facing
  three-quarter view suitable for a character reference sheet; centered on a plain
  flat neutral background; no scenery; no other characters.
- **Costume world:** ancient Iranian-inspired fictional court and provincial
  costume (wrapped robes, sashes, tunics, trousers, headbands, felt caps) —
  original project fiction, not historical reconstruction.
- **Universal exclusions:** no readable text, letters, or numbers; no watermark,
  signature, or logo; no modern clothing, accessories, or technology; no
  European-medieval costume elements (plate armour, mail, European crowns, pointed
  medieval hats); no religious or caricatured imagery; no duplicate of Tahmures's
  identity features (gold diadem with sun medallion, deep-blue robe with gold
  motifs, ivory tunic with burgundy sash combination); do not copy any existing
  franchise.
- **Div characters:** depict divs as capable, dignified, non-human court personages
  — not monsters and not devil-coded: no glowing red eyes, no fangs, no flames, no
  menacing grins.

## 2. Character prompts

### 2.1 Tahmures — protagonist (Chapters 01–04)

**Chapters:** 01, 02, 03, 04. **Design provenance:** all identity elements anchored
to the owner-approved master (an approved project asset — not a claim about
Ferdowsi's text). Do not redesign his face, palette, diadem, beard, or clothing
identity.

**Prompt:**

> Faithful full-body character reference sheet of Tahmures, matching the approved
> master image (Characters/tahmures/versions/layout01-v2/source/approved_master.png,
> SHA-256 3eedfaa5a41965c45a137a74a9137c6e59304a0604f877a81c98870c64dba2e5): a
> king with dark wavy shoulder-length hair and a full dark beard; warm medium skin
> tone; large readable dark eyes with a calm, intelligent expression; simplified
> cartoon facial construction with clean uniform dark outlines; a gold diadem
> across the brow with a central round sun medallion; a deep blue robe decorated
> with small repeating gold motifs over an ivory tunic, bound with a burgundy
> sash. Standing upright, front-facing three-quarter view, arms relaxed, on a
> plain flat neutral background. 2D flat-color cartoon style with clean dark
> outlines, large expressive eyes, controlled cel-like shading, and a limited
> palette. Ancient Iranian-inspired fictional royal costume; not a historical
> reconstruction. No text, letters, numbers, watermark, logo, modern elements,
> European-medieval crown or armour, or other characters. Do not copy any existing
> franchise; keep the face, hair, diadem, beard, palette, and clothing identity
> exactly consistent with the reference.

**Negative prompt:**

> photorealism; 3D render; painterly texture; changing the face, diadem, beard,
> hair, palette, or clothing identity; text, letters, numbers; watermark, logo,
> signature; modern clothing or technology; European-medieval crown, plate armour,
> mail; Rick and Morty characters, Rick Sanchez, Morty Smith, Adult Swim imagery,
> any franchise character or logo; extra limbs; deformed hands; busy background;
> additional characters.

**Note:** candidate only; requires human selection. This prompt anchors identity,
not a final asset.

### 2.2 Shahrasp — First Scribe (Chapters 01–04)

**Design provenance:** `UNLOCKED_ARTISTIC_CHOICE` throughout. The supplied
dossier describes his character (pious, restrained, truthful) but no physical
appearance, and the "First Scribe" function is this project's adaptation. Do not
depict religious garb specifics; keep a court scribe.

**Prompt:**

> Original 2D flat-color cartoon character reference sheet of Shahrasp, the First
> Scribe of King Tahmures's hall: a lean, quiet human court scribe in his thirties
> or forties; neat short dark hair with a light, short-trimmed beard (clearly
> distinct from Tahmures's full beard); thoughtful, observant expression with
> large readable eyes; a plain sage-green robe with simple dark trim and a
> modest cloth headband (no gold sun medallion); ink-stained fingers; holding an
> open bound experiment ledger in one hand and a reed pen in the other. Standing
> slightly angled as if taking notes, full body, front-facing three-quarter view,
> on a plain flat neutral background. Clean uniform dark outlines; simplified
> expressive cartoon facial construction; controlled cel-like shading; limited
> palette. Ancient Iranian-inspired fictional court costume, not a historical
> reconstruction. No text, letters, numbers, watermark, logo, modern elements,
> European-medieval costume, franchise characters, or duplication of Tahmures's
> identity features (gold sun-medallion diadem, deep-blue robe with gold motifs,
> burgundy sash).

**Negative prompt:**

> photorealism; 3D render; painterly texture; religious vestments, priest robes,
> turban; text, letters, numbers on the ledger or elsewhere; watermark, logo,
> signature; modern clothing, eyeglasses, wristwatch; European-medieval costume;
> Rick and Morty or any franchise character; gold sun-medallion diadem; deep-blue
> robe with gold motifs; extra limbs; deformed hands; busy background; additional
> characters.

**Note:** candidate only; requires human selection.

### 2.3 Akvan Div — Keeper of Scripts (Chapters 01, 04)

**Design provenance:** div-ness with small horns is a general traditional Persian
div motif; all specifics (skin tone, costume, props, feminine presentation
following the current English text's "she") are `UNLOCKED_ARTISTIC_CHOICE`. The
source identity (a later-cycle div) is not visually asserted; nothing here comes
from Ferdowsi.

**Prompt:**

> Original 2D flat-color cartoon character reference sheet of Akvan Div, the
> Keeper of Scripts in King Tahmures's Hall of Scripts: a tall, slender, composed
> div — a capable, dignified non-human court personage, not a monster — with
> slate-teal skin, small backward-curving horns, calm focused large eyes, and a
> feminine facial presentation; neat dark work robe with a copper-trimmed sash;
> holding a small stack of clay tablets tied with plain blank catalogue tags
> (tags carry no readable text). Standing upright beside a low shelf of blank
> tablets, full body, front-facing three-quarter view, on a plain flat neutral
> background. Clean uniform dark outlines; simplified expressive cartoon facial
> construction; controlled cel-like shading; limited palette. Ancient
> Iranian-inspired fictional court costume, not a historical reconstruction. No
> glowing red eyes, fangs, flames, or menacing grin; no text, letters, numbers,
> watermark, logo, modern elements, European-medieval costume, franchise
> characters, or duplication of Tahmures's identity features.

**Negative prompt:**

> photorealism; 3D render; painterly texture; monster design, devil imagery,
> glowing red eyes, fangs, claws dripping, flames, menacing grin; readable text or
> letters on tablets or tags; watermark, logo, signature; modern elements;
> European-medieval costume; Rick and Morty or any franchise character; gold
> sun-medallion diadem; deep-blue robe with gold motifs; extra limbs; deformed
> hands; busy background; additional characters.

**Note:** candidate only; requires human selection. Gender presentation follows
the current English text (she/her) and remains a `GPT_REVIEW_REQUIRED` item (see
the behavior file, §6.4).

### 2.4 Black Div — Literal Div (Chapters 01, 04)

**Design provenance:** `UNLOCKED_ARTISTIC_CHOICE` throughout. The personal
identity given to the Black Div is an adaptation of a figure the source describes
**without a personal name**; his visual design must not be attributed to Ferdowsi
or to any source tradition. Dark coloration echoes only the unnamed "black div"
description; everything else is a design proposal. Not villain-coded.

**Prompt:**

> Original 2D flat-color cartoon character reference sheet of the Black Div, the
> Literal Div who serves in King Tahmures's hall: a broad, heavyset, earnest div
> — a capable, dignified non-human personage, not a monster — with deep
> charcoal-grey skin, small blunt horns, warm amber eyes, and an honest,
> hard-working expression; simple practical dark work wrap and a ragged travel
> cloak; holding a wet clay tablet wrapped in a rag, clothing slightly damp as if
> just returned from wading a river. Standing squarely, slightly tired but
> dutiful, full body, front-facing three-quarter view, on a plain flat neutral
> background. Clean uniform dark outlines; simplified expressive cartoon facial
> construction; controlled cel-like shading; limited palette. Ancient
> Iranian-inspired fictional servant costume, not a historical reconstruction. No
> glowing red eyes, fangs, flames, or menacing grin; no text, letters, numbers,
> watermark, logo, modern elements, European-medieval costume, franchise
> characters, or duplication of Tahmures's identity features.

**Negative prompt:**

> photorealism; 3D render; painterly texture; monster design, devil imagery,
> glowing red eyes, fangs, flames, sinister shadows, menacing grin; readable text
> on the tablet; watermark, logo, signature; modern elements; European-medieval
> costume; Rick and Morty or any franchise character; gold sun-medallion diadem;
> deep-blue robe with gold motifs; extra limbs; deformed hands; busy background;
> additional characters.

**Note:** candidate only; requires human selection. This design is an adaptation
of an unnamed source figure and implies no source-canonical appearance.

### 2.5 Div-e Sefid — Mirror Div (Chapters 01 hook, 02)

**Design provenance:** pale/white coloration is supported by the name (Div-e
Sefid, the White Div); all other specifics are `UNLOCKED_ARTISTIC_CHOICE`. The
later-cycle source identity is not visually asserted, and the figure must not be
drawn as malicious by default.

**Prompt:**

> Original 2D flat-color cartoon character reference sheet of Div-e Sefid, the
> Mirror Div of King Tahmures's court: a slender, elegant, composed div — a
> capable, dignified non-human personage, not a monster — with pale ivory-white
> skin, soft grey-blue markings, silver hair, and a thoughtful, self-possessed
> expression with large readable eyes; a pale robe with silver-grey trim;
> holding a polished round hand mirror in one hand and a folded torn document
> fragment in the other. Standing gracefully, full body, front-facing
> three-quarter view, on a plain flat neutral background. Clean uniform dark
> outlines; simplified expressive cartoon facial construction; controlled
> cel-like shading; limited palette. Ancient Iranian-inspired fictional court
> costume, not a historical reconstruction. No glowing red eyes, fangs, flames,
> or menacing grin; no text, letters, numbers, watermark, logo, modern elements,
> European-medieval costume, franchise characters, or duplication of Tahmures's
> identity features.

**Negative prompt:**

> photorealism; 3D render; painterly texture; monster design, devil imagery,
> glowing red eyes, fangs, flames, sinister smirk, evil witch aesthetic; readable
> text on the document; watermark, logo, signature; modern elements;
> European-medieval costume; Rick and Morty or any franchise character; gold
> sun-medallion diadem; deep-blue robe with gold motifs; extra limbs; deformed
> hands; busy background; additional characters.

**Note:** candidate only; requires human selection.

### 2.6 Arzhang Div — Council's Div (Chapter 03)

**Design provenance:** `UNLOCKED_ARTISTIC_CHOICE` throughout; the later-cycle
source identity is not visually asserted. Not evil-coded; his chapter failure
belongs to the requirements owner, not to wickedness.

**Prompt:**

> Original 2D flat-color cartoon character reference sheet of Arzhang Div, the
> council's div in King Tahmures's Council Chamber: a round, portly, genial div —
> a capable, dignified non-human personage, not a monster — with terracotta-red
> skin, small horns, warm sandy-yellow robe accents, and an eager, helpful,
> slightly flustered expression with large readable eyes; a comfortable robe with
> a wide sash; holding a small wooden model of a timber bridge in both hands.
> Standing cheerfully, full body, front-facing three-quarter view, on a plain
> flat neutral background. Clean uniform dark outlines; simplified expressive
> cartoon facial construction; controlled cel-like shading; limited palette.
> Ancient Iranian-inspired fictional court costume, not a historical
> reconstruction. No glowing red eyes, fangs, flames, or menacing grin; no text,
> letters, numbers, watermark, logo, modern elements, European-medieval costume,
> franchise characters, or duplication of Tahmures's identity features.

**Negative prompt:**

> photorealism; 3D render; painterly texture; monster design, devil imagery,
> glowing red eyes, fangs, flames, menacing grin; readable text or numbers;
> watermark, logo, signature; modern elements; European-medieval costume; Rick
> and Morty or any franchise character; gold sun-medallion diadem; deep-blue robe
> with gold motifs; extra limbs; deformed hands; busy background; additional
> characters.

**Note:** candidate only; requires human selection.

### 2.7 Soroush — Archivist (Chapters 02, 03 hook, 04)

**Design provenance:** `UNLOCKED_ARTISTIC_CHOICE` throughout; the Avestan yazata
identity is not visually asserted (no wings, halo, or divine imagery). Feminine
presentation follows the current English text (she/her) and is a
`GPT_REVIEW_REQUIRED` item.

**Prompt:**

> Original 2D flat-color cartoon character reference sheet of Soroush, the
> Archivist of the Royal Archive in King Tahmures's reign: a careful, quiet human
> archivist of medium build with a patient, precise expression and large readable
> eyes; dark hair pinned back under a plain cloth headband; feminine facial
> presentation; an ochre-brown robe with a simple sash; carrying a bundle of clay
> tablets and rolled records bound with knotted seal-cords, one seal held up for
> inspection. Standing evenly, full body, front-facing three-quarter view, on a
> plain flat neutral background. Clean uniform dark outlines; simplified
> expressive cartoon facial construction; controlled cel-like shading; limited
> palette. Ancient Iranian-inspired fictional court costume, not a historical
> reconstruction, and not religious dress. No readable text, letters, numbers,
> watermark, logo, modern elements, European-medieval costume, franchise
> characters, divine attributes such as wings or halos, or duplication of
> Tahmures's identity features.

**Negative prompt:**

> photorealism; 3D render; painterly texture; religious vestments; wings, halo,
> divine glow; readable text on tablets or scrolls; watermark, logo, signature;
> modern elements; European-medieval costume; Rick and Morty or any franchise
> character; gold sun-medallion diadem; deep-blue robe with gold motifs; extra
> limbs; deformed hands; busy background; additional characters.

**Note:** candidate only; requires human selection.

### 2.8 Simurgh — Messenger (Chapter 01)

**Design provenance:** a majestic giant wise bird is the source-supported
identity (the *Shahnameh*'s Simurgh of the Zal/Rostam cycle, per the supplied
dossier); plumage colors, courier gear, and human-scale rendering are
`UNLOCKED_ARTISTIC_CHOICE`. **The form decision (bird-form court messenger vs.
human courier bearing the name) is `GPT_REVIEW_REQUIRED`** (behavior file §3.8);
this draft depicts the bird form as the primary proposal.

**Prompt:**

> Original 2D flat-color cartoon character reference sheet of Simurgh, the
> Messenger of King Tahmures's Hall of Scripts: a majestic, dignified mythical
> bird of roughly human height or taller, standing upright in courier posture;
> dark teal-blue plumage with metallic gold chest and wing accents; a strong
> crest and long tail feathers; a large, wise, readable eye rendered in the
> series' simplified cartoon style; an oilcloth-wrapped packet and a slim
> courier tube slung on a cord across the chest; watchful, composed expression.
> Full body, front-facing three-quarter view, on a plain flat neutral background.
> Clean uniform dark outlines; simplified expressive construction; controlled
> cel-like shading; limited palette. Iranian-inspired project-fiction fantasy
> design, not a historical reconstruction. No flames or phoenix fire imagery, no
> human face, no text, letters, numbers, watermark, logo, modern elements,
> European-medieval imagery, franchise characters, or duplication of Tahmures's
> identity features.

**Negative prompt:**

> photorealism; 3D render; painterly texture; flames, fire bird, phoenix burning
> imagery; human face on a bird body; skeletal or vulture-like menace; readable
> text; watermark, logo, signature; modern elements; European-medieval imagery;
> Rick and Morty or any franchise character; gold sun-medallion diadem; extra
> limbs; deformed features; busy background; additional characters.

**Note:** candidate only; requires human selection. If GPT review selects the
human-courier option instead, this prompt is replaced, not blended.

### 2.9 Arash — current captain / Gatekeeper (Chapters 01, 03, 04)

**Design provenance:** `UNLOCKED_ARTISTIC_CHOICE` throughout; the border-archer
legend is **not** depicted (no bow, no arrow) so the source story is not conflated
with the chapter roles. Whether to add a bow as a source-flavored prop is an
owner decision, deliberately not taken here.

**Prompt:**

> Original 2D flat-color cartoon character reference sheet of Arash, captain of
> the northern frontier and Gatekeeper in King Tahmures's service: an athletic,
> alert human guard captain; short black hair, clean-shaven or with a very short
> beard; dutiful, watchful expression with large readable eyes; bronze-studded
> leather-and-cloth guard uniform with iron-grey accents; a plain cloth
> headband; holding a tall gate staff with a ring of keys hanging from it;
> confident, ready stance. Full body, front-facing three-quarter view, on a
> plain flat neutral background. Clean uniform dark outlines; simplified
> expressive cartoon facial construction; controlled cel-like shading; limited
> palette. Ancient Iranian-inspired fictional guard costume, not a historical
> reconstruction. No bow and arrow; no readable text, letters, numbers,
> watermark, logo, modern elements, European-medieval plate armour or mail,
> franchise characters, or duplication of Tahmures's identity features.

**Negative prompt:**

> photorealism; 3D render; painterly texture; bow, arrows, archery pose;
> European-medieval plate armour, mail, knight helmet; readable text; watermark,
> logo, signature; modern elements; Rick and Morty or any franchise character;
> gold sun-medallion diadem; deep-blue robe with gold motifs; extra limbs;
> deformed hands; busy background; additional characters.

**Note:** candidate only; requires human selection.

### 2.10 Garshasp — remembered captain of the prior court (Chapter 01, offstage)

**Design provenance:** `UNLOCKED_ARTISTIC_CHOICE` throughout; the dossier's
contradictory genealogy details are unused, and no source heroics (dragon-slaying
and the like) are depicted. He is offstage in the live text, so this art is for
optional flashback or companion use only.

**Prompt:**

> Original 2D flat-color cartoon character reference sheet of Garshasp, a
> remembered captain from the court of Tahmures's father: a broad-shouldered,
> weathered veteran soldier; grey-streaked dark hair and a short grey-flecked
> beard; lined face with a stern, dignified expression and large readable eyes;
> an iron-grey cloak over a faded indigo tunic with a simple belt; holding an
> old clay command tablet bearing only an abstract, unreadable carved mark.
> Standing at rest with a veteran's bearing, full body, front-facing
> three-quarter view, on a plain flat neutral background. Clean uniform dark
> outlines; simplified expressive cartoon facial construction; controlled
> cel-like shading; limited palette. Ancient Iranian-inspired fictional soldier's
> costume, not a historical reconstruction. No readable text, letters, numbers,
> watermark, logo, modern elements, European-medieval armour, franchise
> characters, dragon-slaying imagery, or duplication of Tahmures's identity
> features.

**Negative prompt:**

> photorealism; 3D render; painterly texture; readable text on the tablet;
> dragon, monster, or battle scene; European-medieval armour; watermark, logo,
> signature; modern elements; Rick and Morty or any franchise character; gold
> sun-medallion diadem; deep-blue robe with gold motifs; extra limbs; deformed
> hands; busy background; additional characters.

**Note:** candidate only; requires human selection. Offstage character; art is
optional until an editorial decision includes him visually.

### 2.11 Jamshid — governor / treasurer / former governor (Chapters 02, 03, 04)

**Design provenance:** `UNLOCKED_ARTISTIC_CHOICE` throughout; the successor-king
source identity is not visually asserted (no royal regalia beyond tasteful
official dress; no crown).

**Prompt:**

> Original 2D flat-color cartoon character reference sheet of Jamshid, a
> prosperous governor and treasurer of King Tahmures's realm: a well-groomed
> human official; neatly trimmed black beard, confident, shrewd expression with
> large readable eyes; a deep emerald-green robe with fine gold trim and a tidy
> sash; holding a small balance scale in one hand with a neat stack of silver
> coin-marks beside his other arm. Standing with an administrator's upright
> poise, full body, front-facing three-quarter view, on a plain flat neutral
> background. Clean uniform dark outlines; simplified expressive cartoon facial
> construction; controlled cel-like shading; limited palette. Ancient
> Iranian-inspired fictional official costume, not a historical reconstruction.
> No crown or royal regalia; no readable text, letters, numbers, watermark,
> logo, modern elements, European-medieval costume, franchise characters, or
> duplication of Tahmures's identity features.

**Negative prompt:**

> photorealism; 3D render; painterly texture; crown, royal sceptre, throne;
> readable text or numbers; watermark, logo, signature; modern elements;
> European-medieval royal costume; Rick and Morty or any franchise character;
> gold sun-medallion diadem; deep-blue robe with gold motifs; burgundy sash with
> ivory tunic; extra limbs; deformed hands; busy background; additional
> characters.

**Note:** candidate only; requires human selection. The owner fixed the Chapter 02
assignment (2026-10-10): Jamshid is the eastern governor, the one who smiles; this
does not affect the design.

### 2.12 Budhasaf — governor with a competing claim (Chapter 02)

**Design provenance:** `UNLOCKED_ARTISTIC_CHOICE` throughout; identity is
`UNVERIFIED_SOURCE_LEAD` (behavior file §3.12). He must not resemble Shahrasp
and must not be depicted as the scholarly "minister Budhasb" hypothesis or as
Shahrasp under another name.

**Prompt:**

> Original 2D flat-color cartoon character reference sheet of Budhasaf, a sturdy
> provincial governor of King Tahmures's realm: a practical, weather-tanned
> human official; short dark beard; direct, assertive expression with large
> readable eyes; a mustard-saffron robe with deep brown trim and a broad belt;
> holding a sealed clay grain jar against his hip. Standing firmly, full body,
> front-facing three-quarter view, on a plain flat neutral background. Clean
> uniform dark outlines; simplified expressive cartoon facial construction;
> controlled cel-like shading; limited palette. Ancient Iranian-inspired
> fictional provincial costume, not a historical reconstruction. Visually
> distinct from any scribe character. No readable text, letters, numbers,
> watermark, logo, modern elements, European-medieval costume, franchise
> characters, religious imagery, or duplication of Tahmures's identity features.

**Negative prompt:**

> photorealism; 3D render; painterly texture; resembling a scribe, scholar, or
> priest; readable text; watermark, logo, signature; modern elements;
> European-medieval costume; Rick and Morty or any franchise character; gold
> sun-medallion diadem; deep-blue robe with gold motifs; extra limbs; deformed
> hands; busy background; additional characters.

**Note:** candidate only; requires human selection. Unverified source identity
remains flagged in all downstream uses.

### 2.13 Keyumars — builder, deceased king (Chapters 03, 04)

**Design provenance:** `UNLOCKED_ARTISTIC_CHOICE` throughout; the first-king
source identity is not visually asserted (no royal regalia). A single elder
design serves both chapters; his Chapter 04 presence is posthumous.

**Prompt:**

> Original 2D flat-color cartoon character reference sheet of Keyumars, an
> elderly master builder and former king in King Tahmures's world: a
> straight-backed old man; long white beard, weathered, kindly face with deep
> lines and large readable eyes; a limestone-pale robe with pale verdigris
> accents and a simple undecorated cloth band; holding a wooden mason's mallet
> in one hand and a worn architectural plan tablet bearing only abstract,
> unreadable marks in the other. Standing with quiet craft-dignity, full body,
> front-facing three-quarter view, on a plain flat neutral background. Clean
> uniform dark outlines; simplified expressive cartoon facial construction;
> controlled cel-like shading; limited palette. Ancient Iranian-inspired
> fictional builder's dress, not a historical reconstruction. No crown or royal
> regalia; no readable text, letters, numbers, watermark, logo, modern elements,
> European-medieval costume, franchise characters, or duplication of Tahmures's
> identity features.

**Negative prompt:**

> photorealism; 3D render; painterly texture; crown, royal regalia, throne;
> skeletal or ghost imagery; readable text on the plan tablet; watermark, logo,
> signature; modern elements; European-medieval costume; Rick and Morty or any
> franchise character; gold sun-medallion diadem; deep-blue robe with gold
> motifs; extra limbs; deformed hands; busy background; additional characters.

**Note:** candidate only; requires human selection. The owner fixed the timeline
(2026-10-10): Keyumars is the living Chapter 03 builder, and Chapter 04 opens six
years after his death; the single elder design serves both.

### 2.14 Nariman — flood-affected council member (Chapter 03)

**Design provenance:** `UNLOCKED_ARTISTIC_CHOICE` throughout; the Sistani-lineage
source identity is not visually asserted. He is a flood-affected council member (a
farmer whose fields the flood cut off), not the holder of a river-keeping office.

**Prompt:**

> Original 2D flat-color cartoon character reference sheet of Nariman, a
> flood-affected council member from the Varena riverlands: a wiry, weather-worn
> farmer; tanned
> skin, short greying hair, short beard; grounded, watchful expression with
> large readable eyes; a storm blue-grey work tunic with rolled sleeves and a
> rope belt; holding a long flood-gauge staff marked only with abstract level
> notches (no readable numbers). Standing steady as if braced against a current,
> full body, front-facing three-quarter view, on a plain flat neutral background.
> Clean uniform dark outlines; simplified expressive cartoon facial
> construction; controlled cel-like shading; limited palette. Ancient
> Iranian-inspired fictional workman's costume, not a historical reconstruction.
> No readable text, letters, numbers, watermark, logo, modern elements,
> European-medieval costume, franchise characters, water or river scenery, or
> duplication of Tahmures's identity features.

**Negative prompt:**

> photorealism; 3D render; painterly texture; readable numbers on the staff;
> river, waves, or scenery; watermark, logo, signature; modern elements such as
> rubber boots or rain gear with modern fasteners; European-medieval costume;
> Rick and Morty or any franchise character; gold sun-medallion diadem;
> deep-blue robe with gold motifs; extra limbs; deformed hands; busy background;
> additional characters.

**Note:** candidate only; requires human selection.

### 2.15 Sam — orchard keeper (Chapter 04)

**Design provenance:** `UNLOCKED_ARTISTIC_CHOICE` throughout; the epic-champion
source identity is not visually asserted (no warrior imagery, no famous weapon).

**Prompt:**

> Original 2D flat-color cartoon character reference sheet of Sam, the keeper of
> the orchard that was once the cypress garden: a stocky, warm-faced orchard
> keeper; sun-browned skin, short dark beard; patient, unassuming expression
> with large readable eyes; a russet-brown tunic with a straw-colored work
> apron; holding a wicker basket of round fruit in one hand, a pruning knife
> sheathed at his belt. Standing at ease among nothing but the plain background,
> full body, front-facing three-quarter view, on a plain flat neutral background.
> Clean uniform dark outlines; simplified expressive cartoon facial
> construction; controlled cel-like shading; limited palette. Ancient
> Iranian-inspired fictional workman's costume, not a historical reconstruction.
> No warrior imagery or weapons beyond the pruning knife; no readable text,
> letters, numbers, watermark, logo, modern elements, European-medieval costume,
> franchise characters, or duplication of Tahmures's identity features.

**Negative prompt:**

> photorealism; 3D render; painterly texture; warrior, armour, club, mace, or
> epic-hero poses; readable text; watermark, logo, signature; modern elements;
> European-medieval costume; Rick and Morty or any franchise character; gold
> sun-medallion diadem; deep-blue robe with gold motifs; extra limbs; deformed
> hands; busy background; additional characters.

**Note:** candidate only; requires human selection.

### 2.16 Chapar — courier (Chapter 01, role-based prompt)

**Design provenance:** role-based prompt for a Persian courier occupation —
`UNLOCKED_ARTISTIC_CHOICE` for all specifics. This deliberately does **not**
invent a named mythic figure; "Chapar" is the occupational word.

**Prompt:**

> Original 2D flat-color cartoon character reference sheet of a Persian chapar
> courier of King Tahmures's realm (an occupational role, not a named mythic
> figure): a lean, road-worn human courier; dusty travel cloak over a simple
> tunic and trousers; soft cap and worn boots; a bronze message tube on a
> shoulder strap and a small satchel at the hip; hurried but careful posture,
> mid-stride stance, alert expression with large readable eyes. Full body,
> front-facing three-quarter view, on a plain flat neutral background. Clean
> uniform dark outlines; simplified expressive cartoon facial construction;
> controlled cel-like shading; limited palette. Ancient Iranian-inspired
> fictional courier costume, not a historical reconstruction. No readable text,
> letters, numbers, watermark, logo, modern elements, European-medieval costume,
> franchise characters, horse or scenery, or duplication of Tahmures's identity
> features.

**Negative prompt:**

> photorealism; 3D render; painterly texture; readable text on the message tube;
> horse, relay station, or scenery; watermark, logo, signature; modern elements
> such as a courier bag with modern straps and buckles; European-medieval
> costume; Rick and Morty or any franchise character; gold sun-medallion diadem;
> deep-blue robe with gold motifs; extra limbs; deformed hands; busy background;
> additional characters.

**Note:** candidate only; requires human selection. Distinct from the Messenger
(Simurgh) in both behavior and art.

## 3. Open art questions for GPT review

1. **Akvan Div and Soroush presentation** (§2.3, §2.7): current English text uses
   she/her for both roles; the approved names carry other traditional
   associations. Final pronoun/presentation decision pending (behavior file §6.4);
   prompts currently follow the live text.
2. **Simurgh form** (§2.8): bird-form court messenger (current draft) vs. human
   courier bearing the name.
3. **Arash's prop** (§2.9): a bow was deliberately excluded to avoid importing the
   border-archer source motif; adding it would be an explicit owner choice.
4. **Jamshid/Budhasaf east-west assignment** (behavior file §6.1): resolved by the
   owner (2026-10-10) — Jamshid is the eastern governor, Budhasaf the western;
   neither design changes.
5. **Keyumars single-design question** (§2.13): one elder design serves the
   Chapter 03 builder and the Chapter 04 posthumous reference; the owner fixed
   the timeline (alive in Ch03, Ch04 six years after his death).
6. **Garshasp art necessity** (§2.10): he is offstage; producing art at all is an
   editorial decision.
7. **Negative-prompt tuning**: the shared negative blocks are drafts; each
   generation service may need its own syntax adjustments at generation time.

None of the prompts above implies that any generated art exists, is approved, or
has been added to any registry.
