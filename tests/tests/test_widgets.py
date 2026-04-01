import allure
import pytest
from playwright.sync_api import expect

from tests.framework import BaseTest
from tests.framework.pages import DatePickerPage, SliderPage


@allure.epic("DemoQA")
@allure.feature("Widgets")
class TestWidgets(BaseTest):
    @pytest.mark.regression
    @allure.story("Date Picker")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Set a new date in the date picker")
    def test_date_picker_accepts_new_date(self) -> None:
        date_picker = DatePickerPage(self.page).navigate(DatePickerPage.URL)

        date_picker.set_date("01/15/2024")

        expect(date_picker.date_input).to_have_value("01/15/2024")

    @pytest.mark.regression
    @allure.story("Slider")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Slider updates value display")
    def test_slider_updates_value_display(self) -> None:
        slider_page = SliderPage(self.page).navigate(SliderPage.URL)

        slider_page.set_value(75)

        expect(slider_page.value_display).to_have_value("75")
