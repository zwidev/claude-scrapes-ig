# Sylvie videos — production instructions

Standing instructions for every new Sylvie video. These apply to standalone
Sylvie ads such as the ZenCore marketplace spot, *not* the weird-ads skill
format, unless the user asks for that.

## Subject: ZenCore
Every Sylvie video promotes **ZenCore**:
- **The marketplace:** https://zencore.solutions/marketplace
- **What it offers:** personal AI agents, each deployed to a private server the
  customer owns.
- **The agents:** the OS1 voice assistant, research and analysis agents, coding
  agents, and the other agents listed there.
- **The angles:** they remember you, they work while you sleep, and you own them
  rather than rent them.
- **Tagline:** "Your AI. Always On. Always Yours."

Re-read the live site before each batch of scripts. Script only the agents and
features it actually lists (check "Available" vs. "In review"). Keep the ZenCore
AI Beta disclaimer on the end card.

## Rule #1 — Win the first 5 seconds
- Never open with "welcome back to the channel" or any warm-up.
- Open with **conflict, a shocking stat, an unexpected outcome, or the biggest
  question in the video**.
- Earn the next 10 seconds immediately. Second 0 is already the hook line, both
  on screen (big caption) and spoken.
- *Example that worked:* "I fired my assistant… He forgot me. Every morning."

## Rule #2 — Batch relentlessly
Don't make one video from start to finish at a time. **Each batch is 3 complete
videos**, produced together stage by stage:

1. **Scripts.** Write all 3: hook, beats, VO lines, plus title and thumbnail
   options for each.
2. **Voice and visuals.** All voice lines for the 3 in one audio batch, then all
   frames in one image batch, then all clips and lip-syncs in one video batch.
3. **Edit and deliver.** Compose all 3 (denoise, captions, end card), upload,
   and hand over each video with its YouTube title, description and tags.

Batching kills the wasted time between tasks. Reuse saved assets (anchor frames,
the apartment set, voices, end card) across the batch.

## Rule #3 — Obsess over CTR
A perfect script is worthless if nobody clicks. The title and thumbnail get the
viewer through the door. For every video, test:
- **Titles:** at least 3 options per video, with the hook in the first 40 characters.
- **Thumbnail concepts:** at least 2, built around Sylvie's deadpan stare plus
  one bold phrase.
- **Hooks:** two alternate opening lines or first shots where the budget allows.
- **Visual angles:** close-up vs. wide; Sylvie vs. the product.
- **Curiosity gaps:** set up a question the video answers only at the end.

A small CTR bump can change a video's whole trajectory. Log what was posted and
how it performed so the next batch builds on the winners.

## Craft rules learned on previous Sylvie videos
- Sylvie is deadpan. **She never smiles**; at most she raises one eyebrow.
- **Sylvie's voice (approved 2026-10-08). Use it for every line she speaks.**
  - **Model and settings:** Higgsfield `seed_audio`, `speech_rate: -10` (her
    slow, deadpan pace), `sample_rate: 48000`.
  - **Reference:** `medias: [{role: "audio_references", value:
    "2a5bc262-3c91-4348-a2c1-90f0c5d5699f"}]`.
  - **Where the reference comes from:** Kling clip `c080cc21`, "Take 3". It
    was recorded in her silent apartment with a studio-microphone prompt:
    "Don't let that be you, darling. Most people simply scroll past beautiful
    things. I do not."
  - **No processing:** don't apply noise removal, EQ or gates. Her lines come
    out with silences between −76 and −91 dB. Only loudness-normalise in the
    final mix.
  - **Retired reference:** `4025ba42`. It was cut from the original 4 Oct Kling
    clip `feeed90c`, which had Paris street ambience baked in. Every line
    cloned from it carried that noise.
  - **Rejected alternatives:** ElevenLabs stock voices, and the cleaned-up
    composite reference `60bfcf43`.
