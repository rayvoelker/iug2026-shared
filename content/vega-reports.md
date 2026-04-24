---
title: "Vega Reports for Discover and Beyond"
template: session
day: tuesday
date: "April 14"
speakers:
  - jovana-raskovic
speakers_display: "Jovana Raskovic (Product Manager, Clarivate) · 4:30–5:30 PM · Kansas City Room · Vega Track"
description: "Jovana Raskovic introduces Vega Reports: a unified BI platform powered by Metabase for Discover, Polaris, and Sierra. Covers dashboards, custom SQL queries, OverDrive integration, Metabot AI proof of concept, and the 2026 rollout roadmap."
---

<div class="card">
  <p>Jovana Raskovic presented Vega Reports &mdash; Clarivate&rsquo;s new unified business intelligence platform that brings reporting and analytics to the entire Public ecosystem. Built on Metabase (an open-source BI tool comparable to Tableau or Power BI) with a Postgres backend and a secure data lakehouse architecture, Vega Reports is included at no additional cost with a Vega Discover subscription. The session covered preset dashboards, the query builder and native SQL interfaces, an OverDrive integration preview, a Metabot AI proof of concept, and detailed rollout timelines for Discover, Polaris, and Sierra.</p>
</div>

## What Is Vega Reports

<div class="card">
  <p>One intelligent BI platform unifying reporting and analytics across the Public ecosystem. Powered by a secure data lakehouse and built on <a href="https://www.metabase.com/">Metabase</a> &mdash; an open-source BI tool comparable to Tableau or Power BI &mdash; with a Postgres database backend. Vega Reports is <strong>included with every Vega Discover subscription at no additional cost</strong>. The platform is consortia and international ready.</p>
</div>

<div class="section-list">
  <div class="section-item">
    <h3>Streamlined Staff Flows</h3>
    <p>Single login &mdash; ILS and Vega data unified in one place. No switching between systems to get the data you need.</p>
  </div>
  <div class="section-item">
    <h3>Automated &amp; Intelligent</h3>
    <p>AI tools and modern visualizations built into the platform. Reports can be scheduled, shared, and bookmarked.</p>
  </div>
  <div class="section-item">
    <h3>Secure &amp; Private</h3>
    <p>Data protected within the secure lakehouse architecture. GDPR and CCPA compliant.</p>
  </div>
  <div class="section-item">
    <h3>Unique Insights</h3>
    <p>Third-party data integration (Cloudio) and engagement reporting &mdash; data sources that go beyond what the ILS alone can provide.</p>
  </div>
</div>

## Early Access Partners

<div class="card">
  <p>Four Early Access partners &mdash; <strong>Phoenix Public Library</strong>, <strong>STELLA</strong>, <strong>Mid-Hudson Library System</strong>, and <strong>New York Public Library</strong> &mdash; collaborated with the Vega Reports team over several weeks, providing hands-on feedback that shaped the product before general availability.</p>
</div>

## Setup & Access

<div class="card">
  <p><strong>Vega Reports for Discover</strong> requires an active <strong>Vega Discover subscription</strong>. Polaris and Sierra customers already have <strong>LX Starter</strong> included with their ILS subscription, which enables the connection needed to access Vega Reports. LX Starter does not need to be actively used &mdash; Clarivate simply recommends having it enabled to support access to Vega Reports. Once roles are assigned, Vega Reports appears in the left-hand navigation menu within Vega Discover.</p>
</div>

<div class="section-list">
  <div class="section-item">
    <h3>Super Admin assigns roles</h3>
    <p>Role assignment is handled through Vega Discover User Management. Roles can be assigned at the <strong>main site</strong>, <strong>collection site</strong>, or <strong>kiosk site</strong> level.</p>
  </div>
  <div class="section-item">
    <h3>Reports Admin</h3>
    <p>Full access license. Main site admins get both the <strong>query builder</strong> and <strong>native SQL</strong> access. Collection site admins get query builder only (no SQL access).</p>
  </div>
  <div class="section-item">
    <h3>Reports Consumer</h3>
    <p>View-only license. Consumers can view and interact with reports created by admins but cannot build new queries.</p>
  </div>
</div>

## Dashboards

<div class="card">
  <p>Three preset dashboard categories ship with Vega Reports. These dashboards are <strong>read-only</strong> and are the same for both admin and consumer roles. Data is collected using <strong><a href="https://www.pendo.io/">Pendo</a></strong>, ingested into the data lakehouse via API, and <strong>refreshed every 24 hours</strong>. Data collection begins as soon as a library enables Vega Reports, with <strong>up to one week of historical data backfilled</strong>. From there, data continues to accumulate over time to support trend analysis.</p>
