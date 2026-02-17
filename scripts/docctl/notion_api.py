"""
Notion API wrapper for the document control pipeline.

Handles all interactions with the Notion API: querying the Documents
database, creating/updating pages, managing child pages (archives and
redlines), and building the revision history table.

Uses the official notion-client SDK.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from typing import Any

from notion_client import Client
from notion_client.errors import APIResponseError

from .config import PipelineConfig
from .md_to_notion import NOTION_MAX_BLOCKS_PER_REQUEST, _text

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Client factory
# ---------------------------------------------------------------------------


def get_client(config: PipelineConfig) -> Client:
    """Create a Notion client from config."""
    return Client(auth=config.notion_token)


# ---------------------------------------------------------------------------
# Database queries
# ---------------------------------------------------------------------------


def query_page_by_uid(client: Client, database_id: str,
                      doc_uid: str) -> dict | None:
    """Find the canonical page for a doc_uid. Returns the page object or None."""
    response = client.databases.query(
        database_id=database_id,
        filter={"property": "Doc UID", "rich_text": {"equals": doc_uid}},
        page_size=1,
    )
    results = response.get("results", [])
    return results[0] if results else None


def query_all_uids(client: Client, database_id: str,
                   prefix: str = "") -> list[str]:
    """Get all doc_uid values from the database, optionally filtered by prefix."""
    uids: list[str] = []
    cursor = None

    while True:
        kwargs: dict[str, Any] = {
            "database_id": database_id,
            "page_size": 100,
        }
        if prefix:
            kwargs["filter"] = {
                "property": "Doc UID",
                "rich_text": {"starts_with": prefix},
            }
        if cursor:
            kwargs["start_cursor"] = cursor

        response = client.databases.query(**kwargs)
        for page in response.get("results", []):
            uid_prop = page.get("properties", {}).get("Doc UID", {})
            rt = uid_prop.get("rich_text", [])
            if rt:
                uids.append(rt[0].get("plain_text", ""))

        if not response.get("has_more"):
            break
        cursor = response.get("next_cursor")

    return uids


# ---------------------------------------------------------------------------
# Page property helpers
# ---------------------------------------------------------------------------


def _rich_text_prop(value: str) -> dict:
    return {"rich_text": [{"text": {"content": value}}]}


def _title_prop(value: str) -> dict:
    return {"title": [{"text": {"content": value}}]}


def _select_prop(value: str) -> dict:
    return {"select": {"name": value}}


def _multi_select_prop(values: list[str]) -> dict:
    return {"multi_select": [{"name": v} for v in values]}


def _checkbox_prop(value: bool) -> dict:
    return {"checkbox": value}


def _date_prop(iso_str: str) -> dict:
    return {"date": {"start": iso_str}}


def _url_prop(value: str) -> dict:
    return {"url": value if value else None}


def build_page_properties(doc_uid: str, title: str, category: str,
                          department: str, org: str, revision: str,
                          status: str, access_groups: list[str],
                          publish: bool, git_sha: str, git_pr: str,
                          git_repo: str, source_path: str,
                          format_profile: str | None = None) -> dict:
    """Build the properties dict for a page create or update."""
    props: dict[str, Any] = {
        "Title": _title_prop(title),
        "Doc UID": _rich_text_prop(doc_uid),
        "Category": _select_prop(category),
        "Department": _select_prop(department),
        "Org": _select_prop(org),
        "Revision": _rich_text_prop(revision),
        "Status": _select_prop(status),
        "Access Groups": _multi_select_prop(access_groups),
        "Publish Enabled": _checkbox_prop(publish),
        "Git Commit SHA": _rich_text_prop(git_sha),
        "Git PR": _rich_text_prop(git_pr) if git_pr else _rich_text_prop(""),
        "Git Repo": _rich_text_prop(git_repo) if git_repo else _rich_text_prop(""),
        "Source Path": _rich_text_prop(source_path),
        "Published At": _date_prop(datetime.now(timezone.utc).isoformat()),
    }
    if format_profile:
        props["Format Profile"] = _select_prop(format_profile)
    return props


# ---------------------------------------------------------------------------
# Page content management
# ---------------------------------------------------------------------------


def get_page_blocks(client: Client, page_id: str) -> list[dict]:
    """Retrieve all blocks from a page."""
    blocks: list[dict] = []
    cursor = None

    while True:
        kwargs: dict[str, Any] = {"block_id": page_id, "page_size": 100}
        if cursor:
            kwargs["start_cursor"] = cursor

        response = client.blocks.children.list(**kwargs)
        blocks.extend(response.get("results", []))

        if not response.get("has_more"):
            break
        cursor = response.get("next_cursor")

    return blocks


def delete_all_blocks(client: Client, page_id: str) -> int:
    """Delete all blocks from a page. Returns the count of deleted blocks."""
    blocks = get_page_blocks(client, page_id)
    count = 0
    for block in blocks:
        try:
            client.blocks.delete(block_id=block["id"])
            count += 1
        except APIResponseError as e:
            logger.warning("Failed to delete block %s: %s", block["id"], e)
    return count


def append_blocks(client: Client, page_id: str,
                  blocks: list[dict]) -> list[dict]:
    """
    Append blocks to a page, batching to respect the 100-block limit.
    Returns the list of created block objects.
    """
    created: list[dict] = []

    for i in range(0, len(blocks), NOTION_MAX_BLOCKS_PER_REQUEST):
        batch = blocks[i:i + NOTION_MAX_BLOCKS_PER_REQUEST]
        response = client.blocks.children.append(
            block_id=page_id,
            children=batch,
        )
        created.extend(response.get("results", []))

        # Rate limiting: be polite
        if i + NOTION_MAX_BLOCKS_PER_REQUEST < len(blocks):
            time.sleep(0.35)

    return created


# ---------------------------------------------------------------------------
# Revision history table
# ---------------------------------------------------------------------------


def build_revision_history_row(
    revision: str,
    status: str,
    date: str,
    redline_page_id: str | None = None,
    redline_label: str = "",
    archive_page_id: str | None = None,
    archive_label: str = "",
) -> list[list[dict]]:
    """
    Build one row for the revision history table.
    Returns a list of cells, each cell being a list of rich_text objects.
    """
    rev_cell = [_text(revision)]
    status_cell = [_text(status)]
    date_cell = [_text(date)]

    if redline_page_id:
        redline_cell: list[dict] = [{
            "type": "text",
            "text": {
                "content": redline_label or f"Redline",
                "link": {"url": f"/{redline_page_id}"},
            },
        }]
    else:
        redline_cell = [_text("\u2014")]  # em-dash

    if archive_page_id:
        archive_cell: list[dict] = [{
            "type": "text",
            "text": {
                "content": archive_label or f"Archive",
                "link": {"url": f"/{archive_page_id}"},
            },
        }]
    else:
        archive_cell = [_text("\u2014")]

    return [rev_cell, status_cell, date_cell, redline_cell, archive_cell]


def build_revision_history_table(
    rows: list[list[list[dict]]],
) -> dict:
    """
    Build the complete revision history table block.
    Rows should be newest-first (prepend new rows to the list).
    """
    header = [
        [_text("Rev")],
        [_text("Status")],
        [_text("Date")],
        [_text("Redline")],
        [_text("Archive")],
    ]

    table_rows = [header] + rows
    children = []
    for row in table_rows:
        # Pad to 5 columns
        padded = row + [[_text("")] for _ in range(5 - len(row))]
        children.append({
            "type": "table_row",
            "table_row": {"cells": padded},
        })

    return {
        "type": "table",
        "table": {
            "table_width": 5,
            "has_column_header": True,
            "has_row_header": False,
            "children": children,
        },
    }


def build_footer_blocks(git_sha: str, pr_url: str = "",
                        timestamp: str = "") -> list[dict]:
    """Build the footer blocks: divider + 'Published from Git' note."""
    ts = timestamp or datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    parts = [_text(f"Published from Git \u2022 commit {git_sha[:8]}")]
    if pr_url:
        parts.append(_text(" \u2022 "))
        parts.append({
            "type": "text",
            "text": {"content": "PR", "link": {"url": pr_url}},
        })
    parts.append(_text(f" \u2022 {ts}"))

    return [
        {"type": "divider", "divider": {}},
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": parts,
                "color": "gray",
            },
        },
    ]


# ---------------------------------------------------------------------------
# Page creation and update
# ---------------------------------------------------------------------------


def create_page(client: Client, database_id: str,
                properties: dict, blocks: list[dict]) -> dict:
    """Create a new page in the database with properties and content."""
    # Notion API limits children to 100 blocks on create
    initial_blocks = blocks[:NOTION_MAX_BLOCKS_PER_REQUEST]
    remaining_blocks = blocks[NOTION_MAX_BLOCKS_PER_REQUEST:]

    page = client.pages.create(
        parent={"database_id": database_id},
        properties=properties,
        children=initial_blocks,
    )

    if remaining_blocks:
        append_blocks(client, page["id"], remaining_blocks)

    return page


def update_page_properties(client: Client, page_id: str,
                           properties: dict) -> dict:
    """Update a page's properties."""
    return client.pages.update(page_id=page_id, properties=properties)


