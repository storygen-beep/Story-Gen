"""
Django management command for AI-powered project analysis.

Usage:
    python manage.py analyze_project <project_id> [--depth standard] [--format text]
    python manage.py analyze_project --list-projects
"""

import json
import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Case, Count, IntegerField, When

from apps.ai_tools.services.analysis_service import AnalysisService
from apps.projects.models import Project

User = get_user_model()
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Analyze story generation projects using AI tools'

    def add_arguments(self, parser):
        parser.add_argument(
            'project_id',
            nargs='?',
            type=str,
            help='UUID of the project to analyze'
        )

        parser.add_argument(
            '--depth',
            type=str,
            choices=['minimal', 'standard', 'comprehensive', 'expert'],
            default='standard',
            help='Analysis depth level (default: standard)'
        )

        parser.add_argument(
            '--format',
            type=str,
            choices=['text', 'json'],
            default='text',
            help='Output format (default: text)'
        )

        parser.add_argument(
            '--list-projects',
            action='store_true',
            help='List available projects for analysis'
        )

        parser.add_argument(
            '--user',
            type=str,
            help='Filter projects by username (use with --list-projects)'
        )

        parser.add_argument(
            '--complexity',
            action='store_true',
            help='Show only complexity analysis'
        )

        parser.add_argument(
            '--health',
            action='store_true',
            help='Show only health assessment'
        )

        parser.add_argument(
            '--potential',
            action='store_true',
            help='Show only AI generation potential'
        )

    def handle(self, *args, **options):
        try:
            if options['list_projects']:
                self._list_projects(options)
                return

            project_id = options['project_id']
            if not project_id:
                raise CommandError('Project ID is required. Use --list-projects to see available projects.')

            # Initialize analysis service
            analysis_service = AnalysisService()

            # Validate project exists
            try:
                project = Project.objects.get(id=project_id)
                self.stdout.write(
                    self.style.SUCCESS(f"🎯 Analyzing project: {project.name}")
                )
            except Project.DoesNotExist:
                raise CommandError(f'Project with ID {project_id} not found.')

            # Perform analysis based on options
            results = {}

            if options['complexity'] or not (options['health'] or options['potential']):
                self.stdout.write("🔍 Running complexity analysis...")
                results['complexity'] = analysis_service.analyze_project_complexity(project_id)

            if options['health'] or not (options['complexity'] or options['potential']):
                self.stdout.write("🏥 Running health assessment...")
                results['health'] = analysis_service.assess_project_health(project_id)

            if options['potential'] or not (options['complexity'] or options['health']):
                self.stdout.write("🚀 Assessing AI generation potential...")
                results['potential'] = analysis_service.get_project_generation_potential(project_id)

            # Output results
            self._output_results(results, options['format'], options['depth'])

            self.stdout.write(
                self.style.SUCCESS("\n✅ Analysis completed successfully!")
            )

        except Exception as e:
            logger.error(f"Analysis command failed: {e}")
            raise CommandError(f'Analysis failed: {e}')

    def _list_projects(self, options):
        """List available projects for analysis."""

        self.stdout.write(self.style.SUCCESS("📋 Available Projects for Analysis"))
        self.stdout.write("=" * 50)

        # Build query
        projects_query = Project.objects.filter(deleted_at__isnull=True).select_related('owner')

        if options['user']:
            try:
                user = User.objects.get(username=options['user'])
                projects_query = projects_query.filter(owner=user)
                self.stdout.write(f"Filtering by user: {options['user']}")
            except User.DoesNotExist:
                raise CommandError(f"User '{options['user']}' not found.")

        # Add content statistics
        projects = projects_query.annotate(
            canvas_count=Count('story_canvases'),
            character_count=Case(
                When(player_character__isnull=False, then=1),
                default=0,
                output_field=IntegerField()
            )
        ).order_by('-updated_at')[:20]  # Limit to 20 most recent

        if not projects.exists():
            self.stdout.write(
                self.style.WARNING("No projects found. Create some projects first.")
            )
            return

        self.stdout.write(f"Found {projects.count()} projects:\n")

        for i, project in enumerate(projects, 1):
            owner_name = project.owner.username if project.owner else 'No owner'

            # Basic project info
            self.stdout.write(
                f"{i:2d}. {project.name}"
            )
            self.stdout.write(
                f"     ID: {str(project.id)}"
            )
            self.stdout.write(
                f"     Owner: {owner_name} | Status: {project.status}"
            )
            self.stdout.write(
                f"     Content: {project.canvas_count} canvases, {project.character_count} characters"
            )
            self.stdout.write(
                f"     Updated: {project.updated_at.strftime('%Y-%m-%d %H:%M')}"
            )
            self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS("To analyze a project, use: python manage.py analyze_project <project_id>")
        )

    def _output_results(self, results, output_format, depth):
        """Output analysis results in the specified format."""

        if output_format == 'json':
            self.stdout.write(json.dumps(results, indent=2))
            return

        # Text format output
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("📊 PROJECT ANALYSIS RESULTS"))
        self.stdout.write("=" * 60)

        if 'complexity' in results:
            self._output_complexity_analysis(results['complexity'], depth)

        if 'health' in results:
            self._output_health_analysis(results['health'], depth)

        if 'potential' in results:
            self._output_potential_analysis(results['potential'], depth)

    def _output_complexity_analysis(self, complexity, depth):
        """Output complexity analysis in formatted text."""

        self.stdout.write("\n🧮 COMPLEXITY ANALYSIS")
        self.stdout.write("-" * 25)

        overall = complexity['overall_complexity']
        self.stdout.write(f"Overall Complexity: {overall['score']}/100 ({overall['level']})")
        self.stdout.write(f"Description: {overall['description']}")

        if depth in ['standard', 'comprehensive', 'expert']:
            self.stdout.write("\nDetailed Breakdown:")

            structural = complexity['structural_complexity']
            self.stdout.write(f"  🏗️  Structural: {structural['score']}/100 ({structural['level']})")

            content = complexity['content_complexity']
            self.stdout.write(f"  📝 Content: {content['score']}/100 ({content['level']})")

            relationship = complexity['relationship_complexity']
            self.stdout.write(f"  🔗 Relationships: {relationship['score']}/100 ({relationship['level']})")

        if depth in ['comprehensive', 'expert']:
            stats = complexity['project_stats']
            self.stdout.write("\nProject Statistics:")
            self.stdout.write(f"  • {stats['canvas_count']} canvases")
            self.stdout.write(f"  • {stats['node_count']} story nodes")
            self.stdout.write(f"  • {stats['connection_count']} connections")
            self.stdout.write(f"  • {stats['character_count']} characters")
            self.stdout.write(f"  • {stats['location_count']} locations")
            self.stdout.write(f"  • {stats['total_content_length']:,} characters of content")

    def _output_health_analysis(self, health, depth):
        """Output health analysis in formatted text."""

        self.stdout.write("\n🏥 HEALTH ASSESSMENT")
        self.stdout.write("-" * 22)

        overall = health['overall_health']
        self.stdout.write(f"Overall Health: {overall['score']}/100 ({overall['level']})")
        self.stdout.write(f"Description: {overall['description']}")

        if depth in ['standard', 'comprehensive', 'expert']:
            self.stdout.write("\nHealth Breakdown:")

            completeness = health['completeness']
            self.stdout.write(f"  ✅ Completeness: {completeness['score']}/100")

            consistency = health['consistency']
            self.stdout.write(f"  🔄 Consistency: {consistency['score']}/100")

            quality = health['quality']
            self.stdout.write(f"  ⭐ Quality: {quality['score']}/100")

        if health.get('recommendations') and depth in ['comprehensive', 'expert']:
            self.stdout.write("\nRecommendations:")
            for rec in health['recommendations']:
                self.stdout.write(f"  • {rec}")

    def _output_potential_analysis(self, potential, depth):
        """Output AI potential analysis in formatted text."""

        self.stdout.write("\n🚀 AI GENERATION POTENTIAL")
        self.stdout.write("-" * 30)

        overall = potential['generation_potential']
        self.stdout.write(f"AI Potential: {overall['score']}/100 ({overall['level']})")
        self.stdout.write(f"Description: {overall['description']}")

        if depth in ['standard', 'comprehensive', 'expert']:
            self.stdout.write("\nReadiness Assessment:")

            structure = potential['structure_readiness']
            self.stdout.write(f"  🏗️  Structure: {structure['score']}/100 ({structure['level']})")

            content = potential['content_readiness']
            self.stdout.write(f"  📝 Content: {content['score']}/100 ({content['level']})")

            expansion = potential['expansion_opportunities']
            self.stdout.write(f"  📈 Expansion: {expansion['score']}/100")

        if potential.get('ai_recommendations') and depth in ['comprehensive', 'expert']:
            self.stdout.write("\nAI Recommendations:")
            for rec in potential['ai_recommendations']:
                self.stdout.write(f"  • {rec}")

        if potential.get('expansion_opportunities', {}).get('opportunities') and depth in ['expert']:
            opportunities = potential['expansion_opportunities']['opportunities']
            self.stdout.write("\nExpansion Opportunities:")
            for opp in opportunities:
                self.stdout.write(f"  • {opp}")

        # Show example usage for high-potential projects
        if overall['score'] > 70:
            self.stdout.write("\n💡 This project is ready for AI enhancement!")
            self.stdout.write("   Consider using AI for content generation, dialogue expansion, or world building.")
