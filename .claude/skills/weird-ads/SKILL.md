---
name: weird-ads
description: >-
  Produce "weird ads" — short vertical NPC reaction clips where a strange-looking,
  deadpan AI character (Barnaby, Percival, Rupert, Cyril, Sylvie, Clementine, Berthe…)
  reacts comedically to a ZenCore / Agent 18 "Alpha Market Intelligence" signal board,
  in the split-screen format (character on top, banner, live board below). Also covers
  building new NPC characters, lip-synced talking versions, and screen inserts.
  Use whenever the user asks for an NPC reaction clip, a weird ad, a "GTA NPC" style
  character video, a reaction for Agent 18 / Pulse Zen / PLS / HEX, or wants to make
  the same clip with another character — even if they don't say "weird ads".
---

# Weird ads — NPC reaction clips (Higgsfield)

The hook is a character so odd that viewers argue "is this even real?" The screen is
the context; the character is the joke. Every clip is a **comedic reaction**, never a
character reading or explaining a strategy.

Read `references/characters.md` for the saved cast (element IDs, looks, voices) and
`references/lessons.md` for the tool gotchas before generating anything.

## Hard rules (user corrections — never break)

1. **Reaction, not explanation.** The character gasps, squints, panics, celebrates.
   At most a couple of shouted words. Do not have them read entry/exit/stop rules.
2. **Pronunciation.** PZEN is said **"Pulse Zen"**. Always write spoken lines
   phonetically in TTS / video prompts ("Pulse Zen", never "PZEN" or "P-Z-N").
   PLS is the PulseChain coin — avoid making characters say it; prefer "Pulse Zen"
   or "HEX". Verify with a transcription after rendering.
3. **Never show or mention the paper-replay result (+0.0%)** or any "flat/no profit"
   punchline. End on the high (celebration / pointing at camera).
4. **Never invent P/L or profit numbers** for the user's product (no fake balances
   ticking up). The bottom screen is the Agent 18 signal board: real strategy names
   from the user's playbook, RSI ticking, status chips, a "SETUP TRIGGERED" alert.
   Footer always: `Educational demo · Not financial advice`.
5. **Never compress pauses** in a voice take. If a take is longer than the lip-sync
   limit (15 s), split it at natural silences and generate **more frames** — one
   lip-sync clip per segment, each from its own character frame.
6. **Lip-sync must be real.** If a character talks on camera, drive the mouth with
   the audio (MiniMax H3). Don't lay voiceover over a closed mouth.
7. Don't generate clips "to fit" by stretching — generate enough clips for the beats.
8. Show the user deliverables as direct download links (cloudfront `.mp4`/`.png`).

## Default format — split-screen reaction (mirrors the user's reference)

Canvas 1080×1920, 30 fps, ~11.5 s.

| Region | Box | Content |
|---|---|---|
| Top | 0,0 → 1080×960 | character clips (1:1 Kling, scale 1080, crop 1080×960 at y=40) |
| Banner | y 960–1040 | black bar, Montserrat ExtraBold 54 px white, black 5 px border: `AGENT 18 · ALPHA — LINK IN BIO` |
| Bottom | y 1040 → 1080×880 | recorded signal board (`assets/board.html`) |

Beat sheet (adapt per character, keep the arc):

| Time | Character (top) | Board (bottom) |
|---|---|---|
| 0–2.5 s | exaggerated shock — hands on face, gasp | all RSIs tick down, rows red |
| 2.5–5 s | nose to the monitor, squinting, "wait… wait…" | hero row RSI → ~30, `ENTRY ZONE` chip flashes amber |
| 5–11.5 s | dorky victory dance, shouts the coin name, ends pointing at camera | big green `✓ SETUP TRIGGERED` alert pops and glows |

## Pipeline

1. **Frames (Nano Banana 2, 1:1, 2k).** One frame per beat: shock, lean-in, dance.
   Reference the character with `<<<element_id>>>` in the prompt and restate the look
   (hair, glasses, suit) every time. Office setting, cool fluorescent light, candid
   phone-video realism, "No text". If one fails, fold its beat into a neighbour
   (e.g. end the dance clip on the point-at-camera).
2. **Inspect frames** in the sandbox (`image_paths`) before animating.
3. **Animate (Kling 3.0, `mode: pro`, `sound: on`, 1:1, `start_image`).** Durations
   3 s / 3 s / 7 s. Put the shouted words in quotes, phonetic. Add "No music" and
   "face, hair and outfit stay exactly the same". If the batch returns a preset
   recommendation ("IN THE DARK"), resubmit that item with `declined_preset_id`.
4. **Board.** Edit `assets/board.html` CONFIG (brand line, rows, hero row, alert
   text) — use the user's real strategy names. Record with Playwright `recordVideo`
   (1080×880), trim the page-load lead-in (`webm_duration − 11.6`), encode 30 fps.
5. **Compose** with `scripts/compose.sh` (trims 2.5/2.5/6.5 s, concat with audio,
   overlay board, draw banner, loudnorm −14 LUFS).
6. **Verify**: ffprobe durations; whisper the audio (check the shouted word is
   pronounced right); contact-sheet frames at 1.2/3.8/6/8/10.8 s.
7. **Deliver**: upload via `media_upload` → PUT in the same sandbox command →
   `media_confirm`; give the user the cloudfront link + a beat table.

Costs (Oct 2026): Nano Banana 2 2k = 2 cr/frame; Kling 3.0 pro sound on ≈ 2 cr/s
(10 cr per 5 s); MiniMax H3 lip-sync ≈ 12 cr per 6 s.

## Variants

- **Talking NPC (lip-synced).** Voice with `seed_audio` preset (Barnaby: `Archie`),
  or clone an accent: render a Kling clip where the character says one line in the
  accent, extract its audio, use it as `audio_references` for `seed_audio`. Lip-sync
  with MiniMax H3 using `image_references` (+ `audio_references`) — **not**
  `start_image` (rejected when mixed with references). Split long takes per rule 5.
- **Webcam box over a screen recording.** Character 440×440 top-right at (594,104),
  `● LIVE` tag, captions inside the box bottom (ASS, Montserrat 38, MarginL 615,
  MarginR 55, MarginV 1385) — keeps the mouth visible.
- **Phone-screen replacement** (put a user screenshot on a phone a character holds):
  track gold-pattern features with OpenCV LK + RANSAC homography from a hand-picked
  quad, warp the image, mask out the glove/fingers (yellow components touching the
  outside of the quad), stream frames (don't load the whole video into RAM).
- **New character.** JSON prompt (name / subject / wardrobe / pose / scene / camera /
  direction), "One man/woman only, no text", generate, inspect, then
  `manage_reference_elements create` (category character). For transparent cut-outs
  generate on a plain light-grey studio backdrop, then `remove_background`.

## Compliance guard-rails

- Own product only (ZenCore / Agent 18). Decline forex/CFD CPA affiliate funnels and
  fake-profit reaction formats; explain why (FCA s21 / crypto promotion rules,
  platform bans, broker CPA requires deposits).
- No "buy now", no guaranteed returns, no invented results; keep the footer.
- Characters are original fictional people — build from descriptions, never copy a
  real person's face from a reference image.