def replace_page_content(client: Client, page_id: str,
                         new_blocks: list[dict]) -> None:
    """Clear a page's content and replace with new blocks."""
    delete_all_blocks(client, page_id)
    if new_blocks:
        append_blocks(client, page_id, new_blocks)


# ---------------------------------------------------------------------------
# Child pages (archives and redlines)
# ---------------------------------------------------------------------------


def create_child_page(client: Client, parent_page_id: str,
                      title: str, blocks: list[dict]) -> dict:
    """Create a child page under the given parent page."""
    initial_blocks = blocks[:NOTION_MAX_BLOCKS_PER_REQUEST]
    remaining_blocks = blocks[NOTION_MAX_BLOCKS_PER_REQUEST:]

    page = client.pages.create(
        parent={"page_id": parent_page_id},
        properties={"title": [{"text": {"content": title}}]},
        children=initial_blocks,
    )

    if remaining_blocks:
        append_blocks(client, page["id"], remaining_blocks)

    return page


def create_archive_page(client: Client, parent_page_id: str,
                        doc_uid: str, revision: str,
                        content_blocks: list[dict]) -> dict:
    """Create an archive child page with a snapshot of content."""
    title = f"Archive: {doc_uid} v{revision}"
    logger.info("Creating archive page: %s", title)
    return create_child_page(client, parent_page_id, title, content_blocks)


