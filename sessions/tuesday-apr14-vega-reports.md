# Vega Reports and Analytics

**Session Date:** Tuesday, April 14, 2026
**Presenter:** Jovana Raskovic, Product Manager (Belgrade office)
**IUG Session Title:** "Vega Reports for Discover and Beyond" (Kansas City Room)
**Company:** Clarivate / Innovative
**Photos:** Jeremy Goldstein (jmgold42@gmail.com)
**Photo files:** `photos/vega-reports/IMG_0363.JPG` through `IMG_0375.JPG`
**Transcript (cleaned):** [`transcripts/vega-reports-transcript-clean.md`](../transcripts/vega-reports-transcript-clean.md)
**Transcript (raw STT):** [`transcripts/vega-reports-raw.txt`](../transcripts/vega-reports-raw.txt)

---

## Overview (Slide 1 - IMG_0363)

**Vega Reports and Analytics** — One intelligent BI platform that unifies reporting and analytics across the Public ecosystem, delivering modern, user-friendly insights powered by a secure data lakehouse, with the scalability to drive cross-product intelligence and fuel future innovation.

Four pillars:
- **Streamlined Staff Flows** — Single log in; ILS and Vega data in one place
- **Automated & Intelligent** — AI Tools; Modern visuals
- **Secure & Private** — Your data protected; GDPR, CCPA compliant
- **Unique Insights** — 3rd Party Data; Engagement reporting

**Consortia and International Ready**

---

## Setup & Access — Vega Reports for Discover (Slides 2-4 - IMG_0364, 0365)

1. Requires an active **Vega Discover** subscription. Vega Reports is included at no additional cost.
2. **Super Admin** at the library can access Vega Discover User Management and assign roles:
   - **Reports Admin**
   - **Reports Consumer**
   - Both roles can be assigned at any site of the library level (top right corner)
   - Role hierarchy follows the same structure already used in Vega Discover
3. Select the edit icon next to a staff member to choose between Reports Consumer or Reports Admin
4. Once assigned, **Vega Reports** automatically appears in the left-hand navigation menu under settings (Library details > Users & roles > Integrations > Interface configurations > **Vega Reports**)
5. Shows "Vega Discover Dashboard" with tabs: **Patron Analytics**, **Search Analytics**, **Marketing Analytics**

---

## Building Reports (Slides 5-7 - IMG_0366, 0367, 0368)

### Option 1: Query Builder (IMG_0366)
Simple select-option menu interface:
- **Data:** Select data source (e.g., Fund Events)
- **Join data:** Join tables (e.g., Fund Events + Fund Static) with field selection (Date, Specific, Fund Type...)
- **Filter:** e.g., "Last Time is in the previous month"
- **Summarize:** e.g., Sum of Fund Events, with Sub-Totals by Fund Description
- Toolbar: Filter, Summarize, Join data, Sort, Row limit, Custom column

### Option 2: Native SQL Query (IMG_0367)
Direct SQL access. Example shown:
```sql
SELECT
    tt.track_type_name,
    SUM(te.num_events) AS sum
FROM "discover".track_events te
INNER JOIN "discover".track_types tt
    ON te.track_type_id = tt.id
WHERE
    te.last_time >= CAST('2024-01-01 00:00:00Z' AS timestamp)
    AND te.last_time < CAST('2025-01-01 00:00:00Z' AS timestamp)
GROUP BY tt.track_type_name
ORDER BY tt.track_type_name ASC
```

### Option 3: Choose Your Visualization (IMG_0368)
Both approaches let you visualize queried data. Chart types available:
- Number, Gauge, Progress, Funnel, Map, Table, Pivot Table
- Bar chart, Line chart, and others
- Will auto-populate the most relevant visualization for your dataset

---

## Example: Digital and Physical Checkouts Insights (Slide - IMG_0369)

- **No. of checkouts** — bar chart comparing Audiobook, E-magazine, E-ebook over monthly periods (1/2025–1/2026)
- **Top 100 circulated Titles** — donut chart (7,570 total) broken down by format: Books (36,778), Video (14,919), Audio (10,488), Magazine (5,488), etc.

**Track Trends and Usage Patterns:**
1. Track a variety of trends across different time frames
2. Identify the most popular titles
3. See whether there is an overlap between print and digital checkouts

---

## Next Steps / 2026 Roadmap (Slide - IMG_0370)

2026 Deliveries — aligned with Vega Suite Monthly Release schedule

### Vega Reports for Discover
- **Initial Roll Out Complete**
- All customers by April 7th
- Rest of customers by May 5th
- Monthly releases with Vega Suite June and beyond
- Future: Additional data points — Staff Audit, Integration with Programs and Mobile data

