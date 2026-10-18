# GLM execution prompt — GODOT_FRONT_VIEW_CHARACTER_POC_01, stage A

MODE = IMPLEMENT_AND_VERIFY

PHASE = GODOT_FRONT_VIEW_CHARACTER_POC_01
STAGE = PROJECT_BOOTSTRAP_AND_VISUAL_RIG

GLM is the primary implementer and self-tester. GPT-Codex independently
validates submitted files and evidence, then gives only bounded corrections.
The owner inspects the visible preview and owns subjective visual/audio
decisions. Claude is not part of routine implementation or correction.

This stage creates the real Godot project and a testable visual character
prototype. It deliberately does not generate narration or claim lip-sync:
the owner auditioned the installed English and Persian eSpeak voices and
rejected both as too poor. Do not use them for deliverable audio.

## 1. Read the live context

Read:

- .agents/tahmures-media-editor-llm-context.md
- .agents/tahmures-media-production-roadmap.md
- .agents/skills/mehdi-director/SKILL.md
- .agents/skills/mehdi-context/SKILL.md
- .agents/skills/mehdi-media/SKILL.md
- .agents/skills/mehdi-bilingual/SKILL.md
- .agents/skills/mehdi-review/SKILL.md
- .agents/skills/tahmures-editorial/SKILL.md
- .agents/skills/tahmures-narrative/SKILL.md
- Characters/tahmures/workflow/README.md
- Characters/tahmures/workflow/phase-status.json
- Characters/tahmures/workflow/godot-front-view-character-poc-01/ROADMAP.md
- Characters/tahmures/workflow/godot-front-view-character-poc-01/phase-brief.md
- Characters/tahmures/workflow/godot-front-view-character-poc-01/GODOT_INSTALL.md
- Characters/tahmures/workflow/godot-front-view-character-poc-01/toolchain-preflight.json

Use the accepted media continuity and Chapter 01 blueprint only when needed.
Do not modify either.

## 2. Current workstation and preflight

The owner has installed Godot, FFmpeg, and eSpeak NG. The observed versions are
Godot 4.7.2.stable.official.ed1daf0bf, FFmpeg 6.1.1-3ubuntu5, and eSpeak NG
1.51. Verify the live versions with:

    godot --version
    ffmpeg -version
    ffprobe -version

The two eSpeak voices were rejected by the owner. Do not regenerate them,
substitute them as narration, or spend time trying voice parameters. Do not use
cloud TTS, external model endpoints, paid services, or voice cloning. The later
voice stage will use owner-provided recordings or a separately authorized,
bounded local-voice audition.

The target project directory does not exist at task entry. Create it only if
the path remains absent. If it already exists, stop without overwriting it and
report its path and current identity so Codex can assign a new version path.

## 3. Approved input and protected source

Use the facial-state prototype only after confirming its pinned files:

- Characters/tahmures/prototypes/layout01-facial-states-01/manifest.json
  SHA-256 b081e9190f5ddf1e8eff643863b1bbee5ab7b4a176179a26703b1c4ad32e4ba4
- Characters/tahmures/prototypes/layout01-facial-states-01/files-sha256.json
  SHA-256 6135d7b65239919ebb2834913aa20b93d391d16d40f2a35c4a499e337b1cea21
- Human approval:
  Characters/tahmures/workflow/approvals/layout01-facial-states-01-human-approval.json

Verify both hashes and the referenced file digests before copying inputs.
Copy the approved components into the new project and record origin paths and
hashes. Do not edit the approved package, v7 source, approval evidence, book
chapters, blueprints, continuity, registry, glossary, source hashes, review
status, or shared tooling. New Persian media uses طهمورث.

The approval covers the reviewed front-view facial-state prototype for
continued prototyping. It does not approve a permanent body, arm, hand,
pointing pose, new expression art, voice, or finished character design.

## 4. Stage-A objective

Create a real Godot 4.7.2 GDScript project at:

    Characters/tahmures/prototypes/godot-front-view-character-poc-01/

Build a visible 15–20 second deterministic front-view character preview that
exercises the approved head components and a temporary pointing beat. This is
a pipeline/rig prototype, not the final video.

Include at minimum:

- project.godot;
- a configured main scene and scripts;
- copied, hash-recorded approved head/facial components;
- neutral, approved blink, approved thinking brow, and approved small-open
  mouth states;
- one short, deterministic timeline showing idle, blink, think, point, and
  return to neutral;
- clearly labeled temporary torso/arm/hand stand-ins for the pointing action;
- a simple scene background and readable timing/state markers;
- an obvious way to replay the timeline in the editor;
- project README with the exact commands in section 8;
- an implementation report and machine-readable validation report.

Do not invent a new face, body design, or permanent expression. Do not call the
temporarily scheduled open-mouth pose speech or lip-sync. This stage must work
without audio files.

Use a simple deterministic 2D scene and the least complex Godot nodes that
preserve alignment and editability. Prefer AnimationPlayer/AnimationLibrary
or a clearly explained equivalent. Record pivots, parent-child relationships,
z-order, timing, and how to replace temporary body/arm layers later.

