# Site Refactor: Content/Presentation Separation

**Date:** 2026-04-17
**Status:** Approved
**Scope:** iug2026-shared repository

## Problem

The IUG 2026 shared site has 21 hand-authored HTML files in `/docs/`, each duplicating the full page boilerplate: navigation, meta tags, banner, footer, breadcrumbs, and speaker links. Content also exists in 14 markdown files in `/sessions/`, but the HTML pages were written separately — not generated from the markdown. The two sources have likely drifted apart.

Adding or updating a page requires editing raw HTML, manually wiring navigation and breadcrumbs, and copy-pasting boilerplate. Changing a site-wide element (nav, footer) means touching every file. This is error-prone and doesn't scale.

## Goals

1. **Single source of truth** — all page content lives in markdown+frontmatter files. No content in HTML templates.
2. **Automated build** — a Python build script generates the final HTML from content + templates + data.
3. **Dev server** — `uv run build.py --dev` serves the site locally with file watching and auto-rebuild.
4. **Content reconciliation** — audit and merge existing HTML and markdown sources, eliminating drift.
5. **Reusability** — the build system and templates can be copied and adapted for future conferences.

## Non-Goals

- Building a general-purpose static site generator framework
- Redesigning the site's visual appearance (existing `style.css` carries forward)
- Automating the content reconciliation (manual, page-by-page review)

## Project Structure

```
iug2026-shared/
  content/                    # Single source of truth for all pages
    index.md                  # Homepage
    sunday.md                 # Day overview pages
    monday.md
    tuesday.md
    wednesday.md
    sessions/                 # Individual session deep-dives
      sierra-roadmap.md
      amazon-business.md
      vega-reports.md
      cloudflare-sierra-guide.md
      ...
    resources/                # Standalone guides/reference pages
      cloudflare-sierra-protection.md

  templates/                  # Jinja2 HTML layouts
    base.html                 # Master layout: head, nav, footer, OG tags
    page.html                 # Generic content page (extends base)
    session.html              # Session page with speaker cards, metadata sidebar
    day.html                  # Day overview with session listing
    speakers.html             # Speaker gallery (driven by data)

  static/                     # Copied verbatim to output
    style.css                 # Existing stylesheet
    assets/                   # Banner, skyline, logos, etc.

  data/                       # Structured data & site config
    site.yaml                 # Site-wide metadata (title, url, nav, OG defaults)
    speakers.json             # Speaker data (existing speakers-data.json)

  photos/                     # Conference photos (copied to output)
  transcripts/                # Kept as-is, copied or linked

  docs/                       # BUILD OUTPUT — GitHub Pages serves this

  build.py                    # The entire build system
  pyproject.toml              # uv project dependencies
```

### Key Decisions

- `content/` is the only place page content is edited.
- `docs/` becomes pure build output (gitignored except CNAME if needed).
- `static/` holds CSS and assets that pass through untouched.
- `data/site.yaml` holds site-wide config: title, base URL, navigation structure, default OG image, footer text.

## Content File Format

Each markdown file uses YAML frontmatter for metadata.

### Session Page

```markdown
---
title: "Sierra Roadmap Deep Dive"
template: session
date: 2026-04-14
day: tuesday
track: Sierra
room: "Grand Ballroom A"
time: "10:30 AM - 12:00 PM"
speakers:
  - bob-gaydos
  - jason-boland
description: "Key updates to Sierra platform including new API endpoints and migration timeline."
tags: [sierra, roadmap, api]
---

## Session Highlights

The roadmap presentation covered...
```

### Day Overview Page

```markdown
---
title: "Monday, April 13"
template: day
date: 2026-04-13
day: monday
description: "Opening session, Innovation Awards, and afternoon deep dives."
---

## Morning Highlights

The conference kicked off with...
```

### Generic Page

```markdown
---
title: "IUG 2026 - Chicago"
template: page
description: "Knowledge base for the Innovative Users Group 2026 conference."
---

## Welcome

Your guide to IUG 2026...
```

### Frontmatter Conventions

- `template` — selects which Jinja2 template to use (`session`, `day`, `page`, `speakers`)
- `speakers` — list of speaker IDs referencing keys in `data/speakers.json`
- `day` — groups session pages under their parent day for auto-generating day overview listings and breadcrumbs
- `description` — used for OG meta tags and page subtitles
- `date` — used for ordering and display

## Build System (`build.py`)

### Build Pipeline

1. **Load config** — read `data/site.yaml` and `data/speakers.json` into memory
2. **Discover content** — glob `content/**/*.md`, parse frontmatter + body from each
3. **Render markdown** — convert each file's markdown body to HTML fragments
4. **Resolve references** — look up speaker IDs against speakers data, build session-by-day groupings
5. **Render templates** — inject each page's metadata + rendered HTML into its Jinja2 template
6. **Copy static assets** — `static/` to `docs/`, `photos/` to `docs/photos/`
7. **Write output** — rendered HTML to `docs/`, preserving URL structure

