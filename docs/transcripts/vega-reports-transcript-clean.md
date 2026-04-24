# Vega Reports for Discover and Beyond - Cleaned Transcript

**Session:** Vega Reports for Discover and Beyond
**Presenter:** Jovana Raskovic, Product Manager, Clarivate/Innovative (Belgrade office)
**Date:** Tuesday, April 14, 2026 - IUG 2026, Chicago Ballroom G
**Source:** Automatic speech-to-text transcript, cleaned and structured
**Raw transcript:** `vega-reports-raw.txt`

> **Note:** This transcript was generated from automatic speech recognition and
> manually cleaned for readability. Speaker-to-text errors are corrected where
> intent is clear (e.g., "bigger reports" -> "Vega Reports," "pilates" -> "Polaris,"
> "belgian" -> "Belgrade," "alex starter" -> "Vega LX Starter"). Some passages
> remain approximate.

---

## Introduction and Personal Background

**Jovana:** Happy to see you in this number today. So I'm just gonna try and move around the room as much as this mic allows me. So we're here obviously today to talk a little bit about Vega Reports for Discover, and beyond that. I'm gonna introduce myself first -- for some of you, you've met me already over some of the calls and things like that, and we've been meeting in the corridor. But my name is Jovana. I'm coming from Serbia, and I'm based in the Belgrade office. So if anyone wants to know, it's a long time -- it was a very enjoyable, nice experience, I would say. We didn't have any layover, luckily, but it's like a full-on 11 hours.

I've been with Clarivate for a year -- well, a little bit less than a year. It's going to be a year in like 20 days. Not that I'm counting.

And I'm working with analytics for, I'd say, a little bit more than six years. I've been working with different business areas, so I'm really adaptable to different areas within the businesses.

And I wanted to share with you a little something. It's on a personal note, and you're probably gonna start wondering "what does that have to do with reports?" But I promise, it resonates a little bit.

I used to play flute for 11 years, and one of my dreams was playing with a philharmonic orchestra -- I'm gonna travel the world, play the flute, and be amazing at it. That obviously didn't happen. But how does it resonate? When you're really playing -- whoever played anything in their life, or was really musically focused or artsy -- you have a lot of notes that you need to go through, and you need to practice, and you need to figure out the way to compile them all together, right? It's absolutely the same with data, just different views on it. You don't get music, but you get your customers. So it kind of resonates, right?

---

## Strategy Overview

**Jovana:** So without further ado, I'm going to be presenting you today with Reports for Discover, and overall our strategy. Let's say that I don't really like data, I don't want to deal with data, but I want to get a hold of my reports -- this is exactly what I will be showing you today.

For me, data is something that I use every day, regardless of the work side. Even when I'm booking my vacation, I will investigate the destination -- I'm going to pull all the hotels, all the prices, I'm going to do a full-on comparison of what's included and what's not included, and it's going to help me navigate toward the hotel that I want to go to, right?

So our strategy is basically to try and provide you more with less doing. And one of the key pillars, I would say, is our **data lakehouse**. You must be hearing this coming from different presentations -- data lakehouse, data lakehouse. We really love that term. We're very proud of it. That's our infrastructure.

So what does the data lakehouse mean, and what are you getting from it? Consider it as a bucket that all of the different data points can be brought to. So we're talking today about Discover data in specific, but we are going to cover a little bit about Polaris and Sierra as well. To that bucket you can get really any data point.

- It requires a **single login** -- you will be signing into the data
- It has the **automated and intelligent** insights -- we will talk a little bit about the AI tools
- Your **data is protected** -- whether your library is based in Europe or in the U.S., really anywhere in the world, your data is secure
- **Unique insights** -- it does allow us to bring third-party data as well

---

## Early Access Acknowledgment

**Jovana:** Before I move to Vega Reports for Discover, I just really want to extend my gratitude to our early access customers, which is **STELLA**, **Mid-Hudson**, and **Phoenix**. Thank you, thank you, thank you very much for providing us valuable feedback. We've been collaborating over the last couple of weeks together to enable the first rollout and getting regular reports. We will continue to do so, and based on that, we will continue to enhance with future releases.

