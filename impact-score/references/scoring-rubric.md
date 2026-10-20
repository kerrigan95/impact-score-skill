# Impact Score rubric

Contents: 1. Relevance, 2. Domain trust, 3. Placement, 4. Content quality, 5. Combining into the Impact Score, 6. Worked examples.

Scores are 0 to 10, one decimal allowed. Be strict and consistent: the same evidence should always get the same score.

## 1. Relevance (weight 45 before buying, 35 live)

Score topical fit with the **topic family tree**. Topics belong to families, and links inside a family make sense to readers and to search engines.

| Score | Relationship | Example |
|---|---|---|
| 9 to 10 | Same topic: the site covers the target's subject | Any football site (club, fan, regional or league news) linking to football tickets. A payments news section linking to a payment gateway |
| 8 to 9 | Business media to any Business-family target | London business news site linking to a link building or SEO marketplace |
| 7 to 8 | Same family, or business media to a Money-family target | Business or finance magazine linking to a high-risk payment gateway or a crypto exchange |
| 5 to 6 | Cousins, one step further out | Marketing blog linking to a consumer gadget, finance site linking to real estate |
| 3 to 4 | Distant but defensible | Lifestyle site with a money section linking to a loan comparison |
| 0 to 2 | Unrelated | Gardening blog linking to a casino page |

Example families (not exhaustive):
- **Business:** business, entrepreneurship, startups, marketing, SEO, digital marketing, advertising, sales, B2B services, business software and SaaS
- **Money:** finance, banking, fintech, payments, investing, trading, crypto, insurance, accounting, personal finance
- **Tech:** software, SaaS, AI, cybersecurity, IT, gadgets, telecom
- **Health:** health, fitness, nutrition, wellness, medical, supplements
- **Leisure:** gaming, iGaming, sports, sports betting, entertainment
- **Home:** home, interior, garden, DIY, real estate, construction
- **Travel:** travel, hospitality, aviation, outdoors

**Business media is the hub.** A general business publication scores 8 to 9 for any Business-family target, because marketing, SEO, sales and B2B services are core business topics and its readers are the people who buy them. It scores 7 to 8 for Money-family targets, which are close but one step away.

Rules:
- **Same subject means 9 to 10.** Narrower focus inside the subject (one club, a regional league, a different competition, one product line) and the target's commercial angle (tickets, shop, comparison) are not deductions. The article is written to bridge them.
- **Prospect mode: score the best-fitting section, not the homepage.** Content for a bought link is written to fit, so ask "can this site credibly publish an article in the target's family?" A business magazine with fintech and payments sections is a 7 to 8 for a payments target, even if its homepage leads with general news.
- **Never penalise the target's niche.** Gambling, high-risk payments, crypto, CBD, adult-adjacent or other regulated industries are judged on topic fit only. "This niche is risky" is not a relevance argument.
- Audience differences inside the same family (general business readers vs merchants) are a note, not a deduction of more than 1 point.
- Language and market still count. A Danish site linking to a Finnish-language page scores lower unless the audience overlaps.
- A strong site in an unrelated family still scores low. Relevance is never rescued by DR.
- If an anchor is given, also score anchor fit (0 to 10): does it describe the target and read naturally? Fold it in as 85% topical relevance, 15% anchor fit.

## 2. Domain trust (weight 35 before buying, 25 live)

Start from authority and traffic, then subtract for red flags. Clamp the result to 0 to 10.

Domain trust is a property of the domain only. Judge it once per domain and reuse it for every target, so the same site never gets two different trust scores.

Decide the site type first (news, directory, blog, niche site, ecommerce, other). Any site publishing frequent news or match reports counts as news, including fan, club and league sites. It changes how outbound linking is read.

