# Phase 1 — Blender tool selection and Tahmures skill integration

**Date:** 2026-11-17  
**Repository:** `Uncle-Taki/tahmures`  
**Branch:** `try2`  
**Status:** Architecture, skill routing, and private plugin packaging complete. Local Blender/MCP runtime validation remains pending.

## Executive decision

The three tools in the original project decision are complementary, not interchangeable:

1. **Blendstra** remains the connected cloud-side prototyping and model-editing path. It is the immediate execution route while this workstation has no discoverable Blender executable and it preserves the already-established Chapter 01 connected trial.
2. **MCP for Blender** (`ahujasid/mcp-for-blender`) is the planned local execution path for direct operations on a running Blender instance and local `.blend` files. Use Blender 5.3.0 for the new local setup and validate a separate S04 compatibility candidate. Blender 4.3.2 remains historical evidence.
3. **Build 3D Game Rooms** is a specialist room/environment workflow. Use it for room layout, environment dressing, and room-specific assets; it is not the primary character-animation controller.

Do not replace one with another globally. Blendstra is the connected prototype route; local MCP is the direct local authoring route; Build 3D Game Rooms is a supporting environment specialist.

## 1. Existing `try2` baseline — preserve

The existing README already records the Stage 1 decision: Blendstra for the connected trial, Blender MCP as the preferred long-term local interface, and Build 3D Game Rooms as a supporting environment workflow. This Phase 1 follow-up refines that architecture; it does not silently reverse the prior decision.

The existing Chapter 01 sample is S04, **“Three Readings”**, with Akvan, Black Div, and Div-e Sefid around the Ancient Tablet. Its documented target is 120 frames at 12 FPS, 10 seconds, 768 × 432, H.264.

The current context labels the work as a **candidate previsualisation**. It is not approval of final character likeness, production rig, lip-sync, or a completed room milestone. The existing `.blend`, render, operation log, and verification evidence must remain unchanged. Use a new versioned candidate for all further tests.

## 2. Tool comparison

| Tool | Best role | Strengths | Constraints |
|---|---|---|---|
| Blendstra | Connected/cloud-side 3D prototype and revision | Existing connected app; model creation/editing, visual inspection, saved versions, and editable Blender handoff | Cloud project is not the user's local Blender session; export and verify a native `.blend` when local handoff is required |
| MCP for Blender | Direct local Blender control | Operates on a running local Blender through an add-on and MCP server; useful for scene inspection, object/material operations, Python-backed edits, viewport inspection, and file work | Requires local Blender and add-on; the add-on socket is unauthenticated/unencrypted; raw Python execution is powerful; safe mode is a guardrail, not a sandbox |
| Build 3D Game Rooms | Room/environment specialist | Focused room construction, environment dressing, asset pipeline, and room-specific review/export | Not a general character-animation MCP; follow its own Function/Asset/Form/Runtime and approval gates; no paid Meshy generation without explicit user approval |

### Additional MCP candidate considered

**Blenderwright** offers a broader structured tool surface and authenticated localhost communication, but its current release targets Blender 5.2 LTS or newer. The historical Tahmures Chapter 01 sample used Blender 4.3.2. Blender 5.3.0 meets that stated minimum, making Blenderwright eligible for a separate runtime benchmark. Keep the existing plugin controller until evidence justifies switching.

No numerical performance winner is claimed. The existing Blendstra sample is a prior connected workflow result, not a controlled head-to-head benchmark of Blendstra and local MCP.

## 3. Existing `.agents` skills — integration

The uploaded `.agents` archive contains 26 skill definitions, matching the 26 project skill modules tracked under `.agents/skills/` on this branch:

- **12 general publishing/production skills:** context, director, research, knowledge, architecture, narrative, authoring, bilingual work, review, human review, media, and publication.
- **14 Tahmures-specific skills:** Tahmures narrative, story-room direction, episode purpose, character pressure, causal architecture, eleven-scene blueprint, dialogue/subtext, punch/timing, Iranian dramaturgy, visual/sound storytelling, series continuity, story red-team, editorial orchestration, and Flow handoff synchronization.

These remain the creative and editorial source of truth. A new project-local skill, `.agents/skills/tahmures-blender-production/SKILL.md`, acts only as a production orchestrator. It routes work to the existing specialists rather than duplicating their methods.

