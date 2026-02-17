"""
Publishing orchestration for the document control pipeline.

Handles the complete draft and release publishing workflows:
1. Parse and validate documents
2. Auto-assign doc_uid if needed
3. Resolve internal links to Notion page IDs
4. Convert Markdown to Notion blocks
5. Create or update the canonical page (with archiving)
6. Generate redlines
7. Update the revision history table
"""

from __future__ import annotations

import logging
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from notion_client import Client

from .config import PipelineConfig
from .frontmatter import ParsedDoc, parse_doc, parse_all_docs
from .md_to_notion import markdown_to_blocks, _text
from .notion_api import (
    get_client,
    query_page_by_uid,
    get_page_blocks,
    get_page_revision,
    get_page_status,
    get_page_sha,
    build_page_properties,
    build_revision_history_table,
    build_revision_history_row,
    build_footer_blocks,
    create_page,
    update_page_properties,
    replace_page_content,
    create_archive_page,
    create_redline_page,
    delete_all_blocks,
    append_blocks,
)
from .redline import build_redline_blocks
from .uid import assign_uid, commit_uid_assignment
from .validate import validate_doc

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Revision computation
# ---------------------------------------------------------------------------


def compute_next_revision(current_rev: str, is_release: bool) -> str:
    """
    Compute the next revision number.

    Draft: N.M -> N.(M+1), or 0.1 for first publish.
    Release: N.M -> (N+1).0 if N >= 1, else 0.M -> 1.0.
    """
    if not current_rev or current_rev == "0.0":
        return "1.0" if is_release else "0.1"

    parts = current_rev.split(".")
    if len(parts) != 2:
        return "1.0" if is_release else "0.1"

    major, minor = int(parts[0]), int(parts[1])

    if is_release:
        return f"{major + 1}.0"
    else:
        return f"{major}.{minor + 1}"


# ---------------------------------------------------------------------------
# Link resolution
# ---------------------------------------------------------------------------


def build_page_id_lookup(client: Client, database_id: str,
                         all_docs: list[ParsedDoc]) -> dict[str, str]:
    """
    Build a mapping from doc_uid -> Notion page ID for all published docs.
    Used for resolving internal links.
    """
    lookup: dict[str, str] = {}
    for doc in all_docs:
        uid = doc.doc_uid
        if not uid or uid == "auto":
            continue
        page = query_page_by_uid(client, database_id, uid)
        if page:
            lookup[uid] = page["id"]
    return lookup


# ---------------------------------------------------------------------------
# Changed file detection
# ---------------------------------------------------------------------------


