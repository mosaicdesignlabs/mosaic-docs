"""
YAML frontmatter parsing, validation, and write-back.

Uses python-frontmatter for reading and ruamel.yaml for writing
(ruamel preserves formatting and comments when updating doc_uid).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import frontmatter
from ruamel.yaml import YAML

from .config import (
    VALID_CATEGORIES,
    VALID_DEPARTMENTS,
    VALID_DESIRED_STATES,
    VALID_ORGS,
)

# ---------------------------------------------------------------------------
# UID pattern
# ---------------------------------------------------------------------------

DOC_UID_PATTERN = re.compile(
    r"^[A-Z]{2,4}-[A-Z]{2,4}-[A-Z]{2,4}-\d{3,}$"
)


# ---------------------------------------------------------------------------
# Parsed document
# ---------------------------------------------------------------------------


@dataclass
class ParsedDoc:
    """A Markdown document with parsed frontmatter."""

    path: Path
    metadata: dict[str, Any]
    content: str  # Markdown body (after frontmatter)

    # Convenience accessors
    @property
    def doc_uid(self) -> str:
        return self.metadata.get("doc_uid", "")

    @property
    def title(self) -> str:
        return self.metadata.get("title", "")

    @property
    def org(self) -> str:
        return self.metadata.get("org", "")

    @property
    def category(self) -> str:
        return self.metadata.get("category", "")

    @property
    def department(self) -> str:
        return self.metadata.get("department", "")

    @property
    def publish(self) -> bool:
        notion = self.metadata.get("notion", {})
        return bool(notion.get("publish", False))

    @property
    def database(self) -> str:
        notion = self.metadata.get("notion", {})
        return notion.get("database", "")

    @property
    def desired_state(self) -> str:
        lifecycle = self.metadata.get("lifecycle", {})
        return lifecycle.get("desired_state", "none")

    @property
    def access_groups(self) -> list[str]:
        return self.metadata.get("access_groups", [])

    @property
    def format_profile(self) -> str | None:
        return self.metadata.get("format_profile")

    @property
    def needs_auto_uid(self) -> bool:
        return self.doc_uid == "auto"

    @property
    def uid_prefix(self) -> str:
        return f"{self.org}-{self.department}-{self.category}"


# ---------------------------------------------------------------------------
# Parse
# ---------------------------------------------------------------------------


def parse_doc(path: Path) -> ParsedDoc:
    """Parse a Markdown file and extract frontmatter + body."""
    post = frontmatter.load(str(path))
    return ParsedDoc(
        path=path,
        metadata=dict(post.metadata),
        content=post.content,
    )


def parse_all_docs(docs_dir: Path) -> list[ParsedDoc]:
    """Recursively find and parse all .md files under docs_dir."""
    docs = []
    for md_file in sorted(docs_dir.rglob("*.md")):
        try:
            docs.append(parse_doc(md_file))
        except Exception as exc:
            print(f"  WARNING: failed to parse {md_file}: {exc}")
    return docs


# ---------------------------------------------------------------------------
# Validate frontmatter
# ---------------------------------------------------------------------------


@dataclass
class ValidationResult:
    """Collects errors and warnings from validation."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def merge(self, other: ValidationResult) -> None:
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)


