#!/usr/bin/env bash
# Optional, manually activated Quick Tunnel. Sourcing this file runs no commands.
set -euo pipefail
umask 077

ACCOUNT=tahmures-cloudflared
REDSOCKS_PORT=12347
CONFIG_DIR="${HOME}/.config/tahmures-blender-bridge"
STATE_DIR="${HOME}/.local/state/tahmures-blender-bridge/cloudflare-proxy"
CHAIN="TMB_CF_${UID}"
TAG="tahmures-blender-proxy:${UID}:v1"
EXCLUDED=(0.0.0.0/8 10.0.0.0/8 100.64.0.0/10 127.0.0.0/8 169.254.0.0/16
          172.16.0.0/12 192.0.0.0/24 192.0.2.0/24 192.168.0.0/16
          198.18.0.0/15 198.51.100.0/24 203.0.113.0/24 224.0.0.0/4 240.0.0.0/4)

fail() { printf 'Error: %s\n' "$*" >&2; return 1; }
need() { command -v "$1" >/dev/null || fail "Missing $1; install it manually."; }
ipt() { sudo -n -- iptables -w 5 -t "${FIREWALL_TABLE:-nat}" "$@"; }

configuration() {
    python3 "$(dirname -- "${BASH_SOURCE[0]}")/proxy-config.py" "$CONFIG_DIR/cloudflare-proxy.json" "$@"
}

redsocks_config() {
    cat <<'CONFIG'
// Managed by cloudflare-proxy.sh; independent of /etc/redsocks.conf.
base {
    log_debug = off;
    log_info = on;
    log = "stderr";
    daemon = off;
    redirector = iptables;
}
redsocks {
    local_ip = 127.0.0.1;
    local_port = 12347;
    ip = 127.0.0.1;
    port = 10808;
    type = http-connect;
}
CONFIG
}

# Records include kernel start time and boot ID. pidfds prevent PID-reuse races.
# Records are JSON data, never sourced. Privileged code never opens state files.
process() {
    local mode=$1 record=$2 expected_uid=$3 expected_exe=$4 code
    shift 4
    code=$(cat <<'PY'
import json, os, re, signal, subprocess, sys
mode, record, uid, exe = sys.argv[1:5]
uid = int(uid)
expected_args = sys.argv[5:]
with open("/proc/sys/kernel/random/boot_id") as f:
    boot = f.read().strip()

def identity(pid):
    with open(f"/proc/{pid}/stat") as f:
        fields = f.read().rsplit(") ", 1)[1].split()
    if fields[0] == "Z":
        sys.exit(10)
    with open(f"/proc/{pid}/status") as f:
        line = next(line for line in f if line.startswith("Uid:"))
    return dict(pid=pid, start=fields[19], boot=boot,
                uid=int(line.split()[1]),
                exe=os.readlink(f"/proc/{pid}/exe").removesuffix(" (deleted)"))

def matches(data):
    if data["uid"] != uid or data["exe"] != exe:
        return False
    with open(f"/proc/{data['pid']}/cmdline", "rb") as f:
        return f.read().split(b"\0") == [os.fsencode(arg) for arg in expected_args] + [b""]

def owns_listener(pid, port):
    result = subprocess.run(
        ["ss", "-H", "-ltnp", f"sport = :{port}"],
        capture_output=True, text=True, timeout=2, check=True,
    )
    lines = result.stdout.splitlines()
    if result.stderr or len(lines) != 1:
        return False
    state, _, _, local, _, *owners = lines[0].strip().split(maxsplit=5)
    return (state == "LISTEN" and local == f"127.0.0.1:{port}"
            and len(owners) == 1
            and re.fullmatch(r'users:\(\("redsocks",pid=' + str(pid)
                             + r',fd=\d+\)\)', owners[0]) is not None)

try:
    if mode == "listener":
        listener_port = int(expected_args.pop(0))
    if mode == "record":
        pid = int(expected_args.pop(0))
    else:
        data = json.loads(record)
        pid = data["pid"]
        if (not isinstance(data["start"], str) or not data["start"].isdecimal()
                or not isinstance(data["boot"], str)
                or not re.fullmatch(r"[0-9a-f-]{36}", data["boot"])
                or type(data["uid"]) is not int
                or not isinstance(data["exe"], str) or not os.path.isabs(data["exe"])):
            sys.exit(11)
        if data["boot"] != boot:
            sys.exit(10)
    if type(pid) is not int or pid <= 1:
        sys.exit(11)
    fd = os.pidfd_open(pid)
    try:
        current = identity(pid)
        if mode != "record" and data["start"] != current["start"]:
            sys.exit(10)
        if not matches(current) or (mode != "record" and data != current):
            sys.exit(11)
        if mode == "stop":
            signal.pidfd_send_signal(fd, signal.SIGTERM)
        elif mode == "record":
            print(json.dumps(current))
        elif mode == "listener":
            if not owns_listener(pid, listener_port) or current != identity(pid) or not matches(current):
                sys.exit(11)
        elif mode != "check":
            sys.exit(11)
    finally:
        os.close(fd)
except (FileNotFoundError, ProcessLookupError):
    sys.exit(10)  # Definitely stale or missing; never signal it.
except (OSError, ValueError, KeyError, StopIteration, TypeError, subprocess.SubprocessError):
    sys.exit(11)  # Inspection failed; cleanup must retain state and redirection.
PY
)
    if [[ $expected_uid == "$UID" ]]; then
        python3 -c "$code" "$mode" "$record" "$expected_uid" "$expected_exe" "$@"
    else
        sudo -n -- python3 -c "$code" "$mode" "$record" "$expected_uid" "$expected_exe" "$@"
    fi
}

