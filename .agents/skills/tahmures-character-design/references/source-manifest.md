# Source Manifest and Availability

The following installed skill documents were available and copied into `reference-skills/`:

| Bundled path | Installed source URI |
|---|---|
| `reference-skills/game-art-direction/SKILL.md` | `skills://plugins/design-game-studio/game-art-direction/skill.md` |
| `reference-skills/asset-pipeline/SKILL.md` | `skills://plugins/design-game-studio/asset-pipeline/skill.md` |
| `reference-skills/sprite-pipeline/SKILL.md` | `skills://plugins/game-studio/sprite-pipeline/skill.md` |
| `reference-skills/game-asset-production/SKILL.md` | `skills://plugins/game-development-studio/game-asset-production/skill.md` |
| `reference-skills/web-3d-asset-pipeline/SKILL.md` | `skills://plugins/game-studio/web-3d-asset-pipeline/skill.md` |

## Supporting files not included

The source skill documents refer to additional files (scripts, templates, references, CLIs, or sibling skills). Attempts to read several referenced support files returned `Resource not found`. Those files are not fabricated or represented as bundled.

In particular:
- Sprite Pipeline's helper scripts (`build_sprite_edit_canvas.py`, `normalize_sprite_strip.py`, `render_sprite_preview_sheet.py`) are not included.
- Game Asset Production's `game-dev` CLI is not included. Its command reference is included in the source skill text only where explicitly copied.
- Web 3D Asset Pipeline's optional glTF tooling and runtime stack are not included.
- Game Art Direction's additional art-direction reference and art-bible template are replaced here by Tahmures-authored templates, not copied from the source plugin.

## Not bundled as character skills

`build-3d-game-rooms` was reviewed but not included as a direct character workflow because it is room/prop-centric. Its general idea of blocking approval gates is reflected in the Tahmures skill. Phaser, PlayCanvas, and React Three Fiber skills were excluded because they implement game runtimes rather than character design.
