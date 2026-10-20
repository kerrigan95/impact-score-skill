#!/usr/bin/env python3
"""Impact Score calculator. Standard library only.

Usage:
    python impact_score.py input.json            # prints JSON results
    python impact_score.py input.json --table    # prints a markdown table too
    cat input.json | python impact_score.py -

Input: one object or a list of objects. All fields are optional except the
judged scores you have. Unknown or missing metrics are skipped, never guessed.

{
  "publisher": "example.com",
  "target": "https://client.com/page",
  "mode": "prospect" | "live",
  "market": "dk",                       # optional, two-letter country code (uk is read as gb)
  "site_type": "news",                  # news (incl. fan, club, league news) | directory | blog | niche | ecommerce | other
  "metrics": {                          # from Ahrefs, Semrush, Moz or pasted
    "dr": 55,                           # authority score on a 0-100 scale
    "traffic": 12000,                   # monthly organic traffic
    "keywords": 3400,                   # organic keywords
    "refdomains_dofollow": 900,
    "linked_domains_dofollow": 300,
    "top_countries": [["dk", 8000], ["us", 2000]],
    "traffic_history": [5000, 5200, ...],   # monthly, oldest first, ideally 12-13 points
    "tf": 22, "cf": 30                  # Majestic, optional
  },
  "spam": {                             # optional, from inbound anchors, outbound anchors, top keywords
    "inbound_anchors": [["88AA", 0, 25], ["Barcawelt", 88, 377], ...],  # [anchor, dofollow links, total links] or plain strings
    "keywords": [["fc barcelona", 23302], ["barcawelt", 2549], ...],  # [keyword, traffic], top by traffic
    "inbound_spam": "none" | "light" | "heavy",       # your judgement of spam-theme anchors
    "inbound_spam_dofollow_share": 0.05,              # dofollow links / all links for those spam anchors
    "adult_pharma": false,              # porn, escort, viagra or pharma anchors pointing in
    "adult_pharma_dofollow_share": 0.0,
    "outbound_spam": false,             # spam-theme anchors linking OUT, unrelated to the site
    "outbound_spam_dofollow_share": 1.0,              # dofollow links / linked domains for those anchors
    # Spam only deducts when it is confirmed mostly dofollow. A missing dofollow share
    # is treated as unconfirmed: a "watch" note, never a deduction.
    "off_topic_share": 0.1,             # share of top keyword traffic unrelated to the site's topic
    "known_brand": false                # true only for an established, well-known publication or brand
  },
  "placement": {                        # live mode, measured from the page HTML
    "found": true,
    "zone": "body" | "sidebar" | "footer" | "author bio" | "related posts" | "navigation" | "comments",
    "rel": "",                          # "", "nofollow", "sponsored", "ugc"
    "position": 0.25,                   # 0 = top of the article, 1 = end
    "outbound_domains": 6,
    "context_score": 8                  # your 0-10 judgement of contextual fit
  },
  "scores": {                           # your judged pillar scores, 0-10
    "relevance": 8,
    "anchor_fit": 7,                    # optional
    "placement": 7,                     # prospect mode only (live is measured)
    "content": 7
  },
  "weights": {"relevance": 45, "trust": 35, "placement": 10, "content": 10},  # optional; defaults differ by mode
  "thresholds": {"build": 70, "negotiate": 50, "relevance_floor": 3}          # optional
}
"""
import json
import math
import re
import sys
import unicodedata

# Before buying, the article and placement are still negotiable, so relevance and metrics carry the decision.
DEFAULT_WEIGHTS_PROSPECT = {"relevance": 45, "trust": 35, "placement": 10, "content": 10}
# Live links are fixed, so placement and content count for more.
DEFAULT_WEIGHTS_LIVE = {"relevance": 35, "trust": 25, "placement": 20, "content": 20}
DEFAULT_THRESHOLDS = {"build": 70, "negotiate": 50, "relevance_floor": 2}
LINK_HEAVY_TYPES = {"news", "directory"}
ZONE_BASE = {"body": 8, "related posts": 3, "author bio": 3, "sidebar": 2,
             "footer": 1, "navigation": 1, "comments": 1}


def clamp(v, lo=0.0, hi=10.0):
    return max(lo, min(hi, v))


def num(x):
    try:
        return None if x is None or x == "" else float(x)
    except (TypeError, ValueError):
        return None


