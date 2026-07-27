#!/bin/bash
# Frame strips: 4 frames across the loop per candidate, stacked into one image.
# The strip is a claim about the LOOP; a single frame is a claim about one instant.
ITEM="$1"; shift
W="/tmp/fm/$ITEM"
rm -rf "$W/strip"; mkdir -p "$W/strip"
for n in "$@"; do
  f=$(ls "$W"/$n.* 2>/dev/null | head -1)
  [ -z "$f" ] && { echo "missing $n"; continue; }
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" 2>/dev/null)
  [ -z "$dur" ] && dur=2
  rm -f "$W/strip/f"*.jpg
  i=0
  for pct in 0.08 0.35 0.62 0.88; do
    ss=$(python3 -c "print(round($dur*$pct,2))")
    ffmpeg -y -v error -ss "$ss" -i "$f" -frames:v 1 \
      -vf "scale=320:320:force_original_aspect_ratio=decrease,pad=320:320:(ow-iw)/2:(oh-ih)/2:color=black" \
      "$W/strip/f$i.jpg" 2>/dev/null
    i=$((i+1))
  done
  ffmpeg -y -v error -framerate 1 -pattern_type glob -i "$W/strip/f*.jpg" \
    -vf "tile=4x1,drawtext=text='$n':x=8:y=8:fontsize=48:fontcolor=yellow:box=1:boxcolor=black@0.75:boxborderw=6" \
    -frames:v 1 "$W/strip/S$n.jpg" 2>/dev/null
done
CNT=$(ls "$W"/strip/S*.jpg 2>/dev/null | wc -l | tr -d ' ')
ffmpeg -y -v error -framerate 1 -pattern_type glob -i "$W/strip/S*.jpg" \
  -vf "tile=1x$CNT" -frames:v 1 "$W/strips.jpg" 2>&1
echo "strips: $W/strips.jpg ($CNT candidates x 4 frames)"
