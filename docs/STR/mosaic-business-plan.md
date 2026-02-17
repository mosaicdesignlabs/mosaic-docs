---
doc_uid: "MOS-BD-STR-001"
title: "Business Plan"
org: "MOS"
category: "STR"
department: "BD"
notion:
  database: "Documents"
  publish: true
access_groups:
  - "Leadership"
lifecycle:
  desired_state: "draft"
---
# Mosaic Design Labs — Business Plan

*Prepared by Frankie Robles, Founder*
*CONFIDENTIAL*

---

## Executive Summary

Mosaic Design Labs (MDL) is a biomedical product development studio based in the San Francisco Bay Area. We help startups, researchers, and established companies design, prototype, and bring to market devices and instruments at the intersection of hardware, software, and biology. We also conduct internal R&D focused on microfluidic automation and tools for cell biology — platforms with applications spanning drug discovery, cell therapy development, and scientific research.

MDL is not a typical engineering consultancy. We are an AI-native company built from first principles for a post-AI world, with deep expertise in biomedical instrumentation, a global network of engineering talent and manufacturing partners, and a mission-driven culture that attracts exceptional people. We operate as a lean, highly automated organization that delivers outsized value relative to our size.

The company has four years of operating history under Mosaic Engineering LLC, with gross revenues exceeding $700,000 annually and projected growth toward $1.5–2M in the near term. We are profitable, debt-free, and wholly owned by the founder.

This business plan describes the current state of the business, its growth trajectory, the broader Mosaic ecosystem we intend to build, and two pathways forward: a bootstrapped timeline and an accelerated timeline enabled by seed investment.

---

## Table of Contents

1. Company Overview
2. The Opportunity
3. Products and Services
4. Business Model
5. Market Landscape
6. Technical Competencies and Infrastructure
7. Team and Talent Strategy
8. Entity Structure
9. Growth Strategy
10. Financial Overview
11. Risk Factors
12. Appendices

---

## 1. Company Overview

### Legal Entity

Mosaic Engineering LLC, doing business as Mosaic Design Labs. Single-member LLC, wholly owned by Frankie Robles. Incorporated in California.

### History

MDL was founded in 2021 following the founder's departure from Lucira Health, where he spent seven years helping build what became the first FDA-authorized at-home COVID-19 test. At Lucira, the founder led core aspects of product design, vendor selection, regulatory submission, and manufacturing scale-up — gaining deep firsthand experience with the full lifecycle of a biomedical product from concept through FDA authorization to high-volume production.

MDL was started with the conviction that the traditional model of biomedical product development — large in-house teams, expensive consultancies, slow iteration cycles — was ripe for disruption. By combining AI-native workflows, a global freelancer network, rigorous engineering processes, and a small, highly creative core team, MDL has demonstrated that it can deliver exceptional product development at a fraction of the cost and time of conventional firms.

Over four years, MDL has served approximately two dozen clients across biomedical diagnostics, research instrumentation, lab automation, industrial controls, and consumer health. Clients range from pre-seed startups to established companies including Pfizer.

### Location

MDL operates from a lab and office facility in the East Bay (Berkeley/Oakland area), equipped with:

- Four to five lab benches supporting three to four concurrent projects
- Fabrication studio: 3D printers, laser cutter, CNC mill, PCB reflow oven, CNC blade cutter
- Electronics workshop: soldering stations, oscilloscopes, power supplies, logic analyzers
- Cell biology lab: automated microscope, qPCR thermocycler, spectrophotometer, automated liquid handler, incubators, centrifuges, analytical balance
- Core facility membership at UC Berkeley for extended laboratory capabilities

---

## 2. The Opportunity

### The Problem

Biomedical product development is too expensive, too slow, and too inaccessible. The gap between a promising idea in a university lab and a product that reaches patients or researchers is typically measured in years and tens of millions of dollars. This creates several downstream problems:

**For startups and academic inventors:** The cost of engaging a traditional product development firm is prohibitive. First-time hardware founders face a bewildering landscape of manufacturing processes, regulatory requirements, and engineering tradeoffs that they have no framework to navigate. Many promising technologies die in the "valley of death" between academic publication and commercial viability.