We do have a demo available in our sales booth, but I really want to give you a snapshot of what you're going to see and what you can experience.

---

## Setup and Access

**Jovana:** As I mentioned, it does require an active subscription to Vega Discover. There are two roles that you can assign from the User Management within Discover: **Reports Admin** and **Reports Consumer**.

The hierarchy -- basically you can assign any role to a **main site**, a **collection site**, or a **kiosk site** level. It really depends on your preference.

Also, I would like to mention -- the Admin will have two varieties of access. If you're a main site admin for Reports, you will be able to either do a **SQL query** or you can build your own reports by using the **Query Builder**. So it doesn't really limit you -- if you're not a SQL-savvy person, that's okay, we hear you. We do have a Query Builder there that can help you resolve any reporting issue and help you build around it.

The **Consumer** will be an individual within your library who will consume the reports you create. It's kind of a **view-only license** within the reports.

I also wanted to mention that Vega Reports is powered by **Metabase**. Metabase is basically a business intelligence tool, same as your Tableau or your Power BI, or really any BI tool. With this, we're giving you the full license to it, and it's included in your subscription, so there's **no additional cost**. The reason why we chose it is because we found it useful for both case scenarios -- whether you want to create custom reports using SQL or just using Query Builder.

This is just a snapshot of how you can assign a role to your staff member. It's from the User Management -- you'll select the edit icon next to it, and you can pick Reports Consumer or Reports Admin at any site level. And once you save that, it will show in your left-hand side navigation menu.

---

## Dashboard Overview

**Jovana:** So let's talk a little bit about the dashboard.

Dashboards provide your insights to your analytics in terms of Vega Discover usage -- what are your patrons and your staff basically doing on Discover. It's supported by **Pendo** -- Pendo is a tool that really collects your data. And I'm going to mention again the fancy word "data lakehouse" -- we are bringing everything from Pendo by calling their API to Vega Reports.

There are **three sets of statistics** that are built within the dashboard, and the dashboard itself **cannot be edited** -- that is what you get regardless of your role, whether you're a Consumer or an Admin. But you can create or use the models from that dashboard to create your own reports:

1. **Visitor Statistics** -- your users' activity across Discover
2. **Search Statistics** -- your top searches, performance, and weekly trends
3. **Marketing Statistics** -- focused on home page interactions; who comes on the home page, where are they clicking, and what they're actually doing; which elements are taking the least and most attention

We do have some cool capabilities -- you can **share by email or PDF**, you can **bookmark** it for easier access. In the future, once we start releasing many more reports, you can just easily bookmark it -- it's handy on your left-hand side menu. And **filters** -- from the moment you get Vega Reports for Discover, we will back-populate that data for about a week. But then as you start using it, data will just accrue and stay there. So over the course of time, you will be able to see your weekly or monthly trends, and definitely year-on-year.

Within the **site filter** -- this is quite handy, I think, for consortia, and also for other libraries -- you're including all the collection sites, kiosk sites, or the main site. You can really select whichever site you want to see the data for. It's based on the site URL, so you might want to tweak it a little bit to find it more convenient for your library, but the data is there.

---

## Q&A: Export and SQL Flavor

**Audience Member:** Can I share by email or PDF? Does it do Excel?

**Jovana:** Good question. We have exports by Excel, but not for the dashboard, because the dashboard is already set. The best way to download the dashboard is either PDF or shared by email. But if you create your own reports, you can download them in a CSV or an Excel file.

**Audience Member:** What flavor of SQL is it using if you're writing your own queries?

**Jovana:** It's using **Postgres**.

**Audience Member:** [Follow-up about connecting external BI tools]

**Jovana:** That's a good question. So for now, no, but we're exploring the capabilities. It's something that we really want to establish. This kind of infrastructure -- the data lakehouse -- allows us to do anything you would like to do with your data, and that's something that we are thinking about. We're not planning, but let's say we are brainstorming now how we can respond to that requirement. I know that many of you are using your own tools -- I met a couple of customers today who are using Tableau very heavily. And as a previous very heavy Tableau user, I must tell you that Metabase is easier to use.

---

