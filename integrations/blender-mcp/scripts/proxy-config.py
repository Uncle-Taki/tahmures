#!/usr/bin/env python3
"""Strict external configuration data; never evaluate shell expressions."""

import json
import os
import stat
import sys
import tempfile
from pathlib import Path

DEFAULTS = {
    "enabled": False,
    "cloudflared": True,
    "redsocks": True,
    "firewall": True,
    "dedicated_account": True,
    "autostart": False,
    "edge_wait_seconds": 90,
    "edge_egress": "xray",
}


def unique(pairs):
    data = {}
    for key, value in pairs:
        if key in data:
            raise ValueError("duplicate configuration key")
        data[key] = value
    return data


def validate(data, *, activation=False):
    if not isinstance(data, dict) or set(data) != set(DEFAULTS):
        raise ValueError("configuration must contain exactly the documented keys")
    for key in DEFAULTS:
        if type(data[key]) is not type(DEFAULTS[key]):
            raise ValueError(f"invalid type for {key}")
    if data["autostart"] or not 1 <= data["edge_wait_seconds"] <= 300:
        raise ValueError("autostart must be false; edge wait must be 1–300 seconds")
    mode = data["edge_egress"]
    if mode not in ("xray", "direct"):
        raise ValueError("edge_egress must be xray or direct")
    if data["enabled"] or activation:
        if not (data["cloudflared"] and data["dedicated_account"]):
            raise ValueError("Cloudflared and its dedicated account must be enabled")
        proxy = mode == "xray"
        if data["redsocks"] != proxy or data["firewall"] != proxy:
            raise ValueError(f"{mode} requires redsocks and firewall both {proxy}")
    if activation and not data["enabled"]:
        raise ValueError("integration is disabled; explicitly enable before start")


def read(path):
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except FileNotFoundError:
        return DEFAULTS.copy()
    with os.fdopen(fd) as stream:
        info = os.fstat(stream.fileno())
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_uid != os.getuid()
            or info.st_mode & 0o077
            or info.st_size > 4096
        ):
            raise ValueError(
                "configuration must be a private owned regular file ≤4096 bytes"
            )
        data = json.loads(stream.read(4097), object_pairs_hook=unique)
    if isinstance(data, dict):
        data.setdefault("edge_egress", DEFAULTS["edge_egress"])
    validate(data)
    return data


def write(path, data, *, exclusive=False):
    # No directory traversal through a final symlink, and no overwrite at init.
    if path.parent.is_symlink():
        raise ValueError("configuration directory is a symlink")
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    info = path.parent.stat()
    if info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise ValueError("configuration directory must be private and owned")
    payload = json.dumps(data, indent=2) + "\n"
    if exclusive:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, "w") as stream:
            stream.write(payload)
        return
    name = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", dir=path.parent, delete=False
        ) as stream:
            name = stream.name
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if name and os.path.exists(name):
            os.unlink(name)


def main():
    path, action = Path(sys.argv[1]), sys.argv[2]
    if action == "init":
        write(path, DEFAULTS, exclusive=True)
        print("Configuration created; disabled. No host resources provisioned.")
        return
    data = read(path)
    if action == "show":
        print(json.dumps(data, indent=2))
        print("Fixed safety profile: IPv4 HTTP/2 TCP7844; origin 127.0.0.1:8765;")
        if data["edge_egress"] == "xray":
            print("HTTP CONNECT 127.0.0.1:10808; transparent listener 127.0.0.1:12347;")
        else:
            print("Direct edge egress via the host route; no Redsocks or NAT rules.")
        print("dedicated account tahmures-cloudflared; no automatic activation.")
    elif action == "validate":
        validate(data, activation=True)
        print(data["edge_wait_seconds"], data["edge_egress"])
    elif action in ("enable", "disable"):
        data["enabled"] = action == "enable"
        validate(data)
        write(path, data)
        print(f"Activation permitted: {data['enabled']}. No processes started.")
    else:
        raise ValueError("unknown configuration operation")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, IndexError) as error:
        sys.exit(f"Configuration error: {error}")
