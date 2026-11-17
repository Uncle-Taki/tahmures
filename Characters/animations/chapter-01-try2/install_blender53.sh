#!/usr/bin/env bash
# Run on Mehdi's Ubuntu workstation; does not download Blender.
set -euo pipefail
archive_dir="/home/mehdi/Downloads/Persepolis/Compressed"
archive="$archive_dir/blender-5.3.0-linux-x64.tar.xz"
install_dir="$HOME/opt/blender-5.3.0"
if [[ ! -f "$archive" ]]; then
  echo "Expected archive not found: $archive" >&2
  find "$archive_dir" -maxdepth 2 -type f -iname '*blender*' -print
  exit 1
fi
xz -t "$archive"
mkdir -p "$HOME/opt" "$HOME/.local/bin"
stage="$(mktemp -d "$HOME/opt/.blender-5.3.0.XXXXXXXX")"
trap 'rm -rf -- "$stage"' EXIT
tar -xf "$archive" -C "$stage"
candidate="$stage/blender-5.3.0-linux-x64"
test -x "$candidate/blender"
"$candidate/blender" --version | head -n 1
"$candidate/blender" --background --factory-startup --python-expr \
  'import bpy; assert bpy.app.version == (5, 3, 0), bpy.app.version; print("VERSION_OK", bpy.app.version_string)'
if [[ -e "$install_dir" ]]; then
  echo "Keeping existing install: $install_dir"
  "$install_dir/blender" --background --factory-startup --python-expr \
    'import bpy; assert bpy.app.version == (5, 3, 0), bpy.app.version'
else
  mv -- "$candidate" "$install_dir"
fi
link="$HOME/.local/bin/blender-5.3"
if [[ -e "$link" && ! -L "$link" ]]; then
  echo "Refusing to replace non-symlink: $link" >&2
  exit 1
fi
ln -sfn "$install_dir/blender" "$link"
"$link" --version
echo "Launch: $link"
