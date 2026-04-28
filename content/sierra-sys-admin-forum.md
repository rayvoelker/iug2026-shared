---
title: "Sierra Sys Admin Forum"
template: session
day: wednesday
date: "April 15"
speakers:
  - jeff-campbell
speakers_display: "Jeff Campbell (UNC Chapel Hill) & Stephanie Brew · 4:30–5:30 PM · Chicago Ballroom A · Sierra Track"
description: "Open forum for Sierra system administrators covering migration considerations, bot protection, paging lists, accessibility, SDA vs. Sierra Web, and more."
---

<div class="card">
  <p>An open forum for Sierra system administrators &mdash; Jeff&rsquo;s last time hosting. Wide-ranging discussion covering Sierra-to-Polaris migration considerations, invoicing workarounds, Koha feasibility, bot protection strategies (Cloudflare, F5, fail2ban), locations served and paging configuration, SDA vs. Sierra Web, WebPAC accessibility challenges, and circ active date behavior with e-vendor APIs.</p>
</div>

<!-- Sierra vs. Polaris — Migration Considerations -->

<h2>Sierra vs. Polaris &mdash; Migration Considerations</h2>

<div class="section-list">
  <div class="section-item">
    <h3>Room temperature check</h3>
    <p>Show of hands: 2 definite, 4 maybe considering Sierra-to-Polaris migration. <strong>Polaris pricing is similar</strong> to Sierra renewal costs, but there&rsquo;s an additional unknown implementation cost on top. Pricing should be negotiable &mdash; one attendee just renewed Sierra for 3 more years at comparable rates.</p>
    <p>A sales rep deflected on pricing at lunch &mdash; an attendee pushed back: &ldquo;I&rsquo;m the one who has to get it approved&hellip; Our board isn&rsquo;t going to just say oh yeah spend another hundred thousand.&rdquo;</p>
  </div>
  <div class="section-item">
    <h3>Timing and decision pressure</h3>
    <p>One attendee: &ldquo;I feel like it&rsquo;s now or five years from now&rdquo; &mdash; the renewal cycle is the natural decision point.</p>
    <p><strong>A consortium hired Marshall Breeding</strong> for a landscape report. After 20 years on Sierra, his conclusion: <strong>&ldquo;Stay on Sierra for the moment and do a deep dive in about three years, maybe five.&rdquo;</strong></p>
    <p><strong>III themselves recommended staying on Sierra</strong> &mdash; at PLA, an attendee&rsquo;s assistant director spoke with III reps and &ldquo;that was their recommendation. Stay on Sierra. You&rsquo;re good here.&rdquo;</p>
  </div>
  <div class="section-item">
    <h3>Migration evaluation</h3>
    <p>An attendee evaluated Polaris: &ldquo;It couldn&rsquo;t be just a hair better, it had to be like this much better, and it wasn&rsquo;t&hellip; not worth everything that comes with the migration.&rdquo;</p>
    <p><strong>End users driving the push</strong> &mdash; people who migrated Sierra-to-Polaris said the common denominator was end users wanting &ldquo;something that looked a little bit more modern.&rdquo; Staff hired from Polaris libraries miss things from a technical perspective.</p>
  </div>
  <div class="section-item">
    <h3>True cost of migration</h3>
    <p>The true cost extends far beyond the contract: Aspen discovery layer migration, 72+ hours of downtime, communications team, staff training, morale. &ldquo;Your staff want Polaris because it is pretty but do they want to go through all of that?&rdquo;</p>
    <p>A consortium&rsquo;s ILS RFP took <strong>9 months</strong>. Consortium constraints limit choices: &ldquo;Our only two choices are Sierra or Polaris.&rdquo;</p>
    <p>Contact <strong>Derrick Brown</strong> for a Polaris demo &mdash; someone offered to show how Polaris works.</p>
  </div>
</div>

<!-- Invoicing / Order Record Issue -->

