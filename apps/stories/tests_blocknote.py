"""
BlockNote Integration Tests

Tests for BlockNote validation and conversion services.
Follows Django Development Guidelines and SOLID principles.
"""

from django.test import TestCase

from .services.block_conversion import BlockConversionService
from .services.validation import BlockValidationService


class BlockConversionServiceTest(TestCase):
    """Test BlockNote conversion functionality."""

    def test_legacy_content_to_blocks_simple(self):
        """Test converting simple text to blocks."""
        content = "This is a simple paragraph."
        blocks = BlockConversionService.legacy_content_to_blocks(content)

        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0]["type"], "paragraph")
        self.assertEqual(blocks[0]["content"], "This is a simple paragraph.")
        self.assertIn("id", blocks[0])

    def test_legacy_content_to_blocks_headings(self):
        """Test converting headings to blocks."""
        content = "# Main Title\n## Subtitle\n### Sub-subtitle"
        blocks = BlockConversionService.legacy_content_to_blocks(content)

        self.assertEqual(len(blocks), 3)

        # Check heading levels
        self.assertEqual(blocks[0]["type"], "heading")
        self.assertEqual(blocks[0]["props"]["level"], 1)
        self.assertEqual(blocks[0]["content"], "Main Title")

        self.assertEqual(blocks[1]["type"], "heading")
        self.assertEqual(blocks[1]["props"]["level"], 2)
        self.assertEqual(blocks[1]["content"], "Subtitle")

        self.assertEqual(blocks[2]["type"], "heading")
        self.assertEqual(blocks[2]["props"]["level"], 3)
        self.assertEqual(blocks[2]["content"], "Sub-subtitle")

    def test_legacy_content_to_blocks_mixed(self):
        """Test converting mixed content to blocks."""
        content = "# Title\nThis is content.\n## Section\nMore content."
        blocks = BlockConversionService.legacy_content_to_blocks(content)

        self.assertEqual(len(blocks), 4)
        self.assertEqual(blocks[0]["type"], "heading")
        self.assertEqual(blocks[1]["type"], "paragraph")
        self.assertEqual(blocks[2]["type"], "heading")
        self.assertEqual(blocks[3]["type"], "paragraph")

    def test_legacy_content_to_blocks_empty(self):
        """Test converting empty content."""
        blocks = BlockConversionService.legacy_content_to_blocks("")

        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0]["type"], "paragraph")
        self.assertEqual(blocks[0]["content"], "")

    def test_blocks_to_html(self):
        """Test converting blocks to HTML."""
        blocks = [
            {
                "id": "test-1",
                "type": "heading",
                "props": {"level": 1},
                "content": "Test Title",
                "children": []
            },
            {
                "id": "test-2",
                "type": "paragraph",
                "props": {},
                "content": "Test content",
                "children": []
            }
        ]

        html = BlockConversionService.blocks_to_html(blocks)

        self.assertIn('<h1', html)
        self.assertIn('Test Title', html)
        self.assertIn('<p', html)
        self.assertIn('Test content', html)

    def test_blocks_to_plain_text(self):
        """Test converting blocks to plain text."""
        blocks = [
            {
                "id": "test-1",
                "type": "heading",
                "props": {"level": 1},
                "content": "Test Title",
                "children": []
            },
            {
                "id": "test-2",
                "type": "paragraph",
                "props": {},
                "content": "Test content",
                "children": []
            }
        ]

        text = BlockConversionService.blocks_to_plain_text(blocks)

        self.assertEqual(text, "Test Title\nTest content")

    def test_migrate_node_data_legacy(self):
        """Test migrating legacy node data."""
        legacy_data = {
            "content": "# Title\nSome content",
            "version": "1.0"
        }

        migrated = BlockConversionService.migrate_node_data(legacy_data)

        self.assertIn("blocks", migrated)
        self.assertIn("version", migrated)
        self.assertEqual(migrated["version"], "2.0")
        self.assertGreater(len(migrated["blocks"]), 0)

    def test_migrate_node_data_already_blocks(self):
        """Test migrating already-converted node data."""
        block_data = {
            "blocks": [
                {
                    "id": "test-1",
                    "type": "paragraph",
                    "props": {},
                    "content": "Test",
                    "children": []
                }
            ],
            "version": "2.0"
        }

        migrated = BlockConversionService.migrate_node_data(block_data)

        self.assertEqual(migrated["blocks"], block_data["blocks"])
        self.assertEqual(migrated["version"], "2.0")


class BlockValidationServiceTest(TestCase):
    """Test BlockNote validation functionality."""

    def test_validate_story_node_valid(self):
        """Test validating a valid story node."""
        node_data = {
            "name": "Test Node",
            "node_data": {
                "blocks": [
                    {
                        "id": "test-123",
                        "type": "heading",
                        "props": {"level": 1},
                        "content": "Test Heading",
                        "children": []
                    }
                ],
                "version": "2.0"
            },
            "tags": ["test"]
        }

        result = BlockValidationService.validate_story_node(node_data)

        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)

    def test_validate_story_node_missing_name(self):
        """Test validating node with missing name."""
        node_data = {
            "name": "",
            "node_data": {
                "blocks": [],
                "version": "2.0"
            },
            "tags": []
        }

        result = BlockValidationService.validate_story_node(node_data)

        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)

        # Check for name required error
        name_errors = [e for e in result.errors if e.code == "NAME_REQUIRED"]
        self.assertGreater(len(name_errors), 0)

    def test_validate_story_node_invalid_block(self):
        """Test validating node with invalid block."""
        node_data = {
            "name": "Test Node",
            "node_data": {
                "blocks": [
                    {
                        "id": "test-123",
                        "type": "invalid_type",  # Invalid block type
                        "props": {},
                        "content": "Test",
                        "children": []
                    }
                ],
                "version": "2.0"
            },
            "tags": []
        }

        result = BlockValidationService.validate_story_node(node_data)

        self.assertFalse(result.is_valid)

        # Check for unsupported block type error
        type_errors = [e for e in result.errors if e.code == "BLOCK_TYPE_UNSUPPORTED"]
        self.assertGreater(len(type_errors), 0)

    def test_validate_story_node_heading_invalid_level(self):
        """Test validating heading with invalid level."""
        node_data = {
            "name": "Test Node",
            "node_data": {
                "blocks": [
                    {
                        "id": "test-123",
                        "type": "heading",
                        "props": {"level": 5},  # Invalid level (only 1-3 supported)
                        "content": "Test Heading",
                        "children": []
                    }
                ],
                "version": "2.0"
            },
            "tags": []
        }

        result = BlockValidationService.validate_story_node(node_data)

        self.assertFalse(result.is_valid)

        # Check for invalid heading level error
        level_errors = [e for e in result.errors if e.code == "HEADING_LEVEL_INVALID"]
        self.assertGreater(len(level_errors), 0)

    def test_validate_story_node_warnings(self):
        """Test validation warnings for quality issues."""
        node_data = {
            "name": "AB",  # Short name (should generate warning)
            "node_data": {
                "blocks": [
                    {
                        "id": "test-123",
                        "type": "paragraph",
                        "props": {},
                        "content": "",  # Empty content (should generate warning)
                        "children": []
                    }
                ],
                "version": "2.0"
            },
            "tags": []
        }

        result = BlockValidationService.validate_story_node(node_data)

        self.assertTrue(result.is_valid)  # No errors, just warnings
        self.assertGreater(len(result.warnings), 0)

        # Check for name too short warning
        name_warnings = [w for w in result.warnings if w.code == "NAME_TOO_SHORT"]
        self.assertGreater(len(name_warnings), 0)
