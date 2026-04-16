# Cloudflare Protection for Sierra ILS — Practical Guide for Library Sys Admins

From the IUG 2026 Sys Admin Forum discussion and follow-up research. This covers
putting Sierra's web OPAC behind Cloudflare: what works, what breaks, and what to
watch out for.

---

## Table of Contents

1. [Why This Matters Now](#why-this-matters-now)
2. [Architecture Overview](#architecture-overview)
3. [DNS and SSL/TLS Setup](#dns-and-ssltls-setup)
4. [Cloudflare WAF Rules for Sierra](#cloudflare-waf-rules-for-sierra)
5. [Bot Management](#bot-management)
6. [Caching Strategy](#caching-strategy)
7. [Rate Limiting](#rate-limiting)
8. [Page Rules and Transform Rules](#page-rules-and-transform-rules)
9. [Known Issues and Gotchas](#known-issues-and-gotchas)
10. [Free vs. Paid Tiers](#free-vs-paid-tiers)
11. [Comparison: Cloudflare vs. F5/fail2ban](#comparison-cloudflare-vs-f5fail2ban)
12. [Alternative: Anubis (Proof of Work)](#alternative-anubis-proof-of-work)
13. [Practical Recommendations](#practical-recommendations)
14. [Sources and Further Reading](#sources-and-further-reading)

---

## Why This Matters Now

AI bot scraping became a serious problem for libraries starting in late 2024. The
scale is unprecedented:

- **Biodiversity Heritage Library** saw traffic spike to 10x normal levels,
  periodically making the site inaccessible. Bots were loading pages as a human
  would (using real browser user-agents), making them hard to distinguish. Traffic
  came from distributed IPs worldwide, defeating simple IP-based blocking.
- **UNC Chapel Hill** library catalog was "receiving so much traffic that it was
  periodically shutting out students, faculty, and staff."
- **Project Gutenberg** and **OAPEN** both had outages directly caused by AI
  scraper bots.
- **ByWater Solutions** (hosting provider for Koha and Aspen Discovery) responded
  by deploying Cloudflare across all hosted customers — 95% of Aspen and 60% of
  Koha libraries as of mid-2025.
- **Open Fifth** (UK Koha hosting) reported some sites receiving over 1 million
  requests per week, with only a few thousand being genuine.
- **Duke University** rolled out Anubis (proof-of-work challenge) in June 2025.

The common pattern: bots don't identify themselves as GPTBot/GoogleBot/BingBot,
they ignore robots.txt, they use residential proxies, and they crawl at rates that
overwhelm library infrastructure not designed for that load.

**Bottom line:** Any library running a public-facing OPAC or catalog is a target.
Sierra WebPAC is no exception.

---

## Architecture Overview

### What Cloudflare Does

Cloudflare acts as a reverse proxy. All HTTP/HTTPS traffic to your OPAC domain
flows through Cloudflare's network before reaching your Sierra server. This gives
Cloudflare the ability to:

- Filter malicious requests (WAF)
- Challenge suspected bots
- Cache static content (reducing load on Sierra)
- Absorb DDoS attacks
- Provide analytics on traffic patterns
- Block AI scrapers

### What Cloudflare Does NOT Protect

Cloudflare's standard proxy only handles **HTTP/HTTPS** traffic on specific ports.
It does **not** protect:

- **Z39.50** (port 210) — non-HTTP protocol, passes through DNS-only
- **SIP2** (port 6001 typically) — non-HTTP protocol, passes through DNS-only
- **Sierra API** on non-standard ports — only if on a supported port
- **MARC file downloads** — these work through HTTP but may be affected by JS
  challenges (see Known Issues)

Cloudflare-supported HTTP ports: 80, 8080, 8880, 2052, 2082, 2086, 2095
Cloudflare-supported HTTPS ports: 443, 2053, 2083, 2087, 2096, 8443

**Note:** Sierra's WebPAC staging server runs on port 2082, which happens to be a
Cloudflare-supported HTTP port. The live WebPAC typically runs on port 80/443.

For non-HTTP protocols on arbitrary ports, **Cloudflare Spectrum** (Enterprise only)
can proxy TCP/UDP traffic. This is the only way to protect Z39.50 or SIP2 through
Cloudflare — and it requires an Enterprise plan.

### Sierra Deployment Models

Your setup depends on how Sierra is hosted:

| Deployment | Cloudflare Setup |
|---|---|
| **Self-hosted / on-premise** | Full control — point DNS to Cloudflare, configure as needed |
| **III cloud-hosted** | May need to coordinate with III — you may not control DNS or the web server directly |
| **Vega Discover** (SaaS) | Likely already behind III's own CDN/WAF — limited customization |

---

## DNS and SSL/TLS Setup

### Step 1: Move DNS to Cloudflare

1. Create a Cloudflare account and add your OPAC domain
2. Cloudflare will scan existing DNS records
3. Update your domain's nameservers to Cloudflare's assigned nameservers
4. Set your Sierra OPAC's A/AAAA/CNAME record to **Proxied** (orange cloud) —
   this routes traffic through Cloudflare

**Critical:** Only proxy the web OPAC record. Leave other records as DNS-only
(gray cloud) for:
- Z39.50 hostname (if separate)
- SIP2 hostname (if separate)
- Mail (MX) records
- Any non-HTTP services

### Step 2: SSL/TLS Configuration

Set encryption mode to **Full (Strict)**. This encrypts traffic both:
- Browser <-> Cloudflare (Cloudflare's free universal SSL cert)
- Cloudflare <-> your Sierra origin server (requires a valid cert on origin)

**For the origin certificate, you have two options:**

1. **Cloudflare Origin CA certificate** (free, 15-year validity) — only trusted
   by Cloudflare, so only works when traffic comes through Cloudflare
2. **Standard CA certificate** (e.g., Let's Encrypt) — works whether or not
   traffic routes through Cloudflare

Recommendation: Use a Cloudflare Origin CA cert if you're committed to keeping all
traffic through Cloudflare. Use Let's Encrypt if you want flexibility to bypass
Cloudflare temporarily for troubleshooting.

**Never use "Flexible" SSL mode** — this leaves the Cloudflare-to-origin connection
unencrypted, which is a security risk, especially for patron login traffic.

### Step 3: Restore Real Visitor IPs

When Sierra sits behind Cloudflare, all requests appear to come from Cloudflare's
IP addresses. You need to restore the real visitor IP for:
- Sierra's session management (which can fall back to IP-based sessions)
- Access logs and security monitoring
- Any IP-based access controls

Cloudflare sends the real IP in the `CF-Connecting-IP` header and also appends to
`X-Forwarded-For`. Configure your web server (Apache/Nginx in front of Sierra) to
trust these headers from Cloudflare's IP ranges.

---

## Cloudflare WAF Rules for Sierra

### Sierra WebPAC URL Patterns to Know

Before writing rules, understand Sierra's URL structure:

| Path Pattern | Function | Sensitivity |
|---|---|---|
| `/` | Main menu, resets session | Public |
| `/search/...` | Catalog search (by index) | Public, high traffic |
| `/patroninfo/...` | Patron account (My Account) | **Authenticated — protect** |
| `/record/...` | Individual bib/item records | Public |
| `/xrecord/...` | XML record export | Public but abusable |
| `/iii/sierra-api/...` | REST API (v5/v6) | **Authenticated — protect** |
| `/screens/...` | WebPAC template files | Static assets |

### Recommended Custom WAF Rules

**Rule 1: Challenge non-browser traffic to patron login**
```
Expression: (http.request.uri.path contains "/patroninfo" and not cf.bot_management.verified_bot)
Action: Managed Challenge
```

**Rule 2: Block direct access to API from non-allowlisted IPs**
```
Expression: (http.request.uri.path contains "/iii/sierra-api" and not ip.src in {YOUR_TRUSTED_IPS})
Action: Block
```

**Rule 3: Challenge suspicious user agents on search pages**
```
Expression: (http.request.uri.path contains "/search" and
  (http.user_agent contains "python" or
   http.user_agent contains "curl" or
   http.user_agent contains "wget" or
   http.user_agent contains "scrapy") and
  not cf.bot_management.verified_bot)
Action: Block
```

**Rule 4: Block XML record bulk harvesting (unless from known partners)**
```
Expression: (http.request.uri.path contains "/xrecord" and not ip.src in {OCLC_IPS DISCOVERY_IPS})
Action: Managed Challenge
```

### Managed Rulesets

Enable these (available on all plans at varying levels):

- **Cloudflare Free Managed Ruleset** — basic protection against high-profile
  CVEs, SQLi, XSS (all plans)
- **Cloudflare OWASP Core Ruleset** — broader SQLi/XSS/command injection
  protection (Pro plan and above)
- **Cloudflare Managed Ruleset** — Cloudflare's proprietary rules (Pro+)

---

## Bot Management

### Tier Comparison for Bot Protection

| Feature | Free | Pro ($20/mo) | Business ($200/mo) | Enterprise |
|---|---|---|---|---|
| Bot Fight Mode | Basic | -- | -- | -- |
| Super Bot Fight Mode | -- | Yes | Yes | -- |
| Bot Management (full) | -- | -- | -- | Yes |
| Verified bot allowlist | -- | Yes | Yes | Yes |
| Bot score analytics | -- | Yes | Yes | Yes |
| AI Scrapers one-click block | Yes | Yes | Yes | Yes |

### AI Scraper Blocking (All Plans)

Navigate to **Security > Bots** and enable "AI Scrapers and Crawlers" toggle. This
blocks known AI crawlers (GPTBot, CCBot, etc.) and is updated by Cloudflare as new
bot signatures are identified. **Available on all plans including free.**

As of July 2025, Cloudflare blocks AI crawlers by default for new zones.

### Verified Bots — The Library-Specific Challenge

Cloudflare maintains a [verified bots directory](https://radar.cloudflare.com/bots/directory)
of known good bots (Googlebot, Bingbot, etc.) verified via reverse DNS. The concern
for libraries is that **library-specific bots are generally NOT on this list**:

| Service | Bot Behavior | On Cloudflare Verified List? | Mitigation |
|---|---|---|---|
| **Googlebot** | Crawls OPAC for search indexing | Yes | Auto-allowed |
| **Bingbot** | Same | Yes | Auto-allowed |
| **OCLC WorldCat harvesting** | Harvests MARC records | Unlikely | Allowlist by IP |
| **EBSCO EDS connector** | Queries OPAC for discovery | No | Allowlist by IP |
| **Ex Libris Primo/Summon** | Queries OPAC for discovery | No | Allowlist by IP |
| **EZproxy** | Proxies patron requests | No | **Allowlist by IP** |
| **Link resolvers** (SFX, 360 Link) | Checks availability | No | Allowlist by IP |
| **Google Scholar** | Crawls for academic citations | Check verified list | Usually verified |

**Critical: EZproxy + Cloudflare**

OCLC explicitly documents this: "You can use Cloudflare with EZproxy. Make sure you
list your on-campus IP addresses, EZproxy Server IP address, and EZproxy name with
Cloudflare." If you don't allowlist your EZproxy server IP, Cloudflare will
challenge EZproxy traffic and potentially block patron access to the catalog from
off-campus.

Create a WAF rule:
```
Expression: (ip.src in {EZPROXY_IP ON_CAMPUS_RANGES OCLC_IPS DISCOVERY_LAYER_IPS})
Action: Skip (all remaining rules)
```
Place this rule **first** in your rule order so trusted traffic bypasses all
challenges.

### Super Bot Fight Mode (Pro+) Configuration

Recommended settings for a library OPAC:
- **Definitely automated:** Challenge
- **Likely automated:** Challenge
- **Verified bots:** Allow
- **Static resource protection:** On (protects images, CSS, JS)
- **JavaScript detections:** On

---

## Caching Strategy

### What to Cache

Sierra serves a mix of public catalog pages and authenticated patron content. The
caching strategy must be careful:

| Content Type | Cache? | Notes |
|---|---|---|
| Static assets (CSS, JS, images) | **Yes** | Long TTL (1 day+) |
| `/screens/...` template files | **Yes** | WebPAC templates |
| Catalog search results `/search/...` | **Maybe** | Short TTL (5 min) if desired, but dynamic content — test carefully |
| Individual bib records `/record/...` | **Maybe** | Short TTL, but patron-specific elements may appear |
| `/patroninfo/...` | **NEVER** | Authenticated patron data |
| `/iii/sierra-api/...` | **NEVER** | API responses with patron PII |
| MARC downloads | **No** | Dynamic, binary content |

### Cache Rules Configuration

**Rule 1: Bypass cache for authenticated paths**
```
Match: URI path contains "/patroninfo" OR URI path contains "/sierra-api"
Setting: Bypass Cache
```

**Rule 2: Bypass cache when session cookie present**
```
Match: Cookie contains "III_SESSION" (or your Sierra session cookie name)
Setting: Bypass Cache
```
Note: "Bypass Cache on Cookie" requires a **Business plan** or a Cloudflare Worker
on lower plans.

**Rule 3: Cache static assets aggressively**
```
Match: URI path contains "/screens/" OR file extension in {css js png jpg gif ico svg woff woff2}
Setting: Cache Everything, Edge TTL 1 day, Browser TTL 4 hours
```

### Default Behavior

By default, Cloudflare only caches static file extensions (images, CSS, JS, fonts).
It does **not** cache HTML pages unless you explicitly tell it to. This is actually
a safe default for Sierra — it means patron pages won't be accidentally cached.

---

## Rate Limiting

### Sensible Defaults for a Library OPAC

Rate limiting rules are available on all plans (IP-based). Advanced grouping by
cookie/header/ASN requires Business+.

**Rule 1: Protect patron login**
```
Expression: (http.request.uri.path contains "/patroninfo" and http.request.method eq "POST")
Characteristics: IP
Period: 1 minute
Requests: 5
Action: Managed Challenge
Duration: 15 minutes
```
This mirrors Cloudflare's built-in "Protect My Login" pattern: 5 attempts per
minute, then challenge for 15 minutes.

**Rule 2: Rate limit catalog searches**
```
Expression: (http.request.uri.path contains "/search")
Characteristics: IP
Period: 1 minute
Requests: 30
Action: Managed Challenge
Duration: 10 minutes
```
A human doing catalog searches will rarely exceed 30 per minute. A scraper will
hit this quickly.

**Rule 3: Rate limit API requests (if API is exposed)**
```
Expression: (http.request.uri.path contains "/iii/sierra-api")
Characteristics: IP
Period: 1 minute
Requests: 60
Action: Block
Duration: 10 minutes
```

**Rule 4: Global rate limit (DDoS backstop)**
```
Expression: (http.request.uri.path ne "/")
Characteristics: IP
Period: 10 seconds
Requests: 50
Action: Managed Challenge
Duration: 10 minutes
```
Any single IP making 50+ requests in 10 seconds is almost certainly not a human.

**Important:** Rate limiting counters may have a delay of a few seconds. Don't
rely on rate limiting for precise request counts — it's a backstop, not a
metering system.

---

## Page Rules and Transform Rules

Cloudflare is migrating from legacy Page Rules to the newer Rules products (Cache
Rules, Configuration Rules, Transform Rules, Origin Rules, Redirect Rules). Use the
new system if available.

### Useful Rules for Sierra

**Security Level for patron pages** (Configuration Rule):
```
Match: URI path contains "/patroninfo"
Setting: Security Level = High
```
This sets a higher threshold for challenges on authenticated pages.

**Force HTTPS** (Redirect Rule):
```
Match: scheme eq "http"
Action: Redirect to HTTPS (301)
```
All OPAC traffic should be HTTPS, especially patron login.

**Custom error pages** (Configuration Rule):
Present a library-branded error page instead of Cloudflare's generic challenge
page. This reduces patron confusion when they encounter a bot challenge.

**Disable apps/features on API paths** (Configuration Rule):
```
Match: URI path contains "/iii/sierra-api"
Settings: Disable Performance, Disable Apps, Disable Minification
```
API responses should not be modified by Cloudflare's optimization features.

---

## Known Issues and Gotchas

### 1. Session Cookie Handling

Sierra WebPAC uses cookies for session management, falling back to IP-based
sessions if cookies aren't available. Behind Cloudflare:

- **Cloudflare adds its own cookies** (`__cflb` for load balancing, `__cf_bm` for
  bot management, `cf_clearance` for challenge bypass). These should not conflict
  with Sierra's session cookies but increase cookie header size.
- **If you're using Cloudflare + F5**: F5 BIG-IP sets a session cookie at the
  beginning of a TCP connection and then ignores cookies on subsequent requests on
  the same TCP connection. Cloudflare multiplexes HTTP sessions over single TCP
  connections, which **breaks F5 session affinity**. This is a documented
  incompatibility.

### 2. Z39.50 Traffic (Port 210)

Cloudflare's proxy **cannot handle Z39.50**. It's not HTTP. Options:
- Use a separate DNS record (gray-clouded / DNS-only) for Z39.50
- Use Cloudflare Spectrum (Enterprise only) for TCP proxy
- Accept that Z39.50 traffic bypasses Cloudflare protection

### 3. SIP2 Traffic (Typically Port 6001)

Same situation as Z39.50 — SIP2 is a raw TCP protocol. Self-checkout machines,
automated materials handling, and other SIP2 clients must connect to a DNS-only
record or directly to the server IP.

### 4. Sierra REST API

The Sierra API (v5/v6) runs over HTTPS, so it *can* go through Cloudflare. However:
- **Disable Cloudflare's minification and optimization** for API paths (it can
  corrupt JSON responses)
- **Disable Rocket Loader** (Cloudflare's JS optimization) on API paths
- **Watch for `X-Forwarded-For` issues** — if your API implementation uses client
  IP for anything, ensure you're reading `CF-Connecting-IP`
- **Rate limiting on the API** must account for your own automated processes
  (cronjobs pulling data, middleware polling, etc.)

### 5. MARC Record Downloads

MARC downloads from the OPAC (`.mrc` binary files) should work through Cloudflare,
but:
- Ensure Cloudflare's JavaScript challenge isn't triggered for these paths — MARC
  download clients (MarcEdit, automated scripts) typically can't solve JS
  challenges
- Consider a skip rule for known MARC harvesting IPs
- Binary content types pass through Cloudflare fine, but non-browser clients
  will fail challenges

### 6. JavaScript Challenges and Non-Browser Clients

Cloudflare's Managed Challenges and JS Challenges require a browser environment to
solve. Any service that accesses your OPAC without a full browser will fail:
- Link resolvers checking holdings
- Discovery layer connectors
- MARC harvesters
- Screen scrapers used for ILL
- Automated monitoring tools

**You must allowlist these services by IP** before enabling aggressive bot
protection.

### 7. WebPAC Staging Server (Port 2082)

Sierra's staging WebPAC runs on port 2082. This is a Cloudflare-supported HTTP
port, so it *could* be proxied. However, you probably want to keep staging
access restricted — either leave it DNS-only or add a WAF rule blocking external
access to port 2082.

### 8. Encore/Vega Compatibility

If you're running Encore or Vega Discover in addition to WebPAC:
- **Encore** makes heavy AJAX calls — test thoroughly that Cloudflare's
  optimization features (Rocket Loader, Auto Minify) don't break JavaScript
- **Vega** is III's cloud SaaS product — you likely can't put it behind your
  own Cloudflare instance since III controls the infrastructure

---

## Free vs. Paid Tiers

### What Matters for a Library Protecting Sierra

| Feature | Free | Pro ($20/mo) | Business ($200/mo) | Enterprise (custom) |
|---|---|---|---|---|
| DDoS protection | Unmetered | Unmetered | Unmetered | Unmetered |
| SSL/TLS (Universal) | Yes | Yes | Yes | Yes |
| AI Scraper blocking (1-click) | Yes | Yes | Yes | Yes |
| Bot Fight Mode | Basic | Super Bot Fight Mode | Super Bot Fight Mode | Full Bot Management |
| WAF custom rules | 5 | 20 | 100 | 1000 |
| WAF managed rules (free ruleset) | Yes | Yes | Yes | Yes |
| OWASP Core Ruleset | No | Yes | Yes | Yes |
| Rate limiting (IP-based) | Yes | Yes | Yes | Yes |
| Rate limiting (advanced grouping) | No | No | Yes | Yes |
| Bypass cache on cookie | No | No | Yes | Yes |
| Custom error pages | No | No | Yes | Yes |
| Spectrum (non-HTTP proxy) | No | No | No | Yes |
| Bot score analytics | No | Yes | Yes | Yes |

### Recommendation by Library Size

- **Small public library, limited budget:** Free tier gives you DDoS protection,
  basic bot fighting, AI scraper blocking, 5 WAF rules, and rate limiting. This
  is already a massive improvement over no protection.

- **Medium library or academic library:** Pro ($20/mo) adds OWASP rules, 20 WAF
  rules, Super Bot Fight Mode with verified bot allowlisting, and bot analytics.
  Best value for most Sierra installations.

- **Large academic or consortium:** Business ($200/mo) adds bypass-cache-on-cookie
  (important for patron sessions), 100 WAF rules, advanced rate limiting, and
  custom error pages.

- **Major research library:** Enterprise if you need Spectrum for Z39.50/SIP2
  protection or full Bot Management with bot score granularity.

### Project Galileo

Cloudflare's [Project Galileo](https://www.cloudflare.com/galileo/) provides
**Business-tier features for free** to qualifying organizations facing cyber
threats. It's designed for journalism, human rights, and civil society groups.
Public libraries *may* qualify depending on circumstances — worth applying if your
library has been targeted by attacks. Participants get Bot Management and AI Crawl
Control at no cost.

---

## Comparison: Cloudflare vs. F5/fail2ban

This was discussed at the IUG 2026 Sys Admin Forum. Jeff reported his library uses
F5 with fail2ban and has "had good luck." Here's how the approaches compare:

| Aspect | Cloudflare | F5 + fail2ban |
|---|---|---|
| **Cost** | Free tier available; Pro $20/mo | F5 hardware: $10K–$100K+; fail2ban: free |
| **Setup complexity** | DNS change + dashboard config | Network appliance + Linux server + custom filters |
| **DDoS protection** | Absorbs at edge (Cloudflare network) | Limited to your bandwidth/hardware |
| **Bot intelligence** | Global threat data, ML models, verified bot list | Pattern matching on your logs only |
| **AI scraper blocking** | One-click, continuously updated signatures | Manual rules, you maintain signatures |
| **Rate limiting** | Built-in, configurable per path | Custom fail2ban jails per log pattern |
| **WAF rules** | Managed rulesets + custom rules | F5 ASM (separate license) or manual |
| **Handles distributed bots** | Yes (global anycast network) | Poorly (each IP seen briefly, jail never triggers) |
| **Non-HTTP protocols** | No (unless Enterprise Spectrum) | Yes (F5 handles any TCP/UDP) |
| **Latency** | Adds ~1-5ms (edge PoP nearby) | Depends on network topology |
| **Maintenance** | Cloudflare updates rules/signatures | You maintain fail2ban filters and F5 configs |
| **Fail2ban + Cloudflare** | Can combine: fail2ban triggers Cloudflare API to block IPs at edge | N/A |

### Key Advantage of Cloudflare for the Current Threat

The AI bot problem is **distributed** — bots use thousands of residential proxy IPs,
each making only a few requests. fail2ban's strength is banning IPs that show
repeated bad behavior, but if each IP only makes 5 requests before rotating, the
jail threshold is never reached.

Cloudflare's ML-based bot detection looks at behavioral signals beyond IP: TLS
fingerprint, HTTP/2 settings, mouse movement patterns, JavaScript execution
behavior. This catches distributed bots that fail2ban misses.

### Can You Combine Them?

Yes. fail2ban can call the Cloudflare API to push blocks to the Cloudflare edge.
This gives you defense-in-depth:
1. Cloudflare catches known bots and AI scrapers at the edge
2. fail2ban monitors Sierra's logs for patterns that slip through
3. fail2ban pushes offending IPs to Cloudflare's blocklist via API

The Cloudflare API for fail2ban is documented but has had compatibility issues
(check the [Cloudflare Community thread](https://community.cloudflare.com/t/does-cloudflares-fail2ban-action-still-work/640904)
for current status).

---

## Alternative: Anubis (Proof of Work)

[Anubis](https://github.com/TecharoHQ/anubis) is an open-source reverse proxy that
presents a proof-of-work JavaScript challenge before allowing access. It's being
adopted by libraries as a Cloudflare alternative or complement:

- **Duke University** deployed Anubis in June 2025
- **Open Fifth** uses Anubis for Koha instances where they don't control DNS
  (Cloudflare requires DNS control)
- **BHL** used Cloudflare + other mitigations

**How it works:** Anubis sits in front of your web server. First-time visitors get a
small JS challenge (SHA-256 proof of work, ~2 seconds in a browser). Bots running
with minimal compute resources can't solve it economically at scale.

**Pros:**
- Free and open source
- Self-hosted, no third-party dependency
- Works when you don't control DNS
- Being considered as a Koha plugin/default option

**Cons:**
- Requires JavaScript — breaks all non-browser clients
- Adds friction for legitimate patrons (brief delay on first visit)
- Skeptics argue the compute cost for bots is negligible at scale
- Doesn't provide DDoS protection, caching, or WAF features

**Verdict:** Anubis is a good complement to Cloudflare for specific high-traffic
paths, or a standalone option when Cloudflare isn't feasible. It's not a full
replacement for Cloudflare's broader security suite.

---

## Practical Recommendations

### If You're Starting from Zero

1. **Sign up for Cloudflare Free** and point your OPAC DNS to Cloudflare
2. **Set SSL/TLS to Full (Strict)** with a Cloudflare Origin CA cert
3. **Enable AI Scrapers and Crawlers blocking** (one click, immediate effect)
4. **Create IP allowlist rules** for EZproxy, discovery layer, OCLC, and other
   trusted services BEFORE enabling any blocking rules
5. **Add rate limiting** on `/patroninfo` (login) and `/search` paths
6. **Keep Z39.50 and SIP2 on DNS-only records**
7. **Test thoroughly** — especially patron login, MARC downloads, discovery layer
   integration, and any automated processes that query the OPAC

### If You're Already Behind an F5

Consider adding Cloudflare in front of the F5 (Cloudflare -> F5 -> Sierra):
- Cloudflare handles DDoS and bot filtering at the edge
- F5 handles application-level load balancing and non-HTTP protocols
- **Watch for session affinity issues** between Cloudflare and F5 cookies

### The Minimum Viable Protection (15 Minutes)

For a sys admin who needs something deployed today:
1. Cloudflare Free account
2. Change DNS nameservers
3. Orange-cloud your OPAC A record
4. Enable "AI Scrapers and Crawlers" toggle
5. Done — you now have DDoS protection and AI bot blocking

Then iterate on WAF rules, rate limiting, and caching as time allows.

### Monitoring

After deploying Cloudflare:
- Check the **Security > Overview** dashboard for blocked threats
- Review **Bot Analytics** (Pro+) to understand your traffic mix
- Monitor Sierra's own logs — if you see high traffic from Cloudflare IPs,
  you may need to configure `CF-Connecting-IP` header restoration
- Set up Cloudflare notifications for DDoS attacks and rate limit triggers

---

## Sources and Further Reading

### Library-Specific

- [AI Bots Swarm Library, Cultural Heritage Sites, Causing Slowdowns and Crashes](https://www.libraryjournal.com/story/ai-bots-swarm-library-cultural-heritage-sites-causing-slowdowns-and-crashes) — Library Journal
- [BHL Battling a Barrage of Bots](https://blog.biodiversitylibrary.org/2026/04/battling-bots) — Biodiversity Heritage Library
- [BHL Traffic Challenges](https://blog.biodiversitylibrary.org/2025/07/bhl-traffic-challenges) — BHL
- [Impact of AI Bots on Library Websites](https://library.duke.edu/using/off-campus/impact-of-bots) — Duke University Libraries
- [Fighting the AI Bots](https://openfifth.co.uk/fighting-the-ai-bots/) — Open Fifth (Koha hosting)
- [Are AI Bots Knocking Cultural Heritage Offline?](https://www.glamelab.org/products/are-ai-bots-knocking-cultural-heritage-offline/) — GLAM-E Lab
- [Can I use EZproxy with Cloudflare?](https://help.oclc.org/Library_Management/EZproxy/Troubleshooting/Can_I_use_EZproxy_with_Cloudflare) — OCLC Support
- [How do I resolve issues with Cloudflare on websites with EZproxy](https://help.oclc.org/Library_Management/EZproxy/Troubleshooting/How_do_i_resolve_issues_with_Cloudflare_on_websites_with_EZproxy) — OCLC Support

### Sierra/Innovative Documentation

- [Sierra Command Links](https://documentation.iii.com/sierrahelp/Content/sril/sril_command_links.html) — III
- [WebPAC My Account FAQ](https://iii-itlc.s3.amazonaws.com/LibGuides/LibGuides+Articles+and+Docs/Sierra/WebPAC_Discovery/Articles/SYS+Sierra+HTG+My+Account+FAQ+20220301.pdf) — III
- [Sierra REST API](https://github.com/NYPL-Simplified/Simplified/wiki/Sierra-REST-API) — NYPL wiki
- [Sierra System Administration](https://innovative.libguides.com/sierra/sysadmin) — Innovative LibGuides

### Cloudflare Documentation

- [Cloudflare WAF Rate Limiting Best Practices](https://developers.cloudflare.com/waf/rate-limiting-rules/best-practices/) — Cloudflare
- [Rate Limiting Rule Examples](https://developers.cloudflare.com/waf/rate-limiting-rules/use-cases/) — Cloudflare
- [Super Bot Fight Mode](https://developers.cloudflare.com/bots/get-started/super-bot-fight-mode/) — Cloudflare
- [Block AI Bots](https://developers.cloudflare.com/bots/additional-configurations/block-ai-bots/) — Cloudflare
- [Verified Bots Directory](https://radar.cloudflare.com/bots/directory) — Cloudflare Radar
- [Allow Verified Bot Traffic](https://developers.cloudflare.com/waf/custom-rules/use-cases/allow-traffic-from-verified-bots/) — Cloudflare
- [Network Ports](https://developers.cloudflare.com/fundamentals/reference/network-ports/) — Cloudflare
- [SSL/TLS Full (Strict)](https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/full-strict/) — Cloudflare
- [Origin CA Certificates](https://developers.cloudflare.com/ssl/origin-configuration/origin-ca/) — Cloudflare
- [Cache Rules](https://developers.cloudflare.com/cache/how-to/cache-rules/) — Cloudflare
- [Custom WAF Rules](https://developers.cloudflare.com/waf/custom-rules/) — Cloudflare
- [Cloudflare Spectrum](https://developers.cloudflare.com/spectrum/) — Cloudflare
- [Project Galileo](https://www.cloudflare.com/galileo/) — Cloudflare
- [AI Crawl Control](https://www.cloudflare.com/ai-crawl-control/) — Cloudflare

### Alternative Tools

- [Anubis — Proof of Work Anti-Bot](https://github.com/TecharoHQ/anubis) — GitHub
- [fail2ban with Cloudflare](https://community.cloudflare.com/t/does-cloudflares-fail2ban-action-still-work/640904) — Cloudflare Community
- [Cloudflare + F5 Session Affinity](https://community.cloudflare.com/t/cloudflare-f5-cookie-based-session-affinity/175684) — Cloudflare Community
