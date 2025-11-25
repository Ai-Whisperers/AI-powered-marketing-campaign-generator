FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY code/ ./code/
COPY alembic/ ./alembic/
COPY alembic.ini .

# Create data directories
RUN mkdir -p /app/data/projects /app/logs

# Create non-root user
RUN useradd -m -u 1000 maga && \
    chown -R maga:maga /app

USER maga

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run migrations and start server
CMD alembic upgrade head && \
    uvicorn code.api.main:app --host 0.0.0.0 --port 8000 --workers 4
