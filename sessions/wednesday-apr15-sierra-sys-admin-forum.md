# Sierra Sys Admin Forum — Wednesday, April 15

**Type:** Forum / Open Discussion
**Product:** Sierra
**Moderated by:** Jeff (UNC Chapel Hill) and Stephanie Brew — Jeff's last time hosting the forum

## Topics

### Sierra vs. Polaris — Migration Considerations

- Show of hands: 2 definite, 4 maybe considering Sierra-to-Polaris migration
- **Polaris pricing is similar** to Sierra renewal costs, but there's an additional unknown implementation cost on top. Pricing should be negotiable — one attendee just renewed Sierra for 3 more years at comparable rates.
- A sales rep deflected on pricing at lunch — attendee pushed back: "I'm the one who has to get it approved... Our board isn't going to just say oh yeah spend another hundred thousand"
- One attendee: "I feel like it's now or five years from now" — renewal cycle is the natural decision point
- **A consortium hired Marshall Breeding** for a landscape report. After 20 years on Sierra, his conclusion: **"Stay on Sierra for the moment and do a deep dive in about three years, maybe five."**
- **III themselves recommended staying on Sierra** — at PLA, an attendee's assistant director spoke with III reps and "that was their recommendation. Stay on Sierra. You're good here."
- An attendee evaluated Polaris: "It couldn't be just a hair better, it had to be like this much better, and it wasn't... not worth everything that comes with the migration"
- **End users driving the push** — people who migrated Sierra-to-Polaris said the common denominator was end users wanting "something that looked a little bit more modern"
- Staff hired from Polaris libraries miss things from a technical perspective
- **True cost of migration** extends far beyond the contract: Aspen discovery layer migration, 72+ hours of downtime, communications team, staff training, morale. "Your staff want Polaris because it is pretty but do they want to go through all of that?"
- A consortium's ILS RFP took **9 months**
- Consortium constraints limit choices: "Our only two choices are Sierra or Polaris"
- Contact **Derrick Brown** for a Polaris demo — someone offered to show how Polaris works

**Invoicing / Order Record Issue:**
- Currently using Sierra invoicing and order records
- Issue: small standalone library stopped using Sierra invoicing when municipality switched finance systems. A year and a half later, unprocessed invoices are blocking order record deletion (~6,000 records). Can't do global updates on status codes — would have to change each one manually. Innovative support confirmed the problem and has been manually force-clearing on their end.
- **Jeremy's solution (acquisitions expert):**
  1. Go to **Funds function** → **Tools dropdown** → **"Clear payment history"** and force clear
  2. Ideal method: run a **Fund Activity Report** first to get a printout of all transaction info, then clear
  3. The shortcut clear may take **30-45 minutes** to complete
  4. Once invoices are cleared, order records become unlocked
  5. Put order records into a **review file** and use **batch cancel** to clear them in bulk
  6. If the clear doesn't work, Innovative support can help via a support ticket

### Migrating to Koha

