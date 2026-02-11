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
| Large files and datasets | Google Drive / NAS |
| Passwords | VaultWarden (vault.mosaicdesignlabs.com) |
| Internal communication | Slack |
| Client communication | Slack Connect (preferred) or email |

**Rule of thumb:** If it's not in Notion, Slack, or one of the repos above, it's in the wrong place.

---

## SOPs to Read First

Before you start work, familiarize yourself with these SOPs in the Notion wiki:

1. **Project Management** — How projects are structured, how tasks are tracked, how we run weekly reviews.
2. **Purchasing** — How to place orders, issue POs, track lead times, file receipts.
3. **Document Control and Design Control** — How we version, number, and release documents and designs.
4. **Lab Notebook** — How to log your work, experiments, and design decisions.
5. **Password Vault** — How to access and use VaultWarden.
6. **PCB Ordering** — How to order boards and what files to include.
7. **Design Reviews** — When they happen, who's involved, and how to prepare.
8. **Timekeeping** — How to fill out your biweekly timesheet.
9. **Reimbursements** — How to file expense requests in Notion.

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
- We transcribe all meetings—internal, external, even in-person—using Otter or Gemini. Transcripts go into the project's Notion space.
- If you want a conversation, put it on the calendar and invite the right people. Don't ambush people at their desks for extended discussions.

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
| **MOS01** | General and administrative work: lab operations, business tasks, overhead |
| **MOS02** | Internal R&D not tied to a specific project |
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

**AI Summaries** — Include both a link to the AI conversation *and* a text dump. The link lets others pick up the conversation. The text dump preserves the record for our design history files.

**Project Notes** — Design decisions, vendor conversations, price comparisons, design sketches, whiteboard photos, general notes.

**Screenshots** — As you make design revisions, grab a screenshot from CAD, Altium, or the UI and drop it in the lab notebook with a link to the source document. This costs nothing and is enormously useful in meetings.
- Mac: `Cmd + Ctrl + Shift + 4`
- Windows: `Win + Shift + S`

### Vendor Documents

All documents received from vendors—quotes, spec sheets, test reports—should go in the lab notebook for the relevant project.

---

## Document Control and Part Numbers

### Document Numbers

Released documents live in the project's Documents database in Notion and are assigned a document number. Documents can start as lab notebook entries and migrate to released status.

### Part Numbers

Format: `[CLIENT]-P[NNNN].[REV]`

Example: `POP-P0001.1` — Poppy Health owns the design, part number 0001, revision 1.

For Mosaic-owned designs, use the `MOS` prefix.

### Bill of Materials

The BOM is one of the most critical documents in any hardware project. Keep it accurate and current: part numbers, revision numbers, sourcing information, pricing, and links to drawings and design documents.

---

## Design Reviews

Before ordering parts, there should be a design review involving at least one senior team member and ideally an external consultant with relevant expertise.

- Design review meetings are documented and transcribed.
- Any requested changes are documented before part release.
- Designs should be versioned with a PDF drawing and a tagged CAD version in OnShape (or a saved PCB folder with part number and revision in Google Drive).
- Released design revisions get a document number in the project's Documents database.

---

## Purchasing

Hardware development means lead times. If you're not actively managing them, they will slip.

- Issue POs and track delivery dates.
- When placing a long-lead-time order, **set a reminder** to follow up at the appropriate time.
- Attach the PO to the lab notebook entry for the relevant prototyping cycle.
- Follow the Purchasing SOP for logging expenses and submitting receipts.

### Expense Categories

| Category | What it covers |
|---|---|
| **Lab Supplies** | Items not tied to a project—general lab materials, Mosaic operating budget |
| **Direct Materials and Services** | Items tied to a project—always include the project code |

This distinction matters for accounting, especially for grants. When in doubt, ask.

---

## Engineering Tools

We've settled on these tools after years of trial and error. We're open to new ideas, but there's usually a reason we use what we use.

### CAD — OnShape

