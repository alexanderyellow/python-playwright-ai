from typing import Self

import allure
from playwright.sync_api import Page

from tests.framework.pages.base_page import BasePage


class DroppablePage(BasePage):
    URL = "/droppable"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._simple_tab = page.get_by_role("tabpanel", name="Simple")
        self.draggable = page.locator("#draggable")
        self.drop_zone = self._simple_tab.locator("#droppable")
        self.drop_zone_text = self._simple_tab.locator("#droppable p")

    @allure.step("Drag element to drop zone")
    def drag_to_drop_zone(self) -> Self:
        self.draggable.drag_to(self.drop_zone)
        return self
