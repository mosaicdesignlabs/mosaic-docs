#!/usr/bin/env python3
"""
CLI entry point: publish documents to Notion.

Usage:
    # Publish drafts (changed docs on push to main)
    python scripts/publish_to_notion.py --mode draft

    # Publish releases (on merge to release)
    python scripts/publish_to_notion.py --mode release

    # Publish specific files
    python scripts/publish_to_notion.py --mode draft docs/SOP/document-control.md

    # Publish all docs (force full re-publish)
    python scripts/publish_to_notion.py --mode draft --all

Environment variables required:
    NOTION_TOKEN
    NOTION_DATABASE_ID_DOCUMENTS

Exit codes:
    0 — all publishes succeeded (or no-op)
    1 — one or more publishes failed
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from docctl.config import load_config
from docctl.frontmatter import parse_all_docs
from docctl.publish import publish_changed_docs

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish docs to Notion")
    parser.add_argument(
        "--mode",
        choices=["draft", "release"],
        required=True,
        help="Publishing mode: 'draft' or 'release'",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Path to the repo root",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="publish_all",
        help="Publish all docs (not just changed ones)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Write results JSON to this file",
    )
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="Specific files to publish",
    )
    args = parser.parse_args()

    config = load_config(args.repo_root)

    if not config.notion_token:
        logger.error("NOTION_TOKEN not set")
        return 1
    if not config.notion_database_id:
        logger.error("NOTION_DATABASE_ID_DOCUMENTS not set")
        return 1

    is_release = args.mode == "release"
    doc_paths = None

    if args.files:
        doc_paths = [
            (config.repo_root / f).resolve() if not f.is_absolute() else f
            for f in args.files
        ]
    elif args.publish_all:
        doc_paths = [d.path for d in parse_all_docs(config.docs_dir)]

    mode_label = "RELEASE" if is_release else "DRAFT"
    logger.info("Starting %s publish pipeline", mode_label)

    results = publish_changed_docs(
        config=config,
        is_release=is_release,
        doc_paths=doc_paths,
    )

    # Report results
    errors = [r for r in results if r.get("status") == "error"]
    published = [r for r in results if r.get("status") in ("created", "updated")]
    skipped = [r for r in results if r.get("status") in ("skipped", "no-op")]

    print(f"\n{'=' * 60}")
    print(f"  {mode_label} PUBLISH RESULTS")
    print(f"{'=' * 60}")
    print(f"  Published: {len(published)}")
    print(f"  Skipped:   {len(skipped)}")
    print(f"  Errors:    {len(errors)}")
    print()

    for r in published:
        uid = r.get("doc_uid", "?")
        rev = r.get("revision", "?")
        action = r.get("status", "?")
        print(f"  ✓ {uid} v{rev} ({action})")

    for r in skipped:
        uid = r.get("doc_uid", r.get("file", "?"))
        reason = r.get("reason", "")
        print(f"  – {uid}: {reason}")

    for r in errors:
        uid = r.get("doc_uid", r.get("file", "?"))
        reason = r.get("reason", "")
        errs = r.get("errors", [])
        print(f"  ✗ {uid}: {reason}")
        for e in errs:
            print(f"      {e}")

    print()

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(results, indent=2, default=str))
        logger.info("Results written to %s", args.output)

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
