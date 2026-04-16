"""
Memory service for managing per-user conversation memory.

Prevents cross-user memory leakage and provides token-aware memory management.
"""

import hashlib
import logging
import time
from typing import Optional

from django.core.cache import cache
from langchain.memory import ConversationTokenBufferMemory
from langchain_openai import ChatOpenAI

from apps.ai_tools.constants.errors import EloraError
from apps.ai_tools.schemas.config import EloraConfig

logger = logging.getLogger(__name__)

# Memory cache timeout (1 hour by default)
MEMORY_CACHE_TIMEOUT = 3600


class MemoryService:
    """
    Service for managing per-user conversation memory with token awareness.

    Prevents security issues from shared memory and provides efficient
    token-based memory management.
    """

    def __init__(self, config: EloraConfig):
        """Initialize memory service with configuration."""
        self.config = config
        self.llm = ChatOpenAI(**config.get_chat_openai_kwargs())

    def get_memory_for_user(self, user_id: str, session_id: Optional[str] = None) -> ConversationTokenBufferMemory:
        """
        Get conversation memory for a specific user and session.

        Args:
            user_id: Unique user identifier
            session_id: Optional session identifier (defaults to 'default')

        Returns:
            ConversationTokenBufferMemory instance for the user/session
        """
        if not user_id:
            raise EloraError("User ID is required for memory management", "configuration")

        session_id = session_id or "default"
        memory_key = self._get_memory_key(user_id, session_id)

        try:
            # Try to load existing memory from cache
            cached_messages = cache.get(memory_key)

            # Create new memory instance
            memory = ConversationTokenBufferMemory(
                llm=self.llm,
                **self.config.get_memory_kwargs()
            )

            # Restore cached messages if available
            if cached_messages:
                memory.chat_memory.messages = cached_messages
                logger.debug(f"Restored {len(cached_messages)} messages for user {user_id}")
            else:
                logger.debug(f"Created new memory for user {user_id}, session {session_id}")

            return memory

        except Exception as e:
            logger.error(f"Error creating memory for user {user_id}: {e}")
            raise EloraError(f"Failed to initialize conversation memory: {e}", "memory")

    def save_memory_for_user(
        self,
        user_id: str,
        memory: ConversationTokenBufferMemory,
        session_id: Optional[str] = None
    ) -> None:
        """
        Save conversation memory for a user/session.

        Args:
            user_id: Unique user identifier
            memory: Memory instance to save
            session_id: Optional session identifier
        """
        if not user_id:
            return

        session_id = session_id or "default"
        memory_key = self._get_memory_key(user_id, session_id)

        try:
            # Store messages in cache with timeout
            messages = memory.chat_memory.messages
            cache.set(memory_key, messages, timeout=self.config.session_timeout)

            logger.debug(f"Saved {len(messages)} messages for user {user_id}")

        except Exception as e:
            logger.error(f"Error saving memory for user {user_id}: {e}")
            # Don't raise - memory save failures shouldn't break the conversation

    def clear_memory_for_user(self, user_id: str, session_id: Optional[str] = None) -> None:
        """
        Clear conversation memory for a user/session.

        Args:
            user_id: Unique user identifier
            session_id: Optional session identifier
        """
        if not user_id:
            return

        session_id = session_id or "default"
        memory_key = self._get_memory_key(user_id, session_id)

        try:
            cache.delete(memory_key)
            logger.info(f"Cleared memory for user {user_id}, session {session_id}")

        except Exception as e:
            logger.error(f"Error clearing memory for user {user_id}: {e}")

    def get_memory_stats(self, user_id: str, session_id: Optional[str] = None) -> dict:
        """
        Get statistics about user's memory usage.

        Args:
            user_id: Unique user identifier
            session_id: Optional session identifier

        Returns:
            Dictionary with memory statistics
        """
        if not user_id:
            return {"error": "User ID required"}

        session_id = session_id or "default"
        memory_key = self._get_memory_key(user_id, session_id)

        try:
            cached_messages = cache.get(memory_key)

            if not cached_messages:
                return {
                    "message_count": 0,
                    "token_estimate": 0,
                    "memory_exists": False
                }

            # Estimate tokens (rough calculation)
            token_estimate = sum(len(msg.content.split()) * 1.3 for msg in cached_messages if hasattr(msg, 'content'))

            return {
                "message_count": len(cached_messages),
                "token_estimate": int(token_estimate),
                "memory_exists": True,
                "last_updated": time.time()
            }

        except Exception as e:
            logger.error(f"Error getting memory stats for user {user_id}: {e}")
            return {"error": str(e)}

    def cleanup_expired_memories(self) -> int:
        """
        Clean up expired conversation memories.

        Returns:
            Number of memories cleaned up
        """
        # This would be implemented with a proper cache backend that supports
        # pattern matching (like Redis). Django's default cache doesn't support
        # this easily, so we'll rely on cache timeout for now.
        logger.info("Memory cleanup relies on cache timeout")
        return 0

    def _get_memory_key(self, user_id: str, session_id: str) -> str:
        """
        Generate a cache key for user/session memory.

        Args:
            user_id: User identifier
            session_id: Session identifier

        Returns:
            Cache key string
        """
        # Hash to ensure consistent key length and handle special characters
        combined = f"elora_memory_{user_id}_{session_id}"
        return hashlib.md5(combined.encode()).hexdigest()


# Singleton instance - will be replaced with dependency injection later
_memory_service: Optional[MemoryService] = None


def get_memory_service(config: EloraConfig) -> MemoryService:
    """
    Get memory service instance (singleton for now).

    Args:
        config: Elora configuration

    Returns:
        MemoryService instance
    """
    global _memory_service

    if _memory_service is None:
        _memory_service = MemoryService(config)

    return _memory_service


def clear_memory_service():
    """Clear the singleton memory service (for testing)."""
    global _memory_service
    _memory_service = None
