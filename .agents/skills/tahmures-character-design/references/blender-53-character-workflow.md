# Blender 5.3 Character Workflow Notes

This is a project-facing checklist, not a substitute for Blender's official manual or the Tahmures production skill.

## Before modeling
- Verify the actual Blender version from the running application.
- Read the repository's naming, collection, coordinate, unit, and save conventions.
- Load only approved reference images.
- Keep source references immutable.
- Create a new working scene/collection or save a clearly named working copy.

## Modeling order
1. Primary body masses and overall proportions.
2. Silhouette from front, side, and three-quarter views.
3. Head, face, and major costume masses.
4. Secondary costume components.
5. Small details only after the silhouette is approved.

## Review modes
- Flat black silhouette on a neutral background.
- Neutral clay material.
- Orthographic front, side, and back.
- Three-quarter camera.
- Approved palette/material preview.

## Non-destructive principles
- Avoid destructive edits to the only source scene.
- Keep modifier stacks editable where practical.
- Use meaningful object and collection names.
- Keep references and generated outputs separate.
- Save checkpoints at approval gates.

## Rigging
Rigging is a separate stage. A generated armature is not proof of good skinning or deformation. Validate representative poses and inspect weights.

## Export
Export only when a target format is requested. For GLB/glTF, check scale, forward/up orientation, pivots, hierarchy, materials, image paths, and texture budgets. Reopen or import the exported asset for validation.
