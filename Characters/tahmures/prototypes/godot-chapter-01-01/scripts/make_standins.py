#!/usr/bin/env python3
"""Deterministic placeholder stand-in generator for the CH01 Godot candidate.

Produces distinct, role-based silhouettes/cutouts from registry card anchors,
kept deliberately abstract so none can be mistaken for selected character art.
Pure stdlib (minimal PNG encoder + vector fills). No generation, no approved
anatomy, no mythic claims. Byte-identical on re-run (no randomness).

Usage: python3 scripts/make_standins.py --out assets/standins
"""
from __future__ import annotations

import argparse
import os
import struct
import sys
import zlib

W = 360
H = 480


# --- minimal RGBA PNG writer -------------------------------------------------

def save_png(path: str, pixels: bytearray) -> None:
    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    raw = b"".join(b"\x00" + bytes(pixels[y * W * 4:(y + 1) * W * 4]) for y in range(H))
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 6, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    with open(path, "wb") as fh:
        fh.write(png)


class Canvas:
    def __init__(self) -> None:
        self.px = bytearray(W * H * 4)

    def put(self, x: int, y: int, r: int, g: int, b: int, a: int) -> None:
        if 0 <= x < W and 0 <= y < H:
            i = (y * W + x) * 4
            self.px[i] = r
            self.px[i + 1] = g
            self.px[i + 2] = b
            self.px[i + 3] = a

    def fill_circle(self, cx: float, cy: float, rad: float, col) -> None:
        r, g, b, a = col
        x0, x1 = int(cx - rad), int(cx + rad) + 1
        y0, y1 = int(cy - rad), int(cy + rad) + 1
        for y in range(max(0, y0), min(H, y1)):
            for x in range(max(0, x0), min(W, x1)):
                if (x - cx) ** 2 + (y - cy) ** 2 <= rad * rad:
                    self.put(x, y, r, g, b, a)

    def fill_rect(self, x0: int, y0: int, x1: int, y1: int, col) -> None:
        r, g, b, a = col
        for y in range(max(0, y0), min(H, y1)):
            for x in range(max(0, x0), min(W, x1)):
                self.put(x, y, r, g, b, a)

    def fill_poly(self, pts, col) -> None:
        r, g, b, a = col
        ys = [p[1] for p in pts]
        ymin, ymax = int(min(ys)), int(max(ys))
        for y in range(max(0, ymin), min(H, ymax + 1)):
            xs = []
            for i in range(len(pts)):
                x1, y1 = pts[i]
                x2, y2 = pts[(i + 1) % len(pts)]
                if (y1 <= y < y2) or (y2 <= y < y1):
                    if y2 != y1:
                        xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                for x in range(int(xs[i]), int(xs[i + 1]) + 1):
                    self.put(x, y, r, g, b, a)

    def thick_line(self, x0: float, y0: float, x1: float, y1: float, w: float, col) -> None:
        steps = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
        for s in range(steps + 1):
            t = s / steps
            self.fill_circle(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, w / 2.0, col)

    def ring(self, cx: float, cy: float, rad: float, w: float, col) -> None:
        self.fill_circle(cx, cy, rad, col)
        self.fill_circle(cx, cy, max(0.1, rad - w), (0, 0, 0, 0))


# --- palette (flat, muted, animatic) ------------------------------------------

OCHRE = (176, 141, 87, 235)
OCHRE_D = (128, 100, 58, 235)
CLAY = (154, 112, 84, 235)
SLATE = (74, 88, 110, 235)
SLATE_L = (98, 114, 140, 235)
OLIVE = (112, 116, 78, 235)
DUSKBROWN = (104, 84, 66, 235)
TEALGREY = (86, 108, 112, 235)
SMOKEDARK = (58, 56, 60, 235)
EMBER = (214, 128, 64, 235)
CREAM = (228, 216, 188, 235)
DARK = (40, 38, 42, 235)
ASH = (120, 118, 116, 235)
SKIN_ABSTRACT = (196, 168, 140, 235)


