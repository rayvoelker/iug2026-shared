# Navigation & Usability Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix link affordance site-wide, build two homepage variant templates for A/B comparison, and add `llms.txt` agent navigation.

**Architecture:** CSS-only link fixes in `style.css`, two new index templates driven by restructured frontmatter in `content/index.md` and `content/index-b.md`, and a new `generate_llms_txt()` function in `build.py`.

**Tech Stack:** Jinja2 templates, CSS, Python (build.py)

**Spec:** `specs/2026-04-17-navigation-redesign-design.md`

---

## File Map

### Modify

- `static/style.css` — link affordance CSS fixes
- `templates/base.html` — add `<link>` tag for llms.txt
- `templates/index.html` — rewrite for variant A ("Sessions-first")
- `content/index.md` — restructure frontmatter: replace `deep_dives` with `sessions_by_day` and `guides`
- `build.py` — add `generate_llms_txt()` function

### Create

- `templates/index-b.html` — variant B ("Hub") template
- `content/index-b.md` — variant B content file (temporary, removed after A/B decision)

---

## Task 1: CSS Link Affordance Fixes

**Files:**
- Modify: `static/style.css`

- [ ] **Step 1: Fix global text link styles**

In `static/style.css`, replace the existing link rules (lines 21-22):

```css
a { color: var(--teal); text-decoration: none; }
a:hover { text-decoration: underline; }
```

With:

```css
a { color: var(--teal); }
a:hover { color: #004d63; }
```

This makes links underlined by default (browser default) and darkens on hover.

- [ ] **Step 2: Fix container link styles**

Add after the `.container` rule (line 54):

```css
/* Links in content areas — clearly underlined */
.container a { text-decoration: underline; text-underline-offset: 2px; }
.container a:hover { color: #004d63; }

/* Exceptions: cards, nav elements, and headings shouldn't be underlined */
.container a.day-card { text-decoration: none; }
.container .breadcrumb a { text-decoration: none; }
.container .breadcrumb a:hover { text-decoration: underline; }
.container h1 a, .container h2 a, .container h3 a { text-decoration: none; }
.container h1 a:hover, .container h2 a:hover, .container h3 a:hover { text-decoration: underline; }
```

- [ ] **Step 3: Fix nav bar styles**

Replace the existing nav link rules (lines 43-51):

```css
nav a {
  color: rgba(255,255,255,0.7);
  padding: 0.35rem 0.75rem;
  border-radius: 4px;
  font-size: 0.85rem;
  transition: all 0.15s;
}
nav a:hover { color: white; background: rgba(255,255,255,0.1); text-decoration: none; }
nav a.active { color: white; background: rgba(255,255,255,0.15); font-weight: 600; }
```

With:

```css
nav a {
  color: rgba(255,255,255,0.75);
  padding: 0.4rem 0.85rem;
  border-radius: 4px;
  font-size: 0.9rem;
  transition: all 0.15s;
  text-decoration: none;
  border-bottom: 2px solid transparent;
}
nav a:hover {
  color: white;
  background: rgba(255,255,255,0.12);
  text-decoration: none;
}
nav a.active {
  color: white;
  background: rgba(255,255,255,0.18);
  font-weight: 600;
  border-bottom-color: var(--gold);
}
```

Changes: larger font (0.85→0.9rem), larger padding, gold bottom border on active link, more visible hover background.

- [ ] **Step 4: Fix card hover states**

Replace the existing day-card hover rule (line 103):

```css
a.day-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.15); text-decoration: none; }
```

With:

```css
a.day-card {
  text-decoration: none;
  cursor: pointer;
  transition: box-shadow 0.15s, border-left-color 0.15s;
  border-left: 3px solid transparent;
}
a.day-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  text-decoration: none;
  border-left-color: var(--teal);
}
```

- [ ] **Step 5: Fix footer link styles**

Replace the existing footer text rule (line 168):

```css
.footer-text { padding: 1rem; font-size: 0.85rem; color: #999; }
```

With:

```css
.footer-text { padding: 1rem; font-size: 0.85rem; color: #999; }
.footer-text a { text-decoration: underline; color: #999; }
.footer-text a:hover { color: var(--teal); }
```

- [ ] **Step 6: Build and visually verify**

Run: `uv run python build.py`

Check in browser:
- Content links are underlined, darken on hover
- Nav links are larger, active link has gold bottom border
- Card hover shows left border accent and shadow
- Footer links are underlined
- No visual regressions on session, day, or speakers pages

- [ ] **Step 7: Commit**

```bash
git add static/style.css
git commit -m "style: fix link affordance — underlines, nav contrast, card hover states"
```

---

## Task 2: Homepage Variant A — "Sessions-First"

**Files:**
- Modify: `templates/index.html`
- Modify: `content/index.md`

- [ ] **Step 1: Restructure `content/index.md` frontmatter**

Replace the `deep_dives` list with `sessions_by_day` (grouped) and `guides` (separate). Keep `stats`, `days`, and `attendance` unchanged.

Write the full new `content/index.md`:

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
sessions_by_day:
  - day: Sunday
    day_url: sunday.html
    sessions:
      - url: "https://github.com/iug-ils-data-preconf/iug2026"
        title: The Great ILS-Data Preconference
        description: "Data visualization, regex, APIs, Datasette, data lakes, privacy, AMH logs, Python CLI tools, and more"
  - day: Monday
    day_url: monday.html
    sessions:
      - url: sierra-roadmap.html
        title: Sierra Roadmap
        description: "May & November 2026 releases, Admin Corner migration, ERM → Alma Starter, Vega integrations"
      - url: amazon-business.html
        title: Amazon Business EDI Integration
        description: "CHPL (Cincinnati) as early adopter, Sierra acquisitions API, implementation advice"
      - url: hackathon-awards.html
        title: Hackathon Awards
        description: "Six projects: FindIt, Browsr, Shelf Defense (winner), Leap SQL, Auto-Suggest-a-Purchase, Microprojects"
  - day: Tuesday
    day_url: tuesday.html
    sessions:
      - url: ai-the-right-way.html
        title: "AI The Right Way"
        description: "Responsible AI framework, product roadmap, Pulse of the Library data, vibe coding Q&A"
      - url: vega-reports.html
        title: "Vega Reports & Analytics"
        description: "Data lakehouse strategy, early access customers, future roadmap"
      - url: resource-sharing.html
        title: Resource Sharing Update
        description: "Rapido across SearchOhio/OhioLINK, 110+ libraries, 96% fill rate"
      - url: sierra-year-in-review.html
        title: Sierra Year in Review
        description: "Sierra 6.4 & 6.5: checkout limits, inventory check-in, Admin Corner, Create Lists"
      - url: floating-collections-bof.html
        title: Floating Collections BoF
        description: "Smart routing, bulk holds, Sierra API gaps, Vega Reports analytics"
      - url: meep.html
        title: MEEP
        description: "How ideas become guaranteed enhancements, voting, Idea Exchange tips"
  - day: Wednesday
    day_url: wednesday.html
    sessions:
      - url: executive-panel.html
        title: Executive Leadership Panel
        description: "Sierra's future, Vega strategy, Alma Specto, mobile apps, 3–5 year vision"
      - url: cataloging-without-oclc.html
        title: Cataloging without OCLC
        description: "Boise PL's journey: Sky River, BestMark, Bookware. Six digits to three."
      - url: sierra-sso.html
        title: "Sierra Staff & Single Sign-On"
        description: "SAML SSO at RIT, MFA, Keycloak, cyber insurance, passwordless"
      - url: sierra-sys-admin-forum.html
        title: Sierra Sys Admin Forum
        description: "Migration debates, bot protection, Cloudflare, paging lists, WCAG"
