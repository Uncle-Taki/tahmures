#!/usr/bin/env python3
"""Loopback-only HTTP adapter for guarded operations on the Blender TCP add-on."""

import ast
import base64
import builtins
import hmac
import json
import os
import re
import socket
import stat
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HTTP_ADDRESS = ("127.0.0.1", 8765)
BLENDER_ADDRESS = ("127.0.0.1", 9876)
TIMEOUT = 5.0
EXECUTION_TIMEOUT = 30.0
MAX_RESPONSE = 1024 * 1024
MAX_BODY = 64 * 1024
MAX_IMAGE = 4 * 1024 * 1024
MAX_VIEWPORT_RESPONSE = 4 * ((MAX_IMAGE + 2) // 3) + 256
MAX_HEADERS = 8192
REPOSITORY = Path(__file__).resolve().parents[3]
MODULES = {"bpy", "bmesh", "math", "mathutils", "json", "collections", "itertools"}
SAFE_BUILTINS = {
    "len",
    "range",
    "enumerate",
    "zip",
    "min",
    "max",
    "abs",
    "round",
    "sum",
    "sorted",
    "reversed",
    "int",
    "float",
    "str",
    "bool",
    "list",
    "tuple",
    "dict",
    "set",
    "print",
    "any",
    "all",
    "isinstance",
}
SAFE_TYPES = {"int", "float", "str", "bool", "list", "tuple", "dict", "set"}
BLOCKED_NAMES = set(vars(builtins)) - SAFE_BUILTINS
BLOCKED_ATTRIBUTES = {
    "wm",
    "script",
    "preferences",
    "extensions",
    "render",
    "handlers",
    "timers",
    "driver_namespace",
    "register_class",
    "unregister_class",
    "texts",
    "libraries",
}

DATA_GROUPS = [
    "collections",
    "objects",
    "meshes",
    "materials",
    "armatures",
    "cameras",
    "lights",
]
ROOT_CALLS = {
    f"bpy.data.{group}.{method}" for group in DATA_GROUPS for method in ("new", "get")
}
ROOT_CALLS |= {
    f"bpy.ops.{group}.{operator}"
    for group, operators in {
        "mesh": (
            "primitive_cube_add primitive_uv_sphere_add primitive_ico_sphere_add "
            "primitive_cylinder_add primitive_cone_add primitive_plane_add "
            "primitive_torus_add select_all extrude_region_move merge "
            "normals_make_consistent bevel subdivide"
        ),
        "object": (
            "mode_set select_all shade_smooth shade_flat transform_apply "
            "modifier_apply join armature_add"
        ),
        "armature": "select_all subdivide extrude roll_clear calculate_roll",
        "transform": "translate rotate resize",
    }.items()
    for operator in operators.split()
}
ROOT_CALLS |= {
    f"bmesh.ops.{operator}"
    for operator in [
        "create_cube",
        "create_uvsphere",
        "create_icosphere",
        "create_cone",
        "create_grid",
        "translate",
        "rotate",
        "scale",
        "recalc_face_normals",
        "remove_doubles",
    ]
}
ROOT_CALLS |= {
    "bmesh.new",
    "bmesh.from_edit_mesh",
    "bmesh.update_edit_mesh",
    "mathutils.Vector",
    "mathutils.Matrix",
    "mathutils.Euler",
    "mathutils.Quaternion",
    "mathutils.Matrix.Identity",
    "mathutils.Matrix.Translation",
    "mathutils.Matrix.Rotation",
    "mathutils.Matrix.Scale",
    "mathutils.Matrix.Diagonal",
    "collections.deque",
    "collections.defaultdict",
    "itertools.chain",
    "itertools.pairwise",
    "itertools.islice",
}
ROOT_CALLS |= {
    f"math.{function}"
    for function in [
        "acos",
        "asin",
        "atan",
        "atan2",
        "ceil",
        "cos",
        "degrees",
        "dist",
        "exp",
        "fabs",
        "floor",
        "fmod",
        "hypot",
        "isclose",
        "isfinite",
        "log",
        "log2",
        "log10",
        "radians",
        "sin",
        "sqrt",
        "tan",
        "trunc",
    ]
}

ROOT_VALUES = {f"bpy.data.{group}" for group in DATA_GROUPS}
ROOT_VALUES |= {
    f"bpy.context.{property_name}"
    for property_name in [
        "object",
        "active_object",
        "selected_objects",
        "collection",
        "scene",
        "view_layer",
        "mode",
        "edit_object",
        "active_bone",
        "active_pose_bone",
        "selected_bones",
    ]
}
IMPORT_NAMESPACES = {"bpy.context", "bpy.data", "bpy.ops", "bpy.types", "bmesh.ops"}
ROOT_VALUES |= {
    "math.pi",
    "math.tau",
    "math.e",
    *(
        f"bpy.types.{kind}"
        for kind in ("Object", "Mesh", "Armature", "Material", "Bone")
    ),
}

MODEL_WRITES = {
    "name",
    "label",
    "location",
    "rotation_euler",
    "rotation_quaternion",
    "rotation_mode",
    "scale",
    "parent",
    "parent_type",
    "parent_bone",
    "matrix_world",
    "matrix_parent_inverse",
    "show_in_front",
    "display_type",
    "hide_render",
    "hide_viewport",
    "hide_select",
    "use_nodes",
    "diffuse_color",
    "metallic",
    "roughness",
    "default_value",
    "head",
    "tail",
    "roll",
    "use_connect",
    "use_deform",
    "active",
    "active_material",
    "material_index",
    "x",
    "y",
    "z",
    "w",
    "co",
    "use_smooth",
    "length",
    "object",
    "strength",
    "levels",
    "render_levels",
    "mirror_object",
    "use_clip",
    "use_mirror_merge",
}
MODEL_READS = MODEL_WRITES | {
    "type",
    "data",
    "children",
    "objects",
    "collection",
    "scene",
    "view_layer",
    "layer_collection",
    "active_layer_collection",
    "all_objects",
    "node_tree",
    "nodes",
    "links",
    "inputs",
    "outputs",
    "materials",
    "modifiers",
    "vertices",
    "edges",
    "polygons",
    "loops",
    "verts",
    "faces",
    "normal",
    "index",
    "edit_bones",
    "bones",
    "pose",
    "selected_objects",
    "active_object",
    "select",
    "select_head",
    "select_tail",
    "vector",
}
MODEL_METHODS = {
    "link",
    "unlink",
    "append",
    "extend",
    "clear",
    "get",
    "keys",
    "values",
    "items",
    "update",
    "copy",
    "to_mesh",
    "from_mesh",
    "free",
    "ensure_lookup_table",
    "index_update",
    "normal_update",
    "select_set",
    "hide_set",
    "normalized",
    "normalize",
    "dot",
    "cross",
    "lerp",
    "inverted",
    "to_3x3",
    "to_4x4",
    "to_euler",
    "to_quaternion",
}
SHADER_NODES = {
    "ShaderNodeBsdfPrincipled",
    "ShaderNodeOutputMaterial",
    "ShaderNodeRGB",
    "ShaderNodeValue",
    "ShaderNodeMixRGB",
    "ShaderNodeMix",
    "ShaderNodeMath",
    "ShaderNodeVectorMath",
    "ShaderNodeTexNoise",
    "ShaderNodeTexVoronoi",
    "ShaderNodeTexCoord",
    "ShaderNodeMapping",
    "ShaderNodeBump",
    "ShaderNodeNormalMap",
    "ShaderNodeSeparateXYZ",
    "ShaderNodeCombineXYZ",
}
MODIFIER_TYPES = {
    "ARMATURE",
    "BEVEL",
    "MIRROR",
    "SOLIDIFY",
    "SUBSURF",
    "WEIGHTED_NORMAL",
}
GEOMETRY_LIMITS = {
    "segments": 128,
    "ring_count": 128,
    "vertices": 128,
    "x_segments": 128,
    "y_segments": 128,
    "u_segments": 128,
    "v_segments": 128,
    "major_segments": 128,
    "minor_segments": 128,
    "subdivisions": 5,
    "number_cuts": 16,
}


class BridgeError(Exception):
    def __init__(self, status, code, detail=None):
        self.status = status
        self.code = code
        self.detail = detail


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


# Run inside the add-on ahead of the validated script. Submitted names start
# with a public character, so only the generated AST can call these helpers.
MODELING_GUARDS = r"""import operator as _bridge_operator
_bridge_budget = 20000
_bridge_output = 0

def _bridge_tick():
    global _bridge_budget
    _bridge_budget -= 1
    if _bridge_budget < 0:
        raise ValueError("Modeling work budget exceeded")

def _bridge_iter(items):
    for item in items:
        _bridge_tick()
        yield item

def _bridge_writable_items(items):
    if type(items) in (list, dict):
        return items
    from mathutils import Euler
    if type(items) is Euler:
        return items
    raise ValueError("Subscript writes require a Python list, dict, or mathutils.Euler")

def _bridge_range(*args):
    value = range(*args)
    if len(value) > 4096:
        raise ValueError("Modeling range exceeds 4096 items")
    return value

def _bridge_count(value, limit):
    if type(value) is not int or not 1 <= value <= limit:
        raise ValueError("Invalid geometry count")
    return value

def _bridge_binary(op, left, right, inplace=False):
    _bridge_tick()
    sequence_types = (str, bytes, tuple, list)
    if op == 'pow' and (
        type(right) not in (int, float) or abs(right) > 32
    ):
        raise ValueError("Modeling exponent exceeds limit")
    if op == 'mod' and isinstance(left, (str, bytes)):
        raise ValueError("Use an f-string for text formatting")
    for seq, count in ((left, right), (right, left)):
        if op == 'mul' and isinstance(seq, sequence_types):
            if type(count) is int and len(seq) * count > 4096:
                raise ValueError("Modeling sequence exceeds 4096 items")
    if op == 'add' and isinstance(left, sequence_types) and type(left) is type(right):
        if len(left) + len(right) > 4096:
            raise ValueError("Modeling sequence exceeds 4096 items")
    if inplace:
        op = {'or_': 'ior', 'and_': 'iand'}.get(op, 'i' + op)
    result = getattr(_bridge_operator, op)(left, right)
    if type(result) is int and result.bit_length() > 4096:
        raise ValueError("Modeling integer exceeds 4096 bits")
    return result

def _bridge_text_value(value):
    pending = [value]
    size = 0
    while pending:
        item = pending.pop()
        size += len(item) if isinstance(item, (str, bytes)) else 1
        if type(item) in (list, tuple, set, dict):
            size += len(item)
            if size <= 8192:
                pending.extend(item)
                if type(item) is dict:
                    pending.extend(item.values())
        if size > 8192:
            raise ValueError("Modeling text exceeds limit")
    return value

def _bridge_str(value=''):
    return str(_bridge_text_value(value))

def _bridge_print(*values, sep=' ', end='\n'):
    global _bridge_output
    line = sep.join(_bridge_str(value) for value in _bridge_iter(values)) + end
    _bridge_output += len(line)
    if _bridge_output > 65536:
        raise ValueError("Modeling output exceeds limit")
    print(line, end='')
"""


class ModelingCode(ast.NodeTransformer):
    """Validate a Python subset and add shared work guards before forwarding it."""

    ALLOWED = (
        ast.Module,
        ast.Assign,
        ast.AnnAssign,
        ast.Expr,
        ast.If,
        ast.Return,
        ast.Pass,
        ast.Break,
        ast.Continue,
        ast.Subscript,
        ast.Slice,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.IfExp,
        ast.List,
        ast.Tuple,
        ast.Dict,
        ast.Set,
        ast.ListComp,
        ast.DictComp,
        ast.SetComp,
        ast.GeneratorExp,
        ast.JoinedStr,
        ast.Starred,
        ast.arguments,
        ast.arg,
        ast.Load,
        ast.Store,
        ast.unaryop,
        ast.boolop,
        ast.cmpop,
    )
    BINARY = {
        ast.Add: "add",
        ast.Sub: "sub",
        ast.Mult: "mul",
        ast.Div: "truediv",
        ast.FloorDiv: "floordiv",
        ast.Mod: "mod",
        ast.Pow: "pow",
        ast.MatMult: "matmul",
        ast.BitOr: "or_",
        ast.BitAnd: "and_",
        ast.BitXor: "xor",
    }
    GUARDED = {"print": "_bridge_print", "range": "_bridge_range", "str": "_bridge_str"}

    def __init__(self):
        self.imports = {"bpy": "bpy"}
        self.functions = set()
        self.top_level = set()

    def validate(self, code):
        if not isinstance(code, str) or not code.strip():
            self.reject("invalid_code")
        try:
            tree = ast.parse(code, mode="exec")
            if sum(1 for _ in ast.walk(tree)) > 4096:
                self.reject("node_budget_exceeded")
            if not tree.body:
                self.reject("invalid_code")
            self.top_level = set(tree.body)
            for statement in tree.body:
                if isinstance(statement, (ast.Import, ast.ImportFrom)):
                    self.register_import(statement)
                if isinstance(statement, ast.FunctionDef):
                    self.bind_name(statement.name)
                    self.functions.add(statement.name)
            self.visit(tree)
            ast.fix_missing_locations(tree)
            compile(tree, "<modeling>", "exec")
            return MODELING_GUARDS + "\n" + ast.unparse(tree)
        except (SyntaxError, ValueError, RecursionError, OverflowError):
            self.reject("invalid_syntax")

    @staticmethod
    def reject(reason, name=None):
        # Emit fixed diagnostics plus a bounded identifier, never source excerpts.
        detail = reason
        if name is not None:
            detail += ": " + (
                name if re.fullmatch(r"[A-Za-z0-9_.*]{1,64}", name) else "identifier"
            )
        raise BridgeError(400, "unsafe_modeling_code", detail)

    def public_name(self, name):
        if name.startswith("_") or name in BLOCKED_NAMES:
            self.reject("blocked_name", name)

    def bind_name(self, name):
        self.public_name(name)
        if name in SAFE_BUILTINS | self.functions | self.imports.keys():
            self.reject("reserved_name", name)

    def register_import(self, node):
        module = node.module if isinstance(node, ast.ImportFrom) else None
        if isinstance(node, ast.ImportFrom) and (node.level or module not in MODULES):
            self.reject("blocked_import", module or "relative")
        for item in node.names:
            if module is None:
                if item.name not in MODULES:
                    self.reject("blocked_import", item.name)
                qualified = item.name
            else:
                qualified = f"{module}.{item.name}"
                if qualified not in ROOT_CALLS | ROOT_VALUES | IMPORT_NAMESPACES:
                    self.reject("blocked_import", qualified)
            local = item.asname or item.name
            self.public_name(local)
            if local in SAFE_BUILTINS or local in self.functions:
                self.reject("reserved_name", local)
            if local in self.imports and self.imports[local] != qualified:
                self.reject("reserved_name", local)
            self.imports[local] = qualified

    def visit_Import(self, node):
        if node not in self.top_level:
            self.reject("import_requires_module_scope")
        return node

    visit_ImportFrom = visit_Import

    def visit_FunctionDef(self, node):
        if node not in self.top_level or node.decorator_list or node.type_params:
            self.reject("unsupported_function", node.name)
        super().generic_visit(node)
        step = ast.Expr(value=self.helper("_bridge_tick"))
        node.body.insert(0, step)
        return node

    def generic_visit(self, node):
        if not isinstance(node, self.ALLOWED):
            self.reject("blocked_syntax", type(node).__name__)
        return super().generic_visit(node)

    def visit_arg(self, node):
        self.bind_name(node.arg)
        return super().generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.bind_name(node.id)
        else:
            self.public_name(node.id)
            if node.id in self.imports and self.imports[node.id] not in ROOT_VALUES:
                self.reject("blocked_value", node.id)
            if node.id in (SAFE_BUILTINS - SAFE_TYPES) | self.functions:
                self.reject("blocked_value", node.id)
            if node.id == "str":
                node.id = "_bridge_str"
        return node

    def visit_Constant(self, node):
        value = node.value
        if (
            value is None
            or type(value) is bool
            or type(value) is int
            and abs(value) <= 10**9
            or type(value) is float
            and float("-inf") < value < float("inf")
            or type(value) is str
            and len(value) <= 4096
        ):
            return node
        self.reject("blocked_literal")

    def qualified(self, node):
        if isinstance(node, ast.Name):
            self.public_name(node.id)
            return self.imports.get(node.id)
        if isinstance(node, ast.Attribute):
            if node.attr.startswith("_") or node.attr in BLOCKED_ATTRIBUTES:
                self.reject("blocked_attribute", node.attr)
            root = self.qualified(node.value)
            return f"{root}.{node.attr}" if root else None
        return None

    def visit_Attribute(self, node):
        qualified = self.qualified(node)
        if qualified in ROOT_VALUES and isinstance(node.ctx, ast.Load):
            return node
        properties = MODEL_WRITES if isinstance(node.ctx, ast.Store) else MODEL_READS
        if node.attr not in properties:
            self.reject("blocked_attribute", node.attr)
        node.value = self.visit(node.value)
        return node

    def visit_Subscript(self, node):
        super().generic_visit(node)
        if isinstance(node.ctx, ast.Store):
            node.value = self.helper("_bridge_writable_items", node.value)
        return node

    @staticmethod
    def helper(name, *args):
        return ast.Call(
            func=ast.Name(id=name, ctx=ast.Load()), args=list(args), keywords=[]
        )

    def visit_For(self, node):
        super().generic_visit(node)
        node.iter = self.helper("_bridge_iter", node.iter)
        return node

    def visit_comprehension(self, node):
        if node.is_async:
            self.reject("blocked_syntax", "AsyncFor")
        super().generic_visit(node)
        node.iter = self.helper("_bridge_iter", node.iter)
        return node

    def visit_BinOp(self, node):
        op = self.BINARY.get(type(node.op))
        if op is None:
            self.reject("blocked_operator", type(node.op).__name__)
        return self.helper(
            "_bridge_binary",
            ast.Constant(op),
            self.visit(node.left),
            self.visit(node.right),
        )

    def visit_AugAssign(self, node):
        target = self.visit(node.target)
        op = self.BINARY.get(type(node.op))
        if op is None:
            self.reject("blocked_operator", type(node.op).__name__)
        prefix = []
        if isinstance(target, ast.Name):
            current = ast.Name(id=target.id, ctx=ast.Load())
        elif isinstance(target, ast.Attribute):
            prefix.append(
                ast.Assign(
                    targets=[ast.Name(id="_bridge_receiver", ctx=ast.Store())],
                    value=target.value,
                )
            )
            target.value = ast.Name(id="_bridge_receiver", ctx=ast.Load())
            current = ast.Attribute(
                value=target.value, attr=target.attr, ctx=ast.Load()
            )
        else:
            self.reject("augmented_assignment_requires_variable_or_attribute")
        update = self.helper(
            "_bridge_binary",
            ast.Constant(op),
            current,
            self.visit(node.value),
            ast.Constant(True),
        )
        return [*prefix, ast.Assign(targets=[target], value=update)]

    def visit_FormattedValue(self, node):
        node.value = self.helper("_bridge_text_value", self.visit(node.value))
        spec = node.format_spec
        if spec and not (
            len(spec.values) == 1
            and isinstance(spec.values[0], ast.Constant)
            and re.fullmatch(
                r"[<>=^+ -]?[0-9]{0,3}(?:\\.[0-9]{1,3})?[a-zA-Z%]?",
                spec.values[0].value,
            )
        ):
            self.reject("blocked_format_spec")
        return node

    def validate_method(self, func, args, keywords):
        self.qualified(func)
        if func.attr == "new" and isinstance(func.value, ast.Attribute):
            if any(isinstance(arg, ast.Starred) for arg in args):
                self.reject("constructor_requires_explicit_arguments")
            collection = func.value.attr
            if collection in {"edit_bones", "links", "verts", "faces"}:
                return
            if collection in {"nodes", "modifiers"}:
                allowed = SHADER_NODES if collection == "nodes" else MODIFIER_TYPES
                type_index = 0 if collection == "nodes" else 1
                kind = next((kw.value for kw in keywords if kw.arg == "type"), None)
                if kind is not None and len(args) > type_index:
                    self.reject("duplicate_model_type", collection)
                if len(args) > type_index:
                    kind = args[type_index]
                if not isinstance(kind, ast.Constant) or kind.value not in allowed:
                    self.reject("blocked_model_type", collection)
                return
        if func.attr not in MODEL_METHODS:
            self.reject("blocked_call", func.attr)

    def type_argument(self, node):
        if isinstance(node, ast.Tuple):
            node.elts = [self.type_argument(item) for item in node.elts]
        elif isinstance(node, ast.Name) and node.id in SAFE_TYPES:
            pass
        elif (self.qualified(node) or "").startswith("bpy.types."):
            return self.visit(node)
        else:
            self.reject("isinstance_requires_allowed_type")
        return node

    def visit_Call(self, node):
        qualified = self.qualified(node.func)
        builtin = node.func.id if isinstance(node.func, ast.Name) else None
        if (
            isinstance(node.func, ast.Name)
            and node.func.id in SAFE_BUILTINS | self.functions
        ):
            node.func.id = self.GUARDED.get(node.func.id, node.func.id)
        elif qualified in ROOT_CALLS:
            if qualified.startswith("bpy.ops.") and node.args:
                self.reject("operator_requires_keywords")
            if qualified.startswith("bmesh.ops.") and len(node.args) != 1:
                self.reject("bmesh_operator_requires_mesh")
            if qualified.startswith(("bpy.ops.", "bmesh.ops.")) and any(
                isinstance(arg, ast.Starred) for arg in node.args
            ):
                self.reject("operator_requires_explicit_arguments")
        elif isinstance(node.func, ast.Attribute):
            self.validate_method(node.func, node.args, node.keywords)
            node.func.value = self.visit(node.func.value)
        else:
            self.reject("blocked_call", getattr(node.func, "id", None))
        if builtin == "isinstance":
            if len(node.args) != 2 or node.keywords:
                self.reject("isinstance_requires_allowed_type")
            node.args = [self.visit(node.args[0]), self.type_argument(node.args[1])]
        else:
            node.args = [self.visit(arg) for arg in node.args]
        for keyword in node.keywords:
            if keyword.arg is None:
                self.reject("keyword_unpacking_not_allowed")
            if keyword.arg.startswith("_"):
                self.reject("blocked_keyword", keyword.arg)
            if builtin == "print" and keyword.arg not in {"sep", "end"}:
                self.reject("blocked_keyword", keyword.arg)
            keyword.value = self.visit(keyword.value)
            if (
                qualified
                and qualified.startswith(("bpy.ops.", "bmesh.ops."))
                and keyword.arg in GEOMETRY_LIMITS
            ):
                limit = GEOMETRY_LIMITS[keyword.arg]
                if isinstance(keyword.value, ast.Constant) and (
                    type(keyword.value.value) is not int
                    or not 1 <= keyword.value.value <= limit
                ):
                    self.reject("geometry_count_out_of_range", keyword.arg)
                keyword.value = self.helper(
                    "_bridge_count", keyword.value, ast.Constant(limit)
                )
        return node


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
        return self._request(command, {}, self.timeout)

    def execute(self, code):
        result = self._request("execute_code", {"code": code}, EXECUTION_TIMEOUT)
        if result.get("executed") is not True or not isinstance(
            result.get("result"), str
        ):
            raise BridgeError(502, "invalid_blender_response")
        return result["result"]

    def capture(self, path):
        return self._request(
            "get_viewport_screenshot",
            {"filepath": str(path), "max_size": 800, "format": "png"},
            self.timeout,
        )

    def _request(self, command, params, timeout):
        if not self.lock.acquire(timeout=self.timeout):
            raise BridgeError(503, "blender_busy")
        try:
            deadline = time.monotonic() + timeout
            with socket.create_connection(self.address, timeout=self.timeout) as sock:
                sock.settimeout(max(0.001, deadline - time.monotonic()))
                sock.sendall(json.dumps({"type": command, "params": params}).encode())
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


def checked_path(root, value, extensions, *, allow_symlinks=False):
    if (
        not isinstance(value, str)
        or len(value) > 512
        or any(ord(char) < 32 or 0xD800 <= ord(char) <= 0xDFFF for char in value)
        or "\\" in value
        or ":" in value
        or any(part in ("", ".", "..") for part in value.split("/"))
    ):
        raise BridgeError(400, "invalid_path")
    path = root / value
    if path.suffix.lower() not in extensions:
        raise BridgeError(400, "invalid_path")
    try:
        resolved = path.resolve()
        if not resolved.is_relative_to(root) or root.resolve() != root:
            raise BridgeError(400, "invalid_path")
        if not allow_symlinks:
            for component in (path, *path.parents):
                if component == root.parent:
                    break
                if component.is_symlink():
                    raise BridgeError(400, "invalid_path")
    except (OSError, RuntimeError, ValueError):
        raise BridgeError(400, "invalid_path") from None
    return resolved


def load_reference(blender, repository, body):
    if body.keys() != {"repo_path", "name", "height_meters"}:
        raise BridgeError(400, "invalid_body")
    path, name, height = body["repo_path"], body["name"], body["height_meters"]
    if (
        not isinstance(path, str)
        or not path.startswith("Characters/")
        or not isinstance(name, str)
        or not re.fullmatch(r"[\w .-]{1,63}", name)
        or len(name.encode("utf-8")) > 63
        or type(height) not in (int, float)
        or not 0 < height <= 1000
    ):
        raise BridgeError(400, "invalid_body")
    image = checked_path(
        repository / "Characters",
        path.removeprefix("Characters/"),
        {".png", ".jpg", ".jpeg", ".webp"},
        allow_symlinks=True,
    )
    if not image.is_file() or image.suffix.lower() not in {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
    }:
        raise BridgeError(400, "invalid_image")
    output = blender.execute(f"""import math
image = bpy.data.images.load({ascii(str(image))}, check_existing=False)
reference = None
try:
    if not all(image.size):
        raise ValueError("Invalid reference dimensions")
    image.pack()
    reference = bpy.data.objects.new({ascii(name)}, None)
    reference.empty_display_type = 'IMAGE'
    reference.data = image
    units = bpy.context.scene.unit_settings
    meters_per_unit = units.scale_length if units.system != 'NONE' else 1.0
    aspect_scale = max(image.size) / image.size[1]
    reference.empty_display_size = {height!r} * aspect_scale / meters_per_unit
    reference.empty_image_offset = (-0.5, -0.5)
    reference.rotation_euler = (math.pi / 2, 0, 0)
    reference.show_empty_image_orthographic = True
    reference.show_empty_image_perspective = False
    reference.show_empty_image_only_axis_aligned = True
    reference.empty_image_side = 'FRONT'
    locked_axes = (True, True, True)
    reference.lock_location = locked_axes
    reference.lock_rotation = locked_axes
    reference.lock_scale = locked_axes
    reference.hide_select = True
    bpy.context.collection.objects.link(reference)
    print(reference.name)
except Exception:
    if reference is not None:
        bpy.data.objects.remove(reference, do_unlink=True)
    bpy.data.images.remove(image)
    raise
""")
    actual_name = output.removesuffix("\n")
    if not re.fullmatch(r"[\w .-]{1,63}", actual_name):
        raise BridgeError(502, "invalid_blender_response")
    return {"status": "ok", "name": actual_name}


def save_blend(blender, repository, body):
    if "filename" not in body or body.keys() - {"filename", "overwrite"}:
        raise BridgeError(400, "invalid_body")
    overwrite = body.get("overwrite", False)
    if type(overwrite) is not bool:
        raise BridgeError(400, "invalid_body")
    root = repository / "Characters" / "blender"
    destination = checked_path(root, body["filename"], {".blend"})
    try:
        if destination.exists():
            if not overwrite:
                raise BridgeError(409, "file_exists")
            if not destination.is_file():
                raise BridgeError(400, "invalid_path")
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(
            prefix=".bridge-save-", dir=destination.parent
        ) as tmp:
            staged = Path(tmp) / destination.name
            blender.execute(
                "saved = bpy.ops.wm.save_as_mainfile("
                f"filepath={ascii(str(staged))}, check_existing=False, "
                "copy=True, relative_remap=False)\n"
                "if saved != {'FINISHED'}:\n"
                "    raise RuntimeError('Save did not finish')"
            )
            info = staged.lstat()
            if not stat.S_ISREG(info.st_mode) or not info.st_size:
                raise BridgeError(502, "save_failed")
            checked_path(root, body["filename"], {".blend"})
            if overwrite:
                os.replace(staged, destination)
            else:
                os.link(staged, destination, follow_symlinks=False)
    except FileExistsError:
        raise BridgeError(409, "file_exists") from None
    except OSError:
        raise BridgeError(502, "save_failed") from None
    return {
        "status": "ok",
        "repo_path": destination.relative_to(repository).as_posix(),
        "size_bytes": info.st_size,
    }


def capture_viewport(blender):
    try:
        with tempfile.TemporaryDirectory(prefix="blender-viewport-") as tmp:
            path = Path(tmp) / "viewport.png"
            result = blender.capture(path)
            width, height = result.get("width"), result.get("height")
            if (
                result.get("success") is not True
                or result.get("filepath") != str(path)
                or type(width) is not int
                or type(height) is not int
                or not (1 <= width <= 800 and 1 <= height <= 800)
            ):
                raise BridgeError(502, "invalid_blender_response")
            fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
            with os.fdopen(fd, "rb") as image:
                if not stat.S_ISREG(os.fstat(image.fileno()).st_mode):
                    raise BridgeError(502, "invalid_blender_response")
                data = image.read(MAX_IMAGE + 1)
            if len(data) > MAX_IMAGE:
                raise BridgeError(502, "blender_response_too_large")
            if not data.startswith(b"\x89PNG\r\n\x1a\n"):
                raise BridgeError(502, "invalid_blender_response")
    except OSError:
        raise BridgeError(502, "invalid_blender_response") from None
    return {
        "mime_type": "image/png",
        "image_base64": base64.b64encode(data).decode("ascii"),
        "width": width,
        "height": height,
    }


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

    def respond(self, code, body, limit=MAX_RESPONSE):
        self.close_connection = True
        try:
            payload = json.dumps(body, allow_nan=False, separators=(",", ":")).encode()
        except (ValueError, RecursionError):
            code, payload = 502, b'{"error":"invalid_blender_response"}'
        if len(payload) > limit:
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
        if not self.authorized():
            self.respond(401, {"error": "unauthorized"})
            return
        try:
            result = self.server.blender.query(commands[self.path])
            self.respond(
                200, {"connected": True} if commands[self.path] == "ping" else result
            )
        except BridgeError as exc:
            self.respond(exc.status, {"error": exc.code})

    def authorized(self):
        auth = self.headers.get_all("Authorization", [])
        value = auth[0] if len(auth) == 1 else ""
        token = value[7:] if value[:7].lower() == "bearer " else ""
        return hmac.compare_digest(token.encode("utf-8"), self.server.token)

    def read_post_body(self, *, optional=False):
        lengths = self.headers.get_all("Content-Length", [])
        if self.headers.get_all("Transfer-Encoding") or len(lengths) > 1:
            raise BridgeError(400, "invalid_body")
        if (not lengths or lengths == ["0"]) and optional:
            return {}
        if not lengths or not re.fullmatch(r"[0-9]+", lengths[0]):
            raise BridgeError(400, "invalid_body")
        digits = lengths[0].lstrip("0") or "0"
        if len(digits) > len(str(MAX_BODY)) or int(digits) > MAX_BODY:
            raise BridgeError(413, "request_too_large")
        content_types = self.headers.get_all("Content-Type", [])
        if (
            len(content_types) != 1
            or self.headers.get_content_type() != "application/json"
        ):
            raise BridgeError(415, "unsupported_media_type")
        length = int(digits)
        raw = bytearray()
        deadline = time.monotonic() + TIMEOUT
        try:
            while len(raw) < length:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError
                self.connection.settimeout(remaining)
                chunk = self.rfile.stream.read1(length - len(raw))
                if not chunk:
                    raise BridgeError(400, "invalid_body")
                raw.extend(chunk)
            body = json.loads(
                raw.decode("utf-8"),
                parse_constant=reject_constant,
                object_pairs_hook=unique_object,
            )
        except TimeoutError:
            raise BridgeError(408, "request_timeout") from None
        except (ValueError, RecursionError, OSError):
            raise BridgeError(400, "invalid_body") from None
        finally:
            self.connection.settimeout(TIMEOUT)
        if not isinstance(body, dict):
            raise BridgeError(400, "invalid_body")
        return body

    def do_POST(self):
        if self.rfile.exceeded:
            self.respond(431, {"error": "request_too_large"})
            return
        methods = {
            "/v1/blender/execute": self.execute_modeling,
            "/v1/blender/viewport": self.viewport,
            "/v1/blender/load-reference": self.load_reference,
            "/v1/blender/save": self.save_blend,
        }
        if self.path not in methods:
            self.respond(405, {"error": "method_not_allowed"})
            return
        if not self.authorized():
            self.respond(401, {"error": "unauthorized"})
            return
        try:
            body = self.read_post_body(optional=self.path == "/v1/blender/viewport")
            methods[self.path](body)
        except BridgeError as exc:
            error = {"error": exc.code}
            if exc.detail is not None:
                error["detail"] = exc.detail
            self.respond(exc.status, error)

    def execute_modeling(self, body):
        if body.keys() != {"code"}:
            raise BridgeError(400, "invalid_body")
        code = ModelingCode().validate(body["code"])
        output = self.server.blender.execute(code)
        output = "".join(
            char for char in output if char.isprintable() or char in "\n\t"
        )
        output = output.replace(self.server.token.decode("ascii"), "[redacted]")
        self.respond(200, {"status": "ok", "result": output})

    def viewport(self, body):
        if body:
            raise BridgeError(400, "invalid_body")
        self.respond(200, capture_viewport(self.server.blender), MAX_VIEWPORT_RESPONSE)

    def load_reference(self, body):
        self.respond(
            200, load_reference(self.server.blender, self.server.repository, body)
        )

    def save_blend(self, body):
        self.respond(200, save_blend(self.server.blender, self.server.repository, body))

    def reject_method(self):
        self.respond(405, {"error": "method_not_allowed"})

    do_PUT = do_DELETE = do_PATCH = reject_method
    do_OPTIONS = do_HEAD = do_TRACE = do_CONNECT = reject_method


class BridgeServer(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 16
    allow_reuse_address = False

    def __init__(self, token, blender=None, port=8765, repository=REPOSITORY):
        self.token = token
        self.blender = blender if blender is not None else BlenderClient()
        self.repository = repository
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
