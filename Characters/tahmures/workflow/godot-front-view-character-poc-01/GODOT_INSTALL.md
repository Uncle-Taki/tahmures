# Godot setup and first-run guide — Tahmures prototype

This workstation already has Godot 4.7.2, FFmpeg, and eSpeak NG installed. No
installation step is needed. GLM has created the project and `project.godot`;
GPT-Codex has accepted its bounded HUD-layout correction. The owner can run the
preview now. Audio integration remains gated on human-recorded EN/FA narration,
exact transcripts, and the documented mouth-motion choice; eSpeak remains
rejected for narration.

## Confirm the installed tools

Run these from the repository root:

```bash
godot --version
ffmpeg -version
ffprobe -version
espeak-ng --version
```

Observed on 2026-10-09:

- Godot: `4.7.2.stable.official.ed1daf0bf`
- FFmpeg: `6.1.1-3ubuntu5`
- eSpeak NG: `1.51`

The Persian and English eSpeak voices were auditioned and rejected by the
owner for narration quality. Do not use them for the character sample or treat
their pronunciation as approved. Keep eSpeak installed only if useful for
technical smoke tests; it is not the narration solution.

## What the two headless commands mean

The target project path is:

```text
Characters/tahmures/prototypes/godot-front-view-character-poc-01/
```

Godot requires that directory to contain `project.godot`. GLM has now created
that file; `--path` does not itself create a project.

Run from the repository root:

```bash
godot --headless --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --import
```

This imports project resources and exits. The longer command you were given is
also a valid editor-import smoke test:

```bash
godot --headless --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --editor --quit
```

Then run the configured main scene briefly:

```bash
godot --headless --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 --quit-after 2
```

`--quit-after 2` means quit after two engine iterations; it checks that the
main scene starts and exits without an immediate runtime error. It does not
show you the animation, and it is not a video render. Godot documents that
`--path` must point to a directory containing `project.godot`, that `--import`
imports resources and quits, and that `--headless` is intended for non-visual
work such as servers and CI. See the [Godot command-line guide](https://docs.godotengine.org/en/4.7/tutorials/editor/command_line_tutorial.html).

## Open the project and see it

Open the editor window:

```bash
godot --editor --path Characters/tahmures/prototypes/godot-front-view-character-poc-01
```

In the editor:

1. Wait for the project import to finish.
2. Open the main scene shown in the FileSystem panel if it is not already open.
3. Press **F6** to run the current scene, or **F5** to run the project’s main
   scene.
4. Watch the blink, thinking, and pointing beats; inspect the Output and
   Debugger panels for errors.
5. Press the stop button to return to the editor.

You can also run the project visibly without opening the editor UI:

```bash
godot --path Characters/tahmures/prototypes/godot-front-view-character-poc-01
```

Use the GUI run for judging motion and appearance. A headless run cannot tell
you whether the artwork looks right.

## Exporting a test movie comes later

Do not start with movie export. First confirm the scene in the visible editor.
When the timeline and audio inputs are ready, Godot 4.7 Movie Maker can render
non-real-time video and audio. A typical 30 fps, 15 second run writes 450
frames; 20 seconds writes 600:

```bash
mkdir -p Characters/tahmures/prototypes/godot-front-view-character-poc-01/renders
godot --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 \
  --write-movie renders/english.avi --fixed-fps 30 --quit-after 450 -- --language=en
```

Run the same scene and timeline for Persian, changing only the selected voice
and subtitle track:

```bash
godot --path Characters/tahmures/prototypes/godot-front-view-character-poc-01 \
  --write-movie renders/persian.avi --fixed-fps 30 --quit-after 450 -- --language=fa
```

These are target commands for the GLM-built project; they will not work until
its scene accepts the `--language` user argument and the audio files exist.
Movie Maker records video and audio offline; Godot’s [movie creation guide](https://docs.godotengine.org/en/4.7/tutorials/animation/creating_movies.html)
documents `--write-movie`. If MP4 delivery is wanted, FFmpeg can transcode the
actual rendered AVI after checking it with `ffprobe`. Never claim a movie was
rendered from a plan or from a headless scene smoke test.

## Audio decision

The available eSpeak Persian and English voices sound too poor for this
character. Do not spend time generating another full narration with them.
Build the scene so voice files are replaceable and the same motion timeline can
be run against either language. For a natural first sample, record the paired
short lines with human speakers and save them as WAV files; keep both recordings
in the prototype’s `audio/` directory. If you later want a local neural TTS
audition, make that a separate, bounded comparison with license, installation,
runtime, and pronunciation evidence. Do not call a cloud service or buy a
service without explicit approval.

## Keep the project reproducible

- Pin the Godot version and record exact commands in the prototype README.
- Keep project assets, audio, frames, and renders inside the prototype tree.
- Do not install Godot/audio packages into the book’s Python virtualenv.
- Keep temporary torso/arm/hand artwork labeled as noncanonical placeholders.
- Do not change the approved facial-state input package or its approval.
- Do not commit or publish without separate owner instruction.
