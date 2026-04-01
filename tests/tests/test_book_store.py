import allure
import pytest
from playwright.sync_api import expect

from tests.framework import BaseTest
from tests.framework.pages import BookStoreLoginPage, BookStorePage


@allure.epic("DemoQA")
@allure.feature("Book Store Application")
class TestBookStore(BaseTest):
    @pytest.mark.smoke
    @allure.story("Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Invalid login stays on login page")
    def test_invalid_login_stays_on_login_page(self) -> None:
        login = BookStoreLoginPage(self.page).navigate(BookStoreLoginPage.URL)

        login.login("invalid_user", "WrongP@ss1")

        expect(login.login_button).to_be_visible()
        expect(self.page).to_have_url("/login")

    @pytest.mark.smoke
    @allure.story("Book Store")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Book store displays books on load")
    def test_displays_books(self) -> None:
        book_store = BookStorePage(self.page).navigate(BookStorePage.URL)

        expect(book_store.search_input).to_be_visible()
        expect(book_store.book_titles.first).to_be_visible()
        expect(book_store.book_titles).not_to_have_count(0)

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "query",
        ["JavaScript", "Design"],
        ids=["search-javascript", "search-design"],
    )
    @allure.story("Book Store")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Search filters books by keyword")
    def test_search_filters_results(self, query: str) -> None:
        book_store = BookStorePage(self.page).navigate(BookStorePage.URL)

        book_store.search(query)

        expect(book_store.book_titles.first).to_be_visible()
        for title in book_store.book_titles.all():
            expect(title).to_contain_text(query)