def create_redline_page(client: Client, parent_page_id: str,
                        doc_uid: str, prev_rev: str, new_rev: str,
                        redline_blocks: list[dict]) -> dict:
    """Create a redline child page with the diff content."""
    title = f"Redline: {doc_uid} v{prev_rev} \u2192 v{new_rev}"
    logger.info("Creating redline page: %s", title)
    return create_child_page(client, parent_page_id, title, redline_blocks)


# ---------------------------------------------------------------------------
# Read current page state
# ---------------------------------------------------------------------------


def get_page_revision(page: dict) -> str:
    """Extract the current revision string from a page's properties."""
    rev_prop = page.get("properties", {}).get("Revision", {})
    rt = rev_prop.get("rich_text", [])
    return rt[0].get("plain_text", "0.0") if rt else "0.0"


def get_page_status(page: dict) -> str:
    """Extract the current status from a page's properties."""
    status_prop = page.get("properties", {}).get("Status", {})
    select = status_prop.get("select")
    return select.get("name", "") if select else ""


def get_page_sha(page: dict) -> str:
    """Extract the Git commit SHA from a page's properties."""
    sha_prop = page.get("properties", {}).get("Git Commit SHA", {})
    rt = sha_prop.get("rich_text", [])
    return rt[0].get("plain_text", "") if rt else ""
