# Saved cast (Higgsfield Elements)

Use the element id inside prompts as `<<<id>>>`. Refer to characters by name with the user.

| Name | Element id | Look | Notes |
|---|---|---|---|
| Barnaby Biro | `a9cb2773-5481-41e8-a2eb-fd6a9a4ee0fa` | 38, wavy shoulder-length strawberry-blond hair (middle part), big rectangular tortoiseshell glasses, thin moustache, charcoal suit, white shirt, navy tie | Voice: seed_audio preset `Archie` (`bd072316-f77c-588b-b6e5-e46b9b03d008`). Transparent PNG source job `836fb219-68ca-4827-93b8-2659b989f511` |
| Percival Pallor | `86f5242a-5059-4a6c-b99c-478062576a47` | 35, very pale, enormous crimped platinum-white hair with blunt fringe, thin round silver wire glasses, gaunt deadpan face, charcoal suit, navy tie | Transparent job `bc1d1343-9579-41d2-928d-e8af1e528a38` |
| Rupert Ramekin | `95ea4ab9-b160-4411-b8f3-4467b9e83d7d` | 29, copper-ginger helmet bowl cut, freckles, round wire glasses, bushy ginger brows, charcoal suit, navy tie + silver tie bar | Transparent job `07f4865f-6013-4053-991a-03dcdef3aff3` |
| Cyril Cranium | `a01e551c-e629-4609-93d3-66a016c97496` | 50, bald, tall elongated dome head, long gaunt hollow-cheeked face, cold deadpan stare, slim charcoal suit, dark-grey tie | Transparent job `f0f3d232-a722-4e6e-970d-6c9694ca75ac` |
| Sylvie Souffle | `193a6511-470f-49e6-9a6e-fd8b36e59939` | 34, East Asian woman, giant square sculpted black bob, tiny fringe, long tendrils, ivory suit with huge round collar, polka-dot blouse, yellow gloves, red disc earrings | Soft Japanese-accented English: cloned from Kling clip audio, upload `4025ba42-1dd4-4824-b7d5-523e0ed6f2c7` (use as `audio_references`) |
| Clementine Chouquette | `3d854789-dac9-4e73-83bf-a23494fee9c9` | 35, two giant round hot-pink hair puffs, winged liner, mint suit, huge pink bow | — |
| Berthe Biscotte | `c7f9c290-46b5-41e4-9e02-51118a6fd1e1` | 58, massive golden-blonde hair roll, round tortoiseshell glasses, lilac tweed suit, orange blouse, baguette brooch | — |

## Assignment (one character per account / strategy)

- Barnaby → PZEN RSI Mean Reversion (shouts "Pulse Zen!") — done 2026-10-05,
  `https://d2ol7oe51mr4n9.cloudfront.net/user_2zKMA0BhEQMQrmR8OpIagvrvlFP/503eece8-62d2-4f45-9252-72166fd9cf0f.mp4`
- Barnaby → Agent 18 wallet-follow explainer (narrator VO, Barnaby reacts; v2 after
  user fixes: no extra arm, Agent 18 on his monitor, he only looks) — 2026-10-06,
  `https://d2ol7oe51mr4n9.cloudfront.net/user_2zKMA0BhEQMQrmR8OpIagvrvlFP/68e66b83-1641-4ac5-b0b2-50e79a00f47b.mp4`
  (the Cyril v1 of the same clip was rejected for an extra arm and a game on screen)
- Percival → HEX RSI Mean Reversion (shouts "HEX!")
- Rupert → PLS EMA Trend Follow (avoid saying "PLS" — shout "Pulse Chain!" if needed)
- Cyril → PLS RSI Mean Reversion

## User's Agent 18 playbook (real names to show on the board)

From the user's dashboard screenshot (app.zencore.solutions, 2026-10-05):
- PZEN RSI Mean Reversion · PZEN/PLS · 1d · Long — status RSI 42, MONITOR POSITION
- PLS RSI Mean Reversion · PLS/PLS · 1d · Long — RSI 38
- PLS EMA Trend Follow · PLS/PLS · 1d · Long
- HEX RSI Mean Reversion · HEX/PLS · 1d · Long
Rules (mean reversion): entry RSI(14) < 30 near 30-day support; exit RSI(14) > 65 or +6%;
stop 2% below entry. Do not display paper-replay results.

## Reusable media

| What | Media / job id | Notes |
|---|---|---|
| Agent 18 board still (1600×900) for on-camera monitors | `f34574ce-b12f-468d-8b87-6eb837816be2` | Pass as `image_references`; leaderboard + wallet alerts |
| Wallet-follow narrator VO (Archie, 25.5 s) | job `f6f75391-7223-4a4f-ae33-f89a34455ae6` | "Agent Eighteen finds the PulseChain wallets that are actually winning…" |
| Barnaby noir detective covers (1500×600) | `88ed5925-…` (magnifier), `7d352ec1-…` (stakeout) | X Article covers |
| iPhone POV insert — gold phone in Sylvie's yellow gloves, golden-orb Pulse Zen graphic (1.77 s, no audio; Paris street blurred behind) | `6d892e47-8d4b-4bdf-8d4d-c30a00d687c4` | https://d2ol7oe51mr4n9.cloudfront.net/user_2zKMA0BhEQMQrmR8OpIagvrvlFP/6d892e47-8d4b-4bdf-8d4d-c30a00d687c4.mp4 — cut-in whenever a character "checks Pulse Zen" |
| iPhone held up by Sylvie with the PZEN chart on screen (8.37 s, no audio; Champs-Élysées background) | `0331d051-7148-45b2-924e-ce485ed9d411` | https://d2ol7oe51mr4n9.cloudfront.net/user_2zKMA0BhEQMQrmR8OpIagvrvlFP/0331d051-7148-45b2-924e-ce485ed9d411.mp4 |
| Sylvie voice lines (cloned accent) — tennis clip | `64c82c1d…` keep-fit, `a66c9fa1…` investing, `183d79dd…` Agent 18 | seed_audio jobs, 2026-10-06 |
| Sylvie tennis-court frames (same court/outfit) | to-camera `397c9b9a…`, glance `290b8337…`, phone `2bdf85fe…`, look-up `a8de4bcb…`, walk-in `26d08424…`, shirtless players `3078e607…` | Nano Banana 2 jobs |
