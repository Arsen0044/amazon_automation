import pytest
from selenium.webdriver.chrome.webdriver import WebDriver
from utils.driver_configuration import Driver


@pytest.fixture(scope="function")
def browser() -> WebDriver:
    driver_instance: Driver = Driver()
    driver: WebDriver = driver_instance.driver
    yield driver
    driver.quit()