**For pharmaceutical and biotech companies:** Drug discovery and biological research remain heavily dependent on manual laboratory workflows, microtiter-plate formats, and expensive commercial instruments that offer limited flexibility. The bottleneck is not ideas — it's the tools to test them efficiently and reproducibly.

**For the medical device industry broadly:** There is an enormous and growing gap between the cost of consumer electronics and the cost of medical devices, driven by regulatory overhead, antiquated business models, and the absence of competitive pressure that exists in consumer markets. AI and automation present a generational opportunity to close this gap.

### Why Now

Three converging trends make this the right moment for a company like MDL:

**AI has fundamentally changed the economics of engineering.** Generative AI tools have reduced the time and cost to produce documentation, code, specifications, test protocols, grant proposals, and project management artifacts by an order of magnitude. A small team augmented by AI can now do what previously required a large organization. This advantage compounds — every SOP we write, every template we create, every workflow we automate makes the next project faster and cheaper.

**Global engineering talent is more accessible than ever.** Cloud-based CAD (OnShape), distributed version control (Git), real-time collaboration tools (Notion, Slack), and the maturation of the global freelance engineering market mean that a small Bay Area company can assemble world-class, project-specific teams on demand.

**Biology is becoming an engineering discipline.** Advances in microfluidics, organ-on-chip technology, automated microscopy, and computational biology are enabling a shift from artisanal benchwork to reproducible, automated experimentation. The companies that build the tools and platforms for this transition will be positioned at the center of pharmaceutical R&D for decades.

---

## 3. Products and Services

MDL's revenue streams fall into three categories, ordered by current contribution.

### Client Engineering Services (Primary — Current)

We provide end-to-end product development services for clients seeking to build biomedical devices, research instruments, lab automation systems, and related hardware/software products. Our engagement model follows a phased structure:

**Phase 0 — Scoping.** We help clients define the problem, identify the team, assess feasibility, and put together a program plan. This phase often involves customer discovery support, competitive analysis, and preliminary technical architecture. Outcome: statement of work and budget for Phase 1.

**Phase 1 — Feasibility.** We retire key technical risks, build proof-of-concept prototypes, and validate core assumptions. Outcome: feasibility report with go/no-go recommendation.

**Phase 2 — Development.** We deliver looks-like, works-like, and is-like prototypes. We execute design for manufacturability, create production documentation, and support design transfer to manufacturing partners. Outcome: production-ready design package.

We price projects on a milestone (SOW) basis or a monthly retainer, depending on the nature of the engagement. We do not bill primarily for time — we bill for value. We occasionally negotiate equity grants in client companies when we believe in the long-term potential and want to align incentives.

Representative engagements include: custom imaging systems for diabetic wound assessment, foodborne pathogen diagnostic cartridge development, LabVIEW-based instrument controllers, microfluidic chip design and fabrication, and embedded firmware for connected analytical instruments.

### Non-Dilutive Grants (Growing)

MDL actively pursues SBIR/STTR funding from NIH, NSF, ARPA-H, and DoD agencies. The SBIR program is particularly well-suited to our model: it funds high-risk, high-impact technology development at the seed stage, and the Phase I/Phase II structure aligns naturally with our phased engagement model.

We also pursue collaborative grants with university partners (primarily UC Berkeley) and participate in NSF I-Corps customer discovery programs. Grant revenue funds internal R&D while building credibility and an IP portfolio.

The founder has experience writing, receiving, and reviewing NIH grants, and sits on federal review committees.

### Internal R&D Products (Emerging)

Our internal R&D is focused on two platform technologies:

**Microfluidic Automation Controller (MicroLab).** A generalizable system for precisely controlling fluid delivery in microfluidic chips. The platform includes a pressure-based flow controller, valve controller, and software for designing and executing automated protocols. Target customers include academic researchers (cell biology, drug discovery) and pharmaceutical companies developing microphysiological systems. The long-term vision encompasses design tools (in-browser CAD for microfluidic chips), fabrication services (automated PDMS device manufacturing), and automation hardware — the full trifecta of design, fabrication, and automation.

