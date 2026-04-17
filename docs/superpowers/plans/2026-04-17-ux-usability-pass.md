# UX/Usability Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix site-wide link ambiguity with a two-language affordance system, fix hackathon rendering bugs, add build tests, and finalize the homepage.

**Architecture:** CSS-only affordance changes (no template restructuring). Text links get faint-underline-at-rest treatment. Interactive cards get hover lift + directional arrow via `::after`. Non-interactive cards lose hover effects. Build tests verify content integrity. Homepage variant B becomes the default.

**Tech Stack:** Python (mistune, jinja2, pytest), CSS, HTML

---

## File Structure

**Create:**
- `test_build.py` — build test suite (content integrity assertions)

**Modify:**
- `build.py` — harden `render_markdown()` with HTML depth tracking
- `static/style.css` — text link treatment, card affordance, breadcrumb refinement
- `content/hackathon-awards.md` — fix `speakers_display` frontmatter
- `content/executive-panel.md` — fix `speakers_display` frontmatter
- `content/index.md` — merge variant B frontmatter (days structure)
- `templates/index.html` — replace with variant B layout

**Delete:**
- `content/index-b.md` — variant A/B split no longer needed
- `templates/index-b.html` — variant B becomes the default index

---

### Task 1: Build Test Infrastructure

**Files:**
- Create: `test_build.py`

- [ ] **Step 1: Create test file with build fixture and first test**

```python
"""Tests for the IUG 2026 conference site build."""

import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).parent
OUTPUT_DIR = ROOT / "docs"


@pytest.fixture(scope="session", autouse=True)
def build_site():
    """Run the build once before all tests."""
    result = subprocess.run(
        ["uv", "run", "python", "build.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Build failed:\n{result.stderr}"


def get_html_files():
    """Return all built HTML files."""
    return sorted(OUTPUT_DIR.glob("*.html"))


class TestBuildCompleteness:
    def test_expected_pages_built(self):
        """All expected pages should be present in docs/."""
        html_files = {f.name for f in get_html_files()}
        expected = {
            "index.html",
            "sunday.html", "monday.html", "tuesday.html", "wednesday.html",
            "speakers.html",
            "sierra-roadmap.html", "hackathon-awards.html", "amazon-business.html",
            "ai-the-right-way.html", "vega-reports.html", "resource-sharing.html",
            "sierra-year-in-review.html", "floating-collections-bof.html", "meep.html",
            "executive-panel.html", "cataloging-without-oclc.html",
            "sierra-sso.html", "sierra-sys-admin-forum.html",
            "cloudflare-sierra-guide.html", "sierra-sso-guide.html",
            "suggest-a-purchase.html",
        }
        missing = expected - html_files
        assert not missing, f"Missing pages: {missing}"
```

- [ ] **Step 2: Run test to verify it passes**

Run: `cd /home/ray/notes/iug2026-shared && uv run pytest test_build.py::TestBuildCompleteness -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add test_build.py
git commit -m "test: add build completeness test"
```

---

### Task 2: Test + Fix HTML Escaping

**Files:**
- Modify: `test_build.py` (add test)
- Modify: `build.py:53-68` (fix `render_markdown`)

- [ ] **Step 1: Add escaped HTML test**

Add to `test_build.py`:

```python
class TestContentIntegrity:
    def test_no_escaped_html_in_output(self):
        """No page should contain HTML that mistune escaped into code blocks."""
        failures = []
        for html_file in get_html_files():
            content = html_file.read_text()
            if "<pre><code>&lt;div" in content or "<pre><code>&lt;p" in content:
                failures.append(html_file.name)
        assert not failures, f"Pages with escaped HTML: {failures}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /home/ray/notes/iug2026-shared && uv run pytest test_build.py::TestContentIntegrity::test_no_escaped_html_in_output -v`
Expected: FAIL — `hackathon-awards.html` contains escaped HTML

- [ ] **Step 3: Fix render_markdown() in build.py**

Replace the `render_markdown` function in `build.py` (lines 53-68) and add `import re` to the top-level imports:

Add `import re` after `import json` (line 6):

```python
import re
```

Replace the entire `render_markdown` function:

