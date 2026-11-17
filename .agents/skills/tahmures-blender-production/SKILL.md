---
name: tahmures-blender-production
description: Use when translating approved Tahmures media plans into editable Blender scenes, character animation, lighting, rendering, and production QA while coordinating the existing project skills.
---

# Tahmures Blender production orchestrator

## Purpose

Connect the existing Tahmures creative, editorial, continuity, and media-production skills to a reproducible 3D execution workflow. This skill is an orchestration and production-control layer. It does not replace the existing skills, rewrite story canon, approve character designs, or promote candidate media into approved production.

## Non-negotiable source and approval rules

1. Work from the actual Tahmures repository and the current branch. Read root and nested `AGENTS.md` files before changing files.
2. Read `book/project-charter.md`, `book/narrative-continuity.md`, the canonical English chapter, the approved Persian translation where relevant, and the active media handoff.
3. For Chapter 01, inspect `editorial/media-handoff/chapter-01-animation-status.json` and the selected revision under `Characters/animations/chapter-01-candidate-01/production/english-final-03/`. Inspect the current `Characters/animations/chapter-01-try2/` candidate, README, context, timeline, review and worklog before resuming it. Check for superseding owner decisions.
4. Label source-derived statements and production decisions as **CANON**, **APPROVED MEDIA ADAPTATION**, **PROPOSAL**, **CONFLICT**, or **UNKNOWN**. A proposal is never approval.
5. Do not infer, merge, rename, redesign, or silently substitute characters, props, locations, chronology, or mythological claims. The canonical English narrative and continuity govern story facts; approved media references govern approved visual identity.
6. Do not overwrite canonical text, approved visual references, approved media, source `.blend` files, or prior renders. Work in a new candidate/version directory and save a new `.blend` before destructive operations.
7. Treat visual prompts, behavior sheets, generated images, and unapproved character references as proposals until the relevant human approval is recorded. Do not use an unapproved visual prompt as the canonical identity anchor.

## Existing project-skill architecture

The project already has 26 skills. Use them as specialists; do not duplicate their methods in this skill.

### General publishing and production skills

- `mehdi-context`: load canonical project context and rules.
- `mehdi-director`: orchestrate the publishing lifecycle.
- `mehdi-research`: establish reliable research and source evidence.
- `mehdi-knowledge`: create reusable technical knowledge units.
- `mehdi-architecture`: explain system models and trade-offs.
- `mehdi-narrative`: create educational fictional narratives.
- `mehdi-author`: write from approved knowledge and blueprints.
- `mehdi-bilingual`: synchronize multilingual editions.
- `mehdi-review`: technical, editorial, and consistency review.
- `mehdi-human-review`: reconcile human notes and preserve sign-off.
- `mehdi-media`: transform approved content into educational media.
- `mehdi-publisher`: prepare final publication packages.

### Tahmures-specific skills

- `tahmures-narrative`: Shahnameh evidence tiers, cast, chronology, naming, and mythic continuity.
- `tahmures-story-room-director`: orchestrate the complete story-room sequence.
- `tahmures-episode-purpose`: define dramatic purpose and teaching bridge.
- `tahmures-character-pressure`: build character objective, fear, contradiction, and tactics.
- `tahmures-causal-architecture`: design escalation, reversal, costly choice, and aftermath.
- `tahmures-eleven-scene-blueprint`: create sourced scene cards and production constraints.
- `tahmures-dialogue-and-subtext`: playable dialogue, intention, silence, and voice timing.
- `tahmures-punch-and-timing`: measure dramatic beats against the approved timeline.
- `tahmures-original-iranian-dramaturgy`: apply the project's Iranian dramaturgy lens without imitation.
- `tahmures-visual-sound-storytelling`: turn dramatic intention into visible action, camera priorities, props, and sound.
- `tahmures-series-continuity`: audit canon, approved adaptation, world rules, and recurring elements.
- `tahmures-story-red-team`: adversarially review causality, pacing, clarity, animation cost, and continuity.
- `tahmures-editorial`: coordinate evidence, bilingual review, approvals, and quality gates.
- `tahmures-flow-handoff-sync`: package versioned candidate handoffs with review and promotion gates.

For a full episode story-room pass, invoke `tahmures-story-room-director` and let it delegate to its specialist skills. For visual staging, use `tahmures-visual-sound-storytelling`. For continuity and approval, use `tahmures-series-continuity` and `tahmures-editorial`. For media packaging, use `tahmures-flow-handoff-sync`. Do not reimplement those processes here.

## Media-production philosophy

Follow `.agents/tahmures-media-production-roadmap.md` and `.agents/tahmures-media-editor-llm-context.md`.

The target is an **animated educational documentary**, not an AI-generated movie. Preserve the hybrid pipeline:

- Approximately 80% deterministic illustration, diagrams, captions, and animation.
- Approximately 20% selective cinematic AI shots for entrances, atmosphere, and emotional transitions.
- Use Manim, Motion Canvas, Remotion, Python composition, and deterministic renderers where they provide exact technical diagrams, typography, bilingual captions, and reproducibility.
- Use Blender for reusable 3D characters, props, environments, camera work, lighting, and selected cinematic sequences.
- Do not move every scene into Blender or AI video merely because those tools are available.

## Tool selection and responsibility boundaries

### Blendstra

Use the connected Blendstra app when it is available and the task benefits from cloud-side model creation, editing, visual inspection, saved versions, or a downloadable editable Blender artifact. Prefer it for the already-established connected Chapter 01 trial while local Blender is unavailable.

