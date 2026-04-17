# IUG Speaker Cards — Design Spec

## Overview

Build a "Pokemon card" gallery of IUG conference speakers with stats, session history, and personality. A single browsable page on the existing GitHub Pages site, driven by an editable JSON data file, seeded by scraping sched.com archives.

## Goals

- Cross-reference every named speaker at IUG 2026 with their presentation history across all available IUG years
- Present each speaker as a fun, visual "trading card" with stats and flavor
- Make the data trivially editable (JSON file, no HTML changes needed for content)
- Fit naturally into the existing hand-crafted HTML site (no build tools, no frameworks)

## Non-Goals (Sprint 2 / Later)

- Pagination, search, or filtering UI
- Click-to-flip card animations
- Individual speaker detail pages
- Speaker photos (no reliable source)

---

## Architecture

### Files

| File | Purpose |
|---|---|
| `docs/speakers-data.json` | All speaker data — single source of truth |
| `docs/speakers.html` | Card gallery page — reads JSON, renders cards with vanilla JS |
| `scripts/scrape-sched.py` | Scrapes sched.com archives, outputs/updates the JSON file |
| Existing session pages | Add links to relevant speaker cards |

### Data Flow

```
sched.com archives (2019-2026)
        |
        v
scripts/scrape-sched.py  --->  docs/speakers-data.json
                                        |
                                        v
                                docs/speakers.html (vanilla JS reads JSON, renders cards)
```

---

## Speaker Data Schema

Each speaker is one object in a JSON array:

```json
{
  "id": "jeremy-goldstein",
  "name": "Jeremy Goldstein",
  "affiliation": "Minuteman Library Network, MA",
  "type": "Acquisitions Wizard",
  "primaryTrack": "sierra",
  "quote": "You imprint on your first system.",
  "quoteContext": "Sierra Sys Admin Forum, IUG 2026",
  "sessions": [
    {
      "year": 2026,
      "title": "Automating Reports with Python 2",
      "role": "speaker",
      "track": "sierra",
      "schedUrl": "https://iug2026.sched.com/event/..."
    },
    {
      "year": 2026,
      "title": "Acquisitions Forum",
      "role": "moderator",
      "track": "general",
      "schedUrl": null
    },
    {
      "year": 2025,
      "title": "Automating Reports with Python",
      "role": "speaker",
      "track": "sierra",
      "schedUrl": "https://iug2025.sched.com/event/..."
    }
  ],
  "notes": "Acquisitions expert. Provided the invoicing fix at the 2026 Sys Admin Forum."
}
```

### Computed Stats (derived at render time, not stored)

- **Total presentations**: `sessions.length`
- **Years active**: unique years from sessions
- **Tracks covered**: unique tracks from sessions
- **Rarity tier**: based on total presentations
  - Common: 1-2 sessions
  - Uncommon: 3-4 sessions
  - Rare: 5-7 sessions
  - Legendary: 8+
- **Roles**: unique roles from sessions (speaker, moderator, panelist, hackathon)

### Editable Fields

Everything in the JSON is hand-editable:
- `type` — the fun class label, assigned manually (not auto-generated)
- `quote` / `quoteContext` — optional, add when we have a good one
- `notes` — optional freeform context
- `sessions` — can be added/corrected manually after the scrape seeds the data

---

## Card Visual Design

Each card rendered as a `<div>` with this structure:

```
+--[track-color border-top]------------------+
|  [Rarity Badge]              [Track Icon]   |
|                                             |
|  SPEAKER NAME                               |
|  Affiliation                                |
|  "Type / Class"                             |
|                                             |
|  +---+ +---+ +---+                          |
|  | 7 | | 4 | | 3 |    (stat blocks)        |
|  |ses| |yrs| |trk|                          |
|  +---+ +---+ +---+                          |
|                                             |
|  "Quote here if available"                  |
|                                             |
|  > Session History          [expandable]    |
|    2026: Session Title (role)               |
|    2025: Session Title (role)               |
|    ...                                      |
+---------------------------------------------+
```

### Styling