**Live Cell Imaging Tools.** Automated microscopy workflows that integrate with the microfluidic platform, enabling time-lapse imaging, automated analysis, and AI-in-the-loop experimental biology. These tools are designed to attach to standard laboratory microscopes, lowering the barrier to adoption.

Revenue from internal products will come from instrument sales, consumable sales (microfluidic chips), design services for custom applications, and IP licensing.

### Future Service Lines

**Mosaic Consulting / Expert Review Panels.** An AI-enhanced platform for matching expert consultants to client projects, automating scheduling, report generation, and knowledge management. Modeled on GLG/GuidePoint but with dramatically lower overhead through AI automation. This is an early-stage concept with a clear MVP path.

**Design Review and Coaching Services.** One-on-one and panel-based design reviews for hardware startups, leveraging our engineering expertise and AI tools. Lower-touch than full project engagements but high-value and relationship-building.

---

## 4. Business Model

### Revenue Model

| Revenue Stream | Pricing | Margin Profile | Current Status |
|---|---|---|---|
| Client engineering services | SOW milestones or monthly retainer ($15–25K/mo typical) | 40–60% gross margin (varies by project mix of internal labor vs. subcontractors) | Active, primary revenue driver |
| SBIR/STTR grants | $150–300K per Phase I; $750K–1.5M per Phase II | High margin (funds R&D with minimal COGS) | Active, growing pipeline |
| Instrument sales (MicroLab) | TBD — estimated $10–50K per system depending on configuration | Hardware margins 40–60% after initial tooling investment | In development |
| Consumables (microfluidic chips) | TBD — estimated $10–100 per chip at volume | High margin at scale; low margin initially | In development |
| Consulting / expert panels | $500–5,000 per engagement | Very high margin (primarily software and network) | Concept stage |

### Cost Structure

MDL operates with intentionally low fixed costs. The largest expense categories are:

- **Contractor labor.** Freelance engineers (mechanical, electrical, software, biology) engaged on a project basis. Contractors are typically marked up 2x when billed to clients.
- **Materials and prototyping.** Components, PCB fabrication, 3D printing, microfluidic materials, lab consumables. We leverage low-cost global vendors (JLCPCB, etc.) aggressively.
- **Facility.** Lab and office rent, utilities, equipment maintenance.
- **Software and tools.** OnShape, Altium, Cursor, Notion, Slack, AI APIs, cloud services.
- **Full-time staff.** Currently small; growing as revenue allows. Includes engineering, administrative, and intern positions.

The combination of AI-native workflows, global contractor network, and minimal fixed overhead gives MDL a structural cost advantage over traditional product development firms. We estimate that we can deliver comparable engineering output at 30–50% of the cost of a conventional firm, while moving faster due to automation and leaner decision-making.

### Key Metrics

- Gross revenue: ~$700–800K annually (historical), trending toward $1–1.5M in current fiscal year, $2M projected in subsequent year
- Gross margin on client services: 40–60%
- Typical project size: $50–300K
- Active projects at any given time: 3–6
- Grant proposals submitted per year: 3–6
- Team size: 1 full-time founder + 1 full-time engineer + 1 executive assistant + rotating interns and project-based contractors

---

## 5. Market Landscape

### Addressable Markets

MDL operates at the intersection of several large and growing markets:

**Biomedical product development services.** The global medical device contract development and manufacturing (CDMO) market is valued at over $50B. MDL competes in the design and development segment, primarily serving early-stage companies and academic inventors who are underserved by large CDMOs.

**Microfluidics and organ-on-chip.** The global microfluidics market is projected to exceed $30B by 2030. The organ-on-chip segment, while smaller (~$200M today), is growing rapidly as pharmaceutical companies seek alternatives to animal testing and more predictive in vitro models.

**Lab automation and instrumentation.** The laboratory automation market exceeds $6B globally. AI-driven automation is an emerging segment with significant greenfield opportunity, particularly in academic and mid-scale pharma settings.

