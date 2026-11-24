#!/bin/bash
# Assemble the bring-the-humans-03 TikTok ad (fresh in this session).
# Step 1: 24 s clip — hook card (3 s) + BOUNTY RUSH gameplay (9 s, trimmed
# from 3.0-12.0 s of the capture) with lower-third bars + what-is cards
# (2.5 s + 2.5 s) + CTA cards (2.2 s + 4.8 s), brand badge overlaid from
# frame 0 until the end card starts (t=21.5).
# Step 2: llms.txt end-card recipe — transparent 9:16 card over the last
# 2.5 s, referral code typed in once the field rests.
set -euo pipefail
cd "$(dirname "$0")"

echo "== step 1: clip =="
ffmpeg -y -v error \
  -loop 1 -t 3 -i card_hook.png \
  -ss 3 -t 9 -i gameplay.webm \
  -loop 1 -t 2.5 -i card_what1.png \
  -loop 1 -t 2.5 -i card_what2.png \
  -loop 1 -t 2.2 -i card_cta1.png \
  -loop 1 -t 4.8 -i card_cta2.png \
  -i bar1.png -i bar2.png -i bar3.png \
  -i press/makefun-badge-9x16.png \
  -filter_complex "\
[0:v]fps=25,format=yuv420p,setsar=1[hook]; \
[1:v]fps=25,format=yuv420p,setsar=1[gp0]; \
[gp0][6:v]overlay=0:1300:enable='between(t,0,3)'[gp1]; \
[gp1][7:v]overlay=0:1300:enable='between(t,3,6)'[gp2]; \
[gp2][8:v]overlay=0:1300:enable='between(t,6,9)'[gp]; \
[2:v]fps=25,format=yuv420p,setsar=1[w1]; \
[3:v]fps=25,format=yuv420p,setsar=1[w2]; \
[4:v]fps=25,format=yuv420p,setsar=1[c1]; \
[5:v]fps=25,format=yuv420p,setsar=1[c2]; \
[hook][gp][w1][w2][c1][c2]concat=n=6:v=1:a=0[cat]; \
[cat][9:v]overlay=0:0:enable='lt(t,21.5)':format=yuv420[out]" \
  -map '[out]' -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart clip.mp4

ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 clip.mp4

echo "== step 2: end card =="
CLIP=clip.mp4 CODE=y2d7dbzn FONT=press/JetBrainsMono-Bold.ttf
W=1080 H=1920 CARD=press/makefun-card-9x16-transparent.webm LEN=2.5 REST=1.433 CX=210 CY=1232 CW=5 CH=78 MID=1271 SIZE=62
HOLD=0
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$CLIP")
T=$(awk "BEGIN{print $D+$HOLD-$LEN}")
echo "clip duration=$D card starts at T=$T"
ffmpeg -y -v error -i "$CLIP" -c:v libvpx-vp9 -i "$CARD" -filter_complex "\
[0:v]scale=$W:$H:force_original_aspect_ratio=increase,crop=$W:$H,setsar=1,fps=60,tpad=stop_mode=clone:stop_duration=$HOLD,format=yuva420p,split[clip][soft]; \
[soft]gblur=sigma=28,eq=saturation=0.35,fade=t=in:st=$T:d=0.8:alpha=1[soft]; \
[clip][soft]overlay[bg]; \
[1:v]format=yuva420p,setpts=PTS-STARTPTS+$T/TB[card]; \
[bg][card]overlay=eof_action=pass, \
drawbox=x=$CX-2:y=$CY-2:w=$CW+4:h=$CH+4:color=white:t=fill:enable='gte(t,$T+$REST)', \
drawtext=fontfile=$FONT:text=$CODE:fontsize=$SIZE:fontcolor=0x191419:x=$CX:y=$MID-(ascent-descent)/2:enable='gte(t,$T+$REST)'[v]" \
  -map '[v]' -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart bring-the-humans-03-final.mp4

ffprobe -v error -show_entries format=duration,size -show_entries stream=width,height,r_frame_rate,codec_name -of default=noprint_wrappers=1 bring-the-humans-03-final.mp4
sha256sum bring-the-humans-03-final.mp4
