#!/usr/bin/env bash
# compose.sh c1.mp4 c2.mp4 c3.mp4 board.mp4 out.mp4
# c1 squint "wait… wait…" (3s), c2 shock (3s), c3 dance (7s), 1:1 Kling with sound; board.mp4 1080x960 (banner+board).
set -euo pipefail
ffmpeg -loglevel error -y -i "$1" -i "$2" -i "$3" -i "$4" -filter_complex "\
[0:v]trim=0:2.5,setpts=PTS-STARTPTS,fps=30,scale=1080:1080,crop=1080:960:0:40[v1];[0:a]atrim=0:2.5,asetpts=PTS-STARTPTS,aresample=48000[a1];\
[1:v]trim=0:2.5,setpts=PTS-STARTPTS,fps=30,scale=1080:1080,crop=1080:960:0:40[v2];[1:a]atrim=0:2.5,asetpts=PTS-STARTPTS,aresample=48000[a2];\
[2:v]trim=0:6.5,setpts=PTS-STARTPTS,fps=30,scale=1080:1080,crop=1080:960:0:40[v3];[2:a]atrim=0:6.5,asetpts=PTS-STARTPTS,aresample=48000[a3];\
[v1][a1][v2][a2][v3][a3]concat=n=3:v=1:a=1[top][au];[3:v]setpts=PTS-STARTPTS,fps=30,trim=0:11.5[bd];\
[top][bd]vstack=2,format=yuv420p[v];[au]loudnorm=I=-14:TP=-1.5,atrim=0:11.5[aout]" \
 -map "[v]" -map "[aout]" -r 30 -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$5"
