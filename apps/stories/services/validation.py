"""
Block Validation Service

Validates BlockNote block structures following Django Development Guidelines.
Implements Single Responsibility Principle and comprehensive error handling.
"""

import logging
from dataclasses import dataclass
from typing import Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class ValidationError:
    """Validation error structure"""

    code: str
    message: str
    field: Optional[str] = None
    block_id: Optional[str] = None


@dataclass
class ValidationWarning:
    """Validation warning structure"""

    code: str
    message: str
    field: Optional[str] = None
    block_id: Optional[str] = None


@dataclass
class ValidationResult:
    """Complete validation result"""

    is_valid: bool
    errors: list[ValidationError]
    warnings: list[ValidationWarning]


class BlockValidationService:
    """
    Service for validating BlockNote block structures.
    Follows Single Responsibility Principle and Django Development Guidelines.
    """

    SUPPORTED_BLOCK_TYPES = {"heading", "paragraph", "dialog", "image", "video", "clip"}
    SUPPORTED_HEADING_LEVELS = {1, 2, 3}
    MAX_BLOCK_CONTENT_LENGTH = 10000
    MAX_TAG_LENGTH = 50
    MAX_NODE_NAME_LENGTH = 255

    @staticmethod
    def validate_story_node(node_data: dict[str, Any]) -> ValidationResult:
        """
        Validate complete story node data structure.

        Args:
            node_data: Dictionary containing node data with name, node_data, and tags

        Returns:
            ValidationResult with errors and warnings
        """
        errors = []
        warnings = []

        try:
            # Validate name field
            name_result = BlockValidationService._validate_node_name(
                node_data.get("name", "")
            )
            errors.extend(name_result.errors)
            warnings.extend(name_result.warnings)

            # Validate node_data content
            node_content = node_data.get("node_data", {})
            content_result = BlockValidationService._validate_node_content(node_content)
            errors.extend(content_result.errors)
            warnings.extend(content_result.warnings)

            # Validate tags if present
            tags = node_data.get("tags", [])
            if tags:
                tags_result = BlockValidationService._validate_node_tags(tags)
                errors.extend(tags_result.errors)
                warnings.extend(tags_result.warnings)

        except Exception as e:
            logger.error(
                f"Validation error: {e}",
                extra={"node_data": node_data, "error": str(e)},
            )
            errors.append(
                ValidationError(
                    code="VALIDATION_EXCEPTION",
                    message=f"Validation failed with error: {str(e)}",
                )
            )

        return ValidationResult(
            is_valid=len(errors) == 0, errors=errors, warnings=warnings
        )

    @staticmethod
    def _validate_node_name(name: str) -> ValidationResult:
        """Validate node name field"""
        errors = []
        warnings = []

        # Required field check
        if not name or not name.strip():
            errors.append(
                ValidationError(
                    code="NAME_REQUIRED", message="Node name is required", field="name"
                )
            )
        else:
            # Length validation
            if len(name) > BlockValidationService.MAX_NODE_NAME_LENGTH:
                errors.append(
                    ValidationError(
                        code="NAME_TOO_LONG",
                        message=f"Node name must be {BlockValidationService.MAX_NODE_NAME_LENGTH} characters or less",
                        field="name",
                    )
                )

            # Content warnings
            if len(name.strip()) < 3:
                warnings.append(
                    ValidationWarning(
                        code="NAME_TOO_SHORT",
                        message="Node name is very short, consider a more descriptive name",
                        field="name",
                    )
                )

            # Special character check
            dangerous_chars = set("<>'\"&")
            if any(char in name for char in dangerous_chars):
                warnings.append(
                    ValidationWarning(
                        code="NAME_SPECIAL_CHARS",
                        message="Node name contains special characters that may cause display issues",
                        field="name",
                    )
                )

        return ValidationResult(
            is_valid=len(errors) == 0, errors=errors, warnings=warnings
        )

    @staticmethod
    def _validate_node_content(node_data: dict[str, Any]) -> ValidationResult:
        """Validate node content structure"""
        errors = []
        warnings = []

        if not node_data:
            errors.append(
                ValidationError(
                    code="CONTENT_MISSING",
                    message="Node content data is missing",
                    field="node_data",
                )
            )
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)

        # Validate version
        version = node_data.get("version")
        if not version:
            warnings.append(
                ValidationWarning(
                    code="VERSION_MISSING",
                    message="Content version not specified, defaulting to 2.0",
                    field="node_data.version",
                )
            )
        elif version != "2.0":
            warnings.append(
                ValidationWarning(
                    code="VERSION_UNSUPPORTED",
                    message=f"Content version {version} may not be fully supported",
                    field="node_data.version",
                )
            )

        # Validate blocks array
        blocks = node_data.get("blocks", [])
        if not isinstance(blocks, list):
            errors.append(
                ValidationError(
                    code="BLOCKS_MISSING",
                    message="Blocks array is missing or invalid",
                    field="node_data.blocks",
                )
            )
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)

        # Validate individual blocks
        for index, block in enumerate(blocks):
            block_result = BlockValidationService._validate_block(block, index)
            errors.extend(block_result.errors)
            warnings.extend(block_result.warnings)

        # Content quality checks
        if len(blocks) == 0:
            warnings.append(
                ValidationWarning(
                    code="CONTENT_EMPTY",
                    message="Node has no content blocks",
                    field="node_data.blocks",
                )
            )

        # Check for content-less blocks
        empty_blocks = [
            block for block in blocks if not str(block.get("content", "")).strip()
        ]
        if empty_blocks:
            warnings.append(
                ValidationWarning(
                    code="EMPTY_BLOCKS",
                    message=f"{len(empty_blocks)} blocks have no content",
                    field="node_data.blocks",
                )
            )

        return ValidationResult(
            is_valid=len(errors) == 0, errors=errors, warnings=warnings
        )

    @staticmethod
    def _validate_block(block: dict[str, Any], index: int) -> ValidationResult:
        """Validate individual block structure"""
        errors = []
        warnings = []

        # Basic structure validation
        if not isinstance(block, dict):
            errors.append(
                ValidationError(
                    code="BLOCK_INVALID",
                    message=f"Block {index} is not a valid dictionary",
                    field="node_data.blocks",
                )
            )
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)

        # ID validation
        block_id = block.get("id")
        if not block_id:
            errors.append(
                ValidationError(
                    code="BLOCK_ID_MISSING",
                    message=f"Block {index} is missing an ID",
                    field="node_data.blocks",
                )
            )
        elif not isinstance(block_id, str) or len(block_id) == 0:
            errors.append(
                ValidationError(
                    code="BLOCK_ID_INVALID",
                    message=f"Block {index} has an invalid ID",
                    field="node_data.blocks",
                    block_id=str(block_id),
                )
            )

        # Type validation
        block_type = block.get("type")
        if not block_type:
            errors.append(
                ValidationError(
                    code="BLOCK_TYPE_MISSING",
                    message=f"Block {index} is missing type",
                    field="node_data.blocks",
                    block_id=str(block_id),
                )
            )
        elif block_type not in BlockValidationService.SUPPORTED_BLOCK_TYPES:
            errors.append(
                ValidationError(
                    code="BLOCK_TYPE_UNSUPPORTED",
                    message=f"Block {index} has unsupported type: {block_type}",
                    field="node_data.blocks",
                    block_id=str(block_id),
                )
            )

        # Content length validation
        content = str(block.get("content", ""))
        if len(content) > BlockValidationService.MAX_BLOCK_CONTENT_LENGTH:
            errors.append(
                ValidationError(
                    code="BLOCK_CONTENT_TOO_LONG",
                    message=f"Block {index} content is too long ({len(content)} characters)",
                    field="node_data.blocks",
                    block_id=str(block_id),
                )
            )

        # Type-specific validation
        if block_type == "heading":
            heading_result = BlockValidationService._validate_heading_block(
                block, index
            )
            errors.extend(heading_result.errors)
            warnings.extend(heading_result.warnings)
        elif block_type == "paragraph":
            paragraph_result = BlockValidationService._validate_paragraph_block(
                block, index
            )
            errors.extend(paragraph_result.errors)
            warnings.extend(paragraph_result.warnings)
        elif block_type == "dialog":
            dialog_result = BlockValidationService._validate_dialog_block(
                block, index
            )
            errors.extend(dialog_result.errors)
            warnings.extend(dialog_result.warnings)
        elif block_type == "image":
            image_result = BlockValidationService._validate_image_block(block, index)
            errors.extend(image_result.errors)
            warnings.extend(image_result.warnings)
        elif block_type == "video":
            video_result = BlockValidationService._validate_video_block(block, index)
            errors.extend(video_result.errors)
            warnings.extend(video_result.warnings)

        return ValidationResult(
            is_valid=len(errors) == 0, errors=errors, warnings=warnings
        )

    @staticmethod
    def _validate_heading_block(block: dict[str, Any], index: int) -> ValidationResult:
        """Validate heading block specific properties"""
        errors = []
        warnings = []

        props = block.get("props", {})
        level = props.get("level")

        # Level validation
        if not level:
            errors.append(
                ValidationError(
                    code="HEADING_LEVEL_MISSING",
                    message=f"Heading block {index} is missing level property",
                    field="node_data.blocks",
                    block_id=str(block.get("id")),
                )
            )
        elif level not in BlockValidationService.SUPPORTED_HEADING_LEVELS:
            errors.append(
                ValidationError(
                    code="HEADING_LEVEL_INVALID",
                    message=f"Heading block {index} has invalid level: {level}",
                    field="node_data.blocks",
                    block_id=str(block.get("id")),
                )
            )

        # Content warnings
        content = str(block.get("content", "")).strip()
        if not content:
            warnings.append(
                ValidationWarning(
                    code="HEADING_EMPTY",
                    message=f"Heading block {index} has no content",
                    field="node_data.blocks",
                    block_id=str(block.get("id")),
                )
            )
        elif len(content) > 100:
            warnings.append(
                ValidationWarning(
                    code="HEADING_LONG",
                    message=f"Heading block {index} is very long ({len(content)} characters)",
                    field="node_data.blocks",
                    block_id=str(block.get("id")),
                )
            )

        return ValidationResult(
            is_valid=len(errors) == 0, errors=errors, warnings=warnings
        )

    @staticmethod
    def _validate_paragraph_block(
        block: dict[str, Any], index: int
    ) -> ValidationResult:
        """Validate paragraph block specific properties"""
        errors = []
        warnings = []

        # Content warnings
        content = str(block.get("content", "")).strip()
        if not content:
            warnings.append(
                ValidationWarning(
                    code="PARAGRAPH_EMPTY",
                    message=f"Paragraph block {index} has no content",
                    field="node_data.blocks",
                    block_id=str(block.get("id")),
                )
            )

        return ValidationResult(
            is_valid=len(errors) == 0, errors=errors, warnings=warnings
        )

    @staticmethod
    def _validate_image_block(block: dict[str, Any], index: int) -> ValidationResult:
        errors = []
        warnings = []

        props = block.get("props", {}) or {}
        url = props.get("url")
        if not url or not isinstance(url, str) or not url.strip():
            errors.append(
                ValidationError(
                    code="IMAGE_URL_MISSING",
                    message=f"Image block {index} requires url property",
                    field="node_data.blocks",
                    block_id=str(block.get("id")),
                )
            )
        # Optional alt text recommendation
        if not props.get("alt"):
            warnings.append(
                ValidationWarning(
                    code="IMAGE_ALT_MISSING",
                    message=f"Image block {index} missing alt text",
                    field="node_data.blocks",
                    block_id=str(block.get("id")),
                )
            )
        return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)

    @staticmethod
    def _validate_video_block(block: dict[str, Any], index: int) -> ValidationResult:
        errors = []
        warnings = []

        props = block.get("props", {}) or {}
        url = props.get("url")
        if not url or not isinstance(url, str) or not url.strip():
            errors.append(
                ValidationError(
                    code="VIDEO_URL_MISSING",
                    message=f"Video block {index} requires url property",
                    field="node_data.blocks",
                    block_id=str(block.get("id")),
                )
            )
        # Autoplay policy
        if props.get("autoplay") and not props.get("muted"):
            warnings.append(
                ValidationWarning(
                    code="VIDEO_AUTOPLAY_MUTED",
                    message=f"Video block {index} has autoplay without muted; browsers may block playback",
                    field="node_data.blocks",
                    block_id=str(block.get("id")),
                )
            )
        return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)

    @staticmethod
    def _validate_dialog_block(block: dict[str, Any], index: int) -> ValidationResult:
        """Validate dialog block specific properties"""
        errors = []
        warnings = []

        props = block.get("props", {})
        speaker = props.get("speaker")

        # Speaker validation
        if not speaker:
            errors.append(
                ValidationError(
                    code="DIALOG_SPEAKER_MISSING",
                    message=f"Dialog block {index} is missing speaker property",
                    field="node_data.blocks",
                    block_id=str(block.get("id")),
                )
            )
        elif speaker not in {"player", "npc"}:
            errors.append(
                ValidationError(
                    code="DIALOG_SPEAKER_INVALID",
                    message=f"Dialog block {index} has invalid speaker: {speaker}",
                    field="node_data.blocks",
                    block_id=str(block.get("id")),
                )
            )

        # NPC-specific validation
        if speaker == "npc":
            if not props.get("npcName"):
                warnings.append(
                    ValidationWarning(
                        code="DIALOG_NPC_NAME_MISSING",
                        message=f"Dialog block {index} for NPC is missing npcName",
                        field="node_data.blocks",
                        block_id=str(block.get("id")),
                    )
                )

        # Content validation
        content = str(block.get("content", "")).strip()
        if not content:
            warnings.append(
                ValidationWarning(
                    code="DIALOG_EMPTY",
                    message=f"Dialog block {index} has no content",
                    field="node_data.blocks",
                    block_id=str(block.get("id")),
                )
            )

        return ValidationResult(
            is_valid=len(errors) == 0, errors=errors, warnings=warnings
        )

    @staticmethod
    def _validate_node_tags(tags: list[str]) -> ValidationResult:
        """Validate node tags array"""
        errors = []
        warnings = []

        if not isinstance(tags, list):
            errors.append(
                ValidationError(
                    code="TAGS_INVALID_TYPE",
                    message="Tags must be an array of strings",
                    field="tags",
                )
            )
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)

        # Validate individual tags
        for index, tag in enumerate(tags):
            if not isinstance(tag, str):
                errors.append(
                    ValidationError(
                        code="TAG_INVALID_TYPE",
                        message=f"Tag {index} must be a string",
                        field="tags",
                    )
                )
            elif len(tag) == 0:
                warnings.append(
                    ValidationWarning(
                        code="TAG_EMPTY", message=f"Tag {index} is empty", field="tags"
                    )
                )
            elif len(tag) > BlockValidationService.MAX_TAG_LENGTH:
                errors.append(
                    ValidationError(
                        code="TAG_TOO_LONG",
                        message=f"Tag {index} is too long ({len(tag)} characters, max {BlockValidationService.MAX_TAG_LENGTH})",
                        field="tags",
                    )
                )

        # Check for duplicates
        unique_tags = set(tag.lower() for tag in tags if isinstance(tag, str))
        if len(unique_tags) < len([tag for tag in tags if isinstance(tag, str)]):
            warnings.append(
                ValidationWarning(
                    code="DUPLICATE_TAGS",
                    message="Some tags are duplicated",
                    field="tags",
                )
            )

        return ValidationResult(
            is_valid=len(errors) == 0, errors=errors, warnings=warnings
        )

    @staticmethod
    def format_validation_errors(result: ValidationResult) -> list[str]:
        """Format validation errors for API response"""
        formatted_errors = []

        for error in result.errors:
            if error.field and error.block_id:
                formatted_errors.append(
                    f"{error.field} ({error.block_id}): {error.message}"
                )
            elif error.field:
                formatted_errors.append(f"{error.field}: {error.message}")
            else:
                formatted_errors.append(error.message)

        return formatted_errors

    @staticmethod
    def format_validation_warnings(result: ValidationResult) -> list[str]:
        """Format validation warnings for API response"""
        formatted_warnings = []

        for warning in result.warnings:
            if warning.field and warning.block_id:
                formatted_warnings.append(
                    f"{warning.field} ({warning.block_id}): {warning.message}"
                )
            elif warning.field:
                formatted_warnings.append(f"{warning.field}: {warning.message}")
            else:
                formatted_warnings.append(warning.message)

        return formatted_warnings
