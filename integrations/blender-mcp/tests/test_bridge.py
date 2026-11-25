"""Offline tests: ephemeral loopback HTTP/TCP servers; never connect to Blender."""

import ast
import base64
import concurrent.futures
import contextlib
import http.client
import importlib.util
import io
import json
import math
import socket
import socketserver
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

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
PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO"
    "+/h9sAAAAASUVORK5CYII="
)


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
                result = self.server.result(command)
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
        self.stdout = ""

    def result(self, command):
        kind, params = command["type"], command["params"]
        if kind == "ping":
            return {"pong": True}
        if kind == "get_scene_info":
            return SCENE
        if kind == "get_viewport_screenshot":
            path = Path(params["filepath"])
            path.write_bytes(PNG)
            if self.mode == "large_image":
                with path.open("r+b") as image:
                    image.truncate(bridge.MAX_IMAGE + 1)
            if self.mode == "wrong_image_path":
                path = path.with_name("other.png")
            return {"success": True, "filepath": str(path), "width": 1, "height": 1}
        if kind == "execute_code":
            code = params["code"]
            first = ast.parse(code).body[0]
            if code.startswith("saved = bpy.ops.wm.save_as_mainfile"):
                path = Path(ast.literal_eval(first.value.keywords[0].value))
                if self.mode != "missing_save":
                    path.write_bytes(b"fake blend")
            output = "REF_Test.001\n" if "image.pack()" in code else self.stdout
            return {"executed": self.mode != "not_executed", "result": output}
        raise AssertionError(f"Unexpected fake command: {kind}")


class BridgeTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repository = Path(temp.name)
        self.characters = self.repository / "Characters"
        self.characters.mkdir()
        self.reference = self.characters / "front.png"
        self.reference.write_bytes(PNG)
        self.fake = FakeBlender()
        self.fake_thread = threading.Thread(
            target=self.fake.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True
        )
        self.fake_thread.start()
        self.client = bridge.BlenderClient(
            self.fake.server_address, timeout=0.2, max_response=1024
        )
        self.http = bridge.BridgeServer(
            TOKEN, self.client, port=0, repository=self.repository
        )
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

    def post(self, operation, payload=None, **kwargs):
        return self.request(
            f"/v1/blender/{operation}",
            method="POST",
            body=None if payload is None else json.dumps(payload),
            extra={"Content-Type": "application/json"},
            **kwargs,
        )[:2]

    def test_post_routes_require_bearer(self):
        for operation in ("execute", "viewport", "load-reference", "save"):
            with self.subTest(operation=operation):
                self.assertEqual(self.post(operation, token=None)[0], 401)
        self.assertEqual(self.fake.commands, [])

    def test_post_rejects_malformed_requests_before_blender(self):
        path = "/v1/blender/execute"
        for body, extra, expected in (
            (b" " * (bridge.MAX_BODY + 1), {"Content-Type": "application/json"}, 413),
            (b'{"code":"print(1)"}', {"Content-Type": "text/plain"}, 415),
            (b'{"code":"a","code":"b"}', {"Content-Type": "application/json"}, 400),
            (
                b"{}",
                {"Content-Type": "application/json", "Transfer-Encoding": "chunked"},
                400,
            ),
        ):
            with self.subTest(expected=expected):
                self.assertEqual(
                    self.request(path, method="POST", body=body, extra=extra)[0],
                    expected,
                )
        self.assertEqual(self.fake.commands, [])

    def test_execute_guarded_modeling_and_sanitizes_output(self):
        self.fake.stdout = f"modeled\0\r\n{TOKEN.decode()}\n"
        code = (
            "import bpy, bmesh\n"
            "from mathutils import Vector\n"
            "bm = bmesh.new()\n"
            "bmesh.ops.create_cube(bm, size=1)\n"
            "mesh = bpy.data.meshes.new('Base')\n"
            "bm.to_mesh(mesh)\n"
            "bm.free()\n"
            "obj = bpy.data.objects.new('Base', mesh)\n"
            "obj.location = Vector((0, 0, 1))\n"
            "bpy.context.collection.objects.link(obj)\n"
            "print(obj.name)\n"
        )
        self.assertEqual(
            self.post("execute", {"code": code}),
            (200, {"status": "ok", "result": "modeled\n[redacted]\n"}),
        )
        (command,) = self.fake.commands
        self.assertEqual(command["type"], "execute_code")
        self.assertTrue(
            command["params"]["code"].endswith(
                code.replace("print(obj.name)", "_bridge_print(obj.name)").rstrip()
            )
        )

    def test_execute_accepts_character_materials_and_armature(self):
        code = """
import bpy, bmesh, math
from mathutils import Vector

def make_part(name, angle: float):
    mesh = bpy.data.meshes.new(name)
    geometry = bmesh.new()
    bmesh.ops.create_cube(geometry, size=1)
    geometry.to_mesh(mesh)
    geometry.free()
    part = bpy.data.objects.new(name, mesh)
    part.rotation_euler = (0, math.radians(angle), 0)
    return part

group = bpy.data.collections.new("Character")
bpy.context.scene.collection.children.link(group)
skin = bpy.data.materials.new("Skin")
skin.use_nodes = True
shader = skin.node_tree.nodes["Principled BSDF"]
shader.inputs["Base Color"].default_value = (0.5, 0.2, 0.15, 1.0)
skin.node_tree.nodes.new(type="ShaderNodeTexNoise")
parts = [make_part(f"Body_{index:02d}", 10 * index) for index in range(3)]
for index, part in enumerate(parts):
    group.objects.link(part)
    part.data.materials.append(skin)
    if index:
        part.location.z += 0.4

armature = bpy.data.armatures.new("Character Skeleton")
rig = bpy.data.objects.new("Character Rig", armature)
group.objects.link(rig)
bpy.context.view_layer.objects.active = rig
rig.select_set(True)
bpy.ops.object.mode_set(mode="EDIT")
for name, height in (("spine", 1), ("head", 2)):
    bone = armature.edit_bones.new(name)
    bone.head = Vector((0, 0, height))
    bone.tail = Vector((0, 0, height + 0.5))
bpy.ops.object.mode_set(mode="OBJECT")
"""
        self.assertEqual(
            self.post("execute", {"code": code}),
            (200, {"status": "ok", "result": ""}),
        )
        (command,) = self.fake.commands
        self.assertEqual(command["type"], "execute_code")
        forwarded = command["params"]["code"]
        self.assertIn("armature.edit_bones.new(name)", forwarded)
        self.assertIn("shader.inputs['Base Color'].default_value", forwarded)
        self.assertIn("_bridge_iter(enumerate(parts))", forwarded)
        compile(forwarded, "<offline test>", "exec")

    def test_execute_accepts_reported_blender_53_script_and_response(self):
        script = (
            "import bpy, bmesh, math\n"
            "col = bpy.data.collections.get('BRIDGE_LIVE_TEST') or "
            "bpy.data.collections.new('BRIDGE_LIVE_TEST')\n"
            "if col.name not in bpy.context.scene.collection.children:\n"
            "    bpy.context.scene.collection.children.link(col)\n"
            "mesh = bpy.data.meshes.get('BridgeTestMesh') or "
            "bpy.data.meshes.new('BridgeTestMesh')\n"
            "obj = bpy.data.objects.get('BridgeTestObj') or "
            "bpy.data.objects.new('BridgeTestObj', mesh)\n"
            "if obj.name not in col.objects:\n"
            "    col.objects.link(obj)\n"
            "bm = bmesh.new()\n"
            "bmesh.ops.create_cube(bm, size=1.0)\n"
            "bm.to_mesh(mesh)\n"
            "bm.free()\n"
            "mat = bpy.data.materials.get('BridgeTestMat') or "
            "bpy.data.materials.new('BridgeTestMat')\n"
            "bsdf = mat.node_tree.nodes['Principled BSDF']\n"
            "bsdf.inputs['Base Color'].default_value = (0.2, 0.4, 0.8, 1.0)\n"
            "if not obj.data.materials:\n"
            "    obj.data.materials.append(mat)\n"
            "obj.rotation_euler[2] = math.radians(45)\n"
            "print('Created:', obj.name, len(obj.data.vertices))\n"
        )
        # The fake TCP server wraps this in Blender's success/executed envelope.
        self.fake.stdout = "Created: BridgeTestObj 8\n"

        self.assertEqual(
            self.post("execute", {"code": script}),
            (200, {"status": "ok", "result": "Created: BridgeTestObj 8\n"}),
        )
        (command,) = self.fake.commands
        self.assertEqual(command["type"], "execute_code")
        self.assertIn(
            "_bridge_writable_items(obj.rotation_euler)[2] = math.radians(45)",
            command["params"]["code"],
        )

    def test_execute_rejects_unsafe_code_before_blender(self):
        for code, detail in (
            ("import os", "blocked_import: os"),
            ("import subprocess as bpy", "blocked_import: subprocess"),
            ("from bpy import *", "blocked_import: bpy.*"),
            ("from mathutils import __dict__", "blocked_import: mathutils.__dict__"),
            ("open('out')", "blocked_name: open"),
            ("eval('1')", "blocked_name: eval"),
            ("type(1)", "blocked_name: type"),
            ("print((1).__subclasses__)", "blocked_attribute: __subclasses__"),
            (
                "bpy.ops.wm.save_as_mainfile(filepath='x.blend')",
                "blocked_attribute: wm",
            ),
            ("import bpy as b\nb.ops.wm.save_mainfile()", "blocked_attribute: wm"),
            (
                "bpy.ops.script.python_file_run(filepath='x')",
                "blocked_attribute: script",
            ),
            ("bpy.app.handlers", "blocked_attribute: handlers"),
            ("bpy.app.timers", "blocked_attribute: timers"),
            ("bpy.utils.register_class(Foo)", "blocked_attribute: register_class"),
            ("bpy.data.texts.new('test')", "blocked_attribute: texts"),
            ("bpy.data.images.load('/outside.png')", "blocked_call: load"),
            ("bpy.context.preferences", "blocked_attribute: preferences"),
            (
                "operator = bpy.ops.mesh.primitive_cube_add",
                "blocked_attribute: primitive_cube_add",
            ),
            (
                "bpy.ops.mesh.primitive_torus_add(major_segments=10000)",
                "geometry_count_out_of_range: major_segments",
            ),
            (
                "m = bpy.data.materials.new('m')\n"
                "m.node_tree.nodes.new('ShaderNodeScript')",
                "blocked_model_type: nodes",
            ),
            ("print(1e999)", "blocked_literal"),
            ("print(1, file=None)", "blocked_keyword: file"),
            ("alias = help\nalias()", "blocked_name: help"),
            ("def f(range): pass", "reserved_name: range"),
            ("while True: pass", "blocked_syntax: While"),
            ("try:\n    pass\nexcept:\n    pass", "blocked_syntax: Try"),
            ("print(", "invalid_syntax"),
        ):
            with self.subTest(code=code):
                self.assertEqual(
                    self.post("execute", {"code": code}),
                    (400, {"error": "unsafe_modeling_code", "detail": detail}),
                )
        self.assertEqual(self.fake.commands, [])

    def test_custom_bmesh_construction_and_material_assignment(self):
        code = bridge.ModelingCode().validate("""
import bmesh
bm = bmesh.new()
verts = [bm.verts.new(co) for co in [(0, 0, 0), (1, 0, 0), (0, 0, 1)]]
face = bm.faces.new(verts)
face.material_index = 2
bm.to_mesh(mesh)
bm.free()
""")
        self.assertIn("material_index", code)
        for source in ("bm.verts.remove(vertex)", "bm.faces.remove(face)"):
            with self.subTest(source=source), self.assertRaises(bridge.BridgeError):
                bridge.ModelingCode().validate(source)

    def test_modeling_guards_run_offline_with_normal_python(self):
        code = bridge.ModelingCode().validate("""
def square(value: int) -> int:
    return value ** 2

values = {index: square(index) for index in range(4)}
selected = {value for value in values.values() if value > 1}
total: int = sum(value for value in selected)
total += 1
assertions = isinstance(total, (int, str)) and len([*selected]) == 2
print(f"{total:02d}", assertions)
""")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(code, {})
        self.assertEqual(output.getvalue(), "14 True\n")

    def test_modeling_guards_allow_euler_component_write_only_for_euler(self):
        class Euler(list):
            pass

        class OtherWritableSequence(list):
            pass

        code = bridge.ModelingCode().validate(
            "import math\nobj.rotation_euler[2] = math.radians(45)"
        )
        with patch.dict(sys.modules, {"mathutils": SimpleNamespace(Euler=Euler)}):
            rotation = Euler([0.0, 0.0, 0.0])
            exec(code, {"obj": SimpleNamespace(rotation_euler=rotation)})
            self.assertEqual(rotation, [0.0, 0.0, math.radians(45)])

            other = OtherWritableSequence([0.0, 0.0, 0.0])
            with self.assertRaisesRegex(ValueError, "Subscript writes require"):
                exec(code, {"obj": SimpleNamespace(rotation_euler=other)})
            self.assertEqual(other, [0.0, 0.0, 0.0])

    def test_modeling_guards_bound_runtime_work(self):
        for source, detail in (
            ("for index in range(4097): pass", "range exceeds"),
            ("print('a' * 10000)", "sequence exceeds"),
            ("for a in range(200):\n    for b in range(200): pass", "work budget"),
        ):
            with (
                self.subTest(source=source),
                self.assertRaisesRegex(ValueError, detail),
            ):
                exec(bridge.ModelingCode().validate(source), {})

    def test_execute_requires_successful_execution_schema(self):
        self.fake.mode = "not_executed"
        self.assertEqual(
            self.post("execute", {"code": "print(1)"}),
            (502, {"error": "invalid_blender_response"}),
        )

    def test_execute_deadline_returns_generic_timeout(self):
        self.fake.mode = "timeout"
        with patch.object(bridge, "EXECUTION_TIMEOUT", 0.1):
            self.assertEqual(
                self.post("execute", {"code": "print(1)"}),
                (504, {"error": "blender_timeout"}),
            )

    def test_viewport_uses_bridge_owned_png_and_cleans_up(self):
        status, payload = self.post("viewport")
        self.assertEqual(status, 200)
        self.assertEqual(payload["mime_type"], "image/png")
        self.assertEqual((payload["width"], payload["height"]), (1, 1))
        self.assertEqual(base64.b64decode(payload["image_base64"]), PNG)
        (command,) = self.fake.commands
        self.assertEqual(command["type"], "get_viewport_screenshot")
        self.assertEqual(command["params"]["max_size"], 800)
        self.assertEqual(command["params"]["format"], "png")
        self.assertFalse(Path(command["params"]["filepath"]).parent.exists())

    def test_viewport_rejects_oversized_capture_and_unexpected_path(self):
        for mode, error in (
            ("large_image", "blender_response_too_large"),
            ("wrong_image_path", "invalid_blender_response"),
        ):
            with self.subTest(mode=mode):
                self.fake.mode = mode
                self.assertEqual(self.post("viewport", {}), (502, {"error": error}))

    def test_load_reference_builds_locked_front_image(self):
        status, payload = self.post(
            "load-reference",
            {
                "repo_path": "Characters/front.png",
                "name": "REF_Test",
                "height_meters": 2.0,
            },
        )
        self.assertEqual(
            (status, payload), (200, {"status": "ok", "name": "REF_Test.001"})
        )
        (command,) = self.fake.commands
        self.assertEqual(command["type"], "execute_code")
        code = command["params"]["code"]
        for fragment in (
            f"bpy.data.images.load({ascii(str(self.reference))}",
            "bpy.data.objects.new('REF_Test', None)",
            "reference.empty_display_size = 2.0",
            "reference.show_empty_image_perspective = False",
            "reference.empty_image_side = 'FRONT'",
            "reference.lock_location = locked_axes",
            "reference.lock_rotation = locked_axes",
            "reference.lock_scale = locked_axes",
        ):
            self.assertIn(fragment, code)

    def test_load_reference_rejects_escape_and_non_images(self):
        outside = self.repository / "outside.png"
        outside.write_bytes(PNG)
        (self.characters / "escape.png").symlink_to(outside)
        for path in (
            "Characters/../outside.png",
            str(self.reference),
            "Characters/escape.png",
            "Characters/base.blend",
            "Characters/missing.webp",
        ):
            with self.subTest(path=path):
                self.assertEqual(
                    self.post(
                        "load-reference",
                        {
                            "repo_path": path,
                            "name": "REF_Test",
                            "height_meters": 2,
                        },
                    )[0],
                    400,
                )
        self.assertEqual(self.fake.commands, [])

    def test_save_creates_file_and_requires_explicit_overwrite(self):
        request = {"filename": "demo/base.blend"}
        expected = {
            "status": "ok",
            "repo_path": "Characters/blender/demo/base.blend",
            "size_bytes": 10,
        }
        self.assertEqual(self.post("save", request), (200, expected))
        path = self.repository / expected["repo_path"]
        self.assertEqual(path.read_bytes(), b"fake blend")
        path.write_bytes(b"prior revision")
        self.assertEqual(self.post("save", request), (409, {"error": "file_exists"}))
        self.assertEqual(path.read_bytes(), b"prior revision")
        self.assertEqual(len(self.fake.commands), 1)
        self.assertEqual(self.post("save", request | {"overwrite": "true"})[0], 400)
        self.assertEqual(
            self.post("save", request | {"overwrite": True}), (200, expected)
        )
        self.assertEqual(path.read_bytes(), b"fake blend")
        self.assertEqual(list(path.parent.iterdir()), [path])

    def test_save_rejects_path_traversal_and_symlinks(self):
        root = self.characters / "blender"
        root.mkdir()
        (root / "escape").symlink_to(self.repository, target_is_directory=True)
        (root / "alias.blend").symlink_to(root / "missing.blend")
        for filename in (
            "../base.blend",
            "/tmp/base.blend",
            "C:/base.blend",
            "base.png",
            "escape/base.blend",
            "alias.blend",
        ):
            with self.subTest(filename=filename):
                self.assertEqual(
                    self.post("save", {"filename": filename, "overwrite": True})[0], 400
                )
        self.assertEqual(self.fake.commands, [])

    def test_failed_save_preserves_prior_revision(self):
        root = self.characters / "blender"
        root.mkdir()
        path = root / "base.blend"
        path.write_bytes(b"prior revision")
        self.fake.mode = "missing_save"
        self.assertEqual(
            self.post("save", {"filename": path.name, "overwrite": True}),
            (502, {"error": "save_failed"}),
        )
        self.assertEqual(path.read_bytes(), b"prior revision")
        self.assertEqual(list(root.iterdir()), [path])

    def test_concurrent_saves_default_to_no_overwrite(self):
        self.fake.mode = "delay"
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            requests = pool.map(
                lambda _: self.post("save", {"filename": "demo/base.blend"}),
                range(2),
            )
            self.assertEqual(sorted(status for status, _ in requests), [200, 409])
        folder = self.characters / "blender" / "demo"
        self.assertEqual(list(folder.iterdir()), [folder / "base.blend"])

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