## Dashboard Cards and Definitions

**Jovana:** This is what I was referring to when I was saying it's really easier to download a PDF or share by email rather than doing it in CSV. So the dashboard is preset -- it's set in stone -- and you can download it and you can go every day and check the data.

Each of these cards is presenting a reporting card, and behind it there is a calculation -- a SQL query basically pulls the data in. But for instance, if you see it for the first time, you will be like "Okay, so what does Number of Interactions mean? What is Unique Visitors? How did they get to Visitor Frequencies? What is Medium, High, Low?"

So we have included -- you see the information icon -- if you hover over your mouse, you will be able to see each description:
- **Unique Visitors** = distinct count of users
- **Number of Interactions** = a click, really any interaction on the page
- **Visitor Frequencies** = how often a visitor visited Vega Discover (with explanations for Medium, High, and Low thresholds)

---

## Query Builder and Data Models

**Jovana:** So I mentioned at the beginning that you really have two varieties of creating your own reports. This is a snapshot of how the Query Builder looks like -- this is for those individuals who don't really want to interact with SQL in any way.

In the data itself, we have something called **data models** and **data tables**. Please don't be frightened with all the expressions -- they're all in the documentation.

**Data models** basically include the same data as data tables. We created models for the purpose of **controlling data for your collection admins**. So if you have assigned a Reports Admin for a collection site, we had to create models so that once they select that site, they can only see data for that particular site. Main site admins obviously can see everything.

The data: first, you pick your table or event. You can **join data**. Within the documentation included in the last release, you will find something I named a **"unique identifier"** -- it can help you look for the field or attribute that you have to match against to get the result you want.

You can **filter** by different time frames -- we're usually using "last time," which turns out to be the most convenient because we're comparing data from Vega Discover. But you can also do a difference between first and last time.

**Summarize** -- it's your aggregations. Whether it's a count of rows, or an average, or a sum -- it has many options. And you can group by any field within that model or table.

For those who would like to use SQL -- here is an example. It's using **Postgres**. I've used it a couple of times, but I maybe prefer using the Query Builder because I really get to play with it and see what Metabase is trying to show me.

**Important access distinction:** If you're a **main site admin** and you're querying data with the Query Builder, on your right-hand side you're going to see the full SQL query. But if you are a **collection site admin** for Reports, you're just going to see the Query Builder [no SQL access].

---

## Visualizations

**Jovana:** Vega Reports has a tendency to show you the best possible visualization based on your query, whether it's from the Query Builder or SQL. But you can change that -- you can change the colors, you can change the naming conventions of the table or the axis. You see the visualization options at the bottom and in the left-hand side -- whether you would like a bar, a line, or a pie chart, really any. And if you hover over those, there is a settings toggle -- if you click on it, just explore. It's a wonderful word. You can really do anything with it.

---

## Q&A: Rollout Timeline and Scheduling

**Audience Member:** [Question about rollout timeline]

**Jovana:** We initially are focusing on Q2 to get all the customers that have implemented Vega Discover -- so they are currently using Vega Discover. Within May, we will focus on the ones that are in implementation. And after that, we're going to focus on the Polaris and Sierra customers. Polaris will be going first, and Sierra will come right after that.

Also, Polaris and Sierra users -- they have their Vega LX Starter subscription. That helps us because we really need to have something called an ID within our system to be able to expose Reports. But it's not essential -- **you don't have to have Discover in order to get the Reports**.

**Audience Member:** Can you schedule reports?

**Jovana:** Yes, you can schedule reports to be sent to individuals within your library to receive on particular days. Yes, you can do that.

---

## OverDrive Integration Demo

**Jovana:** We have also prepared a demo at the sales booth, and what we're very excited about -- we are working on integrating with **OverDrive checkouts data**. Whether you're a Polaris or a Sierra user, we will be integrating with their checkouts in order to answer some of the questions on the screen.

On the demo slide, we wanted to show:
- What is the **unique number of patrons** that have been checking out digital copies?
- What is the **number of checkouts**?
- What is the **average lending period**?

