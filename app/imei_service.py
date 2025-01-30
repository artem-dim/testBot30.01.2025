import requests
from pydantic import BaseModel
import os

class IMEIInfo(BaseModel):
    status: str
    data: dict

class IMEIService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://imeicheck.net/api/v1/check"

    def check_imei(self, imei: str) -> IMEIInfo:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(self.base_url, json={"imei": imei}, headers=headers)
        response.raise_for_status()
        return IMEIInfo(**response.json())