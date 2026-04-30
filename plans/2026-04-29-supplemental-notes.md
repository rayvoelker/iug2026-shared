# Supplemental Notes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the supplemental-notes infrastructure (Jinja template, conditional banner, CSS) and apply it as the first concrete migration to `ai-the-right-way.md` (Ashley Barey, Clarivate). After this plan, the same migration pattern applies to the remaining vendor-session files (vega-reports, sierra-year-in-review, sierra-roadmap, meep) as separate follow-up work.

**Architecture:** The build pipeline (`build.py`) discovers every `.md` in `content/`, reads frontmatter, and selects a Jinja template by `template:` field. We add (1) a new `supplemental.html` template, (2) a conditional banner block in the existing `session.html` that renders when `page.supplemental` is set in frontmatter, (3) two new CSS classes, and (4) a content split for `ai-the-right-way.md` per the editorial rules in `specs/2026-04-29-supplemental-notes-design.md`.

**Tech Stack:** Python 3 (`uv run` for execution), Jinja2 templates, `python-frontmatter`, `mistune` (markdown), `pytest`, vanilla CSS.

**Reference spec:** `iug2026-shared/specs/2026-04-29-supplemental-notes-design.md`

---

## File Structure

| File | Status | Purpose |
|---|---|---|
| `templates/supplemental.html` | Create | New Jinja template for supplemental pages — first-person attribution banner + content |
| `templates/session.html` | Modify | Add conditional banner block (renders when `page.supplemental` is set) |
| `static/style.css` | Modify | Add `.supplemental-banner` and `.supplemental-header` classes |
| `content/ai-the-right-way.md` | Modify | Cleaned primary — only verbatim/paraphrased speaker content, plus `supplemental:` frontmatter and inline `[📎](...)` markers |
| `content/ai-the-right-way-ray-notes.md` | Create | New supplemental file with research/citations/commentary extracted from the original |
| `test_build.py` | Modify | Expect the new supplemental HTML file in the built output |

---

### Task 1: Create the supplemental template

**Files:**
- Create: `iug2026-shared/templates/supplemental.html`

- [ ] **Step 1: Create the template file**

Write this exact content to `iug2026-shared/templates/supplemental.html`:

```jinja
{% extends "base.html" %}

{% block breadcrumbs %}
<div class="breadcrumb"><a href="index.html">Home</a> / <a href="{{ page.day }}.html">{{ page.day | title }}, {{ page.date }}</a> / <a href="{{ page.primary }}">{{ page.session_title }}</a> / Ray's Notes</div>
{% endblock %}

{% block content %}
<h1>Ray's Research Notes</h1>
<p class="page-subtitle">For &ldquo;<a href="{{ page.primary }}">{{ page.session_title }}</a>&rdquo; &middot; {{ page.day | title }}, {{ page.date }}</p>

<div class="card supplemental-header">
  <p>&#128221; <strong>Ray&rsquo;s research notes for &ldquo;{{ page.session_title }}&rdquo;</strong></p>
  <p><em>These are personal research notes I (Ray) gathered with Claude&rsquo;s help while attending the session &mdash; background context, citations I looked up, related links, and my own commentary. <strong>They are not part of what the speaker presented.</strong> For the actual session content, see <a href="{{ page.primary }}">the session page &#8599;</a>.</em></p>
</div>

{{ content }}
{% endblock %}
```

- [ ] **Step 2: Verify build does not crash**

Run: `cd iug2026-shared && uv run python build.py`
Expected: Build completes successfully (no supplemental pages exist yet, so the new template is unused but must parse).

- [ ] **Step 3: Commit**

```bash
cd iug2026-shared
git add templates/supplemental.html
git commit -m "feat: add supplemental.html template for Ray's research notes"
```

---

### Task 2: Add conditional supplemental banner to session.html

**Files:**
- Modify: `iug2026-shared/templates/session.html`

- [ ] **Step 1: Insert the conditional banner block**

Edit `iug2026-shared/templates/session.html`. After the existing speakers card (the `{% if page.speakers %}` block ending at line ~22), insert this block before `{{ content }}`:

```jinja
{% if page.supplemental %}
<div class="card supplemental-banner">
  <p>&#128206; <strong>These notes contain only what was directly presented.</strong> For background research, references, and Ray&rsquo;s commentary that came up while taking these notes, see <a href="{{ page.supplemental }}">Ray&rsquo;s research notes &#8599;</a>.</p>
</div>
{% endif %}
```

