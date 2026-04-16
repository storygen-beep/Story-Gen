"""
Tests for AI Tools Analysis Service

Tests the analysis service functionality using Django's testing framework.
"""

import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.ai_tools.services.analysis_service import AnalysisService
from apps.characters.models import Character
from apps.projects.models import Project
from apps.stories.models import StoryCanvas, StoryNode
from apps.world.models import Location

User = get_user_model()


class AnalysisServiceTestCase(TestCase):
    """Test cases for the AnalysisService."""

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
            title='Opening Scene',
            content='This is the opening scene of our test story. It sets the stage for adventure.',
            node_type='story_content'
        )

        self.node2 = StoryNode.objects.create(
            canvas=self.canvas,
            title='Decision Point',
            content='The hero must choose their path. This is a crucial moment in the story.',
            node_type='story_content'
        )

        # Create characters
        self.character1 = Character.objects.create(
            project=self.project,
            name='Test Hero',
            description='The main character'
        )

        self.character2 = Character.objects.create(
            project=self.project,
            name='Test Villain',
            description='The antagonist'
        )

        # Create location
        self.location = Location.objects.create(
            project=self.project,
            name='Test Kingdom',
            description='A fantastical kingdom'
        )

        # Initialize service
        self.analysis_service = AnalysisService()

    def test_service_initialization(self):
        """Test that the analysis service initializes correctly."""
        self.assertIsInstance(self.analysis_service, AnalysisService)

    def test_analyze_project_complexity(self):
        """Test project complexity analysis."""
        result = self.analysis_service.analyze_project_complexity(str(self.project.id))

        # Check basic structure
        self.assertIn('project_id', result)
        self.assertIn('project_name', result)
        self.assertIn('overall_complexity', result)
        self.assertIn('structural_complexity', result)
        self.assertIn('content_complexity', result)
        self.assertIn('relationship_complexity', result)
        self.assertIn('project_stats', result)

        # Check overall complexity
        overall = result['overall_complexity']
        self.assertIn('score', overall)
        self.assertIn('level', overall)
        self.assertIn('description', overall)
        self.assertIsInstance(overall['score'], (int, float))
        self.assertGreaterEqual(overall['score'], 0)
        self.assertLessEqual(overall['score'], 100)

        # Check project stats
        stats = result['project_stats']
        self.assertEqual(stats['canvas_count'], 1)
        self.assertEqual(stats['node_count'], 2)
        self.assertEqual(stats['character_count'], 2)
        self.assertEqual(stats['location_count'], 1)
        self.assertGreater(stats['total_content_length'], 0)

    def test_assess_project_health(self):
        """Test project health assessment."""
        result = self.analysis_service.assess_project_health(str(self.project.id))

        # Check basic structure
        self.assertIn('project_id', result)
        self.assertIn('project_name', result)
        self.assertIn('overall_health', result)
        self.assertIn('completeness', result)
        self.assertIn('consistency', result)
        self.assertIn('quality', result)

        # Check overall health
        overall = result['overall_health']
        self.assertIn('score', overall)
        self.assertIn('level', overall)
        self.assertIn('description', overall)
        self.assertIsInstance(overall['score'], (int, float))
        self.assertGreaterEqual(overall['score'], 0)
        self.assertLessEqual(overall['score'], 100)

    def test_get_project_generation_potential(self):
        """Test AI generation potential assessment."""
        result = self.analysis_service.get_project_generation_potential(str(self.project.id))

        # Check basic structure
        self.assertIn('project_id', result)
        self.assertIn('project_name', result)
        self.assertIn('generation_potential', result)
        self.assertIn('structure_readiness', result)
        self.assertIn('content_readiness', result)
        self.assertIn('expansion_opportunities', result)

        # Check generation potential
        potential = result['generation_potential']
        self.assertIn('score', potential)
        self.assertIn('level', potential)
        self.assertIn('description', potential)
        self.assertIsInstance(potential['score'], (int, float))
        self.assertGreaterEqual(potential['score'], 0)
        self.assertLessEqual(potential['score'], 100)

    def test_generate_user_project_insights(self):
        """Test user project insights generation."""
        result = self.analysis_service.generate_user_project_insights(str(self.user.id))

        # Check basic structure
        self.assertIn('user_id', result)
        self.assertIn('username', result)
        self.assertIn('total_projects', result)
        self.assertIn('analyzed_projects', result)

        # Check values
        self.assertEqual(result['username'], self.user.username)
        self.assertEqual(result['total_projects'], 1)
        self.assertEqual(result['analyzed_projects'], 1)

    def test_invalid_project_id(self):
        """Test handling of invalid project ID."""
        fake_id = str(uuid.uuid4())

        with self.assertRaises(ValueError):
            self.analysis_service.analyze_project_complexity(fake_id)

    def test_invalid_user_id(self):
        """Test handling of invalid user ID."""
        fake_id = str(uuid.uuid4())

        with self.assertRaises(ValueError):
            self.analysis_service.generate_user_project_insights(fake_id)

    def test_empty_project_analysis(self):
        """Test analysis of empty project."""
        # Create empty project
        empty_project = Project.objects.create(
            name='Empty Project',
            description='A project with no content',
            owner=self.user,
            status='draft'
        )

        result = self.analysis_service.analyze_project_complexity(str(empty_project.id))

        # Should still return valid structure with low scores
        self.assertIn('overall_complexity', result)
        stats = result['project_stats']
        self.assertEqual(stats['canvas_count'], 0)
        self.assertEqual(stats['node_count'], 0)
        self.assertEqual(stats['character_count'], 0)
        self.assertEqual(stats['location_count'], 0)

    def test_complexity_scoring_ranges(self):
        """Test that complexity scores are within expected ranges."""
        result = self.analysis_service.analyze_project_complexity(str(self.project.id))

        # Test overall complexity
        overall_score = result['overall_complexity']['score']
        self.assertGreaterEqual(overall_score, 0)
        self.assertLessEqual(overall_score, 100)

        # Test component complexities
        structural_score = result['structural_complexity']['score']
        content_score = result['content_complexity']['score']
        relationship_score = result['relationship_complexity']['score']

        self.assertGreaterEqual(structural_score, 0)
        self.assertLessEqual(structural_score, 100)
        self.assertGreaterEqual(content_score, 0)
        self.assertLessEqual(content_score, 100)
        self.assertGreaterEqual(relationship_score, 0)
        self.assertLessEqual(relationship_score, 100)

    def test_health_scoring_ranges(self):
        """Test that health scores are within expected ranges."""
        result = self.analysis_service.assess_project_health(str(self.project.id))

        # Test overall health
        overall_score = result['overall_health']['score']
        self.assertGreaterEqual(overall_score, 0)
        self.assertLessEqual(overall_score, 100)

        # Test component health scores
        completeness_score = result['completeness']['score']
        consistency_score = result['consistency']['score']
        quality_score = result['quality']['score']

        self.assertGreaterEqual(completeness_score, 0)
        self.assertLessEqual(completeness_score, 100)
        self.assertGreaterEqual(consistency_score, 0)
        self.assertLessEqual(consistency_score, 100)
        self.assertGreaterEqual(quality_score, 0)
        self.assertLessEqual(quality_score, 100)


