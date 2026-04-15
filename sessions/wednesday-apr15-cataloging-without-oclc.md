# Kicking the Elephant out of the Room: Cataloging without OCLC — Wednesday, April 15

**Speaker:** Elaine Sloan, Boise Public Library
**Time:** 1:30–2:30 PM | **Room:** Houston | **Track:** General

---

## Key Takeaways

- An 11-library Polaris consortium in Idaho left OCLC (6 figures/year), transitioned through BTCat, and landed on **BookWhere Suite** (WebClarity Software) — total cataloging costs dropped to 5 figures
- **ILL was the biggest hurdle** to leaving OCLC — most consortium libraries solved it by discontinuing ILL entirely after cost analysis showed low usage relative to the cardholder base
- **BookWhere Suite** won the evaluation for best Z39.50 hit rates, familiar client-based interface, and record variety — but lacks BTCat's conditional macro functionality
- **OCLC record ownership** remains a major community flashpoint — speaker called OCLC's proprietary claims over cooperatively-created bibliographic data "bullshit" and expects potential cease-and-desist letters
- Staff transition was the hardest part: 20+ years of OCLC muscle memory doesn't change overnight

---

## Background: Why They Left OCLC

Elaine's consortium of 11 Polaris libraries in Idaho was paying six figures annually to OCLC. The cost was the primary motivation to leave. Their state does not have a statewide library lending service, which simplified the ILL question.

### Solving the ILL Problem

ILL was the biggest hurdle. The consortium libraries performed cost analyses and found that the number of patrons who actually used ILL was a much smaller portion of the cardholder base than expected. Most libraries in the consortium made the controversial decision to **discontinue ILL entirely**.

One library took a creative approach: instead of paying $5+ each way to mail items, they redirected their ILL budget into purchasing items directly — still serving those patrons, just buying the $20 book rather than spending $10+ to borrow it.

The consortium also has **courier routes** between all 11 libraries, so members can still borrow from each other without OCLC. The few libraries that kept ILL service search the online WorldCat database and send requests directly to holding libraries.

Once ILL was off the table, leaving OCLC became much easier.

## Timeline

| Date | Event |
|------|-------|
| June 2025 | OCLC contract ended; switched to **BTCat** (Baker & Taylor) |
| Oct 2025 | Baker & Taylor announced cessation of library services operations |
| Nov 2025 | ~1 month to evaluate alternatives (SkyRiver, BestMARC, BookWhere) |
| Dec 2025 | Went live on **BookWhere Suite** |
| Mar 2026 | Baker & Taylor filed Chapter 11 bankruptcy |

## BTCat: Gone Too Soon

BTCat had incredible **macro functionality with conditional statements** — something no other vendor has replicated. The consortium only used BTCat for about six months before Baker & Taylor shut down. The loss was clearly felt: "All right, baby cat" — an affectionate play on "BTCat."

From the research that Elaine's consortium did, no other vendor offers customizable macros the way BTCat did. It remains the feature they miss the most.

## Evaluating Alternatives

With roughly one month to decide, the consortium evaluated three products:

### BestMARC (Mitinet Library Services)

A web-based product. The consortium administrator preferred this option, but when staff tested it, they "kind of hated it" — they found it clunky, hard to use, and the hit rate wasn't great. Most staff were still accustomed to client-based interfaces (Connexion, BTCat), so the web-based approach didn't resonate.

### SkyRiver (Innovative/Clarivate)

SkyRiver hadn't been actively selling until BTCat announced discontinuation. Its interface looks and acts like Connexion client, which was a point in its favor. However, several issues emerged:

- **Record quality** was not sufficient — both this consortium and an audience commenter confirmed
- Gets records from only two main sources: Library of Congress and INN-Reach libraries
- The INN-Reach pool is **shrinking** as those libraries move to Rapido, though SkyRiver still has MelCat, which is "huge"
- **No Z39.50 searching** option
- Missing **call numbers** in records (audience commenter)
- Lacked **world language titles**, video games, board games, and other non-traditional formats
- The consortium concluded SkyRiver would likely shrink rather than grow

