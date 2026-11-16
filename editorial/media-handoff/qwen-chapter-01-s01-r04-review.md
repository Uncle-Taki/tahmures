# Qwen review — S01 r04 wide reading action

Date: 2026-10-20. Reviewer: Qwen (GLM implementation), local Zed session with
repository filesystem access. Bounded read-only review following
`editorial/media-handoff/qwen-chapter-01-s01-r04-review-prompt.md` and AGENTS.md.
No manuscript, original art, approval, historical evidence, commit, upload,
provider call or automatic repair was performed.

## Verdicts

| Category | Verdict |
| --- | --- |
| Visible motion quality | **UNVERIFIED** — no defect found by actual pixel-level forensics (joins, ghosts, cuts, occlusion, confinement all verified clean), but this reviewer cannot view images in this session, so perceptual join naturalness, reading-action clarity at playback speed and cleanup-wall blend remain unjudged by eyes. No rework trigger was detected. |
| Technical reproducibility | **READY_FOR_OWNER_MOTION_REVIEW** — all four requested commands pass on both interpreters; independent recapture on the local display reproduced both editions bit-exactly (360/360 frames and movie hashes identical); motion-state tests reproduced identically; movies freshly probed and fully decoded; negative fixtures fail exactly their target checks; accepted r03 files and hashes intact. |

The combined recommendation: proceed to owner motion review by watching
`renders/s01-r04/{en,fa}/s01-silent.mp4` and the QA zooms
`revisions/s01-r04/evidence/inspection-only-*.png`. Nothing machine-checkable
blocks that review; nothing machine-checkable can substitute for it either.

## Actual access log

Everything below was actually opened or executed in this session. Filenames
alone were never treated as evidence; every pass claim in this report comes
from a command or pixel computation run here.

Files read (relative to repository root, under
`Characters/animations/chapter-01-candidate-01/` unless noted):

- `revisions/s01-r04/README.md`, `manifest.json`, `s01.gd`,
  `cleanup.gdshader`, `generation-prompt-v2.txt`, `generation-prompt.txt`,
  `asset-attempts.json`, `delivery-summary.json`, `shot-override.json`.
- `revisions/s01-r04/assets/forearm-cleanup-v2.png` (decoded to RGB and
  compared against the accepted art pixel-by-pixel);
  `rejected/forearm-cleanup-v1.png` (present, retained as rejected).
- `revisions/s01-r04/evidence/inspection-source.png`,
  `inspection-only-0.0.png`, `inspection-only-4.2.png`,
  `inspection-only-5.6.png` (decoded and analysed; see access limits below),
  `motion-state-tests-en.json`, `motion-state-tests-fa.json`,
  `accepted-source-pixel-check.json`, `negative-cli-checks.json`.
- `s01-motion.tscn`, `render_s01_motion.py` (all 496 lines),
  `render_s01.py` (all 365 lines), `tests/s01_motion_state_test.gd`.
- Inherited `revisions/s01-r03/s01.gd`, `revisions/s01-r03/manifest.json`,
  `revisions/s01-r03/assets/hall-reading-wide.png` (hash and pixels).
- `renders/s01-r04/en/` and `renders/s01-r04/fa/`: `verification.json`,
  `godot-trace.json` (full 360-frame traces recomputed independently),
  `s01-silent.mp4` (ffprobe + full decode + decoded-frame extraction),
  **all 360 frames per edition** (programmatic diff analysis), all
  `checks/seek-*.png`, `replay-*.png`, `reset.png`, `boundary-*.png` (hashed),
  `ffprobe.json`, `contact-sheet.jpg` and `evidence-*.png` (present),
  `negative-detach/`, `negative-oscillate/`, `negative-whole/` (43 frames and
  traces each, both editions).
- `renders/s01-r03/{en,fa}/frames/*.png` (all 360 per edition, used as the
  accepted reference for full-movie confinement) and `s01-silent.mp4` (hashed).
- `renders/s01-r04/qwen-en/`, `qwen-fa/` (created by my independent
  recapture; see commands).
