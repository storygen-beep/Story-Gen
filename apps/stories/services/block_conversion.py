"""
Block Conversion Service

Handles conversion between different content formats in the backend.
Follows Django Development Guidelines and Single Responsibility Principle.
"""

import html
import logging
import re
import uuid
from typing import Any

logger = logging.getLogger(__name__)


class BlockConversionService:
    """
    Service for converting between different content formats.
    Handles legacy text content to BlockNote blocks conversion.
    """

    DEFAULT_VERSION = "2.0"

    @staticmethod
    def legacy_content_to_blocks(legacy_content: str) -> list[dict[str, Any]]:
        """
        Convert legacy text content to BlockNote blocks.

        Args:
            legacy_content: Plain text content from legacy system

        Returns:
            List of BlockNote block dictionaries
        """
        if not legacy_content or not legacy_content.strip():
            return [BlockConversionService._create_default_paragraph()]

        try:
            lines = [line for line in legacy_content.split("\n") if line.strip()]
            blocks = []

            for line in lines:
                trimmed_line = line.strip()

                # Detect heading patterns
                if trimmed_line.startswith("# "):
                    blocks.append(
                        BlockConversionService._create_heading_block(
                            level=1, content=trimmed_line[2:].strip()
                        )
                    )
                elif trimmed_line.startswith("## "):
                    blocks.append(
                        BlockConversionService._create_heading_block(
                            level=2, content=trimmed_line[3:].strip()
                        )
                    )
                elif trimmed_line.startswith("### "):
                    blocks.append(
                        BlockConversionService._create_heading_block(
                            level=3, content=trimmed_line[4:].strip()
                        )
                    )
                else:
                    # Default to paragraph
                    blocks.append(
                        BlockConversionService._create_paragraph_block(
                            content=trimmed_line
                        )
                    )

            return (
                blocks
                if blocks
                else [BlockConversionService._create_default_paragraph()]
            )

        except Exception as e:
            logger.error(
                f"Error converting legacy content to blocks: {e}",
                extra={
                    "legacy_content": legacy_content[:100] + "..."
                    if len(legacy_content) > 100
                    else legacy_content,
                    "error": str(e),
                },
            )
            return [BlockConversionService._create_default_paragraph()]

    @staticmethod
    def blocks_to_html(blocks: list[dict[str, Any]]) -> str:
        """
        Convert BlockNote blocks to HTML for display.

        Args:
            blocks: List of BlockNote block dictionaries

        Returns:
            HTML string representation of the blocks
        """
        if not blocks or len(blocks) == 0:
            return '<p class="text-gray-400 italic">No content specified</p>'

        try:
            html_parts = []

            for block in blocks:
                if not BlockConversionService._is_valid_block_structure(block):
                    html_parts.append(
                        f'<p class="text-red-400">Invalid block: {block.get("type", "unknown")}</p>'
                    )
                    continue

                content = html.escape(str(block.get("content", "")))
                block_type = block.get("type")

                if block_type == "heading":
                    level = block.get("props", {}).get("level", 1)
                    heading_class = BlockConversionService._get_heading_class(level)
                    html_parts.append(
                        f'<h{level} class="{heading_class}">{content}</h{level}>'
                    )

                elif block_type == "paragraph":
                    html_parts.append(
                        f'<p class="text-gray-700 leading-relaxed">{content}</p>'
                    )

                elif block_type == "dialog":
                    props = block.get("props", {})
                    speaker = props.get("speaker", "npc")
                    npc_name = props.get("npcName", "NPC")

                    if speaker == "player":
                        speaker_label = "Player"
                        dialog_class = "bg-blue-50 border-l-4 border-blue-500 pl-3 py-2 my-2"
                        speaker_class = "font-semibold text-blue-700"
                    else:
                        speaker_label = html.escape(npc_name)
                        dialog_class = "bg-gray-50 border-l-4 border-gray-400 pl-3 py-2 my-2"
                        speaker_class = "font-semibold text-gray-700"

                    html_parts.append(
                        f'<div class="{dialog_class}">'
                        f'<span class="{speaker_class}">{speaker_label}:</span> '
                        f'<span class="text-gray-800">{content}</span>'
                        f'</div>'
                    )

                elif block_type == "image":
                    props = block.get("props", {})
                    url = html.escape(str(props.get("url", "")))
                    alt = html.escape(str(props.get("alt", "")))
                    if not url:
                        continue
                    style = "max-width:100%;height:auto;border-radius:8px;"
                    html_parts.append(
                        f'<img src="{url}" alt="{alt}" loading="lazy" decoding="async" style="{style}" />'
                    )
                elif block_type == "video":
                    props = block.get("props", {})
                    url = html.escape(str(props.get("url", "")))
                    poster = html.escape(str(props.get("poster", ""))) if props.get("poster") else ""
                    controls = " controls"
                    preload = " metadata"
                    # Do not autoplay by default
                    poster_attr = f' poster="{poster}"' if poster else ""
                    style = "max-width:100%;height:auto;border-radius:8px;"
                    html_parts.append(
                        f'<video src="{url}"{controls}{poster_attr} preload="metadata" style="{style}"></video>'
                    )
                else:
                    # Fallback to paragraph
                    html_parts.append(
                        f'<p class="text-gray-700 leading-relaxed">{content}</p>'
                    )

            return "".join(html_parts)

        except Exception as e:
            logger.error(
                f"Error converting blocks to HTML: {e}",
                extra={"blocks_count": len(blocks), "error": str(e)},
            )
            return '<p class="text-red-400">Error rendering content</p>'

    @staticmethod
    def blocks_to_plain_text(blocks: list[dict[str, Any]]) -> str:
        """
        Convert BlockNote blocks to plain text.

        Args:
            blocks: List of BlockNote block dictionaries

        Returns:
            Plain text representation of the blocks
        """
        if not blocks or len(blocks) == 0:
            return ""

        try:
            text_parts = []

            for block in blocks:
                # Recurse into group blocks to extract child text
                if block.get("type") == "group":
                    child_blocks = (block.get("props") or {}).get("blocks", [])
                    if child_blocks:
                        child_text = BlockConversionService.blocks_to_plain_text(child_blocks)
                        if child_text:
                            text_parts.append(child_text)
                    continue
                content = str(block.get("content", "")).strip()
                if content:
                    text_parts.append(content)

            return "\n".join(text_parts)

        except Exception as e:
            logger.error(
                f"Error converting blocks to plain text: {e}",
                extra={"blocks_count": len(blocks), "error": str(e)},
            )
            return ""

    @staticmethod
    def migrate_node_data(node_data: dict[str, Any]) -> dict[str, Any]:
        """
        Migrate node_data from legacy format to new block format.

        Args:
            node_data: Node data dictionary (may be legacy or new format)

        Returns:
            Node data in new block format
        """
        try:
            # If already in block format, validate and return
            if BlockConversionService._is_block_format(node_data):
                return {
                    "blocks": BlockConversionService._sanitize_blocks(
                        node_data.get("blocks", [])
                    ),
                    "version": node_data.get(
                        "version", BlockConversionService.DEFAULT_VERSION
                    ),
                    "content": node_data.get("content"),  # Preserve legacy content
                }

            # Convert from legacy content format
            legacy_content = str(node_data.get("content", ""))
            blocks = BlockConversionService.legacy_content_to_blocks(legacy_content)

            return {
                "blocks": blocks,
                "version": BlockConversionService.DEFAULT_VERSION,
                "content": legacy_content,  # Preserve for backward compatibility
            }

        except Exception as e:
            logger.error(
                f"Error migrating node data: {e}",
                extra={
                    "node_data": str(node_data)[:200] + "..."
                    if len(str(node_data)) > 200
                    else str(node_data),
                    "error": str(e),
                },
            )

            # Return safe default
            return {
                "blocks": [BlockConversionService._create_default_paragraph()],
                "version": BlockConversionService.DEFAULT_VERSION,
                "content": str(node_data.get("content", "")) if node_data else "",
            }

    @staticmethod
    def get_content_stats(blocks: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Calculate content statistics from blocks.

        Args:
            blocks: List of BlockNote block dictionaries

        Returns:
            Dictionary with content statistics
        """
        try:
            heading_count = len([b for b in blocks if b.get("type") == "heading"])
            paragraph_count = len([b for b in blocks if b.get("type") == "paragraph"])
            dialog_count = len([b for b in blocks if b.get("type") == "dialog"])

            # Count words
            total_words = 0
            for block in blocks:
                content = str(block.get("content", ""))
                words = re.findall(r"\S+", content)
                total_words += len(words)

            # Check if content is empty
            is_empty = len(blocks) == 0 or all(
                not str(block.get("content", "")).strip() for block in blocks
            )

            return {
                "heading_count": heading_count,
                "paragraph_count": paragraph_count,
                "dialog_count": dialog_count,
                "total_blocks": len(blocks),
                "total_words": total_words,
                "is_empty": is_empty,
            }

        except Exception as e:
            logger.error(
                f"Error calculating content stats: {e}",
                extra={"blocks_count": len(blocks) if blocks else 0, "error": str(e)},
            )
            return {
                "heading_count": 0,
                "paragraph_count": 0,
                "total_blocks": 0,
                "total_words": 0,
                "is_empty": True,
            }

    @staticmethod
    def get_preview_text(blocks: list[dict[str, Any]], max_length: int = 100) -> str:
        """
        Get preview text from blocks.

        Args:
            blocks: List of BlockNote block dictionaries
            max_length: Maximum length of preview text

        Returns:
            Preview text string
        """
        plain_text = BlockConversionService.blocks_to_plain_text(blocks)

        if len(plain_text) <= max_length:
            return plain_text

        return plain_text[: max_length - 3] + "..."

    # Private helper methods

    @staticmethod
    def _create_default_paragraph() -> dict[str, Any]:
        """Create a default empty paragraph block"""
        return {
            "id": str(uuid.uuid4()),
            "type": "paragraph",
            "props": {},
            "content": "",
            "children": [],
        }

    @staticmethod
    def _create_paragraph_block(content: str) -> dict[str, Any]:
        """Create a paragraph block with content"""
        return {
            "id": str(uuid.uuid4()),
            "type": "paragraph",
            "props": {},
            "content": content,
            "children": [],
        }

    @staticmethod
    def _create_heading_block(level: int, content: str) -> dict[str, Any]:
        """Create a heading block with level and content"""
        return {
            "id": str(uuid.uuid4()),
            "type": "heading",
            "props": {"level": level},
            "content": content,
            "children": [],
        }

    @staticmethod
    def _is_valid_block_structure(block: dict[str, Any]) -> bool:
        """Check if block has valid basic structure"""
        if not isinstance(block, dict):
            return False

        required_fields = ["id", "type"]
        for field in required_fields:
            if field not in block:
                return False

        # Accept media blocks (image, video, clip), group (conditional variants), and block_pool (random variants)
        supported_types = {"heading", "paragraph", "dialog", "image", "video", "clip", "group", "block_pool"}
        if block.get("type") not in supported_types:
            return False

        return True

    @staticmethod
    def _is_block_format(node_data: dict[str, Any]) -> bool:
        """Check if node_data is already in block format"""
        if not node_data or not isinstance(node_data, dict):
            return False

        return (
            "blocks" in node_data
            and isinstance(node_data.get("blocks"), list)
            and node_data.get("version") == BlockConversionService.DEFAULT_VERSION
        )

    @staticmethod
    def _sanitize_blocks(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Sanitize and validate blocks array"""
        if not isinstance(blocks, list):
            return [BlockConversionService._create_default_paragraph()]

        sanitized_blocks = []

        for block in blocks:
            if BlockConversionService._is_valid_block_structure(block):
                sanitized_block = {
                    "id": str(block.get("id", uuid.uuid4())),
                    "type": block.get("type"),
                    "props": BlockConversionService._sanitize_block_props(
                        block.get("props", {})
                    ),
                    "content": BlockConversionService._sanitize_block_content(
                        block.get("content", "")
                    ),
                    "children": [],  # No nested content in Phase 1
                }
                sanitized_blocks.append(sanitized_block)

        return (
            sanitized_blocks
            if sanitized_blocks
            else [BlockConversionService._create_default_paragraph()]
        )

    @staticmethod
    def _sanitize_block_props(props: dict[str, Any]) -> dict[str, Any]:
        """Sanitize block properties"""
        if not isinstance(props, dict):
            return {}

        sanitized = {}

        # Validate heading level
        if "level" in props and props["level"] in {1, 2, 3}:
            sanitized["level"] = props["level"]

        # Validate colors (basic validation)
        color_pattern = re.compile(r"^#[0-9A-Fa-f]{6}$")
        if "textColor" in props and color_pattern.match(str(props["textColor"])):
            sanitized["textColor"] = props["textColor"]

        if "backgroundColor" in props and color_pattern.match(
            str(props["backgroundColor"])
        ):
            sanitized["backgroundColor"] = props["backgroundColor"]

        # Validate dialog properties
        if "speaker" in props and props["speaker"] in {"player", "npc"}:
            sanitized["speaker"] = props["speaker"]

        if "npcId" in props and isinstance(props["npcId"], str):
            sanitized["npcId"] = props["npcId"]

        if "npcName" in props and isinstance(props["npcName"], str):
            sanitized["npcName"] = props["npcName"]

        # Validate image properties
        if "url" in props and isinstance(props["url"], str):
            url = props["url"].strip()
            if url:
                sanitized["url"] = url
        if "alt" in props and isinstance(props["alt"], str):
            sanitized["alt"] = props["alt"].strip()
        if "caption" in props and isinstance(props["caption"], str):
            sanitized["caption"] = props["caption"].strip()
        if "width" in props:
            try:
                w = int(props["width"])  # type: ignore[arg-type]
                if w > 0:
                    sanitized["width"] = min(w, 4096)
            except Exception:
                pass
        if "height" in props:
            try:
                h = int(props["height"])  # type: ignore[arg-type]
                if h > 0:
                    sanitized["height"] = min(h, 4096)
            except Exception:
                pass

        # Validate video properties
        if "poster" in props and isinstance(props["poster"], str):
            poster = props["poster"].strip()
            if poster:
                sanitized["poster"] = poster
        if "controls" in props and isinstance(props["controls"], bool):
            sanitized["controls"] = props["controls"]
        if "autoplay" in props and isinstance(props["autoplay"], bool):
            sanitized["autoplay"] = props["autoplay"]
        if "muted" in props and isinstance(props["muted"], bool):
            sanitized["muted"] = props["muted"]
        if "loop" in props and isinstance(props["loop"], bool):
            sanitized["loop"] = props["loop"]

        # Validate clip properties
        if "clipId" in props and isinstance(props["clipId"], str):
            clip_id = props["clipId"].strip()
            if clip_id:
                sanitized["clipId"] = clip_id

        # Validate group properties (conditional variant blocks)
        if "conditions" in props and isinstance(props["conditions"], dict):
            sanitized["conditions"] = props["conditions"]
        if "blocks" in props and isinstance(props["blocks"], list):
            sanitized["blocks"] = props["blocks"]

        return sanitized

    @staticmethod
    def _sanitize_block_content(content: Any) -> str:
        """Sanitize block content"""
        if not isinstance(content, str):
            content = str(content) if content is not None else ""

        # Remove dangerous HTML tags
        content = re.sub(
            r"<script[^>]*>.*?</script>", "", content, flags=re.IGNORECASE | re.DOTALL
        )
        content = re.sub(r"<[^>]*>", "", content)

        return content.strip()

    @staticmethod
    def _get_heading_class(level: int) -> str:
        """Get CSS classes for heading levels"""
        classes = {
            1: "text-xl font-bold text-gray-900 mb-2",
            2: "text-lg font-semibold text-gray-800 mb-1",
            3: "text-md font-medium text-gray-800 mb-1",
        }
        return classes.get(level, classes[1])
