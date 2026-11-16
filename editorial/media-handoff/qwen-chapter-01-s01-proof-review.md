# Qwen review — Part S01-B: Godot performance and verification

**Role:** independent read-only review of the isolated silent S01 proof
(pipeline, motion, state, bilingual text, provenance, scope). This is **not**
owner acceptance and does not approve art, Simurgh, voice, or chapter
completion. No asset, manuscript, approval evidence, raw bundle, or prior
report was modified. Scratch recaptures were written to a fresh directory and
**deleted** after verification; `renders/s01/{en,fa}` evidence is untouched.

---

## Verdict: `TECHNICALLY_VERIFIED_WITH_ART_REVIEW_PENDING`

The isolated silent S01 pipeline is **independently reproduced from scratch**:
I re-captured both EN and FA to new output directories and the resulting 360
frames are **byte-identical** to the committed evidence, with every metric,
negative fixture, seek/reset/replay comparison, and silent-movie budget
matching. All hash-integrity and two-revision-distinction claims hold. The
controller is correctly scoped as an absolute-time silent candidate. No
pipeline defect, hidden fallback, story/contact blocker, or invented
scope/approval was found.

**Not granted by this review:** owner art acceptance, Simurgh form, voice/
timing, full-chapter integration, or any release gate. The book-gate failures
(789 pass / 8 fail on stale Persian `source_sha256`, Ch 01–04) are **book**
gates, not media failures, and are correctly kept separate.

---

## 1. Review basis — what was reproduced vs. what was read

### Independently reproduced (strongest evidence)

- **Full recapture, both languages.** Ran `render_s01.py --language {en,fa}
  --fps 30 --output renders/qwen-s01/{en,fa}` to fresh dirs. Both printed
  `PASS: 360 Godot frames, seek/reset/replay, caption bounds, 3 motion fixtures
  and silent movie`. Recaptured frames were **byte-identical** to the committed
  `renders/s01/{en,fa}` (0/360 differ, both langs); all `grip_continuity`,
  `one_pass_scan`, `independent_motion`, `seek_reset_replay` and movie budgets
  matched. The whole pipeline (validate → viewport capture → motion → 3
  negatives → ffmpeg → ffprobe → report) is deterministic. Scratch then deleted.
- **`ffprobe` on both committed movies** (independent): each is exactly **1
  video stream, H.264, 1280×720, 30/1 fps, 360 frames, 12.000000 s, 0 audio
  streams**.
- **`--validate-only`** (system interpreter): both langs `PASS: resources, cues
  and 14 adversarial input cases`.
- **Motion recomputed from actual pixels** (my own code, not the report):
  grip 0.0 px; travel 24.0 px; reverse-step −0.0402 px; settle 0.0 px;
  silk/support/backdrop anchors 0.0 px; static ROIs 0 channel delta.
- **Negative fixtures recomputed from pixels:** `detach` grip = 12 px (>1.5
  → rejected); `oscillate` travel = 0.0 px, reverse-step 3.567 px (→ rejected);
  `whole` anchors 24 px, silk/support ROI deltas **137/168** (→ rejected). Each
  breaks the intended measurement, exactly as recorded.
- **Seek/reset/replay pixel equality** at t = 2.0/4.8/6.4/11.9 and reset:
  `seek-*.png == replay-*.png == frames/*.png`, all true, both langs.
- **All 360 committed frame hashes** match `verification.json` (both langs).
- **Two-revision hash distinction verified:** top-level `runner_sha256`
  (`812f0b…`) == archived `evidence/render_s01-capture-revision.py`;
  `image_roi_recheck.runner_sha256` (`3bba1c…`) == current `render_s01.py`.
  The capture revision and the later verification code are correctly separate,
  and both are hash-identified.
- **Manifest + controller + movie hashes** all match the recorded values.
- **11.9 s "final caption clears" claim verified** from pixels: source
  `frames/0357.png` has no caption bar (dark-band ≈ 1 %), the accurate MP4
  decode at 11.9 s has no bar, and the committed sheet's 11.9 s cell has no
  white text (bright = 0 %). (My first low-res impression of that cell was a
  downscale artifact; measurement resolves it.)
