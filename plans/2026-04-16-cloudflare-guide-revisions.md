# Cloudflare Sierra Guide Revisions — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Revise `cloudflare-sierra-guide.html` to address structural weaknesses identified in the revision brief — particularly around DNS strategy (zone-level commitment), Sierra's multi-protocol topology, and several factual/scoping corrections.

**Architecture:** Single-file HTML revision. The guide is a static HTML page (`iug2026-shared/docs/cloudflare-sierra-guide.html`, 1114 lines) using the site's shared `style.css`. All changes are content restructuring and additions within that file. The site uses a consistent card/section-list pattern for content blocks.

**Tech Stack:** Static HTML, CSS (existing `style.css`), GitHub Pages

---

## Context for the Implementer

**Source file:** `iug2026-shared/docs/cloudflare-sierra-guide.html`

**Revision brief:** A detailed brief from Google Drive (`cloudflare-sierra-guide-revisions.md`) identifies 5 priorities. The brief is very specific — follow its instructions closely. Key themes:

1. The guide treats moving nameservers to Cloudflare as routine. It's a whole-zone commitment that can break email, SSO, etc. Present 3 DNS strategy options and recommend partial (Option B/C) as the default.
2. Sierra is multi-protocol (Z39.50, SIP2, SDA, desktop client, etc.), not just a web app. This is the central architectural constraint and needs its own section.
3. Several factual items need correction: pricing should link to docs rather than hard-coding, rate limiting Rule 4 is too broad, F5 is a deployment blocker not a "gotcha," etc.

**Style conventions:** The site uses these HTML patterns:
- `<div class="card">` for callout boxes
- `<div class="section-list"><div class="section-item">` for grouped content
- `<h3 style="color: var(--navy); margin-bottom: 0.75rem;">` for sub-headers within sections
- `<p class="detail">` for metadata lines
- Standard `<table>` elements (no special classes)
- HTML entities: `&mdash;`, `&rsquo;`, `&ldquo;`/`&rdquo;`, `&rarr;`, `&harr;`

**Preserve:** All existing citations/source links, the practitioner-notes tone, the footer, nav, and head metadata.

**Testing:** After each task, open `cloudflare-sierra-guide.html` in a browser and verify the new/changed section renders correctly with proper formatting.

---

## Task 1: Add "Sierra's Service Topology" Section (Priority 2)

**Why first:** This new section establishes the architectural reality that shapes the DNS strategy section (Task 2). Insert it between "Architecture Overview" and "DNS and SSL/TLS Setup."

**Files:**
- Modify: `iug2026-shared/docs/cloudflare-sierra-guide.html:158-162` (between the deployment models table closing and the DNS section opening)

- [ ] **Step 1: Insert the new section after the Sierra Deployment Models table**

Find this line (around line 158-162):

```html
    <!-- DNS and SSL/TLS Setup -->

    <h2 id="dns-and-ssl-tls-setup">DNS and SSL/TLS Setup</h2>
```

Insert the following **before** that block:

```html
    <!-- Sierra's Service Topology -->

    <h2 id="sierra-service-topology">Sierra&rsquo;s Service Topology</h2>

    <div class="card">
      <p>Sierra is a multi-protocol platform, not a web app. Z39.50, SIP2, SDA, the desktop client, NCIP, and FTP-based MARC loads all share the Sierra server and often share hostnames. This is the central architectural constraint for any Cloudflare deployment: if every Sierra service resolves through a single hostname, you cannot selectively proxy anything without breaking something.</p>
    </div>

    <h3 style="color: var(--navy); margin-bottom: 0.75rem;">Services That Typically Share a Sierra Server</h3>

    <table>
      <thead>
        <tr><th>Service</th><th>Protocol</th><th>Default Port</th><th>Cloudflare-Proxyable?</th></tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>WebPAC</strong> (public catalog)</td>
          <td>HTTP/HTTPS</td>
          <td>80 / 443</td>
          <td>Yes</td>
        </tr>
        <tr>
          <td><strong>Encore / Vega</strong> (if licensed)</td>
          <td>HTTPS</td>
          <td>443</td>
          <td>Yes, with caveats (see <a href="#known-issues-and-gotchas">Known Issues</a>)</td>
        </tr>
        <tr>
          <td><strong>Sierra REST API</strong></td>
          <td>HTTPS</td>
          <td>443 or site-configured</td>
          <td>Yes, with caveats</td>
        </tr>
        <tr>
          <td><strong>Sierra Desktop App</strong> (staff client)</td>
          <td>HTTPS</td>
          <td>443</td>
          <td>Usually <strong>no</strong> &mdash; put on separate hostname</td>
        </tr>
        <tr>
          <td><strong>Sierra Direct SQL Access</strong> (SDA)</td>
          <td>TCP</td>
          <td>1032</td>
          <td>No (Enterprise Spectrum only)</td>
        </tr>
        <tr>
          <td><strong>Z39.50</strong></td>
          <td>TCP</td>
          <td>210</td>
          <td>No (Enterprise Spectrum only)</td>
        </tr>
        <tr>
          <td><strong>SIP2</strong> (self-check, AMH, etc.)</td>
          <td>TCP</td>
          <td>6001 (site-configurable)</td>
          <td>No (Enterprise Spectrum only)</td>
        </tr>
        <tr>
          <td><strong>NCIP</strong> (if used)</td>
          <td>HTTP</td>
          <td>varies</td>
          <td>Sometimes</td>
        </tr>
        <tr>
          <td><strong>FTP for MARC loads</strong></td>
          <td>FTP/SFTP</td>
          <td>21 / 22</td>
          <td>No</td>
        </tr>
        <tr>
          <td><strong>SSH for admin</strong></td>
          <td>TCP</td>
          <td>22</td>
          <td>No</td>
        </tr>
      </tbody>
    </table>

    <p style="margin-top: 0.75rem;"><em>This list is typical, not universal. SIP2 port in particular is commonly changed per-site, and III cloud-hosted customers may have different defaults.</em></p>

    <h3 style="color: var(--navy); margin-bottom: 0.75rem;">Key Recommendation: Separate Your Hostnames</h3>

    <div class="card">
      <p><strong>Put the public OPAC on its own hostname.</strong> Do not proxy a hostname that is also serving the Sierra Desktop App, SDA, or any non-HTTP protocol.</p>
    </div>

    <div class="section-list">
      <div class="section-item">
        <h3>Example hostname split</h3>
        <ul style="margin: 0.75rem 0 0 1.5rem;">
          <li><code>catalog.library.org</code> or <code>opac.library.org</code> &mdash; public WebPAC, proxied through Cloudflare</li>
          <li><code>sierra.library.org</code> &mdash; backend hostname used by the desktop client, SDA, Z39.50, SIP2; DNS-only</li>
          <li><code>sip.library.org</code> &mdash; separate hostname for SIP2 endpoints if self-check vendors need a stable name</li>
          <li><code>z3950.library.org</code> &mdash; separate hostname for Z39.50 partners</li>
        </ul>
        <p style="margin-top: 0.75rem;">All hostnames can point to the same IP. The split is a DNS-layer separation so Cloudflare proxying can be applied to one without affecting the others.</p>
        <p><strong>Migration order:</strong> If your library currently has every service on a single hostname, add the new hostnames first, point clients at them, wait for TTL expiry, <em>then</em> proxy the OPAC.</p>
      </div>
    </div>
```

