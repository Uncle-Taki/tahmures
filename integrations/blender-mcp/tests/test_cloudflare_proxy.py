"""Offline controller safety tests. No real firewall or sudo commands are used."""

import json
import os
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/cloudflare-proxy.sh"

# Model just the commands exercised by the controller, retaining unrelated rules.
FAKE_FIREWALL = r"""
import json, os, sys
from pathlib import Path
p = Path(os.environ["FAKE_RULES"])
state = json.loads(p.read_text())
args = sys.argv[1:]
op, *args = args

def render(chain):
    if chain != "OUTPUT": print("-N " + chain)
    for item in state[chain]:
        rendered = item.copy()
        if "--dport" in rendered and "-m" not in rendered[:rendered.index("--dport")]:
            i = rendered.index("--dport")
            rendered[i:i] = ["-m", "tcp"]
        print("-A " + chain + " " + " ".join(rendered))

if op == "-S" and not args:
    for chain in state:
        render(chain)
    sys.exit(0)
chain, *rule = args
if op == "-N":
    if chain in state: sys.exit(1)
    state[chain] = []
elif chain not in state:
    sys.exit(1)
elif op == "-S":
    render(chain)
    sys.exit(0)
elif op == "-C":
    sys.exit(0 if rule in state[chain] else 1)
elif op == "-A":
    if len(state[chain]) == int(os.environ.get("FAIL_APPEND_AT", "-1")): sys.exit(2)
    state[chain].append(rule)
elif op == "-I":
    state[chain].insert(int(rule[0]) - 1, rule[1:])
elif op == "-D":
    state[chain].remove(rule)
elif op == "-X":
    if state[chain]: sys.exit(1)
    del state[chain]
else:
    sys.exit(2)
p.write_text(json.dumps(state))
"""