The full updated `session.html` should read (after edit):

```jinja
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

{% if page.supplemental %}
<div class="card supplemental-banner">
  <p>&#128206; <strong>These notes contain only what was directly presented.</strong> For background research, references, and Ray&rsquo;s commentary that came up while taking these notes, see <a href="{{ page.supplemental }}">Ray&rsquo;s research notes &#8599;</a>.</p>
</div>
{% endif %}

{{ content }}
{% endblock %}
```

- [ ] **Step 2: Build to confirm no regression**

Run: `cd iug2026-shared && uv run python build.py`
Expected: All pages build successfully. No page has `supplemental:` frontmatter yet, so the new block is dormant.

- [ ] **Step 3: Spot-check an existing session page**

Open `iug2026-shared/docs/sierra-roadmap.html` and confirm the page renders identically to before (no supplemental banner appears).

- [ ] **Step 4: Commit**

```bash
cd iug2026-shared
git add templates/session.html
git commit -m "feat: conditional supplemental-notes banner in session template"
```

---

### Task 3: Add CSS for the two supplemental banner classes

**Files:**
- Modify: `iug2026-shared/static/style.css` (append to end of file)

- [ ] **Step 1: Append the new classes**

Append this block to the end of `iug2026-shared/static/style.css`:

```css
/* Supplemental notes — vendor session attribution */
.supplemental-banner {
  background: #fff8e7;
  border-left: 3px solid var(--gold);
}
.supplemental-banner p {
  margin: 0;
  font-size: 0.95rem;
}
.supplemental-header {
  background: #f0f4ff;
  border-left: 3px solid var(--teal);
}
.supplemental-header p {
  margin: 0 0 0.5rem 0;
}
.supplemental-header p:last-child {
  margin-bottom: 0;
}
```

- [ ] **Step 2: Rebuild**

Run: `cd iug2026-shared && uv run python build.py`
Expected: Build succeeds; `static/style.css` is copied to `docs/style.css`.

- [ ] **Step 3: Commit**

```bash
cd iug2026-shared
git add static/style.css
git commit -m "feat: add CSS for supplemental-banner and supplemental-header"
```

---

### Task 4: Smoke-test the infrastructure with a temporary stub supplemental

This task verifies the template + banner + CSS render correctly *before* doing the real content migration. We use a throwaway stub.

**Files:**
- Modify (temporary): `iug2026-shared/content/ai-the-right-way.md` (add one frontmatter line)
- Create (temporary): `iug2026-shared/content/ai-the-right-way-ray-notes.md` (stub)

- [ ] **Step 1: Add `supplemental:` frontmatter to ai-the-right-way.md**

In `iug2026-shared/content/ai-the-right-way.md`, add a single line to the existing frontmatter:

```yaml
supplemental: ai-the-right-way-ray-notes.html
```

(Insert after the `description:` line, before the closing `---`.)

- [ ] **Step 2: Create a stub supplemental file**

Write this minimal stub to `iug2026-shared/content/ai-the-right-way-ray-notes.md`:

```markdown
---
title: "Ray's Notes — AI The Right Way"
template: supplemental
day: tuesday
date: "April 14"
session_title: "AI The Right Way: Smarter Tools, Stronger Outcomes"
primary: ai-the-right-way.html
description: "Ray's research notes and commentary for the AI The Right Way session."
---

## Smoke test placeholder

Real content lands in Tasks 5 and 6.
```

- [ ] **Step 3: Build and visually inspect**

Run: `cd iug2026-shared && uv run python build.py --dev --port 8765`
Open in a browser:
- `http://localhost:8765/ai-the-right-way.html` — confirm the supplemental banner appears under the speaker card with the paperclip icon and link
- `http://localhost:8765/ai-the-right-way-ray-notes.html` — confirm the supplemental page renders with the first-person attribution header, breadcrumbs link back to primary, and the page is reachable

Press Ctrl+C to stop the dev server.

- [ ] **Step 4: Confirm supplemental does not appear in day pages**

Open `http://localhost:8765/tuesday.html` and confirm "Ray's Notes — AI The Right Way" does NOT appear in the session list (the day template filters by `template == "session"`, so this should already be true; this step verifies it).

- [ ] **Step 5: Do NOT commit yet**

Leave the changes uncommitted. Tasks 5–7 will replace the stub with real content; we want a single migration commit, not a stub commit.

---

### Task 5: Create the real supplemental file (ai-the-right-way-ray-notes.md)

