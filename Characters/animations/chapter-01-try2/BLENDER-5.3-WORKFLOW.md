# Blender 5.3 workstation flow

**Updated:** 2026-11-17 · **Branch:** try2 · **Target:** Blender 5.3.0 stable (not LTS).
This supersedes earlier instructions to install Blender 4.3.2 first or to use the generic download page as a version-pinned 5.2.4 link.

## 0. Inputs and actual status

The owner reports downloading Blender into:
`/home/mehdi/Downloads/Persepolis/Compressed`.

Expected official Linux x86_64 archive: `blender-5.3.0-linux-x64.tar.xz`.
The directory and filename have not been inspected from this remote session.
Installation, Blender 5.3 scene compatibility, viewport rendering and Desktop MCP connectivity remain unverified.

The existing 4.3.2 source/render evidence remains historical. Installing 4.3.2 is not a prerequisite for this new flow. Use a separate 5.3 candidate and preserve original artifacts.

## 1. Verify the existing download and install

Run on the owner's Ubuntu workstation:

```bash
find "/home/mehdi/Downloads/Persepolis/Compressed" -maxdepth 2 \
  -type f -iname '*blender*' -print
```

If the expected archive is present, from the repository root run:

```bash
bash Characters/animations/chapter-01-try2/install_blender53.sh
"$HOME/.local/bin/blender-5.3"
```

The installer checks archive integrity, extracts into a temporary directory, verifies Blender reports exactly 5.3.0, installs under `$HOME/opt/blender-5.3.0`, and creates only the versioned `blender-5.3` command. It preserves other Blender installs and the download. Archive integrity is not an authenticity check; optionally compare the archive's SHA-256 with the official manifest.

Official pinned archive (reference only; no redownload required):
https://download.blender.org/release/Blender5.3/blender-5.3.0-linux-x64.tar.xz
Official SHA-256 manifest:
https://download.blender.org/release/Blender5.3/blender-5.3.0.sha256

If Persepolis renamed the file or placed it in a nested folder, use the actual full filename in the installer's `archive` variable. Do not unpack an arbitrary first match.

## 2. Verify the active checkout

```bash
cd /home/mehdi/Project/leela/tahmures
git rev-parse --show-toplevel
git status --short --branch
git log -1 --oneline
```

This is the candidate checkout path supplied by the owner's search, not yet a verified Git root. Confirm it is the intended repository and on `try2`. Preserve uncommitted changes. With a clean tree on `try2`, retrieve the revised flow using `git pull --ff-only origin try2`. Do not use backup, nested, or Gemini cache copies as the active source.

## 3. Blender 5.3 launch and rendering gate

Open factory defaults first. Confirm the viewport works on Intel Iris Xe. Use Eevee for previews and CPU Cycles for path tracing. Record Blender version, render engine, graphics backend, dimensions, elapsed time and any errors. Vulkan enumeration alone does not prove the Blender viewport works.

Keep the existing S04 target: frames 1–120, 12 FPS, 10 seconds, 768 × 432. Retain Akvan, Black Div, Div-e Sefid and the Ancient Tablet, with the same candidate/approval state.

## 4. Install the add-on specifically for Blender 5.3

After launching Blender 5.3 once, close it. If `uvx` is absent, install uv using its official instructions, then open a new terminal:
https://docs.astral.sh/uv/getting-started/installation/

```bash
uvx --version
mkdir -p "$HOME/.config/blender/5.3/scripts/addons"
BLENDERMCP_ADDONS_DIR="$HOME/.config/blender/5.3/scripts/addons" \
  uvx --python 3.11 mcp-for-blender install-addon
"$HOME/.local/bin/blender-5.3"
```

The explicit add-on directory prevents auto-detection from targeting a different Blender version. Record the installed package/add-on version before comparing controllers. Managed Python 3.11 runs the MCP server; Blender uses its own bundled Python.

In Blender 5.3, open Preferences → Add-ons, enable **Interface: MCP for Blender**, then press N in the 3D Viewport and open its panel. Start/check its server on loopback port 9876.