def base_figure(c: Canvas, cloak: tuple, cloak_dark: tuple, head_col: tuple,
                head_r: int = 34, shoulder_w: int = 96, robe_h: int = 300) -> None:
    """Abstract front-view figure: robe trapezoid + head circle (no face)."""
    cx = W // 2
    head_cy = 120
    c.fill_poly([(cx - shoulder_w // 2, head_cy + head_r + 18),
                 (cx + shoulder_w // 2, head_cy + head_r + 18),
                 (cx + shoulder_w // 2 + 42, head_cy + head_r + 18 + robe_h),
                 (cx - shoulder_w // 2 - 42, head_cy + head_r + 18 + robe_h)], cloak)
    c.fill_poly([(cx - shoulder_w // 2, head_cy + head_r + 18),
                 (cx - 14, head_cy + head_r + 18),
                 (cx - 20, head_cy + head_r + 18 + robe_h),
                 (cx - shoulder_w // 2 - 42, head_cy + head_r + 18 + robe_h)], cloak_dark)
    c.fill_circle(cx, head_cy, head_r, head_col)


def satchel_band(c: Canvas, col, double: bool = False) -> None:
    c.thick_line(118, 200, 242, 330, 10, col)
    if double:
        c.thick_line(126, 214, 250, 344, 8, col)
    c.fill_circle(238, 338, 20, col)


# --- one function per stand-in -------------------------------------------------

def akvan_div(c: Canvas) -> None:
    base_figure(c, OCHRE, OCHRE_D, SKIN_ABSTRACT, head_r=36, shoulder_w=100)
    # braided crown braid: top knot + braid running down the right side
    c.fill_circle(180, 74, 14, OCHRE_D)
    for i in range(7):
        c.fill_circle(214 + (i % 2) * 4, 92 + i * 14, 8, OCHRE_D)
    # clay-token necklace
    for i in range(5):
        c.fill_circle(152 + i * 14, 212 + (i - 2) * (i - 2) * 2, 5, CREAM)
    # crystal reading lens held at chest
    c.ring(210, 268, 26, 8, SLATE_L)
    c.fill_circle(210, 268, 6, SLATE)


def simurgh(c: Canvas) -> None:
    # FORM-NEUTRAL by design (owner decision pending): wrapped-cloak silhouette,
    # double satchel band (CHAR-MESSENGER-001 anchor). No bird anatomy, no face.
    base_figure(c, TEALGREY, (60, 82, 86, 235), (46, 64, 68, 235), head_r=32, shoulder_w=92)
    c.fill_circle(180, 122, 36, (46, 64, 68, 235))  # hood/cloak top
    satchel_band(c, DUSKBROWN, double=True)


def black_div(c: Canvas) -> None:
    # CHAR-LITERAL-DIV-001: tall matte dry smoke-dark clay, lamp-point eyes,
    # no ornaments, no horns, flat and featureless.
    c.fill_poly([(128, 110), (232, 110), (252, 460), (108, 460)], SMOKEDARK)
    c.fill_circle(180, 92, 40, SMOKEDARK)
    c.fill_circle(166, 92, 5, EMBER)
    c.fill_circle(194, 92, 5, EMBER)


def arash(c: Canvas) -> None:
    base_figure(c, SLATE, (52, 64, 84, 235), SKIN_ABSTRACT, head_r=34, shoulder_w=124)
    # broad captain shoulders
    c.fill_poly([(96, 172), (264, 172), (264, 196), (96, 196)], SLATE)
    # ring of keys on LEFT hip (viewer's right) — Gatekeeper anchor, S08
    for i in range(3):
        c.fill_circle(258 + i * 6, 300 + i * 8, 6, CREAM)
        c.thick_line(258 + i * 6, 300 + i * 8, 272 + i * 6, 310 + i * 8, 3, CREAM)


def chapar(c: Canvas) -> None:
    # occupational courier; distinct from Simurgh: single satchel band,
    # road-worn dusty brown cloak, shorter.
    base_figure(c, DUSKBROWN, (76, 60, 46, 235), SKIN_ABSTRACT, head_r=30, shoulder_w=86)
    satchel_band(c, CLAY, double=False)
    c.fill_circle(140, 350, 14, CLAY)  # small pouch


def shahrasp(c: Canvas) -> None:
    base_figure(c, OLIVE, (84, 88, 58, 235), SKIN_ABSTRACT, head_r=32, shoulder_w=84)
    # ledger satchel on LEFT (CHAR-FIRST-SCRIBE-001 anchor)
    c.thick_line(128, 196, 232, 320, 9, DARK)
    c.fill_rect(214, 316, 262, 372, DARK)
    c.fill_rect(220, 322, 256, 366, CREAM)
    # ink-stained fingers
    c.fill_circle(138, 330, 7, DARK)
    c.fill_circle(152, 340, 6, DARK)
    # reed pen tucked at side
    c.thick_line(246, 250, 258, 320, 3, OCHRE_D)


def courier_rider(c: Canvas) -> None:
    # anonymous rider on a plain horse silhouette (collective, no identity)
    c.fill_poly([(90, 330), (270, 330), (286, 420), (74, 420)], ASH)
    c.fill_poly([(250, 250), (286, 330), (230, 330), (214, 262)], ASH)
    for x in (104, 150, 210, 258):
        c.fill_rect(x, 420, x + 16, 452, ASH)
    base_figure(c, DUSKBROWN, (76, 60, 46, 235), SKIN_ABSTRACT, head_r=22, shoulder_w=56)
    c.fill_poly([(152, 140), (208, 140), (222, 300), (138, 300)], DUSKBROWN)
    c.fill_circle(180, 118, 22, SKIN_ABSTRACT)


def villager(c: Canvas) -> None:
    base_figure(c, ASH, (92, 90, 88, 235), SKIN_ABSTRACT, head_r=26, shoulder_w=70, robe_h=250)
    # watchful head-lamp held at chest
    c.fill_circle(180, 260, 10, EMBER)


def charcoal_burner(c: Canvas) -> None:
    base_figure(c, (74, 68, 62, 235), (52, 48, 44, 235), SKIN_ABSTRACT, head_r=26, shoulder_w=70, robe_h=240)
    # small fire + calm smoke plume beside the figure
    c.fill_poly([(70, 400), (110, 400), (90, 356)], EMBER)
    for i in range(4):
        c.fill_circle(90 - (i % 2) * 8, 336 - i * 18, 7 - i // 2, ASH)


def apprentice(c: Canvas) -> None:
    base_figure(c, SLATE_L, (74, 88, 110, 235), SKIN_ABSTRACT, head_r=24, shoulder_w=64, robe_h=210)
    # practising hand + thin reed (mere ink context)
    c.fill_circle(236, 300, 9, SKIN_ABSTRACT)
    c.thick_line(240, 296, 262, 344, 3, OCHRE_D)


STANDINS = {
    "akvan_div": akvan_div,
    "simurgh": simurgh,
    "black_div": black_div,
    "arash": arash,
    "chapar": chapar,
    "shahrasp": shahrasp,
    "courier_rider": courier_rider,
    "villager": villager,
    "charcoal_burner": charcoal_burner,
    "apprentice": apprentice,
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="assets/standins")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    for name, fn in STANDINS.items():
        c = Canvas()
        fn(c)
        save_png(os.path.join(args.out, f"{name}.png"), c.px)
    # deterministic props (also pure vector, rendered BLANK)
    props = {
        "tablet": prop_tablet,
        "tablet_sealed_card": prop_sealed_card,
        "label_clay": prop_label,
        "oilcloth_packet": prop_oilcloth_packet,
        "ledger": prop_ledger,
        "reed_pen": prop_reed,
        "lamp": prop_lamp,
        "seal_lapis": prop_seal,
        "fire": prop_fire,
        "series_mark": prop_series_mark,
    }
    for name, fn in props.items():
        c = Canvas()
        fn(c)
        save_png(os.path.join(args.out, f"{name}.png"), c.px)
    print(f"standins + props written to {args.out} ({len(STANDINS) + len(props)} files)")
    return 0


# --- props (all render BLANK; text is programmatic overlay only) --------------

def prop_tablet(c: Canvas) -> None:
    c.fill_rect(100, 120, 260, 300, CLAY)
    c.fill_poly([(100, 120), (120, 120), (100, 148)], (120, 84, 60, 235))  # cracked corner
    c.fill_circle(238, 272, 22, (196, 176, 148, 235))  # dissolved seal scar (smooth)


def prop_sealed_card(c: Canvas) -> None:
    c.fill_rect(104, 150, 256, 290, CREAM)
    c.fill_circle(232, 262, 18, (64, 82, 148, 235))  # lapis wax seal (prop only)


def prop_label(c: Canvas) -> None:
    c.fill_rect(120, 180, 240, 260, CLAY)
    c.fill_rect(120, 180, 240, 196, OCHRE_D)


def prop_oilcloth_packet(c: Canvas) -> None:
    c.fill_poly([(110, 180), (250, 180), (230, 300), (130, 300)], (168, 148, 108, 235))
    c.thick_line(118, 196, 242, 196, 8, (128, 112, 78, 235))
    c.thick_line(150, 300, 210, 180, 6, (128, 112, 78, 235))


def prop_ledger(c: Canvas) -> None:
    c.fill_rect(100, 160, 260, 320, DARK)
    c.fill_rect(112, 172, 248, 308, (58, 52, 48, 235))
    c.fill_poly([(244, 160), (260, 160), (260, 200), (236, 200)], (58, 52, 48, 235))  # flap
    c.fill_circle(250, 184, 6, OCHRE)


def prop_reed(c: Canvas) -> None:
    c.thick_line(120, 340, 240, 140, 6, OCHRE_D)
    c.fill_poly([(236, 148), (252, 120), (248, 152)], DARK)


def prop_lamp(c: Canvas) -> None:
    c.fill_circle(180, 210, 34, CREAM)
    c.fill_poly([(150, 244), (210, 244), (180, 300)], SLATE)
    c.fill_circle(180, 200, 14, EMBER)


def prop_seal(c: Canvas) -> None:
    c.fill_circle(180, 240, 30, (64, 82, 148, 235))
    c.ring(180, 240, 18, 4, (40, 54, 108, 235))


def prop_fire(c: Canvas) -> None:
    c.fill_poly([(140, 320), (220, 320), (180, 220)], EMBER)
    c.fill_poly([(156, 320), (204, 320), (180, 258)], (240, 190, 110, 235))
    c.thick_line(140, 322, 220, 322, 8, (70, 56, 44, 235))


def prop_series_mark(c: Canvas) -> None:
    c.fill_rect(110, 150, 250, 310, CLAY)
    c.thick_line(150, 330, 230, 130, 8, OCHRE_D)
    c.fill_poly([(222, 140), (248, 110), (240, 150)], DARK)


if __name__ == "__main__":
    sys.exit(main())
