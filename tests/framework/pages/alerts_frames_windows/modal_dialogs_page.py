from typing import Self

import allure
from playwright.sync_api import Page

from tests.framework.pages.base_page import BasePage


class ModalDialogsPage(BasePage):
    URL = "/modal-dialogs"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.small_modal_button = page.locator("#showSmallModal")
        self.large_modal_button = page.locator("#showLargeModal")
        self.modal_title = page.locator(".modal-title")
        self.modal_body = page.locator(".modal-body")
        self.close_small_modal_button = page.locator("#closeSmallModal")
        self.close_large_modal_button = page.locator("#closeLargeModal")

    @allure.step("Open small modal dialog")
    def open_small_modal(self) -> Self:
        self.small_modal_button.click()
        return self

    @allure.step("Open large modal dialog")
    def open_large_modal(self) -> Self:
        self.large_modal_button.click()
        return self

    @allure.step("Close small modal dialog")
    def close_small_modal(self) -> Self:
        self.close_small_modal_button.click()
        return self

    @allure.step("Close large modal dialog")
    def close_large_modal(self) -> Self:
        self.close_large_modal_button.click()
        return self