How can this really benefit libraries? If you see a number of digital checkouts in your library, you'll say "Okay, let me see what are the print copies that have been checked out -- or are they?" If they're not being checked out, that would be maybe something to consider -- removing that collection, replacing it with something that is circulating more.

There's a **"print copy checked out" flag/filter** -- yes or no -- so whether a print copy has been checked out within the checkout time frame that you select. And we also have owning branch and checkout branch.

---

## Q&A: OverDrive Matching and Holds

**Audience Member:** How do you match the digital record with the print record? We've had a lot of trouble with that in discovery.

**Jovana:** I've been asking the same question myself. There are a couple of ways that we are trying to do it. You probably know that on the OverDrive Marketplace, you can download all of your checkouts and try to map it. What we will try to do is to **map it in the backend with the patron ID** without really exposing it widely, or we're going to try and find a product ID that resonates with the title. This is a little bit harder because every title is different, but we're working on that in the best possible way.

**Audience Member:** As a follow-up to that -- if you're working on it for the reports, will that potentially work with the roll-ups as well?

**Jovana:** Maybe. Good idea. For now, we didn't consider any roll-ups. And also getting holds as well -- but yes, we're a little bit far from that. I'm saying always with reports, let's take one step at a time. It's something that we're doing for the first time in this environment, and that's also why we're doing it gradually -- we really want to be able to optimize it based on the feedback.

So any data ingestion -- now we're doing Discover. We are then adding ILS data. And based on the feedback and the performance of the tool, we can easily optimize it to customer needs.

---

## Roadmap

**Jovana:** Let me talk a little bit about what's coming next in terms of the roadmap.

### Vega Reports for Discover
- We're going to finish the release in the next couple of months -- **Q2 is the aim**
- You might be wondering if you're going to get any other Vega products (like for Vega LX Starter)
- We're working on that for 2026, and in the second half of 2027 we outlined a plan focusing on ILS, but we're definitely considering adding Vega LX as well

### Vega Reports for Polaris
- **Early access in Q3** -- we're seeking partners. I do have some lists of those who'd like to be early access partners, but please feel free to come and volunteer
- Focus on **Simply Reports and eContent data** specifically
- I had sent out a survey a couple of months back, and the **response rate was 127** -- which means you've been forwarding it to other people, which is great
- What that told me: **you really want circulation reports**
- My plan: get those circulation reports tested, and if we manage to integrate OverDrive in that same timeline, wrap those in. If not, we'll have circulation reports first
- In terms of dashboard: you'll have your Polaris dashboard, and in your collection or reporting folder, you'll have list reports based on circulations
- We'll roll out and keep adding more and more

### Vega Reports for Sierra
- **Early access in Q3-Q4**
- **Sierra folks didn't get the survey yet** -- I'm working on collecting your feedback, and based on that I will be sending out a survey on reports
- My understanding is that not everybody really uses Web Management Reports -- they might be using it for some downloads, but you're really focused on the **Decision Center**
- What I'll be working on in the next couple of weeks is compiling that survey and sending it out to you

---

## Metabot AI Demo

**Jovana:** Everyone's favorite -- AI. That was a little bit of sarcasm in my voice. The reason is I've heard different opinions about AI -- somebody really likes it, somebody is running away from it. This is the future -- you just can't run away from it. As long as you run away from something, it's gonna get you sooner rather than later.

In reports, I think it's fairly good because it's going to enable you to not really think about it that much -- it can help you create reports without really doing anything, just clicking.

We don't have a live demo here, but I do have a screenshot, and I did manage to make my way around it a little bit, so I can show you a video of how it will look.

It's called **Metabot**. We said at the beginning that Vega Reports is powered by Metabase -- Metabot is one of their AI tools. It's **currently not supporting the self-hosted environment**, which we're in. So we're working on getting that, and **this is only a proof of concept** -- we're not really doing anything with it right now. Your ideas are welcome -- if you feel it's good or not so good, feel free to share.

You can see the **AI Exploration** button in the corner. Once you click on it, it will give you a full view and ask you "What can I help you with today?" It's similar to ChatGPT or really any AI tool.

[Showing video]

**Jovana:** My name is Jovana, but I know that you're gonna laugh, so I just put my name in there. So you see -- I found this video and I'm going to show you what it looks like.

