# Project: python-playwright-ai

## Description

This project is a framework for UI test automation.
Utilizing modern approaches and libraries.

## Architecture

- Language: Python 3.14+
- Testing Framework: Pytest
- Automation Library: Playwright
- Pattern: Page Object Model (POM)
- Reporting: Allure
- Package Manager: uv

## Key Conventions

- Use Page Object Model for all UI interactions (see `tests/framework/pages/`)
- Type hints are required for all function signatures (including `-> None`)
- Fixtures should be defined in `tests/conftest.py`
- Use `sync_api` for Playwright operations
- Use `expect()` for all assertions (auto-retrying)

## Critical Rules

- NEVER commit secrets or `.env` files
- ALWAYS run `pytest` before declaring a task done
- Follow PEP 8 style guidelines
- Prefer explicit waits over hardcoded sleeps
- Use `ruff` for linting, `black` for formatting, `mypy` for type checking

## Testing Requirements

- All new features require corresponding E2E tests in `tests/tests/`
- Use the `page` fixture for browser context
- Run tests using: `pytest`
- Use `pytest.mark.parametrize` for data-driven tests

## Git Workflow

- Branch: `feature/short-description`
- Commits: Conventional Commits format (feat:, fix:, chore:)
- PR: Squash merge only

## Common Commands

- Install dependencies: `uv sync`
- Install Playwright browsers: `playwright install`
- Run all tests: `pytest`
- Run specific test file: `pytest tests/tests/test_filename.py`
- Run tests in headed mode: `pytest --headed`
- Run tests with filter: `pytest -k "test_name"`
- Run smoke tests: `pytest -m smoke`
- Generate Allure report: `allure serve allure-results`
