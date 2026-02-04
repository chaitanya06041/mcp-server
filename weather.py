import os
from mcp.server.fastmcp import FastMCP
import requests
import random
from datetime import date

# Move host and port here
# Render provides the PORT env var; 8000 is a safe local default
mcp = FastMCP(
    "Weather-Service",
    host="0.0.0.0", 
    port=int(os.environ.get("PORT", 8000))
)

def get_weather_by_location(city_name: str):
    # Step 1: Get coordinates from Open-Meteo Geocoding API
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
    geo_res = requests.get(geo_url)
    geo_data = geo_res.json()

    if not geo_data.get("results"):
        raise ValueError("Location not found.")

    latitude = geo_data["results"][0]["latitude"]
    longitude = geo_data["results"][0]["longitude"]
    location_name = geo_data["results"][0]["name"]

    # Step 2: Fetch hourly data for today
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&hourly=temperature_2m,relative_humidity_2m,precipitation,uv_index"
        f"&timezone=auto"
    )
    weather_res = requests.get(weather_url)
    weather_data = weather_res.json()

    hourly = weather_data.get("hourly", {})
    times = hourly.get("time", [])

    # Step 3: Filter only today’s data
    today_str = date.today().isoformat()
    today_indices = [i for i, t in enumerate(times) if t.startswith(today_str)]

    if not today_indices:
        raise ValueError("No weather data available for today.")

    # Extract today’s values
    temps = [hourly["temperature_2m"][i] for i in today_indices]
    hums = [hourly["relative_humidity_2m"][i] for i in today_indices]
    rains = [hourly["precipitation"][i] for i in today_indices]
    uvs = [hourly["uv_index"][i] for i in today_indices if hourly["uv_index"][i] is not None]

    # Step 4: Calculate averages and totals
    avg_temp = sum(temps) / len(temps)
    avg_humidity = sum(hums) / len(hums)
    total_rain = sum(rains)
    avg_uv = sum(uvs) / len(uvs) if uvs else 0

    # Step 5: Return formatted data
    return {
        "location": location_name,
        "temperature": round(avg_temp, 2),
        "humidity": round(avg_humidity, 2),
        "rainfall": round(total_rain, 2),
        "index": round(avg_uv, 2),
        "latitude": latitude,
        "longitude": longitude,
    }

@mcp.tool()
def get_weather(city: str) -> dict:
    """Get the current weather for a given city."""
    return get_weather_by_location(city)

if __name__ == "__main__":
    # Clean up the run command
    mcp.run(transport="streamable-http")
    # print(get_weather_by_location("Pune"))