</div>

<div class="section-list">
  <div class="section-item">
    <h3>1. Visitor Statistics</h3>
    <p>User activity across Discover &mdash; unique visitors (distinct count), visitor frequencies, and engagement patterns.</p>
  </div>
  <div class="section-item">
    <h3>2. Search Statistics</h3>
    <p>Top searches, search performance metrics, and weekly trends.</p>
  </div>
  <div class="section-item">
    <h3>3. Marketing Statistics</h3>
    <p>Home page interactions, click patterns, and marketing campaign effectiveness.</p>
  </div>
</div>

<div class="card">
  <p><strong>Sharing &amp; filtering:</strong> Dashboards can be shared via email or PDF, and bookmarked for quick access. A <strong>site filter</strong> allows filtering by site URL &mdash; especially useful for consortia with multiple locations. Each card on the dashboard includes an info tooltip explaining the metric.</p>
</div>

## Building Custom Reports

<div class="card">
  <p>Beyond the preset dashboards, Vega Reports offers <strong>two approaches</strong> for building custom reports. Custom reports can be exported as <strong>CSV or Excel</strong>, and custom report visualizations are fully customizable.</p>
</div>

<div class="section-list">
  <div class="section-item">
    <h3>1. Query Builder</h3>
    <p>A simple select-option menu interface &mdash; no coding required. Select a data source, join tables, add filters, summarize, and aggregate. Both <strong>data models</strong> and <strong>data tables</strong> are available. The toolbar provides: Filter, Summarize, Join data, Sort, Row limit, and Custom column.</p>
  </div>
  <div class="section-item">
    <h3>2. Native SQL Query</h3>
    <p>Direct Postgres SQL access for Reports Admins at the main site level. Write and execute SQL queries against the data lakehouse for maximum flexibility.</p>
  </div>
</div>

<div class="card">
  <p><strong>Visualizations</strong> are available for reports built either way &mdash; Query Builder or Native SQL. Options include bar, line, pie, table, pivot table, gauge, funnel, map, and more. The platform <strong>auto-selects the best visualization</strong> based on the query results, and everything is fully customizable &mdash; colors, naming conventions, and axes can all be adjusted.</p>
</div>

<div class="card">
  <p><strong>Example SQL query</strong> &mdash; aggregating Discover tracking events by type for a given year:</p>
  <pre style="background: #1e1e2e; color: #cdd6f4; padding: 1rem; border-radius: 6px; overflow-x: auto; font-size: 0.85rem; margin-top: 0.75rem; line-height: 1.5;"><code>SELECT
    tt.track_type_name,
    SUM(te.num_events) AS sum
FROM "discover".track_events te
INNER JOIN "discover".track_types tt
    ON te.track_type_id = tt.id
WHERE
    te.last_time >= CAST('2024-01-01 00:00:00Z' AS timestamp)
    AND te.last_time < CAST('2025-01-01 00:00:00Z' AS timestamp)
GROUP BY tt.track_type_name
ORDER BY tt.track_type_name ASC</code></pre>
</div>

## OverDrive Integration Preview

<div class="card">
  <p>Clarivate is working on integrating <strong>OverDrive checkouts data</strong> into Vega Reports for both Polaris and Sierra users. A demo was shown at the sales booth during the conference.</p>
</div>

<div class="section-list">
  <div class="section-item">
    <h3>Key metrics</h3>
    <p>Unique digital checkouts, number of checkouts, and average lending period. A <strong>print copy checkout flag</strong> (yes/no) indicates whether a given title was also checked out in print within the selected timeframe.</p>
  </div>
  <div class="section-item">
    <h3>Filtering</h3>
    <p>Owning branch and checkout branch filters allow libraries to drill into circulation data by location.</p>
  </div>
  <div class="section-item">
    <h3>Digital-to-print matching</h3>
    <p>The team is exploring two approaches: <strong>patron ID matching</strong> in the backend, or <strong>product ID mapping</strong> for titles. Top 100 checked-out digital titles with print copy overlap analysis will help libraries understand format preferences.</p>
  </div>
  <div class="section-item">
    <h3>Trends &amp; usage patterns</h3>
    <p>A variety of trends across time frames, popular titles, and print vs. digital overlap &mdash; giving libraries insight into how their collections are performing across formats.</p>
  </div>
</div>

## Metabot AI (Proof of Concept)

<div class="card">
  <p>Metabase includes an AI tool called <strong>Metabot</strong> that enables natural language interaction with reports and data. Currently, Metabot does <strong>not support self-hosted environments</strong> (which is how Vega Reports operates), so this is a <strong>proof of concept only &mdash; not shipping yet</strong>. Jovana showed a video demo using sample data to illustrate the capabilities.</p>
