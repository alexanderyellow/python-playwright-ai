from typing import Self

import allure
from playwright.sync_api import Page

from tests.framework.pages.base_page import BasePage


class BookStoreLoginPage(BasePage):
    URL = "/login"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input = page.get_by_placeholder("UserName")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")

    @allure.step("Login with username={username}")
    def login(self, username: str, password: str) -> Self:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        return self
