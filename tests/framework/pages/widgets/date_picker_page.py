from typing import Self

import allure
from playwright.sync_api import Page

from tests.framework.pages.base_page import BasePage


class DatePickerPage(BasePage):
    URL = "/date-picker"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.date_input = page.locator("#datePickerMonthYearInput")

    @allure.step("Set date to '{date_str}'")
    def set_date(self, date_str: str) -> Self:
        """Set a new date. Expects MM/DD/YYYY format."""
        self.date_input.click()
        self.date_input.fill(date_str)
        self.page.keyboard.press("Escape")
        return self