<h2>Invoicing / Order Record Issue</h2>

<div class="section-list">
  <div class="section-item">
    <h3>The problem</h3>
    <p>A small standalone library stopped using Sierra invoicing when their municipality switched finance systems. A year and a half later, unprocessed invoices are blocking order record deletion (~6,000 records). Can&rsquo;t do global updates on status codes &mdash; would have to change each one manually. Innovative support confirmed the problem and has been manually force-clearing on their end.</p>
  </div>
  <div class="section-item">
    <h3>Jeremy&rsquo;s solution (acquisitions expert)</h3>
    <ol style="margin: 0.75rem 0 0 1.5rem;">
      <li>Go to <strong>Funds function</strong> &rarr; <strong>Tools dropdown</strong> &rarr; <strong>&ldquo;Clear payment history&rdquo;</strong> and force clear</li>
      <li>Ideal method: run a <strong>Fund Activity Report</strong> first to get a printout of all transaction info, then clear</li>
      <li>The <strong>Fund Activity Report</strong> (the ideal method in step 2) may take <strong>30&ndash;45 minutes</strong> to run</li>
      <li>Once invoices are cleared, order records become unlocked</li>
      <li>Put order records into a <strong>review file</strong> and use <strong>batch cancel</strong> to clear them in bulk</li>
      <li>If the clear doesn&rsquo;t work, Innovative support can help via a support ticket</li>
    </ol>
  </div>
</div>

<!-- Migrating to Koha -->

<h2>Migrating to Koha</h2>

<div class="section-list">
  <div class="section-item">
    <h3>Interest and budget pressure</h3>
    <p>Budget pressure is driving Koha interest: &ldquo;We don&rsquo;t have concrete plans but we are getting a lot of budget pressure to look at another ILS.&rdquo;</p>
    <p>Another attendee came from Koha to Sierra &mdash; they loved the flexibility (direct SQL querying was great).</p>
  </div>
  <div class="section-item">
    <h3>Koha struggles with scale</h3>
    <p>Jeff (UNC): &ldquo;We have 20 million records, almost 23 million&hellip; large library consortiums struggle with Koha and they could not handle our records.&rdquo;</p>
    <p>Jeremy (Minuteman Library Network &mdash; a Sierra consortium in Massachusetts): other MA consortiums are on Koha/Evergreen; as staff move between libraries there&rsquo;s &ldquo;an influx of staff who are used to open source systems&hellip; Sierra is sort of railing to them.&rdquo; That said, the <strong>Minuteman Consortia office staff</strong> &ldquo;are extremely happy&rdquo; with Sierra.</p>
  </div>
  <div class="section-item">
    <h3>Vendor lock-in considerations</h3>
    <p>One attendee feels locked into <strong>Lyngsoe Systems</strong> (automated materials handling / book sorter). Only certain ILS vendors support integration: Sierra supports it, SirsiDynix supports it, Polaris is working on it. This significantly limits ILS migration options.</p>
  </div>
  <div class="section-item">
    <h3>General sentiment</h3>
    <p>Jeff: &ldquo;The ILS you have is the best ILS.&rdquo;</p>
    <p>Victor: his library has a &ldquo;sister library&rdquo; on Koha &mdash; <strong>&ldquo;Acquisitions and cataloging are not quite as mature as Sierra.&rdquo;</strong> His advice: identify what features are essential and make sure the new ILS has them. &ldquo;That kind of frames the conversation into that specific set of requirements. As opposed to like, well the other one was nice, but functionally speaking that doesn&rsquo;t do anything.&rdquo;</p>
    <p>Victor&rsquo;s pragmatic filter for complaints: &ldquo;We have people say oh we hate Sierra&hellip; some of those opinions may be valid but it&rsquo;s one person and we&rsquo;re catering to over 99%.&rdquo;</p>
    <p>Jeremy: &ldquo;The system you start with is kind of what you imprint on&rdquo; &mdash; echoed by multiple attendees.</p>
  </div>
