# Site Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Separate content from presentation in the IUG 2026 shared site, replacing 22 hand-authored HTML files with markdown+frontmatter content files rendered through Jinja2 templates by a Python build script.

**Architecture:** A single `build.py` script reads markdown content files (with YAML frontmatter), loads site config and speaker data, renders through Jinja2 templates, and writes static HTML to `docs/`. All content lives in flat `content/` directory. Templates reproduce the existing visual design. Dev server uses watchdog + http.server.

**Tech Stack:** Python 3.11+, uv, Jinja2, python-frontmatter, mistune, PyYAML, watchdog

**Spec:** `specs/2026-04-17-site-refactor-design.md`

---

## File Map

### Create

- `pyproject.toml` — uv project with dependencies
- `build.py` — the entire build system (~200 lines)
- `data/site.yaml` — site-wide configuration
- `data/speakers.json` — moved from `docs/speakers-data.json`
- `templates/base.html` — master layout
- `templates/page.html` — generic content page
- `templates/session.html` — session deep-dive page
- `templates/day.html` — day overview page
- `templates/index.html` — homepage (structured data-driven)
- `templates/speakers.html` — speaker gallery (server-side rendered)
- `static/style.css` — moved from `docs/style.css`, with speaker card CSS consolidated in
- `static/assets/` — moved from `docs/assets/`
- `content/*.md` — 22 content files (one per page)
- `tests/test_build.py` — core build function tests
- `specs/` — moved from `docs/superpowers/specs/`
- `plans/` — moved from `docs/superpowers/plans/`

### Delete (after migration verified)

- `docs/*.html` — all hand-authored HTML (replaced by build output)
- `docs/style.css` — moved to `static/`
- `docs/assets/` — moved to `static/assets/`
- `docs/speakers-data.json` — moved to `data/speakers.json`
- `docs/superpowers/` — moved to `specs/` and `plans/`
- `sessions/` — content reconciled into `content/`
- `resources/` — content reconciled into `content/`

---

## Task 1: Project Scaffolding

**Files:**
- Create: `pyproject.toml`
- Create: `data/site.yaml`
- Move: `docs/speakers-data.json` → `data/speakers.json`
- Move: `docs/style.css` → `static/style.css`
- Move: `docs/assets/` → `static/assets/`
- Move: `docs/superpowers/specs/` → `specs/`
- Move: `docs/superpowers/plans/` → `plans/`

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p content templates static data tests specs plans
```

- [ ] **Step 2: Create `pyproject.toml`**

```toml
[project]
name = "iug-site"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "jinja2>=3.1",
    "python-frontmatter>=1.1",
    "mistune>=3.0",
    "pyyaml>=6.0",
    "watchdog>=4.0",
]

