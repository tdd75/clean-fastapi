# Default target
.PHONY: all
all: setup dev db-upgrade db-seed

# ------------------------------------------------------------------------------
# Environment Setup
# ------------------------------------------------------------------------------

ifeq ($(OS),Windows_NT)
UV_INSTALL_CMD = curl -LsSf https://astral.sh/uv/install.ps1 | pwsh -c -
else
UV_INSTALL_CMD = curl -LsSf https://astral.sh/uv/install.sh | sh
endif

.PHONY: setup
setup:
	@if ! command -v uv >/dev/null 2>&1; then \
		$(UV_INSTALL_CMD); \
	fi
	uv sync --python 3.12
	uv tool install pre-commit && pre-commit install

# ------------------------------------------------------------------------------
# Development & Deployment
# ------------------------------------------------------------------------------

.PHONY: dev
dev:
	docker compose up --build -d

.PHONY: run
run:
	uv run uvicorn app.main:app --reload

.PHONY: deploy
deploy:
	docker compose --profile prod up --build

# ------------------------------------------------------------------------------
# Database Commands
# ------------------------------------------------------------------------------

.PHONY: db-revision
db-revision:
	uv run alembic revision --autogenerate -m "$(msg)"

.PHONY: db-upgrade
db-upgrade:
	uv run alembic upgrade head

.PHONY: db-downgrade
db-downgrade:
	uv run alembic downgrade -1

.PHONY: db-seed
db-seed:
ifeq ($(OS),Windows_NT)
	PYTHONPATH=. uv run python app/infrastructure/cmd/seed.py
else
	PYTHONPATH=. uv run python3 app/infrastructure/cmd/seed.py
endif

# ------------------------------------------------------------------------------
# Testing
# ------------------------------------------------------------------------------

.PHONY: test
test:
	uv run pytest -n 4

.PHONY: test-coverage
test-coverage:
	uv run pytest -n 4 --cov
	uv run coverage report --fail-under=85
