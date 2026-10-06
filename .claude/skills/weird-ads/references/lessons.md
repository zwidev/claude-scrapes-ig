# Tool lessons (learned the hard way)

## Errors that STOP generation — and the fix

| Symptom | Cause | Fix (do this up front, not after the failure) |
|---|---|---|
| `submission_failed: Preset "IN THE DARK" was recommended instead of submitting a job` | Kling batch auto-suggests a preset for dark/office/night prompts | **Always** pass `declined_preset_id: "24bae836-2c4a-48e0-89b6-49fcc0b21612"` on every Kling 3.0 request. Only the failed item needs resubmitting; the others already have job ids. |
| MiniMax H3 rejects the request | `start_image` mixed with `audio_references` | Pass the frame as `image_references`; prompt "Recreate the reference image exactly as the opening frame…" |
| `No such tool` / tool vanished mid-task | Higgsfield MCP disconnected and reconnected | `ToolSearch select:mcp__higsfield__sandbox_exec,...` again and continue. Job ids stay valid — never resubmit a job just because the tool dropped. |
| Background log/exit file missing, `/home/user/...` empty | Sandbox reset or worker restart killed the job | Before redoing work, `curl -sI <cloudfront url>` of the intended output: if 200, the PUT already happened — just `media_confirm`. Otherwise rerun as ONE self-contained job (download → build → verify → PUT). |
| `sandbox_exec timed out after 60s` even with `timeout_seconds: 110` | MCP transport caps foreground calls at ~60 s | Foreground commands ≤ 50 s. Never `sleep 100`. To wait on generations use `jobs_wait` (≤15 s per call, repeat); to wait on sandbox work use `background: true` + poll loops of `sleep 5` ×≤11. |
| PUT returns 400 | Presigned URL is single-use (`if-none-match`) or was already used | Reserve a fresh `media_upload` slot. After a context reset the old URL is gone anyway — reserve a new one. Confirm only after HTTP 200. |
| OOM-killed during compose / tracking | Whole 1080×1920 video loaded into RAM | Stream frames; keep ffmpeg filtergraphs instead of Python frame arrays. |
| Local container `curl` to cloudfront / upload.higgsfield.ai → 403 | Proxy blocks those hosts locally | Do every download/upload inside `sandbox_exec`. |
| `show_medias` schema error | Tool bug | Ask the user for a direct link, or (with consent) push the asset to the public session branch of `zwidev/claude-scrapes-ig`, fetch via `raw.githubusercontent.com/...@<sha>`, then delete it. |
| User asks to "download to Google Drive" | Drive `create_file` needs base64 in the call; videos are MBs and the sandbox has no Google auth | Not possible for video. Create a Drive folder + a doc of download links instead and tell the user to save the files manually. |

## Visual defects the user has rejected (prevent in the FRAME prompt)

- **Extra arm / third hand.** Kling invents limbs when a hand is near the
  keyboard/mouse and another is on the body. Fix: frame chest-up with
  "arms and hands completely out of frame", or pin both hands somewhere explicit
  ("hands folded in his lap") + "exactly two arms". Inspect frames AND 1-fps
  contact sheets of every clip before composing.
- **Random content on the monitor (a scrolling game).** Never let the model
  invent screen content. Render a still of the Agent 18 board (Playwright
  screenshot, 1600×900), upload it, pass it to Nano Banana 2 as
  `image_references` with "the monitor clearly displays the reference image".
  In Kling add "static camera, the monitor screen content stays exactly the same,
  static, no scrolling".
- **Gaze drifting off the screen** — applies only when the clip narrative has a
  computer screen (Barnaby stared past the camera from ~6 s and
  turned to camera in the shock beat). Frame: "camera beside and slightly behind
  the monitor at a 45-degree angle, BOTH his face (three-quarter) AND the monitor
  screen clearly visible, eyes locked on the screen, NOT looking at the camera".
  Kling: "keeps his eyes locked on the screen the entire time; he never looks at
  the camera". Never prompt "turns to camera" before the dance.
- **Gaze shot that looks like a still photo.** Using the same frame as Kling
  `start_image` AND `end_image` + "almost motionless" locks the gaze but the user
  saw a frozen picture. Fix: generate a second frame (same angle, character has
  leaned closer, mouth open "whoa", still in profile on the screen) and use it as
  `end_image`. Kling then animates real motion between two on-screen poses
  without turning to camera. Check with a 2-fps strip that the pose changes.
- **Character scrolling / clicking.** User wants the character to LOOK, not
  operate the computer. Prompt "does not touch the mouse or keyboard". Clicking
  happens only on the board below (animated cursor).
