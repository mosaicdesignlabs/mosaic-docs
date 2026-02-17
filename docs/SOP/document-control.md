---
doc_uid: "MOS-OPS-SOP-001"
title: "Document Control"
org: "MOS"
category: "SOP"
department: "OPS"
notion:
  database: "Documents"
  publish: true
access_groups:
  - "All-Hands"
lifecycle:
  desired_state: "draft"
---

# Document Control

*Standard Operating Procedure for creating, organizing, reviewing, and publishing controlled documents at Mosaic Design Labs.*

---

## 1. Purpose

This SOP describes how documents are created, categorized, reviewed, approved, and published at Mosaic Design Labs. It applies to anyone authoring documents—whether you're an engineer writing an SOP, a contractor drafting a report, or an AI agent generating a first draft.

Our document control system ensures that:

- Every document has a unique, permanent identifier.
- Documents are version-controlled and traceable to specific authors and reviewers.
- Published documents are read-only, with a clear revision history.
- Everyone can find the current version of any document quickly.

---

## 2. Scope

This SOP covers all controlled documents at Mosaic, including those authored in:

- **Git (Markdown)** — the primary authoring environment for SOPs, policies, design guides, and other structured documents.
- **Notion** — used for documents that require Notion-native features (databases, embedded views, etc.) and cannot be adequately represented in Markdown.

It does not cover:

- Lab notebooks (managed per-project in Notion).
- Meeting notes and transcripts (managed in Notion, not version-controlled).
- CAD files, PCB designs, or source code (managed in their respective tools with their own versioning).

---

## 3. Document Categories

Every document belongs to a **category** that describes its purpose. Categories determine the subfolder a document lives in (in Git) and help people find what they're looking for.

| Code | Category | What It Contains | Examples |
|---|---|---|---|
| **SOP** | Standard Operating Procedure | Step-by-step procedures for repeatable processes. SOPs describe *how* to do something. | Soldering SOP, Document Control SOP, PCB Ordering SOP |
| **POL** | Policy | Organizational policies, guidelines, and onboarding materials. Policies describe *what we expect*. | Engineering Onboarding Guide, Data Retention Policy |
| **DG** | Design Guide | Engineering principles, reference material, and how-to guides for technical work. | How to Be an Engineer, PCB Design Guide |
| **STR** | Strategy | Vision, business plans, frameworks, and criteria used for strategic decision-making. | Mosaic Vision, Business Plan, R&D Project Selection Criteria |
| **GOV** | Governance | Charters, bylaws, entity structures, and committee documents. | Advisory Committee Charter, Entity Structure Memo |
| **MKT** | Marketing | One-pagers, pitch decks, recruiting materials, and other external-facing documents. | Investor Overview, Engineer Recruiting One-Pager |
| **WI** | Work Instruction | Narrow, task-specific instructions (often referenced by SOPs). | Cleanroom Entry Procedure, Autoclave Loading |
| **RPT** | Report | Formal reports — test results, validation reports, literature reviews. | Thermal Validation Report, Design Review Summary |
| **PRO** | Proposal | Project proposals, statements of work, and scoping documents. | Client Project Proposal, Internal R&D Proposal |

If a document doesn't clearly fit a category, ask: *Is this describing a process (SOP), setting expectations (POL), teaching something (DG), informing a decision (STR/RPT), or selling something (MKT)?* When in doubt, default to **POL** for internal guidelines or **RPT** for one-off technical documents.

---

## 4. Departments

Each document is assigned to a **department** that indicates who owns it:

| Code | Department |
|---|---|
| **ENG** | Engineering — technical SOPs, design guides, engineering policies |
| **OPS** | Operations — company-wide policies, admin, governance, HR |
| **BD** | Business Development — strategy, investor materials, client-facing docs, marketing |
| **FIN** | Finance — financial policies and procedures |

---

## 5. Document Identifiers (doc_uid)

Every controlled document is assigned a unique identifier called a `doc_uid`. This is the canonical ID that follows the document across all revisions, across Git and Notion, forever.

### 5.1 Format

```
ORG-DEP-CAT-NNN
```

| Segment | Meaning | Examples |
|---|---|---|
| `ORG` | Organization code (3 letters) | `MOS` (Mosaic), `POP` (Poppy Health), `XCC` (XCellCure) |
| `DEP` | Department code (2–3 letters) | `ENG`, `OPS`, `BD`, `FIN` |
| `CAT` | Category code (2–3 letters) | `SOP`, `POL`, `DG`, `STR`, `GOV`, `MKT`, `WI`, `RPT`, `PRO` |
| `NNN` | Sequential number (zero-padded) | `001`, `012`, `100` |

**Examples:**

