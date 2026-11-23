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

## Clean Shutdown

Stop the public tunnel, then stop the foreground bridge process:

```bash
bash integrations/blender-mcp/scripts/port443-tunnel.sh stop
```

Send Ctrl-C in the terminal running `run-bridge.sh`.
