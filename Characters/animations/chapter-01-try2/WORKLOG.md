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