- `MOS-OPS-SOP-001` — This document (Mosaic, Operations, SOP, #001)
- `MOS-ENG-DG-001` — How to Be an Engineer
- `MOS-BD-MKT-003` — Investor Overview one-pager
- `POP-ENG-RPT-003` — A Poppy Health engineering report

### 5.2 Full document number (with revision)

When displayed, the full document number includes the revision: `MOS-ENG-SOP-012.1` means document `MOS-ENG-SOP-012`, revision 1. The `doc_uid` itself never includes the revision—revision is tracked separately and computed automatically by the publishing pipeline.

### 5.3 Assignment

For documents authored in **Git**, the `doc_uid` is specified in the YAML frontmatter. You can either:

- Assign it manually by choosing the next available number for that ORG-DEP-CAT combination.
- Set `doc_uid: "auto"` and the pipeline will assign the next available number automatically.

For documents created directly in **Notion**, assign the `doc_uid` manually in the document's database properties. The pipeline checks for conflicts to ensure no two documents share the same `doc_uid`.

---

## 6. Repository Structure

Documents authored in Git live under the `docs/` directory, organized by category:

```
docs/
  SOP/
    document-control.md
    laser-safety.md
  POL/
    engineering-onboarding.md
  DG/
    how-to-be-an-engineer.md
  STR/
    mosaic-vision.md
    mosaic-business-plan.md
  GOV/
    advisory-committee-charter.md
  MKT/
    onepager-engineers.md
    onepager-investors.md
  WI/
    cleanroom-entry.md
  RPT/
    thermal-validation-report.md
  images/
    cartridge-exploded-revC.png
```

### 6.1 File naming

- Use **kebab-case** (lowercase, hyphens between words): `laser-safety.md`, not `Laser Safety.md` or `laser_safety.md`.
- Names should be descriptive but concise. The `title` in frontmatter is the display name; the filename is for humans navigating the repo.
- Images go in `docs/images/` and use descriptive, kebab-case names that include context: `cartridge-exploded-revC.png`, `pcb-layout-top-v2.png`.

---

## 7. Frontmatter

Every Markdown document must begin with a YAML frontmatter block. This is the metadata that the publishing pipeline uses to identify, categorize, and publish the document.

### 7.1 Example

```yaml
---
doc_uid: "MOS-ENG-SOP-012"
title: "Laser Safety in the Lab"
org: "MOS"
category: "SOP"
department: "ENG"
notion:
  database: "Documents"
  publish: true
access_groups:
  - "Engineering"
  - "Operations"
lifecycle:
  desired_state: "draft"
---
```

### 7.2 Required fields

| Field | Description |
|---|---|
| `doc_uid` | Unique identifier (see section 5). Use `"auto"` for automatic assignment. |
| `title` | Human-readable document title. |
| `org` | Organization code (e.g., `"MOS"`). |
| `category` | Category code (e.g., `"SOP"`). Must match the subfolder. |
| `department` | Department code (e.g., `"ENG"`). |
| `notion.database` | Notion database to publish to (usually `"Documents"`). |
| `notion.publish` | `true` to publish to Notion; `false` to keep in Git only. |
| `access_groups` | List of groups that should have access (e.g., `["All-Hands"]`, `["Engineering", "Leadership"]`). |
| `lifecycle.desired_state` | `"draft"`, `"release"`, or `"none"`. |

### 7.3 Optional fields

| Field | Description |
|---|---|
| `format_profile` | Template/ruleset for required sections (e.g., `"SOP_v1"`). Used by CI validation. |

---

## 8. Links and Images

### 8.1 Links to other documents

Use relative file paths to link to other Markdown documents in the repo:

```markdown
See the [Laser Safety SOP](../SOP/laser-safety.md) for details.
```

The pipeline resolves these to Notion page links at publish time. Because each document has a stable canonical Notion page, these links never go stale across revisions.

To link to a Notion page that isn't in the repo (e.g., a Lab Inventory database):

```markdown
Refer to the [Lab Inventory](https://www.notion.so/mosaicdesignlabs/13b4efc7c61080e9b35ed246cb753dde) for details.
```

External URLs are passed through as-is:

```markdown
See the [JLCPCB capabilities page](https://jlcpcb.com/capabilities) for tolerances.
```

### 8.2 Images

Use standard Markdown image syntax. The alt text becomes the caption in Notion:

```markdown
![Exploded view of the cartridge assembly, rev C](images/cartridge-exploded-revC.png)
```

- Store images in `docs/images/`.
- Use descriptive alt text — it serves as the caption in Notion and helps with search.
- To control image width in Notion, add a `|width=NNN` hint to the alt text:

```markdown
![Cartridge cross-section |width=400](images/cartridge-cross-section.png)
```

The pipeline strips the width hint from the displayed caption.

---

## 9. Drafting, Review, and Approval Workflow

### 9.1 Drafting

1. Create a new Markdown file in the appropriate category subfolder under `docs/`.
2. Add frontmatter with `doc_uid: "auto"` (or assign a UID manually), set `lifecycle.desired_state: "draft"`, and `notion.publish: true`.
3. Write your content. Use the format profile's required sections if one is specified (see the relevant SOP-writing or design-guide-writing SOPs for templates).
4. Commit and push to `main`. This can be a direct push — no pull request is required for drafts.

### 9.2 Draft publication

When you push to `main` with `publish: true`:

- The CI pipeline validates the document (frontmatter schema, required sections, link checks).
- If validation passes, the document is published to Notion as a **Draft**.
- The Notion page shows the current content, a revision history table, and is read-only with comments enabled.
- A redline (diff against the previous version) is generated and attached as a child page.

### 9.3 Review

Review happens naturally as people read the Draft in Notion and leave comments. For formal review:

- Share the document link with reviewers.
- Reviewers read the Notion page and leave inline comments or top-level comments.
- The author addresses comments by making edits in Git and pushing updates to `main` (each push generates a new draft revision with a redline).

### 9.4 Release

When the document is ready for release:

1. Open a **Pull Request** from `main` to `release` in Gitea.
2. The PR requires at least one approval (the number of required approvers is configured per-repo).
3. On merge, the pipeline publishes the document as **Released** — revision number increments to the next major version (e.g., draft `0.3` becomes release `1.0`).
4. A redline comparing the new release to the previous release is generated and attached as a child page.

### 9.5 Subsequent revisions

After release, further edits follow the same cycle: push to `main` to generate drafts, then PR to `release` when ready. The revision history table on the Notion page maintains a complete audit trail.

---

## 10. Notion-Native Documents

Some documents are created directly in Notion rather than in Git. This is acceptable when:

- The document requires Notion-native features that Markdown cannot represent (e.g., embedded databases, relation properties, synced blocks).
- The document is ephemeral or operational (e.g., meeting agendas, sprint boards).
- The document requires realtime collaboration (although generally such documents should go in the Lab Notebook, not Documents)

For Notion-native documents that require document control:

- Assign a `doc_uid` in the Notion database properties, following the same ORG-DEP-CAT-NNN format.
- The pipeline checks for `doc_uid` conflicts between Git-authored and Notion-native documents.

Notion-native documents do not benefit from automated redlines or the Git-based approval workflow. If a document needs formal version control, author it in Markdown.

---

## 11. Revision Numbering

Revisions are computed automatically. You never set a revision number manually.

| Event | Revision | Example |
|---|---|---|
| First draft publish | `0.1` | Author pushes new doc to `main` |
| Subsequent draft publishes | `0.2`, `0.3`, ... | Author pushes updates to `main` |
| First release | `1.0` | PR merged to `release` |
| Post-release drafts | `1.1`, `1.2`, ... | Author pushes updates to `main` after release |
| Second release | `2.0` | PR merged to `release` again |

The full document number displayed on the Notion page is `doc_uid.revision` (e.g., `MOS-OPS-SOP-001.2.0`).

---

## 12. Training

When a document is released (or updated to a new release), affected personnel must be trained on the changes. Training requirements are determined by the document's `access_groups` — everyone in the listed groups should review the new version.

Training records are managed separately (see the Training Records SOP — *to be created*). At a minimum:

- The document owner notifies affected groups when a new release is published.
- Personnel acknowledge that they have read and understood the document.
- Training completion is tracked in Notion.

Future plans may include AI-generated training quizzes based on document revisions.

---

## 13. Roles and Responsibilities

| Role | Responsibilities |
|---|---|
| **Author** | Drafts and edits documents in Git. Ensures frontmatter is correct. Addresses review comments. |
| **Reviewer** | Reads drafts in Notion. Leaves comments. Approves PRs for release. |
| **Document Owner** | Ensures the document stays current. Initiates reviews when changes are needed. Coordinates training. |
| **Pipeline (automated)** | Validates documents, assigns UIDs, computes revisions, publishes to Notion, generates redlines. |

---

## 14. Summary of Key Rules

1. **Every controlled document gets a `doc_uid`.** No exceptions.
2. **Markdown in Git is the primary authoring format.** Use Notion-native documents only when Markdown can't do the job.
3. **Frontmatter is required.** The pipeline will reject documents without valid frontmatter.
4. **Category determines the subfolder.** `SOP/` for SOPs, `POL/` for policies, etc.
5. **Filenames are kebab-case.** Lowercase, hyphens, `.md` extension.
6. **Drafts are published by pushing to `main`.** No PR required.
7. **Releases require a PR to `release` with at least one approval.**
8. **Notion is read-only.** All edits happen in Git. Comments are welcome in Notion.
9. **Redlines are generated automatically** for both drafts and releases.
10. **The revision history table** on each Notion page is the audit trail. Don't delete it.

---

## 15. Related Documents

| Document | Description |
|---|---|
| [Engineering Onboarding Guide](../POL/engineering-onboarding.md) | Overview of tools, processes, and how we work |
| [Git-to-Notion Pipeline Spec](../../scripts/git-to-notion-doc-control-spec.md) | Technical specification for the publishing pipeline |
| *How to Write a Good SOP* | *(To be created)* — Template and guidance for SOP authors |
| *Training Records SOP* | *(To be created)* — How training is tracked and managed |