**Files:**
- Modify: `iug2026-shared/content/ai-the-right-way-ray-notes.md` (replace stub from Task 4)

This file collects all the research/citations/commentary that the original `ai-the-right-way.md` contained but that were not directly presented by Ashley. Per the spec's tight rule, this includes:

- Specific paper citations Ashley did not cite by name (Acemoglu & Restrepo)
- Detailed Wikipedia/Marxists.org/Brookings external links for literary references
- Detailed PDF link for Pulse of the Library (the survey was named, the PDF URL is research)
- Specific Library Spy / Naperville dates, Hacker News links, "works at OpenAI" detail
- The entire "Related: Simon Willison's Principles for Responsible AI" section
- The entire "Sources & Further Reading" section
- "still cited in AI ethics papers today" editorial framing
- The cross-reference to Joel Goldenberg's Monday opening session

Each entry gets an HTML anchor (heading `id`) so the primary page's inline `[📎](...)` markers can deep-link to it.

- [ ] **Step 1: Replace the stub with the real supplemental content**

Write this content to `iug2026-shared/content/ai-the-right-way-ray-notes.md` (replacing the Task 4 stub):

```markdown
---
title: "Ray's Notes — AI The Right Way"
template: supplemental
day: tuesday
date: "April 14"
session_title: "AI The Right Way: Smarter Tools, Stronger Outcomes"
primary: ai-the-right-way.html
description: "Ray's research notes and commentary for the AI The Right Way session — citations, background context, and external links Ray and Claude looked up during the session."
---

<h2 id="monday-cross-ref">Cross-reference: Monday's opening session</h2>

Ashley's three Responsible AI principles (Transparent, Ethical, Safe) were also outlined during [Monday's opening session](monday.html) by Joel Goldenberg. This session expanded on the framework with data, product details, and audience discussion.

<h2 id="wef-jobs-report">WEF Future of Jobs Report 2025</h2>

Ashley referenced jobs and AI displacement. The full report context I pulled up:

- [The Future of Jobs Report 2025](https://www.weforum.org/publications/the-future-of-jobs-report-2025/digest/) — World Economic Forum, January 2025. Net increase of 78M jobs by 2030; AI creates 11M, displaces 9M; 39% of key skills will change by 2030 ([press release](https://www.weforum.org/press/2025/01/future-of-jobs-report-2025-78-million-new-job-opportunities-by-2030-but-urgent-upskilling-needed-to-prepare-workforces/)).
- Background framework I looked up: Acemoglu & Restrepo, ["Automation and New Tasks: How Technology Displaces and Reinstates Labor"](https://www.aeaweb.org/articles?id=10.1257/jep.33.2.3) (*Journal of Economic Perspectives*, Spring 2019; [NBER WP 25684](https://www.nber.org/papers/w25684)) — historically the reinstatement effect (creation of new tasks) has outpaced displacement.

<h2 id="literary-references">Literary references on AI perception</h2>

Ashley showed a slide of book covers (Butler's *Erewhon*, Asimov, Clarke's *2001*, *The Terminator*) without going into specifics. The detail I looked up while she was speaking:

- Asimov, Isaac. "Runaround." *Astounding Science Fiction*, March 1942. First appearance of the [Three Laws of Robotics](https://en.wikipedia.org/wiki/Three_Laws_of_Robotics); collected in *I, Robot* (1950).
- Butler, Samuel. *Erewhon.* 1872. ["The Book of the Machines" (Ch. 23–25)](https://www.marxists.org/reference/archive/butler-samuel/1872/erewhon/ch23.htm) — one of the earliest explorations of machine consciousness; developed from his 1863 article ["Darwin among the Machines."](https://en.wikipedia.org/wiki/Darwin_among_the_Machines)
- Clarke, Arthur C. *2001: A Space Odyssey.* 1968. HAL 9000 — iconic depiction of AI failure. (<https://en.wikipedia.org/wiki/2001:_A_Space_Odyssey_(novel)>)

<h3 id="asimov-three-laws">Asimov's Three Laws (text)</h3>

For reference — Ashley did not read these aloud:

1. A robot may not injure a human being or, through inaction, allow a human being to come to harm.
2. A robot must obey orders given by human beings, except where such orders would conflict with the First Law.
3. A robot must protect its own existence, as long as such protection does not conflict with the First or Second Law.

A useful counterpoint I came across: [Brookings: Isaac Asimov's Laws of Robotics Are Wrong](https://www.brookings.edu/articles/isaac-asimovs-laws-of-robotics-are-wrong/) (July 2016) — why the framework is insufficient for real-world AI governance.

<h2 id="pulse-2025-pdf">Pulse of the Library 2025 — full PDF</h2>

Ashley referenced the Pulse of the Library 2025 survey. The full PDF report I pulled up while she was presenting:

- [Pulse of the Library 2025 — full PDF](https://clarivate.com/wp-content/uploads/dlm_uploads/2025/10/BXD1675689689-Pulse-of-the-Library-2025-v9.0.pdf)
- [Survey landing page](https://clarivate.com/pulse-of-the-library/)

<h2 id="nist-framework">NIST AI Risk Management Framework</h2>

Ashley referenced NIST in the "Safe" section of the Responsible AI framework. Detail I looked up:

- [NIST AI Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10) — January 2023. Four core functions: Govern, Map, Measure, Manage. ([PDF](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf))
- [NIST Generative AI Profile (AI 600-1)](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) — GenAI-specific extension, July 2024 ([PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf))

<h2 id="nexus-details">Nexus product details</h2>

Ashley mentioned Nexus by name. Details I pulled while she was speaking:

- [Clarivate Introduces Nexus](https://clarivate.com/news/clarivate-introduces-nexus-connecting-ai-users-to-trusted-academic-resources/) — January 2026. Browser extension for AI citation verification ([product page](https://clarivate.com/academia-government/nexus-academic-assistant/)).

<h2 id="library-spy">Library Spy / Naperville Library Spy (Q&A discussion)</h2>

The "vibe coding library catalogs" Q&A topic — context I looked up:

- Walz, Riley. [Library Spy](https://walzr.com/library-spy) — real-time visualization of NYPL checkouts via catalog scraping, March 2025 ([Hacker News](https://news.ycombinator.com/item?id=43384453); [X announcement](https://x.com/rtwlz/status/1901717264707330074)). Walz also created Bop Spotter and works at OpenAI.
- Campolargo, Juan David. [Naperville Library Spy](https://www.juandavidcampolargo.com/projects/naperlibspy) — derivative for Naperville PL; archived at request of library director ([Show HN](https://news.ycombinator.com/item?id=47158355)).
- Willison, Simon. ["Vibe Scraping."](https://simonwillison.net/2025/Jul/17/vibe-scraping/) July 2025.

<h2 id="willison-principles">My own commentary: Simon Willison's responsible-AI principles</h2>

This section is *my* commentary, not Ashley's. I think Simon Willison's principles complement Clarivate's framework well, and I'm including them here because they came to mind during the session.

[Simon Willison](https://simonwillison.net) (developer, blogger) has been a prominent voice on practical responsible AI use. His principles:

- **Transparency** — always disclose when AI was used; label AI-assisted work
- **Human accountability** — you remain responsible for AI output; AI is a tool, you are the author
- **Don't trust, verify** — LLMs hallucinate; treat output as a first draft requiring fact-checking
- **Augment, don't replace, judgment** — AI works best for tasks you already understand
- **Attribution & IP** — respect provenance of training data
- **Experimentation over hype** — ground claims in what LLMs actually do

Core theme: **the human stays in the loop and stays accountable.**

<h2 id="further-reading">Further reading I gathered</h2>

These are sources I assembled from the session — Ashley did not cite these specific items.

### AI risk management & governance

- [EU Artificial Intelligence Act](https://artificialintelligenceact.eu/the-act/) — Regulation (EU) 2024/1689, August 2024
- [UNESCO Recommendation on the Ethics of AI](https://www.unesco.org/en/artificial-intelligence/recommendation-ethics) — adopted November 2021 by 194 member states

### Library-specific AI guidance

- [ARL Research Libraries Guiding Principles for AI](https://www.arl.org/resources/research-libraries-guiding-principles-for-artificial-intelligence/) — April 2024
- [ACRL AI Competencies for Academic Library Workers](https://www.ala.org/acrl/standards/ai) — approved October 2025
- [IFLA: Developing a Library Strategic Response to AI](https://www.ifla.org/g/ai/developing-a-library-strategic-response-to-artificial-intelligence/) — 2023/2024

### Library AI policy & experimentation

- Gupta, Varun. ["AI Experimentation Policy for Libraries."](https://www.tandfonline.com/doi/full/10.1080/01616846.2024.2445356) *Public Library Quarterly*, December 2024
- Ali & Richardson. ["AI Literacy Guidelines and Policies for Academic Libraries: A Scoping Review."](https://journals.sagepub.com/doi/10.1177/03400352251321192) *IFLA Journal*, 2025

### AI environmental impact

- [IEA: Energy and AI](https://www.iea.org/reports/energy-and-ai/executive-summary) — projects data centre electricity doubling to 945 TWh by 2030, April 2025
- [MIT: Generative AI's Environmental Impact Explained](https://news.mit.edu/2025/explained-generative-ai-environmental-impact-0117) — January 2025
- [Pew: Energy Use at US Data Centers Amid the AI Boom](https://www.pewresearch.org/short-reads/2025/10/24/what-we-know-about-energy-use-at-us-data-centers-amid-the-ai-boom/) — October 2025

### Responsible AI commentary (Simon Willison)

- Willison, Simon. ["Things We Learned about LLMs in 2024."](https://simonwillison.net/2024/Dec/31/llms-in-2024/) December 2024
- Willison, Simon. ["Prompt Injection Explained."](https://simonwillison.net/2023/May/2/prompt-injection-explained/) May 2023
- [Simon Willison's prompt injection tag archive](https://simonwillison.net/tags/prompt-injection/) — ongoing collection
```

