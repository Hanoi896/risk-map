# modules/weather_fetcher.py
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app_config import OPENWEATHER_API_KEY


def get_weather_by_coords(lat, lon):
    """
    위도, 경도를 입력받아 현재 날씨 데이터를 반환합니다.

    Args:
        lat (float): 위도
        lon (float): 경도

    Returns:
        dict: 날씨 정보 or 오류 메시지
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "kr"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        # 필요한 정보만 추출
        result = {
            "location": data.get("name", ""),
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }

        return result

    except requests.RequestException as e:
        return {"error": f"Request failed: {e}"}
    except KeyError as e:
        return {"error": f"Invalid response format: {e}"}
