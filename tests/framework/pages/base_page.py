from typing import Self

import allure
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    @allure.step("Navigate to {url}")
    def navigate(self, url: str) -> Self:
        self.page.goto(url, wait_until="domcontentloaded")
        return self

    @allure.step("Get page title")
    def title(self) -> str:
        return self.page.title()