- Keep each iteration in a new saved version.
- Inspect returned model/project identifiers and previews before making follow-up edits.
- Do not claim that a cloud project is the user's local Blender session.
- Export and verify the native `.blend` file when local handoff is required.
- Follow Blendstra's own skill and tool instructions; do not invent tool names or project IDs.

### Local MCP for Blender

Use the local `mcp-for-blender` server when Blender is installed and the user wants direct control of a local scene or local `.blend` files.

- The project's current sample baseline is Blender 4.3.2. Preserve that version for the existing `try2` sample and test the local MCP against it before any version migration.
- Keep the Blender add-on socket bound to loopback (`127.0.0.1` / `localhost`) and port `9876`. Never expose the unauthenticated socket to a LAN, public network, or tunnel.
- Start with `BLENDER_MCP_SAFE_MODE=1` and `DISABLE_TELEMETRY=true`. Safe mode is a guardrail, not a security sandbox.
- Prefer structured MCP tools over arbitrary Python execution. Review every script before running it. Do not disable safe mode or run unreviewed arbitrary code unless the user explicitly approves the specific operation.
- Save a copy before executing complex or destructive operations. Use a new versioned output path.
- Run only one MCP client against a Blender instance at a time.

### Build 3D Game Rooms

Use the separately installed Build 3D Game Rooms workflow for room/environment layout, room geometry, environment dressing, and room-specific deliverables. It is a specialist room-production path, not the primary character-animation controller.

- Follow its own doctrine, pipeline, asset, review, and export instructions.
- Keep the room's function, form, asset provenance, and runtime requirements explicit.
- Do not initiate paid Meshy or other paid generation, consume credits, or request/store API keys without explicit user approval.
- Do not treat a room-generation result as an approved Tahmures location until it passes the project's visual and continuity gates.

### Other MCP candidates

Do not migrate the current project to a different Blender MCP solely because it has more tools. Any replacement must first pass the same local scene, animation, visual review, recovery, export, and compatibility tests. In particular, Blenderwright requires Blender 5.2+ and is a separate migration candidate, not a drop-in replacement for the existing Blender 4.3.2 baseline.

## Required scene/shot contract

Before building or editing a scene, prepare a concise, versioned shot specification containing:

1. `episode_id`, `scene_id`, candidate/revision ID, and source commit.
2. Source authority and approval state for the scene, characters, designs, props, and location.
3. Dramatic purpose and audience/teaching purpose.
4. Character list with exact canonical names and approved visual-reference IDs.
5. Action beats, blocking, screen direction, eye-lines, and contact requirements.
6. Props and environment requirements, with provenance and scale.
7. Camera plan: shot size, angle, lens, movement, framing, and transitions.
8. Lighting, materials, render engine, color management, and output resolution.
9. Frame rate, frame range, duration, and exact timeline mapping.
10. Audio/narration, silence, sound cues, and exact bilingual text/overlay requirements.
11. Expected outputs, file paths, render settings, and reproducibility notes.
12. Review gates, known risks, and items explicitly awaiting human approval.

Do not invent missing values. Mark them **UNKNOWN** and ask only for the missing decision that blocks safe progress.

## Execution workflow

1. **Read and classify sources.** Confirm the active branch, source commit, approval status, scene timeline, and current output. Do not assume a scene count or duration from memory.
2. **Route creative work.** Use the existing story-room, visual/sound, continuity, editorial, and handoff skills as required. Keep story decisions separate from technical execution.
3. **Create a shot contract.** Convert only approved or explicitly requested proposal material into an actionable scene specification.
4. **Choose the execution tool.** Use Blendstra for connected cloud model/project work; local MCP for a running local Blender; Build 3D Game Rooms for room-specific construction. These tools are complementary, not interchangeable.
5. **Build non-destructively.** Work in a new scene/candidate copy. Keep collections, object names, materials, actions, cameras, and outputs organized and deterministic.
6. **Inspect visually.** Capture representative frames and check composition, silhouettes, contact, foot sliding, clipping, intersections, scale, material response, lighting, and readability.
7. **Validate technically.** Reopen the `.blend`; verify frame range, FPS, dimensions, render engine, object/armature counts, action assignments, missing assets, and output files. Use FFprobe to validate encoded video frame count, duration, codec, and resolution.
8. **Review narrative and continuity.** Re-run the relevant Tahmures continuity/editorial skills. Separate defects from creative proposals.
9. **Deliver and record.** Save source `.blend`, rendered preview, shot contract, validation report, and worklog. Never promote a candidate to approved production without explicit human approval.

## Chapter 01 current sample guardrails

The `try2` sample currently documents S04, **“Three Readings”**, with Akvan, Black Div, and Div-e Sefid around the Ancient Tablet. Its documented target is 120 frames at 12 FPS, 10 seconds, 768 × 432, H.264.

Treat that sample as a **candidate previsualisation**, not as approval of final character likeness, production rig, lip-sync, or a completed room milestone. Verify the latest `chapter-context.json`, README, timeline, and review records before continuing; these values may be superseded by a later owner decision.

Do not expand the S04 sample into a full Chapter 01 production, replace its character references, or change the timeline without explicit instruction and the appropriate approval.

## Definition of done

A Blender task is complete only when:

- The source and approval state are recorded.
- The correct specialist skills were used.
- The native `.blend` is saved in a new, versioned candidate location.
- The render/preview is visually inspected.
- Frame rate, frame range, duration, resolution, codec, and asset dependencies are validated.
- Continuity and editorial checks are recorded.
- The worklog and README are updated before a requested push.
- No canonical or approved asset was overwritten.
