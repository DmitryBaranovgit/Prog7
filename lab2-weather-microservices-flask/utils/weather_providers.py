import requests

def openweather(city, api_key):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city, 
        "appid": api_key, 
        "units": "metric"
    }
    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()
    return response.json()

def mock_provider(city):
    return {
        "name": city,
        "main": {"temp": 20},
        "weather": [{"main": "Clear"}]
    }