- **Extra people in a sports shot** (v2 tennis serve had three men, two on one
  side). Prompt "Only these TWO players are on the court for the entire clip — one
  on each side of the net, no other people appear on the court", and check a
  1-fps strip for anyone appearing mid-clip.
- **Ghost reflection creeping onto a phone screen** in Kling POV clips after ~1 s.
  Strip the clip at 5 fps cropped to the screen; use only the clean part
  (boomerang it: forward, reverse, forward) rather than letting it play out.
- **Bad sports physics** (player tossed the ball, CAUGHT it, then hit it). For
  rallies, start the frame mid-rally with the ball incoming and prompt "NO serve,
  no ball toss, he never catches the ball"; keep only the clean hit window.
- **Jump cut from walking to already seated.** Make the entry ONE Kling clip:
  start frame = character walking toward the EMPTY chair (same framing as the
  seated anchor), `end_image` = the seated anchor. She is seen sitting down.
- **Walk-to-sit overshoot.** With the character starting beside/behind the chair
  line, Kling walks her PAST the chair and back (with or without `end_image`).
  Fix: start frame with her already stepping in FRONT of the chair (between chair
  and camera), body half-turned to camera, one step from the seat; `end_image` =
  seated anchor. 5 s.
- **POV phone shots must show what she is looking at.** If the story says she's
  courtside, the background behind the phone shows the court and the players
  (correct count, one each side of the net). Restate wardrobe details visible in
  POV (sleeveless = bare forearms) or the model invents sleeves.
- **Kling ambience can contain stray voices** ("oh my god"). Whisper every clip
  with sound; replace with a clean bed (e.g. the rally clip's own audio, skipping
  segments already used elsewhere so a grunt doesn't repeat).
- **Noisy entry ambience.** Prompt "quiet ambience only… no crowd chatter" and
  duck the clip (volume 0.3) under the following dialogue.
- **Real-world set dressing.** Tennis courts have a tall dark-green chain-link
  fence; put it in every court frame (and behind courtside seats).
- **Unwanted smiling.** Deadpan characters: frame "lips closed, no smile"; lip-sync
  prompt "she NEVER smiles; she only raises one eyebrow on '<word>'".
- **Phone status bar baked into the frame** (Nano Banana sometimes adds
  "80% 🔋"). Add "full frame, no phone interface or status bar"; crop more if it
  survives.

## Higgsfield MCP

- `generate_*_batch` → `jobs_wait` (≤15 s per call, keep polling). While a
  Kling job runs `jobs_wait` may report `type: image` — harmless.
- `nano_banana_2` executes as `nano_banana_flash`; fine. Media role for
  references: `image_references` (Kling: `start_image`).
- Kling 3.0 honours a character only with `start_image` in `medias`.
- Kling durations 3–15 s; generate the length the beat needs (no stretching).
- MiniMax H3 durations are integers ≥ audio length; trim afterwards.

## Sandbox

- Every producing job is self-contained: write HTML/scripts with heredocs,
  download inputs, build, verify (ffprobe + whisper + contact sheet), PUT, echo
  `PUT=<code>` and `DONE_OK`.
- Command limit 16 000 chars incl. the signed URL (~2.5 k) — keep inline HTML lean.
- `magick` isn't installed; use ffmpeg for contact sheets/crops. OpenCV:
  `pip install opencv-python-headless`.
- Playwright: `NODE_PATH=$(npm root -g) node rec.js`; recordVideo includes the
  page-load lead-in — trim `-ss (duration − timeline − 0.3)`.
- Fonts: `/usr/share/fonts/truetype/higgsfield/Montserrat-ExtraBold.ttf`.
- 5:2 covers (X Articles): generate 21:9, then `scale=1500:-2,crop=1500:600`.

## Voice

- seed_audio honours pauses ("…") literally — takes run long. Do NOT trim
  silences; split at silences (`silencedetect=n=-40dB:d=0.4`) into ≤15 s
  segments for lip-sync, or time the visuals to the take for voiceover.
- Write brand names phonetically ("Pulse Zen", "Agent Eighteen"); whisper-check.
  Whisper hears a shouted "HEX!" as "Hacks" — re-check by ear or re-take.

## Accuracy (claims about the user's product)

- Read the live app before scripting a feature. Agent 18 (app.zencore.solutions,
  dashboard JS bundle) has: Trader leaderboard (wallets ranked by 90-day realized
  profit), Follow wallet → buy/sell **alerts**, Smart-money feed ("your choice to
  copy"), Discovered smart wallets, Money flow. It does **not** auto-copy trades —
  never say it does.
- Never restate a chart move as a bigger/faster claim (e.g. "+14.58% across ~6
  4h candles" ≠ "15% in four hours").
