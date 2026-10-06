#!/usr/bin/env bash
# Compose a narrator-explainer weird ad: 4 reaction clips (top) + board (bottom) + off-screen VO.
# Usage: compose_vo.sh c1 c2 c3 c4 board.mp4 vo.wav out.mp4 "t1 t2 t3 t4" [TOTAL] ["BANNER"]
#   c1..c4: 1:1 Kling clips IN ORDER: squint, stare-at-screen, shock, dance
#   "t1 t2 t3 t4": seconds kept from each clip, summing to TOTAL (default 26.2), timed to VO beats
#   board.mp4: 1080x880 recording of assets/wallet_board.html with CUES matched to the VO
# Character audio is ducked to 0.22 under the VO; mix loudnormed to -14 LUFS.
set -euo pipefail
C1=$1; C2=$2; C3=$3; C4=$4; BOARD=$5; VO=$6; OUT=$7; read -r T1 T2 T3 T4 <<<"$8"
TOTAL=${9:-26.2}; BANNER=${10:-"AGENT 18 · ALPHA — LINK IN BIO"}
FONT=/usr/share/fonts/truetype/higgsfield/Montserrat-ExtraBold.ttf
[ -f "$FONT" ] || FONT=$(fc-list | grep -iE "Montserrat.*ExtraBold" | head -1 | cut -d: -f1)
seg(){ echo "[$1:v]trim=0:$2,setpts=PTS-STARTPTS,fps=30,scale=1080:1080,crop=1080:960:0:40[v$1];[$1:a]atrim=0:$2,asetpts=PTS-STARTPTS,aresample=48000[a$1];"; }
ffmpeg -loglevel error -y -i "$C1" -i "$C2" -i "$C3" -i "$C4" -i "$BOARD" -i "$VO" -filter_complex "\
$(seg 0 $T1)$(seg 1 $T2)$(seg 2 $T3)$(seg 3 $T4)\
[v0][a0][v1][a1][v2][a2][v3][a3]concat=n=4:v=1:a=1[top][ca];\
color=c=black:s=1080x1920:r=30:d=$TOTAL[bg];[bg][top]overlay=0:0[t1];\
[4:v]setpts=PTS-STARTPTS,fps=30[bd];[t1][bd]overlay=0:1040:eof_action=repeat[t2];\
[t2]drawbox=x=0:y=960:w=1080:h=80:color=black:t=fill,drawtext=fontfile=$FONT:text='$BANNER':fontcolor=white:fontsize=54:borderw=5:bordercolor=black:x=(w-text_w)/2:y=968,trim=0:$TOTAL,format=yuv420p[v];\
[ca]volume=0.22[cb];[5:a]aresample=48000,apad[vo];[vo][cb]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5,atrim=0:$TOTAL[aout]" \
  -map "[v]" -map "[aout]" -r 30 -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k -movflags +faststart "$OUT"
ffprobe -v error -show_entries stream=codec_type,duration -of csv=p=0 "$OUT"
