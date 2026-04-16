"""
Management command for starting conversations with Elora AI Assistant.

This command provides a terminal-based chat interface where users can interact
with Elora to explore and analyze their story projects using natural language.
"""

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.ai_tools.services.conversation_service import ConversationService


class Command(BaseCommand):
    """Management command to start chat with Elora AI Assistant."""

    help = 'Start a conversation with Elora, your AI story assistant'

    def add_arguments(self, parser):
        """Add command line arguments."""
        parser.add_argument(
            '--quick-test',
            action='store_true',
            help='Run a quick configuration test without starting full conversation',
        )

        parser.add_argument(
            '--show-config',
            action='store_true',
            help='Show current Elora configuration settings',
        )

        parser.add_argument(
            '--help-commands',
            action='store_true',
            help='Show available commands and examples',
        )

    def handle(self, *args, **options):
        """Handle the command execution."""

        if options['show_config']:
            self.show_configuration()
            return

        if options['help_commands']:
            self.show_command_help()
            return

        if options['quick_test']:
            self.run_quick_test()
            return

        # Start full conversation
        self.start_conversation()

    def start_conversation(self):
        """Start the main conversation with Elora."""
        self.stdout.write(
            self.style.SUCCESS('🚀 Starting Elora AI Assistant...')
        )

        # Initialize and start conversation service
        conversation = ConversationService()
        conversation.start_conversation()

    def run_quick_test(self):
        """Run a quick test to verify Elora configuration."""
        self.stdout.write("🔍 Running Elora configuration test...")

        try:
            from apps.ai_tools.services.elora_service import EloraService

            # Test configuration
            config = settings.ELORA_CONFIG

            self.stdout.write("\n📋 Configuration Check:")
            self.stdout.write(f"  • Enabled: {config.get('enabled', False)}")
            self.stdout.write(f"  • Model: {config.get('model', 'not set')}")
            self.stdout.write(f"  • API Key: {'✅ Set' if config.get('openai_api_key') else '❌ Not set'}")
            self.stdout.write(f"  • Max Tokens: {config.get('max_tokens', 'default')}")
            self.stdout.write(f"  • Temperature: {config.get('temperature', 'default')}")

            # Test service initialization
            elora = EloraService()

            if elora.is_configured():
                self.stdout.write(
                    self.style.SUCCESS("\n✅ Elora is properly configured and ready!")
                )

                # Test basic functionality
                self.stdout.write("\n🔧 Testing basic functionality...")
                projects_info = elora.get_available_projects()
                self.stdout.write("  • Projects query: ✅ Success")
                self.stdout.write(f"  • Available tools: {len(elora.tools)} tools loaded")

                # Test a simple chat interaction
                test_response = elora.chat("Hello, can you introduce yourself?")
                if test_response and len(test_response) > 10:
                    self.stdout.write("  • Chat functionality: ✅ Success")
                    self.stdout.write(f"\\n🤖 Sample response: {test_response[:100]}...")
                else:
                    self.stdout.write("  • Chat functionality: ⚠️ Limited response")

            else:
                self.stdout.write(
                    self.style.ERROR("\n❌ Elora configuration issues detected!")
                )
                self.stdout.write("\\nPlease check:")
                self.stdout.write("  1. OPENAI_API_KEY environment variable is set")
                self.stdout.write("  2. All required dependencies are installed")
                self.stdout.write("  3. Django settings ELORA_CONFIG is properly configured")

        except ImportError as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Import error: {e}")
            )
            self.stdout.write("\\nPlease ensure all AI dependencies are installed:")
            self.stdout.write("  pip install openai langchain langchain-openai")

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Configuration test failed: {e}")
            )

    def show_configuration(self):
        """Show current Elora configuration."""
        self.stdout.write("⚙️  Elora Configuration:")
        self.stdout.write("="*50)

        try:
            config = settings.ELORA_CONFIG

            self.stdout.write(f"Enabled: {config.get('enabled', 'Not set')}")
            self.stdout.write(f"Model: {config.get('model', 'Not set')}")
            self.stdout.write(f"Max Tokens: {config.get('max_tokens', 'Not set')}")
            self.stdout.write(f"Temperature: {config.get('temperature', 'Not set')}")
            self.stdout.write(f"Max History: {config.get('max_history', 'Not set')}")
            self.stdout.write(f"Session Timeout: {config.get('session_timeout', 'Not set')}s")

            # Show API key status without exposing the key
            api_key = config.get('openai_api_key', '')
            if api_key:
                masked_key = api_key[:8] + "*" * (len(api_key) - 12) + api_key[-4:] if len(api_key) > 12 else "****"
                self.stdout.write(f"OpenAI API Key: {masked_key}")
            else:
                self.stdout.write("OpenAI API Key: ❌ Not configured")

        except AttributeError:
            self.stdout.write(
                self.style.ERROR("❌ ELORA_CONFIG not found in Django settings")
            )

    def show_command_help(self):
        """Show detailed command help and examples."""
        help_text = """
🤖 Elora AI Assistant - Command Help
==================================

STARTING ELORA:
  python manage.py chat_with_elora

COMMAND OPTIONS:
  --quick-test      Test configuration without starting chat
  --show-config     Display current Elora settings
  --help-commands   Show this help message

ENVIRONMENT SETUP:
Before using Elora, ensure you have:

1. OpenAI API Key:
   export OPENAI_API_KEY=your_api_key_here

2. Optional Configuration:
   export ELORA_MODEL=gpt-4                 # or gpt-3.5-turbo
   export ELORA_MAX_TOKENS=2000             # response length
   export ELORA_TEMPERATURE=0.7             # creativity (0-1)
   export ELORA_MAX_HISTORY=50              # conversation memory
   export ELORA_SESSION_TIMEOUT=3600        # 1 hour

CONVERSATION COMMANDS:
Once in chat mode, you can:

• Ask natural language questions:
  "Tell me about my projects"
  "How many characters do I have?"
  "Find mentions of dragons in my story"

• Get project analysis:
  "What's the health score of my main project?"
  "Analyze the structure of my fantasy story"
  "Show me dead ends in my story"

• Explore world building:
  "What characters live in the tavern?"
  "List all locations in my world"
  "Show me character relationships"

• Search content:
  "Where did I mention the magic sword?"
  "Find all dialogue about betrayal"
  "Search for references to the ancient prophecy"

EXIT COMMANDS:
  Type: exit, quit, bye, goodbye
  Or press: Ctrl+C

TROUBLESHOOTING:
• Configuration issues: python manage.py chat_with_elora --quick-test
• View settings: python manage.py chat_with_elora --show-config
• Check logs: Look in logs/django.log for detailed errors

EXAMPLES:
  # Test setup
  python manage.py chat_with_elora --quick-test

  # Start chatting
  python manage.py chat_with_elora

  # In chat:
  You: "Show me my projects"
  Elora: "Here are your projects: ..."

  You: "Tell me about my fantasy project"
  Elora: "Your 'Epic Fantasy' project has 23 nodes..."

For more help, visit the ELORA_DESIGN.md documentation.
        """

        self.stdout.write(help_text)
