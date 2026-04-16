"""
Error handling constants and user-friendly error mappings.
"""

import logging

logger = logging.getLogger(__name__)

# User-friendly error messages for common issues
KNOWN_ERRORS: dict[str, str] = {
    "validation error": "I couldn't parse that. Try a clear ask like: 'List my projects.'",
    "not found": "I couldn't find what you're looking for. Try 'list my projects' to see what's available.",
    "rate_limit": "I'm getting rate-limited. Please retry in a moment.",
    "timeout": "The request timed out. Please try again with a simpler question.",
    "openai": "There's an issue with the OpenAI API connection. Please check your configuration.",
    "api key": "There's an issue with the OpenAI API key. Please check your configuration.",
    "connection": "I'm having trouble connecting to the AI service. Please try again.",
    "unauthorized": "The API key is invalid or has insufficient permissions.",
    "quota": "API quota exceeded. Please check your OpenAI billing.",
    "model": "The requested AI model is not available.",
    "parsing": "I had trouble understanding the response format. Please try rephrasing.",
    "agent": "I encountered an issue with the agent system. Please try again.",
    "tool": "There was an issue with one of my tools. Please try a different approach.",
    "memory": "I'm having memory issues. Let me start fresh.",
}

# Default fallback message
DEFAULT_ERROR_MESSAGE = "Something went wrong on my end. Could you please try rephrasing your question?"

# Recovery suggestions for different error types
RECOVERY_SUGGESTIONS: dict[str, str] = {
    "validation": "Try asking: 'show me my projects' or 'help' for examples.",
    "not_found": "Use 'list my projects' to see what's available first.",
    "connection": "Check your internet connection and try again.",
    "configuration": "Verify your OpenAI API key is set correctly.",
    "quota": "Check your OpenAI billing and usage limits.",
    "general": "Try rephrasing your question or type 'help' for guidance."
}


def map_error_to_user_message(error: Exception) -> str:
    """
    Map an exception to a user-friendly error message.

    Args:
        error: The exception that occurred

    Returns:
        User-friendly error message with recovery suggestion
    """
    error_str = str(error).lower()

    # Log the original error for debugging
    logger.error(f"Elora error: {type(error).__name__}: {error}")

    # Find matching error pattern
    for key, message in KNOWN_ERRORS.items():
        if key in error_str:
            # Add recovery suggestion if available
            error_type = _get_error_type(key)
            suggestion = RECOVERY_SUGGESTIONS.get(error_type, RECOVERY_SUGGESTIONS["general"])
            return f"{message} {suggestion}"

    # No specific match found
    return f"{DEFAULT_ERROR_MESSAGE} {RECOVERY_SUGGESTIONS['general']}"


def _get_error_type(error_key: str) -> str:
    """
    Map error keys to broader error types for recovery suggestions.

    Args:
        error_key: The matched error key

    Returns:
        Broader error type for recovery suggestions
    """
    error_type_mapping = {
        "validation error": "validation",
        "parsing": "validation",
        "not found": "not_found",
        "rate_limit": "quota",
        "quota": "quota",
        "timeout": "connection",
        "connection": "connection",
        "openai": "configuration",
        "api key": "configuration",
        "unauthorized": "configuration",
        "model": "configuration",
        "agent": "general",
        "tool": "general",
        "memory": "general",
    }

    return error_type_mapping.get(error_key, "general")


class EloraError(Exception):
    """Base exception for Elora-specific errors."""

    def __init__(self, message: str, error_type: str = "general", recoverable: bool = True):
        super().__init__(message)
        self.error_type = error_type
        self.recoverable = recoverable

    def get_user_message(self) -> str:
        """Get user-friendly error message."""
        suggestion = RECOVERY_SUGGESTIONS.get(self.error_type, RECOVERY_SUGGESTIONS["general"])
        return f"{str(self)} {suggestion}"


class ConfigurationError(EloraError):
    """Configuration-related errors."""

    def __init__(self, message: str):
        super().__init__(message, error_type="configuration", recoverable=False)


class ToolError(EloraError):
    """Tool execution errors."""

    def __init__(self, message: str, tool_name: str = None):
        if tool_name:
            message = f"Tool '{tool_name}': {message}"
        super().__init__(message, error_type="general", recoverable=True)


class AgentError(EloraError):
    """Agent execution errors."""

    def __init__(self, message: str):
        super().__init__(message, error_type="general", recoverable=True)
