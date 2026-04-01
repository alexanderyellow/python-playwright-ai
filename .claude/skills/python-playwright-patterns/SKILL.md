---
name: python-playwright-patterns
description: Playwright web test automation best practices and patterns for building robust, efficient, and maintainable Python test frameworks.
---

# Python Playwright Web Test Automation

Idiomatic Playwright web test automation best practices and patterns for building robust, efficient, and maintainable
Python test frameworks.

## Activation Triggers

Activate this skill and strictly adhere to the following guidelines when prompted with any of the following tasks:

* Writing new Web tests
* Reviewing Web test code
* Refactoring existing Web test code
* Designing Web test architecture
* Debugging Playwright Python scripts

## Core Architectural Directives

When generating, refactoring, or reviewing code, you **MUST** strictly adhere to the following structural rules. There
are no exceptions.

1. **Page Object Model (POM):** All web interactions **MUST** be abstracted into Page Object classes. Tests should never
   contain raw Playwright locators or actions (e.g., `page.click()`).
2. **The `BaseTest` Contract:** Every single test class **MUST** inherit from a `BaseTest` class. This base class
   handles driver instantiation, setup, and teardown.
3. **Class-Bound Code:** **ALL** code **MUST** be wrapped in classes. Do not generate floating/module-level functions.
   Tests **MUST** be methods inside a test class, and page actions **MUST** be methods inside a page class.
   The file **MUST** contain only one class

## Framework Concepts & Best Practices

### 1. Locators & Interactions

* **User-Facing Locators:** Prioritize locators in the following order: `get_by_role`, `get_by_label`,
  `get_by_placeholder`, `get_by_text`, `get_by_alt_text`, `get_by_title`, `get_by_test_id`,
  and finally `locator` (XPath or CSS selectors) as a last resort.
  This ensures tests simulate actual user behavior and are more resilient to DOM changes.
* **Encapsulation:** Locators must be defined as class properties or initialized in the `__init__` method of the Page
  Object.
* **Chaining:** Return `self` in Page Object methods where appropriate to allow method chaining (fluent interface) for
  consecutive actions on the same page.

### 2. Assertions & Auto-Waiting

* **Use `expect`:** Always use Playwright's `expect()` for assertions. It features built-in auto-retries which
  eliminates the need for hardcoded `time.sleep()`.
* **Avoid Explicit Waits:** Rely on Playwright's actionability checks (auto-waiting). Only use
  `page.wait_for_selector()` or `page.wait_for_load_state()` in exceptional cases where the framework's auto-wait fails.

### 3. State Management & Data

* **Isolation:** Tests must be completely independent. Do not rely on state from previous tests.
* **Environment Variables:** Never hardcode URLs, credentials, or sensitive data. Use `os.environ` or a configuration
  class.

### 4. Pytest Configuration & Execution Strategy

When generating or modifying Pytest configuration files (`pytest.ini`, `conftest.py`) or test execution scripts, you
must strictly enforce the following framework standards:

* **Plugin Reliance:** The framework heavily relies on the `pytest-playwright` plugin. Do not manually instantiate
  Playwright sync/async APIs (e.g., `sync_playwright().start()`) in standard test flows. Rely on the plugin's built-in
  fixtures (`page`, `context`, `browser`).
* **The `conftest.py` Boundary:** `conftest.py` is reserved strictly for global hooks (e.g.,
  `pytest_runtest_makereport` for attaching screenshots on failure), custom CLI arguments, and global environment setup.
    * Do **NOT** put page object initializations or test-specific setup routines in `conftest.py`. Those belong in
      `BaseTest` or the individual test classes.
* **Fixture Scoping:** Be explicit about fixture scopes. Use `scope="session"` for expensive setups (like environment
  provisioning) and `scope="function"` for isolated state (like the `page` fixture, which is function-scoped by default
  in Playwright).
* **Execution Flags:** When providing commands to run tests, default to utilizing `pytest-playwright` CLI flags for
  cross-browser testing and debugging, such as `--browser=chromium --browser=firefox`, `--headed`, and
  `--tracing=retain-on-failure`.

## Post-Refactoring

**DO NOT** run tests after refactoring code. The responsibility for test execution and validation lies with the user.

## Configuration File Templates

### 1. `pytest.ini` Example

Always enforce strict marker definitions and default CLI behaviors to ensure consistent test execution.

