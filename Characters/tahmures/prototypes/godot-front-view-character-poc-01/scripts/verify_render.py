#!/usr/bin/env python3
"""Render-frame verification against approved state composites.

GODOT_FRONT_VIEW_CHARACTER_POC_01 — stage A evidence check.

Checks that the Movie Maker render (renders/stage-a-preview.avi,
extracted frames in renders/frames/) does two things:

1. reproduces the human-approved head states pixel-faithfully in the
   head region (neutral / blink / thinking / open), by compositing the
   copied approved sprites in the documented layer order and comparing
   against the rendered frames; and
2. actually shows the scheduled beats: blink (eye region changes),
   thinking brow (brow band changes), open mouth (lower-face patch
   changes), raised temporary arm (arm region changes), and the point
   target mark (gold ring appears); and
3. keeps the re-laid-out HUD in its own screen zones (stage-A layout
   revision): no text crosses the head/diadem, no HUD text covers the
   torso, the state indicator is visible, both temporary-placeholder
   callouts are visible outside the silhouette, and the gold mark label
   appears only beside the ring during the pointing beat.

Screen mapping used by the scene: world coordinates equal the source
canvas coordinates (1086x1448); screen = world + (80, 30) because the
Camera2D sits at (560, 330) in a 1280x720 viewport.

Run from anywhere (paths are resolved relative to this file):

    python3 scripts/verify_render.py

Writes renders/verification.json with the numeric results.
Standard library only; deterministic.
"""

import json
import math
import os
import struct
import sys
import zlib

PROJ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FRAMES = os.path.join(PROJ, "renders", "frames")
BG = (23, 26, 34)  # scene background #171a22

NEUTRAL_ORDER = [
    "hair_back", "head_base", "ear_right", "ear_left", "beard",
    "lower_face_neutral", "nose", "eye_right", "eye_left",
    "eyebrow_right", "eyebrow_left", "moustache", "diadem_gold",
]