The orchestrator preserves the media roadmap: an animated educational documentary, approximately 80% deterministic illustration/animation and 20% selective cinematic AI shots. Blender is a reusable 3D production layer, not a replacement for the Manim, Motion Canvas, Remotion, Python composition, diagram, caption, and bilingual pipeline.

The portable plugin includes the 26 source skills plus the new orchestrator (27 total), along with the two media-production context documents. The portable copy quotes the `tahmures-punch-and-timing` YAML description because its colon was unquoted; the repository source is corrected in this commit as well.

## 4. Local MCP configuration and security

The private ChatGPT Desktop plugin **Tahmures Blender Studio 0.1.0** was created with:

- the 26 existing skills plus `tahmures-blender-production`;
- a local stdio MCP entry for `mcp-for-blender`;
- `BLENDER_HOST=127.0.0.1` and `BLENDER_PORT=9876`;
- `BLENDER_MCP_SAFE_MODE=1`;
- `DISABLE_TELEMETRY=true`;
- managed Python 3.11 through `uvx`.

The plugin is private and not publicly published. Creating it does not mean the local MCP server is connected or that the plugin has been installed in ChatGPT Desktop.

**Security requirements:** keep the add-on socket on loopback only; do not expose port 9876 to a LAN, public network, or tunnel. Safe mode is not a security sandbox. Prefer structured tools, review any code before execution, save a versioned copy before complex edits, and use only one MCP client per Blender instance.

## 5. Blender version decision

The workstation audit did not find a Blender executable in `PATH` or in the searched installation locations. However, the existing Tahmures sample records Blender 4.3.2 as its baseline.

Use **Blender 5.3.0 stable** for the new workstation setup. The owner already downloaded the archive into `/home/mehdi/Downloads/Persepolis/Compressed`. Follow [BLENDER-5.3-WORKFLOW.md](BLENDER-5.3-WORKFLOW.md) for offline extraction, versioned installation, the 5.3-specific add-on directory, Desktop handshake and isolated S04 validation. Installing 4.3.2 first is unnecessary; retain its original evidence. Blender 5.3 is a regular stable release, not LTS.

The local workstation has an i5-12500H, 38 GiB RAM, and Intel Iris Xe graphics. Use Eevee for interactive previews and CPU Cycles as the reliable path-tracing baseline. No NVIDIA driver installation is warranted for the detected hardware.

## 6. Runtime validation still required

The following tests are not claimed complete:

1. Install the downloaded Blender 5.3.0 archive and verify the executable version.
2. Install and enable the `mcp-for-blender` add-on.
3. Start the add-on server on `127.0.0.1:9876`.
4. Install the private plugin in ChatGPT Desktop and verify a successful MCP handshake.
5. Inspect a copy of the existing S04 scene without modifying the original.
6. Make a small object/material/camera change in a new candidate copy.
7. Preview, correct one visible issue, save, close, reopen, and verify the saved state.
8. Render the existing 120-frame target to a new output directory and validate frame count, duration, codec, and resolution with FFprobe.
9. Compare local MCP results with the existing Blendstra workflow using the same scene specification and record actual tool calls, elapsed time, errors, and human corrections.

Until these tests pass, local MCP connectivity and comparative runtime performance remain **UNKNOWN**.

## 7. ChatGPT surface limitation

A local stdio MCP plugin runs on the user's computer and is a **ChatGPT Desktop-only** integration. Saving the plugin to the account does not expose its local Blender tools in ChatGPT Web or mobile. The existing Blendstra cloud connector remains available separately when connected.

## 8. References

- Existing project decision and sample: `Characters/animations/chapter-01-try2/README.md`, `chapter-context.json`, `RESULT.md`, and `WORKLOG.md`.
- Project skill inventory: `.agents/skills/`.
- Media production roadmap: `.agents/tahmures-media-production-roadmap.md`.
- Media editor context: `.agents/tahmures-media-editor-llm-context.md`.
- MCP for Blender: https://github.com/ahujasid/mcp-for-blender
- Blenderwright (future migration candidate): https://github.com/HoldMyBeer-gg/blenderwright
- ChatGPT plugins and local MCP: https://help.openai.com/en/articles/20001256-plugins-in-chatgpt
- Blender download archive: https://download.blender.org/release/Blender5.3/

## Completion gate

Phase 1 architecture and skill integration are complete. Phase 1 runtime validation remains open until Blender 5.3.0, the add-on, and the local ChatGPT Desktop MCP handshake are verified. No existing Chapter 01 asset was modified or overwritten by this phase.
