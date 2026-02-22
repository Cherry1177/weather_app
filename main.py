import requests

def fmt(v):
   try:
     return f"{float(v):.1f}"
   except (TypeError, ValueError):
     return "?"

def safe_get(url,params):
    try:
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        return r
    except requests.RequestException:
        print('Error retrieving data')
        exit()

city = input("Enter your city: ").strip() or "Kathmandu"
geo_url="https://geocoding-api.open-meteo.com/v1/search"
wx_url="https://api.open-meteo.com/v1/forecast"

params = {
    "name" : city,
    "count" : 1,
    "language" : "en",
    "format" : "json"
}

# r= requests.get(geo_url, params, timeout=5)
r = safe_get(geo_url, params)

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
    "timezone": "auto",
    "daily" : ["temperature_2m_max", "temperature_2m_min"],
    "forecast_days" : 3
}

w = safe_get(wx_url, params=wx_params)
wx = w.json()

cw = wx.get("current_weather" , {})
temp_now = cw.get("temperature")

daily = wx.get("daily", {})
dates = daily.get("time", []) or []
tmax = daily.get("temperature_2m_max", []) or []
tmin = daily.get("temperature_2m_min", []) or []

print("3-day Forecast:")
for d, lo, hi in zip(dates, tmin, tmax):
    print(f"{d}: {lo:.1f}°C → {hi:.1f}°C")

summary_line = temp_now
print(f"Current temp: {summary_line}")
