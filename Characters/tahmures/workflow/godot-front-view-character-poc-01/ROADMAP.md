# Godot front-view character proof — roadmap

## Current state

Godot 4.7.2, FFmpeg 6.1.1, and eSpeak NG 1.51 are installed. Stage A's
18-second visual rig and bounded HUD correction passed GPT-Codex review:
29/29 project integrity checks and all 8 rendered HUD checks pass, and the six
sampled frames were visually inspected. The preview remains silent. The owner
auditioned and rejected both eSpeak voices. Stage B0 audio/subtitle interface
passed Codex validation and Claude's final check, including a genuine Persian
caption frame. Stage B1 waits for paired recordings, exact transcripts, and a
mouth-motion choice.

**Execution model update (owner instruction, 2026-10-10):** GLM has reached
its usage limit. GPT-Codex now implements bounded phases directly and performs
the technical checks; Claude receives a read-only final-check prompt near the
phase boundary. Human approval remains required for voice quality,
pronunciation, and subjective art decisions. This supersedes the earlier GLM
primary-implementer wording below.

## The work in short

| Step | GPT-Codex does | You do | Claude does |
| --- | --- | --- | --- |
| 1. Project bootstrap | Create the project and run import/main-scene smoke tests. | Open the visible editor and confirm the project opens. | Check final evidence read-only when requested. |
| 2. Head assembly | Copy verified approved facial assets and build the front-view scene. | Inspect the result in the editor. | Check hashes, layer use, and continuity near the phase boundary. |
| 3. Acting beats | Add deterministic blink/thinking/temporary pointing motion. | Judge motion and visual preferences. | Check timing and temporary-art boundaries in the final review. |
| 4. Voice input | Integrate only owner-provided EN/FA recordings and exact transcripts after permission; never use eSpeak. | Record paired lines and decide whether the open-test mouth may serve as a simple speech proxy. | Check technical boundaries after implementation. |
| 5. Two renders | Render both languages from the same timeline after prerequisites are met. | Listen/watch and approve or reject narration and art. | Perform the read-only final check; do not implement corrections. |

GPT-Codex implements and validates each bounded step. Claude performs the
read-only near-final check from a saved prompt; it does not implement changes.
The human owns subjective character and voice decisions.

## Step 1 — make a real Godot project

GLM created this project tree:

    Characters/tahmures/prototypes/godot-front-view-character-poc-01/
    ├── project.godot
    ├── scenes/main.tscn
    ├── scripts/
    ├── assets/
    ├── audio/en/
    ├── audio/fa/
    ├── renders/
    └── README.md

The project pins/records Godot 4.7.2, uses the GL Compatibility 2D renderer,
defines the main scene, imports the approved head assets, and passes headless
main-scene smoke tests. GPT has accepted the bounded HUD/layout correction.
Stage B0 is being implemented by GPT-Codex without voice files. It must not
create final character art or modify the approved facial-state package.

**Your visible check after GLM submits:**

    godot --editor --path Characters/tahmures/prototypes/godot-front-view-character-poc-01

The editor window should open with the project. Open scenes/main.tscn and
press **F6** to run it. Press **F5** to run the main project scene. The two
headless commands are for smoke testing; they do not display the scene.

## Step 2 — assemble the approved face

GLM verifies the human-approved facial-state manifest and file index before
copying assets. It uses the approved front-view head, eyelids, brow state, and
mouth states without repainting or modifying their source files. It creates a
clear Godot node/layer structure and documents sprite pivots and draw order.

**Your check:** the face should be recognizable and aligned; the neutral and
small-open mouths should be the approved states. Report appearance concerns
with a screenshot and a short description. Do not edit the approved source
package directly.

## Step 3 — add motion and temporary pointing

GLM creates one deterministic 15–20 second timeline:

1. neutral idle and one natural blink;
2. thinking beat using the approved brow state;
3. pointing beat with clearly labeled temporary torso/arm/hand shapes;
4. return to neutral.

The front-view art has no approved body or arm. GLM must not stretch the face
to fake body parts or describe placeholder shapes as extracted sprites. It
records key timings, easing, and the identical event timeline used in both
language renders.

**Your check:** run the scene visibly, watch it at normal speed, and decide
whether blink, thought, and point are readable. This is a prototype preview,
not final animation or character-art approval.

## Step 4 — provide narration inputs

