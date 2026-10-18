# CH01 Godot candidate — Review-finding closure record

- **Status:** CANDIDATE-LOCAL CLOSURE EVIDENCE (2026-10-18). This candidate is a
  **visual animatic candidate**, not a production approval. The screenplay
  supervisory status remains `CH01_ANIMATION_SCREENPLAY_REVISION_REQUIRED`
  upstream; nothing here claims it cleared.
- **Inputs:** `GPT-CH01-animation-screenplay-review.md` (findings F1–F7),
  `prompts/05-glm-ch01-animation-screenplay-revision-1.md` (R1–R7), the live
  tales, the accepted `ch01-video-blueprint.md`, the media registry, and the
  2026-10-18 process-state record.
- **Rule applied:** a screenplay staging inference is never a new story fact.
  All four record-truth buckets are used throughout:
  source facts / staging inferences / production estimates / human art choices.

## Finding dispositions (implemented in this candidate)

### F1 / R1 — S06 cause (CLOSED)
- **Required:** show Simurgh arriving and delivering the wrapped packet,
  followed by Arash dispatching riders; do not make reading the tablet the
  stated cause; do not imply delivery authenticates authority; keep the
  charcoal-burner fires and the villages' fear.
- **Implementation:** `data/chapter-cues.json` scene `CH01-S06` (17 s) is
  beat-structured in `scripts/stage/scene_ch01_s06.gd` as four beats:
  (a) Simurgh arrives at the northern post and hands over the wrapped packet
  (handoff action), (b) Arash dispatches riders — caption text carries the
  source causality ("Simurgh's arrival caused…" is *not* added as dialogue;
  the dispatch follows the visible handoff and the tale states Simurgh's
  arrival caused it), (c) three village rooftops alarmed, (d) eleven
  charcoal-burner fires. Simurgh is added to S06's presence. Neither Simurgh
  nor Arash receives new dialogue. An on-screen boundary note (overlay) states
  delivery is not authentication.

### F2 / R2 — S10 Simurgh carrier (CLOSED)
- **Required:** stage Simurgh as carrier, labelled a production inference;
  remove the unnamed-rider alternative; keep Simurgh's form undecided; the
  seal may remain as a prop only and must not prove identity or grant
  authority.
- **Implementation:** `scripts/stage/scene_ch01_s10.gd` hands the short
  corrective message to the Simurgh stand-in; the scene carries a visible
  "STAGING INFERENCE — carrier not named in the tale" tag in the debug view
  and a concise prop-only seal indication. The seal is visually distinct from
  the dissolved tablet seal (S02) and the S07 card. No new dialogue, no form
  decision, no text added to the message.

### F3 / R3 — Persian prose defects (CLOSED, candidate-local)
The malformed strings called out in the review, and their candidate-local
repairs (in `data/chapter-cues.json` FA texts, the FA caption file, and FA
stand-in/label text):
1. **«فیروزه‌های بی‌نام»** → replaced with **«گروه‌های بی‌نام»** (unnamed
   collectives).
2. **«تراشید و می‌تراشد»** (doubled tense) → one completed action:
   **«دبیر قلم نی خود را تراشید.»** (matches the live tale FA L91–92).
3. **«اختیار یا امنیت را اجباری نمی‌کنند»** → natural boundary wording:
   **«برچسب، کارت یا مُهر به‌تنهایی اختیار نمی‌سازند و امنیتی هم فراهم
   نمی‌کنند.»**
- Preserved throughout: source dialogue verbatim, **طهمورث**, and
  **چاپاری** (indefinite, first mention in NEN/NFA-02) → **چاپار** (definite,
  later reference). No mechanical English-mirror prose.

### F4 / R4 — Style (CLOSED)
- **Required:** current look = provisional working direction only; no
  supersedure of the accepted blueprint; no locked/approved art claims.