cloudflared_args=(tunnel --config /dev/null --no-autoupdate --protocol http2
                 --edge-ip-version 4 --url http://127.0.0.1:8765)

managed_process() {
    local name=$1 mode=$2 record=$3 expected_uid=$4 binary=$5
    shift 5
    if [[ $name == redsocks ]]; then
        process "$mode" "$record" "$expected_uid" "$binary" "$@" "$binary" -c "$CONFIG_DIR/redsocks.conf"
    else
        process "$mode" "$record" "$expected_uid" "$binary" "$@" "$binary" "${cloudflared_args[@]}"
    fi
}

load_identity() {
    local entry name password gid gecos home shell
    entry=$(getent passwd "$ACCOUNT") || { fail "Create the dedicated $ACCOUNT account first."; return 1; }
    IFS=: read -r name password CF_UID gid gecos home shell <<< "$entry"
    [[ $CF_UID =~ ^[0-9]+$ && $CF_UID != 0 && $CF_UID != 1000 && $CF_UID != "$UID" ]] ||
        { fail "Unsafe cloudflared UID: $CF_UID"; return 1; }
    [[ $home == /nonexistent && ( $shell == /usr/sbin/nologin || $shell == /bin/false ) ]] ||
        { fail 'Dedicated account must have /nonexistent home and a disabled login shell.'; return 1; }
    [[ $(getent passwd | awk -F: -v u="$CF_UID" '$3 == u {n++} END {print n+0}') == 1 ]] ||
        { fail 'Dedicated UID is shared by multiple accounts.'; return 1; }
}

load_binary() {
    CF_BIN="$HOME/.local/bin/cloudflared"
    if [[ -e $CONFIG_DIR/cloudflared.path ]]; then
        [[ -f $CONFIG_DIR/cloudflared.path && ! -L $CONFIG_DIR/cloudflared.path ]] ||
            fail 'cloudflared.path must be a regular file.'
        CF_BIN=$(cat "$CONFIG_DIR/cloudflared.path")
    fi
    [[ $CF_BIN == /* && $CF_BIN != *$'\n'* ]] || fail 'Use one absolute cloudflared path.'
    CF_BIN=$(readlink -m -- "$CF_BIN")
    RS_BIN=$(command -v redsocks || true)
    if [[ -n $RS_BIN ]]; then RS_BIN=$(readlink -f -- "$RS_BIN"); fi
}

jump_args() {
    JUMP=(-p tcp --dport 7844 -m owner --uid-owner "$CF_UID"
          -m comment --comment "$TAG" -j "$CHAIN")
}

dedicated_idle() {
    local result
    # Root inspection also works on hosts whose /proc hides other users' PIDs.
    # Capture the command status directly, rather than the enclosing if status.
    if sudo -n -- pgrep -u "$CF_UID" >/dev/null; then return 1
    else result=$?; fi
    [[ $result == 1 ]] || { fail 'Cannot inspect dedicated-account processes.'; return 1; }
}

CHAIN_SIZE=$(( ${#EXCLUDED[@]} + 2 ))
NEW_CHAIN=0
ADDED_RULES=0
ADDED_JUMP=0

chain_rule() {
    local index=$1
    if ((index == 0)); then
        RULE=(-m addrtype --dst-type LOCAL -m comment --comment "$TAG" -j RETURN)
    elif ((index < CHAIN_SIZE - 1)); then
        RULE=(-d "${EXCLUDED[index - 1]}" -m comment --comment "$TAG" -j RETURN)
    else
        RULE=(-p tcp -m tcp --dport 7844 -m comment --comment "$TAG" -j REDIRECT --to-ports "$REDSOCKS_PORT")
    fi
}

# Take one complete snapshot. Check the chain's ordered rules and every reference
# to it, including gotos from foreign chains. Only an exact, single jump is allowed.
inspect_firewall() {
    local snapshot line index=0 expected_jump
    CHAIN_PRESENT=0
    JUMP_PRESENT=0
    CHAIN_RULES=0
    jump_args
    expected_jump="-A OUTPUT -p tcp -m tcp ${JUMP[*]:2}"
    if [[ ${FIREWALL_TABLE:-nat} == filter ]]; then
        expected_jump="-A OUTPUT -d 127.0.0.1/32 -p tcp -m tcp ${JUMP[*]:4}"
    fi
    snapshot=$(ipt -S) || return 1
    while IFS= read -r line; do
        line=${line//\"$TAG\"/$TAG}
        case $line in
            "-N $CHAIN") CHAIN_PRESENT=1 ;;
            "-A $CHAIN "*)
                ((index < CHAIN_SIZE)) || return 1
                chain_rule "$index"
                [[ $line == "-A $CHAIN ${RULE[*]}" ]] || return 1
                index=$((index + 1)) ;;
        esac
        if [[ $line =~ [[:space:]](-j|-g|--jump|--goto)[[:space:]]$CHAIN($|[[:space:]]) ]]; then
            [[ $line == "$expected_jump" && $JUMP_PRESENT == 0 ]] || return 1
            JUMP_PRESENT=1
        fi
    done <<< "$snapshot"
    CHAIN_RULES=$index
    (( CHAIN_PRESENT || (CHAIN_RULES == 0 && JUMP_PRESENT == 0) ))
}

firewall_active() { chain_matches && (( JUMP_PRESENT )); }

chain_matches() {
    inspect_firewall && (( CHAIN_PRESENT && CHAIN_RULES == CHAIN_SIZE ))
}

require_clear_firewall() {
    if inspect_firewall && (( ! CHAIN_PRESENT && ! JUMP_PRESENT )); then
        return 0
    fi
    fail "Firewall state for $CHAIN is existing or unverifiable. Run 'bash ${BASH_SOURCE[0]} stop' to clean up verified stale integration resources."
}

install_firewall() {
    # Recheck after Redsocks starts. Fresh startup never adopts existing rules.
    require_clear_firewall || return 1
    ipt -N "$CHAIN" || return 1
    NEW_CHAIN=1
    while (( ADDED_RULES < CHAIN_SIZE )); do
        chain_rule "$ADDED_RULES"
        ipt -A "$CHAIN" "${RULE[@]}" || return 1
        ADDED_RULES=$((ADDED_RULES + 1))
    done
    ipt -I OUTPUT 1 "${JUMP[@]}" || return 1
    ADDED_JUMP=1
    chain_matches && (( JUMP_PRESENT ))
}

delete_chain_rules() {
    local index=$1
    while (( index > 0 )); do
        index=$((index - 1))
        chain_rule "$index"
        ipt -D "$CHAIN" "${RULE[@]}" || return 1
    done
    ipt -X "$CHAIN"
}

remove_firewall() {
    inspect_firewall || { fail "Cannot verify $CHAIN ownership; firewall retained."; return 1; }
    if (( ! CHAIN_PRESENT )); then return 0; fi
    (( CHAIN_RULES == CHAIN_SIZE || (CHAIN_RULES > 0 && ! JUMP_PRESENT) )) ||
        { fail "Unverifiable incomplete $CHAIN; firewall retained."; return 1; }
    if (( JUMP_PRESENT )); then ipt -D OUTPUT "${JUMP[@]}" || return 1; fi
    delete_chain_rules "$CHAIN_RULES" || return 1
    inspect_firewall && (( ! CHAIN_PRESENT ))
}

rollback_firewall() {
    inspect_firewall || { fail "Cannot verify $CHAIN ownership; firewall retained."; return 1; }
    if (( ! NEW_CHAIN )); then
        if (( JUMP_PRESENT )); then
            fail "An existing redirect to Redsocks remains; retaining its listener."
            return 1
        fi
        return 0
    fi
    (( CHAIN_PRESENT && CHAIN_RULES == ADDED_RULES && JUMP_PRESENT == ADDED_JUMP )) ||
        { fail "Firewall changed during startup; firewall retained."; return 1; }
    if (( ADDED_JUMP )); then ipt -D OUTPUT "${JUMP[@]}" || return 1; fi
    delete_chain_rules "$ADDED_RULES" || return 1
    inspect_firewall && (( ! CHAIN_PRESENT && ! JUMP_PRESENT ))
}

# A direct connection to a transparent listener has itself as SO_ORIGINAL_DST.
# Refuse it before accept, so an accidental probe cannot ask Xray to CONNECT
# back to Redsocks. NAT-redirected connections retain original dport 7844.
# Reuse the same exact-ownership inspection for a separate filter chain.
guard_firewall() (
    FIREWALL_TABLE=filter
    CHAIN="TMB_CG_${UID}"
    TAG="tahmures-blender-guard:${UID}:v1"
    CHAIN_SIZE=1
    NEW_CHAIN=0 ADDED_RULES=0 ADDED_JUMP=0
    jump_args() {
        JUMP=(-d 127.0.0.1/32 -p tcp --dport "$REDSOCKS_PORT"
              -m comment --comment "$TAG" -j "$CHAIN")
    }
    chain_rule() {
        RULE=(-p tcp -m conntrack --ctorigdstport "$REDSOCKS_PORT"
              -m comment --comment "$TAG" -j REJECT --reject-with tcp-reset)
    }
    if [[ $1 == install_firewall ]]; then
        if install_firewall; then return 0; fi
        rollback_firewall || fail 'Guard rollback incomplete; inspect filter table.'
        return 1
    fi
    "$@"
)

proxy_ready() {
    python3 - <<'PY'
import socket, sys
try:
    with socket.create_connection(("127.0.0.1", 10808), timeout=2):
        pass
except OSError:
    sys.exit(1)
PY
}

redsocks_port_free() {
    local listeners
    listeners=$(ss -H -ltn "sport = :$REDSOCKS_PORT" 2>&1) ||
        { fail "Cannot inspect listeners on port $REDSOCKS_PORT."; return 1; }
    [[ -z $listeners ]] || fail "Port $REDSOCKS_PORT has an existing listener or inspection was ambiguous."
}

redsocks_ready() {
    local record
    record=$(cat "$STATE_DIR/redsocks.pid") || return 1
    managed_process redsocks listener "$record" "$UID" "$RS_BIN" "$REDSOCKS_PORT"
}

bridge_ready() {
    curl --noproxy '*' --fail --silent --max-time 3 http://127.0.0.1:8765/healthz >/dev/null
}

record_running() {
    local name=$1 expected_uid=$2 binary=$3
    [[ -f $STATE_DIR/$name.pid ]] &&
        managed_process "$name" check "$(cat "$STATE_DIR/$name.pid")" "$expected_uid" "$binary"
}

stop_process() {
    local name=$1 expected_uid=$2 binary=$3 record i result
    [[ -f $STATE_DIR/$name.pid ]] || return 0
    record=$(cat "$STATE_DIR/$name.pid")
    if managed_process "$name" check "$record" "$expected_uid" "$binary"; then
        managed_process "$name" stop "$record" "$expected_uid" "$binary" || return 1
        for ((i=0; i<160; i++)); do
            if managed_process "$name" check "$record" "$expected_uid" "$binary"; then :
            else
                result=$?
                [[ $result == 10 ]] || { fail "Cannot inspect $name; state retained."; return 1; }
                break
            fi
            sleep 0.25
        done
        if managed_process "$name" check "$record" "$expected_uid" "$binary"; then
            fail "$name did not exit after SIGTERM; retaining its record and firewall."
            return 1
        else
            result=$?
            [[ $result == 10 ]] || { fail "Cannot confirm $name exit; state retained."; return 1; }
        fi
    else
        result=$?
        [[ $result == 10 ]] || { fail "Cannot inspect $name; state retained."; return 1; }
        printf '%s: stale record; no signal sent.\n' "$name"
    fi
    rm -f -- "$STATE_DIR/$name.pid"
}

edge_registered() {
    [[ -f $STATE_DIR/cloudflared.log ]] || return 1
    # Observation only: this is not a current external reachability guarantee.
    grep -q 'Registered tunnel connection' "$STATE_DIR/cloudflared.log"
}

show_url() {
    local url
    [[ -f $STATE_DIR/cloudflared.log ]] || return 1
    url=$(grep -Eo 'https://[a-z0-9]+(-[a-z0-9]+)*\.trycloudflare\.com' "$STATE_DIR/cloudflared.log" | head -n 1) || return 1
    [[ -n $url ]] || return 1
    printf 'Quick Tunnel URL (allocation does not prove readiness): %s\n' "$url"
}

stop_all() {
    local mode=${1:-stop} result
    if record_running redsocks "$UID" "$RS_BIN"; then :
    else
        result=$?
        if [[ -f $STATE_DIR/redsocks.pid && $result != 10 ]]; then
            fail 'Cannot verify the recorded Redsocks process; retaining firewall and processes.'
            return 1
        fi
        redsocks_port_free || return 1
    fi
    # Retain redirection if cloudflared cannot be stopped, avoiding proxy bypass.
    if [[ ! -f $STATE_DIR/cloudflared.pid ]] && ! dedicated_idle; then
        fail 'Unrecorded process under dedicated account; retaining firewall and redsocks for inspection.'
        return 1
    fi
    stop_process cloudflared "$CF_UID" "$CF_BIN" || return 1
    if ! dedicated_idle; then
        fail 'Dedicated account still has processes; retaining firewall and redsocks.'
        return 1
    fi
    if [[ $mode == rollback ]]; then
        rollback_firewall || return 1
    else
        remove_firewall || return 1
    fi
    stop_process redsocks "$UID" "$RS_BIN" || return 1
    redsocks_port_free || return 1
    if [[ $mode != rollback || ${GUARD_CREATED:-0} == 1 ]]; then
        guard_firewall remove_firewall || return 1
    fi
}

start_controller() {
    local i pid record cloudflared_running=0 egress=${EDGE_EGRESS:-xray}
    need curl; need sudo; need iptables; need flock; need ss
    if [[ $egress == xray ]]; then need redsocks; fi
    load_identity
    load_binary
    [[ -x $CF_BIN ]] || fail "Cloudflared executable missing: $CF_BIN"
    sudo -v
    sudo -n -- iptables --version | grep -q nf_tables || fail 'Expected iptables nf_tables backend.'
    if record_running cloudflared "$CF_UID" "$CF_BIN"; then
        cloudflared_running=1
    else
        require_clear_firewall || return 1
    fi
    if [[ $egress == xray ]]; then
        proxy_ready || fail 'V2RayN HTTP proxy is not accepting connections at 127.0.0.1:10808.'
    else
        require_clear_direct_path || return 1
    fi
    bridge_ready || fail 'Bridge health check failed at 127.0.0.1:8765/healthz.'
    if (( cloudflared_running )); then
        if [[ $egress == xray ]]; then
            redsocks_ready && chain_matches && (( JUMP_PRESENT )) &&
                guard_firewall firewall_active || fail 'Partly active; run stop before restarting.'
        fi
        printf 'Controller already running.\n'
        show_url || true
        return
    fi
    dedicated_idle || fail 'Dedicated account is busy or cannot be inspected; inspect/stop it first.'
    if [[ -f $STATE_DIR/cloudflared.pid || -f $STATE_DIR/redsocks.pid ]]; then fail 'Existing process records; run stop first.'; fi
    sudo -n -u "$ACCOUNT" -- test -x "$CF_BIN" || fail 'Dedicated account cannot execute cloudflared; see README.'
    trap 'on_start_exit $?' EXIT
    trap 'exit 130' INT
    trap 'exit 143' TERM
    if [[ $egress == xray ]]; then start_proxy_resources; fi
    launch_cloudflared
}

require_clear_direct_path() {
    [[ ! -e $STATE_DIR/redsocks.pid ]] ||
        { fail 'Prior Redsocks record present; run stop before starting direct.'; return 1; }
    redsocks_port_free && require_clear_firewall && guard_firewall require_clear_firewall
}

start_proxy_resources() {
    local i pid record
    redsocks_port_free || return 1
    guard_firewall require_clear_firewall || return 1
    if [[ -e $CONFIG_DIR/redsocks.conf ]]; then
        cmp -s <(redsocks_config) "$CONFIG_DIR/redsocks.conf" || fail 'Existing redsocks.conf differs; preserve/move it first.'
    else
        redsocks_config > "$CONFIG_DIR/redsocks.conf"
    fi
    "$RS_BIN" -t -c "$CONFIG_DIR/redsocks.conf"
    guard_firewall install_firewall
    GUARD_CREATED=1
    "$RS_BIN" -c "$CONFIG_DIR/redsocks.conf" > "$STATE_DIR/redsocks.log" 2>&1 9>&- &
    pid=$!
    RS_PENDING_PID=$pid
    # The forked Bash child may not have exec'd yet; allow that short transition.
    for ((i=0; i<20; i++)); do
        if record=$(managed_process redsocks record unused "$UID" "$RS_BIN" "$pid"); then
            printf '%s\n' "$record" > "$STATE_DIR/redsocks.pid"
            RS_PENDING_PID=
            break
        fi
        sleep 0.1
    done
    [[ -s $STATE_DIR/redsocks.pid ]] || fail 'Redsocks exited before recording; see redsocks.log.'
    for ((i=0; i<20; i++)); do
        if redsocks_ready; then break; fi
        sleep 0.25
    done
    redsocks_ready || fail 'Cannot verify the Redsocks listening socket.'
    install_firewall
}

launch_cloudflared() {
    local i pid record
    # Capture the shell PID that exec becomes, never the sudo launcher PID.
    # Logs are opened by the caller, never by a privileged process.
    CF_LAUNCHED=1
    sudo -n -u "$ACCOUNT" -- /bin/sh -c '
        printf "controller-pid=%s\n" "$$"
        exec /usr/bin/env -i HOME=/nonexistent PATH=/usr/bin:/bin "$@"
    ' sh "$CF_BIN" "${cloudflared_args[@]}" \
        > "$STATE_DIR/cloudflared.log" 2>&1 9>&- &
    CF_LAUNCHER_PID=$!
    for ((i=0; i<40; i++)); do
        pid=$(sed -n 's/^controller-pid=\([0-9][0-9]*\)$/\1/p' "$STATE_DIR/cloudflared.log" | head -n 1)
        if [[ -n $pid ]]; then
            if record=$(managed_process cloudflared record unused "$CF_UID" "$CF_BIN" "$pid"); then
                printf '%s\n' "$record" > "$STATE_DIR/cloudflared.pid"
                break
            fi
        fi
        sleep 0.25
    done
    [[ -s $STATE_DIR/cloudflared.pid ]] || fail 'Cloudflared did not start; see cloudflared.log.'
    for ((i=0; i<${EDGE_WAIT_SECONDS:-90}; i++)); do
        record_running cloudflared "$CF_UID" "$CF_BIN" || fail 'Cloudflared exited; see cloudflared.log.'
        if edge_registered; then break; fi
        sleep 1
    done
    edge_registered || fail 'No registered edge connection before deadline; rolling back.'
    show_url || true
    printf 'Controller active; registered edge observed; logs: %s\n' "$STATE_DIR"
    printf 'Remote reachability still requires an external authenticated check.\n'
    trap - EXIT INT TERM
}

on_start_exit() {
    local result=$1 pending record
    trap - EXIT INT TERM
    if ((result != 0)); then
        printf 'Start failed; cleaning up owned resources.\n' >&2
        # Capture children that reached exec just as an interrupt/failure arrived.
        if [[ -n ${RS_PENDING_PID:-} && ! -s $STATE_DIR/redsocks.pid ]]; then
            if record=$(managed_process redsocks record unused "$UID" "$RS_BIN" "$RS_PENDING_PID"); then
                printf '%s\n' "$record" > "$STATE_DIR/redsocks.pid"
            elif kill -0 "$RS_PENDING_PID" 2>/dev/null; then
                printf 'Redsocks launch identity uncertain; retaining state for inspection.\n' >&2
                exit "$result"
            fi
        fi
        if [[ ${CF_LAUNCHED:-0} == 1 && ! -s $STATE_DIR/cloudflared.pid ]]; then
            pending=$(sed -n 's/^controller-pid=\([0-9][0-9]*\)$/\1/p' "$STATE_DIR/cloudflared.log" | head -n 1)
            if [[ -n $pending ]] && record=$(managed_process cloudflared record unused "$CF_UID" "$CF_BIN" "$pending"); then
                printf '%s\n' "$record" > "$STATE_DIR/cloudflared.pid"
            elif [[ -z ${CF_LAUNCHER_PID:-} ]] ||
                kill -0 "$CF_LAUNCHER_PID" 2>/dev/null || ! dedicated_idle; then
                printf 'Cloudflared launch identity uncertain; retaining firewall and redsocks. Run stop after inspecting the dedicated account.\n' >&2
                exit "$result"
            fi
        fi
        stop_all rollback || printf 'Cleanup incomplete; run stop and inspect retained state.\n' >&2
    fi
    exit "$result"
}

status_controller() {
    local label
    printf 'Configuration (does not imply runtime OFF):\n'
    configuration show || printf 'Configuration: INVALID; stop remains available.\n'
    load_binary
    if ! load_identity; then
        printf 'Dedicated identity unavailable/unsafe; cloudflared and firewall inspection skipped.\n'
        if record_running redsocks "$UID" "$RS_BIN"; then printf 'redsocks: running\n'; else printf 'redsocks: stopped/stale or inspection unavailable\n'; fi
        if proxy_ready; then printf 'V2RayN: TCP listener available\n'; else printf 'V2RayN: unavailable\n'; fi
        printf 'Tunnel URL: unavailable\n'
        return
    fi
    for label in redsocks cloudflared; do
        if [[ $label == redsocks ]]; then
            if record_running "$label" "$UID" "$RS_BIN"; then printf 'redsocks: running\n'; else printf 'redsocks: stopped/stale or inspection unavailable\n'; fi
        else
            if record_running "$label" "$CF_UID" "$CF_BIN"; then printf 'cloudflared: running\n'; else printf 'cloudflared: stopped/stale or inspection unavailable\n'; fi
        fi
    done
    jump_args
    if ! ipt -S >/dev/null 2>&1; then
        printf 'Firewall: unknown (read permission unavailable; status never prompts for sudo)\n'
    elif chain_matches >/dev/null 2>&1 && (( JUMP_PRESENT )); then
        printf 'Firewall: controller chain and OUTPUT jump present\n'
    elif ipt -S "$CHAIN" >/dev/null 2>&1; then
        printf 'Firewall: partial/conflicting controller chain\n'
    else
        printf 'Firewall: controller chain absent\n'
    fi
    if guard_firewall firewall_active >/dev/null 2>&1; then
        printf 'Loop guard: verified chain and OUTPUT jump\n'
    else printf 'Loop guard: absent/conflicting or inspection unavailable\n'; fi
    if edge_registered && record_running cloudflared "$CF_UID" "$CF_BIN"; then
        printf 'Edge: registration observed in current process log; current reachability unverified\n'
    else printf 'Edge: no verified running process with registration evidence\n'; fi
    printf 'Remote reachability: not tested by status\n'
    if proxy_ready; then printf 'V2RayN: 127.0.0.1:10808 accepts TCP (not an upstream test)\n';
    else printf 'V2RayN: 127.0.0.1:10808 unavailable\n'; fi
    if bridge_ready; then printf 'Bridge: healthy\n'; else printf 'Bridge: unavailable\n'; fi
    if record_running cloudflared "$CF_UID" "$CF_BIN"; then show_url || printf 'Tunnel URL: pending\n';
    else printf 'Tunnel URL: inactive (old URL, if any, retained only in log)\n'; fi
}

plan() {
    printf 'DRY RUN: %s; no probes, files, sudo, processes, or firewall commands.\n' "$1"
    printf 'Dedicated account: %s (UID validated at activation; never invoking UID %s or 1000).\n' "$ACCOUNT" "$UID"
    printf 'Config: %s\nState/logs: %s\n' "$CONFIG_DIR" "$STATE_DIR"
    case $1 in
        start)
            printf '%s\n' 'Check enabled configuration, bridge /healthz, dependencies, identity and process records.'
            printf 'Xray profile: check 10808 and free port 12347, install owned guard and %s, then route dedicated UID TCP7844 via Redsocks.\n' "$CHAIN"
            printf '%s\n' 'Direct profile: require proxy records, listener and both owned chains absent; use the existing route without creating rules.'
            printf '%s\n' 'Launch as dedicated account: cloudflared tunnel --config /dev/null --no-autoupdate --protocol http2 --edge-ip-version 4 --url http://127.0.0.1:8765.'
            printf '%s\n' 'Record process identity; require edge registration within deadline; save logs and URL; roll back failures.' ;;
        stop) printf 'Verify/SIGTERM recorded cloudflared; delete exact OUTPUT jump; delete verified %s rules; stop recorded redsocks; remove owned loop guard.\n' "$CHAIN" ;;
        status) printf '%s\n' 'Read configuration, process identities, exact firewall rules, loopback connectivity and registration evidence.' ;;
        config) printf '%s\n' 'Display validated external settings and effective fixed safety profile; no mutation.' ;;
        init-config) printf '%s\n' 'Create private default-OFF JSON exclusively; never overwrite existing data.' ;;
        enable) printf '%s\n' 'Permit manual activation only after all safety components validate; launch nothing.' ;;
        disable) printf '%s\n' 'Verify runtime stop, remove owned NAT and filter rules, then atomically set enabled=false.' ;;
        uninstall) printf '%s\n' 'Requires --confirm-uninstall: verify OFF, disable and remove exact generated config and JSON.' \
            'Retain logs, token and legacy host resources; deprovision only with verified ownership.' ;;
        *) printf '%s\n' 'Review README for configuration or removal semantics; dry-run performs no action.' ;;
    esac
}

main() {
    local action= dry=0 confirm=0 arg directory activation
    for arg in "$@"; do
        case $arg in
            --dry-run) dry=1 ;;
            --confirm-uninstall) confirm=1 ;;
            start|stop|status|config|init-config|enable|disable|uninstall) [[ -z $action ]] || { fail 'Supply one command.'; return 2; }; action=$arg ;;
            *) printf 'Usage: %s [--dry-run] {start|stop|status|config|init-config|enable|disable|uninstall}\n' "$0" >&2; return 2 ;;
        esac
    done
    [[ -n $action ]] || { fail 'Expected one supported command.'; return 2; }
    if ((dry)); then plan "$action"; return; fi
    if [[ $action == uninstall && $confirm == 0 ]]; then
        fail 'Uninstall requires --confirm-uninstall. Review retained host resources and token in README first.'
        return 1
    fi
    ((UID != 0)) || { fail 'Run as your normal user; sudo is requested only where needed.'; return 1; }
    need python3
    if [[ $action == config ]]; then
        configuration show
        load_binary
        printf 'Effective cloudflared executable: %s\n' "$CF_BIN"
        printf 'Effective Redsocks executable: %s\n' "${RS_BIN:-missing}"
        printf 'NAT chain: %s; filter chain: TMB_CG_%s\n' "$CHAIN" "$UID"
        printf 'Config directory: %s\nState directory: %s\n' "$CONFIG_DIR" "$STATE_DIR"
        return
    fi
    if [[ $action == init-config ]]; then configuration init; return; fi
    if [[ $action == status ]]; then status_controller; return; fi
    # Preserve the side-effect-free refusal before creating a lock on first use.
    if [[ $action == start ]]; then
        configuration validate >/dev/null || return 1
    fi
    need flock
    for directory in "$CONFIG_DIR" "$STATE_DIR"; do
        [[ ! -L $directory ]] || { fail "Refusing symlink directory $directory"; return 1; }
        mkdir -p -- "$directory"
        [[ -O $directory ]] || { fail "Directory is not owned by current user: $directory"; return 1; }
        chmod 700 -- "$directory"
    done
    for arg in "$STATE_DIR"/* "$CONFIG_DIR/redsocks.conf"; do
        [[ ! -L $arg ]] || { fail "Refusing symlink $arg"; return 1; }
    done
    exec 9> "$STATE_DIR/controller.lock"
    flock -n 9 || { fail 'Another start/stop is running.'; return 1; }
    if [[ $action == enable ]]; then configuration enable; return; fi
    if [[ $action == start ]]; then
        activation=$(configuration validate) || return 1
        read -r EDGE_WAIT_SECONDS EDGE_EGRESS <<< "$activation"
        start_controller
    else
        load_identity; load_binary; need sudo; need iptables; need ss
        sudo -v
        stop_all
        printf 'Runtime OFF verified: owned processes, NAT redirect and loop guard removed.\n'
        if [[ $action == disable ]]; then configuration disable; fi
        if [[ $action == uninstall ]]; then
            configuration disable
            if [[ -e $CONFIG_DIR/redsocks.conf ]]; then
                cmp -s <(redsocks_config) "$CONFIG_DIR/redsocks.conf" ||
                    { fail 'Modified Redsocks config retained; finish uninstall after review.'; return 1; }
                rm -- "$CONFIG_DIR/redsocks.conf"
            fi
            rm -- "$CONFIG_DIR/cloudflare-proxy.json"
            printf '%s\n' 'Runtime and generated configuration removed. Logs and bridge token retained.' \
                'Legacy account/binary/path file lack an ownership receipt: deprovision only after review (README).'
        fi
    fi
}

if [[ ${BASH_SOURCE[0]} == "$0" ]]; then main "$@"; fi