- **Half-open boundaries** from the trace: caption A active 0.6–6.2, caption B
  6.4–11.6, title `The Three Readings`/`سه خوانش` 0.6–4.8, `Hall of
  Scripts`/`تالار دبیره‌ها` 5.0–11.8. At t = 6.2 caption A is empty, at 4.8 the
  first title is empty, at 11.6 caption B is empty, at 11.8 the second title is
  empty, and at **t = 12.0** (shot C) both caption and title are empty. Last
  frame 359 (t = 11.967) caption empty. Boundaries are half-open everywhere.

### Code / docs read

`AGENTS.md`; `render_s01.py` (all 504 lines); `s01.gd`; `s01.tscn`;
`project.godot`; `s01-manifest.json`; `README.md`; `s01-review-report.md`;
`planning/s01-proof-specification.md`; `planning/review-reconciliation.md`;
`editorial/media-handoff/chapter-01-animation-status.json`;
`evidence/s01-delivery-checks.json`; both `renders/s01/{en,fa}/verification.
json`, `godot-trace.json`, `ffprobe.json`, `runtime-state-tests.json`; both
encoded-movie sample sheets.

### Inspected visually (pixels)

- `evidence/encoded-movie-samples-en.jpg` and `-fa.jpg` — **actual decoded
  MP4 output** (8 samples each): A/B/C structure, the 24 px right→left scan
  progressing across the 3.5/4.2/4.8/5.6 s cells, the 6.4 s material reveal,
  correct EN LTR and FA RTL shaping (ZWNJ in `دبیره‌ها`), and a **cleared**
  caption at 11.9 s in both editions.
- (Carried from Part S01-A) the A/B/C stills, contact sheets, and source
  references for identity/contact judgment.

### Not reproduced / unavailable

- Continuous decoded MP4 **playback** (only discrete accurate decodes + the
  committed sample sheets were used).
- Individual `decoded-{en,fa}-N.png` per-sample PNGs referenced in
  `s01-delivery-checks.json.decode_commands` — **not committed** (only the two
  `.jpg` sheets are present). The sheets plus my own decodes cover the claim.
- Headless/dummy Godot — not used; all viewport captures ran on a real display
  (`DISPLAY=:0`).

---

## 2. Prioritised findings

### Pipeline defects

**S01B-01 — `low` (informational, disclosed) — the prompt's literal review
command does not run under the canonical interpreter.**
- **Evidence:** `rtk proxy python3 …/render_s01.py … --validate-only` fails
  with `ModuleNotFoundError: No module named 'PIL'` because `rtk proxy python3`
  resolves to the book `.venv`, which has no Pillow (a known, documented repo
  condition — the README says "with system Python/Pillow and Godot available").
  It runs fine via `rtk proxy /usr/bin/python3`.
- **Consequence:** the "low-cost commands" in the review prompt are not
  runnable as written; a reviewer must switch to the system interpreter.
- **Smallest repair:** document (or auto-select) the system interpreter for
  this runner, or add Pillow to the venv when a dependency change is approved.
- **Closure check:** `--validate-only` exits 0 under the interpreter named in
  the prompt.

**S01B-02 — `low` (informational) — `--validate-only` does not re-check
committed evidence; `--recheck-existing` does not re-probe the MP4.**
- **Evidence:** `--validate-only` runs only `validate()` + `input_negative_
  checks()` (manifest/inputs/cues/adversarial inputs). It never opens
  `verification.json` or any frame. `--recheck-existing` re-verifies the
  manifest/controller/language + all 360 frame hashes + normal motion + the
  three negative fixtures, but it does **not** re-`ffprobe` the MP4 (the movie
  is a by-product of the hash-verified frames).
- **Consequence:** a single command does not both validate inputs *and* prove
  the committed report/movie are intact; the movie is only re-verified in the
  full capture path (which I reproduced). No integrity issue was found — the
  committed movies are correct — but the invariant is split across two modes.
- **Smallest repair:** optionally fold the ffprobe budget check into
  `--recheck-existing`, or add a dedicated `--verify-report` mode.
