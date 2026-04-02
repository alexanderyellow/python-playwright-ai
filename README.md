# Python Playwright AI

UI test automation framework built with **Python 3.14+**, **Playwright**, **Pytest**, and **Allure**.

Targets [DemoQA](https://demoqa.com/) using the Page Object Model pattern with strongly-typed configuration and modern
tooling.

## Features

- **Page Object Model** -- all UI interactions abstracted into page objects with method chaining (`Self` return types)
- **Allure Reporting** -- epics, features, stories, severity levels, step-level tracing, failure screenshots,
  environment metadata
- **Pydantic Settings** -- typed configuration with validation, env var overrides (`PW_*`), `.env` file support
- **Parallel Execution** -- pytest-xdist with configurable thread count (`PW_THREADS`)
- **Pytest Markers** -- `smoke` for critical path, `regression` for full suite, `parametrize` for data-driven tests
- **Faker** -- dynamic test data generation via session-scoped fixture
- **Playwright** -- auto-waiting, tracing, screenshots, and video on failure
- **Code Quality** -- Ruff (linting + import sorting), Black (formatting), Mypy (type checking)

## Project Structure

```
tests/
  conftest.py                         # Fixtures, Playwright config, Allure hooks
  framework/
    base_test.py                      # BaseTest class (injects page fixture)
    config/
      settings.py                     # PlaywrightConfig (pydantic-settings)
    pages/
      base_page.py                    # BasePage with navigate() and @allure.step
      alerts_frames_windows/
        alerts_page.py                # AlertsPage
        modal_dialogs_page.py         # ModalDialogsPage
      book_store/
        book_store_page.py            # BookStorePage
        login_page.py                 # BookStoreLoginPage
      elements/
        check_box_page.py             # CheckBoxPage
        text_box_page.py              # TextBoxPage
      forms/
        practice_form_page.py         # PracticeFormPage
      interactions/
        droppable_page.py             # DroppablePage
        selectable_page.py            # SelectablePage
      widgets/
        date_picker_page.py           # DatePickerPage
        slider_page.py                # SliderPage
  tests/
    test_alerts_frames_windows.py     # Alerts and modal dialog tests
    test_book_store.py                # Login and book search tests
    test_elements.py                  # Text box and checkbox tests
    test_forms.py                     # Practice form tests (parametrized)
    test_interactions.py              # Drag-and-drop and selectable tests
    test_widgets.py                   # Date picker and slider tests
```

## Setup

Requires [uv](https://github.com/astral-sh/uv) as the package manager.

```bash
# Install uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Install Playwright browsers
uv run playwright install chromium
```

## Configuration

Managed via `PlaywrightConfig` in `tests/framework/config/settings.py` using `pydantic-settings`.

**Priority order:** OS env variables (`PW_*`) > `.env` file > `pyproject.toml` > defaults.

| Variable             | Default              | Description                                      |
|----------------------|----------------------|--------------------------------------------------|
| `PW_BROWSER`         | `chromium`           | Browser engine (`chromium`, `firefox`, `webkit`) |
| `PW_HEADLESS`        | `true`               | Run in headless mode                             |
| `PW_BASE_URL`        | `https://demoqa.com` | Base URL for all tests                           |
| `PW_TIMEOUT`         | `30000`              | Default timeout in milliseconds                  |
| `PW_VIEWPORT_WIDTH`  | `1280`               | Browser viewport width (320-3840)                |
| `PW_VIEWPORT_HEIGHT` | `720`                | Browser viewport height (240-2160)               |
| `PW_SLOWMO`          | `0`                  | Slow down actions by ms                          |
| `PW_TRACING`         | `retain-on-failure`  | Playwright tracing mode                          |
| `PW_SCREENSHOT`      | `only-on-failure`    | Screenshot capture mode                          |
| `PW_VIDEO`           | `retain-on-failure`  | Video recording mode                             |
| `PW_OUTPUT_DIR`      | `test-results`       | Output directory for artifacts                   |
| `PW_FULLSCREEN`      | `false`              | Run in fullscreen mode                           |
| `PW_THREADS`         | `3`                  | Number of parallel xdist workers (0 to disable)  |

Override via environment:

```bash
PW_HEADLESS=false PW_BROWSER=firefox uv run pytest
```

## Running Tests

```bash
# Run all tests (3 parallel workers by default)
uv run pytest

# Run smoke tests only
uv run pytest -m smoke

# Run regression suite
uv run pytest -m regression

# Run specific test file
uv run pytest tests/tests/test_elements.py

# Run by keyword
uv run pytest -k "test_search"

# Run headed (visible browser) with 3 parallel workers
PW_HEADLESS=false uv run pytest -n=3

# Run with custom number of parallel workers
PW_THREADS=5 uv run pytest

# Run sequentially (disable parallel execution)
uv run pytest -n=0
```

## Allure Reports

Allure results are generated automatically in `allure-results/` on every test run.

View the report:

```bash
allure serve allure-results
```

The report includes:

- **Epic/Feature/Story** hierarchy matching the DemoQA application structure
- **Severity levels** (CRITICAL, NORMAL) on each test
- **Step-level tracing** from page object `@allure.step()` decorators
- **Failure screenshots** attached automatically
- **Environment metadata** (browser, base URL, Python version, viewport)
- **Defect categories** (element interaction failures, assertion failures, infrastructure issues)

## CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push and PR to `main`:

1. **Lint & Type Check** -- Ruff, Black, Mypy
2. **Tests** -- parallel matrix across Chromium and Firefox
3. **Allure Report** -- generated and deployed to GitHub Pages (main branch only)

Test artifacts (screenshots, traces, videos) are uploaded on failure. Allure results are uploaded for all runs.

## Claude Code Integration

`claude.yml` implements a two-phase AI-assisted workflow via [Claude Code Action](https://github.com/anthropics/claude-code-action):

**Phase 1 — Analyze** (read-only)

Triggered automatically on PRs, or when a PR review or issue body contains `@claude`. Claude reads the diff or issue, identifies problems and improvements, and posts a summary comment ending with:
> "Reply `@claude apply` to approve and apply these changes."

**Phase 2 — Apply**

Triggered when `@claude` appears in an issue comment or PR review comment. Claude applies the proposed changes directly to the branch.

Both phases use `claude-sonnet-4-6` with up to 25 turns.

## Code Quality

```bash
# Lint
uv run ruff check tests/

# Format
uv run black tests/

# Type check
uv run mypy tests/
```
