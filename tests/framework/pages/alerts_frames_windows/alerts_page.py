from typing import Self

import allure
from playwright.sync_api import Page

from tests.framework.pages.base_page import BasePage


class AlertsPage(BasePage):
    URL = "/alerts"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.alert_button = page.get_by_role("button", name="Click me").first
        self.confirm_button = page.locator("#confirmButton")
        self.prompt_button = page.locator("#promtButton")
        self.confirm_result = page.locator("#confirmResult")
        self.prompt_result = page.locator("#promptResult")

    @allure.step("Click alert button")
    def click_alert(self) -> Self:
        self.alert_button.click()
        return self

    @allure.step("Click confirm button")
    def click_confirm(self) -> Self:
        self.confirm_button.click()
        return self

    @allure.step("Click prompt button")
    def click_prompt(self) -> Self:
        self.prompt_button.click()
        return self
