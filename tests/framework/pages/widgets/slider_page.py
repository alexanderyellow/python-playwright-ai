from typing import Self

import allure
from playwright.sync_api import Page

from tests.framework.pages.base_page import BasePage


class SliderPage(BasePage):
    URL = "/slider"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.value_display = page.locator("#sliderValue")
        self.slider = page.locator("input.range-slider")

    @allure.step("Set slider value to {value}")
    def set_value(self, value: int) -> Self:
        """Set the slider to a specific integer value via JavaScript.

        Uses direct DOM manipulation because React-controlled range inputs
        do not respond to Playwright's fill() or keyboard-based approaches.
        """
        self.page.evaluate(
            """(value) => {
                const el = document.querySelector('input.range-slider');
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value'
                ).set;
                nativeInputValueSetter.call(el, value);
                el.dispatchEvent(new Event('input', {bubbles: true}));
                el.dispatchEvent(new Event('change', {bubbles: true}));
            }""",
            value,
        )
        return self
