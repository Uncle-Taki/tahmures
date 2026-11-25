---
name: tahmures-character-design
description: Design, review, construct, and validate Tahmures characters across 2D visual development and stylized 3D Blender production. Use when creating a new mythological character, evaluating character-design workflows, or preparing a character for animation.
---

# Tahmures Character Design & Production

## Mission

Create a repeatable character-design workflow for the Tahmures project. Preserve approved character identity while moving from 2D visual development to a stylized 3D Blender character.

This skill is additive. It does not replace `skills/tahmures-blender-production/SKILL.md`, the project's approved character specifications, or its reference-governance documents.

## Authority order

Resolve conflicts in this order:

1. The current approved character specification and approved master reference.
2. The current approved reference/conflict register and component map.
3. The existing Tahmures Blender production skill and repository-specific technical contracts.
4. This Tahmures character-design skill.
5. The bundled generic reference skills.
6. Model-generated suggestions or unapproved candidate images.

Never use a generated concept to silently override an approved source. If the approved documents conflict, stop and report the conflict instead of choosing one arbitrarily.

## Current project direction

The known production direction is a **stylized 3D blockout that retains the project's paper-cut / illustrated visual language**. Treat this as the current working direction, but verify it against the latest approved project documents before making irreversible design decisions.

The known target DCC version is **Blender 5.3**. Verify the actual running version before using version-specific APIs or features.

## Workflow router

### A. Character discovery and source audit

Before designing or modifying a character:

1. Inspect the repository and locate the current character specification, approved references, reference-conflict register, component map, and production skill.
2. Read only the files authorized by the task or the project's source-of-truth document.
3. Record the exact reference file paths and hashes where practical.
4. Separate approved, candidate, rejected, and historical references.
5. Identify unresolved design decisions. Do not fill them with guesses.
6. Preserve all original files; work from copies or additive outputs.

For Akvan Div, the previously identified authoritative inputs include:
- `CHARACTER_SPECIFICATION.md`
- `APPROVED_REFERENCES.md`
- `REFERENCE_CONFLICTS.md`
- the selected approved Akvan master image
- `skills/tahmures-blender-production/SKILL.md`
- its approved reference and tool-selection documentation

These are discovery hints, not proof that the paths or contents are unchanged. Verify them in the current repository.

### B. 2D visual development

Use the Game Art Direction reference skill for:
- visual pillars and character role;
- silhouette and shape language;
- front, side, and back views;
- head/face studies and expression range;
- costume layers and construction;
- palette and material callouts;
- props and accessories, where approved;
- scale and proportion guides;
- a concise character art bible.

The 2D stage should define the character, not invent new identity details. Keep a clear distinction between:
- approved facts;
- proposed design alternatives;
- unresolved questions;
- rejected alternatives.

If a 2D animation strip is requested, route to Sprite Pipeline. Start from an approved seed frame and preserve character identity across all frames. Do not create each frame independently unless the user explicitly accepts the resulting consistency risk.

### C. 3D blockout in Blender

Use the existing Tahmures Blender production skill for repository-specific construction instructions. Use the generic Game Asset Production reference only for asset inspection, normalization, validation, and packaging.

Before building:
1. Verify Blender 5.3 and the active scene.
2. Verify the reference image and its orientation.
3. Confirm the project's coordinate, scale, naming, collection, and save conventions from repository documentation.
4. Create a non-destructive working copy or a clearly named new collection.
5. Build primary masses and silhouette before small details.
6. Compare front, side, back, and three-quarter views against approved references.
7. Use separate mesh components where they improve editability or are required by the component map.
8. Keep object names, origins, transforms, and collection hierarchy meaningful and stable.
9. Do not add unapproved costume elements, weapons, ornaments, facial features, or anatomy.

Do not assume a particular number of mesh objects, armature layout, polygon budget, or texture resolution. Read the character specification and production rules first.

### D. Materials and visual consistency

Only develop final materials after the blockout passes silhouette and proportion review.

