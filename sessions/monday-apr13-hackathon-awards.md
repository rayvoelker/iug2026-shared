# IUG 2026 Hackathon Awards — Monday, April 13

**Session:** Hackathon Presentation & Awards, 4:00–5:00 PM
**Organizers:** Gabrielle Gosselin, Mike Dicus

## FindIt — Shelf Mapping for Vega Catalogs

**Presenter:** Rochester Hills Public Library (RHPubLib)
**Repo:** https://github.com/RHPubLib/FindIt
**License:** MIT

### What It Does

FindIt adds physical shelf location maps to the Vega Discover catalog. Patrons search the catalog, find an item, and get an interactive floor map showing exactly where it lives on the shelf — bridging the gap between a call number and a physical location in the building.

**The workflow: Search → Find → Go Get It**

### Three Components

1. **Vega Catalog Widget** (`src/findit.js`) — Vanilla JS injected into Vega via Custom Header Code. Uses MutationObserver to detect availability rows, scrapes call number and collection data from the DOM, and injects a "View Shelf Location" button that opens an interactive floor map modal with zoom/pan/pinch support. Supports multi-branch libraries with tabs.

2. **Rectangle Editor** (`editor/`) — Flask web app for staff to visually define shelf locations on floor plan images. Features canvas-based drawing, Polaris PAPI integration for populating collection/shelf location dropdowns, and one-click publish to production (combines projects into `ranges.json` and SCPs to hosting).

3. **Standalone Map App** (`map-app/`) — Mobile-first web app where patrons can search the catalog and see results on a floor plan. Supports kiosk mode for Chrome OS kiosks with inactivity timeout.

### Tech Stack

| Layer | Technology |
|-------|-----------|
| Vega Widget | Vanilla JavaScript — zero dependencies, no build step |
| Editor Backend | Python 3.13, Flask, Authlib (Google Workspace OAuth) |
| Editor Frontend | Vanilla JS canvas drawing engine |
| ILS Integration | Polaris PAPI (HMAC-SHA1 signed REST API) |
| Hosting | GoDaddy cPanel (Apache) for production; Debian server for editor |

### PAPI Integration

The editor backend acts as a proxy between the browser and Polaris ILS. PAPI requires HMAC-SHA1 request signing, so the browser never talks to Polaris directly.

Two key API endpoints:
- **Collections** — fetches collection names (e.g., "Adult Biography", "Large Print") for editor dropdowns
- **Shelf Locations** — fetches shelf location descriptions for mapping

The map app also uses PAPI for catalog search, enriching results with floor map data and Syndetics book covers.

### Configuration System

Shelf locations are defined as `ranges` entries with matchers:
- **Collection name** — substring match (e.g., "Large Print")
- **Location** — substring match (e.g., "Children")
- **Call number prefix** — starts-with match (e.g., "DVD")
- **Dewey range** — numeric range with auto-stripping of juvenile prefixes (J/YA/E/JE/JR/JUV)

Each range includes a floor map image URL, SVG rectangle overlay coordinates, pin marker position, branch assignment, and wayfinding directions text.

### Design Decisions

- **Zero dependencies** — intentionally no npm/framework so any library can deploy regardless of technical capacity
- **Self-host mandate** — each library hosts its own copy; README warns against loading from GitHub
- **Data/code separation** — staff update `ranges.json` via the editor without touching JavaScript
- **DOM scraping over API calls** — the Vega widget reads availability data from the page DOM rather than making separate API calls, avoiding CORS issues and API key exposure

### Documentation

The repo includes comprehensive docs:
- `docs/setup.md` — Quick start guide
- `docs/configuration.md` — Full config property reference
- `docs/editor-server.md` — Editor server setup and PAPI docs
- `docs/floor-map-guide.md` — How to prepare floor plan images
- `docs/FindIt_Hackathon_IUG_2026.pptx` — The IUG 2026 presentation slides

---

## Browsr — Collection Browsing Tool

**Presenter:** Andrew (last name TBD)
**PAPI-based project**

A tool that allows patrons to browse through a smaller, curated collection. Uses the Polaris PAPI for catalog data.

*Details TBD — repo link not yet captured.*

---

## Offline Circulation Tool

**Presenters:** Wes and Bryan (sp?)

A better offline tool for handling checkouts and offline transactions. The idea started complex and was narrowed down during the hackathon. Built on **PocketBase** — an all-in-one backend in a single file for managing the app (database, auth, API).

### How It Works

**Name:** Shelf Defense

- **SIP2-based** — uses the standard library self-checkout/circulation protocol
- **Runs everywhere** — portable, not tied to a specific platform
- **Peer architecture** — one device acts as the server, others connect to it
- **Sync later** — when connectivity is restored, syncs transactions back to the ILS
- **CSV export** — alternative to live sync; export offline transactions for manual processing
- **Bring your own SIP2 server** — works with any ILS that supports SIP2
- **Cross-platform** — runs on Windows, Mac, Linux
- Built with assistance from **Claude Code and ChatGPT**

---

## Leap SQL Template Manager

**Presenters:** Kalee Gulosh (sp?) and Mike Parks (sp?)

A web-based tool for running parameterized SQL searches against library databases. Staff select a saved query template, fill in parameters via form fields (dropdowns, text inputs), and run the query — no SQL knowledge required.

- **Template manager** — a dashboard listing all saved queries with name, template info, status, last updated, and a "Configure & Run" button for each
- **Parameterized execution** — staff fill in a web form rather than editing raw SQL
- **Consortium sharing** — member libraries can share query templates with each other; one library writes a useful query, the whole consortium benefits
- **Search/browse** — templates are searchable and browsable from the main dashboard
- **Tech stack** — ASP.NET / C#, built for Polaris environments

---

## Suggest a Purchase

**Presenter:** Somalia Jamall — Jacksonville Public Library
**Repo:** https://github.com/SomaliaJamall/Auto-Suggest-a-Purchase

A patron-facing tool for suggesting purchases, designed to take some of the load off the collection development team. Gives patrons a better experience for submitting purchase requests, and gives staff a more manageable workflow.

- **Already in production** — approximately 400 patrons have used it
- Solves a real operational problem for collection development teams
- **Nightly script-based** — runs on a schedule, emails patrons with updates on their suggestions
- **Tech stack** — PHP, JavaScript, Python, HTML/CSS

---

## Microprojects — Sierra Bulk Editing via Create Lists + Review Files

**Presenter:** Victor Zuniga

A tool that leverages the Sierra API's **Create Lists** and **Review Files** endpoints to perform bulk record edits — pushing updates back to Sierra. Staff can edit multiple fields at once, including both **variable-length and fixed-length fields**.

- Uses the Sierra API to create lists, then work with the review file to apply changes
- Works with **patron records** — demo showed a "Patron Review Files" interface with columns for Name, Address, Phone(s), Barcode(s), Email(s), and Actions
- Enables batch editing workflows that would otherwise require manual record-by-record work in the Sierra client
- **TODO/Next step:** Incorporate permissions into the tool
