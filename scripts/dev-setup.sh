#!/bin/bash

# Django Development Setup Script

set -e

echo "🚀 Setting up Django development environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements/development.txt

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Install pre-commit hooks
echo "🔧 Installing pre-commit hooks..."
pre-commit install

# Create superuser if needed
echo "👤 Setting up superuser..."
PYTHONPATH=. python scripts/create-superuser.py

echo "✅ Django development environment is ready!"
echo ""
echo "To start the development server:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "API Documentation will be available at:"
echo "  http://127.0.0.1:8000/api/docs/"