- `editorial/media-handoff/chapter-01-owner-acceptance.json`,
  `chapter-01-animation-status.json`, `README.md`,
  `qwen-chapter-01-s01-r04-review-prompt.md`;
  `book/narrative-continuity.md` (Hall of Scripts setting revision, cast
  mapping, Chapter 01 episode row); `s01-review.html`, `s01-review-report.md`.

Commands actually executed from repository root (all exit 0 unless stated):

```bash
rtk proxy .venv/bin/python Characters/animations/chapter-01-candidate-01/render_s01_motion.py --language en --fps 30 --output renders/s01-r04/en --validate-only   # PASS, 15 negatives
rtk proxy /usr/bin/python3 Characters/animations/chapter-01-candidate-01/render_s01_motion.py --language fa --fps 30 --output renders/s01-r04/fa --validate-only   # PASS, 15 negatives
rtk proxy /usr/bin/python3 Characters/animations/chapter-01-candidate-01/render_s01_motion.py --language en --fps 30 --output renders/s01-r04/en --recheck-existing # PASS
rtk proxy /usr/bin/python3 Characters/animations/chapter-01-candidate-01/render_s01_motion.py --language fa --fps 30 --output renders/s01-r04/fa --recheck-existing # PASS
# extra interpreter coverage requested by question 6:
rtk proxy .venv/bin/python ... --language en ... --recheck-existing  # PASS
rtk proxy .venv/bin/python ... --language fa ... --recheck-existing  # PASS
# independent recapture on the real local display (X11 :0 available):
rtk proxy /usr/bin/python3 ... --language en --fps 30 --output renders/s01-r04/qwen-en  # PASS end-to-end
rtk proxy /usr/bin/python3 ... --language fa --fps 30 --output renders/s01-r04/qwen-fa  # PASS end-to-end
# separate node/state test, reproduced by me:
rtk proxy godot --path Characters/animations/chapter-01-candidate-01 --headless --script tests/s01_motion_state_test.gd -- --language=en --test-output=/tmp/qwen-motion-state-test-en.json  # PASS
rtk proxy godot --path Characters/animations/chapter-01-candidate-01 --headless --script tests/s01_motion_state_test.gd -- --language=fa --test-output=/tmp/qwen-motion-state-test-fa.json  # PASS
# fresh metadata probes and full decodes of all four movies (en/fa + qwen-en/qwen-fa):
ffprobe -v error -show_streams -show_format -of json <movie>   # single h264 video stream each
ffmpeg -v error -i <movie> -f null -                            # full decode, clean
```

Independent pixel analysis was run with `/usr/bin/python3` (PIL 10.2.0 +
numpy) over the actual PNG frames and the two source images; the analysis
scripts were temporary and removed after use. The book `.venv` has no PIL and
was used only for the stdlib validators, as documented.

## Question 1 — Is the accepted wide composition preserved?

**Yes, verified at pixel level, and more strongly than the project's own
checks.** I diffed **every one of the 360 frames per edition** of
`renders/s01-r04/{en,fa}` against the corresponding accepted r03 frame:
**zero pixels differ outside the declared edit ROI [795,190,110,140] in any
frame of either edition.** The project's own accepted-source check covered
only frame 0; the confinement holds for the whole movie, including all
caption/title rendering (the caption strip is outside the ROI, so EN/FA text
pixels are byte-identical to the accepted preview).

- At rest (frame 0) only 372 of 15,400 edit-ROI pixels (2.4%) differ from the
  accepted art by more than 8 levels; diff bbox (817,202)-(877,315) viewport,
  which maps exactly to the arm/hand/crystal silhouette (patch contour native
  1067–1146 × 264–365, cuff to 412).
- No close hand shot exists anywhere in either movie (rejected r02 art did
  not return; r02 files remain historical only).
- No flat material cards, no vector body collage: the materials/counter and
  all body regions outside the edit ROI are pixel-identical to the accepted
  wide illustration.
- The only moving part is the source-textured forearm/crystal pair rotating
  about the fixed sleeve opening, with the fixed cuff occluder polygon on
  top; room, face, silk, desk and message materials never change (see Q4).
