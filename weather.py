import os
from mcp.server.fastmcp import FastMCP
import requests
import random

# Move host and port here
# Render provides the PORT env var; 8000 is a safe local default
mcp = FastMCP(
    "Weather-Service",
    host="0.0.0.0", 
    port=int(os.environ.get("PORT", 8000))
)

def generate_random_weather(city: str) -> str:
    # ... (rest of your weather logic)
    conditions = ["Sunny", "Cloudy", "Rainy", "Windy", "Stormy", "Snowy"]
    temperature = random.randint(0, 40)
    condition = random.choice(conditions)
    return f"The current weather in {city} is {condition} with a temperature of {temperature}°C."

@mcp.tool()
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    return generate_random_weather(city)

if __name__ == "__main__":
    # Clean up the run command
    mcp.run(transport="streamable-http")