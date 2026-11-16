# Qwen review — Part S01-A: minimal reconstructed art

**Reviewer role:** independent read-only art & continuity review of the S01
candidate assets. This is **not** owner approval. No assets, manuscript,
approval evidence, raw bundle, or prior report were modified. The prior
`qwen-chapter-01-board-review.md` was left untouched.

---

## Verdict: `READY_FOR_PROOF_REVIEW`

The S01-A reconstructed-art package is **internally consistent, numerically
verified, and honestly scoped**. Every hash I could measure matches the
manifest; the motion/grip claims are reproduced independently from the recorded
traces; the three negative fixtures genuinely break; and the art is correctly
labelled as a **new editable-vector reconstruction with a source-sampled face**,
`owner_review_pending`. No new contradiction, hidden prop, modern lens,
magical beam, pseudo-Persian text, or book/reed ghost was found.

`READY_FOR_PROOF_REVIEW` means the package may be put in front of the owner for
visual acceptance of the reconstruction. It does **not** grant art acceptance,
approve the character, or clear the unit for full-chapter integration.

**Not assessed or granted here:** completed S01 performance acceptance, final
animation, owner art approval, Simurgh form, voice approach, and any repository
release gate.

---

## 1. Review basis and access limits

### Content inspected directly (pixels actually read)

| File | What it establishes |
| --- | --- |
| `Characters/Shahrasp.png` | Source identity: dark curly hair, olive headband, full dark beard, **forward-facing wide-open eyes**, green robe, cream inner tunic, brown sash, holds brown book + reed. |
| `Characters/godot-character-library-recovery-01/characters/shahrasp/cutout/shahrasp_cutout.png` | Pixel-identical to `Shahrasp.png` (the contour-sampled source). |
| `Characters/environments/chapter-01-candidate-01/preview/bg-hall-01.png` | Hall plate: stone floor, central chest, left bench/cabinet, right shelves + bench/table, single ordinary door (no decorative door/handle motif). |
| `renders/s01/en/evidence-0030.png` (A, 1.0 s) | Full hall, standing Shahrasp, small reading table with silk, title + caption. |
| `renders/s01/en/evidence-0126.png` (B align, 4.2 s) | Close reading insert: large table, silk with indistinct marks, left resting sleeve, right forearm holding crystal. |
| `renders/s01/en/evidence-0144.png` (B scan, 4.8 s) | Crystal moved left mid-scan. |
| `renders/s01/en/evidence-0168.png` (B settle, 5.6 s) | Crystal settled left of start. |
| `renders/s01/en/evidence-0240.png` (C, 8.0 s) | Intake stand (4 materials) + reading table persist. |
| `renders/s01/en/contact-sheet.jpg` | A/B/B/B/C structure; scan visibly advances left across the three B cells. |
| `renders/s01/en/material-support-check.png` | Intake materials on individual tray rests. |
| `renders/s01/fa/evidence-0030.png` (A) | Same plate, RTL title/caption, ZWNJ in `دبیره‌ها`. |
| `renders/s01/fa/evidence-0168.png` (B) | Geometrically identical to EN B; only text differs. |
| `renders/s01/fa/evidence-0240.png` (C) | Same intake scene; RTL caption. |

### Docs / code read

`AGENTS.md`; `s01-proof-specification.md`; `planning/review-reconciliation.md`;
`README.md`; `s01-review-report.md`; `s01-manifest.json`; `s01.gd`;
`build_s01_assets.py`; `assets/s01/{robe,support,silk,steady_hand,grip_back,
crystal,grip_front,messages}.svg`; `assets/s01/FONT-LICENSE.txt`.

### Commands actually run (all `rtk proxy`-prefixed, all exit 0)

- `rtk proxy ls -la .../renders/s01/{en,fa}/` — confirmed all 5 EN and 5 FA
  evidence stills, contact sheets, `frames/`, `checks/`, 3 `negative-*/`,
  `verification.json`, `godot-trace.json`, `s01-silent.mp4`, `ffprobe.json`,
  `runtime-state-tests.json` exist.
- `rtk proxy sha256sum` on the 6 book/env/character inputs and separately the
  2 remaining manifest inputs — **all 7 manifest input hashes match**.
- `rtk proxy sha256sum` on the 10 `assets/s01/*` files — **all 10 match** the
  manifest `assets[].sha256`.
- `rtk proxy /usr/bin/python3` (trace re-derivation) — see §4 numeric
  re-derivation.
- `rtk proxy /usr/bin/python3` (negative-fixture trace analysis).
- `rtk proxy /usr/bin/python3` (verification.json assertions dump).
- `rtk proxy ls -la editorial/media-handoff/ | grep ...` — confirmed target
  file does not yet exist and prior board review is present.

