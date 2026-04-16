FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (including OpenCV and FFmpeg requirements)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    libgl1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/ requirements/
RUN pip install --upgrade pip
RUN pip install -r requirements/development.txt

# Copy project
COPY . .

# Create logs directory
RUN mkdir -p logs

## Collect static files at runtime (via init.sh) to avoid requiring env vars at build time

# Create superuser script
COPY scripts/create-superuser.py scripts/create-superuser.py

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