```ini
[pytest]
addopts =
    --browser=chromium
    --tracing=retain-on-failure
    --screenshot=only-on-failure
    --video=retain-on-failure
    -v
    --tb=short
markers =
    smoke: Quick, critical path tests
    regression: Comprehensive suite
    api: Tests that interact directly with the backend
testpaths = tests
```

### 2. API Interception & Mocking (Network Control)

When tests require specific data states without relying on a live backend, use Playwright’s `page.route` within the Page
Object Model. This ensures that mocking logic is reusable and encapsulated.

* **Encapsulation:** Mocking logic must live inside Page Object methods (e.g., `mock_empty_results()`) or a dedicated
  `MockManager` class. Never define `page.route` directly inside a test method.
* **Early Activation:** Mocking routes must be defined **before** the action that triggers the network request (e.g.,
  before clicking a "Search" button or calling `page.goto`).
* **Fulfillment Strategy:** Use `route.fulfill()` to provide custom JSON bodies, status codes, or headers.

#### Mocking Template (Page Object Integration)

```python
import json
from playwright.sync_api import Page, Route


class SearchPage:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = page.get_by_placeholder("Search products...")
        self.results_container = page.locator(".results-list")

    def mock_search_results(self, mock_data: list) -> None:
        """
        Intercepts the search API call and returns custom mock data.
        """

        def handle_route(route: Route):
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps({"items": mock_data})
            )

        # Intercept specific API glob pattern or regex
        self.page.route("**/api/v1/search*", handle_route)

    def search_for(self, term: str) -> 'SearchPage':
        self.search_input.fill(term)
        self.search_input.press("Enter")
        return self
```

---

## Code Generation Templates

When asked to write code, use the following structural templates.

### 1. Page Object Example

```python
from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_label("Username")
        self.password_input = page.get_by_label("Password")
        self.login_button = page.get_by_role("button", name="Log in")
        self.error_message = page.locator(".error-message")

    def navigate(self, url: str) -> 'LoginPage':
        self.page.goto(url)
        return self

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def verify_error_message_is_visible(self) -> None:
        expect(self.error_message).to_be_visible()
```

### 2. Test Structure Example

```python
from playwright.sync_api import Page, expect

from tests.framework.pages import LoginPage


def test_successful_login_redirects_to_dashboard(page: Page) -> None:
    login_page = LoginPage(page)
    login_page.navigate("/login")

    login_page.login("valid_user", "valid_pass")

    expect(page).to_have_url("/dashboard")


def test_invalid_login_shows_error(page: Page) -> None:
    login_page = LoginPage(page)
    login_page.navigate("/login")

    login_page.login("invalid_user", "wrong_pass")

    login_page.verify_error_message_is_visible()
```

### 3. Conftest Template

```python
from collections.abc import Generator

import pytest
from playwright.sync_api import Page


@pytest.fixture
def page(page: Page) -> Generator[Page, None, None]:
    """Override the default page fixture with custom setup."""
    page.add_init_script("""
        // Custom initialization scripts (e.g., hide banners)
    """)
    yield page
```

### 4. Debugging Patterns

* **Trace Viewer:** Use `--tracing=retain-on-failure` to capture trace files for failed tests.
  Run `playwright show-trace trace.zip` to inspect.
* **Screenshots:** Use `--screenshot=only-on-failure` for automatic failure screenshots.
* **Headed Mode:** Use `--headed` to watch test execution in a visible browser.
* **Pause:** Insert `page.pause()` in test code to open Playwright Inspector for step-by-step debugging.
* **Slow Motion:** Use `--slowmo=500` to slow down interactions for visual debugging.

## Quick Reference

| Pattern                                | When to Use                               |
|----------------------------------------|-------------------------------------------|
| `page.get_by_role(role)`               | Accessible role-based locator (preferred) |
| `page.get_by_label(label)`             | Form label locator                        |
| `page.get_by_placeholder(text)`        | Placeholder text locator                  |
| `page.get_by_text(text)`               | Text content locator                      |
| `page.get_by_alt_text(text)`           | Image alt text locator                    |
| `page.get_by_title(text)`              | Title attribute locator                   |
| `page.get_by_test_id(test_id)`         | `data-testid` attribute locator           |
| `page.locator(selector)`               | CSS/XPath locator (last resort)           |
| `expect(locator).to_be_visible()`      | Assert visibility                         |
| `expect(locator).to_have_text(text)`   | Assert text content                       |
| `expect(page).to_have_url(url)`        | Assert navigation                         |
| `page.route(pattern, handler)`         | Intercept network requests                |
| `locator.scroll_into_view_if_needed()` | Scroll before interaction                 |