def is_gibberish(a):
    """Random or numbered anchors that make no sense: 88AA, OPEN88, KQXSMN, comment-46123, 1234567."""
    a = " ".join(str(a or "").split())
    if not a or len(a) > 24 or re.search(r"^https?:|www\.|\.[a-z]{2,4}(/|$)", a, re.I):
        return False
    if re.match(r"^(comment|post|member|user|id)[-_ ]?\d+$", a, re.I):
        return True
    if re.match(r"^(19|20)\d\d$", a):
        return False
    digits, letters = len(re.findall(r"\d", a)), len(re.findall(r"[a-z]", a, re.I))
    if digits >= 2 and letters >= 1 and " " not in a:
        return True
    if re.match(r"^\d{4,}$", a):
        return True
    if re.match(r"^[A-Z]{4,8}$", a) and not re.search(r"[AEIOUY]", a):
        return True
    return False


def brand_token(host):
    parts = str(host or "").lower().replace("www.", "").split(".")
    second = {"co", "com", "org", "net", "ac", "gov", "or", "ne"}
    b = parts[-3] if len(parts) > 2 and parts[-2] in second else (parts[-2] if len(parts) > 1 else parts[0])
    return re.sub(r"[^a-z0-9]", "", b)


def _norm(x):
    x = unicodedata.normalize("NFD", str(x or "").lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in x if unicodedata.category(c) != "Mn"))


def traffic_points(t):
    return clamp((math.log10(t + 1) - 1) * 2.2)


