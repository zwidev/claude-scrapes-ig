# Agent 18 daily reaction clip

One 11.5 s vertical clip each morning: a deadpan NPC (top) reacts to one real card from the
Agent 18 playbook (bottom board). Follow the `skillwierdclips` skill's hard rules; this folder
adds the daily data + board pipeline.

## Daily steps

1. **Data**: `python3 -I rsi.py card.json`. Uses yesterday's completed PulseX daily candle for each
   playbook card and picks the feature card (a card that hit its rule, else the one nearest a threshold).
   If the same card and status was featured yesterday (see `log.md`) and another card is closer to a
   threshold, feature that one instead so the series doesn't repeat.
2. **Character**: next in the rotation after the last daily `log.md` entry (ignore rows marked `(extra)`):
   Cyril → Barnaby → Percival → Rupert → Cyril … (element ids in the skill's `references/characters.md`).
3. **Frames** (Nano Banana 2, 1:1, 2k, character via `<<<element_id>>>` in the prompt only, no `element` media role):
   squint at monitor ("wait… wait…", hands out of frame), shock (both palms on cheeks), dance (fists up).
   **Squint frame must be SIDE-ON (user rule, 14 Oct):** camera at 90° to the desk, character in profile
   facing the monitor, and the monitor's screen faces the character (seen obliquely from the side), never the
   camera. Reject any frame where the screen faces the viewer while the character looks at it from behind.
   Monitor frames pass the Agent 18 board still `f34574ce-b12f-468d-8b87-6eb837816be2` as `image_references`.
   Inspect all three for limbs and screen content.
4. **Animate** (Kling 3.0 `kling3_0`, `mode: pro`, `sound: on`, 1:1, `start_image`, 3 s / 3 s / 7 s,
   `declined_preset_id: 24bae836-2c4a-48e0-89b6-49fcc0b21612`). The dance clip shouts the card's
   `spoken` name from `card.json` twice, then points at camera. Check a 1–2 fps contact sheet of each clip.
5. **Board**: `npm install` once, then `node frames.mjs card.json bf` and
   `ffmpeg -framerate 30 -i bf/%04d.jpg -c:v libx264 -pix_fmt yuv420p -crf 16 board.mp4`.
6. **Compose**: `./compose.sh c1.mp4 c2.mp4 c3.mp4 board.mp4 out.mp4`, then whisper-check the shouted name.
7. **Deliver**: `media_upload` → `curl -X PUT -H "Content-Type: video/mp4" -H "If-None-Match: *" --upload-file out.mp4 <url>`
   → `media_confirm`. Send the cloudfront link, a beat table and a caption. Append a line to `log.md`.

Works locally (Claude Code container: `pip install imageio-ffmpeg` for ffmpeg, Chromium at
`/opt/pw-browsers/chromium`) or in the Higgsfield sandbox. Board labels follow the data: `EXIT RULE HIT`
(RSI > 65), `SETUP TRIGGERED` (RSI < 30) or `ON WATCH` — never claim a trigger that didn't happen,
never show P/L. Crypto promotions need FCA-authorised approval before posting.
