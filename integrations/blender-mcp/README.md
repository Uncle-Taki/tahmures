# Local read-only Blender HTTP bridge

This is an HTTP adapter, not an MCP server. No ChatGPT, Sites, tunnel, or provider
connection is established by the bridge itself. The optional controller below
can establish a temporary HTTPS tunnel when explicitly activated. Architecture:

ChatGPT Work Web → Sites-hosted MCP plugin → Cloudflare HTTPS tunnel →
127.0.0.1:8765 HTTP bridge → 127.0.0.1:9876 existing Blender add-on.

## Verified installed protocol

Inspected the installed file at
`/home/mehdi/.config/blender/5.3/scripts/addons/blender_mcp.py`, not an upstream
substitute. Its SHA-256 at inspection was
`35e5f317b932d15b485a37d914f7c9d7b527c7ea527f526569c1c111e5f39a05`.
The installed add-on declares version 2.0, protocol 16, on Blender 5.3.0.

`_handle_client` accumulates TCP bytes, UTF-8 decodes them, and calls `json.loads`.
There is no newline, length prefix, HTTP, or MCP framing. Send exactly one JSON
object per connection; do not pipeline. Commands are queued and processed on
Blender's main thread by `_drain_command_queue`.

The two bridge requests are exactly:

```json
{"type":"ping","params":{}}
```

```json
{"type":"get_scene_info","params":{}}
```

The ping branch in `_execute_command_internal` returns:

```json
{"status":"success","result":{"pong":true}}
```

The scene handler returns:

```json
{"status":"success","result":{"name":"Scene","object_count":1,"objects":[{"name":"Cube","type":"MESH","location":[0.0,0.0,0.0]}],"materials_count":0}}
```

`object_count` counts all scene objects, but `objects` lists only the first ten;
locations are local object locations rounded to two decimal places. Materials
count is from `bpy.data.materials`. Errors use
`{"status":"error","message":"..."}`; a scene-handler failure can also be
wrapped as success with `result.error`. Both become generic HTTP 502 errors.
Replies are unframed JSON and the socket remains open. The bridge reads until
one complete JSON value, then closes its own connection; it never waits for EOF
after a valid reply. Incomplete or malformed replies that remain open time out.

The installed dispatcher also exposes commands such as `get_addon_info`,
`get_object_info`, `list_scene_items`, `execute_code`, and `export_scene`, plus
conditional asset/generation commands. **None are exposed by this bridge.**

## API and limits

| GET route | Authentication | Result |
| --- | --- | --- |
| `/healthz` | None | Generic `{"status":"ok"}`; no Blender call |
| `/v1/blender/status` | Bearer | Ping; `{"connected":true}` on success |
| `/v1/blender/scene` | Bearer | Scene result object |

Failures return `{"error":"generic_code"}`: 400 invalid body, 401 authentication,
404 unknown exact route (queries and trailing slashes included), 405 unsupported
method, 431 oversized headers, 502 invalid/error/oversized Blender reply, 503
unavailable/busy Blender, 504 timeout. Unknown HTTP methods receive generic 501.

Only IPv4 loopback is bound. At most 16 HTTP workers run; excess connections are
closed. Header/request-line budget is 8 KiB; request bodies and transfer encoding
are rejected. HTTP reads time out after five seconds. Blender commands are
serialized across bridge requests, with a five-second lock wait and a separate
five-second total socket deadline. TCP input and HTTP output are capped at 1 MiB.
There are no retries. JSON duplicate keys and non-finite constants are rejected.
No CORS headers are emitted. Requests, tokens, upstream exception text, and scene
contents are not logged. HTTP responses disable caching.

The token is loaded once at startup from `BLENDER_BRIDGE_TOKEN_FILE`. It must be
outside this repository, a regular file owned by the current user, with no group
or other permissions, and not a final-component symlink. It contains 32–256 ASCII
letters, digits, `_` or `-`, optionally followed by one newline. Use a randomly
generated token, not a memorable password. Missing/invalid files prevent binding.
Bearer values use `hmac.compare_digest`. Rotation requires restarting the bridge.

## First live test (manual, not run during implementation)

The existing Blender add-on must already be listening at 127.0.0.1:9876.
Do not launch another `mcp-for-blender` process. Create a private external token
once, without printing it or overwriting an existing token:

```bash
/usr/bin/python3 -B - <<'PY'
import os
from pathlib import Path
import secrets
directory = Path.home() / '.config/tahmures-blender-bridge'
directory.mkdir(mode=0o700, parents=True, exist_ok=True)
fd = os.open(directory / 'token', os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(fd, 'w') as stream:
    stream.write(secrets.token_urlsafe(32) + '\n')
PY
export BLENDER_BRIDGE_TOKEN_FILE="$HOME/.config/tahmures-blender-bridge/token"
bash integrations/blender-mcp/scripts/run-bridge.sh
```

