# IUG Speaker Cards — Sprint 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a sched.com scraper, seed a speaker JSON data file, and render a "Pokemon card" gallery page on the existing IUG 2026 GitHub Pages site.

**Architecture:** A Python scraper (`scripts/scrape_sched.py`) fetches and caches sched.com HTML for IUG 2019-2026, extracts speaker/session data, and writes `docs/speakers-data.json`. A static HTML page (`docs/speakers.html`) reads that JSON with vanilla JS and renders a CSS Grid of speaker cards with stats, rarity tiers, and session histories. Navigation across all 21 existing HTML pages gets a new "Speakers" link.

**Tech Stack:** Python 3.11+ (httpx, beautifulsoup4 — already in pyproject.toml), vanilla HTML/CSS/JS (no build tools), pytest for scraper tests.

**Spec:** `iug2026-shared/docs/superpowers/specs/2026-04-15-speaker-cards-design.md`

---

## File Structure

| Action | File | Purpose |
|--------|------|---------|
| Create | `scripts/scrape_sched.py` | Scraper: fetch sched.com, parse HTML, output/merge JSON |
| Create | `tests/test_scrape_sched.py` | Tests for name normalization and JSON merge logic |
| Create | `iug2026-shared/docs/speakers-data.json` | Speaker data — single source of truth for the gallery |
| Create | `iug2026-shared/docs/speakers.html` | Card gallery page with inline CSS and vanilla JS |
| Modify | `iug2026-shared/docs/index.html` | Add "Speaker Cards" to Deep Dives section |
| Modify | All 21 HTML files in `iug2026-shared/docs/` | Add "Speakers" link to nav bar |
| Modify | `pyproject.toml` | Add `scrape-sched` CLI entry point and pytest dev dep |

---

### Task 1: Project setup — pytest and scraper entry point

**Files:**
- Modify: `pyproject.toml`
- Create: `tests/__init__.py`
- Create: `tests/test_scrape_sched.py` (empty scaffold)
- Create: `scripts/scrape_sched.py` (empty scaffold)

- [ ] **Step 1: Add pytest dev dependency and scraper entry point to pyproject.toml**

```toml
# In pyproject.toml, add to [project.scripts]:
scrape-sched = "scripts.scrape_sched:main"

# Add after [build-system]:
[project.optional-dependencies]
dev = ["pytest"]
```

- [ ] **Step 2: Create test scaffold**

Create `tests/__init__.py` (empty file).

Create `tests/test_scrape_sched.py`:
```python
"""Tests for scrape_sched speaker name normalization and JSON merge logic."""
```

- [ ] **Step 3: Create scraper scaffold**

Create `scripts/scrape_sched.py`:
```python
"""Scrape sched.com archives (IUG 2019-2026) and output speakers-data.json."""


def main():
    pass
```

- [ ] **Step 4: Install dev dependencies and verify**

Run: `cd /home/ray/notes && uv pip install -e ".[dev]"`
Expected: successful install including pytest

Run: `cd /home/ray/notes && uv run pytest tests/ -v`
Expected: "no tests ran" (0 collected), exit 0 or 5 (no tests)

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml tests/__init__.py tests/test_scrape_sched.py scripts/scrape_sched.py
git commit -m "chore: scaffold scraper and test infrastructure for speaker cards"
```

---

### Task 2: Speaker name normalization utilities (TDD)

**Files:**
- Modify: `scripts/scrape_sched.py`
- Modify: `tests/test_scrape_sched.py`

- [ ] **Step 1: Write failing tests for name normalization**

In `tests/test_scrape_sched.py`:
```python
"""Tests for scrape_sched speaker name normalization and JSON merge logic."""

from scripts.scrape_sched import normalize_name, names_match


class TestNormalizeName:
    def test_basic(self):
        assert normalize_name("Jeremy Goldstein") == "jeremy goldstein"

    def test_extra_whitespace(self):
        assert normalize_name("  Jeremy   Goldstein  ") == "jeremy goldstein"

    def test_strips_titles(self):
        assert normalize_name("Dr. Sarah Johnson") == "sarah johnson"

    def test_strips_suffixes(self):
        assert normalize_name("Bob Smith Jr.") == "bob smith"
        assert normalize_name("Alice Brown III") == "alice brown"

    def test_last_comma_first(self):
        assert normalize_name("Goldstein, Jeremy") == "jeremy goldstein"

    def test_middle_initial(self):
        assert normalize_name("Jeremy A. Goldstein") == "jeremy goldstein"
        assert normalize_name("Jeremy A Goldstein") == "jeremy goldstein"


class TestNamesMatch:
    def test_exact(self):
        assert names_match("Jeremy Goldstein", "Jeremy Goldstein") is True

    def test_case_insensitive(self):
        assert names_match("jeremy goldstein", "Jeremy Goldstein") is True

    def test_with_title(self):
        assert names_match("Dr. Sarah Johnson", "Sarah Johnson") is True

    def test_last_comma_first(self):
        assert names_match("Goldstein, Jeremy", "Jeremy Goldstein") is True

    def test_middle_initial_difference(self):
        assert names_match("Jeremy A. Goldstein", "Jeremy Goldstein") is True

    def test_different_people(self):
        assert names_match("Jeremy Goldstein", "Bob Gaydos") is False
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /home/ray/notes && uv run pytest tests/test_scrape_sched.py -v`
Expected: FAIL — `ImportError: cannot import name 'normalize_name'`

- [ ] **Step 3: Implement name normalization**

In `scripts/scrape_sched.py`, add above the `main()` function:
```python
import re


# --- Name normalization ---

