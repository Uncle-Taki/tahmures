"""Offline tests: ephemeral loopback HTTP/TCP servers; never connect to Blender."""

import concurrent.futures
import http.client
import importlib.util
import json
import socket
import socketserver
import tempfile
import threading
import time
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "bridge", Path(__file__).resolve().parents[1] / "bridge/server.py"
)
bridge = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bridge)
TOKEN = b"test-token-" + b"x" * 40
SCENE = {
    "name": "Test",
    "object_count": 1,
    "materials_count": 0,
    "objects": [{"name": "Cube", "type": "MESH", "location": [0, 0, 0]}],
}


class FakeHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(1)
        processing = True
        with self.server.guard:
            self.server.active += 1
            self.server.peak = max(self.server.peak, self.server.active)
        try:
            data = bytearray()
            while True:
                chunk = self.request.recv(4096)
                if not chunk:
                    return
                data.extend(chunk)
                try:
                    command = json.loads(data)
                    break
                except json.JSONDecodeError:
                    continue
            self.server.commands.append(command)
            mode = self.server.mode
            if mode == "timeout":
                self.server.release.wait(1)
                return
            if mode == "delay":
                time.sleep(0.03)
            if mode == "malformed":
                self.request.sendall(b"not JSON")
                return
            if mode == "oversize":
                self.request.sendall(b"x" * 1025)
                return
            if mode == "error":
                response = {"status": "error", "message": "private details"}
            elif mode == "wrong_pong":
                response = {"status": "success", "result": {"pong": False}}
            elif mode == "wrong_scene":
                response = {"status": "success", "result": {"objects": []}}
            else:
                result = {"pong": True} if command["type"] == "ping" else SCENE
                response = {"status": "success", "result": result}
            payload = json.dumps(response).encode()
            # Count command work, not handlers waiting for the client's EOF.
            # A completed reply releases the client lock before this thread is
            # necessarily scheduled again to notice the closed socket.
            with self.server.guard:
                self.server.active -= 1
                processing = False
            if mode == "fragment":
                for start in range(0, len(payload), 3):
                    self.request.sendall(payload[start : start + 3])
            else:
                self.request.sendall(payload)
            # Real add-on sockets stay open: successful parsing must not await EOF.
            self.request.recv(1)
        except OSError:
            pass
        finally:
            if processing:
                with self.server.guard:
                    self.server.active -= 1


