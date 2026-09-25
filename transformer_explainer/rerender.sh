#!/usr/bin/env bash
# Re-render specific scenes at 1080p60: ./rerender.sh S01_ColdOpen S02_Recurrence ...
cd "$(dirname "$0")"
for cls in "$@"; do
  f=$(grep -l "^class $cls" scenes/*.py)
  ./render.sh h "$f" "$cls" > "build/logs/$cls.log" 2>&1 && echo "done $cls" || echo "FAILED $cls"
done
