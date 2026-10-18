# Claude independent final check — Stage B0 audio/subtitle interface

Date: 2026-10-10  
Phase: `GODOT_FRONT_VIEW_CHARACTER_POC_01_STAGE_B0_AUDIO_INTERFACE`  
Mode: `VERIFY_IMPLEMENTATION_AND_VISUAL_EVIDENCE`  
Role: independent checker; no implementation repairs

## Gate summary

| Gate | Result |
| --- | --- |
| Existing focused tests | PASS — 22 passed, 0 failed |
| Project integrity and manifest bindings | PASS — all 32 checks passed; 77 project file bindings match |
| Accepted Stage-A AVI and six key frames | PASS — byte-identical to pinned hashes |
| Inert audio / no narration / no speech-motion boundary | PASS |
| Complete input-validator correctness | REVISION REQUIRED — two concrete validation defects below |
| Genuine Godot Persian frame inspection | NOT COMPLETED — no rendered frame inspected; no visual acceptance |
| Human wording, voice, pronunciation, subjective visuals | NOT APPROVED by this check; owner authority unchanged |

Full Stage-B0 acceptance is withheld. Passing the existing tests and integrity checker does not cover the malformed inputs identified below.

## Actual files examined

Read all six requested skill instructions through the skill loader: `.agents/skills/mehdi-context/SKILL.md`, `mehdi-media/SKILL.md`, `mehdi-bilingual/SKILL.md`, `mehdi-review/SKILL.md`, `tahmures-editorial/SKILL.md`, and `tahmures-narrative/SKILL.md`.

Under `Characters/tahmures/workflow/godot-front-view-character-poc-01/`, read:

- `phase-brief.md`
- `ROADMAP.md`
- `reports/codex/stage-b0-implementation.md`

Under `Characters/tahmures/prototypes/godot-front-view-character-poc-01/`, examined:

- `README.md`, `project.godot`, and `manifest.json` (outline and targeted contents covering timeline, boundaries, all project bindings, and B0 state)
- `scripts/audio_subtitle_pipeline.gd`
- `scripts/tests/audio_subtitle_pipeline_test.gd`
- `scripts/tests/fixtures/en-caption.vtt` and `fa-caption.vtt`
- `scripts/main.gd`
- `scripts/check_integrity.py` (pinned constants, HUD checks, and main validation logic)
- `scenes/main.tscn` (entire scene)
- `audio/en/README.md` and `audio/fa/README.md`
- `renders/stage-b0/README.md`

The checker independently hashed the approved assets, accepted AVI/frames, and manifest-listed files. An additional read-only Python check verified all four manifest bindings to the facial-state and v7 package manifests/indexes. All four match.

## Concrete implementation blockers

### B0-01 — PCM block alignment is not validated

Location: `scripts/audio_subtitle_pipeline.gd:123–153`.