[dependency-groups]
dev = ["pytest>=8.0"]
```

- [ ] **Step 3: Install dependencies**

Run: `uv sync`
Expected: dependencies installed, `uv.lock` created

- [ ] **Step 4: Move assets to new locations**

```bash
mv docs/style.css static/style.css
cp -r docs/assets static/assets
mv docs/speakers-data.json data/speakers.json
mv docs/superpowers/specs/* specs/
mv docs/superpowers/plans/* plans/
```

Note: we `cp` assets (not move) because the existing HTML still references them. We'll delete the originals in the cleanup task.

- [ ] **Step 5: Create `data/site.yaml`**

```yaml
title: "IUG 2026 Conference Notes"
subtitle: "Innovative Users Group · Chicago, IL"
url: "https://rayvoelker.github.io/iug2026-shared"
repo: "https://github.com/rayvoelker/iug2026-shared"
schedule_url: "https://iug2026.sched.com/"
og_image: "assets/iug2026-banner.png"
banner_image: "assets/iug2026-banner.png"
banner_alt: "IUG 2026 — Chicago Marriott Downtown Magnificent Mile — April 12-15"
footer_image: "assets/chicago-skyline.png"
footer_links:
  - label: "innovativeusers.org"
    url: "https://www.innovativeusers.org/iug_2026.php"
  - label: "View on GitHub"
    url: "https://github.com/rayvoelker/iug2026-shared"

nav:
  - label: Home
    url: index.html
  - label: Sunday
    url: sunday.html
  - label: Monday
    url: monday.html
  - label: Tuesday
    url: tuesday.html
  - label: Wednesday
    url: wednesday.html
  - label: Speakers
    url: speakers.html

conference:
  when: "April 12–15, 2026"
  where: "Chicago Marriott Downtown Magnificent Mile"

tracks:
  - name: Gatherings
    css_class: gatherings
    description: "Social events, breaks & birds of a feather"
  - name: General
    css_class: general
    description: "Cross-platform sessions & forums"
  - name: Sierra
    css_class: sierra
    description: "Sierra ILS"
  - name: Polaris
    css_class: polaris
    description: "Polaris ILS"
  - name: Vega
    css_class: vega
    description: "Vega LX Platform"
```

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml uv.lock data/ static/ templates/ content/ tests/ specs/ plans/
git commit -m "feat: scaffold site refactor — pyproject.toml, site config, move assets"
```

---

## Task 2: Build Script Core

**Files:**
- Create: `build.py`
- Create: `tests/test_build.py`

- [ ] **Step 1: Write tests for core build functions**

Create `tests/test_build.py`:

```python
"""Tests for the core build pipeline functions."""

import json
import tempfile
from pathlib import Path

import frontmatter
import yaml

from build import load_config, discover_content, render_markdown, get_rarity


def test_load_config(tmp_path):
    """load_config reads site.yaml and speakers.json correctly."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    site_yaml = {"title": "Test Site", "url": "https://example.com"}
    (data_dir / "site.yaml").write_text(yaml.dump(site_yaml))

    speakers = [{"id": "alice", "name": "Alice", "sessions": []}]
    (data_dir / "speakers.json").write_text(json.dumps(speakers))

    site, spk = load_config(data_dir)
    assert site["title"] == "Test Site"
    assert "alice" in spk
    assert spk["alice"]["name"] == "Alice"


def test_discover_content(tmp_path):
    """discover_content finds .md files and parses frontmatter."""
    content_dir = tmp_path / "content"
    content_dir.mkdir()

    md = "---\ntitle: Test Page\ntemplate: page\n---\n\n# Hello\n\nWorld"
    (content_dir / "test.md").write_text(md)

    pages = discover_content(content_dir)
    assert len(pages) == 1
    assert pages[0]["title"] == "Test Page"
    assert pages[0]["template"] == "page"
    assert pages[0]["url"] == "test.html"
    assert "# Hello" in pages[0]["_body"]


def test_render_markdown():
    """render_markdown converts markdown to HTML."""
    html = render_markdown("# Title\n\nA paragraph with **bold**.")
    assert "<h1>" in html
    assert "<strong>bold</strong>" in html


def test_get_rarity():
    """get_rarity returns correct tier labels."""
    assert get_rarity(1)["tier"] == "common"
    assert get_rarity(3)["tier"] == "rare"
    assert get_rarity(5)["tier"] == "epic"
    assert get_rarity(8)["tier"] == "legendary"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_build.py -v`
Expected: FAIL — `build` module not found

- [ ] **Step 3: Create `build.py` with core functions**

```python
#!/usr/bin/env python3
"""Static site builder for IUG conference notes."""

import argparse
import http.server
import json
import shutil
import threading
from pathlib import Path

import frontmatter
import mistune
import yaml
from jinja2 import Environment, FileSystemLoader

# Directories (defaults, overridable for testing)
ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content"
TEMPLATE_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "docs"
PHOTOS_DIR = ROOT / "photos"
TRANSCRIPTS_DIR = ROOT / "transcripts"


def load_config(data_dir=None):
    """Load site.yaml and speakers.json. Returns (site_dict, speakers_by_id)."""
    data_dir = data_dir or DATA_DIR
    with open(data_dir / "site.yaml") as f:
        site = yaml.safe_load(f)
    with open(data_dir / "speakers.json") as f:
        speakers_list = json.load(f)
    speakers = {s["id"]: s for s in speakers_list}
    return site, speakers


def discover_content(content_dir=None):
    """Find all .md files in content/ and parse frontmatter + body."""
    content_dir = content_dir or CONTENT_DIR
    pages = []
    for md_file in sorted(content_dir.glob("*.md")):
        post = frontmatter.load(md_file)
        url = md_file.stem + ".html"
        page = dict(post.metadata)
        page["url"] = url
        page["_body"] = post.content
        page["_source"] = md_file.name
        pages.append(page)
    return pages


def render_markdown(text):
    """Convert markdown text to HTML."""
    return mistune.html(text)


def get_rarity(session_count):
    """Compute speaker rarity tier from session count."""
    if session_count >= 8:
        return {"tier": "legendary", "label": "\u2605 LEGENDARY"}
    if session_count >= 5:
        return {"tier": "epic", "label": "\u25c6 Epic"}
    if session_count >= 3:
        return {"tier": "rare", "label": "\u25cf Rare"}
    return {"tier": "common", "label": "\u25cb Common"}


def enrich_speakers(speakers):
    """Add computed fields (rarity, unique years, unique tracks) to each speaker."""
    for sid, speaker in speakers.items():
        sessions = speaker.get("sessions", [])
        speaker["rarity"] = get_rarity(len(sessions))
        speaker["unique_years"] = sorted(set(s["year"] for s in sessions), reverse=True)
        speaker["unique_tracks"] = sorted(set(s.get("track", "general") for s in sessions))
        speaker["sessions_sorted"] = sorted(sessions, key=lambda s: s["year"], reverse=True)
        speaker["session_count"] = len(sessions)
        speaker["year_count"] = len(speaker["unique_years"])
        speaker["track_count"] = len(speaker["unique_tracks"])
    return speakers


def get_sessions_for_day(pages, day):
    """Return all session pages for a given day, sorted by time."""
    return [p for p in pages if p.get("day") == day and p.get("template") == "session"]


def build_site():
    """Run the full build pipeline."""
    print("Building site...")
    site, speakers = load_config()
    speakers = enrich_speakers(speakers)
    pages = discover_content()

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

    for page in pages:
        template_name = page.get("template", "page") + ".html"
        template = env.get_template(template_name)

        content_html = render_markdown(page["_body"])

        # Compute nav_active: for sessions, highlight the parent day
        if page.get("day"):
            nav_active = page["day"] + ".html"
        else:
            nav_active = page["url"]

        html = template.render(
            site=site,
            page=page,
            content=content_html,
            speakers=speakers,
            pages=pages,
            nav_active=nav_active,
            get_sessions_for_day=get_sessions_for_day,
        )

        out_path = OUTPUT_DIR / page["url"]
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html)
        print(f"  {page['url']}")

    # Copy static assets
    if STATIC_DIR.exists():
        for item in STATIC_DIR.iterdir():
            dest = OUTPUT_DIR / item.name
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)
        print(f"  Copied static/")

    # Copy photos
    if PHOTOS_DIR.exists():
        shutil.copytree(PHOTOS_DIR, OUTPUT_DIR / "photos", dirs_exist_ok=True)
        print(f"  Copied photos/")

    # Copy transcripts
    if TRANSCRIPTS_DIR.exists():
        shutil.copytree(TRANSCRIPTS_DIR, OUTPUT_DIR / "transcripts", dirs_exist_ok=True)
        print(f"  Copied transcripts/")

    print(f"Built {len(pages)} pages -> {OUTPUT_DIR}/")


def clean():
    """Remove the output directory."""
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
        print(f"Cleaned {OUTPUT_DIR}/")


def main():
    parser = argparse.ArgumentParser(description="Build the IUG conference site")
    parser.add_argument("--clean", action="store_true", help="Clean output before building")
    parser.add_argument("--dev", action="store_true", help="Build, serve, and watch")
    parser.add_argument("--port", type=int, default=8000, help="Dev server port")
    args = parser.parse_args()

    if args.clean:
        clean()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    build_site()

    if args.dev:
        serve_and_watch(args.port)


if __name__ == "__main__":
    main()
```

Note: `serve_and_watch()` is defined in Task 5. For now the script builds but `--dev` will error.

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_build.py -v`
Expected: all 4 tests PASS

- [ ] **Step 5: Commit**

```bash
git add build.py tests/test_build.py
git commit -m "feat: add build script core — config loading, content discovery, markdown rendering"
```

---

## Task 3: Templates — base.html, page.html, session.html, day.html

**Files:**
- Create: `templates/base.html`
- Create: `templates/page.html`
- Create: `templates/session.html`
- Create: `templates/day.html`

- [ ] **Step 1: Create `templates/base.html`**

This master layout reproduces the existing HTML structure: banner, nav, container, footer.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}{{ page.title }} — {{ site.title }}{% endblock %}</title>
  <meta name="description" content="{{ page.description }}">
  <meta property="og:title" content="{{ page.title }}">
  <meta property="og:description" content="{{ page.description }}">
  <meta property="og:image" content="{{ site.url }}/{{ site.og_image }}">
  <meta property="og:url" content="{{ site.url }}/{{ page.url }}">
  <meta property="og:type" content="{% if page.template == 'session' %}article{% else %}website{% endif %}">
  <meta property="og:site_name" content="{{ site.title }}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{{ page.title }}">
  <meta name="twitter:description" content="{{ page.description }}">
  <meta name="twitter:image" content="{{ site.url }}/{{ site.og_image }}">
  <link rel="stylesheet" href="style.css">
  {% block head_extra %}{% endblock %}
</head>
<body>

  <div class="banner">
    <img src="{{ site.banner_image }}" alt="{{ site.banner_alt }}">
  </div>
  <nav>
    <ul>
      {% for link in site.nav %}
      <li><a href="{{ link.url }}"{% if link.url == nav_active %} class="active"{% endif %}>{{ link.label }}</a></li>
      {% endfor %}
    </ul>
  </nav>

  <div class="container">
    {% block breadcrumbs %}{% endblock %}
    {% block content %}{% endblock %}
  </div>

  <div class="footer">
    <img src="{{ site.footer_image }}" alt="Chicago skyline">
    <div class="footer-text">
      {% for link in site.footer_links %}
      <a href="{{ link.url }}">{{ link.label }}</a>{% if not loop.last %} &middot; {% endif %}
      {% endfor %}
       &middot; &#9999;&#65039; <a href="{{ site.repo }}/issues/new?title=Correction:+{{ page.title | urlencode }}&body=Page:+{{ page.url }}%0A%0ACorrection:">Suggest a correction</a>
    </div>
  </div>

</body>
</html>
```

- [ ] **Step 2: Create `templates/page.html`**

```html
{% extends "base.html" %}

{% block content %}
<h1>{{ page.title }}</h1>
{% if page.page_subtitle %}<p class="subtitle">{{ page.page_subtitle }}</p>{% endif %}

{{ content }}
{% endblock %}
```

- [ ] **Step 3: Create `templates/session.html`**

```html
{% extends "base.html" %}

{% block breadcrumbs %}
<div class="breadcrumb"><a href="index.html">Home</a> / <a href="{{ page.day }}.html">{{ page.day | title }}, {{ page.date }}</a> / {{ page.title }}</div>
{% endblock %}

{% block content %}
<h1>{{ page.title }}</h1>
<p class="page-subtitle">
  {%- if page.speakers_display %}{{ page.speakers_display }} &middot; {% endif -%}
  {{ page.day | title }}, {{ page.date }}
</p>

{% if page.speakers %}
<div class="card">
  <p><strong>Speaker{{ 's' if page.speakers | length > 1 else '' }}:</strong>
    {% for sid in page.speakers %}
    <a href="speakers.html#{{ sid }}">{{ speakers[sid].name if sid in speakers else sid }}</a>{% if not loop.last %}, {% endif %}
    {% endfor %}
  </p>
</div>
{% endif %}

{{ content }}
{% endblock %}
```

- [ ] **Step 4: Create `templates/day.html`**

```html
{% extends "base.html" %}

{% block breadcrumbs %}
<div class="breadcrumb"><a href="index.html">Home</a> / {{ page.title }}</div>
{% endblock %}

{% block content %}
<h1>{{ page.title }}</h1>
{% if page.page_subtitle %}<p class="page-subtitle">{{ page.page_subtitle }}</p>{% endif %}

{{ content }}

{% set day_sessions = get_sessions_for_day(pages, page.day) %}
{% if day_sessions %}
<h2>Session Notes from This Day</h2>
<div class="section-list">
  {% for session in day_sessions %}
  <a class="day-card" href="{{ session.url }}">
    <div class="day-info">
      <h3>{{ session.title }}</h3>
      <p>{{ session.description }}</p>
    </div>
  </a>
  {% endfor %}
</div>
{% endif %}
{% endblock %}
```

- [ ] **Step 5: Create a test content file and verify build**

Create `content/test.md`:

```markdown
---
title: "Test Page"
template: page
description: "A test page to verify the build pipeline works."
---

## Hello

This is a test page with **bold** and a [link](https://example.com).
```

Run: `uv run python build.py --clean`
Expected: `docs/test.html` is created. Open it and verify it has the banner, nav, styled content, and footer.

- [ ] **Step 6: Remove test file, commit templates**

```bash
rm content/test.md docs/test.html
git add templates/
git commit -m "feat: add base, page, session, and day templates"
```

---

## Task 4: Index + Speakers Templates

**Files:**
- Create: `templates/index.html`
- Create: `templates/speakers.html`
- Modify: `static/style.css` — append speaker card CSS from `docs/speakers.html`

- [ ] **Step 1: Create `templates/index.html`**

The homepage template renders structured data from the index.md frontmatter: stats, day grid, deep dives, tracks, and attendance table.

```html
{% extends "base.html" %}

{% block title %}{{ site.title }}{% endblock %}

{% block content %}
<h1>{{ site.title }}</h1>
<p class="subtitle">{{ site.subtitle }}</p>

<div class="info-bar">
  <div>
    <span class="label">When</span>
    <span class="value">{{ site.conference.when }}</span>
  </div>
  <div>
    <span class="label">Where</span>
    <span class="value">{{ site.conference.where }}</span>
  </div>
  <div>
    <span class="label">Schedule</span>
    <span class="value"><a href="{{ site.schedule_url }}">iug2026.sched.com</a></span>
  </div>
  <div>
    <span class="label">Source</span>
    <span class="value"><a href="{{ site.repo }}">GitHub Repo</a></span>
  </div>
</div>

{% if page.stats %}
<div class="stats-row">
  {% for stat in page.stats %}
  <div class="stat">
    <div class="number">{{ stat.number }}</div>
    <div class="stat-label">{{ stat.label }}</div>
  </div>
  {% endfor %}
</div>
{% endif %}

<h2>Session Notes</h2>
<div class="day-grid">
  {% for day in page.days %}
  <a class="day-card" href="{{ day.url }}">
    <div class="day-date">
      <div class="dow">{{ day.dow }}</div>
      <div class="num">{{ day.num }}</div>
      <div class="month">{{ day.month }}</div>
    </div>
    <div class="day-info">
      <h3>{{ day.title }}</h3>
      <p>{{ day.description }}</p>
    </div>
  </a>
  {% endfor %}
</div>

<h2>Deep Dives</h2>
<div class="section-list">
  {% for dive in page.deep_dives %}
  <a class="day-card" href="{{ dive.url }}">
    <div class="day-info">
      <h3>{{ dive.title }}</h3>
      <p>{{ dive.description }}</p>
    </div>
  </a>
  {% endfor %}
</div>

<h2>Conference Tracks</h2>
<div class="tracks">
  {% for track in site.tracks %}
  <div class="track-card {{ track.css_class }}"><h3>{{ track.name }}</h3><p>{{ track.description }}</p></div>
  {% endfor %}
</div>

{% if page.attendance %}
<h2>Post-COVID Attendance</h2>
<table>
  <thead><tr><th>Year</th><th>Location</th><th>Attendance</th></tr></thead>
  <tbody>
    {% for row in page.attendance %}
    <tr{% if row.current %} class="current"{% endif %}><td>{% if row.current %}<strong>{{ row.year }}</strong>{% else %}{{ row.year }}{% endif %}</td><td>{{ row.location }}</td><td>{% if row.current %}<strong>{{ row.count }}</strong>{% else %}{{ row.count }}{% endif %}</td></tr>
    {% endfor %}
  </tbody>
</table>
{% endif %}

{{ content }}
{% endblock %}
```

- [ ] **Step 2: Extract speaker card CSS from `docs/speakers.html` into `static/style.css`**

Read the `<style>` block from `docs/speakers.html` (the speaker-grid, speaker-card, rarity-badge, and related styles). Append them to the end of `static/style.css` under a `/* Speaker Cards */` comment.

The inline styles to extract are everything inside the `<style>` tag in `docs/speakers.html` — approximately 100 lines of CSS covering `.speaker-grid`, `.speaker-card`, `.card-top`, `.card-body`, `.card-header`, `.rarity-badge`, `.speaker-name`, `.speaker-affiliation`, `.speaker-type`, `.speaker-quote`, `.stat-blocks`, `.session-toggle`, `.session-list`, `.session-entry`, and the rarity tier colors.

- [ ] **Step 3: Create `templates/speakers.html`**

Server-side rendered from `data/speakers.json`. Replaces the client-side JS approach.

```html
{% extends "base.html" %}