### URL Mapping

```
content/index.md           -> docs/index.html
content/monday.md          -> docs/monday.html
content/sessions/foo.md    -> docs/sessions/foo.html
```

### Template Context

Every template receives:

```python
{
    "site": { ... },        # from site.yaml
    "page": {               # from this file's frontmatter
        "title": "...",
        "description": "...",
        "template": "...",
        "url": "...",       # computed relative URL
        # ... all other frontmatter fields
    },
    "content": "<p>...</p>",  # markdown body rendered as HTML
    "speakers": { ... },      # full speakers data for lookups
    "pages": [ ... ],         # all pages metadata for cross-referencing
}
```

### CLI Interface

```bash
uv run build.py              # full build -> docs/
uv run build.py --clean      # wipe docs/ first, then build
uv run build.py --dev        # build + serve on 0.0.0.0:8000 + file watching
```

### Dev Server (`--dev` mode)

- Serves `docs/` on `0.0.0.0:8000` (accessible via Tailscale)
- Uses `watchdog` to monitor `content/`, `templates/`, `static/`, and `data/` for changes
- On any file change, re-runs the full build pipeline
- No incremental build complexity — full rebuild is well under a second for ~25 pages

## Template Design

Templates reproduce the existing site's HTML structure using Jinja2 inheritance.

### `base.html` — Master Layout

Provides: `<head>` with OG/Twitter meta tags, banner, navigation bar, container wrapper, footer. All auto-populated from `site` and `page` context.

Navigation is generated from `site.nav` (defined in `site.yaml`), with active-page highlighting.

A `static()` helper function resolves relative paths to static assets based on the page's output depth (e.g., `style.css` from top-level, `../style.css` from a session page).

### `session.html` — Session Pages

Extends `base.html`. Adds:
- Breadcrumbs: Home -> Day -> Session title
- Metadata subtitle: track, time, room
- Speaker cards: auto-resolved from `speakers` frontmatter field against `speakers.json`
- Markdown content body

### `day.html` — Day Overview Pages

Extends `base.html`. Adds:
- Auto-generated session listing from all pages where `day` matches
- Markdown content body for editorial highlights

### `speakers.html` — Speaker Gallery

Extends `base.html`. Driven entirely by `data/speakers.json`. Generates the gallery with stats, rarity tiers, and session history.

### `page.html` — Generic Pages

Extends `base.html`. Simple: title + content. Used for index, any page that doesn't fit a specialized template.

### Visual Continuity

The existing `style.css` and its class names (`.banner`, `.nav`, `.container`, `.card`, `.section-list`, etc.) remain unchanged. Templates produce the same HTML structure the current hand-authored pages have.

## Content Reconciliation

Before the build system can run, the existing HTML and markdown sources must be reconciled into canonical `content/` markdown files.

### Process

1. **Audit** — for each session with both a `.md` and `.html` version, do a side-by-side comparison
2. **Identify drift** — content only in HTML, content only in markdown, content in both but different
3. **Merge** — produce a single reconciled markdown+frontmatter file per page

### Reconciliation Rules

- **Structure and formatting** — take from HTML (the published, polished version)
- **Raw notes, details, implementation advice** — take from markdown if it has content the HTML lacks
- **Speaker references, links, metadata** — take from HTML (richer linking)
- **Frontmatter** — generate from the HTML's meta tags, breadcrumbs, and page structure

### Pages Without Markdown Source

Pages that exist only as HTML (day overviews, speakers gallery, index) become template-driven. Their content is either:
- Minimal markdown + auto-generated listings (day pages)
- Purely data-driven (speakers gallery from `speakers.json`)
- Editorial content extracted from the HTML into markdown (index page)

### Approach

Page-by-page, assisted by Claude but with human review. This is a one-time cost that eliminates the drift problem permanently.

### Post-Reconciliation Cleanup

After all content is reconciled into `content/`, the original `/sessions/` directory is removed — its contents have been merged into `content/sessions/`. The original hand-authored HTML files in `/docs/` are replaced by build output. The `/resources/` markdown file moves to `content/resources/`.

## Dependencies

```toml
[project]
dependencies = [
    "jinja2",
    "python-frontmatter",
    "mistune",
    "pyyaml",
    "watchdog",
]
```

Managed via `uv` with `pyproject.toml`.

## Reusability

### Conference-Specific (replace per event)

- `data/site.yaml` — title, branding, nav, URLs
- `data/speakers.json` — speaker data
- `content/` — all page content
- `static/assets/` — banner images, logos

### Reusable Across Events

- `build.py` — works on any content/templates/data structure
- `templates/` — session, day, speakers, page layouts
- `static/style.css` — CSS variables at the top for easy rebranding

### To Start a New Conference

1. Copy or fork the repo
2. Replace `data/site.yaml` with new conference info
3. Clear `content/`, start writing new session notes
4. Optionally tweak CSS variables for rebranding
5. Templates work as-is
