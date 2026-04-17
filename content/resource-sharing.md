---
title: "Resource Sharing Update"
template: session
day: tuesday
date: "April 14"
speakers:
  - hope-harley
  - katy-aranoff
speakers_display: "Hope Harley & Katy Aranoff · Denver Room"
description: "Rapido resource sharing: consortial borrowing across SearchOhio/OhioLINK (110+ libraries), Rapido stand-alone for academics (5.5M requests, 96% fill rate)."
---

<div class="card">
  <p>Two-part session covering the Rapido resource sharing platform: <strong>Rapido CB</strong> (Consortial Borrowing) for cross-ILS lending, and <strong>Rapido stand-alone</strong> for academic institutions. Features the SearchOhio/OhioLINK deployment &mdash; the largest cross-ILS Rapido implementation to date.</p>
</div>

## Part 1: Rapido Consortial Borrowing

<p style="margin-bottom: 1rem; color: #777;">Presented by Hope Harley</p>

<h3 style="color: var(--navy); margin-bottom: 0.75rem;">SearchOhio / OhioLINK Deployment</h3>

<div class="stats-row">
  <div class="stat">
    <div class="number">11</div>
    <div class="stat-label">Sierra libraries</div>
  </div>
  <div class="stat">
    <div class="number">6</div>
    <div class="stat-label">Polaris libraries</div>
  </div>
  <div class="stat">
    <div class="number">5</div>
    <div class="stat-label">Other ILS</div>
  </div>
  <div class="stat">
    <div class="number">88</div>
    <div class="stat-label">Alma (OhioLINK)</div>
  </div>
</div>

<div class="section-list">
  <div class="section-item">
    <h3>Timeline</h3>
    <p><strong>February 5, 2026</strong> &mdash; SearchOhio soft launch (go-live)</p>
    <p><strong>March 2026</strong> &mdash; Connected with OhioLINK (88 Alma academic institutions)</p>
    <p>Met with staff from 8 libraries to work through a prioritized list of challenges. Feedback used to strengthen the solution &mdash; a Clarivate investment.</p>
  </div>
</div>

<h3 style="color: var(--navy); margin-bottom: 0.75rem;">52-Day Usage Stats (as of April 1)</h3>

<div class="stats-row">
  <div class="stat">
    <div class="number">~45K</div>
    <div class="stat-label">Requests submitted</div>
  </div>
  <div class="stat">
    <div class="number">37%</div>
    <div class="stat-label">Fill rate</div>
  </div>
  <div class="stat">
    <div class="number">~865</div>
    <div class="stat-label">Requests / day</div>
  </div>
  <div class="stat">
    <div class="number">6 days</div>
    <div class="stat-label">Avg turnaround</div>
  </div>
</div>

<h3 style="color: var(--navy); margin-bottom: 0.75rem;">Same Goals, Fundamentally Different Approach</h3>

<table>
  <thead>
    <tr><th></th><th>INN-Reach (old)</th><th>Rapido CB (new)</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Infrastructure</strong></td>
      <td>Local server</td>
      <td>Cloud-based architecture</td>
    </tr>
    <tr>
      <td><strong>Catalog</strong></td>
      <td>Separate union catalog</td>
      <td>Integrated catalog &mdash; single search across SearchOhio + OhioLINK</td>
    </tr>
    <tr>
      <td><strong>Request interface</strong></td>
      <td>Per-ILS</td>
      <td>Vega CRI (Central Request Interface)</td>
    </tr>
    <tr>
      <td><strong>Holdings data</strong></td>
      <td>Stored in union catalog</td>
      <td>Tracks bibs only &mdash; real-time callbacks to each ILS for item availability</td>
    </tr>
  </tbody>
</table>

<div class="section-list">
  <div class="section-item">
    <h3>What stays the same</h3>
    <p>Sierra and Polaris staff stay in their native catalog &mdash; workflows unchanged. ILS-specific operations remain in each system.</p>
  </div>
  <div class="section-item">
    <h3>Known gap being addressed</h3>
    <p>Rapido CB does not readily show holdings because it only stores bibs and does real-time lookups. This is a recognized issue actively being worked on.</p>
  </div>
</div>

<h3 style="color: var(--navy); margin-bottom: 0.75rem;">What's Next</h3>