_TITLES = re.compile(r"\b(dr|prof|mr|mrs|ms|rev)\.?\s*", re.IGNORECASE)
_SUFFIXES = re.compile(r"\s+(jr\.?|sr\.?|ii|iii|iv|phd|md)\s*$", re.IGNORECASE)
_MIDDLE_INITIAL = re.compile(r"\s+[a-z]\.?\s+", re.IGNORECASE)


def normalize_name(name: str) -> str:
    """Lowercase, strip titles/suffixes/middle initials, handle 'Last, First'."""
    name = name.strip()
    # Handle "Last, First" format
    if "," in name:
        parts = name.split(",", 1)
        name = f"{parts[1].strip()} {parts[0].strip()}"
    name = _TITLES.sub("", name)
    name = _SUFFIXES.sub("", name)
    name = _MIDDLE_INITIAL.sub(" ", name)
    # Collapse whitespace
    name = " ".join(name.split()).lower()
    return name


def names_match(a: str, b: str) -> bool:
    """Check if two speaker names refer to the same person."""
    return normalize_name(a) == normalize_name(b)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /home/ray/notes && uv run pytest tests/test_scrape_sched.py -v`
Expected: all 12 tests PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/scrape_sched.py tests/test_scrape_sched.py
git commit -m "feat: add speaker name normalization with fuzzy matching"
```

---

### Task 3: JSON merge logic (TDD)

**Files:**
- Modify: `scripts/scrape_sched.py`
- Modify: `tests/test_scrape_sched.py`

- [ ] **Step 1: Write failing tests for JSON merge**

Append to `tests/test_scrape_sched.py`:
```python
class TestMergeSpeakers:
    def test_new_speaker_added(self):
        from scripts.scrape_sched import merge_speakers

        existing = []
        scraped = [
            {
                "id": "jeremy-goldstein",
                "name": "Jeremy Goldstein",
                "affiliation": "",
                "type": "",
                "primaryTrack": "",
                "quote": "",
                "quoteContext": "",
                "sessions": [{"year": 2026, "title": "Test", "role": "speaker", "track": "sierra", "schedUrl": None}],
                "notes": "",
            }
        ]
        result = merge_speakers(existing, scraped)
        assert len(result) == 1
        assert result[0]["name"] == "Jeremy Goldstein"

    def test_hand_edited_fields_preserved(self):
        from scripts.scrape_sched import merge_speakers

        existing = [
            {
                "id": "jeremy-goldstein",
                "name": "Jeremy Goldstein",
                "affiliation": "Minuteman Library Network, MA",
                "type": "Acquisitions Wizard",
                "primaryTrack": "sierra",
                "quote": "You imprint on your first system.",
                "quoteContext": "Sierra Sys Admin Forum, IUG 2026",
                "sessions": [{"year": 2026, "title": "Old Session", "role": "speaker", "track": "sierra", "schedUrl": None}],
                "notes": "Hand-written note",
            }
        ]
        scraped = [
            {
                "id": "jeremy-goldstein",
                "name": "Jeremy Goldstein",
                "affiliation": "",
                "type": "",
                "primaryTrack": "",
                "quote": "",
                "quoteContext": "",
                "sessions": [
                    {"year": 2026, "title": "New Session", "role": "speaker", "track": "sierra", "schedUrl": "https://example.com"},
                    {"year": 2025, "title": "Old Year", "role": "speaker", "track": "sierra", "schedUrl": None},
                ],
                "notes": "",
            }
        ]
        result = merge_speakers(existing, scraped)
        assert len(result) == 1
        speaker = result[0]
        # Hand-edited fields preserved
        assert speaker["type"] == "Acquisitions Wizard"
        assert speaker["quote"] == "You imprint on your first system."
        assert speaker["notes"] == "Hand-written note"
        assert speaker["affiliation"] == "Minuteman Library Network, MA"
        # Sessions replaced with scraped data (sessions are always re-scraped)
        assert len(speaker["sessions"]) == 2

    def test_existing_speaker_not_in_scrape_kept(self):
        from scripts.scrape_sched import merge_speakers

        existing = [
            {
                "id": "manual-add",
                "name": "Manual Add",
                "affiliation": "",
                "type": "Manually Added",
                "primaryTrack": "",
                "quote": "",
                "quoteContext": "",
                "sessions": [],
                "notes": "Added by hand",
            }
        ]
        scraped = []
        result = merge_speakers(existing, scraped)
        assert len(result) == 1
        assert result[0]["id"] == "manual-add"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /home/ray/notes && uv run pytest tests/test_scrape_sched.py::TestMergeSpeakers -v`
Expected: FAIL — `ImportError: cannot import name 'merge_speakers'`

- [ ] **Step 3: Implement merge logic**

In `scripts/scrape_sched.py`, add after the name functions:
```python
# --- Merge logic ---

# Fields that are hand-editable and should be preserved if already set
_HAND_EDITED_FIELDS = ("affiliation", "type", "primaryTrack", "quote", "quoteContext", "notes")


def _make_speaker_id(name: str) -> str:
    """Generate a URL-safe id from a speaker name."""
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower().strip())
    return slug.strip("-")


def merge_speakers(existing: list[dict], scraped: list[dict]) -> list[dict]:
    """Merge scraped speaker data with existing JSON, preserving hand-edited fields.

    - Existing speakers not in scraped data are kept as-is.
    - For speakers in both, hand-edited fields from existing are preserved
      if they have non-empty values. Sessions are replaced from scraped data.
    - New speakers from scraped data are added.
    """
    existing_by_id = {s["id"]: s for s in existing}
    result_by_id = dict(existing_by_id)  # start with all existing

    for speaker in scraped:
        sid = speaker["id"]
        if sid in result_by_id:
            merged = dict(speaker)
            old = result_by_id[sid]
            for field in _HAND_EDITED_FIELDS:
                if old.get(field):
                    merged[field] = old[field]
            result_by_id[sid] = merged
        else:
            result_by_id[sid] = speaker

    # Sort alphabetically by name
    return sorted(result_by_id.values(), key=lambda s: s["name"].lower())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /home/ray/notes && uv run pytest tests/test_scrape_sched.py -v`
