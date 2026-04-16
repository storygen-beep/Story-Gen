# Django Development Guidelines

This document outlines the development standards, best practices, and guidelines for the Django REST Framework backend migration.

## Table of Contents

- [Code Quality Standards](#code-quality-standards)
- [Architecture Principles](#architecture-principles)
- [Security Best Practices](#security-best-practices)
- [Development Workflow](#development-workflow)
- [API Design Standards](#api-design-standards)
- [Testing Guidelines](#testing-guidelines)
- [Performance Guidelines](#performance-guidelines)
- [Deployment Standards](#deployment-standards)

## Code Quality Standards

### SOLID Principles

1. **Single Responsibility Principle (SRP)**
   - Each class, function, or module should have one reason to change
   - Separate business logic into service classes
   - Keep views focused on HTTP request/response handling

2. **Open/Closed Principle (OCP)**
   - Software entities should be open for extension but closed for modification
   - Use mixins and inheritance for extending functionality
   - Leverage Django's class-based views for customization

3. **Liskov Substitution Principle (LSP)**
   - Derived classes must be substitutable for their base classes
   - Follow Django's established patterns for model inheritance
   - Ensure consistent interfaces across similar components

4. **Interface Segregation Principle (ISP)**
   - Clients should not be forced to depend on interfaces they don't use
   - Create specific serializers for different use cases
   - Use composition over inheritance where appropriate

5. **Dependency Inversion Principle (DIP)**
   - Depend on abstractions, not concretions
   - Use Django's dependency injection patterns
   - Abstract external services behind interfaces

### Code Organization

- **Service Layer Pattern**: Business logic resides in services, not views or models
- **DRY (Don't Repeat Yourself)**: Abstract common functionality into utilities and mixins
- **KISS (Keep It Simple, Stupid)**: Prefer simplicity over complexity
- **YAGNI (You Aren't Gonna Need It)**: Implement only current requirements

### Documentation Standards

- All public methods must have docstrings following Google style
- API endpoints must be documented with drf-spectacular
- README files for complex modules
- Inline comments for complex business logic only

## Architecture Principles

### Project Structure

```
apps/
├── authentication/     # JWT auth, user management
├── projects/          # Project management logic
├── stories/           # Story and canvas system
├── characters/        # Character management
├── worlds/            # World building features
└── common/            # Shared utilities and mixins

core/
├── services/          # Business logic services
├── validators/        # Custom validation logic
└── exceptions/        # Custom exception classes

api/v1/               # API versioning
config/settings/      # Environment-based settings
```

### Service Layer Architecture

- **Views**: Handle HTTP requests/responses, authentication, permissions
- **Services**: Contain business logic, coordinate between models
- **Models**: Data layer only, minimal business logic
- **Serializers**: Data validation and transformation

```python
# Example service structure
class StoryService:
    @staticmethod
    def create_story(user, story_data):
        # Business logic here
        pass

    @staticmethod
    def validate_story_permissions(user, story):
        # Permission logic here
        pass
```

### Model Best Practices

- Use `UUIDField` for primary keys where appropriate
- Implement `__str__` methods for all models
- Use `help_text` for complex fields
- Define custom managers for complex queries
- Use model properties for calculated fields

## Security Best Practices

### Authentication & Authorization

- **JWT Tokens**: Use short-lived access tokens (1 hour) with refresh tokens
- **Permission Classes**: Implement granular permissions per endpoint
- **Rate Limiting**: Apply rate limiting to prevent abuse
- **HTTPS Only**: Enforce HTTPS in production environments

### Data Protection

- **Environment Variables**: Store all secrets in environment variables
- **Input Validation**: Validate and sanitize all user inputs
- **SQL Injection Prevention**: Use Django ORM, avoid raw SQL
- **XSS Protection**: Use Django's built-in XSS protection
- **CSRF Protection**: Enable CSRF tokens for state-changing operations

### Security Headers

```python
# Production security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
```

## Development Workflow

### Git Workflow

1. **Branch Naming**: `feature/feature-name`, `bugfix/issue-description`, `hotfix/critical-fix`
2. **Commits**: Follow conventional commit format: `type(scope): description`
3. **Pull Requests**: Require code review before merging
4. **Main Branch**: Always keep main branch deployable

### Pre-commit Hooks

All code must pass these checks before commit:

- **Black**: Code formatting (88 character line length)
- **Ruff**: Fast linting (replaces flake8 + isort)
- **mypy**: Static type checking
- **Django Tests**: All tests must pass
- **Migration Check**: No missing migrations

### Code Review Checklist

- [ ] Follows SOLID principles
- [ ] Has appropriate tests (minimum 80% coverage)
- [ ] Includes proper error handling
- [ ] Uses type hints
- [ ] Has proper documentation
- [ ] Follows security best practices
- [ ] No hardcoded values
- [ ] Database queries are optimized

## API Design Standards

### RESTful Principles

- Use appropriate HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Consistent URL naming conventions
- Proper HTTP status codes
- Meaningful error messages

### URL Patterns

```
/api/v1/projects/                    # List all projects
/api/v1/projects/{id}/               # Project detail
/api/v1/projects/{id}/stories/       # Project's stories
/api/v1/stories/{id}/characters/     # Story's characters
```

### Response Format

```json
{
  "data": {
    "id": "uuid",
    "attributes": {},
    "relationships": {}
  },
  "meta": {
    "pagination": {},
    "timestamps": {}
  }
}
```

### Error Handling

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field_name": ["This field is required."]
    }
  }
}
```

## Testing Guidelines

### Test Structure

- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test component interactions
- **API Tests**: Test endpoint behavior
- **Performance Tests**: Test response times and query counts

### Test Organization

```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/
│   ├── test_api_workflows.py
│   └── test_service_integration.py
└── fixtures/
    └── test_data.py
```

### Testing Best Practices

- Use `factory_boy` for test data creation
- Test both success and failure cases
- Mock external services
- Use `pytest` fixtures for setup/teardown
- Aim for 80%+ test coverage

## Performance Guidelines

### Database Optimization

- Use `select_related()` for forward foreign keys
- Use `prefetch_related()` for reverse foreign keys and many-to-many
- Add database indexes for frequently queried fields
- Use `django-debug-toolbar` to identify N+1 queries

### Caching Strategy

- Cache expensive computed results
- Use Redis for session storage in production
- Implement cache invalidation strategies
- Cache API responses for read-heavy endpoints

### Query Optimization

```python
# Good: Optimized query
stories = Story.objects.select_related('project').prefetch_related('characters')

# Bad: N+1 query problem
for story in Story.objects.all():
    print(story.project.name)  # Additional query per story
```

## Deployment Standards

### Environment Configuration

- **Development**: Full debugging, local database
- **Staging**: Production-like, test database
- **Production**: Optimized settings, monitoring enabled

### Health Checks

Implement health check endpoints:

```python
# /api/v1/health/
{
  "status": "healthy",
  "database": "connected",
  "cache": "connected",
  "version": "1.0.0"
}
```

### Monitoring

- Log all errors with structured logging
- Monitor database query performance
- Track API response times
- Set up alerts for critical issues

## Migration Guidelines

### Database Migrations

- Always create migrations for model changes
- Test migrations on copy of production data
- Make migrations backward compatible when possible
- Document breaking changes

### Deployment Process

1. Run tests in CI/CD pipeline
2. Deploy to staging environment
3. Run integration tests
4. Deploy to production during maintenance window
5. Monitor for errors post-deployment

## Error Handling Standards

### Custom Exceptions

```python
class StoryGenerationException(Exception):
    """Base exception for story generation errors"""
    pass

class ValidationError(StoryGenerationException):
    """Raised when validation fails"""
    pass
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

try:
    # Business logic
    pass
except Exception as e:
    logger.error(f"Story creation failed: {e}", extra={
        'user_id': user.id,
        'story_data': story_data
    })
    raise
```

This document should be reviewed regularly and updated as the project evolves.
