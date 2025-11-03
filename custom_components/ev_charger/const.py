"""Constants for EV Charger integration."""

DOMAIN = "ev_charger"
NAME = "EV Charger"

CONF_EMAIL = "email"
CONF_PASSWORD = "password"

DEFAULT_SCAN_INTERVAL = 60  # seconds

# API endpoints
LOGIN_URL = "https://www.aefa-ev.com/api/charge/login/pass"
HARDWARE_LIST_URL = "https://www.aefa-ev.com/api/charge/hardware/list"
BLUETOOTH_INFO_URL = "https://www.aefa-ev.com/api/charge/bluetooth/accept/now_information"

# Headers
HEADERS = {
    "Host": "www.aefa-ev.com",
    "appid": "__UNI__F86E78D",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0 (Immersed/20) uni-app",
    "appversion": "2.0.63",
    "priority": "u=3, i",
    "deviceid": "DF533914337DA509B06F296065DE5567",
    "appname": "EV-Chargergo",
    "devicemodel": "iPhone 15 Pro Max",
    "accept-language": "ru",
    "appwgtversion": "2.0.63",
    "timezone": "Europe/Minsk",
    "osversion": "26.0.1",
    "osname": "ios",
    "accept": "*/*",
    "content-type": "application/json",
    "devicebrand": "apple",
    "applanguage": "en"
}