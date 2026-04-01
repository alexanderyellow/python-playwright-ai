from typing import ClassVar, Self

import allure
from playwright.sync_api import Page

from tests.framework.pages.base_page import BasePage


class PracticeFormPage(BasePage):
    URL = "/automation-practice-form"

    GENDER_LABEL_FOR: ClassVar[dict[str, str]] = {
        "Male": "gender-radio-1",
        "Female": "gender-radio-2",
        "Other": "gender-radio-3",
    }

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.first_name_input = page.get_by_placeholder("First Name")
        self.last_name_input = page.get_by_placeholder("Last Name")
        self.email_input = page.get_by_placeholder("name@example.com")
        self.mobile_input = page.get_by_placeholder("Mobile Number")
        self.submit_button = page.get_by_role("button", name="Submit")
        self.confirmation_modal = page.locator(".modal-content")
        self.modal_title = page.locator(".modal-title")
        self.modal_table = page.locator("table.table-dark")

    @allure.step("Fill first name: {name}")
    def fill_first_name(self, name: str) -> Self:
        self.first_name_input.fill(name)
        return self

    @allure.step("Fill last name: {name}")
    def fill_last_name(self, name: str) -> Self:
        self.last_name_input.fill(name)
        return self

    @allure.step("Fill email: {email}")
    def fill_email(self, email: str) -> Self:
        self.email_input.fill(email)
        return self

    @allure.step("Fill mobile: {mobile}")
    def fill_mobile(self, mobile: str) -> Self:
        self.mobile_input.fill(mobile)
        return self

    @allure.step("Select gender: {gender}")
    def select_gender(self, gender: str) -> Self:
        label_for = self.GENDER_LABEL_FOR[gender]
        self.page.locator(f"label[for='{label_for}']").click()
        return self

    @allure.step("Submit practice form")
    def submit(self) -> Self:
        self.submit_button.scroll_into_view_if_needed()
        self.submit_button.click()
        return self
