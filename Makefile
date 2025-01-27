# Default target
.PHONY: all
all: setup local db-upgrade db-seed

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

.PHONY: docker
docker:
	docker compose up --build -d

.PHONY: dev
dev:
	make docker
	uv run uvicorn app.main:app --reload

.PHONY: prod
prod:
	make docker
	uv run gunicorn app.main:app --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker -w 8

.PHONY: deploy
deploy:
	docker compose --profile prod up --build

# ------------------------------------------------------------------------------
# Testing
# ------------------------------------------------------------------------------

.PHONY: test
test:
	uv run pytest -n 4

.PHONY: test-cov
test-cov:
	uv run pytest -n 4 --cov
	uv run coverage report --fail-under=85

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
# Localization
# ------------------------------------------------------------------------------

LOCALE_PATH = app/infrastructure/locale

.PHONY: translations-extract
translations-extract:
	uv run pybabel extract --keywords="gettext _ t" -o $(LOCALE_PATH)/messages.pot .

.PHONY: translations-init
translations-init:
	$(MAKE) translations-extract
	uv run pybabel init -i $(LOCALE_PATH)/messages.pot -d $(LOCALE_PATH) -l "$(lang)"

.PHONY: translations-update
translations-update:
	$(MAKE) translations-extract
	uv run pybabel update -i $(LOCALE_PATH)/messages.pot -d $(LOCALE_PATH)

.PHONY: translations-compile
translations-compile:
	uv run pybabel compile -d $(LOCALE_PATH)
