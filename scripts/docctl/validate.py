"""
Full document validation: frontmatter schema, link checking,
image references, and optional format-profile section checks.
"""

from __future__ import annotations

import re
from pathlib import Path

from .config import PipelineConfig
from .frontmatter import ParsedDoc, ValidationResult, parse_all_docs, validate_frontmatter

# ---------------------------------------------------------------------------
# Format profile section requirements
# ---------------------------------------------------------------------------

FORMAT_PROFILES: dict[str, list[str]] = {
    "SOP_v1": [
        "Purpose",
        "Scope",
        "Responsibilities",
        "Definitions",
        "Safety",
        "Procedure",
        "Records",
        "Revision History",
    ],
}

# ---------------------------------------------------------------------------
# Link patterns
# ---------------------------------------------------------------------------

# Markdown links: [text](url)
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
# Markdown images: ![alt](path)
MD_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
# Heading: ## Heading Text
HEADING_RE = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE)
# Fenced code block
CODE_FENCE_RE = re.compile(r"^```[^\n]*\n.*?^```", re.MULTILINE | re.DOTALL)


def _strip_code_blocks(content: str) -> str:
    """Remove fenced code blocks so regexes don't match inside examples."""
    return CODE_FENCE_RE.sub("", content)


# ---------------------------------------------------------------------------
# Link validation
# ---------------------------------------------------------------------------


def _resolve_relative_link(doc_path: Path, target: str, docs_dir: Path) -> Path | None:
    """Resolve a relative markdown link to an absolute path."""
    resolved = (doc_path.parent / target).resolve()
    try:
        resolved.relative_to(docs_dir.resolve())
    except ValueError:
        return None
    return resolved


def validate_links(doc: ParsedDoc, all_docs: list[ParsedDoc],
                   config: PipelineConfig) -> ValidationResult:
    """Validate all links in a document."""
    result = ValidationResult()
    rel = doc.path.name

    doc_uids_by_path: dict[Path, str] = {}
    for d in all_docs:
        doc_uids_by_path[d.path.resolve()] = d.doc_uid

    content = _strip_code_blocks(doc.content)

    for match in MD_LINK_RE.finditer(content):
        link_text, target = match.group(1), match.group(2)

        # Skip image links (handled separately)
        if doc.content[match.start() - 1:match.start()] == "!":
            continue

        # Internal repo link (relative .md path)
        if target.endswith(".md") and not target.startswith("http"):
            resolved = (doc.path.parent / target).resolve()
            if not resolved.exists():
                result.error(
                    f"{rel}: broken internal link [{link_text}]({target}) — "
                    f"target file does not exist"
                )
            elif resolved in doc_uids_by_path:
                target_uid = doc_uids_by_path[resolved]
                if not target_uid or target_uid == "auto":
                    result.warn(
                        f"{rel}: internal link [{link_text}]({target}) points "
                        f"to a doc without an assigned doc_uid"
                    )
            continue

        # Notion URL
        if "notion.so" in target or "notion.site" in target:
            result.warn(
                f"{rel}: Notion URL found [{link_text}]({target}) — "
                f"pipeline will attempt to convert to page mention"
            )
            continue

        # External URL (non-blocking, just informational)
        if target.startswith("http://") or target.startswith("https://"):
            continue

        # Anchor or other
        if target.startswith("#"):
            continue

        result.warn(f"{rel}: unrecognized link target: {target}")

    return result


# ---------------------------------------------------------------------------
# Image validation
# ---------------------------------------------------------------------------


def validate_images(doc: ParsedDoc, config: PipelineConfig) -> ValidationResult:
    """Validate all image references in a document."""
    result = ValidationResult()
    rel = doc.path.name

    content = _strip_code_blocks(doc.content)

    for match in MD_IMAGE_RE.finditer(content):
        alt_text, img_path = match.group(1), match.group(2)

        # External image URLs are fine
        if img_path.startswith("http://") or img_path.startswith("https://"):
            continue

        resolved = (doc.path.parent / img_path).resolve()
        if not resolved.exists():
            result.error(
                f"{rel}: broken image reference ![{alt_text}]({img_path}) — "
                f"file does not exist"
            )
        elif not resolved.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif",
                                               ".svg", ".webp", ".bmp"):
            result.warn(
                f"{rel}: unusual image extension: {resolved.suffix}"
            )

    return result


