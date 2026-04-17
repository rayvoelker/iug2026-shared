---
title: "Sierra Year in Review"
template: session
day: tuesday
date: "April 14"
speakers:
  - mike-dicus
speakers_display: "Mike Dicus · McHenry Room · Sierra Track"
description: "Sierra 6.4 and 6.5 release highlights: patron checkout limits, inventory check-in at circulation, Admin Corner migration, Create Lists navigation, and IMMS enhancements."
---

<div class="card">
  <p>A walkthrough of features delivered in the Sierra <strong>6.4</strong> (June 2025) and <strong>6.5</strong> (November 2025) releases, with a focus on customer-driven enhancements sourced from MEEP, Idea Exchange, and direct user feedback. More than half of Sierra libraries worldwide are now running either 6.4 or 6.5.</p>
  <p style="margin-top: 0.5rem; font-size: 0.9rem; color: #777;">See also: <a href="sierra-roadmap.html">Sierra Roadmap (Monday)</a> for the May and November 2026 release plans.</p>
</div>

## Sierra 6.4 Highlights (June 2025)

### Return Date in Patron History

<div class="card">
  <ul>
    <li>Added the <strong>return date</strong> as a new field in patron reading history (field group 38).</li>
    <li>When a patron borrows and returns an item, the return date is now recorded &mdash; patrons can see they had an item last month, last year, or several years ago.</li>
  </ul>
</div>

## Sierra 6.5 Highlights (November 2025)

### Patron Checkout Limits

<div class="card">
  <p>The headline feature of 6.5 &mdash; originated from MEEP / Idea Exchange requests to extend the category A&ndash;D values beyond four options.</p>
  <ul>
    <li><strong>What it does:</strong> Configures checkout limits by <strong>patron type</strong> combined with a second variable:
      <ul>
        <li>Patron type + item type</li>
        <li>Patron type + item location</li>
        <li>Patron type + library location / location served</li>
      </ul>
    </li>
    <li><strong>Configuration:</strong> Found in <em>Circulation &rarr; Administration &rarr; Patron Checkout Limits</em>, with three tabs: item type blocks, item location blocks, and location served settings.</li>
    <li><strong>Import/export:</strong> Limits can be imported and exported via CSV &mdash; critical for libraries needing hundreds or thousands of limit combinations.</li>
    <li><strong>Staff override:</strong> When a patron hits a limit, staff see a pop-up identifying the specific limit exceeded (e.g., &ldquo;item type: Picture Book, limit: 3, current: 3&rdquo;). Staff can override, and overrides are logged in the circulation override logs.</li>
  </ul>

  <h4>Loan Rule Precedence Order</h4>
  <ol>
    <li>Patron blocks (expired card, etc.)</li>
    <li>Item location and library location blocks</li>
    <li>Item type blocks</li>
    <li>All other block types (including patron checkout limits)</li>
  </ol>
</div>

### Print Locations Served Table

<div class="card">
  <ul>
    <li>New option in the Sierra client to <strong>print the locations served table</strong> directly.</li>
    <li>Previously required contacting support. Now available self-service.</li>
  </ul>
</div>

### Navigate to Patron Record from Item Record

<div class="card">
  <ul>
    <li>From any item record (Acquisitions, Cataloging, or Circulation), staff can <strong>open the patron record</strong> for the current or last patron.</li>
    <li>Three navigation methods:
      <ul>
        <li>Double-click on the current/last patron field</li>
        <li>Edit menu &rarr; View actions &rarr; Navigate to patron (view or edit mode)</li>
        <li>Right-click context menu</li>
      </ul>
    </li>
    <li>Opens the patron record in the checkout screen, ready for action.</li>
  </ul>
</div>

### Penalty Points for Unclaimed Holds

<div class="card">
  <ul>
    <li>Extended the penalty points / demerits system to support <strong>unclaimed holds</strong>.</li>
    <li>Libraries can assess penalty points when a patron fails to pick up a held item.</li>
    <li>Point values are library-defined; accumulated points can block further transactions for a configurable period.</li>
  </ul>
</div>

### Create Lists — Delete Records Navigation

<div class="card">
  <ul>
    <li>Continued the navigation enhancement started in 6.3 (Create Lists &rarr; Global Update, Rapid Update).</li>
    <li><strong>New in 6.5:</strong> Jump from Create Lists directly to <strong>Delete Records</strong> with the review file name pre-populated.</li>
    <li>More navigation targets planned for future releases based on Idea Exchange requests.</li>
  </ul>
</div>

### Inventory Check-in via Circulation Desk

