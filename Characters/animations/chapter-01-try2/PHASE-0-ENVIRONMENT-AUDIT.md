# Phase 0 — Workstation environment audit

**Audit date:** 2026-11-17  
**Repository:** `Uncle-Taki/tahmures`  
**Branch:** `try2`  
**Scope:** Read-only interpretation of the workstation diagnostics supplied by the owner. No packages, drivers, Blender builds, project files, or local settings were changed by this audit.

## Current follow-up — Blender 5.3 (2026-11-17)

The subsequent owner search found no Blender executable and identified several Tahmures directories. The owner now reports downloading Blender 5.3 into `/home/mehdi/Downloads/Persepolis/Compressed`. Use [BLENDER-5.3-WORKFLOW.md](BLENDER-5.3-WORKFLOW.md) as the active setup sequence. Installing historical 4.3.2 first is unnecessary. Exact archive filename, active Git root, installation and runtime tests remain unverified. Original audit findings below remain evidence at capture time.

## Executive result

**Status: hardware assessment complete; local software and integration preflight incomplete.**

The Ubuntu workstation is suitable for Blender scene authoring, Eevee previewing, procedural modelling, animation blocking, and moderate CPU-rendered work. The detected Intel Iris Xe iGPU supports the reported OpenGL 4.6 environment, but it is not an Intel Arc Xe HPG device supported by Cycles oneAPI GPU rendering. Plan on CPU rendering for Cycles and use the iGPU for display and Eevee.

The diagnostic did not find a `blender` executable in `PATH`, and it was run outside a Git working tree. These observations do **not** prove Blender is absent from the machine or that the local repository is missing; they only mean neither was discoverable from the shell's current command context.

ChatGPT Desktop is installed, but its presence alone does not establish that a local Blender MCP server is configured or connected.

## 1. Captured workstation baseline

| Area | Reported result |
|---|---|
| OS | Ubuntu 24.04.5 LTS |
| Architecture | x86_64 |
| Kernel | 7.0.0-38-generic |
| CPU | 12th Gen Intel Core i5-12500H |
| CPU topology | 16 online logical CPUs; 12 physical cores reported |
| Memory | 38 GiB RAM; 26 GiB available at audit time |
| Swap | 8 GiB configured; unused at audit time |
| Root filesystem | 937 GiB total; 299 GiB available; 67% used |
| GPU | Intel Alder Lake-P GT2 / Iris Xe, PCI ID 8086:46a6 |
| Kernel GPU driver | `i915` |
| OpenGL | 4.6, Mesa 25.2.8, direct rendering enabled |
| Vulkan | 1.4; Intel Iris Xe device enumerated |
| NVIDIA | No NVIDIA GPU detected; `nvidia-smi` cannot communicate with an NVIDIA driver |
| FFmpeg / ffprobe | 6.1.1 |
| Python | 3.12.3 |
| Git | 2.43.0 |
| ChatGPT Desktop | `/usr/bin/chatgpt`, version 26.1007.21434 |
| Blender CLI | `blender` not found in current `PATH` |
| Local repository | Current directory is not inside a Git working tree |

The OpenGL diagnostic's approximately 39.8 GB “video memory” figure is reported as **unified memory**. It must not be treated as 39.8 GB of dedicated VRAM.

## 2. Rendering and authoring implications

### Eevee and viewport

The Intel Mesa driver reports OpenGL 4.6 and accelerated direct rendering. This is above Blender's published Linux OpenGL 4.3 minimum. Eevee and interactive viewport work are therefore reasonable targets, subject to a real Blender launch and scene test.

### Cycles

Blender's Cycles oneAPI backend requires a compatible Intel Arc GPU with Xe HPG architecture. The detected Alder Lake-P Iris Xe integrated GPU is not in that supported Arc A/B-series class. Do not plan on Cycles oneAPI acceleration on this workstation.

**Default strategy:** CPU rendering for Cycles; Intel Iris Xe for viewport and Eevee. A small render benchmark is still required after Blender is located or installed.

### CPU, RAM and storage

