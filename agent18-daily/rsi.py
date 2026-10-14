#!/usr/bin/env python3
"""Today's Agent 18 playbook cards from public PulseX daily candles (GeckoTerminal).

Writes card.json: all cards plus the one to feature. Strategy rules (user's playbook):
mean reversion entry RSI(14) < 30, exit RSI(14) > 65. Usage: python3 -I rsi.py [out.json]
"""
import datetime, json, sys, time, urllib.request

POOLS = "https://api.geckoterminal.com/api/v2/networks/pulsechain/pools/"
CARDS = [  # name, pair label, pool, query, spoken name (phonetic)
    ("PZEN RSI Mean Reversion", "PZEN/PLS · 1d · Long", "0xdfc23736c6910dc27e7fb60553cd1f44d65eb556", "currency=token&token=base", "Pulse Zen"),
    ("HEX RSI Mean Reversion", "HEX/PLS · 1d · Long", "0x19bb45a7270177e303dee6eaa6f5ad700812ba98", "currency=token&token=base", "HEX"),
    ("PLS RSI Mean Reversion", "PLS · 1d · Long", "0x6753560538eca67617a9ce605178f788be7e524e", "currency=usd&token=quote", "Pulse Chain"),
]
ENTRY, EXIT = 30.0, 65.0


def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"accept": "application/json"})
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429 or i == tries - 1:
                raise
            time.sleep(15 * (i + 1))


def rsi_series(closes, n=14):
    g = [max(closes[i] - closes[i - 1], 0) for i in range(1, len(closes))]
    l = [max(closes[i - 1] - closes[i], 0) for i in range(1, len(closes))]
    ag, al = sum(g[:n]) / n, sum(l[:n]) / n
    out = []
    for i in range(n, len(g)):
        ag = (ag * (n - 1) + g[i]) / n
        al = (al * (n - 1) + l[i]) / n
        out.append(100.0 if al == 0 else 100 - 100 / (1 + ag / al))
    return out


cards = []
for name, sub, pool, q, spoken in CARDS:
    d = get(f"{POOLS}{pool}/ohlcv/day?aggregate=1&limit=100&{q}")
    today = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    # Completed daily candles only: drop today's still-forming candle.
    rows = [r for r in sorted(d["data"]["attributes"]["ohlcv_list"])
            if r[0] < today.replace(tzinfo=datetime.timezone.utc).timestamp()]
    rs = rsi_series([r[4] for r in rows])
    now, prev = rs[-1], rs[-2]
    if now > EXIT:
        status = "EXIT RULE HIT"
    elif now < ENTRY:
        status = "SETUP TRIGGERED"
    else:
        status = "MONITOR"
    dist = min(abs(now - EXIT), abs(now - ENTRY))
    cards.append(dict(name=name, sub=sub, spoken=spoken, rsi=round(now, 1), prev=round(prev, 1),
                      status=status, distance=round(dist, 1),
                      date=str(datetime.datetime.utcfromtimestamp(rows[-1][0]).date())))
    time.sleep(3)

# Feature a card that actually hit a rule; otherwise the one closest to a threshold.
hit = [c for c in cards if c["status"] != "MONITOR"]
feature = max(hit, key=lambda c: abs(c["rsi"] - 50)) if hit else min(cards, key=lambda c: c["distance"])
out = dict(generated=datetime.datetime.utcnow().isoformat() + "Z", feature=feature["name"], cards=cards)
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "card.json", "w"), indent=2)
print(json.dumps(out, indent=2))
