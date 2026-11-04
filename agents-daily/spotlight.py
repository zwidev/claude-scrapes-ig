#!/usr/bin/env python3
"""Pick today's agent + character and verify the agent against its live marketplace page.

Usage: python3 -I spotlight.py [agent.json] [--slug SLUG]
Writes agent.json. Exits non-zero (and writes nothing) if the marketplace can't be read,
so the daily run reports the failure instead of inventing anything.
"""
import datetime, html, json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://zencore.solutions/marketplace/stacks/"
CHARS = ["Cyril Cranium", "Barnaby Biro", "Percival Pallor", "Rupert Ramekin"]


def page_text(slug):
    req = urllib.request.Request(BASE + slug, headers={"User-Agent": "zencore-spotlight/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        t = r.read().decode("utf-8", "replace")
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=re.S)
    lines = [l.strip() for l in html.unescape(re.sub(r"<[^>]+>", "\n", t)).splitlines() if l.strip()]
    return lines


def check(a):
    """Return (ok, reason, live_billing)."""
    L = page_text(a["slug"])
    try:
        i = L.index("← Back to marketplace")
    except ValueError:
        return False, "page layout changed (no back link)", ""
    status, title = L[i + 2], L[i + 3]
    billing = next((L[j + 1] for j, l in enumerate(L) if l == "Billing"), "")
    joined = " ".join(L)
    if status != "Available":
        return False, f"status is '{status}'", billing
    if a["name"] not in title or f"Agent {a['num']}" not in title:
        return False, f"title is '{title}'", billing
    if a["price"] not in billing:
        return False, f"price changed: '{billing}' (expected {a['price']})", billing
    if re.search(r"Hold at least [\d,]+ PZEN|PZEN gate at checkout", joined):
        return False, "page now requires PZEN", billing
    return True, "", billing


def last_rows():
    p = os.path.join(HERE, "log.md")
    if not os.path.exists(p):
        return []
    return [[c.strip() for c in l.strip().strip("|").split("|")]
            for l in open(p) if re.match(r"\| \d{4}-\d\d-\d\d \|", l) and "(extra)" not in l]


def main():
    out = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else os.path.join(HERE, "agent.json")
    forced = sys.argv[sys.argv.index("--slug") + 1] if "--slug" in sys.argv else None
    agents = json.load(open(os.path.join(HERE, "agents.json")))["agents"]
    rows = last_rows()
    today = datetime.date.today().isoformat()
    if rows and rows[-1][0] == today and "--force" not in sys.argv:
        print(f"Already made today's spotlight ({rows[-1][2]}); nothing to do. Use --force for an extra.", file=sys.stderr)
        sys.exit(4)
    # Character: next after the last spotlight row; the first spotlight follows Rupert (last Agent 18 clip).
    char = CHARS[(CHARS.index(rows[-1][1]) + 1) % 4] if rows else "Cyril Cranium"
    # Agent: next after the last spotlighted agent number.
    start = 0
    if rows:
        m = re.search(r"Agent (\d+)", rows[-1][2])
        nums = [a["num"] for a in agents]
        if m and m.group(1) in nums:
            start = (nums.index(m.group(1)) + 1) % len(agents)
    order = [a for a in agents if a["slug"] == forced] if forced else agents[start:] + agents[:start]
    skipped = []
    for a in order:
        try:
            ok, why, billing = check(a)
        except Exception as e:  # network / HTTP failure: stop, don't guess
            print(f"ERROR: could not read {BASE + a['slug']}: {e}", file=sys.stderr)
            sys.exit(2)
        if ok:
            a = dict(a, character=char, live_billing=billing, url=BASE + a["slug"],
                     date=datetime.date.today().isoformat(), skipped=skipped)
            json.dump(a, open(out, "w"), indent=2)
            print(json.dumps(a, indent=2))
            return
        skipped.append(f"Agent {a['num']} {a['name']}: {why}")
        print("skip:", skipped[-1], file=sys.stderr)
    print("ERROR: no agent passed the live check", file=sys.stderr)
    sys.exit(3)


if __name__ == "__main__":
    main()
