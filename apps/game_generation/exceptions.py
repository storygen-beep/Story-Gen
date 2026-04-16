"""
Game Generation Exceptions.

Basic exception classes for game generation errors.
"""


class GameGenerationException(Exception):
    """Base exception for game generation errors."""

    pass


class SystemNotFoundException(GameGenerationException):
    """Raised when requested generation system is not found."""

    pass


class GeneratorVersionException(GameGenerationException):
    """Raised when requested generator version is not found."""

    pass


class ProjectValidationException(GameGenerationException):
    """Raised when project fails validation for generation."""

    pass


class CompilationException(GameGenerationException):
    """Raised when game compilation fails."""

    pass
