from mcp.server.fastmcp import FastMCP
import requests
import random
import os

mcp = FastMCP("Weather-Service")

def generate_random_weather(city: str) -> str:
    """Generate random weather data for a given city."""
    conditions = ["Sunny", "Cloudy", "Rainy", "Windy", "Stormy", "Snowy"]
    temperature = random.randint(0, 40)  # Temperature in Celsius
    condition = random.choice(conditions)
    return f"The current weather in {city} is {condition} with a temperature of {temperature}°C."

@mcp.tool()
def get_weather(city: str) -> str:
    """
    Get the current weather for a given city.
    Args:
        city (str): Name of the city to get the weather for.
    """
    return generate_random_weather(city)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port)