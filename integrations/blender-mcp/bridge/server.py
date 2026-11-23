#!/usr/bin/env python3
"""Loopback-only, read-only HTTP adapter for the installed Blender TCP add-on."""

import hmac
import json
import os
import re
import socket
import stat
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HTTP_ADDRESS = ("127.0.0.1", 8765)
BLENDER_ADDRESS = ("127.0.0.1", 9876)
TIMEOUT = 5.0
MAX_RESPONSE = 1024 * 1024
MAX_HEADERS = 8192
REPOSITORY = Path(__file__).resolve().parents[3]


class BridgeError(Exception):
    def __init__(self, status, code):
        self.status = status
        self.code = code


def load_token(path):
    """Read only a small, private, external regular file; never expose its value."""
    if not path:
        raise ValueError("invalid token file")
    token_path = Path(path).absolute()
    if token_path.resolve().is_relative_to(REPOSITORY):
        raise ValueError("invalid token file")
    fd = os.open(token_path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        info = os.fstat(fd)
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_uid != os.getuid()
            or info.st_mode & 0o077
            or info.st_size > 257
        ):
            raise ValueError("invalid token file")
        token = os.read(fd, 258)
    finally:
        os.close(fd)
    if token.endswith(b"\n"):
        token = token[:-1]
    if not re.fullmatch(rb"[A-Za-z0-9_-]{32,256}", token):
        raise ValueError("invalid token file")
    return token


def reject_constant(_value):
    raise ValueError("non-finite JSON")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


class BlenderClient:
    def __init__(
        self, address=BLENDER_ADDRESS, timeout=TIMEOUT, max_response=MAX_RESPONSE
    ):
        self.address = address
        self.timeout = timeout
        self.max_response = max_response
        self.lock = threading.Lock()

    def query(self, command):
        if command not in ("ping", "get_scene_info"):
            raise BridgeError(405, "command_not_allowed")
        if not self.lock.acquire(timeout=self.timeout):
            raise BridgeError(503, "blender_busy")
        try:
            deadline = time.monotonic() + self.timeout
            with socket.create_connection(self.address, timeout=self.timeout) as sock:
                sock.settimeout(max(0.001, deadline - time.monotonic()))
                sock.sendall(json.dumps({"type": command, "params": {}}).encode())
                data = bytearray()
                while True:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise BridgeError(504, "blender_timeout")
                    sock.settimeout(remaining)
                    chunk = sock.recv(min(8192, self.max_response + 1 - len(data)))
                    if not chunk:
                        raise BridgeError(502, "invalid_blender_response")
                    data.extend(chunk)
                    if len(data) > self.max_response:
                        raise BridgeError(502, "blender_response_too_large")
                    try:
                        response = json.loads(
                            data.decode("utf-8"),
                            parse_constant=reject_constant,
                            object_pairs_hook=unique_object,
                        )
                    except (UnicodeDecodeError, json.JSONDecodeError):
                        # No terminator: the add-on keeps the connection open.
                        continue
                    except (ValueError, RecursionError):
                        raise BridgeError(502, "invalid_blender_response") from None
                    if not isinstance(response, dict):
                        raise BridgeError(502, "invalid_blender_response")
                    if response.get("status") == "error":
                        raise BridgeError(502, "blender_error")
                    result = response.get("result")
                    if (
                        response.get("status") != "success"
                        or not isinstance(result, dict)
                        or "error" in result
                    ):
                        raise BridgeError(502, "invalid_blender_response")
                    if command == "ping" and result.get("pong") is not True:
                        raise BridgeError(502, "invalid_blender_response")
                    if command == "get_scene_info":
                        self._validate_scene(result)
                    return result
        except TimeoutError:
            raise BridgeError(504, "blender_timeout") from None
        except OSError:
            raise BridgeError(503, "blender_unavailable") from None
        finally:
            self.lock.release()

    @staticmethod
    def _validate_scene(result):
        if (
            not isinstance(result.get("name"), str)
            or type(result.get("object_count")) is not int
            or result["object_count"] < 0
            or type(result.get("materials_count")) is not int
            or result["materials_count"] < 0
            or not isinstance(result.get("objects"), list)
            or len(result["objects"]) > 10
        ):
            raise BridgeError(502, "invalid_blender_response")
        for obj in result["objects"]:
            if (
                not isinstance(obj, dict)
                or not isinstance(obj.get("name"), str)
                or not isinstance(obj.get("type"), str)
                or not isinstance(obj.get("location"), list)
                or len(obj["location"]) != 3
                or any(type(v) not in (int, float) for v in obj["location"])
            ):
                raise BridgeError(502, "invalid_blender_response")