</div>

<div class="section-list">
  <div class="section-item">
    <h3>AI exploration via chat</h3>
    <p>Ask questions in natural language and get answers from your data through a conversational interface.</p>
  </div>
  <div class="section-item">
    <h3>Natural language report creation</h3>
    <p>Create reports using the query builder via plain English prompts. Step-by-step guided report creation walks users through the process.</p>
  </div>
  <div class="section-item">
    <h3>SQL generation</h3>
    <p>Generate SQL queries from natural language prompts &mdash; no need to know Postgres syntax.</p>
  </div>
  <div class="section-item">
    <h3>Chart analysis &amp; error fixing</h3>
    <p>Analyze and ask questions about existing charts. Metabot can also identify and fix errors in SQL code. Reports can be saved directly to a personal collection.</p>
  </div>
</div>

<div class="card">
  <p><strong>Jovana on AI:</strong> &ldquo;This is the future. We can&rsquo;t run away from it. As long as you run away from something, it&rsquo;s gonna get you sooner rather than later.&rdquo;</p>
</div>

## 2026 Roadmap

<div class="section-list">
  <div class="section-item">
    <h3>Vega Reports for Discover</h3>
    <p><strong>The first phase of the rollout is complete.</strong> Additional releases of Vega Reports for Discover are continuing, with the goal of ensuring that all current Vega Discover subscribers receive access by the <strong>end of Q2 2026</strong>. Monthly releases will continue with the Vega Suite thereafter.</p>
    <p style="margin-top: 0.5rem;"><strong>Future plans:</strong> Staff Audit data, Programs data, and Mobile data integration. The team is also considering adding Vega LX Starter data.</p>
  </div>
  <div class="section-item">
    <h3>Vega Reports for Polaris</h3>
    <p><strong>Early Access:</strong> Q3 2026. <strong>Delivery:</strong> Q4 with Polaris Release. The team is actively seeking early access partners.</p>
    <p style="margin-top: 0.5rem;"><strong>Focus:</strong> Simply Reports restoration plus eContent and circulation data. OverDrive integration in the same timeline if possible. A survey was sent and received <strong>127 responses</strong> &mdash; strong demand for circulation reports. Will include dashboards and a reporting folder with list reports.</p>
  </div>
  <div class="section-item">
    <h3>Vega Reports for Sierra</h3>
    <p><strong>Early Access:</strong> Q3&ndash;Q4 2026. <strong>Release:</strong> Early 2027. The survey has <strong>not yet been sent</strong> &mdash; Jovana is collecting feedback now and plans to send the survey in the coming weeks.</p>
    <p style="margin-top: 0.5rem;"><strong>Focus:</strong> Web Management reports and Decision Center analysis. Not all Sierra users actively use Web Management reports &mdash; many are focused on Decision Center, which will be incorporated into the platform.</p>
  </div>
</div>

## Key Takeaways for Sierra Libraries

<div class="card">
  <p>What Sierra-specific customers should know about Vega Reports:</p>
  <ul style="margin: 0.75rem 0 0 1.5rem;">
    <li>Vega Reports for Discover requires an active Vega Discover subscription. For Sierra customers, <strong>LX Starter is already included as part of the ILS subscription</strong> and enables the connection needed to access Vega Reports (for those not subscribed to Vega Discover). LX Starter does not need to be actively used &mdash; Clarivate simply recommends having it enabled to support access to Vega Reports.</li>
    <li>Sierra customers are <strong>next in the rollout</strong>, following Discover and Polaris customers.</li>
    <li>Clarivate is <strong>seeking Early Access partners</strong> &mdash; an optional, volunteer opportunity to provide feedback and help shape the product.</li>
    <li><strong>Decision Center data</strong> is planned for future analysis and incorporation.</li>
    <li>A customer survey will be <strong>shared soon</strong>, offering an opportunity to help influence priorities for the Sierra release.</li>
  </ul>
</div>

## Team

<div class="section-list">
  <div class="section-item">
    <h3>Jovana Raskovic</h3>
    <p>Product Manager for Vega Reports, based in the Belgrade office. Almost one year at Clarivate, with over six years of experience in analytics.</p>
  </div>
  <div class="section-item">
    <h3>Jesse Ryan</h3>
    <p>Development Manager for Vega Reports. Leads a small development team building and maintaining the platform.</p>
  </div>
</div>

## Audience Q&A