def domain_trust(m, market=None, site_type=None, spam=None, host=None):
    dr, t, kw = num(m.get("dr")), num(m.get("traffic")), num(m.get("keywords"))
    if dr is None and t is None:
        return None, ["No authority or traffic data, Domain trust not scored."], {}
    flags, facts = [], {}
    major = 0
    s = 0.45 * clamp((dr or 0) / 10) + 0.55 * traffic_points(t or 0)

    if kw is not None and t is not None:
        if kw == 0 and t > 0:
            s -= 1.5
            major += 1
            flags.append("Traffic with zero ranking keywords. The traffic figure is unreliable.")
        elif kw > 0:
            tpk = t / kw
            facts["traffic_per_keyword"] = round(tpk, 1)
            if tpk > 100:
                s -= 2
                major += 1
                flags.append(f"{tpk:.0f} visits per keyword. Matches the 'inflated premium site' pattern.")
            elif tpk > 40:
                s -= 0.75
                flags.append(f"{tpk:.0f} visits per keyword, on the high side.")

    if (dr or 0) >= 40 and t is not None and t < 500:
        s -= 1.5
        major += 1
        flags.append(f"DR {dr:.0f} with only {t:.0f} monthly visits. Authority without an audience.")

    out_d, in_d = num(m.get("linked_domains_dofollow")), num(m.get("refdomains_dofollow"))
    if out_d is not None and in_d:
        ratio = out_d / in_d
        facts["out_in_ratio"] = round(ratio, 2)
        link_heavy = (site_type or "").lower() in LINK_HEAVY_TYPES
        if link_heavy:
            # News sites cite sources and directories exist to link out: only flag extreme ratios.
            if ratio > 5:
                major += 1
                s -= 2
                flags.append(f"Links out to {ratio:.1f}x more domains than link in. High even for a {site_type} site.")
        elif ratio > 1.5:
            s -= 2
            major += 1
            flags.append(f"Links out to {ratio:.1f}x more domains than link in. Typical link seller pattern.")
        elif ratio > 0.8:
            s -= 0.75
            flags.append(f"Outbound dofollow domains close to referring domains ({ratio:.2f}x).")

    hist = [num(x) for x in (m.get("traffic_history") or []) if num(x) is not None]
    if len(hist) >= 6:
        first, last = sum(hist[:3]) / 3, sum(hist[-3:]) / 3
        if first > 50:
            change = round((last - first) / first * 100)
            facts["traffic_change_pct"] = change
            if change <= -60:
                s -= 2.5
                major += 1
                flags.append(f"Organic traffic down {-change}% over the period. Possibly hit by an update.")
            elif change <= -30:
                s -= 1
                flags.append(f"Organic traffic down {-change}% over the period.")
            elif change >= 30:
                s += 0.5
                flags.append(f"Organic traffic up {change}% over the period. A growing site.")
        med = sorted(hist)[len(hist) // 2]
        if med > 50 and max(hist) > med * 4:
            s -= 0.5
            flags.append("Sharp traffic spike in the period. Check what caused it.")

    if market and market.lower() == "uk":
        market = "gb"
    if market and t:
        top = m.get("top_countries") or []
        hit = next((c for c in top if str(c[0]).lower() == market.lower()), None)
        share = (num(hit[1]) or 0) / t if hit else 0
        if share < 0.2:
            s -= 1
            flags.append(f"Only {share*100:.0f}% of traffic from {market.upper()}." if hit
                         else f"{market.upper()} is not among the top traffic countries.")

    base = clamp(s)
    watch = []
    if spam:
        def is_do(key):
            v = num(spam.get(key))
            return v is not None and v >= 0.5
        lvl = str(spam.get("inbound_spam") or "none").lower()
        if spam.get("adult_pharma"):
            if is_do("adult_pharma_dofollow_share"):
                major += 1
                s -= 2
                flags.append("Adult or pharma anchors point at the site, mostly dofollow.")
            else:
                watch.append("Adult or pharma anchors point at the site, but mostly nofollow.")
        if lvl in ("heavy", "light"):
            if is_do("inbound_spam_dofollow_share"):
                if lvl == "heavy":
                    major += 1
                    s -= 2
                else:
                    s -= 0.75
                flags.append(f"{'Heavy' if lvl == 'heavy' else 'Some'} dofollow spam in the inbound anchor cloud.")
            else:
                watch.append(f"{'Heavy' if lvl == 'heavy' else 'Some'} spam in the inbound anchor cloud, but mostly nofollow. Not passing value today, so watch it over time.")
        rows = []
        for a in spam.get("inbound_anchors") or []:
            if isinstance(a, (list, tuple)):
                d, tot = num(a[1]) if len(a) > 1 else None, num(a[2]) if len(a) > 2 else None
                rows.append((a[0], None if d is None or not tot else d / tot))
            else:
                rows.append((a, None))
        gib = [a for a, _ in rows if is_gibberish(a)]
        gib_do = [a for a, share in rows if is_gibberish(a) and share is not None and share >= 0.5]
        if len(gib_do) >= 3:
            s -= 1
            facts["random_anchors"] = gib_do[:8]
            flags.append(f"{len(gib_do)} random or numbered dofollow anchors that make no sense ({', '.join(gib_do[:3])}).")
        elif len(gib) >= 3:
            watch.append(f"{len(gib)} random or numbered anchors, mostly nofollow ({', '.join(gib[:3])}).")
        if spam.get("outbound_spam"):
            if is_do("outbound_spam_dofollow_share"):
                major += 1
                s -= 2
                flags.append("Links out with dofollow spam anchors unrelated to its topic. Points to hacked pages, spam user profiles or link selling.")
            else:
                watch.append("Links out with spam anchors unrelated to its topic, but mostly nofollow.")
        ots = num(spam.get("off_topic_share"))
        if ots is not None:
            if ots > 0.5:
                major += 1
                s -= 1.5
                flags.append(f"About {ots*100:.0f}% of its top keyword traffic is off-topic. Booster or parasite traffic.")
            elif ots > 0.25:
                watch.append(f"About {ots*100:.0f}% of its top keyword traffic is off-topic.")
        kws = spam.get("keywords") or []
        tok = brand_token(host)
        tot = sum(num(k[1]) or 0 for k in kws if isinstance(k, (list, tuple)) and len(k) > 1)
        if tot and len(tok) >= 4:
            brand = sum(num(k[1]) or 0 for k in kws if isinstance(k, (list, tuple)) and len(k) > 1 and tok in _norm(k[0]))
            share = brand / tot
            facts["own_name_traffic_share"] = round(share, 2)
            if share > 0.6 and (t or 0) >= 1000 and not spam.get("known_brand"):
                major += 1
                s -= 1.5
                flags.append(f"{share*100:.0f}% of its top keyword traffic comes from searches for its own name. Suspicious for a site without a well-known brand.")

    tf, cf = num(m.get("tf")), num(m.get("cf"))
    if tf is not None and cf:
        if tf / cf < 0.4:
            s -= 1
            flags.append(f"Majestic TF/CF {tf/cf:.2f}. Link volume over link quality.")
        elif tf >= 25:
            s += 0.5

    s = clamp(s)
    if major >= 2:
        s = min(s, 2.0)
        facts["major_red_flags"] = major
    facts["trust_before_spam"] = round(base, 1)
    facts["watch"] = watch
    return round(s, 1), flags, facts


def measured_placement(p):
    if not p.get("found"):
        return 0.0, "Link to the target not found on the page."
    zone = (p.get("zone") or "body").lower()
    s = ZONE_BASE.get(zone, 5)
    bits = ["in the article body" if zone == "body" else f"in the {zone}"]
    pos = num(p.get("position"))
    if zone == "body" and pos is not None:
        if pos <= 0.33:
            s += 1
            bits.append("early in the text")
        elif pos > 0.8:
            s -= 1
            bits.append("near the end")
    rel = (p.get("rel") or "").lower()
    if "nofollow" in rel or "ugc" in rel:
        s -= 3
        bits.append(f"rel {rel}")
    elif "sponsored" in rel:
        s -= 2
        bits.append("rel sponsored")
    else:
        bits.append("dofollow")
    ob = num(p.get("outbound_domains"))
    if ob is not None and ob > 15:
        s -= 1.5
        bits.append(f"{ob:.0f} outbound domains in the content")
    s = clamp(s)
    ctx = num(p.get("context_score"))
    if ctx is not None:
        s = 0.7 * s + 0.3 * clamp(ctx)
    return round(s, 1), "Link " + ", ".join(bits) + "."


def score(item):
    mode = item.get("mode", "prospect")
    base_w = DEFAULT_WEIGHTS_LIVE if mode == "live" else DEFAULT_WEIGHTS_PROSPECT
    w = {**base_w, **(item.get("weights") or {})}
    th = {**DEFAULT_THRESHOLDS, **(item.get("thresholds") or {})}
    js = item.get("scores") or {}
    out = {"publisher": item.get("publisher"), "target": item.get("target"), "mode": mode}

    trust, flags, facts = domain_trust(item.get("metrics") or {}, item.get("market"), item.get("site_type"),
                                      item.get("spam"), item.get("publisher"))
    out["trust_flags"], out["facts"] = flags, facts

    rel = num(js.get("relevance"))
    anchor = num(js.get("anchor_fit"))
    rel_combined = None if rel is None else (0.85 * rel + 0.15 * anchor if anchor is not None else rel)

    placement_reason = None
    if mode == "live" and item.get("placement") is not None:
        place, placement_reason = measured_placement(item["placement"])
    else:
        place = num(js.get("placement"))
    content = num(js.get("content"))

    pillars = {"relevance": rel_combined, "trust": trust, "placement": place, "content": content}
    scored = {k: v for k, v in pillars.items() if v is not None}
    total_w = sum(w[k] for k in scored)
    impact = round(sum(w[k] * v for k, v in scored.items()) / total_w * 10) if total_w else None

    if impact is None:
        verdict = "Not enough data"
    elif impact >= th["build"]:
        verdict = "Build"
    elif impact >= th["negotiate"]:
        verdict = "Negotiate"
    else:
        verdict = "Skip"
    override = None
    if rel is not None and rel <= th["relevance_floor"] and verdict not in ("Skip", "Not enough data"):
        verdict, override = "Skip", f"Relevance {rel:g}/10 is at or below the floor of {th['relevance_floor']:g}."
    if (verdict == "Skip" and override is None and facts.get("major_red_flags", 0) == 0
            and (rel or 0) >= 7 and (facts.get("trust_before_spam") or 0) >= 7):
        verdict, override = "Negotiate", "Relevance and metric quality are both 7 or higher with no hard red flags, so this stays at Negotiate."
    if facts.get("major_red_flags", 0) >= 2:
        verdict, override = "Skip", f"Fails {facts['major_red_flags']} major trust checks. Two is the walk-away line."
    if mode == "live" and item.get("placement") is not None and not item["placement"].get("found"):
        verdict, override = "Not found", "The link is not on the page."

    out.update({
        "impact_score": impact,
        "verdict": verdict,
        "override": override,
        "partial_data": len(scored) < 4,
        "watch": facts.get("watch", []),
        "pillars": {k: (round(v, 1) if v is not None else None) for k, v in pillars.items()},
        "placement_reason": placement_reason,
        "weights_used": w,
    })
    return out


def table(results):
    rows = ["| Publisher | Verdict | Score | Relevance | Trust | Placement | Content | Main flag |",
            "|---|---|---|---|---|---|---|---|"]
    fmt = lambda v: "–" if v is None else f"{v:g}"
    for r in sorted(results, key=lambda x: -(x["impact_score"] or -1)):
        p = r["pillars"]
        neg = [f for f in r["trust_flags"] if "A growing site" not in f]
        flag = r["override"] or (neg[0] if neg else "")
        rows.append(f"| {r['publisher']} | {r['verdict']} | {fmt(r['impact_score'])} | {fmt(p['relevance'])} | "
                    f"{fmt(p['trust'])} | {fmt(p['placement'])} | {fmt(p['content'])} | {flag} |")
    return "\n".join(rows)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = sys.stdin.read() if sys.argv[1] == "-" else open(sys.argv[1], encoding="utf-8").read()
    data = json.loads(src)
    items = data if isinstance(data, list) else [data]
    results = [score(i) for i in items]
    print(json.dumps(results if isinstance(data, list) else results[0], indent=2, ensure_ascii=False))
    if "--table" in sys.argv:
        print()
        print(table(results))


if __name__ == "__main__":
    main()
