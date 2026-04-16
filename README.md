# Django Story Generation Platform

A modern Django REST Framework backend for the story generation platform, built with industry best practices and enterprise-grade architecture.

## Features

- **Modern Django**: Django 5.0 with Django REST Framework 3.14
- **JWT Authentication**: Secure token-based authentication with refresh tokens
- **PostgreSQL Database**: Production-ready database with optimized queries
- **API Documentation**: Auto-generated OpenAPI documentation with Swagger UI
- **Code Quality**: Pre-commit hooks with Black, Ruff, and mypy
- **Docker Support**: Complete containerized development environment
- **Environment-based Settings**: Separate configurations for dev/staging/production
- **Service Layer Architecture**: Clean separation of concerns following SOLID principles

## Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository and navigate to Django backend
cd story_gen_django

# Run the automated setup script
./scripts/dev-setup.sh

# Start the development server
source venv/bin/activate
python manage.py runserver
```

### Option 2: Docker Setup

```bash
# Start all services (PostgreSQL, Redis, Django)
docker-compose up --build

# The API will be available at http://localhost:8000
```

### Option 3: Manual Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements/development.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/
- **OpenAPI Schema**: http://127.0.0.1:8000/api/schema/

## Architecture

```
story_gen_django/
├── config/                     # Django configuration
│   ├── settings/              # Environment-based settings
│   ├── urls.py               # Root URL configuration
│   ├── wsgi.py               # WSGI config
│   └── asgi.py               # ASGI config
├── apps/                      # Django applications
│   ├── authentication/       # JWT auth, user management
│   ├── projects/             # Project management
│   ├── stories/              # Story and canvas system
│   ├── characters/           # Character management
│   ├── worlds/               # World building
│   └── common/               # Shared utilities
├── api/                      # API versioning
│   └── v1/                   # API v1 routes
├── core/                     # Core business logic
│   ├── services/             # Service layer
│   ├── validators/           # Custom validators
│   └── exceptions/           # Custom exceptions
├── requirements/             # Environment-specific dependencies
├── docs/                     # Project documentation
└── tests/                    # Test suite
```

## Development Guidelines

This project follows strict development standards outlined in [docs/DEVELOPMENT_GUIDELINES.md](docs/DEVELOPMENT_GUIDELINES.md), including:

- **SOLID Principles**: Clean architecture with separation of concerns
- **Service Layer Pattern**: Business logic isolated from views
- **Security Best Practices**: JWT tokens, input validation, HTTPS enforcement
- **Code Quality**: Pre-commit hooks, 80%+ test coverage requirement
- **API Design**: RESTful endpoints with consistent error handling

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

```bash
# Register a new user
curl -X POST http://localhost:8000/api/v1/auth/register/ \\
  -H "Content-Type: application/json" \\
  -d '{"username": "user", "password": "secure123", "password2": "secure123", "email": "user@example.com"}'

# Login to get tokens
curl -X POST http://localhost:8000/api/v1/auth/token/ \\
  -H "Content-Type: application/json" \\
  -d '{"username": "user", "password": "secure123"}'

# Access protected endpoints
curl -X GET http://localhost:8000/api/v1/auth/me/ \\
  -H "Authorization: Bearer <access_token>"
```

## Environment Variables

Create a `.env` file with the following variables:

```env
# Django Configuration
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=story_gen_django_dev
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## Supabase Postgres

Connect the backend to a Supabase-managed Postgres by setting the existing `DB_*` env vars to your Supabase connection values and enabling SSL.

- DB host: `db.<project-ref>.supabase.co` (direct) or `<region>.pooler.supabase.net` (pooler)
- DB port: `5432` (direct) or `6543` (pooler)
- DB name: usually `postgres`
- DB user: `postgres` or a dedicated user you create
- DB password: from Supabase dashboard

Environment templates:

Direct connection (recommended to start):

```env
# Supabase (Direct)
DB_HOST=db.<project-ref>.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=<your-db-password>

# Required for Supabase connections
PGSSLMODE=require
```

Connection Pooler (PgBouncer):

```env
# Supabase (Pooler)
DB_HOST=<region>.pooler.supabase.net
DB_PORT=6543
DB_NAME=postgres
DB_USER=<your-db-user>
DB_PASSWORD=<your-db-password>

# Required for Supabase connections
PGSSLMODE=require
```

Notes:
- `PGSSLMODE=require` is read by libpq/psycopg to enforce TLS; no code change needed.
- For stricter verification, you can use `PGSSLMODE=verify-full` with `PGSSLROOTCERT`.
- If you later switch to transaction pooling, consider setting `CONN_MAX_AGE=0` (a small code change in settings).

Migrate and verify:

```bash
source venv/bin/activate
python manage.py check
python manage.py migrate
python manage.py runserver
```

Optional extensions (run once in Supabase SQL editor):

```sql
create extension if not exists vector;
create extension if not exists pg_trgm; -- if trigram ops are used
```

## Development Commands

```bash
# Code quality checks
black .                    # Format code
ruff check .              # Lint code
mypy .                    # Type checking
pre-commit run --all-files # Run all checks

# Django management
python manage.py check             # Check for issues
python manage.py migrate           # Run migrations
python manage.py collectstatic     # Collect static files
python manage.py test              # Run tests

# Database operations
python manage.py makemigrations    # Create migrations
python manage.py shell             # Django shell
python manage.py dbshell          # Database shell
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test modules
pytest apps/authentication/tests/
pytest tests/integration/

# Run performance tests
pytest -m "not slow"
```

## Deployment

The project supports multiple deployment strategies:

- **Development**: SQLite, debug mode, hot reload
- **Staging**: PostgreSQL, production settings, test data
- **Production**: PostgreSQL, Redis cache, monitoring

See [docs/DEVELOPMENT_GUIDELINES.md](docs/DEVELOPMENT_GUIDELINES.md) for detailed deployment instructions.

## Contributing

1. Follow the coding standards in [docs/DEVELOPMENT_GUIDELINES.md](docs/DEVELOPMENT_GUIDELINES.md)
2. Write tests for new features (minimum 80% coverage)
3. Run pre-commit hooks before committing
4. Use conventional commit messages
5. Create pull requests for code review

## Migration from FastAPI

This Django backend is designed to replace the existing FastAPI backend. Key migration considerations:

- **Models**: SQLModel → Django ORM models
- **Serializers**: Pydantic → DRF serializers
- **Authentication**: FastAPI JWT → djangorestframework-simplejwt
- **API Structure**: FastAPI routes → DRF viewsets and routers
- **Database**: Direct PostgreSQL connection preserved

## License

This project is part of the Story Generation Platform.
# Story-Gen
