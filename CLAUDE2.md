# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Quick Setup
- `./scripts/dev-setup.sh` - Automated setup script that creates venv, installs dependencies, runs migrations, and sets up pre-commit hooks
- `source venv/bin/activate` - Activate the virtual environment (required for all Django commands)

### Django Management
- `python manage.py runserver` - Start Django development server (default: http://127.0.0.1:8000)
- `python manage.py migrate` - Apply database migrations
- `python manage.py makemigrations` - Create new migrations after model changes
- `python manage.py collectstatic` - Collect static files
- `python manage.py createsuperuser` - Create Django admin superuser
- `python manage.py shell` - Open Django shell with models loaded
- `python manage.py check` - Check for Django issues without running server

### Testing
- `pytest` - Run all tests
- `pytest --cov` - Run tests with coverage report
- `pytest apps/authentication/tests/` - Run tests for specific app
- `pytest tests/integration/` - Run integration tests only
- `pytest -m "not slow"` - Skip slow tests
- `pytest -v` - Verbose test output

### Code Quality
- `black .` - Format all Python code (88 character line length)
- `ruff check .` - Lint code with Ruff (replaces flake8 + isort)
- `mypy .` - Static type checking
- `pre-commit run --all-files` - Run all pre-commit checks
- `bandit -r .` - Security scanning

### Docker Development
- `docker-compose up --build` - Start all services (PostgreSQL, Redis, Django)
- `docker-compose down` - Stop all services
- `docker-compose logs [service_name]` - View logs for specific service

## Architecture Overview

### Service Layer Architecture
This Django project implements a clean service layer architecture following SOLID principles:

- **Views**: Handle HTTP requests/responses, authentication, and permissions only
- **Services**: Contain all business logic, coordinate between models
- **Models**: Data layer with minimal business logic
- **Serializers**: Data validation and transformation

### App Structure
```
apps/
├── authentication/    # JWT auth, custom User model
├── projects/         # Project management
├── stories/          # Canvas system with nodes, connections, flags
├── characters/       # Character management
├── worlds/           # World building (separate from 'world' app)
├── world/            # Location management (legacy compatibility)
├── npcs/             # NPC management
├── game_generation/  # Modular game generation systems
└── common/           # Shared utilities and mixins
```

### Key Django Patterns
- **Custom User Model**: `authentication.User` with UUID primary keys
- **Soft Delete**: Projects and other models support soft deletion via `deleted_at` timestamps
- **UUID Primary Keys**: All models use UUID fields for FastAPI compatibility
- **JSONField**: Extensive use of JSONField for flexible metadata storage
- **Service Classes**: Business logic isolated in `services.py` files per app

### Database Architecture
- **PostgreSQL**: Primary database with connection pooling (`CONN_MAX_AGE`)
- **UUID Fields**: All primary keys are UUIDs for distributed system compatibility
- **Indexes**: Strategic indexing on frequently queried fields (owner, status, created_at)
- **Soft Deletes**: Most models support soft deletion rather than hard deletes

### API Design Patterns
- **JWT Authentication**: Short-lived access tokens (15 min) with refresh tokens (7 days)
- **DRF ViewSets**: RESTful API endpoints with automatic routing
- **Filtering**: Built-in filtering, search, and ordering via `django-filter`
- **Pagination**: Page-based pagination with 20 items per page default
- **OpenAPI Documentation**: Auto-generated Swagger UI at `/api/docs/`

### Game Generation System
The project features a modular game generation architecture with complete isolation between different generation systems:

#### Architecture Overview
- **Single Django App**: `apps/game_generation/` contains all generation systems
- **Complete Isolation**: Each generation system is completely isolated with no shared dependencies
- **Unified API**: Single `GameService` interface delegates to appropriate isolated systems
- **Dynamic Loading**: Systems are loaded at runtime using importlib for flexibility
- **Version Support**: Each system supports multiple generator versions (v1, v2, etc.)

#### Available Generation Systems

**Twee Navigation System** (`twee_navigation/`)
- Simple navigation-based exploration games
- Basic scene-to-scene movement
- Minimal state management
- Quick prototyping and testing

**Twee Comprehensive System** (`twee_comprehensive/`)
- Sophisticated interactive experiences with multiple layers
- Character progression and NPC interactions
- Location discovery and time management
- Relationship tracking and activity systems
- Full narrative layer with dialogue and choices

#### Using the Game Service

```python
from apps.game_generation.services.game_service import GameService

service = GameService()

# Generate navigation game
twee_content = service.generate_game(project, 'twee_navigation', 'v1')

# Generate comprehensive game
twee_content = service.generate_game(project, 'twee_comprehensive', 'v1')

# Compile to HTML
html_content = service.compile_twee_to_html(twee_content, project.name)

# Get available systems
systems = service.get_available_systems()
```

#### Adding New Generation Systems

1. Create a new folder under `apps/game_generation/` (e.g., `unity_export/`)
2. Add isolated generator versions in `generators/v1.py`
3. Create a service class in `services.py`
4. Register in `GameService.REGISTERED_SYSTEMS` dictionary
5. No shared code or dependencies with other systems

### Migration from FastAPI
This Django backend replaces an existing FastAPI system:
- **API Compatibility**: Maintains same endpoint structure and response formats
- **Model Migration**: SQLModel → Django ORM models with UUID preservation
- **JWT Compatibility**: Matches FastAPI token structure and expiry times
- **Feature Parity**: All FastAPI features replicated in Django

## Critical Development Notes

### Pre-commit Hooks
All commits must pass these checks (configured in `pyproject.toml`):
- **Black**: Code formatting (88 character lines, excludes migrations)
- **Ruff**: Fast linting with Django-specific rules (DJ prefix)
- **MyPy**: Type checking with Django plugin
- **Tests**: All tests must pass before commit

### Environment Configuration
The project uses environment-based settings:
- **Development**: `config.settings.development` (default)
- **Testing**: `config.settings.testing` (for pytest)
- **Production**: `config.settings.production`

### Database Migrations
- Always create migrations after model changes: `python manage.py makemigrations`
- Review migration files before applying - especially for production
- Test migrations on copy of production data for complex changes
- Use `--fake-initial` only when absolutely necessary

### SugarCube Game Generation
When working with the game generation systems:
- **Story Canvas**: Models in `apps/stories/models.py` represent visual story editor
- **Node Types**: Currently simplified to single `story_content` type
- **Game Generation**: Handled by modular systems in `apps/game_generation/`
- **System Selection**: Choose between `twee_navigation` (simple) or `twee_comprehensive` (full-featured)
- **Validation**: Each system has its own validation logic before generation
- **Output Format**: Generated Twee files must be SugarCube 2.36.1 compatible
- **HTML Compilation**: Automatic Tweego compilation with fallback HTML wrapper

### Testing Strategy
- **Unit Tests**: Test individual functions and methods in isolation
- **Integration Tests**: Test component interactions and API endpoints
- **Game Generation Tests**: `apps/game_generation/tests/` — a package, NOT a `tests.py`.
  A sibling `tests.py` is shadowed by it and silently collects zero tests, which is exactly
  what happened to the legacy suite for 140 commits (see `tests/test_legacy_engine.py`).
  Put new suites in the package as `test_<feature>.py` and run them by explicit path:
  `pytest apps/game_generation/tests/ -q` (pyproject sets `testpaths = ["tests"]`, so a
  bare `pytest` does not collect app suites).
- **System Isolation Tests**: Verify complete isolation between generation systems
- **Fixtures**: Use `factory_boy` for test data creation
- **Coverage**: Maintain 80%+ test coverage requirement
- **Performance**: Mark slow tests with `@pytest.mark.slow`

### Security Considerations
- **JWT Tokens**: Access tokens expire in 15 minutes, refresh tokens in 7 days
- **CORS**: Configured for frontend origins (localhost:3000)
- **Input Validation**: All user inputs validated via DRF serializers
- **Permission Classes**: Granular permissions per endpoint
- **Environment Variables**: All secrets stored in environment variables

### API Documentation
- **Swagger UI**: Available at `http://127.0.0.1:8000/api/docs/`
- **ReDoc**: Available at `http://127.0.0.1:8000/api/redoc/`
- **OpenAPI Schema**: Available at `http://127.0.0.1:8000/api/schema/`
- **Auto-generated**: Documentation updates automatically with code changes

This Django backend maintains full compatibility with the existing FastAPI system while providing better developer experience, stronger typing, and enterprise-grade architecture patterns.
