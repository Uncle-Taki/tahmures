# try2 work log

## Stage 1 — context and tool selection
- Created `try2` from `e8afb28d077e7daa5623d2fec9ab041236395724`.
- Read repository instructions, charter, continuity, Chapter 1, current media script and both cast collection records.
- Chose Blendstra for the connected trial; documented Blender MCP as the preferred full-production interface.
- Created a private Blendstra project and prepared a pinned 10-second S04 excerpt context.
- Room advice is used for candidate set planning only. Function/Form/Runtime and artistic acceptance remain unapproved.
- No source manuscript, existing artwork or prior production output changed.

## Stage 2 — authored scene and execution
- Added a dependency-free Blender scene generator and local rebuild/render/audit wrapper.
- Built three separately named, articulated object hierarchies, round cedar table, stationary tablet, archive record and a candidate film set with a real Boolean passage.
- Local Blender 4.3.2 checks passed: 120 frames at 12 fps, 31,139 evaluated triangles, eight animated objects, three moving figure hierarchies, stable tablet/cloth support and deterministic reset/replay.
- Inspected first/middle/last poses. Corrected the Black Div's vest front to the observed ochre reference. New geometry and performance remain candidates.
- First hosted attempt failed because the empty hosted scene had no World datablock. Added explicit World creation and resubmitted the corrected source to the same private project under a new idempotency key.
- Local OpenImageDenoise is unavailable. The render wrapper disables it; local EEVEE proof confirms the staged geometry, while the full CPU preview is being rendered separately.
- Full repository `make check PYTHON=.venv/bin/python` passed on a source-hash-checked book/code snapshot with Python 3.12 and Go 1.26.11. Media checks remain separate.
- Full-sequence rendering and hosted exact-version review are in progress; no artistic or room-gate approval is claimed.


## Stage 3 — recovery and delivery
- Hosted export rejected authored object IDs; a third submission delegates ID assignment to the fixed exporter.
- Recovered interrupted local frame ranges without discarding completed renders.
- Full movie verification and hosted result are recorded in RESULT.md.


## Follow-up Phase 0 — workstation environment audit (2026-11-17)
- Recorded the owner's Ubuntu 24.04.5 hardware/software diagnostic in `PHASE-0-ENVIRONMENT-AUDIT.md`.
- Confirmed Intel Iris Xe / Mesa OpenGL 4.6, 38 GiB RAM, 299 GiB free disk, FFmpeg 6.1.1 and ChatGPT Desktop 26.1007.21434.
- Set Eevee as the interactive viewport target and CPU Cycles as the reliable path-tracing baseline; the detected Iris Xe is not a supported Intel Arc Xe HPG device for Cycles oneAPI.
- Did not install drivers or software. No NVIDIA GPU was detected; do not install NVIDIA drivers for this machine.
- Blender was not found in the diagnostic shell's `PATH`, and the shell was outside a Git working tree. Blender's package/alternate install state and the local checkout path remain unverified.
- No local Blender rebuild, render benchmark, or MCP handshake was possible from the supplied output. ChatGPT Desktop presence does not establish MCP connectivity.
- Existing Blender 4.3.2 sample, native source and verification evidence remain unchanged. Next gate: locate Blender and the local checkout, then run a real launch/render and MCP handshake before selecting an upgrade path.


## Phase 1 — Blender tool and skill integration (2026-11-17)
- Reviewed the existing `try2` baseline and preserved the documented tool roles: Blendstra for connected/cloud prototyping, MCP for Blender for planned local scene control, and Build 3D Game Rooms for room/environment-specific work.
- Inventoried the 26 existing `.agents/skills` modules (12 general publishing/production skills and 14 Tahmures-specific skills).
- Added `.agents/skills/tahmures-blender-production/SKILL.md` as an orchestration layer; it routes to the existing specialists and preserves canon, approval, continuity, and media-production gates.
- Corrected the unquoted YAML description in `tahmures-punch-and-timing/SKILL.md`; no skill body or meaning changed.
- Created private ChatGPT Desktop plugin `Tahmures Blender Studio` v0.1.0, packaging the 26 existing skills plus the new orchestrator and a local `mcp-for-blender` stdio configuration.
- Configured local MCP for loopback `127.0.0.1:9876`, safe mode enabled, telemetry disabled, and managed Python 3.11. The plugin has not yet been installed in Desktop or connected to Blender.
- Kept Blender 4.3.2 as the compatibility baseline for the existing S04 sample. Blenderwright/Blender 5.2+ is a future migration candidate only; no version upgrade was performed.
- No new Blender scene, render, character asset, or room was generated. Existing S04 source, render, logs, and verification evidence were not overwritten.
- Runtime acceptance tests remain open pending Blender 4.3.2 discovery/installation, add-on activation, Desktop MCP handshake, and a controlled render/round-trip test.

## Blender 5.3 workflow correction (2026-11-17)
- Owner selected the Blender 5.3 download in `/home/mehdi/Downloads/Persepolis/Compressed`.
- Superseded the instruction to install 4.3.2 first; preserve its historical source/render evidence.
- Added a version-checked offline installer and complete installation, 5.3-specific add-on, Desktop handshake, isolated S04 migration and render-validation flow.
- Updated active documentation and production routing. Preserve the existing controller pending actual benchmark evidence; Blenderwright is eligible on 5.3.
- Updated private plugin v0.1.1 and verified its saved release and instructions, preserving the other 26 skills, MCP configuration, identity and sharing scope.
- Owner explicitly authorized committing and pushing this prepared update to `try2`.
- No local installation, Blender 5.3 render, MCP handshake or artistic approval is claimed.