- **Closure check:** one command confirms manifest integrity + all frame
  hashes + movie stream budget together.

### Story / contact blockers

**None.** The unit correctly renders the canonical Setting (Shahrasp reads
fine silk through a polished crystal; clay, folded leather/bronze tube,
charcoal-marked bark and silk are incoming messages). No book/reed ghost, no
modern handled lens, no simulated optics beam, no floating crystal, no
pseudo-Persian (the silk marks are indistinct, intentionally unreadable), no
Simurgh, and no voice. The static forward-facing source eyes are a **disclosed
acting limitation** (the proof does not claim a reading gaze), not a story
defect.

### Art-review issues (owner decisions — same set as Part S01-A, cross-referenced)

These are not pipeline defects; they are the concrete items owner art review
must resolve. See `qwen-chapter-01-s01-assets-review.md` S01A-01…S01A-05 for
the frame/coordinate detail. In short: (1) forward-facing source eyes vs. a
reading gaze; (2) face/neck contour seam; (3) flat vector style vs. the raster
source; (4) the wide/close table perspective as an intentional insert cut;
(5) stylized hand-grip believability. **A numeric 0 px grip anchor does not
establish a believable finger grip** — that remains owner judgment on the
actual B frames.

### Optional polish

- **S01B-03 — `info`** — commit the per-decode sample PNGs
  (`decoded-{en,fa}-N.png`) alongside the `.jpg` sheets so the decode evidence
  is reproducible file-by-file, or drop the reference in
  `s01-delivery-checks.json`.
- **S01B-04 — `info`** — the scan ROI `[480,380,590,417]` lies to the left of
  the crystal's travel, so it verifies the silk is static but is never crossed
  by the lens. The crystal/silk independence is still fully proven (crystal
  anchor moves while the silk anchor and this ROI stay static, and the `whole`
  fixture is caught by the moving silk/support anchors). No change required;
  noted so the ROI's role is not misread as a "crystal crossed the silk" check.

---

## 3. Question-by-question disposition (pipeline)

1. **12 s / 30 fps / 360 real 1280×720 frames, real silent movie, hash
   parity.** ✅ Verified independently (ffprobe on both committed movies; all
   360 frame hashes; movie hash; recapture byte-identity). Movie existence is
   scoped to this 12 s silent candidate — it does not imply chapter completion
   or recorded narration.
2. **One complete reading action; static head/eye as limitation.** ✅ The
   approach (3.5–4.2 s, y 364→394), one right→left 24 px scan (4.2–5.6 s),
   stable settle (frames 168–192, 0 px), and the 6.4 s material reveal are all
   present in the actual motion and both cuts. The forward-facing source face
   is a disclosed limitation, not approved acting.
3. **Grip continuity, signed monotonic scan, static anchors, ROIs, negatives.**
   ✅ All reproduced from pixels. The deliberate detach / oscillate / whole
   fixtures each fail their target measurement (12 px grip / 0 px net travel +
   reverse steps / 48 px travel + moving silk & support anchors, ROI 137/168).
   Computed 0 px anchors are explicitly distinguished from the visible grip
   (owner art question, §2).
4. **Absolute time, direct seek vs. sequential, reset/replay, node count,
   half-open boundaries incl. t=12.** ✅ `seek-*.png == replay-*.png == frames`
   at 2.0/4.8/6.4/11.9 and reset; `runtime-state-tests.json` records 14
   boundary states with `recursive_node_count = 22` stable across five replay
   cycles (both langs); boundaries are half-open including t=12.0 (empty
   caption/title, shot C).
