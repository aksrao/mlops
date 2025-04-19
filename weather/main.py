from typing import Any
import os
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv



mcp = FastMCP("weather")

load_dotenv()
base_url = "http://dataservice.accuweather.com"
api_key=os.getenv("ACCUWEATHER_API_KEY")

async def get_location_key(location: str) -> str | None:
    """get location key"""
    location_url = f"{base_url}/locations/v1/cities/search"
    params = {
                "apikey": api_key,
                "q": location,
            }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(location_url, params=params, timeout=30.0)
            data =  response.json()
            print(data[0]["Key"])
            return data[0]["Key"]
        except Exception:
            return None
        

async def get_forecast(location_key: str) -> dict[str, Any] | None:
    """get the forecast"""
    location_url = f"{base_url}/currentconditions/v1/{location_key}"
    params = {
        "apikey": api_key
    }
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(location_url, params=params, timeout=30.0)
            res.raise_for_status()
            return res.json()
        except Exception:
            return None


@mcp.tool()
async def get_weather(location: str)-> str:
    """handling the forecast"""
    location_key = await get_location_key(location)
    if not location_key:
        return "please provide correct location"
    forecast = await get_forecast(location_key)
    time = forecast[0]["LocalObservationDateTime"]
    Weathertext = forecast[0]["WeatherText"]

    if forecast[0]["HasPrecipitation"] == "false":
        rainfall = "There's no rainfall at the moment"
    rainfall = "There's rainfall at the moment."

    temp_c = forecast[0]["Temperature"]["Metric"]["Value"] 
    temp_f = forecast[0]["Temperature"]["Imperial"]["Value"]
    return(
        f"Currently in {location}, it's {Weathertext} with a temperature of {temp_c}°C (about {temp_f}°F). {rainfall} This information is current as of {time}."
        f"The weather forecast of {location}"
        f"Time: {time}\n"
        f"Type of weather: {Weathertext}\n"
        f"Rainfall: {rainfall}\n"
        f"Temperature: {temp_c}\u00b0C"
    )

if __name__ == "__main__":
    mcp.run(transport='stdio')