### Not inspected (marked, not silently passed)

- Individual `frames/0000..0359.png`, `checks/boundary|seek|replay|reset*.png`,
  and the **pixel images** of the three `negative-*/` fixtures — only their
  `godot-trace.json` was read (sufficient to confirm the fixtures break, but not
  a pixel-level look at the broken frames).
- `renders/s01/fa/contact-sheet.jpg` and `renders/s01/fa/material-support-check.png`
  (their EN counterparts were inspected; FA frames were inspected and are
  geometrically identical to EN, only text differs).
- `ffprobe.json`, `runtime-state-tests.json` contents were not opened (the
  corresponding `verification.json`/trace claims are treated as recorded
  assertions, not independently reproduced).
- Full decoded MP4 playback — not performed.

---

## 2. Prioritised actionable findings

No finding is a hard engineering defect that the implementer failed to disclose.
The substantive art weaknesses are **already disclosed** in
`s01-review-report.md` (limitations 1–5) and in
`s01-manifest.json.provenance_limits`. They are listed here as the concrete
items the owner must resolve, with two low-severity observations added.

### S01A-01 — `medium` (disclosed) — Source eye state does not read as "reading"
- **File/anchor:** `s01-manifest.json` `source_head_contour`; visible in
  `renders/s01/en/evidence-0030.png` (head at ~x=780, y=235 in A) and the FA
  equivalent. Source eyes in `Shahrasp.png` are wide-open and **forward-facing**.
- **Evidence:** The runtime reuses the static source face; there is no downward
  gaze, blink, or head performance. The "reading" cue comes only from the
  crystal + hands at the silk, not from the face.
- **Consequence:** Whether the face communicates reading is an open owner
  question; as drawn, a viewer reads the eyes as alert/forward, not reading.
- **Smallest repair:** Owner decision only — accept the forward state, or
  commission a downward-gaze head state to sample in place of the contour.
- **Closure check:** At a full-res A still, the face/eye direction unambiguously
  reads as reading (or is consciously accepted as-is).

### S01A-02 — `medium` (disclosed) — Face/neck seam is a straight contour edge, not a neck
- **File/anchor:** `s01.gd` lines 63–71 (`head` `Polygon2D`, `position
  (653.5,213.1)`, `scale 0.23`); meets the vector robe collar in A.
- **Evidence:** The head is a static 8-point **non-rectangular** contour of the
  source, placed over the new vector robe. The lower edge is a straight polygon
  line meeting the green collar — an acceptable stand-in at A's small scale,
  but not a recovered anatomical neck.
- **Consequence:** At close zoom the join is visibly a cut; must be judged by
  the owner, not assumed fine because pixels are preserved.
- **Smallest repair:** Owner review of the seam at full-res A; if rejected,
  redraw the neck join / trim the contour's lower edge.
- **Closure check:** Full-res A still shows a clean head-to-robe junction.

### S01A-03 — `low` (disclosed) — Vector style is flatter than the raster source
- **File/anchor:** all `assets/s01/*.svg`; visible in A vs `Shahrasp.png`.
- **Evidence:** Robe/sleeves/fingers are flat single-tone vector with 2.5 px
  strokes; the source is shaded raster. Style mismatch is inherent and disclosed
  (review report limitation 1).
- **Consequence:** Visual consistency with the existing character pack is a
  matter of owner preference, not correctness.
- **Smallest repair:** Optional; accept or restyle. **Closure:** owner sign-off.

### S01A-04 — `low` (disclosed) — Close view is a new staging on the flat plate; wide/close perspective differs
- **File/anchor:** `s01.gd` `apply_time` (`close` branch, `reading.position
  ZERO / scale 1.0` vs `position (680,400) / scale 0.16`).
- **Evidence:** B is a top-down-ish large-table composition drawn over the flat
  hall plate; it is not camera geometry recovered from a 3D set (review report
  limitation 4). The wide (A/C) table is a small floor-level piece in front of a
  standing figure; the close (B) table fills the frame.
- **Consequence:** The A→B cut is a staging change, not a continuous dolly;
  acceptable as a cut but should be accepted as such.
- **Smallest repair:** None required for a candidate; owner accepts the cut.
- **Closure check:** A→B→C reads as an intentional insert cut.

### S01A-05 — `low` (new observation) — Wide view implies two arm sets
- **File/anchor:** `assets/s01/robe.svg` (static side sleeves) **and** the
  `reading` assembly (`steady_hand.svg` + dynamic `forearm`), both present in A
  at `scale 0.16`.