def load_png(path):
    with open(path, "rb") as fh:
        data = fh.read()
    pos = 8
    idat = b""
    while pos < len(data):
        ln = struct.unpack(">I", data[pos:pos + 4])[0]
        typ = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + ln]
        pos += 12 + ln
        if typ == b"IHDR":
            w, h, bd, ct, comp, filt, inter = struct.unpack(">IIBBBBB", chunk)
            assert bd == 8 and ct in (2, 6) and inter == 0, (path, bd, ct, inter)
        elif typ == b"IDAT":
            idat += chunk
        elif typ == b"IEND":
            break
    raw = zlib.decompress(idat)
    bpp = 4 if ct == 6 else 3
    stride = w * bpp
    out = bytearray(stride * h)
    prev = bytearray(stride)
    ptr = 0
    for y in range(h):
        f = raw[ptr]
        ptr += 1
        line = bytearray(raw[ptr:ptr + stride])
        ptr += stride
        if f == 1:
            for i in range(bpp, stride):
                line[i] = (line[i] + line[i - bpp]) & 0xFF
        elif f == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif f == 3:
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 0xFF
        elif f == 4:
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                b = prev[i]
                c = prev[i - bpp] if i >= bpp else 0
                pp = a + b - c
                pa, pb, pc = abs(pp - a), abs(pp - b), abs(pp - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 0xFF
        out[y * stride:(y + 1) * stride] = line
        prev = line
    return w, h, bytes(out)


_CACHE = {}


def layer(name):
    if name not in _CACHE:
        _CACHE[name] = load_png(os.path.join(PROJ, "assets", "approved-head", name + ".png"))
    return _CACHE[name]


def composite(state):
    """Composite an approved state over transparency, canvas coords."""
    order = list(NEUTRAL_ORDER)
    if state == "blink":
        order = [n + "_closed" if n in ("eye_right", "eye_left") else n for n in order]
    elif state == "open":
        order = ["lower_face_open_test" if n == "lower_face_neutral" else n for n in order]
    elif state == "thinking":
        order = []
        for n in NEUTRAL_ORDER:
            order.append(n)
            if n == "head_base":
                order.append("thinking_brow_underlay")
    w0, h0, _ = layer(order[0])
    W, H = w0, h0
    buf = bytearray(W * H * 4)
    for n in order:
        _, _, px = layer(n)
        dy = -1 if (state == "thinking" and n == "eyebrow_left") else 0
        dlo = max(0, dy)
        dhi = H + min(0, dy)
        for d in range(dlo, dhi):
            srow = (d - dy) * W * 4
            drow = d * W * 4
            for i in range(0, W * 4, 4):
                a = px[srow + i + 3]
                if a == 0:
                    continue
                sa = a / 255.0
                da = buf[drow + i + 3] / 255.0
                oa = sa + da * (1 - sa)
                if oa == 0:
                    continue
                for c in range(3):
                    sc = px[srow + i + c] / 255.0
                    dc = buf[drow + i + c] / 255.0
                    buf[drow + i + c] = int(round(255 * ((sc * sa + dc * da * (1 - sa)) / oa)))
                buf[drow + i + 3] = int(round(255 * oa))
    return W, H, bytes(buf)


def head_ref_over_bg(state):
    """Approved state composited over the scene background colour."""
    W, H, px = composite(state)
    out = bytearray(W * H * 3)
    for i in range(W * H):
        a = px[i * 4 + 3] / 255.0
        for c in range(3):
            out[i * 3 + c] = int(round(px[i * 4 + c] * a + BG[c] * (1 - a)))
    return W, H, out


def region_stats_vs_ref(frame_img, ref, W, H, x0, y0, x1, y1):
    fw, fh, fpx = frame_img
    fbpp = len(fpx) // (fw * fh)
    total = 0.0
    mx = 0
    n = 0
    for wy in range(y0, y1):
        for wx in range(x0, x1):
            sx, sy = wx + 80, wy + 30
            fi = (sy * fw + sx) * fbpp
            ri = (wy * W + wx) * 3
            for c in range(3):
                d = abs(fpx[fi + c] - ref[ri + c])
                total += d
                mx = max(mx, d)
                n += 1
    return total / max(n, 1), mx


def frame(name):
    return load_png(os.path.join(FRAMES, name))


def diff_region(fa, fb, region):
    (x0, y0, x1, y1) = region
    w = fa[0]
    pa, pb = fa[2], fb[2]
    bpp = len(pa) // (w * fa[1])
    total = 0.0
    mx = 0
    n = 0
    changed = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            i = (y * w + x) * bpp
            dsum = 0
            for c in range(3):
                d = abs(pa[i + c] - pb[i + c])
                dsum += d
                total += d
                mx = max(mx, d)
            n += 1
            if dsum / 3 > 12:
                changed += 1
    return total / max(n * 3, 1), mx, changed / max(n, 1)


def main():
    results = {}

    print("== head-region fidelity: render frame vs approved state composite ==")
    HEAD = (389, 15, 688, 385)
    for png, t, state in [
        ("t1.0s-idle-neutral.png", "t=1.00", "neutral"),
        ("t2.65s-blink-closed.png", "t=2.65", "blink"),
        ("t6.5s-thinking.png", "t=6.50", "thinking"),
        ("t11.0s-point-open-mouth.png", "t=11.00", "open"),
        ("t15.0s-return-neutral.png", "t=15.00", "neutral"),
    ]:
        fimg = frame(png)
        W, H, ref = head_ref_over_bg(state)
        mean, mx = region_stats_vs_ref(fimg, ref, W, H, *HEAD)
        results[f"head_match_{state}_{t}"] = {"mean_abs_diff": round(mean, 3), "max_abs_diff": mx}
        print(f"{png:32s} vs {state:8s} composite: mean={mean:6.3f}  max={mx}")

    print("\n== beat visibility (frame vs frame regional diffs) ==")
    f_idle = frame("t1.0s-idle-neutral.png")
    f_blink = frame("t2.65s-blink-closed.png")
    f_think = frame("t6.5s-thinking.png")
    f_hold = frame("t10.6s-point-hold.png")
    f_open = frame("t11.0s-point-open-mouth.png")
    f_end = frame("t15.0s-return-neutral.png")

    EYES = (559, 165, 688, 218)
    BROW = (556, 136, 694, 170)
    MOUTH = (577, 246, 665, 304)
    ARM = (690, 420, 1100, 566)

    checks = [
        ("blink_eyes_diff", f_blink, f_idle, EYES),
        ("baseline_eyes_diff", f_end, f_idle, EYES),
        ("thinking_brow_diff", f_think, f_idle, BROW),
        ("baseline_brow_diff", f_end, f_idle, BROW),
        ("open_mouth_diff", f_open, f_hold, MOUTH),
        ("baseline_mouth_diff", f_end, f_idle, MOUTH),
        ("arm_raised_diff", f_open, f_idle, ARM),
        ("baseline_arm_diff", f_end, f_idle, ARM),
    ]
    for name, fa, fb, region in checks:
        mean, mx, frac = diff_region(fa, fb, region)
        results[name] = {
            "mean_abs_diff": round(mean, 3),
            "max_abs_diff": mx,
            "changed_pixel_fraction": round(frac, 4),
        }
        print(f"{name:24s} mean={mean:7.3f} max={mx:3d} changed_frac={frac:.4f}")

    print("\n== point target mark presence ==")
    w = f_open[0]
    for tag, f in (("t11.0", f_open), ("t1.0", f_idle)):
        px = f[2]
        bpp = len(px) // (w * f[1])
        gold = 0
        samples = 0
        cx, cy = 1040, 380
        for ang in range(0, 360, 5):
            for r in (15, 16, 17, 18):
                x = int(cx + r * math.cos(math.radians(ang)))
                y = int(cy + r * math.sin(math.radians(ang)))
                i = (y * w + x) * bpp
                samples += 1
                if (abs(px[i] - 232) < 60 and abs(px[i + 1] - 184) < 60
                        and abs(px[i + 2] - 75) < 60):
                    gold += 1
        frac = gold / samples
        results[f"mark_ring_gold_fraction_{tag}"] = round(frac, 4)
        print(f"mark ring gold fraction {tag}: {frac:.3f} ({gold}/{samples})")

    print("\n== state discrimination: right state at the right time ==")
    W, H, ref_neutral = head_ref_over_bg("neutral")
    W, H, ref_blink = head_ref_over_bg("blink")
    W, H, ref_think = head_ref_over_bg("thinking")
    W, H, ref_open = head_ref_over_bg("open")
    MOUTH_WORLD = (500, 225, 580, 265)
    BROW_WORLD = (545, 100, 620, 140)
    EYE_WORLD = (545, 125, 615, 195)
    disc = [
        ("blink_frame_eye", f_blink, [("blink", ref_blink), ("neutral", ref_neutral)], EYE_WORLD),
        ("thinking_frame_brow", f_think, [("thinking", ref_think), ("neutral", ref_neutral)], BROW_WORLD),
        ("open_frame_mouth", f_open, [("open", ref_open), ("neutral", ref_neutral)], MOUTH_WORLD),
    ]
    for name, fimg, refs, region in disc:
        entry = {}
        for tag, ref in refs:
            m, mx = region_stats_vs_ref(fimg, ref, W, H, *region)
            entry[tag] = {"mean_abs_diff": round(m, 3), "max_abs_diff": mx}
            print(f"{name:22s} vs {tag:8s}: mean={m:6.3f} max={mx}")
        results[name] = entry
        expected = refs[0][0]
        others = [v["mean_abs_diff"] for tag, v in entry.items() if tag != expected]
        if not entry[expected]["mean_abs_diff"] < min(others):
            print(f"  WARNING: {name} does not match the expected {expected} state best")

    print("\n== HUD safe-layout pixel checks (stage-A layout revision) ==")
    hud_frames = {
        "t1.0": f_idle, "t2.65": f_blink, "t6.5": f_think,
        "t10.6": f_hold, "t11.0": f_open, "t15.0": f_end,
    }

    LIGHT_TEXT = (237, 240, 244)  # matches LS_title/LS_time/LS_state cores
    GOLD = (232, 184, 75)         # LS_mark / LS_fa

    def is_ink(p):
        return any(abs(p[c] - BG[c]) > 12 for c in range(3))

    def is_light_text(p):
        return all(abs(p[c] - LIGHT_TEXT[c]) <= 22 for c in range(3))

    def is_gold(p):
        return (abs(p[0] - GOLD[0]) < 60 and abs(p[1] - GOLD[1]) < 60
                and abs(p[2] - GOLD[2]) < 60)

    def count_pred(fimg, region, pred):
        x0, y0, x1, y1 = region
        w = fimg[0]
        px = fimg[2]
        bpp = len(px) // (w * fimg[1])
        n = 0
        for y in range(y0, y1):
            for x in range(x0, x1):
                i = (y * w + x) * bpp
                if pred((px[i], px[i + 1], px[i + 2])):
                    n += 1
        return n

    hud = {}

    def hud_check(name, region, pred, limit, mode):
        counts = {}
        ok = True
        for tag, fimg in hud_frames.items():
            n = count_pred(fimg, region, pred)
            counts[tag] = n
            ok = ok and (n <= limit if mode == "max" else n >= limit)
        hud[name] = {
            "region": list(region),
            "expectation": ("<=" if mode == "max" else ">=") + f" {limit}",
            "counts": counts,
            "pass": ok,
        }
        state = "PASS" if ok else "FAIL"
        compact = " ".join(f"{k}:{v}" for k, v in counts.items())
        print(f"{name:44s} {state}  [{compact}]")

    hud_check("language_band_left_of_head", (465, 80, 508, 112), is_ink, 0, "max")
    hud_check("language_band_right_of_head", (730, 80, 1280, 112), is_ink, 0, "max")
    hud_check("header_band_above_diadem", (560, 30, 680, 46), is_ink, 0, "max")
    hud_check("torso_band_free_of_hud_text", (465, 560, 770, 668), is_light_text, 0, "max")
    hud_check("state_label_visible", (16, 556, 430, 602), is_light_text, 100, "min")
    hud_check("torso_callout_visible", (0, 440, 465, 500), is_ink, 1000, "min")
    hud_check("arm_callout_visible", (900, 570, 1280, 660), is_ink, 1000, "min")

    mark_region = (1090, 395, 1280, 430)
    mark_counts = {tag: count_pred(fimg, mark_region, is_gold)
                   for tag, fimg in hud_frames.items()}
    mark_ok = (mark_counts["t10.6"] >= 50 and mark_counts["t11.0"] >= 50
               and all(mark_counts[t] <= 10
                       for t in ("t1.0", "t2.65", "t6.5", "t15.0")))
    mark_entry = {
        "region": list(mark_region),
        "expectation": ">= 50 at t10.6/t11.0, <= 10 otherwise",
        "counts": mark_counts,
        "pass": mark_ok,
    }
    state = "PASS" if mark_ok else "FAIL"
    compact = " ".join(f"{k}:{v}" for k, v in mark_counts.items())
    print(f"{'mark_label_gold_beside_ring':44s} {state}  [{compact}]")

    hud_pass = all(v["pass"] for v in hud.values()) and mark_ok
    results["hud_layout"] = {
        "checks": hud,
        "mark_label_gold_beside_ring": mark_entry,
        "pass": hud_pass,
    }
    print(f"HUD layout checks: {'PASS' if hud_pass else 'FAIL'}")

    out_path = os.path.join(PROJ, "renders", "verification.json")
    with open(out_path, "w") as fh:
        json.dump(
            {
                "screen_mapping": "screen = world + (80, 30)",
                "background_rgb": list(BG),
                "results": results,
            },
            fh,
            indent=2,
        )
        fh.write("\n")
    print(f"\nwrote {out_path}")
    return 0 if hud_pass else 1


if __name__ == "__main__":
    sys.exit(main())
