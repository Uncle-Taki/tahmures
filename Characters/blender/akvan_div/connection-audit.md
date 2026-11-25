# Connection audit — 2026-11-25

Blender 5.3.0, build 02f0899d78e3 (2026-11-10). Executable `/home/mehdi/opt/blender-5.3.0/blender`, launcher `/home/mehdi/.local/bin/blender-5.3`; running GUI PID 11160 verified via /proc executable. Version command and independent background launch/reopen both succeeded.

Native MCP `mcp-for-blender`: connected, add-on 2.0, protocol 16 matches server. Scene inspection, reviewed Python modeling, and rendered visual inspection succeeded. Telemetry consent false. Active MCP process environments report BLENDER_MCP_SAFE_MODE=1, DISABLE_TELEMETRY=true, BLENDER_HOST=127.0.0.1, BLENDER_PORT=9876. Safe-mode rejection of a binary_path query also confirmed the guard was active; the query was removed rather than relaxing safe mode. Several pre-existing MCP server processes were observed; operations in this task were serialized, no unrelated process was terminated.

Final listeners: Blender 127.0.0.1:9876; authenticated Python bridge 127.0.0.1:8765. No public/LAN bindings or tunnels started. Bridge process PID 84704; foreground service started using existing private token file without displaying its contents. Startup across reboot is not configured or claimed.

| Route | Runtime result |
|---|---|
| GET /healthz | 200, status ok |
| GET /v1/blender/status | 200, connected true |
| GET /v1/blender/scene | 200, real scene response |
| POST /v1/blender/execute | 200, rebuilt Akvan_Eyes_Brows: 88 vertices, 62 faces |
| POST /v1/blender/viewport | 200, actual PNG 800 x 457 |
| POST /v1/blender/load-reference | 200, Akvan_ApprovedMaster loaded using documented schema |
| POST /v1/blender/save | 200, v01 2032881 bytes; v02 2032904 bytes |

## Failures and repairs

The shell sandbox initially prevented host socket inspection; authorized host execution distinguished this from real service failure. Port 9876 and native MCP were healthy, but no bridge listener existed on 8765. Started existing server with its external token configuration. All GET checks then passed.

Guarded modeling initially rejected BMesh `verts.new` / `faces.new`, then `material_index`. Added those narrowly scoped constructors and per-face material property to the existing allowlist without replacing pre-existing bridge edits. Added regression coverage including continued rejection of destructive remove calls. Restarted only the bridge and verified real custom mesh execution afterward. First immediate restart hit address-in-use due to the existing allow_reuse_address=False/TIME_WAIT behavior; retry after cooldown succeeded, without altering that policy.

The first render exposed material indices being clamped when slots were not yet present. Assigned face materials after populating slots and made generated build payloads retain that ordering. First viewport capture showed reference/lights overlays; hid only the reference for inspection and disabled overlays, retaining its packed locked Empty. Corrected a request-helper invocation that supplied an empty file instead of the required JSON object; no bridge fault.

## Discovery diagnosis

This bridge is an HTTP adapter, not an MCP server. Its OpenAPI declares seven operation IDs and server do_POST dispatch registers all four POST paths; runtime HTTP calls succeeded for every path. This Codex session discovers the native mcp-for-blender toolset (including execute_blender_code and look), not a generated seven-tool OpenAPI plugin. No three-GET-only local bridge failure exists. A separate ChatGPT plugin exposing only three tools would need its schema/import/registration refreshed; that separate client configuration was not accessible here and is not claimed repaired. No external plugin, public tunnel or cloud service was needed.

Verification: 42 focused bridge tests passed; full make check passed, including 82 integration tests. Final health check passed after restart and after saving. Service restart persistence verified; reboot persistence not tested.
