import allure
import pytest
from playwright.sync_api import expect

from tests.framework import BaseTest
from tests.framework.pages import AlertsPage, ModalDialogsPage


@allure.epic("DemoQA")
@allure.feature("Alerts, Frames & Windows")
class TestAlertsFramesWindows(BaseTest):
    @pytest.mark.smoke
    @allure.story("Alerts")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Accept a simple JavaScript alert")
    def test_simple_alert(self) -> None:
        alerts = AlertsPage(self.page).navigate(AlertsPage.URL)

        self.page.on("dialog", lambda dialog: dialog.accept())
        alerts.click_alert()

    @pytest.mark.regression
    @allure.story("Alerts")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Accept a confirm dialog and verify result")
    def test_confirm_dialog_accept(self) -> None:
        alerts = AlertsPage(self.page).navigate(AlertsPage.URL)

        self.page.on("dialog", lambda dialog: dialog.accept())
        alerts.click_confirm()

        expect(alerts.confirm_result).to_have_text("You selected Ok")

    @pytest.mark.regression
    @allure.story("Alerts")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Accept a prompt dialog with input text")
    def test_prompt_dialog_accept(self) -> None:
        alerts = AlertsPage(self.page).navigate(AlertsPage.URL)

        self.page.on("dialog", lambda dialog: dialog.accept(prompt_text="Test input"))
        alerts.click_prompt()

        expect(alerts.prompt_result).to_contain_text("Test input")

    @pytest.mark.smoke
    @allure.story("Modal Dialogs")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Open small modal and verify title")
    def test_small_modal_title(self) -> None:
        modals = ModalDialogsPage(self.page).navigate(ModalDialogsPage.URL)

        modals.open_small_modal()

        expect(modals.modal_title).to_have_text("Small Modal")
        expect(modals.modal_body).to_be_visible()

    @pytest.mark.regression
    @allure.story("Modal Dialogs")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Open and close small modal")
    def test_small_modal_close(self) -> None:
        modals = ModalDialogsPage(self.page).navigate(ModalDialogsPage.URL)

        modals.open_small_modal()
        expect(modals.modal_title).to_be_visible()

        modals.close_small_modal()
        expect(modals.modal_title).not_to_be_visible()

    @pytest.mark.regression
    @allure.story("Modal Dialogs")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Open large modal and verify title")
    def test_large_modal_title(self) -> None:
        modals = ModalDialogsPage(self.page).navigate(ModalDialogsPage.URL)

        modals.open_large_modal()

        expect(modals.modal_title).to_have_text("Large Modal")
        expect(modals.modal_body).to_be_visible()
