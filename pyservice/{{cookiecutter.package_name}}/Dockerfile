# Multi-stage build using uv for fast, reproducible installs.
# https://docs.astral.sh/uv/guides/integration/docker/
#
# The builder installs uv-managed Python into /python and copies it into the
# prod stage, so builder and prod run byte-identical Python. If you change the
# Python version, update it in both FROM lines AND the `uv python install` line.

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_INSTALL_DIR=/python \
    UV_PYTHON_PREFERENCE=only-managed

RUN uv python install 3.12

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev

COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev


FROM python:3.12-slim-bookworm AS prod

WORKDIR /app

COPY --from=builder /python /python
COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH" \
    VIRTUAL_ENV="/app/.venv"

ENTRYPOINT []

CMD ["python", "-m", "{{ cookiecutter.import_name }}"]
