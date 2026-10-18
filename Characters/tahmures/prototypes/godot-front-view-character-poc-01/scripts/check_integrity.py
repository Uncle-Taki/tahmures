#!/usr/bin/env python3
"""Stage-A integrity checker for the Godot front-view character POC.

GODOT_FRONT_VIEW_CHARACTER_POC_01 — re-runnable, read-only checks:

1. Every copied approved-head asset still matches the pinned SHA-256
   recorded in the human-approved layout01-facial-states-01 package
   index (and, for v7 layers, the layout01-v7 manifest/index).
2. The temporary placeholder PNGs regenerate byte-identically from the
   committed deterministic generator (no hidden manual edits).
3. Every resource path referenced by scenes/main.tscn exists.
4. project.godot configures scenes/main.tscn as the main scene.
5. The AnimationPlayer master animation exists with the declared
   length/loop and beat key times that match scripts/main.gd's BEATS
   table.
6. The in-scene TEMPORARY PROTOTYPE PLACEHOLDER labels exist.
7. Every file listed in manifest.json exists with a matching hash, and
   every project file outside the report set is listed there.

Exit code 0 = all checks passed. Writes nothing (validation.json is
produced by the implementer from recorded evidence; this script is the
re-runnable equivalent for reviewers).

Paths resolve relative to this file, so it can be run from anywhere:

    python3 scripts/check_integrity.py [--repo-root PATH]

--repo-root defaults to ../../../.. from this script (the Tahmures
repository root that contains Characters/).
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, ".."))

FS_PACKAGE = "Characters/tahmures/prototypes/layout01-facial-states-01"
V7_PACKAGE = "Characters/tahmures/versions/layout01-v7"

FS_MANIFEST_SHA = "b081e9190f5ddf1e8eff643863b1bbee5ab7b4a176179a26703b1c4ad32e4ba4"
FS_INDEX_SHA = "6135d7b65239919ebb2834913aa20b93d391d16d40f2a35c4a499e337b1cea21"

EXPECTED_BEATS = [
    (0.0, "idle"),
    (2.5, "blink"),
    (2.85, "idle_after_blink"),
    (5.0, "thinking"),
    (8.0, "neutral_pause"),
    (9.0, "point_raise"),
    (10.5, "point_hold"),
    (10.8, "point_open_mouth"),
    (12.2, "point_hold_2"),
    (13.0, "return"),
    (14.0, "idle_end"),
]
TIMELINE_LENGTH = 18.0
STAGE_A_RENDER_SHA256 = "91bcb60405d0b3a85a0537cf01430962dc218807d4bb40aa82dacc4b25ed8b87"
STAGE_A_FRAME_HASHES = {
    "t1.0s-idle-neutral.png": "c9c09e542cf7bbebe4d3f987821c00fcf01783f11aaf9892222fd85e9655d37f",
    "t10.6s-point-hold.png": "7a70c2c613981d0cc4f5de60c22eed5f3d564c6f0af6110611771e9b58c231de",
    "t11.0s-point-open-mouth.png": "9c17f41b94e32a4722839aa29413df8799e6577137fa0cfbcabd39cf6e1c5952",
    "t15.0s-return-neutral.png": "ca99a637b5ab9bc6ad86fb5cdcd1e7d4bf9da1796d5bfd0d94f1243031c2bdc9",
    "t2.65s-blink-closed.png": "93af9c5e645ff26eee3ebad43cf492a2a19050fdea4ace1500112c6138466441",
    "t6.5s-thinking.png": "6c32f0ecabb4349e5d3ed04a09193858cbe39cb48313bd75ee712b68245c6ca9",
}

# Compact on-screen state labels (stage-A layout revision): the HUD state
# indicator must stay short so it never spans the character.
COMPACT_STATE_LABELS = {
    "IDLE", "BLINK", "THINKING", "POINT", "POINT + OPEN TEST", "RETURN",
}

# HUD safe-layout zones (screen pixels, 1280x720). Measured from the
# approved-art character extents at every key state:
#   - head/hair/torso/rest-arms occupy the core rect below;
#   - the pointing arm sweeps inside a circle of radius 240 around the
#     shoulder at screen (728, 460) and the hand approaches the mark ring
#     at screen (1016..1064, 356..404);
#   - so fixed UI must not intersect the core rect, the sweep circle, or
#     the mark rect (the bottom-right pocket outside the circle is safe).
VIEWPORT = (0, 0, 1280, 720)
CHARACTER_CORE = (465, 46, 775, 720)
ARM_SWEEP_CENTRE = (728.0, 460.0)
ARM_SWEEP_RADIUS = 240.0
MARK_RECT = (1005, 350, 1075, 410)

# Fixed HUD controls (CanvasLayer "HUD") whose rects are parsed from
# main.tscn and must respect the safe-layout zones and stay pairwise
# disjoint. BarFill is excluded (it is script-animated inside BarTrack).
HUD_CONTROL_NODES = [
    "Title", "VersionLine", "Subtitle", "FaNameLabel", "LanguageLine",
    "StateCaption", "StateLabel", "TimeLabel", "HintLabel", "BarTrack",
]
# World-space callout labels (children of World/Rig at origin): their
# control offsets are world coordinates; screen = world + (80, 30).
WORLD_CALLOUT_NODES = ["LabelTorsoNote", "LabelArmNote"]
# Mark label: child of World/PointTarget at world (960, 350).
POINT_TARGET_POS = (960.0, 350.0)
SCREEN_OFFSET = (80.0, 30.0)

REPORT_FILES = {
    "README.md", "manifest.json", "validation.json", "implementation-report.md",
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def check(label, ok, detail=""):
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {label}" + (f" — {detail}" if detail else ""))
    return ok


def parse_node_rects(tscn, names):
    """Parse offset_* rects of [node name=...] blocks from main.tscn."""
    rects = {}
    for name in names:
        m = re.search(
            r'\[node name="' + re.escape(name) + r'"[^\n]*\n(.*?)(?=\n\[)',
            tscn, re.S,
        )
        if not m:
            continue
        block = m.group(1)
        vals = {}
        for key in ("offset_left", "offset_top", "offset_right", "offset_bottom"):
            km = re.search(r"^" + key + r" = (-?[0-9.]+)$", block, re.M)
            if km:
                vals[key] = float(km.group(1))
        if len(vals) == 4:
            rects[name] = (vals["offset_left"], vals["offset_top"],
                           vals["offset_right"], vals["offset_bottom"])
    return rects


def rects_intersect(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def rect_near_circle(rect, centre, radius):
    """True when rect is within radius of centre (nearest-point test)."""
    nx = min(max(centre[0], rect[0]), rect[2])
    ny = min(max(centre[1], rect[1]), rect[3])
    return (nx - centre[0]) ** 2 + (ny - centre[1]) ** 2 <= radius * radius


def in_viewport(rect):
    return (rect[0] >= 4 and rect[1] >= 4
            and rect[2] <= VIEWPORT[2] - 16 and rect[3] <= VIEWPORT[3] - 16)


def respects_zones(rect):
    """Fixed UI must stay out of the character core rect, the arm-sweep
    circle, and the mark-ring rect."""
    if rects_intersect(rect, CHARACTER_CORE):
        return False
    if rect_near_circle(rect, ARM_SWEEP_CENTRE, ARM_SWEEP_RADIUS):
        return False
    if rects_intersect(rect, MARK_RECT):
        return False
    return True


def check_hud_layout(tscn, ok_only=True):
    """Stage-A layout revision assertions (all machine-checkable)."""
    ok = True

    hud = parse_node_rects(tscn, HUD_CONTROL_NODES)
    ok &= check(
        "HUD control nodes parsed from main.tscn",
        len(hud) == len(HUD_CONTROL_NODES),
        f"{sorted(hud)}" if len(hud) != len(HUD_CONTROL_NODES)
        else f"{len(hud)} nodes",
    )

    world = parse_node_rects(tscn, WORLD_CALLOUT_NODES)
    ok &= check(
        "world callout labels parsed from main.tscn",
        len(world) == len(WORLD_CALLOUT_NODES),
        f"{sorted(world)}" if len(world) != len(WORLD_CALLOUT_NODES)
        else f"{len(world)} nodes",
    )
    world_screen = {
        n: (r[0] + SCREEN_OFFSET[0], r[1] + SCREEN_OFFSET[1],
            r[2] + SCREEN_OFFSET[0], r[3] + SCREEN_OFFSET[1])
        for n, r in world.items()
    }

    target = parse_node_rects(tscn, ["TargetLabel"])
    if "TargetLabel" in target:
        r = target["TargetLabel"]
        world_screen["TargetLabel"] = (
            r[0] + POINT_TARGET_POS[0] + SCREEN_OFFSET[0],
            r[1] + POINT_TARGET_POS[1] + SCREEN_OFFSET[1],
            r[2] + POINT_TARGET_POS[0] + SCREEN_OFFSET[0],
            r[3] + POINT_TARGET_POS[1] + SCREEN_OFFSET[1],
        )
    ok &= check(
        "TargetLabel parsed and mapped to screen",
        "TargetLabel" in world_screen,
        f"screen rect {world_screen.get('TargetLabel')}",
    )

    all_rects = {}
    all_rects.update(hud)
    all_rects.update(world_screen)

    # (a) viewport bounds
    outside = [n for n, r in sorted(all_rects.items()) if not in_viewport(r)]
    ok &= check(
        "all fixed UI rects inside viewport with margin",
        not outside,
        f"outside: {outside}" if outside else f"{len(all_rects)} rects ok",
    )

    # (b) character-zone separation (left / right / above + sweep + mark)
    violating = [n for n, r in sorted(all_rects.items()) if not respects_zones(r)]
    ok &= check(
        "no fixed UI rect intersects the character/arm/mark zone",
        not violating,
        f"violating: {violating}" if violating else f"{len(all_rects)} rects clear",
    )

    # (c) pairwise disjointness of all fixed UI rects
    names = sorted(all_rects)
    clashes = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            if rects_intersect(all_rects[a], all_rects[b]):
                clashes.append(f"{a} x {b}")
    ok &= check(
        "fixed UI rects are pairwise disjoint",
        not clashes,
        f"clashes: {clashes}" if clashes else f"{len(names)} rects, no clashes",
    )

    # (d) compact state labels in scripts/main.gd
    gd = open(os.path.join(PROJ, "scripts", "main.gd"), encoding="utf-8").read()
    labels = set(re.findall(r'"label": "([^"]+)"', gd))
    bad_labels = sorted(l for l in labels if l not in COMPACT_STATE_LABELS)
    ok &= check(
        "state labels are compact (bounded-width HUD set)",
        not bad_labels and len(labels) > 0,
        f"labels={sorted(labels)}" if bad_labels else f"{len(labels)} compact labels",
    )

    # (e) bar + tick geometry from main.gd constants
    def const(name):
        m = re.search(r'^const ' + name + r' := ([0-9.]+)$', gd, re.M)
        return float(m.group(1)) if m else None

    bar_x, bar_y, bar_w, bar_h = (const("BAR_X"), const("BAR_Y"),
                                  const("BAR_W"), const("BAR_H"))
    tick_off = const("TICK_LABEL_Y_OFFSET")
    bar_ok = (bar_x is not None and bar_x >= 16
              and bar_x + bar_w <= CHARACTER_CORE[0]
              and bar_y >= 640 and bar_y + bar_h <= 700 and tick_off is not None
              and bar_y + tick_off >= bar_y + bar_h + 4)
    ok &= check(
        "progress bar and tick labels stay in the left control column",
        bar_ok,
        f"BAR_X={bar_x} BAR_Y={bar_y} BAR_W={bar_w} BAR_H={bar_h} tick_off={tick_off}",
    )

    # (f) language line must not reach the head band (y 80..110)
    if "LanguageLine" in hud:
        r = hud["LanguageLine"]
        ok &= check(
            "language line stays left of the head silhouette",
            r[2] <= CHARACTER_CORE[0] and r[1] >= 46,
            f"rect={r}",
        )

    # (g) state label must not span the torso (left column only)
    if "StateLabel" in hud:
        r = hud["StateLabel"]
        ok &= check(
            "state label stays in the left control column",
            r[2] <= CHARACTER_CORE[0] and r[1] >= 500,
            f"rect={r}",
        )

    return ok


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        default=os.path.normpath(os.path.join(PROJ, "..", "..", "..", "..")),
    )
    args = parser.parse_args()
    root = os.path.abspath(args.repo_root)
    ok = True

    # 1. pinned input package identity
    fs_manifest_path = os.path.join(root, FS_PACKAGE, "manifest.json")
    fs_index_path = os.path.join(root, FS_PACKAGE, "files-sha256.json")
    ok &= check(
        "input manifest.json pinned hash",
        sha256(fs_manifest_path) == FS_MANIFEST_SHA,
    )
    ok &= check(
        "input files-sha256.json pinned hash",
        sha256(fs_index_path) == FS_INDEX_SHA,
    )

    fs_index = json.load(open(fs_index_path))
    v7_index = json.load(open(os.path.join(root, V7_PACKAGE, "files-sha256.json")))

    approved_dir = os.path.join(PROJ, "assets", "approved-head")
    approved = sorted(f for f in os.listdir(approved_dir) if f.endswith(".png"))
    mismatched = []
    for f in approved:
        got = sha256(os.path.join(approved_dir, f))
        if f in ("eye_left_closed.png", "eye_right_closed.png", "thinking_brow_underlay.png"):
            expect = fs_index["assets/" + f]
        elif f.startswith("lower_face"):
            expect = v7_index["mouths/" + f]
        elif f in ("hair_back.png", "head_base.png", "diadem_gold.png"):
            expect = v7_index["head/" + f]
        else:
            expect = v7_index["face/" + f]
        if got != expect:
            mismatched.append(f)
    ok &= check(
        "approved-head assets match source package hashes",
        not mismatched and len(approved) == 17,
        f"{len(approved)} files checked" + (f", mismatched: {mismatched}" if mismatched else ""),
    )

    # 2. temporary placeholder determinism
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            [sys.executable, os.path.join(HERE, "generate_temporary_body.py"), "--out", tmp],
            check=True, capture_output=True,
        )
        regen_ok = True
        for f in ("torso.png", "upper_arm.png", "forearm.png", "hand_point.png",
                  "point_target.png", "placeholders.json"):
            a = os.path.join(PROJ, "assets", "temporary-body", f)
            b = os.path.join(tmp, f)
            if not os.path.exists(a) or sha256(a) != sha256(b):
                regen_ok = False
    ok &= check("temporary placeholders regenerate byte-identically", regen_ok)

    # 3. tscn references exist
    tscn_path = os.path.join(PROJ, "scenes", "main.tscn")
    tscn = open(tscn_path, encoding="utf-8").read()
    refs = re.findall(r'^\[ext_resource [^\]]*path="res://([^"]+)"', tscn, re.M)
    missing = [r for r in refs if not os.path.exists(os.path.join(PROJ, r))]
    ok &= check(
        "all main.tscn ext_resource paths exist",
        not missing and len(refs) >= 23,
        f"{len(refs)} references" + (f", missing: {missing}" if missing else ""),
    )

    # 4. main scene configuration
    pg = open(os.path.join(PROJ, "project.godot"), encoding="utf-8").read()
    ok &= check(
        "project.godot main scene is scenes/main.tscn",
        'run/main_scene="res://scenes/main.tscn"' in pg,
    )
    ok &= check(
        "project.godot pins GL Compatibility renderer",
        'renderer/rendering_method="gl_compatibility"' in pg,
    )

    # Stage-B0 remains an inert boundary: it validates expected owner inputs,
    # but creates no audio and cannot play anything in the accepted Stage-A
    # scene. Caption fixtures are explicitly test-only strings.
    main_gd = open(os.path.join(PROJ, "scripts", "main.gd"), encoding="utf-8").read()
    pipeline_path = os.path.join(PROJ, "scripts", "audio_subtitle_pipeline.gd")
    tests_path = os.path.join(PROJ, "scripts", "tests", "audio_subtitle_pipeline_test.gd")
    audio_player = re.search(
        r'\[node name="NarrationPlayer" type="AudioStreamPlayer" parent="\."\]\n(.*?)(?=\n\[|\Z)',
        tscn, re.S,
    )
    audio_player_block = audio_player.group(1) if audio_player else ""
    ok &= check(
        "B0 audio player is inert and source remains absent",
        bool(audio_player)
        and "autoplay = false" in audio_player_block
        and "stream = null" in audio_player_block
        and "narration_player.play(" not in main_gd
        and os.path.isfile(pipeline_path)
        and os.path.isfile(tests_path)
        and not any(os.path.exists(os.path.join(PROJ, "audio", lang, name))
                    for lang in ("en", "fa")
                    for name in ("narration.wav", "narration.txt", "subtitles.vtt")),
    )
    ok &= check(
        "caption test is opt-in and marked non-approved",
        '"--caption-test"' in main_gd
        and "NOT OWNER-APPROVED NARRATION" in main_gd
        and os.path.isfile(os.path.join(PROJ, "scripts", "tests", "fixtures", "en-caption.vtt"))
        and os.path.isfile(os.path.join(PROJ, "scripts", "tests", "fixtures", "fa-caption.vtt")),
    )
    stage_a_render = os.path.join(PROJ, "renders", "stage-a-preview.avi")
    stage_a_frames = os.path.join(PROJ, "renders", "frames")
    ok &= check(
        "accepted Stage-A render and six frames remain byte-identical",
        os.path.isfile(stage_a_render)
        and sha256(stage_a_render) == STAGE_A_RENDER_SHA256
        and all(os.path.isfile(os.path.join(stage_a_frames, name))
                and sha256(os.path.join(stage_a_frames, name)) == digest
                for name, digest in STAGE_A_FRAME_HASHES.items()),
    )

    # 5. animation identity and beat keys
    ok &= check(
        "animation library/animation names present",
        '&"preview": SubResource("AnimationLibrary_preview")' in tscn
        and '&"preview_master": SubResource("Animation_master")' in tscn,
    )
    ok &= check(
        "master animation length is 18.0 s with linear loop",
        re.search(r"^length = 18(\.0)?$", tscn, re.M) is not None
        and re.search(r"^loop_mode = 1$", tscn, re.M) is not None,
    )
    # visible-track key times must include every beat time
    key_times = set()
    for m in re.finditer(r'"times": PackedFloat32Array\(([^)]*)\)', tscn):
        for t in m.group(1).split(","):
            t = t.strip()
            if t:
                key_times.add(round(float(t), 3))
    beat_times = {round(t, 3) for t, _ in EXPECTED_BEATS}
    missing_beats = sorted(beat_times - key_times)
    ok &= check(
        "beat times from scripts/main.gd BEATS appear as animation key times",
        not missing_beats,
        f"missing: {missing_beats}" if missing_beats else f"{len(beat_times)} beat times present",
    )
    # discrete state toggles at the exact approved windows
    for path, times in [
        ("World/Rig/Head/eye_left:visible", [2.5, 2.85]),
        ("World/Rig/Head/eye_left_closed:visible", [2.5, 2.85]),
        ("World/Rig/Head/thinking_brow_underlay:visible", [5.0, 8.0]),
        ("World/Rig/Head/lower_face_neutral:visible", [10.8, 12.2]),
        ("World/Rig/Head/lower_face_open_test:visible", [10.8, 12.2]),
    ]:
        block = re.search(
            r'path = NodePath\("' + re.escape(path) + r'"\).*?"times": PackedFloat32Array\(([^)]*)\)',
            tscn, re.S,
        )
        got_times = {round(float(t), 3) for t in block.group(1).split(",") if t.strip()}
        ok &= check(
            f"state toggle keys for {path}",
            all(round(t, 3) in got_times for t in times),
            f"keys={sorted(got_times)}",
        )
    # brow shift is exactly the approved 1 px
    brow = re.search(
        r'path = NodePath\("World/Rig/Head/eyebrow_left:position"\).*?"values": \[([^\]]*)\]',
        tscn, re.S,
    )
    ok &= check(
        "thinking brow shift is exactly 1 source pixel",
        brow is not None and "Vector2(0, -1)" in brow.group(1),
        brow.group(1).strip() if brow else "not found",
    )

    # 6. placeholder labels
    ok &= check(
        "in-scene TEMPORARY PROTOTYPE PLACEHOLDER labels present",
        tscn.count("TEMPORARY PROTOTYPE PLACEHOLDER") >= 2
        and tscn.count("NOT APPROVED CHARACTER ART") >= 2,
        f"{tscn.count('TEMPORARY PROTOTYPE PLACEHOLDER')} labels",
    )

    # 6b. HUD safe layout (stage-A layout revision 01)
    ok &= check_hud_layout(tscn)

    # 7. manifest cross-check
    manifest_path = os.path.join(PROJ, "manifest.json")
    if not os.path.exists(manifest_path):
        ok &= check("manifest.json exists", False)
    else:
        manifest = json.load(open(manifest_path))
        listed = manifest.get("project_files", {})
        hash_bad = []
        for rel, expect in sorted(listed.items()):
            p = os.path.join(PROJ, rel)
            if not os.path.exists(p):
                hash_bad.append(rel)
            elif sha256(p) != expect:
                hash_bad.append(rel)
        ok &= check(
            "manifest.json project file hashes match the tree",
            not hash_bad,
            f"{len(listed)} files listed" + (f", bad: {hash_bad}" if hash_bad else ""),
        )
        # everything except the report set and editor/python caches must be listed
        unlisted = []
        for cur, dirs, names in os.walk(PROJ):
            dirs[:] = [d for d in dirs if d not in (".godot", "__pycache__")]
            for n in names:
                rel = os.path.relpath(os.path.join(cur, n), PROJ)
                if rel in REPORT_FILES:
                    continue
                if rel not in listed:
                    unlisted.append(rel)
        ok &= check(
            "all non-report project files are listed in manifest.json",
            not unlisted,
            f"unlisted: {unlisted}" if unlisted else "complete",
        )

    print()
    if ok:
        print("RESULT: ALL INTEGRITY CHECKS PASSED")
        return 0
    print("RESULT: INTEGRITY CHECKS FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
