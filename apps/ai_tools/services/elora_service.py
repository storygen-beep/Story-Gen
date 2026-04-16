"""
Elora AI Assistant Service

Handles the LangChain agent configuration and conversation management for the Elora
interactive AI assistant with proper architecture and security.
"""

import logging
from typing import Any

from django.conf import settings
from langchain.schema import AIMessage, HumanMessage
from pydantic import ValidationError

from apps.ai_tools.builders.agent_builder import build_elora_agent, validate_agent_tools
from apps.ai_tools.constants.errors import (
    AgentError,
    ConfigurationError,
    map_error_to_user_message,
)
from apps.ai_tools.schemas.config import EloraConfig
from apps.ai_tools.services.memory_service import get_memory_service

logger = logging.getLogger(__name__)

from apps.ai_tools.tools.project_analysis import (
    analyze_project,
    assess_project_complexity,
    get_project_summary,
)


class EloraService:
    """Service for managing Elora AI Assistant conversations with proper architecture."""

    def __init__(self):
        """Initialize Elora service with validated configuration."""
        try:
            # Validate configuration using Pydantic
            raw_config = settings.ELORA_CONFIG
            self.config = EloraConfig(**raw_config)
            logger.info("Elora configuration validated successfully")

        except ValidationError as e:
            logger.error(f"Elora configuration validation failed: {e}")
            raise ConfigurationError(f"Invalid Elora configuration: {e}")
        except Exception as e:
            logger.error(f"Failed to load Elora configuration: {e}")
            raise ConfigurationError(f"Configuration error: {e}")

        # Initialize tools and memory service
        self.tools = []
        self.memory_service = get_memory_service(self.config)
        self._load_tools()

        logger.info("EloraService initialized successfully")

    def _load_tools(self):
        """Load all available tools for the agent."""
        # Import all available tools with explicit schema support
        from apps.ai_tools.tools.content_search import (
            find_content_references,
            search_project_content,
        )
        from apps.ai_tools.tools.entity_queries import (
            get_project_statistics,
            query_project_entities,
        )
        from apps.ai_tools.tools.project_management import (
            get_project_by_name,
            get_project_summary_stats,
            list_all_projects,
        )
        from apps.ai_tools.tools.story_details import (
            get_canvas_information,
            get_story_details,
        )
        from apps.ai_tools.tools.structure_analysis import (
            analyze_project_structure,
            validate_project_health,
        )
        from apps.ai_tools.tools.world_information import (
            get_character_details,
            get_world_information,
        )

        # Use the tools directly with LangChain's native @tool decorator support
        # This avoids manual Tool wrapper which can cause parameter issues
        self.tools = [
            # Project Management Tools - These should be used FIRST for project queries
            list_all_projects,
            get_project_by_name,
            get_project_summary_stats,

            # Project Analysis Tools
            analyze_project,
            get_project_summary,
            assess_project_complexity,

            # Entity and Structure Analysis
            query_project_entities,
            get_project_statistics,
            analyze_project_structure,
            validate_project_health,

            # Story and World Information
            get_story_details,
            get_canvas_information,
            get_world_information,
            get_character_details,

            # Content Search
            search_project_content,
            find_content_references,
        ]

    def _get_agent_for_user(self, user_id: str) -> 'AgentExecutor':
        """
        Get or create an agent for a specific user.

        Args:
            user_id: Unique user identifier

        Returns:
            Configured AgentExecutor for the user
        """
        try:
            # Get user-specific memory
            memory = self.memory_service.get_memory_for_user(user_id)

            # Build agent using the new architecture
            agent = build_elora_agent(
                config=self.config,
                tools=self.tools,
                memory=memory,
                user_id=user_id
            )

            return agent

        except Exception as e:
            logger.error(f"Failed to create agent for user {user_id}: {e}")
            raise AgentError(f"Failed to initialize agent: {e}")

    def chat(self, message: str, user_id: str = "anonymous") -> str:
        """
        Process a user message and return Elora's response with per-user context.

        Args:
            message: User's input message
            user_id: Unique user identifier for memory management

        Returns:
            Elora's response string
        """
        if not message or not message.strip():
            return "I'm here to help! What would you like to know about your story projects?"

        try:
            # Get user-specific agent
            agent = self._get_agent_for_user(user_id)

            # Process the message through the agent
            response = agent.invoke({"input": message.strip()})
            result = response.get("output", "I'm sorry, I couldn't process that request.")

            # Save memory after successful interaction
            try:
                self.memory_service.save_memory_for_user(user_id, agent.memory)
            except Exception as mem_error:
                logger.warning(f"Failed to save memory for user {user_id}: {mem_error}")

            return result

        except Exception as e:
            logger.error(f"Chat error for user {user_id}: {type(e).__name__}: {e}")
            return map_error_to_user_message(e)

    def get_conversation_history(self, user_id: str = "anonymous") -> list[dict[str, Any]]:
        """
        Get the conversation history for a specific user.

        Args:
            user_id: Unique user identifier

        Returns:
            List of message dictionaries
        """
        try:
            memory = self.memory_service.get_memory_for_user(user_id)
            history = []

            for message in memory.chat_memory.messages:
                if isinstance(message, HumanMessage):
                    history.append({"role": "user", "content": message.content})
                elif isinstance(message, AIMessage):
                    history.append({"role": "assistant", "content": message.content})

            return history

        except Exception as e:
            logger.error(f"Error getting conversation history for user {user_id}: {e}")
            return []

    def clear_conversation(self, user_id: str = "anonymous"):
        """
        Clear the conversation history for a specific user.

        Args:
            user_id: Unique user identifier
        """
        try:
            self.memory_service.clear_memory_for_user(user_id)
            logger.info(f"Cleared conversation for user {user_id}")
        except Exception as e:
            logger.error(f"Error clearing conversation for user {user_id}: {e}")

    def get_memory_stats(self, user_id: str = "anonymous") -> dict[str, Any]:
        """
        Get memory statistics for a specific user.

        Args:
            user_id: Unique user identifier

        Returns:
            Dictionary with memory statistics
        """
        return self.memory_service.get_memory_stats(user_id)

    def is_configured(self) -> bool:
        """Check if Elora is properly configured with required settings."""
        try:
            return (
                self.config.enabled and
                bool(self.config.openai_api_key) and
                len(self.tools) > 0 and
                self.memory_service is not None
            )
        except Exception as e:
            logger.error(f"Configuration check failed: {e}")
            return False

    def get_available_projects(self) -> str:
        """Get a formatted list of available projects using helper function."""
        # Use helper function to avoid direct tool invocation issues
        from apps.ai_tools.tools.project_management import _get_all_projects_helper
        return _get_all_projects_helper()

    def validate_configuration(self) -> dict[str, Any]:
        """
        Validate the current configuration and return diagnostic information.

        Returns:
            Dictionary with configuration validation results
        """
        results = {
            "valid": False,
            "errors": [],
            "warnings": [],
            "config_summary": {}
        }

        try:
            # Test configuration
            results["config_summary"] = {
                "enabled": self.config.enabled,
                "model": self.config.model,
                "api_key_set": bool(self.config.openai_api_key),
                "tools_loaded": len(self.tools),
                "memory_service_available": self.memory_service is not None
            }

            # Validate tools
            try:
                validate_agent_tools(self.tools)
                results["config_summary"]["tools_valid"] = True
            except Exception as e:
                results["errors"].append(f"Tool validation failed: {e}")
                results["config_summary"]["tools_valid"] = False

            # Check if we can create a test agent (without memory)
            try:
                from langchain.memory import ConversationBufferMemory
                test_memory = ConversationBufferMemory(
                    memory_key="chat_history",
                    return_messages=True
                )
                build_elora_agent(self.config, self.tools, test_memory)
                results["config_summary"]["agent_buildable"] = True
            except Exception as e:
                results["errors"].append(f"Agent build test failed: {e}")
                results["config_summary"]["agent_buildable"] = False

            # Overall validation
            results["valid"] = len(results["errors"]) == 0

        except Exception as e:
            results["errors"].append(f"Validation error: {e}")

        return results