On the chat with the AI -- let's forget about this one, I was just testing it -- I'm asking it a question. Folks in the back, can you see it? So with sample data, which is really demo data, I asked it to show me how I can create a report using the Query Builder. So it's now leading me through each step -- the same as what I was showing you on the Query Builder. So you can actually see how to create your own reports as well.

It gives you different options -- a couple of rows, some aggregations, check-out date, branch name. When I click on "Visualize," it shows the visualization -- obviously in table mode, but it's telling you to choose your visualization if you'd like to. You can see bar, chart, pie chart. Follow the steps, save it, change the name, save it to your analytics. Every person that gets Metabase access can save it to their **personal collection** -- that's the place if you don't want to share it with anyone. It's your personal playground.

What I did next -- I asked it to do the report for me from A to Z. First, I asked it to summarize the main stats, but I didn't really like it, so I said "Can you break that down even further?" See it in the blue -- it already saved the model. The report I've been asking for is already saved there, and if you click on it, it will lead you to it.

It can save to your own folder. It's asking me "Do you want me to do all of this? Circulation by format, by checkout date, popular titles, trends over time, lending period?" And I'm like "Okay, let's try it." That's good -- you're taking my job, but that's fine.

I opened one of the models it created for me, and I can see the SQL for it. I'm asking "Can you show me the SQL for this model?" -- in case I want to use the SQL for something else, I can save it. I did one more thing: everything it was doing, it wasn't showing me the SQL. So I asked "Can you help me generate the SQL query to show checkouts by title?" And it just writes it for you -- you don't have to write anything.

I'm going to pause it here because there's another two or three minutes.

How do you like it? [Audience responds positively]

---

## Closing Remarks

**Jovana:** Before we wrap it up, I just want to extend my thanks to one of my -- I would say -- partners in crime in reports, and that's **Jesse Ryan**. He's right there. He is a **development manager** for Vega Reports. He has a small development team, and we've been working together since I joined -- so for 11 months he had to put up with me, and he has to keep putting up with me for the next... I don't know how long. But it turns out we were great together. Thank you, Jesse, one more time for making this happen.

That really brings me to the end of the presentation. I just want to remind everyone of the opening slide -- what Vega Reports really gives you:

- **Streamlined staff flows**
- **Automated and intelligent** -- we just saw that coming
- **Secure and private**
- **Unique insights**
- And most importantly, it is **consortia and international ready** -- we are rolling it out to European customers, U.S. customers, really any customer

Thank you very much. I will stay here for any questions. I will definitely share my email -- the reason why I didn't include it on the slides is because my last name changed, so my email has a different last name. I will be sharing it with you. Thank you.

---

## Q&A Summary

| Topic | Question | Jovana's Answer |
|-------|----------|-----------------|
| **Export formats** | Can you export to Excel? | Dashboard exports are PDF/email only. Custom reports you create can be exported as CSV or Excel. |
| **SQL flavor** | What SQL dialect does it use? | PostgreSQL. |
| **External BI tools** | Can you connect your own BI tools (e.g., Tableau)? | Not currently, but they are brainstorming/exploring this capability. The data lakehouse infrastructure would allow it. |
| **Rollout timeline** | When will non-Discover customers get it? | Q2 for all current Discover customers; May for those in implementation; Polaris next, then Sierra. You don't need Discover to eventually get Reports -- Vega LX Starter is sufficient. |
| **Scheduling** | Can you schedule reports? | Yes, you can schedule reports to be delivered to individuals on particular days. |
| **OverDrive matching** | How do you match digital records with print records? | They plan to match via patron ID in the backend, or find a product ID that maps to the title. Still in development. |
| **Roll-ups and holds** | Will OverDrive integration work with roll-ups? And holds? | Not currently considered, but noted as a good idea. They're taking a step-at-a-time approach. |
| **Sierra survey** | Has the Sierra feedback survey been sent? | Not yet. Jovana is compiling it and will send it out in the coming weeks. |
| **Metabot AI** | Is the AI available now? | No -- Metabot does not yet support self-hosted environments. This is proof of concept only. |
