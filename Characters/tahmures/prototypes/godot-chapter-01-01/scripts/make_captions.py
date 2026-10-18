#!/usr/bin/env python3
"""Generate candidate-local WebVTT caption files from data/chapter-cues.json.

Deterministic: identical bytes on re-run. Cue text is verbatim from the cue
plan (source dialogue verbatim from the live tales; narration per the
corrected plan in planning/review-findings.md).

Usage: python3 scripts/make_captions.py
Writes: data/captions-en.vtt, data/captions-fa.vtt
Exit 0 on success, 1 on any validation failure.
"""
from __future__ import annotations

import json
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CUES = ROOT / "data" / "chapter-cues.json"
TOTAL_SECONDS = 173.0


def fmt(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def main() -> int:
    data = json.loads(CUES.read_text(encoding="utf-8"))
    scenes = {s["id"]: s for s in data["scenes"]}
    if abs(sum(s["duration"] for s in data["scenes"]) - 173.0) > 1e-6:
        print("FAIL: scene durations do not sum to 173")
        return 1

    errors: list[str] = []
    cues = []
    for cue in data["cues"]:
        scene = scenes.get(cue["scene"])
        if scene is None:
            errors.append(f"cue {cue['id']}: unknown scene {cue['scene']}")
            continue
        s_start = scene["start"]
        s_end = scene["start"] + scene["duration"]
        if not (s_start <= cue["start"] < cue["end"] <= s_end + 1e-6):
            errors.append(f"cue {cue['id']}: outside scene bounds [{cue['start']}, {cue['end']}] ! [ {s_start}, {s_end}]")
        if cue["end"] > TOTAL_SECONDS + 1e-6:
            errors.append(f"cue {cue['id']}: exceeds timeline ({cue['end']} > {TOTAL_SECONDS})")
        for lang in ("en", "fa"):
            text = cue.get(lang, "")
            if not text.strip():
                errors.append(f"cue {cue['id']}: empty {lang} text")
            if lang == "fa":
                if text != unicodedata.normalize("NFC", text):
                    errors.append(f"cue {cue['id']}: FA text not NFC")
                if any(ch in text for ch in "يك"):
                    errors.append(f"cue {cue['id']}: FA text contains Arabic yeh/kaf")
        cues.append(cue)

    # single caption track: no overlaps allowed
    ordered = sorted(cues, key=lambda c: c["start"])
    for a, b in zip(ordered, ordered[1:]):
        if b["start"] < a["end"] - 1e-9:
            errors.append(f"overlap: {a['id']} ends {a['end']} after {b['id']} starts {b['start']}")

    # dialogue census
    dialogue_ids = [c["id"] for c in cues if c["speaker"] != "narrator"]
    expected_dialogue = ["D-S03-1", "D-S04-1", "D-S04-2", "D-S05-1", "D-S05-2",
                         "D-S05-3", "D-S05-4", "D-S05-5", "D-S07-1", "D-S07-2"]
    if sorted(dialogue_ids) != sorted(expected_dialogue):
        errors.append(f"dialogue cues mismatch: {sorted(dialogue_ids)}")

    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1

    for lang, fname in (("en", "captions-en.vtt"), ("fa", "captions-fa.vtt")):
        lines = ["WEBVTT", ""]
        for i, cue in enumerate(ordered, 1):
            lines.append(str(i))
            lines.append(f"{fmt(cue['start'])} --> {fmt(cue['end'])}")
            lines.append(cue[lang])
            lines.append("")
        (ROOT / "data" / fname).write_text("\n".join(lines), encoding="utf-8")
        print(f"wrote data/{fname} ({len(ordered)} cues)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
