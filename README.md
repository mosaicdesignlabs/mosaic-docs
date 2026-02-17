# mosaic-docs

Controlled document repository for Mosaic Design Labs. All SOPs, policies, design guides, strategy documents, governance charters, and marketing materials are authored here in Markdown and published to Notion through an automated pipeline.

For the full document control policy — categories, naming conventions, frontmatter requirements, revision numbering, and the drafting/review/approval workflow — see [Document Control SOP](docs/SOP/document-control.md).

## Repository layout

```
docs/
  SOP/          Standard Operating Procedures
  POL/          Policies and guidelines
  DG/           Design guides and engineering references
  STR/          Strategy — vision, plans, frameworks
  GOV/          Governance — charters, entity structures
  MKT/          Marketing — one-pagers, pitch materials
  WI/           Work instructions
  RPT/          Reports
  PRO/          Proposals
  images/       Shared images referenced by documents

scripts/
  docctl/       Python package — validation, Notion API, publishing logic
  validate_docs.py        CLI: validate documents
  publish_to_notion.py    CLI: publish documents to Notion
  git-to-notion-doc-control-spec.md   Pipeline specification

.gitea/workflows/
  docs-ci.yml             Validation on push to main / PR to release
  publish-draft.yml       Draft publish on push to main
  publish-release.yml     Release publish on merge to release
```

Every Markdown document under `docs/` has YAML frontmatter with a `doc_uid` (e.g. `MOS-ENG-SOP-012`), title, category, department, and publishing metadata. The pipeline uses this frontmatter to manage Notion pages, revision numbers, and access groups automatically.

## How the pipeline works

1. **Push to `main`** — CI validates all changed documents (frontmatter schema, link checks, image references). If validation passes and `publish: true`, the document is published to Notion as a **Draft**. Previous content is archived as a child page and a redline (diff) is generated.

2. **PR from `main` → `release`** — Same validation runs. On merge, the document is published as **Released** with a major revision bump (e.g. `0.3` → `1.0`). A redline comparing the two releases is attached.

3. **Auto-UID assignment** — Documents with `doc_uid: "auto"` get a UID assigned automatically. The pipeline writes it back to the file and commits.

Each `doc_uid` maps to exactly one Notion page that is updated in place across revisions. A revision history table at the top of the page links to archived snapshots and redlines.

## Local setup

**Requirements:** Python 3.10+

```bash
# Install dependencies
pip install -r requirements.txt

# Validate all documents
python scripts/validate_docs.py --repo-root .

# Validate specific files
python scripts/validate_docs.py docs/SOP/document-control.md
```

## Publishing (local or CI)

Publishing requires two environment variables:

```bash
export NOTION_TOKEN="secret_..."
export NOTION_DATABASE_ID_DOCUMENTS="your-database-id"
```

Then:

```bash
# Publish drafts (changed docs)
python scripts/publish_to_notion.py --mode draft --repo-root .

# Publish all docs as drafts (full re-publish)
python scripts/publish_to_notion.py --mode draft --all --repo-root .

# Publish releases
python scripts/publish_to_notion.py --mode release --all --repo-root .
```

In production, this runs automatically via Gitea Actions on the self-hosted Gitea instance (see `mosaic-server`). Secrets are configured in Gitea's repository settings.

## Writing a new document

1. Create a Markdown file in the appropriate category folder (e.g. `docs/SOP/my-new-sop.md`).
2. Add frontmatter — at minimum:

```yaml
---
doc_uid: "auto"
title: "My New SOP"
org: "MOS"
category: "SOP"
department: "ENG"
notion:
  database: "Documents"
  publish: true
access_groups:
  - "All-Hands"
lifecycle:
  desired_state: "draft"
---
```

3. Write your content in Markdown. Use relative links for cross-references (`[other doc](../POL/engineering-onboarding.md)`) and put images in `docs/images/`.
4. Push to `main`. The pipeline validates, assigns a UID if needed, and publishes to Notion.

For the full authoring guide, see the [Document Control SOP](docs/SOP/document-control.md).

## Key references

| Document | Description |
|---|---|
| [Document Control SOP](docs/SOP/document-control.md) | Categories, naming, frontmatter, workflow |
| [Pipeline Spec](scripts/git-to-notion-doc-control-spec.md) | Technical specification for the publishing pipeline |
| [Engineering Onboarding](docs/POL/engineering-onboarding.md) | How we work at Mosaic |
