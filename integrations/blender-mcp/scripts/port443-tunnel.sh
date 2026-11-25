#!/usr/bin/env bash
# Zero-sudo port-443 HTTPS tunnel controller for the local Blender HTTP bridge.
# Exposes only 127.0.0.1:8765 (never Blender's 127.0.0.1:9876).
set -euo pipefail
umask 077

BRIDGE_HOST="127.0.0.1"
BRIDGE_PORT="8765"
PROXY_HOST="127.0.0.1"
PROXY_PORT="10808"
TOKEN_FILE="${BLENDER_BRIDGE_TOKEN_FILE:-$HOME/.config/tahmures-blender-bridge/token}"
STATE_DIR="$HOME/.local/state/tahmures-blender-bridge/port443-tunnel"
PID_FILE="$STATE_DIR/ssh.pid"
LOG_FILE="$STATE_DIR/tunnel.log"
PROXY_MODE="http"   # http | socks5 | direct
WAIT_SECONDS="30"

usage() {
  cat <<'USAGE'
Usage: port443-tunnel.sh [--proxy-mode http|socks5|direct] {start|stop|status|test [https-url]|reload [--copy]}

Commands:
  start             Start Pinggy over TCP 443 and print the allocated https:// URL
  stop              Stop only the SSH tunnel started by this script
  status            Read-only check of tunnel, bridge, V2RayN proxy, and active https:// URL
  test [https-url]  Verify /healthz (200), unauth /v1/blender/scene (401), and Bearer-auth routes (200)
  reload [--copy]   Run stop, start, and test; print BLENDER_BRIDGE_URL for ChatGPT Sites
USAGE
}

fail() { printf 'Error: %s\n' "$*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || fail "Missing required command: $1"; }

is_running() {
  [[ -f "$PID_FILE" ]] || return 1
  local pid uid args
  pid="$(tr -d '[:space:]' < "$PID_FILE" 2>/dev/null || true)"
  [[ "$pid" =~ ^[0-9]+$ ]] || return 1
  kill -0 "$pid" 2>/dev/null || return 1
  uid="$(ps -p "$pid" -o uid= 2>/dev/null | tr -d '[:space:]' || true)"
  args="$(ps -p "$pid" -o args= 2>/dev/null || true)"
  [[ "$uid" == "$(id -u)" && "$args" == *"free.pinggy.io"* ]]
}

extract_https_url() {
  [[ -f "$LOG_FILE" ]] || return 1
  LC_ALL=C sed -E \
    -e 's/\x1B\][^\x07\x1B]*(\x07|\x1B\\)//g' \
    -e 's/\x1B\[[0-?]*[ -/]*[@-~]//g; s/\r//g' \
    "$LOG_FILE" \
    | LC_ALL=C awk '
      !found {
        for (i = 1; i <= NF; i++) {
          if ($i ~ /^https:\/\/([a-zA-Z0-9-]+\.)+(pinggy-free\.link|pinggy\.(link|net))$/) {
            print $i
            found = 1
            break
          }
        }
      }
      END { exit !found }
    '
}

check_bridge() {
  curl --noproxy '*' -fsS --max-time 3 "http://${BRIDGE_HOST}:${BRIDGE_PORT}/healthz" >/dev/null 2>&1
}

check_proxy() {
  nc -z -w 2 "$PROXY_HOST" "$PROXY_PORT" >/dev/null 2>&1
}

cmd_start() {
  need ssh; need nc; need curl
  if is_running; then
    printf 'Tunnel already running (PID %s).\n' "$(cat "$PID_FILE")"
    local existing_url
    if existing_url="$(extract_https_url)" && [[ -n "$existing_url" ]]; then
      printf 'HTTPS URL: %s\n' "$existing_url"
    fi
    return 0
  fi

  check_bridge || fail "Blender HTTP bridge is not healthy on ${BRIDGE_HOST}:${BRIDGE_PORT}. Start run-bridge.sh first."
  if [[ "$PROXY_MODE" != "direct" ]]; then
    check_proxy || fail "V2RayN/Xray proxy is not listening on ${PROXY_HOST}:${PROXY_PORT}."
  fi

  install -d -m 700 "$STATE_DIR"
  rm -f "$PID_FILE"
  : > "$LOG_FILE"

  local ssh_cmd=(
    ssh -T -p 443
    -o BatchMode=yes
    -o ConnectTimeout=15
    -o ServerAliveInterval=30
    -o ServerAliveCountMax=3
    -o ExitOnForwardFailure=yes
    -o StrictHostKeyChecking=accept-new
    -R "0:${BRIDGE_HOST}:${BRIDGE_PORT}"
  )

  case "$PROXY_MODE" in
    http)   ssh_cmd+=(-o "ProxyCommand=nc -X connect -x ${PROXY_HOST}:${PROXY_PORT} %h %p") ;;
    socks5) ssh_cmd+=(-o "ProxyCommand=nc -X 5 -x ${PROXY_HOST}:${PROXY_PORT} %h %p") ;;
    direct) ;;
    *)      fail "Invalid --proxy-mode: $PROXY_MODE (expected http, socks5, or direct)" ;;
  esac
  ssh_cmd+=(free.pinggy.io)

  nohup "${ssh_cmd[@]}" </dev/null >"$LOG_FILE" 2>&1 &
  local pid=$!
  printf '%s\n' "$pid" > "$PID_FILE"

  local i url=""
  for ((i = 0; i < WAIT_SECONDS; i++)); do
    if ! kill -0 "$pid" 2>/dev/null; then
      rm -f "$PID_FILE"
      tail -n 20 "$LOG_FILE" >&2 || true
      fail "SSH tunnel exited before allocation. If auth failed, ensure an SSH key exists (ssh-keygen) or try --proxy-mode socks5."
    fi
    url="$(extract_https_url || true)"
    if [[ -n "$url" ]]; then
      printf 'Tunnel active (PID %s, proxy=%s)\n' "$pid" "$PROXY_MODE"
      printf 'HTTPS URL: %s\n' "$url"
      printf 'Logs: %s\n' "$LOG_FILE"
      return 0
    fi
    sleep 1
  done

  cmd_stop >/dev/null 2>&1 || true
  tail -n 20 "$LOG_FILE" >&2 || true
  fail "Timed out waiting ${WAIT_SECONDS}s for Pinggy HTTPS URL."
}