### Vega Reports for Polaris
- **Early Access Q3**
- **Delivery Q4** with Polaris Release
- Seeking early access partners
- Simply Reports and eContent data specifically
- Simply Reports will be restored with additional available data
- eContent circulation reports
- Additional 3rd party data

### Vega Reports for Sierra
- **Early Access Q3**
- **Early 2027 Release**
- Seeking early access partners
- Web Management reports/analysis and 3rd party circulation reports
- Decision Center analysis and incorporation

---

## Metabase / Metabot AI (Slides - IMG_0371, 0372, 0373)

Vega Reports is **powered by Metabase** (open-source BI tool).

### Metabot AI Features (IMG_0371)
- AI Exploration
- Create a chart using query builder
- Generate SQL in the native editor
- Edit SQL directly
- Analyze and ask questions of a chart
- Fix errors in SQL code
- Documentation, help and how-tos

### Metabase Query Builder UI (IMG_0372, 0373)
Data sources available include:
- Sample Data, Checkouts, Items, Print Circ Analytics, CheckoutEvents, Fiscal Year ID, Collection ID, Organization ID, Owning Location, LendingPeriodDate

Steps to Build a Report:
1. Select Your Data Source
2. Add Filters (Optional)
3. Summarize/Aggregate (Optional)

---

## Handwritten Notes from Jeremy (IMG_0374, IMG_0375)

### Page 1 (IMG_0374)
- Product Manager from Belgrade office: **Jovana Raskovic** (handwriting read as "Boskovic")
- Consortia & International Ready
- Allows for 3rd party data (**Cloudio**) to be brought in
- Middleware: NYPL, Phoenix, Stella — early adopters
- Can query via SQL & will provide a query builder
- Powered by **Metabase**
- Permissions for Reports Admins & Report Consumers
- Discover data currently **refreshed every 24 hours**
- DB is using **Postgres**
- SQL queries are using Postgres
- Currently **lacks any integrations with other BI tools** but are exploring the possibility
- Will auto-populate the most relevant visualization for your dataset

### Page 2 (IMG_0375)
- Must have Vega set up to access, but could just be **Vega LX Starter**
- Available for Discover users through May; working on Sierra & Polaris later
- Scheduling reports available; showed example of patron report based on checkouts
- Polaris goes before Sierra (conflicting with other scheduling)
- Physical collection concerns — difficult to accomplish
- Also hope that capabilities to import will be possible
- Polaris Vega Reports: early access Q3, delivery Q4 with Polaris release
- Sierra Vega: early access Q4(?), delivery 2027 release incorporated
- Web Management reports — Sierra customers surveyed
- Metabase AI tool — but it's just a proof of concept at this stage; hosted environment
- Each user can save reports/queries to their own login
- Branded Metabase consisting of a series of capped circ queries
- In a single prompt: pending visualization & SQL query

---

## Verbal Details from Transcript (not on slides)

The following details were shared verbally by Jovana during the presentation and are not captured in the slide photos or handwritten notes. See the [cleaned transcript](../transcripts/vega-reports-transcript-clean.md) for full context.

### Presenter Background
- Jovana is from Serbia, based in the Belgrade office; the trip to Chicago was 11 hours with no layover
- She has been with Clarivate for almost a year (20 days from anniversary at time of presentation)
- 6+ years working with analytics across different business areas
- She played flute for 11 years and dreamed of playing with a philharmonic orchestra; used this as an analogy for data -- "you have a lot of notes you need to go through and figure out how to compile them all together; it's absolutely the same with data"

### Pando - Data Collection Tool
- **Pando** is the tool that collects Vega Discover usage data
- Data flows from Pando via API into the data lakehouse, then into Vega Reports
- Dashboard data is back-populated approximately one week when Reports is first enabled; data accrues from that point forward

### Dashboard Behavior
- The preset dashboard **cannot be edited** by any role (Admin or Consumer)
- However, admins can use the **data models** from the dashboard to create their own reports
- Dashboard export is **PDF or email only**; custom-created reports can export as **CSV or Excel**
- Each dashboard card has an information (eye) icon on hover that explains metrics:
  - Unique Visitors = distinct count of users
  - Number of Interactions = any click/interaction on the page
  - Visitor Frequencies = how often a visitor visits Discover (with Medium/High/Low thresholds explained)

### Access Permissions Detail
- **Main site admins** get both Query Builder and Native SQL; when using Query Builder, the generated SQL is visible on the right-hand side
- **Collection site admins** get Query Builder only (no SQL access)
- **Reports Consumer** = view-only license; can view reports created by admins
- Every user can save reports/queries to their own **personal collection** (private to that user)

### Data Models vs. Data Tables
- Data models contain the same data as data tables but exist to **control access for collection site admins** -- when a collection admin selects their site, they only see data scoped to that site
- Documentation includes **"unique identifiers"** to help users find the correct field to join tables
- Recommended filter: "last time" is the most convenient for comparing Discover data over time