- Accepted files intact (sha256): r03 art
  `15c86426…eda197`, r03 manifest `71c397e5…677928`, r03 movies
  `583874b5…71f29` (en) / `5837c7ad…8e058d` (fa) — all matching
  `chapter-01-owner-acceptance.json`. r04 dependency hashes in
  `verification.json` match the current files. The cleanup derivative
  `forearm-cleanup-v2.png` matches its manifest hash
  `d61fe6b1…1f1b4d` (1672×941) and is revealed only inside the bounded patch.
- The cleanup PNG itself differs from the art globally (9.1% of sampled
  pixels outside the patch differ >8) — expected for generated art and
  disclosed in the README; it is harmless because only the patch interior is
  ever composited (proven by the full-movie confinement above), and the
  accepted art file itself is untouched.

## Question 2 — Actual moving edges at neutral, alignment, mid-scan, settle

Programmatic edge forensics on the actual frames and QA zooms (this reviewer
cannot view images — see Access limits):

- **Zoom geometry verified.** `inspection-source.png` is the accepted art,
  unmodified: with the correct mapping (zoom origin native (832.75, 179.93),
  magnification 3.0622×), it matches a bilinear upscale of the art crop with
  mean diff 2.92, median 1. The zooms cover native (833–1251 × 180–415),
  which contains the entire patch/arm/cuff region.
- **Cuff/skin join stays connected.** Sampling the emergence line just above
  the cuff top edge (native y=371, x=1098–1126 at 0.5px steps, 56 samples) on
  actual frames 0, 105, 126, 144, 168, 240: 0/56 non-skin at neutral and
  pre-align, 0/56 at mid-scan and settle, 1/56 at settle (a single
  sleeve-edge pixel at the arm silhouette boundary), and 3/56 at the
  alignment pose (frame 126). Those 3 samples (native ~1105, rgb≈25,25,15)
  are the **source art's own dark shadow crease** at the sleeve opening —
  the accepted art has rgb(14,13,2) there and the cleanup also reconstructed
  dark interior — partially revealed as the arm edge shifts; the composite
  preserves the source's cream-lining → crease → skin order. No wall-colored
  gap ever appears in the join.
- **No straight cuts / angular seams.** Column/row gradient detector over the
  patch region of the settle zoom: strongest vertical gradient 10.3, *below*
  the accepted art's own baseline of 16.7 in the same region; at rest the
  strongest edge sits at the same column as the source's own crystal edge.
  No gradient ridge at the patch boundary — the 5px feather blend holds.
- **No old-hand ghost.** In the region vacated at settle (native 1124–1138 ×
  285–335), the composite matches the cleanup texture with median difference
  1 (p90 = 1) and clearly does not match the old arm pixels (median 5, p90
  79 against the art). The arm's original position is genuinely removed.
- **No wall inside the sleeve.** The cuff opening (native ~1105–1123 ×
  378–395) shows the original accepted pixels (composite vs art median 5),
  because the fixed cuff polygon redraws source pixels there; the v1
  "wall inside cuff" failure mode is structurally prevented in v2.
- **No misaligned thumb/crystal, no double fingers.** Forearm and crystal are
  separate polygons under the same pivot with the same source texture, so
  their relative geometry is rigidly identical to the accepted art at every
  instant; the hand is never redrawn. The detach fixture demonstrates the
  grip check detects separation (12.25px) while the normal run measures 0.0.
- **No lens halos.** No shader or glow is applied to the crystal (the only
  shader is the patch feather blend); the at-rest overlay footprint is
  sparse (2.4% of ROI, edge antialiasing only).
- **Occlusion.** At settle the crystal reaches native x≈1058, about 9 native
  px (≈7 viewport px) left of the cleanup patch edge (1067) — still inside
  the declared edit ROI (viewport x=795 ≙ native 1038.5) — passing in front
  of original background, which is correct occlusion for a foreground object.

## Question 3 — Does the wide action communicate one crystal-assisted reading?

Mechanically yes; perceptually unjudged (access limit). From the raw traces
and pixels:

- One rigid pivot about the fixed sleeve opening (elbow anchor native
  (1112,376), screen (851.3, 287.7)): angle 0 → +0.06 rad during 3.5–4.2s
  (alignment), one right-to-left sweep 4.2–5.6s reaching −0.30 rad, then a
  hold with 0.0px drift through 12s. Measured signed travel of the crystal
  centre: 20.9413px, monotonic (max reverse step −0.033px, zero rightward
  steps).
