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
- Clarke, Arthur C. [*2001: A Space Odyssey.*](https://en.wikipedia.org/wiki/2001:_A_Space_Odyssey_(novel)) 1968. HAL 9000 — iconic depiction of AI failure.

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
