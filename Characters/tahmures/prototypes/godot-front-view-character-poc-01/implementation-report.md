# GODOT_FRONT_VIEW_CHARACTER_POC_01 — Stage A implementation report

**Phase:** GODOT_FRONT_VIEW_CHARACTER_POC_01
**Stage:** PROJECT_BOOTSTRAP_AND_VISUAL_RIG
**Implementer:** GLM (primary implementer and self-tester)
**Date:** 2026-10-09
**Revised:** 2026-10-10 — bounded layout revision 01 (see the addendum at the
end of this report)
**Project:** `Characters/tahmures/prototypes/godot-front-view-character-poc-01/`
**Machine-readable record:** `validation.json` (same directory)

---

## 1. Toolchain versions and command results

| Tool | Observed version | Result |
| --- | --- | --- |
| Godot | `4.7.2.stable.official.ed1daf0bf` | matches the preflight record |
| FFmpeg | `6.1.1-3ubuntu5` | matches the preflight record |
| ffprobe | `6.1.1-3ubuntu5` | matches the preflight record |
| eSpeak NG | `1.51` | present, owner-auditioned and **rejected** — never used for narration |

Section-8 smoke tests (run from the repository root, exit codes recorded in
`validation.json`):

- `godot --headless --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --import`
  → **exit 0**, clean first scan and reimport, no errors or warnings.
- `godot --headless --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --quit-after 2`
  → **exit 0**; printed the stage header, Godot version, language `en`,
  timeline identity (`preview/preview_master`, 18.0 s, 11 beats, auto-loop)
  and `BEAT t=0.00 -> NEUTRAL IDLE`. (Headless reports a dummy 64x64
  viewport; these two commands are smoke tests only and do not show the
  animation.)

## 2. Approved source hash verification

All verified live by `scripts/check_integrity.py` (19/19 checks pass) and by
direct hashing during implementation:

- `Characters/tahmures/prototypes/layout01-facial-states-01/manifest.json`
  SHA-256 `b081e9190f5ddf1e8eff643863b1bbee5ab7b4a176179a26703b1c4ad32e4ba4`
  — **matches the pinned value**.
- `Characters/tahmures/prototypes/layout01-facial-states-01/files-sha256.json`
  SHA-256 `6135d7b65239919ebb2834913aa20b93d391d16d40f2a35c4a499e337b1cea21`
  — **matches the pinned value**.
- Every referenced file digest in that package index — verified before
  copying and re-verified after copying (17/17 byte-identical components).
- Cross-check of the v7 source package
  (`Characters/tahmures/versions/layout01-v7`): manifest SHA-256
  `b7539646b960fc9313c907effabb1f5de84ca816678fc0a0d1224c5f46ee1cd4` and
  index SHA-256
  `3b2ad23048da5ba009069f6c0ca86f78e6694927e151ac3e7b5e84393f4347bc` —
  both match.
- Human approval record
  `Characters/tahmures/workflow/approvals/layout01-facial-states-01-human-approval.json`
  — read and honoured; not modified (its mtime predates implementation).

The approval covers the reviewed front-view facial-state head for continued
prototyping only. No permanent body/arm/hand art, pointing pose, new
expression art, voice, or finished character design is approved, and none is
claimed.

## 3. Project and main scene paths

- Project root (did not exist at task entry; created fresh):
  `Characters/tahmures/prototypes/godot-front-view-character-poc-01/`
- `project.godot` — Godot 4.7.2, GL Compatibility renderer, 1280x720
  viewport, main scene configured as `scenes/main.tscn`.
- Main scene: `scenes/main.tscn` (56 nodes: World/Rig/Head with the 17
  approved sprite layers, temporary torso/arm chain, HUD, labels,
  AnimationPlayer with the `preview/preview_master` animation).
- Controller: `scripts/main.gd` (timeline beats, HUD state readout, R-key
  replay, `-- --language=en|fa` hook).

## 4. Exact animation events and durations

One deterministic timeline, `preview/preview_master` in the `preview`
AnimationLibrary, **18.0 s** (within the required 15–20 s), linear auto-loop;
the **R** key replays immediately. Driven by AnimationPlayer tracks (13
tracks: visibility toggles, the 1 px brow position shift, arm rotation keys,
mark opacity, torso breathing scale) — not by manual timing.