</div>

<h3 style="color: var(--navy); margin-bottom: 0.75rem;">ILS Migration Studies</h3>

<div class="section-list">
  <div class="section-item">
    <ul style="margin: 0.25rem 0 0 1.5rem;">
      <li><a href="https://www.sciencedirect.com/science/article/abs/pii/S0099133309000275">ILS Challenges and Opportunities: A Survey of U.S. Academic Libraries with Migration Projects</a> (Journal of Academic Librarianship, 2009)</li>
      <li><a href="https://digitalcommons.unl.edu/libphilprac/2535/">Challenges of ILS Migration in Academic Libraries</a></li>
      <li><a href="https://ital.corejournals.org/index.php/ital/article/download/2268/pdf">Experiences of Migrating to an Open-Source ILS</a></li>
    </ul>
  </div>
</div>

<!-- Sierra's Future / Longevity -->

<h2>Sierra&rsquo;s Future / Longevity</h2>

<div class="section-list">
  <div class="section-item">
    <h3>Domestic sales declining</h3>
    <p>Jeff: &ldquo;I don&rsquo;t think it&rsquo;s any secret that they&rsquo;re not selling a lot of Sierra subscriptions in the United States. But it sounds like it is doing better overseas.&rdquo; Saudi Arabia deploying Sierra for 175 libraries.</p>
    <p><strong>Public libraries are going Polaris</strong> &mdash; III would &ldquo;absolutely encourage them to buy&rdquo; Polaris for public libraries.</p>
  </div>
  <div class="section-item">
    <h3>IUG attendance shifting</h3>
    <p>Roughly <strong>2/3 Polaris, 1/3 Sierra</strong> at IUG &mdash; Jeff predicted &ldquo;that&rsquo;s probably going to become more lopsided.&rdquo;</p>
    <p>&ldquo;One company with two competing products seems curious&rdquo; &mdash; the elephant in the room about Clarivate/III having Sierra, Polaris, Millennium (legacy), and Leap all active. There are still a few Millennium customers.</p>
  </div>
  <div class="section-item">
    <h3>The Millennium-to-Sierra transition</h3>
    <p>The migration was a &ldquo;nothing burger&rdquo; &mdash; Jeff was a beta institution: staff were terrified but &ldquo;Oh, new color scheme. Great.&rdquo; Intentional design decision to keep it similar, but &ldquo;the interface felt dated already when it came out.&rdquo; &ldquo;They got rid of the mountains&rdquo; (Sierra splash screen reference).</p>
  </div>
</div>

<!-- The Dated Look -->

<h2>The &ldquo;Dated Look&rdquo; Debate</h2>

<div class="section-list">
  <div class="section-item">
    <h3>Functionality over aesthetics</h3>
    <p>The &ldquo;looks old&rdquo; complaint is the #1 thing Polaris fans say.</p>
    <p><strong>&ldquo;Pretty things are usually shallow. If you focus on the UI first, the power behind it is not as strong. That&rsquo;s how databases work.&rdquo;</strong></p>
    <p>Jeff&rsquo;s pushback: &ldquo;Why does the look matter more than the functionality? Is it to please my younger users, my Gen Zers?&rdquo;</p>
    <p><strong>&ldquo;This is not an end user system. This is not meant to be used by someone who has never been trained before.&rdquo;</strong></p>
  </div>
  <div class="section-item">
    <h3>UNC&rsquo;s staffing situation</h3>
    <p>Lost 55 staff due to hiring freeze &mdash; migration impossible without adequate staff. Part of Triangle Research Library Network (Duke, NC State, NC Central). Getting Rapido because partner institutions moved to Alma, but don&rsquo;t have budget/staff to migrate.</p>
  </div>
</div>

<!-- Overrides / Vega -->

<h2>Overrides / Vega</h2>