Expected: all 15 tests PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/scrape_sched.py tests/test_scrape_sched.py
git commit -m "feat: add speaker JSON merge logic preserving hand-edited fields"
```

---

### Task 4: Scraper — HTTP fetching with caching

**Files:**
- Modify: `scripts/scrape_sched.py`

- [ ] **Step 1: Add HTTP fetching with /tmp/ cache and rate limiting**

In `scripts/scrape_sched.py`, add these imports at the top:
```python
import json
import time
from pathlib import Path

import httpx
```

Add after the merge logic:
```python
# --- HTTP fetching with cache ---

CACHE_DIR = Path("/tmp/iug-sched-cache")
SCHED_YEARS = range(2019, 2027)  # 2019 through 2026
USER_AGENT = "iug2026-speaker-cards/1.0 (conference notes project)"
REQUEST_DELAY = 1.5  # seconds between requests


def _cache_path(year: int) -> Path:
    return CACHE_DIR / f"iug{year}.html"


def fetch_schedule_page(year: int, *, force: bool = False) -> str | None:
    """Fetch a sched.com schedule page, using /tmp/ cache if available.

    Returns HTML string or None if the page doesn't exist / returns error.
    """
    cache = _cache_path(year)
    if cache.exists() and not force:
        return cache.read_text(encoding="utf-8")

    url = f"https://iug{year}.sched.com/"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    try:
        resp = httpx.get(url, headers={"User-Agent": USER_AGENT}, follow_redirects=True, timeout=30)
        if resp.status_code == 200:
            html = resp.text
            cache.write_text(html, encoding="utf-8")
            print(f"  Fetched iug{year}.sched.com ({len(html):,} bytes)")
            return html
        else:
            print(f"  iug{year}.sched.com returned {resp.status_code}, skipping")
            return None
    except httpx.HTTPError as e:
        print(f"  Error fetching iug{year}.sched.com: {e}")
        return None


def fetch_all_years(*, force: bool = False) -> dict[int, str]:
    """Fetch schedule pages for all years, returning {year: html}."""
    pages = {}
    for year in SCHED_YEARS:
        html = fetch_schedule_page(year, force=force)
        if html:
            pages[year] = html
        time.sleep(REQUEST_DELAY)
    return pages
```

- [ ] **Step 2: Quick manual test of the cache**

Run: `cd /home/ray/notes && uv run python -c "from scripts.scrape_sched import fetch_schedule_page; html = fetch_schedule_page(2026); print(f'Got {len(html) if html else 0} bytes') if html else print('No response')"`
Expected: prints bytes fetched (or an error if sched.com blocks — we handle both cases)

Check the cache: `ls -la /tmp/iug-sched-cache/`
Expected: `iug2026.html` exists

- [ ] **Step 3: Commit**

```bash
git add scripts/scrape_sched.py
git commit -m "feat: add sched.com HTTP fetcher with /tmp/ caching and rate limiting"
```

---

### Task 5: Scraper — HTML parsing

This task requires exploring the actual sched.com HTML structure. The parsing logic must be written after examining cached HTML.

**Files:**
- Modify: `scripts/scrape_sched.py`

- [ ] **Step 1: Fetch one page and explore the HTML structure**

Run the fetch from Task 4 if not done yet, then examine the cached HTML:
```bash
cd /home/ray/notes && uv run python -c "from scripts.scrape_sched import fetch_schedule_page; fetch_schedule_page(2026)"
```

Then open `/tmp/iug-sched-cache/iug2026.html` and look for:
- How events/sessions are listed (look for repeating `<div>` or `<a>` elements with event info)
- Where speaker names appear (often in a subtitle or metadata line)
- Where track names appear (often as a CSS class or label)
- Where event URLs are structured

Use `grep -i "speaker\|presenter\|event" /tmp/iug-sched-cache/iug2026.html | head -30` and examine the DOM structure. Take notes on the selectors needed.

**Important:** The actual HTML structure will determine the exact BeautifulSoup selectors below. The code in Step 2 shows the **expected** pattern based on typical sched.com pages. **You MUST adjust the selectors** based on what you find in Step 1.

- [ ] **Step 2: Implement HTML parser based on actual HTML structure**

In `scripts/scrape_sched.py`, add the import at the top:
```python
from bs4 import BeautifulSoup
```

Add after the fetch functions:
```python
# --- HTML parsing ---

def parse_schedule_page(html: str, year: int) -> list[dict]:
    """Parse a sched.com schedule page and extract session/speaker data.

    Returns a list of dicts: {title, speakers: [str], track, schedUrl}

    NOTE: The CSS selectors below must match the actual sched.com HTML structure.
    Inspect /tmp/iug-sched-cache/iug{year}.html to verify selectors before running.
    """
    soup = BeautifulSoup(html, "html.parser")
    sessions = []

    # TODO: Replace these selectors based on actual sched.com HTML structure
    # found during Step 1 exploration. Common patterns:
    #   - Events in divs with class "sched-event" or "event"
    #   - Speaker names in spans with class "event-speakers" or similar
    #   - Track as a data attribute or class name
    #   - Event links as <a> with href containing "/event/"
    #
    # Typical sched.com structure:
    #   <div class="sched-container-inner">
    #     <div class="sched-event">
    #       <a class="event" href="/event/...">Title</a>
    #       <span class="speakers">Speaker Name</span>
    #       ...
    #
    # ADJUST ALL SELECTORS BELOW BASED ON WHAT YOU FIND IN THE HTML.

    for event_el in soup.select(".sched-event, .event-row, [id^='sched-event']"):
        title_el = event_el.select_one("a.event, .event-name, .name a")
        if not title_el:
            continue

        title = title_el.get_text(strip=True)
        sched_url = title_el.get("href", "")
        if sched_url and not sched_url.startswith("http"):
            sched_url = f"https://iug{year}.sched.com{sched_url}"

        # Extract speaker names
        speaker_els = event_el.select(".event-speakers a, .sched-event-details-speakers a, .speaker")
        speakers = [el.get_text(strip=True) for el in speaker_els if el.get_text(strip=True)]

        # Extract track
        track = ""
        track_el = event_el.select_one(".sched-event-type, .event-type, .track")
        if track_el:
            track = _normalize_track(track_el.get_text(strip=True))

        if speakers:  # Only include events that have named speakers
            sessions.append({
                "title": title,
                "speakers": speakers,
                "track": track,
                "schedUrl": sched_url or None,
            })

    return sessions


