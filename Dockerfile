# ---- Builder Stage ----
# This stage installs dependencies, including build-time tools.
FROM python:3.12-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install build-time dependencies needed for psycopg2
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


# ---- Runtime Stage ----
# This is the final, lean image for production.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install runtime dependencies for PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev --no-install-recommends && apt-get clean

# Copy pre-built wheels from the builder stage and install them
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy the application code
COPY . .

# Create a non-root user to run the application for better security
RUN addgroup --system app && adduser --system --group app
USER app

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
