# Tool lessons (learned the hard way)

## Higgsfield MCP
- Tools drop and reconnect often; reload with ToolSearch `select:...` and continue.
- `generate_*_batch` → `jobs_wait` (≤15 s per call, keep polling) → inspect.
- Kling 3.0 honours a character only with `start_image` in `medias`.
- MiniMax H3: `start_image` cannot be mixed with `audio_references` → pass the frame
  as `image_references`, prompt "Recreate the reference image exactly as the opening
  frame…". Durations are integers ≥ audio length; trim to the segment afterwards.
- Video batch may refuse an item with a preset recommendation ("IN THE DARK"):
  resubmit with `declined_preset_id`.
- `show_medias` currently errors (schema mismatch) — the user's library uploads can't
  be listed. Ask for a direct share link, or (with consent) push the asset to the
  public session branch of `zwidev/claude-scrapes-ig` and fetch
  `raw.githubusercontent.com/...@<sha>`; delete it afterwards.
- The local container cannot reach `upload.higgsfield.ai` or cloudfront (proxy 403):
  do all downloads/uploads inside `sandbox_exec`.
- `media_upload` presigned URLs are single-use (`if-none-match`): a second PUT returns
  400 — reserve a fresh slot. Confirm only after HTTP 200.

## Sandbox
- The sandbox resets between turns/worker restarts. Make every producing job
  self-contained (download inputs → build → verify → PUT) and upload intermediates.
- Foreground calls time out at ~60 s through MCP: use `background: true` and poll
  with `sleep` loops of ≤ 50 s.
- Don't hold a whole 1080×1920 video in RAM (OOM-killed) — stream frames.
- `magick` isn't installed; use ffmpeg for contact sheets. OpenCV: `pip install
  opencv-python-headless`.
- Playwright: `NODE_PATH=$(npm root -g) node rec.js`; recordVideo includes page-load
  lead-in — trim `duration − timeline_length`.
- Fonts: `/usr/share/fonts/truetype/higgsfield/Montserrat-ExtraBold.ttf`.

## Voice
- seed_audio honours pauses ("…") literally — takes run long. Do NOT trim silences;
  split at silences (`silencedetect=n=-40dB:d=0.4`) into ≤15 s segments instead.
- Write brand names phonetically ("Pulse Zen"); whisper-check after.
