from typing import Self

import allure
from playwright.sync_api import Page

from tests.framework.pages.base_page import BasePage


class SelectablePage(BasePage):
    URL = "/selectable"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.list_items = page.locator("#demo-tabpane-list .list-group-item")
        self.active_items = page.locator("#demo-tabpane-list .list-group-item.active")

    @allure.step("Select item at index {index}")
    def select_item(self, index: int) -> Self:
        self.list_items.nth(index).click()
        return self
