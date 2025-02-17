# === BASE STAGE (Common Dependencies) ===
FROM python:3.11-slim AS base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies first for better caching
COPY requirements.txt .

# Virtual environment (optional)
RUN python -m venv /venv

# Install dependencies
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# === DEVELOPMENT STAGE ===
FROM base AS dev

# Set environment variables for development
ENV FLASK_ENV=development
ENV FLASK_APP=app.py
ENV PATH="/venv/bin:$PATH"

# Copy all application code
COPY . .

# Expose Flask default port
EXPOSE 5000

# Command for local development (auto-reloading)
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

# === PRODUCTION STAGE ===
FROM base AS prod

# Set environment variables for production
ENV FLASK_ENV=production
ENV FLASK_APP=app.py
ENV PATH="/venv/bin:$PATH"

# Copy application code
COPY . .

# Expose Flask port (Render will set $PORT)
EXPOSE 5000

# Command for production using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