| t (s) | Event |
| --- | --- |
| 0.0 | neutral idle; temporary torso breathing (3.0 s period, 1.2% scale) |
| 2.5 | blink — approved closed-eyelid state |
| 2.85 | blink ends (back to neutral) |
| 5.0 | thinking — approved brow state (underlay + 1 px brow raise) |
| 8.0 | thinking ends |
| 9.0 | point raise — temporary arm shoulder −6° → −80° over 0.8 s (smoothstep); elbow staggered 9.2–10.0, hand 9.4–10.2 |
| 9.8 | gold point-target mark fades in (fully visible at 10.4) |
| 10.8 | approved small-open mouth state — **NOT speech / lip-sync** |
| 12.2 | mouth returns to neutral lower face |
| 13.0 | arm returns (13.0–13.8); mark fades out (13.4–14.0) |
| 14.0 | neutral idle to 18.0, then the timeline loops |

Headless evidence (`--quit-after 3400`): the full 11-beat sequence prints at
the designed times (within one 60 Hz frame) and then **repeats from t=0** —
auto-loop confirmed. The HUD shows the current state, time, and a progress
bar with beat ticks; it sits at the screen edge and does not obscure the
character.

## 5. Approved input components actually used

17 components, copied byte-exact and hash-recorded in `manifest.json`:

- From `layout01-v7` (14): `head_base`, `hair_back`, `diadem_gold`,
  `ear_left`, `ear_right`, `eyebrow_left`, `eyebrow_right`, `eye_left`,
  `eye_right`, `nose`, `moustache`, `beard`, `lower_face_neutral`,
  `lower_face_open_test`.
- From `layout01-facial-states-01` (3): `eye_left_closed`,
  `eye_right_closed`, `thinking_brow_underlay`.

States exercised: **neutral** (all base layers), **blink** (closed-eyelid
pair replacing the open eyes), **thinking** (underlay + the approved 1 px
brow raise), **small-open mouth** (`lower_face_open_test` replacing
`lower_face_neutral` — labelled open-test, not speech).

Approved art is used without modification: sprites are unrotated, unscaled,
nearest-filtered, full-canvas children of `Head` at the source-canvas centre,
so world coordinates equal the original 1086x1448 canvas coordinates; draw
order reproduces the approved render groups exactly. States are driven only
by visibility toggles plus the approved 1 px brow shift (asserted by
`check_integrity.py`). The render was additionally verified against approved
state composites pixel-by-pixel (`renders/verification.json`).

## 6. Temporary placeholder body parts

There is no approved Tahmures body/arm art, so the pointing beat uses
clearly labelled flat stand-ins in `assets/temporary-body/`:

- `torso.png`, `upper_arm.png`, `forearm.png`, `hand_point.png`,
  `point_target.png` — deterministic flat shapes generated by
  `scripts/generate_temporary_body.py` (regenerates byte-identically;
  verified by `check_integrity.py`).
- Two in-scene labels read **“TEMPORARY PROTOTYPE PLACEHOLDER — NOT
  APPROVED CHARACTER ART”** (torso and arm/hand), and all placeholder nodes
  are in the `temporary_placeholder` group.
- Not added to the canonical registry; not represented as extracted source
  pixels. Pivot-preserving replacement instructions are documented in
  `assets/temporary-body/README.md` and `manifest.json`.

## 7. Visible GUI inspection

**Possible: yes.** The workstation has `DISPLAY=:0` (X11, Mesa Intel Iris Xe
graphics). During implementation the project was run visibly: a real
1280x720 window played the full 18 s timeline and looped; the process was
ended by an external timeout (~25 s, exit 124 by design — not a crash).
Owner re-inspection command (from the repository root):

```bash
godot --path Characters/tahmures/prototypes/godot-front-view-character-poc-01
```