We use OnShape for 3D CAD, accessed through the shared `engineering@mosaicdesignlabs.com` account. It runs entirely in the browser and has robust versioning and collaboration features. We follow consistent naming conventions and folder structures, use standard title block formatting, part numbering, and document numbering, and make intelligent use of the built-in versioning tools. We also have a SolidWorks license on Organa.

### PCB Design — Altium Designer

We use Altium 17. It's an older version but works fine and can view designs from newer versions. We maintain a common Altium library with standardized components, connectors, stepper drivers, LED drivers, and power supplies. See the PCB Altium Design Guide in Notion. We use a few basic template architectures: Linux RPi CM and STM32.

### Finite Element Modeling — COMSOL

We have the base package plus the electrochemical module, installed on Skywalker. We can purchase other modules as needed and prefer perpetual licenses.

### Software Development — Cursor

Cursor is our IDE. It's built on VS Code and compatible with most VS Code plugins. AI-driven development is evolving fast, but Cursor remains the standard for now. See the Notion tutorials for plugins for STM32, web, and Linux development.

### Embedded Platforms

- **Raspberry Pi Compute Module** for embedded Linux applications. Software in Python.
- **STM32 ARM Cortex** for real-time microcontroller applications. Firmware in C using STM32CubeMX libraries.

### Backend and Web

Python with Flask, Postgres databases, and React/JavaScript frontends. All AI-driven. All backend tools should be **dockerized with Docker Compose**. We use open-source software wherever possible.

### Source Code and Documentation

We follow consistent naming conventions, keep comments concise and accurate, and maintain up-to-date `README.md` files, `.env.example` files, and API specs. AI makes this easy—there's no excuse for poor documentation.

---

## Hardware Development Workflow

### Prototyping Progression

1. **3D printing first.** Use our Bambu Labs FDM printer or SLA printer for most mechanical parts.
2. **CNC machining or laser-cut laminates** for parts that 3D printing can't handle well (e.g., microfluidic cartridges).
3. **Injection molding** is always the target for production unless there's a good reason otherwise.

For microfluidics specifically: we prototype with CNC machining or laser-cut laminate stack-ups with pressure-sensitive adhesive, with injection molding as the production target.

### Standard Components

We standardize on connectors, stepper drivers, LED drivers, power supplies, and other common components. Check the Altium library and design guides before sourcing something new. Don't reinvent the wheel.

---

## Test Equipment and Automation

The lab is equipped with: oscilloscope, spectrum analyzer, function generator, power supply, USB data acquisition modules, temperature and humidity loggers, thermal camera, calipers, drop gauges, force tester, gas and liquid flow meters, spectrophotometer, PCR thermocycler, Nanodrop, and a fully automated fluorescence microscope.

**Automate wherever possible.** Most of our test equipment can be remote-controlled. Write automation scripts in Python. The ideal verification experiment is one where you push a button, go to lunch, and come back to your data.

---

## Network and Remote Access

We use **OpenVPN** for remote access. Installation instructions are in the SOPs.

### Servers

| Name | OS | What's on it |
|---|---|---|
| **Organa** | Windows | Nikon microscope PC. SolidWorks, LibreCAD, ImageJ, Altium |
| **Skywalker** | Windows | COMSOL Multiphysics |
| **Yoda** | Linux | Backend processes and services |

An on-prem AI server is coming online soon.

You can also remotely access Raspberry Pis running in prototype instruments—both in the lab and at customer sites around the world—for diagnostics, troubleshooting, and software updates. We also have a network-attached storage (NAS) for large datasets.

---

## Password Management

We use **VaultWarden** (self-hosted Bitwarden clone) at `vault.mosaicdesignlabs.com`. Contact Frankie to activate your account. Install the Bitwarden browser extension.

Most engineers get access to the **Engineering Password Vault**, which includes: software tools, vendor purchasing accounts, the `engineering@mosaicdesignlabs.com` Google account, and general office accounts (Adobe, stock photos, Excalidraw, Smartsheet, etc.).

