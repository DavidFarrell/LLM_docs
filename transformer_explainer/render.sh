#!/usr/bin/env bash
# Usage: ./render.sh <quality l|m|h> <scene_file> <SceneName>
set -e
Q=${1:-l}; FILE=$2; NAME=$3
cd "$(dirname "$0")"
/opt/venv/bin/manim -q$Q --disable_caching --media_dir build/media --progress_bar none "$FILE" "$NAME"
