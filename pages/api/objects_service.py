"""pages/api/objects_service.py — Objects API service (extends APICommon)."""
import allure
from pages.api.api_common import APICommon
from config.config_loader import CFG


class ObjectsService(APICommon):
    """
    Client for the restful-api.dev /objects endpoints.
    Replace with your actual service endpoints.
    """
    _ENDPOINT = "/objects"

    def __init__(self, token: str = None):
        super().__init__(base_url=CFG.api_base_url, token=token)

    @allure.step("Get all objects")
    def get_all_objects(self):
        return self.get(self._ENDPOINT)

    @allure.step("Get object by id: {obj_id}")
    def get_object(self, obj_id: str):
        return self.get(f"{self._ENDPOINT}/{obj_id}")

    @allure.step("Create object")
    def create_object(self, name: str, data: dict):
        payload = {"name": name, "data": data}
        return self.post(self._ENDPOINT, body=payload)

    @allure.step("Update object: {obj_id}")
    def update_object(self, obj_id: str, name: str, data: dict):
        return self.put(f"{self._ENDPOINT}/{obj_id}", body={"name": name, "data": data})

    @allure.step("Partial update object: {obj_id}")
    def patch_object(self, obj_id: str, updates: dict):
        return self.patch(f"{self._ENDPOINT}/{obj_id}", body=updates)

    @allure.step("Delete object: {obj_id}")
    def delete_object(self, obj_id: str):
        return self.delete(f"{self._ENDPOINT}/{obj_id}")