<div class="section-list">
  <div class="section-item">
    <h3>Override management</h3>
    <p>Overrides are a problem &mdash; consortium/shared system admin actively discourages staff from using overrides to reduce downstream data cleanup.</p>
    <p><strong>Patron override coming to Vega</strong> &mdash; once it arrives, front-line staff expected to &ldquo;stop using the actual Sierra client and go exclusively in Vega for everything.&rdquo;</p>
  </div>
</div>

<!-- SDA vs. Sierra Web -->

<h2>Sierra Desktop App (SDA) vs. Sierra Web</h2>

<div class="section-list">
  <div class="section-item">
    <h3>SDA stability improvements</h3>
    <p>Remote desktop user reporting issues with SDA &mdash; failure to log in or initialize once or twice a week. <strong>Updating the JRE</strong> to the most recent version dramatically improved SDA startup (&ldquo;night and day&rdquo;), though &ldquo;not perfect.&rdquo;</p>
    <p>Growing sentiment that more reliance on Sierra Web is important &mdash; one speaker noted &ldquo;Leap is going to be a more sustainable platform than the Sierra desktop app.&rdquo;</p>
  </div>
  <div class="section-item">
    <h3>Current usage split</h3>
    <p>Some libraries are ~50-50: front desk/circ on Sierra Web, collection management staff still on SDA.</p>
    <p><strong>ERM (Electronic Resource Management) is bad in Sierra Web</strong> &mdash; electronic resources person at one library &ldquo;hates Sierra Web&rdquo; and refuses to give up the desktop app. Sierra Web only works properly in Chrome, not Firefox.</p>
    <p><strong>Pagination is painful in Sierra Web</strong> &mdash; editing records that get paginated is bad enough to drive users back to SDA.</p>
  </div>
  <div class="section-item">
    <h3>Workflows vs. permissions</h3>
    <p>One user couldn&rsquo;t see expected menu functions despite having all permissions &mdash; workflows (which control dropdown menus) are configured separately from permissions.</p>
  </div>
</div>

<!-- Accessibility / WCAG -->

<h2>Accessibility / WCAG</h2>

<div class="section-list">
  <div class="section-item">
    <h3>WebPAC accessibility problems</h3>
    <p>Multiple libraries are <strong>getting &ldquo;dinged&rdquo; about accessibility</strong> of the classic WebPAC. Even if you don&rsquo;t point patrons to it, it&rsquo;s still publicly accessible, which &ldquo;alarms our accessibility people.&rdquo;</p>
    <p>Libraries want to <strong>hide classic catalog from public but keep it for staff</strong> &mdash; no one has found a solution yet. Firewall approaches tried; ticket open with Innovative.</p>
  </div>
  <div class="section-item">
    <h3>Dependencies blocking removal</h3>
    <p>A &ldquo;very small core set of patrons&rdquo; still use the classic catalog and are already complaining. <strong>Catalogers &ldquo;will revolt&rdquo;</strong> if classic is removed entirely &mdash; staff still depend on it.</p>
    <p><strong>Patron registration forms</strong> are served through WebPAC &mdash; another dependency that blocks removal.</p>
    <p>Innovative may be &ldquo;working with somebody to figure out how to disable it&rdquo; &mdash; uncertain.</p>
  </div>
  <div class="section-item">
    <h3>Templates cannot fix it</h3>
    <p>&ldquo;We fixed everything you can fix using the templates.&rdquo; The remaining failures are in server-side code: &ldquo;Your template calls this function and then magic happens on the back end, and the magic is broken. You can&rsquo;t fix it in post.&rdquo;</p>
    <p>Some exploring <strong>Vega Discover</strong> as a WebPAC replacement. Good to see other people concerned about WCAG compliance.</p>
  </div>
</div>

<!-- Circ Active / Patron Record Updates -->

<h2>Circ Active / Patron Record Updates</h2>