guides:
  - url: cloudflare-sierra-guide.html
    title: "Cloudflare Protection for Sierra"
    description: "Complete setup guide for protecting Sierra WebPAC with Cloudflare"
  - url: sierra-sso-guide.html
    title: "Sierra SSO Technical Guide"
    description: "SAML SSO implementation reference — IdP setup, Sierra config, Keycloak, SCIM"
  - url: suggest-a-purchase.html
    title: "Suggest-a-Purchase Comparison"
    description: "Jacksonville Auto-Suggest vs. chimpy-me (Datasette) — patron purchase suggestion systems"
  - url: speakers.html
    title: Speaker Cards
    description: "Conference speaker gallery — history, stats, and rarity tiers"
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

Note: `days` list is removed — sessions_by_day subsumes it.

- [ ] **Step 2: Rewrite `templates/index.html` for variant A**

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

{% for day_group in page.sessions_by_day %}
<h2><a href="{{ day_group.day_url }}">{{ day_group.day }}</a></h2>
<div class="section-list">
  {% for session in day_group.sessions %}
  <a class="day-card" href="{{ session.url }}">
    <div class="day-info">
      <h3>{{ session.title }}</h3>
      <p>{{ session.description }}</p>
    </div>
  </a>
  {% endfor %}
</div>
{% endfor %}

{% if page.guides %}
<h2>Guides & References</h2>
<div class="section-list">
  {% for guide in page.guides %}
  <a class="day-card" href="{{ guide.url }}">
    <div class="day-info">
      <h3>{{ guide.title }}</h3>
      <p>{{ guide.description }}</p>
    </div>
  </a>
  {% endfor %}
</div>
{% endif %}

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

- [ ] **Step 3: Build and verify variant A**

Run: `uv run python build.py`

Check `http://<tailscale-ip>:8080/index.html`:
- Sessions grouped by day (Sunday, Monday, Tuesday, Wednesday headings)
- Day headings are links to the day page
- Each session is a card with title + description
- Guides section appears after sessions
- Tracks and attendance at the bottom

- [ ] **Step 4: Commit**

```bash
git add templates/index.html content/index.md
git commit -m "feat: homepage variant A — sessions-first layout with day grouping"
```

---

## Task 3: Homepage Variant B — "Hub"

**Files:**
- Create: `templates/index-b.html`
- Create: `content/index-b.md`

- [ ] **Step 1: Create `content/index-b.md`**

Copy the same frontmatter from `content/index.md` but change template to `index-b` and add back the `days` list (variant B uses day cards):

