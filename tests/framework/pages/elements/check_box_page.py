from typing import Self

import allure
from playwright.sync_api import Page

from tests.framework.pages.base_page import BasePage


class CheckBoxPage(BasePage):
    URL = "/checkbox"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.home_toggle = page.locator("span.rc-tree-switcher").first
        self.desktop_node = page.get_by_text("Desktop")
        self.result = page.locator("#result")

    @allure.step("Expand Home checkbox tree")
    def expand_home(self) -> Self:
        self.home_toggle.click()
        return self

    @allure.step("Check node '{name}'")
    def check_node(self, name: str) -> Self:
        node = self.page.locator(".rc-tree-treenode", has_text=name)
        node.locator("span.rc-tree-checkbox").click()
        return self