- **Implementation:** this candidate renders as a clearly-labelled animatic
  (flat-colour stage graphics, temporary cutouts). The on-screen animatic tag
  reads "PROVISIONAL ANIMATIC — NOT APPROVED ART"; the README and this file
  state that visual style and character-reference selection remain human
  decisions. The accepted blueprint is not edited or reopened.

### F5 / R5 — S09 eight components equal weight (CLOSED)
- **Required:** all eight peer components equal conceptual weight; rows are a
  neutral layout only; remove authority-implying seal icons from review
  questions; keep the exact formula.
- **Implementation:** `scripts/stage/scene_ch01_s09.gd` reveals eight chips of
  identical size/colour in two neutral rows (4+4, no primary/subordinate
  styling); the review questions are posed with neutral numbered dots (no seal
  icons); the formula OST-S09-1 is programmatic text (byte-exact, both
  languages); no laptop/screen icons; a boundary line states authentication
  and enforcement belong to the application, not the prompt.

### F6 / R6 — 173-second budget (CLOSED)
- **Required:** use the revision brief's budget without cutting source lines;
  both tracks within 180 s; cue/hold guidance in dense scenes; timing is an
  estimate only.
- **Implementation:** `data/chapter-cues.json` scenes:
  `12, 16, 10, 15, 15, 17, 31, 15, 20, 15, 7` = **173 s** (≤ 180).
  One visual timeline for both languages; caption timing is provisional
  (estimated from text length, no voice test — claimed nowhere as measured).
  Dense scenes carry per-cue holds so speech, the four S07 labels, the S09
  formula, and overlay reading do not compete (S06: 3 narration sub-cues +
  beat actions; S07: 31 s split across 6 sub-beats; S09: formula hold while
  chips reveal; S10: 3 sub-cues + handoff/return actions).
  The old 149 s plan and compact variant are superseded by this budget; no
  owner runtime choice is posed.
- **Justified deviations from the starting budget:** none — the candidate uses
  the budget exactly as given.

### F7 / R7 — Record truth and media order (CLOSED)
- **Implementation:** `data/chapter-cues.json` separates the four
  record-truth buckets and marks each scene's truth class and any staging
  inference. The Div-e Sefid hook is **outside this sequence** (not staged).
  Runtime is a production estimate, not an owner choice. The S10 carrier is a
  staging inference. NFA-09 is a documented spoken-flow adaptation (VO:
  «چه می‌کند», plural imperative «ثبت کنید») while OST-S11-1 keeps the
  tale-verbatim written ledger line («چه کاری انجام می‌دهد», singular
  imperative «ثبت کن»). The scene order is a **deliberate media adaptation**
  (engineering overlay before the second message; ledger/end card closing),
  not literal manuscript order — recorded in the cue plan and the README.
  The inherited FA-11 timing-note contamination in the old narration file is
  **out of scope** and that file was not edited.

## Additional inherited defects noted (not re-implemented silently)

- **OV-01-04 mis-attribution:** the blueprint manifest assigns the four-label
  plate to S05 and its SVG holds only three «؟» labels, while the blueprint
  shot spec places the four labels in S07 (fourth with a seal icon). This
  candidate does **not** reuse `OV-01-04` as the S07 four-label plate; it
  renders its own programmatic label ticks (OST-S07-1…4) with all four labels
  per the shot spec. Flagged for the owner/blueprint reconciliation, not
  fixed in the blueprint (out of scope).
- **FA-11 contamination** in `ch01-narration.yml/.md` (timing note merged into
  the text field): out of scope; this candidate's FA-11 text is the clean
  tale line.
- **Blueprint `title:` field** has unescaped quotes (invalid YAML in the
  recorded file): out of scope; noted here only.

## What this candidate does NOT claim

- No screenplay production approval; no human signoff; no visual-style lock;
  no character-art approval; no voice/narration approval; no publication
  acceptance.
- No mouth motion for spoken cues unless the owner separately enables the
  two-state `open_test` proxy (off by default); that proxy is not lip-sync.
- All timings are paper estimates pending recorded speech.
