# Stage 1: build dependencies
FROM python:3.13-slim AS builder
WORKDIR /build

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Stage 2: runtime
FROM python:3.13-slim AS runtime
WORKDIR /app

COPY --from=builder /build/.venv /app/.venv
COPY src/ ./src/

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

EXPOSE 8080

CMD ["python", "-m", "babubi_mcp"]