class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.env = dict(os.environ, HOME=str(self.home))
        self.rules = self.home / "rules.json"
        self.initial = {"OUTPUT": [["-j", "DOCKER"]], "DOCKER": [["-j", "RETURN"]]}
        self.rules.write_text(json.dumps(self.initial))
        self.fake = self.home / "firewall.py"
        self.fake.write_text(FAKE_FIREWALL)
        self.env["FAKE_RULES"] = str(self.rules)

    def bash(self, body, *, success=True):
        prefix = f"source {shlex.quote(str(SCRIPT))}\n"
        # Every privileged command must be explicitly stubbed in these tests.
        prefix += "GUARD_FUNCTION=$(declare -f guard_firewall)\n"
        prefix += "guard_firewall() { :; }\n"
        prefix += "sudo() { echo 'UNEXPECTED SUDO' >&2; return 99; }\n"
        result = subprocess.run(
            ["bash", "-c", prefix + body],
            env=self.env,
            text=True,
            capture_output=True,
            check=False,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def firewall_prelude(self):
        return f'CF_UID=991\nipt() {{ python3 {shlex.quote(str(self.fake))} "$@"; }}\n'

    def test_syntax_and_dry_run_without_any_host_commands(self):
        subprocess.run(["bash", "-n", str(SCRIPT)], check=True)
        # No commands except Bash builtins exist in PATH. Dry-run must still work.
        empty_path = self.home / "empty-bin"
        empty_path.mkdir()
        for command in ("start", "stop", "status"):
            result = subprocess.run(
                ["/bin/bash", str(SCRIPT), command, "--dry-run"],
                env=dict(self.env, PATH=str(empty_path)),
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("DRY RUN", result.stdout)
        self.assertFalse((self.home / ".config").exists())
        self.assertFalse((self.home / ".local").exists())

    def test_invalid_arguments_fail_before_commands(self):
        for args in ([], ["restart"], ["start", "stop"], ["--dry-run"]):
            result = subprocess.run(
                ["bash", str(SCRIPT), *args],
                env=self.env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.home / ".config").exists())

    def test_generated_config_matches_example(self):
        result = self.bash("redsocks_config")
        self.assertEqual(result.stdout, (ROOT / "redsocks.conf.example").read_text())

    def test_firewall_install_and_repeated_removal_preserve_docker(self):
        self.bash(self.firewall_prelude() + "install_firewall\nchain_matches")
        state = json.loads(self.rules.read_text())
        self.assertEqual(len(state["OUTPUT"]), 2)
        self.assertEqual(state["OUTPUT"][1], ["-j", "DOCKER"])
        jump = state["OUTPUT"][0]
        self.assertIn("991", jump)
        self.assertEqual(jump[jump.index("--dport") + 1], "7844")
        chain = next(name for name in state if name.startswith("TMB_CF_"))
        self.assertEqual(state[chain][-1][-3:], ["REDIRECT", "--to-ports", "12347"])
        self.assertIn(["-m", "addrtype", "--dst-type", "LOCAL"], [state[chain][0][:4]])
        self.bash(self.firewall_prelude() + "remove_firewall\nremove_firewall")
        self.assertEqual(json.loads(self.rules.read_text()), self.initial)

    def test_foreign_or_reordered_chain_is_preserved(self):
        self.bash(self.firewall_prelude() + "install_firewall")
        state = json.loads(self.rules.read_text())
        chain = next(name for name in state if name.startswith("TMB_CF_"))
        state[chain].insert(0, state[chain].pop())
        self.rules.write_text(json.dumps(state))
        result = self.bash(self.firewall_prelude() + "remove_firewall", success=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(self.rules.read_text()), state)
        result = self.bash(self.firewall_prelude() + "install_firewall", success=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(self.rules.read_text()), state)

    def test_shutdown_refuses_ambiguous_chain_references(self):
        self.bash(self.firewall_prelude() + "install_firewall")
        owned = json.loads(self.rules.read_text())
        jump = owned["OUTPUT"][0]
        chain = jump[-1]
        alternatives = {
            "duplicate": ("OUTPUT", jump),
            "wrong UID": (
                "OUTPUT",
                ["1000" if part == "991" else part for part in jump],
            ),
            "wrong port": (
                "OUTPUT",
                ["443" if part == "7844" else part for part in jump],
            ),
            "wrong tag": (
                "OUTPUT",
                ["foreign" if part.startswith("tahmures-") else part for part in jump],
            ),
            "foreign goto": ("DOCKER", ["-g", chain]),
        }
        for name, (source, rule) in alternatives.items():
            with self.subTest(name=name):
                state = json.loads(json.dumps(owned))
                state[source].append(rule)
                self.rules.write_text(json.dumps(state))
                result = self.bash(
                    self.firewall_prelude() + "remove_firewall", success=False
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(json.loads(self.rules.read_text()), state)

    def test_fresh_start_refuses_stale_or_ambiguous_firewall_before_redsocks(self):
        self.bash(self.firewall_prelude() + "install_firewall")
        owned = json.loads(self.rules.read_text())
        jump = owned["OUTPUT"][0]
        for condition in ("complete", "no jump", "foreign reference"):
            with self.subTest(condition=condition):
                state = json.loads(json.dumps(owned))
                if condition == "no jump":
                    state["OUTPUT"].pop(0)
                elif condition == "foreign reference":
                    state["DOCKER"].append(["-g", jump[-1]])
                self.rules.write_text(json.dumps(state))
                result = self.bash(
                    self.firewall_prelude()
                    + """
RS_BIN=/usr/bin/false; CF_BIN=/usr/bin/true
need() { :; }
load_identity() { :; }
load_binary() { :; }
sudo() {
    case "$*" in
        -v) ;;
        '-n -- iptables --version') echo nf_tables ;;
        *) return 99 ;;
    esac
}
record_running() { return 10; }
redsocks_port_free() { touch "$HOME/unexpected-start"; }
start_controller
""",
                    success=False,
                )
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn(f"Run 'bash {SCRIPT} stop'", result.stderr)
                self.assertIn("verified stale integration resources", result.stderr)
                self.assertFalse((self.home / "unexpected-start").exists())
                self.assertFalse((self.home / ".config").exists())
                self.assertFalse((self.home / ".local").exists())
                self.assertEqual(json.loads(self.rules.read_text()), state)

    def test_rollback_stops_redsocks_only_after_its_redirect_is_gone(self):
        self.bash(self.firewall_prelude() + "install_firewall")
        existing = json.loads(self.rules.read_text())
        for preexisting in (False, True):
            with self.subTest(preexisting=preexisting):
                state = existing if preexisting else self.initial
                self.rules.write_text(json.dumps(state))
                result = self.bash(
                    self.firewall_prelude()
                    + ("" if preexisting else "install_firewall\n")
                    + """
CF_BIN=/missing/cloudflared; RS_BIN=/missing/redsocks
dedicated_idle() { return 0; }
record_running() { [[ $1 == redsocks ]]; }
redsocks_port_free() { :; }
touch "$HOME/redsocks-listening"
stop_process() {
    if [[ $1 == redsocks ]]; then
        touch "$HOME/redsocks-stop-attempted"
        inspect_firewall && (( ! JUMP_PRESENT )) || return 99
        rm "$HOME/redsocks-listening"
    fi
}
trap 'on_start_exit $?' EXIT
exit 42
""",
                    success=False,
                )
                self.assertEqual(result.returncode, 42, result.stderr)
                self.assertEqual(json.loads(self.rules.read_text()), state)
                self.assertEqual(
                    (self.home / "redsocks-listening").exists(), preexisting
                )
                if preexisting:
                    self.assertIn("retaining its listener", result.stderr)
                    self.assertFalse((self.home / "redsocks-stop-attempted").exists())
                else:
                    self.assertNotIn("Cleanup incomplete", result.stderr)
                    self.assertTrue((self.home / "redsocks-stop-attempted").exists())
                    (self.home / "redsocks-stop-attempted").unlink()

    def test_install_refuses_rules_added_after_initial_preflight(self):
        self.bash(self.firewall_prelude() + "install_firewall")
        existing = self.rules.read_text()
        self.rules.write_text(json.dumps(self.initial))
        late_rules = self.home / "late-rules.json"
        late_rules.write_text(existing)
        result = self.bash(
            self.firewall_prelude()
            + """
require_clear_firewall
cp "$HOME/late-rules.json" "$FAKE_RULES"
install_firewall
""",
            success=False,
        )
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(self.rules.read_text(), existing)

    def test_partial_chain_rollback_and_later_recovery(self):
        self.bash(
            self.firewall_prelude()
            + """
export FAIL_APPEND_AT=2
if install_firewall; then exit 80; fi
rollback_firewall
"""
        )
        self.assertEqual(json.loads(self.rules.read_text()), self.initial)

    def test_readonly_status_uses_only_queries_and_does_not_create_state(self):
        self.bash("""
load_identity() { CF_UID=991; }
load_binary() { CF_BIN=/missing/cloudflared; RS_BIN=/missing/redsocks; }
ipt() { [[ $1 == -S ]] || return 99; return 1; }
proxy_ready() { return 1; }
bridge_ready() { return 1; }
status_controller
""")
        self.assertFalse((self.home / ".config").exists())
        self.assertFalse((self.home / ".local").exists())

    def test_unsafe_uids_are_rejected(self):
        for uid in {"0", "1000", str(os.getuid())}:
            entry = f"tahmures-cloudflared:x:{uid}:991::/nonexistent:/usr/sbin/nologin"
            result = self.bash(
                f"getent() {{ printf '%s\\n' {shlex.quote(entry)}; }}\nload_identity",
                success=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unsafe cloudflared UID", result.stderr)

    def test_pid_reuse_record_never_signals_unrelated_process(self):
        child = subprocess.Popen(["/usr/bin/sleep", "60"])

        def cleanup():
            if child.poll() is None:
                child.terminate()
            child.wait(timeout=2)

        self.addCleanup(cleanup)
        # Kernel start-time mismatch models a recycled PID, while that PID exists.
        result = self.bash(f"""
record=$(process record unused "$UID" /usr/bin/sleep {child.pid} /usr/bin/sleep 60)
bad=$(python3 -c '
import json,sys
d=json.loads(sys.argv[1]); d["start"]="0"; print(json.dumps(d))
' "$record")
if process stop "$bad" "$UID" /usr/bin/sleep /usr/bin/sleep 60; then
    exit 80
else [[ $? == 10 ]]; fi
process check "$record" "$UID" /usr/bin/sleep /usr/bin/sleep 60
process stop "$record" "$UID" /usr/bin/sleep /usr/bin/sleep 60
""")
        self.assertEqual(result.returncode, 0)
        child.wait(timeout=2)

    def test_listener_requires_exact_process_and_socket_identity(self):
        with subprocess.Popen(["/usr/bin/sleep", "30"]) as child:
            try:
                transient_bin = self.home / "bin"
                transient_bin.mkdir()
                ss = transient_bin / "ss"
                ss.write_text(
                    "#!/bin/bash\n"
                    "[[ $# == 3 && $1 == -H && $2 == -ltnp ]] || exit 80\n"
                    '[[ $3 == "sport = :12347" ]] || exit 80\n'
                    'printf "%s" "$SS_OUTPUT"\n'
                )
                ss.chmod(0o700)
                self.env["PATH"] = str(transient_bin) + os.pathsep + self.env["PATH"]
                owner = f'("redsocks",pid={child.pid},fd=6)'
                row = f"LISTEN 0 4096 127.0.0.1:12347 0.0.0.0:* users:({owner})"
                body = f"""
record=$(process record unused "$UID" /usr/bin/sleep {child.pid} /usr/bin/sleep 30)
process listener "$record" "$EXPECT_UID" "$EXPECT_EXE" 12347 \\
    /usr/bin/sleep "$EXPECT_ARG"
"""
                cases = {
                    "correct": ({"SS_OUTPUT": row + "  \n"}, 0),
                    "incorrect UID": (
                        {"SS_OUTPUT": row, "EXPECT_UID": str(os.getuid() + 1)},
                        11,
                    ),
                    "unexpected executable": (
                        {"SS_OUTPUT": row, "EXPECT_EXE": "/usr/bin/bash"},
                        11,
                    ),
                    "unexpected command": ({"SS_OUTPUT": row, "EXPECT_ARG": "31"}, 11),
                    "missing listener": ({"SS_OUTPUT": ""}, 11),
                    "missing owner": ({"SS_OUTPUT": row.split(" users:")[0]}, 11),
                    "wrong listener": (
                        {"SS_OUTPUT": row.replace("127.0.0.1:", "0.0.0.0:")},
                        11,
                    ),
                    "multiple owners": (
                        {"SS_OUTPUT": row[:-1] + ',("other",pid=1,fd=8))'},
                        11,
                    ),
                    "multiple listeners": ({"SS_OUTPUT": row + "\n" + row}, 11),
                }
                # Keep the test inside the stub even when testing a different UID.
                body = (
                    """
sudo() {
    [[ $1 == -n && $2 == -- && $3 == python3 ]] || return 99
    shift 2
    "$@"
}
"""
                    + body
                )
                for name, (env, status) in cases.items():
                    with self.subTest(name=name):
                        self.env.update(
                            EXPECT_UID=str(os.getuid()),
                            EXPECT_EXE="/usr/bin/sleep",
                            EXPECT_ARG="30",
                        )
                        self.env.update(env)
                        try:
                            result = self.bash(body, success=False)
                            self.assertEqual(result.returncode, status, result.stderr)
                        finally:
                            for key in env:
                                self.env.pop(key)
            finally:
                child.terminate()

    def test_startup_checks_redsocks_passively(self):
        redsocks = self.home / "redsocks"
        redsocks.write_text("#!/bin/bash\nexit 0\n")
        redsocks.chmod(0o700)
        result = self.bash(
            f"RS_BIN={shlex.quote(str(redsocks))}\n"
            + """
CF_BIN=/usr/bin/true; CF_UID=991
mkdir -p "$STATE_DIR" "$CONFIG_DIR"
need() { :; }
load_identity() { :; }
load_binary() { :; }
proxy_ready() { :; }
bridge_ready() { :; }
dedicated_idle() { :; }
ipt() { [[ $* == -S ]] || return 99; }
sudo() {
    case "$*" in
        -v) ;;
        '-n -- iptables --version') echo nf_tables ;;
        '-n -u tahmures-cloudflared -- test -x /usr/bin/true') ;;
        *) return 99 ;;
    esac
}
# The startup path should only use the passive ss check and the identity helper.
python3() { echo 'UNEXPECTED TCP PROBE' >&2; exit 99; }
ss() {
    [[ $# == 3 && $1 == -H && $2 == -ltn && $3 == 'sport = :12347' ]] || return 99
    touch "$HOME/passive-port-check"
}
managed_process() {
    case "$1 $2" in
        'redsocks record') echo fake-record ;;
        'redsocks listener')
            [[ $3 == fake-record && $4 == "$UID" ]] || return 99
            [[ $5 == "$RS_BIN" && $6 == 12347 ]] || return 99
            echo 'verified listener readiness' >&2 ;;
        *) return 99 ;;
    esac
}
install_firewall() { return 42; }
stop_all() { [[ $1 == rollback ]]; }
start_controller
""",
            success=False,
        )
        self.assertEqual(result.returncode, 42, result.stderr)
        self.assertTrue((self.home / "passive-port-check").exists())
        self.assertIn("verified listener readiness", result.stderr)
        self.assertNotIn("UNEXPECTED TCP PROBE", result.stderr)
        self.assertNotIn("Cleanup incomplete", result.stderr)

    def test_shutdown_stops_only_verified_processes_in_order(self):
        self.bash(
            self.firewall_prelude()
            + """
install_firewall
CF_BIN=/missing/cloudflared; RS_BIN=/missing/redsocks
touch "$HOME/operations"
dedicated_idle() { return 0; }
record_running() { [[ $* == "redsocks $UID $RS_BIN" ]]; }
redsocks_port_free() { :; }
stop_process() {
    if [[ $1 == cloudflared ]]; then
        [[ $2 == "$CF_UID" && $3 == "$CF_BIN" ]] && chain_matches || return 99
    else
        [[ $1 == redsocks && $2 == "$UID" && $3 == "$RS_BIN" ]] || return 99
        inspect_firewall && (( ! CHAIN_PRESENT )) || return 99
    fi
    echo "$1" >> "$HOME/operations"
}
stop_all
[[ $(cat "$HOME/operations") == $'cloudflared\nredsocks' ]]
"""
        )
        self.assertEqual(json.loads(self.rules.read_text()), self.initial)

    def test_stop_retains_firewall_when_inspection_fails(self):
        self.bash("""
mkdir -p "$STATE_DIR"
printf '%s' '{"exe":"/usr/bin/cloudflared"}' > "$STATE_DIR/cloudflared.pid"
CF_UID=991; CF_BIN=/usr/bin/cloudflared; RS_BIN=/usr/bin/redsocks
process() { return 11; }
redsocks_port_free() { return 0; }
remove_firewall() { echo BAD_FIREWALL_CHANGE; return 99; }
if stop_all; then exit 80; fi
[[ -f $STATE_DIR/cloudflared.pid ]]
""")

    def test_unrecorded_dedicated_process_prevents_firewall_removal(self):
        result = self.bash("""
CF_UID=991; CF_BIN=/missing/cloudflared; RS_BIN=/missing/redsocks
dedicated_idle() { return 1; }
redsocks_port_free() { return 0; }
remove_firewall() { echo BAD_FIREWALL_CHANGE; return 99; }
if stop_all; then exit 80; fi
""")
        self.assertNotIn("BAD_FIREWALL_CHANGE", result.stdout)

    def test_failure_cleanup_removes_own_partial_chain(self):
        result = self.bash(
            self.firewall_prelude()
            + """
CF_BIN=/missing/cloudflared; RS_BIN=/missing/redsocks
dedicated_idle() { return 0; }
redsocks_port_free() { return 0; }
trap 'on_start_exit $?' EXIT
export FAIL_APPEND_AT=2
install_firewall
""",
            success=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cleaning up owned resources", result.stderr)
        self.assertEqual(json.loads(self.rules.read_text()), self.initial)

    def test_loop_guard_preserves_other_rules_and_uses_original_destination(self):
        self.bash(
            self.firewall_prelude()
            + 'eval "$GUARD_FUNCTION"\n'
            + "guard_firewall install_firewall\nguard_firewall chain_matches"
        )
        state = json.loads(self.rules.read_text())
        chain = next(name for name in state if name.startswith("TMB_CG_"))
        rule = state[chain][0]
        self.assertEqual(rule[rule.index("--ctorigdstport") + 1], "12347")
        self.assertEqual(rule[:2], ["-p", "tcp"])
        self.assertIn("REJECT", rule)
        self.assertNotIn("991", state["OUTPUT"][0])
        self.assertEqual(state["DOCKER"], self.initial["DOCKER"])
        self.bash(
            self.firewall_prelude()
            + 'eval "$GUARD_FUNCTION"\n'
            + "guard_firewall remove_firewall\nguard_firewall remove_firewall"
        )
        self.assertEqual(json.loads(self.rules.read_text()), self.initial)

    def test_guard_failure_rolls_back_its_own_empty_chain(self):
        self.env["FAIL_APPEND_AT"] = "0"
        self.bash(
            self.firewall_prelude()
            + 'eval "$GUARD_FUNCTION"\n'
            + "if guard_firewall install_firewall; then exit 80; fi"
        )
        self.assertEqual(json.loads(self.rules.read_text()), self.initial)

    def test_shutdown_failure_retains_guard_and_reports_failure(self):
        result = self.bash(
            self.firewall_prelude()
            + """
CF_UID=991; CF_BIN=/missing/cloudflared; RS_BIN=/missing/redsocks
record_running() { [[ $1 == redsocks ]]; }
dedicated_idle() { :; }
stop_process() { [[ $1 == cloudflared ]]; }
guard_firewall() { echo UNEXPECTED_GUARD_REMOVAL; }
stop_all
""",
            success=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("UNEXPECTED_GUARD_REMOVAL", result.stdout)

    def test_partial_shutdown_prefix_recovers_without_touching_docker(self):
        self.bash(self.firewall_prelude() + "install_firewall")
        state = json.loads(self.rules.read_text())
        state["OUTPUT"].pop(0)
        chain = next(name for name in state if name.startswith("TMB_CF_"))
        state[chain] = state[chain][:3]
        self.rules.write_text(json.dumps(state))
        self.bash(self.firewall_prelude() + "remove_firewall")
        self.assertEqual(json.loads(self.rules.read_text()), self.initial)

    def test_url_allocation_is_not_edge_registration(self):
        self.bash("""
mkdir -p "$STATE_DIR"
echo 'https://allocated.trycloudflare.com' > "$STATE_DIR/cloudflared.log"
if edge_registered; then exit 80; fi
show_url
echo 'INF Registered tunnel connection connIndex=0' >> "$STATE_DIR/cloudflared.log"
edge_registered
""")

    def test_central_config_default_off_and_strict_activation(self):
        helper = ROOT / "scripts/proxy-config.py"
        config = self.home / "config/cloudflare-proxy.json"

        def run(action):
            return subprocess.run(
                ["python3", str(helper), str(config), action],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(run("show").returncode, 0)
        self.assertFalse(config.exists())
        self.assertNotEqual(run("validate").returncode, 0)
        self.assertEqual(run("init").returncode, 0)
        self.assertNotEqual(run("init").returncode, 0)
        self.assertFalse(json.loads(config.read_text())["enabled"])
        self.assertEqual(run("enable").returncode, 0)
        self.assertEqual(run("validate").returncode, 0)
        original = config.read_text()
        for key in ("cloudflared", "redsocks", "firewall", "dedicated_account"):
            data = json.loads(original)
            data[key] = False
            config.write_text(json.dumps(data))
            self.assertNotEqual(run("validate").returncode, 0)
        config.write_text(original)
        direct = json.loads(original)
        direct.update(edge_egress="direct", redsocks=False, firewall=False)
        config.write_text(json.dumps(direct))
        self.assertEqual(run("validate").stdout.strip(), "90 direct")
        direct["firewall"] = True
        config.write_text(json.dumps(direct))
        self.assertNotEqual(run("validate").returncode, 0)
        config.write_text(original)
        self.assertEqual(run("disable").returncode, 0)
        self.assertNotEqual(run("validate").returncode, 0)
        for invalid in (
            '{"enabled":true,"enabled":false}',
            "[]",
            "null",
            '{"unknown":"$(touch unexpected)"}',
        ):
            config.write_text(invalid)
            self.assertNotEqual(run("show").returncode, 0)
        config.unlink()
        config.symlink_to(self.rules)
        self.assertNotEqual(run("enable").returncode, 0)
        self.assertEqual(json.loads(self.rules.read_text()), self.initial)

    def test_default_off_start_has_no_side_effects(self):
        result = subprocess.run(
            ["bash", str(SCRIPT), "start"],
            env=self.env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("disabled", result.stderr)
        self.assertFalse((self.home / ".config").exists())
        self.assertFalse((self.home / ".local").exists())

    def lifecycle_prelude(self):
        filter_rules = self.home / "filter.json"
        filter_rules.write_text(json.dumps(self.initial))
        redsocks = self.home / "redsocks"
        redsocks.write_text("#!/bin/bash\nexit 0\n")
        redsocks.chmod(0o700)
        return (
            self.firewall_prelude()
            + 'eval "$GUARD_FUNCTION"\n'
            + f"RS_BIN={shlex.quote(str(redsocks))}\n"
            + f"FILTER_RULES={shlex.quote(str(filter_rules))}\n"
            + f"FAKE_IPT={shlex.quote(str(self.fake))}\n"
            + """
ipt() {
    if [[ ${FIREWALL_TABLE:-nat} == filter ]]; then
        FAKE_RULES="$FILTER_RULES" python3 "$FAKE_IPT" "$@"
    else python3 "$FAKE_IPT" "$@"; fi
}
CF_BIN=/usr/bin/true
mkdir -p "$STATE_DIR" "$CONFIG_DIR"
need() { :; }
load_identity() { :; }
load_binary() { :; }
proxy_ready() { :; }
bridge_ready() { :; }
dedicated_idle() { :; }
redsocks_port_free() { :; }
redsocks_ready() { [[ -f $STATE_DIR/redsocks.pid ]]; }
managed_process() {
    case $2 in
        record) echo mock-record ;;
        check) [[ -f $STATE_DIR/$1.pid ]] ;;
        *) return 99 ;;
    esac
}
record_running() { [[ -f $STATE_DIR/$1.pid ]]; }
stop_process() { rm -f "$STATE_DIR/$1.pid"; }
sudo() {
    case "$*" in
        -v) ;;
        '-n -- iptables --version') echo nf_tables ;;
        '-n -u tahmures-cloudflared -- test -x /usr/bin/true') ;;
        '-n -u tahmures-cloudflared -- /bin/sh -c '*)
            echo controller-pid=999
            echo https://fixture.trycloudflare.com
            if [[ ${NO_REGISTRATION:-0} == 0 ]]; then
                echo 'Registered tunnel connection connIndex=0'
            fi ;;
        *) return 99 ;;
    esac
}
"""
        )

    def test_activation_reactivation_and_deactivation_restore_both_tables(self):
        result = self.bash(
            self.lifecycle_prelude()
            + """
start_controller
start_controller
stop_all
stop_all
"""
        )
        self.assertIn("already running", result.stdout)
        self.assertIn("registered edge observed", result.stdout)
        for path in (self.rules, self.home / "filter.json"):
            self.assertEqual(json.loads(path.read_text()), self.initial)
        self.assertFalse(list(self.home.glob(".local/state/**/*.pid")))

    def test_direct_lifecycle_starts_only_cloudflared(self):
        result = self.bash(
            self.lifecycle_prelude()
            + """
EDGE_EGRESS=direct
proxy_ready() { exit 81; }
start_proxy_resources() { exit 82; }
start_controller
start_controller
stop_all
"""
        )
        self.assertIn("registered edge observed", result.stdout)
        self.assertIn("already running", result.stdout)
        for path in (self.rules, self.home / "filter.json"):
            self.assertEqual(json.loads(path.read_text()), self.initial)
        self.assertFalse(list(self.home.glob(".local/state/**/*.pid")))

    def test_direct_refuses_existing_proxy_rules(self):
        result = self.bash(
            self.lifecycle_prelude()
            + """
EDGE_EGRESS=direct
install_firewall
start_controller
""",
            success=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(list(self.home.glob(".local/state/**/*.pid")))
        self.assertGreater(len(json.loads(self.rules.read_text())["OUTPUT"]), 1)

    def test_registration_deadline_rolls_back_both_tables(self):
        result = self.bash(
            self.lifecycle_prelude()
            + "NO_REGISTRATION=1; EDGE_WAIT_SECONDS=1\nstart_controller",
            success=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("No registered edge connection", result.stderr)
        for path in (self.rules, self.home / "filter.json"):
            self.assertEqual(json.loads(path.read_text()), self.initial)

    def test_interrupted_start_rolls_back_guard_and_redirect(self):
        result = self.bash(
            self.lifecycle_prelude()
            + """
edge_registered() { exit 143; }
start_controller
""",
            success=False,
        )
        self.assertEqual(result.returncode, 143, result.stderr)
        for path in (self.rules, self.home / "filter.json"):
            self.assertEqual(json.loads(path.read_text()), self.initial)

    def test_missing_dependency_fails_before_mutation(self):
        result = self.bash("need definitely-missing-tahmures-command", success=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("install it manually", result.stderr)
        self.assertEqual(json.loads(self.rules.read_text()), self.initial)
        self.assertFalse((self.home / ".config").exists())

    def test_old_boot_record_is_stale_without_signalling(self):
        with subprocess.Popen(["/usr/bin/sleep", "30"]) as child:
            try:
                result = self.bash(f"""
record=$(process record unused "$UID" /usr/bin/sleep {child.pid} /usr/bin/sleep 30)
bad=$(python3 -c '
import json,sys
d=json.loads(sys.argv[1]); d["boot"]="00000000-0000-0000-0000-000000000000"
print(json.dumps(d))' "$record")
if process stop "$bad" "$UID" /usr/bin/sleep /usr/bin/sleep 30; then
    exit 80
else [[ $? == 10 ]]; fi
process check "$record" "$UID" /usr/bin/sleep /usr/bin/sleep 30
""")
                self.assertEqual(result.returncode, 0)
                self.assertIsNone(child.poll())
            finally:
                child.terminate()

    def test_uninstall_requires_confirmation_before_changes(self):
        result = subprocess.run(
            ["bash", str(SCRIPT), "uninstall"],
            env=self.env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--confirm-uninstall", result.stderr)
        self.assertFalse((self.home / ".config").exists())

    def test_uninstall_preserves_token_path_file_and_logs(self):
        self.bash(
            self.lifecycle_prelude()
            + """
configuration init
printf 'fixture-secret' > "$CONFIG_DIR/token"
printf '/legacy/path' > "$CONFIG_DIR/cloudflared.path"
start_controller
main uninstall --confirm-uninstall
[[ ! -e $CONFIG_DIR/cloudflare-proxy.json ]]
[[ ! -e $CONFIG_DIR/redsocks.conf ]]
[[ $(cat "$CONFIG_DIR/token") == fixture-secret ]]
[[ $(cat "$CONFIG_DIR/cloudflared.path") == /legacy/path ]]
[[ -f $STATE_DIR/cloudflared.log ]]
"""
        )
        for path in (self.rules, self.home / "filter.json"):
            self.assertEqual(json.loads(path.read_text()), self.initial)


if __name__ == "__main__":
    unittest.main()
