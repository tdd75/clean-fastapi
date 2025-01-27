FROM python:3.12

WORKDIR /code

# Install uv
RUN pip install --no-cache-dir uv

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --locked

# Copy application code
COPY app ./app
COPY tests ./tests

# Copy configuration files
COPY Makefile ./
COPY alembic.ini ./
COPY migration ./migration
