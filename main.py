from tuya_iot import TuyaOpenAPI
from requests import get
import random

PUBLIC_IP = get('https://api.ipify.org').text

ACCESS_ID = ''
ACCESS_KEY = ''

# For more info: https://developer.tuya.com/en/docs/iot/api-request?id=Ka4a8uuo1j4t4
ENDPOINT = "https://openapi.tuyaus.com"

USERNAME = ''
PASSWORD = ''

FINGERBOT_DEVICE_ID = ''
LIGHTSTRIP_DEVICE_ID = ''

DARK_BLUE = {'h': 246, 's': 100, 'v': 100}
LIGHT_BLUE = {'h': 193, 's': 56, 'v': 100}
WHITE = {'h': 1, 's': 1, 'v': 100}
ORANGE = {'h': 23, 's': 90, 'v': 100}
YELLOW = {'h': 62, 's': 81, 'v': 100}
RED = {'h': 1, 's': 100, 'v': 100}

openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.login(USERNAME, PASSWORD)


def get_weather():
	location_url = f'/v1.0/iot-03/locations/ip?ip={PUBLIC_IP}'
	location = openapi.get(location_url)['result']
	lat, lon = location['latitude'], location['longitude']

	weather_url = f"/v2.0/iot-03/weather/current?lat={lat}&lon={lon}"
	weather = openapi.get(weather_url)['result']['current_weather']['temp']
	return weather


weather = float(get_weather())

color = None
if weather < -20:
	color = DARK_BLUE
elif weather < -10:
	color = LIGHT_BLUE
elif weather < 0:
	color = WHITE
elif weather < 10:
	color = ORANGE
elif weather < 20:
	color = RED
elif weather < 30:
	color = YELLOW

commands = {'commands': [{'code': 'colour_data', 'value': color}]}
result = openapi.post(f"/v1.0/iot-03/devices/{LIGHTSTRIP_DEVICE_ID}/commands", commands)
print(result)


# x = input('Press enter to brew')
# commands = {'commands': [{'code': 'switch', 'value': True}]}
# result = openapi.post(f"/v1.0/iot-03/devices/{FINGERBOT_DEVICE_ID}/commands", commands)
# print(result)