ARG UV_VERSION=0.9.25

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv-repo
FROM python:3.12 AS builder

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_NO_EDITABLE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_FROZEN=1 \
    UV_CACHE_DIR=/tmp/uv_cache

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:/root/.local/bin/:$PATH"

WORKDIR /app

RUN python -m venv "$VIRTUAL_ENV"

COPY --from=uv-repo /uv /usr/bin/uv
COPY pyproject.toml uv.lock ./


RUN --mount=type=cache,target=$UV_CACHE_DIR \
    uv sync --active

FROM python:3.12-slim AS runtime

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV

WORKDIR /opi-api

COPY app ./app
