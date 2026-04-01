from typing import Self

import allure
from playwright.sync_api import Page

from tests.framework.pages.base_page import BasePage


class TextBoxPage(BasePage):
    URL = "/text-box"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.full_name_input = page.get_by_placeholder("Full Name")
        self.email_input = page.get_by_placeholder("name@example.com")
        self.current_address_input = page.get_by_placeholder("Current Address")
        self.permanent_address_input = page.locator("#permanentAddress")
        self.submit_button = page.get_by_role("button", name="Submit")
        self.output_name = page.locator("#name")
        self.output_email = page.locator("#email")

    @allure.step("Fill text box form: name={full_name}, email={email}")
    def fill_form(
        self,
        full_name: str,
        email: str,
        current_address: str = "",
        permanent_address: str = "",
    ) -> Self:
        self.full_name_input.fill(full_name)
        self.email_input.fill(email)
        if current_address:
            self.current_address_input.fill(current_address)
        if permanent_address:
            self.permanent_address_input.fill(permanent_address)
        return self

    @allure.step("Submit text box form")
    def submit(self) -> Self:
        self.submit_button.scroll_into_view_if_needed()
        self.submit_button.click()
        return self
