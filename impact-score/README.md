# Impact Score: a Claude skill for vetting backlinks

Stop buying links on DR alone. This skill teaches Claude to score any link, before you buy it or after it goes live, with four questions:

1. **Relevance.** Would a reader of this page actually want your page?
2. **Domain trust.** Is this a real site with a real, healthy audience?
3. **Placement.** Is the link in the article body, or buried in a sidebar or footer?
4. **Content quality.** Would an editor sign off on the page your link lives on?

You get a score from 0 to 100, a **Build**, **Negotiate** or **Skip** verdict, the red flags it found, and a plain explanation of why, so you learn to spot spam yourself.

Created by Tamara Novitović, Head of SEO at Bazoom.

## Install

1. Download `impact-score.zip`.
2. In Claude, open Settings and find Skills (under Capabilities or Customize, depending on your app version). Make sure code execution is turned on.
3. Upload the ZIP and switch the skill on.

## Connect your data (recommended)

The skill uses whatever you have connected in Claude:
- **Ahrefs** (best), Semrush or Moz connectors for metrics
- **Firecrawl** or Claude's built-in web fetch to read both pages
- A **Majestic** export, if you have one, for Trust Flow and Citation Flow

No connectors? Paste the metrics (DR, organic traffic, keywords, referring domains, linking-out domains) and Claude scores the rest.

## Try it

- "Impact Score this link before I buy it: technewsdaily.com → https://mysite.com/best-vpn"
- "Audit this live link: https://blog.example.com/article → https://mysite.com/page, anchor 'best running shoes'"
- "Here are 20 domains from a marketplace and my target page. Which are worth buying?"
- "Is this site a link farm? DR 68, 120k traffic, 40 keywords, links out to 9,000 domains."

## What it catches

Inflated traffic, DR without an audience, link-selling outbound patterns, sites in traffic decline, wrong-market audiences, PBNs, parasite sections, bulk niche edits and more. The full list is in `references/spam-patterns.md`.

All metrics are third-party estimates. Treat the score as a strong second opinion, not a guarantee.
