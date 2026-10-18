# Expected English narration inputs

The owner auditioned the installed English and Persian eSpeak voices and
rejected both as too poor for narration. Do not add synthesized, silent, or
placeholder speech files.

## Expected owner-provided files

    audio/en/narration.wav
    audio/en/narration.txt
    audio/en/subtitles.vtt

- Human-recorded narration; a quiet-room phone recording is acceptable for the
  pipeline prototype.
- WAV PCM 16-bit, mono or stereo, 22.05–96 kHz; mono at 48 kHz is preferred.
  A local M4A conversion example is:
  `ffmpeg -i recording.m4a -ar 48000 -ac 1 -c:a pcm_s16le narration.wav`.
- The transcript must be owner-confirmed verbatim. WebVTT cues must preserve
  its wording, be ordered, non-overlapping, and fit the 18-second prototype.
- The current validator checks metadata and cue structure only. It does not
  play audio or establish voice quality or pronunciation.

Stage B0's NarrationPlayer is inert (`stream = null`, autoplay disabled).
Actual playback/export and any speech-motion proxy require owner-provided
inputs and a separate explicit owner decision. The installed eSpeak voice is
not an authorized fallback.