{% block content %}
<h1>{{ page.title }}</h1>
{% if page.page_subtitle %}<p class="page-subtitle">{{ page.page_subtitle }}</p>{% endif %}

{% set all_speakers = speakers.values() | sort(attribute='name') %}
{% set all_sessions = [] %}
{% for s in all_speakers %}{% for sess in s.sessions %}{% if all_sessions.append(sess) %}{% endif %}{% endfor %}{% endfor %}
{% set legendary_count = all_speakers | selectattr('rarity.tier', 'equalto', 'legendary') | list | length %}

<div class="stats-row">
  <div class="stat"><div class="number">{{ all_speakers | length }}</div><div class="stat-label">Speakers</div></div>
  <div class="stat"><div class="number">{{ all_sessions | length }}</div><div class="stat-label">Sessions Tracked</div></div>
  <div class="stat"><div class="number">{{ all_speakers | map(attribute='year_count') | max }}</div><div class="stat-label">Years Covered</div></div>
  <div class="stat"><div class="number">{{ legendary_count }}</div><div class="stat-label">Legendary</div></div>
</div>

<div class="speaker-grid">
  {% for speaker in all_speakers | sort(attribute='session_count', reverse=true) %}
  <div class="speaker-card" id="{{ speaker.id }}">
    <div class="card-top {{ speaker.primaryTrack or speaker.unique_tracks[0] or 'general' }}"></div>
    <div class="card-body">
      <div class="card-header">
        <span class="rarity-badge rarity-{{ speaker.rarity.tier }}">{{ speaker.rarity.label }}</span>
        <span class="track-icon">{{ speaker.primaryTrack or speaker.unique_tracks[0] or 'general' }}</span>
      </div>
      <div class="speaker-name">{{ speaker.name }}</div>
      {% if speaker.affiliation %}<div class="speaker-affiliation">{{ speaker.affiliation }}</div>{% endif %}
      {% if speaker.type %}<div class="speaker-type">{{ speaker.type }}</div>{% else %}<div class="speaker-type">&nbsp;</div>{% endif %}
      <div class="stat-blocks">
        <div class="stat-block"><div class="stat-num">{{ speaker.sessions | length }}</div><div class="stat-lbl">sessions</div></div>
        <div class="stat-block"><div class="stat-num">{{ speaker.unique_years | length }}</div><div class="stat-lbl">years</div></div>
        <div class="stat-block"><div class="stat-num">{{ speaker.unique_tracks | length }}</div><div class="stat-lbl">tracks</div></div>
      </div>
      {% if speaker.quote %}
      <div class="speaker-quote">"{{ speaker.quote }}"{% if speaker.quoteContext %}<span class="quote-ctx">&mdash; {{ speaker.quoteContext }}</span>{% endif %}</div>
      {% endif %}
      <button class="session-toggle" onclick="this.classList.toggle('open'); this.nextElementSibling.classList.toggle('open')">
        <span class="arrow">&#9656;</span> Session History ({{ speaker.sessions | length }})
      </button>
      <div class="session-list">
        {% for s in speaker.sessions_sorted %}
        <div class="session-entry">
          <span class="session-year">{{ s.year }}</span>
          {% if s.schedUrl %}<a href="{{ s.schedUrl }}">{{ s.title }}</a>{% else %}{{ s.title }}{% endif %}
          <span class="session-role">({{ s.role }})</span>
        </div>
        {% endfor %}
      </div>
    </div>
  </div>
  {% endfor %}