- Cards use existing CSS classes where possible (`card`, `section-item`, etc.)
- New CSS added inline in `speakers.html` (consistent with `suggest-a-purchase.html` pattern)
- Track colors from existing CSS custom properties:
  - Sierra: `var(--green)` / `#2D8232`
  - Polaris: `var(--gold)` / `#E6B900`
  - Vega: `var(--red)` / `#D42426`
  - General: `var(--teal)` / `#006482`
  - Gatherings: `var(--sky)` / `#7CC4E2`
- Rarity badges:
  - Common: gray
  - Uncommon: green
  - Rare: blue/teal
  - Legendary: gold with subtle glow/border effect
- Card grid: CSS Grid, `repeat(auto-fill, minmax(300px, 1fr))`
- Cards should be compact enough that 2-3 fit per row on desktop

### Page Structure

Standard site template:
- Banner, nav (no specific day active — this is a cross-conference page), breadcrumb (Home / Speakers)
- Title: "IUG Speaker Cards"
- Subtitle: "Conference presentation history across all IUG years"
- Stats row: total speakers, total sessions tracked, years covered, legendary count
- Filter/sort: Sprint 2 (not in Sprint 1 — just render all cards alphabetically)
- Card grid
- Footer

---

## Sched.com Scraper

### Target URLs

Check all of these for existence, scrape the ones that respond:

- `https://iug2026.sched.com/`
- `https://iug2025.sched.com/`
- `https://iug2024.sched.com/`
- `https://iug2023.sched.com/`
- `https://iug2022.sched.com/`
- `https://iug2021.sched.com/`
- `https://iug2020.sched.com/`
- `https://iug2019.sched.com/`

### Scraping Strategy

1. For each year, fetch the full schedule page
2. Extract all sessions with: title, speaker name(s), track, time, event URL
3. Normalize speaker names (trim whitespace, handle "First Last" vs "Last, First")
4. Cross-reference against our known 67 speakers from IUG 2026
5. Also capture any speakers NOT in our 2026 list but who appear in multiple years (they may be worth including as "alumni" cards)
6. Output to `docs/speakers-data.json`

### Technical Details

- Use Python with `requests` + `beautifulsoup4` (install into venv: `uv pip install requests beautifulsoup4`)
- Sched.com pages are server-rendered HTML — no JS rendering needed
- Rate limit: 1-2 second delay between requests
- Cache raw HTML to `/tmp/` to avoid re-fetching during development
- The script should be idempotent: re-running merges new data with existing JSON (preserving hand-edited fields like `type`, `quote`, `notes`)

### Name Matching

Speaker names across years may not match exactly. The scraper should:
- Exact match first
- Fuzzy match on normalized names (lowercase, strip titles like "Dr.", handle middle initials)
- Flag uncertain matches for manual review rather than auto-merging

---

## Session Page Updates

After the speaker gallery is built, add a small callout to each existing session HTML page linking to the relevant speaker cards. Format:

```html
<div class="card">
  <p><strong>Speakers:</strong>
    <a href="speakers.html#jeremy-goldstein">Jeremy Goldstein</a> ·
    <a href="speakers.html#jeff-campbell">Jeff Campbell</a>
  </p>
</div>
```

Each card in the gallery gets an `id` attribute matching the speaker's `id` field for anchor linking.

---

## Navigation Updates

- Add "Speakers" link to the nav bar on all pages (after Wednesday)
- Add a "Speaker Cards" entry to the Deep Dives section on index.html

---

## Sprint 1 Scope

1. Write the sched.com scraper script
2. Run it, seed `speakers-data.json`
3. Hand-edit the JSON: assign types, add quotes from transcripts, fix any scraper errors
4. Build `speakers.html` with the card gallery
5. Update `index.html` and nav across all pages
6. Add speaker callout links to existing session pages
7. Commit and push

## Sprint 2 Scope (Future)

- Client-side search/filter (by name, track, year, rarity)
- Pagination or virtual scrolling if page gets heavy
- Card flip animation (front = stats, back = full session list)
- Sort options (alphabetical, rarity, presentation count)
- "Compare" mode — select two cards side by side
- Speaker alumni cards (people who presented in past years but not 2026)