class FakeBlender(socketserver.ThreadingTCPServer):
    daemon_threads = True

    def __init__(self):
        super().__init__(("127.0.0.1", 0), FakeHandler)
        self.mode = "normal"
        self.commands = []
        self.active = self.peak = 0
        self.guard = threading.Lock()
        self.release = threading.Event()


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.fake = FakeBlender()
        self.fake_thread = threading.Thread(
            target=self.fake.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True
        )
        self.fake_thread.start()
        self.client = bridge.BlenderClient(
            self.fake.server_address, timeout=0.2, max_response=1024
        )
        self.http = bridge.BridgeServer(TOKEN, self.client, port=0)
        self.http_thread = threading.Thread(
            target=self.http.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True
        )
        self.http_thread.start()

    def tearDown(self):
        self.fake.release.set()
        self.http.shutdown()
        self.http.server_close()
        self.fake.shutdown()
        self.fake.server_close()
        self.http_thread.join()
        self.fake_thread.join()

    def request(
        self,
        path="/v1/blender/status",
        token=TOKEN,
        method="GET",
        body=None,
        extra=None,
    ):
        headers = {} if token is None else {"Authorization": "Bearer " + token.decode()}
        headers.update(extra or {})
        conn = http.client.HTTPConnection(*self.http.server_address, timeout=2)
        conn.request(method, path, body=body, headers=headers)
        response = conn.getresponse()
        result = (
            response.status,
            json.loads(response.read()),
            dict(response.getheaders()),
        )
        conn.close()
        return result

    def test_valid_authentication_and_ping(self):
        status, result, headers = self.request()
        self.assertEqual((status, result), (200, {"connected": True}))
        self.assertEqual(self.fake.commands, [{"type": "ping", "params": {}}])
        self.assertNotIn("Access-Control-Allow-Origin", headers)

    def test_missing_authentication(self):
        self.assertEqual(self.request(token=None)[0], 401)
        self.assertEqual(self.fake.commands, [])

    def test_invalid_authentication(self):
        self.assertEqual(self.request(token=b"wrong")[0], 401)
        self.assertEqual(self.fake.commands, [])

    def test_health_generic_no_blender_call(self):
        self.assertEqual(
            self.request("/healthz", token=None)[:2], (200, {"status": "ok"})
        )
        self.assertEqual(self.fake.commands, [])

    def test_scene(self):
        self.assertEqual(self.request("/v1/blender/scene")[:2], (200, SCENE))
        self.assertEqual(self.fake.commands, [{"type": "get_scene_info", "params": {}}])

    def test_scene_requires_auth(self):
        self.assertEqual(self.request("/v1/blender/scene", token=None)[0], 401)
        self.assertEqual(self.fake.commands, [])

    def test_unavailable(self):
        with socket.socket() as reserved:
            reserved.bind(("127.0.0.1", 0))  # Bound but not listening.
            self.client.address = reserved.getsockname()
            self.assertEqual(
                self.request()[:2], (503, {"error": "blender_unavailable"})
            )

    def test_malformed_response(self):
        self.fake.mode = "malformed"
        self.assertEqual(self.request()[0], 502)

    def test_timeout(self):
        self.fake.mode = "timeout"
        self.assertEqual(self.request()[:2], (504, {"error": "blender_timeout"}))

    def test_oversized_response(self):
        self.fake.mode = "oversize"
        self.assertEqual(
            self.request()[:2], (502, {"error": "blender_response_too_large"})
        )

    def test_fragmented_json_without_eof(self):
        self.fake.mode = "fragment"
        self.assertEqual(self.request()[0], 200)

    def test_blender_error_redacted(self):
        self.fake.mode = "error"
        self.assertEqual(self.request()[:2], (502, {"error": "blender_error"}))

    def test_invalid_success_payloads(self):
        for mode, path in [
            ("wrong_pong", "/v1/blender/status"),
            ("wrong_scene", "/v1/blender/scene"),
        ]:
            with self.subTest(mode=mode):
                self.fake.mode = mode
                self.assertEqual(self.request(path)[0], 502)

    def test_unknown_routes_and_queries(self):
        for path in ["/missing", "/v1/blender/scene?command=execute_code", "/healthz/"]:
            with self.subTest(path=path):
                self.assertEqual(self.request(path)[0], 404)
        self.assertEqual(self.fake.commands, [])

    def test_arbitrary_command_and_write_rejection(self):
        for method in ["POST", "PUT", "DELETE", "PATCH", "OPTIONS", "TRACE", "CONNECT"]:
            with self.subTest(method=method):
                self.assertEqual(
                    self.request(method=method, body='{"type":"execute_code"}')[0], 405
                )
        self.assertEqual(self.request("/v1/blender/execute_code")[0], 404)
        with self.assertRaises(bridge.BridgeError):
            self.client.query("execute_code")
        self.assertEqual(self.fake.commands, [])

    def test_get_body_rejected(self):
        self.assertEqual(self.request(body='{"type":"execute_code"}')[0], 400)
        self.assertEqual(self.fake.commands, [])

    def test_transfer_encoding_rejected(self):
        self.assertEqual(self.request(extra={"Transfer-Encoding": "chunked"})[0], 400)
        self.assertEqual(self.fake.commands, [])

    def test_oversized_headers(self):
        self.assertEqual(self.request(extra={"X-Padding": "x" * 9000})[0], 431)
        self.assertEqual(self.fake.commands, [])

    def test_serialized_execution(self):
        self.fake.mode = "delay"
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            results = list(pool.map(lambda _: self.request()[0], range(3)))
        self.assertEqual(results, [200, 200, 200])
        self.assertEqual(self.fake.peak, 1)

    def test_disconnected_http_client(self):
        self.fake.mode = "delay"
        with socket.create_connection(self.http.server_address) as conn:
            conn.sendall(
                b"GET /v1/blender/status HTTP/1.0\r\nAuthorization: Bearer "
                + TOKEN
                + b"\r\n\r\n"
            )
        time.sleep(0.06)
        self.assertEqual(self.request()[0], 200)


class TokenTests(unittest.TestCase):
    def test_valid_private_external_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "token"
            path.write_bytes(TOKEN + b"\n")
            path.chmod(0o600)
            self.assertEqual(bridge.load_token(path), TOKEN)

    def test_invalid_files(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "token"
            for content in [b"", b"short", b"x" * 258, TOKEN + b"\n\n", b" " + TOKEN]:
                path.write_bytes(content)
                path.chmod(0o600)
                with (
                    self.subTest(content_length=len(content)),
                    self.assertRaises(ValueError),
                ):
                    bridge.load_token(path)
            path.write_bytes(TOKEN)
            path.chmod(0o644)
            with self.assertRaises(ValueError):
                bridge.load_token(path)
            path.chmod(0o600)
            link = Path(directory) / "link"
            link.symlink_to(path)
            with self.assertRaises(OSError):
                bridge.load_token(link)
            with self.assertRaises((OSError, ValueError)):
                bridge.load_token(directory)
        for missing in [None, "/does-not-exist/token", bridge.REPOSITORY / "token"]:
            with self.subTest(path=missing), self.assertRaises((OSError, ValueError)):
                bridge.load_token(missing)


if __name__ == "__main__":
    unittest.main()
