import time
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class BasePage:
    base_url: str = 'https://www.amazon.com/'
    items_book_name_tag: tuple = (By.TAG_NAME, 'h2')
    items_author_string_tag: tuple = (By.TAG_NAME, 'div')

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_element(self, by_locator: tuple, is_many=False) -> WebElement or List[WebElement]:
        """
        Finds and returns a single web element or a list of web elements based on the provided locator.

        Args:
            by_locator (tuple): A tuple containing the locator strategy and value.
            is_many (bool, optional): Indicates whether to find multiple elements. Defaults to False.

        Returns:
            WebElement or List[WebElement]: The found web element(s).
        """
        find_action = self.driver.find_elements if is_many else self.driver.find_element
        el: WebElement or List[WebElement] = find_action(*by_locator)
        return el

    def get_base_url(self) -> None:
        self.driver.get(self.base_url)

    def click_on_element(self, by_locator: tuple) -> None:
        """
        Clicks on the web element located using the provided locator.

        Args:
            by_locator (tuple): A tuple containing the locator strategy and value.
        """
        el: WebElement = self.get_element(by_locator)
        el.click()

    def input_text(self, text: str, by_locator: tuple) -> None:
        """
        Enters text into the input field located using the provided locator.

        Args:
            text (str): The text to be entered into the input field.
            by_locator (tuple): A tuple containing the locator strategy and value.
        """
        el: WebElement = self.get_element(by_locator)
        el.send_keys(text)

    def go_to_url(self, url: str) -> None:
        """
        Navigates the browser to the specified URL.

        Args:
            url (str): The URL to navigate to.
        """
        self.driver.get(url)

    @staticmethod
    def waiter(seconds: int) -> None:
        """
        Pauses the execution for the specified number of seconds.

        Args:
            seconds (int): The duration of the pause in seconds.
        """
        time.sleep(seconds)
