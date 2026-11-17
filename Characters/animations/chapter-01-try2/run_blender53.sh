#!/usr/bin/env bash
# Run from any directory: bash /path/to/run_blender53.sh [existing-candidate-directory]
set -euo pipefail
bundle_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
blender_bin="${BLENDER_BIN:-$HOME/.local/bin/blender-5.3}"
test -x "$blender_bin" || { echo "Blender not found: $blender_bin" >&2; exit 1; }
command -v ffmpeg >/dev/null
command -v ffprobe >/dev/null
command -v python3 >/dev/null
if [[ $# -gt 1 ]]; then
  echo "Usage: bash run_blender53.sh [existing-candidate-directory]" >&2
  exit 1
fi
if [[ $# -eq 1 ]]; then
  trial="$(cd -- "$1" && pwd)"
  test -f "$trial/render_local.py"
  test -f "$trial/output/chapter-01-try2.blend"
else
  mkdir -p "$bundle_dir/compatibility"
  trial="$(mktemp -d "$bundle_dir/compatibility/blender-5.3-XXXXXXXX")"
  cp -- "$bundle_dir/build_scene.py" "$bundle_dir/render_local.py" "$trial/"
  "$blender_bin" --background --factory-startup --python-exit-code 1 \
    --python "$trial/render_local.py" -- --build --audit
  "$blender_bin" --background --factory-startup --python-exit-code 1 \
    --python "$trial/render_local.py" -- --stills
fi
printf 'Candidate: %s\n' "$trial"
if [[ -e "$trial/output/preview.mp4" ]]; then
  echo "Keeping existing preview.mp4; choose a new run directory to rerender." >&2
  exit 1
fi
# The same shell owns trial for rendering, encoding and verification.
"$blender_bin" --background --factory-startup --python-exit-code 1 \
  --python "$trial/render_local.py" -- --frames 1 120
for ((frame=1; frame<=120; frame++)); do
  printf -v image_path '%s/output/frames/frame-%04d.png' "$trial" "$frame"
  test -s "$image_path" || { echo "Missing frame: $image_path" >&2; exit 1; }
done
ffmpeg -n -framerate 12 -start_number 1 \
  -i "$trial/output/frames/frame-%04d.png" -frames:v 120 \
  -c:v libx264 -pix_fmt yuv420p "$trial/output/preview.mp4"
ffprobe -v error -count_frames -select_streams v:0 \
  -show_entries stream=codec_name,width,height,r_frame_rate,nb_read_frames:format=duration \
  -of json "$trial/output/preview.mp4" > "$trial/output/video-verification.json"
python3 - "$trial/output/video-verification.json" <<'PY'
import json, sys
from fractions import Fraction
report = json.load(open(sys.argv[1]))
stream = report["streams"][0]
assert stream["codec_name"] == "h264", stream
assert (stream["width"], stream["height"]) == (768, 432), stream
assert Fraction(stream["r_frame_rate"]) == 12, stream
assert int(stream["nb_read_frames"]) == 120, stream
assert abs(float(report["format"]["duration"]) - 10) < 0.05, report
print("VIDEO VERIFIED: H.264, 768 x 432, 12 FPS, 120 frames, 10 seconds.")
PY
printf 'Video: %s/output/preview.mp4\n' "$trial"