def _normalize_track(raw_track: str) -> str:
    """Map sched.com track names to our canonical track slugs."""
    raw = raw_track.lower().strip()
    if "sierra" in raw:
        return "sierra"
    if "polaris" in raw:
        return "polaris"
    if "vega" in raw:
        return "vega"
    if "gathering" in raw or "social" in raw:
        return "gatherings"
    return "general"
```

- [ ] **Step 3: Test the parser against cached HTML**

Run: `cd /home/ray/notes && uv run python -c "
from scripts.scrape_sched import fetch_schedule_page, parse_schedule_page
html = fetch_schedule_page(2026)
sessions = parse_schedule_page(html, 2026)
print(f'Found {len(sessions)} sessions with speakers')
for s in sessions[:5]:
    print(f'  {s[\"title\"]} — {s[\"speakers\"]} [{s[\"track\"]}]')
"`

Expected: a non-zero number of sessions with speaker names. If 0, revisit the selectors in Step 2 by examining the HTML more carefully.

**Iterate on selectors until the parser extracts reasonable data.** This is exploratory — expect 2-3 iterations.

- [ ] **Step 4: Commit**

```bash
git add scripts/scrape_sched.py
git commit -m "feat: add sched.com HTML parser for session/speaker extraction"
```

---

### Task 6: Scraper — assembly and main() entry point

**Files:**
- Modify: `scripts/scrape_sched.py`

- [ ] **Step 1: Build the pipeline that assembles speaker data from parsed sessions**

In `scripts/scrape_sched.py`, add after the parsing functions:
```python
# --- Assembly ---

def _infer_role(title: str) -> str:
    """Infer speaker role from session title keywords."""
    lower = title.lower()
    if "forum" in lower or "bof" in lower or "birds of a feather" in lower:
        return "moderator"
    if "panel" in lower:
        return "panelist"
    if "hackathon" in lower:
        return "hackathon"
    return "speaker"


def build_speakers_from_sessions(all_sessions: dict[int, list[dict]]) -> list[dict]:
    """Build speaker objects from parsed session data across all years.

    Args:
        all_sessions: {year: [session_dicts]} from parse_schedule_page

    Returns:
        List of speaker dicts matching the schema in the design spec.
    """
    # Collect sessions by normalized speaker name
    speakers_raw: dict[str, dict] = {}  # normalized_name -> {name, sessions}

    for year, sessions in sorted(all_sessions.items()):
        for session in sessions:
            for speaker_name in session["speakers"]:
                norm = normalize_name(speaker_name)
                if norm not in speakers_raw:
                    speakers_raw[norm] = {
                        "name": speaker_name,  # keep original casing from first appearance
                        "sessions": [],
                    }
                speakers_raw[norm]["sessions"].append({
                    "year": year,
                    "title": session["title"],
                    "role": _infer_role(session["title"]),
                    "track": session["track"],
                    "schedUrl": session["schedUrl"],
                })

    # Build full speaker objects
    speakers = []
    for norm_name, data in speakers_raw.items():
        sid = _make_speaker_id(data["name"])
        speakers.append({
            "id": sid,
            "name": data["name"],
            "affiliation": "",
            "type": "",
            "primaryTrack": "",
            "quote": "",
            "quoteContext": "",
            "sessions": data["sessions"],
            "notes": "",
        })

    return sorted(speakers, key=lambda s: s["name"].lower())
```

- [ ] **Step 2: Implement main() with full pipeline**

Replace the existing `main()` function in `scripts/scrape_sched.py`:
```python
def main():
    """Scrape sched.com archives and output/update speakers-data.json."""
    import argparse

    parser = argparse.ArgumentParser(description="Scrape sched.com for IUG speaker data")
    parser.add_argument("--force", action="store_true", help="Re-fetch even if cached")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "iug2026-shared" / "docs" / "speakers-data.json",
        help="Output JSON file path",
    )
    args = parser.parse_args()

    print("Fetching sched.com schedule pages...")
    pages = fetch_all_years(force=args.force)
    print(f"Got {len(pages)} years: {sorted(pages.keys())}")

    print("\nParsing sessions...")
    all_sessions = {}
    for year, html in sorted(pages.items()):
        sessions = parse_schedule_page(html, year)
        all_sessions[year] = sessions
        print(f"  {year}: {len(sessions)} sessions with speakers")

    print("\nBuilding speaker data...")
    scraped_speakers = build_speakers_from_sessions(all_sessions)
    print(f"Found {len(scraped_speakers)} unique speakers")

    # Merge with existing data if present
    existing = []
    if args.output.exists():
        existing = json.loads(args.output.read_text(encoding="utf-8"))
        print(f"Merging with {len(existing)} existing speakers...")

    result = merge_speakers(existing, scraped_speakers)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nWrote {len(result)} speakers to {args.output}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Verify the scraper runs end-to-end**

Run: `cd /home/ray/notes && uv run scrape-sched`

Expected output like:
```
Fetching sched.com schedule pages...
  Fetched iug2019.sched.com (xxxxx bytes)
  ...