def get_changed_docs(config: PipelineConfig) -> list[Path]:
    """
    Determine which docs changed in the current push.
    Falls back to all docs if git diff fails.
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            cwd=config.repo_root,
            capture_output=True, text=True, check=True,
        )
        changed = []
        for line in result.stdout.strip().splitlines():
            path = config.repo_root / line
            if (path.suffix == ".md"
                    and path.is_file()
                    and str(path).startswith(str(config.docs_dir))):
                changed.append(path)
        if changed:
            logger.info("Detected %d changed doc(s)", len(changed))
            return changed
    except subprocess.CalledProcessError:
        logger.warning("git diff failed; falling back to all docs")

    # Fallback: return all docs
    return [d.path for d in parse_all_docs(config.docs_dir)]


# ---------------------------------------------------------------------------
# Reconstruct previous markdown from archive
# ---------------------------------------------------------------------------


def get_previous_markdown(client: Client, page_id: str,
                          current_revision: str) -> str:
    """
    Get the markdown content of the previous version by reading the
    current page blocks before they're replaced.

    Since we always archive before replacing, we read the current
    page content. This is called BEFORE the page is cleared.
    """
    blocks = get_page_blocks(client, page_id)
    return _blocks_to_plain_text(blocks)


def _blocks_to_plain_text(blocks: list[dict]) -> str:
    """
    Extract plain text from Notion blocks for diffing purposes.
    Not a perfect Markdown reconstruction, but sufficient for redlines.
    """
    lines: list[str] = []
    for block in blocks:
        btype = block.get("type", "")
        data = block.get(btype, {})

        if btype in ("paragraph", "quote", "callout",
                      "bulleted_list_item", "numbered_list_item"):
            rt = data.get("rich_text", [])
            text = "".join(r.get("plain_text", "") for r in rt)
            if btype == "bulleted_list_item":
                text = f"- {text}"
            elif btype == "numbered_list_item":
                text = f"1. {text}"
            elif btype == "quote":
                text = f"> {text}"
            lines.append(text)

        elif btype.startswith("heading_"):
            level = btype[-1]
            rt = data.get("rich_text", [])
            text = "".join(r.get("plain_text", "") for r in rt)
            lines.append(f"{'#' * int(level)} {text}")

        elif btype == "code":
            rt = data.get("rich_text", [])
            text = "".join(r.get("plain_text", "") for r in rt)
            lang = data.get("language", "")
            lines.append(f"```{lang}")
            lines.append(text)
            lines.append("```")

        elif btype == "divider":
            lines.append("---")

        elif btype == "table":
            # Tables are complex; extract row text
            children = block.get("children", data.get("children", []))
            if not children:
                # Need to fetch children separately if not included
                pass
            for row_block in children:
                row_data = row_block.get("table_row", {})
                cells = row_data.get("cells", [])
                cell_texts = []
                for cell in cells:
                    ct = "".join(r.get("plain_text", "") for r in cell)
                    cell_texts.append(ct)
                lines.append("| " + " | ".join(cell_texts) + " |")

        elif btype == "image":
            caption = data.get("caption", [])
            cap_text = "".join(r.get("plain_text", "") for r in caption)
            lines.append(f"![{cap_text}](image)")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Revision history parsing
# ---------------------------------------------------------------------------


def _parse_existing_history_rows(blocks: list[dict]) -> list[list[list[dict]]]:
    """
    Extract revision history rows from the first table in the page blocks.
    Returns the data rows (excluding header).
    """
    for block in blocks:
        if block.get("type") == "table":
            table_data = block.get("table", {})
            children = table_data.get("children", [])
            if not children:
                continue
            rows = []
            for i, row_block in enumerate(children):
                if i == 0:
                    continue  # Skip header row
                cells = row_block.get("table_row", {}).get("cells", [])
                rows.append(cells)
            return rows
    return []


# ---------------------------------------------------------------------------
# Core publish logic
# ---------------------------------------------------------------------------


def publish_doc(
    doc: ParsedDoc,
    config: PipelineConfig,
    client: Client,
    is_release: bool = False,
    all_docs: list[ParsedDoc] | None = None,
    page_id_lookup: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Publish a single document. Returns a result dict with status info.

    This is the heart of the pipeline:
    1. Handle auto-UID assignment
    2. Query for existing canonical page
    3. Compute next revision
    4. Check idempotency
    5. Archive current content (if updating)
    6. Generate redline (if updating)
    7. Convert markdown to Notion blocks
    8. Create or update the canonical page
    9. Build and prepend revision history table
    10. Add footer
    """
    result: dict[str, Any] = {
        "doc_uid": doc.doc_uid,
        "file": str(doc.path.name),
        "status": "unknown",
    }

    # --- Step 1: Auto-UID ---
    doc_uid = doc.doc_uid
    if doc.needs_auto_uid:
        doc_uid = assign_uid(doc, client, config)
        commit_uid_assignment(doc.path, doc_uid, config)
        # Re-parse the file after write-back
        doc = parse_doc(doc.path)
        result["doc_uid"] = doc_uid
        result["auto_assigned"] = True

    # --- Eligibility check ---
    if not doc.publish:
        result["status"] = "skipped"
        result["reason"] = "publish is false"
        return result

    desired = doc.desired_state
    if is_release and desired != "release":
        result["status"] = "skipped"
        result["reason"] = f"desired_state is '{desired}', not 'release'"
        return result
    if not is_release and desired not in ("draft", "release"):
        result["status"] = "skipped"
        result["reason"] = f"desired_state is '{desired}'"
        return result

    # --- Step 2: Query for canonical page ---
    existing_page = query_page_by_uid(client, config.notion_database_id, doc_uid)

    # --- Step 3: Compute revision ---
    if existing_page:
        current_rev = get_page_revision(existing_page)
        current_status = get_page_status(existing_page)
        current_sha = get_page_sha(existing_page)
    else:
        current_rev = "0.0"
        current_status = ""
        current_sha = ""

    next_rev = compute_next_revision(current_rev, is_release)
    status_label = "Released" if is_release else "Draft"

    # --- Step 4: Idempotency check ---
    if (existing_page
            and current_rev == next_rev
            and current_sha == config.git_commit_sha):
        result["status"] = "no-op"
        result["reason"] = "already published at this revision and commit"
        result["revision"] = current_rev
        logger.info("%s: already published (rev %s, sha %s) — skipping",
                    doc_uid, current_rev, config.git_commit_sha[:8])
        return result

    logger.info(
        "Publishing %s: %s -> %s (%s)",
        doc_uid, current_rev, next_rev, status_label,
    )

    # --- Step 5: Convert markdown to Notion blocks ---
    raw_url_base = config.raw_content_base_url
    content_blocks = markdown_to_blocks(doc, page_id_lookup, raw_url_base)

    # --- Step 6: Build properties ---
    source_path = str(doc.path.relative_to(config.repo_root))
    properties = build_page_properties(
        doc_uid=doc_uid,
        title=doc.title,
        category=doc.category,
        department=doc.department,
        org=doc.org,
        revision=next_rev,
        status=status_label,
        access_groups=doc.access_groups,
        publish=True,
        git_sha=config.git_commit_sha,
        git_pr=config.git_pr_url,
        git_repo=f"{config.gitea_url}/{config.gitea_repo_owner}/{config.gitea_repo_name}"
        if config.gitea_url else "",
        source_path=source_path,
        format_profile=doc.format_profile,
    )

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if existing_page is None:
        # ===== FIRST PUBLISH =====
        logger.info("%s: first publish — creating canonical page", doc_uid)

        # Build revision history with one row
        history_row = build_revision_history_row(
            revision=next_rev,
            status=status_label,
            date=today,
        )
        history_table = build_revision_history_table([history_row])

        # Assemble full page: history table + content + footer
        footer = build_footer_blocks(config.git_commit_sha, config.git_pr_url)
        all_blocks = [history_table] + content_blocks + footer

        page = create_page(client, config.notion_database_id,
                           properties, all_blocks)

        result["status"] = "created"
        result["revision"] = next_rev
        result["notion_page_id"] = page["id"]
        result["notion_url"] = page.get("url", "")

    else:
        # ===== SUBSEQUENT PUBLISH =====
        page_id = existing_page["id"]
        logger.info("%s: updating canonical page %s", doc_uid, page_id)

        # Read current content for archiving and diffing
        current_blocks = get_page_blocks(client, page_id)
        old_markdown = _blocks_to_plain_text(current_blocks)

        # Parse existing revision history rows
        existing_history = _parse_existing_history_rows(current_blocks)

        # Archive current content
        archive_page = create_archive_page(
            client, page_id, doc_uid, current_rev, current_blocks,
        )
        archive_page_id = archive_page["id"]
        logger.info("%s: archived v%s as child page %s",
                    doc_uid, current_rev, archive_page_id)

        # Generate redline
        redline_page_id = None
        if current_rev != "0.0":
            new_markdown = doc.content
            redline_blocks = build_redline_blocks(
                doc_uid=doc_uid,
                prev_revision=current_rev,
                new_revision=next_rev,
                old_markdown=old_markdown,
                new_markdown=new_markdown,
                git_sha=config.git_commit_sha,
                pr_url=config.git_pr_url,
            )
            redline_page = create_redline_page(
                client, page_id, doc_uid, current_rev, next_rev,
                redline_blocks,
            )
            redline_page_id = redline_page["id"]
            logger.info("%s: created redline v%s -> v%s as child page %s",
                        doc_uid, current_rev, next_rev, redline_page_id)

        # Build new revision history
        new_row = build_revision_history_row(
            revision=next_rev,
            status=status_label,
            date=today,
            redline_page_id=redline_page_id,
            redline_label=f"v{current_rev} \u2192 v{next_rev}" if redline_page_id else "",
            # Current version has no archive link (it IS the live page)
            archive_page_id=None,
            archive_label="",
        )

        # Update the previous "current" row to include its archive link
        if existing_history:
            # The first data row was the previous "current" — add archive link
            prev_row = existing_history[0]
            if len(prev_row) >= 5:
                prev_row[4] = [{
                    "type": "text",
                    "text": {
                        "content": f"v{current_rev}",
                        "link": {"url": f"/{archive_page_id}"},
                    },
                }]

        all_history_rows = [new_row] + existing_history
        history_table = build_revision_history_table(all_history_rows)

        # Clear page and write new content
        footer = build_footer_blocks(config.git_commit_sha, config.git_pr_url)
        all_blocks = [history_table] + content_blocks + footer

        replace_page_content(client, page_id, all_blocks)

        # Update properties
        update_page_properties(client, page_id, properties)

        result["status"] = "updated"
        result["revision"] = next_rev
        result["previous_revision"] = current_rev
        result["notion_page_id"] = page_id
        result["archive_page_id"] = archive_page_id
        result["redline_page_id"] = redline_page_id

    logger.info(
        "%s: published as %s v%s",
        doc_uid, status_label, next_rev,
    )
    return result


