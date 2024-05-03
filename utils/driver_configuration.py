from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class Driver:
    def __init__(self, browser_name: str = 'chrome', remote_url=None):
        self.remote_url: str = remote_url
        self.browser_name: str = browser_name
        self.browsers: list = ['chrome', 'firefox', 'edge', 'safari']
        self.choose_browser()

    def choose_browser(self):
        """Assign the driver object based on the provided self.browser_name"""
        options = None

        if self.remote_url:
            if self.browser_name == 'chrome':
                options = webdriver.ChromeOptions()
            elif self.browser_name == 'firefox':
                options = webdriver.FirefoxOptions()
            elif self.browser_name == 'edge':
                options = webdriver.EdgeOptions()
            elif self.browser_name == 'safari':
                options = webdriver.SafariOptions()

        if options:
            self.driver = webdriver.Remote(command_executor=self.remote_url, options=options)
        else:
            if self.browser_name == 'chrome':
                self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            elif self.browser_name == 'firefox':
                self.driver = webdriver.Firefox()
            elif self.browser_name == 'edge':
                self.driver = webdriver.Edge()
            elif self.browser_name == 'safari':
                self.driver = webdriver.Safari()

        if self.driver:
            self.driver.maximize_window()
            self.driver.implicitly_wait(3)