```python
def render_markdown(text):
    """Convert markdown text to HTML.

    Preprocesses to:
    1. Strip leading whitespace from HTML lines (prevents code block treatment)
    2. Bridge blank lines inside nested HTML (prevents block splitting)
    """
    BLOCK_TAGS = (
        r"(?:div|ul|ol|table|section|article|nav|aside|header|footer"
        r"|main|details|figure|blockquote|form|fieldset|dl|pre)"
    )

    lines = text.split("\n")
    processed = []
    depth = 0

    for line in lines:
        stripped = line.lstrip()

        # Strip indentation from HTML lines
        if stripped.startswith("<") or stripped.startswith("</"):
            line = stripped

        # Track block-level HTML depth
        opens = len(re.findall(rf"<{BLOCK_TAGS}\b", line, re.I))
        closes = len(re.findall(rf"</{BLOCK_TAGS}\b", line, re.I))
        depth = max(0, depth + opens - closes)

        # Bridge blank lines inside nested HTML blocks to prevent
        # mistune from ending the HTML block prematurely
        if stripped == "" and depth > 0:
            processed.append("<!-- -->")
        else:
            processed.append(line)

    return mistune.html("\n".join(processed))
```

- [ ] **Step 4: Rebuild and run test to verify it passes**

Run: `cd /home/ray/notes/iug2026-shared && uv run python build.py && uv run pytest test_build.py::TestContentIntegrity::test_no_escaped_html_in_output -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add build.py test_build.py
git commit -m "fix: harden render_markdown to track HTML depth and bridge blank lines

Prevents mistune from splitting nested HTML blocks at blank lines,
which caused project details on hackathon-awards to render as escaped
code blocks."
```

---

### Task 3: Test + Fix Subtitle Duplication

**Files:**
- Modify: `test_build.py` (add test)
- Modify: `content/hackathon-awards.md:9` (fix frontmatter)
- Modify: `content/executive-panel.md:8` (fix frontmatter)

- [ ] **Step 1: Add subtitle duplication test**

Add to the `TestContentIntegrity` class in `test_build.py`:

```python
    def test_no_duplicate_dates_in_subtitles(self):
        """Session subtitles should not repeat the date."""
        failures = []
        for html_file in get_html_files():
            content = html_file.read_text()
            match = re.search(
                r'class="page-subtitle">(.*?)</p>', content, re.DOTALL
            )
            if match:
                subtitle = match.group(1)
                dates = re.findall(r"(?:Monday|Tuesday|Wednesday|Sunday),\s+April\s+\d+", subtitle)
                if len(dates) != len(set(dates)):
                    failures.append(f"{html_file.name}: {subtitle.strip()}")
        assert not failures, f"Duplicate dates in subtitles:\n" + "\n".join(failures)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /home/ray/notes/iug2026-shared && uv run pytest test_build.py::TestContentIntegrity::test_no_duplicate_dates_in_subtitles -v`
Expected: FAIL — hackathon-awards.html and executive-panel.html

- [ ] **Step 3: Fix hackathon-awards.md frontmatter**

In `content/hackathon-awards.md`, change line 9:

Old: `speakers_display: "Monday, April 13 · 4:00–5:00 PM"`
New: `speakers_display: "4:00–5:00 PM"`

- [ ] **Step 4: Fix executive-panel.md frontmatter**

In `content/executive-panel.md`, change line 8:

Old: `speakers_display: "Wednesday, April 15, 9:00–10:00 AM · Chicago Ballroom A · General Track"`
New: `speakers_display: "9:00–10:00 AM · Chicago Ballroom A · General Track"`

- [ ] **Step 5: Rebuild and run test to verify it passes**

Run: `cd /home/ray/notes/iug2026-shared && uv run python build.py && uv run pytest test_build.py::TestContentIntegrity::test_no_duplicate_dates_in_subtitles -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add content/hackathon-awards.md content/executive-panel.md test_build.py
git commit -m "fix: remove duplicate dates from hackathon and executive panel subtitles

speakers_display included the day/date, but the session template already
appends it. Removed the redundant prefix from both pages."
```

---

### Task 4: Test Inter-Page Links and Speaker References

**Files:**
- Modify: `test_build.py` (add tests)

- [ ] **Step 1: Add link resolution tests**

Add to the `TestContentIntegrity` class in `test_build.py`:

```python
    def test_internal_links_resolve(self):
        """All internal .html links should point to files that exist."""
        failures = []
        for html_file in get_html_files():
            content = html_file.read_text()
            for href in re.findall(r'href="([^"#][^"]*?\.html)', content):
                if href.startswith("http"):
                    continue
                target = OUTPUT_DIR / href
                if not target.exists():
                    failures.append(f"{html_file.name} -> {href}")
        assert not failures, f"Broken internal links:\n" + "\n".join(failures)

    def test_speaker_anchor_links_resolve(self):
        """Speaker anchor links should reference IDs in speakers.html."""
        speakers_html = (OUTPUT_DIR / "speakers.html").read_text()
        speaker_ids = set(re.findall(r'id="([^"]+)"', speakers_html))
        failures = []
        for html_file in get_html_files():
            if html_file.name == "speakers.html":
                continue
            content = html_file.read_text()
            for anchor in re.findall(r'href="speakers\.html#([^"]+)"', content):
                if anchor not in speaker_ids:
                    failures.append(f"{html_file.name} -> speakers.html#{anchor}")
        assert not failures, f"Broken speaker links:\n" + "\n".join(failures)
```

- [ ] **Step 2: Run tests**

Run: `cd /home/ray/notes/iug2026-shared && uv run pytest test_build.py::TestContentIntegrity::test_internal_links_resolve test_build.py::TestContentIntegrity::test_speaker_anchor_links_resolve -v`
Expected: PASS (fix any failures found)

- [ ] **Step 3: Commit**

```bash
git add test_build.py
git commit -m "test: add link resolution and speaker anchor tests"
```

---

### Task 5: CSS — Text Link Treatment

**Files:**
- Modify: `static/style.css:21-76` (link rules)

- [ ] **Step 1: Replace link CSS rules**

In `static/style.css`, replace lines 21-76 (from `a { color:` through the heading hover rules) with:

```css
a { color: var(--teal); text-decoration: none; }
a:hover { color: #004d63; }

/* Text links in content: faint underline at rest, solid on hover */
.container a {
  text-decoration: underline;
  text-decoration-color: rgba(0, 100, 130, 0.3);
  text-underline-offset: 2px;
  transition: text-decoration-color 0.15s;
}
.container a:hover {
  text-decoration-color: var(--teal);
  color: #004d63;
}

/* Card links use card-level affordance, not underlines */
.container a.day-card,
.container a.day-card-header,
.container a.day-session-link {
  text-decoration: none;
}

/* Breadcrumbs: faint underline to distinguish from plain-text segment */
.container .breadcrumb a {
  text-decoration: underline;
  text-decoration-color: rgba(0, 100, 130, 0.3);
  text-underline-offset: 2px;
}
.container .breadcrumb a:hover {
  text-decoration-color: var(--teal);
}

/* Headings with links: no underline at rest, underline on hover */
.container h1 a, .container h2 a, .container h3 a {
  text-decoration: none;
}
.container h1 a:hover, .container h2 a:hover, .container h3 a:hover {
  text-decoration: underline;
  text-decoration-color: var(--teal);
}
```

- [ ] **Step 2: Rebuild and visually verify**

Run: `cd /home/ray/notes/iug2026-shared && uv run python build.py`

Open in browser and check:
- `index-b.html` — inline links in info bar have faint underline
- `monday.html` — links inside update feed cards (e.g., "Full writeup →") have faint underline
- `sierra-roadmap.html` — speaker link has faint underline, breadcrumb links have faint underline
- `cloudflare-sierra-guide.html` — TOC links and body links have faint underline
- `speakers.html` — session history links have faint underline

- [ ] **Step 3: Commit**

```bash
git add static/style.css
git commit -m "style: text link treatment — faint underline at rest, solid on hover

Replaces the old underline-with-exceptions approach. Text links get a
30% opacity teal underline that goes solid on hover. Card links, breadcrumbs,
and headings each have their own consistent treatment."
```

---

### Task 6: CSS — Card Affordance System

**Files:**
- Modify: `static/style.css` (card rules)

- [ ] **Step 1: Add interactive card affordance**

In `static/style.css`, replace the existing `a.day-card` rules (lines ~125-135 after Task 5 changes) with:

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

- [ ] **Step 2: Add directional arrow to interactive cards**

Add after the `a.day-card:hover` rule:

```css
/* Directional arrow on interactive card titles */
a.day-card .day-info h3::after,
.day-card-expanded .day-info h3::after {
  content: " \2192";
  color: var(--teal);
  font-weight: 400;
  opacity: 0.5;
  transition: opacity 0.15s;
}
a.day-card:hover .day-info h3::after,
.day-card-expanded .day-card-header:hover .day-info h3::after {
  opacity: 1;
}
```

- [ ] **Step 3: Remove hover from non-interactive cards**

