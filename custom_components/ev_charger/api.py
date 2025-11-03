"""API client for EV Charger."""
from __future__ import annotations

import logging
import requests
from typing import Any

from .const import LOGIN_URL, HARDWARE_LIST_URL, BLUETOOTH_INFO_URL, HEADERS

_LOGGER = logging.getLogger(__name__)


class EVChargerAPI:
    """API client for EV Charger."""
    
    def __init__(self, email: str, password: str) -> None:
        """Initialize the API client."""
        self._email = email
        self._password = password
        self._authorization = None
        self._session = requests.Session()
    
    def authenticate(self) -> bool:
        """Authenticate with the API."""
        try:
            login_data = {
                "email": self._email,
                "pass": self._password,
                "languageCode": "en"
            }
            
            response = self._session.post(LOGIN_URL, json=login_data)
            response.raise_for_status()
            
            data = response.json()
            if data.get("result") == 200:
                self._authorization = data["data"]["authorization"]
                _LOGGER.debug("Authentication successful")
                return True
            else:
                _LOGGER.error("Authentication failed: %s", data.get("message"))
                return False
                
        except Exception as err:
            _LOGGER.error("Error during authentication: %s", err)
            return False
    
    def get_all_data(self) -> dict[str, Any]:
        """Get all data from hardware and bluetooth endpoints."""
        if not self._authorization and not self.authenticate():
            raise Exception("Authentication failed")
        
        data = {}
        
        try:
            # Get hardware data
            hardware_headers = HEADERS.copy()
            hardware_headers["authorization"] = self._authorization
            
            hardware_response = self._session.post(
                HARDWARE_LIST_URL, 
                json={}, 
                headers=hardware_headers
            )
            hardware_response.raise_for_status()
            hardware_data = hardware_response.json()
            
            if hardware_data.get("result") == 200:
                data["hardware"] = hardware_data.get("data", [])
                
                # Get bluetooth data if we have devices
                if data["hardware"]:
                    first_device = data["hardware"][0]
                    biz_id = first_device.get("bizId")
                    sn = first_device.get("sn")
                    
                    if biz_id and sn:
                        bluetooth_data = {
                            "code": "",
                            "bizId": biz_id,
                            "sn": sn,
                            "online": True
                        }
                        
                        bluetooth_response = self._session.post(
                            BLUETOOTH_INFO_URL,
                            json=bluetooth_data,
                            headers=hardware_headers
                        )
                        bluetooth_response.raise_for_status()
                        bluetooth_result = bluetooth_response.json()
                        
                        if bluetooth_result.get("result") == 200:
                            data["bluetooth"] = bluetooth_result.get("data", {})
            
        except Exception as err:
            _LOGGER.error("Error fetching data: %s", err)
            # Reset authorization on error
            self._authorization = None
            raise
        
        return data