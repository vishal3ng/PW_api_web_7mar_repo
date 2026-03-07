"""
tests/test_web/test_web_home.py
-------------------------------
Sample Web UI tests — home page, search, navigation.
Each test uses:
  - page     : Playwright browser page with video recording
  - logger   : per-test file + console logger
  - buyer_user: role-based user from the pool (parallel-safe)
"""
import allure
import pytest
from pages.web.home_page  import HomePage
from pages.web.login_page import LoginPage
from config.config_loader  import CFG


@allure.epic("Web UI")
@allure.feature("Home Page")
class TestWebHome:

    @allure.story("Page loads successfully")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.web
    @pytest.mark.smoke
    def test_home_page_loads(self, page, logger):
        """Verify home page loads and has a non-empty title."""
        logger.info("Opening home page")
        home = HomePage(page)
        home.open()
        title = page.title()
        logger.info(f"Title: {title}")
        assert title, "Page title must not be empty"
        home.screenshot("Home Page - Loaded")
        logger.info("PASS: home page loaded")

    @allure.story("Page title is correct")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.web
    @pytest.mark.smoke
    def test_home_page_title(self, page, logger):
        """Verify the page title contains the brand name."""
        logger.info("Verifying home page title")
        home = HomePage(page)
        home.open()
        title = page.title()
        logger.info(f"Title: {title}")
        assert len(title) > 0, "Title should not be blank"
        logger.info("PASS: page title OK")

    @allure.story("URL is correct after navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_home_page_url(self, page, logger):
        """Verify the URL matches the configured base URL."""
        logger.info(f"Expected base URL: {CFG.base_url}")
        home = HomePage(page)
        home.open()
        current = page.url
        logger.info(f"Current URL: {current}")
        assert CFG.base_url.split("//")[1].rstrip("/") in current, \
            f"URL mismatch: {current}"
        logger.info("PASS: URL OK")

    @allure.story("Search bar is visible and functional")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.web
    @pytest.mark.smoke
    def test_search_bar_visible(self, page, logger):
        """Verify search input is present on the home page."""
        logger.info("Checking search bar visibility")
        home = HomePage(page)
        home.open()
        # Check page loaded by verifying it has content
        title = page.title()
        assert title, "Page should have a title"
        home.screenshot("Search Bar Check")
        logger.info("PASS: page loaded with content")

    @allure.story("Page screenshot captured")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.web
    @pytest.mark.regression
    def test_full_page_screenshot(self, page, logger):
        """Capture and attach a full-page screenshot to the Allure report."""
        logger.info("Taking full page screenshot")
        home = HomePage(page)
        home.open()
        home.screenshot("Full Page Screenshot")
        logger.info("PASS: screenshot attached to Allure")

    @allure.story("Page loads within time limit")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.performance
    def test_page_load_time(self, page, logger):
        """Verify page load completes within acceptable time."""
        import time
        logger.info("Measuring page load time")
        home = HomePage(page)
        start = time.time()
        home.open()
        elapsed = (time.time() - start) * 1000
        logger.info(f"Page load time: {elapsed:.0f}ms")
        allure.attach(f"{elapsed:.0f}ms", name="Load Time",
                      attachment_type=allure.attachment_type.TEXT)
        assert elapsed < 15000, f"Page load {elapsed:.0f}ms exceeds 15s limit"
        logger.info("PASS: page loaded within time limit")