### Why BookWhere Won

BookWhere Suite had the **best hit rate** of anything tested — the speaker thinks it's actually better than BTCat. Its client-based interface was familiar to staff who were already using Polaris client rather than Leap. And with Z39.50 access to thousands of libraries, it offered far more variety of records than SkyRiver's limited pool.

## BookWhere Suite in Practice

### Searching and Database Groups

BookWhere connects to approximately 2,400 libraries over Z39.50 (the vendor advertises 3,000+ targets in their current marketing). Searching all 2,400 at once is impractical — too many hits, too slow. Instead, the consortium created curated **database groups**:

- **"Links Recommended"** — ~20 libraries known for good records (shoutouts to SILS, CLC, and particularly Allen County)
- **World language groups** — targeting libraries with strong non-English collections
- **Format-specific groups** — for board games, library of things, and other non-traditional items

The search interface "looks like it's from the 1990s" — not pretty, but it works. You can search by virtually any MARC field, which is both extensive and daunting.

### Record Scoring

BookWhere ranks search results by **RDA score** and **MARC 21 score**, displayed as colored boxes alongside a numerical ranking. The consortium guideline is to choose records scoring 50 or above when possible. This was similar to BTCat's ranking system, which eased the staff transition.

### Macros: The Biggest Pain Point

BookWhere Suite **does have macros**, but they **lack conditional statements** — the key feature that made BTCat's macros special. BookWhere macros are basic "remove this" / "add this" operations, with notable limitations:

- Must repeat remove commands multiple times (e.g., "remove 856" entered four times to catch all instances)
- Adding/removing fields sometimes strips preceding or following punctuation unexpectedly
- A **"clean record mapper"** macro runs automatically when records are sent to the MARC editor, removing unwanted fields

Coming from BTCat's conditional macros, this was the most painful part of the transition.

### The MARC Notepad Editor

The built-in editor is "as utilitarian as it gets." It works, but editing leader fields is a nightmare — there are no positional guides, so it's very easy to get a space in the wrong place and throw everything off. The recommendation is to **export records into Polaris** for leader editing, where the positional guides make it much clearer.

On the plus side, you can open multiple records simultaneously in the editor, drag-and-drop fields between them, and do comparison work. This is particularly useful for copy catalogers piecing together records.

### Configuration and Administration

Configuration is stored in **XML files** that can be distributed to workstations — staff drops them into a folder. It's not as seamless as web-based administration, but at least each user doesn't have to change individual settings. Managing this across ~50 workstations in a consortium is painful but workable.

Licensing requires a per-PC key that must be deactivated and reactivated when hardware is replaced. Individual licenses run in the hundreds of dollars; site licenses in the thousands. The total consortium cost dropped from six figures (OCLC) to five figures — significant savings.

### BookWhere Online: A Warning

BookWhere Online (the web version) is a **completely different product** from the Suite — less functionality, no macros, different interface. The speaker was emphatic: **"the online version is truly awful."** Crowdsourced advice from catalogers on Facebook confirmed this. If you're evaluating BookWhere, look at the Suite first.

### Legal Position

BookWhere has not been sued by OCLC despite being in business for 25+ years. Their strategy, whether intentional or not, is legally sound: they **save nothing and have no record repository**. They only facilitate Z39.50 connections between libraries. BTCat, by contrast, had its own "community records" database, which contributed to OCLC's case against them. BookWhere's position: "there's nothing to sue."

## OCLC Record Quality

The speaker noted that OCLC record quality has gone down, particularly in the last five years. Because of this, the additional vetting required when using BookWhere isn't as dramatic a change as it would have been a decade ago.

One practical issue: records retrieved via Z39.50 include more localized fields that OCLC and BTCat used to strip out automatically. The consortium had to beef up their Polaris import profiles to handle fields they "never would have expected to come in."