<div class="section-list">
  <div class="section-item">
    <h3>Staff requesting</h3>
    <p>Ability for staff to place requests on behalf of patrons.</p>
  </div>
  <div class="section-item">
    <h3>Holdings &amp; availability display</h3>
    <p>Fixing the visibility gap &mdash; making holdings data visible in the interface.</p>
  </div>
  <div class="section-item">
    <h3>Local Vega Discover integration</h3>
    <p>SearchOhio/OhioLINK results surfaced directly in each library's own Vega Discover instance &mdash; patrons never need to leave their home catalog.</p>
  </div>
  <div class="section-item">
    <h3>PIN authentication transition</h3>
    <p>Many member libraries still use barcode-only auth. Rapido requires PIN-based auth via Vega Discover. Focus is on minimizing disruption during migration.</p>
  </div>
  <div class="section-item">
    <h3>Idea Exchange</h3>
    <p>Using Clarivate's Idea Exchange as the feedback channel for Rapido CB feature requests and prioritization.</p>
  </div>
</div>

<h3 style="color: var(--navy); margin-bottom: 0.75rem;">Next Deployment</h3>

<div class="card">
  <p><strong>San Diego circuit</strong> is the next group of libraries to deploy Rapido CB resource sharing.</p>
  <p>Target go-live: <strong>late June 2026</strong></p>
</div>

## Part 2: Rapido Stand-Alone

<p style="margin-bottom: 1rem; color: #777;">Presented by Katy Aranoff</p>

<div class="section-list">
  <div class="section-item">
    <h3>What is Rapido?</h3>
    <p>A resource sharing solution integrated with the library system that streamlines the user experience. Primarily aimed at <strong>academic library partners</strong>.</p>
    <ul style="padding-left: 1.25rem; margin: 0.5rem 0 0;">
      <li>Libraries manage ILL and the system searches the collection catalog</li>
      <li>Staff manage all their requests in one place</li>
      <li>Users place and track their requests in one system</li>
    </ul>
  </div>
</div>

<h3 style="color: var(--navy); margin-bottom: 0.75rem;">Key Features</h3>

<div class="section-list">
  <div class="section-item">
    <h3>Metadata import</h3>
    <p>Rapido automatically imports metadata for articles and physical books when patrons place requests &mdash; easing the process and improving fill rates. No more manual citation entry.</p>
  </div>
  <div class="section-item">
    <h3>Patron transparency</h3>
    <p>Users see request status and progress directly in their library card using familiar language &mdash; not ILL jargon.</p>
  </div>
  <div class="section-item">
    <h3>Smart automation</h3>
    <p>Routine requests handled automatically. Staff focus on mediating complex requests. Libraries configure workflows to match their own policies. Enables handling higher volume without adding staff.</p>
  </div>
  <div class="section-item">
    <h3>Timezone-based routing</h3>
    <p>Requests route to partners in active timezones for faster fulfillment &mdash; not just proximity-based.</p>
  </div>
</div>

<h3 style="color: var(--navy); margin-bottom: 0.75rem;">2025 Performance</h3>

<div class="stats-row">
  <div class="stat">
    <div class="number">5.5M</div>
    <div class="stat-label">Requests</div>
  </div>
  <div class="stat">
    <div class="number">96%</div>
    <div class="stat-label">Fill rate</div>
  </div>
  <div class="stat">
    <div class="number">9.8 hrs</div>
    <div class="stat-label">Digital turnaround</div>
  </div>
  <div class="stat">
    <div class="number">95%</div>
    <div class="stat-label">First-partner fill</div>
  </div>
</div>

<div class="card">
  <p><strong>Global community:</strong> Rapido is active across <strong>20 countries</strong> spanning USA/Canada, Latin America, EMEA, APAC, Africa, and Australia/New Zealand.</p>
</div>

## Q&A Highlights

<div class="section-list">
  <div class="section-item">
    <h3>Item type distinction</h3>
    <p>Distinguishing item types (e.g., DVD vs. Blu-ray) is one of the <strong>top features requested</strong> at listening sessions. Patrons need to tell formats apart when requesting through Rapido.</p>
  </div>
  <div class="section-item">
    <h3>INN-Reach is not going away &mdash; but Rapido is next-gen</h3>
    <p>Not rushing anyone off INN-Reach, but the two systems <strong>do not interoperate and likely never will</strong>. No plans to build a bridge. When a consortium moves to Rapido, it's a full cutover.</p>
  </div>
  <div class="section-item">
    <h3>Moving away from OCLC ILL</h3>
    <p>Trend toward fewer OCLC resource sharing platforms and reducing dependency on OCLC ILL. Rapido offers <strong>customizable workflow management</strong> that puts more control in the hands of staff users.</p>
  </div>
</div>

## Slide Photos

<div class="sources">
  <ol>
    <li><a href="https://photos.app.goo.gl/mxMfA6hJ36z1NLgo6">Slide photos &mdash; Google Photos album</a></li>
  </ol>
</div>