Do not use the rejected eSpeak voices for the deliverable. The quickest
zero-cost path to natural short speech is a human-recorded English line and a
human-recorded Persian line, saved as WAV. Keep the wording semantically
matched and check the spoken names Tahmures and طهمورث by listening. A
phone recording is sufficient for a pipeline prototype if the room is quiet
and the words are clear.

Suggested short matched lines:

- EN: “Tahmures paused, considered the question, and pointed to the mark.”
- FA: «طهمورث مکث کرد، به پرسش اندیشید و به نشانه اشاره کرد.»

Record WAV if the phone supports it. If it records M4A, convert locally:

    ffmpeg -i recording.m4a -ar 48000 -ac 1 -c:a pcm_s16le narration.wav

Put the selected files at:

    audio/en/narration.wav
    audio/fa/narration.wav

Do not retry the rejected eSpeak voices. Stage B0 builds the input/subtitle
plumbing without speech files. Stage B1 requires paired recordings and exact
owner-confirmed transcripts before it integrates or exports narration. This
workflow does not authorize synthetic speech, cloud TTS, or paid services. Any
local-voice audition requires a separate owner request.

## Step 5 — integrate audio and export

After both WAVs and transcripts exist, GLM integrates them and creates the
paired exports. The open-test mouth is not automatically a speaking pose. Use
the neutral mouth unless the owner explicitly authorizes the existing
open-test sprite as a simple two-state speech-motion proxy. If authorized,
GLM must label it **audio-driven two-state mouth motion**, not phoneme-accurate
lip-sync. No new mouth artwork is authorized.

The language selector changes only voice and captions; character action and
timing stay identical. GLM renders both versions with Godot Movie Maker or a
documented deterministic frame-plus-audio route, then probes both outputs with
ffprobe. Target: 15–20 seconds with intelligible speech, aligned captions,
and a real audio stream in each file. eSpeak output may not be substituted to
make the gate green.

## Exact commands, and when to use them

The project directory and `project.godot` exist. The smoke commands work from
the repository root. The corrected layout is ready for the owner's continued
visual inspection.

1. Import resources and parse the editor project:

       godot --headless --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --import

   The command from your earlier prompt also works as an editor smoke test:

       godot --headless --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --editor --quit

2. Run the main scene for two iterations and exit:

       godot --headless --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --quit-after 2

3. Open the GUI editor and visually inspect:

       godot --editor --path Characters/tahmures/prototypes/godot-front-view-character-poc-01

4. Run the project visibly without opening the editor:

       godot --path Characters/tahmures/prototypes/godot-front-view-character-poc-01

Godot requires --path to contain a project.godot file. --import imports
resources and quits; --quit-after 2 runs only two engine iterations. For
movie generation, Godot 4.7 supports offline Movie Maker via --write-movie,
but use it only after the visible scene and actual audio inputs work. See the
[Godot CLI guide](https://docs.godotengine.org/en/4.7/tutorials/editor/command_line_tutorial.html)
and [movie-making guide](https://docs.godotengine.org/en/4.7/tutorials/animation/creating_movies.html).

## Gate order and what a pass means

1. **Project and visual rig:** implemented; import and run
   checks, and creates a silent proof render.
2. **GPT validation:** Stage-A layout accepted; 29/29 integrity and 8/8 HUD
   checks pass, and the sampled frames are clear.
3. **Owner preview:** optionally run the accepted 18-second scene and judge
   prototype motion and temporary body stand-ins.
4. **Stage B0 (GPT-Codex):** implement and test replaceable audio-input and subtitle
   plumbing with no voice files, no speech motion, and no narrated exports.
5. **GPT-Codex technical validation:** verify scaffolding and preservation of
   the accepted Stage-A render; prepare a read-only Claude final-check prompt.
6. **Claude final check:** independently inspect evidence and report blockers;
   Claude does not edit implementation files.
7. **Owner voice inputs:** provide paired human-recorded WAVs and exact EN/FA
   transcripts; decide whether the existing small-open test may serve as a
   simple speech-motion proxy.
8. **Stage B1 (GPT-Codex):** integrate the real inputs and make two reproducible
   exports; no input means no audio integration.
9. **GPT-Codex technical validation and Claude read-only final check:** inspect
   hashes, clips, timing, captions, audio streams, and identical scene timelines.
10. **Owner listening/visual approval:** judge voice quality, pronunciation,
   captions, and prototype motion before any later production phase.

Passing a headless test means only that Godot can import/run the project. It
does not mean the art looks good, the voice sounds natural, or the character is
approved for production.
