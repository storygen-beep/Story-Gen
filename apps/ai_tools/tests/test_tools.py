"""
Tests for AI Tools LangChain Tools

Tests the LangChain tool implementations.
"""

import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.ai_tools.tools.project_analysis import (
    analyze_multiple_projects,
    analyze_project,
    assess_project_complexity,
    get_project_summary,
)
from apps.characters.models import Character
from apps.projects.models import Project
from apps.stories.models import StoryCanvas, StoryNode

User = get_user_model()


class ProjectAnalysisToolsTestCase(TestCase):
    """Test cases for LangChain project analysis tools."""

    def setUp(self):
        """Set up test data."""
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Create a test project
        self.project = Project.objects.create(
            name='Test Story Project',
            description='A test project for AI analysis',
            owner=self.user,
            status='active'
        )

        # Create story content
        self.canvas = StoryCanvas.objects.create(
            project=self.project,
            name='Main Story'
        )

        self.node1 = StoryNode.objects.create(
            canvas=self.canvas,
            name='Opening Scene',
            node_data={'content': 'This is the opening scene of our test story. It sets the stage for adventure and introduces the main character who will face many challenges.',
                       'node_type': 'story_content'},
        )

        self.node2 = StoryNode.objects.create(
            canvas=self.canvas,
            name='Decision Point',
            node_data={'content': 'The hero must choose their path. This is a crucial moment in the story that will determine the outcome of their journey.',
                       'node_type': 'story_content'},
        )

        # Create characters
        self.character1 = Character.objects.create(
            project=self.project,
            name='Test Hero',
            description='The main character'
        )

        # Only ONE Character per project: Character.project is a OneToOneField
        # (related_name="player_character"), so a project has a single player character.
        # NPC.project is the ForeignKey — that is where a cast of many belongs.

        self.project_id = str(self.project.id)

    def test_analyze_project_tool_minimal(self):
        """Test analyze_project tool with minimal depth."""
        result = analyze_project.invoke({"project_id": self.project_id, "analysis_depth": "minimal"})

        # Should be a string with analysis content
        self.assertIsInstance(result, str)
        self.assertIn(self.project.name, result)
        self.assertIn('Complexity:', result)
        self.assertIn('Health:', result)
        self.assertIn('AI Potential:', result)
        self.assertNotIn('❌ Failed', result)

    def test_analyze_project_tool_standard(self):
        """Test analyze_project tool with standard depth."""
        result = analyze_project.invoke({"project_id": self.project_id, "analysis_depth": "standard"})

        # Should be a string with detailed analysis
        self.assertIsInstance(result, str)
        self.assertIn(self.project.name, result)
        self.assertIn('Standard Analysis', result)
        self.assertIn('Complexity Analysis:', result)
        self.assertIn('Health Assessment:', result)
        self.assertIn('AI Generation Potential:', result)
        self.assertIn('Key Statistics:', result)
        self.assertNotIn('❌ Failed', result)

    def test_analyze_project_tool_comprehensive(self):
        """Test analyze_project tool with comprehensive depth."""
        result = analyze_project.invoke({"project_id": self.project_id, "analysis_depth": "comprehensive"})

        # Should be a string with comprehensive analysis
        self.assertIsInstance(result, str)
        self.assertIn(self.project.name, result)
        self.assertIn('Detailed Component Analysis', result)
        self.assertNotIn('❌ Failed', result)

    def test_analyze_project_tool_expert(self):
        """Test analyze_project tool with expert depth."""
        result = analyze_project.invoke({"project_id": self.project_id, "analysis_depth": "expert"})

        # Should be a string with expert-level analysis
        self.assertIsInstance(result, str)
        self.assertIn(self.project.name, result)
        self.assertIn('Expert Analysis', result)
        self.assertIn('Technical Metrics', result)
        self.assertNotIn('❌ Failed', result)

    def test_get_project_summary_tool(self):
        """Test get_project_summary tool."""
        result = get_project_summary.invoke({"project_id": self.project_id})

        # Should be a string with project summary
        self.assertIsInstance(result, str)
        self.assertIn(self.project.name, result)
        self.assertIn('Project Summary:', result)
        self.assertIn('Content Statistics:', result)
        self.assertIn('story canvases', result)
        self.assertIn('story nodes', result)
        self.assertIn('characters', result)
        self.assertNotIn('❌ Failed', result)

    def test_assess_project_complexity_tool(self):
        """Test assess_project_complexity tool."""
        result = assess_project_complexity.invoke({"project_id": self.project_id})

        # Should be a string with complexity assessment
        self.assertIsInstance(result, str)
        self.assertIn(self.project.name, result)
        self.assertIn('Complexity Assessment:', result)
        self.assertIn('Overall Complexity:', result)
        self.assertIn('Structural Complexity:', result)
        self.assertIn('Content Complexity:', result)
        self.assertIn('Relationship Complexity:', result)
        self.assertIn('Project Statistics:', result)
        self.assertNotIn('❌ Failed', result)

    def test_analyze_multiple_projects_tool(self):
        """Test analyze_multiple_projects tool."""
        # Create second project for comparison
        project2 = Project.objects.create(
            name='Second Test Project',
            description='Another test project',
            owner=self.user,
            status='draft'
        )

        # Add minimal content to second project
        canvas2 = StoryCanvas.objects.create(
            project=project2,
            name='Second Canvas'
        )

        StoryNode.objects.create(
            canvas=canvas2,
            name='Simple Scene',
            node_data={'content': 'A simple scene.',
                       'node_type': 'story_content'},
        )

        project_ids = [self.project_id, str(project2.id)]
        result = analyze_multiple_projects.invoke({"project_ids": project_ids, "comparison_focus": "overview"})

        # Should be a string with comparison analysis
        self.assertIsInstance(result, str)
        self.assertIn('Project Portfolio Overview', result)  # heading for focus='overview'
        self.assertIn('Project Rankings', result)
        self.assertIn(self.project.name, result)
        self.assertIn(project2.name, result)
        self.assertIn('Portfolio Averages:', result)
        self.assertNotIn('❌ Failed', result)

    def test_analyze_multiple_projects_complexity_focus(self):
        """Test analyze_multiple_projects with complexity focus."""
        # Create another project
        project2 = Project.objects.create(
            name='Complex Project',
            description='A more complex project',
            owner=self.user,
            status='active'
        )

        project_ids = [self.project_id, str(project2.id)]
        result = analyze_multiple_projects.invoke({"project_ids": project_ids, "comparison_focus": "complexity"})

        self.assertIsInstance(result, str)
        self.assertIn('Complexity Comparison', result)
        self.assertIn(self.project.name, result)
        self.assertIn(project2.name, result)
        self.assertNotIn('❌ Failed', result)

    def test_tools_with_invalid_project_id(self):
        """Test tools with invalid project ID."""
        fake_id = str(uuid.uuid4())

        # All tools should handle invalid IDs gracefully
        result1 = analyze_project.invoke({"project_id": fake_id})
        self.assertIn('❌ Failed', result1)

        result2 = get_project_summary.invoke({"project_id": fake_id})
        self.assertIn('❌ Failed', result2)

        result3 = assess_project_complexity.invoke({"project_id": fake_id})
        self.assertIn('❌ Failed', result3)

    def test_analyze_multiple_projects_too_many(self):
        """Test analyze_multiple_projects with too many projects."""
        # Create list of 11 project IDs (more than max of 10)
        project_ids = [str(uuid.uuid4()) for _ in range(11)]

        result = analyze_multiple_projects.invoke({"project_ids": project_ids})

        self.assertIn('Too many projects', result)
        self.assertIn('❌', result)

    def test_analyze_multiple_projects_empty_list(self):
        """Test analyze_multiple_projects with empty list."""
        result = analyze_multiple_projects.invoke({"project_ids": []})

        self.assertIn('No projects could be analyzed', result)
        self.assertIn('❌', result)

    def test_tool_output_format_consistency(self):
        """Test that all tools return properly formatted strings."""
        # StructuredTools take a dict via .invoke() and expose .name, not .__name__.
        tools_and_payloads = [
            (analyze_project, {"project_id": self.project_id}),
            (get_project_summary, {"project_id": self.project_id}),
            (assess_project_complexity, {"project_id": self.project_id}),
            (analyze_multiple_projects, {"project_ids": [self.project_id]}),
        ]

        for tool_func, payload in tools_and_payloads:
            with self.subTest(tool=tool_func.name):
                result = tool_func.invoke(payload)

                # Should be a string
                self.assertIsInstance(result, str)

                # Should not be empty
                self.assertGreater(len(result), 0)

                # Should contain the project name
                self.assertIn(self.project.name, result)

    def test_tool_error_handling(self):
        """Test that tools handle various error conditions gracefully."""
        # Test with malformed UUID
        result1 = analyze_project.invoke({"project_id": "not-a-uuid"})
        self.assertIn('❌', result1)

        # Test with None (should be handled by tool validation)
        try:
            result2 = get_project_summary.invoke({"project_id": None})
            # If it doesn't raise an exception, it should return an error message
            self.assertIn('❌', result2)
        except (TypeError, ValueError):
            # This is also acceptable behavior
            pass


