---
title: "IUG 2026 Hackathon Awards"
template: session
day: monday
date: "April 13"
speakers:
  - gabrielle-gosselin
  - mike-dicus
speakers_display: "Monday, April 13 · 4:00–5:00 PM"
description: "Six hackathon projects solving real library problems: FindIt, Browsr, Shelf Defense (winner), Leap SQL, Auto-Suggest-a-Purchase, and Microprojects."
---

<div class="card">
  <h3>Organizers</h3>
  <p><strong>Gabrielle Gosselin</strong> and <strong>Mike Dicus</strong></p>
  <p style="font-size: 0.85rem; color: #777; margin-top: 0.5rem;">Six teams presented projects built during the IUG Hackathon pre-conference. All projects solve real operational problems for libraries using Polaris, Sierra, or standard protocols like SIP2.</p>
</div>

<!-- TOC -->
<div class="card" style="margin-bottom: 1.5rem;">
  <h3>Projects</h3>
  <ol style="padding-left: 1.25rem; margin: 0.5rem 0 0 0; line-height: 1.8;">
    <li><a href="#findit">FindIt</a> &mdash; Shelf mapping for Vega catalogs <span class="tag new" style="vertical-align: middle;">Polaris / PAPI</span></li>
    <li><a href="#browsr">Browsr</a> &mdash; Curated collection browsing <span class="tag new" style="vertical-align: middle;">Polaris / PAPI</span></li>
    <li><a href="#shelf-defense">Shelf Defense</a> &mdash; Offline circulation tool <span class="tag award" style="vertical-align: middle;">Winner</span></li>
    <li><a href="#leap-sql">Leap SQL Template Manager</a> &mdash; Parameterized SQL for consortia <span class="tag new" style="vertical-align: middle;">Polaris / SQL</span></li>
    <li><a href="#auto-suggest">Auto-Suggest-a-Purchase</a> &mdash; Patron purchase requests <span class="tag new" style="vertical-align: middle;">Polaris</span></li>
    <li><a href="#microprojects">Microprojects</a> &mdash; Sierra bulk editing via API <span class="tag new" style="vertical-align: middle;">Sierra / API</span></li>
  </ol>
</div>

<!-- Winners Circle -->
<div class="update announcement" style="margin: 1.5rem 0;">
  <div class="update-meta">Winner</div>
  <h3>Shelf Defense &mdash; A Better Offline Circulation Tool</h3>
  <p>By Wes and Bryan. SIP2-based offline checkout system built on PocketBase. <a href="#shelf-defense">Details below &darr;</a></p>
  <div style="display: flex; gap: 1rem; margin-top: 1rem; flex-wrap: wrap;">
    <img src="assets/hackathon/winners-closeup.jpg" alt="Hackathon winners — Bryan and team" style="border-radius: 6px; max-width: 48%; height: auto; box-shadow: 0 2px 6px rgba(0,0,0,0.15);">
    <img src="assets/hackathon/winners-award.jpg" alt="Hackathon award presentation" style="border-radius: 6px; max-width: 48%; height: auto; box-shadow: 0 2px 6px rgba(0,0,0,0.15);">
  </div>
</div>

## The Projects

