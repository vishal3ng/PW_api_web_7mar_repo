"""
login_page.py
-------------
Page Object for the Login page.
"""
import time

import allure
from playwright.sync_api import Page
from pages.common_method import Common
from config.config_loader import CFG


class LoginPage(Common):
    # Locators
    _USERNAME = "input[name='loginId']"
    _PASSWORD = "input[name='password']"
    _LOGIN_BTN = "button[type='submit']"
    _ERROR_MSG = ".error-message"


    # xpath

    download_xpath = "//span[text()='Downloads']"

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Login with credentials from config")
    def login(self, username: str = None, password: str = None):
        """Login using config credentials by default."""
        user = username or CFG.username
        pwd = password or CFG.password
        self.fill(self._USERNAME, user)
        self.fill(self._PASSWORD, pwd)
        self.click(self._LOGIN_BTN)

    @allure.step("Get login error message")
    def get_error_message(self) -> str:
        return self.get_text(self._ERROR_MSG)

    @allure.step("print step from login check")
    def print_login(self):
        self.click(self.download_xpath)
        time.sleep(5)