Got N years: [2019, 2020, ...]
Parsing sessions...
  2019: X sessions with speakers
  ...
Building speaker data...
Found N unique speakers
Wrote N speakers to /home/ray/notes/iug2026-shared/docs/speakers-data.json
```

If any year returns 0 sessions, debug the parser selectors for that year's HTML.

- [ ] **Step 4: Run all tests**

Run: `cd /home/ray/notes && uv run pytest tests/ -v`
Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/scrape_sched.py
git commit -m "feat: complete scraper pipeline — fetch, parse, assemble, merge, output JSON"
```

---

### Task 7: Run scraper and curate seed data

This task is manual — run the scraper, inspect the output, hand-edit the JSON.

**Files:**
- Create/Modify: `iug2026-shared/docs/speakers-data.json`

- [ ] **Step 1: Run the scraper to seed speakers-data.json**

Run: `cd /home/ray/notes && uv run scrape-sched`

Inspect the output: `cd /home/ray/notes && uv run python -c "
import json
data = json.load(open('iug2026-shared/docs/speakers-data.json'))
print(f'{len(data)} speakers')
for s in data[:10]:
    print(f'  {s[\"name\"]} — {len(s[\"sessions\"])} sessions')
"`

- [ ] **Step 2: Hand-edit speakers-data.json to curate priority speakers**

Using the speaker bios from `iug2026-private/resources/speaker-bios.md`, update at minimum these speakers with `type`, `quote`, `affiliation`, `primaryTrack`, and `notes` fields:

1. **Jeremy Goldstein** — type: "Acquisitions Wizard", affiliation: "Minuteman Library Network, MA", primaryTrack: "sierra"
2. **Bob Gaydos** — type: "SQL Sage", affiliation: "Stark County District Library, OH", primaryTrack: "sierra"
3. **Joel Tonyan** — type: "Dashboard Architect", affiliation: "Kraemer Family Library, UCCS", primaryTrack: "sierra"
4. **Ashley Barey** — type: "Product Strategist", affiliation: "Innovative (Clarivate)", primaryTrack: "vega"
5. **Jason Boland** — type: "Training Specialist", affiliation: "Innovative (Clarivate)", primaryTrack: "sierra"

Add quotes from session transcripts if available. Set `primaryTrack` based on the track they present in most.

- [ ] **Step 3: Validate JSON is well-formed**

Run: `cd /home/ray/notes && uv run python -c "import json; data = json.load(open('iug2026-shared/docs/speakers-data.json')); print(f'Valid JSON: {len(data)} speakers'); assert all('id' in s and 'sessions' in s for s in data), 'Missing required fields'"`
Expected: `Valid JSON: N speakers`

- [ ] **Step 4: Commit**

```bash
git add iug2026-shared/docs/speakers-data.json
git commit -m "feat: seed speakers-data.json from sched.com scrape with curated bios"
```

---

### Task 8: Build speakers.html — card gallery page

**Files:**
- Create: `iug2026-shared/docs/speakers.html`

- [ ] **Step 1: Create speakers.html with full page structure**