### Competitive Positioning

MDL does not compete head-to-head with large CDMOs (Flex, Jabil) or established design firms (IDEO, Ximedica, StarFish Medical). These firms serve larger clients with larger budgets and more mature products. MDL serves earlier-stage clients with more technical risk and smaller budgets — a segment that large firms find uneconomical.

Our differentiation rests on three pillars:

1. **AI-native operations** — We are structurally faster and cheaper than firms built on pre-AI workflows.
2. **Biological fluency** — Unlike most hardware development firms, we speak bio. We have laboratory facilities, academic relationships, and hands-on experience with cell culture, molecular diagnostics, and microfluidics.
3. **Founder-led engagement** — Clients hire us and work directly with a founder who has deep, cross-functional experience. They are not handed off to junior staff.

On the product side (MicroLab), competitors in the microfluidic automation space include Fluigent, Elveflow, and Dolomite, as well as emerging organ-on-chip platform companies (Emulate, CN Bio, TissUse). MDL's intended differentiation is an open, customizable platform approach — rather than selling a closed system optimized for one application, we provide design, fabrication, and automation tools that let researchers create their own solutions.

---

## 6. Technical Competencies and Infrastructure

### Core Disciplines

- Embedded systems design (ARM-based architectures, STM32, Raspberry Pi CM)
- PCB design and layout (Altium Designer)
- Mechanical design and prototyping (OnShape, SolidWorks)
- Microfluidic chip design and fabrication (PDMS soft lithography, 3D printed manifolds)
- Firmware development (C/C++, Python, LabVIEW)
- Full-stack software development (web applications, cloud-connected instruments, data pipelines)
- Optical system design (imaging systems, microscopy, ray tracing)
- Cell and molecular biology (cell culture, qPCR, microscopy, liquid handling)
- Regulatory strategy (FDA 510(k), De Novo, SBIR/STTR compliance)
- Technical project management and grant writing

### Design Philosophy

We rigorously apply preferred architectures and design guides across projects so that we are not reinventing the wheel. Common embedded platforms, connector families, PCB templates, CAD conventions, and fabrication methods are standardized and documented. This means a new engineer or intern can be productive within days, and each new project benefits from the accumulated wisdom of prior work.

Our philosophy is to build flexible architectures around whatever core technology is unique to the product, so that the team can focus most of its attention on the novel science and engineering rather than on boilerplate systems work.

### Key Vendor Partnerships

- Messenger Molding and Manufacturing (injection molding, Reno NV)
- Waynamics (microfluidics, Fremont CA)
- Rapid Fluidics (3D printed microfluidic parts)
- Rush PCB (local Bay Area PCB vendor)
- JLCPCB (PCBs, 3D printing, CNC machining from China)

---

## 7. Team and Talent Strategy

### Current Team

- **Frankie Robles, Founder and Principal Engineer.** PhD Bioengineering, UC Berkeley. 15+ years of experience across microfluidics, biomedical instrumentation, molecular diagnostics, product development, and manufacturing. Core inventor at Lucira Health (FDA-authorized at-home COVID test). SBIR grant recipient and federal grant reviewer. Teaches product development; maintains university affiliations.
- **Full-time engineer** (mechanical/electrical, general-purpose prototyping and project execution)
- **Executive assistant** (operations, scheduling, contractor onboarding, administrative workflows)
- **Rotating interns** (typically UC Berkeley engineering students on semester or summer appointments)
- **Project-based contractors** (mechanical engineering, electrical engineering, firmware, biology — sourced from a cultivated global network)

### Hiring Philosophy

We recruit junior and mid-level talent — interns, recent graduates, PhD students — and give them real responsibility within a structured framework of design guides, SOPs, and mentorship. We complement this with specialized senior contractors engaged on a project basis. This keeps fixed costs low while maintaining access to world-class expertise when needed.

We are selective. We look for people who are curious, creative, self-directed, and drawn to work that matters. We would rather leave a position unfilled than hire someone who isn't the right fit.

### Near-Term Hiring Priorities (Next 12 Months)