## Original Cataloging without OCLC

The speaker does original cataloging in BookWhere's MARC Notepad editor, piecing records together. Others in the consortium do it directly in Polaris.

The downside is clear: original records stay local. You can't share them back to WorldCat the way you could with Connexion. "That was a bummer for me for leaving OCLC," the speaker acknowledged.

The upside: anyone with your Z39.50 connection open can access your records. "Bibliographic data is not proprietary and should be shared," the speaker said — a philosophy that informs their willingness to leave their Z39.50 server open for other libraries.

## The OCLC Ownership Flashpoint

This was the most heated part of the session.

When using BTCat, the consortium ran a macro to **remove 035 fields containing OCLC numbers** before importing records. After switching to BookWhere, they didn't remove existing OCLC numbers from their catalog — "maybe we should have."

The speaker asked **Marshall Breeding on Monday** (at the conference) about this. His assessment: even removing OCLC numbers wouldn't matter because the records are still "marked as proprietary."

The speaker's response, on the record: **"I think it's bullshit."**

She expects the consortium may receive a cease-and-desist at some point, and expressed concern that individual libraries don't have the resources to fight OCLC in court. OCLC has already prevailed against BTCat and MetaDoor.

Her position: "For people that have stopped using OCLC, those records really don't belong to them. We should still be able to share them, no matter what OCLC says."

An audience member suggested starting an alternative: **"NOclc"** — which got a good laugh.

## Q&A and Audience Discussion

### Staff Impact
**Q: What was the biggest pain point for staff?**

Loss of familiarity. Staff had been on OCLC for 20+ years and had never used anything else. The other hurdle was retraining staff to evaluate bibliographic record content holistically — many had relied on the presence of an OCLC number as a proxy for quality, which "obviously wasn't always the case."

Staff time has gone up overall. It increased when they moved to BTCat (new system) and again when they moved to BookWhere (different system + more careful record evaluation). However, staff actually settled into BookWhere faster than BTCat, likely because the client-based interface felt familiar.

### Import Profiles
**Q: Can you set up an import profile in BookWhere?**

Not exactly. The macros only do basic add/remove operations, and you have to enter remove commands multiple times per field. It's not a true import profile in the OCLC sense.

### E-book Records
**Q (academic library): How do you handle Collection Manager for e-book/database records?**

The speaker's library uses Collection Manager for their O'Reilly database — it's part of the O'Reilly subscription, separate from OCLC, so it still works. "OCLC doesn't love it because they're losing part of your subscription, but it is possible."

### Authority Records
**Q: How do you handle authority records?**

The consortium uses **Backstage Library Works** and has for years — that didn't change when they left OCLC. "If any of you need authority work, check out Backstage. They're the best."

### Z39.50 Connection Issues
**Q: Any issues with connections going down?**

Occasional individual library connections go down, but with thousands of alternatives, it's never been a real issue. However, setting up client-to-client connections across a consortium can be an **IT nightmare** — non-standard ports, firewall rules that need to be configured per library. The speaker's assistant administrator Brad managed this across the 11 organizations.

### MarcEdit
The consortium looked at MarcEdit but decided it was too complicated for copy catalogers, especially given their tight evaluation timeframe. An audience member noted that Polaris's built-in Z39.50 client is another option, but the speaker didn't like that records save immediately to the system with no staging area.

### BookWhere as Cataloging Service
**Q: Does BookWhere contract with a vendor for cataloging services?**

No. BookWhere is purely a connection service — "they don't offer full cataloging. They are just a connection service."

### Amazon Records
Audience discussion: Amazon vendor records "have gotten progressively better, and they've gotten better faster than I ever expected." But the consensus was they're still poor quality — an audience member's description was more colorful.

### OCLC Frustration
An academic library commenter expressed significant frustration with OCLC: turnaround time on paperwork is "abysmal" (5+ weeks), their county council red-lined OCLC contract terms, and OCLC refused to negotiate. The commenter questioned why they even maintain a contract.

