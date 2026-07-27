#!/bin/bash
# Contact sheet: one representative frame per candidate, tiled + numbered.
ITEM="$1"; COLS="${2:-4}"
W="/tmp/fm/$ITEM"
rm -rf "$W/rep"; mkdir -p "$W/rep"
for f in "$W"/[0-9][0-9].*; do
  [ -e "$f" ] || continue
  b=$(basename "$f"); n="${b%%.*}"
  case "$b" in
    *.jpg|*.jpeg|*.png|*.webp)
      # a still has no timeline: -ss would seek past EOF and yield no frame at all
      ffmpeg -y -v error -i "$f" -frames:v 1 \
        -vf "scale=300:300:force_original_aspect_ratio=decrease,pad=300:300:(ow-iw)/2:(oh-ih)/2:color=black,drawtext=text='$n':x=6:y=6:fontsize=44:fontcolor=yellow:box=1:boxcolor=black@0.7:boxborderw=5" \
        "$W/rep/$n.jpg" 2>/dev/null
      continue ;;
  esac
  # sample at ~40% through the loop, not frame 0 (title cards / black leader)
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" 2>/dev/null | cut -d. -f1)
  [ -z "$dur" ] && dur=0
  ss=$(python3 -c "print(max(0,$dur*0.4))" 2>/dev/null || echo 0)
  ffmpeg -y -v error -ss "$ss" -i "$f" -frames:v 1 \
    -vf "scale=300:300:force_original_aspect_ratio=decrease,pad=300:300:(ow-iw)/2:(oh-ih)/2:color=black,drawtext=text='$n':x=6:y=6:fontsize=44:fontcolor=yellow:box=1:boxcolor=black@0.7:boxborderw=5" \
    "$W/rep/$n.jpg" 2>/dev/null
done
CNT=$(ls "$W"/rep/*.jpg 2>/dev/null | wc -l | tr -d ' ')
ROWS=$(( (CNT + COLS - 1) / COLS ))
ffmpeg -y -v error -framerate 1 -pattern_type glob -i "$W/rep/*.jpg" \
  -vf "tile=${COLS}x${ROWS}" -frames:v 1 "$W/sheet.jpg" 2>&1
echo "sheet: $W/sheet.jpg  ($CNT tiles, ${COLS}x${ROWS})"
