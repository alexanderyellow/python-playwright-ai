from typing import Self

import allure
from playwright.sync_api import Page

from tests.framework.pages.base_page import BasePage


class BookStorePage(BasePage):
    URL = "/books"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.search_input = page.get_by_placeholder("Type to search")
        self.book_titles = page.locator(".action-buttons a")

    @allure.step("Search for '{query}'")
    def search(self, query: str) -> Self:
        self.search_input.fill(query)
        return self