- [ ] **Step 2: Verify the supplemental file builds**

Run: `cd iug2026-shared && uv run python build.py`
Expected: Build succeeds; `docs/ai-the-right-way-ray-notes.html` exists.

---

### Task 6: Rewrite ai-the-right-way.md as the audited primary

**Files:**
- Modify: `iug2026-shared/content/ai-the-right-way.md`

The primary keeps only what Ashley directly presented (verbatim or paraphrased). It adds inline `[📎](...)` markers at spots where the supplemental adds context. Per the spec's tight rule, the following are removed and now live in the supplemental:

- The "Sources & Further Reading" section (entire)
- The "Related: Simon Willison's Principles" section (entire)
- The cross-reference to Monday's opening session ("Clarivate outlined the same three Responsible AI principles during Monday's opening session...")
- Specific paper citations not made by Ashley (WEF report URL detail, Acemoglu & Restrepo, Brookings)
- Specific Wikipedia/Marxists.org/external URLs for literary references
- The "(NIST AI RMF 1.0, Govern/Map/Measure/Manage)" detailed framework breakdown
- The "Pulse of the Library 2025" PDF URL link
- "still cited in AI ethics papers today" editorial framing
- Specific Library Spy / Naperville dates, HN links, "Walz also created Bop Spotter; works at OpenAI"

