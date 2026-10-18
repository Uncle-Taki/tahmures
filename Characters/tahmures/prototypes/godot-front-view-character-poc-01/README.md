# Tahmures — Godot Front-View Character POC 01 (Stage A visual rig + Stage B0 interface)

A real Godot 4.7.2 project that assembles the human-approved front-view
facial-state head (layout01-facial-states-01) on a deterministic,
repeatable 18-second preview timeline with clearly labelled temporary
body stand-ins for a pointing beat.

- **Pipeline/rig prototype only** — not final character art, not the
  final video, and **no narration audio** (the owner rejected the
  installed eSpeak voices; stage B waits for acceptable recorded
  voice input).
- **Stage B0 adds only an inert input contract and a test-only caption
  layout.** It does not load/play audio, create narration, or animate speech.
  The Persian/English fixture strings are not owner-approved narration.
- The temporarily scheduled open-mouth pose is the approved
  *open-test* state. It is **not** speech and **not** lip-sync.
- Everything under `assets/temporary-body/` and every node in the
  `temporary_placeholder` group is **TEMPORARY PROTOTYPE PLACEHOLDER —
  NOT APPROVED CHARACTER ART**.

## Toolchain (observed on this workstation)

| Tool | Version |
| --- | --- |
| Godot | 4.7.2.stable.official.ed1daf0bf |
| FFmpeg / ffprobe | 6.1.1-3ubuntu5 |
| eSpeak NG | 1.51 — auditioned and **rejected** by the owner for narration; not used |

## Commands (run from the repository root)

1. Import resources (headless smoke test):

   ```bash
   godot --headless --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --import
   ```

2. Run the main scene for two engine iterations (headless smoke test):

   ```bash
   godot --headless --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --quit-after 2
   ```

   Both commands print engine output and must exit 0. They do **not**
   show the animation.