- [ ] **Step 2: Verify in browser**

Open `cloudflare-sierra-guide.html` in a browser. Confirm:
- New section appears between "Architecture Overview" and "DNS and SSL/TLS Setup"
- Table renders with 4 columns and 10 rows
- Card callout renders with the key recommendation
- Hostname split list is readable

- [ ] **Step 3: Commit**

```bash
git add iug2026-shared/docs/cloudflare-sierra-guide.html
git commit -m "feat(cloudflare-guide): add Sierra Service Topology section

New section documents all protocols/ports sharing a Sierra server
and recommends hostname separation before proxying."
```

---

## Task 2: Rework DNS Section — "Choose a DNS Strategy First" (Priority 1)

**Why:** The current DNS section jumps straight to "move nameservers to Cloudflare" without acknowledging that this is a whole-zone commitment. Replace the "Step 1: Move DNS to Cloudflare" subsection with a strategy-first approach presenting three options.

**Files:**
- Modify: `iug2026-shared/docs/cloudflare-sierra-guide.html` — the `#dns-and-ssl-tls-setup` section (originally lines 162-205, shifted by Task 1 insertion)

- [ ] **Step 1: Replace the "Step 1: Move DNS to Cloudflare" subsection**

Find the existing content starting at:

```html
    <h3 style="color: var(--navy); margin-bottom: 0.75rem;">Step 1: Move DNS to Cloudflare</h3>

    <div class="section-list">
      <div class="section-item">
        <h3>Initial setup</h3>
        <ol style="margin: 0.75rem 0 0 1.5rem;">
          <li>Create a Cloudflare account and add your OPAC domain</li>
          <li>Cloudflare will scan existing DNS records</li>
          <li>Update your domain&rsquo;s nameservers to Cloudflare&rsquo;s assigned nameservers</li>
          <li>Set your Sierra OPAC&rsquo;s A/AAAA/CNAME record to <strong>Proxied</strong> (orange cloud) &mdash; this routes traffic through Cloudflare</li>
        </ol>
        <p><strong>Critical:</strong> Only proxy the web OPAC record. Leave other records as DNS-only (gray cloud) for:</p>
        <ul style="margin: 0.75rem 0 0 1.5rem;">
          <li>Z39.50 hostname (if separate)</li>
          <li>SIP2 hostname (if separate)</li>
          <li>Mail (MX) records</li>
          <li>Any non-HTTP services</li>
        </ul>
      </div>
    </div>
```

Replace with:

```html
    <h3 style="color: var(--navy); margin-bottom: 0.75rem;">Choose a DNS Strategy First</h3>

    <div class="card">
      <p>Before touching any DNS settings, understand what you&rsquo;re committing to. Moving nameservers to Cloudflare transfers authoritative DNS for the <strong>entire zone</strong> &mdash; including MX, SPF/DKIM/DMARC, every subdomain, and every non-library service on the same domain. For libraries whose main domain also runs email, SSO, staff intranet, LibGuides, EZproxy, and link resolvers, that is a significantly larger operational change than it appears.</p>
    </div>

    <div class="section-list">
      <div class="section-item">
        <h3>Option A: Full nameserver delegation (zone-level)</h3>
        <p>Move the whole domain&rsquo;s authoritative DNS to Cloudflare.</p>
        <p><strong>Appropriate when:</strong> The library owns the domain outright and uses it primarily for library services.</p>
        <p><strong>Caveats:</strong></p>
        <ul style="margin: 0.75rem 0 0 1.5rem;">
          <li>Every MX, SPF, DKIM (all selectors), DMARC, TXT, SRV, CAA, and subdomain record must be faithfully recreated before the nameserver switch. Missing a DKIM selector or an SRV record can silently break email or other services for days.</li>
          <li>Any other team or department using the domain now depends on Cloudflare uptime and Cloudflare DNS for their services.</li>
          <li>This is the simplest model for small libraries whose domain is library-only.</li>
        </ul>
      </div>
      <div class="section-item">
        <h3>Option B: Partial DNS / CNAME setup</h3>
        <p>Keep existing authoritative DNS. CNAME a single hostname (e.g., <code>catalog.library.org</code>) to a Cloudflare-provided target.</p>
        <p><strong>Appropriate when:</strong> The domain is shared with the parent institution (common in academic libraries) or when the library does not control DNS.</p>
        <ul style="margin: 0.75rem 0 0 1.5rem;">
          <li>No zone takeover. Only the hostnames you CNAME go through Cloudflare.</li>
          <li>Historically a Business-plan feature; tier requirements change &mdash; check <a href="https://developers.cloudflare.com/dns/zone-setups/partial-setup/">current Cloudflare documentation on partial setups</a>.</li>
        </ul>
      </div>
      <div class="section-item">
        <h3>Option C: Dedicated subdomain delegation</h3>
        <p>Delegate a subzone like <code>cat.library.org</code> as its own zone on Cloudflare nameservers. Parent domain stays wherever it is.</p>
        <p><strong>Appropriate when:</strong> You want Cloudflare&rsquo;s full feature set for the catalog but cannot touch the parent zone.</p>
        <ul style="margin: 0.75rem 0 0 1.5rem;">
          <li>Requires the parent DNS admin to add NS records for the subzone.</li>
          <li>Gives you full nameserver-mode capabilities for just the catalog subdomain.</li>
        </ul>
      </div>
      <div class="section-item">
        <h3>Recommended default</h3>
        <p>For most libraries, the right default is <strong>Option B or C</strong>, not Option A. Option A is the simplest path if the domain is library-only and you&rsquo;re comfortable owning the full zone at Cloudflare &mdash; but most academic and consortium libraries share their domain with other institutional services.</p>
      </div>
    </div>

    <h3 style="color: var(--navy); margin-bottom: 0.75rem;">Pre-Migration DNS Checklist</h3>

    <div class="section-list">
      <div class="section-item">
        <h3>Before any DNS cutover (regardless of option chosen)</h3>
        <ol style="margin: 0.75rem 0 0 1.5rem;">
          <li>Export the current zone file (or a full record listing) from the existing DNS provider</li>
          <li>Lower TTLs to 300 seconds 24&ndash;48 hours ahead of the cutover</li>
          <li>Verify MX, SPF, DKIM (all selectors), DMARC, and any SRV or CAA records are captured</li>
          <li>Identify every hostname that points to a Sierra-adjacent service (see <a href="#sierra-service-topology">Sierra&rsquo;s Service Topology</a>)</li>
          <li>Document which records will be proxied (orange cloud) vs. DNS-only (gray cloud) <em>before</em> flipping the switch</li>
          <li>Set your Sierra OPAC&rsquo;s A/AAAA/CNAME record to <strong>Proxied</strong> (orange cloud) &mdash; this routes traffic through Cloudflare</li>
          <li>Leave all non-HTTP service records as DNS-only (gray cloud): Z39.50, SIP2, mail (MX), SDA, SSH</li>
        </ol>
      </div>
    </div>
```

- [ ] **Step 2: Verify in browser**

Confirm:
- Three DNS options render as separate section-items with clear headings
- "Recommended default" callout is present
- Pre-migration checklist renders as an ordered list
- No broken HTML or missing closing tags

- [ ] **Step 3: Commit**

```bash
git add iug2026-shared/docs/cloudflare-sierra-guide.html
git commit -m "feat(cloudflare-guide): rework DNS section with three strategy options

Replace the 'move nameservers to Cloudflare' step with a strategy-first
approach: full delegation, partial CNAME, or subdomain delegation.
Adds pre-migration DNS checklist."
```

---

## Task 3: Expand Sierra Deployment Models Table (Priority 3)

**Files:**
- Modify: `iug2026-shared/docs/cloudflare-sierra-guide.html` — the deployment models table (originally lines 140-158, shifted by prior tasks)

- [ ] **Step 1: Replace the deployment models table and add the III cloud-hosted advisory**

Find the existing table:

```html
    <table>
      <thead>
        <tr><th>Deployment</th><th>Cloudflare Setup</th></tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Self-hosted / on-premise</strong></td>
          <td>Full control &mdash; point DNS to Cloudflare, configure as needed</td>
        </tr>
        <tr>
          <td><strong>III cloud-hosted</strong></td>
          <td>May need to coordinate with III &mdash; you may not control DNS or the web server directly</td>
        </tr>
        <tr>
          <td><strong>Vega Discover (SaaS)</strong></td>
          <td>Likely already behind III&rsquo;s own CDN/WAF &mdash; limited customization</td>
        </tr>
      </tbody>
    </table>
```

Replace with:

```html
    <table>
      <thead>
        <tr><th>Deployment</th><th>Cloudflare Setup</th><th>DNS Strategy</th></tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Self-hosted / on-premise</strong></td>
          <td>Full control &mdash; point DNS to Cloudflare, configure as needed</td>
          <td>Any option (A, B, or C)</td>
        </tr>
        <tr>
          <td><strong>III cloud-hosted</strong></td>
          <td>Coordinate with III first. You may not control DNS or the web server directly. Whether you can CNAME your own hostname to III&rsquo;s target depends on your hosting contract and whether III&rsquo;s infrastructure permits SNI for a customer-provided hostname.</td>
          <td>Typically Option B (CNAME), since the IP can change and you never had direct A-record control</td>
        </tr>
        <tr>
          <td><strong>Vega Discover (SaaS)</strong></td>
          <td>III controls the infrastructure. Vega Discover is SaaS and <strong>cannot</strong> be fronted by your own Cloudflare tenant.</td>
          <td>N/A</td>
        </tr>
      </tbody>
    </table>

    <div class="card">
      <p><strong>If you&rsquo;re III cloud-hosted:</strong> Ask III before starting any of this. The answer to &ldquo;can we put a Cloudflare-proxied CNAME in front of our catalog?&rdquo; varies by contract and hosting generation.</p>
    </div>
```

- [ ] **Step 2: Verify in browser**

Confirm the table now has 3 columns, the III cloud-hosted row has substantially more detail, and the advisory card appears below the table.

- [ ] **Step 3: Commit**

```bash
git add iug2026-shared/docs/cloudflare-sierra-guide.html
git commit -m "feat(cloudflare-guide): expand deployment models table

Add DNS strategy column, detail III cloud-hosting constraints,
clarify Vega Discover cannot be fronted by customer Cloudflare."
```

---

## Task 4: Promote F5 Session Affinity to Architecture Overview (Priority 4)

**Why:** The F5 + Cloudflare incompatibility is a pre-deployment blocker, not a "gotcha." Move it to the Architecture section and expand it.

**Files:**
- Modify: `iug2026-shared/docs/cloudflare-sierra-guide.html` — two locations: Architecture Overview section and Known Issues section

- [ ] **Step 1: Add F5 subsection to Architecture Overview**

Find the closing of the Sierra Deployment Models section (after the `</div>` that closes the card added in Task 3, before the new "Sierra's Service Topology" section). Insert **before** the `<!-- Sierra's Service Topology -->` comment:

```html
    <h3 style="color: var(--navy); margin-bottom: 0.75rem;">If You Already Have F5 in Front of Sierra</h3>

    <div class="section-list">
      <div class="section-item">
        <h3>F5 + Cloudflare session affinity incompatibility</h3>
        <p>This is a <strong>pre-deployment blocker</strong> for any library running F5 BIG-IP with cookie-based persistence in front of Sierra.</p>
        <p><strong>The problem:</strong> F5 sets a session cookie at the beginning of a TCP connection and then ignores cookies on subsequent requests within that connection. Cloudflare multiplexes many HTTP sessions over single TCP connections to your origin. This breaks F5&rsquo;s cookie-based session affinity &mdash; requests from different users get routed to the wrong backend.</p>
        <p><strong>Resolution options:</strong></p>
        <ul style="margin: 0.75rem 0 0 1.5rem;">
          <li>Switch F5 to source-IP persistence using the <code>CF-Connecting-IP</code> header</li>
          <li>Disable F5 persistence entirely if Sierra doesn&rsquo;t require it</li>
          <li><strong>Test in a staging configuration before any production cutover</strong></li>
        </ul>
        <p>See the <a href="https://community.cloudflare.com/t/cloudflare-f5-cookie-based-session-affinity/175684">Cloudflare Community thread on F5 session affinity</a> for details.</p>
      </div>
    </div>
```

- [ ] **Step 2: Remove F5 content from Known Issues**

