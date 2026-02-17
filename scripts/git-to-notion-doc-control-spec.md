# SPEC: Git → Notion Document Control Pipeline (Gitea)

**Owner:** Mosaic Engineering LLC (Mosaic Design Labs)  
**Status:** Draft  
**Scope:** Markdown documents in Git repositories, published as read-only pages in a single Notion “Documents” database with revisioning, redlines, and auditable linkage to Git commits/PRs.

---

## 1. Goals

1. **Single source of truth in Git** for all documents (SOPs, policies, design guides, work instructions, templates, proposals, literature reviews, etc.).
2. **Controlled publishing to Notion** into a specified Notion database (“Documents”) with:
   - status (`Draft`, `Released`)
   - revision numbers auto-managed
   - links to Notion pages auto-managed
   - sharing and group permissions auto-managed
   - strict read-only in Notion (comments allowed)
   - traceability to Git commit + PR
   - embedded images with captions
3. **Approval workflow enforced by Gitea** (protected branches + required checks + required approvers).
4. **Automated validation** of doc format (YAML frontmatter + section rules + linting).
5. **Redlined version in Notion** attached as a child page beneath the published doc.
6. **Idempotent + reproducible** publishing pipeline with a clear audit trail.

---

## 2. Non-goals

- Editing content in Notion (Notion is a publication surface only).
- Full QMS/QSR e-signature system (this spec supports approvals via Git PR review + audit metadata).

---

## 3. Terminology

- **Doc source**: Markdown file in Git.
- **Draft**: Published to Notion with status `Draft`, read-only, commentable.
- **Release**: Published to Notion with status `Released`, read-only, commentable.
- **Canonical page**: The single, stable Notion page for a given `doc_uid`. Always contains the current version. Its Notion page ID never changes.
- **Archive**: A child page beneath the canonical page containing a snapshot of a previous revision's content.
- **Doc UID**: Stable identifier for a document across revisions (not the Notion page ID).

---

## 4. High-level workflow

Each `doc_uid` has exactly **one canonical Notion page** that is always the current version. The pipeline creates this page on first publish and updates it in place on every subsequent publish. Previous content is preserved as archive child pages, and a **revision history table** at the top of the page links to all prior versions and redlines.

### 4.1 Authoring + Draft publishing

1. Author creates/edits a Markdown doc and commits to `main` (direct push or via PR — both are allowed).
2. On push to `main`, pipeline runs:
   - CI validation (YAML schema, markdown formatting, link checks, required section checks)
   - If validation passes and `publish: true`, publishes as **Draft**:
     - If no canonical page exists for this `doc_uid`, create one in the "Documents" database.
     - If a canonical page already exists, **archive** the current content as a child page (e.g., `Archive: MOS-ENG-SOP-012 v0.1`).
     - Update the canonical page in place with the new content.
     - Increment revision to next draft rev (e.g., `0.2`).
     - Update database properties: Status = `Draft`, Revision, Git SHA (+ PR info if available).
     - Prepend a row to the **revision history table** at the top of the page.
     - Generate a **redline child page** comparing the previous version to the new Draft.
     - Page remains locked/read-only; comments allowed.

### 4.2 Release publishing

1. A "Release PR" is opened from `main` → `release`.
2. Same CI runs as above.
3. On merge to `release`, pipeline publishes as **Released**:
   - **Archive** the current content as a child page.
   - Update the canonical page in place with the new content.
   - Revision becomes next major release (`0.3` draft → `1.0`; `1.2` draft → `2.0`).
   - Update database properties: Status = `Released`, Revision, Git SHA + PR info.
   - Prepend a row to the **revision history table**.
   - Generate a **redline child page** comparing the previous Released version to the new Released version.
   - Page remains locked/read-only; comments allowed.

---

## 5. Repository layout

Recommended:

```
repo/
  docs/
    SOP/                                  # Standard Operating Procedures
      laser-safety.md
      pcb-ordering.md
    POL/                                  # Policies and guidelines
      engineering-onboarding.md
      document-control.md
    DG/                                   # Design Guides and engineering references
      how-to-be-an-engineer.md
    STR/                                  # Strategy — vision, plans, frameworks
      mosaic-vision.md
      mosaic-business-plan.md
    GOV/                                  # Governance — charters, entity structures
      advisory-committee-charter.md
      entity-structure-memo.md
    MKT/                                  # Marketing — one-pagers, pitch materials
      onepager-engineers.md
      onepager-investors.md
    WI/                                   # Work Instructions
      cleanroom-entry.md
    RPT/                                  # Reports
      thermal-validation-report.md
    images/
      cleanroom-flow-chart.png
      laser-safety-guarding.jpg
  templates/
    doc-template.md
  scripts/
    validate_docs.py
    publish_to_notion.py
    redline.py
  .gitea/workflows/
    docs-ci.yml
    docs-publish-draft.yml
    docs-publish-release.yml
```

Rules:

- All publishable docs live under `docs/`.
- File path is *not* the canonical doc identifier; frontmatter is.

### 5.1 Links

Documents frequently reference other documents, Notion pages, and external resources. We support three link types, all using standard Markdown syntax:

**1. Internal repo links (other Markdown docs in the repo)**

```markdown
See the [Laser Safety SOP](../SOP/laser-safety.md) for details.
```

Use relative file paths to other Markdown files in the `docs/` directory. The pipeline resolves these at publish time:

- Look up the target file's `doc_uid` from its frontmatter.
- Query Notion for the **canonical page** matching that `doc_uid`.
- Replace the link with a Notion page mention (which renders with the page title and icon).
- If the target file has `publish: false` or doesn't exist, the pipeline emits a validation warning.

Because each `doc_uid` has a **stable canonical page** that is updated in place (see section 4), these links never go stale when the target document is revised. The Notion page ID remains the same across all revisions, so bookmarks, sidebar favorites, and cross-document links are always valid.

In a local Markdown viewer (Obsidian, VS Code, GitHub), these render as normal clickable links to the file.

**2. Notion page links (pages not in the repo)**

```markdown
Refer to the [Lab Inventory](https://www.notion.so/mosaicdesignlabs/13b4efc7c61080e9b35ed246cb753dde) for details.
```

Use the full Notion page URL. The pipeline detects `notion.so` URLs and converts them to Notion page mentions (rendered with the page title and icon inline). This is how you link to Notion-native pages — databases, views, or any page that doesn't have a corresponding Markdown source file.

In a local Markdown viewer, these render as standard hyperlinks to the Notion page (the reader would need to be logged in to view).

**3. External URLs**

```markdown
See the [JLCPCB capabilities page](https://jlcpcb.com/capabilities) for tolerances.
```

Standard hyperlinks. These are passed through as-is to Notion and render as normal links in both Markdown viewers and Notion.

**Validation:** The CI pipeline checks all links:

- Internal repo links: target file must exist and contain valid frontmatter.
- Notion URLs: optionally validate that the page ID resolves (requires API call; may be non-blocking).
- External URLs: optionally check for 404s (non-blocking warning).

### 5.2 Images

Use standard Markdown image syntax. The **alt text becomes the caption** in both Notion and Markdown viewers:

```markdown
![Exploded view of the cartridge assembly, rev C](images/cartridge-exploded-revC.png)
```

**File location:** Store images in `docs/images/`. Reference them with relative paths from the document.

**How it renders:**

| Context | Behavior |
|---|---|
| **Notion** | Image uploaded as a Notion image block, displayed at full column width, with the alt text rendered as the caption below the image. |
| **Obsidian / VS Code / GitHub** | Image displayed inline with alt text visible on hover (or as a caption in renderers that support it, like Obsidian with certain plugins). |

**Sizing:** The pipeline renders images at **full column width** by default in Notion. If you need to override the size, use an HTML-style attribute hint in the alt text:

```markdown
![Cartridge cross-section |width=400](images/cartridge-cross-section.png)
```

The pipeline parses the `|width=NNN` suffix from the alt text, applies it as the Notion image width (in pixels), and strips it from the displayed caption. In a local Markdown viewer, the hint is visible in the alt text but does not affect rendering — an acceptable tradeoff for simplicity.

**Captions:** Keep captions descriptive — include what the image shows and, when relevant, the revision or date. Good captions make images useful in isolation (e.g., when browsing the Notion database or searching).

