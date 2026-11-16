# Tahmures Story Room — Codex project skills

This is an **installable, candidate-only writing enhancement package** for the Tahmures repo. It is NOT an approved new canon, screenplay, movie, or Google Flow integration. It contains 12 scoped Codex `SKILL.md` files, working templates, a source/ethics reference, a validator, and a full Codex run prompt.

## Installing
1. From the Tahmures repository root, inspect the archive before copying. Ensure no `.agents/skills/tahmures-*` name already exists with different user-created content. Merge manually on conflicts; **do not overwrite**.
2. Extract `.agents/skills/tahmures-*/SKILL.md` and `story-room/` from this archive into the repo root. Example, from repo root: `unzip -n /path/to/tahmures_story_room_codex_skills.zip` (`-n` never replaces existing files). Verify the command extracted the expected files and check for skipped conflicts.
3. Run `python3 story-room/scripts/validate_skill_bundle.py .` from the repo root. Restart Codex if the new skills do not appear. Existing `.agents/skills/tahmures-editorial/` is intentionally left untouched.
4. Open `story-room/CODEX_STORY_ROOM_PROMPT.md`, paste its entire contents into Codex with this repository as the workspace. For direct invocation start with `$tahmures-story-room-director`.
5. In the **same story-room Codex run**, `$tahmures-flow-handoff-sync` must generate a fully synchronized **candidate** Google Flow handoff with updated contexts, shot prompts, Agent instructions, media mappings, and operator guides. Do not feed it to Google Flow as if approved. After explicit owner approval, perform a separate versioned official handoff promotion without overwriting prior records.

## Skill graph
`episode-purpose` -> `character-pressure` -> `causal-architecture` -> `original-iranian-dramaturgy` -> `eleven-scene-blueprint` -> `punch-and-timing` -> `dialogue-and-subtext` -> `visual-sound-storytelling` -> `series-continuity` -> `story-red-team`; `flow-handoff-sync` regenerates the candidate Google Flow production contexts after red-team; `story-room-director` orchestrates the sequence.

## Out-of-scope
Do not modify chapter text, approved video revisions, approved voices, Persian translations, story canon, human approval records, or production timeline. Do not generate AI artwork/video/voice, use provider APIs, commit, push, or upload. Candidate-only files go in separate workspace with source ledger.