- **Evidence:** In A the full-body robe already has its own static side sleeves,
  while the separate (tiny) reading assembly adds hands at the table. At full
  body scale these can read as hands in two places rather than one pair reaching
  to the table. This is a readability nit, not a correctness failure.
- **Consequence:** Minor ambiguity in the wide shot.
- **Smallest repair:** Confirm at A scale the hands read as reaching the table;
  if ambiguous, angle/fade the robe's static side sleeves toward the table, or
  drop the wide robe's forearms so the reading-assembly arms carry the read.
- **Closure check:** A still shows a single coherent pair of arms to the table.

### S01A-06 — `informational` (verified-consistent, **no repair**) — A vs C crystal offset
- **File/anchor:** `s01.gd` `approach`/`scan`; traces `f30` vs `f192/f240`.
- **Evidence:** A's wide crystal global ≈ (793.9, 458.2) and C's ≈ (790.1,
  463.0) differ ~6 px. Re-derived cause: A sits at the **pre-scan approach** pose
  (`approach = −30`, `scan = 0`), C at the **post-settle** pose (`approach = 0`,
  `scan = −24`). This is the same approach→scan→settle action viewed wide, not a
  discontinuity.
- **Consequence:** None. Recorded to preempt a false "prop jump" finding.
- **Smallest repair:** None.

---

## 3. Numeric claims — independently reproduced (not just echoed)

Re-derived from `renders/s01/{en,fa}/godot-trace.json` (identical geometry in
both languages, only text differs):

| Claim | Re-derived result | Match |
| --- | --- | --- |
| Grip hand == crystal (0 px) | hand and crystal arrays are **equal at every sampled frame** (e.g. f168 both `(688.0, 394.0)`) | ✅ by construction |
| Scan 24 px, right→left, monotonic | crystal x `712.0 → 702.6 → 688.0` over 4.2–5.6 s; net dx = **−24.0** | ✅ |
| Silk/support static in B | silk `(590,420)`, support `(600,500)` constant across all B frames | ✅ |
| Single scan event | `scan_events` 0 before 4.2 s, 1 from 4.2 s onward, never re-fires | ✅ |

`verification.json` records (treated as **recorded assertions**, consistent with
the traces above): `grip_continuity.max_anchor_error_px = 0.0`,
`one_pass_scan.travel_px = 24.0`, `max_reverse_step_px ≈ −0.04`,
`settle_error_px = 0.0`; 14/14 input negatives rejected; 3/3 motion negatives
rejected; `owner_approved = false`, `silent = true`, movie 0 audio streams;
`seek_reset_replay` all true; caption `missing_glyphs` empty.

**Negative fixtures independently confirmed from their `godot-trace.json`:**
- `detach` — crystal ≠ hand (sampled error **12 px**); grip breaks. ✅
- `oscillate` — crystal x ranges 688.1↔712.0 and **returns to start** (zero net
  travel, non-monotonic). ✅
- `whole` — `backdrop` moves (x → −12) and crystal travels **48 px** (whole-picture
  translation, not a scan). ✅

Each is a genuine broken capture, not a nominal check.

---

## 4. Question-by-question disposition (art)

- **Visibly Shahrasp?** Yes, at identity level: same hair/headband/beard (source
  face sample) and same robe/cream/sash palette (vector). The source **eye state
  is forward-facing**, not a reading gaze (→ S01A-01). Source-pixel preservation
  of the face is preserved, but that is not the same as accepting the new pose.
