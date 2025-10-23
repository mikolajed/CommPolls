# ---- Builder Stage ----
FROM python:3.12-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Build dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# ---- Runtime Stage ----
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install runtime dependencies (Postgres client, libraries)
RUN apt-get update && \
    apt-get install -y libpq-dev postgresql-client --no-install-recommends && \
    apt-get clean && \
    mkdir -p /app/staticfiles /app/media && \
    groupadd --system app && useradd --system --gid app app && \
    chown -R app:app /app/staticfiles /app/media /app

# Copy pre-built wheels
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy source code
COPY . .

# Switch to non-root user
USER app

EXPOSE 8000

# Wait for DB, migrate, collect static, run Gunicorn
CMD ["sh", "-c", "./wait_for_db.sh db python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --reload"]
