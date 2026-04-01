import allure
import pytest
from playwright.sync_api import expect

from tests.framework import BaseTest
from tests.framework.pages import CheckBoxPage, TextBoxPage


@allure.epic("DemoQA")
@allure.feature("Elements")
class TestElements(BaseTest):
    @pytest.mark.smoke
    @allure.story("Text Box")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Submit text box form and verify output")
    def test_text_box_form_submission(self) -> None:
        text_box = TextBoxPage(self.page).navigate(TextBoxPage.URL)

        text_box.fill_form(
            full_name="John Doe",
            email="john.doe@example.com",
            current_address="123 Main St",
        )
        text_box.submit()

        expect(text_box.output_name).to_contain_text("John Doe")
        expect(text_box.output_email).to_contain_text("john.doe@example.com")

    @pytest.mark.regression
    @allure.story("Check Box")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Expand tree and select Home checkbox")
    def test_check_box_expand_and_select_home(self) -> None:
        check_box = CheckBoxPage(self.page).navigate(CheckBoxPage.URL)

        check_box.expand_home()
        expect(check_box.desktop_node).to_be_visible()

        check_box.check_node("Home")
        expect(check_box.result).to_contain_text("home")