Editor route: `godot --editor --path Characters/tahmures/prototypes/godot-front-view-character-poc-01`,
open `scenes/main.tscn`, **F6**/**F5** to run, **R** to replay, Stop to
return.

## 8. Silent render evidence

**An actual silent render exists and was inspected:**
`renders/stage-a-preview.avi` — MJPEG, 1280x720, 30 fps, 540 frames,
exactly 18.000 s, 41,467,098 bytes, SHA-256
`65075c5885e74a2589577e4e6191aa747cf49d66de135cdd72d08969453c5323`
(hash-pinned in `manifest.json`). Produced locally and deterministically
with Godot Movie Maker (`--write-movie --fixed-fps 30 --quit-after 540`).

Its audio track is the engine-recorded **silent** master bus (pcm_s16le,
48 kHz stereo; measured mean/max volume −91.0 dB — the digital-silence
floor). It is **not** narration and **not** a speech placeholder.

Six key frames are extracted to `renders/frames/`, and
`renders/verification.json` (hash-pinned) records the pixel-level
verification against approved state composites. Highlights:

- Head-region fidelity: mean abs diff 5.8–6.4 of 255 across the five
  sampled states — MJPEG texture loss on hair/gold regions, no alignment or
  state error; screen mapping `screen = world + (80, 30)` confirmed by a
  sharp alignment minimum.
- Blink: eye-region diff mean 53.7, 64.6 % of eye pixels changed (baseline
  0.0); frame discrimination blink 3.78 vs neutral 38.72 — clearly visible.
- Thinking: brow region 10.1 % changed (baseline 0.0 %); discrimination
  5.99 vs 11.85 — visible.
- Pointing: arm region 6.8 % changed on raise (baseline 0.04 %); target
  ring 100 % gold at t=11.0 vs 0 % at t=1.0 — clearly visible.
- Open-test mouth: 1.2 % of mouth-region pixels changed; discrimination
  6.46 vs 7.20 — intentionally subtle, because the approved open-test state
  is a small (~23x3 px) sliver. It is not speech.

## 9. All test commands, exit codes, and observed errors

| Command | Exit | Notes |
| --- | --- | --- |
| `godot --version` | 0 | 4.7.2.stable.official.ed1daf0bf |
| `ffmpeg -version` / `ffprobe -version` | 0 | 6.1.1-3ubuntu5 |
| `godot --headless --path <p> --import` | 0 | clean, no warnings |
| `godot --headless --path <p> --quit-after 2` | 0 | header + first beat |
| `godot --headless --path <p> --quit-after 3400` | 0 | 15 BEAT lines; full loop + restart |
| `godot --headless --path <p> --quit-after 2 -- --language=fa` | 0 | `language: fa` hook works |
| `godot --path <p>` (visible) | 124 | external timeout kill by design; full loop observed |
| Movie Maker render (`--write-movie … --fixed-fps 30 --quit-after 540`) | 0 | 540 frames, deterministic |
| `python3 scripts/check_integrity.py` | 0 | 19/19 PASS |
| `ffprobe renders/stage-a-preview.avi` | 0 | properties as listed above |
| `ffmpeg … -af volumedetect` | 0 | mean/max −91.0 dB (silence) |
| `git diff --check` / `git diff --cached --check` | 0 | clean |
| `git status --porcelain` | 0 | only untracked additions (see §10) |

**Observed errors — none in the final state.** One incident was found and
resolved during final validation: re-running the documented `--import`
command generates `renders/frames/*.png.import` Godot metadata files that
were not yet listed in `manifest.json` (the frames had been extracted after
the last import of the implementation session). The 6 entries were added to
the manifest (65 → 71 listed files, hashes recorded); `check_integrity.py`
is now green and remains stable across repeated runs of both documented
smoke commands. No content file changed — metadata only. Recorded as
incident `frame-import-metadata-unlisted` in `validation.json`.

## 10. Protected-source integrity

- `git diff --check` and `git diff --cached --check` are clean; **no tracked
  file in the repository was modified**.
- `git status --porcelain` shows only `?? Characters/` (a pre-existing
  untracked tree that contains this new project and the already-untracked
  approved packages) and `?? li*3` (a pre-existing unrelated untracked
  file). All new files live inside the project directory.
- The approved packages, v7 sources, approval evidence, workflow files,
  book chapters, blueprints, continuity, registry, glossary, and shared
  tooling were not edited; input-package hashes re-verify, and
  workflow/approval file mtimes predate implementation.

## 11. eSpeak / audio policy confirmation

**eSpeak was not used for narration or any deliverable audio.** The owner
auditioned the installed English and Persian eSpeak voices and rejected
both; no eSpeak invocation was made, no voice parameters were tuned, and no
cloud TTS, external endpoints, paid services, or voice cloning were used.
No speech files exist: `audio/en/` and `audio/fa/` contain only READMEs
describing the expected **human-recorded WAV** inputs for the future audio
stage. The AVI’s audio track is engine-recorded digital silence, documented
as such. The temporarily scheduled open-mouth pose is the approved
open-test state and is never called speech or lip-sync.

## 12. Stage-A acceptance gates

| Gate | Status |
| --- | --- |
| GODOT_PROJECT_IMPORTS? | **PASS** — `--import` exit 0, clean |
| MAIN_SCENE_RUNS? | **PASS** — smoke, visible GUI, and Movie Maker runs all succeeded |
| APPROVED_INPUT_HASHES_MATCH? | **PASS** — pinned package, index, v7 cross-check, 17/17 components |
| APPROVED_FACE_STATES_USED_WITHOUT_MODIFICATION? | **PASS** — byte-exact copies; visibility toggles + approved 1 px brow shift only; render-verified |
| BLINK_AND_THINKING_VISIBLE? | **PASS** — strong pixel evidence (§8) |
| TEMPORARY_POINTING_BEAT_VISIBLE? | **PASS** — arm + gold-mark pixel evidence (§8) |
| TIMELINE_IS_REPEATABLE? | **PASS** — auto-loop observed, R-key replay, fixed-fps deterministic render |
| AUDIO_NOT_FAKED_OR_MISREPRESENTED? | **PASS** — no audio files; documented engine silence only |
| NO_PROTECTED_SOURCE_CHANGED? | **PASS** — §10 |
| git_diff_check_clean? | **PASS** — both diff checks exit 0 |

## 13. Next owner action and voice-stage prerequisite

1. **Owner action (visual):** run
   `godot --path Characters/tahmures/prototypes/godot-front-view-character-poc-01`
   from the repository root and watch the 18 s loop (idle → blink → think →
   point + mark → open-test mouth → return). Judge timing, readability of
   the HUD/labels, and placeholder-body acceptability for continued
   prototyping. Optionally inspect `scenes/main.tscn` in the editor.
2. **Voice-stage prerequisite:** the owner must provide recorded narration
   WAVs (English and Persian) or separately authorize a bounded local-voice
   audition. eSpeak is rejected and will not be revisited.

**Stage B (documented, not started):** audio integration, envelope
extraction, subtitle timing, mouth/audio synchronization (viseme policy
needs new human approval), final two-language movie export, and
permanent body/arm/hand art approval.

## 14. Scope statement

Stage A is a pipeline/rig prototype and is technically ready for GPT-Codex
review. The complete 15–20 second bilingual video proof is **not** complete
and is not claimed; voice selection and exports remain pending.

---

# Addendum — Stage-A layout revision 01 (2026-10-10)

**Gate:** STAGE_A_HUD_AND_SAFE_LAYOUT_CORRECTION (bounded correction)
**Trigger:** GPT-Codex `workflow/godot-front-view-character-poc-01/reports/codex/verification-01.md`
**Scope:** visual UI/layout only. The already-passing Godot project, approved
art, animation behaviour, and render route are preserved; no audio work.

## R.1 Revision summary

The defect: in the original 1280x720 preview, the language/debug line at
y≈92 crossed the head/diadem, the temporary torso/arm labels sat at
y≈540–616, and the dynamic state label spanned x≈16–1000 at y≈606–646,
drawing across the body and colliding with the placeholder labels, while
time, hint, and progress competed for the remaining lower strip (see the
six original frames, especially `t6.5s-thinking.png` and
`t11.0s-point-open-mouth.png`).

The correction assigns five distinct, readable zones (map in R.2):

1. approved character + temporary body/arm motion — centre;
2. Persian name + short project header — top strip;
3. temporary-placeholder identification — mid-left and bottom-right
   callouts outside the silhouette;
4. current-state indicator — bottom-left control column;
5. time/progress controls — same control column, below the state label.

On-screen state text is now compact (`IDLE`, `BLINK`, `THINKING`, `POINT`,
`POINT + OPEN TEST`, `RETURN`); long explanations moved to the console
(`BEAT t=%.2f -> label (detail)`). The progress-bar tick labels moved below
the bar. The language line reads `language: en · narration: none (stage A)`
and stays left of the head. No approved sprite was rescaled, rotated,
repainted, or moved — only HUD/callout Label nodes and the mark label were
re-positioned (the rig and camera are untouched).

Unchanged by design: the 17 approved input images and their source hashes;
the approved facial-state prototype, approval record, and v7 package;
facial layer order, state art, and the 1 px thinking-brow shift; the 18.0 s
timeline, event ordering, and beat times; the temporary-only status of
torso, arms, hands, and target marker; language selection behaviour; the
eSpeak rejection; and the silent-audio documentation.

## R.2 Screen-region map (1280x720, screen coordinates)

| Region | Rect (x0, y0, x1, y1) | Contents |
| --- | --- | --- |
| Header top-left | 16–460, 4–102 | title (4–26), subtitle (26–44), طهمورث (50–82), language line (86–102) |
| Header top-right | 760–1264, 6–24 | right-aligned version line |
| Character core | 465–775, 46–720 | approved head (diadem top y≈48) + temporary torso/arms |
| Torso callout | 110–430, 448–492 | 2-line TEMPORARY placeholder note, right-aligned, outside silhouette |
| Arm callout | 975–1264, 584–648 | 3-line TEMPORARY placeholder note, outside silhouette |
| Control column | 16–430, 540–700 | CURRENT STATE caption (540–556), state label (558–600), time (606–626), hint (630–646), bar (662–674), tick labels (681–697) |
| Mark label | 1104–1240, 402–424 | gold `MARK (scene prop)`, pointing beat only, right of the ring |

Guard zones asserted by `check_integrity.py`: character core rect
(465, 46, 775, 720); raised-arm sweep circle (centre (728, 460), radius
240 px); point-mark rect (1005, 350, 1075, 410). All 13 fixed UI rects must
stay inside the viewport (16 px margin), avoid those zones, and remain
pairwise disjoint.

## R.3 Files changed (all inside the project directory)

- `scenes/main.tscn` — HUD label rects, callout rects/alignment, mark label
  position, `LS_world` font size 13; animation tracks, rig, camera unchanged.
- `scripts/main.gd` — compact BEATS labels + console-only details; bar
  constants (16, 662, 410, 12) with tick labels below the bar; shortened
  language/hint lines. Beat times unchanged.
- `scripts/check_integrity.py` — new HUD safe-layout static checks (10 new
  checks; 19 → 29 total) and `__pycache__` skip in the unlisted-file walk.
- `scripts/verify_render.py` — new `hud_layout` pixel-check section (8
  checks, exits non-zero on failure).
- `.gitignore` — added `__pycache__/`.
- `renders/stage-a-preview.avi` — regenerated (UI is baked into the render):
  34,591,924 bytes, SHA-256
  `91bcb60405d0b3a85a0537cf01430962dc218807d4bb40aa82dacc4b25ed8b87`.
- `renders/frames/*.png` — the six keyframes re-extracted at t=1.0, 2.65,
  6.5, 10.6, 11.0, 15.0 (same filenames/times).
- `renders/verification.json` — regenerated with the `hud_layout` section.
- `manifest.json` — refreshed hashes for every changed/generated file;
  added `scene.hud_safe_layout`; updated `generated_by`/`date`.
- `README.md` — owner-facing HUD description + screen-zone table;
  `verify_render.py` exit-code semantics.
- `validation.json` — this revision's validation record
  (`record_type: stage-a-validation-layout-revision-01`).
- `implementation-report.md` — this addendum.

## R.4 Frame inspection evidence

Machine pixel checks (`verify_render.py` `hud_layout`, all six keyframes,
recorded in `renders/verification.json`):

| Check | Region | Result |
| --- | --- | --- |
| language band left of head | 465–508, 80–112 | 0 ink pixels (all frames) — PASS |
| language band right of head | 730–1280, 80–112 | 0 ink pixels (all frames) — PASS |
| header band above diadem | 560–680, 30–46 | 0 ink pixels (all frames) — PASS |
| torso band free of HUD text | 465–770, 560–668 | 0 light-text pixels (all frames) — PASS |
| state label visible | 16–430, 556–602 | 446–1580 px depending on label — PASS |
| torso callout visible | 0–465, 440–500 | 4367 px, constant — PASS |
| arm callout visible | 900–1280, 570–660 | 4551 px, constant — PASS |
| mark label gold beside ring | 1090–1280, 395–430 | 130 px at t10.6/t11.0, 0 elsewhere — PASS |

Head-region fidelity against the approved composites **improved** from
mean 5.8–6.4 / max 227 (original render) to mean 4.2–4.9 / **max 82**
(regenerated render) — the old maximum was dominated by HUD text pixels
that crossed the head region and are now gone.

Human-equivalent visual inspection: the six regenerated keyframes were
inspected at full view by a vision-capable review agent. Verdict **PASS**
on all six frames: no text overlaps or touches the head, face, diadem,
beard, or hair; state labels clear of the torso; both placeholder callouts
clear of the silhouette, the HUD, and each other; the raised arm and hand
clear all text on the pointing frames; the `MARK (scene prop)` label stays
clear of the ring and hand; all text legible; the five zones are distinct;
no clipping or stray artifacts. One observation, resolved as by-design:
at t=15.0 the compact label reads `IDLE` because the RETURN beat
(arm lowering, mark fade) runs 13.0–14.0 and the final beat 14.0–18.0 is
"neutral idle to end of loop".

The owner should still re-inspect the live preview (R.6); geometry and
frame evidence do not replace the owner's subjective judgement.

## R.5 Commands and results (revision pass)

| Command | Exit | Result |
| --- | --- | --- |
| `godot --headless --path <p> --import` | 0 | clean; 0 error/warning lines |
| `godot --headless --path <p> --quit-after 2` | 0 | header + `BEAT t=0.00 -> IDLE (…)` |
| `godot --headless --path <p> --quit-after 3400` | 0 | full 11-beat loop + restart at t=0.01; beat times unchanged |
| `godot --headless --path <p> --quit-after 2 -- --language=fa` | 0 | `language: fa (visual timeline identical for en/fa)` |
| Movie Maker render (`--write-movie --fixed-fps 30 --quit-after 540`) | 0 | 540 frames, 34,591,924 bytes |
| `python3 scripts/check_integrity.py` | 0 | 29/29 PASS (incl. 10 new layout checks) |
| `python3 scripts/verify_render.py` | 0 | all checks recorded; HUD layout 8/8 PASS |
| `ffprobe renders/stage-a-preview.avi` | 0 | mjpeg 1280x720 30 fps 540 frames; pcm_s16le 48 kHz stereo; 18.000 s |
| `ffmpeg … -af volumedetect` | 0 | mean/max −91.0 dB (engine silence, not narration) |
| `git diff --check` / `git diff --cached --check` | 0 | clean |
| `git status --porcelain` | 0 | `?? Characters/` (pre-existing untracked tree with this project) and `?? li*3` (pre-existing, unrelated, untouched by this pass) |

Observed errors in the final state: none. Two development-time issues were
found and fixed before the recorded runs: (1) the new checker section
initially failed to parse the `TargetLabel` node header (regex broke on
`groups=[...]`) and had a set/bool `TypeError`; (2) an ad-hoc analysis
import created `scripts/__pycache__/`, which would trip the unlisted-file
walk — the checker now skips bytecode caches like `.godot` and
`__pycache__/` was added to the project `.gitignore`. Recorded as incidents
in `validation.json`.

## R.6 Gates after the revision

All ten original Stage-A gates remain **PASS** (re-verified; see
`validation.json` for evidence). New layout gates:

| Gate | Status |
| --- | --- |
| HUD_ZONES_RESPECTED? | **PASS** — static zone checks + pixel bands |
| LANGUAGE_LINE_CLEAR_OF_HEAD? | **PASS** — 0 ink in both head-flank bands, all frames |
| STATE_TEXT_NOT_OVER_TORSO? | **PASS** — 0 light-text pixels in the torso band |
| CALLOUTS_OUTSIDE_SILHOUETTE? | **PASS** — outside core rect and arm sweep |
| CALLOUTS_NOT_COLLIDING_WITH_HUD? | **PASS** — pairwise disjoint + visual inspection |
| LABELS_LEGIBLE? | **PASS** — vision-agent inspection of all six frames |
| RENDER_EVIDENCE_REGENERATED? | **PASS** — new AVI + frames + verification.json |

## R.7 Still pending (unchanged by this revision)

Audio stage (owner voice decision: human-recorded WAVs or a separately
authorized bounded local audition), narration quality, lip-sync, and
permanent body/arm/hand art. The complete 15–20 s bilingual video proof is
**not** complete and is not claimed.

Owner re-inspection command (from the repository root):

```bash
godot --path Characters/tahmures/prototypes/godot-front-view-character-poc-01
```

---

GODOT_FRONT_VIEW_CHARACTER_POC_01_LAYOUT_REVISION_READY_FOR_GPT