## 5. Temporary-body policy and art limits

There is no approved Tahmures body or arm art in the input package. If needed
for the point gesture, create simple flat vector shapes or labeled cutouts.
Mark every such file and in-scene label TEMPORARY PROTOTYPE PLACEHOLDER —
NOT APPROVED CHARACTER ART. Do not add placeholders to the canonical registry
or represent them as extracted source pixels.

Do not use AI image generation, local image generation, or a full-head redraw.
Do not modify any input artwork. Preserve the approved face/eye/brow/mouth
identity and state geometry exactly. Record any scaling or transforms used by
the scene.

## 6. Project behavior and repeatability

The scene should have one repeatable timeline, 15–20 seconds long, driven by
the project itself rather than by manual timing. The same future event timeline
will be reused for English and Persian. Add a debug control or timeline marker
that lets the owner identify the current state; it must not obscure the
character.

If practical, implement a small scene-level language argument/config hook so a
future audio stage can select English or Persian without altering the visual
timeline. Do not add fake, silent, synthesized, or placeholder speech files.
Create audio/en/README.md and audio/fa/README.md describing the expected
human-recorded WAV inputs instead.

Do not perform the later audio integration, envelope extraction, subtitle
timing, mouth/audio synchronization, final two-language movie export, or
character-art approval in this stage. Document these as the next stage.

## 7. Deliverables

Create only under the new project directory:

    project.godot
    scenes/main.tscn
    scripts/
    assets/approved-head/
    assets/temporary-body/
    audio/en/README.md
    audio/fa/README.md
    renders/ or preview/
    README.md
    manifest.json
    validation.json
    implementation-report.md

Include an actual silent preview render or frame sequence if Godot's local
Movie Maker or a deterministic project-local route allows it. A render is
useful evidence but not mandatory if the visible project runs and the report
explains the exact way the owner can inspect it. Never claim a render exists
unless it exists and was inspected.

The manifest records input file hashes, Godot version, scene/timeline IDs,
temporary asset status, dimensions, layer order, generated file hashes, and
approval boundaries.

## 8. Validate and give the owner usable commands

From the repository root, execute and record exit status and relevant output:

    godot --headless --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --import

    godot --headless --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --quit-after 2

Then run the project visibly if the environment supports a display:

    godot --path Characters/tahmures/prototypes/godot-front-view-character-poc-01

The first two commands are smoke tests only. The visible command is the owner’s
way to watch the preview. For the editor UI, the owner will use:

    godot --editor --path Characters/tahmures/prototypes/godot-front-view-character-poc-01

In the editor, open scenes/main.tscn, press F6 to run the current scene or F5
to run the configured main scene, and press Stop to return. If the machine has
no graphical display, do not claim visual testing; provide the exact owner
command and captured headless evidence.

Do not use --headless for the owner's visual inspection. The project path
must contain project.godot. Do not install packages into the book venv.

Run focused checks for input hashes, referenced asset paths, scene/main-scene
configuration, animation events, placeholder labels, output hashes, and
git diff --check. Do not run the full book gate for a prototype-only change.

## 9. Stage-A acceptance report

In implementation-report.md and your final response, explicitly report:

- Godot/FFmpeg versions and command results;
- approved source hash verification;
- project and main scene paths;
- exact animation events and durations;
- which approved input components are actually used;
- which body parts are temporary placeholders;
- whether visible GUI inspection was possible;
- whether an actual silent render/frame sequence exists;
- all test commands, exit codes, and observed errors;
- confirmation that eSpeak was not used for narration;
- next owner action and the voice-stage prerequisite.

Use PASS / FAIL / BLOCKED for:

    GODOT_PROJECT_IMPORTS?
    MAIN_SCENE_RUNS?
    APPROVED_INPUT_HASHES_MATCH?
    APPROVED_FACE_STATES_USED_WITHOUT_MODIFICATION?
    BLINK_AND_THINKING_VISIBLE?
    TEMPORARY_POINTING_BEAT_VISIBLE?
    TIMELINE_IS_REPEATABLE?
    AUDIO_NOT_FAKED_OR_MISREPRESENTED?
    NO_PROTECTED_SOURCE_CHANGED?
    git_diff_check_clean?

Stage A may be technically ready for GPT even though voice selection and
exports remain pending. Do not describe the complete 15–20 second bilingual
video proof as complete.

## 10. Return token

Finish with exactly one:

GODOT_FRONT_VIEW_CHARACTER_POC_01_VISUAL_STAGE_READY_FOR_GPT

GODOT_FRONT_VIEW_CHARACTER_POC_01_VISUAL_STAGE_REVISION_REQUIRED

GODOT_FRONT_VIEW_CHARACTER_POC_01_TOOLING_BLOCKED

GODOT_FRONT_VIEW_CHARACTER_POC_01_OWNER_INPUT_REQUIRED

Do not commit, publish, approve new art, modify source/manuscripts, or begin
the audio/export stage.

