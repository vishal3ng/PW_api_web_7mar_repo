"""
common_method.py
----------------
Base class for all Page Object classes.
Provides reusable, stable interaction wrappers around Playwright.
"""
import allure
import logging
from playwright.sync_api import Page, expect

log = logging.getLogger(__name__)


class Common:
    def __init__(self, page: Page):
        self.page = page

    # ------------------------------------------------------------------ #
    #  Navigation
    # ------------------------------------------------------------------ #
    @allure.step("Navigate to {url}")
    def navigate(self, url: str):
        log.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="domcontentloaded")

    # ------------------------------------------------------------------ #
    #  Element interactions
    # ------------------------------------------------------------------ #
    @allure.step("Click element: {selector}")
    def click(self, selector: str):
        log.info(f"Click: {selector}")
        self.page.locator(selector).wait_for(state="visible")
        self.page.locator(selector).click()

    @allure.step("Fill '{selector}' with value")
    def fill(self, selector: str, value: str):
        log.info(f"Fill: {selector}")
        self.page.locator(selector).wait_for(state="visible")
        self.page.locator(selector).fill(value)

    @allure.step("Get text of '{selector}'")
    def get_text(self, selector: str) -> str:
        self.page.locator(selector).wait_for(state="visible")
        text = self.page.locator(selector).inner_text()
        log.info(f"Text of {selector}: {text!r}")
        return text

    # ------------------------------------------------------------------ #
    #  Assertions
    # ------------------------------------------------------------------ #
    @allure.step("Assert element visible: {selector}")
    def assert_visible(self, selector: str):
        log.info(f"Asserting visible: {selector}")
        expect(self.page.locator(selector)).to_be_visible()

    @allure.step("Assert page title contains '{expected}'")
    def assert_title_contains(self, expected: str):
        log.info(f"Asserting title contains: {expected!r}")
        expect(self.page).to_have_title(expected)

    # ------------------------------------------------------------------ #
    #  Screenshot utility (manual call)
    # ------------------------------------------------------------------ #
    def take_screenshot(self, name: str = "screenshot") -> bytes:
        data = self.page.screenshot()
        allure.attach(data, name=name, attachment_type=allure.attachment_type.PNG)
        log.info(f"Screenshot taken: {name}")
        return data