- [ ] **Step 1: Replace the file with the audited primary**

Write this exact content to `iug2026-shared/content/ai-the-right-way.md` (replaces the file in full):

```markdown
---
title: "AI The Right Way: Smarter Tools, Stronger Outcomes"
template: session
day: tuesday
date: "April 14"
speakers:
  - ashley-barey
speakers_display: "Ashley Barey (VP Product Management, Clarivate) · 4:30–5:30 PM · Denver Room · General Track"
description: "Clarivate's Responsible AI framework (Transparent, Ethical, Safe), product roadmap (Data Explorer, Metadata Assistant, Acquisitions Agent), Pulse of the Library 2025 data, and audience Q&A."
supplemental: ai-the-right-way-ray-notes.html
---

<div class="card">
  <p>Ashley Barey presented Clarivate&rsquo;s approach to AI across the Innovative product suite &mdash; the Responsible AI framework (Transparent, Ethical, Safe), current and upcoming AI capabilities, and data from the 2025 Pulse of the Library survey.</p>
</div>

## AI Is Fundamentally Different from Prior Tech Waves

<div class="card">
  <p>Ashley opened by challenging the common comparison of AI to cloud computing or Google search, arguing that AI is fundamentally different in three ways:</p>
</div>

<div class="section-list">
  <div class="section-item">
    <h3>Different error profile</h3>
    <p>A bad Google search just returns wrong results &mdash; you can tell. A bad AI output can come across as <strong>very convincing and fluent</strong>. Not knowing whether the AI is wrong is the real danger.</p>
  </div>
  <div class="section-item">
    <h3>Agentic by nature</h3>
    <p>AI reasons, makes decisions, and builds on prior context &mdash; it&rsquo;s not just infrastructure and retrieval. Google search doesn&rsquo;t assume anything; AI is asking and answering questions.</p>
  </div>
  <div class="section-item">
    <h3>Different regulatory surface area</h3>
    <p>AI raises all the prior concerns (antitrust, privacy) plus new ones: bias, autonomy, misinformation at scale, and existential risks.</p>
  </div>
</div>

<div class="card">
  <p>Ashley referenced jobs and AI displacement, drawing on the World Economic Forum&rsquo;s Future of Jobs reporting &mdash; reskilling and job transformation, not wholesale replacement. <a href="ai-the-right-way-ray-notes.html#wef-jobs-report">&#128206;</a></p>
</div>

## Literary & Cultural Influences on AI Perception

<div class="card">
  <p>Ashley showed a slide of book covers and made the point that our collective perception of AI is deeply shaped by fiction &mdash; from Samuel Butler&rsquo;s <em>Erewhon</em>, to Asimov&rsquo;s Three Laws of Robotics, to Arthur C. Clarke&rsquo;s HAL 9000, to <em>The Terminator</em>. <a href="ai-the-right-way-ray-notes.html#literary-references">&#128206;</a></p>
  <p style="margin-top: 0.75rem;">&ldquo;Your patrons have been watching all of that too. They don&rsquo;t know how to interpret AI. Libraries are the best civic hub &mdash; the place to go to get good information, to use those trusted advisors for teaching and leadership.&rdquo;</p>
</div>

## 2025 Pulse of the Library

<div class="card">
  <p>Data from the <a href="https://clarivate.com/pulse-of-the-library/">Clarivate Pulse of the Library 2025</a> survey (2,000+ librarians across 109 countries; 400+ public library responses). <a href="ai-the-right-way-ray-notes.html#pulse-2025-pdf">&#128206;</a></p>
</div>

<div class="stats-row">
  <div class="stat">
    <div class="number">67%</div>
    <div class="stat-label">Exploring or implementing AI</div>
  </div>
  <div class="stat">
    <div class="number">56%</div>
    <div class="stat-label">Recognize upskilling needed</div>
  </div>
  <div class="stat">
    <div class="number">49%</div>
    <div class="stat-label">Say innovation is their top skill</div>
  </div>
  <div class="stat">
    <div class="number">33%</div>
    <div class="stat-label">Focus on digital expansion</div>
  </div>
</div>

<div class="section-list">
  <div class="section-item">
    <h3>Biggest concerns: security &amp; privacy</h3>
    <p>&ldquo;Where does the information go?&rdquo; &mdash; the top concern across public libraries. Use of public LLMs with library data is a governance issue.</p>
  </div>
  <div class="section-item">
    <h3>Environmental impacts</h3>
    <p>Came up at PLA from 3 different customers, largely in areas where data centers are being built. Ashley offered a counterpoint: data centers were already being built during the Big Data era, and AI may actually help <em>reduce</em> environmental impact through efficiencies (e.g., supply chain emissions reduction via prescriptive analytics).</p>
  </div>
  <div class="section-item">
    <h3>Budget concerns</h3>
    <p>All current Clarivate AI features (Data Explorer, Metadata Assistant, etc.) are <strong>included under existing licenses</strong> &mdash; no extra cost. Ashley acknowledged this is a &ldquo;golden age&rdquo; of cost vs. value.</p>
  </div>
</div>

<div class="card">
  <p><strong>Key quote from survey:</strong> <em>&ldquo;Getting beyond initial exploration and into problem solving with AI will therefore be essential to libraries taking a positive long term strategic approach.&rdquo;</em></p>
</div>

## Keys to Successful AI Adoption

<div class="section-list">
  <div class="section-item">
    <h3>1. Strategic leadership</h3>
    <p>Libraries that have identified someone to champion AI &mdash; making decisions, setting guidelines, working on policy &mdash; are seeing more successful adoption.</p>
  </div>
  <div class="section-item">
    <h3>2. Invest in training and development</h3>
    <p>Clarivate has invested heavily in internal AI training over the past year. Libraries seeing success are doing the same &mdash; upskilling staff to understand business problems and apply tools effectively.</p>
  </div>
  <div class="section-item">
    <h3>3. Close the implementation gap</h3>
    <p>Don&rsquo;t dive in with scattershot AI adoption. Understand your business problems first, then run focused proof of concepts. <strong>It&rsquo;s OK if a POC isn&rsquo;t successful</strong> &mdash; that&rsquo;s the point.</p>
  </div>
</div>

## Clarivate's Responsible AI Framework

<div class="section-list">
  <div class="section-item">
    <h3>Transparent</h3>
    <p>Clear indication of AI features. Clear information about what data is used and how. Data is not stored with AI agents.</p>
  </div>
  <div class="section-item">
    <h3>Ethical</h3>
    <p>AI with a purpose &mdash; solving real problems, not playing around. Measures to reduce bad information. Collaboration with industry organizations and the Customer Advisory Board on responsible AI implementations.</p>
  </div>
  <div class="section-item">
    <h3>Safe</h3>
    <p>Human in the loop. Uphold privacy &amp; security standards. Adherence to evolving global regulations. Referenced the NIST AI Risk Management Framework. <a href="ai-the-right-way-ray-notes.html#nist-framework">&#128206;</a></p>
  </div>
</div>

<div class="card">
  <p><strong>AI model:</strong> Clarivate uses a smaller, closed AI model (&ldquo;Mini&rdquo;) as part of their controlled environment.</p>
</div>

## New Public AI Advisory Board

<div class="card">
  <p>Launching in the latter half of 2026. Clarivate&rsquo;s academic side already has an AI Advisory Board; the public board follows that model.</p>
  <ul style="margin: 0.75rem 0 0 1.5rem;">
    <li>Share knowledge across the community</li>
    <li>Develop best practices for responsible AI in public libraries</li>
    <li>Collaborate on prioritization and responsible adoption</li>
    <li>Diverse membership: academic crossover, industry analysts, and other sectors</li>
    <li>Invite-only, but findings shared via knowledge portal</li>
  </ul>
</div>

## AI Product Roadmap

### Already in the Vega Suite

<div class="section-list">
  <div class="section-item">
    <h3>Vega Promote &amp; LX Starter</h3>
    <p>AI-assisted content generation for newsletters and community outreach. On-demand AI image generation.</p>
  </div>
  <div class="section-item">
    <h3>Vega WebBuilder</h3>
    <p>AI-enhanced web experiences (available as an option).</p>
  </div>
</div>

### Coming to the ILS — Intelligent Automation

<div class="section-list">
  <div class="section-item">
    <h3>Polaris Data Explorer <span class="tag new">Coming EOY</span></h3>
    <p>Generate SQL via natural language search. Early access coming by end of year.</p>
  </div>
  <div class="section-item">
    <h3>Metadata Assistant</h3>
    <p>Generates MARC suggestions, saving libraries <strong>20&ndash;180 minutes per record</strong>.</p>
  </div>
</div>

### Accelerating in 2026

<div class="section-list">
  <div class="section-item">
    <h3>Vega Reports</h3>
    <p>Conversational AI for reporting and analytics. Supports AI for Polaris and Sierra as well.</p>
  </div>
  <div class="section-item">
    <h3>Vega Discover</h3>
    <p>Showcase generation. Natural Language Search and Chat POCs.</p>
  </div>
  <div class="section-item">
    <h3>Acquisitions Agent</h3>
    <p>Handles purchasing and invoicing workflows.</p>
  </div>
</div>

## Academic AI Cross-Pollination

<div class="card">
  <p>Clarivate&rsquo;s academic side is ahead on AI adoption, and the public side benefits from their learnings. Key product:</p>
  <p style="margin-top: 0.75rem;"><strong><a href="https://clarivate.com/academia-government/nexus-academic-assistant/">Nexus</a></strong> &mdash; a browser extension that works inside ChatGPT, Claude, and Gemini. Scans AI responses for scholarly references and verifies them against Web of Science, ProQuest, and Primo/Summon. <a href="ai-the-right-way-ray-notes.html#nexus-details">&#128206;</a></p>
</div>

## Audience Q&A

<div class="section-list">
  <div class="section-item">
    <h3>Proof of concepts &amp; &ldquo;failing fast&rdquo;</h3>
    <p>Audience member commented on the value of achieving a failure state quickly &mdash; it&rsquo;s much quicker to develop and test ideas with AI. &ldquo;What didn&rsquo;t work is sometimes a lot more valuable than anything else.&rdquo; Ashley agreed and noted AI is also excellent for <strong>problem refinement</strong>: &ldquo;Here is the problem I&rsquo;m having &mdash; what are the data points or KPIs I need?&rdquo;</p>
  </div>
  <div class="section-item">
    <h3>Vibe coding &amp; library catalogs <a href="ai-the-right-way-ray-notes.html#library-spy">&#128206;</a></h3>
    <p>Question raised about a &ldquo;bring your own agent&rdquo; model &mdash; making catalogs more agent-friendly rather than having agents scrape them in uncontrolled ways. Ashley acknowledged this is a security concern: &ldquo;These things are so hungry for data, and your catalog is an obvious source.&rdquo; Need guardrails to prevent agents from bringing down existing infrastructure.</p>
  </div>
  <div class="section-item">
    <h3>AI model costs</h3>
    <p>Will AI features eventually cost extra? Ashley: &ldquo;We&rsquo;re in a golden age of cost vs. value.&rdquo; AI providers are already &ldquo;turning up the dial.&rdquo; Current features won&rsquo;t have added costs, but more advanced capabilities may. &ldquo;We&rsquo;re very hesitant in the environment we find ourselves in.&rdquo;</p>
  </div>
</div>
```

