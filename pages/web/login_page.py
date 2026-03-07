"""pages/web/login_page.py — Web Login Page Object."""
import allure
from playwright.sync_api import Page
from pages.web.web_common import WebCommon
from config.config_loader import CFG


class LoginPage(WebCommon):
    _USER_INPUT  = "input[name='loginId'], input[type='email'], #username"
    _PASS_INPUT  = "input[name='password'], input[type='password'], #password"
    _LOGIN_BTN   = "button[type='submit'], .login-btn, #loginBtn"
    _ERROR_MSG   = ".error-message, .alert-danger, [class*='error']"
    _FORGOT_LINK = "a[href*='forgot'], .forgot-password"

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Open login page")
    def open(self):
        self.goto(CFG.base_url)

    @allure.step("Login with role credentials")
    def login(self, username: str = None, password: str = None):
        self.fill(self._USER_INPUT,  username or CFG._raw["credentials"]["staging"]["username"])
        self.fill(self._PASS_INPUT,  password or CFG._raw["credentials"]["staging"]["password"])
        self.click(self._LOGIN_BTN)

    @allure.step("Login with user dict")
    def login_as(self, user: dict):
        self.fill(self._USER_INPUT, user["username"])
        self.fill(self._PASS_INPUT, user["password"])
        self.click(self._LOGIN_BTN)

    def get_error_message(self) -> str:
        return self.get_text(self._ERROR_MSG)

    def click_forgot_password(self):
        self.click(self._FORGOT_LINK)