- No eye/blink/head/lip-sync: the head ROI (760,100,55,45) is
  pixel-identical across all 360 frames in both editions; there is no
  simulated optics or anatomical rig — only the two source-textured polygons
  and the fixed occluder.
- The motion is genuinely present in the encoded movies, not only in PNGs:
  decoded movie frame 126 vs 168 differs on 2659/2664 pixels (>8) inside the
  arm ROI and 0 pixels in the silk ROI.
- Magnitude context for the owner: 20.94px is ≈1.6% of frame width and
  ≈0.66 crystal widths — a deliberately small "reading sweep". The crystal
  does not pass over the silk (≈34px viewport gap remains at settle), and
  the downward gaze is static (accepted art). Whether this reads clearly as
  one crystal-assisted reading at 30fps playback is a perceptual judgement
  this reviewer cannot make; if the owner finds it too subtle, the bounded
  repair is a revised action contract (settle_radians / travel band), which
  the validator currently pins exactly, followed by recapture.

## Question 4 — Recomputed motion metrics and independence

Recomputed independently from `godot-trace.json` (not from
`verification.json`), identical in both editions:

| Metric | Value | Contract | Result |
| --- | --- | --- | --- |
| Grip (hand↔crystal) max error | 0.000 px | ≤ 1.5 px | pass |
| Signed travel (crystal centre x) | 20.9413 px | 20–28 px, right-to-left | pass |
| Monotonicity | max reverse step −0.033 px; 0 rightward steps | ≤ 0.25 px | pass |
| Settle drift (frames ≥168) | 0.000 px | ≤ 0.25 px | pass |
| Fixed anchors (elbow, silk, materials, head, plate) | 0.000 px each | ≤ 0.25 px | pass |

Pixel verification (my own PIL implementation, agreeing with the ffmpeg-based
reports): silk (705,328,65,20), materials (155,325,170,50), head
(760,100,55,45) and shelf (945,110,80,65) ROIs show **zero channel
difference** across frames 126–168; the arm ROI (795,195,95,120) changes on
**2536 pixels** (>8 levels) — exactly the reported count.

Negative fixtures (recomputed from their actual traces and confirmed by my
recheck and recapture runs):

- `detach`: grip 12.249 px → fails `grip_continuity` (target) ✓
- `oscillate`: travel 0.0 px, max reverse 3.114 px, 20 rightward steps →
  fails `one_pass_scan` (target) ✓
- `whole`: all anchors 24.0 px, silk ROI max channel diff 209, head 254,
  9831 changed pixels → fails `independent_motion` (target) ✓

The `whole` fixture failing **both** the anchor trace check and the pixel ROI
checks proves the zero ROI diffs in the normal run are meaningful evidence of
independent movement, not whole-image motion.

## Question 5 — Text, layout, captures, streams, cue boundaries, replays

- r04 manifest `captions`/`on_screen_text` are JSON-identical to the accepted
  r03 manifest; the trace caption/title text matches the expected cue at
  **all 360 frames in both editions** (0 mismatches); no missing glyphs;
  caption extent 33px < 88px limit.
- Cue boundaries behave exactly: NEN-01A 0.6–6.2s, NEN-01B 6.4–11.6s,
  OST-S01-1 0.6–4.8s, OST-S01-2 5–11.8s; boundary captures exist at all
  listed times; caption/title pixels are byte-identical to the accepted r03
  preview (outside-edit-ROI zero diff).
- 360 actual 1280×720 PNG captures per edition (count, PNG header dimensions
  and hashes verified; my recapture reproduced all hashes).
- Both movies freshly probed by me: exactly one h264 video stream, 1280×720,
  30/1 fps, 360 frames, 12.000000s, no audio stream; full decode clean.
  Decoded movie frames match the captured PNGs within normal CRF-18 lossy
  noise (mean ≈2.0, p99 ≈12).
- Direct seek/reset pixel equality at 2.0/4.8/6.4/11.9s and reset: verified
  by my own hashes (seek == replay == continuous frame; reset == frame 0).
