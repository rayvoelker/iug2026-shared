# Sierra Year in Review — Tuesday, April 14

**Presenter:** Mike Dicus  
**Time:** 1:30–2:30 PM | **Room:** McHenry | **Track:** Sierra

A walkthrough of features delivered in the Sierra 6.4 (June 2025) and 6.5 (November 2025) releases, with a focus on customer-driven enhancements sourced from MEEP, Idea Exchange, and direct user feedback. More than half of Sierra libraries worldwide are now running either 6.4 or 6.5.

> **See also:** [Sierra Roadmap (Monday)](monday-apr13-sierra-roadmap.md) for the May and November 2026 release plans.

---

## Sierra 6.4 Highlights (June 2025)

### Return Date in Patron History

- Added the **return date** as a new field in patron reading history (field group 38).
- When a patron borrows and returns an item, the return date is now recorded, making the history more complete — patrons can see they had an item last month, last year, or several years ago.

---

## Sierra 6.5 Highlights (November 2025)

### Patron Checkout Limits

The headline feature of 6.5 — originated from MEEP / Idea Exchange requests to extend the category A–D values beyond four options.

- **What it does:** Configures checkout limits by **patron type** combined with a second variable:
  - Patron type + item type
  - Patron type + item location
  - Patron type + library location / location served
- **Configuration:** Found in the Sierra client under *Circulation → Administration → Patron Checkout Limits*, with three tabs:
  - Item type blocks
  - Item location blocks
  - Location served settings
- **Import/export:** Limits can be imported and exported via CSV — critical for libraries needing hundreds or thousands of limit combinations.
- **How it works in loan rules:** Checkout limits are evaluated in precedence order:
  1. Patron blocks (expired card, etc.)
  2. Item location and library location blocks
  3. Item type blocks
  4. All other block types (including patron checkout limits)
- **Staff override:** When a patron hits a limit, staff see a pop-up identifying the specific limit exceeded (e.g., "item type: Picture Book, limit: 3, current: 3"). Staff can override, and overrides are logged in the circulation override logs.

### Print Locations Served Table

- New option in the Sierra client to **print the locations served table** directly.
- Previously, libraries had to contact support to obtain this data. Now available self-service for patron checkout limits configuration or any other purpose.

### Navigate to Patron Record from Item Record

- From any item record (in Acquisitions, Cataloging, or Circulation), staff can now **open the patron record** for the current or last patron.
- Three navigation methods:
  - Double-click on the current/last patron field
  - Edit menu → View actions → Navigate to patron (view or edit mode)
  - Right-click context menu
- Opens the patron record in the checkout screen, ready for action.

### Penalty Points for Unclaimed Holds

- Extended the penalty points / demerits system to support **unclaimed holds**.
- Libraries can assess penalty points when a patron fails to pick up a held item.
- Point values are library-defined; accumulated points can block further transactions for a configurable period.

### Create Lists → Delete Records Navigation

- Continued the navigation enhancement started in 6.3 (Create Lists → Global Update, Rapid Update).
- **New in 6.5:** Jump from Create Lists directly to **Delete Records** with the review file name pre-populated.
- More navigation targets planned for future releases based on Idea Exchange requests.

### Inventory Check-in via Circulation Desk

- Uses the standard check-in screen with a configurable switch in the SDA (system administration).
- **Configuration options per branch / location served:**
  - Start date only (perpetual inventory — never turns off)
  - Start and end dates (time-limited inventory period)
- Updates the **inventory date field** in the item record with each scan.
- Status bar shows "Inventory check-in is enabled" and a running count of items scanned in the session.
- **Popular use case:** Perpetual inventory — leave it on permanently so every item scanned at the desk updates the last-seen date.
- Some libraries have relabeled the inventory date field to "Last Scanned" to reflect this usage.
- **Note:** If you don't have an inventory date field in your item records, open a support ticket to have it enabled.

### Admin Corner → Sierra Client/Admin App Migration

Features moved out of Admin Corner in 6.5:

| Feature | Moved To |
|---------|----------|
| System status (record counts: bib, order, patron, etc.) | Admin App (web-based) |
| Restart terminal | Admin App |
| Scope menu maintenance (scope names and numbers) | Sierra Client |
| Check missing items | Sierra Client |
| Batch check-in (from review files) | Sierra Client / Sierra Web |

**Check Missing Items:** Displays items previously marked missing whose status has since changed (returned, found, checked out). Staff can right-click to view individual item records, sort by column headers, and clear items individually or in bulk.

**Batch Check-in:** Select a review file containing items to be checked in. Bypasses normal check-in logic (transits, holds) — a "quick and dirty" process to clear items from checkout status.

**Scope Menu Maintenance:** Update scope names and numbers directly in the client, eliminating the need for support tickets or Admin Corner access. Builds on the scoping rules maintenance added in an earlier release.

### Create Lists Without Patron Data (New Permission)

- New permission allows staff to use Create Lists **without access to patron data**.
- Operates at the lowest permission level — if a staff member also has a higher Create Lists permission, the higher one takes precedence.
- Staff with only this permission cannot view or create review files containing patron data; attempts trigger an override prompt they cannot fulfill.

### IMMS (Intelligent Materials Management System) Enhancements

For libraries using automated materials handling:

- **Exhibition/display routing:** New settings identify display or exhibition locations. When items are trapped or checked in, the system evaluates whether they should be routed to an active exhibition based on subject criteria and available space.
- **Chaotic hold shelf assignment:** Supports random shelf assignment for holds (no slips in items). Pickup shelf location is displayed in staff screens and patron notifications so staff and patrons can locate held items.

### Other 6.5 Changes

| Enhancement | Details |
|-------------|---------|
| Locations served limit doubled | From 1,000 to **2,000** location codes per entry |
| SQS connection test for notices | Tests connectivity before sending notice data to Alma Starter; prevents data loss if connection fails |
| Accessibility improvements | Name, role, and value attributes set for fields in circulation and search screens (assistive technology support) |
| Client branding update | **Glacier Point** theme: light gray background, updated fonts. **Half Dome** theme: dark version. Switchable via *Settings → Display* tab. |

---

## Library Engagement & Feedback Channels

- **Product Roadmap Portal** — vote on features from "not important" to "critically important" and add comments
- **Idea Exchange** — submit and vote on ideas; past 12 months across all products:
  - 120+ users/day average
  - ~1,200 total users
  - 900 new ideas
  - ~14,000 votes
  - 1,500+ comments
- **MEEP session** — Tuesday at 3:00 PM with Katie LeBlanc and Alex Vancina

### Links from Final Slide

- [Webinars & Recordings](https://www.iii.com/resources/webinars/)
- [Product Roadmap Portal](https://iii.com/roadmap/) *(customer login required)*
- [Idea Exchange](https://ideaexchange.iii.com/)
- Contact: Mike Dicus (email shown on slide)

## Slide Photos

[Google Photos album](https://photos.app.goo.gl/zoPBpkxfebk75eiQ8)

---

*Note: Ray joined this session in progress; the transcript begins mid-presentation during the 6.4 return-date feature discussion. The first portion of the session (likely covering earlier 6.4 features and overall statistics) was not captured.*
