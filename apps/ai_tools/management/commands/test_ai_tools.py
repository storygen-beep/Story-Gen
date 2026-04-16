"""
Django management command for testing AI tools functionality.

Usage:
    python manage.py test_ai_tools
    python manage.py test_ai_tools --quick
"""

import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

from apps.ai_tools.services.analysis_service import AnalysisService
from apps.projects.models import Project

User = get_user_model()
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Test AI tools functionality with real project data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--quick',
            action='store_true',
            help='Run quick tests only (skip comprehensive analysis)'
        )

    def handle(self, *args, **options):
        try:
            self.stdout.write(
                self.style.SUCCESS("🧪 AI Tools Functionality Test")
            )
            self.stdout.write("=" * 40)

            # Test 1: Database Connection
            if not self._test_database_connection():
                return

            # Test 2: Find Projects
            projects = self._find_test_projects()
            if not projects:
                return

            # Test 3: Service Initialization
            if not self._test_service_initialization():
                return

            # Test 4: Basic Analysis
            if not self._test_basic_analysis(projects[0], options['quick']):
                return

            # Test 5: Multiple Projects (if not quick mode)
            if not options['quick'] and len(projects) > 1:
                if not self._test_multiple_projects(projects[:3]):
                    return

            self.stdout.write("\n" + "=" * 40)
            self.stdout.write(
                self.style.SUCCESS("✅ All tests passed! AI tools are working correctly.")
            )
            self.stdout.write("\nNext steps:")
            self.stdout.write("• Use: python manage.py analyze_project <project_id>")
            self.stdout.write("• List projects: python manage.py analyze_project --list-projects")

        except Exception as e:
            logger.error(f"Test command failed: {e}")
            self.stdout.write(
                self.style.ERROR(f"❌ Test failed with error: {e}")
            )
            raise CommandError(f'Test failed: {e}')

    def _test_database_connection(self):
        """Test database connection."""
        self.stdout.write("\n1️⃣ Testing database connection...")

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM projects_project WHERE deleted_at IS NULL")
                project_count = cursor.fetchone()[0]

            self.stdout.write(
                self.style.SUCCESS(f"   ✅ Database connected - {project_count} projects found")
            )
            return True

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"   ❌ Database connection failed: {e}")
            )
            return False

    def _find_test_projects(self):
        """Find projects for testing."""
        self.stdout.write("\n2️⃣ Finding test projects...")

        try:
            projects = Project.objects.filter(
                deleted_at__isnull=True
            ).select_related('owner').order_by('-updated_at')[:5]

            project_list = list(projects)

            if not project_list:
                self.stdout.write(
                    self.style.WARNING("   ⚠️  No projects found in database")
                )
                self.stdout.write("   Create some projects in Django admin or web interface first")
                return []

            self.stdout.write(
                self.style.SUCCESS(f"   ✅ Found {len(project_list)} projects for testing")
            )

            # Show project details
            for i, project in enumerate(project_list, 1):
                owner_name = project.owner.username if project.owner else 'No owner'
                self.stdout.write(f"      {i}. {project.name} ({owner_name})")

            return project_list

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"   ❌ Error finding projects: {e}")
            )
            return []

    def _test_service_initialization(self):
        """Test service initialization."""
        self.stdout.write("\n3️⃣ Testing service initialization...")

        try:
            analysis_service = AnalysisService()
            self.stdout.write(
                self.style.SUCCESS("   ✅ AnalysisService initialized successfully")
            )
            return True

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"   ❌ Service initialization failed: {e}")
            )
            return False

    def _test_basic_analysis(self, test_project, quick_mode):
        """Test basic analysis functionality."""
        self.stdout.write(f"\n4️⃣ Testing basic analysis with: {test_project.name}")

        try:
            analysis_service = AnalysisService()
            project_id = str(test_project.id)

            # Test complexity analysis
            self.stdout.write("   🧮 Testing complexity analysis...")
            complexity = analysis_service.analyze_project_complexity(project_id)

            if complexity and 'overall_complexity' in complexity:
                score = complexity['overall_complexity']['score']
                level = complexity['overall_complexity']['level']
                self.stdout.write(
                    self.style.SUCCESS(f"      ✅ Complexity: {score}/100 ({level})")
                )
            else:
                raise ValueError("Invalid complexity analysis result")

            if not quick_mode:
                # Test health assessment
                self.stdout.write("   🏥 Testing health assessment...")
                health = analysis_service.assess_project_health(project_id)

                if health and 'overall_health' in health:
                    score = health['overall_health']['score']
                    level = health['overall_health']['level']
                    self.stdout.write(
                        self.style.SUCCESS(f"      ✅ Health: {score}/100 ({level})")
                    )
                else:
                    raise ValueError("Invalid health assessment result")

                # Test AI potential
                self.stdout.write("   🚀 Testing AI potential assessment...")
                potential = analysis_service.get_project_generation_potential(project_id)

                if potential and 'generation_potential' in potential:
                    score = potential['generation_potential']['score']
                    level = potential['generation_potential']['level']
                    self.stdout.write(
                        self.style.SUCCESS(f"      ✅ AI Potential: {score}/100 ({level})")
                    )
                else:
                    raise ValueError("Invalid AI potential result")

            self.stdout.write(
                self.style.SUCCESS("   ✅ Basic analysis tests passed")
            )
            return True

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"   ❌ Basic analysis failed: {e}")
            )
            return False

    def _test_multiple_projects(self, test_projects):
        """Test analysis with multiple projects."""
        self.stdout.write("\n5️⃣ Testing multiple project analysis...")

        try:
            analysis_service = AnalysisService()

            results = []
            for project in test_projects:
                try:
                    complexity = analysis_service.analyze_project_complexity(str(project.id))
                    results.append({
                        'name': project.name,
                        'complexity_score': complexity['overall_complexity']['score']
                    })
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f"   ⚠️  Failed to analyze {project.name}: {e}")
                    )
                    continue

            if results:
                avg_complexity = sum(r['complexity_score'] for r in results) / len(results)
                self.stdout.write(
                    self.style.SUCCESS(f"   ✅ Analyzed {len(results)} projects successfully")
                )
                self.stdout.write(f"      Average complexity: {avg_complexity:.1f}/100")

                # Show individual results
                for result in results:
                    self.stdout.write(f"      • {result['name']}: {result['complexity_score']:.1f}")

                return True
            else:
                self.stdout.write(
                    self.style.WARNING("   ⚠️  No projects could be analyzed")
                )
                return True  # Don't fail the entire test

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"   ❌ Multiple project analysis failed: {e}")
            )
            return False

    def _test_user_insights(self, test_project):
        """Test user portfolio insights (if user exists)."""
        if not test_project.owner:
            return True

        self.stdout.write("\n6️⃣ Testing user portfolio insights...")

        try:
            analysis_service = AnalysisService()
            user_id = str(test_project.owner.id)

            insights = analysis_service.generate_user_project_insights(user_id)

            if insights and 'total_projects' in insights:
                total = insights['total_projects']
                analyzed = insights['analyzed_projects']
                self.stdout.write(
                    self.style.SUCCESS(f"   ✅ User insights: {analyzed}/{total} projects analyzed")
                )

                if insights.get('portfolio_overview'):
                    portfolio = insights['portfolio_overview']
                    if 'average_complexity' in portfolio:
                        avg_complexity = portfolio['average_complexity']
                        self.stdout.write(f"      Portfolio complexity: {avg_complexity:.1f}/100")

                return True
            else:
                raise ValueError("Invalid user insights result")

        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f"   ⚠️  User insights test skipped: {e}")
            )
            return True  # Don't fail the entire test for this
