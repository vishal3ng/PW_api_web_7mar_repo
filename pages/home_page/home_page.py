"""
home_page.py
------------
Page Object for the Home page.
"""
import allure
from playwright.sync_api import Page
from pages.common_method import Common
from config.config_loader import CFG


class HomePage(Common):
    # Locators
    _SEARCH_BAR = "input[class*='search']"
    _SEARCH_BTN = "button[class*='search']"
    _USER_ICON  = ".user-profile-icon"

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Open home page")
    def open(self):
        self.navigate(CFG.base_url)

    @allure.step("Search for '{query}'")
    def search(self, query: str):
        self.fill(self._SEARCH_BAR, query)
        self.click(self._SEARCH_BTN)