- Five replay states: `five_state_replays_match` true in traces, and I
  re-ran `tests/s01_motion_state_test.gd` headless for both languages: 13
  boundary/seek states × five replays, all state-equal, stable recursive
  node count 11 — outputs byte-identical to the committed
  `evidence/motion-state-tests-{en,fa}.json`.
- No text-shaping backend is inferred anywhere in this review; only actual
  Godot RTL rendering with the same DejaVu font as the accepted preview is
  claimed (and the FA caption pixels equal the accepted FA preview).

## Question 6 — Negative validation, recheck binding, both interpreters

- The 15 input negatives recorded in `verification.json` were enumerated and
  match the code: missing accepted art, missing cleanup, bad elbow/contact
  anchor, out-of-range contour, unearned approval, forbidden close-up, bad
  action interval, changed cue, unsupported language (xx), unsupported fps
  (60), and four invalid times — plus the inherited base negatives (missing
  assets, duplicate asset, path escape, bad cue, false performance claim).
  All were exercised through my validate-only runs (which execute the
  negative cases) on both interpreters.
- Output containment: the runner rejects any output outside
  `renders/s01-r04/`; the recorded `accepted_output_guard` negative shows
  exit 1 "output must stay in renders/s01-r04; accepted r03 is protected".
  My recaptures wrote only to new `qwen-en`/`qwen-fa` folders; nothing
  existing was overwritten (recheck-existing verifies all 360 frame hashes
  and the movie hash before appending its record, and my runs left the
  report files byte-stable — the deterministic recheck record reproduced
  identically across four runs and two interpreters, matching the hashes in
  `delivery-summary.json`).
- Recheck binding verified in my runs: 10 dependency hashes (r04
  manifest/s01.gd/shader/tscn/runner/render_s01.py, r03 manifest/s01.gd,
  font, license), all 360 frame hashes, movie hash, fresh ffprobe metadata,
  full decode, normal motion checks and the three negative fixtures. The
  corrupt-movie regression (`regression-modified-movie`, exit 1 "changed
  dependencies or movie") is recorded in `negative-cli-checks.json`; I did
  not re-run it to avoid rewriting the existing fixture folder.
- Interpreter coverage: book `.venv` (stdlib-only) and `/usr/bin/python3`
  both pass validate-only and full recheck for both languages. The motion
  validators use only the standard library plus installed FFmpeg/Godot, as
  documented; no Pillow requirement exists in the validators.

## Question 7 — Approval boundaries

- r03 artwork/timing acceptance is scoped exactly as recorded: art, manifest
  and movie hashes in `chapter-01-owner-acceptance.json` all match the
  current files; the record's limits (no animation approval, no r02 revival,
  no Simurgh/voice selection, not final chapter acceptance) are respected by
  this candidate.
- r04 motion/cleanup remains unapproved: manifest `owner_approved: false`,
  status `motion_candidate_not_owner_approved`; production status records
  `owner_motion_review_pending`. This review does not approve it either.
- Simurgh form and voice approach remain unresolved owner choices; phases
  3–7 of chapter production are not implemented; `chapter_complete: false`.
- Source pixels sampled inside the forearm/crystal polygons are limited
  extraction for a rigid pivot, not an anatomical rig; no rig approval is
  inferred.
- No rejected r02 art was revived and no Persian source hashes were
  rewritten. The repository release gate remains blocked by the pre-existing
  stale Persian `source_sha256` failures in Chapters 01–04 (789 pass / 8
  fail, `make check` exit 2) — unrelated to this candidate, unchanged by
  this review, and outside its authorized scope.

## Findings

