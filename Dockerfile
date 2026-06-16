# =========================
# Base stage (shared)
# =========================
FROM python:3.13-slim AS base

ENV PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /code

RUN apt-get update && apt-get install -y \
    gettext \
    curl \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install poetry

COPY pyproject.toml poetry.lock ./



# =========================
# Development stage
# =========================
FROM base AS development

# Install ALL dependencies (including dev + test)
RUN poetry install --no-root

# Install Playwright browsers + system deps
RUN poetry run playwright install --with-deps

COPY start-django.sh /code/start-django.sh
RUN chmod +x /code/start-django.sh

COPY . .

EXPOSE 8000

ENTRYPOINT ["/code/start-django.sh"]


# =========================
# Production stage
# =========================
FROM base AS production

# Install ONLY production dependencies
RUN poetry install --no-root --only main

COPY start-django.sh /code/start-django.sh
RUN chmod +x /code/start-django.sh

COPY . .

EXPOSE 8000

ENV ENV_STATE=production

ENTRYPOINT ["/code/start-django.sh"]