class ToolIntegrationTestCase(TestCase):
    """Integration tests for tools with realistic project data."""

    def setUp(self):
        """Set up realistic test data."""
        self.user = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='testpass123'
        )

        # Create rich project
        self.rich_project = Project.objects.create(
            name='Epic Adventure Novel',
            description='A rich fantasy adventure with multiple characters and locations',
            owner=self.user,
            status='active'
        )

        # Create multiple canvases
        canvas1 = StoryCanvas.objects.create(
            project=self.rich_project,
            name='Act 1: The Call to Adventure'
        )

        canvas2 = StoryCanvas.objects.create(
            project=self.rich_project,
            name='Act 2: The Journey'
        )

        # Create nodes with substantial content
        substantial_content = "This is a substantial piece of story content that demonstrates the depth and quality of the narrative. " * 5

        for i in range(3):
            StoryNode.objects.create(
                canvas=canvas1,
                name=f'Act 1 Scene {i+1}',
                node_data={'content': f"{substantial_content} Scene {i+1} specific details.",
                           'node_type': 'story_content'},
            )

        for i in range(3):
            StoryNode.objects.create(
                canvas=canvas2,
                name=f'Act 2 Scene {i+1}',
                node_data={'content': f"{substantial_content} Act 2 scene {i+1} developments.",
                           'node_type': 'story_content'},
            )

        # Create characters
        Character.objects.create(
            project=self.rich_project,
            name='Aria Stormwind',
            description='A brave warrior princess with a mysterious heritage'
        )

        # Thorek and Lady Shadowmere removed: Character.project is OneToOne.

        self.rich_project_id = str(self.rich_project.id)

    def test_rich_project_analysis(self):
        """Test analysis of a project with rich content."""
        result = analyze_project.invoke({"project_id": self.rich_project_id, "analysis_depth": "comprehensive"})

        # Should reflect the rich content
        self.assertIn(self.rich_project.name, result)
        self.assertIn('Detailed Component Analysis', result)

        # Should show higher complexity due to rich content
        # (We can't test exact values, but we can test structure)
        # analyze_project labels these Structural:/Content:/Relationships:;
        # '<X> Complexity:' is assess_project_complexity's wording.
        self.assertIn('Structural:', result)
        self.assertIn('Content:', result)
        self.assertIn('Relationships:', result)

    def test_summary_with_rich_content(self):
        """Test project summary with rich content."""
        result = get_project_summary.invoke({"project_id": self.rich_project_id})

        # Should reflect the rich statistics
        self.assertIn('2 story canvases', result)
        self.assertIn('6 story nodes', result)
        self.assertIn('1 characters', result)  # OneToOne: one player character

        # Should indicate this is a well-developed project
        # (Content length should be substantial)
        self.assertRegex(result, r'\d{1,3},?\d{3}.*characters of content')

    def test_complexity_assessment_rich_project(self):
        """Test complexity assessment with rich project."""
        result = assess_project_complexity.invoke({"project_id": self.rich_project_id})

        # Should show detailed breakdown
        self.assertIn('Canvas organization:', result)
        self.assertIn('Node complexity:', result)
        self.assertIn('Character development:', result)
        self.assertIn('World building:', result)

        # Should show substantial project statistics
        self.assertIn('Canvases: 2', result)
        self.assertIn('Story nodes: 6', result)
        self.assertIn('Characters: 1', result)  # OneToOne: one player character
