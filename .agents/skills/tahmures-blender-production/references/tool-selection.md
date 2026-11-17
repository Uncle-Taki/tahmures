# Tahmures tool-selection note

**Snapshot:** Phase 1, 2026-11-17  
**Repository baseline:** `try2`; inspect the live repository before acting.

## Current responsibilities

- **Blendstra:** connected cloud-side 3D modeling/editing and review workflow. Use for the existing connected Chapter 01 experiment and when local Blender is unavailable. It is not the user's local Blender session.
- **MCP for Blender (`ahujasid/mcp-for-blender`):** direct local Blender scene control. It requires a running Blender instance with its add-on enabled. Use safe mode and disable telemetry in the MCP process configuration.
- **Build 3D Game Rooms:** specialist workflow for game-room/environment construction and room-specific deliverables. It is not the primary character-animation controller. Follow its own approval gates; paid Meshy generation requires explicit user approval.
- **Blenderwright:** eligible benchmark alternative on the owner's selected Blender 5.3.0, which meets its stated 5.2+ minimum. Keep the current controller until identical runtime tests justify switching. Agent Bridge is another separately tested alternative.

## Provisional architecture

Blendstra remains the connected prototype path. MCP for Blender is the planned local execution path. Build 3D Game Rooms is a supporting environment-design specialist. These tools are complementary.

## Local MCP security

The plugin configuration uses:
- `BLENDER_HOST=127.0.0.1`
- `BLENDER_PORT=9876`
- `BLENDER_MCP_SAFE_MODE=1`
- `DISABLE_TELEMETRY=true`
- Python 3.11 managed by uv

The MCP add-on's socket has no authentication or encryption. Keep it on loopback only; never expose port 9876 to the LAN or public internet. Safe mode is a guardrail, not a security sandbox. Review generated code and save a versioned copy before complex edits.

## Runtime status

No live local MCP benchmark is claimed until Blender is installed, the add-on starts, the MCP server handshakes, and the same scene operations are run on the local workstation. The previous Blendstra sample is a separate cloud-side baseline, not a controlled comparison.

## Active version and download

Blender 5.3.0 stable is the workstation target. The owner reports the archive in `/home/mehdi/Downloads/Persepolis/Compressed`; the exact local file remains unverified. Install the add-on explicitly in Blender 5.3's scripts/addons directory. Blender 4.3.2 remains historical evidence, with no installation-first requirement. Follow `Characters/animations/chapter-01-try2/BLENDER-5.3-WORKFLOW.md` in the repository and validate a new S04 candidate before production use.