### External BI Tool Integration
- Currently **no integration with external BI tools** (Tableau, Power BI, etc.)
- They are "brainstorming" how to respond to this requirement but not yet planning it
- The data lakehouse infrastructure would technically allow it
- Jovana noted she was a heavy Tableau user previously and finds Metabase easier to use

### OverDrive Integration Approach
- Plan to match digital vs. print records via **patron ID** in the backend (without broadly exposing patron data)
- Alternative approach: matching via a **product ID** that maps to the title (acknowledged as harder since every title is different)
- **Roll-ups and holds** from OverDrive are not currently considered but noted as a good idea for the future
- The demo showed three key OverDrive metrics: unique patron count, number of checkouts, and average lending period
- Includes a **"print copy checked out" flag/filter** (yes/no) within the checkout time frame

### Survey Results and Feedback
- Polaris survey sent out a couple of months prior received **127 responses**
- Polaris users overwhelmingly want **circulation reports** first
- **Sierra survey has NOT been sent yet** -- Jovana is compiling it and will distribute in the coming weeks
- Sierra users appear to be more focused on **Decision Center** than Web Management Reports

### Vega LX Starter Requirement
- Polaris and Sierra users need a **Vega LX Starter** subscription (which provides the system ID needed to expose Reports)
- However, you do **not** need a full Vega Discover subscription to eventually get Reports

### Metabot AI Details
- Metabot **does not support self-hosted environments** (which is what Vega Reports uses) -- currently proof of concept only
- Jovana showed a **pre-recorded video demo** rather than a live demo
- In the demo, Metabot could: walk users through Query Builder steps, generate reports from A to Z (circulation by format, popular titles, trends over time, lending period), and generate/display the underlying SQL on request
- Reports created by Metabot are auto-saved and can be placed in personal folders

### Jesse Ryan - Development Manager
- **Jesse Ryan** is the development manager for Vega Reports
- Has a small development team
- Has been working with Jovana since she joined (11 months)

### Rollout Sequencing Detail
- Q2 2026: All current Vega Discover subscribers
- May 2026: Customers currently in Discover implementation
- Q3 2026: Polaris early access (seeking partners)
- Q4 2026: First Polaris delivery with circulation reports (+ OverDrive if timeline allows)
- Q3-Q4 2026: Sierra early access
- Early 2027: Sierra release
- Second half of 2027: Considering Vega LX integration

---

## Additional Context (from web research)

### Official Announcement (April 1, 2026)
Per [Innovative's blog post](https://iii.com/whats-new/smarter-insights-ahead-vega-reports-launching-soon/):
- Vega Reports launched April 7, 2026 with gradual rollout
- Included with Vega Discover subscription at no additional cost
- **Early Adopter partners:** Phoenix Public Library, STELLA, Mid-Hudson Library System
- Designed for directors, department heads, marketing teams, and digital services staff
- Capabilities: visitor statistics, engagement metrics, search activity analysis, patron discovery behavior insights
- Supports both consortia and non-consortia libraries

### OverDrive / Libby / Kanopy Integration
Per [OverDrive announcement (June 2025)](https://company.overdrive.com/2025/06/24/clarivate/):
- OverDrive and Clarivate previewed a deep integration roadmap at ALA Annual 2025
- Three pillars:
  1. **Smarter Discovery** — Deep linking from Vega LX to all OverDrive content (Libby ebooks, audiobooks, magazines, comics; Kanopy movies/docs/TV; Sora for students). Works regardless of underlying ILS (Polaris, Symphony, Sierra).
  2. **Better Engagement** — Vega Program integration lets Libby/Kanopy users discover local library events
  3. **Clearer Insights** — Consolidated analytics dashboard combining Vega Reports + OverDrive Marketplace data
- New tools rolling out through 2026
- Polaris ILS data and OverDrive checkouts data integration with Vega Reports in progress

### Presenter Note
IUG schedule lists presenter as **Jovana Raskovic** (Jeremy's handwritten notes may have read "Boskovic" — likely the same person).

---

## References

1. [Smarter Insights Ahead: Vega Reports Launching Soon](https://iii.com/whats-new/smarter-insights-ahead-vega-reports-launching-soon/) — Innovative Interfaces official announcement, April 1, 2026
2. [OverDrive and Clarivate to Preview Roadmap of Deep Integration for Libby, Kanopy, and Sora with Vega Discover](https://company.overdrive.com/2025/06/24/clarivate/) — OverDrive, June 24, 2025
3. [IUG 2026 Annual Conference Schedule](https://iug2026.sched.com/) — Session listing: "Vega Reports for Discover and Beyond" by Jovana Raskovic
4. [Vega Discover Support & Documentation](https://innovative.libguides.com/Vega) — Innovative Interfaces LibGuides