**Base**
- DR points = DR ÷ 10 (use the tool's equivalent authority score on a 0 to 100 scale if not Ahrefs).
- Traffic points = (log10(monthly organic traffic + 1) − 1) × 2.2, clamped to 0 to 10. Roughly: 100 visits ≈ 2.2, 1,000 ≈ 4.4, 10,000 ≈ 6.6, 100,000 ≈ 8.8.
- Base = 0.45 × DR points + 0.55 × traffic points. Traffic weighs more because it shows a real audience and Google's current opinion of the site.

**Deductions**

| Check | Condition | Deduction | What it suggests |
|---|---|---|---|
| Traffic per keyword | traffic ÷ keywords above 100 | −2 | Inflated, bot or one-lucky-page traffic |
| | above 40 | −0.75 | Worth a closer look |
| | traffic with zero keywords | −1.5 | Traffic number unreliable |
| DR vs traffic | DR 40+ with under 500 visits | −1.5 | Authority pumped with links, no audience |
| Outbound linking (blogs, niche sites, other) | linking-out dofollow domains ÷ referring dofollow domains above 1.5 | −2 | Link seller pattern |
| | above 0.8 | −0.75 | Links out heavily |
| Outbound linking (news sites, directories) | ratio above 5 only | −2 | Extreme even for a site type that links out by nature |
| 12-month trend | average of last 3 months vs first 3 months down 60%+ | −2.5 | Likely hit by an update or abandoned |
| | down 30 to 60% | −1 | Declining |
| Growth | last 3 months 30%+ above the first 3 | +0.5 | A growing site |
| Spike | any month above 4× the 12-month median | −0.5 | Check what caused it |
| Market | under 20% of traffic from the target market (when given; "uk" means "gb" in Ahrefs) | −1 | Audience doesn't match |
| Majestic | TF ÷ CF below 0.4 | −1 | Volume of links over quality |
| | TF 25+ and ratio fine | +0.5 | Trusted link profile |

**Walk-away rule.** If the site hits two or more major red flags (inflated traffic per keyword, traffic with zero keywords, high DR with no traffic, link seller outbound ratio as defined for the site type, 60%+ traffic collapse, or any major spam check below), cap Domain trust at 2 and make the verdict Skip, whatever the other pillars say. This is the "fail two, walk away" rule from the 5-minute check.

**Spam checks** (anchor cloud, outbound anchors, ranking keywords). Full rules in `spam-patterns.md`. Spam only deducts when the links are mostly dofollow, or for keywords, when off-topic traffic is the majority. Otherwise it's a "Spam to watch" note with no deduction.

| Check | Mostly dofollow / majority | Mostly nofollow / minority |
|---|---|---|
| Adult or pharma anchors pointing in | −2, major | Watch note |
| Heavy injected spam in inbound anchors | −2, major (light: −0.75) | Watch note |
| 3+ random or numbered anchors (88AA, OPEN88, KQXSMN) | −1 | Watch note |
| Spam anchors linking out, unrelated to the site | −2, major | Watch note |
| Off-topic keyword traffic | Over 50%: −1.5, major | 25 to 50%: watch note |
| Over 60% of traffic from its own name, 1,000+ visits, not a known brand | −1.5, major | |

**Strong-site protection.** Relevance 7+ and Domain trust before spam deductions 7+, with no major red flags, is never a Skip. It's at least Negotiate, with spam shown as a watch note.

Also flag (as notes, no automatic deduction) anything from `spam-patterns.md`: topic spread across unrelated niches, a rented casino or crypto subfolder, spammy anchor cloud, traffic geography that doesn't match the language.

## 3. Placement (weight 10 before buying, 20 live)

### Live link (measured)

| Where the link sits | Base |
|---|---|
| Article body, in a sentence | 8 |
| Related posts, author bio | 3 |
| Sidebar or widget | 2 |
| Footer, navigation, comments | 1 |
| Not on the page | 0, verdict Not found |

Adjust:
- In the first third of the article: +1. In the last 20%: −1.
- rel nofollow or ugc: −3. rel sponsored: −2. Dofollow: no change.
- More than 15 other outbound domains in the content: −1.5 (crowded, value is diluted).

Then blend: 70% the measured score above, 30% a contextual judgement of how naturally the link sits in its paragraph (0 to 10).

### Prospect (judged)

Score the site's capacity to host the link, not the current homepage: the article and placement are negotiated.
- 8 to 9: a real editorial site with a section in the target's family. This is the default for any active publisher on the right topic.
- 5 to 7: **directories and listing sites** with a matching category (for example a Finance category for a payments target). A listing or company profile is the site's native placement and is valid. These can reach Negotiate.
- 4 to 6: the site would place it, but only in a generic or loosely fitting article.
- 2 to 3: the only realistic option is a footer, sidebar or blogroll link.
- 0 to 1: link farm: posts that exist only to carry links, outbound casino, CBD or loan clutter across unrelated topics.

Sponsored labels and press-release or wire sections are **notes for negotiation**, not deductions. Plenty of strong publishers run both.

## 4. Content quality (weight 10 before buying, 20 live)

Judge the linking page (live) or a typical recent article on the site (prospect).
- 9 to 10: original, well structured, clear expertise, updated, light ads.
- 6 to 8: solid and useful, some generic sections.
- 3 to 5: thin, spun or AI-generic, heavy ads, written around the links.
- 0 to 2: no editor would sign off on it: keyword stuffing, broken language, pages that only exist to hold links.

For a directory, judge the category and listing pages (are they maintained, real businesses, useful categories) rather than editorial depth.

If the article itself ranks for keywords (page-level traffic above zero), that's evidence Google values it: nudge up by up to 0.5.

## 5. Combining into the Impact Score

Impact Score = (Σ weight × pillar score) ÷ (Σ weights of the pillars that were scored) × 10, rounded.

Weights: before buying 45 / 35 / 10 / 10 (relevance, trust, placement, content). Live link 35 / 25 / 20 / 20.

- 70 to 100: Build
- 50 to 69: Negotiate
- 0 to 49: Skip
- Overrides: relevance at or below 2 (unrelated family) is Skip. Two or more major trust red flags is Skip. Live link missing is Not found.

Weights can be changed if the user asks (for example a client who cares only about relevance). Say which weights you used when they differ from the defaults.

## 6. Worked examples

**Build.** Sports site, basketball article about NBA players and ankle injuries, link to an ankle brace page in the body copy, dofollow. DR 72, 180k monthly traffic, healthy trend. Relevance 10, Domain trust 9, Placement 9, Content quality 8. Score 92. Build.

**Negotiate.** Danish fintech news site, relevant to a crypto exchange target, strong metrics, but every post carries a "Sponsored" label and links sit near the end. Relevance 8, Trust 7, Placement 5, Content 7. Score 70, a Build on paper, but the label and placement are the real issues: negotiate a body placement and the label, or accept and price it lower.

**Build (same subject).** Spanish regional football news site, DR 41, about 4,400 visits and growing, target is a Champions League ticket page. Football site plus football tickets is the same subject: relevance 9.5, even though the site covers Valencia clubs rather than European competition. Trust 5.5, placement 7, content 6. Before-buying score 75. Build, with an article about a Valencia CF or Villarreal European fixture.

**Negotiate (same family).** European business magazine, DR 71, about 2,300 monthly visits and growing, with fintech and payments sections. Target: a UK high-risk payment gateway. Business and payments sit in the same money family, so relevance is 7.5, not 4. Outbound ratio 2.8x is normal for a news site. The weak point is traffic for the DR and a small UK share, so negotiate price and ask for the payments section.

**Negotiate (directory).** UK business directory, DR 24, about 3,900 visits and growing, with a Finance category. A listing in Finance is the native placement for a directory and is valid. Fine as a low-cost diversification link with a branded or partial anchor.

**Negotiate with a spam watch (spammed fan site).** German Barcelona fan site, DR 35, 38,000 visits, a perfect topic match for Champions League tickets. But its top inbound anchors include "88AA", "OPEN88", "KQXSMN", Telegram SEO-seller spam and IPTV anchors, and it links out with Vietnamese lottery anchors ("xổ số miền nam", XSMN) from spam member profiles. The inbound spam is almost all nofollow, so it's only a watch note. The outbound lottery links are dofollow, so that's one major flag and a Domain trust hit. Result: Negotiate, with a clear note that the site hosts spam profiles and should be re-checked. If the inbound spam were dofollow too, it would be two major flags and a Skip.

**Skip.** "Premium" DR 70 site ranking for 29 keywords and claiming 238,000 visits. That's about 8,200 visits per keyword, so the traffic is not real. It links out to 4x more domains than link to it. That's two major red flags, so Domain trust is capped at 2 and the verdict is Skip by the walk-away rule, even with a relevant article. The site matches the "Inflated premium site" pattern.
