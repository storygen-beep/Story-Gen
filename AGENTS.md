# Repository Guidelines

## Project Structure & Module Organization
- `apps/`: Django apps (e.g., `authentication/`, `projects/`, `stories/`, `characters/`, `world/`, `npcs/`, `worlds/`, `common/`, `game_generation/`).
- `api/v1/`: Versioned API routes and health checks.
- `config/`: Django settings (`settings/` for `development`, `testing`, `production`), URLs, ASGI/WSGI.
- `core/`: Service layer, validators, exceptions.
- `requirements/`: Env-specific dependencies; `scripts/`: helper scripts.
- `static/`, `staticfiles/`, `media/`, `logs/`, `tests/`, `docs/`.

## Build, Test, and Development Commands
- Setup: `./scripts/dev-setup.sh` (venv, deps, migrate, collectstatic, hooks).
- Run dev server: `source venv/bin/activate && python manage.py runserver`.
- Docker: `docker-compose up --build`.
- Quality: `black .`, `ruff check .`, `mypy .`, `pre-commit run --all-files`.
- Django: `python manage.py migrate | makemigrations | check | collectstatic`.
- Tests: `pytest` or `python manage.py test`; with coverage: `pytest --cov`.

## Coding Style & Naming Conventions
- Formatting: Black (line length 88). Linting: Ruff (pycodestyle/pyflakes/isort), MyPy for types.
- Indentation: 4 spaces; imports grouped and sorted (ruff-isort).
- Names: Classes `PascalCase`; functions/vars `snake_case`; modules `snake_case`; constants `UPPER_SNAKE_CASE`.
- Django: keep business logic in `core/services`, thin views/serializers; validate with DRF serializers.

## Testing Guidelines
- Framework: `pytest` with Django (`DJANGO_SETTINGS_MODULE=config.settings.testing`).
- Locations: place tests in `tests/` or app-level `tests/` packages.
- Naming: files `test_*.py`, functions `test_*`; use markers `@pytest.mark.unit|integration|slow`.
- Coverage: target ≥80% (see `README.md`); exclude migrations and settings as configured in `pyproject.toml`.

## Commit & Pull Request Guidelines
- Commits: Conventional Commits style, e.g., `feat(auth): add JWT refresh`.
- Branches: `feature/<slug>`, `fix/<slug>`, `chore/<slug>`.
- PRs: clear description, linked issues, steps to test, screenshots (for API responses if relevant), migration notes, and checklist that pre-commit passes.

## Security & Configuration
- Do not commit secrets. Copy `.env.example` to `.env`; set DB and JWT settings.
- Use PostgreSQL locally (see `config/settings/*`). Keep `DEBUG` off outside development.
- CORS origins configured via `CORS_ALLOWED_ORIGINS` in `.env`.

## Architecture Overview
- Django REST Framework + JWT (SimpleJWT), service-layer architecture, versioned API under `api/v1/`, OpenAPI docs available at `/api/docs/`.

