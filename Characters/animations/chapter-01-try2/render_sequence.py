"""Render all 120 frames and encode a review movie using Blender and FFmpeg.

Run with normal Python: python render_sequence.py [--workers 3] [--skip-render].
No pip dependencies. Frame count and child errors are checked before encoding.
"""

import argparse
import concurrent.futures
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "output"
parser = argparse.ArgumentParser()
parser.add_argument("--workers", type=int, default=3, choices=range(1, 5))
parser.add_argument("--skip-render", action="store_true")
args = parser.parse_args()


def render_chunk(bounds):
    first, last = bounds
    log_path = OUT / f"render-{first:03d}-{last:03d}.log"
    command = [
        "blender",
        "--background",
        "--python-exit-code",
        "1",
        "--python",
        str(ROOT / "render_local.py"),
        "--",
        "--frames",
        str(first),
        str(last),
    ]
    with log_path.open("w") as log:
        subprocess.run(command, check=True, stdout=log, stderr=subprocess.STDOUT)
    print(f"Rendered {first}-{last}", flush=True)


if not args.skip_render:
    bounds = [
        (1 + i * 120 // args.workers, (i + 1) * 120 // args.workers)
        for i in range(args.workers)
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(render_chunk, bounds))

expected = [OUT / "frames" / f"frame-{n:04d}.png" for n in range(1, 121)]
missing = [p.name for p in expected if not p.is_file()]
if missing:
    raise RuntimeError(f"Missing rendered frames: {missing}")
movie = OUT / "chapter-01-try2-sample.mp4"
# A restrained spatial/temporal denoise removes low-sample CPU grain.
# Raw frames remain untouched for direct comparison.
command = [
    "ffmpeg",
    "-y",
    "-framerate",
    "12",
    "-start_number",
    "1",
    "-i",
    str(OUT / "frames" / "frame-%04d.png"),
    "-vf",
    "hqdn3d=4:3:6:4.5,subtitles=captions.ass",
    "-frames:v",
    "120",
    "-c:v",
    "libx264",
    "-crf",
    "19",
    "-pix_fmt",
    "yuv420p",
    "-movflags",
    "+faststart",
    "-an",
    str(movie),
]
subprocess.run(command, cwd=ROOT, check=True)
probe = subprocess.run(
    [
        "ffprobe",
        "-v",
        "error",
        "-count_frames",
        "-show_streams",
        "-show_format",
        "-of",
        "json",
        str(movie),
    ],
    check=True,
    capture_output=True,
    text=True,
)
data = json.loads(probe.stdout)
video = [s for s in data["streams"] if s["codec_type"] == "video"]
assert len(video) == 1 and len(data["streams"]) == 1
assert int(video[0]["nb_read_frames"]) == 120
assert video[0]["avg_frame_rate"] == "12/1"
assert abs(float(data["format"]["duration"]) - 10.0) < 0.05
assert (video[0]["width"], video[0]["height"]) == (768, 432)
(OUT / "video-verification.json").write_text(json.dumps(data, indent=2) + "\n")
print("Verified: 120 frames, 12 fps, 10 seconds, silent 768x432 H.264", flush=True)
