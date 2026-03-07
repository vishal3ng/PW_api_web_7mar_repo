"""
pages/mobile/mobile_common.py
------------------------------
Base class for ALL mobile (Appium) Page Objects — iOS & Android.
Contains every generic interaction for native/hybrid mobile apps.
"""
import time
import allure
import logging
from typing import Optional

log = logging.getLogger(__name__)

# Appium is optional — framework still works without it for web/API only runs
try:
    from appium.webdriver.common.appiumby import AppiumBy
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import (
        NoSuchElementException, TimeoutException, StaleElementReferenceException
    )
    _APPIUM_AVAILABLE = True
except ImportError:
    _APPIUM_AVAILABLE = False
    log.warning("[MobileCommon] appium-python-client not installed. Mobile tests will be skipped.")


class MobileCommon:
    """Generic Appium helpers for iOS and Android native/hybrid apps."""

    def __init__(self, driver):
        self.driver  = driver
        self.wait    = WebDriverWait(driver, 30) if _APPIUM_AVAILABLE else None
        self.platform = driver.capabilities.get("platformName", "").lower() if driver else ""

    # ================================================================
    # ELEMENT FINDERS
    # ================================================================
    def _find(self, by, value, timeout: int = 10):
        """Find element with explicit wait."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def find_by_id(self, resource_id: str, timeout: int = 10):
        return self._find(AppiumBy.ID, resource_id, timeout)

    def find_by_xpath(self, xpath: str, timeout: int = 10):
        return self._find(AppiumBy.XPATH, xpath, timeout)

    def find_by_accessibility_id(self, acc_id: str, timeout: int = 10):
        return self._find(AppiumBy.ACCESSIBILITY_ID, acc_id, timeout)

    def find_by_class(self, class_name: str, timeout: int = 10):
        return self._find(AppiumBy.CLASS_NAME, class_name, timeout)

    def find_by_text(self, text: str, timeout: int = 10):
        """Find element containing exact text (cross-platform)."""
        if self.platform == "android":
            return self.find_by_xpath(f'//*[@text="{text}"]', timeout)
        else:  # iOS
            return self.find_by_xpath(f'//*[@label="{text}" or @value="{text}"]', timeout)

    def find_all_by_xpath(self, xpath: str) -> list:
        return self.driver.find_elements(AppiumBy.XPATH, xpath)

    # ================================================================
    # TAP / CLICK
    # ================================================================
    @allure.step("Tap element by accessibility_id: {acc_id}")
    def tap_by_accessibility_id(self, acc_id: str):
        log.info(f"Tap: {acc_id}")
        el = self.find_by_accessibility_id(acc_id)
        el.click()

    @allure.step("Tap element by id: {resource_id}")
    def tap_by_id(self, resource_id: str):
        log.info(f"Tap id: {resource_id}")
        self.find_by_id(resource_id).click()

    @allure.step("Tap element by xpath: {xpath}")
    def tap_by_xpath(self, xpath: str):
        self.find_by_xpath(xpath).click()

    @allure.step("Tap at coordinates ({x}, {y})")
    def tap_at(self, x: int, y: int):
        self.driver.tap([(x, y)])

    @allure.step("Long press: {acc_id}")
    def long_press(self, acc_id: str, duration_ms: int = 1000):
        el = self.find_by_accessibility_id(acc_id)
        self.driver.execute_script("mobile: longClickGesture", {
            "elementId": el.id, "duration": duration_ms
        })

    # ================================================================
    # TEXT INPUT
    # ================================================================
    @allure.step("Type into field: {acc_id}")
    def type_text(self, acc_id: str, text: str):
        log.info(f"Type '{text}' into {acc_id}")
        el = self.find_by_accessibility_id(acc_id)
        el.clear()
        el.send_keys(text)

    @allure.step("Type into field by id: {resource_id}")
    def type_text_by_id(self, resource_id: str, text: str):
        el = self.find_by_id(resource_id)
        el.clear()
        el.send_keys(text)

    @allure.step("Clear field: {acc_id}")
    def clear_field(self, acc_id: str):
        self.find_by_accessibility_id(acc_id).clear()

    def hide_keyboard(self):
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass

    # ================================================================
    # READING VALUES
    # ================================================================
    def get_text(self, acc_id: str) -> str:
        return self.find_by_accessibility_id(acc_id).text.strip()

    def get_text_by_id(self, resource_id: str) -> str:
        return self.find_by_id(resource_id).text.strip()

    def get_text_by_xpath(self, xpath: str) -> str:
        return self.find_by_xpath(xpath).text.strip()

    def get_attribute(self, acc_id: str, attr: str) -> Optional[str]:
        return self.find_by_accessibility_id(acc_id).get_attribute(attr)

    def is_element_visible(self, acc_id: str, timeout: int = 5) -> bool:
        try:
            el = self.find_by_accessibility_id(acc_id, timeout=timeout)
            return el.is_displayed()
        except Exception:
            return False

    def is_element_enabled(self, acc_id: str) -> bool:
        try:
            return self.find_by_accessibility_id(acc_id).is_enabled()
        except Exception:
            return False

    # ================================================================
    # SCROLLING / SWIPING
    # ================================================================
    @allure.step("Scroll down")
    def scroll_down(self, duration: int = 800):
        size   = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.7)
        end_y   = int(size["height"] * 0.3)
        self.driver.swipe(start_x, start_y, start_x, end_y, duration)

    @allure.step("Scroll up")
    def scroll_up(self, duration: int = 800):
        size    = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.3)
        end_y   = int(size["height"] * 0.7)
        self.driver.swipe(start_x, start_y, start_x, end_y, duration)

    @allure.step("Swipe left")
    def swipe_left(self, duration: int = 600):
        size    = self.driver.get_window_size()
        start_x = int(size["width"] * 0.8)
        end_x   = int(size["width"] * 0.2)
        y       = size["height"] // 2
        self.driver.swipe(start_x, y, end_x, y, duration)

    @allure.step("Swipe right")
    def swipe_right(self, duration: int = 600):
        size    = self.driver.get_window_size()
        start_x = int(size["width"] * 0.2)
        end_x   = int(size["width"] * 0.8)
        y       = size["height"] // 2
        self.driver.swipe(start_x, y, end_x, y, duration)

    @allure.step("Scroll until text visible: {text}")
    def scroll_to_text(self, text: str, max_swipes: int = 5):
        for _ in range(max_swipes):
            if self.is_element_visible(text, timeout=2):
                return True
            self.scroll_down()
        log.warning(f"[Mobile] Text '{text}' not found after {max_swipes} swipes")
        return False

    # ================================================================
    # NAVIGATION
    # ================================================================
    @allure.step("Press Android BACK button")
    def back(self):
        self.driver.back()

    @allure.step("Press Android HOME button")
    def home(self):
        self.driver.press_keycode(3)   # Android keycode for HOME

    @allure.step("Open notifications")
    def open_notifications(self):
        self.driver.open_notifications()

    @allure.step("Launch app")
    def launch_app(self):
        self.driver.launch_app()

    @allure.step("Close app")
    def close_app(self):
        self.driver.close_app()

    @allure.step("Reset app")
    def reset_app(self):
        self.driver.reset()

    # ================================================================
    # ALERTS
    # ================================================================
    def accept_alert(self):
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self):
        self.driver.switch_to.alert.dismiss()

    def get_alert_text(self) -> str:
        return self.driver.switch_to.alert.text

    def handle_permission_popup(self, action: str = "allow"):
        """Handle iOS/Android permission popups (allow/deny)."""
        buttons = {
            "allow":     ["Allow", "Allow While Using App", "OK", "Continue"],
            "deny":      ["Don't Allow", "Deny", "No Thanks"],
        }
        for label in buttons.get(action, []):
            try:
                el = self.find_by_accessibility_id(label, timeout=3)
                el.click()
                log.info(f"[Mobile] Permission popup handled: {label}")
                return
            except Exception:
                continue

    # ================================================================
    # WAITS
    # ================================================================
    def wait_for_element(self, acc_id: str, timeout: int = 15):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, acc_id))
        )

    def wait_seconds(self, seconds: float):
        time.sleep(seconds)

    # ================================================================
    # SCREENSHOT
    # ================================================================
    @allure.step("Take mobile screenshot: {name}")
    def screenshot(self, name: str = "mobile_screenshot") -> bytes:
        data = self.driver.get_screenshot_as_png()
        allure.attach(data, name=name, attachment_type=allure.attachment_type.PNG)
        log.info(f"Mobile screenshot: {name}")
        return data

    # ================================================================
    # ASSERTIONS
    # ================================================================
    @allure.step("Assert element visible: {acc_id}")
    def assert_visible(self, acc_id: str, timeout: int = 10):
        assert self.is_element_visible(acc_id, timeout), \
            f"Element '{acc_id}' not visible on screen."

    @allure.step("Assert text equals: {acc_id}")
    def assert_text(self, acc_id: str, expected: str):
        actual = self.get_text(acc_id)
        assert actual == expected, f"Expected '{expected}', got '{actual}'"

    @allure.step("Assert text contains: {acc_id}")
    def assert_text_contains(self, acc_id: str, expected: str):
        actual = self.get_text(acc_id)
        assert expected in actual, f"Expected '{expected}' in '{actual}'"

    @allure.step("Assert element not visible: {acc_id}")
    def assert_not_visible(self, acc_id: str):
        assert not self.is_element_visible(acc_id, timeout=3), \
            f"Element '{acc_id}' should NOT be visible."

    # ================================================================
    # DEVICE INFO
    # ================================================================
    def get_platform(self) -> str:
        return self.platform

    def get_device_size(self) -> dict:
        return self.driver.get_window_size()

    def is_android(self) -> bool:
        return self.platform == "android"

    def is_ios(self) -> bool:
        return self.platform == "ios"
