"""
test_fno_api.py
---------------
Example API tests using Allure decorators and the logger fixture.
"""
import allure
import pytest
import requests

from config.config_loader import CFG


@allure.epic("API Tests")
@allure.feature("FNO API")
class TestFnoApi:

    @allure.story("GET endpoint availability")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_fno_api_001(self, logger):
        """Verify the API root endpoint returns HTTP 200."""
        logger.info("Testing FNO API root endpoint")
        url = f"{CFG.api_base_url}/"

        with allure.step(f"GET {url}"):
            res = requests.get(url, timeout=10)

        logger.info(f"Response status: {res.status_code}")
        allure.attach(
            res.text,
            name="API Response",
            attachment_type=allure.attachment_type.TEXT,
        )

        assert res.status_code == 200, (
            f"Expected 200 but got {res.status_code}"
        )
        logger.info("test_fno_api_001 PASSED")

    @allure.story("GET objects list")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_fno_api_002(self, logger):
        """Verify /objects endpoint returns a non-empty list."""
        logger.info("Testing /objects endpoint")
        url = f"{CFG.api_base_url}/objects"

        with allure.step(f"GET {url}"):
            res = requests.get(url, timeout=10)

        logger.info(f"Response status: {res.status_code}")
        allure.attach(
            res.text[:500],
            name="API Response (truncated)",
            attachment_type=allure.attachment_type.TEXT,
        )

        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list) and len(data) > 0, "Expected non-empty list"
        logger.info(f"test_fno_api_002 PASSED - {len(data)} objects returned")
