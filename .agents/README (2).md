# Tahmures Character Skills Pack

**Purpose:** An additive skill bundle for designing, building, reviewing, and preparing Tahmures characters in Blender.

## Included

- `skills/tahmures-character-design/SKILL.md` — Tahmures-specific workflow and skill router.
- A reusable 2D/3D utility scoring function and JSON weight profiles.
- Five selected installed skill workflows, retained under `skills/tahmures-character-design/reference-skills/`:
  1. Game Art Direction
  2. Sprite Pipeline
  3. Asset Pipeline
  4. Game Asset Production
  5. Web 3D Asset Pipeline
- Character brief, art-bible, asset-register, and review templates.
- Blender 5.3 workflow and quality gates.
- Skill comparison matrix, source manifest, and installation instructions.

## Repository impact

The ZIP contains a project-root `skills/` directory. Extracting it at the Tahmures repository root adds:

```text
skills/tahmures-character-design/
```

It does **not** replace:

```text
skills/tahmures-blender-production/
```

## Recommended routing

| Need | Use |
|---|---|
| Character identity, silhouette, palette, costume | `reference-skills/game-art-direction/SKILL.md` |
| 2D animation strip | `reference-skills/sprite-pipeline/SKILL.md` |
| Asset provenance, rights, imports and QA | `reference-skills/asset-pipeline/SKILL.md` |
| 3D asset inspection, normalization and packaging | `reference-skills/game-asset-production/SKILL.md` |
| GLB/glTF runtime export | `reference-skills/web-3d-asset-pipeline/SKILL.md` |
| Complete Tahmures character workflow | `SKILL.md` |

## Important limitations

The source skill instructions refer to additional plugin-specific scripts, templates, CLIs, and external providers. Those dependencies are **not** bundled here unless explicitly present as a file in this ZIP. The skill instructions are workflows, not standalone executables.

This package does not contain Blender itself, the Tahmures repository source code, original Akvan reference images, the local Blender MCP bridge or credentials, provider credentials/credits, or source plugin scripts that were unavailable for export.

The source skill text is retained for local project reference. Check the source plugin's terms before redistributing this bundle outside your own project.