5. **All malformed inputs fail explicitly; no hidden fallbacks.** ✅ `validate()`
   rejects language, fps/duration/size, asset ID set + duplicates, asset path
   escape (must be under `assets/s01`), asset hash, SVG size ≤ 0, input path
   escape (must be under repo root), input hash, unregistered grip anchors,
   wrong `wide` anchors, out-of-bounds contour, cue ID mismatch, malformed cue
   interval, and cue ≠ board. `input_negative_checks` **raises `AssertionError`
   if any of 14 cases is accepted** (no silent pass): 4 missing assets,
   duplicate asset, invalid anchor, invalid contour, malformed interval,
   unsupported language (`xx`), unsupported fps (60), and 4 invalid-time values
   (−0.1, 12.1, NaN, inf). Output is constrained to the candidate `renders/`
   tree (`is_relative_to(HERE/"renders")`). `run()` aborts on nonzero exit or
   `SCRIPT ERROR`/`ERROR:`. Stale-report risk is bounded by manifest/controller/
   language + full 360-frame hash re-check in `--recheck-existing` (S01B-02).
6. **Exact EN/FA cue strings, shaping, ZWNJ, direction, line breaks, glyphs,
   bounds; captions must not cover hands.** ✅ Cue strings match the board
   (the validator enforces `cue == board` for all four IDs). FA is a real Godot
   RAQM render — correct RTL order and the ZWNJ in `دبیره‌ها` — not a Pillow
   specimen. Per-frame `missing_glyphs` is empty; measured `caption_lines ×
   line_height ≤ 88`. The caption backing occupies y 600–704 while all hands /
   crystal / intake sit well above y ≈ 552, so **captions never cover hands**
   (confirmed in the B and C stills and encoded samples). Measured layout ≠
   human readability or recording-timing approval (silent candidate).
7. **Provenance / source-hash integrity, unchanged inputs, font licence,
   new-art disclosures, export portability.** ✅ All 7 manifest input hashes and
   10 asset hashes match; `s01-manifest.json.art_method` + `provenance_limits`
   disclose the new editable-vector reconstruction and the contour-sampled
   source face (`owner_approved = false`); the font is unmodified DejaVu Sans
   with the Bitstream Vera notice. Export is honestly scoped: Godot emits an
   image-file/export warning for the relative source cutout, no standalone
   export/package was performed, and the project runs inside the checkout —
   no standalone app is claimed. All my commands used `rtk`/`rtk proxy`.
8. **Scope/status — no invented Simurgh, voice, integration, signoff, or
   Persian-gate resolution.** ✅ `chapter-01-animation-status.json` keeps
   `chapter_complete = false`, `owner_final_approval = false`, phase 7
   `not_ready`, owner choices (Simurgh form, voice, art selections) all
   unresolved/pending, and the release gate recorded as the **book** gate
   (789 pass / 8 fail, stale Persian `source_sha256` Ch 01–04, exit 2, later
   targets not reached) — explicitly **not** a media failure. Nothing in the
   S01 evidence asserts a Simurgh form, voice, or owner approval.

---

## 4. Commands actually run (with exits)

| # | Command (all `rtk proxy`-prefixed) | Exit |
| --- | --- | --- |
| 1 | `python3 …/render_s01.py --language {en,fa} … --validate-only` (book `.venv`) | **1** (`No module named 'PIL'`) |
| 2 | `/usr/bin/python3 -c "import PIL"` | 0 (PIL 10.2.0) |
| 3 | `/usr/bin/python3 …/render_s01.py --language {en,fa} … --validate-only` | 0 (PASS, 14 adversarial cases) |
| 4 | `ffprobe … en/s01-silent.mp4` and `… fa/s01-silent.mp4` | 0 (1 video stream, 360, 12.0 s, 1280×720, 30 fps, 0 audio) |
| 5 | `sha256sum render_s01.py evidence/render_s01-capture-revision.py s01.gd s01-manifest.json` | 0 |
| 6 | `/usr/bin/python3` — 360-frame + movie + manifest/controller/revision-hash checks | 0 (all match; two revisions distinct) |
| 7 | `/usr/bin/python3` — motion recompute + seek/reset/replay + 3 negatives | 0 (all reproduced; negatives fail as expected) |
| 8 | `/usr/bin/python3` — boundaries + runtime-state tests | 0 (half-open incl. t=12; node 22 stable) |
| 9 | `ffmpeg` accurate decode at 11.9 s + PIL caption-bar measurement | 0 (bar cleared) |
| 10 | `ffmpeg` exact-frame decode 356/357 + PIL | 0 |
| 11 | `/usr/bin/python3 … --output renders/qwen-s01/en` (recapture) | 0 (PASS); frames byte-identical |
| 12 | `/usr/bin/python3 … --output renders/qwen-s01/fa` (recapture) | 0 (PASS); frames byte-identical |
| 13 | `git --no-optional-locks status --porcelain` (inspect only) | 0 (pre-existing mods not mine; scratch untracked) |
| 14 | `delete_path renders/qwen-s01` (cleanup of 980 M scratch) | done |

