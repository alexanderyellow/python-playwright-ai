import allure
import pytest
from playwright.sync_api import expect

from tests.framework import BaseTest
from tests.framework.pages import PracticeFormPage


@allure.epic("DemoQA")
@allure.feature("Forms")
class TestPracticeForm(BaseTest):
    @pytest.mark.smoke
    @allure.story("Practice Form")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Submit form with minimum required fields")
    def test_minimum_submission(self) -> None:
        form = PracticeFormPage(self.page).navigate(PracticeFormPage.URL)

        form.fill_first_name("John")
        form.fill_last_name("Doe")
        form.select_gender("Male")
        form.fill_mobile("1234567890")
        form.submit()

        expect(form.modal_title).to_have_text("Thanks for submitting the form")

    @pytest.mark.regression
    @pytest.mark.parametrize(
        ("first_name", "last_name", "email", "gender", "mobile"),
        [
            ("Jane", "Smith", "jane.smith@example.com", "Female", "0987654321"),
            ("Alex", "Johnson", "alex.j@example.com", "Other", "5551234567"),
        ],
        ids=["female-user", "other-gender-user"],
    )
    @allure.story("Practice Form")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify submitted data appears in confirmation modal")
    def test_data_in_confirmation(
        self,
        first_name: str,
        last_name: str,
        email: str,
        gender: str,
        mobile: str,
    ) -> None:
        form = PracticeFormPage(self.page).navigate(PracticeFormPage.URL)

        form.fill_first_name(first_name)
        form.fill_last_name(last_name)
        form.fill_email(email)
        form.select_gender(gender)
        form.fill_mobile(mobile)
        form.submit()

        expect(form.modal_table).to_contain_text(f"{first_name} {last_name}")
        expect(form.modal_table).to_contain_text(email)
