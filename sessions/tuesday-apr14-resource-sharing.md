# Resource Sharing Update — Tuesday, April 14

**Speakers:** Hope Harley, Katy Aranoff
**Time:** 9:00–10:00 AM | **Room:** Denver | **Track:** General

Photos: [Google Photos Album](https://photos.app.goo.gl/mxMfA6hJ36z1NLgo6)

---

## Part 1: Rapido Consortial Borrowing (Hope Harley)

### SearchOhio / OhioLINK Deployment

The session opened with the Rapido CB deployment across Ohio — the largest cross-ILS Rapido consortial borrowing implementation to date.

**ILS breakdown:**
- 11 Sierra libraries
- 6 Polaris libraries
- 5 other ILS
- 88 Alma institutions (OhioLINK)

**Timeline:**
- **February 5, 2026** — SearchOhio soft launch (go-live)
- **March 2026** — Connected with OhioLINK
- Met with staff from 8 of the libraries to address a prioritized list of challenges learned from feedback to strengthen the solution

### Usage Stats (52 days, as of April 1)

| Metric | Value |
|--------|-------|
| Total requests submitted | ~45,000 |
| Fill rate | 37% |
| Average turnaround time | 6 days |
| Daily request volume | ~865/day |

### Same Goals, Fundamentally Different Approach

**What stays the same:**
- Sierra and Polaris staff stay in their native catalog — workflows unchanged
- ILS-specific operations remain in each system

**What's different from INN-Reach:**

| | INN-Reach (old) | Rapido CB (new) |
|--|----------------|-----------------|
| Infrastructure | Local server | Cloud-based architecture |
| Catalog | Separate union catalog | Integrated catalog — single search across SearchOhio + OhioLINK |
| Request interface | Per-ILS | Vega CRI (Central Request Interface) |
| Holdings data | Stored in union catalog | Only tracks bibs — calls back to each ILS for real-time item availability |

**Known gap:** Rapido CB does not readily show holdings because it only stores bibs and does real-time lookups. This is being actively addressed.

### What's Next for Rapido CB

- **Staff requesting** — ability for staff to place requests on behalf of patrons
- **Holdings & availability display** — making holdings visible in the interface
- **Idea Exchange** — using Clarivate's Idea Exchange for Rapido CB feature requests and prioritization
- **Local Vega Discover integration** — SearchOhio/OhioLINK results surfaced directly in each library's own Vega Discover instance
- **PIN authentication** — many member libraries still use barcode-only auth; Rapido requires PIN-based auth via Vega Discover. Focus is to minimize disruption during transition.

### Next Deployment

- **San Diego circuit** is the next group of libraries to deploy Rapido CB
- **Target go-live: late June 2026**

---

## Part 2: Rapido Stand-Alone (Katy Aranoff)

### What is Rapido?

Rapido is a resource sharing solution integrated with the library system that streamlines the user experience:
- Libraries manage ILL and the system searches the collection catalog
- Staff manage all their requests in one place
- Users place and track their requests in one system

Primarily aimed at **academic library partners**.

### Key Features

- **Metadata import** — when patrons place requests, Rapido can import metadata automatically for articles and physical books, easing the request process and improving fill rates
- **Transparency** — users can see request status and progress; status updates visible in library card/patron account using familiar language
- **Automation** — routine requests handled automatically; staff focus on mediating complex requests
- **Configurable workflows** — libraries set up automation rules matching their own policies and concerns
- **Higher volume capacity** — automation enables more requests without adding staff

### Rapido Stand-Alone Stats (2025)

| Metric | Value |
|--------|-------|
| Total requests | 5.5 million |
| Fill rate | 96% |
| Digital turnaround | 9.8 hours |
| First-partner fill rate | 95% |

- **Timezone-based routing** — requests route to partners in active timezones for faster fulfillment
- 95% of requests filled by the first partner due to metadata accuracy

### Global Community

Rapido is a growing community across **20 countries** spanning USA/Canada, Latin America, EMEA, APAC, Africa, and Australia/New Zealand.

---

## Slide Reference

| Slide | Description |
|-------|-------------|
| photo_001 | SearchOhio & OhioLINK overview — ILS breakdown and timeline |
| photo_002 | Planning for the future — Vega Discover, PIN auth, San Diego, what's next |
| photo_003 | What is Rapido? — definition and value proposition |
| photo_004 | A global community — 20 countries map |
| photo_005 | SearchOhio stats — 52 days of data, requests, fill rate, turnaround |
| photo_006 | Same goals, fundamentally different approach — INN-Reach vs. Rapido CB comparison |
| photo_007 | Integrating Rapido within local Vega Discover — UI screenshots |