- Someone asked about migrating from Sierra to Koha
- Another attendee came from Koha to Sierra — they loved the flexibility (direct SQL querying was great)
- Budget pressure driving Koha interest: "We don't have concrete plans but we are getting a lot of budget pressure to look at another ILS"
- Jeremy (Minuteman Library Network, MA): other MA consortiums are on Koha/Evergreen; as staff move between libraries there's "an influx of staff who are used to open source systems... Sierra is sort of railing to them." But their libraries "are extremely happy"
- **Koha struggles with large catalogs** — Jeff (UNC): "We have 20 million records, almost 23 million... large library consortiums struggle with Koha and they could not handle our records"
- Someone noted they feel locked into **Lyngsoe Systems** (Lyngsoe IMS — automated materials handling / book sorter). Only certain ILS vendors support integration: Sierra supports it, SirsiDynix supports it, Polaris is working on it. This significantly limits ILS migration options.
- General sentiment: migrating away from Sierra is too painful — too many moving pieces involved
- Jeff: "The ILS you have is the best ILS"
- Reference to studies on ILS migration:
  - [ILS Challenges and Opportunities: A Survey of U.S. Academic Libraries with Migration Projects](https://www.sciencedirect.com/science/article/abs/pii/S0099133309000275) (Journal of Academic Librarianship, 2009)
  - [Challenges of ILS Migration in Academic Libraries](https://digitalcommons.unl.edu/libphilprac/2535/)
  - [Experiences of Migrating to an Open-Source ILS](https://ital.corejournals.org/index.php/ital/article/download/2268/pdf)
- Discussion about RFP processes — big institutional pressure to stay with current ILS, but many staff have had exposure to other systems and know what else is out there
- Sierra has more maturity in some areas compared to other ILS options
- Victor: his library has a "sister library" on Koha — **"Acquisitions and cataloging are not quite as mature as Sierra."** His advice: identify what features are essential and make sure the new ILS has them. "That kind of frames the conversation into that specific set of requirements. As opposed to like, well the other one was nice, but functionally speaking that doesn't do anything."
- Victor's pragmatic filter for complaints: "We have people say oh we hate Sierra... some of those opinions may be valid but it's one person and we're catering to over 99%."
- Jeremy: "The system you start with is kind of what you imprint on" — echoed by multiple attendees
- Switching to Polaris remains a hot topic in the room
- Catalogers have deep workflows baked into Sierra — **record templates and macros** are critical to cataloger performance. "Our catalogers will revolt" if classic is removed.

### Sierra's Future / Longevity — HOT TOPIC

- **Sierra is not selling well domestically** — Jeff: "I don't think it's any secret that they're not selling a lot of Sierra subscriptions in the United States. But it sounds like it is doing better overseas." Saudi Arabia deploying Sierra for 175 libraries.
- **Public libraries are going Polaris** — III would "absolutely encourage them to buy" Polaris for public libraries
- **IUG attendance ratio shifting**: roughly **2/3 Polaris, 1/3 Sierra** — Jeff predicted "that's probably going to become more lopsided"
- "One company with two competing products seems curious" — the elephant in the room about Clarivate/III having Sierra, Polaris, Millennium (legacy), and Leap all active
- There are still a few Millennium customers
- The **Millennium-to-Sierra migration was a "nothing burger"** — Jeff was a beta institution: staff were terrified but "Oh, new color scheme. Great." Intentional design decision to keep it similar, but "the interface felt dated already when it came out." "They got rid of the mountains" (Sierra splash screen reference)

### The Dated Look

- The "looks old" complaint is the #1 thing Polaris fans say
- Full quote: **"Pretty things are usually shallow. If you focus on the UI first, the power behind it is not as strong. That's how databases work."**
- Jeff's pushback: "Why does the look matter more than the functionality? Is it to please my younger users, my Gen Zers?"
- **"This is not an end user system. This is not meant to be used by someone who has never been trained before."**
- **UNC's staffing situation:** lost 55 staff due to hiring freeze — migration impossible without adequate staff. Part of Triangle Research Library Network (Duke, NC State, NC Central). Getting Rapido because partner institutions moved to Alma, but don't have budget/staff to migrate.

### Overrides / Vega

- Overrides are a problem — consortium/shared system admin actively discourages staff from using overrides to reduce downstream data cleanup
- **Patron override coming to Vega** — once it arrives, front-line staff expected to "stop using the actual Sierra client and go exclusively in Vega for everything"

### Sierra Desktop App (SDA) vs. Sierra Web

- Remote desktop user reporting issues with SDA — failure to log in or initialize once or twice a week. **Updating the JRE** to the most recent version dramatically improved SDA startup ("night and day"), though "not perfect"
- Growing sentiment that more reliance on Sierra Web is important — one speaker noted "Leap is going to be a more sustainable platform than the Sierra desktop app"
- Current split at some libraries is ~50-50: front desk/circ on Sierra Web, collection management staff still on SDA
- **ERM (Electronic Resource Management) is bad in Sierra Web** — electronic resources person at one library "hates Sierra Web" and refuses to give up the desktop app. Sierra Web only works properly in Chrome, not Firefox.
- **Pagination is painful in Sierra Web** — editing records that get paginated is bad enough to drive users back to SDA
- **Workflows vs. permissions confusion**: one user couldn't see expected menu functions despite having all permissions — workflows (which control dropdown menus) are configured separately from permissions

### Accessibility / WCAG

- Multiple libraries are **getting "dinged" about accessibility** of the classic WebPAC
- WebPAC can't be turned off — even if you don't point patrons to it, it's still publicly accessible, which "alarms our accessibility people"
- Libraries want to **hide classic catalog from public but keep it for staff** — no one has found a solution yet. Firewall approaches tried; ticket open with Innovative.
- A "very small core set of patrons" still use the classic catalog and are already complaining
- **Catalogers "will revolt"** if classic is removed entirely — staff still depend on it
- **Patron registration forms** are served through WebPAC — another dependency that blocks removal
- Innovative may be "working with somebody to figure out how to disable it" — uncertain
- Some exploring **Vega Discover** as a WebPAC replacement
- **Templates cannot fix the accessibility issues** — "We fixed everything you can fix using the templates." The remaining failures are in server-side code: "Your template calls this function and then magic happens on the back end, and the magic is broken. You can't fix it in post."
- Good to see other people concerned about WCAG compliance

### Circ Active / Patron Record Updates

- Bulk updating patron records is difficult because the circ active date gets updated whenever a patron record is modified (including via API) — makes it unreliable for purging inactive patrons
- **Mike Dykus (Clarivate) confirmed a new API enhancement coming:** for e-vendors (Hoopla, Overdrive) validating patrons, the record won't get its "last updated" date changed, but the circ active date can be set to indicate the patron is using e-resources. However, it does NOT take a date parameter to backdate. Toggle is "all or nothing."
- **Action item:** everyone should contact Hoopla/Overdrive to push them to adopt the new validation method
- Someone has a script workaround for this issue

### Cloudflare Protection

- Someone implemented Cloudflare on Monday morning to stop bot/DDoS attacks — it stopped the bots **but also blocked all staff** from Sierra and Sierra Web. Associated resources authenticating against Sierra also broke. They were "desperately trying to get lists of IPs from different vendors" to whitelist.
- Advice: become "best friends with your networking team" — use **Admin Corner** in Sierra to get list of currently connected IPs to feed to firewall allowlist
- Another library's firewall upgrade broke Sierra connectivity because "they didn't really consider Sierra before they upgraded the firewall"
- **F5 experience (Bambi, UNC — bambi@unc.edu):** went behind F5 for bot control starting 2024-2025, cost **$30,000/year** and "they weren't really providing much after that initial catch up." Switched to block lists and fail2ban "in a fairly robust way." Set up a **separate hostname** — public-facing domain behind F5 for bot protection, different one for internal services. Currently "hardly any bot now" on Sierra, but digital library hosts still getting hit (38K-120K bot attacks daily). **Offered to share setup via email.**
- **Innovative's crawler blocker ("old browser trick"):** III can put a blocker on your Sierra host — if a client claims to be a browser version more than 3 versions old, it gets blocked. Everything rewritten to denied. Rarely catches legitimate users (maybe one every few months). When bots get rebuilt and start claiming newer versions, they just update the block. "Whack-a-mole, but it does work." Advantage: **didn't lock any API access or integrations** because legitimate integrations don't claim to be browser versions.
- Justin: bot blocking is a game of whack-a-mole — "once the bots pretend they are version 144, then we'll get 400,000 requests one morning" and they just block all 144s. AI can help write those rewrite rules.
- **Jeff:** has a dedicated sysadmin who "attacks this constantly." **Offered to share fail2ban rules and set up a call with "Joe"** — contact Jeff directly. Credited Justin for the old browser trick. Applied same rule sets to protect **ArchivesSpace and other digital asset management systems**.
- **III currently uses fail2ban** and is **moving to Cloudflare in June/July 2026**
- ByWater Solutions (Koha hosting) already uses Cloudflare
- Some discussed setting up a **separate hostname** — public-facing behind Cloudflare, separate for internal services — but called it "very unwieldy"

**Bot Protection Approaches for Sierra:**

| Approach | Pros | Cons |
|---|---|---|
| **Cloudflare** (reverse proxy/WAF) | DDoS mitigation, bot filtering, SSL termination, caching, free tier | Can block staff and integrations if not configured carefully; only HTTP |
| **F5 BIG-IP** | Full protocol support, session persistence | $30K/year; "weren't really providing much" after initial setup |
| **fail2ban + block lists** | Free, effective for known patterns | Requires dedicated sysadmin effort; constant maintenance |
| **III's crawler blocker** (old browser trick) | Simple, doesn't break APIs/integrations | Whack-a-mole; bots adapt their version strings |

**Key considerations when putting Sierra behind a proxy:**
- **Get your IP allowlists ready FIRST** — staff IPs, vendor IPs, discovery layer, OCLC, EZproxy
- **Use Admin Corner** in Sierra to see currently connected IPs
- **Session affinity is critical** — Sierra WebPAC is stateful; must use sticky sessions
- **SIP2 (port 6001) and Z39.50 (port 210) are TCP, not HTTP** — Cloudflare can't proxy these
- **Client IP pass-through** — configure `X-Forwarded-For` / `CF-Connecting-IP`
- **Consider a separate hostname** for public vs. internal access

> **See full guide:** [Cloudflare Protection for Sierra ILS — Practical Guide](../resources/cloudflare-sierra-protection.md)

### Locations Served

- Bob: order of locations served matters — he actually read the manual (hat tip to Dan and Dave Blizinski as knowledge sources)
- Drives the paging list — pickup location matches the **first group it encounters going down the list**, so supersets must come before subsets or items will fail to page
- Issue: items getting picked up while the paging list is still being processed
- Discussion around title-level priority paging
- Item-level vs. title-level paging — key distinction being discussed

**Item-Level vs. Title-Level Paging — Key Differences:**

| Aspect | Item-Level Paging | Title Priority Paging |
|---|---|---|
| Slip format | One slip per item | One list with all eligible items |
| Priority table | Library Priority table (0-99) | Hold Pickup Locations table, Paging Priority field (0-999) |
| Items targeted | Single item at highest-priority branch | All eligible items across multiple locations |
| Cycling/escalation | Not built-in | Automatic — cycles through priority tiers |
| Permission | 358 | 394 |

**Gotchas:**
- Title Priority Paging and Library Priority tables are **incompatible** — enabling one disables the other
- Also incompatible with "Page Pickup Location First" feature
- Adding a new pickup location requires updating paging priority for **all** existing entries (default is 999/lowest)
- Print title paging lists frequently — at least once/day
- Without "Keeping the Title Hold" enabled, if all locations reject a page the hold gets cancelled

**Sierra documentation:**
- [Item Paging Lists](https://documentation.iii.com/sierrahelp/Content/sril/sril_notices_paging_lists_item.html)
- [Title Paging Lists](https://documentation.iii.com/sierrahelp/Content/sril/sril_notices_paging_lists_title.html)
- [Using Title Paging Lists](https://documentation.iii.com/sierrahelp/Content/sgcir/sgcir_using_title_pages.html)
- [Optional Holds Functionality](https://documentation.iii.com/sierrahelp/Content/sgcir/sgcir_optional_holds.html)
- [How Sierra Determines Whether an Item Satisfies a Hold](https://documentation.iii.com/sierrahelp/Content/sgcir/sgcir_holds_fillhold.html)
- [Hold Pickup Locations Table](https://documentation.iii.com/sierrahelp/Content/sril/sril_circ_param_holdshelfmap.html)
- [Library Priority Table](https://documentation.iii.com/sierrahelp/Content/sril/sril_circ_param_libpr.html)
- [How to Start Using Title Priority Paging (PDF)](https://iii-itlc.s3.amazonaws.com/LibGuides/LibGuides+Articles+and+Docs/Sierra/Circulation/Articles/CIR+Sierra+HTG+Circulation+Start+Using+Title+Priority+Paging+20220301.pdf)

---

**IUG 2027 will be in Boston.**