<div class="section-list">
  <div class="section-item">
    <h3>The problem</h3>
    <p>Bulk updating patron records is difficult because the circ active date gets updated whenever a patron record is modified (including via API) &mdash; makes it unreliable for purging inactive patrons.</p>
  </div>
  <div class="section-item">
    <h3>New API enhancement</h3>
    <p><strong>Mike Dicus (Clarivate) confirmed a new API enhancement coming:</strong> for e-vendors (Hoopla, Overdrive) validating patrons, the record won&rsquo;t get its &ldquo;last updated&rdquo; date changed, but the circ active date can be set to indicate the patron is using e-resources. However, it does <strong>not</strong> take a date parameter to backdate. Toggle is &ldquo;all or nothing.&rdquo;</p>
    <p><strong>Action item:</strong> everyone should contact Hoopla/Overdrive to push them to adopt the new validation method.</p>
    <p>Someone has a script workaround for this issue.</p>
  </div>
</div>

<!-- Cloudflare Protection -->

<h2>Cloudflare / Bot Protection</h2>

<div class="section-list">
  <div class="section-item">
    <h3>Cloudflare cautionary tale</h3>
    <p>Someone implemented Cloudflare on Monday morning to stop bot/DDoS attacks &mdash; it stopped the bots <strong>but also blocked all staff</strong> from Sierra and Sierra Web. Associated resources authenticating against Sierra also broke. They were &ldquo;desperately trying to get lists of IPs from different vendors&rdquo; to whitelist.</p>
    <p>Advice: become &ldquo;best friends with your networking team&rdquo; &mdash; use <strong>Admin Corner</strong> in Sierra to get list of currently connected IPs to feed to firewall allowlist.</p>
    <p>Another library&rsquo;s firewall upgrade broke Sierra connectivity because &ldquo;they didn&rsquo;t really consider Sierra before they upgraded the firewall.&rdquo;</p>
  </div>
  <div class="section-item">
    <h3>F5 experience (Bambi, UNC &mdash; bambi@unc.edu)</h3>
    <p>Went behind F5 for bot control starting 2024&ndash;2025, cost <strong>$30,000/year</strong> and &ldquo;they weren&rsquo;t really providing much after that initial catch up.&rdquo; Switched to block lists and fail2ban &ldquo;in a fairly robust way.&rdquo;</p>
    <p>Set up a <strong>separate hostname</strong> &mdash; public-facing domain behind F5 for bot protection, different one for internal services. Currently &ldquo;hardly any bot now&rdquo; on Sierra, but digital library hosts still getting hit (38K&ndash;120K bot attacks daily). <strong>Offered to share setup via email.</strong></p>
  </div>
  <div class="section-item">
    <h3>Innovative&rsquo;s crawler blocker (&ldquo;old browser trick&rdquo;)</h3>
    <p>III can put a blocker on your Sierra host &mdash; if a client claims to be a browser version more than 3 versions old, it gets blocked. Everything rewritten to denied. Rarely catches legitimate users (maybe one every few months). When bots get rebuilt and start claiming newer versions, they just update the block. &ldquo;Whack-a-mole, but it does work.&rdquo;</p>
    <p>Advantage: <strong>didn&rsquo;t lock any API access or integrations</strong> because legitimate integrations don&rsquo;t claim to be browser versions.</p>
  </div>
  <div class="section-item">
    <h3>Ongoing bot arms race</h3>
    <p>Justin: bot blocking is a game of whack-a-mole &mdash; &ldquo;once the bots pretend they are version 144, then we&rsquo;ll get 400,000 requests one morning&rdquo; and they just block all 144s. AI can help write those rewrite rules.</p>
    <p>Jeff: has a dedicated sysadmin who &ldquo;attacks this constantly.&rdquo; <strong>Offered to share fail2ban rules and set up a call with &ldquo;Joe&rdquo;</strong> &mdash; contact Jeff directly. Credited Justin for the old browser trick. Applied same rule sets to protect <strong>ArchivesSpace and other digital asset management systems</strong>.</p>
    <p><strong>III currently uses fail2ban</strong> and is <strong>moving to Cloudflare in June/July 2026</strong>. ByWater Solutions (Koha hosting) already uses Cloudflare.</p>
  </div>
