from typing import List
from pages.search_page import SearchPage
from utils.enums import SearchRequests


class TestFilterBooks:

    def test_filter_books(self, browser, get_java_books, get_testing_book_info):
        """
            Precondition:
                1. Amazon Home page is opened
                2. Books filter is selected
                3. Search request with keyword 'Java' is sent
            Steps:
                1. Verify the search result contains the testing data
        :param browser: Selenium WebDriver
        :param get_java_books: filter_books_java
        :param get_testing_book_info: Tuple[str]
        :return: A tuple containing the Selenium WebDriver instance, a list of filtered Java books, and a tuple of strings.
        """
        book_name: str = SearchRequests.topic_for_book_search.value
        get_java_books(book_name, browser)
        self.filter: SearchPage = SearchPage(browser)
        books_info_list: List[list] = self.filter.get_information_about_books(self.filter)
        self.filter.verify_book_is_in_list(books_info_list, get_testing_book_info)
