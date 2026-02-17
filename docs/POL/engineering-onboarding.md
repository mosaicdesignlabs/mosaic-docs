---
doc_uid: "MOS-ENG-POL-001"
title: "Engineering Onboarding Guide"
org: "MOS"
category: "POL"
department: "ENG"
notion:
  database: "Documents"
  publish: true
access_groups:
  - "All-Hands"
lifecycle:
  desired_state: "draft"
---

# Mosaic Design Labs — Engineering Onboarding Guide

*Everything you need to be productive from day one.*

---

## Welcome

Welcome to Mosaic. We're a small, multidisciplinary R&D studio in Berkeley building biomedical instruments, diagnostic devices, and embedded systems. We're selective about the people we bring on and the projects we take on—so if you're reading this, we're glad you're here.

This guide covers how we operate day to day: our tools, our processes, where to find things, and the reasoning behind our choices. Read it through once, then use it as a reference. If something is unclear or out of date, tell us—this is a living document.

The companion document, *How to Be an Engineer*, covers our engineering philosophy and the mindset we cultivate here. Read that too.

---

## Where Everything Lives

Almost everything at Mosaic lives in **Notion**. The Mosaic Operating Manual in Notion outlines our vision, core business activities, operational procedures, and SOPs. When in doubt, start there.

Here's the map:

| What | Where |
|---|---|
| SOPs and policies | Notion wiki |
| Project management and task tracking | Notion databases |
| Lab notebooks | Notion (per project) |
| Released documents and document control | Notion documents database |
| Meeting notes and transcripts | Notion |
| Design guides and templates | Notion wiki |
| Vendor list | Notion |
| CAD files | OnShape |
| PCB designs | Altium Designer |
| Source code | GitHub |
| Large binary files (Altium, STEP, images, video) | Google Drive (per-project folder) |
| Large datasets (e.g. timelapse microscopy) | NAS (andor / per-project folder) |
| Passwords | VaultWarden (vault.mosaicdesignlabs.com) |
| Internal communication | Slack |
| Client communication | Slack Connect (preferred) or email |

**Rule of thumb:** If it's not in Notion, Slack, or one of the repos above, it's in the wrong place.

### How Notion Works

A little background is helpful. We chose Notion specifically because it is architecturally very simple but offers a wide range of UI customizations. Everything in Notion is either a **Page** or a **Database**. Database entries can have pages attached to them. Pages can embed databases or *views* into databases. Views present data from an underlying database with filters, sorts, and layout options — you can create a view that shows only lab notebook entries tagged with a specific project, for example.

It's helpful to create your own views in your private Notion space for things you reference often — filtered task lists, project dashboards, or your own lab notebook feed. The more comfortable you get with Notion's data model, the more useful it becomes. It's also helpful to add pages to your favorites so they show up on the sidebar.

### How Project Data Is Organized

At the project level, all data is contained within — or pointed to from — five pillars:

1. **Lab Notebook** — The chronological record of everything that happens on a project: design decisions, experimental results, vendor conversations, AI summaries, and screenshots. This is where work-in-progress lives. The Lab Notebook is meant to be *low friction*. The goal should be to create several lab notebook entries each week for every active project.
2. **Meeting Notes** — Meeting notes and transcripts live in their own Notion table, tagged with the relevant project code(s). This lets them appear in filtered views within each project page while keeping them in a single, searchable database across the organization. We use both Gemini and Otter for meeting transcription, and these notes go into a central database in Notion.
3. **Documents** — Released, versioned deliverables. These can be Notion pages, PDFs, or ZIPs, each with a link back to the editable source document or repository. We are in the process of implementing formal document control within Notion (ultimately, we'll build something ISO 13485 compliant). Documents should include a read-only released copy (e.g. PDF) along with a link to the underlying editable source document.
4. **Bill of Materials** — A special document type backed by a structured Notion database with standardized annotations. BOMs are hierarchical, with assemblies and sub-assemblies. The BOM lives in the Documents database but follows its own schema. See the BOM Management SOP.
5. **Repositories** — OnShape for CAD, GitHub for source code (note: migrating to local git server soon), and Altium for PCB designs (with files stored in Google Drive). Released documents should reference the specific repository and commit or version tag.

Each project also gets a **Google Drive folder** for large binary files — Altium designs, STEP files, images, videos, and other assets that don't belong in Notion. We also have a **NAS** at `andor` (accessible via WebDAV or SFTP over VPN) for large datasets such as timelapse microscopy. We may migrate off Google Drive in the future and rely strictly on our own storage server, but Google Drive remains useful for collaboration with third parties.

**Important:** Even if a file lives in Google Drive, the NAS, or a remote file system, include a link to it in the Lab Notebook or Documents database. These listings are the primary index and source of truth for a project — if something isn't linked from one of the five pillars above, it's effectively invisible.

---

## SOPs to Read First

Before you start work, familiarize yourself with these SOPs in the Notion wiki:

1. **Project Management** — How projects are structured, how tasks are tracked, how we run weekly reviews.
2. **Purchasing** — How to place orders, issue POs, track lead times, file receipts.
3. **Document Control and Design Control** — How we version, number, and release documents and designs.
4. **Lab Notebook** — How to log your work, experiments, and design decisions.
5. **BOM Management** — How to create, structure, and maintain bills of materials.
6. **Password Vault** — How to access and use VaultWarden.
7. **VPN Access** — How to install and configure OpenVPN for remote access.
8. **PCB Ordering** — How to order boards and what files to include.
9. **Schematic & PCBA Design Guide** — Standards for schematic capture, layout, and PCB assembly.
10. **OnShape Design Guide** — CAD naming conventions, folder structure, versioning, and drawing standards.
11. **Design Reviews** — When they happen, who's involved, and how to prepare.
12. **Engineering Lab Tools & Policies** — Lab equipment usage, safety, and maintenance expectations.
13. **Shipping & Receiving** — How to ship packages, receive deliveries, and manage packing materials.
14. **Timekeeping** — How to fill out your biweekly timesheet.
15. **Reimbursements** — How to file expense requests in Notion.

---

## Communication

### The Golden Rule: No Email

Use **Slack** for internal communication and for communicating with clients via Slack Connect. Use **Notion** for documents, project notes, and anything that needs to persist. Avoid email unless you're dealing with vendors, POs, or external parties who aren't on Slack.

### Response Times

- **Slack message during business hours:** Respond as quickly as possible, but at minimum within two hours.
- **Tagged in Notion:** Respond the same day.
- **You receive a file** (draft PDF, STEP file, schematic, etc.): Commit to looking at it *briefly* right away, even if a thorough review comes later. A quick acknowledgment goes a long way.

### Meetings and Calls

- Use a headset or quality microphone on calls. Place the mic close to your mouth.
- We transcribe all meetings — internal, external, even in-person — using Otter or Gemini. See the **Meeting Notes** section for how transcripts are stored and tagged.
- If you want a conversation, put it on the calendar and invite the right people. Don't ambush people at their desks for extended discussions.

### Client Communication

Generally, the **project manager (PM)** is the primary point of contact with a client — particularly early in the project as the relationship is being established. This separation is intentional: it helps engineers focus on the work at hand (fewer meetings, fewer direct client interactions) and gives the PM the visibility they need to manage timelines, budgets, and expectations effectively.

That said, **transparency is key.** All client conversations should ideally be transcribed, and all communication should happen in channels where the full team can follow along. When a new project is created, we set up two Slack channels — for example, `#poppy-internal` and `#poppy-external`. The client is invited to the external channel via Slack Connect.

Even if you're not the one managing the client relationship, stay engaged with the project conversation. Use the discussion features in the Lab Notebook, tag people, respond to questions, and generally remain plugged in. The goal is for everyone on the project to have full context without everyone needing to be in every meeting.

### Communication Style

We prefer direct, honest communication. Support your arguments with data. Work toward consensus. Connect directly with the people you need to work with—engineers to engineers, engineers to vendors.

---

## Timekeeping

Even if you're salaried, timekeeping is how we manage project budgets. This is non-negotiable.

- Log your hours to the nearest half hour on your biweekly timesheet.
- Include a brief note of what you worked on each week.
- Sign your timesheet on time so we can process it.
- Use **PTO column** if your contract includes paid time off.

### Project Codes

| Code | Use for |
|---|---|
| **MOS-01** | General and administrative work: lab operations, business tasks, overhead |
| **MOS-02** | Internal R&D not tied to a specific project |
| **[Client code]** | Work attributable to a specific client project (e.g., POP-01, ACC-01) |

Project codes follow the format: three letters, a dash, two numbers. Example: `POP-01` = Poppy Health, project 01. Internal Mosaic projects use `MOS-XX`.

---

## Lab Notebook

The lab notebook is one of the most important tools we use. Its purpose is to:

1. Minimize friction in getting ideas out of your head and onto paper.
2. Act as a central repository for PDFs, links, and references relevant to the project.
3. Add enough metadata that everything is sortable and searchable.
4. Serve as the collection point for draft content that feeds into deliverables.
5. Make it easy to tell a client "here's what we did last week."

The lab notebook is organized **chronologically** (in contrast to the Documents database, which is organized by document number).

### What Goes in the Lab Notebook

**Change Requests** — Every time you build a prototype, test a part, or release a software version, create a change request to collect your learnings. This feeds the next design cycle. We want to minimize iteration cycles and never repeat mistakes from rev to rev.

**Experimental Results** — Write these up as mini lab reports: Background, Materials, Methods, Results (with links to raw data), Conclusions. Once an experimental protocol is stable, move it into Document Control and issue formal reports against it.

**AI Summaries** — Include both a link to the AI conversation *and* a text dump. The link lets others pick up the conversation. The text dump preserves the record for our design history files and agentic browsing.

**Project Notes** — Design decisions, vendor conversations, price comparisons, design sketches, whiteboard photos, general notes.

**Screenshots** — As you make design revisions, grab a screenshot from CAD, Altium, or the UI and drop it in the lab notebook with a link to the source document. This costs nothing and is enormously useful in meetings.
- Mac: `Cmd + Ctrl + Shift + 4`
- Windows: `Win + Shift + S`

### Vendor Documents

All documents received from vendors—quotes, spec sheets, test reports—should go in the lab notebook for the relevant project.

---

## Meeting Notes

Meeting notes and transcripts (from Otter or Gemini) live in their own Notion database — not in the lab notebook. Each entry is tagged with the relevant project code(s), so meeting notes appear in filtered views within each project page while remaining in a single, searchable table across the organization. If a meeting touches multiple projects, tag it with all relevant codes.

---

## Document Control and Part Numbers

### Document Numbers

Released documents live in the project's Documents database in Notion and are assigned a document number. Documents can start as lab notebook entries and migrate to released status.

Format: `[CLIENT]-D[NNNN].[REV]`

Example: `XCC-D0012.1` — a document owned by XCellCure, document number 0012, revision 1. For Mosaic-owned documents, use the `MOS` prefix.

### Part Numbers

Format: `[CLIENT]-P[NNNN].[REV]`

Example: `POP-P0001.1` — Poppy Health owns the design, part number 0001, revision 1.

For Mosaic-owned designs, use the `MOS` prefix.

When a document references a design in OnShape, a codebase in GitHub, or a PCB project in Altium, include the repository location and the specific version tag or commit hash. This ensures traceability between released documents and the exact state of the design they describe.

For full procedures, see the **Document Control and Design Control SOP**.

### Part Numbers — Assemblies

Assemblies and sub-assemblies use the format: `[CLIENT]-A[NNNN].[REV]`

Example: `POP-A0001.1` — Poppy Health assembly 0001, revision 1. Use `MOS` for Mosaic-owned assemblies.

### Off-the-Shelf Parts

When a part is off-the-shelf (a catalog item from a vendor), use the vendor's part number in the BOM. We don't create our own part numbers for catalog items.

### Bill of Materials

The BOM is one of the most critical documents in any hardware project. BOMs are **hierarchical** — a top-level assembly BOM references sub-assembly BOMs, which in turn reference individual parts. Keep every level accurate and current: part numbers, revision numbers, sourcing information, pricing, and links to drawings and design documents.

For full procedures, see the **BOM Management SOP**.

---

## Design Reviews

Before ordering parts, there should be a design review involving at least one senior team member and ideally an external consultant with relevant expertise.

- Design review meetings are documented and transcribed.
- Any requested changes are documented before part release.
- Mechanical designs should be versioned with a PDF drawing (following our drawing template) and a tagged CAD version in OnShape. Documents, electrical designs, and source code should follow similar guidelines.
- Released design revisions get a document number in the project's Documents database.

For full procedures, see the **Design Reviews SOP**.

---

## Purchasing

Hardware development means lead times. If you're not actively managing them, they will slip.

We prefer **credit card purchases** for most things. Everyone has access to the company credit card (AMEX) — please use it responsibly and do not save or share the credit card info. When you make a credit card purchase, add an entry to the **Expense Log** in Notion and attach the receipt if available.

If a **purchase order (PO)** is needed — and many vendors will require one — create a **Purchase Request** in Notion and Trisha will issue the PO. Note that Trisha can also make credit card purchases on your behalf; the Purchase Request process applies to both credit card and PO purchases.

- When placing a long-lead-time order, **set a reminder** to follow up at the appropriate time.
- Attach the PO or receipt to the lab notebook entry for the relevant prototyping cycle.
- Track delivery dates and follow up proactively.

For full procedures, see the **Purchasing SOP**.

### Expense Categories

| Category | What it covers |
|---|---|
| **Lab Supplies** | Items not tied to a project — general lab materials, Mosaic operating budget |
| **Direct Materials and Services** | Items tied to a project — always include the project code |
| **Office Supplies** | General office consumables |
| **Cloud Computing** | AWS, GCP, hosting, and other cloud services |
| **Software Licenses** | Subscriptions and perpetual licenses for engineering and business tools |
| **Travel** | Transportation, lodging, and related expenses |
| **Meals & Entertainment** | Client meals, team events |
| **Professional Services** | Consulting, legal, accounting, and other outside services |
| **Advertising & Marketing** | Marketing materials, trade show expenses, promotional costs |

This is not an exhaustive list. The distinction between project-specific and general expenses matters for accounting, especially for grants. When in doubt, ask.

---

## Engineering Tools

We've settled on these tools after years of trial and error. We're open to new ideas, but there's usually a reason we use what we use.

### CAD — OnShape

We use OnShape for 3D CAD, accessed through the shared `engineering@mosaicdesignlabs.com` account. It runs entirely in the browser and has robust versioning and collaboration features. We follow consistent naming conventions and folder structures, use standard title block formatting, part numbering, and document numbering, and make intelligent use of the built-in versioning tools. We also have a perpetual SolidWorks Standard license on Organa.

### PCB Design — Altium Designer

We use Altium 17. It's an older version but works fine and can view designs from newer versions. We maintain a common Altium library with standardized components such as: connectors, MCUs, stepper drivers, LED drivers, power supplies, etc. See the PCB Altium Design Guide in Notion.

### Finite Element Modeling — COMSOL

We have the base package plus the electrochemical module, installed on Skywalker. We can purchase other modules as needed and prefer perpetual licenses.

### Software Development — Cursor

Cursor is our IDE. It's built on VS Code and compatible with most VS Code plugins. AI-driven development is evolving fast, but Cursor remains the standard for now. See the Notion tutorials for plugins for STM32, web, and Linux development.

### Embedded Platforms

- **Raspberry Pi Compute Module** for embedded Linux applications. Software in Python. Touchscreen UIs in HTML/CSS with Eel bindings in a Chromium kiosk browser.
- **STM32 ARM Cortex** for real-time microcontroller applications. Firmware in C using STM32CubeMX libraries.

### Backend and Web

Python with Flask, Postgres databases, and React/JavaScript frontends. All AI-driven. All backend tools should be **dockerized with Docker Compose**. We use open-source software wherever possible.

### Source Code and Documentation

We follow consistent naming conventions, keep comments concise and accurate, and maintain up-to-date `README.md` files, `.env.example` files, and API specs. AI makes this easy—there's no excuse for poor documentation.

### Authoring Documents in Markdown

We author documents in **Markdown** whenever possible. Markdown is plain text, version-controllable, and — critically — it enables AI assistance in drafting, editing, and indexing content. We have built tools for generating grant proposals from Markdown, and we are actively developing a document control and Notion integration system based on Markdown.

The preferred workflow is to **draft documents in Cursor**, where you get the full benefit of AI-assisted writing and editing, and then **export drafts and releases to Notion** following our automated document control workflow. Documents can also be created and edited directly in Notion, but Cursor-first is the standard path.

**Avoid Google Docs and Google Sheets** for document authoring. They don't integrate well with our AI tooling or version control workflows.

### Presentations

We primarily use **Google Slides** for presentations, though our thinking here is evolving — we are exploring **Canva** as an alternative. Regardless of the tool, always include a link to the presentation in the **Lab Notebook** for the relevant project.

### Illustrations

Engineering illustrations are extremely valuable — a good block diagram, state flow diagram, or system schematic can communicate the essential elements of a design far more effectively than text alone. Invest time in clear, well-labeled illustrations for your documents and presentations.

Our primary illustration tools:

- **Adobe Illustrator** — Our go-to for polished, publication-quality diagrams and figures. We have a shared account under `engineering@mosaicdesignlabs.com`, and Illustrator is also installed on Organa.
- **Excalidraw** — Browser-based, lightweight, and great for quick sketches and annotations. Especially useful during live meetings for collaborative drawing, or for marking up images and screenshots. No account needed.

Other useful tools:

| Tool | Best for |
|---|---|
| **Figma** | UI/UX mockups, interactive prototypes, and collaborative design work |
| **Canva** | Quick, polished graphics — slide assets, social media images, simple diagrams |
| **BioRender** | Scientific and biomedical illustrations — assay workflows, cell diagrams, instrument schematics |
| **PowerPoint** | Diagrams that need to live inside a slide deck or be easily editable by non-designers |

Use whatever tool fits the job, but always export a copy (PNG, SVG, or PDF) and include it in the Lab Notebook or the relevant document.

### AI and LLM Tools

We have professional accounts — including API access — for **ChatGPT**, **Claude**, and **Gemini**. Credentials are in VaultWarden. This space is evolving rapidly, but as of now:

- **Claude (Opus 4.6)** is generally the most advanced for deep research, complex reasoning, and long-form writing. It produces the best prose.
- **GPT (5.3)** does an excellent job summarizing and organizing ideas, and handles structured output well.
- Both are strong for coding and are integrated into Cursor.

We encourage the use of AI throughout our process — it is how we punch above our weight as a small team. Lean on these tools aggressively.

**Tips:**

- Make use of the **Projects** feature in ChatGPT and Claude to organize conversations by topic, client, or project. You can upload reference documents, set persistent instructions, and build context over time.
- You can **collaborate on a chat with others** — useful for pair problem-solving, design reviews, or working through a technical question with a colleague.
- Always include a link to the AI conversation (and a text dump of key outputs) in the **Lab Notebook**, so the team can pick up where you left off and the record is preserved for design history files.

**Key use cases:**

- Feasibility calculations across any engineering discipline — thermal, fluidic, optical, structural, electrical
- Ingesting and summarizing research papers and technical literature
- Drafting content for grant proposals, project proposals, product requirements, and specifications
- Automatically proposing test protocols based on specifications and acceptance criteria
- Drafting test reports from templates and collected data
- Summarizing weekly progress from meeting notes and lab notebook entries
- Generating training quizzes based on revised SOPs
- Parsing voice transcripts and generating document deliverables, action items, and follow-ups
- Reviewing and red-lining documents — SOPs, design specs, SOWs — for completeness, consistency, and errors
- Generating and refining BOM entries, vendor comparison matrices, and sourcing recommendations
- Translating between programming languages or porting code between platforms (e.g., Python to C for embedded)
- Brainstorming design alternatives and trade-off analyses
- Drafting client-facing emails, status updates, and presentation outlines

This list is not exhaustive — if you find a new use case that saves time or improves quality, share it with the team and add it to the **Workflow Suggestions** page.

---

## Engineering Design Standards

We maintain discipline-specific design guides in Notion — including the Schematic & PCBA Design Guide, the OnShape Design Guide, and others as they develop. Before diving into a new design, review the relevant guide.

A few general principles apply across all disciplines:

- **Reuse proven components.** We try to stick with components we've used before — connectors, ICs, mechanical parts, materials. This reduces risk, simplifies the BOM, and lets us leverage existing library parts and supplier relationships. If you want to introduce something new, make the case and discuss it with the team.
- **Design in metric.** We work primarily in metric units — both in our CAD tools and in the fasteners and hardware we spec into our products. Unless a client requirement or off-the-shelf interface dictates otherwise, default to metric. Try to use fasteners we already have in stock (we certainly have a lot!).
- **Follow the design guides.** The discipline-specific guides cover naming conventions, drawing standards, library usage, and review expectations. They exist to keep our work consistent and reviewable — use them.

---

## What We Build

Many of our products involve two complementary elements: an **instrument** (an electromechanical assembly, possibly incorporating sensors, optics, and mechatronics) and a **consumable** (generally a plastic, microfluidic component, possibly with onboard reagents). Understanding this instrument-plus-consumable architecture is important context for design decisions, BOM structures, and prototyping strategies across most of our projects.

---

## Hardware Development Workflow

### Prototyping Progression

1. **3D printing first.** Use our Bambu Labs FDM printer or SLA printer for most mechanical parts.
2. **CNC machining or laser-cut laminates** for parts that 3D printing can't handle well (e.g., microfluidic cartridges). Vapor polishing of CNC machined parts can be useful for microfluidics.
3. **Injection molding** is always the target for production cartridges unless there's a good reason otherwise.

For microfluidics specifically: we prototype with CNC machining or laser-cut laminate stack-ups with pressure-sensitive adhesive, with injection molding as the production target.


---

## Test Equipment and Automation

The lab is equipped with: oscilloscope, spectrum analyzer, function generator, power supply, USB data acquisition modules, temperature and humidity loggers, thermal camera, calipers, drop gauges, force tester, gas and liquid flow meters, spectrophotometer, PCR thermocycler, Nanodrop, and a fully automated fluorescence microscope.

**Automate wherever possible.** Most of our test equipment can be remote-controlled. Write automation scripts in Python. The ideal verification experiment is one where you push a button, go to lunch, and come back to your data.

---

## Network and Remote Access

We use **OpenVPN** for remote access. Installation instructions are in the SOPs.

We run a **local DNS server**, so you can access any computer or server on the network by typing its hostname into your browser or SSH client — no need to look up IP addresses. For example, `ssh c3po` or navigating to `http://gonk` will work when you're connected to the local network or VPN.

### PCs and Servers

A few key machines are listed here for reference. See the **IT and Network Reference** page in Notion for a full listing of PCs, servers, network configuration, and other IT details.

| Name | OS | What's on it |
|---|---|---|
| **Organa** | Windows | Nikon microscope PC. SolidWorks, LibreCAD, ImageJ, Altium |
| **Skywalker** | Windows | COMSOL Multiphysics |
| **Yoda** | Linux | Backend processes and services |

An on-prem AI server is coming online soon.

You can also remotely access Raspberry Pis running in prototype instruments—both in the lab and at customer sites around the world—for diagnostics, troubleshooting, and software updates.

### Network-Attached Storage (NAS)

The NAS is accessible at `files.mosaicdesignlabs.com` via WebDAV or SFTP (requires VPN). We use it for large datasets — timelapse microscopy, raw experimental data, and anything too large for Google Drive. Files stored on the NAS should still be linked from the project's Lab Notebook or Documents database.

---

## Password Management

We use **VaultWarden** (self-hosted Bitwarden clone) at `vault.mosaicdesignlabs.com`. Contact Frankie to activate your account. Install the Bitwarden browser extension.

Most engineers get access to the **Engineering Password Vault**, which includes: software tools, vendor purchasing accounts, the `engineering@mosaicdesignlabs.com` Google account, and general office accounts (Adobe, stock photos, Excalidraw, Smartsheet, etc.).

The vault also includes our Credit Card numbers, storage unit gate code, and lots of other important information. You will get an individual vault account. Credentials are shared on an as-needed basis.

### Account Creation Rules

| Type of account | Attach to |
|---|---|
| Technical / engineering / vendors | `engineering@mosaicdesignlabs.com` |
| Financial transactions | `accounting@mosaicdesignlabs.com` |
| IT administration | `admin@mosaicdesignlabs.com` |

Discuss with Frankie before creating accounts tied to IT or financial transactions.

### Password Rules

- Every account gets a unique password (defined in the wiki). Do not use the same password for multiple accounts.
- Passwords consist of 3 capitalized words plus a 2 digit number. These are long enough to be secure but easy enough to remember when you walk from one side of the lab to the other. An example of a good password is `WalrusJitterbugLamp28`.
- Never write passwords down.
- Use the Bitwarden browser extension so you never need to see the password on screen. See Bitwarden SOP for installation instructions.

---

## Lab Space

### Bench Assignments

| Bench | Purpose |
|---|---|
| 1 | Microscopy and biology experiments |
| 2 | Wet lab / experimental space |
| 3 | Project engineering |
| 4 | Project engineering |
| 5 | Electronics test and automated test fixtures; oscilloscope and lab PC |
| 6 | Large flex bench — demos, discussions, teardowns, larger builds |
| 7 | Fab workbench — fabrication and assembly fixtures |

### Storage Bins

| Color | Contents |
|---|---|
| Yellow | Mechanical parts for prototyping |
| Red | Electronic parts for prototyping |
| Black | Materials for a currently active project (project code on the bin) |
| Blue | General lab supplies or active project materials |
| Bankers boxes (fab lab) | Materials from completed projects |

### Lab Inventory

We maintain a **Lab Inventory** database in Notion that catalogs parts and tools across the facility — items in storage, in the parts room, in archival project boxes (banker's boxes), and in bins throughout the lab. It also covers tools and equipment, including computers and instruments. We include photos wherever possible so people can identify items without digging through bins. If you add, move, or consume inventory, update the database.

**Before purchasing a new tool or piece of equipment, check the inventory first.** It may already be in our possession — either in the lab or in storage.

### Computers

Lab and office computers are listed in the Lab Inventory database. See that listing for details on specs, installed software, and current assignments.

### Storage Unit

We maintain an off-site storage unit for overflow equipment, archived project materials, and surplus tools. We also occasionally buy equipment at auction — either to resell for profit or to put to use in our lab. As a result, we have a broad collection of tools and instruments in storage that may be useful for future projects or as we move into larger lab spaces.

---

## Lab Organization

Everything in the lab should have a designated place. Every shelf, bin, and drawer should be labeled clearly and unambiguously — if someone unfamiliar with the space can't find what they're looking for without asking, the labeling isn't good enough. When you use something, put it back. When you reorganize an area, update the labels and the inventory database to match.

---

## Lab Etiquette

- **One project per bench.** Keep your workspace organized.
- **Friday lab cleanup.** Everyone tidies their bench and common areas before they leave on Friday.
- **Mill safety:** Never use the CNC mill alone. At least one other person must be in the lab.
- **Soldering iron:** Turn it off when you leave. Same for the reflow oven and hot air rework station.
- **Equipment maintenance:** If you notice something isn't working right — a printer jamming, a calibration drifting, a tool wearing out — flag it in Slack and log it in Notion. Don't assume someone else will catch it.
- **Keep it clean.** Clean your surfaces, do your dishes, take out your trash.
- **Noise:** Noise-canceling headphones are recommended.
- **Scents:** Don't wear strong perfume or cologne.
- **Snacks:** Let us know what you like. We restock monthly.

### Monthly Lab Cleanup

Once a month, we do a deeper cleaning of the entire facility. Each person is assigned an area to maintain — this includes wiping down surfaces, organizing supplies, clearing out expired materials, and making sure everything is where it belongs.

### Office Plants

Plants bring life to a space, and they're important to us. Our plants are on automatic watering, but every two weeks we refill the water bottles and give each plant a healthy additional watering by hand. Remove dead leaves when you see them. If a plant looks unhealthy, mention it in Slack so we can address it.

### Shipping and Receiving

- **Receiving:** Break down cardboard boxes and take them to the recycling bins by the front gate.
- **Shipping:** Refer to the **Shipping & Receiving SOP**. Print labels, schedule a pickup, and leave packages by the front door.
- We keep an assortment of boxes and packing material in the fab lab — keep this area organized.

### Janitorial

We have janitorial services every eight weeks for a deep clean. In between, please remove trash and recycling when you notice the bins are full. The outdoor bins are by the front gate.

---

## Working Hours and Flexibility

We trust you to get your work done. Your hours are yours to set, with two caveats:

1. We drive toward milestones and review project status weekly.
2. We value in-person collaboration, so we'll work to align schedules between people on related projects.

Most of our tools work remotely. The network is accessible via VPN. We even have lab bench cameras you can check from home. People with lab access get a key and 24-hour facility access.

---

## Learning and Development

Learning is a core part of who we are. We encourage you to develop yourself as an engineer during your time here. We'll support—within reason—training, certifications, and conference attendance. We'll support you learning on the job, because as systems thinkers, we know nobody starts with all the skills they need.

We also give engineers the opportunity to develop their own ideas. We encourage experimentation, hobby projects, and play.

---

## Recommended Software

Install these tools as part of your onboarding:

- Google Chrome
- Google Drive (sync the folder for your project)
- Bitwarden browser extension
- Notion desktop app
- Slack desktop app
- Cursor (our IDE — see tutorials for git, STM32, web, and RPi/Linux dev)
- Adobe suite
- eDrawings (for viewing STEP files)
- Excalidraw (browser-based — great for interactive sketching on calls and design feedback)
- MS Office (though we generally prefer Google Docs for collaboration)
- Mountain Duck (for accessing files on Organa via Mac)
- Superhuman (optional - if you do a lot of email, though you shouldn't need to)

---

## Key Vendor Partnerships

We maintain a preferred vendor list in Notion. Key partnerships include:

- **Messenger Molding and Manufacturing** — Injection molding (Reno)
- **Wainamics** — Microfluidics (Fremont)
- **Rapid Fluidics** — 3D-printed microfluidics and manifolds
- **Rush PCB** — Local PCB vendor (Bay Area)
- **JLCPCB** — PCBs, 3D-printed parts, CNC-machined parts (China)

Consult the list and discuss with Frankie or the team before engaging a new vendor. As you find vendors that work well, help us keep the list updated.

---

## Intellectual Property

We take intellectual property seriously. We maintain **mutual NDAs** with our clients, vendors, contractors, and employees. If you're working on a project, assume the details are confidential unless explicitly told otherwise.

- Do not share client project details, designs, data, or business information outside the team.
- When working with external contractors or vendors, ensure an NDA is in place before sharing any proprietary information.
- Be mindful of IP in casual settings — conversations at conferences, on social media, or with friends in the industry. When in doubt, keep it to yourself.
- **Always be thinking about potentially patentable inventions** — whether on behalf of our clients or arising from our own internal R&D. If you believe something you're working on may be patentable, flag it to Frankie so we can evaluate and document it properly.
- If you have questions about what you can and can't share, ask Frankie.

For full procedures, see the **Intellectual Property Management SOP** *(link TBD)*.

---

## Contracting and Statements of Work

Most of our project relationships — whether we're the ones being hired or the ones hiring — are governed by a **Statement of Work (SOW)**. The SOW defines milestones, deliverables, timelines, and payment terms.

- **If you're a contractor:** The SOW is what you'll be held accountable to. Read it carefully, understand the deliverables, and flag concerns early. If something is ambiguous, ask for clarification before work begins.
- **If you're hiring contractors:** Put real thought into the SOW. Define the scope clearly, break the work into meaningful milestones, and specify acceptance criteria. The more aligned both parties are at the start, the more likely the relationship will be successful and expectations will be met.

SOWs are stored in Notion under the relevant project. Refer to the **Project Management SOP** for templates and procedures.

---

## Sourcing Talent — Upwork and Fiverr

We use **Upwork** and **Fiverr** to source freelance talent for specialized tasks. Use the `engineering@mosaicdesignlabs.com` login for both platforms (credentials in VaultWarden).

### Upwork

Upwork is our primary platform for hiring technical contractors — firmware engineers, software developers, mechanical designers, etc.

- **Always evaluate at least three candidates.** Schedule video calls, review portfolios, and assess communication skills before making a hire.
- **Start with a small, well-defined project.** This lets you evaluate quality, responsiveness, and working style before committing to larger engagements.
- We maintain a **list of past contractors** we've worked with in Notion. Check this list first — we're always looking for good people, and rehiring someone who's already proven themselves saves time and reduces risk.

### Fiverr

Fiverr is more suited to **design and creative services** — graphic design, renderings, animations, branding, etc.

- Post projects with **clear specs and deliverable expectations.**
- **Do not share proprietary details** that could constitute a breach of IP. Keep project descriptions generic enough to protect client and internal information. If the work requires sharing sensitive material, ensure an NDA is in place first.

### Transitioning to Direct Contracts

Once a freelancer has successfully completed a project through Upwork or Fiverr, we may invite them to contract with us directly — outside the platform. This reduces fees and simplifies the relationship for ongoing work. Discuss with Frankie before extending a direct contract offer.

---

## Mosaic Workflow and Automations

**Workflow** is our umbrella project for automation and AI integration across Mosaic operations. We use a combination of **custom software** (mostly Python scripts), a **local n8n instance** for workflow automation, and we are actively experimenting with **AI agents** to streamline repetitive tasks.

If you encounter a task — in engineering, operations, purchasing, documentation, or anywhere else — that you think would benefit from automation, add it to the **Workflow Suggestions** page in Notion. We review these regularly and prioritize based on impact and feasibility.

---

## Suggestions

We maintain a **Suggestions** page in Notion where anyone on the team is invited to submit ideas for improving Mosaic Design Labs — process improvements, tool recommendations, lab layout changes, policy tweaks, or anything else. We want to hear from you.

Note: suggestions are not anonymous. We believe in open, accountable communication, and attaching your name to an idea helps us follow up and give credit where it's due.

---

## Privacy and Data Security

We strive for transparency through Notion and share information broadly across the organization. However:

- Financial and accounting information is restricted to a small set of people.
- We take care to prevent client data from mixing between projects.
- If you see data in Notion that appears to be shared inappropriately, notify us immediately.

---

## Gathering Visual Content

Good photos tell stories that help us win the next project, client, or partnership. Even on mediocre projects, collect beautiful photos, renderings, and videos. Drop them in the Lab Notebook or the shared Google Photos album.

---

## Annual Cleanup

Once a year, we go through Notion and Google Drive and move anything we no longer need—or that could pose a security/privacy risk—to Archive folders. This includes old CSV exports, personal info from former team members, and orphaned documents. We also work to bring any new documents into proper organization.

---

*Questions? Ask in Slack. If it's not in Notion, it should be—help us put it there.*