## 5. Connect the existing private plugin

Use the updated Tahmures Blender Studio plugin in ChatGPT Desktop and start a new local thread. Its local stdio MCP settings remain:
`uvx --python 3.11 mcp-for-blender`, host `127.0.0.1`, port `9876`,
`BLENDER_MCP_SAFE_MODE=1`, `DISABLE_TELEMETRY=true`,
`UV_PYTHON_PREFERENCE=only-managed`.

If Desktop cannot resolve `uvx`, use the absolute path reported by `command -v uvx` in its local configuration. Run one controller against one Blender instance. Do not expose the unauthenticated socket remotely.

First ask for add-on status and scene information. Confirm the returned Blender version is 5.3.0. Then create/save/reopen a disposable scene and inspect its viewport. A listening port is not a successful MCP handshake, and a saved plugin is not proof of Desktop execution.

## 6. Migrate and validate S04 in an isolated copy

The current render wrapper writes beside itself to `output/`. Running it in the original sample directory would overwrite historical evidence. Copy the source files to a fresh candidate first:

```bash
cd /home/mehdi/Project/leela/tahmures
(
  set -e
  sample="Characters/animations/chapter-01-try2"
  trial="$sample/compatibility/blender-5.3-$(date +%Y%m%d-%H%M%S)"
  mkdir -p "$sample/compatibility"
  mkdir "$trial"
  cp "$sample/build_scene.py" "$sample/render_local.py" "$trial/"
  "$HOME/.local/bin/blender-5.3" --background --factory-startup \
    --python-exit-code 1 --python "$trial/render_local.py" -- --build --audit
  "$HOME/.local/bin/blender-5.3" --background --factory-startup \
    --python-exit-code 1 --python "$trial/render_local.py" -- --stills
  printf 'Candidate: %s\n' "$trial"
)
```

Inspect stills at frames 1, 46, 82 and 120 for identity, framing, materials, contacts and motion. If Blender 5.3 API changes break the generator/audit, stop at the failure and patch the new candidate; never reinterpret old verification as a 5.3 pass.

After stills and the audit pass, render frames 1–120 using the copied wrapper's `--frames 1 120` option. Encode with FFmpeg:

```bash
# Set trial to the exact candidate path printed above.
ffmpeg -n -framerate 12 -start_number 1 -i "$trial/output/frames/frame-%04d.png" \
  -frames:v 120 -c:v libx264 -pix_fmt yuv420p "$trial/output/preview.mp4"
ffprobe -v error -count_frames -select_streams v:0 \
  -show_entries stream=codec_name,width,height,r_frame_rate,nb_read_frames:format=duration \
  -of json "$trial/output/preview.mp4"
```

Expected: H.264, 768 × 432, 12 FPS, 120 decoded frames, 10 seconds. Reopen the saved .blend in Blender 5.3 and verify animation/asset state. Save new audit evidence, logs and first/middle/last previews.

## 7. Controller benchmark and completion

Keep the packaged mcp-for-blender configuration as the initial integration path. Blender 5.3 removes the previous version-based reason for excluding Blenderwright; it does not establish that Blenderwright or Agent Bridge works better. Test alternatives separately against the same S04 candidate only after the initial handshake.

Measure scene inspection, reversible editing, motion, viewport feedback, save/reopen and render/export. Record controller versions, tool calls, elapsed time, failures and corrections. Select a winner from runtime evidence. Blendstra remains the cloud prototype route and Build 3D Game Rooms the environment specialist.

Phase 1 closes after installation, viewport/render gate, Desktop handshake, isolated S04 migration, video verification and recorded visual review. Existing 26 creative skills plus the production orchestrator remain in use; no new character approval or full-chapter production is implied.

## References

- https://www.blender.org/releases/5-3/
- https://download.blender.org/release/Blender5.3/
- https://github.com/ahujasid/mcp-for-blender
- https://github.com/HoldMyBeer-gg/blenderwright
- https://github.com/CallMeJones/blender-agent-bridge
