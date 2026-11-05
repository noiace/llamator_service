# FROM python:3.12-slim

# WORKDIR /app

# COPY pyproject.toml uv.lock ./

# RUN pip install uv \
#     && uv sync --frozen --no-dev

# COPY app ./app

# WORKDIR /app/app

# EXPOSE 8000

# # CMD ["uv", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

RUN pip install uv \
    && uv sync --frozen --no-dev

COPY alembic.ini ./
COPY migrations ./migrations
COPY app ./app

WORKDIR /app/app

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
