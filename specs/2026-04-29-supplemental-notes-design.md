# Supplemental Notes — Design Spec

## Overview

Split conference session notes into two clearly-separated files: a **primary** page containing only what the speaker(s) directly presented, and an optional **supplemental** page (`<session>-ray-notes.html`) containing Ray's research, citations, commentary, and curiosities gathered during the session with Claude's help. Primary and supplemental are linked via a header banner and inline pinpoint markers.

The pattern responds to direct vendor feedback (Ashley Barey, Clarivate, 2026-04-29; Mike Dicus, Clarivate, same period) that vendor-presented sessions should not contain content the speakers did not actually say. The supplemental file preserves the research value to the community while making attribution unambiguous.

## Goals

- Give every iii/Clarivate-presented session a primary page that contains **only** content the speakers directly presented
- Preserve Ray's research, citations, and commentary as a clearly-labeled, first-person sidecar file
- Make attribution unambiguous to a vendor reading their own session page: nothing on it can plausibly be attributed to them that they didn't say
- Keep the existing build pipeline and templates — no new infrastructure if avoidable

## Non-Goals

- Retroactive vendor approval workflow (separate runbook for IUG 2027 — not in scope)
- Inline collapsible/expandable supplemental content within the primary page
- Surfacing supplemental files in day pages, speaker pages, or top-level nav
- Footnote-style numbered citations
- Different visual treatment per content type within the supplemental (research vs. commentary vs. cross-refs all live together)

---

## Editorial Rules

### Tight rule (mandatory) — applies to all iii/Clarivate-presented sessions

Primary page contains **only**:

1. Verbatim quotes the speaker(s) said
2. Paraphrased claims the speaker(s) directly made (their slides, their argument, their data)

Everything else moves to the supplemental file:

3. Background context Claude pulled in (e.g., specific framework breakdowns, paper authors/years)
4. External links/articles Claude added (e.g., Library Spy, Brookings, Wikipedia)
5. Editorial framing ("still cited in AI ethics papers today", "this expanded on...")
6. Cross-references between sessions the speaker did not explicitly draw
7. Ray's own observations, opinions, or curiosities

### Discretion rule — applies to non-vendor sessions (community talks, librarian-led panels, BoFs)

The supplemental file is available but not required. Use it when there is research/commentary worth preserving but the author wants clean attribution. Skip it when everything in the notes was actually said.

### Cross-pollination case

When content on session A's page was actually said in session B (different speaker or different time slot — Mike Dicus's keycloak example):

- **Default:** Move the content to session B's primary page. No asterisk, no "see also" pointer on A. The content was said; it just landed on the wrong page.
- **Fallback:** When the originating session genuinely cannot be traced, park the content in the originating-session-best-guess supplemental with a note: "I think this came up in another session — flagging here for now."

---

## Architecture

### File layout

| File | Purpose |
|---|---|
| `content/<session>.md` | Primary page. Frontmatter: `template: session`, `supplemental: <session>-ray-notes.html` (optional, presence triggers the header banner). |
| `content/<session>-ray-notes.md` | Supplemental page. Frontmatter: `template: supplemental`, `primary: <session>.html`, `title`, `day`, `date`. |

URLs stay parallel: `ai-the-right-way.html` ↔ `ai-the-right-way-ray-notes.html`.

### Discoverability

Supplemental pages are **only** reachable via the primary page (header banner + inline markers). They do **not** appear in:

- Day index pages
- Speakers page
- Top-level site nav
- Site index

This guarantees that any reader landing on a supplemental file came through the primary page first and has seen the attribution banner.

### Templates

Two changes to `iug2026-shared/templates/`:

1. **`session.html` (existing)** — Add a conditional banner card just under the speaker subtitle, rendered when `page.supplemental` is set in frontmatter:

   ```jinja
   {% if page.supplemental %}
   <div class="card supplemental-banner">
     <p>📎 <strong>These notes contain only what was directly presented.</strong>
     For background research, references, and Ray's commentary that came up while taking these notes, see
     <a href="{{ page.supplemental }}">Ray's research notes ↗</a>.</p>
   </div>
   {% endif %}
   ```

2. **`supplemental.html` (new)** — Extends `base.html`. Renders an unmistakable first-person attribution banner at the top:

   ```jinja
   <div class="card supplemental-header">
     <p>📝 <strong>Ray's research notes for "{{ page.session_title }}"</strong></p>
     <p><em>These are personal research notes I (Ray) gathered with Claude's help while attending the session — background context, citations I looked up, related links, and my own commentary. <strong>They are not part of what the speaker presented.</strong> For the actual session content, see <a href="{{ page.primary }}">the session page ↗</a>.</em></p>
   </div>
   ```

   Followed by `{{ content }}`.

### Inline pinpoint markers

In primary page markdown, use a paperclip-only link to deep-link into the supplemental:

```markdown
Clarivate referenced the NIST AI Risk Management Framework. [📎](ai-the-right-way-ray-notes.html#nist-framework)
```

Anchors inside the supplemental are standard markdown heading IDs (auto-generated by the renderer). Authors are responsible for ensuring inline-marker URLs resolve to a real anchor in the supplemental file.

### Static styles

Add to `iug2026-shared/static/style.css` (or wherever site styles live):

- `.supplemental-banner` — light accent background distinguishing it from regular cards (e.g., subtle paperclip icon, slight tint)
- `.supplemental-header` — stronger visual weight on the supplemental page itself, signaling "this is annotation, not session content"

Visual specifics deferred to implementation; they should be subtle but unmistakable, and consistent with the existing site palette.

### Build changes

Minimal. The build script (`build.py`) already discovers all `.md` files in `content/`. The supplemental files build automatically. Two small additions:

1. Recognize `template: supplemental` and route to the new template.
2. (Optional, nice-to-have) During build, validate that every `<session>.md` with a `supplemental:` frontmatter key has a corresponding `<session>-ray-notes.md` file, and warn if not.

---

## Author workflow

When taking session notes for a vendor session:

1. Capture everything in a working file as before.
2. Before publishing, split:
   - Primary file (`<session>.md`): only verbatim/paraphrased speaker content.
   - Supplemental file (`<session>-ray-notes.md`): everything else — research, citations, commentary, cross-refs.
3. In the primary, add `supplemental: <session>-ray-notes.html` to frontmatter.
4. In the supplemental, add `primary: <session>.html` and `session_title: "..."` to frontmatter.
5. Add inline `[📎](...)` markers in the primary at any spot where the supplemental adds relevant context.

For non-vendor sessions, skip steps 2–5 unless there's research worth pulling out.

---

## Migration

Apply the pattern retroactively to existing files containing iii-presented content:

1. `ai-the-right-way.md` (Ashley Barey) — primary already drafted; needs split.
2. `vega-reports.md` (Jovana Raskovic) — has transcript, audit + split.
3. `sierra-year-in-review.md` (Mike Dicus) — no transcript, conservative split.
4. `sierra-roadmap.md` (Mike Dicus) — no transcript, conservative split.
5. `meep.md` — verify presenters' affiliations first; may or may not need split.
6. `monday.md` and `amazon-business.md` — only minor Clarivate refs; review for inferred content but unlikely to need a split.

Migration is the subject of a separate implementation plan.

---

## Open Items

- Visual design of the two banner classes (`.supplemental-banner`, `.supplemental-header`) — color, iconography, exact spacing. Defer to implementation.
- Whether to add a "Last updated" / "Source: my session notes + Claude research" footer to supplemental pages. Recommend yes; defer wording.
- Runbook for IUG 2027 (vendor pre-publication review) — out of scope for this spec, separate document.
