# creator-sourcing

A Claude Code skill that turns a niche into a ranked, contactable creator list plus
a self-contained dashboard.

It discovers creators three independent ways (profile/bio search, hashtag search,
video search), enriches each with follower count, average likes and comments,
engagement rate and last-post date, ranks them, resolves public contact paths from
bios and link-in-bio pages, and renders a filterable HTML dashboard.

Requires the **ScrapeCreators** MCP connector. No API key lives in this repo — the
connector holds credentials server-side.

## Install

```bash
git clone https://github.com/mikefutia/claude-scrapes-ig.git
cp -R claude-scrapes-ig/creator-sourcing ~/.claude/skills/
```

Then invoke it in Claude Code with `/creator-sourcing`.

## Inputs

| Input | Default | Notes |
|---|---|---|
| `platform` | instagram | Instagram and TikTok verified. YouTube endpoints mapped but unverified. |
| `niche keywords` | — | 2–3 bio terms, 2–3 hashtags, 2 video-search phrases |
| `follower range` | no limit | Applied after enrichment, on the fresh follower count |
| `how many results` | all | A cut-off applied after ranking, not during discovery |

## Pipeline

```
1. collect_pool.py     3-way search    → output/raw-pool.json
2. enrich.py           metrics + rank  → output/enriched.json + run-meta.json
3. contacts.py         emails + links  → enriched.json (in place)
4. build_dashboard.py  self-contained  → output/creator-pool.html
```

The scripts never call the API. Claude makes the MCP calls; large responses spill to
the session `tool-results` cache, and the scripts parse them from disk with
`--cache-dir`. That keeps context clean and makes reruns free.

## Read this before changing the metrics

`reference/gotchas.md` documents ten data-quality landmines, every one of which was
hit in a real run and produced plausible-but-wrong output. The three that matter most:

- **Pinned posts break chronological order.** Recency must come from
  `max(timestamp)`, never the first item. One creator's grid led with a post 686 days
  older than their newest — taking `[0]` would have dropped active creators as stale.
- **A 12-post mean is dominated by one viral post.** In one Instagram run, 28 of 58
  creators had a top post ≥5× their median; one read 15.93% on the mean and 0.17% on
  the median. Always compute both.
- **Follower-based engagement is meaningless on TikTok.** The For You page
  distributes beyond followers, so likes routinely exceed follower count — 11 of 70
  creators scored over 100%, topping out at 334%. Use `(likes + comments) / views`.

`reference/platforms.md` has the verified per-platform endpoint map and field paths,
including several places where the live response disagrees with the tool's own
documentation.

## Scope

Sources public professional data for partnership outreach — creators' own bios and
their own link-in-bio pages. It does not compile personal information beyond a
business contact path, and it does not send anything on your behalf.
