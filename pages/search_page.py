import re
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import List, Tuple
from pages.base_page import BasePage


class SearchPage(BasePage):
    email_field_id: tuple = (By.ID, 'ap_email')
    password_field_id: tuple = (By.ID, 'ap_password')
    login_continue_button_id: tuple = (By.ID, 'continue')
    sign_in_button_id: tuple = (By.ID, '')
    filter_button_id: tuple = (By.ID, 'nav-search-dropdown-card')
    books_option_in_filter: tuple = (By.CSS_SELECTOR, '[value="search-alias=stripbooks-intl-ship"]')
    search_field_id: tuple = (By.ID, 'twotabsearchtextbox')
    search_submit_button_id: tuple = (By.ID, 'nav-search-submit-button')
    items_on_search_result: tuple = (By.CSS_SELECTOR, '[data-component-type="s-search-result"]')
    items_title: tuple = (By.CSS_SELECTOR, '[data-cy="title-recipe"]')
    items_price_whole_class: tuple = (By.CLASS_NAME, 'a-price-whole')
    items_price_fraction_class: tuple = (By.CLASS_NAME, 'a-price-fraction')
    items_best_seller_badge: tuple = (By.CSS_SELECTOR, '[data-component-type="s-status-badge-component"]')

    def __init__(self, driver: WebDriver = None):
        super().__init__(driver)
        self.driver = driver

    @staticmethod
    def verify_book_is_in_list(list_info: List[list], verification_book: Tuple[str, str, str, str]) -> None:
        """
        Verify if the specified book information is present in the list.

        :param list_info: The list of book information to search.
        :param verification_book: The book information to verify.
        :return: None
        """
        for sublist in list_info:
            if all(item in sublist for item in verification_book):
                assert True, 'Book is in the list'
                break
        else:
            assert False, 'Book is not in the list'

    def get_information_about_books(self, filter_obj) -> List[list]:
        """
        Retrieves information about books from the search results.

        :param filter_obj: An instance of the filtering class.
        :return: A list of lists containing information about each book.
                 Each inner list contains the name, author, price, and best seller status.
        """
        # Initialize an empty list to store book information
        books_information: list = []

        # Get all items from the search result
        items_on_search_result: List[WebElement] = self.get_element(self.items_on_search_result, is_many=True)

        # Iterate through each item in the search result
        for item in items_on_search_result:
            # Get the name and author of the book
            information_list: list = self.get_name_and_author(item)

            # Get the full price and best seller status of the book using the filter object
            full_price: list = filter_obj.get_price_and_best_seller(item)

            # Check if the full price is a list
            if isinstance(full_price, list):
                # If it's a list, extend the information list with the price and best seller status
                information_list.extend(full_price)
            else:
                # If it's not a list, append the price to the information list
                information_list.append(full_price)

            # Add the information list to the books_information list
            books_information.append(information_list)

        # Return the list of books information
        return books_information

    def get_name_and_author(self, item: WebElement) -> List[str]:
        """
        Extracts the name and author of a book from the item element.

        :param item: The element containing information about the book.
        :return: A list containing the name and author of the book.
        """
        # Find the title element within the item
        title: WebElement = item.find_element(*self.items_title)

        # Find the element containing the book name within the title
        name: WebElement = title.find_element(*self.items_book_name_tag)

        # Find the element containing the author string within the title
        author_string: WebElement = title.find_element(*self.items_author_string_tag)

        # Extract the text of the author string and clean it
        author: str = self.clear_string(author_string.text)

        # Create a list with the book name and author
        information_list: list = [name.text, author]

        # Return the list containing the book name and author
        return information_list

    def get_price_and_best_seller(self, item: WebElement) -> List[str]:
        """
        Extracts the price and best seller information from the given item.

        :param item: The WebElement representing the item.
        :return: A list containing the price and best seller information.
        """
        self.driver.implicitly_wait(1)
        result: list = []
        try:
            # Extract whole and fractional parts of the price
            price: List[WebElement] = item.find_elements(*self.items_price_whole_class)
            fraction: List[WebElement] = item.find_elements(*self.items_price_fraction_class)

            # Combine whole and fractional parts to form the price
            for i in range(len(price)):
                result.append(f'{price[i].text}.{fraction[i].text}')

            # Extract best seller badge
            best_seller: WebElement = item.find_element(*self.items_best_seller_badge)
            result.append(best_seller.text)

            # Reset implicit wait to default
            self.driver.implicitly_wait(10)
            return result
        except Exception:
            # Reset implicit wait to default in case of any exception
            self.driver.implicitly_wait(10)
            return result

    def input_and_search_by_text(self, text) -> None:
        """
        Inputs the given text into the search field and submits the search.

        :param text: The text to input into the search field.
        :return: None
        """
        self.input_text(text, self.search_field_id)
        self.click_on_element(self.search_submit_button_id)

    def set_the_book_filter(self) -> None:
        """
        Sets the book filter option.

        :return: None
        """
        self.click_on_element(self.filter_button_id)
        self.click_on_element(self.books_option_in_filter)

    @staticmethod
    def clear_string(string_: str) -> str:
        """
        Removes the content between the first and last '|' characters in the given string, if present.

        Args:
            string_: The input string to be processed.

        Returns:
            str: The modified string with the content between the first and last '|' characters removed, if present.
        """
        # Find all occurrences of the '|' character in the string
        matches = re.findall(r'\|', string_)

        # If no '|' characters are found, return the original string
        if len(matches) == 0:
            return string_
        # If only one '|' character is found, remove the content after it and return the modified string
        elif len(matches) == 1:
            index: int = string_.find('|')
            return string_[:index]
        # If more than one '|' character is found, remove the content between the first and last occurrences
        else:
            start: int = string_.find('|') + 1
            end: int = string_.rfind('|')
            return string_[start:end]
