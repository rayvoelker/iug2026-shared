# How Could New Analytics Tools Help Multi-Branch Sierra Systems with Floating Collections? — Tuesday, April 14

**Facilitator:** Elizabeth Wright
**Time:** 10:30–11:30 AM | **Room:** Cook | **Track:** Gatherings

A roundtable discussion among Sierra libraries of varying sizes — from 12-branch systems to a 129-library consortium — sharing practical experience with floating collections, the tools they've built or adopted, and the gaps that remain. An Innovative staff member joined to gather input on Vega Reports priorities.

---

## The Landscape: Who's Floating and How

The group represented a wide cross-section of floating maturity:

| System Size | Float Status | Key Tools |
|-------------|-------------|-----------|
| 79 locations / 39 branches | Active float, fully mapped | Library IQ for shelf mapping |
| 24 branches (Tulsa City County) | Active float | Library IQ, vendor grids for new item distribution |
| 12 locations (growing to 14) | Pilot projects | Custom Sierra API tools for bulk holds |
| 129-library consortium | Exploring — potential new floating member | Sierra float rules |
| Cincinnati & Hamilton County PL | Sierra API development | Custom bulk-hold web app (in development) |

---

## Shelf Mapping & Collection Sizing

Multiple libraries use [Library IQ](https://libraryiq.com) — a cloud-based collection analytics platform — to map their entire collections and set **optimal shelf sizes per area**. Librarians can see at a glance which branches are "pooling" (over capacity) and which are in "drought" (under capacity).

**The gap everyone identified:** knowing you need to move 10 items from branch A to branch B is helpful, but no tool currently provides good criteria for *which specific items* to move. Participants wanted selection filters based on:

- Last checkout date
- Item created date
- Total circulations (including zero-circ items)
- Whether the receiving branch has seen the title recently

[Decision Center](https://documentation.iii.com/product-documentation/decision-center.php) (Innovative's existing analytics product) was discussed but several participants noted it was being de-emphasized. In 2024, Innovative partnered with Library IQ to offer analytics within the Vega LX portfolio, further signaling a strategic shift.

[CollectionHQ](https://collectionhq.com) (Baker & Taylor) was also mentioned as a tool some selectors use for evidence-based stock management — benchmarking, demand-driven acquisition, and identifying underperforming stock. Some libraries use CollectionHQ's list exports to feed into custom transfer workflows.

---

## Floating in Practice: What Works and What Doesn't

### Practical approaches

**Tulsa City County Library** (24 branches) shared their mature floating workflow:

- All branches mapped to "shop locations" with defined shelf capacity
- Staff instructions for pulls: "Send 100 picture books. Pull A through Z. Don't pull everything from one area. Avoid duplicates."
- Typical float volume: **50–300 items** between branches at a time
- Title-level pick lists (from Decision Center or Library IQ) were tried and abandoned — **nobody has time** to process item-by-item lists when you're moving 50+ items

### The resistance curve

A consistent theme across participants: **initial resistance is strong, but libraries don't want to go back.**

- Branch staff have deep ownership of "their" shelves and are protective of what's on them
- If you say "pull 20 items," staff will pull the worst items — they want to keep the best for their customers
- One system avoided floating juvenile nonfiction entirely because they feared staff would game the system
- **But:** after about a year of floating, one system offered to let branches opt out — they unanimously refused. The constant refreshment of paperbacks, media, and large print was too valuable to give up.

### Delivery logistics drive everything

Float timing decisions are surprisingly constrained by delivery schedules:

- One system sends float requests Monday morning (the busiest delivery day) because staff can't ship Monday — but if they get the list Monday afternoon, they can start sending Wednesday when trucks are lighter
- The day with the lowest delivery volume is the best day to trigger automated float requests
- As one participant put it: **"It's funny how delivery drives everything."**

---

## Bulk Holds: Using the Hold System to Move Collections

### The problem

When branches need items for programs, displays, or to fill collection gaps, the standard answer is "just place holds." But this is **tedious** — staff have to search for individual titles, find available copies at other branches, and place holds one at a time.

### Approach 1: Disposable patron accounts + barcode import

One library is building a **web application** using the Sierra REST API that allows staff to:

1. Import a list of barcodes (a "shopping list") — sourced from CollectionHQ, Library IQ, or manual selection
2. Place bulk item-level holds to route everything to a target branch
3. Track the status of all holds through the web app rather than digging through the Sierra client

**Key innovation — disposable patron accounts:** Sierra enforces a ~2,000 hold limit per patron card. Rather than juggling multiple admin cards, this tool creates a **temporary patron account on the fly** via the API with:

- Patron expiration set to 30 days out
- "Not needed after" date on all holds matching the same 30-day window
- The entire batch becomes a self-contained, trackable unit tied to one disposable account
- After 30 days, both the patron and unfilled holds auto-expire

### Approach 2: Bib-based and patron-based bulk placement

A consortium participant shared existing tools that work in the opposite direction:

| Tool | Input | Output |
|------|-------|--------|
| Patron-to-bib | Bib record number + patron CSV | Hold placed for every patron on that bib |
| Bib-to-location | Item records or bib number + target location | Holds placed to send all items to a location |

Each library in their consortium maintains a **virtual admin patron** for this purpose. For their floating pilot, they ran a **weekly automated script**: any item sitting on the shelf longer than X days gets a hold placed to send it home — "basically just an API call and a SQL script."

### Approach 3: Item status changes instead of holds

Several participants raised concerns about using holds for collection movement:

- Holds are **contentious** — they can impact patron access to items
- If bulk holds get "hung up," they may block legitimate patron requests
- Heavy hold volume adds paging burden to branch staff

**Alternative discussed:** use **item status codes** instead. Sierra's Circa tool already supports batch status changes via barcode scanning. The group envisioned:

- A new dynamic "shopping" status code (similar to how "missing" has progressive stages)
- Auto-expiration on the status after a set period
- Automated status changes via the API

The blocker: **Sierra Scheduler can't currently execute API calls.** If it could, libraries could chain together Create Lists queries with API-driven status changes on a schedule — a frequently requested capability.

### Sierra API limitation: holds are not first-class citizens

A significant technical limitation surfaced: when you place a hold via the Sierra REST API's [POST endpoint](https://techdocs.iii.com/sierraapi/Content/zAPIs/patronAPI_holds.htm), the response is **HTTP 204 No Content** — the body is empty and **no hold ID is returned**. Since holds aren't a first-class record type in Sierra (they have no record number), there's no reliable way to programmatically track a specific hold after placement.

**Workaround:** immediately GET the patron's hold list after placing, and identify the new hold by timestamp or record number. This is fragile and doesn't scale well for bulk operations.

**Sierra API reference:**
- [API documentation](https://techdocs.iii.com/sierraapi/Content/titlePage.htm) (currently v6.6)
- [Interactive sandbox](https://techdocs.iii.com/sierraapi/Content/interactive.htm)
- [Developer portal](https://innovative.libguides.com/Developer/Sierra)

---

## The Biggest Gap: Tracking Where Items Have Been

### The core problem

Sierra stores only **current state** for item locations. There is no built-in way to answer:

- Where has this item been over the last year?
- How long does it take for an item to get from branch A to branch B?
- What is the actual flow pattern of our floating collection?

As one participant said: **"Administration always asks how long it takes to get from A to B. And you can't answer that."**

### What's missing from transaction data

- Items that pass through a **sorter** while already checked in produce **no circulation transaction** — there's no status change, so nothing is recorded
- Reconstructing item journeys from existing circulation transaction data is possible but "unwieldy"
- There's no equivalent of a shipping/tracking log for physical items

### Workarounds in use

| Approach | How it works | Limitations |
|----------|-------------|-------------|
| **Collection snapshots** | Dump entire collection locations at regular intervals, diff over time | Storage-heavy, requires custom tooling |
| **Annual checkout rankings** | Rank branches by format checkout frequency to inform float decisions | Only annual granularity, reactive not predictive |
| **Inventory check-in analysis** | Check in every item over a month; analyze where things ended up | Recent improvement — inventory check-ins now create transactions (they didn't used to) |

### The data lake hope: Vega Reports

[Vega Reports](https://iii.com/whats-new/smarter-insights-ahead-vega-reports-launching-soon/) — which launched April 7, 2026 — is expected to create a **data lake** with regular snapshots of ILS data. If it captures item location changes over time, it could finally solve the historical tracking problem. Currently Vega Reports surfaces Vega Discover data (visitor stats, engagement trends, search activity); Innovative is working on integrating Polaris ILS and OverDrive checkout data. Sierra ILS integration is on the roadmap.

**Enhancement request:** participants strongly advocated for the circulation transaction system to capture more operations — not just checkouts and returns, but sorter pass-throughs, in-transit state changes, and inventory scans. The recent addition of inventory check-in transactions was cited as a positive step in this direction.

---

## Smart Routing at Check-In: The Feature Everyone Wants

### The concept

Instead of float rules that simply say "this item type floats between these locations," the system would make **intelligent routing decisions at check-in** based on real-time collection state:

**Example scenario:**
> A copy of a popular title is returned at Branch A. The system checks: Branch A already has 8 copies. Branch B has only 2 copies and hasn't seen this title in 18 months. The system creates a transit request to send the item to Branch B.

### Proposed parameters

- **Maximum duplicates per branch** — "this branch can only have 3 copies"
- **Recency filter** — "only send to branches that haven't had this title in X months"
- **Capacity awareness** — if no branch qualifies by title, send to the branch with the most available shelf space
- **Format-aware** — different rules for different material types

### Precedents that prove it's possible

- **Automated sorters** already implement routing logic at check-in based on item attributes — proving the concept works at the system level
- **Polaris** has functionality in this direction (referred to as "jacket" by participants)
- [Lyngsoe Systems' IMMS](https://lyngsoesystems.com/library/intelligent-material-management-system) (Intelligent Material Management System) is an RFID-based platform that tracks every item movement and supports automated routing — a hardware-based version of what this group wants in software
- Sierra's own [floating collection configuration](https://documentation.iii.com/sierrahelp/Content/sgcir/sgcir_floating_collection.html) supports rule-based float at check-in, but lacks the dupe-aware, capacity-aware intelligence discussed here

### Idea Exchange submission planned

Elizabeth Wright committed to submitting this as an Idea Exchange enhancement request. The group discussed strategy for building support:

- Reach out to other floating libraries to vote
- Even contact non-floating libraries: "You might want to float someday, and if you do, this would be a really good feature"
- Don't just click "yes" — **write a comment with your library's use case**; substantive comments carry more weight

---

## New Item Distribution in Floating Systems

A challenge unique to floating: **how do you ensure new acquisitions are distributed fairly when items naturally drift toward high-demand branches?**

### Approaches discussed

| Strategy | How it works | Who uses it |
|----------|-------------|-------------|
| **Rotating vendor grids** | Acquisitions grids cycle through branches so each gets proportional new items | Tulsa City County Library |
| **Assign to one branch** | For high-hold items (Lucky Day / Quick Picks), assign to one branch — holds will distribute them | Multiple participants |
| **Percentage-based allocation** | Small branches get the same *percentage* of new items as large branches | Tulsa |

**The underlying tension:** small branches with heavy reader populations see popular items float away quickly. Without deliberate new-item allocation, these branches would perpetually feel underserved. As one participant said: **"We don't want our small branches to say we never get anything new."**

Some libraries actively weed more aggressively at branches that accumulate float, while others use checkout data to verify that floating items are actually being used at their new locations.

---

## Consortium Floating: Can One Library Float Inside a Non-Floating Consortium?

An interesting edge case: a library with an existing floating collection wants to join a 129-library consortium where no one else floats. Would their float rules break the consortium?

**The group's consensus: it would just work.** Sierra's float rules are scoped to the floating library's own locations. When a floating library's item is returned at a non-floating consortium member, it goes in transit back to its owning location — the same behavior that already happens for all non-floating consortium items. The floating library would set up float rules for their own branches, and the rest of the consortium would be unaffected.

The only real challenge is convincing the library to migrate from their current ILS (they're currently on a competing system) to Sierra.

---

## Vega Reports: First Look and Feedback

An Innovative staff member (presenting in the later session [Vega Reports for Discover and Beyond](https://iug2026.sched.com/)) joined the discussion to gather input on reporting priorities.

### Technical architecture

| Component | Detail |
|-----------|--------|
| **Platform** | [Metabase](https://www.metabase.com/) — open-source BI tool ([GitHub](https://github.com/metabase/metabase)) |
| **Query builder** | Visual drag-and-drop interface; generates SQL behind the scenes |
| **SQL access** | Direct SQL editor for power users (role-dependent) |
| **Role model** | Admins: query builder + SQL; Collection staff: query builder only |
| **Current data** | Vega Discover metrics (visitor stats, engagement, search activity) |
| **Roadmap** | Polaris ILS data, OverDrive checkout data, Sierra ILS data |

The query builder's SQL transparency was well-received: staff can build a query visually, then **see and copy the generated SQL** — useful for learning, sharing, and fine-tuning. As one participant noted, you could get 90% of the way with the builder and then hand the SQL to a data analyst for the last 10%.

### Feedback from the group

**Focus on smaller libraries first.** Large library systems typically have data analysts who can write SQL and pull whatever they need. The biggest impact for a first release would be **standard, ready-to-use reports** that medium and small libraries can run without technical staff. The group suggested identifying **10 standard Sierra reports** as a starting point.

**Speed is critical.** Decision Center's biggest complaint: it frequently enters an "infinite loop of loading" when complex filter criteria are applied. For Vega Reports to succeed, query performance must be a priority from day one.

**Survey incoming.** Innovative plans to send a survey to understand which Decision Center and Web Management Reports are most used, to help shape the first release.

### Comparable open-source tool: Datasette

[Datasette](https://datasette.io/) ([GitHub](https://github.com/simonw/datasette)) by Simon Willison was mentioned as a comparable tool already in use at one library for exploring and publishing library data. Key features relevant to this audience:

- Publishes any SQLite database as an **explorable website** with a built-in JSON API
- **Faceted browsing** — useful for exploring circulation stats, MARC field distributions, collection breakdowns
- Full-text search across database tables
- Plugin ecosystem for visualization, authentication, and export
- Companion tool [sqlite-utils](https://sqlite-utils.datasette.io/) converts CSV/JSON into SQLite from the command line
- One-command deployment to cloud platforms
- A lightweight alternative to standing up a full BI stack

---

## The Idea Exchange & MEEP: How Enhancement Requests Actually Work

The session closed with a practical discussion about the [Idea Exchange](https://ideas.iii.com) and how to effectively advocate for enhancements.

### How the process works

1. **Submit & vote** — Anyone can submit ideas at [ideas.iii.com](https://ideas.iii.com) (UserVoice platform). All Innovative customers can vote and comment.
2. **Working group review** — IUG Working Groups (e.g., the Sierra MEEP group) review top-voted ideas each cycle.
3. **Sizing** — Innovative product owners estimate development effort in points.
4. **Final vote** — IUG member site contacts cast the deciding votes. Each cycle allocates **500 development points** — which may yield one large feature or several smaller ones.
5. **Implementation** — Innovative commits to delivering winners within **12 months**.

### Recent Sierra 6.7 MEEP winners (targeted Q4 2026)

1. Automatic SSL Certificate Renewal
2. REST API endpoint to update patron "last circ activity date"
3. Allow use of spine label print templates in Create Lists

Source: [Sierra 6.7 MEEP winners announcement](https://forum.innovativeusers.org/t/winning-ideas-from-sierra-6-7-meep-vote/2883)

### Practical advice from the group

- **Know who votes at your library.** Each IUG member site has a designated voter — find out who that person is.
- **Lobby directly.** When an idea you care about reaches the final round, tell your voter: "This will change our daily operations. Please prioritize it."
- **Bridge the knowledge gap.** If your IT person votes but doesn't do collection work, make sure they understand *why* a collection management feature matters. And vice versa.
- **Write substantive comments.** Don't just click the vote button — describe your library's specific use case. Comments with real-world context carry more weight.
- **Cross-pollinate.** Reach out to peer libraries and encourage them to vote for ideas that benefit the broader community.

Details: [MEEP overview](https://www.innovativeusers.org/member_exclusive_enhancement_p.php) | [Idea Exchange FAQ](https://www.innovativeusers.org/idea_exchange_-_faq.php)

---

## Key Themes

1. **Floating works, but the tools haven't kept up.** Libraries that float are committed to it, but Sierra's tooling for managing float — especially around intelligent routing, item tracking, and bulk operations — lags behind operational needs.

2. **Libraries are building their own tools.** Multiple participants have built custom applications using the Sierra REST API to fill gaps: bulk hold placement, automated return-to-home scripts, collection movement tracking. This is both a testament to the API's value and an indicator of unmet product needs.

3. **Historical item tracking is the biggest missing capability.** Every library at the table wanted to know where items have been, not just where they are now. Vega Reports' data lake concept could address this if it captures location snapshots over time.

4. **Smart routing at check-in is the most-wanted feature.** Capacity-aware, dupe-aware routing that doesn't require hardware sorters was the consensus top priority for the Idea Exchange.

5. **Analytics tools need to serve non-technical staff first.** The libraries with data analysts can already get what they need via SQL. The first release of any new reporting tool should prioritize ready-to-use reports for smaller libraries without dedicated technical staff.

---

## Further Reading

### Floating Collections
- [To Float or Not To Float](https://www.libraryjournal.com/story/to-float-or-not-to-float-collection-management) — Library Journal overview of implementation considerations
- [Rethinking Floating in Collection Development](https://www.urbanlibraries.org/innovations/rethinking-floating-in-collection-development) — Urban Libraries Council innovation brief
- [Floating Collections Review and Change](https://www.urbanlibraries.org/innovations/floating-collections-review-and-change) — ULC case study on modifying or turning off float
- [Benefits and Drawbacks of Floating Collections](https://cdr.lib.unc.edu/downloads/3b591d031?locale=en) — UNC research paper (75% of respondents found redistribution challenging)
- [Are Floating Collections the Answer?](https://www.collectionhq.com/are-floating-collections-the-answer/) — collectionHQ analysis
- [Floaters: Are Floating Collections Really Delivering?](https://librarianpete.substack.com/p/floaters-are-floating-collections) — critical perspective on float outcomes
- *Floating Collections* by Wendy K. Bartlett — [ALA LRTS book review](https://journals.ala.org/lrts/article/view/2758/2739)

### Tools & Platforms Referenced
- [Library IQ](https://libraryiq.com) — collection analytics and shelf mapping
- [CollectionHQ](https://collectionhq.com) — evidence-based stock management (Baker & Taylor)
- [Vega Reports announcement](https://iii.com/whats-new/smarter-insights-ahead-vega-reports-launching-soon/) — Innovative's new reporting platform
- [Metabase](https://www.metabase.com/) — open-source BI platform powering Vega Reports
- [Datasette](https://datasette.io/) — open-source data exploration and publishing tool
- [sqlite-utils](https://sqlite-utils.datasette.io/) — companion CLI for Datasette
- [Lyngsoe IMMS](https://lyngsoesystems.com/library/intelligent-material-management-system) — RFID-based intelligent material management

### Sierra Technical References
- [Sierra REST API docs](https://techdocs.iii.com/sierraapi/Content/titlePage.htm) (v6.6)
- [Sierra API interactive sandbox](https://techdocs.iii.com/sierraapi/Content/interactive.htm)
- [Sierra developer portal](https://innovative.libguides.com/Developer/Sierra)
- [Sierra floating collection configuration](https://documentation.iii.com/sierrahelp/Content/sgcir/sgcir_floating_collection.html)
- [Decision Center documentation](https://documentation.iii.com/product-documentation/decision-center.php)

### Idea Exchange & MEEP
- [Idea Exchange](https://ideas.iii.com) — submit and vote on enhancement requests
- [MEEP overview](https://www.innovativeusers.org/member_exclusive_enhancement_p.php)
- [Idea Exchange FAQ](https://www.innovativeusers.org/idea_exchange_-_faq.php)
- [Sierra 6.7 MEEP winners](https://forum.innovativeusers.org/t/winning-ideas-from-sierra-6-7-meep-vote/2883)
