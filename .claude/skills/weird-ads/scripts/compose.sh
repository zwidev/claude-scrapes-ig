#!/usr/bin/env bash
# Compose a weird-ads split-screen reaction clip inside the Higgsfield sandbox.
# Usage: compose.sh c1.mp4 c2.mp4 c3.mp4 board.mp4 out.mp4 ["BANNER TEXT"]
#   c1/c2/c3: 1:1 Kling reaction clips IN ORDER: lean-in squint "wait… wait…" (3s), shock (3s), dance (7s); sound on
#   board.mp4: 1080x880 recorded signal board (11.5 s)
set -euo pipefail
C1=$1; C2=$2; C3=$3; BOARD=$4; OUT=$5; BANNER=${6:-"AGENT 18 · ALPHA — LINK IN BIO"}
FONT=$(fc-list | grep -iE "Montserrat.*(ExtraBold|Black)" | head -1 | cut -d: -f1)
[ -z "$FONT" ] && FONT=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
ffmpeg -loglevel error -y -i "$C1" -i "$C2" -i "$C3" -i "$BOARD" -filter_complex "\
[0:v]trim=0:2.5,setpts=PTS-STARTPTS,fps=30,scale=1080:1080,crop=1080:960:0:40[v1];[0:a]atrim=0:2.5,asetpts=PTS-STARTPTS,aresample=48000[a1];\
[1:v]trim=0:2.5,setpts=PTS-STARTPTS,fps=30,scale=1080:1080,crop=1080:960:0:40[v2];[1:a]atrim=0:2.5,asetpts=PTS-STARTPTS,aresample=48000[a2];\
[2:v]trim=0:6.5,setpts=PTS-STARTPTS,fps=30,scale=1080:1080,crop=1080:960:0:40[v3];[2:a]atrim=0:6.5,asetpts=PTS-STARTPTS,aresample=48000[a3];\
[v1][a1][v2][a2][v3][a3]concat=n=3:v=1:a=1[top][au];\
color=c=black:s=1080x1920:r=30:d=11.5[bg];[bg][top]overlay=0:0[t1];\
[3:v]setpts=PTS-STARTPTS,fps=30[bd];[t1][bd]overlay=0:1040[t2];\
[t2]drawbox=x=0:y=960:w=1080:h=80:color=black:t=fill,drawtext=fontfile=$FONT:text='$BANNER':fontcolor=white:fontsize=54:borderw=5:bordercolor=black:x=(w-text_w)/2:y=968,trim=0:11.5,format=yuv420p[v];\
[au]loudnorm=I=-14:TP=-1.5,atrim=0:11.5[aout]" \
  -map "[v]" -map "[aout]" -r 30 -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k -movflags +faststart "$OUT"
ffprobe -v error -show_entries stream=codec_type,duration -of csv=p=0 "$OUT"