**Watched/inspected:** EN + FA encoded-movie sample sheets (actual decoded
MP4); EN/FA A/B/C stills, contact sheets, and the 11.9 s caption-clear
measurement. **Unverified claims:** continuous MP4 playback; the individual
`decoded-*.png` sample files (not committed); headless Godot (not used).

---

## 5. Coverage summary

| Area | Status |
| --- | --- |
| 360 × 1280×720 / 12 s / 30 fps frames per language | ✅ reproduced (byte-identical recapture) |
| Real silent MP4, 0 audio, hash parity | ✅ reproduced (ffprobe + hash) |
| One reading action: approach / 24 px scan / settle / 6.4 s reveal | ✅ reproduced (anchors + encoded samples) |
| Grip continuity 0 px (anchors) | ✅ reproduced |
| Signed monotonic single-pass scan, settle stability | ✅ reproduced |
| Static silk/support/backdrop anchors + ROIs | ✅ reproduced |
| Negatives detach / oscillate / whole each fail | ✅ reproduced from pixels |
| Direct seek vs. sequential at 2.0/4.8/6.4/11.9 + reset | ✅ reproduced (pixel equality) |
| Half-open cue boundaries incl. t=12.0 | ✅ verified (trace + cleared-caption measurement) |
| Stable recursive node count (22) over 14 states / 5 replays | ✅ verified (runtime-state tests, both langs) |
| 14 malformed-input cases explicitly rejected | ✅ reproduced (`--validate-only`) |
| Output-path containment; no hidden fallback | ✅ verified (code) |
| Exact EN/FA cue strings vs. board | ✅ verified (code + trace) |
| FA shaping / ZWNJ / direction (real Godot RAQM render) | ✅ inspected |
| Glyph coverage + measured caption bounds; captions clear of hands | ✅ verified |
| Provenance / source + asset hashes; font licence; new-art disclosures | ✅ verified |
| Two-revision capture-vs-verification hash distinction | ✅ verified |
| Scope/status integrity (no invented Simurgh/voice/signoff; book gate ≠ media) | ✅ verified |
| Continuous MP4 playback | **not verified** |
| Per-decode sample PNGs | **not committed** (sheets present) |
| Owner art acceptance | **not assessed/granted** |

---

## 6. Can the next chapter part proceed, and what still needs checking

**Yes — the technical foundation is sound.** The S01 proof is technically
verified and deterministic; nothing in it blocks moving to the *next*
reconciliation unit. The next step is **owner art/performance acceptance of
this concrete S01 proof** (the S01A items), after which production continues on
the bounded plan.

**Still needed before integration (not pipeline defects):**
- **Owner art acceptance** — reading gaze (or accept forward state), face/neck
  seam, vector style, wide/close cut, grip believability (S01A-01…S01A-05).
- **Owner decisions (out of this silent unit):** Simurgh form, voice approach
  and performances, final recorded timing/runtime.
- **Remaining shot assets/rigs (phase 3+)** and the animatic (phase 4) —
  unimplemented.
- **Book release gate (separate):** the 8 stale Persian `source_sha256`
  failures (Ch 01–04) require scoped editorial reconciliation; this is a
  manuscript/editorial matter, not a media proof failure, and must not be
  conflated with S01.
- **Minor media polish (optional):** S01B-01 (interpreter for the review
  command), S01B-02 (one-shot report+movie verification), S01B-03 (commit
  per-decode PNGs).

**No review verdict here grants owner art acceptance.** Codex remains
responsible for reproducing and addressing any findings.
