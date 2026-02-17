"""
Redline (diff) generation for the document control pipeline.

Compares two versions of a Markdown document and produces a rich
redline as Notion blocks: additions highlighted in green, deletions
in red, and unchanged context in gray.

Uses Python's built-in difflib for word-level and line-level diffs.
"""

from __future__ import annotations

import difflib
import re
from datetime import datetime, timezone

from .md_to_notion import _text, _paragraph_block, _heading_block, _divider_block


# ---------------------------------------------------------------------------
# Diff computation
# ---------------------------------------------------------------------------


def compute_line_diff(old_text: str, new_text: str) -> list[dict]:
    """
    Compute a line-by-line diff and return Notion blocks representing
    the redline.

    - Added lines: green background text
    - Removed lines: red/strikethrough text
    - Unchanged lines: gray text (context)
    - Section headers preserved as headings
    """
    old_lines = old_text.splitlines(keepends=True)
    new_lines = new_text.splitlines(keepends=True)

    differ = difflib.unified_diff(
        old_lines, new_lines,
        fromfile="previous", tofile="current",
        lineterm="",
    )

    blocks: list[dict] = []
    current_chunk: list[dict] = []

    for line in differ:
        # Skip diff headers
        if line.startswith("---") or line.startswith("+++"):
            continue

        if line.startswith("@@"):
            # Flush current chunk
            if current_chunk:
                blocks.append(_paragraph_block(current_chunk))
                current_chunk = []
            # Add chunk header as a divider
            blocks.append(_divider_block())
            blocks.append(_paragraph_block([
                _text(line.strip(), {"italic": True, "color": "gray"})
            ]))
            continue

        stripped = line.rstrip("\n")

        if line.startswith("+"):
            # Addition
            if current_chunk:
                blocks.append(_paragraph_block(current_chunk))
                current_chunk = []
            blocks.append(_paragraph_block([
                _text("+ " + stripped[1:], {"color": "green"})
            ]))

        elif line.startswith("-"):
            # Deletion
            if current_chunk:
                blocks.append(_paragraph_block(current_chunk))
                current_chunk = []
            blocks.append(_paragraph_block([
                _text("- " + stripped[1:], {"strikethrough": True, "color": "red"})
            ]))

        else:
            # Context line
            content = stripped[1:] if stripped.startswith(" ") else stripped
            current_chunk.append(_text(content + "\n", {"color": "gray"}))

    if current_chunk:
        blocks.append(_paragraph_block(current_chunk))

    return blocks


def compute_summary(old_text: str, new_text: str) -> dict[str, int]:
    """Compute summary statistics for the diff."""
    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()

    matcher = difflib.SequenceMatcher(None, old_lines, new_lines)
    added = 0
    removed = 0
    changed = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "insert":
            added += j2 - j1
        elif tag == "delete":
            removed += i2 - i1
        elif tag == "replace":
            changed += max(i2 - i1, j2 - j1)

    return {"added": added, "removed": removed, "changed": changed}


# ---------------------------------------------------------------------------
# Build redline blocks for Notion
# ---------------------------------------------------------------------------


def build_redline_blocks(
    doc_uid: str,
    prev_revision: str,
    new_revision: str,
    old_markdown: str,
    new_markdown: str,
    git_sha: str = "",
    pr_url: str = "",
) -> list[dict]:
    """
    Build the full set of Notion blocks for a redline child page.

    Structure:
    1. Summary heading with change stats
    2. Metadata (commit, PR, timestamp)
    3. Divider
    4. Line-by-line diff blocks
    """
    blocks: list[dict] = []
    stats = compute_summary(old_markdown, new_markdown)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Title heading
    blocks.append(_heading_block(1, [
        _text(f"Redline: {doc_uid} v{prev_revision} \u2192 v{new_revision}")
    ]))

    # Summary
    summary_parts = []
    if stats["added"]:
        summary_parts.append(f"{stats['added']} lines added")
    if stats["removed"]:
        summary_parts.append(f"{stats['removed']} lines removed")
    if stats["changed"]:
        summary_parts.append(f"{stats['changed']} lines changed")
    summary_text = ", ".join(summary_parts) if summary_parts else "No changes detected"

    blocks.append(_paragraph_block([
        _text("Summary: ", {"bold": True}),
        _text(summary_text),
    ]))

    # Metadata
    meta_parts = [_text(f"Generated: {ts}")]
    if git_sha:
        meta_parts.append(_text(f" \u2022 Commit: {git_sha[:8]}"))
    if pr_url:
        meta_parts.append(_text(" \u2022 "))
        meta_parts.append({
            "type": "text",
            "text": {"content": "Pull Request", "link": {"url": pr_url}},
        })
    blocks.append(_paragraph_block(meta_parts))

    blocks.append(_divider_block())

    # Diff blocks
    if not old_markdown:
        blocks.append(_paragraph_block([
            _text("Initial version \u2014 no previous content to compare.", {"italic": True})
        ]))
    else:
        diff_blocks = compute_line_diff(old_markdown, new_markdown)
        if diff_blocks:
            blocks.extend(diff_blocks)
        else:
            blocks.append(_paragraph_block([
                _text("No differences detected.", {"italic": True})
            ]))

    return blocks