- **Both arms connected in wide / tabletop supported?** In B the right forearm
  polygon runs shoulder `(1010,308)/(1050,365)` → wrist `moving+(158,67)`
  (settle ≈ `(756,407)`) — a continuous sleeve, no gap. The left `steady_hand`
  rests on the silk. The `support` table spans x 90–1120, y 300–559 with legs to
  y 590; it is a supported piece, not floating (matches the repaired "floating
  short table" note in the review report). Wide↔close arm-assignment ambiguity
  is → S01A-05.
- **Feet on painted floor, away from furniture?** Legs at x≈707 & 841, y 486–552
  land on the stone floor in front of the central chest; the reading table is in
  **front** of the lower body (correct depth), and no shelf/bench is touched.
  ✅
- **Close insert plausibly shows these sleeves/hands without claiming unseen
  source surfaces?** Yes — the close hands/sleeves are new vector art matching
  the wide palette and cream cuffs; nothing is presented as recovered from the
  source body. The face is simply absent in B (intentional insert), which is the
  S01A-04 staging note.
- **Grip actually holds the crystal (front/back overlap, alpha)?** In the B
  stills, `grip_back` sits behind the crystal and `grip_front` shows three finger
  bumps overlapping the lens with a thumb on top; the crystal is semi-transparent
  (`fill-opacity 0.68`) with a small specular arc. The hold reads as a hand on a
  lens. Simple/stylized (owner art judgment), but there is genuine front/back
  overlap and no floating. **No** modern handled lens, **no** magical beam,
  **no** floating crystal, **no** pseudo-Persian (silk marks are indistinct
  dashes, intentionally unreadable per `provenance_limits`).
- **Fine writing visible through/under the crystal?** Indistinct fine dashes are
  drawn on the silk beneath the lens; no magnification or authenticated-script
  claim is made (matches manifest `scan.direction` and review-report limit 5). ✅
- **A (<3 s) / B (3–6.4 s) / C (>6.4 s) crystal, silk, hand assignment consistent?**
  Same layered `reading` assembly is reused at all three states; hand/prop
  assignment is preserved across both cuts; A↔C offset explained as
  approach→settle (S01A-06). ✅
- **Clay, leather/tube, bark, silk distinguishable and supported at intake?** In
  C: clay (brown, dash marks), leather (dark envelope w/ folded flap + ellipse
  tube end), bark (tan sheet, dark lines), silk (cream, dash marks) — four
  distinct forms, each on an individual tray rest on the intake stand. ✅
- **Any drawing implying a new plot object/action?** No. The intake materials are
  the canonical incoming messages (not the later river tablet); no courier,
  extra, book, or reed appears. ✅
- **Book/reed ghost?** The source pose holds a book + reed, but the runtime uses
  the new vector reading assembly; **no book or reed is present** in A, B, or C.
  ✅
- **Provenance, source hashes, font notice?** `s01-manifest.json.art_method` and
  `provenance_limits` correctly disclose new-vector reconstruction + source
  face sampled by a static contour; the face is **not** anatomical extraction and
  **not** an approved pose. `FONT-LICENSE.txt` is the proper Bitstream Vera /
  DejaVu notice. No new-character approval is implied anywhere
  (`owner_approved=false`). ✅
- **Bilingual quality?** EN LTR correct. FA is an **actual Godot viewport render
  (RAQM)**, not a Pillow/RAQM specimen — stronger evidence. Shaping, RTL word
  order, and the ZWNJ in `دبیره‌ها` render correctly; titles `سه خوانش` /
  `تالار دبیره‌ها` match the manifest. The FA B/C geometry is pixel-identical to
  EN (only text differs). ✅

---

## 5. Coverage summary

| Area | Status |
| --- | --- |
| S01 minimum assets (crystal, grip back/front, silk, steady hand, support, robe, messages, font) present & hash-verified | ✅ verified |
| Source input hashes (7) match manifest | ✅ verified |
| Grip continuity (0 px) | ✅ reproduced |
| 24 px monotonic single-pass scan | ✅ reproduced |
| Silk/support/backdrop static in normal run | ✅ reproduced |
| Negative fixtures detach / oscillate / whole break | ✅ reproduced (traces) |
| A/B/C crystal-silk-hand assignment consistency | ✅ inspected |
| No book/reed ghost | ✅ inspected |
| No modern lens / beam / floating crystal / pseudo-Persian | ✅ inspected |
| Intake materials distinguishable + supported | ✅ inspected |
| Feet on floor, table in front (depth) | ✅ inspected |
| B arm connection (no disconnected wrist) | ✅ inspected |
| EN/FA shaping, direction, ZWNJ (Godot render) | ✅ inspected |
| Caption layout fits safe region, no missing glyphs | ✅ recorded assertion (consistent with stills) |
| Full decoded MP4 playback | **not verified** |
| `ffprobe.json` / `runtime-state-tests.json` contents | **not verified** (not opened) |
| FA contact sheet & FA material-support check pixels | **not verified** (EN inspected; FA frames inspected & identical) |
| Pixel images of the 3 negative fixtures | **not verified** (traces inspected) |

---

## 6. Remaining owner choices (not engineering work)

1. **Vector robe/arms/sleeves style** — accept the simpler flat vector, or
   restyle toward the raster source (S01A-03).
2. **Face/neck seam** of the source-face contour (S01A-02).
3. **Reading gaze** — accept the forward-facing source eyes as the reading state,
   or commission a downward-gaze head state (S01A-01).
4. **Wide/close perspective + B insert staging** — accept as an intentional cut
   (S01A-04) and the wide arm-assignment nit (S01A-05).
5. **Hand-grip believability** (stylized vector grip).
6. **Out of this silent unit (unresolved, not needed for S01):** Simurgh form,
   voice approach, soundtrack, and final recorded runtime remain owner decisions
   and must not be assumed resolved.
