# Qwen — Independent Review: Chapter 01 Static Board & S01 Preparation

Reviewer role: independent Qwen reviewer. Scope: static Chapter 01 board and S01
production preparation. This is a **review only** — no implementation, no
animation, no character redesign, no owner approval, no phase-state mutation.

This report is created for handoff to Codex. Its existence is **not** approval,
and it grants no owner signoff.

---

## 1. Review basis and access limits

### Content inspected directly (repository checkout)

- `Characters/animations/chapter-01-candidate-01/planning/shot-board.json` (full: header, 34 captions, 18 OST, risks, owner_choices, 34 shots).
- `Characters/animations/chapter-01-candidate-01/planning/missing-asset-action-matrix.json` (full, 47 rows).
- `Characters/animations/chapter-01-candidate-01/planning/s01-proof-specification.md` (full).
- `Characters/animations/chapter-01-candidate-01/planning/board-validation.json` (full).
- `Characters/animations/chapter-01-candidate-01/planning/s01-caption-layout-check.json` (full).
- `editorial/media-handoff/chapter-01-production-plan.json` (full structure + cue/OST/scene cross-check).
- `editorial/media-handoff/chapter-01-animation-status.json` (full).
- `editorial/media-handoff/2026-10-20-tahmures-beard-repair.md` (full).
- `book/part-1/01-what-is-a-prompt.md` (full — canonical story/bridge).
- `book/fa/part-1/01-what-is-a-prompt.md` (tale region, for Persian caption faithfulness).
- `book/narrative-continuity.md` (characters section, L12–303).

### Images inspected directly (pixels, not filenames)

- `Characters/Shahrasp.png` — **source art reference**: right hand holds a raised
  reed pen; left hand/arm cradles a closed brown book. Both hands occupied by
  stock props. (Essential for the S01 prop-conflict judgment.)
- `planning/panels/ch01-s01-a.png` — wide establish; Shahrasp (book+reed) at
  right-center, feet on floor, clear of the right bench; amber caption-safe band.
- `planning/panels/ch01-s01-b.png` — contact insert shown **only** as an amber
  "shahrasp / CONTACT ART / NOT YET BUILT" marker over a flat wall crop; no
  rendered performance.
- `planning/panels/ch01-s01-c.png` — wide material reprise; book+reed pose.
- `planning/s01-caption-layout-en-nen-01a.png` — EN LTR, single line, in-band.
- `planning/s01-caption-layout-fa-nen-01a.png` — FA RTL, correctly shaped, ZWNJ
  half-spaces visible (دبیره‌ها، نوشته‌های، صیقل‌خورده، می‌خواند), single line, in-band.
- `planning/storyboard-contact-sheet.jpg` — all 34 shots as static blocking
  proposals; amber markers for missing art; three distinct village nights/dawns;
  camp with fires; gate/court/apprentice; engineering-bridge slate; end card.

### Independently reproduced (actual commands, results shown in-session)

> Process note: I ran **read-only local commands** (`sha256sum`, `python3` for
> JSON/hash/arithmetic, `file`, `ls`, `head`) directly, not wrapped in `rtk`.
> All were local file operations and succeeded; `rtk` (a sandbox proxy) was not
> needed for them. No command wrote anything, no provider call, no `build_board.py`
> run (it overwrites planning outputs), no Godot invocation, no `make check` run.
> The fact that the computed SHA-256s **match the board's recorded hashes** is
> strong independent evidence the commands executed against the real files.

- **All 5 `source_hashes` MATCH** actual files: production-plan, EN book, FA book,
  narrative-continuity, environments manifest.
- **All 6 named character cutouts + both Simurgh alternatives MATCH** their
  recorded SHA-256 (shahrasp, chapar, akvan_div, tahmures, black_div, arash,
  simurgh_human, simurgh_bird).
- **All 24 unique `background_source` + `background_sha256` MATCH** actual files
  (note: `bg-overlay-01.svg` and `bg-overlay-02.svg` share one hash — both are a
  blank 1280×720 `#20242d` slate; acceptable as a neutral stage, not a defect).
