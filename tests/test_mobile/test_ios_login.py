"""
tests/test_mobile/test_ios_login.py
-------------------------------------
Sample iOS mobile tests using Appium + XCUITest.
Requires:
  - macOS with Xcode
  - Appium server running
  - Real device or Simulator
  - IOS_UDID env var set for real device

Tests auto-skip if Appium is not available.
"""
import allure
import pytest
from pages.mobile.mobile_login_page import MobileLoginPage


@allure.epic("Mobile — iOS")
@allure.feature("Login")
class TestiOSLogin:

    @allure.story("Valid login on iOS")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.mobile
    @pytest.mark.ios
    @pytest.mark.smoke
    def test_ios_login_success(self, ios_driver, mobile_user, logger):
        """Verify successful login on iOS with valid credentials."""
        logger.info(f"iOS login — user: {mobile_user['username']}")
        login_page = MobileLoginPage(ios_driver)
        login_page.screenshot("iOS Login Page")
        login_page.login_as(mobile_user)
        login_page.wait_seconds(2)
        logger.info("PASS: iOS login completed")

    @allure.story("iOS login elements are accessible")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.mobile
    @pytest.mark.ios
    @pytest.mark.regression
    def test_ios_login_elements_present(self, ios_driver, logger):
        """Verify all login screen elements are accessible on iOS."""
        logger.info("Checking iOS login elements")
        login_page = MobileLoginPage(ios_driver)
        login_page.assert_visible("username_input")
        login_page.assert_visible("password_input")
        login_page.assert_visible("login_button")
        login_page.screenshot("iOS Login Elements")
        logger.info("PASS: iOS login elements accessible")

    @allure.story("iOS swipe gesture works")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.mobile
    @pytest.mark.ios
    def test_ios_swipe(self, ios_driver, logger):
        """Verify swipe gesture works on iOS."""
        logger.info("Testing iOS swipe")
        login_page = MobileLoginPage(ios_driver)
        login_page.swipe_left()
        login_page.wait_seconds(1)
        login_page.swipe_right()
        login_page.screenshot("After iOS Swipe")
        logger.info("PASS: iOS swipe works")

    @allure.story("iOS permission popup handled")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.mobile
    @pytest.mark.ios
    def test_ios_permission_popup(self, ios_driver, logger):
        """Verify permission popups are handled correctly on iOS."""
        logger.info("Testing iOS permission popup handling")
        login_page = MobileLoginPage(ios_driver)
        login_page.handle_permission_popup("allow")
        login_page.screenshot("After Permission Allow")
        logger.info("PASS: permission popup handled")
