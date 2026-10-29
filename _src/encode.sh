#!/bin/bash
# Re-encode the films for the web (about 5-6 MB each instead of ~20 MB; checked side by side, no visible loss on the
# voxel art) and take a poster frame from each. Source: the animation project's out/. Skips files already done.
set -euo pipefail
ANIM=/home/none/git/animation/out
cd "$(dirname "$0")/.."
for src in "$ANIM"/[0-9][0-9][0-9]-*.mp4; do
  name=$(basename "$src" .mp4)
  [ -s "videos/$name.mp4" ] || ffmpeg -v error -y -i "$src" -c:v libopenh264 -b:v 600k -maxrate 900k -g 60 -pix_fmt yuv420p \
      -c:a aac -b:a 96k -ac 1 -movflags +faststart "videos/$name.mp4"
  [ -s "posters/$name.jpg" ] || ffmpeg -v error -y -ss 1.0 -i "$src" -frames:v 1 -q:v 4 "posters/$name.jpg"
  echo "$name"
done