- Use the approved palette and material notes.
- Keep material response consistent with the project's stylized paper-cut / illustrated language.
- Avoid adding realism, surface noise, or decorative detail that weakens shape readability.
- Prefer a controlled, reusable material set over many one-off materials.
- Maintain a neutral clay/flat-shaded review mode alongside the final material preview.

### E. Rigging and animation readiness

Rig only when requested or when the production plan explicitly reaches the rigging gate.

Before rigging:
- verify topology and deformation zones;
- check shoulder, hip, elbow, knee, neck, and facial deformation needs;
- identify rigid costume pieces versus deforming surfaces;
- agree on the intended animation range;
- preserve the approved silhouette in neutral and extreme poses.

Rigify may be considered for control-rig generation, but it does not automatically guarantee correct mesh weights, deformation, or a production-ready character. Test skinning and poses separately.

### F. Validation and delivery

Run the checks that are relevant to the requested stage:

**Reference and design**
- approved source files are identified;
- no unresolved reference conflict was silently ignored;
- silhouette and proportions are reviewed in orthographic views;
- palette and costume match the approved design.

**Blender scene**
- Blender version is recorded;
- object and collection names are stable;
- transforms and origins follow project conventions;
- no unintended duplicate or hidden proxy objects remain;
- no source asset was overwritten;
- the saved `.blend` file reopens successfully.

**Geometry and materials**
- normals and mesh integrity are inspected;
- non-manifold or accidental geometry is reviewed;
- material slots and textures are present and correctly assigned;
- no missing external image paths remain.

**Rigging, if applicable**
- armature hierarchy is valid;
- weights are inspected;
- representative extreme poses are reviewed;
- rigid costume elements behave as intended.

**Export, if applicable**
- use Web 3D Asset Pipeline only when a GLB/glTF delivery target exists;
- validate scale, orientation, pivots, hierarchy, materials, and texture budget;
- do not claim runtime readiness from a successful export alone.

Record what was actually checked, what failed, and what remains unverified.

## Blocking approval gates

Do not advance past a gate without evidence and approval where required.

| Gate | Required evidence |
|---|---|
| Reference gate | Approved source files and resolved reference conflicts |
| 2D design gate | Character brief, approved silhouette, views, palette and costume |
| 3D blockout gate | Orthographic and three-quarter reviews against the approved source |
| Materials gate | Approved palette and material review |
| Rig gate | Topology/deformation review and pose tests |
| Delivery gate | Reopen/export checks and asset manifest |

A render is evidence for visual review, not proof that all geometry, rigging, or runtime checks passed.

## External generation and paid services

- Do not submit a character or reference image to a third-party provider without explicit user authorization.
- Before any paid generation, disclose the provider, asset/data being sent, cost ceiling, and intended output; require explicit approval.
- Never request or expose provider API keys in chat, prompts, source files, logs, or reports.
- Keep original references and generated derivatives separate.
- Record provider, job ID, prompt, settings, license, transformations, and validation evidence.

## Utility scoring

Use:

`python3 scripts/tahmures_character_utility.py --help`

The scoring profiles are in `config/utility_weights.json`. Scores range from 0 to 5. A numerical score does not override a failed hard gate.

- `eligible`: all required gates are explicitly true.
- `provisional`: no gate is known to fail, but one or more are unverified.
- `excluded`: at least one required gate is false.

The bundled comparison matrix is a document-based estimate of installed skill instructions, not a benchmark of actual artistic output.

## Bundled reference skills

- `reference-skills/game-art-direction/SKILL.md`
- `reference-skills/sprite-pipeline/SKILL.md`
- `reference-skills/asset-pipeline/SKILL.md`
- `reference-skills/game-asset-production/SKILL.md`
- `reference-skills/web-3d-asset-pipeline/SKILL.md`

These are reference workflows. Their external scripts, plugin CLIs, paid providers, and unavailable supporting files are not automatically installed by copying this bundle.