```yaml
---
title: "IUG 2026 Conference Notes"
template: index-b
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
    sessions:
      - url: "https://github.com/iug-ils-data-preconf/iug2026"
        title: The Great ILS-Data Preconference
  - url: monday.html
    dow: Mon
    num: "13"
    month: Apr
    title: "Day 1 — Opening Session"
    sessions:
      - url: sierra-roadmap.html
        title: Sierra Roadmap
      - url: amazon-business.html
        title: Amazon Business EDI
      - url: hackathon-awards.html
        title: Hackathon Awards
  - url: tuesday.html
    dow: Tue
    num: "14"
    month: Apr
    title: "Day 2 — Breakout Sessions"
    sessions:
      - url: ai-the-right-way.html
        title: "AI The Right Way"
      - url: vega-reports.html
        title: "Vega Reports & Analytics"
      - url: resource-sharing.html
        title: Resource Sharing Update
      - url: sierra-year-in-review.html
        title: Sierra Year in Review
      - url: floating-collections-bof.html
        title: Floating Collections BoF
      - url: meep.html
        title: MEEP
  - url: wednesday.html
    dow: Wed
    num: "15"
    month: Apr
    title: "Day 3 — Final Sessions"
    sessions:
      - url: executive-panel.html
        title: Executive Leadership Panel
      - url: cataloging-without-oclc.html
        title: Cataloging without OCLC
      - url: sierra-sso.html
        title: "Sierra Staff & SSO"
      - url: sierra-sys-admin-forum.html
        title: Sierra Sys Admin Forum
guides:
  - url: cloudflare-sierra-guide.html
    title: "Cloudflare Protection for Sierra"
    description: "Complete setup guide for protecting Sierra WebPAC with Cloudflare"
  - url: sierra-sso-guide.html
    title: "Sierra SSO Technical Guide"
    description: "SAML SSO implementation reference — IdP setup, Sierra config, Keycloak, SCIM"
  - url: suggest-a-purchase.html
    title: "Suggest-a-Purchase Comparison"
    description: "Jacksonville Auto-Suggest vs. chimpy-me (Datasette) — patron purchase suggestion systems"
  - url: speakers.html
    title: Speaker Cards
    description: "Conference speaker gallery — history, stats, and rarity tiers"
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

- [ ] **Step 2: Create `templates/index-b.html`**

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
  <div class="day-card day-card-expanded">
    <a href="{{ day.url }}" class="day-card-header">
      <div class="day-date">
        <div class="dow">{{ day.dow }}</div>
        <div class="num">{{ day.num }}</div>
        <div class="month">{{ day.month }}</div>
      </div>
      <div class="day-info">
        <h3>{{ day.title }}</h3>
      </div>
    </a>
    {% if day.sessions %}
    <div class="day-sessions">
      {% for session in day.sessions %}
      <a href="{{ session.url }}" class="day-session-link">{{ session.title }} &rarr;</a>
      {% endfor %}
    </div>
    {% endif %}
  </div>
  {% endfor %}
</div>

{% if page.guides %}
<h2>Guides & References</h2>
<div class="section-list">
  {% for guide in page.guides %}
  <a class="day-card" href="{{ guide.url }}">
    <div class="day-info">
      <h3>{{ guide.title }}</h3>
      <p>{{ guide.description }}</p>
    </div>
  </a>
  {% endfor %}
</div>
{% endif %}

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

- [ ] **Step 3: Add variant B CSS to `static/style.css`**

Append to `static/style.css`:

```css
/* Variant B: Expanded day cards with session links */
.day-card-expanded {
  background: white;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  overflow: hidden;
  margin-bottom: 1rem;
}
.day-card-expanded .day-card-header {
  display: flex;
  gap: 1.25rem;
  align-items: center;
  padding: 1.25rem;
  text-decoration: none;
  color: inherit;
  transition: background 0.15s;
}
.day-card-expanded .day-card-header:hover {
  background: var(--light);
}
.day-sessions {
  border-top: 1px solid #eee;
  padding: 0.5rem 1.25rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.day-session-link {
  display: block;
  padding: 0.4rem 0.75rem;
  border-radius: 4px;
  font-size: 0.9rem;
  color: var(--teal);
  text-decoration: none;
  transition: background 0.1s;
}
.day-session-link:hover {
  background: var(--light);
  text-decoration: none;
}
```

- [ ] **Step 4: Build and verify variant B**

Run: `uv run python build.py`

Check `http://<tailscale-ip>:8080/index-b.html`:
- Day cards with date badge and title as the visual anchor
- Session links nested below each day card
- Compact session links (title + arrow)
- Guides section same as variant A
- Tracks and attendance at bottom

- [ ] **Step 5: Commit**

```bash
git add templates/index-b.html content/index-b.md static/style.css
git commit -m "feat: homepage variant B — hub layout with expanded day cards"
```

---

## Task 4: Agent Navigation — llms.txt

**Files:**
- Modify: `build.py` — add `generate_llms_txt()` function
- Modify: `templates/base.html` — add link tag

- [ ] **Step 1: Write test for `generate_llms_txt`**

Add to `tests/test_build.py`:

```python
def test_generate_llms_txt(tmp_path):
    """generate_llms_txt creates llms.txt from page metadata."""
    site = {"title": "Test Site", "url": "https://example.com"}
    pages = [
        {"title": "Home", "url": "index.html", "template": "index", "description": "Home page"},
        {"title": "Session A", "url": "session-a.html", "template": "session", "description": "A session", "day": "monday"},
    ]
    output_dir = tmp_path / "docs"
    output_dir.mkdir()

    from build import generate_llms_txt
    generate_llms_txt(site, pages, output_dir)

    llms = (output_dir / "llms.txt").read_text()
    assert "Test Site" in llms
    assert "session-a.html" in llms
    assert "Session A" in llms

    llms_full = (output_dir / "llms-full.txt").read_text()
    assert "Test Site" in llms_full
    assert "session-a.html" in llms_full
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_build.py::test_generate_llms_txt -v`
Expected: FAIL — `generate_llms_txt` not found

- [ ] **Step 3: Implement `generate_llms_txt` in `build.py`**

Add after the `get_sessions_for_day` function:

```python
def generate_llms_txt(site, pages, output_dir=None):
    """Generate llms.txt and llms-full.txt for AI agent navigation."""
    output_dir = output_dir or OUTPUT_DIR

    # Categorize pages
    sessions = [p for p in pages if p.get("template") == "session"]
    day_pages = [p for p in pages if p.get("template") == "day"]
    guides = [p for p in pages if p.get("template") == "page"]
    special = [p for p in pages if p.get("template") in ("index", "speakers", "index-b")]

    lines = []
    lines.append(f"# {site['title']}")
    lines.append(f"> {site.get('url', '')}")
    lines.append("")
    lines.append("Conference knowledge base with session notes, technical guides, and speaker data.")
    lines.append("")

    if special:
        lines.append("## Pages")
        for p in special:
            lines.append(f"- [{p['title']}]({p['url']}): {p.get('description', '')}")
        lines.append("")

    if day_pages:
        lines.append("## Day Overviews")
        for p in sorted(day_pages, key=lambda p: p.get("date", "")):
            lines.append(f"- [{p['title']}]({p['url']}): {p.get('description', '')}")
        lines.append("")

    if sessions:
        lines.append("## Sessions")
        for p in sorted(sessions, key=lambda p: (p.get("day", ""), p.get("title", ""))):
            day = p.get("day", "")
            lines.append(f"- [{p['title']}]({p['url']}): {p.get('description', '')} [{day}]")
        lines.append("")

    if guides:
        lines.append("## Guides")
        for p in guides:
            lines.append(f"- [{p['title']}]({p['url']}): {p.get('description', '')}")
        lines.append("")

    lines.append("## Structured Data")
    lines.append("- [speakers.json](speakers-data.json): Full speaker database with session history")
    lines.append("")

    (output_dir / "llms.txt").write_text("\n".join(lines))

    # llms-full.txt: include rendered content
    full_lines = list(lines)
    full_lines.append("---")
    full_lines.append("")
    for p in pages:
        full_lines.append(f"# {p['title']}")
        full_lines.append(f"URL: {p['url']}")
        if p.get("description"):
            full_lines.append(f"Description: {p['description']}")
        full_lines.append("")
        body = p.get("_body", "")
        if body.strip():
            full_lines.append(body.strip())
        else:
            full_lines.append("(Template-driven page — see structured data)")
        full_lines.append("")
        full_lines.append("---")
        full_lines.append("")

    (output_dir / "llms-full.txt").write_text("\n".join(full_lines))
    print("  Generated llms.txt and llms-full.txt")
```

- [ ] **Step 4: Call `generate_llms_txt` from `build_site()`**

In the `build_site()` function, add after the page rendering loop and before static copy:

```python
    # Generate agent navigation files
    generate_llms_txt(site, pages)
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/test_build.py -v`
Expected: all 5 tests PASS

- [ ] **Step 6: Add link tag to `templates/base.html`**

After the `<link rel="stylesheet" href="style.css">` line, add:

```html
  <link rel="help" href="llms.txt" title="LLM site navigation">
```

- [ ] **Step 7: Build and verify**

Run: `uv run python build.py`

Check:
- `docs/llms.txt` exists, lists all pages by category
- `docs/llms-full.txt` exists, includes page content
- `<link rel="help" href="llms.txt">` appears in every generated HTML page

- [ ] **Step 8: Commit**

```bash
git add build.py tests/test_build.py templates/base.html
git commit -m "feat: add llms.txt and llms-full.txt agent navigation"
```
