"""pages/web/home_page.py — Web Home Page Object."""
import allure
from playwright.sync_api import Page
from pages.web.web_common import WebCommon
from config.config_loader import CFG


class HomePage(WebCommon):
    _SEARCH_INPUT = "input[class*='search'], input[placeholder*='Search']"
    _SEARCH_BTN   = "button[class*='search'], .search-bar__action"
    _BANNER       = ".banner, [class*='hero'], [class*='banner']"
    _NAV_ITEMS    = "nav a, .desktop-nav a"
    _CART_ICON    = "[class*='cart'], [aria-label*='cart']"
    _USER_ICON    = "[class*='user'], [aria-label*='profile']"

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Open home page")
    def open(self):
        self.goto(CFG.base_url)

    @allure.step("Search for: {query}")
    def search(self, query: str):
        self.fill(self._SEARCH_INPUT, query)
        self.click(self._SEARCH_BTN)

    def get_nav_items(self) -> list[str]:
        return self.get_all_texts(self._NAV_ITEMS)

    def go_to_cart(self):
        self.click(self._CART_ICON)

    def go_to_profile(self):
        self.click(self._USER_ICON)
