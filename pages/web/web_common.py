"""
pages/web/web_common.py
-----------------------
Base class for ALL web (Playwright) Page Objects.
Contains every generic interaction a UI test will ever need.
Import this and extend it in every page class.
"""
import os
import re
import time
import allure
import logging
from typing import Optional
from playwright.sync_api import Page, expect, Locator

log = logging.getLogger(__name__)


class WebCommon:
    """Generic Playwright helpers — navigation, clicks, forms, waits, asserts."""

    def __init__(self, page: Page):
        self.page = page

    # ================================================================
    # NAVIGATION
    # ================================================================
    @allure.step("Navigate to: {url}")
    def goto(self, url: str, wait_until: str = "domcontentloaded"):
        log.info(f"→ Navigate: {url}")
        self.page.goto(url, wait_until=wait_until)

    @allure.step("Reload page")
    def reload(self):
        self.page.reload(wait_until="domcontentloaded")

    @allure.step("Go back")
    def go_back(self):
        self.page.go_back()

    @allure.step("Go forward")
    def go_forward(self):
        self.page.go_forward()

    def current_url(self) -> str:
        return self.page.url

    def page_title(self) -> str:
        return self.page.title()

    # ================================================================
    # ELEMENT INTERACTIONS
    # ================================================================
    def _loc(self, selector: str) -> Locator:
        return self.page.locator(selector)

    @allure.step("Click: {selector}")
    def click(self, selector: str, timeout: int = 10000):
        log.info(f"Click: {selector}")
        self._loc(selector).wait_for(state="visible", timeout=timeout)
        self._loc(selector).click()

    @allure.step("Double-click: {selector}")
    def double_click(self, selector: str):
        self._loc(selector).wait_for(state="visible")
        self._loc(selector).dblclick()

    @allure.step("Right-click: {selector}")
    def right_click(self, selector: str):
        self._loc(selector).wait_for(state="visible")
        self._loc(selector).click(button="right")

    @allure.step("Fill: {selector}")
    def fill(self, selector: str, value: str, clear_first: bool = True):
        log.info(f"Fill '{selector}' = '{value}'")
        self._loc(selector).wait_for(state="visible")
        if clear_first:
            self._loc(selector).clear()
        self._loc(selector).fill(value)

    @allure.step("Type slowly: {selector}")
    def type_slow(self, selector: str, value: str, delay: int = 80):
        """Simulate human typing (useful for autocomplete inputs)."""
        self._loc(selector).wait_for(state="visible")
        self._loc(selector).type(value, delay=delay)

    @allure.step("Clear field: {selector}")
    def clear(self, selector: str):
        self._loc(selector).clear()

    @allure.step("Select dropdown option: {selector} → '{label}'")
    def select_option(self, selector: str, label: str = None, value: str = None, index: int = None):
        log.info(f"Select dropdown {selector}: label={label} value={value} index={index}")
        if label:
            self._loc(selector).select_option(label=label)
        elif value:
            self._loc(selector).select_option(value=value)
        elif index is not None:
            self._loc(selector).select_option(index=index)

    @allure.step("Check checkbox: {selector}")
    def check(self, selector: str):
        self._loc(selector).check()

    @allure.step("Uncheck checkbox: {selector}")
    def uncheck(self, selector: str):
        self._loc(selector).uncheck()

    @allure.step("Hover over: {selector}")
    def hover(self, selector: str):
        self._loc(selector).hover()

    @allure.step("Focus element: {selector}")
    def focus(self, selector: str):
        self._loc(selector).focus()

    @allure.step("Press key: {key}")
    def press_key(self, selector: str, key: str):
        """Example: press_key('#input', 'Enter')"""
        self._loc(selector).press(key)

    @allure.step("Upload file to: {selector}")
    def upload_file(self, selector: str, file_path: str):
        self._loc(selector).set_input_files(file_path)

    @allure.step("Drag '{source}' to '{target}'")
    def drag_and_drop(self, source: str, target: str):
        self._loc(source).drag_to(self._loc(target))

    @allure.step("Scroll into view: {selector}")
    def scroll_into_view(self, selector: str):
        self._loc(selector).scroll_into_view_if_needed()

    @allure.step("Scroll to bottom of page")
    def scroll_to_bottom(self):
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    @allure.step("Scroll to top of page")
    def scroll_to_top(self):
        self.page.evaluate("window.scrollTo(0, 0)")

    # ================================================================
    # READING VALUES
    # ================================================================
    def get_text(self, selector: str) -> str:
        self._loc(selector).wait_for(state="visible")
        return self._loc(selector).inner_text().strip()

    def get_value(self, selector: str) -> str:
        return self._loc(selector).input_value()

    def get_attribute(self, selector: str, attr: str) -> Optional[str]:
        return self._loc(selector).get_attribute(attr)

    def get_all_texts(self, selector: str) -> list[str]:
        return self._loc(selector).all_inner_texts()

    def count_elements(self, selector: str) -> int:
        return self._loc(selector).count()

    def is_visible(self, selector: str) -> bool:
        return self._loc(selector).is_visible()

    def is_enabled(self, selector: str) -> bool:
        return self._loc(selector).is_enabled()

    def is_checked(self, selector: str) -> bool:
        return self._loc(selector).is_checked()

    # ================================================================
    # WAITS
    # ================================================================
    @allure.step("Wait for element visible: {selector}")
    def wait_for_visible(self, selector: str, timeout: int = 10000):
        self._loc(selector).wait_for(state="visible", timeout=timeout)

    @allure.step("Wait for element hidden: {selector}")
    def wait_for_hidden(self, selector: str, timeout: int = 10000):
        self._loc(selector).wait_for(state="hidden", timeout=timeout)

    @allure.step("Wait for URL to contain: {partial}")
    def wait_for_url(self, partial: str, timeout: int = 10000):
        self.page.wait_for_url(f"**{partial}**", timeout=timeout)

    def wait_for_network_idle(self, timeout: int = 15000):
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def wait_seconds(self, seconds: float):
        time.sleep(seconds)

    # ================================================================
    # ALERTS / DIALOGS
    # ================================================================
    def accept_alert(self):
        self.page.once("dialog", lambda d: d.accept())

    def dismiss_alert(self):
        self.page.once("dialog", lambda d: d.dismiss())

    def get_alert_text(self) -> str:
        text = []
        self.page.once("dialog", lambda d: text.append(d.message) or d.accept())
        return text[0] if text else ""

    # ================================================================
    # FRAMES / IFRAMES
    # ================================================================
    def switch_to_frame(self, frame_selector: str):
        return self.page.frame_locator(frame_selector)

    # ================================================================
    # NEW TAB / WINDOW
    # ================================================================
    def click_and_get_new_page(self, selector: str):
        """Click a link that opens a new tab; return the new Page object."""
        with self.page.context.expect_page() as new_page_info:
            self.click(selector)
        new_page = new_page_info.value
        new_page.wait_for_load_state()
        return new_page

    # ================================================================
    # JAVASCRIPT
    # ================================================================
    def execute_js(self, script: str, *args):
        return self.page.evaluate(script, *args)

    def set_local_storage(self, key: str, value: str):
        self.page.evaluate(f"localStorage.setItem('{key}', '{value}')")

    def get_local_storage(self, key: str) -> str:
        return self.page.evaluate(f"localStorage.getItem('{key}')")

    # ================================================================
    # COOKIES
    # ================================================================
    def get_cookies(self) -> list[dict]:
        return self.page.context.cookies()

    def set_cookie(self, name: str, value: str, domain: str = None):
        cookie = {"name": name, "value": value}
        if domain:
            cookie["domain"] = domain
        self.page.context.add_cookies([cookie])

    def clear_cookies(self):
        self.page.context.clear_cookies()

    # ================================================================
    # ASSERTIONS (Playwright built-in — auto-retry)
    # ================================================================
    @allure.step("Assert visible: {selector}")
    def assert_visible(self, selector: str):
        expect(self._loc(selector)).to_be_visible()

    @allure.step("Assert not visible: {selector}")
    def assert_not_visible(self, selector: str):
        expect(self._loc(selector)).not_to_be_visible()

    @allure.step("Assert text equals: {selector}")
    def assert_text(self, selector: str, expected: str):
        expect(self._loc(selector)).to_have_text(expected)

    @allure.step("Assert text contains: {selector}")
    def assert_text_contains(self, selector: str, expected: str):
        expect(self._loc(selector)).to_contain_text(expected)

    @allure.step("Assert URL contains: {partial}")
    def assert_url_contains(self, partial: str):
        expect(self.page).to_have_url(re.compile(f".*{re.escape(partial)}.*"))

    @allure.step("Assert title contains: {expected}")
    def assert_title_contains(self, expected: str):
        expect(self.page).to_have_title(re.compile(f".*{re.escape(expected)}.*"))

    @allure.step("Assert element count: {selector}")
    def assert_count(self, selector: str, count: int):
        expect(self._loc(selector)).to_have_count(count)

    @allure.step("Assert element enabled: {selector}")
    def assert_enabled(self, selector: str):
        expect(self._loc(selector)).to_be_enabled()

    @allure.step("Assert element disabled: {selector}")
    def assert_disabled(self, selector: str):
        expect(self._loc(selector)).to_be_disabled()

    @allure.step("Assert checkbox checked: {selector}")
    def assert_checked(self, selector: str):
        expect(self._loc(selector)).to_be_checked()

    @allure.step("Assert input value: {selector}")
    def assert_value(self, selector: str, expected: str):
        expect(self._loc(selector)).to_have_value(expected)

    # ================================================================
    # SCREENSHOT (manual + allure auto-attach)
    # ================================================================
    def screenshot(self, name: str = "screenshot") -> bytes:
        data = self.page.screenshot(full_page=True)
        allure.attach(data, name=name, attachment_type=allure.attachment_type.PNG)
        log.info(f"Screenshot: {name}")
        return data

    # ================================================================
    # TABLE HELPERS
    # ================================================================
    def get_table_row_count(self, table_selector: str) -> int:
        return self._loc(f"{table_selector} tbody tr").count()

    def get_table_cell(self, table_selector: str, row: int, col: int) -> str:
        return self.get_text(f"{table_selector} tbody tr:nth-child({row}) td:nth-child({col})")

    def get_table_headers(self, table_selector: str) -> list[str]:
        return self.get_all_texts(f"{table_selector} thead th")

    # ================================================================
    # NETWORK INTERCEPT
    # ================================================================
    def intercept_route(self, url_pattern: str, handler):
        """Block or mock a network request.
        handler: lambda route: route.fulfill(status=200, body='...')
        """
        self.page.route(url_pattern, handler)

    def block_ads(self):
        self.page.route("**/*.{png,jpg,jpeg,gif,webp,css}", lambda r: r.abort())