Find the F5 bullet within the "Session cookie handling" gotcha (item #1 in Known Issues):

```html
          <li><strong>If you&rsquo;re using Cloudflare + F5:</strong> F5 BIG-IP sets a session cookie at the beginning of a TCP connection and then ignores cookies on subsequent requests on the same TCP connection. Cloudflare multiplexes HTTP sessions over single TCP connections, which <strong>breaks F5 session affinity</strong>. This is a documented incompatibility.</li>
```

Replace with:

```html
          <li><strong>If you&rsquo;re using Cloudflare + F5:</strong> See the <a href="#architecture-overview">F5 section under Architecture Overview</a> &mdash; this is a pre-deployment blocker, not a post-deployment surprise.</li>
```

- [ ] **Step 3: Verify in browser**

Confirm:
- F5 subsection appears in Architecture Overview with resolution options
- Known Issues item #1 now has a cross-reference instead of duplicated content
- The Cloudflare Community link works in both locations

- [ ] **Step 4: Commit**

```bash
git add iug2026-shared/docs/cloudflare-sierra-guide.html
git commit -m "feat(cloudflare-guide): promote F5 session affinity to Architecture section

F5+Cloudflare incompatibility is a pre-deployment blocker, not a gotcha.
Moved detailed explanation to Architecture Overview, left cross-ref in
Known Issues."
```

---

## Task 5: Smaller Corrections and Clarifications (Priority 5)

Seven independent fixes. Apply them all in one pass through the file.

**Files:**
- Modify: `iug2026-shared/docs/cloudflare-sierra-guide.html` — multiple locations

- [ ] **Step 1: Fix Universal SSL subdomain depth**

Find the SSL/TLS Configuration section, specifically after the "Origin certificate options" section-item closing `</div>`. Add a new section-item before the `</div>` that closes the section-list:

Find:
```html
        <p><strong>Never use &ldquo;Flexible&rdquo; SSL mode</strong> &mdash; this leaves the Cloudflare-to-origin connection unencrypted, which is a security risk, especially for patron login traffic.</p>
      </div>
    </div>
```

Replace with:
```html
        <p><strong>Never use &ldquo;Flexible&rdquo; SSL mode</strong> &mdash; this leaves the Cloudflare-to-origin connection unencrypted, which is a security risk, especially for patron login traffic.</p>
      </div>
      <div class="section-item">
        <h3>Universal SSL subdomain depth</h3>
        <p>Cloudflare&rsquo;s Universal SSL covers only one level of subdomain by default. <code>catalog.library.org</code> is covered; <code>catalog.branch.library.org</code> is <strong>not</strong>, and requires <a href="https://developers.cloudflare.com/ssl/edge-certificates/advanced-certificate-manager/">Advanced Certificate Manager</a> or a custom certificate upload. If your OPAC hostname uses a multi-level subdomain, verify certificate coverage before going live.</p>
      </div>
    </div>
```

- [ ] **Step 2: Reframe port 2082 staging risk**

Find the staging server gotcha (item #7 in Known Issues):

```html
        <h3>7. WebPAC staging server (port 2082)</h3>
        <p>Sierra&rsquo;s staging WebPAC runs on port 2082. This is a Cloudflare-supported HTTP port, so it <em>could</em> be proxied. However, you probably want to keep staging access restricted &mdash; either leave it DNS-only or add a WAF rule blocking external access to port 2082.</p>
```

Replace with:

```html
        <h3>7. WebPAC staging server (port 2082)</h3>
        <p>Sierra&rsquo;s staging WebPAC runs on port 2082, which is a Cloudflare-supported HTTP port. This means <strong>staging is reachable on a proxiable port by default</strong> once your hostname is proxied through Cloudflare. This is a risk, not a convenience &mdash; decide deliberately whether to expose staging through Cloudflare or block it with a WAF rule. Recommended: add a WAF rule blocking external access to port 2082, or keep the staging hostname DNS-only.</p>
```

- [ ] **Step 3: Replace hard-coded pricing figures**

Find **all** instances of `~$20&ndash;25/mo` and `~$200&ndash;250/mo` in the file. There are occurrences in:
- The Bot Management tier comparison table header (line ~317)
- The Free vs. Paid Tiers table header (line ~696)
- The "Recommendation by Library Size" section (lines ~802, 806)
- The Comparison table (line ~839)

In the **Bot Management table header row**, replace:
```html
        <tr><th>Feature</th><th>Free</th><th>Pro (~$20&ndash;25/mo)</th><th>Business (~$200&ndash;250/mo)</th><th>Enterprise</th></tr>
```
with:
```html
        <tr><th>Feature</th><th>Free</th><th>Pro</th><th>Business</th><th>Enterprise</th></tr>
```

In the **Free vs. Paid Tiers table header row**, replace:
```html
        <tr><th>Feature</th><th>Free</th><th>Pro (~$20&ndash;25/mo)</th><th>Business (~$200&ndash;250/mo)</th><th>Enterprise</th></tr>
```
with:
```html
        <tr><th>Feature</th><th>Free</th><th>Pro</th><th>Business</th><th>Enterprise</th></tr>
```

In the **"Medium library" recommendation**, replace:
```html
        <p>Pro (~$20&ndash;25/mo) adds OWASP rules, 20 WAF rules, Super Bot Fight Mode with verified bot allowlisting, and bot analytics. Best value for most Sierra installations.</p>
```
with:
```html
        <p>Pro adds OWASP rules, 20 WAF rules, Super Bot Fight Mode with verified bot allowlisting, and bot analytics. Best value for most Sierra installations. See <a href="https://www.cloudflare.com/plans/">Cloudflare&rsquo;s current pricing</a>.</p>
```

In the **"Large academic" recommendation**, replace:
```html
        <p>Business (~$200&ndash;250/mo) adds bypass-cache-on-cookie (important for patron sessions), 100 WAF rules, advanced rate limiting, and custom error pages.</p>
```
with:
```html
        <p>Business adds bypass-cache-on-cookie (important for patron sessions), 100 WAF rules, advanced rate limiting, and custom error pages. See <a href="https://www.cloudflare.com/plans/">Cloudflare&rsquo;s current pricing</a>.</p>
```

In the **Comparison table**, replace:
```html
          <td>Free tier available; Pro ~$20&ndash;25/mo</td>
```
with:
```html
          <td>Free tier available; see <a href="https://www.cloudflare.com/plans/">current pricing</a> for Pro/Business</td>
```

- [ ] **Step 4: Fix Rate Limiting Rule 4**

Find:
```html
      <div class="section-item">
        <h3>Rule 4: Global rate limit (DDoS backstop)</h3>
        <p><code>(http.request.uri.path ne "/")</code></p>
        <p class="detail">Characteristics: IP &middot; Period: 10 seconds &middot; Requests: 50 &middot; Action: Managed Challenge &middot; Duration: 10 minutes</p>
        <p>Any single IP making 50+ requests in 10 seconds is almost certainly not a human.</p>
      </div>
```

Replace with:
```html
      <div class="section-item">
        <h3>Rule 4: Global rate limit (DDoS backstop)</h3>
        <p><code>(http.request.uri.path ne "/" and not http.request.uri.path contains "/screens/" and not http.request.uri.path.extension in {"css" "js" "png" "jpg" "gif" "ico" "svg" "woff" "woff2"})</code></p>
        <p class="detail">Characteristics: IP &middot; Period: 10 seconds &middot; Requests: 100 &middot; Action: Managed Challenge &middot; Duration: 10 minutes</p>
        <p>The previous match <code>http.request.uri.path ne "/"</code> was too broad and would fire on legitimate asset loads &mdash; a single record page can trigger dozens of CSS/JS/image requests. This version excludes static assets and raises the threshold to 100 requests in 10 seconds.</p>
      </div>
```

- [ ] **Step 5: Fix "Bypass cache on cookie" tier note**

Find:
```html
        <p class="detail">Note: &ldquo;Bypass Cache on Cookie&rdquo; requires a <strong>Business plan</strong> or a Cloudflare Worker on lower plans.</p>
```

Replace with:
```html
        <p class="detail">Note: &ldquo;Bypass Cache on Cookie&rdquo; has historically required a Business plan. Check <a href="https://developers.cloudflare.com/cache/how-to/cache-rules/">current Cache Rules documentation</a> to verify whether cookie-based bypass is now available on lower tiers. A Cloudflare Worker can achieve the same result on any plan.</p>
```

- [ ] **Step 6: Fix Google Scholar and add vendor IP links in Verified Bots table**

Find:
```html
        <tr>
          <td><strong>Google Scholar</strong></td>
          <td>Crawls for academic citations</td>
          <td>Check verified list</td>
          <td>Usually verified</td>
        </tr>
```

Replace with:
```html
        <tr>
          <td><strong>Google Scholar</strong></td>
          <td>Crawls for academic citations</td>
          <td>Yes (uses Googlebot infrastructure)</td>
          <td>Auto-allowed as Googlebot</td>
        </tr>
```

Find:
```html
        <tr>
          <td><strong>Ex Libris Primo/Summon</strong></td>
          <td>Queries OPAC for discovery</td>
          <td>No</td>
          <td>Allowlist by IP</td>
        </tr>
```

Replace with:
```html
        <tr>
          <td><strong>Ex Libris Primo/Summon</strong></td>
          <td>Queries OPAC for discovery</td>
          <td>No</td>
          <td>Allowlist by IP &mdash; <a href="https://knowledge.exlibrisgroup.com/Primo/Knowledge_Articles/Primo_Central_IPs">published IP ranges</a></td>
        </tr>
```

Find:
```html
        <tr>
          <td><strong>EBSCO EDS connector</strong></td>
          <td>Queries OPAC for discovery</td>
          <td>No</td>
          <td>Allowlist by IP</td>
        </tr>
```

Replace with:
```html
        <tr>
          <td><strong>EBSCO EDS connector</strong></td>
          <td>Queries OPAC for discovery</td>
          <td>No</td>
          <td>Allowlist by IP &mdash; <a href="https://connect.ebsco.com/s/article/EBSCOhost-IP-Addresses">published IP ranges</a></td>
        </tr>
```

- [ ] **Step 7: Strengthen Project Galileo language**

Find:
```html
        <p>Cloudflare&rsquo;s <a href="https://www.cloudflare.com/galileo/">Project Galileo</a> provides <strong>Business and Enterprise-tier features for free</strong> to qualifying organizations facing cyber threats. Participants get Bot Management, AI Crawl Control, and Zero Trust security products at no cost. It&rsquo;s designed for journalism, human rights, and civil society groups. Public libraries <em>may</em> qualify depending on circumstances &mdash; worth applying if your library has been targeted by attacks.</p>
```

Replace with:
```html
        <p>Cloudflare&rsquo;s <a href="https://www.cloudflare.com/galileo/">Project Galileo</a> provides <strong>Business and Enterprise-tier features for free</strong> to qualifying organizations facing cyber threats. Participants get Bot Management, AI Crawl Control, and Zero Trust security products at no cost. Originally designed for journalism, human rights, and civil society groups, Cloudflare has explicitly expanded Galileo to include library and cultural heritage contexts in recent years. Public libraries should seriously consider <a href="https://www.cloudflare.com/galileo/#apply">applying</a>, especially if targeted by bot attacks or scraping campaigns.</p>
```

- [ ] **Step 8: Verify all changes in browser**

Open the guide and check each changed section:
- SSL/TLS section has new subdomain depth note
- Staging server gotcha reframed as a risk
- No dollar figures remain in table headers or recommendation text
- Rate limiting Rule 4 shows the updated expression and threshold
- Cache bypass note links to current docs
- Google Scholar row says "Yes" with explanation
- EBSCO and Ex Libris rows have IP documentation links
- Project Galileo language is stronger with application link

- [ ] **Step 9: Commit**

```bash
git add iug2026-shared/docs/cloudflare-sierra-guide.html
git commit -m "fix(cloudflare-guide): priority 5 corrections

- Add Universal SSL subdomain depth warning
- Reframe port 2082 staging as a risk
- Replace hard-coded pricing with links to Cloudflare pricing page
- Fix rate limiting Rule 4: exclude static assets, raise threshold
- Add tier-verification note to bypass-cache-on-cookie
- Fix Google Scholar verified bot status
- Add vendor IP documentation links for EBSCO and Ex Libris
- Strengthen Project Galileo eligibility language"
```

---

## Task 6: Update Table of Contents

**Why:** The section order has changed with new sections added. Update the TOC to match.

**Files:**
- Modify: `iug2026-shared/docs/cloudflare-sierra-guide.html` — the TOC `<ol>` block

- [ ] **Step 1: Replace the TOC**

Find:
```html
        <ol style="margin: 0.25rem 0 0 1.5rem;">
          <li><a href="#why-this-matters-now">Why This Matters Now</a></li>
          <li><a href="#architecture-overview">Architecture Overview</a></li>
          <li><a href="#dns-and-ssl-tls-setup">DNS and SSL/TLS Setup</a></li>
          <li><a href="#cloudflare-waf-rules-for-sierra">Cloudflare WAF Rules for Sierra</a></li>
          <li><a href="#bot-management">Bot Management</a></li>
          <li><a href="#caching-strategy">Caching Strategy</a></li>
          <li><a href="#rate-limiting">Rate Limiting</a></li>
          <li><a href="#page-rules-and-transform-rules">Page Rules and Transform Rules</a></li>
          <li><a href="#known-issues-and-gotchas">Known Issues and Gotchas</a></li>
          <li><a href="#free-vs-paid-tiers">Free vs. Paid Tiers</a></li>
          <li><a href="#comparison-cloudflare-vs-f5-fail2ban">Comparison: Cloudflare vs. F5/fail2ban</a></li>
          <li><a href="#alternative-anubis">Alternative: Anubis (Proof of Work)</a></li>
          <li><a href="#practical-recommendations">Practical Recommendations</a></li>
          <li><a href="#sources-and-further-reading">Sources and Further Reading</a></li>
        </ol>
```

Replace with:
```html
        <ol style="margin: 0.25rem 0 0 1.5rem;">
          <li><a href="#why-this-matters-now">Why This Matters Now</a></li>
          <li><a href="#architecture-overview">Architecture Overview</a></li>
          <li><a href="#sierra-service-topology">Sierra&rsquo;s Service Topology</a></li>
          <li><a href="#dns-and-ssl-tls-setup">DNS and SSL/TLS Setup</a></li>
          <li><a href="#cloudflare-waf-rules-for-sierra">Cloudflare WAF Rules for Sierra</a></li>
          <li><a href="#bot-management">Bot Management</a></li>
          <li><a href="#caching-strategy">Caching Strategy</a></li>
          <li><a href="#rate-limiting">Rate Limiting</a></li>
          <li><a href="#page-rules-and-transform-rules">Page Rules and Transform Rules</a></li>
          <li><a href="#known-issues-and-gotchas">Known Issues and Gotchas</a></li>
          <li><a href="#free-vs-paid-tiers">Free vs. Paid Tiers</a></li>
          <li><a href="#comparison-cloudflare-vs-f5-fail2ban">Comparison: Cloudflare vs. F5/fail2ban</a></li>
          <li><a href="#alternative-anubis">Alternative: Anubis (Proof of Work)</a></li>
          <li><a href="#practical-recommendations">Practical Recommendations</a></li>
          <li><a href="#sources-and-further-reading">Sources and Further Reading</a></li>
        </ol>
```

- [ ] **Step 2: Verify TOC links work**

Open the guide in a browser. Click each TOC link. Verify all 15 anchor links scroll to the correct section.

- [ ] **Step 3: Commit**

```bash
git add iug2026-shared/docs/cloudflare-sierra-guide.html
git commit -m "fix(cloudflare-guide): update table of contents

Add Sierra Service Topology section to TOC."
```

---

## Task 7: Update "Practical Recommendations" to Reflect DNS Strategy

**Files:**
- Modify: `iug2026-shared/docs/cloudflare-sierra-guide.html` — the "Minimum Viable Protection" and "Starting from Zero" subsections

- [ ] **Step 1: Update "Starting from Zero" steps**

Find:
```html
        <ol style="margin: 0.75rem 0 0 1.5rem;">
          <li><strong>Sign up for Cloudflare Free</strong> and point your OPAC DNS to Cloudflare</li>
          <li><strong>Set SSL/TLS to Full (Strict)</strong> with a Cloudflare Origin CA cert</li>
          <li><strong>Enable AI Scrapers and Crawlers blocking</strong> (one click, immediate effect)</li>
          <li><strong>Create IP allowlist rules</strong> for EZproxy, discovery layer, OCLC, and other trusted services BEFORE enabling any blocking rules</li>
          <li><strong>Add rate limiting</strong> on <code>/patroninfo</code> (login) and <code>/search</code> paths</li>
          <li><strong>Keep Z39.50 and SIP2 on DNS-only records</strong></li>
          <li><strong>Test thoroughly</strong> &mdash; especially patron login, MARC downloads, discovery layer integration, and any automated processes that query the OPAC</li>
        </ol>
```

Replace with:
```html
        <ol style="margin: 0.75rem 0 0 1.5rem;">
          <li><strong>Read <a href="#sierra-service-topology">Sierra&rsquo;s Service Topology</a></strong> and separate your OPAC hostname from non-HTTP services if you haven&rsquo;t already</li>
          <li><strong><a href="#dns-and-ssl-tls-setup">Choose a DNS strategy</a></strong> &mdash; most libraries should use Option B (CNAME) or C (subdomain delegation), not full nameserver transfer</li>
          <li><strong>Run the <a href="#dns-and-ssl-tls-setup">pre-migration DNS checklist</a></strong></li>
          <li><strong>Sign up for Cloudflare Free</strong> and configure DNS per your chosen strategy</li>
          <li><strong>Set SSL/TLS to Full (Strict)</strong> with a Cloudflare Origin CA cert</li>
          <li><strong>Enable AI Scrapers and Crawlers blocking</strong> (one click, immediate effect)</li>
          <li><strong>Create IP allowlist rules</strong> for EZproxy, discovery layer, OCLC, and other trusted services BEFORE enabling any blocking rules</li>
          <li><strong>Add rate limiting</strong> on <code>/patroninfo</code> (login) and <code>/search</code> paths</li>
          <li><strong>Keep Z39.50 and SIP2 on DNS-only records</strong></li>
          <li><strong>Test thoroughly</strong> &mdash; especially patron login, MARC downloads, discovery layer integration, and any automated processes that query the OPAC</li>
        </ol>
```

- [ ] **Step 2: Update "Minimum Viable Protection" steps**

Find:
```html
        <ol style="margin: 0.75rem 0 0 1.5rem;">
          <li>Cloudflare Free account</li>
          <li>Change DNS nameservers</li>
          <li>Orange-cloud your OPAC A record</li>
          <li>Enable &ldquo;AI Scrapers and Crawlers&rdquo; toggle</li>
          <li>Done &mdash; you now have DDoS protection and AI bot blocking</li>
        </ol>
        <p>Then iterate on WAF rules, rate limiting, and caching as time allows.</p>
```

Replace with:
```html
        <ol style="margin: 0.75rem 0 0 1.5rem;">
          <li>Cloudflare Free account</li>
          <li>Configure DNS per your <a href="#dns-and-ssl-tls-setup">chosen strategy</a> (if you own the domain outright, full nameserver delegation is fastest; otherwise use a CNAME setup)</li>
          <li>Orange-cloud your OPAC A/CNAME record (and <strong>only</strong> the OPAC &mdash; see <a href="#sierra-service-topology">Service Topology</a>)</li>
          <li>Enable &ldquo;AI Scrapers and Crawlers&rdquo; toggle</li>
          <li>Done &mdash; you now have DDoS protection and AI bot blocking</li>
        </ol>
        <p>Then iterate on WAF rules, rate limiting, and caching as time allows.</p>
```

- [ ] **Step 3: Verify in browser**

Confirm the updated steps render correctly and internal links work.

- [ ] **Step 4: Commit**

```bash
git add iug2026-shared/docs/cloudflare-sierra-guide.html
git commit -m "fix(cloudflare-guide): update practical recommendations for DNS strategy

Starting-from-zero and minimum-viable-protection now reference the
DNS strategy decision and service topology sections."
```

---

## Task 8: Add "Revised from Earlier Version" Note

**Why:** The brief asks for a note so sys admins who bookmarked the original understand what changed.

**Files:**
- Modify: `iug2026-shared/docs/cloudflare-sierra-guide.html` — just below the page subtitle

- [ ] **Step 1: Add revision note**

Find:
```html
    <div class="card">
      <p>A comprehensive guide to putting Sierra&rsquo;s web OPAC behind Cloudflare: what works, what breaks, and what to watch out for. Compiled from the IUG 2026 Sys Admin Forum discussion and follow-up research.</p>
    </div>
```

Replace with:
```html
    <div class="card">
      <p>A comprehensive guide to putting Sierra&rsquo;s web OPAC behind Cloudflare: what works, what breaks, and what to watch out for. Compiled from the IUG 2026 Sys Admin Forum discussion and follow-up research.</p>
      <p style="margin-top: 0.5rem; font-size: 0.85rem; color: var(--text);"><em><strong>Revised April 2026:</strong> Added DNS strategy options (the original version assumed full nameserver delegation), Sierra service topology section, expanded III cloud-hosting guidance, promoted F5 session affinity to a pre-deployment blocker, and corrected several tier/pricing claims. See the revision history on <a href="https://github.com/rayvoelker/iug2026-shared/commits/main/docs/cloudflare-sierra-guide.html">GitHub</a>.</em></p>
    </div>
```

- [ ] **Step 2: Verify in browser**

Confirm the revision note appears in smaller italic text below the intro paragraph inside the same card.

- [ ] **Step 3: Commit**

```bash
git add iug2026-shared/docs/cloudflare-sierra-guide.html
git commit -m "docs(cloudflare-guide): add revision note for returning readers

Notes the major changes from the original version so sys admins who
bookmarked the page understand what's different."
```

---

## Task 9: Final Review Pass

- [ ] **Step 1: Full browser review**

Open the completed guide in a browser. Walk through every section top to bottom:
- TOC links all work (15 items)
- No broken HTML (check for unclosed tags visually)
- Tables render with correct column counts
- All internal `#anchor` links resolve
- All external links are clickable
- No hard-coded dollar figures remain (search for `$` in the HTML source)
- The revision note is visible
- The practitioner-notes tone is preserved throughout

- [ ] **Step 2: Validate HTML**

```bash
# Quick check for unclosed tags
grep -c '<div' iug2026-shared/docs/cloudflare-sierra-guide.html
grep -c '</div>' iug2026-shared/docs/cloudflare-sierra-guide.html
# These counts should match
```

- [ ] **Step 3: Final commit if any cleanup needed**

Only if issues were found and fixed in the review pass.