<div class="card">
  <ul>
    <li>Uses the standard check-in screen with a configurable switch in the SDA.</li>
    <li><strong>Configuration options per branch / location served:</strong>
      <ul>
        <li>Start date only (perpetual inventory &mdash; never turns off)</li>
        <li>Start and end dates (time-limited inventory period)</li>
      </ul>
    </li>
    <li>Updates the <strong>inventory date field</strong> in the item record with each scan.</li>
    <li>Status bar shows &ldquo;Inventory check-in is enabled&rdquo; and a running count of items scanned.</li>
    <li><strong>Popular use case:</strong> Perpetual inventory &mdash; leave it on permanently so every scan updates the last-seen date.</li>
    <li>Some libraries have relabeled the field to &ldquo;Last Scanned.&rdquo;</li>
    <li><strong>Note:</strong> If you don&rsquo;t have an inventory date field in your item records, open a support ticket to have it enabled.</li>
  </ul>
</div>

### Admin Corner — Sierra Client / Admin App Migration

<div class="card">
  <table>
    <thead>
      <tr><th>Feature</th><th>Moved To</th></tr>
    </thead>
    <tbody>
      <tr><td>System status (record counts)</td><td>Admin App (web-based)</td></tr>
      <tr><td>Restart terminal</td><td>Admin App</td></tr>
      <tr><td>Scope menu maintenance</td><td>Sierra Client</td></tr>
      <tr><td>Check missing items</td><td>Sierra Client</td></tr>
      <tr><td>Batch check-in (from review files)</td><td>Sierra Client / Sierra Web</td></tr>
    </tbody>
  </table>
  <p style="margin-top: 1rem;"><strong>Check Missing Items:</strong> Displays items previously marked missing whose status has since changed. Staff can right-click to view records, sort by column, and clear items individually or in bulk.</p>
  <p><strong>Batch Check-in:</strong> Select a review file of items to check in. Bypasses normal check-in logic (transits, holds) &mdash; a quick process to clear items from checkout status.</p>
  <p><strong>Scope Menu Maintenance:</strong> Update scope names and numbers directly in the client, eliminating the need for support tickets or Admin Corner.</p>
</div>

### Create Lists Without Patron Data

<div class="card">
  <ul>
    <li>New permission allows staff to use Create Lists <strong>without access to patron data</strong>.</li>
    <li>Operates at the lowest permission level &mdash; if a staff member also has a higher Create Lists permission, the higher one takes precedence.</li>
    <li>Staff with only this permission cannot view or create review files containing patron data.</li>
  </ul>
</div>

### IMMS (Intelligent Materials Management System) Enhancements

<div class="card">
  <p>For libraries using automated materials handling:</p>
  <ul>
    <li><strong>Exhibition/display routing:</strong> New settings identify display or exhibition locations. Items are evaluated at check-in for routing to active exhibitions based on subject criteria and available space.</li>
    <li><strong>Chaotic hold shelf assignment:</strong> Supports random shelf assignment for holds (no slips in items). Pickup shelf location is displayed in staff screens and patron notifications.</li>
  </ul>
</div>

### Other Changes

<div class="card">
  <table>
    <thead>
      <tr><th>Enhancement</th><th>Details</th></tr>
    </thead>
    <tbody>
      <tr><td>Locations served limit doubled</td><td>From 1,000 to <strong>2,000</strong> location codes per entry</td></tr>
      <tr><td>SQS connection test for notices</td><td>Tests connectivity before sending notice data to Alma Starter; prevents data loss</td></tr>
      <tr><td>Accessibility improvements</td><td>Name, role, and value attributes set for fields in circulation and search screens</td></tr>
      <tr><td>Client branding update</td><td><strong>Glacier Point</strong>: light gray theme. <strong>Half Dome</strong>: dark theme. Switchable via <em>Settings &rarr; Display</em>.</td></tr>
    </tbody>
  </table>
</div>

## Library Engagement & Feedback Channels

<div class="card">
  <ul>
    <li><strong>Product Roadmap Portal</strong> &mdash; vote on features from &ldquo;not important&rdquo; to &ldquo;critically important&rdquo; and add comments <em>(customer login required)</em></li>
    <li><strong>Idea Exchange</strong> &mdash; submit and vote on ideas
      <ul>
        <li>120+ users/day average</li>
        <li>~1,200 total users</li>
        <li>900 new ideas in the past 12 months</li>
        <li>~14,000 votes</li>
        <li>1,500+ comments</li>
      </ul>
    </li>
    <li><strong>MEEP session</strong> &mdash; Tuesday at 3:00 PM with Katie LeBlanc and Alex Vancina</li>
  </ul>

  <h3>Links</h3>
  <ul>
    <li><a href="https://www.iii.com/resources/webinars/">Webinars &amp; Recordings</a></li>
    <li><a href="https://iii.com/roadmap/">Product Roadmap Portal</a> <em>(customer login required)</em></li>
    <li><a href="https://ideaexchange.iii.com/">Idea Exchange</a></li>
  </ul>
</div>

## Slide Photos

<div class="sources">
  <ol>
    <li><a href="https://photos.app.goo.gl/zoPBpkxfebk75eiQ8">Slide photos &mdash; Google Photos album</a></li>
  </ol>
</div>

*Note: These notes begin mid-presentation during the 6.4 return-date feature discussion. The first portion of the session (likely covering earlier 6.4 features and overall statistics) was not captured.*
