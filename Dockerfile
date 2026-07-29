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
    unzip \
    libgl1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Tweego — the game compiler. REQUIRED, not optional: package_from_toml now raises when it
# is absent rather than emitting a "Basic Preview Mode" page of raw Twee source (which is
# what silently shipped to the portal on 2026-07-28). Without this layer every build in
# this image would hard-fail.
#
# Pinned to match EXPECTED_TWEEGO_VERSION in apps/game_generation/services/game_service.py.
# Tweego bundles its own story format, so this version is what decides the SugarCube
# (2.30.0) every game built here ships against.
#
# storyformats/ must land NEXT TO the binary — format lookup is binary-relative, and the
# binary alone compiles nothing. Upstream publishes no linux-arm64 build, so this image is
# amd64-only; on arm64 hosts build with --platform=linux/amd64.
ENV TWEEGO_VERSION=2.1.1
RUN curl -fsSL -o /tmp/tweego.zip \
      "https://github.com/tmedwards/tweego/releases/download/v${TWEEGO_VERSION}/tweego-${TWEEGO_VERSION}-linux-x64.zip" \
    && unzip -q /tmp/tweego.zip -d /tmp/tweego \
    && install -m 0755 /tmp/tweego/tweego /usr/local/bin/tweego \
    && cp -R /tmp/tweego/storyformats /usr/local/bin/storyformats \
    && rm -rf /tmp/tweego /tmp/tweego.zip \
    # --list-formats writes to STDERR and exits 1 on success, hence the 2>&1 and the `|| true`.
    && (tweego --list-formats 2>&1 || true) | grep -q sugarcube-2

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
