---
name: impact-score
description: Score backlinks and link building prospects with the Impact Score framework (Relevance, Domain trust, Placement, Content quality) and give a clear Build, Negotiate or Skip verdict. Use this whenever someone wants to vet a publisher, guest post site, niche edit or link insertion before buying, audit a link that is already live, check if a site or link is spammy, compare link prospects, decide which links are worth paying for, or asks "is this a good link?", "should I buy this link?", "is this site a PBN / link farm?", or pastes a list of domains from a marketplace. Also use it when someone shares Ahrefs, Semrush, Majestic or Moz metrics for a site and wants to know if the site is safe to get a link from, even if they never say "Impact Score".
---

# Impact Score

A link is worth buying when it is relevant, sits on a real site with a real audience, is placed where readers actually see it, and lives on content an editor would sign off on. DR on its own tells you almost nothing. This skill turns that into a repeatable score so anyone can make the call, and explains the reasoning so they learn to spot spam themselves.

Framework by Tamara Novitović, Head of SEO at Bazoom.

## The four pillars

Each pillar is scored 0 to 10, then weighted into an Impact Score from 0 to 100.

| Pillar | Before buying | Live link | Question it answers |
|---|---|---|---|
| Relevance | 45% | 35% | Would a reader of this page naturally want the target page? |
| Domain trust | 35% | 25% | Is this a real site with real, healthy organic traffic? |
| Placement | 10% | 20% | Is the link editorial and in-content, or hidden in a sidebar, footer or bio? |
| Content quality | 10% | 20% | Is the linking page something an editor would publish? |

Before buying, the article and placement are still negotiable, because the content is written to fit. So relevance and metrics carry the decision, and placement and content only pull a site down when it genuinely can't host an editorial link. Once a link is live, placement and content are fixed facts, so they count for more.

Verdict: **Build** at 70 or above, **Negotiate** from 50 to 69, **Skip** below 50.

Four overrides beat the number:
- Relevance at 2 or below (an unrelated topic family) is always **Skip**. A strong site on the wrong topic is a wasted link, and a pattern of them looks manipulative.
- Relevance 7+ and Domain trust before spam deductions 7+, with no major red flags, is never a Skip: at least **Negotiate**, with any spam shown as a watch note.
- Two or more major trust red flags (for example inflated traffic per keyword plus a link seller outbound ratio, or heavy inbound anchor spam plus spam outbound anchors) is always **Skip**. Fail two, walk away. Great relevance never rescues a site that fails two.
- In a live link audit, if the link is not on the page, the verdict is **Not found**.

"Negotiate" means the site is usable if something changes: lower price, removed sponsored label, better placement in the body, a more relevant article, or a different target page. Always say what to negotiate.

Full scoring rules for every pillar are in `references/scoring-rubric.md`. Read it before scoring.

**A site that covers the target's subject is a 9 to 10, full stop.** Any football site is a top match for football tickets, whatever club, league or region it focuses on. Narrower focus inside the subject and the commercial angle of the target (tickets, products, comparisons) are not deductions, because the article bridges them.

**Relevance follows the topic family tree.** Marketing, SEO, sales, B2B services and business software sit in the Business family, and finance, payments, fintech and crypto in the Money family. General business media is the hub: 8 to 9 for any Business-family target, 7 to 8 for any Money-family target. In prospect mode, score the best-fitting section the site can publish in, because the content is written to fit. Never lower a score because the client is in a regulated or high-risk niche: judge topic fit, not the industry.

## Two modes

**Before buying (prospect).** Input: publisher domain or page, target page, optional anchor and target market. Judge the site as a link source.

**Live link audit.** Input: the published article URL, target page, optional expected anchor. Confirm the link exists, then score where and how it sits.

If the user doesn't say which, infer it: a full article URL with a path usually means live, a bare domain means prospect. Ask only if it's genuinely unclear.

## Workflow

### 1. Collect the inputs
Publisher or article URL, target URL, anchor (optional), target market country (optional, helps the geo check). For a list, accept pasted lines, a table or a CSV. Work through lists in batches and keep a running table.

### 2. Get the metrics
Use whatever the user has connected, in this order of preference. Never invent numbers. If no data source is available, ask the user to paste the metrics (see the list below) or score the remaining pillars and mark Domain trust as not scored.

- **Ahrefs connector**: `batch-analysis` with `mode: subdomains`, `protocol: both`, `top_countries: 3` and select `domain_rating, org_traffic, org_keywords, org_keywords_1_3, refdomains_dofollow, linked_domains_dofollow, org_traffic_top_by_country`. It takes up to 100 targets per call, so batch lists. For a live article add the article URL with `mode: exact` to get its `url_rating` and page traffic. For the trend, `site-explorer-metrics-history` with `history_grouping: monthly`, `select: date,org_traffic`, and `date_from` 12 months back.
- **Spam checks with Ahrefs** (run these for every prospect, they catch what metrics hide):
  - Inbound anchors: `site-explorer-anchors`, `history: live`, `select: anchor,refdomains,links_to_target,dofollow_links`, `order_by: refdomains:desc`, `limit: 30`.
  - Outbound anchors: `site-explorer-linked-anchors-external`, `select: anchor,linked_domains,dofollow_links`, `order_by: linked_domains:desc`, `limit: 30`.
  - Ranking keywords: `site-explorer-organic-keywords`, `date` = yesterday, `select: keyword,sum_traffic,best_position_url`, `order_by: sum_traffic:desc`, `limit: 25`. Don't trust Ahrefs' `is_branded` flag for the own-name check: it also marks topic entities (a club name on a fan site) as branded. Match the site's own name instead.
  Then judge them with the anchor and keyword checks in `references/spam-patterns.md`. Spam only counts against the site when those links are mostly dofollow, or for keywords, when off-topic traffic is the majority. Mostly-nofollow spam is reported as "Spam to watch", with no deduction.
