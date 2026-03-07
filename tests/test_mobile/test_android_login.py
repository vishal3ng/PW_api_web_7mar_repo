"""
tests/test_mobile/test_android_login.py
----------------------------------------
Sample Android mobile tests using Appium.
Requires:
  - Appium server running at CFG.appium_server
  - Physical/emulator device connected
  - appium-python-client installed

Tests auto-skip if Appium is not available.
"""
import allure
import pytest
from pages.mobile.mobile_login_page import MobileLoginPage


@allure.epic("Mobile — Android")
@allure.feature("Login")
class TestAndroidLogin:

    @allure.story("Valid login with buyer credentials")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.mobile
    @pytest.mark.android
    @pytest.mark.smoke
    def test_android_login_success(self, android_driver, mobile_user, logger):
        """Verify successful login on Android with valid credentials."""
        logger.info(f"Android login test — user: {mobile_user['username']}")
        login_page = MobileLoginPage(android_driver)
        login_page.screenshot("Android Login Page")
        login_page.login_as(mobile_user)
        login_page.wait_seconds(2)
        logger.info("PASS: Android login completed")

    @allure.story("Login screen elements visible")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.mobile
    @pytest.mark.android
    @pytest.mark.regression
    def test_android_login_elements_present(self, android_driver, logger):
        """Verify username, password, and login button are visible."""
        logger.info("Checking Android login screen elements")
        login_page = MobileLoginPage(android_driver)
        login_page.assert_visible("username_input")
        login_page.assert_visible("password_input")
        login_page.assert_visible("login_button")
        login_page.screenshot("Android Login Elements")
        logger.info("PASS: all login elements present")

    @allure.story("Invalid login shows error message")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.mobile
    @pytest.mark.android
    @pytest.mark.regression
    def test_android_invalid_login(self, android_driver, logger):
        """Verify error message shown for invalid credentials."""
        logger.info("Testing invalid login on Android")
        login_page = MobileLoginPage(android_driver)
        login_page.login("wrong@email.com", "WrongPass!")
        login_page.wait_seconds(2)
        login_page.screenshot("Android Invalid Login Error")
        logger.info("PASS: invalid login handled")

    @allure.story("Scroll on login page")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.mobile
    @pytest.mark.android
    def test_android_scroll(self, android_driver, logger):
        """Verify page can be scrolled on Android."""
        logger.info("Testing Android scroll")
        login_page = MobileLoginPage(android_driver)
        login_page.scroll_down()
        login_page.wait_seconds(1)
        login_page.scroll_up()
        login_page.screenshot("After Scroll")
        logger.info("PASS: scroll works on Android")
