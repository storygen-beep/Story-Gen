"""
Pydantic configuration models for Elora AI Assistant.

Provides validated configuration with proper defaults and type safety.
"""


from pydantic import BaseModel, Field, validator


class EloraConfig(BaseModel):
    """Configuration model for Elora AI Assistant with validation."""

    enabled: bool = Field(default=True, description="Enable/disable Elora AI assistant")
    openai_api_key: str = Field(..., description="OpenAI API key (required)")
    model: str = Field(default="gpt-4o", description="OpenAI model to use")
    temperature: float = Field(default=0.5, ge=0.0, le=2.0, description="Model temperature (0-2)")
    max_tokens: int = Field(default=1500, ge=100, le=4000, description="Maximum tokens per response")
    memory_token_limit: int = Field(default=4000, ge=1000, le=10000, description="Memory token budget")
    request_timeout: int = Field(default=30, ge=5, le=120, description="Request timeout in seconds")
    max_iterations: int = Field(default=7, ge=3, le=15, description="Max agent iterations")
    max_history: int = Field(default=50, ge=10, le=100, description="Max conversation messages")
    session_timeout: int = Field(default=3600, ge=300, le=86400, description="Session timeout in seconds")

    @validator('openai_api_key')
    def validate_api_key(cls, v):
        """Validate OpenAI API key format."""
        if not v or not v.strip():
            raise ValueError("OpenAI API key is required")

        # Basic format validation - OpenAI keys start with sk-
        if not v.startswith('sk-'):
            raise ValueError("Invalid OpenAI API key format - should start with 'sk-'")

        # Should be at least 20 characters
        if len(v) < 20:
            raise ValueError("OpenAI API key appears to be too short")

        return v.strip()

    @validator('model')
    def validate_model(cls, v):
        """Validate supported models."""
        supported_models = {
            'gpt-4o', 'gpt-4o-mini', 'gpt-4', 'gpt-4-turbo',
            'gpt-3.5-turbo', 'gpt-3.5-turbo-16k'
        }

        if v not in supported_models:
            raise ValueError(f"Unsupported model: {v}. Supported: {', '.join(supported_models)}")

        return v

    def get_chat_openai_kwargs(self) -> dict:
        """Get kwargs for ChatOpenAI initialization."""
        return {
            'api_key': self.openai_api_key,
            'model': self.model,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'timeout': self.request_timeout,
        }

    def get_memory_kwargs(self) -> dict:
        """Get kwargs for memory initialization."""
        return {
            'max_token_limit': self.memory_token_limit,
            'memory_key': "chat_history",
            'return_messages': True,
        }

    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        extra = "forbid"  # Don't allow extra fields
        json_schema_extra = {
            "example": {
                "enabled": True,
                "openai_api_key": "sk-proj-...",
                "model": "gpt-4o",
                "temperature": 0.5,
                "max_tokens": 1500,
                "memory_token_limit": 4000,
                "request_timeout": 30,
                "max_iterations": 7,
                "max_history": 50,
                "session_timeout": 3600
            }
        }