class AnalysisServiceIntegrationTestCase(TestCase):
    """Integration tests for AnalysisService with realistic data."""

    def setUp(self):
        """Set up realistic test data."""
        self.user = User.objects.create_user(
            username='storywriter',
            email='writer@example.com',
            password='testpass123'
        )

        # Create complex project
        self.complex_project = Project.objects.create(
            name='Epic Fantasy Adventure',
            description='A complex multi-chapter fantasy story',
            owner=self.user,
            status='active'
        )

        # Create multiple canvases
        self.canvas1 = StoryCanvas.objects.create(
            project=self.complex_project,
            name='Chapter 1: The Beginning'
        )

        self.canvas2 = StoryCanvas.objects.create(
            project=self.complex_project,
            name='Chapter 2: The Journey'
        )

        # Create multiple nodes with substantial content
        for i in range(5):
            StoryNode.objects.create(
                canvas=self.canvas1,
                title=f'Scene {i+1}',
                content=f'This is scene {i+1} with detailed content about the story progression. ' * 20,
                node_type='story_content'
            )

        for i in range(3):
            StoryNode.objects.create(
                canvas=self.canvas2,
                title=f'Chapter 2 Scene {i+1}',
                content=f'Chapter 2 scene {i+1} continues the story with rich narrative content. ' * 15,
                node_type='story_content'
            )

        # Create multiple characters
        characters_data = [
            ('Aria the Brave', 'The heroic protagonist with a mysterious past'),
            ('Malgor the Dark', 'Ancient evil wizard seeking world domination'),
            ('Finn Swiftarrow', 'Elven ranger and loyal companion'),
            ('Lady Blackwood', 'Noble patron with hidden motives'),
            ('Grunk the Mighty', 'Dwarf warrior with a heart of gold')
        ]

        for name, desc in characters_data:
            Character.objects.create(
                project=self.complex_project,
                name=name,
                description=desc
            )

        # Create multiple locations
        locations_data = [
            ('Elderwood Forest', 'Ancient forest filled with magical creatures'),
            ('Shadowmere Castle', 'Dark fortress of the evil wizard'),
            ('Brightwater Village', 'Peaceful village where the journey begins'),
            ('Dragon\'s Peak', 'Treacherous mountain where dragons nest')
        ]

        for name, desc in locations_data:
            Location.objects.create(
                project=self.complex_project,
                name=name,
                description=desc
            )

        self.analysis_service = AnalysisService()

    def test_complex_project_analysis(self):
        """Test analysis of a complex project with rich content."""
        result = self.analysis_service.analyze_project_complexity(str(self.complex_project.id))

        # Complex project should have higher scores
        overall_score = result['overall_complexity']['score']
        self.assertGreater(overall_score, 20)  # Should be above minimal threshold

        # Check stats reflect the complex content
        stats = result['project_stats']
        self.assertEqual(stats['canvas_count'], 2)
        self.assertEqual(stats['node_count'], 8)
        self.assertEqual(stats['character_count'], 5)
        self.assertEqual(stats['location_count'], 4)
        self.assertGreater(stats['total_content_length'], 1000)  # Substantial content

        # Component diversity should be high
        self.assertEqual(stats['component_diversity'], 4)  # All component types present
        self.assertIn('canvases', stats['component_types'])
        self.assertIn('nodes', stats['component_types'])
        self.assertIn('characters', stats['component_types'])
        self.assertIn('locations', stats['component_types'])

    def test_multiple_projects_portfolio(self):
        """Test user insights with multiple projects."""
        # Create second project
        simple_project = Project.objects.create(
            name='Simple Story',
            description='A basic story',
            owner=self.user,
            status='draft'
        )

        # Add minimal content to second project
        canvas = StoryCanvas.objects.create(
            project=simple_project,
            name='Simple Canvas'
        )

        StoryNode.objects.create(
            canvas=canvas,
            title='Simple Scene',
            content='A simple scene with basic content.',
            node_type='story_content'
        )

        # Test user insights
        insights = self.analysis_service.generate_user_project_insights(str(self.user.id))

        self.assertEqual(insights['total_projects'], 2)
        self.assertEqual(insights['analyzed_projects'], 2)

        # Should have portfolio overview
        self.assertIn('portfolio_overview', insights)
        portfolio = insights['portfolio_overview']

        # Should have reasonable averages
        self.assertIn('average_complexity', portfolio)
        self.assertIn('average_health', portfolio)
        self.assertGreater(portfolio['average_complexity'], 0)
        self.assertGreater(portfolio['average_health'], 0)
