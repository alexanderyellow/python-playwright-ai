import allure
import pytest
from playwright.sync_api import expect

from tests.framework import BaseTest
from tests.framework.pages import DroppablePage, SelectablePage


@allure.epic("DemoQA")
@allure.feature("Interactions")
class TestInteractions(BaseTest):
    @pytest.mark.regression
    @allure.story("Selectable")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Select multiple items from list")
    def test_selectable_items_activate(self) -> None:
        selectable = SelectablePage(self.page).navigate(SelectablePage.URL)

        selectable.select_item(0)
        selectable.select_item(2)

        expect(selectable.active_items).to_have_count(2)