def validate_frontmatter(doc: ParsedDoc) -> ValidationResult:
    """Validate frontmatter fields against the schema."""
    result = ValidationResult()
    meta = doc.metadata
    rel = doc.path.name

    # --- Required top-level fields ---
    for key in ("title", "org", "category", "department"):
        if not meta.get(key):
            result.error(f"{rel}: missing required field '{key}'")

    # doc_uid: required but can be "auto"
    uid = meta.get("doc_uid")
    if not uid:
        result.error(f"{rel}: missing required field 'doc_uid'")
    elif uid != "auto" and not DOC_UID_PATTERN.match(uid):
        result.error(
            f"{rel}: invalid doc_uid '{uid}' "
            f"(expected ORG-DEP-CAT-NNN or 'auto')"
        )

    # --- Enum validation ---
    if meta.get("org") and meta["org"] not in VALID_ORGS:
        result.error(
            f"{rel}: invalid org '{meta['org']}' "
            f"(expected one of {sorted(VALID_ORGS)})"
        )

    if meta.get("category") and meta["category"] not in VALID_CATEGORIES:
        result.error(
            f"{rel}: invalid category '{meta['category']}' "
            f"(expected one of {sorted(VALID_CATEGORIES)})"
        )

    if meta.get("department") and meta["department"] not in VALID_DEPARTMENTS:
        result.error(
            f"{rel}: invalid department '{meta['department']}' "
            f"(expected one of {sorted(VALID_DEPARTMENTS)})"
        )

    # --- Notion block ---
    notion = meta.get("notion")
    if not isinstance(notion, dict):
        result.error(f"{rel}: missing 'notion' block")
    else:
        if "publish" not in notion:
            result.error(f"{rel}: missing 'notion.publish'")
        if not notion.get("database"):
            result.error(f"{rel}: missing 'notion.database'")

    # --- Lifecycle block ---
    lifecycle = meta.get("lifecycle")
    if not isinstance(lifecycle, dict):
        result.error(f"{rel}: missing 'lifecycle' block")
    else:
        ds = lifecycle.get("desired_state")
        if not ds:
            result.error(f"{rel}: missing 'lifecycle.desired_state'")
        elif ds not in VALID_DESIRED_STATES:
            result.error(
                f"{rel}: invalid desired_state '{ds}' "
                f"(expected one of {sorted(VALID_DESIRED_STATES)})"
            )

    # --- Access groups ---
    ag = meta.get("access_groups")
    if ag is None:
        result.error(f"{rel}: missing 'access_groups'")
    elif not isinstance(ag, list):
        result.error(f"{rel}: 'access_groups' must be a list")

    # --- Computed fields must not be in source ---
    for forbidden in ("revision", "status", "git_commit", "git_pr",
                      "published_at", "notion_page_id"):
        if forbidden in meta:
            result.error(
                f"{rel}: '{forbidden}' is a computed field and must not "
                f"appear in source frontmatter"
            )

    # --- UID consistency check ---
    if uid and uid != "auto" and DOC_UID_PATTERN.match(uid):
        parts = uid.split("-")
        if len(parts) >= 3:
            uid_org, uid_dep, uid_cat = parts[0], parts[1], parts[2]
            if meta.get("org") and uid_org != meta["org"]:
                result.error(
                    f"{rel}: doc_uid org '{uid_org}' doesn't match "
                    f"frontmatter org '{meta['org']}'"
                )
            if meta.get("department") and uid_dep != meta["department"]:
                result.error(
                    f"{rel}: doc_uid department '{uid_dep}' doesn't match "
                    f"frontmatter department '{meta['department']}'"
                )
            if meta.get("category") and uid_cat != meta["category"]:
                result.error(
                    f"{rel}: doc_uid category '{uid_cat}' doesn't match "
                    f"frontmatter category '{meta['category']}'"
                )

    # --- Category / subfolder consistency ---
    category = meta.get("category", "")
    if category and doc.path.parent.name != category:
        result.warn(
            f"{rel}: file is in folder '{doc.path.parent.name}' but "
            f"category is '{category}' — expected folder '{category}/'"
        )

    return result


# ---------------------------------------------------------------------------
# Write-back (for auto-UID assignment)
# ---------------------------------------------------------------------------


def write_doc_uid(path: Path, new_uid: str) -> None:
    """
    Replace doc_uid: "auto" with the assigned UID in the file,
    preserving all other formatting.
    """
    text = path.read_text(encoding="utf-8")
    updated = re.sub(
        r'(doc_uid:\s*)"auto"',
        rf'\g<1>"{new_uid}"',
        text,
        count=1,
    )
    if updated == text:
        raise ValueError(
            f"Could not find doc_uid: \"auto\" in {path} to replace"
        )
    path.write_text(updated, encoding="utf-8")
