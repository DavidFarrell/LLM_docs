#!/usr/bin/env bash
# Final assembly: mix audio from the render logs, add the dust layer, encode the MP4.
# Usage: ./assemble.sh [quality_dir=1080p60] [crf=18]
set -e
Q=${1:-1080p60}; CRF=${2:-18}
cd "$(dirname "$0")"
PY=/opt/venv/bin/python
$PY mix.py "$Q"
TOTAL=$(ffprobe -v error -show_entries format=duration -of csv=p=0 build/mix.wav)
[ -f build/particles.mp4 ] && [ "$(ffprobe -v error -show_entries format=duration -of csv=p=0 build/particles.mp4 | cut -d. -f1)" -ge "${TOTAL%.*}" ] \
  || $PY particles.py "$(echo "$TOTAL + 2" | bc)"
mkdir -p output
OUT=output/attention_is_all_you_need_explained.mp4
ffmpeg -v warning -stats -y \
  -f concat -safe 0 -i build/concat.txt \
  -i build/particles.mp4 \
  -i build/mix.wav \
  -i build/subtitles.srt \
  -f ffmetadata -i build/chapters.txt \
  -filter_complex "[1:v]scale=1920:1080:flags=bicubic,fps=60,format=gbrp[p];[0:v]format=gbrp[m];[m][p]blend=all_mode=screen:all_opacity=0.85:shortest=1,format=yuv420p[v]" \
  -map "[v]" -map 2:a -map 3:s -map_metadata 4 -map_chapters 4 \
  -c:v libx264 -preset slow -crf "$CRF" -tune animation -profile:v high -pix_fmt yuv420p -g 120 \
  -c:a aac -b:a 256k -ar 48000 \
  -c:s mov_text -metadata:s:s:0 language=eng -disposition:s:0 0 \
  -movflags +faststart "$OUT"
cp build/subtitles.srt output/attention_is_all_you_need_explained.srt
ls -la output/
