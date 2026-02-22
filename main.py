# Things to improve later
# Geocoding the city (name → coordinates)
# Fetching the weather (coordinates → data)
# Formatting the temperature (number → display)
import requests

def fmt(v):
   try:
     return f"{float(v):.1f}"
   except (TypeError, ValueError):
     return "?"

city = input("Enter your city: ").strip() or "Kathmandu"
geo_url="https://geocoding-api.open-meteo.com/v1/search"
wx_url="https://api.open-meteo.com/v1/forecast"

params = {
    "name" : city,
    "count" : 1,
    "language" : "en",
    "format" : "json"
}

r= requests.get(geo_url, params, timeout=5)

data = r.json()
# print("Raw geocoding JSON:", data)

if(not data.get("results")):
    print("City not found.")
    exit()

top = data["results"][0]

lat, lon = top["latitude"], top["longitude"]
print("Coords:", lat, lon)

wx_params = {
    "latitude": lat,
    "longitude": lon,
    "current_weather": True,
    "timezone": "auto"
}

w = requests.get(wx_url, params=wx_params, timeout=5)
wx = w.json()

cw = wx.get("current_weather" , {})
temp_now = cw.get("temperature")

summary_line = temp_now
print(summary_line)