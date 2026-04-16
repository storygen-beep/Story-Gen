"""
Conversation Service

Handles terminal-based conversation interface and session management for Elora.
"""

import time
from typing import Any, Optional

from apps.ai_tools.services.elora_service import EloraService


class ConversationService:
    """Service for managing terminal-based conversations with Elora."""

    def __init__(self, user_id: str = None):
        self.elora = None
        self.session_start_time = time.time()
        self.message_count = 0
        self.is_active = False
        # Generate a session-specific user ID for terminal usage
        self.user_id = user_id or f"terminal_{int(time.time())}"

    def initialize_elora(self) -> bool:
        """Initialize Elora service and verify configuration."""
        try:
            self.elora = EloraService()
            if not self.elora.is_configured():
                self.print_error("Elora is not properly configured. Please check your settings.")
                self._print_configuration_help()
                return False
            return True
        except Exception as e:
            self.print_error(f"Failed to initialize Elora: {str(e)}")
            self._print_configuration_help()
            return False

    def _print_configuration_help(self):
        """Print configuration help information."""
        print("\\n🔧 Configuration Help:")
        print("   • Make sure OPENAI_API_KEY is set in your environment")
        print("   • Check that your Django settings include ELORA_CONFIG")
        print("   • Verify your OpenAI API key is valid and has credits")
        print("   • Try running: export OPENAI_API_KEY='your-key-here'")

    def start_conversation(self):
        """Start the main conversation loop."""
        if not self.initialize_elora():
            return

        self.is_active = True
        self.print_welcome()

        # Show available projects with better error handling
        try:
            projects_info = self.elora.get_available_projects()
            self.print_elora_response(projects_info)
        except Exception as e:
            self.print_error(f"Could not load projects: {str(e)}")
            self.print_info("You can still ask questions, but I may need project names to help you.")

        try:
            while self.is_active:
                user_input = self.get_user_input()

                if not user_input:
                    continue

                if self.should_exit(user_input):
                    self.handle_exit()
                    break

                self.process_message(user_input)

        except KeyboardInterrupt:
            self.handle_keyboard_interrupt()
        except EOFError:
            self.handle_eof()
        except Exception as e:
            self.print_error(f"Unexpected error: {str(e)}")
        finally:
            self.cleanup()

    def print_welcome(self):
        """Print welcome message and instructions."""
        print("\\n" + "="*60)
        print("🤖 Welcome to Elora - Your Story Assistant!")
        print("="*60)
        print("\\nI can help you explore and analyze your story projects.")
        print("\\nCommands:")
        print("  • Type your questions naturally")
        print("  • 'help' or '?' for detailed examples")
        print("  • 'exit', 'quit', or 'bye' to end conversation")
        print("  • Ctrl+C to force exit")
        print("\\n" + "-"*60)

    def get_user_input(self) -> Optional[str]:
        """Get input from user with proper prompt."""
        try:
            user_input = input("\\n👤 You: ").strip()
            return user_input
        except (EOFError, KeyboardInterrupt):
            raise
        except Exception:
            return None

    def should_exit(self, user_input: str) -> bool:
        """Check if user wants to exit the conversation."""
        exit_commands = ['exit', 'quit', 'bye', 'goodbye', 'stop', 'end', 'done']
        return user_input.lower().strip() in exit_commands

    def process_message(self, message: str):
        """Process user message and display Elora's response."""
        self.message_count += 1

        # Handle help command
        if message.lower() in ['help', 'commands', 'what can you do', '?']:
            self.show_help()
            return

        # Show thinking indicator
        print("\\n🤖 Elora: ", end="", flush=True)
        print("Thinking...", end="", flush=True)

        try:
            # Get response from Elora with user context
            response = self.elora.chat(message, user_id=self.user_id)

            # Clear thinking indicator and show response
            print("\\r🤖 Elora: ", end="")
            self.print_elora_response(response)

            # Suggest follow-ups for common issues
            self._suggest_follow_ups(message, response)

        except Exception as e:
            print("\\r🤖 Elora: ", end="")
            error_msg = str(e)

            # Enhanced error handling with specific suggestions
            if "validation error" in error_msg.lower():
                self.print_error("I had trouble understanding your request.")
                self.print_info("Try asking: 'show me my projects' or 'help' for examples.")
            elif "not found" in error_msg.lower() or "does not exist" in error_msg.lower():
                self.print_error("I couldn't find what you're looking for.")
                self.print_info("Try asking: 'list my projects' to see what's available.")
            elif "openai" in error_msg.lower() or "api key" in error_msg.lower():
                self.print_error("There's an issue with the OpenAI API connection.")
                self.print_info("Please check your API key configuration.")
            else:
                self.print_error(f"I encountered an error: {error_msg}")
                self.print_info("Please try rephrasing your question or type 'help' for guidance.")

    def print_elora_response(self, response: str):
        """Print Elora's response with proper formatting."""
        # Split long responses into paragraphs for better readability
        lines = response.split('\\n')
        formatted_lines = []

        for line in lines:
            if line.strip():
                # Wrap long lines
                if len(line) > 80:
                    words = line.split()
                    current_line = ""
                    for word in words:
                        if len(current_line + word) > 80:
                            formatted_lines.append(current_line.strip())
                            current_line = word + " "
                        else:
                            current_line += word + " "
                    if current_line:
                        formatted_lines.append(current_line.strip())
                else:
                    formatted_lines.append(line)
            else:
                formatted_lines.append("")

        print("\\n".join(formatted_lines))

    def _suggest_follow_ups(self, user_message: str, response: str):
        """Suggest relevant follow-up questions based on the conversation."""
        # Don't suggest follow-ups for short responses or errors
        if len(response) < 50 or "error" in response.lower():
            return

        message_lower = user_message.lower()
        suggestions = []

        # Suggest follow-ups based on what the user asked
        if "projects" in message_lower and "list" in message_lower:
            suggestions = [
                "Tell me about [project name]",
                "What's my most complex project?",
                "Show project statistics"
            ]
        elif "characters" in message_lower:
            suggestions = [
                "Show character relationships",
                "Where do my characters live?",
                "Tell me about NPCs in [location]"
            ]
        elif "story" in message_lower or "canvas" in message_lower:
            suggestions = [
                "Analyze story structure",
                "Show story connections",
                "Find story issues"
            ]
        elif "project" in message_lower and any(word in message_lower for word in ["tell", "about", "analyze"]):
            suggestions = [
                "Show detailed statistics",
                "Analyze project health",
                "What characters are in this project?"
            ]

        if suggestions:
            print("\\n💡 You might also ask:")
            for suggestion in suggestions[:3]:  # Limit to 3 suggestions
                print(f"   • {suggestion}")

    def handle_exit(self):
        """Handle graceful exit."""
        goodbye_messages = [
            "Goodbye! Happy storytelling! 📚✨",
            "See you later! Keep creating amazing stories! 🎮",
            "Until next time! Your stories await! 📖",
            "Farewell, storyteller! ✨",
        ]

        # Choose message based on session length
        session_duration = time.time() - self.session_start_time
        if session_duration < 60:  # Less than 1 minute
            message = goodbye_messages[0]
        elif self.message_count > 10:  # Long conversation
            message = goodbye_messages[1]
        else:
            message = goodbye_messages[2]

        print(f"\\n🤖 Elora: {message}")
        self.print_session_summary()

    def handle_keyboard_interrupt(self):
        """Handle Ctrl+C gracefully."""
        print("\\n\\n🤖 Elora: Goodbye! (Interrupted)")
        self.print_session_summary()

    def handle_eof(self):
        """Handle EOF (Ctrl+D) gracefully."""
        print("\\n🤖 Elora: Goodbye!")
        self.print_session_summary()

    def print_session_summary(self):
        """Print session summary."""
        duration = int(time.time() - self.session_start_time)
        minutes = duration // 60
        seconds = duration % 60

        print("\\n" + "-"*40)
        print("📊 Session Summary:")
        print(f"   Messages: {self.message_count}")
        print(f"   Duration: {minutes}m {seconds}s" if minutes > 0 else f"   Duration: {seconds}s")
        print("-"*40)

    def cleanup(self):
        """Clean up resources."""
        self.is_active = False
        if self.elora:
            try:
                # Clear user's conversation memory to free up resources
                self.elora.clear_conversation(self.user_id)
            except Exception:
                # Don't fail cleanup if memory clearing fails
                pass

    def print_error(self, message: str):
        """Print error message with appropriate formatting."""
        print(f"❌ Error: {message}")

    def print_info(self, message: str):
        """Print info message with appropriate formatting."""
        print(f"ℹ️  {message}")

    def print_success(self, message: str):
        """Print success message with appropriate formatting."""
        print(f"✅ {message}")

    # Additional utility methods for enhanced conversation features

    def show_help(self):
        """Show help information."""
        help_text = """
🤖 Elora Help - What I Can Do:

📊 Project Analysis:
   • "Tell me about my [project name]"
   • "What's the health score of project X?"
   • "Show me my most complex project"

🔍 Entity Queries:
   • "How many characters do I have?"
   • "List all locations in [project]"
   • "Show me NPCs in the tavern"

🏗️  Structure Analysis:
   • "Is my story well-connected?"
   • "Find dead ends in my story"
   • "Analyze story complexity"

📖 Story Details:
   • "Tell me about the main story canvas"
   • "Show details for canvas [name]"
   • "What nodes are in my intro?"

🌍 World Information:
   • "What characters live in [location]?"
   • "Show me character relationships"
   • "List all world locations"

🔎 Content Search:
   • "Find mentions of dragons"
   • "Where did I write about magic?"
   • "Search for dialogue about betrayal"

💬 Conversation:
   • Ask follow-up questions naturally
   • I remember our conversation context
   • Type 'exit', 'quit', or 'bye' to end

Examples:
   • "Show me my projects"
   • "Tell me about my fantasy project"
   • "How many locations do I have in project X?"
   • "Find all mentions of the magic sword"
        """
        print(help_text)

    def get_conversation_stats(self) -> dict[str, Any]:
        """Get current conversation statistics."""
        return {
            'message_count': self.message_count,
            'session_duration': time.time() - self.session_start_time,
            'is_active': self.is_active,
            'elora_configured': self.elora is not None and self.elora.is_configured(),
        }