- **Semrush or Moz connectors**: use the equivalent authority score, organic traffic, organic keywords, referring domains and outbound linking domains.
- **Majestic**: if the user has a Majestic export or connector, add Trust Flow, Citation Flow and Topical Trust Flow.
- **Pasted by the user**: DR or equivalent, organic traffic, organic keywords, referring domains, linking-out domains, top traffic countries, 12-month traffic trend.

### 3. Read both pages
Use a crawler connector (Firecrawl `firecrawl_scrape` with `formats: ["markdown","links","html"]` and `onlyMainContent: true`) or the web fetch tool. Read the linking page and the target page. Note title, meta description, headings, language, publish date, word count and the main topic of each.

For a live audit, find the link in the HTML. Record where it sits (body, sidebar, footer, author bio, related posts, comments), its `rel` attribute (dofollow, nofollow, sponsored, ugc), the anchor text, how far into the article it appears, and how many other outbound domains the content links to. Match the target loosely: ignore protocol, `www`, trailing slashes and tracking parameters.

If a page can't be fetched, say so and score what you can. Don't guess what a page says.

### 4. Score
**Domain trust belongs to the domain, not the pair.** Decide site type and the spam check once per publisher domain, then reuse that exact judgement for every target page you score against it. The same domain must get the same Domain trust whatever the target. Only Relevance, Placement and Content quality change from target to target. In a list, group rows by publisher and judge each domain once.

Decide the site type first (news, directory, blog, niche site, ecommerce, other). Count any site publishing frequent news or match reports as news, including fan, club and league sites. News sites and directories link out by nature, so their outbound ratio is only a red flag above 5x. Score each pillar with `references/scoring-rubric.md`. Check the domain against `references/spam-patterns.md`, including the anchor cloud, outbound anchors, random anchors, off-topic keyword traffic and own-name traffic checks. Every pattern you match becomes a named flag with the actual anchors or keywords as evidence.

If code execution is available, run `scripts/impact_score.py` for the Domain trust score and the final weighting so results are consistent across runs:

```bash
python scripts/impact_score.py input.json
```

The input format is documented at the top of the script. It accepts one link or a list. Without code execution, apply the same formulas from the rubric by hand.

If a pillar can't be scored (no metrics, page blocked), leave it out and re-weight the others. Mark the result "Partial data".

### 5. Report
Use the output format below. Lead with the verdict. Keep reasons concrete: numbers, the actual topics, the actual placement. The goal is that the reader learns what to look for next time.

## Output format

For a single link:

```
## [Verdict]: Impact Score [NN]/100
[publisher] → [target page]

| Pillar | Score | Why |
|---|---|---|
| Relevance | x/10 | [publisher topic] vs [target topic]. One sentence. |
| Domain trust | x/10 | Key numbers and any flags. |
| Placement | x/10 | Where the link sits or would sit, rel, position. |
| Content quality | x/10 | One sentence. |

**Red flags:** [named spam patterns matched, or "None found"]
**Spam to watch:** [nofollow or minority spam that doesn't affect the score today but should be re-checked later, or leave out]
**What to do:** [Build as is / what to negotiate / why skip, and a better alternative if obvious. Must agree with the verdict, which comes from the score, never the other way round]
**Why this matters:** [one or two sentences teaching the principle behind the biggest factor]
```

For a list: one summary table (publisher, target, verdict, score, the four pillar scores, DR, traffic, main flag), sorted by score, then short notes only for Negotiate rows and any surprising Skips. Offer a CSV or spreadsheet if the list is longer than about 10 rows.

## Teaching, not just scoring

Many people asking for this are learning what separates a good link from a spammy one. When a link fails, name the pattern and show the evidence, for example: "29 ranking keywords can't produce 238,000 visits. That's 8,200 visits per keyword, which points to inflated traffic." When a modest site wins, say why: "DR 38, but it writes only about trail running and the target is a running shoe guide. Relevance beats DR."

Point out the common misconceptions when they show up:
- High DR with almost no organic traffic is a red flag, not a win.
- A relevant DR 35 site often beats an unrelated DR 80 generalist.
- "Sponsored" tags are a disclosure issue to negotiate, not proof of spam.
- A blog that links out to far more domains than link to it is usually selling links. News sites and directories link out by nature, so judge them on more than the ratio.
- Relevance isn't only "same keyword". A business or finance site is a natural home for a payments, banking or crypto link.
- A directory listing in the right category is a legitimate, low-cost diversification link, not spam.
- Traffic that collapsed recently means the site may have been hit, and your link may be discounted too.
- Good metrics and a perfect topic can hide a hacked or spammed site. Always look at what links in, what links out, and what the site actually ranks for.

## Guardrails

- Never fabricate metrics, page content or a found link. Say what's missing.
- Third-party metrics are estimates. Present them as signals, and say so when a call rests on one number.
- Stay neutral about vendors and marketplaces. Judge the site, not who sells it.
