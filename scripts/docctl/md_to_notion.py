"""
Convert Markdown content to Notion API block objects.

Uses markdown-it-py to parse Markdown into tokens, then walks the token
stream to produce Notion block dicts suitable for the Notion API's
`append_block_children` endpoint.

Handles: headings, paragraphs, bold/italic/strikethrough/code, links
(internal, Notion, external), images (with captions and width hints),
tables, code blocks, bulleted/numbered lists, blockquotes, horizontal
rules, and nested list items.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins.front_matter import front_matter_plugin

from .frontmatter import ParsedDoc

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

NOTION_MAX_TEXT_LENGTH = 2000
NOTION_MAX_BLOCKS_PER_REQUEST = 100

WIDTH_HINT_RE = re.compile(r"\s*\|width=(\d+)\s*$")
NOTION_URL_RE = re.compile(r"https?://(?:www\.)?notion\.so/")

# Language map for code blocks
NOTION_LANGUAGES = {
    "python", "javascript", "typescript", "java", "c", "cpp", "c++",
    "c#", "csharp", "go", "rust", "ruby", "php", "swift", "kotlin",
    "scala", "r", "matlab", "sql", "html", "css", "scss", "json",
    "yaml", "xml", "markdown", "bash", "shell", "powershell", "docker",
    "dockerfile", "makefile", "toml", "ini", "diff", "graphql",
    "protobuf", "arduino", "elixir", "erlang", "haskell", "lua",
    "nix", "perl", "plain text", "mermaid",
}


# ---------------------------------------------------------------------------
# Rich text helpers
# ---------------------------------------------------------------------------


def _text(content: str, annotations: dict | None = None,
          link: dict | None = None) -> dict:
    """Create a Notion rich_text text object."""
    obj: dict[str, Any] = {
        "type": "text",
        "text": {"content": content},
    }
    if link:
        obj["text"]["link"] = link
    if annotations:
        obj["annotations"] = annotations
    return obj


def _mention_page(page_id: str) -> dict:
    """Create a Notion rich_text page-mention object."""
    return {
        "type": "mention",
        "mention": {
            "type": "page",
            "page": {"id": page_id},
        },
    }


def _split_long_text(rich_texts: list[dict]) -> list[dict]:
    """Split any rich_text element exceeding 2000 chars into chunks."""
    result = []
    for rt in rich_texts:
        content = rt.get("text", {}).get("content", "")
        if len(content) <= NOTION_MAX_TEXT_LENGTH:
            result.append(rt)
            continue
        for i in range(0, len(content), NOTION_MAX_TEXT_LENGTH):
            chunk = dict(rt)
            chunk["text"] = dict(rt["text"])
            chunk["text"]["content"] = content[i:i + NOTION_MAX_TEXT_LENGTH]
            result.append(chunk)
    return result


# ---------------------------------------------------------------------------
# Inline token → rich_text conversion
# ---------------------------------------------------------------------------


class InlineConverter:
    """Converts markdown-it inline tokens to Notion rich_text arrays."""

    def __init__(self, doc: ParsedDoc, page_id_lookup: dict[str, str] | None = None,
                 raw_url_base: str = ""):
        self.doc = doc
        self.page_id_lookup = page_id_lookup or {}
        self.raw_url_base = raw_url_base

    def convert(self, tokens: list[Token]) -> list[dict]:
        """Walk inline child tokens and produce a rich_text list."""
        result: list[dict] = []
        annotations: dict[str, bool] = {}
        link_stack: list[dict | None] = []
        i = 0

        while i < len(tokens):
            tok = tokens[i]

            if tok.type == "text":
                rt = _text(tok.content, annotations.copy() if annotations else None,
                           link_stack[-1] if link_stack else None)
                result.append(rt)

            elif tok.type == "code_inline":
                ann = {**annotations, "code": True}
                result.append(_text(tok.content, ann))

            elif tok.type == "softbreak" or tok.type == "hardbreak":
                result.append(_text("\n"))

            elif tok.type == "strong_open":
                annotations["bold"] = True
            elif tok.type == "strong_close":
                annotations.pop("bold", None)

            elif tok.type == "em_open":
                annotations["italic"] = True
            elif tok.type == "em_close":
                annotations.pop("italic", None)

            elif tok.type == "s_open":
                annotations["strikethrough"] = True
            elif tok.type == "s_close":
                annotations.pop("strikethrough", None)

            elif tok.type == "link_open":
                href = tok.attrGet("href") or ""
                link_info = self._resolve_link(href)
                link_stack.append(link_info)

            elif tok.type == "link_close":
                if link_stack:
                    link_stack.pop()

            elif tok.type == "image":
                blocks = self._image_to_block(tok)
                if blocks:
                    # Images are block-level, return them separately
                    pass

            elif tok.type == "html_inline":
                result.append(_text(tok.content))

            i += 1

        return _split_long_text(result)

    def _resolve_link(self, href: str) -> dict | None:
        """Resolve a link href to a Notion link or page mention."""
        if not href:
            return None

        # Internal .md link — try to resolve to Notion page ID
        if href.endswith(".md") and not href.startswith("http"):
            resolved = (self.doc.path.parent / href).resolve()
            for uid, page_id in self.page_id_lookup.items():
                # We'll use uid matching later; for now, return as URL
                pass
            return {"url": href}

        # Any URL
        return {"url": href}

    def _image_to_block(self, tok: Token) -> dict | None:
        """Convert an image token to a Notion image block."""
        src = tok.attrGet("src") or ""
        alt = tok.content or ""
        return image_block(src, alt, self.doc.path, self.raw_url_base)


# ---------------------------------------------------------------------------
# Image block
# ---------------------------------------------------------------------------


def image_block(src: str, alt: str, doc_path: Path,
                raw_url_base: str) -> dict | None:
    """Create a Notion image block from markdown image syntax."""
    # Parse width hint from alt text
    width = None
    caption = alt
    width_match = WIDTH_HINT_RE.search(alt)
    if width_match:
        width = int(width_match.group(1))
        caption = alt[:width_match.start()].strip()

    # Determine image URL
    if src.startswith("http://") or src.startswith("https://"):
        url = src
    elif raw_url_base:
        # Resolve relative path to raw Gitea URL
        img_path = (doc_path.parent / src).resolve()
        try:
            rel = img_path.relative_to(Path.cwd())
        except ValueError:
            rel = Path(src)
        url = f"{raw_url_base}/{rel}"
    else:
        url = src

    block: dict[str, Any] = {
        "type": "image",
        "image": {
            "type": "external",
            "external": {"url": url},
        },
    }
    if caption:
        block["image"]["caption"] = [_text(caption)]

    return block


# ---------------------------------------------------------------------------
# Block-level conversion
# ---------------------------------------------------------------------------


def _heading_block(level: int, rich_text: list[dict]) -> dict:
    """Create a heading block (level 1-3; Notion only supports 3 levels)."""
    level = min(level, 3)
    key = f"heading_{level}"
    return {"type": key, key: {"rich_text": rich_text}}


def _paragraph_block(rich_text: list[dict]) -> dict:
    return {"type": "paragraph", "paragraph": {"rich_text": rich_text}}


def _code_block(content: str, language: str = "plain text") -> dict:
    lang = language.lower() if language.lower() in NOTION_LANGUAGES else "plain text"
    rich_text = _split_long_text([_text(content)])
    return {"type": "code", "code": {"rich_text": rich_text, "language": lang}}


def _bulleted_list_item(rich_text: list[dict],
                        children: list[dict] | None = None) -> dict:
    block: dict[str, Any] = {
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": rich_text},
    }
    if children:
        block["bulleted_list_item"]["children"] = children
    return block


def _numbered_list_item(rich_text: list[dict],
                        children: list[dict] | None = None) -> dict:
    block: dict[str, Any] = {
        "type": "numbered_list_item",
        "numbered_list_item": {"rich_text": rich_text},
    }
    if children:
        block["numbered_list_item"]["children"] = children
    return block


def _quote_block(rich_text: list[dict]) -> dict:
    return {"type": "quote", "quote": {"rich_text": rich_text}}


def _divider_block() -> dict:
    return {"type": "divider", "divider": {}}


def _table_block(rows: list[list[list[dict]]], has_header: bool = True) -> dict:
    """Create a table block. rows is list of rows, each row is list of cells,
    each cell is a list of rich_text objects."""
    if not rows:
        return _paragraph_block([_text("(empty table)")])

    width = max(len(row) for row in rows) if rows else 0
    table_rows = []
    for row in rows:
        # Pad cells to table width
        cells = row + [[] for _ in range(width - len(row))]
        table_rows.append({
            "type": "table_row",
            "table_row": {"cells": cells},
        })

    return {
        "type": "table",
        "table": {
            "table_width": width,
            "has_column_header": has_header,
            "has_row_header": False,
            "children": table_rows,
        },
    }


def _callout_block(rich_text: list[dict], emoji: str = "💡") -> dict:
    return {
        "type": "callout",
        "callout": {
            "rich_text": rich_text,
            "icon": {"type": "emoji", "emoji": emoji},
        },
    }


# ---------------------------------------------------------------------------
# Main converter
# ---------------------------------------------------------------------------


class MarkdownToNotionConverter:
    """
    Converts a Markdown string to a list of Notion block objects.

    Usage:
        converter = MarkdownToNotionConverter(doc, page_id_lookup, raw_url_base)
        blocks = converter.convert()
    """

    def __init__(self, doc: ParsedDoc,
                 page_id_lookup: dict[str, str] | None = None,
                 raw_url_base: str = ""):
        self.doc = doc
        self.page_id_lookup = page_id_lookup or {}
        self.raw_url_base = raw_url_base
        self.inline_converter = InlineConverter(doc, page_id_lookup, raw_url_base)

        self.md = MarkdownIt("commonmark", {"breaks": True})
        self.md.enable("table")
        self.md.enable("strikethrough")
        front_matter_plugin(self.md)

    def convert(self, markdown: str | None = None) -> list[dict]:
        """Convert markdown content to Notion blocks."""
        content = markdown if markdown is not None else self.doc.content
        tokens = self.md.parse(content)
        return self._process_tokens(tokens)

    def _process_tokens(self, tokens: list[Token]) -> list[dict]:
        """Walk top-level tokens and produce blocks."""
        blocks: list[dict] = []
        i = 0

        while i < len(tokens):
            tok = tokens[i]

            # Skip frontmatter
            if tok.type == "front_matter":
                i += 1
                continue

            # Headings
            if tok.type == "heading_open":
                level = int(tok.tag[1])  # h1 → 1, h2 → 2, etc.
                inline_tok = tokens[i + 1] if i + 1 < len(tokens) else None
                rich_text = self._inline_to_rich_text(inline_tok)
                blocks.append(_heading_block(level, rich_text))
                i += 3  # heading_open, inline, heading_close
                continue

            # Paragraphs
            if tok.type == "paragraph_open":
                inline_tok = tokens[i + 1] if i + 1 < len(tokens) else None
                # Check if this paragraph contains only an image
                img_block = self._check_image_paragraph(inline_tok)
                if img_block:
                    blocks.append(img_block)
                else:
                    rich_text = self._inline_to_rich_text(inline_tok)
                    if rich_text:
                        blocks.append(_paragraph_block(rich_text))
                i += 3  # paragraph_open, inline, paragraph_close
                continue

            # Fenced code blocks
            if tok.type == "fence":
                lang = tok.info.strip() if tok.info else "plain text"
                blocks.append(_code_block(tok.content.rstrip("\n"), lang))
                i += 1
                continue

            # Code blocks (indented)
            if tok.type == "code_block":
                blocks.append(_code_block(tok.content.rstrip("\n")))
                i += 1
                continue

            # Bullet list
            if tok.type == "bullet_list_open":
                list_blocks, consumed = self._process_list(
                    tokens[i:], "bullet_list", _bulleted_list_item
                )
                blocks.extend(list_blocks)
                i += consumed
                continue

            # Ordered list
            if tok.type == "ordered_list_open":
                list_blocks, consumed = self._process_list(
                    tokens[i:], "ordered_list", _numbered_list_item
                )
                blocks.extend(list_blocks)
                i += consumed
                continue

            # Blockquote
            if tok.type == "blockquote_open":
                inner_blocks, consumed = self._process_blockquote(tokens[i:])
                blocks.extend(inner_blocks)
                i += consumed
                continue

            # Table
            if tok.type == "table_open":
                table_block, consumed = self._process_table(tokens[i:])
                blocks.append(table_block)
                i += consumed
                continue

            # Horizontal rule
            if tok.type == "hr":
                blocks.append(_divider_block())
                i += 1
                continue

            # HTML blocks (pass through as paragraph)
            if tok.type == "html_block":
                content = tok.content.strip()
                if content:
                    blocks.append(_paragraph_block([_text(content)]))
                i += 1
                continue

            # Skip tokens we don't handle
            i += 1

        return blocks

    def _inline_to_rich_text(self, token: Token | None) -> list[dict]:
        """Convert an inline token's children to rich_text."""
        if token is None or not token.children:
            content = token.content if token else ""
            return [_text(content)] if content else []
        return self.inline_converter.convert(token.children)

    def _check_image_paragraph(self, inline_tok: Token | None) -> dict | None:
        """If a paragraph contains only an image, return an image block."""
        if inline_tok is None or not inline_tok.children:
            return None

        children = inline_tok.children
        # Single image token (possibly with softbreaks around it)
        image_tokens = [c for c in children if c.type == "image"]
        non_whitespace = [
            c for c in children
            if c.type not in ("image", "softbreak", "hardbreak")
            and not (c.type == "text" and not c.content.strip())
        ]

        if len(image_tokens) == 1 and not non_whitespace:
            img = image_tokens[0]
            src = img.attrGet("src") or ""
            alt = img.content or ""
            return image_block(src, alt, self.doc.path, self.raw_url_base)

        return None

    def _process_list(self, tokens: list[Token], list_type: str,
                      item_factory: Any) -> tuple[list[dict], int]:
        """Process a list (bullet or ordered) and return blocks + tokens consumed."""
        blocks: list[dict] = []
        depth = 0
        i = 0

        while i < len(tokens):
            tok = tokens[i]

            if tok.type == f"{list_type}_open":
                depth += 1
                i += 1
                continue

            if tok.type == f"{list_type}_close":
                depth -= 1
                i += 1
                if depth == 0:
                    break
                continue

            if tok.type == "list_item_open":
                item_blocks, consumed = self._process_list_item(
                    tokens[i:], item_factory
                )
                blocks.extend(item_blocks)
                i += consumed
                continue

            i += 1

        return blocks, i

    def _process_list_item(self, tokens: list[Token],
                           item_factory: Any) -> tuple[list[dict], int]:
        """Process a single list item, including nested lists."""
        depth = 0
        i = 0
        item_rich_text: list[dict] = []
        children: list[dict] = []

        while i < len(tokens):
            tok = tokens[i]

            if tok.type == "list_item_open":
                depth += 1
                i += 1
                continue

            if tok.type == "list_item_close":
                depth -= 1
                i += 1
                if depth == 0:
                    break
                continue

            # Paragraph inside list item → the item text
            if tok.type == "paragraph_open" and not item_rich_text:
                inline_tok = tokens[i + 1] if i + 1 < len(tokens) else None
                item_rich_text = self._inline_to_rich_text(inline_tok)
                i += 3  # paragraph_open, inline, paragraph_close
                continue

            # Nested bullet list
            if tok.type == "bullet_list_open":
                nested, consumed = self._process_list(
                    tokens[i:], "bullet_list", _bulleted_list_item
                )
                children.extend(nested)
                i += consumed
                continue

            # Nested ordered list
            if tok.type == "ordered_list_open":
                nested, consumed = self._process_list(
                    tokens[i:], "ordered_list", _numbered_list_item
                )
                children.extend(nested)
                i += consumed
                continue

            i += 1

        if not item_rich_text:
            item_rich_text = [_text("")]

        block = item_factory(item_rich_text, children if children else None)
        return [block], i

    def _process_blockquote(self, tokens: list[Token]) -> tuple[list[dict], int]:
        """Process a blockquote, collecting inner content."""
        blocks: list[dict] = []
        depth = 0
        i = 0
        collected_text: list[dict] = []

        while i < len(tokens):
            tok = tokens[i]

            if tok.type == "blockquote_open":
                depth += 1
                i += 1
                continue

            if tok.type == "blockquote_close":
                depth -= 1
                i += 1
                if depth == 0:
                    break
                continue

            if tok.type == "paragraph_open":
                inline_tok = tokens[i + 1] if i + 1 < len(tokens) else None
                rt = self._inline_to_rich_text(inline_tok)
                if collected_text:
                    collected_text.append(_text("\n"))
                collected_text.extend(rt)
                i += 3
                continue

            i += 1

        if collected_text:
            blocks.append(_quote_block(collected_text))

        return blocks, i

    def _process_table(self, tokens: list[Token]) -> tuple[dict, int]:
        """Process a table and return a table block + tokens consumed."""
        rows: list[list[list[dict]]] = []
        has_header = False
        i = 0
        depth = 0

        while i < len(tokens):
            tok = tokens[i]

            if tok.type == "table_open":
                depth += 1
                i += 1
                continue

            if tok.type == "table_close":
                depth -= 1
                i += 1
                if depth == 0:
                    break
                continue

            if tok.type == "thead_open":
                has_header = True
                i += 1
                continue

            if tok.type in ("thead_close", "tbody_open", "tbody_close"):
                i += 1
                continue

            if tok.type == "tr_open":
                row: list[list[dict]] = []
                i += 1
                while i < len(tokens) and tokens[i].type != "tr_close":
                    if tokens[i].type in ("th_open", "td_open"):
                        i += 1
                        if i < len(tokens) and tokens[i].type == "inline":
                            cell_rt = self._inline_to_rich_text(tokens[i])
                            row.append(cell_rt)
                            i += 1
                        else:
                            row.append([_text("")])
                        # Skip th_close / td_close
                        if i < len(tokens) and tokens[i].type in ("th_close", "td_close"):
                            i += 1
                    else:
                        i += 1
                rows.append(row)
                i += 1  # tr_close
                continue

            i += 1

        return _table_block(rows, has_header), i


# ---------------------------------------------------------------------------
# Convenience function
# ---------------------------------------------------------------------------


def markdown_to_blocks(doc: ParsedDoc,
                       page_id_lookup: dict[str, str] | None = None,
                       raw_url_base: str = "") -> list[dict]:
    """Convert a parsed document's markdown to Notion blocks."""
    converter = MarkdownToNotionConverter(doc, page_id_lookup, raw_url_base)
    return converter.convert()


def text_to_blocks(text: str) -> list[dict]:
    """Convert raw markdown text to Notion blocks (without doc context)."""
    from .frontmatter import ParsedDoc
    dummy = ParsedDoc(path=Path("."), metadata={}, content=text)
    converter = MarkdownToNotionConverter(dummy)
    return converter.convert(text)
