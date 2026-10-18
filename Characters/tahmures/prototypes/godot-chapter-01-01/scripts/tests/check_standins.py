#!/usr/bin/env python3
"""Validate the deterministic stand-in/prop PNG outputs.

Checks: PNG signature, IHDR dimensions (360x480), non-empty pixel data,
and (with --compare DIR) byte-identical regeneration against a second run.
Exit 0 = all pass, 1 = any fail.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import os
import struct
import sys
import zlib

W, H = 360, 480


def _decode_rgba(d: bytes) -> bytes:
    """Minimal PNG decoder for 8-bit RGBA (filter 0) — validates IDAT."""
    w, h = struct.unpack(">II", d[16:24])
    bit_depth, color_type = d[24], d[25]
    if bit_depth != 8 or color_type != 6:
        raise ValueError("expected 8-bit RGBA")
    idat = b""
    off = 8
    while off < len(d):
        (length,), tag = struct.unpack(">I", d[off:off + 4]), d[off + 4:off + 8]
        if tag == b"IDAT":
            idat += d[off + 8:off + 8 + length]
        off += 12 + length
    raw = zlib.decompress(idat)
    stride = w * 4
    out = bytearray()
    prev = bytearray(stride)
    pos = 0
    for _ in range(h):
        ftype = raw[pos]
        pos += 1
        line = bytearray(raw[pos:pos + stride])
        pos += stride
        if ftype == 0:
            pass
        elif ftype == 1:
            for i in range(stride):
                a = line[i - 4] if i >= 4 else 0
                line[i] = (line[i] + a) & 0xFF
        elif ftype == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif ftype == 3:
            for i in range(stride):
                a = line[i - 4] if i >= 4 else 0
                line[i] = (line[i] + (a + prev[i]) // 2) & 0xFF
        elif ftype == 4:
            for i in range(stride):
                a = line[i - 4] if i >= 4 else 0
                b = prev[i]
                c = prev[i - 4] if i >= 4 else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 0xFF
        else:
            raise ValueError(f"unsupported filter {ftype}")
        out += line
        prev = line
    return bytes(out)


def check_png(path: str) -> list:
    errs = []
    with open(path, "rb") as fh:
        d = fh.read()
    if d[:8] != b"\x89PNG\r\n\x1a\n":
        return [f"{path}: bad PNG signature"]
    w, h = struct.unpack(">II", d[16:24])
    if (w, h) != (W, H):
        errs.append(f"{path}: dimensions {w}x{h} != {W}x{H}")
        return errs
    try:
        px = _decode_rgba(d)
    except Exception as exc:
        errs.append(f"{path}: IDAT decode failed: {exc}")
        return errs
    opaque = 0
    for i in range(3, len(px), 4):
        if px[i] > 0:
            opaque += 1
    if opaque < 300:
        errs.append(f"{path}: only {opaque} opaque pixels (empty stand-in?)")
    return errs


def digest(paths: list) -> str:
    h = hashlib.sha256()
    for p in sorted(paths):
        with open(p, "rb") as fh:
            h.update(os.path.basename(p).encode())
            h.update(fh.read())
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--compare", default=None, help="second dir for determinism check")
    args = ap.parse_args()

    files = glob.glob(os.path.join(args.dir, "*.png"))
    if len(files) != 20:
        print(f"FAIL: expected 20 pngs in {args.dir}, found {len(files)}")
        return 1
    errs = []
    for f in files:
        errs.extend(check_png(f))
    if args.compare:
        d1 = digest(files)
        d2 = digest(glob.glob(os.path.join(args.compare, "*.png")))
        if d1 != d2:
            errs.append(f"determinism: {d1[:16]} != {d2[:16]}")
        else:
            print(f"DETERMINISTIC digest={d1[:16]}…")
    if errs:
        for e in errs:
            print("FAIL:", e)
        return 1
    print(f"OK: {len(files)} standin/prop PNGs valid ({W}x{H})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