- Senior engineer with biomedical device commercialization experience (ideally someone who complements the founder's strengths in business development, customer discovery, or regulatory strategy)
- Software developer to build and maintain internal operational tools (Mosaic Workflow platform)
- Grant writer / business development support (possibly part-time or contract)
- Two to four summer interns from UC Berkeley or comparable programs

### Long-Term Talent Vision

MDL aspires to operate a structured internship and apprenticeship program — a kind of trade school for product development. We envision cross-generational teams: industry veterans, mid-career professionals, graduate students, undergraduates, and career-changers working side by side on projects of real significance. Graduates of our program would carry skills, relationships, and a professional reputation that position them for careers in product development, entrepreneurship, or academic research.

---

## 8. Entity Structure

The Mosaic ecosystem comprises multiple legal entities, each serving a distinct purpose. (See Entity Structure Memo for full detail.)

**Mosaic Engineering LLC (DBA Mosaic Design Labs)** — The core operating company. Wholly owned by the founder. All client services, grants, R&D, and hiring flow through MDL.

**Mosaic Commons** — An operating entity for the larger physical space: shared fabrication studio, bio lab, event and community space, and tenant offices. Leases to MDL and other entities.

**Mosaic Property Holdings** — A property holding company (LP/GP structure) to purchase the building housing the Commons. Mission-aligned investors participate as limited partners.

**Nonprofit Fiscal Sponsorship** — A 501(c)(3) entity or fiscal sponsorship arrangement to receive philanthropic contributions funding mission-driven activities: global health projects, education programming, internship stipends, artist-in-residence, and basic research.

**Mosaic Seed Fund (Future)** — An internal investment vehicle for funding and incubating projects. Team members and outside investors participate at the project level rather than through equity in MDL.

---

## 9. Growth Strategy

We present two timelines: a bootstrapped path (no external investment) and an accelerated path (with seed capital). In both cases, MDL is the engine that drives growth. The broader ecosystem develops as revenue and investment allow.

### Path A: Bootstrapped Growth

**Year 1 (Current)** — Stabilize client revenue at $1–1.5M. Submit 3–5 SBIR proposals. Complete MicroLab feasibility prototype. Hire one senior engineer and one software developer. Formalize SOPs, design guides, and onboarding materials. Begin quarterly advisory committee meetings. Launch blog and podcast content.

**Year 2** — Grow client revenue to $2M. Land at least one SBIR Phase I award. Deliver first MicroLab beta units to academic partners. Establish two to three university collaboration agreements. Run first summer internship cohort (four to six interns). Begin scouting properties for Mosaic Commons.

**Year 3** — Client revenue $2–3M. Pursue SBIR Phase II for MicroLab. Begin selling microfluidic automation systems and consumables to early adopters. Formalize nonprofit fiscal sponsorship. Host first public community events. Negotiate building acquisition or long-term lease.

**Year 4–5** — Revenue from product sales supplements client services. Incubate first spin-out project. Establish Mosaic Commons in a dedicated facility. Advisory committee and internship program operating at steady state. Evaluate readiness for seed fund.

### Path B: Accelerated Growth (With Seed Investment)

With an initial investment of $1–3M (from aligned investors, philanthropic sources, or a combination), we accelerate the timeline by approximately 18–24 months:

**Investment Deployment:**
- Hire two to three senior technical staff immediately (engineer, software developer, grant writer/BD)
- Accelerate MicroLab development to production-ready prototype within 12 months
- Secure and build out Mosaic Commons facility in Year 1
- Fund first internship cohort and community programming in Year 1
- Establish nonprofit entity and begin philanthropic fundraising in Year 1

**Expected Outcomes (by end of Year 3):**
- Revenue $3–5M (combined client services, grants, and product sales)
- MicroLab generating recurring product revenue
- Two to three active SBIR grants
- One to two incubated spin-out projects
- Mosaic Commons operating with three to five tenant projects
- Structured internship program with annual cohorts

### Scaling Philosophy

We scale out, not up. If this model works, we offer it as a blueprint for others. We are not trying to build a 500-person company. We are trying to build a 15–25 person company that punches far above its weight, trains the next generation of builders, and spins out innovations that grow into their own organizations. If others want to replicate this model — in manufacturing, in climate tech, in policy — we encourage it.

---

## 10. Financial Overview

### Historical Revenue

| Fiscal Year | Approximate Gross Revenue |
|---|---|
| Year 1 (2021) | ~$700K |
| Year 2 (2022) | ~$700K |
| Year 3 (2023) | ~$800K |
| Year 4 (2024) | ~$1M (estimated) |

Revenue has been generated primarily through client engineering services, with some contribution from SBIR grants. The company has been profitable each year with minimal debt.

### Projected Revenue (Bootstrapped Path)

| Year | Client Services | Grants | Product Sales | Total |
|---|---|---|---|---|
| Year 5 (2025) | $1.2M | $300K | — | $1.5M |
| Year 6 (2026) | $1.5M | $500K | $100K | $2.1M |
| Year 7 (2027) | $1.5M | $750K | $500K | $2.75M |
| Year 8 (2028) | $1.5M | $500K | $1M | $3M |

These projections assume no external investment. Grant revenue assumes one to two active SBIR awards. Product revenue assumes MicroLab begins shipping in Year 7 with a modest initial customer base. Client services revenue stabilizes as the team's attention shifts partially toward internal products and grants.

### Use of Funds (If Seed Investment Received)

| Category | Allocation |
|---|---|
| Hiring (2–3 senior staff, first 18 months) | 40% |
| MicroLab product development (prototyping, tooling, testing) | 25% |
| Facility acquisition / build-out (Mosaic Commons) | 20% |
| Operations (legal, accounting, software, marketing) | 10% |
| Reserve | 5% |

---

## 11. Risk Factors

**Founder dependency.** MDL's reputation, client relationships, and technical leadership are currently concentrated in the founder. Mitigation: hiring senior staff who can independently lead projects and client relationships; documenting institutional knowledge in SOPs and design guides.

**SBIR funding uncertainty.** The federal grant landscape is subject to political and budgetary fluctuation. Mitigation: maintaining a diversified revenue base where grants supplement rather than replace client services; pursuing grants from multiple agencies.

**Product development risk (MicroLab).** The MicroLab platform involves meaningful technical and market risk. Mitigation: phased development with clear go/no-go milestones; customer discovery through I-Corps and direct engagement (50+ interviews completed to date); pursuing grant funding to de-risk development costs.

**Market timing.** The organ-on-chip and microfluidic automation markets are growing but still early. Customer adoption may be slower than projected. Mitigation: maintaining client services as the primary revenue base; designing the MicroLab platform for broad applicability rather than a single niche.

**Hiring in a competitive market.** Top engineering talent in the Bay Area has many options. Mitigation: offering meaningful work, creative latitude, and mentorship rather than competing purely on compensation; leveraging university relationships and the intern pipeline.

**Real estate risk.** Acquiring and maintaining a facility is a significant financial commitment. Mitigation: pursuing building acquisition only when revenue supports it; structuring the property holding company with aligned investors to share risk; maintaining optionality between purchase and long-term lease.

---

## 12. Appendices

*The following appendices are referenced but will be developed as separate documents:*

- A. Founder CV and background
- B. Detailed financial model (multi-year P&L, cash flow, balance sheet)
- C. MicroLab product specification and development roadmap
- D. Representative client case studies (Empo Health, Spectacular Labs, and others)
- E. SBIR proposal pipeline and award history
- F. Letters of support from advisors and academic partners
- G. Competitive landscape analysis (microfluidic automation, organ-on-chip)
- H. Entity structure diagram and legal framework

---

*This business plan is a living document. It reflects the founder's current understanding and intentions as of the date of preparation. All projections are estimates based on assumptions that may change as the business evolves. This document is confidential and intended for internal use, legal counsel, and potential investors and partners with whom the founder has a relationship of trust.*

---

*Mosaic Design Labs — San Francisco Bay Area*
*Incubating Innovation*