class HeaderReader:
    """Bound all request-line/header reads before the HTTP parser allocates them."""

    def __init__(self, stream):
        self.stream = stream
        self.remaining = MAX_HEADERS
        self.exceeded = False

    def readline(self, size=-1):
        if self.exceeded:
            return b"\r\n"
        limit = self.remaining + 1
        line = self.stream.readline(limit if size < 0 else min(size, limit))
        self.remaining -= len(line)
        if self.remaining < 0:
            self.exceeded = True
            return b"\r\n"
        return line

    def close(self):
        self.stream.close()


class BridgeHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"

    def setup(self):
        super().setup()
        self.connection.settimeout(TIMEOUT)
        self.rfile = HeaderReader(self.rfile)

    def log_message(self, _format, *args):
        pass  # Never log request headers, URLs, credentials, or scene contents.

    def version_string(self):
        return "BlenderBridge"

    def send_error(self, code, message=None, explain=None):
        self.respond(code, {"error": "invalid_http_request"})

    def respond(self, code, body):
        self.close_connection = True
        try:
            payload = json.dumps(body, allow_nan=False, separators=(",", ":")).encode()
        except (ValueError, RecursionError):
            code, payload = 502, b'{"error":"invalid_blender_response"}'
        if len(payload) > MAX_RESPONSE:
            code, payload = 502, b'{"error":"blender_response_too_large"}'
        try:
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Connection", "close")
            if code == 401:
                self.send_header("WWW-Authenticate", "Bearer")
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(payload)
        except OSError:
            pass  # The HTTP client may have disconnected while Blender worked.

    def do_GET(self):
        if self.rfile.exceeded:
            self.respond(431, {"error": "request_too_large"})
            return
        lengths = self.headers.get_all("Content-Length", [])
        if self.headers.get_all("Transfer-Encoding") or (lengths and lengths != ["0"]):
            self.respond(400, {"error": "request_body_not_allowed"})
            return
        if self.path == "/healthz":
            self.respond(200, {"status": "ok"})
            return
        commands = {"/v1/blender/status": "ping", "/v1/blender/scene": "get_scene_info"}
        if self.path not in commands:
            self.respond(404, {"error": "not_found"})
            return
        auth = self.headers.get_all("Authorization", [])
        value = auth[0] if len(auth) == 1 else ""
        token = value[7:] if value[:7].lower() == "bearer " else ""
        if not hmac.compare_digest(token.encode("utf-8"), self.server.token):
            self.respond(401, {"error": "unauthorized"})
            return
        try:
            result = self.server.blender.query(commands[self.path])
            self.respond(
                200, {"connected": True} if commands[self.path] == "ping" else result
            )
        except BridgeError as exc:
            self.respond(exc.status, {"error": exc.code})

    def reject_method(self):
        self.respond(405, {"error": "method_not_allowed"})

    do_POST = do_PUT = do_DELETE = do_PATCH = reject_method
    do_OPTIONS = do_HEAD = do_TRACE = do_CONNECT = reject_method


class BridgeServer(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 16
    allow_reuse_address = False

    def __init__(self, token, blender=None, port=8765):
        self.token = token
        self.blender = blender if blender is not None else BlenderClient()
        self.workers = threading.BoundedSemaphore(16)
        super().__init__(("127.0.0.1", port), BridgeHandler)

    def process_request(self, request, client_address):
        if not self.workers.acquire(blocking=False):
            self.shutdown_request(request)
            return
        try:
            super().process_request(request, client_address)
        except Exception:
            self.workers.release()
            raise

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self.workers.release()

    def handle_error(self, request, client_address):
        pass  # Suppress request-derived traceback output.


def main():
    try:
        token = load_token(os.environ.get("BLENDER_BRIDGE_TOKEN_FILE"))
    except (OSError, ValueError, RuntimeError):
        raise SystemExit(
            "Bridge refused to start: invalid external token file."
        ) from None
    try:
        with BridgeServer(token) as server:
            print("Blender bridge listening on 127.0.0.1:8765", flush=True)
            server.serve_forever()
    except KeyboardInterrupt:
        pass
    except OSError:
        raise SystemExit("Bridge could not bind to 127.0.0.1:8765.") from None


if __name__ == "__main__":
    main()
