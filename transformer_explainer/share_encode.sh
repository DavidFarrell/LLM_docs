#!/usr/bin/env bash
# Two-pass 720p30 "share" encode sized to fit a ~29 MiB upload limit.
# Usage: ./share_encode.sh [video_kbps=195] [audio_kbps=72]
set -e
cd "$(dirname "$0")"
VK=${1:-195}; AK=${2:-72}
IN=output/attention_is_all_you_need_explained.mp4
OUT=output/attention_is_all_you_need_explained_720p.mp4
VF="fps=30,scale=1280:720:flags=lanczos"
ffmpeg -v error -y -i "$IN" -vf "$VF" -c:v libx264 -preset slow -tune animation -b:v ${VK}k \
  -pass 1 -passlogfile build/x264share -an -sn -dn -f null /dev/null
ffmpeg -v error -y -i "$IN" -vf "$VF" -map 0:v -map 0:a -map 0:s -map_chapters 0 \
  -c:v libx264 -preset slow -tune animation -b:v ${VK}k -maxrate $((VK * 4))k -bufsize $((VK * 8))k \
  -pass 2 -passlogfile build/x264share -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a ${AK}k -c:s mov_text -metadata:s:s:0 language=eng -disposition:s:0 0 \
  -movflags +faststart "$OUT"
ls -la "$OUT"