</div>

<h3 style="color: var(--navy); margin-bottom: 0.75rem;">Bot Protection Approaches for Sierra</h3>

<table>
  <thead>
    <tr>
      <th>Approach</th>
      <th>Pros</th>
      <th>Cons</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Cloudflare</strong> (reverse proxy/WAF)</td>
      <td>DDoS mitigation, bot filtering, SSL termination, caching, free tier</td>
      <td>Can block staff and integrations if not configured carefully; only HTTP</td>
    </tr>
    <tr>
      <td><strong>F5 BIG-IP</strong></td>
      <td>Full protocol support, session persistence</td>
      <td>$30K/year; &ldquo;weren&rsquo;t really providing much&rdquo; after initial setup</td>
    </tr>
    <tr>
      <td><strong>fail2ban + block lists</strong></td>
      <td>Free, effective for known patterns</td>
      <td>Requires dedicated sysadmin effort; constant maintenance</td>
    </tr>
    <tr>
      <td><strong>III&rsquo;s crawler blocker</strong> (old browser trick)</td>
      <td>Simple, doesn&rsquo;t break APIs/integrations</td>
      <td>Whack-a-mole; bots adapt their version strings</td>
    </tr>
  </tbody>
</table>

<h3 style="color: var(--navy); margin-bottom: 0.75rem;">Key Considerations When Putting Sierra Behind a Proxy</h3>

<div class="section-list">
  <div class="section-item">
    <ul style="margin: 0.25rem 0 0 1.5rem;">
      <li><strong>Get your IP allowlists ready FIRST</strong> &mdash; staff IPs, vendor IPs, discovery layer, OCLC, EZproxy</li>
      <li><strong>Use Admin Corner</strong> in Sierra to see currently connected IPs</li>
      <li><strong>Session affinity is critical</strong> &mdash; Sierra WebPAC is stateful; must use sticky sessions</li>
      <li><strong>SIP2 (port 6001) and Z39.50 (port 210) are TCP, not HTTP</strong> &mdash; Cloudflare can&rsquo;t proxy these</li>
      <li><strong>Client IP pass-through</strong> &mdash; configure <code>X-Forwarded-For</code> / <code>CF-Connecting-IP</code></li>
      <li><strong>Consider a separate hostname</strong> for public vs. internal access</li>
    </ul>
  </div>
</div>

<div class="card">
  <p><strong>See full guide:</strong> <a href="cloudflare-sierra-guide.html">Cloudflare Protection for Sierra ILS &mdash; Practical Guide</a></p>
</div>

<!-- Locations Served / Paging -->

<h2>Locations Served / Paging</h2>

<div class="section-list">
  <div class="section-item">
    <h3>Order of locations served matters</h3>
    <p>Bob: order of locations served matters &mdash; he actually read the manual (hat tip to Dan and Dave Blizinski as knowledge sources).</p>
    <p>Drives the paging list &mdash; pickup location matches the <strong>first group it encounters going down the list</strong>, so supersets must come before subsets or items will fail to page.</p>
    <p>Issue: items getting picked up while the paging list is still being processed. Discussion around title-level priority paging and item-level vs. title-level paging &mdash; a key distinction.</p>
  </div>
</div>

<h3 style="color: var(--navy); margin-bottom: 0.75rem;">Item-Level vs. Title-Level Paging &mdash; Key Differences</h3>

