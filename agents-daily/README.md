# ZenCore agent spotlight (daily)

One 11.5 s vertical clip each morning promoting **one individual agent** from the
zencore.solutions marketplace. It uses the same format as the Agent 18 clips: a deadpan NPC on top reacts and an
animated panel below shows the agent. Follow the `skillwierdclips` skill's hard rules. This replaced
the Agent 18 RSI clip on 4 Nov 2026 at the user's request ("start promoting individual agents on
zencore.solutions, leave PZEN out").

**PZEN is left out:**
- Agents 02 (Alpha Server) and 18 (Web Alpha) need PZEN at checkout, so they are not in `agents.json`.
- No clip, panel or caption mentions PZEN, PLS or HEX.
- Never use the old Agent 18 board still `f34574ce…` as a monitor image, because it shows "BUY PZEN".

Rotation (`agents.json`): 01 ZenCore Basic → 03 OS1 Voice → 14 Switchboard → 16 Vault Voice →
17 Vault Papers → 19 OS1 Web → 20 Research Desk → 21 Decision Desk → 22 Automaton Trader → 01 …
Agents marked "In review" on the site are left out because nobody can buy them yet. When one becomes Available, add it here with
copy taken from its page.

## Daily steps

1. **Pick + verify**: `python3 -I spotlight.py`. This picks the next agent after the last `log.md` row and the next
   character (Cyril → Barnaby → Percival → Rupert). It then re-reads that agent's live page and checks the title,
   "Available" status, price and that there's no PZEN requirement.
   - If a check fails, it skips to the next agent and records why in `skipped`. Mention any skip in the report.
   - If `log.md` already has a row for today, it exits with code 4. Say so and stop; `--force` makes an extra clip.
   - If the site can't be read, it exits non-zero. Report the failure and don't make anything.
2. **Screen**: `node pageshot.mjs agent.json screen.png`. This takes a screenshot of the live agent page.
   Upload it with `media_upload` → curl PUT → `media_confirm`.
3. **Squint frame** (Nano Banana 2, 1:1, 2k):
   - Reference the character only as `<<<element_id>>>` in the prompt, and pass the screenshot as `image_references`.
   - **The shot must be SIDE-ON (user rule, 14 Oct).** The camera is at 90° to the desk. The character is in profile,
     facing right, leaning in and squinting. The monitor's screen faces the character and is seen obliquely, never
     facing the camera. Reject any frame that breaks this.
   - Element ids:
     - Cyril `a01e551c-e629-4609-93d3-66a016c97496`
     - Barnaby `a9cb2773-5481-41e8-a2eb-fd6a9a4ee0fa`
     - Percival `86f5242a-5059-4a6c-b99c-478062576a47`
     - Rupert `95ea4ab9-b160-4411-b8f3-4467b9e83d7d`
   - The **shock** and **dance** frames can be reused, but check the shock frame the first time it's used. The old
     ones were made for Agent 18, and Cyril's showed the Agent 18 (PZEN) board behind him. If a screen is readable,
     regenerate the frame facing the camera with the monitors off, then update this table:

     | Character | Shock | Dance |
     |---|---|---|
     | Cyril | `60ff3d83-6467-4173-a02f-4517d069b3d5` (clean, 4 Nov) | `4e0b7d7b-4f58-453a-b841-97bdd1132ff2` |
     | Barnaby | `57674de6-2054-4927-8f01-4fda43ae419c` (clean, 5 Nov) | `15ad1423-77a5-413b-aaff-e96846fac594` |
     | Percival | `644ec71a-a51f-42ca-932a-6e3cd2facacb` (clean, 11 Nov) | `92e18039-68dc-4e34-8c19-ac6dc53537cc` |
     | Rupert | `d10b4b97-66c8-4dd4-bfdf-1cdc4cf5f557` (screen edge-on, OK) | `8e46b818-0819-42c9-b2e5-5a12c3596800` |

4. **Animate** with Kling 3.0:
   - Settings: `kling3_0`, `mode: pro`, `sound: on`, 1:1, `start_image`, `declined_preset_id: 24bae836-2c4a-48e0-89b6-49fcc0b21612`.
   - c1, squint (3 s): he whispers "wait... wait...". The screen stays static and his hands stay out of frame.
   - c2, shock (3 s): palms on cheeks and a loud comic gasp "oh!".
   - c3, dance (7 s): an awkward victory dance while he shouts the agent's `spoken` name exactly twice. At second four
     he stops dead and points at the camera, "deadpan and silent" (without "silent" Kling sometimes adds a third shout).
   - Check a contact sheet of each clip for limbs and screen orientation.
5. **Panel**: `node frames.mjs agent.json bf` then
   `ffmpeg -framerate 30 -i bf/%04d.jpg -c:v libx264 -pix_fmt yuv420p -crf 16 panel.mp4`.
   The panel shows:
   - 0–2.5 s: the problem (`hook`), typed out.
   - 2.5–5 s: the agent card and who it's for.
   - 5 s onwards: three bullets, the live price and the zencore.solutions call to action with the 14-day money-back line.
   - On the trading agents (20, 21, 22), a disclaimer strip.
6. **Compose**: `./compose.sh c1.mp4 c2.mp4 c3.mp4 panel.mp4 out.mp4`. Whisper-check that the shouted name is in the audio.
7. **Deliver**:
   - Upload `out.mp4` (`media_upload` → PUT with `If-None-Match: *` → `media_confirm`).
   - Remux to `.mov` (`ffmpeg -i out.mp4 -c copy -movflags +faststart -f mov spotlight-<date>-<character>-agent<num>.mov`)
     and send it with `SendUserFile`.
   - Send the link, a beat table and a caption (headline, description, comma-separated tags).
   - Append a row to `log.md`, commit and push.

## Copy rules

- Only use claims that appear on the agent's own marketplace page. Show the live price.
- No earnings, profit or time-saving promises. The site itself says its human-vs-agent cost figure "is not a saving".
- For trading agents, keep "Not financial advice", "Capital at risk" and "paper by default" where the page says so.
- Don't mention the "founding customers 20% back" offer unless the user asks.