| # | Severity | Finding | Consequence | Bounded repair |
| --- | --- | --- | --- | --- |
| F-1 | Blocker (for the visual verdict only) | This reviewer cannot view images in this session (`read_file` image reading unsupported). All image inspection here was programmatic pixel forensics. | Perceptual join naturalness, reading clarity at playback speed and cleanup-wall blend cannot be approved by this review; verdict for visible quality stays UNVERIFIED. | Owner (or a vision-capable reviewer) watches `renders/s01-r04/{en,fa}/s01-silent.mp4` and `revisions/s01-r04/evidence/inspection-only-*.png` (QA zooms, not scenes). |
| F-2 | Low (visual risk) | Cleanup wall reconstruction differs from original wall texture in a small zone: right wall strip (native 1132–1141 × 270–360) median 3, but 8% of pixels >32 and 4% >64 levels; top strip clean (0 px >16). At settle the vacated area shows this regenerated wall. | Possible faintly visible wall-texture change right of the reading hand at settle, mainly under zoom. | If the owner sees it: regenerate the cleanup with tighter wall preservation or widen the feather, then recapture (pipeline is deterministic; all checks re-run). |
| F-3 | Low (visual risk) | At settle the crystal/hand extend ≈9 native px (≈7 viewport px) left of the cleanup patch edge (native 1058 vs 1067), over unpatched original background; still inside the declared edit ROI. | None mechanically (correct foreground occlusion over wall/desk background); confirm visually that nothing inappropriate is covered. | Owner eyeball check; no code change anticipated. |
| F-4 | Info (no defect) | At the alignment pose (frame 126, t=4.2s) a 1.5 native-px dark sliver (rgb≈25,25,15) appears at the emergence line, native ~1105 × 369–372. Verified to be the accepted art's own shadow crease (source rgb(14,13,2)), not a hole or gap; join order preserved. | None — this is source structure, correctly revealed. | None. |
| F-5 | Info (owner judgement) | Motion magnitude is deliberately small: 20.94px ≈ 1.6% of frame width ≈ 0.66 crystal widths; crystal never passes over the silk; gaze static. | Reading clarity at playback speed is unproven either way; a numeric anchor cannot approve clarity. | If judged too subtle: revise the action contract (settle_radians / expected travel band) via a new bounded unit; the validator pins exact action values, so it must be updated in step. |
| F-6 | Medium (pre-existing, out of scope) | Repository `make check` exit 2: 789 pass / 8 fail on stale Persian source hashes, Chapters 01–04. | Full-chapter gates remain blocked; not caused or fixed by this candidate. | Separate scoped editorial reconciliation (already tracked in `chapter-01-animation-status.json`); no automatic repair attempted here. |
| F-7 | Info | `--recheck-existing` appends/overwrites the `recheck` record inside `renders/s01-r04/{en,fa}/verification.json` by design. | Report files change on recheck; frames/movies never do. Content proved deterministic (byte-identical across 4 runs and 2 interpreters; hashes still match `delivery-summary.json`). | None needed; future rechecks remain non-destructive to evidence. |
| F-8 | Info (resolved) | Recapture required real display access. | — | Display was available (X11 :0); independent recapture succeeded and was **bit-identical** (360/360 frames, movie hashes `966a6340…`/`f9adb0dc…`), so recapture is verified, not unverified. |

## Remaining visual risks (for the owner's motion review)

1. Skin-texture continuity where the rotated forearm crosses the fixed cuff
   edge (mechanically covered; texture alignment unverifiable without eyes).
2. Cleanup wall blend in the vacated area (F-2 numbers above).
3. Overall readability of the small right-to-left sweep as "one
   crystal-assisted reading" (F-5).

## Access limits

- **No image viewing.** This session's model could not render image files
  (`read_file` on PNG returns "model doesn't support it"). Every image claim
  above comes from decoding pixels programmatically (PIL/numpy) — actual
  data, but not human-like perception. This is why the visible-quality
  verdict is UNVERIFIED despite clean forensics.
- **Recapture verified.** Real display existed; both editions recaptured
  end-to-end with bit-identical outputs (F-8).
- The corrupt-movie regression fixture was read but not re-executed, to
  avoid overwriting the existing fixture folder (F-7 covers equivalence via
  my rechecks).
- No web/network access was used; no external model, provider or upload was
  involved.

## Conclusion

Everything executable in this review scope was executed, and reproduced
bit-exactly where reproduction was possible. No machine-detectable defect
remains: composition preservation, join continuity, ghost/cut/occlusion
forensics, motion metrics, negative fixtures, cue fidelity, stream
properties, replay/state stability and both-interpreter validation all pass
on actual files. The decisive remaining question — whether the action *looks*
like a clean, single crystal-assisted reading with a natural cuff join —
requires the owner's eyes on the two movies and the QA zooms. Recommend
proceeding to that owner motion review with F-2/F-3/F-5 as the specific
points to watch.