<table>
  <thead>
    <tr>
      <th>Aspect</th>
      <th>Item-Level Paging</th>
      <th>Title Priority Paging</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Slip format</strong></td>
      <td>One slip per item</td>
      <td>One list with all eligible items</td>
    </tr>
    <tr>
      <td><strong>Priority table</strong></td>
      <td>Library Priority table (0&ndash;99)</td>
      <td>Hold Pickup Locations table, Paging Priority field (0&ndash;999)</td>
    </tr>
    <tr>
      <td><strong>Items targeted</strong></td>
      <td>Single item at highest-priority branch</td>
      <td>All eligible items across multiple locations</td>
    </tr>
    <tr>
      <td><strong>Cycling/escalation</strong></td>
      <td>Not built-in</td>
      <td>Automatic &mdash; cycles through priority tiers</td>
    </tr>
    <tr>
      <td><strong>Permission</strong></td>
      <td>358</td>
      <td>394</td>
    </tr>
  </tbody>
</table>

<h3 style="color: var(--navy); margin-bottom: 0.75rem;">Gotchas</h3>

<div class="section-list">
  <div class="section-item">
    <ul style="margin: 0.25rem 0 0 1.5rem;">
      <li>Title Priority Paging and Library Priority tables are <strong>incompatible</strong> &mdash; enabling one disables the other</li>
      <li>Also incompatible with &ldquo;Page Pickup Location First&rdquo; feature</li>
      <li>Adding a new pickup location requires updating paging priority for <strong>all</strong> existing entries (default is 999/lowest)</li>
      <li>Print title paging lists frequently &mdash; at least once/day</li>
      <li>Without &ldquo;Keeping the Title Hold&rdquo; enabled, if all locations reject a page the hold gets cancelled</li>
    </ul>
  </div>
</div>

<h3 style="color: var(--navy); margin-bottom: 0.75rem;">Sierra Documentation</h3>

<div class="section-list">
  <div class="section-item">
    <ul style="margin: 0.25rem 0 0 1.5rem;">
      <li><a href="https://documentation.iii.com/sierrahelp/Content/sril/sril_notices_paging_lists_item.html">Item Paging Lists</a></li>
      <li><a href="https://documentation.iii.com/sierrahelp/Content/sril/sril_notices_paging_lists_title.html">Title Paging Lists</a></li>
      <li><a href="https://documentation.iii.com/sierrahelp/Content/sgcir/sgcir_using_title_pages.html">Using Title Paging Lists</a></li>
      <li><a href="https://documentation.iii.com/sierrahelp/Content/sgcir/sgcir_optional_holds.html">Optional Holds Functionality</a></li>
      <li><a href="https://documentation.iii.com/sierrahelp/Content/sgcir/sgcir_holds_fillhold.html">How Sierra Determines Whether an Item Satisfies a Hold</a></li>
      <li><a href="https://documentation.iii.com/sierrahelp/Content/sril/sril_circ_param_holdshelfmap.html">Hold Pickup Locations Table</a></li>
      <li><a href="https://documentation.iii.com/sierrahelp/Content/sril/sril_circ_param_libpr.html">Library Priority Table</a></li>
      <li><a href="https://iii-itlc.s3.amazonaws.com/LibGuides/LibGuides+Articles+and+Docs/Sierra/Circulation/Articles/CIR+Sierra+HTG+Circulation+Start+Using+Title+Priority+Paging+20220301.pdf">How to Start Using Title Priority Paging (PDF)</a></li>
    </ul>
  </div>
</div>

<!-- Cataloger Concerns -->

<h2>Cataloger Concerns</h2>

<div class="section-list">
  <div class="section-item">
    <h3>Record templates and macros</h3>
    <p>Catalogers have deep workflows baked into Sierra &mdash; <strong>record templates and macros</strong> are critical to cataloger performance. &ldquo;Our catalogers will revolt&rdquo; if classic is removed.</p>
    <p>Switching to Polaris remains a hot topic in the room.</p>
  </div>
</div>

<!-- Closing -->

<h2>Closing Note</h2>

<div class="card">
  <p><strong>IUG 2027 will be in Boston.</strong></p>