cmd_stop() {
  if ! [[ -f "$PID_FILE" ]]; then
    printf 'Tunnel stopped (no PID file).\n'
    return 0
  fi
  if is_running; then
    local pid
    pid="$(tr -d '[:space:]' < "$PID_FILE")"
    kill "$pid" 2>/dev/null || true
    for _ in 1 2 3 4 5; do
      kill -0 "$pid" 2>/dev/null || break
      sleep 0.5
    done
    if kill -0 "$pid" 2>/dev/null; then
      kill -9 "$pid" 2>/dev/null || true
    fi
    printf 'Tunnel stopped (PID %s terminated).\n' "$pid"
  else
    printf 'Tunnel not running (cleaned stale PID file).\n'
  fi
  rm -f "$PID_FILE"
}

cmd_status() {
  if is_running; then
    printf 'Tunnel: running (PID %s)\n' "$(cat "$PID_FILE")"
    local url
    url="$(extract_https_url || true)"
    printf 'HTTPS URL: %s\n' "${url:-pending}"
  else
    printf 'Tunnel: stopped\n'
    printf 'HTTPS URL: inactive\n'
  fi
  if check_bridge; then
    printf 'Bridge (%s:%s): healthy\n' "$BRIDGE_HOST" "$BRIDGE_PORT"
  else
    printf 'Bridge (%s:%s): unavailable\n' "$BRIDGE_HOST" "$BRIDGE_PORT"
  fi
  if check_proxy; then
    printf 'V2RayN (%s:%s): listening\n' "$PROXY_HOST" "$PROXY_PORT"
  else
    printf 'V2RayN (%s:%s): unavailable\n' "$PROXY_HOST" "$PROXY_PORT"
  fi
}