- **Counts verified**: 34 shots, 11 scenes, 34 captions, 18 OST, 47 matrix rows.
- **Frame arithmetic verified**: contiguous 0→5190, `frames == 173*30`, every
  `start_frame == round(start*30)`, every `end_frame_exclusive == round(end*30)`,
  half-open and positive intervals throughout.
- **Cross-references verified**: no unresolved `caption_refs`/`on_screen_text_refs`;
  no wrong-scene references; every cue/OST span is fully covered by the union of
  its referencing shots (no gaps). The 8 "span multiple shots" cues are legitimate
  cross-shot spans (NEN-01A, NEN-02C, NEN-06A, NEN-06B, NEN-08B, NEN-10B,
  NEN-10C, NEN-11, OST-S01-1, OST-S01-2, OST-S02-1, OST-S11-1).
- **All 34 `verbatim_anchor` strings and all 34 `heading` values are present
  verbatim** in the canonical English book (whitespace-normalized match).
- **Board cue text is byte-identical to the production plan** for all 34 captions
  and all 18 OST (scene, speaker, start, end, en, fa / kind).
- **All 34 `crop_reference_rect` are in-bounds and positive; every non-full crop
  preserves the 1280×720 aspect (1.778).** `caption_region` is uniform
  `[64,600,1152,104]` across all shots.
- **Matrix covers all 34 board shots**; every `required_assets` in the board maps
  to a matrix asset; no orphan assets either direction.
- **S01 runner/renders confirmed ABSENT** (`render_s01.py`, `project.godot`,
  `renders/`), matching the spec's "planned, not implemented" labelling.
- **`board-validation.json` counts match** my recompute (34/11/34/18, 4 specimens).
- **Image dimensions confirmed**: cutout 1086×1448 (matches spec), plate/panel
  1280×720, contact sheet 2560×4068.
- **Persian caption specimen (nen-01a)** is faithful to the canonical FA tale
  (شهراسپ … از پشت بلوری صیقل‌خورده می‌خواند) — not a re-translation that mimics
  English structure.

### Not verified / unavailable (stated explicitly, not papered over)

- **Native alpha bbox `[266,17,801,1424]` and scale `335/1407`** could NOT be
  re-measured (Pillow/PIL not installed in the venv). The spec itself defers this
  to "verify on the actual sprite before locking" and offers two alternative
  anchor derivations — so this is an *appropriately deferred, unconfirmed* number,
  not a defect I can confirm or refute.
- **Full-repository baseline (789 passed / 8 failed, stale Persian source hashes
  Ch 01–04)** was **NOT independently reproduced** — I did not run `make check`
  (out of scope for a review, and the task forbids claiming it without running).
  It is an assertion from two corroborating documents (`board-validation.json`,
  `chapter-01-animation-status.json`), treated as a *status assertion*, not a
  verified fact.
- **Godot rendering / actual reading performance / recorded audio** — not available
  in this session; nothing here is evidence of rendered pacing.

---

## 2. Two distinct verdicts

### Planning-package quality: **PASS_WITH_REWORK**

The board is a high-quality, internally consistent, well-scoped planning artifact.
Every claim I could measure checks out: hashes (source, characters, all 24
backgrounds), counts, frame arithmetic, cross-references, verbatim story anchors,
byte-identical cue text, in-bounds aspect-preserving cameras, complete matrix
coverage, and an honestly disclosed (not hidden) risk list. It is **not**
BLOCKED or INSUFFICIENT_EVIDENCE — the evidence is strong and reproducible. It is
**PASS_WITH_REWORK** because several concrete, fixable items remain open (S06
narration/visual mismatch, S11 OST overlap, S08 sentence-not-in-all-three-contexts,
S03/S07 density, the S01-C contingent continuity + missing matrix contingency
asset, and three missing S01 acceptance tests). These are rework, not fundamental
flaws.

### Ready to start bounded S01 implementation: **READY_WITH_EXPLICIT_CONSTRAINTS**

`s01-proof-specification.md` is an **executable work specification**: complete
minimum asset list (CONTACT-S01, PROP-CRYSTAL, PROP-SILK, PROP-MESSAGES,
LAYOUT-S01, TEXT-S01), a finite action spec (approach → align → one scan →
settle), coordinate/layout conventions, bilingual caption handling (Pillow/RAQM
specimen vs. untested Godot), absolute-time / seek / reset / malformed-input tests,
and render commands correctly labelled **unimplemented** (verified absent).
Scaffolding `project.godot`, the controller, the crystal/silk/hand contact art, and
the `render_s01.py` runner can begin now.

