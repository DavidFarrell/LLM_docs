#!/usr/bin/env bash
# Render every scene. Usage: ./render_all.sh [quality l|m|h|p|k] [parallel jobs]
# Final video uses -qh (1080p60). Manim's partial-movie CRF is patched to 12 for a clean master.
set -e
Q=${1:-h}; JOBS=${2:-4}
cd "$(dirname "$0")"
sed -i 's/"crf": "23",  # ffmpeg: -crf/"crf": "12",  # ffmpeg: -crf/' \
  "$(/opt/venv/bin/python -c 'import manim, os; print(os.path.join(os.path.dirname(manim.__file__), "scene", "scene_file_writer.py"))')"
mkdir -p build/logs
for f in scenes/s*.py; do
  cls=$(grep -o "^class S[0-9A-Za-z_]*" "$f" | head -1 | cut -d' ' -f2)
  echo "$f $cls"
done | xargs -P "$JOBS" -L 1 bash -c './render.sh '"$Q"' "$0" "$1" > build/logs/$1.log 2>&1 && echo "done $1" || echo "FAILED $1"'
