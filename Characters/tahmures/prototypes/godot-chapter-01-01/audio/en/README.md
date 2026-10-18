# Narration audio contract — en (PENDING)

Status: **NO_OWNER_AUDIO** — this chapter candidate plays as a *silent animatic*.
The audio track in rendered previews is engine silence, NOT narration.

## What is needed for a later narrated export

| File | Contract |
|---|---|
| audio/en/narration.wav | Owner-recorded narration, PCM 16-bit WAV, mono preferred, 48 kHz (22.05–96 kHz accepted), duration **≤ 173.0 s** (the chapter timeline — NOT the 18 s POC limit) |
| audio/en/narration.txt | Verbatim transcript, one line per cue, cue order |
| audio/en/subtitles.vtt | Per-cue timing (optional; the cue plan drives captions) |

The director auto-attaches audio/en/narration.wav when present and keeps it
glued to the master clock. No TTS, no eSpeak (rejected), no cloud voices.
Mouth stays neutral for spoken cues unless --mouth-proxy=open_test is set
explicitly; that two-state proxy is NOT lip-sync.
