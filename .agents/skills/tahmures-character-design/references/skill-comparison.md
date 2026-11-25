# Installed Skill Comparison

The scores below are **document-based estimates** of how well each installed skill's written workflow maps to Tahmures character production. They are not measured artistic-quality benchmarks, and they do not prove that a tool, provider, or script is installed or operational.

## 2D profile

Weights: reference fidelity 25, silhouette/shape language 20, character-sheet completeness 15, costume/palette 15, 2D asset readiness 10, handoff to 3D 10, reproducibility/QA 5.

| Rank | Skill | Score / 100 | Best use | Limitation |
|---:|---|---:|---|---|
| 1 | Game Art Direction | 89 | Character identity, silhouette, visual pillars, palette and art bible | Does not build Blender meshes |
| 2 | Sprite Pipeline | 86 | Consistent 2D animation strips from an approved seed | Animation-asset workflow, not complete concept design |
| 3 | Asset Pipeline | 71 | Asset provenance, rights, imports and QA | Asset operations rather than character ideation |
| 4 | Game Asset Production | 64 | Optional 2D source/texture handoff and packaging | Primarily asset production; not a full character design method |

## 3D profile

Weights: reference fidelity 20, silhouette/proportions 15, modular mesh quality 15, materials/palette 10, rigging/deformation readiness 10, Blender 5.3 compatibility 10, non-destructive reproducibility 10, validation evidence 10.

| Rank | Skill | Score / 100 | Best use | Limitation |
|---:|---|---:|---|---|
| 1 | Game Asset Production | 79 | Inspect, normalize, validate and package 3D assets | Not a dedicated character sculpt/modeling methodology |
| 2 | Asset Pipeline | 76 | Topology, scale, orientation, rig/animation checks and provenance | Does not create the character by itself |
| 3 | Game Art Direction | 73 | Character visual direction and design consistency | No mesh construction or rig implementation |
| 4 | Web 3D Asset Pipeline | 71 | GLB/glTF cleanup, optimization and runtime validation | Export/shipping workflow, not original character design |

## Selection

Use Game Art Direction first, then the Tahmures-specific Blender production workflow for the actual character. Use Asset Pipeline and Game Asset Production for QA and packaging. Use Sprite Pipeline only for 2D animation work. Use Web 3D Asset Pipeline only when a GLB/glTF runtime deliverable is needed.

## Scope exclusions

- `build-3d-game-rooms`: useful gate and audit ideas, but its primary scope is rooms, architecture, and props rather than character authoring.
- Phaser, PlayCanvas, React Three Fiber: game runtime implementation, not character design or Blender modeling.
- Engine selection skills: not needed while the project has already selected Blender for character production.
