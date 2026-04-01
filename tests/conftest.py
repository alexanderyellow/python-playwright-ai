import json
import sys
from collections.abc import Generator
from pathlib import Path
from typing import Any

import allure
import pytest
from faker import Faker
from playwright.sync_api import BrowserContext, Page
from pytest import Config, FixtureRequest, Parser

from tests.framework.config import PlaywrightConfig


def pytest_addoption(parser: Parser) -> None:
    parser.addini("pw_browser", "Playwright browser")
    parser.addini("pw_headless", "Playwright headless mode")
    parser.addini("pw_base_url", "Base URL for the application")
    parser.addini("pw_browser_channel", "Browser channel")
    parser.addini("pw_tracing", "Playwright tracing")
    parser.addini("pw_screenshot", "Playwright screenshot")
    parser.addini("pw_video", "Playwright video")
    parser.addini("pw_slowmo", "Playwright slowmo")
    parser.addini("pw_viewport_width", "Viewport width")
    parser.addini("pw_viewport_height", "Viewport height")
    parser.addini("pw_timeout", "Playwright timeout")
    parser.addini("pw_output_dir", "Playwright output dir")
    parser.addini("pw_full_page_screenshot", "Full page screenshot")
    parser.addini("pw_fullscreen", "Full screen mode")


def pytest_configure(config: Config) -> None:
    # Build our custom config and store it on the pytest config object
    pw_config = PlaywrightConfig.from_pytest(config)
    config.pw_config = pw_config  # type: ignore[attr-defined]

    # Inject into pytest-playwright so its fixtures work automatically
    config.option.browser = [pw_config.browser]
    config.option.headed = not pw_config.headless
    config.option.browser_channel = pw_config.browser_channel
    config.option.tracing = pw_config.tracing
    config.option.screenshot = pw_config.screenshot
    config.option.video = pw_config.video
    config.option.output = pw_config.output_dir
    config.option.full_page_screenshot = pw_config.full_page_screenshot


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    allure_dir = session.config.getoption("--alluredir", default=None)
    if not allure_dir:
        return

    allure_path = Path(allure_dir)
    allure_path.mkdir(parents=True, exist_ok=True)

    pw_config: PlaywrightConfig = session.config.pw_config  # type: ignore[attr-defined]

    # Write environment.properties for Allure report
    env_file = allure_path / "environment.properties"
    env_file.write_text(
        f"Base.URL={pw_config.base_url}\n"
        f"Browser={pw_config.browser}\n"
        f"Headless={pw_config.headless}\n"
        f"Viewport={pw_config.viewport_width}x{pw_config.viewport_height}\n"
        f"Timeout={pw_config.timeout}ms\n"
        f"Python={sys.version.split()[0]}\n"
        f"pytest={pytest.__version__}\n"
    )

    # Write categories.json for defect classification
    categories_file = allure_path / "categories.json"
    categories_file.write_text(
        json.dumps(
            [
                {
                    "name": "Element Interaction Failures",
                    "matchedStatuses": ["broken"],
                    "messageRegex": ".*TimeoutError.*",
                },
                {
                    "name": "Assertion Failures",
                    "matchedStatuses": ["failed"],
                    "messageRegex": ".*AssertionError.*",
                },
                {
                    "name": "Infrastructure Issues",
                    "matchedStatuses": ["broken"],
                    "messageRegex": ".*ConnectionError.*|.*net::ERR.*",
                },
            ],
            indent=2,
        )
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item) -> Generator[None, Any, None]:
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or report.passed:
        return

    # Attach screenshot on failure if available
    page: Page | None = item.funcargs.get("page")  # type: ignore[attr-defined]
    if page and not page.is_closed():
        screenshot = page.screenshot(full_page=False)
        allure.attach(
            screenshot,
            name="failure-screenshot",
            attachment_type=allure.attachment_type.PNG,
        )


@pytest.fixture(scope="session")
def fake() -> Faker:
    return Faker()


@pytest.fixture(scope="session")
def pw_config(request: FixtureRequest) -> PlaywrightConfig:
    return request.config.pw_config  # type: ignore[attr-defined,no-any-return]


@pytest.fixture(scope="session")
def browser_type_launch_args(
    browser_type_launch_args: dict[str, Any], pw_config: PlaywrightConfig
) -> dict[str, Any]:
    args = {**browser_type_launch_args}
    args["headless"] = pw_config.headless
    if pw_config.browser_channel:
        args["channel"] = pw_config.browser_channel
    if pw_config.slowmo > 0:
        args["slow_mo"] = pw_config.slowmo
    if pw_config.fullscreen:
        # Pass start-maximized arg to browser launch
        # Note: --start-maximized primarily works on Chromium,
        # but is safe to inject as it might be ignored or handled by others
        args["args"] = args.get("args", []) + ["--start-maximized"]
    return args


@pytest.fixture(scope="session")
def browser_context_args(
    browser_context_args: dict[str, Any], pw_config: PlaywrightConfig
) -> dict[str, Any]:
    args = {**browser_context_args}
    if pw_config.base_url:
        args["base_url"] = pw_config.base_url

    if pw_config.fullscreen:
        args["no_viewport"] = True
    else:
        args["viewport"] = {
            "width": pw_config.viewport_width,
            "height": pw_config.viewport_height,
        }
    return args


@pytest.fixture
def context(new_context: Any, pw_config: PlaywrightConfig) -> BrowserContext:
    ctx: BrowserContext = new_context()
    ctx.set_default_timeout(pw_config.timeout)
    ctx.set_default_navigation_timeout(pw_config.timeout)
    return ctx


@pytest.fixture
def page(page: Page, pw_config: PlaywrightConfig) -> Generator[Page, None, None]:
    # Hide the fixed bottom ad banner that can intercept clicks on demoqa.com
    page.add_init_script("""
        const observer = new MutationObserver(() => {
            const ban = document.getElementById('fixedban');
            if (ban) ban.style.display = 'none';
        });
        observer.observe(document.documentElement, {childList: true, subtree: true});
    """)

    yield page