- **OS1's voice and look (approved 2026-10-08).** Whenever OS1 speaks or appears:
  - **Voice:** the real OS1 voice. That's ElevenLabs voice `JSWO6cw2AyFE324d5kEr`
    ("Carolyn Scarlett Jo"), from the HERLIVE agent `agent_3101ksb1zwbzfd9a5x3a9qf5ccb6`.
  - **Voice settings:** generate lines through the ElevenLabs API with model
    `eleven_v3_conversational`, stability 0.15, similarity 0.8, speed 1.0, and
    output `mp3_44100_192`.
  - **API access:** Higgsfield's built-in voices can't use this voice, so call
    ElevenLabs directly. api.elevenlabs.io is reachable from the Higgsfield
    sandbox, not from the Claude container. The API key is the owner's. Never
    commit it or save it to a file.
  - **Screen:** the real OS1 graphic from
    `https://zencore.solutions/images/os1-voice-hero.webp`. It's an animated WebP
    (56 frames, 4.44 s loop): a white ribbon that morphs between an infinity
    loop and a circle, on coral `#D1684E`.
  - **Never** use an invented orb or glow. For phone close-ups, build the screen
    from the WebP frames (keep each frame's own duration, crop to the ribbon,
    pad to 9:16 with the coral). For wider shots, edit the frame with the
    graphic as a second image reference.
- **Clean mix.** Don't lay generated room tone or ambience under dialogue.
  Whisper-check every generated clip's audio for stray voices before using it.
- **Gaze follows the story.** When something on a screen is talking or being
  read (chatbot, phone, laptop), she looks at the screen, not the camera. Prompt
  "keeps her eyes fixed on the screen the ENTIRE time — never looks at the
  camera", and check a 2-fps contact sheet.
- **Spatial logic.** Backgrounds stay consistent with where she is sitting or
  standing; point-of-view shots show what she would actually see.
- **Accuracy.** Read the product's live site before scripting. Only claim
  features it actually lists, and keep its disclaimer on the end card.
- **Length.** Aim for 50–60 s. Shorts hold viewers best there. Don't compress
  pauses in the voice track; cut a shot instead.
- **YouTube copy for each video:** a curiosity-gap title, a description with a
  comment-prompt question, 3–5 hashtags including #Shorts, and comma-separated
  tags under 500 characters.

## Batch log
Record each batch here: what was posted, then its CTR and retention once known.

### Batch 1 (2026-10-08): ZenCore, 3 videos
| # | Title used | Product focus | Length | Video | CTR / views |
|---|---|---|---|---|---|
| 1 | My Phone Remembers More Than My Ex Did 💅 | Agent 03 OS1 Voice Agent | 58.6 s | [mp4](https://d2ol7oe51mr4n9.cloudfront.net/user_2zKMA0BhEQMQrmR8OpIagvrvlFP/7b87b903-9cf5-4836-8f3b-e62b272f8adf.mp4) | _tbd_ |
| 2 | I Had 47 AI Tabs Open. None Knew My Name. | Agent 01 Basic Package | 51.4 s | [mp4](https://d2ol7oe51mr4n9.cloudfront.net/user_2zKMA0BhEQMQrmR8OpIagvrvlFP/184541d4-8d0d-474a-bfa2-9fc2d435937e.mp4) | _tbd_ |
| 3 | My AI Assistants Talk About Me Behind My Back | Linked standalone agents | 52.1 s | [mp4](https://d2ol7oe51mr4n9.cloudfront.net/user_2zKMA0BhEQMQrmR8OpIagvrvlFP/1aca56f0-7bbf-442a-9c27-b584bf6dd5f0.mp4) | _tbd_ |

**Batch 1 production notes:**
- Voice: batch 1 used the retired noisy reference `4025ba42`. Use the approved Take 3 voice (see Craft rules) from batch 2 onward.
- Lip-syncs: MiniMax H3, duration about the audio length + 1 s. A line under 4 s gets silence padded onto the end.
- Inserts: Kling 3.0 pro with sound off. Voices are laid on in the edit.
- Marketplace insert: a live Playwright scroll at 540×960, scaled ×2, to the card the video sells.

### OS1 ad "One Conversation" (2026-10-08)
| Version | Length | Video |
|---|---|---|
| Sylvie (Take 3 voice) + OS1 (HERLIVE voice, real OS1 screen) | 75.3 s | [mp4](https://d2ol7oe51mr4n9.cloudfront.net/user_2zKMA0BhEQMQrmR8OpIagvrvlFP/b7b7c80b-c0d2-47f0-9477-d96f927262e3.mp4) |