### Account Creation Rules

| Type of account | Attach to |
|---|---|
| Technical / engineering | `engineering@mosaicdesignlabs.com` |
| Financial transactions | `admin@mosaicdesignlabs.com` or `accounting@mosaicdesignlabs.com` |

Discuss with Frankie before creating accounts tied to financial transactions.

### Password Rules

- Every account gets a unique password (defined in the wiki).
- Never write passwords down.
- Use the Bitwarden browser extension so you never need to see the password on screen.

---

## Lab Space

### Bench Assignments

| Bench | Purpose |
|---|---|
| 1 | Microscopy and biology experiments |
| 2 | Wet lab / experimental space (currently: Microlab development) |
| 3 | Project engineering (currently: ACCEL CURE) |
| 4 | Project engineering (currently: POPPY) |
| 5 | Electronics test and automated test fixtures; oscilloscope and lab PC |
| 6 | Large flex bench — demos, discussions, teardowns, larger builds |
| 7 | Fab lab — fabrication and assembly fixtures |

### Storage Bins

| Color | Contents |
|---|---|
| Yellow | Mechanical parts for prototyping |
| Red | Electronic parts for prototyping |
| Black | Materials for a currently active project (project code on the bin) |
| Blue | General lab supplies or active project materials |
| Bankers boxes (fab lab) | Materials from completed projects |

---

## Lab Etiquette

- **One project per bench.** Keep your workspace organized.
- **Friday lab cleanup.** Everyone participates.
- **Mill safety:** Never use the CNC mill alone. At least one other person must be in the lab.
- **Soldering iron:** Turn it off when you leave. Same for the reflow oven and hot air rework station.
- **The plants are everyone's responsibility.**
- **Keep it clean.** Clean your surfaces, do your dishes, take out your trash.
- **Noise:** Noise-canceling headphones are recommended.
- **Scents:** Don't wear strong perfume or cologne.
- **Snacks:** Let us know what you like.

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
- Cursor (our IDE — see tutorials for STM32, web, and Linux dev plugins)
- Loom (for async video communication)
- Adobe suite
- eDrawings (for viewing STEP files)
- Excalidraw (browser-based — great for interactive sketching on calls and design feedback)
- MS Office (though we generally prefer Google Docs for collaboration)
- Mountain Duck (for accessing files on Organa via Mac)
- GitKraken (optional — Cursor's built-in Git features cover most needs)
- Superhuman (if you do a lot of email, though you shouldn't need to)

---

## Key Vendor Partnerships

We maintain a preferred vendor list in Notion. Key partnerships include:

- **Messenger Molding and Manufacturing** — Injection molding (Reno)
- **Waynamics** — Microfluidics (Fremont)
- **Rapid Fluidics** — 3D-printed microfluidics and manifolds
- **Rush PCB** — Local PCB vendor (Bay Area)
- **JLCPCB** — PCBs, 3D-printed parts, CNC-machined parts (China)

Consult the list and discuss with Frankie or the team before engaging a new vendor. As you find vendors that work well, help us keep the list updated.

---

## Privacy and Data Security

We strive for transparency through Notion and share information broadly across the organization. However:

- Financial and accounting information is restricted to a small set of people.
- We take care to prevent client data from mixing between projects.
- If you see data in Notion that appears to be shared inappropriately, notify us immediately.

---

## Gathering Visual Content

Good photos tell stories that help us win the next project, client, or partnership. Even on mediocre projects, collect beautiful photos, renderings, and videos. Drop them in `G:/Marketing/Projects` or the shared Google Photos album.

---

## Annual Cleanup

Once a year, we go through Notion and Google Drive and move anything we no longer need—or that could pose a security/privacy risk—to Archive folders. This includes old CSV exports, personal info from former team members, and orphaned documents. We also work to bring any new documents into proper organization.

---

*Questions? Ask in Slack. If it's not in Notion, it should be—help us put it there.*