In another terminal, from the repository root:

```bash
export BLENDER_BRIDGE_TOKEN_FILE="$HOME/.config/tahmures-blender-bridge/token"
bash integrations/blender-mcp/scripts/check-bridge.sh
```

The check script prints only endpoint status codes. Stop the foreground bridge
with Ctrl-C. No service is installed. The scripts do not modify Blender or Codex
configuration. `openapi.yaml` is the HTTP contract for later plugin development.

## Offline verification

```bash
python3 -m py_compile integrations/blender-mcp/bridge/server.py
python3 -m unittest discover -s integrations/blender-mcp/tests -v
bash -n integrations/blender-mcp/scripts/run-bridge.sh
bash -n integrations/blender-mcp/scripts/check-bridge.sh
```

Tests create ephemeral loopback fake TCP/HTTP servers and temporary external test
token files, never contact port 9876, and do not require Blender.

## Remaining boundaries

Serialization covers this bridge, not the independently running Codex MCP client.
The installed add-on may execute an already queued read request after the bridge
times out or its HTTP caller disconnects; the bridge cannot cancel add-on work.
It sends only ping and scene inspection. The installed dispatcher wraps commands
in its existing recorder context; the bridge does not alter that behavior.
No live bridge/Blender test, plugin deployment, HTTPS tunneling, remote identity,
or end-to-end ChatGPT integration is implied by offline tests. Future exposure
needs its own reviewed configuration. Keep port 9876 on localhost.

## Optional Cloudflare proxy controller

The controller is **default OFF**, manual-only, and has no autostart. The bridge,
Blender, Xray/V2RayN, system Redsocks and Docker operate independently of it.
Supported host: Ubuntu 24.04, iptables nf_tables, Linux pidfds, Python 3.12.

```text
cloudflared (exclusive non-login account), IPv4 HTTP/2 TCP:7844
  -> owned NAT OUTPUT jump -> TMB_CF_<caller UID>
  -> REDIRECT to 127.0.0.1:12347 -> owned Redsocks (caller UID)
  -> HTTP CONNECT 127.0.0.1:10808 -> existing Xray -> Cloudflare
remote HTTPS -> cloudflared -> authenticated bridge 127.0.0.1:8765
```

A separate owned filter chain, `TMB_CG_<caller UID>`, rejects direct loopback
connections to `12347` whose conntrack original destination port is `12347`.
Redirected edge connections retain original destination port `7844` and are not
rejected. This is necessary because a direct connection to a transparent proxy
can make it CONNECT back to itself through Xray. **Never probe `12347` with TCP,
curl, nc or a generic readiness checker.** Readiness uses passive socket ownership.
The guard is installed before Redsocks, retained until Redsocks has stopped,
and removed last. The guard was accepted by the live nf_tables kernel after an
explicit TCP protocol constraint was added; edge registration still fails at TLS.

The NAT chain excludes local/private/reserved destinations. Its sole OUTPUT jump
matches the exclusive cloudflared UID and TCP destination port 7844. Xray's UID,
root, UID 1000, the caller UID and shared identities cannot be used for cloudflared.
A busy dedicated account prevents fresh startup. Rule inspection rejects foreign
rules, extra/duplicate references and reordered chains. Cleanup never flushes a
NAT/filter table, OUTPUT, Docker chains, routes, policies, DNS or sysctl.

