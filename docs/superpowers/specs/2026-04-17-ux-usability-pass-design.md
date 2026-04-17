# UX/Usability Pass — IUG 2026 Conference Site

**Date:** 2026-04-17
**Status:** Approved
**Branch:** feature/site-refactor

## Problem

The site's link affordance is inconsistent across page types. Interactive and non-interactive elements share the same visual treatment (white cards with shadows), making it unclear what is and isn't clickable. Additionally, the hackathon awards page has rendering bugs, and no test suite exists to catch regressions.

## Approach: Two-Language Affordance System

Establish two distinct interactive vocabularies applied rigorously across the entire site:

1. **Text links** — teal color with a subtle underline signal
2. **Card/block links** — hover elevation, left-border accent, directional arrow

Non-interactive elements are stripped of any hover effects that mimic interactivity.

## Section 1: Text Link Treatment

All inline text links use teal color with a faint underline at rest (low-opacity `text-decoration-color`) that becomes full-opacity on hover.

- **Resting state:** teal text + faint underline (~30% opacity teal)
- **Hover state:** darker teal + solid underline

Applies to:
- Body text links in session content
- Source/reference links
- Footer links (already fine — no changes)
- Breadcrumb links (add faint underline at rest to distinguish from plain-text current-page segment)
- Speaker name links in session pages
- Links inside update feed cards (e.g., "Full writeup ->")

Replaces the current approach of `text-decoration: underline` on `.container a` with carved-out exceptions. The new rule: faint underline at rest, solid on hover, fewer exceptions.

## Section 2: Card Affordance System

### Interactive Cards (navigate somewhere)

These elements are links and must signal it:
- Day cards on homepage (-> day pages)
- Session list cards on day pages and homepage (-> session pages)
- Guide cards on homepage (-> guide pages)
- Day session links in expanded day cards (-> sessions)

**Treatment:**
- Hover: shadow lift + left-border accent (teal)
- Add a `->` arrow to card text/title via CSS `::after` pseudo-element (keeps content/templates clean)
- Explicit `cursor: pointer`

### Non-Interactive Cards (display info only)

These elements are NOT links and must stop looking like they could be:
- Track cards (Gatherings, General, Sierra, Polaris, Vega)
- Stat boxes (412 Attendees, 130+ First-timers, etc.)
- Speaker info card on session pages
- Info bar (the bar itself — individual values inside may contain links)
- Update feed cards on day pages (card isn't a link; may contain links inside)

**Treatment:**
- Remove hover shadow transitions — stays flat
- Explicit `cursor: default`
- Keep colored top-border on track cards (informational, not an affordance cue)

## Section 3: Navigation & Breadcrumbs

**Nav bar:** No changes needed. The navy bar with pill-shaped hover backgrounds and gold active underline reads correctly as navigation.

**Breadcrumbs:** Add faint underline at rest (matching Section 1 text link treatment) so breadcrumb links are distinguishable from the plain-text current-page segment.

**Footer:** No changes needed. Gray text with underline already reads as links.

## Section 4: Site-Wide Rendering & Content Integrity

### 4a: Subtitle Duplication Audit

The `session.html` template renders `{{ speakers_display }} · {{ day }}, {{ date }}`. Any page where `speakers_display` already contains the date will duplicate it.

- Audit all session pages' `speakers_display` frontmatter
- Fix offending frontmatter rather than complicating template logic
- Known issue: `hackathon-awards.md` has `speakers_display: "Monday, April 13 · 4:00-5:00 PM"`

### 4b: HTML Escaping Audit

Mistune wraps deeply nested HTML blocks in `<pre><code>` and escapes them. The `render_markdown()` preprocessor strips leading whitespace but doesn't fully prevent this.

- Scan all built pages for `<pre><code>&lt;` (the fingerprint of escaped HTML)
- Fix affected content files
- Harden `render_markdown()` if a general-purpose fix exists

### 4c: Build Test Suite

Add `test_build.py` with assertions:
- All pages build without error
- No page contains escaped HTML artifacts (`<pre><code>&lt;div`, `&lt;p&gt;`)
- No page has duplicate adjacent text in the subtitle area
- All inter-page links resolve to files that exist in `docs/`
- Speaker links (`speakers.html#id`) reference IDs present in `speakers.json`

## Section 5: Homepage Finalization

- Make variant B's layout the default `index.html` template
- Merge `content/index-b.md` frontmatter into `content/index.md`
- Delete `content/index-b.md` and `templates/index-b.html`
- Update `content/index.md` to use `template: index`

## Design Constraints

- Keep existing color palette (navy, teal, green, gold, sky)
- Keep card-based visual style
- Keep banner/footer
- Don't change build system architecture
- Prioritize usability over aesthetics where they conflict

## Files Affected

- `static/style.css` — primary changes (link treatment, card affordance, hover rules)
- `templates/session.html` — no template changes (fix frontmatter instead)
- `templates/index.html` — replace with variant B layout
- `templates/index-b.html` — delete after merge
- `templates/day.html` — add arrow to session card links
- `content/index.md` — merge variant B frontmatter
- `content/index-b.md` — delete after merge
- `content/hackathon-awards.md` — fix speakers_display, fix HTML nesting
- `content/*.md` — audit all for subtitle duplication and HTML escaping
- `build.py` — potentially harden `render_markdown()`
- `test_build.py` — new file, build test suite