cmd_test() {
  need python3
  local target_url="${1:-}"
  if [[ -z "$target_url" ]]; then
    is_running || fail "Tunnel is not running. Pass an https:// URL explicitly or run 'start' first."
    target_url="$(extract_https_url || true)"
  fi
  [[ "$target_url" == https://* ]] || fail "Expected an https:// URL (do not use the http:// URL)."
  [[ -r "$TOKEN_FILE" ]] || fail "Token file not readable: $TOKEN_FILE"

  local proxy_env=()
  if [[ "$PROXY_MODE" != "direct" ]]; then
    local purl="http://${PROXY_HOST}:${PROXY_PORT}"
    proxy_env=(
      "HTTP_PROXY=$purl" "HTTPS_PROXY=$purl" "ALL_PROXY=$purl"
      "http_proxy=$purl" "https_proxy=$purl" "all_proxy=$purl"
      "NO_PROXY=localhost,127.0.0.1,::1" "no_proxy=localhost,127.0.0.1,::1"
    )
  fi

  env "${proxy_env[@]}" BLENDER_TUNNEL_URL="$target_url" BLENDER_BRIDGE_TOKEN_FILE="$TOKEN_FILE" \
    python3 - <<'PY'
import json, os
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

base = os.environ["BLENDER_TUNNEL_URL"].rstrip("/")
token = Path(os.environ["BLENDER_BRIDGE_TOKEN_FILE"]).read_text().strip()

def check(path, auth=False):
    headers = {"Authorization": f"Bearer {token}"} if auth else {}
    req = Request(base + path, headers=headers)
    try:
        with urlopen(req, timeout=20) as resp:
            code, body = resp.status, resp.read()
    except HTTPError as err:
        code, body = err.code, err.read()
    if auth and code == 200:
        json.loads(body)
    print(f"{path} (auth={auth}): HTTP {code}")
    return code

assert check("/healthz") == 200
assert check("/v1/blender/scene") == 401
assert check("/v1/blender/status", True) == 200
assert check("/v1/blender/scene", True) == 200
print("REMOTE CONNECTION SUCCESSFUL")
PY
}

copy_url_to_clipboard() {
  local url="$1"
  if [[ -n "${WAYLAND_DISPLAY:-}" ]] && command -v wl-copy >/dev/null 2>&1; then
    if printf '%s' "$url" | wl-copy; then
      printf 'HTTPS URL copied to clipboard.\n' >&2
      return 0
    fi
  fi
  if [[ -n "${DISPLAY:-}" ]] && command -v xclip >/dev/null 2>&1; then
    if printf '%s' "$url" | xclip -selection clipboard; then
      printf 'HTTPS URL copied to clipboard.\n' >&2
      return 0
    fi
  fi
  printf 'Clipboard copy unavailable; continuing without it.\n' >&2
  return 0
}

cmd_reload() {
  local copy=0 arg url
  for arg in "$@"; do
    case "$arg" in
      --copy) copy=1 ;;
      *) fail "Unknown reload option: $arg (use --copy)" ;;
    esac
  done

  cmd_stop
  cmd_start
  url="$(extract_https_url || true)"
  [[ "$url" == https://* ]] || fail 'Could not extract the new Pinggy HTTPS URL after start.'
  cmd_test "$url"
  if (( copy )); then
    copy_url_to_clipboard "$url"
  fi
  printf 'BLENDER_BRIDGE_URL=%s\n' "$url"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --proxy-mode)
      [[ $# -ge 2 ]] || fail "--proxy-mode requires a value (http|socks5|direct)"
      PROXY_MODE="$2"; shift 2 ;;
    -h|--help)
      usage; exit 0 ;;
    start|stop|status|test|reload)
      ACTION="$1"; shift; break ;;
    *)
      fail "Unknown argument: $1 (use --help)" ;;
  esac
done

[[ -n "${ACTION:-}" ]] || { usage; exit 1; }

case "$ACTION" in
  start)  cmd_start ;;
  stop)   cmd_stop ;;
  status) cmd_status ;;
  test)   cmd_test "${1:-}" ;;
  reload) cmd_reload "$@" ;;
esac