The i5-12500H, 38 GiB RAM and 299 GiB free disk provide a workable local development baseline. Keep texture sizes, geometry, simulation caches and render resolution controlled. The shared-memory iGPU and limited integrated graphics throughput make heavy real-time scenes and long high-sample renders less suitable for this machine.

### NVIDIA driver

The `nvidia-smi` failure is expected when no NVIDIA GPU is enumerated. Do not install NVIDIA drivers as a response to this output.

## 3. Existing repository baseline retained

The existing `try2` sample was authored and rendered with Blender 4.3.2. Its committed evidence records a 120-frame, 12 FPS, 10-second, 768 × 432 H.264 sample; 31,139 evaluated triangles; eight animated objects; stationary tablet support; and deterministic sampled seek/reset/replay.

The workstation audit does not invalidate that result. It also does not reproduce it locally, because no Blender executable or local repository path was available in the submitted diagnostics.

Keep the known-good Blender 4.3.2 sample and its native `.blend` file unchanged. Any later Blender version needed for MCP compatibility should be installed side-by-side, not used to overwrite the known-good baseline until a compatibility test passes.

## 4. Tool-integration status

| Requirement | Status | Evidence / limitation |
|---|---|---|
| Linux workstation | Detected | Ubuntu 24.04.5 |
| GPU-backed viewport prerequisites | Promising | OpenGL 4.6, Mesa direct rendering |
| Cycles GPU backend | Not supported by detected GPU | Iris Xe is not a supported Arc Xe HPG device for oneAPI |
| Blender executable/version | Unverified | Not found in current `PATH`; package-manager and alternate-path checks not supplied |
| ChatGPT Desktop installed | Detected | Version 26.1007.21434 |
| Local Blender MCP server | Unverified | No server process, config, or handshake was tested |
| Local `tahmures` working tree | Unverified | Shell was outside a Git repository |
| Local sample rebuild | Not run | Blender CLI and repository path unavailable |
| Local render benchmark | Not run | Requires Blender executable and project checkout |

Installing ChatGPT Desktop is not equivalent to configuring an MCP server. A successful integration test must demonstrate that the client can discover the server, invoke a harmless Blender operation, receive a result, and save or inspect a native Blender artifact.

## 5. Decisions for the next phase

1. Preserve the current remote `try2` branch and existing Blender 4.3.2 source/render evidence.
2. Do not install NVIDIA drivers for this Intel-only GPU.
3. Use Eevee for interactive previews and CPU Cycles as the supported path-tracing baseline.
4. Locate or install Blender without replacing the known-good 4.3.2 environment.
5. Locate the local repository and inspect its branch and uncommitted changes before any local build.
6. Configure and test the chosen MCP server only after the Blender executable and client configuration paths are known.
7. Record a small reproducible render benchmark before deciding whether any cloud-rendering service is needed.

## 6. Remaining Phase 0 checks

Run these from a normal Ubuntu terminal to distinguish “not in PATH” from “not installed” and to locate the local checkout:

```bash
echo "PWD: $PWD"
type -a blender || true
dpkg-query -W -f='${Package} ${Version}\\n' blender 2>/dev/null || true
snap list blender 2>/dev/null || true
flatpak list --app 2>/dev/null | grep -i blender || true

find /opt /usr/local "$HOME" -maxdepth 5 \
  -type f -name blender -executable -print 2>/dev/null | head -n 30

find "$HOME" -maxdepth 5 -type d -name tahmures -print 2>/dev/null | head -n 30
```

Once the repository path is found, inspect it without changing anything:

```bash
git -C "/path/to/tahmures" status --short --branch
git -C "/path/to/tahmures" branch --show-current
git -C "/path/to/tahmures" log -1 --oneline
git -C "/path/to/tahmures" remote -v
```

Do not paste credentials or authenticated remote URLs into the chat.

## 7. References

- Blender system requirements: https://www.blender.org/download/requirements/
- Blender 5.2 Manual, Cycles GPU rendering: https://docs.blender.org/manual/en/5.2/render/cycles/gpu_rendering.html

## Completion gate

Phase 0 is **not fully closed** until Blender's actual version/path, the local repository path/status, and a basic Blender launch/render are verified. MCP connectivity is a separate integration gate and must be tested rather than inferred from the Desktop installation.
