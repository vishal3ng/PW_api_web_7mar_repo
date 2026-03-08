"""
test_home_ui.py
---------------
Example UI tests using the page fixture (with video recording).
"""
import allure
import pytest

from config.config_loader import CFG
from pages.home_page.home_page import HomePage
from pages.login.login_page import LoginPage


@allure.epic("UI Tests")
@allure.feature("Home Page")
class TestHomeUI:

    @allure.story("Page loads successfully")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.ui
    def test_home_page_loads(self, page, logger):
        """Verify the home page loads without errors."""
        logger.info(f"Opening home page: {CFG.base_url}")
        home = HomePage(page)
        lg = LoginPage(page)

        with allure.step("Navigate to home page"):
            home.open()

        with allure.step("Click on download"):
            lg.print_login()
            pass



        with allure.step("Verify page title"):
            title = page.title()
            logger.info(f"Page title: {title}")
            assert title, "Page title should not be empty"

        with allure.step("Verify Home page Ui element "):
            title = page.title()
            logger.info(f"Page title: {title}")
            assert title, "Page title should not be empty"

        logger.info("test_home_page_loads PASSED")

    @allure.story("Page screenshot")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.ui
    def test_home_page_screenshot(self, page, logger):
        """Capture a screenshot of the home page and attach to report."""
        logger.info("Capturing home page screenshot")
        home = HomePage(page)
        home.open()
        home.take_screenshot("Home Page")
        logger.info("test_home_page_screenshot PASSED")
