"""
Test management command for Elora AI Assistant setup.

This command tests the Elora configuration and tool loading without requiring
an OpenAI API key, allowing us to verify the setup is correct.
"""

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Management command to test Elora setup without API calls."""

    help = 'Test Elora AI Assistant setup and configuration'

    def handle(self, *args, **options):
        """Handle the command execution."""

        self.stdout.write("🔧 Testing Elora AI Assistant Setup...")
        self.stdout.write("="*50)

        # Test 1: Configuration
        self.stdout.write("\\n1️⃣ Testing Configuration...")
        try:
            config = settings.ELORA_CONFIG
            self.stdout.write("  ✅ ELORA_CONFIG found")
            self.stdout.write(f"  • Model: {config.get('model', 'not set')}")
            self.stdout.write(f"  • Enabled: {config.get('enabled', False)}")
            self.stdout.write(f"  • API Key: {'✅ Set' if config.get('openai_api_key') else '❌ Not set'}")
        except AttributeError:
            self.stdout.write(self.style.ERROR("  ❌ ELORA_CONFIG not found in settings"))
            return

        # Test 2: Import all tools
        self.stdout.write("\\n2️⃣ Testing Tool Imports...")
        try:
            # Test existing tools
            from apps.ai_tools.tools.project_analysis import (
                analyze_project,
                assess_project_complexity,
                get_project_summary,
            )
            self.stdout.write("  ✅ Existing analysis tools imported")

            # Test new tools
            from apps.ai_tools.tools.entity_queries import (
                get_project_statistics,
                query_project_entities,
            )
            self.stdout.write("  ✅ Entity query tools imported")

            from apps.ai_tools.tools.structure_analysis import (
                analyze_project_structure,
                validate_project_health,
            )
            self.stdout.write("  ✅ Structure analysis tools imported")

            from apps.ai_tools.tools.story_details import (
                get_canvas_information,
                get_story_details,
            )
            self.stdout.write("  ✅ Story detail tools imported")

            from apps.ai_tools.tools.world_information import (
                get_character_details,
                get_world_information,
            )
            self.stdout.write("  ✅ World information tools imported")

            from apps.ai_tools.tools.content_search import (
                find_content_references,
                search_project_content,
            )
            self.stdout.write("  ✅ Content search tools imported")

        except ImportError as e:
            self.stdout.write(self.style.ERROR(f"  ❌ Import error: {e}"))
            return

        # Test 3: Service imports
        self.stdout.write("\\n3️⃣ Testing Service Imports...")
        try:
            from apps.ai_tools.services.conversation_service import ConversationService
            from apps.ai_tools.services.elora_service import EloraService
            self.stdout.write("  ✅ Service classes imported")
        except ImportError as e:
            self.stdout.write(self.style.ERROR(f"  ❌ Service import error: {e}"))
            return

        # Test 4: Test tool function calls (without API)
        self.stdout.write("\\n4️⃣ Testing Tool Functions...")
        try:
            # Test with a real project (if any exist)
            from apps.projects.models import Project

            projects = Project.objects.all()[:1]
            if projects:
                project = projects[0]
                project_id = str(project.id)
                self.stdout.write(f"  • Using test project: {project.name}")

                # Test entity queries
                result = query_project_entities(project_id, "story_canvases", "count_only")
                self.stdout.write(f"  ✅ Entity query test: {result[:50]}...")

                # Test project overview
                result = analyze_project(project_id, "basic")
                self.stdout.write(f"  ✅ Analysis test: {result[:50]}...")

            else:
                self.stdout.write("  ⚠️ No projects found - skipping function tests")

        except Exception as e:
            self.stdout.write(self.style.WARNING(f"  ⚠️ Tool function test error: {e}"))

        # Test 5: Database connectivity
        self.stdout.write("\\n5️⃣ Testing Database Connectivity...")
        try:
            from apps.npcs.models import NPC
            from apps.projects.models import Project
            from apps.stories.models import StoryCanvas, StoryNode
            from apps.world.models import Location

            project_count = Project.objects.count()
            canvas_count = StoryCanvas.objects.count()
            node_count = StoryNode.objects.count()
            npc_count = NPC.objects.count()
            location_count = Location.objects.count()

            self.stdout.write("  ✅ Database connectivity working")
            self.stdout.write(f"  • Projects: {project_count}")
            self.stdout.write(f"  • Story Canvases: {canvas_count}")
            self.stdout.write(f"  • Story Nodes: {node_count}")
            self.stdout.write(f"  • NPCs: {npc_count}")
            self.stdout.write(f"  • Locations: {location_count}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ❌ Database error: {e}"))
            return

        # Test 6: LangChain dependencies
        self.stdout.write("\\n6️⃣ Testing LangChain Dependencies...")
        try:
            import langchain
            import langchain_core
            import langchain_openai
            import openai

            self.stdout.write("  ✅ All LangChain dependencies available")
            self.stdout.write(f"  • LangChain: {langchain.__version__ if hasattr(langchain, '__version__') else 'installed'}")
            self.stdout.write(f"  • OpenAI: {openai.__version__ if hasattr(openai, '__version__') else 'installed'}")

        except ImportError as e:
            self.stdout.write(self.style.ERROR(f"  ❌ LangChain dependency error: {e}"))
            return

        # Summary
        self.stdout.write("\\n" + "="*50)
        if config.get('openai_api_key'):
            self.stdout.write(self.style.SUCCESS("🎉 Elora setup is complete and ready!"))
            self.stdout.write("\\nYou can now start chatting with Elora:")
            self.stdout.write("  python manage.py chat_with_elora")
        else:
            self.stdout.write(self.style.WARNING("⚠️ Elora setup is mostly complete!"))
            self.stdout.write("\\nTo finish setup, add your OpenAI API key:")
            self.stdout.write("  export OPENAI_API_KEY=your_api_key_here")
            self.stdout.write("\\nThen test with:")
            self.stdout.write("  python manage.py chat_with_elora --quick-test")

        self.stdout.write("="*50)
