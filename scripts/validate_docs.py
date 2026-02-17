#!/usr/bin/env python3
"""
CLI entry point: validate documents.

Usage:
    python scripts/validate_docs.py [--repo-root .] [file1.md file2.md ...]

If no files are specified, validates all docs under docs/.

Exit codes:
    0 — all checks passed
    1 — validation errors found
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Allow running from repo root or scripts/
sys.path.insert(0, str(Path(__file__).resolve().parent))

from docctl.config import load_config
from docctl.validate import validate_all

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Mosaic documents")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Path to the repo root (default: auto-detect)",
    )
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="Specific files to validate (default: all docs)",
    )
    args = parser.parse_args()

    config = load_config(args.repo_root)

    paths = None
    if args.files:
        paths = [
            (config.repo_root / f).resolve() if not f.is_absolute() else f
            for f in args.files
        ]

    print(f"Validating docs in {config.docs_dir} ...")
    result = validate_all(config, paths)

    if result.warnings:
        print(f"\n⚠  {len(result.warnings)} warning(s):")
        for w in result.warnings:
            print(f"   {w}")

    if result.errors:
        print(f"\n✗  {len(result.errors)} error(s):")
        for e in result.errors:
            print(f"   {e}")
        print("\nValidation FAILED.")
        return 1

    print(f"\n✓  All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