</div>
{% endblock %}
```

- [ ] **Step 4: Commit**

```bash
git add templates/index.html templates/speakers.html static/style.css
git commit -m "feat: add index and speakers templates, consolidate speaker card CSS"
```

---

## Task 5: Dev Server + CLI

**Files:**
- Modify: `build.py` — add `serve_and_watch()` function

- [ ] **Step 1: Add the dev server and file watcher to `build.py`**

Append before the `main()` function:

```python
def serve_and_watch(port):
    """Start HTTP server and file watcher. Blocks until Ctrl+C."""

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(OUTPUT_DIR), **kwargs)

        def log_message(self, format, *args):
            # Suppress per-request logs to keep rebuild output visible
            pass

    server = http.server.HTTPServer(("0.0.0.0", port), Handler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    print(f"Serving on http://0.0.0.0:{port}")

    try:
        from watchdog.events import FileSystemEventHandler
        from watchdog.observers import Observer

        class RebuildHandler(FileSystemEventHandler):
            def __init__(self):
                self._timer = None

            def on_any_event(self, event):
                if event.src_path.startswith(str(OUTPUT_DIR)):
                    return
                if self._timer:
                    self._timer.cancel()
                self._timer = threading.Timer(0.3, self._rebuild)
                self._timer.start()

            def _rebuild(self):
                print("\nChange detected, rebuilding...")
                try:
                    build_site()
                    print("Ready.")
                except Exception as e:
                    print(f"Build error: {e}")

        observer = Observer()
        handler = RebuildHandler()
        for watch_dir in [CONTENT_DIR, TEMPLATE_DIR, STATIC_DIR, DATA_DIR]:
            if watch_dir.exists():
                observer.schedule(handler, str(watch_dir), recursive=True)
        observer.start()
        print("Watching for changes... (Ctrl+C to stop)")

        server_thread.join()
    except KeyboardInterrupt:
        print("\nStopping...")
        observer.stop()
        server.shutdown()
```

- [ ] **Step 2: Test dev server**

Run: `uv run python build.py --dev`
Expected: "Serving on http://0.0.0.0:8000" and "Watching for changes..." printed. Site accessible at `http://<tailscale-ip>:8000`. Ctrl+C stops cleanly.

- [ ] **Step 3: Commit**

```bash
git add build.py
git commit -m "feat: add dev server with file watching and auto-rebuild"
```

---

## Task 6: Content Migration — Index + Day Overview Pages

**Files:**
- Create: `content/index.md`
- Create: `content/sunday.md`
- Create: `content/monday.md`
- Create: `content/tuesday.md`
- Create: `content/wednesday.md`

For each page: read the existing HTML in `docs/`, extract the content into markdown+frontmatter. For `monday.md`, also read `sessions/monday-apr13.md` and merge any unique content.

- [ ] **Step 1: Create `content/index.md`**

Read `docs/index.html`. Extract the structured data into frontmatter, and any prose content into the markdown body.

Frontmatter must include:
```yaml
---
title: "IUG 2026 Conference Notes"
template: index
description: "Notes from the Innovative Users Group 2026 conference in Chicago — 412 attendees, 4 days, 5 tracks covering Sierra, Polaris, and Vega platforms."
stats:
  - number: "412"
    label: Attendees
  - number: "130+"
    label: First-timers
  - number: "4"
    label: Days
  - number: "5"
    label: Tracks
days:
  - url: sunday.html
    dow: Sun
    num: "12"
    month: Apr
    title: Pre-Conference
    description: "The Great ILS-Data Pre-Conference, Hackathon, workshops"
  - url: monday.html
    dow: Mon
    num: "13"
    month: Apr
    title: "Day 1 — Opening Session"
    description: "Beacon Award, AI framework, Rapido launch, Vega Reports, Amazon Business, Innovation Awards, IUG 2027 announcement"
  - url: tuesday.html
    dow: Tue
    num: "14"
    month: Apr
    title: "Day 2 — Breakout Sessions"
    description: "Resource sharing (Rapido), SQL, Python automation, AI session, Vega Reports deep dive, forums"
  - url: wednesday.html
    dow: Wed
    num: "15"
    month: Apr
    title: "Day 3 — Final Sessions"
    description: "Sierra APIs, system admin forums, leadership panel, trivia night"
deep_dives:
  - url: sierra-roadmap.html
    title: Sierra Roadmap
    description: "May & November 2026 releases, Admin Corner migration, ERM → Alma Starter, Vega integrations, MEEP enhancements"
  - url: amazon-business.html
    title: Amazon Business EDI Integration
    description: "CHPL (Cincinnati) as early adopter, Sierra acquisitions API, implementation advice"
  - url: hackathon-awards.html
    title: Hackathon Awards
    description: "Six projects: FindIt (shelf mapping), Browsr, Shelf Defense (winner — offline circ), Leap SQL, Auto-Suggest-a-Purchase, Microprojects (Sierra bulk editing)"
  - url: resource-sharing.html
    title: Resource Sharing Update
    description: "Rapido CB across SearchOhio/OhioLINK (110+ libraries, 4 ILSs), Rapido stand-alone (5.5M requests, 96% fill rate), San Diego next — late June 2026"
  - url: sierra-year-in-review.html
    title: Sierra Year in Review
    description: "Sierra 6.4 & 6.5 releases: patron checkout limits, inventory check-in at circ desk, Admin Corner migration, Create Lists navigation, IMMS enhancements"
  - url: ai-the-right-way.html
    title: "AI The Right Way: Smarter Tools, Stronger Outcomes"
    description: "Clarivate's Responsible AI framework, product roadmap (Data Explorer, Metadata Assistant, Acquisitions Agent), Pulse of the Library 2025 data, Q&A on vibe coding catalogs. 25 sources."
  - url: floating-collections-bof.html
    title: Floating Collections BoF
    description: "Smart routing, bulk holds, Sierra API gaps, Vega Reports for collection analytics"
  - url: meep.html
    title: MEEP
    description: "Member-Exclusive Enhancement Process — how ideas become guaranteed enhancements, voting, Idea Exchange tips"
  - url: vega-reports.html
    title: "Vega Reports & Analytics"
    description: "Data lakehouse strategy, Vega Reports for Discover, early access customers, future roadmap"
  - url: executive-panel.html
    title: Executive Leadership Panel
    description: "Sierra's future (400+ customers), Vega platform strategy, Alma Specto, mobile apps, 3–5 year vision, public library headwinds, Knowledge Portal, communication improvements."
  - url: cataloging-without-oclc.html
    title: Cataloging without OCLC
    description: "Boise Public Library's journey: evaluating Sky River, BestMark, and Bookware after leaving OCLC. Cost savings from six digits to three."
  - url: sierra-sso.html
    title: "Sierra Staff & Single Sign-On"
    description: "SAML SSO for Sierra staff auth at RIT, MFA practices, Keycloak unification plans, cyber insurance, passwordless. Includes technical implementation guide."
  - url: sierra-sys-admin-forum.html
    title: Sierra Sys Admin Forum
    description: "Migration debates (Sierra vs. Polaris/Koha), bot protection & Cloudflare, paging lists, SDA vs. Sierra Web, WCAG accessibility, circ active. Includes Cloudflare protection guide."
  - url: "https://github.com/iug-ils-data-preconf/iug2026"
    title: The Great ILS-Data Preconference
    description: "Sunday pre-conference: data visualization, regex, APIs, Datasette, data lakes, privacy, AMH logs, Python CLI tools, and more"
  - url: speakers.html
    title: Speaker Cards
    description: "Conference speaker gallery — presentation history, stats, and rarity tiers across all IUG years"
attendance:
  - year: 2026
    location: Chicago
    count: "412"
    current: true
  - year: 2025
    location: Denver
    count: "502"
  - year: 2024
    location: Detroit
    count: "~400"
  - year: 2019
    location: "Phoenix (pre-COVID)"
    count: "700+"
---
```

The markdown body should be empty (all index content is structured data in the frontmatter and site.yaml).

- [ ] **Step 2: Create day overview pages**

For each day page, read the existing HTML and extract content.

**`content/sunday.md`**: Read `docs/sunday.html`. No markdown counterpart exists.
```yaml
---
title: "Sunday, April 12"
template: day
date: "April 12"
day: sunday
page_subtitle: "Pre-Conference Day"
description: "<extract from docs/sunday.html meta description>"
---
```
Markdown body: convert the HTML content sections into markdown.

**`content/monday.md`**: Read both `docs/monday.html` AND `sessions/monday-apr13.md`. Merge content — the HTML has the polished "update feed" structure, the markdown may have additional raw notes.
```yaml
---
title: "Monday, April 13"
template: day
date: "April 13"
day: monday
page_subtitle: "Opening Session · Day 1"
description: "<extract from docs/monday.html meta description>"
---
```

**`content/tuesday.md`**: Read `docs/tuesday.html`. No markdown counterpart.
```yaml
---
title: "Tuesday, April 14"
template: day
date: "April 14"
day: tuesday
page_subtitle: "Breakout Sessions · Day 2"
description: "<extract from docs/tuesday.html meta description>"
---
```

**`content/wednesday.md`**: Read `docs/wednesday.html`. No markdown counterpart.
```yaml
---
title: "Wednesday, April 15"
template: day
date: "April 15"
day: wednesday
page_subtitle: "Final Sessions · Day 3"
description: "<extract from docs/wednesday.html meta description>"
---
```

**Important note on day pages**: The existing HTML day pages contain rich structured content (update-feed divs, card layouts, section lists). Some of this structure does not translate to plain markdown. You have two options per section:

1. Convert to markdown (when the content is paragraph/list-based)
2. Use raw HTML in the markdown body (when the existing card/feed structure is essential to the presentation)

Prefer markdown where possible. Use raw HTML sparingly for sections that truly need it (like the Monday update-feed cards).

- [ ] **Step 3: Build and compare**

Run: `uv run python build.py --clean`

For each page, compare the generated HTML output against the original hand-authored HTML. Check:
- Title and meta tags render correctly
- Navigation bar shows with correct active state
- Content sections are present and match
- Footer renders with correct page-specific correction link

- [ ] **Step 4: Commit**

```bash
git add content/index.md content/sunday.md content/monday.md content/tuesday.md content/wednesday.md
git commit -m "feat: migrate index and day overview pages to content/markdown"
```

---

## Task 7: Content Reconciliation — Session Pages

This is the largest task. For each of the 12 session pages that have both HTML and markdown sources, reconcile them into a single canonical content file.

**Files:**
- Create 12 files in `content/`:
  - `sierra-roadmap.md`
  - `amazon-business.md`
  - `hackathon-awards.md`
  - `ai-the-right-way.md`
  - `floating-collections-bof.md`
  - `meep.md`
  - `resource-sharing.md`
  - `sierra-year-in-review.md`
  - `vega-reports.md`
  - `cataloging-without-oclc.md`
  - `executive-panel.md`
  - `sierra-sys-admin-forum.md`

- [ ] **Step 1: Reconciliation process (repeat for each page)**

For each session page, follow this process:

1. Read the HTML file (`docs/<name>.html`)
2. Read the markdown file (`sessions/<day>-<date>-<name>.md`)
3. Extract frontmatter from the HTML:
   - `title`: from `<h1>` tag
   - `description`: from `<meta name="description">` content
   - `template`: `session`
   - `day`: from breadcrumb (monday/tuesday/wednesday)
   - `date`: from the page subtitle (e.g., "April 13")
   - `speakers`: list of speaker IDs from `speakers.html#<id>` links
   - `speakers_display`: the display text from the subtitle (e.g., "Mike Dicus")
   - `track`, `room`, `time`: from the info-bar or subtitle if present
4. Compare the content:
   - What sections exist in HTML but not in markdown?
   - What content exists in markdown but not in HTML?
   - Where do they differ?
5. Merge: take the polished structure from HTML, add any unique content from markdown
6. Convert the merged content to markdown (preserving raw HTML only where card/structured layout is essential)
7. Write the result to `content/<name>.md`

**Source mapping for reference:**

| Content file | HTML source | Markdown source |
|---|---|---|
| `sierra-roadmap.md` | `docs/sierra-roadmap.html` | `sessions/monday-apr13-sierra-roadmap.md` |
| `amazon-business.md` | `docs/amazon-business.html` | `sessions/monday-apr13-amazon-business.md` |
| `hackathon-awards.md` | `docs/hackathon-awards.html` | `sessions/monday-apr13-hackathon-awards.md` |
| `ai-the-right-way.md` | `docs/ai-the-right-way.html` | `sessions/tuesday-apr14-ai-the-right-way.md` |
| `floating-collections-bof.md` | `docs/floating-collections-bof.html` | `sessions/tuesday-apr14-floating-collections-bof.md` |
| `meep.md` | `docs/meep.html` | `sessions/tuesday-apr14-meep.md` |
| `resource-sharing.md` | `docs/resource-sharing.html` | `sessions/tuesday-apr14-resource-sharing.md` |
| `sierra-year-in-review.md` | `docs/sierra-year-in-review.html` | `sessions/tuesday-apr14-sierra-year-in-review.md` |
| `vega-reports.md` | `docs/vega-reports.html` | `sessions/tuesday-apr14-vega-reports.md` |
| `cataloging-without-oclc.md` | `docs/cataloging-without-oclc.html` | `sessions/wednesday-apr15-cataloging-without-oclc.md` |
| `executive-panel.md` | `docs/executive-panel.html` | `sessions/wednesday-apr15-executive-panel.md` |
| `sierra-sys-admin-forum.md` | `docs/sierra-sys-admin-forum.html` | `sessions/wednesday-apr15-sierra-sys-admin-forum.md` |

- [ ] **Step 2: Build and verify each migrated session**

After creating each content file, run: `uv run python build.py`

Compare `docs/<name>.html` output against the original. Verify:
- Title, description, breadcrumbs correct
- Speaker links resolve to `speakers.html#<id>`
- All content sections present
- No content lost from either source

- [ ] **Step 3: Commit the batch**

```bash
git add content/sierra-roadmap.md content/amazon-business.md content/hackathon-awards.md content/ai-the-right-way.md content/floating-collections-bof.md content/meep.md content/resource-sharing.md content/sierra-year-in-review.md content/vega-reports.md content/cataloging-without-oclc.md content/executive-panel.md content/sierra-sys-admin-forum.md
git commit -m "feat: reconcile and migrate 12 session pages to content/markdown"
```

---

## Task 8: Content Migration — Guides + HTML-Only Pages

**Files:**
- Create: `content/cloudflare-sierra-guide.md`
- Create: `content/sierra-sso-guide.md`
- Create: `content/suggest-a-purchase.md`
- Create: `content/sierra-sso.md`
- Create: `content/speakers.md`

- [ ] **Step 1: Migrate `cloudflare-sierra-guide`**

Sources: `docs/cloudflare-sierra-guide.html` (1150 lines, with inline CSS for vibedAF badge) and `resources/cloudflare-sierra-protection.md` (30KB detailed guide).

These are related but different depths. Read both, then decide: is the HTML a summary of the markdown resource, or are they covering the same content differently?

Reconcile into `content/cloudflare-sierra-guide.md` with:
```yaml
---
title: "Cloudflare Protection for Sierra"
template: session
day: wednesday
date: "April 15"
description: "<from HTML meta>"
speakers_display: "<from HTML if present>"
---
```

The vibedAF badge CSS should already be in `static/style.css` (or add it now if not already extracted). Use a raw HTML snippet in the markdown body for the badge element if it needs to be preserved.

- [ ] **Step 2: Migrate `sierra-sso-guide`**

Sources: `docs/sierra-sso-guide.html` and `sessions/wednesday-apr15-sierra-sso-technical-guide.md`.

```yaml
---
title: "Sierra SSO Technical Implementation Guide"
template: session
day: wednesday
date: "April 15"
description: "<from HTML meta>"
---
```

- [ ] **Step 3: Migrate `suggest-a-purchase`**

Source: `docs/suggest-a-purchase.html` only (no markdown counterpart).

```yaml
---
title: "Suggest-a-Purchase Comparison"
template: page
description: "<from HTML meta>"
---
```

Convert the HTML content to markdown.

- [ ] **Step 4: Migrate `sierra-sso`**

Source: `docs/sierra-sso.html` only (no markdown counterpart). This is an informal gathering page (separate from the technical guide).

```yaml
---
title: "Sierra Staff & Single Sign-On"
template: session
day: wednesday
date: "April 15"
description: "<from HTML meta>"
---
```

- [ ] **Step 5: Create `content/speakers.md`**

This is minimal — the template does all the rendering from `data/speakers.json`.

```yaml
---
title: "Speaker Cards"
template: speakers
page_subtitle: "Presentation history, stats, and rarity tiers across all IUG years"
description: "IUG conference speaker cards — presentation history, stats, and personality across all IUG years."
---
```

No markdown body needed.

- [ ] **Step 6: Build and verify**

Run: `uv run python build.py --clean`

Verify all 22 pages render correctly. Spot-check:
- `index.html` — stats, day grid, deep dives list, tracks, attendance table
- `monday.html` — content sections, session listing auto-generated
- `sierra-roadmap.html` — breadcrumbs, speaker link, content sections
- `speakers.html` — gallery renders with all speakers, rarity badges, session history toggles
- `cloudflare-sierra-guide.html` — vibedAF badge renders, content complete

- [ ] **Step 7: Commit**

```bash
git add content/cloudflare-sierra-guide.md content/sierra-sso-guide.md content/suggest-a-purchase.md content/sierra-sso.md content/speakers.md
git commit -m "feat: migrate guides, HTML-only pages, and speakers page to content/markdown"
```

---

## Task 9: Cleanup + Final Verification

**Files:**
- Delete: `sessions/` directory
- Delete: `resources/` directory
- Delete: `docs/superpowers/` directory (already moved to `specs/` and `plans/`)
- Modify: `.gitignore` — add rules for build output

- [ ] **Step 1: Full build from clean state**

Run: `uv run python build.py --clean`

Verify all 22 pages are generated in `docs/`. List them:

```bash
ls docs/*.html | wc -l
```

Expected: 22 HTML files.

- [ ] **Step 2: Compare old vs new output**

For a representative sample of pages, diff the structure of old (git show HEAD:docs/file.html) vs new (docs/file.html). Check:
- All navigation links work
- All inter-page links work
- All speaker links resolve to correct anchors
- OG meta tags have correct values
- Footer correction links are page-specific
- Banner and skyline images render

- [ ] **Step 3: Clean up old source directories**

```bash
rm -rf sessions/
rm -rf resources/
rm -rf docs/superpowers/
```

- [ ] **Step 4: Update `.gitignore`**

Add to `.gitignore`:

```
# Build output (regenerated by build.py)
docs/*.html
docs/style.css
docs/assets/
docs/photos/
docs/transcripts/
```

Note: we gitignore the build output files but NOT the `docs/` directory itself (GitHub Pages needs it to exist).

**Important consideration**: If the site is deployed via GitHub Pages from the `docs/` folder, the build output MUST be committed. In that case, do NOT gitignore the docs output. Instead, just commit the generated files. The choice depends on your deployment setup:

- **Option A (commit build output)**: Don't gitignore docs. Run `build.py` before committing. GitHub Pages serves directly from committed files.
- **Option B (CI builds)**: Gitignore docs. Use a GitHub Action to build and deploy. Cleaner git history but more setup.

Ask the user which approach they prefer. For now, assume Option A (simpler, matches current workflow).

- [ ] **Step 5: Run all tests**

```bash
uv run pytest tests/ -v
```

Expected: all tests pass.

- [ ] **Step 6: Start dev server and do a manual walkthrough**

```bash
uv run python build.py --dev
```

Navigate through the site via Tailscale. Check:
- Home page loads, all links work
- Each day page shows session listings
- Each session page has breadcrumbs, speaker links, content
- Speaker gallery renders, session history toggles work
- Cloudflare guide has vibedAF badge
- Footer correction links are per-page

- [ ] **Step 7: Commit cleanup**

```bash
git add -A
git commit -m "chore: remove old source directories, finalize site refactor"
```

- [ ] **Step 8: Final summary commit**

If all verifications pass, optionally squash or tag:

```bash
git tag v2.0-refactor
```
