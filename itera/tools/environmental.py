import requests

def get_place_infos(lat: float, lon: float) -> dict:
    """Retrieve weather and air quality for a location."""
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "hourly": "temperature_2m,precipitation,windspeed_10m",
        "timezone": "auto",
    }
    weather_data = requests.get(weather_url, params=weather_params).json()

    air_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    air_params = {
        "latitude": lat,
        "longitude": lon,
        "current": "european_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide"
    }
    try:
        air_data = requests.get(air_url, params=air_params).json()
    except Exception:
        air_data = None

    return {
        "current_weather": weather_data.get("current_weather"),
        "hourly": weather_data.get("hourly"),
        "air_quality": air_data.get("current") if isinstance(air_data, dict) else None,
    }