3. Watch the preview visibly (this is the owner's inspection command):

   ```bash
   godot --path Characters/tahmures/prototypes/godot-front-view-character-poc-01
   ```

4. Open the editor UI:

   ```bash
   godot --editor --path Characters/tahmures/prototypes/godot-front-view-character-poc-01
   ```

   In the editor: open `scenes/main.tscn`, press **F6** to run the
   current scene or **F5** to run the configured main scene, watch the
   beats, then press Stop. The timeline auto-loops every 18 seconds;
   press **R** at any time to replay it immediately.

## What you should see (18 s, loops)

| Time | Beat |
| --- | --- |
| 0.0–2.5 | neutral idle (temporary torso breathes gently; approved head static) |
| 2.5–2.85 | blink (approved closed-eyelid state) |
| 5.0–8.0 | thinking (approved brow state: 1 px raise + underlay) |
| 9.0–9.8 | pointing beat: temporary arm raises toward the mark |
| 9.8–10.4 | gold mark fades in |
| 10.8–12.2 | approved small-open mouth state (**not speech**) while pointing |
| 13.0–14.0 | arm returns, mark fades out |
| 14.0–18.0 | neutral idle, then the timeline loops |

The HUD (screen-space) stays in its own zones and never crosses the
character: the header and language line sit in the top strip; the
compact state label (`IDLE` / `BLINK` / `THINKING` / `POINT` /
`POINT + OPEN TEST` / `RETURN`), time readout, hint line, and progress
bar with tick labels sit in a bottom-left control column; and two
world-space labels — one beside the torso, one at the bottom-right —
mark the torso and arm/hand as temporary placeholders. The Persian
name طهمورث is shown using a system font (Noto Naskh Arabic). Long
state explanations go to the console, not the screen.

Approximate screen zones (1280x720, layout revision 01):

| Zone | Region (x, y) | Contents |
| --- | --- | --- |
| header | top-left + top-right, y 4–102 | title, subtitle, طهمورث, language line, version |
| character | centre, x 465–775, y 46–720 | approved head + temporary body/arm/hand |
| torso callout | mid-left, x 110–430, y 448–492 | TORSO temporary-placeholder note |
| arm callout | bottom-right, x 975–1264, y 584–648 | ARM + HAND temporary-placeholder note |
| control column | bottom-left, x 16–430, y 540–700 | state label, time, hint, progress bar |
| mark label | x 1104–1240, y 402–424 | `MARK (scene prop)` during the pointing beat |

## Stage B0 audio/subtitle interface

The Stage-A scene now has an inert NarrationPlayer node (stream = null,
autoplay = false) and a validator for future owner-provided inputs. Expected
files, separately for en and fa, are:

    audio/<language>/narration.wav
    audio/<language>/narration.txt
    audio/<language>/subtitles.vtt

The WAV contract is PCM 16-bit, mono or stereo, 22.05–96 kHz, non-empty, and
no longer than the 18-second prototype timeline; mono 48 kHz is preferred.
WebVTT cue text is retained as written and cues must be ordered, non-overlapping,
and within the timeline. Missing files are reported as pending; validation
does not synthesize, rewrite, or play anything. No audio or transcript files
are currently present. The owner rejected the installed eSpeak voices, so do
not use them.

Run the focused parser/contract tests:

    godot --headless --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --script res://scripts/tests/audio_subtitle_pipeline_test.gd

The opt-in caption layout test uses clearly labelled fixture text, not an
approved narration sample:

    godot --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --write-movie Characters/tahmures/prototypes/godot-front-view-character-poc-01/renders/stage-b0/fa-caption-test.avi --fixed-fps 30 --quit-after 30 -- --language=fa --caption-test

It should be rendered with a working desktop display. Headless import and
script tests cannot establish visual glyph shaping. This test changes no
Stage-A rendering and adds no audio.

## Language hook (for the future audio stage)

The visual timeline is identical for every language. Select the future
narration/caption track with a user argument:

```bash
godot --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 -- --language=fa
godot --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 -- --language=en
```

or set `tahmures/language` in `project.godot`. The language hook selects a
future input set only. Actual playback/export and mouth-motion integration are
a later owner-gated phase; they require human-recorded WAVs, owner-confirmed
transcripts, subtitles, and an explicit mouth-motion decision.

## Silent render evidence (already produced, regenerable)

The committed render is `renders/stage-a-preview.avi` (MJPEG, 1280x720,
30 fps, 540 frames, 18.0 s). It was produced deterministically with
Godot Movie Maker:

```bash
cd Characters/tahmures/prototypes/godot-front-view-character-poc-01
godot --path . --write-movie renders/stage-a-preview.avi --fixed-fps 30 --quit-after 540
```

The AVI contains an engine-recorded **silent** stereo track (Movie
Maker captures the empty master bus; measured at the −91 dB digital
floor). It is not narration and not a speech placeholder. Six key
frames are extracted to `renders/frames/`, and
`renders/verification.json` records the pixel-level comparison of the
render against the approved state composites (see "Verification"
below). If you re-render with a different Godot build, the AVI bytes
may differ; refresh its hash in `manifest.json` and re-run
`check_integrity.py` afterwards.

## Verification commands

```bash
# re-run all static integrity checks (input hashes, scene refs,
# animation keys, placeholder labels, manifest cross-check)
python3 Characters/tahmures/prototypes/godot-front-view-character-poc-01/scripts/check_integrity.py

# re-run the render-frame verification against approved state composites
python3 Characters/tahmures/prototypes/godot-front-view-character-poc-01/scripts/verify_render.py

# inspect the render
ffprobe Characters/tahmures/prototypes/godot-front-view-character-poc-01/renders/stage-a-preview.avi
```

`check_integrity.py` must print `RESULT: ALL INTEGRITY CHECKS PASSED`
(exit 0). `verify_render.py` rewrites `renders/verification.json`
deterministically and exits non-zero if any HUD safe-layout pixel
check fails (head/diadem clearance bands, torso text-free band, state
label, placeholder callouts, mark label).

## Project layout

```
project.godot            Godot 4.7.2 project (GL Compatibility, 1280x720)
scenes/main.tscn         main scene: rig, timeline, HUD, labels
scripts/main.gd          timeline controller, HUD, replay, language hook
scripts/audio_subtitle_pipeline.gd  WAV input checks and exact-text WebVTT parser (no playback)
scripts/tests/            offline interface tests and non-approved caption fixtures
scripts/generate_temporary_body.py   deterministic placeholder-art generator
scripts/check_integrity.py           re-runnable static validation
scripts/verify_render.py             re-runnable render verification
assets/approved-head/    17 byte-exact copied approved sprites (+README)
assets/temporary-body/   temporary stand-in PNGs (+README, placeholders.json)
audio/en/README.md       expected human-recorded English WAV (stage B)
audio/fa/README.md       expected human-recorded Persian WAV (stage B)
renders/                 stage-a-preview.avi + frames/ + verification.json
manifest.json            inputs, hashes, scene/timeline identity, boundaries
validation.json          machine-readable validation record
implementation-report.md stage-A acceptance report
```

`.godot/` (git-ignored) and the `.png.import` / `main.gd.uid` files are
Godot-generated cache/import metadata.

## Scene structure and how to swap the temporary body later

- `World/Rig/Head` sits at the source-canvas centre (543, 724); every
  approved sprite is an unrotated, unscaled child at local (0, 0), so
  world coordinates equal the original 1086x1448 canvas coordinates.
  The camera (560, 330, zoom 1.0) maps them to the screen as
  `screen = world + (80, 30)` — pixel-exact.
- Draw order is the tree order and reproduces the approved render
  groups exactly (see `assets/approved-head/README.md`).
- The pointing arm is a 3-joint chain (`ShoulderL` → `ElbowL` →
  `HandL`) animated by rotation keys only. To replace the stand-ins
  with approved art later, swap the textures and keep the pivots
  documented in `assets/temporary-body/README.md` and `manifest.json`.
- The temporary torso breathes (1.2% scale, 3 s period) around its neck
  anchor; the approved head is never scaled, rotated, or repainted.

## Approval boundaries (from the human approval record)

Approved for continued prototype use: the reviewed front-view
facial-state head components and states. Not approved: permanent
body/arm/hand art, new expressions, visemes/lip-sync claims, voice,
final video, or publication. Stage B (voice integration, audio-driven
mouth switch, bilingual exports) requires the owner's voice input
decision first.
