# Claude independent final check 02 — Stage B0

Date: 2026-10-10  
Phase: `GODOT_FRONT_VIEW_CHARACTER_POC_01_STAGE_B0_AUDIO_INTERFACE`  
Mode: `VERIFY_IMPLEMENTATION_AND_VISUAL_EVIDENCE`  
Role: independent checker; no implementation repairs

## Gate summary

| Gate | Result |
| --- | --- |
| Bounded audio/subtitle implementation | PASS |
| First-check PCM block-alignment counterexamples | RESOLVED — rejected, with executed regression coverage |
| First-check WebVTT signature/separator counterexamples | RESOLVED — rejected, with executed regression coverage |
| Focused tests | PASS — 30 passed, 0 failed |
| Integrity before and after rendering | PASS — all 32 checks; all 77 project file bindings match |
| Accepted Stage-A AVI and six frames | PASS — pinned hashes preserved |
| Genuine Godot Persian fixture visual evidence | PASS for the inspected frame/backend; AVI and extracted PNG retained |
| Human voice, wording, pronunciation, subjective visual approval | NOT APPROVED by this check; owner authority unchanged |

No concrete blocker remains for this bounded B0 interface stage. Acceptance is for receiving owner inputs, not Stage B1 integration, narration playback, speech animation, final art, publication, or release.

## Actual review inputs

Read the six requested skill instructions: `.agents/skills/mehdi-context/SKILL.md`, `.agents/skills/mehdi-media/SKILL.md`, `.agents/skills/mehdi-bilingual/SKILL.md`, `.agents/skills/mehdi-review/SKILL.md`, `.agents/skills/tahmures-editorial/SKILL.md`, and `.agents/skills/tahmures-narrative/SKILL.md`.

Under `Characters/tahmures/workflow/godot-front-view-character-poc-01/`, examined `phase-brief.md`, `ROADMAP.md`, `reports/codex/stage-b0-implementation.md`, and the first Claude findings in `reports/claude/stage-b0-final-check.md`.

Under the live project, `Characters/tahmures/prototypes/godot-front-view-character-poc-01/`, examined:

- `README.md` and relevant `manifest.json` contents, including approved inputs, project hash bindings, boundaries, and B0 state;
- complete `scripts/audio_subtitle_pipeline.gd` and `scripts/tests/audio_subtitle_pipeline_test.gd`;
- `scripts/tests/fixtures/en-caption.vtt` and `fa-caption.vtt`;
- complete `scripts/main.gd` and `scenes/main.tscn`;
- `scripts/check_integrity.py` constants and validation logic;
- `renders/stage-b0/README.md` and the audio-directory inventory.

The findings below are based on live files, executed commands, and an actual extracted Godot frame, not solely the implementation report.

## Input contracts and regression fixes

The helper distinguishes unsupported language (`unsupported_language`), missing input sets (`pending`, listing missing paths), invalid WAV metadata (`invalid_audio`), empty transcript (`invalid_transcript`), and invalid captions (`invalid_captions`). Missing-file detection takes precedence when any required input is absent. File access is read-only; the helper has no input-rewriting, synthesis, stream-loading, or playback path.

PCM validation checks RIFF/WAVE structure, chunk bounds, required format/data chunks, PCM encoding, mono/stereo channels, supported sample rate, PCM16 depth, byte rate, nonempty frame-aligned data, and duration. The bounded repair now reads `nBlockAlign` at `chunk_start + 12`, requires it to equal channels times bytes per sample, and checks byte rate against sample rate times block alignment. Invalid mono PCM16 alignment values 0 and 4 are explicitly tested and rejected; valid stereo and inconsistent byte-rate cases are covered. This resolves B0-01 from the first report.

The WebVTT signature must now be exactly `WEBVTT` or have a permitted space/tab boundary; an optional BOM is handled. The parser requires a blank header/cue separator and rejects cue timing encountered before it. Executed tests reject `WEBVTTgarbage` and missing header separation and accept the valid metadata-header/BOM cases. This resolves B0-02 from the first report.

Cue wording, Persian characters, punctuation, spaces, and multiline payloads are retained; line endings are normalized to LF. Cues require positive duration, ordered timing, and no overlap. The 18-second ceiling is applied by `inspect_language_inputs()`; the standalone parser does not itself enforce that project ceiling. This is a bounded subtitle parser, not a claim of complete WebVTT feature support, transcript/caption semantic equivalence, or listening approval.