In `static/style.css`, find and update the `.speaker-card` hover rule. Replace:

```css
.speaker-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
```

With:

```css
/* speaker-card hover removed — card is not a link */
```

Also remove `transition: box-shadow 0.15s;` from the `.speaker-card` base rule.

- [ ] **Step 4: Rebuild and visually verify**

Run: `cd /home/ray/notes/iug2026-shared && uv run python build.py`

Open in browser and check:
- `index-b.html` — day card headers show `→` arrow, guide cards show `→` arrow; hover lifts shadow + shows teal left-border
- `monday.html` — session cards in "Session Notes from This Day" show arrows, hover lifts
- `tuesday.html` — same as monday
- `speakers.html` — speaker cards no longer lift on hover
- Track cards on `index-b.html` — no hover effect (stay flat)
- Stat boxes on `index-b.html` — no hover effect

- [ ] **Step 5: Commit**

```bash
git add static/style.css
git commit -m "style: card affordance system — arrows on interactive cards, no hover on inert cards

Interactive cards (session links, day cards, guides) get a directional
arrow and hover lift. Non-interactive cards (speaker cards, track cards,
stat boxes) lose hover effects so they stop looking clickable."
```

---

### Task 7: Homepage Finalization

**Files:**
- Modify: `templates/index.html` (replace with variant B layout)
- Modify: `content/index.md` (merge variant B frontmatter)
- Delete: `templates/index-b.html`
- Delete: `content/index-b.md`
- Modify: `build.py:109` (remove `index-b` from special pages list)

- [ ] **Step 1: Replace index.html template with variant B**

Copy the full contents of `templates/index-b.html` into `templates/index.html`, replacing everything. The file is already in this plan — it's the template with expanded day cards and nested session links.

- [ ] **Step 2: Merge frontmatter into content/index.md**

Replace `content/index.md` with the contents of `content/index-b.md`, but change the template field:

In the frontmatter, change:
Old: `template: index-b`
New: `template: index`

- [ ] **Step 3: Delete variant A/B split artifacts**

```bash
rm templates/index-b.html content/index-b.md
```

- [ ] **Step 4: Update build.py special pages list**

In `build.py`, line 109, change:

Old: `special = [p for p in pages if p.get("template") in ("index", "speakers", "index-b")]`
New: `special = [p for p in pages if p.get("template") in ("index", "speakers")]`

- [ ] **Step 5: Rebuild and run all tests**

Run: `cd /home/ray/notes/iug2026-shared && uv run python build.py && uv run pytest test_build.py -v`
Expected: All tests pass. `docs/index.html` uses the expanded day card layout. `docs/index-b.html` no longer exists.

- [ ] **Step 6: Visually verify homepage**

Open `index.html` in browser. Verify:
- Expanded day cards with nested session links
- Guide cards with arrows
- Track cards without hover
- Stat boxes without hover
- No `index-b.html` page in the nav or build output

- [ ] **Step 7: Commit**

```bash
git add templates/index.html content/index.md build.py
git rm templates/index-b.html content/index-b.md
git commit -m "feat: finalize homepage — variant B becomes the default

Expanded day cards with nested session links are now the standard
index layout. Removed variant A/B split artifacts."
```

---

### Task 8: Final Verification

**Files:** None (verification only)

- [ ] **Step 1: Run full test suite**

Run: `cd /home/ray/notes/iug2026-shared && uv run pytest test_build.py -v`
Expected: All tests pass.

- [ ] **Step 2: Visual spot-check all page types**

Open each page type in browser and verify the affordance system is consistent:

| Page | Check |
|------|-------|
| `index.html` | Day cards have arrows + hover. Guides have arrows + hover. Tracks flat. Stats flat. Info bar links have faint underline. |
| `monday.html` | Session cards have arrows + hover. Update feed cards flat (internal links have faint underline). Source links have faint underline. |
| `sierra-roadmap.html` | Breadcrumb links have faint underline. Speaker link has faint underline. Body links have faint underline. Speaker card in info box is flat. |
| `hackathon-awards.html` | No escaped HTML. No duplicate date. TOC links have faint underline. Winner card flat. |
| `speakers.html` | Speaker cards flat (no hover lift). Toggle button still works. Session links inside cards have faint underline. |
| `cloudflare-sierra-guide.html` | TOC links, body links all have faint underline. vibedAF badge unaffected. |

- [ ] **Step 3: Commit any final adjustments**

If any visual issues found, fix and commit with a descriptive message.
