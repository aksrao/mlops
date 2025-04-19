from typing import Any
import os
import httpx
from mcp.server.fastmcp import FastMCP



mcp = FastMCP("weather")

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
            response.raise_for_status()
            data =  await response.json()
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
    rainfall = forecast[0]["HasPrecipitation"]
    temp = forecast["Temperature"]["Metric"]["Value"] 
    unit = forecast["Temperature"]["Metric"]["Unit"]
    return(
        f"The weather forecast of {location}"
        f"Time: {time}\n"
        f"Type of weather: {Weathertext}\n"
        f"Rainfall: {rainfall}\n"
        f"Temperature: {temp}{unit}"
    )

if __name__ == "__main__":
    mcp.run(transport='stdio')