The WAV parser reads format code, channels, sample rate, byte rate, and bit depth, but never reads or validates the `nBlockAlign` field at `chunk_start + 12` (absolute offset 32 in the test's standard 44-byte WAV header). PCM16 requires block alignment of `channels * 2`.

Concrete counterexample derived directly from the existing test builder: construct `_pcm16_wav(48000, 1, 4800)`, then set `encode_u16(32, 0)` (or `4`). Every checked field and the data length remains unchanged, so the current validator returns `ok: true` despite invalid mono PCM16 metadata. This conclusion is from source inspection, not a separately executed adversarial test.

Required bounded correction: reject inconsistent block alignment and add a focused regression test. No voice/art changes are needed.

### B0-02 — malformed WebVTT signatures are accepted

Location: `scripts/audio_subtitle_pipeline.gd:170–176`.

The header test uses only `begins_with("WEBVTT")`. Consequently, the invalid source below passes the current header check and proceeds to a valid cue:

```text
WEBVTTgarbage

00:00.000 --> 00:01.000
text
```

WebVTT requires the signature to end or be followed by permitted whitespace/header text, not an arbitrary suffix. The parser also does not require the header/cue separator: `WEBVTT\n00:00.000 --> 00:01.000\ntext\n` is accepted by the current control flow. These are source-derived counterexamples, not newly executed tests.

Required bounded correction: validate the signature boundary and required header separation; add regression coverage. A deliberately limited cue parser need not implement every optional WebVTT feature, but it must not classify these malformed inputs as valid.

## Input contracts and focused tests

The helper correctly separates unsupported language (`unsupported_language`), missing inputs (`pending` with all missing paths), invalid WAV (`invalid_audio`), empty transcript (`invalid_transcript`), and invalid captions (`invalid_captions`). Missing-file detection takes precedence when any member of the input set is absent. It opens WAV files read-only and has no input-writing or playback path.

WAV checks cover RIFF/WAVE signatures, declared chunk bounds, required format/data chunks, PCM encoding, channel count, sample-rate range, PCM16 depth, byte rate, aligned nonempty data, and the 18-second duration ceiling. These checks are useful but incomplete because of B0-01.

Cue payloads retain their text, spaces, punctuation, Persian characters, and multiline structure; CRLF/CR line endings are normalized to LF. Cues require positive duration and reject overlap/out-of-order timing. `inspect_language_inputs()` rejects ends beyond 18 seconds; `parse_webvtt()` alone does not apply that ceiling. Validation does not establish transcript-to-cue identity or listening approval.

The executed tests exercise valid in-memory PCM16 WAV, duration calculation, truncated WAV, unsupported sample rate/channel count/encoding, overlong WAV, unsupported language, three missing inputs, exact Persian cue text, timing, optional cue identifier, missing header, zero-duration cue, overlap, missing cue text, and malformed timing. They do not cover block alignment, malformed signature suffixes, required header separation, or the complete on-disk ready/invalid input-set paths. Thus 22/22 is accurately reported, but not comprehensive validation acceptance.

## Stage-A preservation and audio boundary

`NarrationPlayer` is genuinely inert: `stream = null`, `autoplay = false` in the scene and explicitly reset in `_ready()`. No script loads an audio stream or calls this player's playback method. Animation tracks are value tracks; no audio/method playback track is present.

The audio directory contains only the two README files. Across the project outside `.godot`, the WAV/TXT/VTT inventory contains only the two test WebVTT fixtures. No owner WAV, transcript, or owner subtitles exist. There is no eSpeak invocation or synthetic-voice fallback in the runtime helper/controller/tests examined. Both rejected voices remain excluded.

Normal mode keeps the established HUD and AnimationPlayer timeline; B0 adds input diagnostics and the inert player. The caption layer is created only when the explicit user argument `--caption-test` is present. The approved head uses the 17 hash-matching source assets without new head transforms or artwork. Blink remains 2.5–2.85 s; thinking remains 5–8 s with a 1-source-pixel brow shift; the scheduled small-open test remains 10.8–12.2 s and is not speech or lip-sync. Temporary pointing/body boundaries remain documented and labeled.

The accepted AVI hash remains:

`91bcb60405d0b3a85a0537cf01430962dc218807d4bb40aa82dacc4b25ed8b87`

All six key-frame hashes match the pins in `scripts/check_integrity.py`. `ffprobe` independently confirms MJPEG 1280×720, 30 fps, 540 frames, 18 seconds, with the existing PCM16 48 kHz stereo track. This check did not listen to or re-measure silence; byte identity preserves the accepted artifact. The current scene/timeline inspection supports preservation, but no historical code diff is available: Git reports the entire `Characters/` tree as untracked.

## Caption mode and visual evidence

Caption mode reads only the fixture map under `scripts/tests/fixtures/`, not owner subtitle slots. The fixtures themselves contain sample cues without a textual approval warning inside the VTT; their test-directory provenance, documentation, runtime log, and displayed `RTL / SUBTITLE LAYOUT TEST — NOT OWNER-APPROVED NARRATION` notice identify them as unapproved test material.

Persian caption code explicitly sets both `TEXT_DIRECTION_RTL` and `LAYOUT_DIRECTION_RTL` and uses the intended font list: Noto Naskh Arabic, Noto Kufi Arabic, Vazirmatn, FreeSerif, DejaVu Sans. The test displays the first cue statically; it does not implement timed subtitle playback. These are source-level findings, not visual proof.

Unlike the Codex environment described in its report, this review environment has `DISPLAY=:0`, `WAYLAND_DISPLAY=wayland-0`, and both display sockets. A non-headless Godot caption-mode launch succeeded with OpenGL 4.6 / Mesa 25.2.8 / Intel Iris Xe and a 1280×720 viewport. The DRI_PRIME warning fell back to GPU 0 and did not prevent execution. Therefore the previous no-display limitation does not describe this environment.

**No actual Godot frame was extracted or inspected.** The task simultaneously requests Movie Maker output/frame extraction and restricts writes to this report alone. The specified movie and an extracted image would violate that exclusive write allowance; the reviewer did not create them. The non-headless two-iteration launch establishes a functioning backend, not Persian visual acceptance. `renders/stage-b0/` still contains only its README. Shaping, visual/logical RTL order, punctuation placement, safe margins, readability, face visibility, and actual visibility of the notice remain unverified. No browser mockup or headless control-tree result was substituted. A narrowly authorized render/frame evidence run is still needed; no backend failure is claimed.

## Commands and observed results

Commands ran from the repository root:

```sh
git --no-optional-locks status --short
git --no-pager diff --check
printenv DISPLAY WAYLAND_DISPLAY
command -v godot
command -v Xvfb
command -v ffmpeg
godot --headless --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --script res://scripts/tests/audio_subtitle_pipeline_test.gd
python3 Characters/tahmures/prototypes/godot-front-view-character-poc-01/scripts/check_integrity.py
godot --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --quit-after 2 -- --language=fa --caption-test
godot --headless --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --quit-after 2
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,duration,nb_frames,sample_rate,channels -of json Characters/tahmures/prototypes/godot-front-view-character-poc-01/renders/stage-a-preview.avi
```

Focused tests: exit 0, 22 passed / 0 failed. Integrity: exit 0, `RESULT: ALL INTEGRITY CHECKS PASSED`. Normal headless and actual non-headless Persian caption launches: exit 0. The headless viewport was 64×64, underscoring why that smoke is not visual evidence. Additional read-only Python commands inspected display-socket existence, inventoried audio and Stage-B0 render files, and hashed the four approved-source manifest/index bindings; results are recorded above.

`git diff --check` emitted no output on both runs. Important limitation: `git status --short` reports `?? Characters/` and an unrelated `?? li*3`; the whitespace check does not inspect this untracked implementation tree. It is not evidence of a clean tracked Stage-B0 patch. Unrelated files were left untouched.

No formatter, repair, narration synthesis/playback, approved-media modification, commit, or push was performed. The only intentional persistent file written is this report. The integrity checker regenerates temporary body files in an automatically cleaned system temporary directory, as part of its prescribed read-only validation; it does not rewrite project assets. Godot may maintain ignored runtime caches. The full repository `make check` was not rerun: this is a bounded independent review, not implementation work, and its documentation builds write outputs beyond the permitted report. The Codex full-suite result remains reported evidence, not an independently reproduced result here.

## Owner gate and disposition

Stage B1 remains gated on paired owner-provided human recordings, verbatim owner-confirmed EN/FA transcripts and subtitles, owner listening/pronunciation approval, and an explicit mouth-motion-proxy choice. This report approves none of those decisions and authorizes no speech animation, lip-sync, voice generation, or exports.

The concrete implementation blockers are B0-01 and B0-02. Separately, genuine Persian rendered-frame inspection remains outstanding and requires resolving the render-write permission conflict. Implementation revisions and subsequent visual evidence must be reviewed before full B0 acceptance; no character-art or voice decision needs reopening.

GODOT_STAGE_B0_REVISION_REQUIRED
