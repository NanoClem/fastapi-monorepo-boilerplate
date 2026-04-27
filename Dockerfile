ARG PYTHON_VERSION=3.13
ARG UV_VERSION=0.11.7

FROM ghcr.io/astral-sh/uv:${UV_VERSION}-python${PYTHON_VERSION}-trixie-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /workspace

# Install dependencies first to leverage Docker cache.
# Skipped if uv.lock and pyproject.toml have not changed.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-workspace --package backend

COPY . .

# Install the project itself. 
# Skipped if source code has not changed.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package=backend

FROM python:${PYTHON_VERSION}-slim-trixie
# It is important to use the image that matches the builder, as the path to the
# Python executable must be the same, e.g., using `python:3.11-slim-bookworm`
# will fail.

ARG PORT=8000
ENV PORT=$PORT

# Setup a non-root user
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

# Add curl for health checks
RUN apt-get update && apt-get install -y curl

COPY --from=builder --chown=nonroot:nonroot /workspace /workspace

# Activate virtual environment by default when the container starts
ENV PATH="/workspace/.venv/bin:$PATH"

USER nonroot

WORKDIR /workspace

EXPOSE $PORT

CMD ["sh", "-c", "fastapi run --host 0.0.0.0 --port $PORT apps/backend/src/backend/main.py"]
