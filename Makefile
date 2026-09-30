# Recipes are POSIX sh. On Windows, use Git Bash's sh instead of cmd.exe.
ifeq ($(OS),Windows_NT)
SHELL := C:/PROGRA~1/Git/bin/sh.exe
endif

# Load .env for local commands when it exists (settings defaults match docker-compose).
ENV_FILE := $(if $(wildcard .env),--env-file ../.env,)
UV_RUN := cd backend && uv run $(ENV_FILE)

.PHONY: up down migrate run test lint fmt

up: ## Start Postgres and Redis
	docker compose up -d --wait db redis

down: ## Stop all services
	docker compose --profile api down

migrate: ## Apply migrations locally
	$(UV_RUN) python manage.py migrate

run: ## gunicorn (gthread) on :8000, in a container, same flags as prod
	docker compose --profile api up api

test: ## Run backend tests
	$(UV_RUN) pytest

lint: ## Lint and check formatting
	$(UV_RUN) ruff check .
	$(UV_RUN) ruff format --check .

fmt: ## Auto-fix lint and format
	$(UV_RUN) ruff check --fix .
	$(UV_RUN) ruff format .