It is **READY_WITH_EXPLICIT_CONSTRAINTS**, not READY, because:

- Missing contact artwork (CONTACT-S01 / PROP-CRYSTAL / PROP-SILK) is **expected
  next-unit work**; it blocks *accepting an S01 performance*, not starting the
  implementation.
- The S01-C wide-reprise continuity question (book/reed vs. crystal/silk) is
  **correctly deferred to pre-acceptance review**, but the implementer needs one
  committed resolution (see F-008) before the wide can be built.
- The S01 acceptance tests should be extended before/with implementation so the
  proof actually catches faked articulation (F-005).
- **No Godot render command may be run until `render_s01.py` exists** (spec says
  this; confirmed absent).
- The 789/8 repo baseline is **not independently verified** by this review.

> **Completed S01 performance, final animation, and owner art approval are NOT
> assessed or granted by this planning review.** No owner signoff, no certification
> flag, and no execution claim is made.

---

## 3. Prioritised actionable findings

Severity: blocker / high / medium / low. "Disclosed" = already in the board's risk
list; "NEW" = identified by this review, not in the board's risk list.

### F-001 — S06 narration leads the visuals (charcoal burners) — **medium** (disclosed: R-S06-CUES)
- **File/keys:** `shot-board.json` captions `NEN-06A` (68.4–72.8); shots
  `CH01-S06-A` (68–71, delivery), `CH01-S06-B` (71–73, dispatch), `CH01-S06-F`
  (79–85, camp reveal).
- **Evidence:** The line "The eleven fires proved to be charcoal burners, camped
  outside the frontier." plays over the **delivery + dispatch** shots, but the
  charcoal-burner reveal is S06-F, ~11 s later. Confirmed numerically.
- **Consequence:** The audience hears the answer before seeing it; the visuals show
  delivery/dispatch while the narration names charcoal burners.
- **Smallest repair (preserves delivery-before-dispatch causality, per the board's
  own note):** re-time `NEN-06A` to start near/after S06-B so it lands across the
  village alarms into the S06-F reveal; or reorder S06 so the camp reveal
  coincides with the line. Do **not** reorder delivery→dispatch to hide it.
- **Closure check:** after re-timing, `NEN-06A` start ≥ S06-B start (or the reveal
  shot precedes the line) and the line's visual anchor is the camp shot.

### F-002 — S08 sentence not shown in all three role contexts — **medium** (disclosed: R-S08-TEXT)
- **File/keys:** OST `OST-S08-0` (116.8–122.4, "Close the western gate"); shots
  `CH01-S08-A` (116–122.6, gate), `CH01-S08-B` (122.6–127, court), `CH01-S08-C`
  (127–131, apprentice).
- **Evidence:** `OST-S08-0` is referenced **only** by S08-A (the gate/watch
  context). S08-B references only `OST-S08-2` (Role B label) and S08-C only
  `OST-S08-3` (Role C label). So the **same sentence** is visible in only one of
  the three contexts.
- **Consequence:** The scene's core pedagogical point (same sentence = current task
  / quoted evidence / mere ink) is only *demonstrated* once; the court and
  apprentice contexts get a role label but not the shared sentence. This is a
  story-completeness gap for Review A.6, not purely cosmetic.
- **Smallest repair:** extend `OST-S08-0` (or add an equivalent sentence OST) into
  S08-B and S08-C so the identical sentence is on screen in all three contexts,
  keeping the board's note that this is a graphics extension, not newly approved
  prose.
- **Closure check:** the "Close the western gate" sentence OST is referenced by all
  of S08-A, S08-B, S08-C with identical `en`/`fa`.

### F-003 — S11 ledger OST overlaps the end-card takeaway — **medium** (disclosed: R-S11-OST-OVERLAP)
- **File/keys:** OST `OST-S11-1` (166.6–172.6, ledger line) and `OST-S11-2`
  (169.8–173, takeaway); shots `CH01-S11-A` (166–169.8, ledger), `CH01-S11-B`
  (169.8–173, end card).
