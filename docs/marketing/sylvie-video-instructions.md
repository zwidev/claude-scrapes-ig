# Sylvie videos — production instructions

Standing instructions for every new Sylvie video. These apply to standalone
Sylvie ads such as the ZenCore marketplace spot, *not* the weird-ads skill
format, unless the user asks for that.

## Rule #1 — Win the first 5 seconds
- Never open with "welcome back to the channel" or any warm-up.
- Open with **conflict, a shocking stat, an unexpected outcome, or the biggest
  question in the video**.
- Earn the next 10 seconds immediately. Second 0 is already the hook line, both
  on screen (big caption) and spoken.
- *Example that worked:* "I fired my assistant… He forgot me. Every morning."

## Rule #2 — Batch relentlessly
Don't make one video from start to finish each day. Work in batches:

| Day | Work |
|---|---|
| Day 1 | 10 scripts from Claude: hook, beats, VO lines, title and thumbnail options for each |
| Day 2 | Voiceovers and visuals for all 10: Sylvie's cloned voice, frames, clips |
| Days 3–4 | Edit and schedule: captions, denoise, end cards, upload, posting calendar |

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
- **Clean audio.** Run every voice line through
  `highpass=f=80,afftdn=nr=30:nf=-38:tn=1,agate=threshold=0.02:ratio=4:attack=5:release=120`.
  Her cloned voice carries a hiss at about −34 dB. Don't lay generated room
  tone under dialogue. Whisper-check every generated clip's audio for stray
  voices before using it.
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