---

## Appendix: Background Research

*Additional context gathered during the session to supplement the speaker's presentation.*

### BookWhere Suite (WebClarity Software)
- Windows-only Z39.50 copy cataloging client, current version 7.5.2 (Oct 2024)
- 3,000+ Z39.50 targets (LOC, British Library, national libraries, etc.) — libraries report 97%+ hit rates
- Per-PC perpetual license, no per-record fees; annual maintenance covers upgrades
- ~6,000–8,000 copies in use worldwide, 1,000+ libraries in 40 countries
- Notable users: 600+ Finnish academic libraries, Ontario public libraries, Nova Scotia Provincial Library
- Canadian company (WebClarity Software / Convergent Library Technologies); originally developed by Sea Change Corporation in the mid-1990s

### BestMARC (Mitinet Library Services)
- Cloud-based MARC record management — searches Z39.50 databases, auto-ranks results by quality
- Three tiers: Essential, Plus, Global (pricing requires contacting Mitinet)
- ~5,263 libraries; won LibraryWorks Modern Library Award 4 consecutive years (2019–2022)

### SkyRiver (Innovative/Clarivate)
- Launched 2009 as cheaper OCLC alternative — flat-rate pricing, claimed 40% savings
- Filed antitrust lawsuit against OCLC (2010); lawsuit withdrawn 2013 when absorbed into Innovative Interfaces
- Database: ~60M+ records (43M was circa 2013); still much smaller than OCLC's 500M+
- Still available as an III/Clarivate product; lacked OCLC's ILL network
- Academic study (Blackman & Seikel, LRTS) confirmed "meaningful differences in non-English-language records" vs WorldCat

### Backstage Library Works (BSLW)
- Provo, Utah company, operating since 1986; still fully active
- Flagship product: **MARS** (MARC Record Service) — acquired from OCLC in 2004
- Compares name/subject headings against LC and other authority files, standardizes access points, adds cross-references
- First vendor to offer RDA-compatible authority control; most customizable RDA services on the market
- Notable clients: Stanford, UCLA, University of Hawaii, New York Historical Society
- New 2026 partnership with Ingram for shelf-ready services

### MarcEdit
- Free, open metadata editing suite created by Terry Reese (1999, Oregon State University); still actively maintained
- Runs on Windows, Linux, macOS; has native Z39.50/SRU client
- Integrates with OCLC Connexion via plugin — complementary, not competing
- Widely regarded as indispensable; Library Carpentry has a full curriculum built around it

### OCLC Record Ownership — Legal Landscape
- OCLC claims copyright over WorldCat *as a compilation*, not individual records
- Under *Feist v. Rural Telephone* (1991), bare facts cannot be copyrighted — individual MARC records are standardized factual data and likely uncopyrightable
- OCLC enforces control through **contracts and membership agreements**, not copyright law
- MetaDoor settlement (2022): OCLC sued Clarivate/Ex Libris over a planned MARC record exchange; Clarivate settled, shut down MetaDoor
- BTCat lawsuit (2025): OCLC alleged B&T used a third party to access WorldCat, exceeded license terms, built BTCat from extracted data
- OCLC has sent cease-and-desist letters to individual consortia (e.g., FALSC in Florida)

### OCLC Alternatives Landscape (2025–2026)
- OCLC has used litigation to eliminate competitors: **BTCat** (2025 injunction + B&T bankruptcy) and **MetaDoor** (2022 settlement)
- ILL remains the biggest lock-in — OCLC owns WorldShare ILL, Tipasa, ILLiad; **Relais** is the main non-OCLC option
- Open-source options: Koha and Evergreen support Z39.50 copy cataloging; BiblioteQ is standalone
- Growing community frustration — OCLC seen as gatekeeper over collectively-created metadata
- OCLC laid off ~80 staff in July 2025, citing AI