- [ ] **Step 2: Build and verify both pages render correctly**

Run: `cd iug2026-shared && uv run python build.py --dev --port 8765`
Open in a browser:
- `http://localhost:8765/ai-the-right-way.html` — confirm:
  - Supplemental banner appears at top (under the speaker card)
  - Each `📎` inline marker is clickable
  - Clicking a marker jumps to the correct anchor on the supplemental page
- `http://localhost:8765/ai-the-right-way-ray-notes.html` — confirm:
  - First-person attribution header displays clearly
  - All anchors (`#wef-jobs-report`, `#literary-references`, `#pulse-2025-pdf`, `#nist-framework`, `#nexus-details`, `#library-spy`, etc.) exist and are reachable
  - Breadcrumb links back to primary
- `http://localhost:8765/tuesday.html` — confirm "AI The Right Way" still appears in the day's session list, and the supplemental does NOT appear separately.

Press Ctrl+C to stop the dev server.

---

### Task 7: Update test_build.py for the new supplemental page

**Files:**
- Modify: `iug2026-shared/test_build.py`

- [ ] **Step 1: Add the supplemental file to the expected pages set**

Edit `iug2026-shared/test_build.py`. In `TestBuildCompleteness.test_expected_pages_built` (around line 32), add `"ai-the-right-way-ray-notes.html"` to the `expected` set.