This is a narrow edge proxy, not all-traffic containment. DNS and Quick Tunnel
HTTPS/443 allocation need ordinary connectivity. The clean cloudflared environment
uses HTTP/2, IPv4, no auto-update and `/dev/null` configuration. No global proxy
variables or Xray settings are changed. V2RayN must support CONNECT to port 7844.
[Cloudflare parameters](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/configure-tunnels/run-parameters/)
and [Redsocks upstream](https://github.com/darkk/redsocks) describe these components.

### Direct edge egress

The default `edge_egress` is `xray`, including for older configuration files
that omit the field. If the existing IPv4 route passes the Cloudflared TLS
reachability gate, stop the controller and verify it is OFF before selecting
`"edge_egress": "direct"`. Set `redsocks` and `firewall` to `false` together.
Keep `cloudflared` and `dedicated_account` true, `autostart` false, and the master
disabled until ready for an explicitly authorized test. Mixed profiles are
rejected. Direct egress uses the host's existing route and sends edge traffic
without Xray. It starts only Cloudflared under the existing dedicated account.

The controller reads the owned firewall state and refuses direct activation
if the old proxy chain, guard, Redsocks record or listener remains. It creates
no firewall rule in direct mode. Start, registration, token enforcement and
verified stop use the same lifecycle. To revert, run `disable` first. Set
`edge_egress` to `xray` and both proxy components to true while disabled.

### Provisioning is separate from activation

Nothing installs packages, creates accounts or enables services automatically.
Review existing resources first; never overwrite an existing binary or reuse an
account without verifying its ownership and exclusive use. Required commands are
`redsocks`, `iptables` (nf_tables), `curl`, `python3`, `sudo`, `ss`, `flock`, `pgrep`.
Use the existing cloudflared binary at `~/.local/bin/cloudflared` if the dedicated
account can execute it. Prefer a separately reviewed root-owned copy at
`/usr/local/libexec/tahmures-cloudflared` over opening home-directory permissions.

Manual provisioning, **only on a fresh host after approval**:

```bash
sudo apt install redsocks iptables curl python3 util-linux procps
# Only if this account does not already exist:
sudo useradd --system --user-group --no-create-home \
  --home-dir /nonexistent --shell /usr/sbin/nologin tahmures-cloudflared
# Only if this path does not already exist:
sudo install -o root -g root -m 755 "$HOME/.local/bin/cloudflared" \
  /usr/local/libexec/tahmures-cloudflared
```

Package installation can start the distribution Redsocks service. That service is
unrelated and must not be stopped or modified. Reserve `12347` for the integration;
its config is never `/etc/redsocks.conf`. Record newly created account UID/GID and
binary hash in a provisioning receipt outside Git before later deprovisioning.
The current host's legacy resources have **no verified provisioning receipt**;
the controller deliberately will not delete them automatically.

### Configuration and effective configuration

All activation switches live in the private external JSON file
`~/.config/tahmures-blender-bridge/cloudflare-proxy.json`. No secrets belong there.
Missing configuration means OFF. `init-config` creates it exclusively and refuses
to overwrite anything:

```bash
bash integrations/blender-mcp/scripts/cloudflare-proxy.sh init-config
bash integrations/blender-mcp/scripts/cloudflare-proxy.sh config
```

Defaults:

```json
{
  "enabled": false,
  "cloudflared": true,
  "redsocks": true,
  "firewall": true,
  "dedicated_account": true,
  "autostart": false,
  "edge_wait_seconds": 90,
  "edge_egress": "xray"
}
```

The component switches enforce the chosen egress profile. Both profiles require
Cloudflared and its dedicated account. The Xray profile requires Redsocks and
the integration firewall rules, while direct requires both switches OFF.
Autostart must always be false.
The edge wait accepts integer seconds 1–300. Unknown/duplicate keys, strings instead
of booleans, unsafe file ownership/mode and symlinks fail validation. JSON is never
sourced as shell code. Writes are atomic; configuration creation is exclusive.

Ports, origin and transport form a fixed validated safety profile displayed by
`config`; arbitrary origin/port changes are deliberately unsupported. The legacy
`cloudflared.path` file remains a compatibility input for the executable path:
place one absolute path there if using the administrator-installed binary. `config`
shows the resolved effective executable, chains, directories and safety profile.
Do not change the binary path, account identity or managed Redsocks file while
process records or rules exist: stop first. Config errors never prevent `stop`.

### Runtime activation, pause and disabling

Run as the normal user; the controller requests sudo only for inspection, firewall
operations and the dedicated account. No sudoers changes are installed.
Start the existing Blender add-on, bridge and V2RayN independently first.

```bash
bash integrations/blender-mcp/scripts/cloudflare-proxy.sh config
bash integrations/blender-mcp/scripts/cloudflare-proxy.sh enable
bash integrations/blender-mcp/scripts/cloudflare-proxy.sh --dry-run start
bash integrations/blender-mcp/scripts/cloudflare-proxy.sh start
bash integrations/blender-mcp/scripts/cloudflare-proxy.sh status
bash integrations/blender-mcp/scripts/cloudflare-proxy.sh stop
# Stop, verify cleanup, and also revoke permission for future manual start:
bash integrations/blender-mcp/scripts/cloudflare-proxy.sh disable
```

`enable` changes only activation permission; it launches nothing. `stop` means
runtime OFF: recorded processes stopped, owned NAT rules and loop guard absent.
It retains permission for a later manual start. `disable` first performs that
verified stop, then saves master OFF. Merely editing `enabled` to false does not
stop a running tunnel. Reboot has no automatic activation even if permission is ON.

`start` verifies dependencies, dedicated UID, proxy TCP listener, bridge `/healthz`,
Redsocks syntax and passive socket ownership. It installs guard, starts Redsocks,
installs NAT, then starts cloudflared. A successful startup requires a running
recorded process and an observed `Registered tunnel connection` before the deadline.
A Quick Tunnel URL alone is insufficient. Failure or interruption rolls back owned
resources. Repeated start verifies the full runtime; legacy runtimes missing the
new guard must be stopped before reactivation. Start/stop/disable/uninstall share a
lock. No background supervisor or service is installed.

`status` is read-only and never prompts for sudo. It distinguishes configuration,
process identity, exact firewall state, proxy TCP availability, bridge health,
registration evidence and external reachability. An observed registration is
historical evidence in the current log, not a current reachability guarantee.
Unknown sudo permissions remain unknown. For full status, authenticate sudo first
in the same terminal. Status never contacts the transparent listener. `--dry-run`
for any action performs no writes, probes, sudo or firewall commands and prints a
plan; it does not prove the host is ready.

The URL exposes `/healthz` publicly. Blender routes still require the existing
external bearer token. Never expose `9876`, print tokens, put them in command
arguments, or save them in Git. Verify public health, missing-token HTTP 401, and an
authenticated remote status request after actual registration. Quick Tunnels are
[temporary](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/trycloudflare/).

### Runtime files and recovery

| External resource | Lifetime / ownership |
| --- | --- |
| `~/.config/tahmures-blender-bridge/cloudflare-proxy.json` | Activation permission; private user file |
| Same directory: `cloudflared.path` | Legacy executable path; preserved |
| Same directory: `redsocks.conf` | Generated only when absent; mismatches refused |
| Same directory: `token` | Bridge secret; never read/removed by controller |
| `~/.local/state/tahmures-blender-bridge/cloudflare-proxy/` | Lock, process JSON records and logs |
| `TMB_CF_<UID>` in NAT | Exact commented TCP7844 redirect, runtime only |
| `TMB_CG_<UID>` in filter | Exact commented loop prevention guard, runtime only |

Process identity includes boot ID, PID, start time, executable, full argument list,
UID and pidfds. A recycled/old-boot PID is not signalled. Uninspectable or mismatched
records are retained. No broad kill command is used. Logs are replaced on fresh
activation, so preserve needed diagnostics before restarting.

After reboot, crash or SIGKILL, run `stop` before start. Fully verified stale records
are discarded without signals. Exact tagged ordered prefixes left by interrupted
NAT deletion can be removed if no OUTPUT reference remains. Empty orphan chains,
foreign references and other ambiguous state require operator ownership review;
the script fails without deleting it. Failed shutdown retains guard/listener if
needed and never claims OFF. There is no automatic cleanup at reboot, firewall
persistence installation, timer or autostart. An independent administrator saving
runtime rules could persist them; that is outside this controller.

### Full removal and deprovisioning

1. Review `--dry-run uninstall`, then use `uninstall --confirm-uninstall` to verify
   runtime OFF, revoke activation permission and remove the exact generated
   Redsocks configuration and central JSON. Modified configuration is retained
   with an error. Logs, lock, bridge token and legacy path file remain.
2. Review a provisioning receipt and live UID processes, groups, executable hash,
   all references and firewall state before removing persistent host resources.
   Only if created solely for this integration and unchanged: remove the dedicated
   binary, then `sudo userdel tahmures-cloudflared` and its unused dedicated group.
   Never use `userdel -r` (home is `/nonexistent`) or remove a pre-existing account.
3. Remove the legacy `cloudflared.path` only if integration-owned. Preserve the
   original `~/.local/bin/cloudflared`, packages, `/etc/redsocks.conf`, bridge token,
   V2RayN, Xray, Blender, Docker and unrelated rules. Review logs before explicitly
   removing individual files and the now-empty state directory with `rmdir`.
   Never recursively delete the parent config/state directories or user data.

The legacy account/binary cannot currently be proven controller-created. Automatic
host deprovisioning is intentionally unavailable until ownership is established.
Stopping a tunnel never uninstalls dependencies. Full host removal needs separate
approval and leaves the local bridge functional.

### Verification and live-test approval boundary

```bash
make test-blender-integration PYTHON=.venv/bin/python
make check PYTHON=.venv/bin/python
```

Controller tests use fake NAT/filter tables with unrelated Docker rules and stubbed
privileged commands. Bridge tests use ephemeral loopback fixtures only. No test
activates the live controller. Tests cover lifecycle, rollback, interruptions,
foreign rules, original-port guard construction, stale/reused/old-boot PIDs,
configuration rejection and identity errors. They do not prove kernel conntrack
behavior, host firewall coexistence or actual Cloudflare registration.

See `TAHMURES_CODEX_HANDOFF.md` for current audit evidence and the bounded live
operation plan. Live rule/process changes, account provisioning and host removals
require explicit approval. Acceptance remains pending until real registration,
authenticated remote access, no loop/exhaustion, and verified OFF baseline are all
observed on the host.
