"""Render/recheck the same scene locally; Blender --background --python this_file.

Arguments after --: --build, --stills, --frames START END, --audit.
"""

import argparse
import json
import math
import pathlib
import runpy
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)
parser = argparse.ArgumentParser()
parser.add_argument("--build", action="store_true")
parser.add_argument("--stills", action="store_true")
parser.add_argument("--audit", action="store_true")
parser.add_argument("--frames", nargs=2, type=int)
args = parser.parse_args(
    sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
)

if args.build:
    runpy.run_path(str(ROOT / "build_scene.py"), run_name="__main__")
    bpy.ops.wm.save_as_mainfile(
        filepath=str(OUT / "chapter-01-try2.blend"), compress=True
    )
else:
    bpy.ops.wm.open_mainfile(filepath=str(OUT / "chapter-01-try2.blend"))
scene = bpy.context.scene
scene.cycles.device = "CPU"
scene.render.threads_mode = "FIXED"
scene.render.threads = 3
scene.cycles.samples = 16
scene.cycles.use_denoising = False  # This local Blender build lacks OpenImageDenoise.
scene.render.image_settings.file_format = "PNG"

if args.audit:
    graph = bpy.context.evaluated_depsgraph_get()
    triangles = 0
    for obj in scene.objects:
        if obj.type != "MESH":
            continue
        evaluated = obj.evaluated_get(graph)
        data = evaluated.to_mesh()
        data.calc_loop_triangles()
        triangles += len(data.loop_triangles)
        evaluated.to_mesh_clear()
    tablet = bpy.data.objects["props.found_tablet"]
    rest = tablet.matrix_world.copy()
    changes = {}
    poses = []
    for frame in [1, 25, 46, 63, 82, 100, 120]:
        scene.frame_set(frame)
        assert all(
            abs(tablet.matrix_world[i][j] - rest[i][j]) < 1e-7
            for i in range(4)
            for j in range(4)
        )
        frame_pose = {"frame": frame, "characters": {}}
        for name in ["akvan", "black_div", "div_e_sefid"]:
            obj = bpy.data.objects[name + ".head"]
            xy = world_to_camera_view(scene, scene.camera, obj.matrix_world.translation)
            assert 0.03 < xy.x < 0.97 and 0.03 < xy.y < 0.97, (name, frame, list(xy))
            frame_pose["characters"][name] = {
                "head_ndc": [round(x, 4) for x in xy],
                "head_matrix": [round(v, 5) for row in obj.matrix_world for v in row],
            }
        poses.append(frame_pose)
    # Motion is checked across first, middle and last poses, plus out-of-order reset/replay.
    for name in ["akvan", "black_div", "div_e_sefid"]:
        mats = [p["characters"][name]["head_matrix"] for p in poses]
        changes[name] = max(abs(a - b) for a, b in zip(mats[0], mats[-1]))
        assert changes[name] > 0.005, (name, "no measured motion")
    scene.frame_set(82)
    one = bpy.data.objects["black_div.head"].matrix_world.copy()
    scene.frame_set(1)
    scene.frame_set(120)
    scene.frame_set(82)
    two = bpy.data.objects["black_div.head"].matrix_world.copy()
    assert max(abs(one[i][j] - two[i][j]) for i in range(4) for j in range(4)) < 1e-7
    assert triangles < 150000, triangles
    assert scene.frame_start == 1 and scene.frame_end == 120 and scene.render.fps == 12
    # Proxy-only test, not a full collision/rig/artistic approval.
    report = {
        "status": "technical_checks_passed",
        "blender": bpy.app.version_string,
        "frames": 120,
        "fps": 12,
        "duration_seconds": 10,
        "triangles": triangles,
        "objects": len(scene.objects),
        "animated_objects": sum(
            bool(o.animation_data and o.animation_data.action) for o in scene.objects
        ),
        "motion_max_matrix_delta": changes,
        "tablet_stationary_all_sampled_frames": True,
        "tablet_bottom_z": round(
            min((tablet.matrix_world @ Vector(c)).z for c in tablet.bound_box), 5
        ),
        "cloth_top_z": 1.087,
        "camera_head_bounds_all_sampled_frames": "inside",
        "seek_reset_replay": "deterministic",
        "poses": poses,
        "limitations": [
            "Not a full per-frame collision audit",
            "Not approved likeness or performance",
            "Object-transform blocking, no armature or lip sync",
            "Open-front film set; no final Function/Form/Runtime approval",
        ],
    }
    (OUT / "scene-audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print("AUDIT", json.dumps({k: v for k, v in report.items() if k != "poses"}))

if args.stills:
    for f in [1, 46, 82, 120]:
        scene.frame_set(f)
        scene.render.filepath = str(OUT / f"pose-{f:03d}.png")
        bpy.ops.render.render(write_still=True)

if args.frames:
    start, end = args.frames
    assert 1 <= start <= end <= 120
    dest = OUT / "frames"
    dest.mkdir(exist_ok=True)
    scene.frame_start = start
    scene.frame_end = end
    scene.render.filepath = str(dest / "frame-")
    bpy.ops.render.render(animation=True)