<div class="section-list">
  <div class="section-item">
    <h3>Export formats</h3>
    <p>Dashboard exports are limited to <strong>PDF or email</strong> only. Custom reports can be exported as <strong>CSV or Excel</strong>.</p>
  </div>
  <div class="section-item">
    <h3>SQL flavor</h3>
    <p>The database backend is <strong>Postgres</strong>. Native SQL queries use standard Postgres syntax.</p>
  </div>
  <div class="section-item">
    <h3>BI tool integrations</h3>
    <p>Direct integrations with external BI tools (e.g., connecting your own Tableau instance) are <strong>not currently available</strong>, but the team is exploring the possibility.</p>
  </div>
  <div class="section-item">
    <h3>Report scheduling</h3>
    <p>Yes &mdash; you can <strong>schedule reports to be delivered to individuals on particular days</strong>.</p>
  </div>
  <div class="section-item">
    <h3>Roll-ups/holds data</h3>
    <p>Not being considered at this time. Jovana: &ldquo;Let&rsquo;s take one step at a time.&rdquo;</p>
  </div>
</div>

## About Pendo

<div class="card">
  <p><a href="https://www.pendo.io/">Pendo</a> is a product analytics and user-engagement platform used by SaaS companies to understand how customers interact with their software. Clarivate uses Pendo to instrument <strong>Vega Discover</strong> &mdash; capturing the usage events that ultimately flow into Vega Reports. Pendo is the <strong>instrumentation layer</strong> in the pipeline; Metabase is the BI layer that surfaces it.</p>
</div>

<div class="section-list">
  <div class="section-item">
    <h3>Company snapshot</h3>
    <p>Founded in 2013, headquartered in Raleigh, North Carolina. Publicly referenced customers include Verizon, Morgan Stanley, Salesforce, Okta, LabCorp, OpenTable, and Zendesk. Pendo competes with Mixpanel, Amplitude, and Heap in the product-analytics space.</p>
  </div>
  <div class="section-item">
    <h3>What Pendo actually does</h3>
    <p>Pendo embeds a tracking snippet into a web or mobile application to capture user behavior &mdash; page views, clicks, search terms, feature usage, and session patterns. Beyond analytics, the platform also offers <strong>in-app guidance</strong> (tooltips, walkthroughs, announcements) and <strong>user feedback</strong> collection (NPS, in-app surveys). For the Vega Reports pipeline, the behavioral-analytics capture is the piece that matters.</p>
  </div>
  <div class="section-item">
    <h3>Where Pendo sits in the Vega Reports pipeline</h3>
    <p>Pendo captures raw Vega Discover usage events. Clarivate pulls those events out via Pendo&rsquo;s API into the <strong>data lakehouse</strong> on a 24-hour cadence. <strong>Metabase</strong> then queries the lakehouse to power the dashboards and custom reports that library staff see inside Vega Reports. Understanding this layering helps explain a few behaviors: the 24-hour refresh is set by the ingest job from Pendo into the lakehouse, and the &ldquo;up to one week of historical backfill&rdquo; on enablement reflects how far back Clarivate can pull existing Pendo events when a library turns Vega Reports on.</p>
  </div>
  <div class="section-item">
    <h3>Simplified data flow</h3>
    <p>Activity in <strong>Vega Discover</strong> &rarr; captured by the <strong>Pendo</strong> snippet &rarr; ingested via Pendo&rsquo;s API into Clarivate&rsquo;s <strong>data lakehouse</strong> (refreshed every 24 hours) &rarr; queried and visualized by <strong>Metabase</strong> &rarr; surfaced to admins and consumers as <strong>Vega Reports</strong>.</p>
  </div>
</div>

## References

<div class="sources">
  <ol>
    <li><a href="https://iii.com/whats-new/smarter-insights-ahead-vega-reports-launching-soon/">Smarter Insights Ahead: Vega Reports Launching Soon</a> &mdash; Innovative Interfaces, April 1, 2026</li>
    <li><a href="https://company.overdrive.com/2025/06/24/clarivate/">OverDrive and Clarivate Integration Announcement</a> &mdash; OverDrive, June 24, 2025</li>
    <li><a href="https://iug2026.sched.com/">IUG 2026 Annual Conference Schedule</a> &mdash; iug2026.sched.com</li>
    <li><a href="https://innovative.libguides.com/Vega">Vega Discover Documentation</a> &mdash; Innovative LibGuides</li>
    <li><a href="https://www.metabase.com/">Metabase</a> &mdash; Open Source Business Intelligence</li>
    <li><a href="https://www.pendo.io/">Pendo</a> &mdash; Product analytics and user-engagement platform (the instrumentation layer behind Vega Reports)</li>
  </ol>
</div>
