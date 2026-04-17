# Handoff: IUG 2026 Site — UX/Usability Deep Pass

## What This Project Is

Conference knowledge base for IUG 2026 (Innovative Users Group, library technology conference). Public site deployed via GitHub Pages from `docs/`. The repo is at `/home/ray/notes/iug2026-shared/` on branch `feature/site-refactor`.

## What Was Just Completed

A full site refactor separating content from presentation:

- **22 markdown+frontmatter content files** in `content/` — single source of truth
- **6 Jinja2 templates** in `templates/` — base, page, session, day, index, speakers
- **`build.py`** (~250 lines) — Python build script with dev server (`uv run python build.py --dev`)
- **`data/site.yaml`** + **`data/speakers.json`** — site config and speaker data
- **`static/style.css`** — consolidated stylesheet
- **`llms.txt`** and **`llms-full.txt`** — auto-generated agent navigation

A navigation redesign was started but needs a deeper pass:
- CSS link affordance fixes were applied (underlines, nav contrast, card hovers)
- Two homepage variants were built for A/B comparison
- The user **prefers variant B** ("Hub" — expanded day cards with nested session links)
- Variant A is still present and should be cleaned up

## What Needs To Be Done

### 1. Homepage Finalization
- **Keep variant B** (`templates/index-b.html` + `content/index-b.md`)
- Remove variant A's layout from `templates/index.html` and make B the default
- Clean up: remove `content/index-b.md`, rename template, update `content/index.md` frontmatter to use the B layout

### 2. Deep UX/Usability Pass for Links
The user's feedback: *"it still seems ambiguous what are and are not links"* — the CSS fixes from the first pass weren't sufficient. This needs:

- **Audit every page type** (index, day, session, speakers, guides) for link clarity
- **Identify specific problem areas** — which elements look like links but aren't? Which are links but don't look like it?
- **Fix the CSS** to make interactive elements unmistakable
- **Test on the live dev server** — the user is on a remote Tailscale connection viewing at `http://100.79.155.74:8080`

Key problem areas flagged:
- Card elements that are links vs cards that aren't (some `.card` divs are clickable, others aren't)
- Text links within content that blend with surrounding text
- Navigation items not reading as obviously interactive
- Overall: "we picked looks nice but sacrificed usability"

### 3. Visual QA Across All Pages
- Verify all 22 pages render correctly (the hackathon-awards page had HTML escaping issues that were fixed)
- Check the duplicate subtitle on hackathon-awards.html (`speakers_display` repeats the date — line 51 of output)
- Verify the speakers gallery renders with all 150 cards
- Check the cloudflare guide's vibedAF badge
- Verify inter-page links, speaker links, and breadcrumbs all work

## Key Files

```
iug2026-shared/
  build.py              # Build script — `uv run python build.py --dev` for dev server
  pyproject.toml        # uv project (jinja2, mistune, python-frontmatter, pyyaml, watchdog)
  content/*.md          # 22 content files (+ index-b.md temporary)
  templates/            # base.html, page.html, session.html, day.html, index.html, index-b.html, speakers.html
  static/style.css      # All CSS (main + speaker cards + vibedAF + variant B styles)
  data/site.yaml        # Site config (nav, tracks, footer, conference info)
  data/speakers.json    # Speaker data (150 speakers)
  specs/                # Design specs
  plans/                # Implementation plans
  docs/                 # BUILD OUTPUT — GitHub Pages serves this
```

## How To Work

```bash
cd /home/ray/notes/iug2026-shared
git checkout feature/site-refactor
uv run python build.py --dev --port 8080   # Dev server at 0.0.0.0:8080
```

Edit content in `content/`, templates in `templates/`, styles in `static/style.css`. The dev server auto-rebuilds on file changes.

## Design Constraints

- Keep the existing color palette and conference branding (navy, teal, green, gold, sky)
- Keep the card-based visual style
- Keep the banner/footer
- Don't change the build system architecture
- Prioritize usability over aesthetics where they conflict
