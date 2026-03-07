"""pages/mobile/mobile_login_page.py — Mobile Login Page Object (Android & iOS)."""
import allure
from pages.mobile.mobile_common import MobileCommon


class MobileLoginPage(MobileCommon):
    # Accessibility IDs (use same IDs across iOS/Android where possible)
    _USERNAME_FIELD = "username_input"
    _PASSWORD_FIELD = "password_input"
    _LOGIN_BTN      = "login_button"
    _ERROR_LABEL    = "error_message"
    _FORGOT_BTN     = "forgot_password_btn"

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Mobile: Login with credentials")
    def login(self, username: str, password: str):
        self.type_text(self._USERNAME_FIELD, username)
        self.type_text(self._PASSWORD_FIELD, password)
        self.hide_keyboard()
        self.tap_by_accessibility_id(self._LOGIN_BTN)

    @allure.step("Mobile: Login as user from pool")
    def login_as(self, user: dict):
        self.login(user["username"], user["password"])

    def get_error_message(self) -> str:
        return self.get_text(self._ERROR_LABEL)

    def tap_forgot_password(self):
        self.tap_by_accessibility_id(self._FORGOT_BTN)
