# Blender Bridge Runbook

## Post-Reboot Cold Start

Start the local services in dependency order:

1. Launch Blender 5.3 and enable its bridge listener on `127.0.0.1:9876`.
2. In a terminal, run `bash integrations/blender-mcp/scripts/run-bridge.sh`.
3. Check the local HTTP bridge with `bash integrations/blender-mcp/scripts/check-bridge.sh`.
4. Start V2RayN and confirm its local proxy listens on `127.0.0.1:10808`.
5. Run `bash integrations/blender-mcp/scripts/port443-tunnel.sh start`, then `bash integrations/blender-mcp/scripts/port443-tunnel.sh test`.

## 60-Minute Pinggy Reload

Pinggy's free tunnel URL expires after 60 minutes. Run:

```bash
bash integrations/blender-mcp/scripts/port443-tunnel.sh reload
```

Copy the final `BLENDER_BRIDGE_URL=...` line into `BLENDER_BRIDGE_URL` in ChatGPT Sites, then smoke-test `check_bridge_health` and `get_blender_status`.

## Character-building API

Restart the local HTTP process after updating the bridge. Use `openapi.yaml`
when updating the client’s tools. The existing startup check is read-only.
The new POST routes all require Bearer authentication.

1. `/v1/blender/load-reference` loads an approved image from `Characters/`.
   Switch Blender to front orthographic view to see the reference.
2. `/v1/blender/execute` applies a small batch of guarded modeling code.
3. `/v1/blender/viewport` captures the current 3D view as a base64 PNG. Use it
   to inspect each batch. After a timeout, check the scene before retrying
   because a command already started in Blender may still finish.
4. `/v1/blender/save` writes a copy under `Characters/blender/`. Use a new
   versioned filename if the server returns HTTP 409.

## Clean Shutdown

Stop the public tunnel, then stop the foreground bridge process:

```bash
bash integrations/blender-mcp/scripts/port443-tunnel.sh stop
```

Send Ctrl-C in the terminal running `run-bridge.sh`.
