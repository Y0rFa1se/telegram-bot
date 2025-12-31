FROM ghcr.io/astral-sh/uv:alpine AS builder
WORKDIR /app
COPY pyproject.toml uv.lock .python-version ./

RUN uv sync --frozen --no-dev --no-install-project


FROM gcr.io/distroless/python3-debian12
WORKDIR /app

COPY --from=builder /app/.venv/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
ENV PYTHONPATH="/usr/local/lib/python3.11/site-packages:/app"

COPY main.py .
COPY ./modules ./modules

ENTRYPOINT [ "/usr/bin/python3", "main.py" ]