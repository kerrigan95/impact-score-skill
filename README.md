# Impact Score: a free Claude skill for vetting backlinks

"It's DR 70 though" is not a link strategy.

The Impact Score is the framework I've used for years to decide whether a link is worth building, and the one I've been showing on stage. This repo turns it into a Claude skill, so Claude can score any link for you and explain why.

It asks four questions about every link:

1. **Relevance.** Would a reader of this page actually care about your page?
2. **Domain trust.** Is the traffic real, or just dressed up?
3. **Placement.** Is the link in the article, or hiding in a footer?
4. **Content.** Would a real editor put their name on this page?

You get a score from 0 to 100, a **Build**, **Negotiate** or **Skip** verdict, the red flags it found, and the reasons, so you learn to spot it yourself.

It also checks what most link audits get wrong:
- the anchor cloud pointing at the site, and whether that spam is actually **dofollow**
- what the site links **out** to, and from where
- what the site **really ranks for**, so booster, parasite and own-name traffic shows up
- random anchors like `88AA` or `OPEN88` that make no sense

Spam that's mostly nofollow doesn't kill a good site. It gets a "Spam to watch" note instead, because negative SEO happens to plenty of real publishers.

## Install

1. Download **[impact-score.zip](https://github.com/kerrigan95/impact-score-skill/releases/latest/download/impact-score.zip)**.
2. In Claude, open **Settings** and find **Skills** (under Capabilities or Customize, depending on your app version). Make sure code execution is on.
3. Upload the ZIP and switch the skill on.

## Connect your data (recommended)

The skill uses whatever you have connected in Claude:
- **Ahrefs** works best. Semrush or Moz also work.
- **Firecrawl**, or Claude's built-in web fetch, to read both pages
- A **Majestic** export, if you have one, for Trust Flow and Citation Flow

No connectors? Paste the metrics (DR, organic traffic, keywords, referring domains, linking-out domains) and Claude scores the rest.

## Try it

- `Impact Score this link before I buy it: technewsdaily.com → https://mysite.com/best-vpn`
- `Audit this live link: https://blog.example.com/article → https://mysite.com/page, anchor "best running shoes"`
- `Here are 20 domains from a marketplace and my target page. Which are worth buying?`
- `Is this site a link farm? DR 68, 120k traffic, 40 keywords, links out to 9,000 domains.`

## Send me your cursed link stories

The weird cases make the next version smarter. The "premium" site that wasn't, the anchor that made zero sense, the audit that told you to disavow half the internet: **[share it here](https://github.com/kerrigan95/impact-score-skill/issues/new?template=cursed-link.yml)**.

## What's inside

```
impact-score/
├── SKILL.md                      the workflow Claude follows
├── references/
│   ├── scoring-rubric.md         how every pillar is scored
│   └── spam-patterns.md          spam patterns, anchor and keyword checks
└── scripts/
    └── impact_score.py           the scoring maths, so results stay consistent
```

All metrics are third-party estimates. Treat the score as a strong second opinion, not a guarantee.

Made by **Tamara Novitović**, Head of SEO at Bazoom. Free to use and share with credit.
