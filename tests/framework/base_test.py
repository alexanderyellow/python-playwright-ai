import pytest
from playwright.sync_api import Page


class BaseTest:
    @pytest.fixture(autouse=True)
    def setup(self, page: Page) -> None:
        self.page = page