<!-- FindIt -->
<div class="section-list">
  <div class="section-item" id="findit">
    <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap;">
      <h3>FindIt &mdash; Shelf Mapping for Vega Catalogs</h3>
      <span class="tag new">Polaris / PAPI</span>
    </div>
    <p><strong>Rochester Hills Public Library</strong> &middot; <a href="https://github.com/RHPubLib/FindIt">GitHub</a> (MIT)</p>
    <p style="margin-top: 0.5rem;">Adds interactive floor maps to the Vega Discover catalog. Patrons search, find an item, and see exactly where it sits on the shelf. <strong>Search &rarr; Find &rarr; Go Get It.</strong></p>

    <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #eee;">
      <p><strong>Three components:</strong></p>
      <ul style="padding-left: 1.25rem; margin-top: 0.25rem;">
        <li><strong>Vega Widget</strong> &mdash; vanilla JS injected via Custom Header Code. Uses MutationObserver to detect availability rows, injects a "View Shelf Location" button that opens an interactive map modal with zoom, pan, and pinch-to-zoom. Multi-branch support with tabs.</li>
        <li><strong>Rectangle Editor</strong> &mdash; Flask web app for staff. Draw shelf zones on floor plan images, map them to call number ranges and collections via PAPI dropdowns, and one-click publish to production.</li>
        <li><strong>Standalone Map App</strong> &mdash; mobile-first search + map at <code>map.rhpl.org</code>. Supports kiosk mode for Chrome OS devices.</li>
      </ul>
    </div>

    <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #eee;">
      <p><strong>Tech:</strong> Vanilla JS (zero dependencies, no build step), Python/Flask, Polaris PAPI (HMAC-SHA1), Google Workspace OAuth</p>
      <p><strong>Key design choice:</strong> Zero framework dependencies so any library can deploy regardless of technical capacity. Self-host mandate &mdash; each library hosts its own copy. Data/code separation &mdash; staff update shelf mappings without touching JavaScript.</p>
    </div>

    <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #eee;">
      <p><strong>Photos:</strong> <a href="https://photos.app.goo.gl/3y7FAS7CZtFhT6Ce7">Presentation slides</a></p>
    </div>
  </div>

  <!-- Browsr -->
  <div class="section-item" id="browsr">
    <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap;">
      <h3>Browsr &mdash; Collection Browsing Tool</h3>
      <span class="tag new">Polaris / PAPI</span>
    </div>
    <p><strong>Andrew</strong></p>
    <p style="margin-top: 0.5rem;">Allows patrons to browse through a smaller, curated collection. Built on the Polaris PAPI.</p>
  </div>

  <!-- Shelf Defense -->
  <div class="section-item" id="shelf-defense" style="border-left: 4px solid var(--gold);">
    <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap;">
      <h3>Shelf Defense &mdash; Offline Circulation Tool</h3>
      <span class="tag award">Winner</span>
    </div>
    <p><strong>Wes and Bryan</strong></p>
    <p style="margin-top: 0.5rem;">A better offline tool for library checkouts. When the network goes down, staff can still circulate items and reconcile later. Started as a complex idea and was narrowed down during the hackathon.</p>

    <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #eee;">
      <ul style="padding-left: 1.25rem;">
        <li><strong>SIP2-based</strong> &mdash; uses the standard library self-checkout protocol, works with any ILS ("bring your own SIP2 server")</li>
        <li><strong>Peer architecture</strong> &mdash; one device acts as the server, others connect to it</li>
        <li><strong>Sync later</strong> &mdash; transactions sync back to the ILS when connectivity is restored, or export to CSV as a fallback</li>
        <li><strong>Cross-platform</strong> &mdash; runs on Windows, Mac, Linux</li>
      </ul>
    </div>

    <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #eee;">
      <p><strong>Tech:</strong> PocketBase (single-file backend &mdash; database, auth, and API in one binary), SIP2</p>
      <p><strong>Built with:</strong> Claude Code and ChatGPT</p>
    </div>

    <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #eee;">
      <p><strong>Photos:</strong> <a href="https://photos.app.goo.gl/J2vWEtC8EnPq3xyi8">Presentation slides</a></p>
    </div>
  </div>

  <!-- Leap SQL -->
  <div class="section-item" id="leap-sql">
    <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap;">
      <h3>Leap SQL Template Manager</h3>
      <span class="tag new">Polaris / SQL</span>
    </div>
    <p><strong>Kalee Gulosh and Mike Parks</strong></p>
    <p style="margin-top: 0.5rem;">Parameterized SQL searches for library staff who don't write SQL. Pick a saved template, fill in a form, run the query. Built for consortium environments where member libraries share query templates with each other.</p>

    <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #eee;">
      <ul style="padding-left: 1.25rem;">
        <li><strong>Template dashboard</strong> &mdash; browse, search, and run saved queries with one click</li>
        <li><strong>Parameterized forms</strong> &mdash; dropdowns and text fields instead of raw SQL</li>
        <li><strong>Consortium sharing</strong> &mdash; one library writes a useful query, the whole consortium benefits</li>
      </ul>
    </div>

    <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #eee;">
      <p><strong>Tech:</strong> ASP.NET / C#, Polaris SQL</p>
    </div>

    <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #eee;">
      <p><strong>Photos:</strong> <a href="https://photos.app.goo.gl/EqrDv5uQrooEwNGy5">Presentation slides</a></p>
    </div>
  </div>

  <!-- Auto-Suggest-a-Purchase -->
  <div class="section-item" id="auto-suggest">
    <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap;">
      <h3>Auto-Suggest-a-Purchase</h3>
      <span class="tag new">Polaris</span>
    </div>
    <p><strong>Somalia Jamall</strong> &mdash; Jacksonville Public Library &middot; <a href="https://github.com/SomaliaJamall/Auto-Suggest-a-Purchase">GitHub</a></p>
    <p style="margin-top: 0.5rem;">Patron-facing purchase suggestion tool that takes work off the collection development team's plate. A nightly script processes suggestions and emails patrons with updates.</p>

    <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #eee;">
      <ul style="padding-left: 1.25rem;">
        <li><strong>Already in production</strong> &mdash; approximately 400 patrons have used it</li>
        <li><strong>Nightly script-based</strong> &mdash; processes suggestions on a schedule and emails patrons</li>
        <li><strong>Solves a real problem</strong> &mdash; reduces manual collection development workload</li>
      </ul>
    </div>

    <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #eee;">
      <p><strong>Tech:</strong> PHP, JavaScript, Python</p>
    </div>
  </div>

  <!-- Microprojects -->
  <div class="section-item" id="microprojects">
    <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap;">
      <h3>Microprojects &mdash; Sierra Bulk Editing</h3>
      <span class="tag new">Sierra / API</span>
    </div>
    <p><strong>Victor Zuniga</strong></p>
    <p style="margin-top: 0.5rem;">Bulk record editing via the Sierra API's Create Lists and Review Files endpoints. Edit multiple variable-length and fixed-length fields at once &mdash; no more record-by-record work in the Sierra client.</p>

    <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #eee;">
      <ul style="padding-left: 1.25rem;">
        <li><strong>Patron records</strong> &mdash; demo showed a "Patron Review Files" interface with Name, Address, Phone, Barcode, Email, and Actions columns</li>
        <li><strong>Create Lists + Review Files</strong> &mdash; uses Sierra API to build lists and then batch-edit through the review file</li>
        <li><strong>Next step:</strong> incorporate permissions</li>
      </ul>
    </div>

    <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #eee;">
      <p><strong>Photos:</strong> <a href="https://photos.app.goo.gl/74bUD5Xceta1funz9">Presentation slides</a></p>
    </div>
  </div>
</div>