# ---------------------------------------------------------------------------
# Format profile validation
# ---------------------------------------------------------------------------


def validate_format_profile(doc: ParsedDoc) -> ValidationResult:
    """Check that required sections are present for the format profile."""
    result = ValidationResult()
    profile = doc.format_profile
    if not profile:
        return result

    required_sections = FORMAT_PROFILES.get(profile)
    if required_sections is None:
        result.warn(
            f"{doc.path.name}: unknown format_profile '{profile}' — "
            f"skipping section checks"
        )
        return result

    headings = [m.group(1).strip() for m in HEADING_RE.finditer(doc.content)]
    heading_lower = [h.lower() for h in headings]

    for section in required_sections:
        if section.lower() not in heading_lower:
            result.error(
                f"{doc.path.name}: format profile '{profile}' requires "
                f"section '{section}' but it was not found"
            )

    return result


# ---------------------------------------------------------------------------
# Duplicate UID check
# ---------------------------------------------------------------------------


def validate_unique_uids(docs: list[ParsedDoc]) -> ValidationResult:
    """Ensure no two documents share the same doc_uid."""
    result = ValidationResult()
    seen: dict[str, Path] = {}

    for doc in docs:
        uid = doc.doc_uid
        if not uid or uid == "auto":
            continue
        if uid in seen:
            result.error(
                f"Duplicate doc_uid '{uid}': found in both "
                f"{seen[uid].name} and {doc.path.name}"
            )
        else:
            seen[uid] = doc.path

    return result


# ---------------------------------------------------------------------------
# Orphaned image check
# ---------------------------------------------------------------------------


def validate_orphaned_images(docs: list[ParsedDoc],
                             config: PipelineConfig) -> ValidationResult:
    """Warn about image files not referenced by any document."""
    result = ValidationResult()

    if not config.images_dir.exists():
        return result

    image_files = set()
    for ext in ("*.png", "*.jpg", "*.jpeg", "*.gif", "*.svg", "*.webp"):
        image_files.update(config.images_dir.glob(ext))

    referenced: set[Path] = set()
    for doc in docs:
        for match in MD_IMAGE_RE.finditer(doc.content):
            img_path = match.group(2)
            if not img_path.startswith("http"):
                resolved = (doc.path.parent / img_path).resolve()
                referenced.add(resolved)

    orphans = image_files - referenced
    for orphan in sorted(orphans):
        result.warn(f"Orphaned image: {orphan.relative_to(config.repo_root)}")

    return result


# ---------------------------------------------------------------------------
# Top-level validation entry point
# ---------------------------------------------------------------------------


def validate_doc(doc: ParsedDoc, all_docs: list[ParsedDoc],
                 config: PipelineConfig) -> ValidationResult:
    """Run all validations on a single document."""
    result = validate_frontmatter(doc)
    result.merge(validate_links(doc, all_docs, config))
    result.merge(validate_images(doc, config))
    result.merge(validate_format_profile(doc))
    return result


def validate_all(config: PipelineConfig,
                 paths: list[Path] | None = None) -> ValidationResult:
    """
    Validate documents.

    If paths is provided, validate only those files (but still load all docs
    for cross-reference checks). If None, validate everything under docs/.
    """
    all_docs = parse_all_docs(config.docs_dir)
    result = validate_unique_uids(all_docs)
    result.merge(validate_orphaned_images(all_docs, config))

    if paths:
        targets = {p.resolve() for p in paths}
        docs_to_check = [d for d in all_docs if d.path.resolve() in targets]
    else:
        docs_to_check = all_docs

    for doc in docs_to_check:
        doc_result = validate_doc(doc, all_docs, config)
        result.merge(doc_result)

    return result
