#!/usr/bin/env bash
set -euo pipefail
base="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
# Keep the bearer token out of command arguments and terminal output.
exec /usr/bin/python3 -B - "$base/bridge/server.py" <<'PY'
import http.client
import importlib.util
import os
import sys

spec = importlib.util.spec_from_file_location("bridge_check", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
try:
    token = module.load_token(os.environ.get("BLENDER_BRIDGE_TOKEN_FILE"))
    for path in ("/healthz", "/v1/blender/status", "/v1/blender/scene"):
        connection = http.client.HTTPConnection("127.0.0.1", 8765, timeout=12)
        headers = {} if path == "/healthz" else {"Authorization": "Bearer " + token.decode("ascii")}
        connection.request("GET", path, headers=headers)
        response = connection.getresponse()
        body = response.read(module.MAX_RESPONSE + 1)
        print(f"{path}: HTTP {response.status}")
        connection.close()
        if response.status != 200 or len(body) > module.MAX_RESPONSE:
            raise ValueError("check failed")
except (OSError, ValueError, RuntimeError, http.client.HTTPException):
    sys.exit("Bridge check failed; verify token file, foreground bridge, and Blender listener.")
PY