Create `iug2026-shared/docs/speakers.html` with the complete page. This is a large file — inline CSS (per project convention, same as `suggest-a-purchase.html`), vanilla JS that fetches `speakers-data.json` and renders cards.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Speaker Cards — IUG 2026</title>
  <meta name="description" content="IUG conference speaker cards — presentation history, stats, and personality across all IUG years.">
  <meta property="og:title" content="Speaker Cards — IUG 2026">
  <meta property="og:description" content="IUG conference speaker cards — presentation history, stats, and personality across all IUG years.">
  <meta property="og:image" content="https://rayvoelker.github.io/iug2026-shared/assets/iug2026-banner.png">
  <meta property="og:url" content="https://rayvoelker.github.io/iug2026-shared/speakers.html">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="IUG 2026 Conference Notes">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Speaker Cards — IUG 2026">
  <meta name="twitter:description" content="IUG conference speaker cards — presentation history, stats, and personality across all IUG years.">
  <meta name="twitter:image" content="https://rayvoelker.github.io/iug2026-shared/assets/iug2026-banner.png">
  <link rel="stylesheet" href="style.css">
  <style>
    /* Speaker card grid */
    .speaker-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 1.25rem;
      margin-bottom: 2rem;
    }

    /* Individual speaker card */
    .speaker-card {
      background: white;
      border-radius: 6px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
      overflow: hidden;
      transition: box-shadow 0.15s;
    }
    .speaker-card:hover {
      box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }

    /* Track-color top border */
    .speaker-card .card-top {
      height: 4px;
    }
    .speaker-card .card-top.sierra { background: var(--green); }
    .speaker-card .card-top.polaris { background: var(--gold); }
    .speaker-card .card-top.vega { background: var(--red); }
    .speaker-card .card-top.general { background: var(--teal); }
    .speaker-card .card-top.gatherings { background: var(--sky); }

    .speaker-card .card-body {
      padding: 1.25rem;
    }

    /* Header row: rarity badge + track icon */
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.75rem;
    }

    .rarity-badge {
      font-size: 0.65rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 0.15rem 0.5rem;
      border-radius: 10px;
    }
    .rarity-common { background: #e0e0e0; color: #666; }
    .rarity-uncommon { background: #e8f5e9; color: var(--green); }
    .rarity-rare { background: #e0f2f1; color: var(--teal); }
    .rarity-legendary {
      background: linear-gradient(135deg, #fff8e1, #ffecb3);
      color: #b8860b;
      box-shadow: 0 0 6px rgba(230, 185, 0, 0.3);
    }

    .track-icon {
      font-size: 0.7rem;
      font-weight: 600;
      text-transform: uppercase;
      color: #999;
    }

    /* Speaker info */
    .speaker-name {
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--navy);
      margin-bottom: 0.15rem;
    }
    .speaker-affiliation {
      font-size: 0.8rem;
      color: #999;
      margin-bottom: 0.1rem;
    }
    .speaker-type {
      font-size: 0.8rem;
      color: var(--teal);
      font-style: italic;
      margin-bottom: 0.75rem;
    }

    /* Stat blocks */
    .stat-blocks {
      display: flex;
      gap: 0.5rem;
      margin-bottom: 0.75rem;
    }
    .stat-block {
      background: var(--light);
      border-radius: 4px;
      padding: 0.4rem 0.6rem;
      text-align: center;
      min-width: 50px;
    }
    .stat-block .stat-num {
      font-size: 1.2rem;
      font-weight: 700;
      color: var(--navy);
      line-height: 1;
    }
    .stat-block .stat-lbl {
      font-size: 0.6rem;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      color: #999;
    }

    /* Quote */
    .speaker-quote {
      font-size: 0.8rem;
      font-style: italic;
      color: #777;
      margin-bottom: 0.75rem;
      padding-left: 0.75rem;
      border-left: 2px solid var(--gold);
    }
    .speaker-quote .quote-ctx {
      display: block;
      font-size: 0.7rem;
      font-style: normal;
      color: #aaa;
      margin-top: 0.25rem;
    }

    /* Session history */
    .session-toggle {
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--teal);
      cursor: pointer;
      background: none;
      border: none;
      padding: 0;
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }
    .session-toggle:hover { text-decoration: underline; }
    .session-toggle .arrow {
      transition: transform 0.15s;
      font-size: 0.65rem;
    }
    .session-toggle.open .arrow { transform: rotate(90deg); }

    .session-list {
      display: none;
      margin-top: 0.5rem;
      font-size: 0.78rem;
      color: #666;
    }
    .session-list.open { display: block; }
    .session-list .session-entry {
      padding: 0.2rem 0;
      border-bottom: 1px solid #f0f0f0;
    }
    .session-list .session-entry:last-child { border-bottom: none; }
    .session-year { font-weight: 600; color: var(--navy); min-width: 35px; display: inline-block; }
    .session-role { font-size: 0.7rem; color: #aaa; }
  </style>
</head>
<body>

  <div class="banner">
    <img src="assets/iug2026-banner.png" alt="IUG 2026">
  </div>
  <nav>
    <ul>
      <li><a href="index.html">Home</a></li>
      <li><a href="sunday.html">Sunday</a></li>
      <li><a href="monday.html">Monday</a></li>
      <li><a href="tuesday.html">Tuesday</a></li>
      <li><a href="wednesday.html">Wednesday</a></li>
      <li><a href="speakers.html" class="active">Speakers</a></li>
    </ul>
  </nav>

  <div class="container">

    <div class="breadcrumb"><a href="index.html">Home</a> / Speakers</div>
    <h1>IUG Speaker Cards</h1>
    <p class="page-subtitle">Conference presentation history across all IUG years</p>

    <div class="stats-row" id="page-stats"></div>

    <div class="speaker-grid" id="speaker-grid"></div>

  </div>

  <div class="footer">
    <img src="assets/chicago-skyline.png" alt="Chicago skyline">
    <div class="footer-text">
      <a href="https://www.innovativeusers.org/iug_2026.php">innovativeusers.org</a> &middot;
      <a href="https://github.com/rayvoelker/iug2026-shared">View on GitHub</a> &middot;
      &#9998; <a href="https://github.com/rayvoelker/iug2026-shared/issues/new?title=Correction:+Speakers&body=Page:+speakers.html%0A%0ACorrection:">Suggest a correction</a>
    </div>
  </div>

  <script>
    (async function() {
      const resp = await fetch('speakers-data.json');
      const speakers = await resp.json();

      // --- Computed stats ---
      function getRarity(count) {
        if (count >= 8) return { tier: 'legendary', label: 'Legendary' };
        if (count >= 5) return { tier: 'rare', label: 'Rare' };
        if (count >= 3) return { tier: 'uncommon', label: 'Uncommon' };
        return { tier: 'common', label: 'Common' };
      }

      function uniqueYears(sessions) {
        return [...new Set(sessions.map(s => s.year))];
      }

      function uniqueTracks(sessions) {
        return [...new Set(sessions.map(s => s.track).filter(Boolean))];
      }

      // --- Page stats ---
      const totalSessions = speakers.reduce((sum, s) => sum + s.sessions.length, 0);
      const allYears = [...new Set(speakers.flatMap(s => s.sessions.map(ss => ss.year)))].sort();
      const legendaryCount = speakers.filter(s => s.sessions.length >= 8).length;

      document.getElementById('page-stats').innerHTML = `
        <div class="stat"><div class="number">${speakers.length}</div><div class="stat-label">Speakers</div></div>
        <div class="stat"><div class="number">${totalSessions}</div><div class="stat-label">Sessions Tracked</div></div>
        <div class="stat"><div class="number">${allYears.length}</div><div class="stat-label">Years Covered</div></div>
        <div class="stat"><div class="number">${legendaryCount}</div><div class="stat-label">Legendary</div></div>
      `;

      // --- Render cards ---
      const grid = document.getElementById('speaker-grid');

      speakers.forEach(speaker => {
        const sessions = speaker.sessions;
        const rarity = getRarity(sessions.length);
        const years = uniqueYears(sessions);
        const tracks = uniqueTracks(sessions);
        const track = speaker.primaryTrack || tracks[0] || 'general';

        const card = document.createElement('div');
        card.className = 'speaker-card';
        card.id = speaker.id;

        const quoteHtml = speaker.quote
          ? `<div class="speaker-quote">"${speaker.quote}"${speaker.quoteContext ? `<span class="quote-ctx">&mdash; ${speaker.quoteContext}</span>` : ''}</div>`
          : '';

        const typeHtml = speaker.type
          ? `<div class="speaker-type">${speaker.type}</div>`
          : '<div class="speaker-type">&nbsp;</div>';

        const affiliationHtml = speaker.affiliation
          ? `<div class="speaker-affiliation">${speaker.affiliation}</div>`
          : '';

        const sessionsHtml = sessions
          .sort((a, b) => b.year - a.year)
          .map(s => {
            const link = s.schedUrl ? `<a href="${s.schedUrl}">${s.title}</a>` : s.title;
            return `<div class="session-entry"><span class="session-year">${s.year}</span> ${link} <span class="session-role">(${s.role})</span></div>`;
          })
          .join('');

        card.innerHTML = `
          <div class="card-top ${track}"></div>
          <div class="card-body">
            <div class="card-header">
              <span class="rarity-badge rarity-${rarity.tier}">${rarity.label}</span>
              <span class="track-icon">${track}</span>
            </div>
            <div class="speaker-name">${speaker.name}</div>
            ${affiliationHtml}
            ${typeHtml}
            <div class="stat-blocks">
              <div class="stat-block"><div class="stat-num">${sessions.length}</div><div class="stat-lbl">sessions</div></div>
              <div class="stat-block"><div class="stat-num">${years.length}</div><div class="stat-lbl">years</div></div>
              <div class="stat-block"><div class="stat-num">${tracks.length}</div><div class="stat-lbl">tracks</div></div>
            </div>
            ${quoteHtml}
            <button class="session-toggle" onclick="this.classList.toggle('open'); this.nextElementSibling.classList.toggle('open')">
              <span class="arrow">&#9656;</span> Session History (${sessions.length})
            </button>
            <div class="session-list">${sessionsHtml}</div>
          </div>
        `;

        grid.appendChild(card);
      });
    })();
  </script>

</body>
</html>
```

- [ ] **Step 2: Test in browser**

If the GitHub Pages dev server is available, open `speakers.html`. Otherwise:
```bash
cd /home/ray/notes/iug2026-shared/docs && python3 -m http.server 8000 &
```
Open `http://localhost:8000/speakers.html` in a browser. Verify:
- Stats row shows correct numbers
- Cards render in a grid (2-3 per row on desktop)
- Track-color top borders appear
- Rarity badges show correct tiers
- Session history expand/collapse works
- Quotes display where present
- Speaker `id` attributes work as anchor targets (try `#jeremy-goldstein`)

Kill the server: `kill %1`

- [ ] **Step 3: Commit**

```bash
git add iug2026-shared/docs/speakers.html
git commit -m "feat: add speaker cards gallery page with stats, rarity tiers, and session history"
```

---

### Task 9: Navigation updates — add "Speakers" link to all pages

**Files:**
- Modify: All 21 HTML files in `iug2026-shared/docs/` (except `speakers.html` which already has it)

The nav in every existing page looks like this:
```html
    <ul>
      <li><a href="index.html">Home</a></li>
      ...
      <li><a href="wednesday.html">Wednesday</a></li>
    </ul>
```

Add `<li><a href="speakers.html">Speakers</a></li>` after the Wednesday line in every file.

- [ ] **Step 1: Add Speakers nav link to all existing HTML pages**

For each of these 20 files (speakers.html already has it), find the `</ul>` inside `<nav>` and add the Speakers link after the Wednesday `<li>`:

Files to update:
1. `iug2026-shared/docs/index.html`
2. `iug2026-shared/docs/sunday.html`
3. `iug2026-shared/docs/monday.html`
4. `iug2026-shared/docs/tuesday.html`
5. `iug2026-shared/docs/wednesday.html`
6. `iug2026-shared/docs/sierra-roadmap.html`
7. `iug2026-shared/docs/amazon-business.html`
8. `iug2026-shared/docs/hackathon-awards.html`
9. `iug2026-shared/docs/resource-sharing.html`
10. `iug2026-shared/docs/sierra-year-in-review.html`
11. `iug2026-shared/docs/ai-the-right-way.html`
12. `iug2026-shared/docs/floating-collections-bof.html`
13. `iug2026-shared/docs/meep.html`
14. `iug2026-shared/docs/vega-reports.html`
15. `iug2026-shared/docs/executive-panel.html`
16. `iug2026-shared/docs/cataloging-without-oclc.html`
17. `iug2026-shared/docs/sierra-sso.html`
18. `iug2026-shared/docs/sierra-sso-guide.html`
19. `iug2026-shared/docs/cloudflare-sierra-guide.html`
20. `iug2026-shared/docs/suggest-a-purchase.html`

In each file, find:
```html
      <li><a href="wednesday.html">Wednesday</a></li>
    </ul>
```

Replace with:
```html
      <li><a href="wednesday.html">Wednesday</a></li>
      <li><a href="speakers.html">Speakers</a></li>
    </ul>
```

Note: some pages have `class="active"` on the Wednesday link — preserve that. The pattern to match is the `wednesday.html` `<li>` followed by `</ul>`.

A sed one-liner to do all 20 files at once:
```bash
cd /home/ray/notes/iug2026-shared/docs && for f in index.html sunday.html monday.html tuesday.html wednesday.html sierra-roadmap.html amazon-business.html hackathon-awards.html resource-sharing.html sierra-year-in-review.html ai-the-right-way.html floating-collections-bof.html meep.html vega-reports.html executive-panel.html cataloging-without-oclc.html sierra-sso.html sierra-sso-guide.html cloudflare-sierra-guide.html suggest-a-purchase.html; do sed -i 's|<li><a href="wednesday.html">\(.*\)</a></li>|<li><a href="wednesday.html">\1</a></li>\n      <li><a href="speakers.html">Speakers</a></li>|' "$f"; done
```

- [ ] **Step 2: Verify nav updated correctly**

Run: `cd /home/ray/notes && grep -l "speakers.html" iug2026-shared/docs/*.html | wc -l`
Expected: 21 (all 20 existing + speakers.html itself)

Spot-check one page:
```bash
grep -A1 "wednesday.html" /home/ray/notes/iug2026-shared/docs/index.html
```
Expected: Wednesday link followed by Speakers link.

- [ ] **Step 3: Commit**

```bash
cd /home/ray/notes && git add iug2026-shared/docs/*.html
git commit -m "feat: add Speakers nav link to all 20 existing pages"
```

---

### Task 10: Add Speaker Cards to index.html Deep Dives section

**Files:**
- Modify: `iug2026-shared/docs/index.html`

- [ ] **Step 1: Add Speaker Cards entry to the Deep Dives section**

In `iug2026-shared/docs/index.html`, find the closing `</div>` of the `section-list` div (after the last `day-card` in Deep Dives — currently "The Great ILS-Data Preconference"). Add a new entry before the closing `</div>`:

Find (the last entry in Deep Dives):
```html
      <a class="day-card" href="https://github.com/iug-ils-data-preconf/iug2026">
        <div class="day-info">
          <h3>The Great ILS-Data Preconference</h3>
          <p>Sunday pre-conference: data visualization, regex, APIs, Datasette, data lakes, privacy, AMH logs, Python CLI tools, and more</p>
        </div>
      </a>
    </div>
```

Replace with:
```html
      <a class="day-card" href="https://github.com/iug-ils-data-preconf/iug2026">
        <div class="day-info">
          <h3>The Great ILS-Data Preconference</h3>
          <p>Sunday pre-conference: data visualization, regex, APIs, Datasette, data lakes, privacy, AMH logs, Python CLI tools, and more</p>
        </div>
      </a>
      <a class="day-card" href="speakers.html">
        <div class="day-info">
          <h3>Speaker Cards</h3>
          <p>Conference speaker gallery &mdash; presentation history, stats, and rarity tiers across all IUG years</p>
        </div>
      </a>
    </div>
```

- [ ] **Step 2: Verify in browser**

Open `index.html` in browser (or via local server). Verify "Speaker Cards" appears as the last Deep Dives entry and links to `speakers.html`.

- [ ] **Step 3: Commit**

```bash
git add iug2026-shared/docs/index.html
git commit -m "feat: add Speaker Cards to Deep Dives section on index page"
```

---

### Task 11: Session page speaker links

**Files:**
- Modify: existing session HTML pages that mention speakers in `speakers-data.json`

- [ ] **Step 1: Identify which session pages have speakers to link**

The session pages that have known speakers (from the bios and spec):

1. `sierra-roadmap.html` — Mike Dicus
2. `amazon-business.html` — (check for speaker names)
3. `resource-sharing.html` — (check for speaker names)
4. `sierra-year-in-review.html` — (check for speaker names)
5. `ai-the-right-way.html` — Ashley Barey
6. `vega-reports.html` — (check for speaker names)
7. `executive-panel.html` — (check for speaker names)
8. `cataloging-without-oclc.html` — (check for speaker names)
9. `sierra-sso.html` — (check for speaker names)
10. `sierra-sys-admin-forum.html` — (check for speaker names)
11. `meep.html` — (check for speaker names)
12. `hackathon-awards.html` — (check for speaker names)

Read each session page and cross-reference speaker names with `speakers-data.json`. For each page that mentions a speaker in the data, add a speaker callout card.

- [ ] **Step 2: Add speaker callout cards to session pages**

For each session page that has matching speakers, add a `<div class="card">` block after the breadcrumb/title area (before the main content) with links to the speaker cards. Follow this exact pattern:

```html
    <div class="card">
      <p><strong>Speakers:</strong>
        <a href="speakers.html#speaker-id">Speaker Name</a> &middot;
        <a href="speakers.html#speaker-id-2">Speaker Name 2</a>
      </p>
    </div>
```

Place this right after the `<p class="page-subtitle">` line in each file.

The exact speakers per page depend on what's in `speakers-data.json` after the scrape. Cross-reference by matching speaker names in the page content against speaker IDs in the JSON.

- [ ] **Step 3: Verify links work**

Open a session page with speaker links in browser. Click each speaker link — it should navigate to `speakers.html#speaker-id` and scroll to that card.

- [ ] **Step 4: Commit**

```bash
cd /home/ray/notes && git add iug2026-shared/docs/*.html
git commit -m "feat: add speaker card links to session pages"
```

---

## Summary

| Task | What | Key output |
|------|------|------------|
| 1 | Project setup | pytest, scraper scaffold |
| 2 | Name normalization (TDD) | `normalize_name()`, `names_match()` + 12 tests |
| 3 | JSON merge logic (TDD) | `merge_speakers()` + 3 tests |
| 4 | HTTP fetching | `fetch_schedule_page()` with /tmp/ cache |
| 5 | HTML parsing | `parse_schedule_page()` — exploratory, selector iteration |
| 6 | Scraper assembly | `main()` — full pipeline, CLI entry point |
| 7 | Seed + curate data | `speakers-data.json` with hand-edited bios |
| 8 | Gallery page | `speakers.html` — cards, stats, expand/collapse |
| 9 | Nav updates | "Speakers" link on all 21 pages |
| 10 | Index update | Speaker Cards in Deep Dives |
| 11 | Session links | Speaker callout cards on session pages |
