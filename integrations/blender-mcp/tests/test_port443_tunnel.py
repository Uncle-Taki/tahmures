"""Offline tests for the Pinggy tunnel controller using command stubs."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/port443-tunnel.sh"


class Port443TunnelTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.bin = self.home / "bin"
        self.bin.mkdir()
        self.events = self.home / "events.log"
        self.clipboard = self.home / "clipboard.txt"
        self.token_file = self.home / "stub-token"
        self.token_file.write_text("test-only-placeholder\n")
        self.env = dict(os.environ)
        self.env.update(
            HOME=str(self.home),
            PATH=f"{self.bin}:/usr/bin:/bin",
            BLENDER_BRIDGE_TOKEN_FILE=str(self.token_file),
            FAKE_EVENTS=str(self.events),
            FAKE_CLIPBOARD=str(self.clipboard),
        )
        self.env.pop("DISPLAY", None)
        self.env.pop("WAYLAND_DISPLAY", None)
        self.install_stub(
            "curl",
            "printf 'bridge-check\\n' >> \"$FAKE_EVENTS\"\nexit 0\n",
        )
        self.install_stub(
            "nc",
            "printf 'proxy-check\\n' >> \"$FAKE_EVENTS\"\nexit 0\n",
        )
        self.install_stub("nohup", 'exec "$@"\n')
        self.install_stub(
            "ssh",
            """printf 'dashboard https://dashboard.pinggy.io/account\\n'
printf 'allocated https://edge-42.pinggy.link\\n'
printf 'ssh-start\\n' >> \"$FAKE_EVENTS\"
exec -a 'ssh -T free.pinggy.io' /bin/sleep 300
""",
        )
        self.install_stub(
            "env",
            """printf 'test\\n' >> \"$FAKE_EVENTS\"
for arg do
  case \"$arg\" in
    BLENDER_TUNNEL_URL=*) printf 'test_url=%s\\n' \"${arg#*=}\" >> \"$FAKE_EVENTS\" ;;
  esac
done
exit 0
""",
        )
        self.install_stub(
            "python3",
            "printf 'unexpected-python3-execution\\n' >> \"$FAKE_EVENTS\"\nexit 97\n",
        )
        self.install_stub(
            "xclip",
            "cat > \"$FAKE_CLIPBOARD\"\nprintf 'xclip\\n' >> \"$FAKE_EVENTS\"\n",
        )
        self.install_stub(
            "wl-copy",
            "cat > \"$FAKE_CLIPBOARD\"\nprintf 'wl-copy\\n' >> \"$FAKE_EVENTS\"\n",
        )

    def install_stub(self, name, body):
        stub = self.bin / name
        stub.write_text(f"#!/bin/bash\nset -eu\n{body}")
        stub.chmod(0o755)

    def run_controller(self, *args):
        return subprocess.run(
            ["bash", str(SCRIPT), *args],
            env=self.env,
            text=True,
            capture_output=True,
            check=False,
            timeout=10,
        )

    def test_reload_stops_starts_tests_and_exports_pinggy_url(self):
        self.env["DISPLAY"] = ":stub-display"
        result = self.run_controller("reload", "--copy")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertLess(result.stdout.index("Tunnel stopped"), result.stdout.index("Tunnel active"))
        self.assertEqual(
            result.stdout.rstrip().splitlines()[-1],
            "BLENDER_BRIDGE_URL=https://edge-42.pinggy.link",
        )
        self.assertNotIn("BLENDER_BRIDGE_URL=https://dashboard.pinggy.io", result.stdout)
        events = self.events.read_text().splitlines()
        self.assertLess(events.index("ssh-start"), events.index("test"))
        self.assertIn("test_url=https://edge-42.pinggy.link", events)
        self.assertEqual(self.clipboard.read_text(), "https://edge-42.pinggy.link")
        self.assertIn("xclip", events)
        self.assertNotIn("unexpected-python3-execution", events)

    def test_reload_copy_is_optional_without_a_display_session(self):
        result = self.run_controller("reload", "--copy")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            result.stdout.rstrip().splitlines()[-1],
            "BLENDER_BRIDGE_URL=https://edge-42.pinggy.link",
        )
        self.assertIn("Clipboard copy unavailable", result.stderr)
        self.assertFalse(self.clipboard.exists())

    def test_wayland_clipboard_is_supported(self):
        self.env["WAYLAND_DISPLAY"] = "wayland-stub"
        result = self.run_controller("reload", "--copy")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.clipboard.read_text(), "https://edge-42.pinggy.link")
        self.assertIn("wl-copy", self.events.read_text().splitlines())


if __name__ == "__main__":
    unittest.main()