The focused suite ran twice with **30 passed, 0 failed**, exit 0. It covers valid/invalid in-memory WAVs, missing inputs, unsupported language, exact Persian text, malformed timing, zero-duration and overlapping cues, block alignment, signature boundaries, and header separation. It does not establish complete on-disk ready/invalid input-set integration or correctness for every possible malformed file. Those limits do not reopen the resolved counterexamples.

## Inert audio and Stage-A preservation

`NarrationPlayer` has `stream = null` and `autoplay = false` in the scene and is reset to those values in `_ready()`. No controller/helper playback call or audio-stream loading path exists. Animation tracks are value tracks, not audio or method-call playback tracks. Installed eSpeak voices remain excluded: there is no runtime invocation or synthesized fallback, and the manifest explicitly records owner rejection.

Both `audio/en/` and `audio/fa/` contain only README files. The project WAV/TXT/VTT inventory contains only the two test VTT fixtures. No owner WAV, transcript, or subtitle files were added.

Normal execution retains the Stage-A HUD and animation path, apart from nonvisual input diagnostics and the inert node. Caption test mode is false by default and requires the explicit `--caption-test` user argument. The approved 18-second loop and 11 beats remain intact: blink 2.5–2.85 seconds; thinking 5–8 seconds with exactly one source-pixel brow movement; small-open mouth test 10.8–12.2 seconds; temporary pointing/return sequence unchanged. The mouth test remains explicitly **not speech**. All 17 approved head assets match their source hashes; the scene retains the approved alignment and state swaps without new art or head transforms.

Integrity passed before rendering and again after the evidence render/extraction: **all 32 checks**, all **77 manifest-listed files** matching, and project-tree completeness passing. The accepted Stage-A AVI still hashes to:

`91bcb60405d0b3a85a0537cf01430962dc218807d4bb40aa82dacc4b25ed8b87`

All six key-frame hashes match the independent pins in `scripts/check_integrity.py`. Neither the accepted AVI nor its frames were overwritten. Preservation is supported by live scene/controller inspection and hash checks, not a new full Stage-A render or a historical source diff.

All four approved-source manifest/index bindings were independently hashed and matched: facial-state manifest/index and v7 manifest/index. The v7 index is `files-sha256.json`; an initial supplemental command incorrectly requested nonexistent `index.json` and failed after confirming the first three bindings. Discovery and a corrected hash command confirmed the fourth; this was a reviewer command error, not a repository defect.

Current project manifest SHA-256:

`6497c53c14792bed9775dfa522afcffb974272ad54a11ec5b8f81364a3e7505f`

Current manifest bindings verified by the checker include:

- helper: `7079722d5a733f599c1ec75f3f8360a006b1703f8d8712fad9193a638782b2f7`;
- focused tests: `5024c6b90b78e8a894605ba6574f2f86f95721afbc338e209d08c968dcd160c3`;
- controller: `b7c083d1164ecfb314e68c4008bb4de5ccad32fa5ae7670c1c04da701c53d376`;
- scene: `ed393adc6f05382a862a0c30e59a83251a1eca55c1cf6c4426cc2b8f8efbfa51`.

The manifest still describes the implementer's recheck-pending state and its own unavailable rendering environment. This independent report supplies the later review result without modifying that metadata.

## Genuine Persian visual evidence

The prior review's evidence-write limitation is resolved by this request's explicit allowance. A real non-headless Godot Movie Maker run succeeded with Godot `4.7.2.stable.official.ed1daf0bf`, OpenGL 4.6 Core, Mesa `25.2.8-0ubuntu0.24.04.2`, and Intel Iris Xe ADL GT2. The DRI_PRIME warning fell back to GPU 0 without preventing rendering.

Evidence, outside the Godot project:

- [Godot caption-test AVI](evidence/stage-b0-fa-caption-test.avi): MJPEG, 1280×720, 30 fps, 30 frames, 1 second, confirmed by `ffprobe`. The container also has the engine's PCM audio track; no narration was supplied or played.
- [Extracted frame at 0.5 seconds](evidence/stage-b0-fa-caption-test.png): 1280×720 PNG, opened and visually inspected directly.

SHA-256:

- AVI: `e808d816f67ca0e65b6d588749afd7fa2523d7c41b035f659ebfcafc10644f72`
- PNG: `ef3d2cada3e4b0157782c2019cc6c8bcdc66a47689b1881ccd68a044dffa1aab`

The actual frame displays the fixture sentence:

> طهمورث مکث کرد، به پرسش اندیشید و به نشانه اشاره کرد.

Observed joined Persian shaping, natural visual RTL word order consistent with the logical fixture, correctly placed Persian comma and terminal full stop, and a readable centered white line without clipping. The panel has approximately 64-pixel horizontal and 29-pixel bottom margins. The head and face remain fully visible. The gold notice is readable:

`RTL / SUBTITLE LAYOUT TEST — NOT OWNER-APPROVED NARRATION`

The panel overlaps the lower temporary body/arm area; the torso warning remains visible above it, while part of the arm warning is obscured beneath it. This occurs only in explicit caption test mode and is not a face-visibility or caption-readability blocker.

The controller uses the intended fallback list (`Noto Naskh Arabic`, `Noto Kufi Arabic`, `Vazirmatn`, `FreeSerif`, `DejaVu Sans`) and explicitly sets both RTL text and layout directions. The actual selected system font was not instrumented; observed shaping is verified on this backend, not promised across all machines.

The fixtures are sourced only from the test-fixture map, not owner subtitle slots. Although the VTT payloads have no embedded approval disclaimer, their test paths, documentation, runtime marker, and visible notice distinguish them unmistakably from approved narration. This test displays the first cue statically; the one-second clip/frame does not validate timed subtitles, long/multiline wrapping, later animation beats, or every Persian glyph combination. No browser mockup, synthetic substitute, or headless control-tree result was used as visual proof. Owner approval of wording and subjective visuals remains separate.

## Commands and results

Commands executed from the repository root include:

```sh
godot --headless --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --script res://scripts/tests/audio_subtitle_pipeline_test.gd
python3 Characters/tahmures/prototypes/godot-front-view-character-poc-01/scripts/check_integrity.py
godot --headless --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --quit-after 2
git --no-pager diff --check
git --no-optional-locks status --short
```

Focused tests and integrity exit 0. Normal headless launch exits 0 and reports pending owner inputs, unchanged timeline, and no caption test marker. It is a smoke check, not visual evidence.

Actual render and extraction commands:

```sh
godot --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --write-movie /home/mehdi/Project/leela/tahmures/Characters/tahmures/workflow/godot-front-view-character-poc-01/reports/claude/evidence/stage-b0-fa-caption-test.avi --fixed-fps 30 --quit-after 30 -- --language=fa --caption-test
ffmpeg -y -ss 0.5 -i Characters/tahmures/workflow/godot-front-view-character-poc-01/reports/claude/evidence/stage-b0-fa-caption-test.avi -frames:v 1 Characters/tahmures/workflow/godot-front-view-character-poc-01/reports/claude/evidence/stage-b0-fa-caption-test.png
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,nb_frames -show_entries format=duration -of json Characters/tahmures/workflow/godot-front-view-character-poc-01/reports/claude/evidence/stage-b0-fa-caption-test.avi
```

All three exit 0. FFmpeg emitted nonblocking pixel-format and single-image filename warnings; the extracted PNG exists and was inspected. Additional read-only `find`, `sha256sum`, and Python JSON/hash commands inventoried inputs and verified bindings/evidence hashes.

`git diff --check` emitted no output. Git reports the entire `Characters/` tree as untracked (`?? Characters/`) plus unrelated `?? li*3`; therefore this command does not validate whitespace within the untracked implementation or establish a clean tracked patch. Unrelated files were untouched.

No formatter, repair, narration synthesis/playback, approved-media modification, commit, or push was performed. Intentional persistent outputs are limited to this report and the two authorized evidence artifacts. Godot may maintain ignored runtime caches. The prescribed integrity checker uses cleaned system-temporary files for placeholder regeneration without rewriting project assets. Full `make check` was not independently rerun because this is bounded read-only review and broader build workflows write outputs; implementation-report suite claims are not presented as independently reproduced here.

## Owner boundary and disposition

Technical acceptance and bounded Persian fixture visual verification pass. Human voice quality, pronunciation, transcript wording, and subjective visual approval are neither inferred nor granted.

Stage B1 still requires paired owner-provided human recordings, verbatim owner-confirmed EN/FA transcripts and subtitles, owner listening/pronunciation approval, and an explicit mouth-motion-proxy choice. No speech animation, lip-sync, voice generation, or exports are authorized. No character-art or voice decision is reopened.

GODOT_STAGE_B0_ACCEPTED_FOR_OWNER_INPUTS
