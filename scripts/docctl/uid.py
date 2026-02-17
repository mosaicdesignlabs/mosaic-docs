"""
Automatic doc_uid assignment.

When a document has `doc_uid: "auto"`, this module determines the next
available sequential number for the given ORG-DEP-CAT prefix and assigns it.
"""

from __future__ import annotations

import logging
import re
import subprocess
from pathlib import Path

from notion_client import Client

from .config import PipelineConfig
from .frontmatter import ParsedDoc, parse_all_docs, write_doc_uid
from .notion_api import query_all_uids

logger = logging.getLogger(__name__)

UID_NUMBER_RE = re.compile(r"-(\d+)$")


def _extract_number(uid: str) -> int | None:
    """Extract the sequential number from a doc_uid like MOS-ENG-SOP-012."""
    match = UID_NUMBER_RE.search(uid)
    return int(match.group(1)) if match else None


def find_next_uid(prefix: str, existing_uids: list[str]) -> str:
    """
    Given a prefix (e.g. 'MOS-ENG-SOP') and a list of existing UIDs,
    return the next available UID (e.g. 'MOS-ENG-SOP-013').
    """
    max_num = 0
    prefix_with_dash = f"{prefix}-"

    for uid in existing_uids:
        if uid.startswith(prefix_with_dash):
            num = _extract_number(uid)
            if num is not None and num > max_num:
                max_num = num

    next_num = max_num + 1
    return f"{prefix}-{next_num:03d}"


def collect_existing_uids(client: Client, database_id: str,
                          prefix: str, docs_dir: Path) -> list[str]:
    """
    Collect all existing UIDs matching a prefix from both Notion and local files.
    This ensures we don't conflict with unpublished docs or Notion-native pages.
    """
    # From Notion
    notion_uids = query_all_uids(client, database_id, prefix=prefix)

    # From local Git files
    local_uids: list[str] = []
    for doc in parse_all_docs(docs_dir):
        uid = doc.doc_uid
        if uid and uid != "auto" and uid.startswith(prefix):
            local_uids.append(uid)

    # Union of both sources
    all_uids = list(set(notion_uids + local_uids))
    logger.info(
        "Found %d existing UIDs with prefix '%s' (%d Notion, %d local)",
        len(all_uids), prefix, len(notion_uids), len(local_uids),
    )
    return all_uids


def assign_uid(doc: ParsedDoc, client: Client,
               config: PipelineConfig) -> str:
    """
    Assign a doc_uid to a document with doc_uid: "auto".

    1. Determine the prefix from org, department, category.
    2. Query Notion + local files for existing UIDs with that prefix.
    3. Compute the next sequential number.
    4. Write the UID back to the file.
    5. Return the assigned UID.
    """
    if not doc.needs_auto_uid:
        return doc.doc_uid

    prefix = doc.uid_prefix
    existing = collect_existing_uids(
        client, config.notion_database_id, prefix, config.docs_dir
    )
    new_uid = find_next_uid(prefix, existing)

    logger.info("Assigning doc_uid '%s' to %s", new_uid, doc.path.name)
    write_doc_uid(doc.path, new_uid)

    return new_uid


def commit_uid_assignment(doc_path: Path, new_uid: str,
                          config: PipelineConfig) -> None:
    """
    Commit the auto-assigned doc_uid back to the repo.

    Uses the bot account to avoid triggering another pipeline run
    (the pipeline checks for bot commits and skips them).
    """
    rel_path = doc_path.relative_to(config.repo_root)
    commit_msg = f"docs: assign doc_uid {new_uid}"

    try:
        subprocess.run(
            ["git", "add", str(rel_path)],
            cwd=config.repo_root, check=True, capture_output=True,
        )
        subprocess.run(
            [
                "git", "commit",
                "--author", f"{config.bot_commit_author} <bot@mosaicdesignlabs.com>",
                "-m", commit_msg,
            ],
            cwd=config.repo_root, check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "push"],
            cwd=config.repo_root, check=True, capture_output=True,
        )
        logger.info("Committed and pushed UID assignment: %s", commit_msg)
    except subprocess.CalledProcessError as e:
        logger.error("Failed to commit UID assignment: %s", e.stderr.decode())
        raise
