# Chapter 01 — try2 Blender animation trial

Candidate only. This separate trial does not replace a manuscript, cast master, approved voice, timing, or existing film.

## Choice
Use **Blendstra for this connected trial**. It runs hosted Blender and retains editable source and an interactive animated derivative. Its current guide limits source animation to 240 frames and optional MP4 output to 24 frames at 12 fps (two seconds). Render the full authored sample locally from the same Blender Python source.

For unrestricted production on the owner's Blender workstation, **Blender MCP is the preferred long-term control interface**. A live Blender MCP connection is not exposed in this session. The local Blender executable is a render/verification fallback, not evidence that Blender MCP is connected.

| Option | What it supplies | Fit for this project |
| --- | --- | --- |
| Blender MCP / mcp-for-blender | Live Blender control, Python execution, viewport and animation verification | Best for full-length production, rigging, audio and repeated interactive revisions; requires a connected Blender instance |
| Blendstra | Hosted Blender Python authoring, saved native source, short supported GLB animation, exact-version review | Best available connected route for a short reproducible sample |
| Build 3D Game Rooms | Room design, procedural shell, prop and clearance audits, staged review workflow | Supporting environment discipline; not an animation transport or character-performance engine |

Primary MCP source, checked 2026-11-16: https://github.com/ahujasid/mcp-for-blender
Blendstra source: connected authoring guide v2026-11-14.1, topics modeling, animation, geometry; runtime Blender 4.5.3; CPU available.
Room workflow source: installed Build 3D Game Rooms instructions and custom adapter.

## Phase 0 — workstation audit

The 2026-11-17 workstation audit is recorded in
[PHASE-0-ENVIRONMENT-AUDIT.md](PHASE-0-ENVIRONMENT-AUDIT.md).
Hardware assessment is complete. Owner-supplied logs now confirm Blender 5.3.0 scene build/audit and four still renders; full-video verification, visual review and MCP connectivity remain open. The audit preserves the known-good
Blender 4.3.2 sample and recommends Eevee for interactive work and CPU Cycles
for path-traced rendering on the detected Intel Iris Xe workstation.

## Sample scope
A **10-second silent 3D blocking study** of S04, “Three Readings”, at 12 fps (frames 1–120). Akvan studies the record, Black Div leans toward the inscription then turns to leave empty-handed, and Div-e Sefid reaches toward the still-unidentified tablet. One tablet remains on the table throughout this excerpt; this stops before the later wrapping/delivery. No newly invented dialogue or performance approval.

New procedural, stylised 3D interpretations use the observed Illustrated V2 colours, horns, hair and clothing as design references. They are candidate geometry, not established likenesses or finished production rigs. Fixed camera, readable gestures, actual cast separation, a physical table/tablet and a real set provide a useful Blender communication test.

The room workflow is applied to a **previsualisation set only**. No approved Function, Form or Runtime milestone is claimed. No Meshy generation, image alteration, voice generation, publication or runtime deployment is part of this trial.

## Stages and branch
Historical stages were committed to `try2`. Further changes use a new branch and pull request into `main`, as directed by the owner.
1. Tool comparison and pinned Chapter 1 context.
2. Reproducible Blender source and private Blendstra submission.
3. Rendered sample, measurements, review evidence and result report.

See `chapter-context.json`, `WORKLOG.md` and the stage deliverables.

## Rebuild and inspect

Historical rebuild commands below use the original output directory. For the active Blender 5.3.0 setup use [BLENDER-5.3-WORKFLOW.md](BLENDER-5.3-WORKFLOW.md), which isolates outputs and reuses the download in `/home/mehdi/Downloads/Persepolis/Compressed`.

Requirements: the historical sample was tested on Blender 4.3.2 and FFmpeg; the owner has since demonstrated the 5.3.0 build/audit and four still renders. Full-video and visual acceptance remain open. The scene generator uses only Blender's bundled Python.

```bash
blender --background --python Characters/animations/chapter-01-try2/render_local.py -- --build --audit
blender --background --python Characters/animations/chapter-01-try2/render_local.py -- --stills
blender --background --python Characters/animations/chapter-01-try2/render_local.py -- --frames 1 120
```

Open `output/chapter-01-try2.blend`, use the production camera, and play frames 1–120 at 12 fps. Named timeline markers identify the three beats. `render_local.py` measures visible head framing, stationary tablet support, actual transform changes and deterministic seek/reset/replay. It does not establish full collision-free motion, artistic acceptance or a finished character rig.

The local Blender build lacks OpenImageDenoise; the local wrapper disables that feature explicitly. Hosted creation starts with an empty world, so the generator creates a World datablock when needed. These are recorded compatibility fixes, not changes to the story.



## Phase 1 — Blender tool and skill integration

See [PHASE-1-BLENDER-INTEGRATION.md](PHASE-1-BLENDER-INTEGRATION.md) for the tool comparison, 26-skill routing architecture, local MCP security configuration, and runtime acceptance tests. The new project skill is [tahmures-blender-production](../../../.agents/skills/tahmures-blender-production/SKILL.md). The private ChatGPT Desktop plugin `Tahmures Blender Studio` v0.1.1 targets Blender 5.3.0 and packages 27 skills and a local `mcp-for-blender` configuration; it is not published and has not yet completed a local MCP handshake. The existing Blendstra sample and all prior artifacts remain unchanged.

## Blender 5.3 render launcher

From the repository root run `bash Characters/animations/chapter-01-try2/run_blender53.sh` to create an isolated candidate, build/audit, render four stills and 120 animation frames, encode `preview.mp4`, and validate it. Pass an existing candidate directory as the sole argument to continue its render. The default executable is `$HOME/.local/bin/blender-5.3`; `BLENDER_BIN` can override it. Existing preview movies are preserved. See [BLENDER-5.3-WORKFLOW.md](BLENDER-5.3-WORKFLOW.md) for exact commands. This launcher produces the silent compatibility preview; the historical `render_sequence.py` retains its separate captioned sample workflow.
