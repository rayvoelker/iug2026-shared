---
title: "About This Site"
template: page
page_subtitle: "How this conference knowledge base was built"
description: "About the IUG 2026 conference notes site — who built it, how it works, and what it contains."
---

<div class="card">
  <h3>About the Author</h3>
  <p><strong>Ray Voelker</strong> is a library technology professional and IUG conference attendee. He works with Sierra ILS, library data systems, and open-source tools like Datasette. You can find him on GitHub at <a href="https://github.com/rayvoelker">@rayvoelker</a>.</p>
  <p style="margin-top: 0.5rem;">At IUG 2026, Ray presented two talks at the Great ILS-Data Pre-Conference: <a href="https://rayvoelker.github.io/iug2026/talk-combined-datasette-at-the-library.html">Datasette at the Library</a> and <a href="https://rayvoelker.github.io/iug2026/talk-datalake-building-a-data-lake.html">Building a Data Lake</a>.</p>
</div>

## What This Site Contains

This is a conference knowledge base for IUG 2026 (Innovative Users Group), held April 12&ndash;15 at the Chicago Marriott Downtown Magnificent Mile. It contains:

<div class="section-list">
  <div class="section-item">
    <h3>Session Notes</h3>
    <p>Detailed notes from 15+ sessions across all four days &mdash; keynotes, breakout sessions, forums, and birds-of-a-feather discussions covering Sierra, Polaris, Vega, and cross-platform topics.</p>
  </div>
  <div class="section-item">
    <h3>Technical Guides</h3>
    <p>Deep-dive reference guides written up from session content &mdash; including a <a href="cloudflare-sierra-guide.html">Cloudflare protection guide for Sierra</a>, an <a href="sierra-sso-guide.html">SSO implementation guide</a>, and a <a href="suggest-a-purchase.html">Suggest-a-Purchase comparison</a>.</p>
  </div>
  <div class="section-item">
    <h3>Speaker Cards</h3>
    <p>A <a href="speakers.html">gallery of 150 speakers</a> with session history, stats, and rarity tiers spanning multiple IUG years.</p>
  </div>
  <div class="section-item">
    <h3>LLM Navigation</h3>
    <p>Auto-generated <a href="llms.txt">llms.txt</a> and <a href="llms-full.txt">llms-full.txt</a> files so AI agents can navigate and understand the site content.</p>
  </div>
</div>

## How It Was Built

This site was built collaboratively with <a href="https://claude.ai/claude-code">Claude Code</a> (Anthropic's AI coding tool). The entire pipeline &mdash; from initial conference note-taking through the final published site &mdash; was a human-AI collaboration.

<div class="section-list">
  <div class="section-item">
    <h3>Architecture</h3>
    <p>A Python static site generator: 22 markdown+frontmatter content files, 6 Jinja2 templates, a ~350-line build script, and a YAML site config. Content is the source of truth; presentation is separated into templates and CSS.</p>
  </div>
  <div class="section-item">
    <h3>Speaker Data Pipeline</h3>
    <p>Speaker data was scraped from <a href="https://iug2026.sched.com/">sched.com</a>, parsed, enriched with rarity tiers and session history, and merged with hand-edited fields (quotes, affiliations). The result is a 150-speaker JSON database that powers the speaker cards gallery.</p>
  </div>
  <div class="section-item">
    <h3>Deployment</h3>
    <p>The build script outputs static HTML to a <code>docs/</code> directory, served by GitHub Pages. A dev server with file watching supports live editing.</p>
  </div>
  <div class="section-item">
    <h3>Testing</h3>
    <p>A pytest test suite verifies build completeness, catches HTML rendering issues, detects duplicate content, and validates all inter-page links and speaker references.</p>
  </div>
</div>

<div class="card" style="margin-top: 1.5rem;">
  <p>The source code is open: <a href="https://github.com/rayvoelker/iug2026-shared">github.com/rayvoelker/iug2026-shared</a>. Corrections and contributions welcome &mdash; file an issue or open a PR.</p>
</div>
