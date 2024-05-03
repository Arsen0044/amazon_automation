import pytest
from typing import Tuple
from selenium.webdriver.chrome.webdriver import WebDriver
from pages.search_page import SearchPage


def filter_books_java(book_name: str, driver_obj: WebDriver) -> None:
    filter_obj: SearchPage = SearchPage(driver_obj)
    filter_obj.get_base_url()
    filter_obj.set_the_book_filter()
    filter_obj.input_and_search_by_text(book_name)


@pytest.fixture(scope="function")
def get_java_books() -> filter_books_java:
    return filter_books_java


@pytest.fixture
def get_testing_book_info() -> Tuple[str, str, str, str]:
    verification_book: Tuple[str, str, str, str] = (
        'Head First Java: A Brain-Friendly Guide',
        ' by Kathy Sierra, Bert Bates, et al. ',
        '17.60', '41.79'
    )
    return verification_book
