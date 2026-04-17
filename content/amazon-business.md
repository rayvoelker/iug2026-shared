---
title: "Amazon Business EDI Integration"
template: session
day: monday
date: "April 13"
speakers_display: "Opening Session Deep Dive"
description: "Amazon Business EDI integration with Sierra — Cincinnati Public Library as early adopter, implementation strategy and best practices for acquisitions workflows."
---

<div class="card">
  <h3>Presenters</h3>
  <p><strong>Holbrook Sample</strong> &mdash; CTLO, Public Library of Cincinnati and Hamilton County (CHPL)</p>
  <p><strong>Moses Lai</strong> &mdash; Sr. Technical Product Manager, Amazon</p>
</div>

## The Integration

<div class="section-list">
  <div class="section-item">
    <h3>How It Works</h3>
    <p>Order books from Amazon Business, download brief MARC records with order info, load into the ILS. EDI is the backbone.</p>
    <p>Amazon's "grid" technology lets libraries add structured metadata &mdash; fund codes, locations, processing instructions &mdash; to orders before they flow into EDI.</p>
  </div>
  <div class="section-item">
    <h3>Sierra Side</h3>
    <p><strong>Sierra acquisitions API is being developed</strong> on the III side to support this integration.</p>
  </div>
  <div class="section-item">
    <h3>Amazon's Library Focus</h3>
    <p>Amazon has had procurement tools broadly, but has been <strong>focused on libraries for less than 1 year</strong>.</p>
    <p>MARC record quality has been improved. More features coming. Looking for additional partnerships.</p>
    <p>Positions Amazon as a <strong>primary materials vendor</strong> (competing with B&amp;T), not just a la carte.</p>
    <p><strong>Patron-driven acquisitions</strong> mentioned as a future possibility.</p>
  </div>
</div>

## CHPL Implementation

<div class="section-list">
  <div class="section-item">
    <h3>Getting Started</h3>
    <p>Acquisitions/selection experts on CHPL staff. Early meetings included cataloging, processing, fiscal office, MSA, and cataloging teams.</p>
    <p>Outsource MARC records (brief records from Amazon supplemented).</p>
  </div>
  <div class="section-item">
    <h3>Launch</h3>
    <p><strong>Launched mid-April 2026.</strong></p>
    <p>Half the budget goes to physical materials. Purchase order driven workflow. EDI enforces the structure &mdash; the more methodical the work, the better.</p>
  </div>
  <div class="section-item">
    <h3>Current State</h3>
    <p>Selectors still use Library Hub for pre-pub work. Currently working out fund mapping between Amazon and ILS.</p>
    <p>Aligning Amazon Business tools with existing workflows was essential.</p>
  </div>
</div>

## Key Points from Markdown Notes

- **EDI was the biggest request** from libraries — operational improvements over credit card purchasing
- Validated features with librarians throughout development

## Implementation Advice

<div class="card">
  <ul style="padding-left: 1.25rem; margin: 0;">
    <li>Get acquisitions, cataloging, processing, AND fiscal office involved from the start</li>
    <li>Know up front how to route materials to different locations/branches</li>
    <li>Have a short list of goals defined before you begin</li>
    <li>Get solid MARC records up front to focus on change control</li>
    <li>Define all important features before implementation</li>
    <li>Align vendor tools to your workflows, not the other way around</li>
    <li>EDI-driven workflow is more structured and reliable than credit card purchasing</li>
  </ul>
</div>

## Source

<div class="sources">
  <ol>
    <li><a href="https://iii.com/whats-new/innovative-from-clarivate-collaborates-with-amazon-business-to-enable-edi-ordering-integration-for-sierra-libraries/">Innovative from Clarivate Collaborates with Amazon Business</a> &mdash; iii.com</li>
  </ol>
</div>