# ---------------------------------------------------------------------------
# Batch publish
# ---------------------------------------------------------------------------


def publish_changed_docs(
    config: PipelineConfig,
    is_release: bool = False,
    doc_paths: list[Path] | None = None,
) -> list[dict[str, Any]]:
    """
    Publish all changed (or specified) documents.

    Returns a list of result dicts, one per document processed.
    """
    client = get_client(config)

    # Skip bot commits to prevent infinite loops
    if config.git_actor == config.bot_commit_author:
        logger.info("Skipping pipeline — commit by bot account '%s'",
                     config.bot_commit_author)
        return [{"status": "skipped", "reason": "bot commit"}]

    # Determine which files to process
    if doc_paths:
        paths = doc_paths
    else:
        paths = get_changed_docs(config)

    if not paths:
        logger.info("No changed docs to publish")
        return []

    # Parse all docs for cross-reference
    all_docs = parse_all_docs(config.docs_dir)

    # Build page ID lookup for link resolution
    page_id_lookup = build_page_id_lookup(
        client, config.notion_database_id, all_docs
    )

    results: list[dict[str, Any]] = []
    for path in paths:
        try:
            doc = parse_doc(path)

            # Validate before publishing
            validation = validate_doc(doc, all_docs, config)
            if not validation.ok:
                logger.error(
                    "%s: validation failed:\n  %s",
                    path.name, "\n  ".join(validation.errors),
                )
                results.append({
                    "doc_uid": doc.doc_uid,
                    "file": path.name,
                    "status": "error",
                    "errors": validation.errors,
                })
                continue

            if validation.warnings:
                for warn in validation.warnings:
                    logger.warning("  %s", warn)

            pub_result = publish_doc(
                doc=doc,
                config=config,
                client=client,
                is_release=is_release,
                all_docs=all_docs,
                page_id_lookup=page_id_lookup,
            )
            results.append(pub_result)

        except Exception:
            logger.exception("Failed to publish %s", path.name)
            results.append({
                "file": str(path.name),
                "status": "error",
                "reason": "unhandled exception",
            })

    return results