The relevant chunk before:
```python
expected = {
    "index.html",
    "sunday.html", "monday.html", "tuesday.html", "wednesday.html",
    "speakers.html",
    "sierra-roadmap.html", "hackathon-awards.html", "amazon-business.html",
    "ai-the-right-way.html", "vega-reports.html", "resource-sharing.html",
    ...
```

After:
```python
expected = {
    "index.html",
    "sunday.html", "monday.html", "tuesday.html", "wednesday.html",
    "speakers.html",
    "sierra-roadmap.html", "hackathon-awards.html", "amazon-business.html",
    "ai-the-right-way.html", "ai-the-right-way-ray-notes.html",
    "vega-reports.html", "resource-sharing.html",
    ...
```

- [ ] **Step 2: Run the tests**

Run: `cd iug2026-shared && uv run pytest test_build.py -v`
Expected: All tests pass, including `test_expected_pages_built`.

If other tests fail (e.g., one that asserts session counts in the day pages or speakers index), investigate before claiming success — the supplemental should not be counted as a session.

---

### Task 8: Final commit of the migration

- [ ] **Step 1: Stage the migration files**

```bash
cd iug2026-shared
git add content/ai-the-right-way.md content/ai-the-right-way-ray-notes.md test_build.py
git status
```
Expected: Three files staged (one modified, one created, one modified).

- [ ] **Step 2: Commit**

```bash
git commit -m "$(cat <<'EOF'
content: split ai-the-right-way per supplemental-notes spec

Primary page now contains only what Ashley directly presented (verbatim
quotes and paraphrased claims). Research, citations, external links, and
my own commentary moved to ai-the-right-way-ray-notes.html, which is
clearly attributed as Ray's personal research notes and reachable only
via inline markers and the header banner on the primary page.

First concrete application of the supplemental-notes pattern; same
migration pending for vega-reports, sierra-year-in-review, sierra-roadmap,
and meep.

Refs: specs/2026-04-29-supplemental-notes-design.md
EOF
)"
```

- [ ] **Step 3: Verify final state**

```bash
cd iug2026-shared
git log --oneline -5
git status
```
Expected: Recent commits include "feat: add supplemental.html template", "feat: conditional supplemental-notes banner...", "feat: add CSS for supplemental-banner...", "content: split ai-the-right-way..." Working tree clean.