**Image naming:** Use descriptive, kebab-case filenames that include the document context:

```
images/cartridge-exploded-revC.png
images/pcb-layout-top-v2.png
images/test-fixture-thermal-chamber.jpg
```

**Validation:** The CI pipeline checks that:

- All image paths in documents resolve to actual files in the repo.
- Image files in `docs/images/` are referenced by at least one document (optional; warns on orphaned images).

---

## 6. YAML frontmatter schema

### 6.1 Doc UID format

`doc_uid` is the **single canonical identifier** for a document across all revisions. It encodes the owning organization, department, category, and a sequential number:

```
ORG-DEP-CAT-NNN
```

Examples:

- `MOS-ENG-SOP-012` — Mosaic, Engineering, SOP, document 012
- `POP-ENG-RPT-003` — Poppy Health, Engineering, Report, document 003
- `MOS-OPS-POL-001` — Mosaic, Operations, Policy, document 001

The full document number as displayed (including revision) is `ORG-DEP-CAT-NNN.REV` (e.g., `MOS-ENG-SOP-012.1`), but `doc_uid` does not include the revision — revision is computed separately (see section 7).

### 6.2 Example frontmatter

```yaml
---
doc_uid: "auto"                      # or a specific UID like "MOS-ENG-SOP-012"; see auto-assignment below
title: "Laser Safety in the Lab"     # required
org: "MOS"                           # required: owning organization (e.g., "MOS", "POP", "XCC", "ACC")
category: "SOP"                      # enum, required (SOP, POL, WI, RPT, DG, STR, GOV, MKT, PRO, etc.)
department: "ENG"                    # enum, required (ENG, OPS, FIN, BD)
notion:
  database: "Documents"              # required (logical name), maps to Notion DB ID in config
  publish: true                      # required boolean: false => stays in Git only
access_groups:                       # required list (can be empty if public-internal)
  - "Engineering"
  - "Operations"
lifecycle:
  desired_state: "draft"             # "draft" | "release" | "none"
  # "none" means never publish; publish=false is preferred for clarity
format_profile: "SOP_v1"             # optional: determines required sections/ruleset
---
```

### 6.3 Required fields

- `title`, `org`, `category`, `department`, `notion.database`, `notion.publish`, `access_groups`, `lifecycle.desired_state`
- `doc_uid` is required but may be set to `"auto"` for auto-assignment (see 6.5)

`doc_uid` is the single canonical identifier. It is composed from `org`, `department`, `category`, and a zero-padded sequential number. There is no separate `doc_number` field.

### 6.4 Notion-native pages

Users may create pages directly in the Notion "Documents" database that are not backed by a file in Git. This preserves the full flexibility of Notion for content that cannot be represented in Markdown alone (e.g., databases, embedded views, complex layouts).

The pipeline must be robust to this:

- On publish, query Notion for existing `doc_uid` values and **never overwrite or conflict with a Notion-native page**.
- Notion-native pages should use a distinct `doc_uid` prefix or range (e.g., `N-XXXX`) to avoid collisions, or the pipeline should simply skip any page whose `doc_uid` does not match a Git-tracked document.
- The validation step should warn if a `doc_uid` in a Git document already exists in Notion and is not pipeline-managed (i.e., missing a `Git Commit SHA`).

### 6.5 Auto-assignment of `doc_uid`

When a new document is pushed with `doc_uid: "auto"`, the pipeline:

1. Reads `org`, `department`, and `category` from the frontmatter.
2. Queries the Notion "Documents" database for all existing `doc_uid` values matching the prefix `{org}-{department}-{category}-*`.
3. Also scans all Git-tracked documents for `doc_uid` values with the same prefix (to catch docs with `publish: false` that aren't in Notion).
4. Determines the next available sequential number (zero-padded to 3 digits).
5. Constructs the `doc_uid` (e.g., `MOS-ENG-SOP-013`).
6. **Writes the assigned `doc_uid` back into the file's YAML frontmatter**, replacing `"auto"`.
7. Commits the change to the repo with a message like `docs: assign doc_uid MOS-ENG-SOP-013`.
8. Proceeds with the normal draft publishing flow.

**Implementation considerations:**

- **Avoid infinite loops.** The pipeline's own commit will trigger another push event. Guard against this by checking the commit author (e.g., skip pipeline if author is the bot account) or by checking whether `doc_uid` is already assigned (not `"auto"`).
- **Race conditions.** If two new docs are pushed near-simultaneously, they could both query and get the same next number. Mitigate by serializing the assignment step (e.g., a lightweight lock via a Notion counter row or a Git-based lock file).
- **Write access.** The pipeline needs push access to the repo. Use a Gitea bot account with scoped permissions.
- **Existing documents.** If `doc_uid` is already set to a valid UID (not `"auto"`), the pipeline skips auto-assignment and uses it as-is. This allows manual assignment when needed.

### 6.6 Disallowed / computed fields

These fields are **not allowed in source** (computed at publish time and stored in Notion + optionally in a sidecar):

- `revision` (computed)
- `status` (computed from publishing event: Draft/Released)
- `git_commit`, `git_pr`, `published_at`, `notion_page_id`

### 6.7 Storage of computed metadata

Preferred approach:

- Store computed metadata in **Notion only** and optionally in a machine-readable **sidecar file** in Git:
  - `docs/.meta/MOS-ENG-SOP-012.json`
  - generated by pipeline on release branch only (or stored externally in DB)

This prevents authors from “hand-editing” audit fields.

---

## 7. Revisioning rules

### 7.1 Revision format

`MAJOR.MINOR` with:

- Drafts increment MINOR
- Releases increment MAJOR and reset MINOR to 0

Examples:

- First draft: `0.1`
- Additional drafts: `0.2`, `0.3`, …
- First release: `1.0`
- Post-release drafts: `1.1`, `1.2`, …
- Next release: `2.0`

### 7.2 How revision is computed

Revision is computed at publish time using the canonical Notion page as the source of truth:

1. Query Notion “Documents” database for the canonical page matching `doc_uid`.
2. Read the current `Revision` and `Status` properties from that page.
3. Determine the next revision based on the publish event:
   - Draft publish event:
     - If no page exists yet (first publish): `0.1`
     - If current revision is `N.M` (any status): next is `N.(M+1)`
   - Release publish event:
     - If current revision is `0.M`: next is `1.0`
     - If current revision is `N.M` where `N >= 1`: next is `(N+1).0`
4. Update the canonical page’s `Revision` and `Status` properties.

### 7.3 Archiving prior versions

There is no concept of “Obsolete” top-level database rows. Each `doc_uid` has exactly one row in the database (the canonical page), and its properties always reflect the current version.

When the canonical page is updated, the pipeline first copies the current content to an **archive child page** beneath the canonical page:

- Title: `Archive: <doc_uid> v<revision>` (e.g., `Archive: MOS-ENG-SOP-012 v0.2`)
- Content: full snapshot of the previous page body
- The archive is a static record and is not updated after creation.

Archive child pages are linked from the **revision history table** at the top of the canonical page (see section 9.2), providing a browsable version history directly within Notion.

---

## 8. Branching strategy (best practices)

### 8.1 Branches

- `main`: **integration branch** for ongoing edits; merging here produces/updates **Draft** publications.
- `release`: **release branch**; merging here produces **Released** publications.

Rationale:

- Keeps “draft publishing” and “release publishing” separable and enforceable with different rules.
- Avoids ambiguity of tags-only workflows while staying simple for a small team.

### 8.2 Allowed flows

- **Direct push to `main`** — for routine drafts and edits (no PR required)
- **Feature branch → `main` via PR** — optional, for larger changes or when you want review before merging
- **`main` → `release` via PR** — required for all releases (may batch multiple docs)

### 8.3 Protections / enforcement

**`main` (open for direct pushes):**

- Direct pushes allowed
- CI validation runs on every push (YAML schema, markdown lint, link checks)
- If validation fails, pipeline posts a warning to Slack but does not block the push
- PRs are optional but encouraged for large or cross-functional changes

**Protect `release`:**

- No direct pushes
- Require PR from `main`
- Require CI checks pass
- Require at least 2 approvals, including an “Approver” group member
- Require “fresh” approvals (dismiss approvals on new commits)

### 8.4 Naming conventions

- Feature branches: `doc/<doc_uid>/<short-slug>` e.g. `doc/MOS-ENG-SOP-012/add-ppe-section`
- Release branches (optional): `rel/<YYYY-MM-DD>` or `rel/<version>` created temporarily for batch releases
- Tags (optional): `docs/<doc_uid>/v2.0` on successful release publish, for Git traceability.

---

## 9. Notion data model

### 9.1 Single “Documents” database properties

There is exactly **one row per `doc_uid`** in the database. Properties always reflect the current (latest) version.

Required properties:

- `Doc UID` (text) — the stable canonical identifier
- `Title` (title)
- `Category` (select)
- `Department` (select)
- `Org` (select) e.g., `MOS`, `POP`, `XCC`
- `Revision` (text) e.g., `1.2` — always the current revision
- `Status` (select: Draft, Released) — always the current status
- `Access Groups` (multi-select)
- `Publish Enabled` (checkbox)
- `Git Commit SHA` (text) — the commit that produced the current version
- `Git PR` (text/url)
- `Git Repo` (text/url)
- `Published At` (date) — when the current version was published
- `Source Path` (text)
- `Format Profile` (select)

Note: The `Obsolete` status value is no longer used for top-level database rows. Version history is maintained through archive child pages (see 9.2).

### 9.2 Page structure

Each canonical page has the following structure:

**1. Revision history table** (at the top of the page):

| Rev | Status | Date | Redline | Archive |
|---|---|---|---|---|
| 2.0 | Released | 2026-02-16 | v1.0 → v2.0 | — |
| 1.0 | Released | 2025-11-03 | v0.1 → v1.0 | v1.0 |
| 0.3 | Draft | 2025-10-20 | v0.2 → v0.3 | v0.3 |
| 0.2 | Draft | 2025-10-15 | v0.1 → v0.2 | v0.2 |
| 0.1 | Draft | 2025-10-10 | — | v0.1 |

- The **current row** (top of table) has no archive link — it *is* the live page.
- **Redline** column links to the redline child page for that transition.
- **Archive** column links to the archived content child page.

**2. Document body** (markdown content rendered to Notion blocks).

**3. Footer**: “Published from Git” with commit SHA, PR link (if available), and timestamp.

**Child pages:**

- `Archive: <doc_uid> v<rev>` — full content snapshot of a previous revision
- `Redline: <doc_uid> v<prev> → v<new>` — diff between two versions

### 9.3 Read-only requirement

Enforcement approach:

- Notion permissions: give general viewers “Can comment” only.
- The integration/bot has edit rights but only used by the publisher.
- Any “owners” must also be restricted to comment-only in production database.

Note: Notion’s exact permission model depends on workspace tier and DB sharing; configure the DB and its parent page with comment-only access for human groups.

---

## 10. Publishing rules

### 10.1 Eligibility

A doc is eligible for publishing if:

- It is under `docs/`
- YAML frontmatter passes schema
- `notion.publish: true`
- `lifecycle.desired_state` matches the pipeline (draft/release)

Docs with `notion.publish: false` are ignored by publisher.

### 10.2 Draft publishing behavior

Event: push to `main` (direct push or merge)

1. **First publish** (no canonical page exists for this `doc_uid`):
   - Create a new page in the "Documents" database.
   - Set Revision = `0.1`, Status = `Draft`.
   - Render the revision history table with one row (no archive, no redline).
   - Render the document body and footer.

2. **Subsequent publishes** (canonical page already exists):
   - Create an **archive child page** with the current content (snapshot).
   - Generate a **redline child page** comparing the previous version to the new Draft (see section 11).
   - Clear and re-render the canonical page body with the new content.
   - Prepend a new row to the revision history table with links to the archive and redline child pages.
   - Update database properties: Revision (incremented), Status = `Draft`, Git SHA, Published At.

### 10.3 Release publishing behavior

Event: merge to `release`

1. Create an **archive child page** with the current content.
2. Generate a **redline child page** comparing the previous Released version (or initial content) to the new Released content (see section 11).
3. Clear and re-render the canonical page body with the new content.
4. Prepend a new row to the revision history table.
5. Update database properties: Revision (next major), Status = `Released`, Git SHA + PR info, Published At.

---

## 11. Redline generation

Redlines are generated on **both Draft and Release publishes** and stored as child pages beneath the canonical page.

### 11.1 What gets compared

**On Draft publish:**

- Compare the **archived version** (the content just archived in the previous step) to the new Draft content.
- If no prior version exists at all (first-ever draft), skip the redline. The revision history table row shows “—” in the Redline column.

**On Release publish:**

- Compare the **previous Released version** to the new Released content. The pipeline identifies the previous Released version by scanning the revision history table or archive child pages for the most recent entry with Status = `Released`.
- If no prior Released version exists, redline compares empty → new content (or skip redline and attach an “Initial Release” note).

### 11.2 Output format

Create a child page beneath the canonical page:

- Title: `Redline: <doc_uid> v<prev_rev> → v<new_rev>`
- Content:
  - Summary: what changed, commit SHA, PR link (if available)
  - Redline body:
    - either a rich-text diff with additions/deletions
    - or a block-by-block markdown diff rendering
  - Attachments (optional): a `.diff` text file and/or PDF

The redline child page is linked from the **Redline** column in the revision history table at the top of the canonical page.

### 11.3 Implementation notes

- Generate diff from markdown source before conversion to Notion blocks.
- Use a deterministic algorithm (e.g., word-level diff) to produce stable redlines.
- For drafts, the redline helps reviewers see what changed since the last version. For releases, it provides the formal record of changes between released versions.

---

## 12. Automation architecture (Gitea)

### 12.1 Triggers

- **CI/validation**: on push to `main`, on PR opened/updated targeting `release`
- **Draft publish**: on push to `main` (direct push or merge)
- **Release publish**: on merge to `release`

### 12.2 Execution

Use Gitea Actions with a self-hosted runner.

Workflows:

- `.gitea/workflows/docs-ci.yml`
- `.gitea/workflows/publish-draft.yml`
- `.gitea/workflows/publish-release.yml`

### 12.3 Secrets

- `NOTION_TOKEN`
- `NOTION_DATABASE_ID_DOCUMENTS` (or mapping file keyed by logical name)
- Optional: `GITEA_TOKEN` for PR comment backflow (posting CI summaries to PR thread)

### 12.4 PR feedback

On CI failure:

- Post a single “Validator Report” comment (update-in-place to avoid spam):
  - ✅/❌ checks
  - specific line/section errors
  - links to logs

---

## 13. Validation rules

### 13.1 YAML schema validation

- Required keys and types
- Enums for category/department/access_groups if desired

### 13.2 Document structure validation (profile-based)

Example `SOP_v1` required headings:

- Purpose
- Scope
- Responsibilities
- Definitions
- Safety
- Procedure
- Records
- Revision History

### 13.3 Formatting + hygiene

- Markdown linting
- Link checking (internal links must resolve)
- Forbidden patterns (e.g., raw HTML if disallowed)
- Optional: “Mosaic style” checks (terminology, tone, risky language)

---

## 14. Idempotency and update semantics

### 14.1 Idempotency key

Publishing should be safe to re-run:

- Idempotency key = `{doc_uid}:{target_revision}:{git_sha}`

Before updating the canonical page, check whether its current `Revision` and `Git Commit SHA` already match the target. If so, the publish is a no-op — do nothing.

### 14.2 Mapping Git → Notion

The pipeline must be able to look up the canonical Notion page for a given `doc_uid`. This is done by querying the “Documents” database for the row matching the `Doc UID` property. Since there is exactly one row per `doc_uid`, this query always returns zero or one result.

Stored in Notion page properties:

- `Doc UID` (the lookup key)
- `Git Commit SHA` (used for idempotency check)
- `Source Path`
- `Revision`

Optional external mapping store (for faster lookups without querying Notion):

- `docs/.meta/<doc_uid>.json` or a small internal DB table, containing the `notion_page_id` for each `doc_uid`.

---

## 15. Error handling and safety

- If Notion API fails mid-run, pipeline:
  - must not partially update the canonical page (e.g., archive created but body not yet replaced); use atomic-style sequencing
  - should retry safely (idempotency)
- If revision computation fails (e.g., conflicting revisions), pipeline stops and comments on PR.
- If multiple docs are released in one merge, each doc is handled independently, with independent rollback behavior.

---

## 16. Security & access control

### 16.1 Gitea

- Use teams: Authors, Approvers, Admins
- Protect branches; enforce required approvals and checks
- Use bot account with minimal permissions to post PR comments

### 16.2 Notion

- Human groups get “Can comment”
- Bot integration has edit permissions only to the Documents DB page tree
- Access groups in YAML map to Notion “Access Groups” property; enforcement is primarily via Notion sharing/permissions configuration (policy decision: whether to segment DB views by groups vs. true page-level permissions)

---

## 17. Implementation plan (phased)

### Phase 1: MVP

- YAML schema + markdown lint
- Draft publish on `main`
- Notion DB single database, read-only for humans
- Revisioning + Git metadata

### Phase 2: Release controls

- `release` branch
- Release publish + archive workflow
- Release PR approvals tightened

### Phase 3: Redlines

- Generate redline child page on both draft and release publishes
- Attach diff artifacts

### Phase 4: Enhanced review automation

- SOP profile validators
- “AI review comments” (non-blocking or blocking by policy)
- Dashboard/reporting

---

## 18. Open decisions (to finalize)

1. How to enforce “access_groups” in Notion (views vs page-level sharing).
2. Whether to store mapping metadata in Git sidecar files or solely in Notion.
3. Whether release merges should be single-doc only or allow batching.

---

## Appendix A: Deployment architecture

This pipeline spans two repositories:

- **`mosaic-docs`** — Contains the documents themselves (under `docs/`), the publishing scripts (under `scripts/`), and the Gitea Actions workflow definitions (under `.gitea/workflows/`). This is the repo that authors push to and that triggers the pipeline.
- **`mosaic-server`** — Contains the Gitea server configuration, runner registration, Docker Compose setup, and infrastructure-level secrets management. This is the sister repo that runs the self-hosted Gitea instance.

**How they connect:** Gitea Actions reads `.gitea/workflows/` directly from the repo where the event occurs. So when a push lands on `main` in `mosaic-docs`, Gitea picks up `docs-publish-draft.yml` from that same repo and runs it on the self-hosted runner configured in `mosaic-server`. Secrets (`NOTION_TOKEN`, `NOTION_DATABASE_ID_DOCUMENTS`, etc.) are configured in Gitea's repository or organization settings, managed from the server side.

This keeps document-side concerns (scripts, validation logic, workflow definitions) co-located with the documents, while server-side concerns (infrastructure, secrets, runner lifecycle) live in `mosaic-server`. Authors never need to touch `mosaic-server`; infrastructure changes never require touching `mosaic-docs`.

---

## Appendix B: Example lifecycle

All actions below operate on a single canonical Notion page for `MOS-ENG-SOP-012`:

1. **Author pushes to `main` (first time):** Pipeline creates the canonical page. Revision = `0.1`, Status = `Draft`. Revision history table has one row. No archive, no redline.

2. **Next push to `main`:** Pipeline archives v0.1 content as a child page, updates the canonical page with new content. Revision = `0.2`, Status = `Draft`. Generates redline child page (v0.1 → v0.2). Revision history table now has two rows.

3. **Another push to `main`:** Archives v0.2, updates page. Revision = `0.3`. Redline (v0.2 → v0.3). Three rows in the table.

4. **Release PR merged to `release`:** Archives v0.3, updates page with released content. Revision = `1.0`, Status = `Released`. Redline compares last Released (none) → v1.0, or v0.3 → v1.0. Four rows in the table.

5. **Later edit pushed to `main`:** Archives v1.0, updates page. Revision = `1.1`, Status = `Draft`. Redline (v1.0 → v1.1). Five rows.

6. **Release PR merged:** Archives v1.1, updates page. Revision = `2.0`, Status = `Released`. Redline (v1.0 → v2.0). Six rows.

Throughout this entire lifecycle, the canonical page’s Notion page ID never changes. All links from other documents remain valid.