- **Evidence:** Overlap window is 169.8–172.6 = **2.8 s**; the ledger OST bleeds
  2.8 s into the end-card shot. Confirmed numerically.
- **Consequence:** Two OST layers (ledger + takeaway) are on screen simultaneously
  over the end card — accidental text overlap.
- **Smallest repair:** trim `OST-S11-1` to end at 169.8 (the S11-A/S11-B boundary)
  or shorten the ledger line so it clears the takeaway.
- **Closure check:** `OST-S11-1.end ≤ OST-S11-2.start`.

### F-004 — S03-B: 2.5 s for three inspections + two readings — **medium** (disclosed: R-S03-DENSITY)
- **File/keys:** shot `CH01-S03-B` (35.5–38.0 = exactly **2.500 s**, 75 frames),
  `camera.kind = inspection_montage`; action text "Akvan examines marks, Simurgh
  checks weight/cord, Black Div reads twice."
- **Evidence:** 2.500 s for three inspection actions plus two readings. Confirmed
  numerically.
- **Consequence:** A *performed* "reads the sentence twice" in a ~0.8 s sub-beat is
  not legible.
- **Smallest repair (keeps it a montage):** either extend S03-B, or express
  "reads twice" as a brief OST/label beat rather than a performed action, so each
  visible inspection gets enough time. Do not claim recorded pacing has passed.
- **Closure check:** each inspection sub-beat ≥ a legible minimum, or "reads twice"
  is carried by a text/label beat.

### F-005 — S01 acceptance tests cannot catch faked articulation — **medium** (NEW)
- **File/key:** `s01-proof-specification.md` — "One complete reading action"
  (line ~53–54, 78–85) and "Acceptance tests" (135–151).
- **Evidence:** The spec *names* the requirements — "Move the gripped crystal
  together with its holding hand; no sliding through fingers," "Separate its moving
  crystal/hand assembly and stationary silk/background; do not fake articulation by
  translating a whole picture containing both," "Do not animate actual text
  backwards" — but the **acceptance test list has no automated check** for any of
  them. The existing tests (normal / boundary / seek-reset-replay / malformed /
  visual / scope) would all *pass* for a proof that: (a) slides the whole contact
  image to fake a scan, (b) loops/oscillates the scan, or (c) lets the crystal
  detach from the hand mid-scan (seek-vs-continuous wouldn't catch a consistent
  wrong state).
- **Consequence:** The most likely real failures (cheapest faked articulation,
  looped scan, mid-scan detachment) are exactly what the current tests won't
  catch — so a passing proof could still be incoherent.
- **Smallest repair — add three tests:**
  1. Per-frame **hand↔crystal contact continuity** over the 4.2–5.6 s scan (crystal
     grip point stays attached; no separation frame).
  2. **Scan one-pass / monotonicity** (crystal displacement is monotonic over the
     scan interval; no oscillation/loop).
  3. **"Not a whole-image translation"** check (silk/background pixels static while
     crystal pixels move across the scan).
- **Closure check:** the three tests are present in the spec and wired into
  `render_s01.py` evidence JSON.

### F-006 — S07 label/card density; card visual separation not demonstrated — **medium** (disclosed: R-S07-DENSITY)
- **File/keys:** shot `CH01-S07-E` (105.3–116 = 10.7 s); OST `OST-S07-1..4`
  (label_ticks, ~2.2–2.4 s each); `OST-S07-4` long bilingual "Requested result:
  classify the object and identify missing context."
- **Evidence:** Four long bilingual labels + a separate sealed card in 10.7 s; the
  fourth label text is the longest. The **semantic** separation of the request card
  from the examined sentence **is** present in the data (separate OST id, distinct
  `kind`, `boundary_note`, and shot action "A separate request card remains
  visibly distinct"). The **visual** separation is **not** demonstrated (static
  proposal; no render).
- **Consequence:** Readability of four dense bilingual labels + a card in 10.7 s is
  unproven; the card's on-screen distinctness is unproven.
- **Smallest repair:** at render, verify the card is a visually distinct object
  (not a 5th label) and the requested-result line fits the caption-safe region at
  a readable size (measure/rewrap, don't shrink). Re-time/pacing after the
  bilingual read-through.
- **Closure check:** rendered S07-E shows the card as a separate object and all four
  labels + card legible; OST `OST-S07-4` fits the region.

### F-007 — S10 three village reprises at 1.3/1.3/1.4 s — **low** (disclosed: R-S10-DENSITY)
- **File/keys:** shots `CH01-S10-C/D/E` (measured **1.300 / 1.300 / 1.400 s**).
- **Evidence:** Three dawn "lower the lamps" reprises at ~1.3 s each. Confirmed
  numerically.
- **Consequence (low):** These are calm, low-information reprises (no new
  narrative event; the backgrounds already carry the hillside/orchard identity
  landmarks). A rapid 3-panel montage is a defensible staging choice; the real
  risk is only *labelling* three distinct villages in 1.3 s.
- **Smallest repair (optional):** if the identity labels prove unreadable, use a
  clearly labelled three-panel montage or extend one beat. Do not force 173 s.
- **Closure check:** village identity is legible at the chosen duration, or a
  labelled montage is used.

### F-008 — No "wide contact pose" contingency asset in the matrix (S01-C) — **low** (NEW)
- **File/keys:** `s01-proof-specification.md` "Stock-hold conflict" (lines ~68–74);
  matrix P0-S01 rows; shot `CH01-S01-C` (wide, `mode = unchanged_source_pose_reference_only`).
- **Evidence:** The source pose holds book + reed (confirmed in `Shahrasp.png`).
  S01-C is specified with the unchanged book/reed pose, while its `prop_custody`
  and the action table require "Crystal/silk remain where the performance leaves
  them; no unexplained disappearance/hand reassignment." The data supports a
  *set-down* reading (PROP-CRYSTAL/PROP-SILK are `required_assets` for S01-C, so
  they can rest on the reading surface while Shahrasp holds book/reed). The spec
  correctly defers this to pre-acceptance review and names the fallback
  ("a new bounded wide contact pose is required"), **but the matrix has no
  "wide contact pose" row**, so if the review concludes the fallback is needed,
  there is no budgeted asset for it.
- **Consequence:** A *flagged, contingent* (not hard) continuity beat — the crystal
  set-down between the close insert and the wide — with a named-but-unbudgeted
  resolution. The implementer can start, but needs one committed interpretation.
- **Smallest repair:** either (a) add a "WIDE-CONTACT-S01" contingency row to the
  matrix, or (b) explicitly commit the set-down interpretation (crystal/silk on the
  table, Shahrasp book/reed) in the spec so there is a single resolution to build
  to. Confirm in the actual render during pre-acceptance review.
- **Closure check:** the spec/matrix states one committed S01-C interpretation and
  the render shows no unexplained prop disappearance or hand reassignment.

### F-009 — S01-B contact crop is backdrop-only; contact insert is 100% new art — **low** (disclosed: R-FLAT-SET)
- **File/keys:** shot `CH01-S01-B` `camera.crop_reference_rect = [390,195,640,360]`;
  `panels/ch01-s01-b.png`; spec lines ~40–45.
- **Evidence:** The crop is a flat plaster wall + bookshelf edge — **no tabletop /
  reading surface is in-frame**. The spec is explicit that this is "a temporary
  camera backdrop only" and "A wide tabletop's projected surface is not a hand
  rig." The panel shows only the amber "CONTACT ART NOT YET BUILT" marker.
- **Consequence:** None unexpected — the entire contact insert (hands, crystal,
  silk, surface) is new art. This is expected next-unit work, **not** a defect, and
  the board does **not** depict the source pose as evidence the performance exists.
- **Smallest repair:** none (disclosed, expected). Ensure the new contact art
  includes a coherent surface the silk rests on, since the crop provides none.
- **Closure check:** the produced contact insert shows a supported silk + held
  crystal with a connected surface; not a translated whole image (see F-005 test 3).

---

## 4. Known-risk disposition

Board's `risks[]` (9) → confirmed / refined / dismissed, with evidence.
"Already disclosed" items are not double-counted as new contradictions.

| Risk (board severity) | Disposition | Evidence |
|---|---|---|
| **R-S06-CUES** (high) | **CONFIRMED** (F-001) | NEN-06A 68.4–72.8 over delivery (S06-A) + dispatch (S06-B); reveal is S06-F 79–85. Causal order delivery-before-dispatch **preserved**; narration leads visuals. Not hidden — board correctly says "Do not change delivery-before-dispatch to conceal mismatch." |
| **R-S03-DENSITY** (high) | **CONFIRMED** (F-004) | S03-B = exactly 2.500 s for 3 inspections + 2 readings. |
| **R-S07-DENSITY** (high) | **CONFIRMED, refined** (F-006) | S07-E 10.7 s; four bilingual label_ticks + card. Semantic card separation present in data; visual separation unproven. |
| **R-S08-TEXT** (medium) | **CONFIRMED** (F-002) | Sentence OST only in S08-A; not in court/apprentice. Genuine story-completeness gap, not cosmetic. |
| **R-S10-DENSITY** (medium) | **CONFIRMED, low harm** (F-007) | 1.300/1.300/1.400 s; low-information calm reprises; montage defensible. |
| **R-CUSTODY-S07** (medium) | **CONFIRMED, handled** | S07 explicitly states the packet is at the frontier and the labels/card are "the earlier object under discussion, not a newly teleported packet." No silent teleport. |
| **R-FLAT-SET** (medium) | **CONFIRMED** (F-009) | Crop is backdrop-only; contact inserts are new art. Board does not claim reach/occlusion is solved. |
| **R-VOICE** (high) | **CONFIRMED** | No recordings; all 173 s + bilingual cue times provisional. I cannot verify speech fit without audio; the clean arithmetic is **not** proof of recorded pacing. |
| **R-S11-OST-OVERLAP** (medium) | **CONFIRMED** (F-003) | 2.8 s overlap; ledger bleeds into the end card. |

No board-listed risk was dismissed as unfounded. The only **new** (non-disclosed)
items this review adds are **F-005** (missing S01 acceptance tests) and **F-008**
(missing matrix contingency asset).

---

## 5. Coverage summary

| Area | Status |
|---|---|
| **All 11 scenes present, shots → scenes complete** | ✅ Verified (11 scenes; every shot has a scene; no orphan scene/shot). |
| **Custody chain (tablet/wrapping/packet)** | ✅ Well-tracked. Chapar→intake (S02) → Tahmures→cedar stand (S03) → Simurgh wraps (S04-B, "not also left on stand") → Black Div empty-handed (S04-C) → Simurgh→Arash (S06-A, "never a seal-based authentication claim") → packet stays with Arash (S06-B) → S07 labels/card ≠ river tablet → S10 NEW correction message (distinct object). No duplicated tablet travels. |
| **Cue/OST mapping** | ✅ 34 captions + 18 OST; all refs resolve; no wrong-scene refs; all spans covered; byte-identical to the plan. |
| **Camera / reference checks** | ✅ 24 unique backgrounds exist + hash-match; all 34 crops in-bounds, positive, aspect 1.778; all cameras `proposed_not_contact_validated`; all shots `static_blocking_proposal_not_performance`. |
| **Story/roles/causality (Review A)** | ✅ Strong. 34/34 verbatim anchors + headings in the canonical book. Chapar ≠ Simurgh; Garshasp offstage; Div-e Sefid **not** inserted; three recipients interpret one tablet; no malicious-div / seal-as-auth; S06 delivery precedes dispatch; three villages distinct; eleven fires = charcoal burners (not invaders); S07 = one sharpen + stop + four labels + separate card, requested result = classify + missing-info (not count fires); S09 = 8 equal-weight components, enforcement outside the metaphor, no seal hierarchy; S10/S11 staging-labelled, ledger = recap not new night. **Gaps:** F-002 (S08 sentence only once), F-008 (S01-C contingent continuity). |
| **S01 minimum assets (Review D.1)** | ✅ Complete and P0-prioritised: CONTACT-S01, LAYOUT-S01, PROP-CRYSTAL, PROP-MESSAGES, PROP-SILK, TEXT-S01. Matrix covers all board `required_assets`. **Gap:** no wide-contact-pose contingency (F-008). |
| **Bilingual specimens (Review C)** | ✅ EN LTR + FA RTL (shaped, ZWNJ preserved) specimens exist for NEN-01A/B; correctly scoped as "Pillow/RAQM static layout only; Godot test pending" (i.e., **not** a Godot render test). FA faithful to canonical FA tale. |
| **Future proof tests (Review D.6)** | ⚠️ Strong set (normal/boundary/seek-reset-replay/malformed/visual/scope) **but** missing faked-articulation / scan-loop / detachment checks (F-005). |
| **789 passed / 8 failed repo baseline (Review E)** | ⚠️ **Not verified** (I did not run `make check`). Treated as a status assertion from `board-validation.json` + `chapter-01-animation-status.json`. |
| **Native alpha bbox `[266,17,801,1424]` / scale 335/1407** | ⚠️ **Not verified** (no Pillow). Spec defers to on-sprite verification. |
| **Godot render / actual performance / audio** | ⚠️ **Not available**; runner/renders confirmed absent (spec correctly labels them planned). |
| **Evidence scoping (Review E)** | ✅ Static board vs. animation, source-pose vs. rigging, beard-alpha repair (preserve RGBA, no face repaint) vs. new art, machine checks vs. owner signoff, media checks vs. full repo release — all kept in scope. Raw `tahmures_complete_studio_bundle.json` is present on disk, marked `preserved_unchanged`, and **not** used as acceptance evidence (correct). |

---

## 6. Next repair order for Codex

### A. Before S01 implementation (planning rework — do not skip)
1. **F-005:** Add the three S01 acceptance tests — per-frame hand↔crystal contact
   continuity over the scan; scan one-pass/monotonicity; "silk static while crystal
   moves" (no whole-image translation). Wire them into the `render_s01.py` evidence
   contract.
2. **F-008:** Commit one S01-C interpretation — either add a `WIDE-CONTACT-S01`
   contingency row to the matrix or explicitly adopt the set-down reading
   (crystal/silk on the reading surface, Shahrasp book/reed).
3. **F-001:** Decide and record the S06 `NEN-06A` re-timing (land the line on the
   camp reveal; preserve delivery-before-dispatch).
4. **F-003:** Trim `OST-S11-1` to end at 169.8 (or shorten the ledger line).

### B. Implementable within S01
5. Produce CONTACT-S01 / PROP-CRYSTAL / PROP-SILK contact art (expected next-unit
   work; includes a coherent surface the silk rests on — the crop provides none).
6. Build the proof scene + `render_s01.py`; run the F-005 tests; verify the S01-C
   wide-reprise continuity in the **actual render** during pre-acceptance review.
7. Record the S08 sentence-OST extension decision (extend into court + apprentice)
   now so the OST contract is fixed, even though S08 renders after S01 (F-002).

### C. Later-chapter / later-stage — do **not** block S01
8. **F-006:** Render S07-E; verify card-as-distinct-object + legible bilingual
   labels/card; re-time after read-through.
9. **F-007:** If 1.3 s reprises prove unreadable, use a labelled 3-panel montage or
   extend one beat.
10. **F-004:** After the bilingual read-through, extend S03-B or move "reads twice"
    to a text/label beat.

### D. Owner decisions (kept distinct from routine engineering — not granted by this review)
- **Simurgh form** (human / bird): unresolved; blocks Simurgh contact art + the
  final affected shots (S03, S04-B, S06-A, S10-A). **Does not block S01.**
- **Voice approach** (owner recordings / separately authorised synthetic):
  unresolved; blocks final audio/timing lock. **Does not block the silent S01
  proof.**
- **Art / performance selection**: pending concrete owner review. This review grants
  no approval.

---

### Reviewer boundary statement
- No source/planning file was edited; no assets regenerated; no status/approval
  record, Persian hash, or review metadata changed; no provider call; no dependency
  install; no commit/push/publish.
- `build_board.py` was **not** run (it overwrites planning outputs).
- The Godot render commands in the spec were **not** run (they are labelled planned
  and the runner does not exist).
- No percentage scores, certification flags, or human approvals are asserted.
- Where a check could not be run (full `make check`, alpha-bbox measurement, Godot
  render), it is marked **not verified** rather than claimed.
