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

def weather_icon(code):
    icons = {
        0: "☀️",   # Clear sky
        1: "🌤️", 2: "⛅", 3: "☁️",   # Cloudy
        45: "🌫️", 48: "🌫️",        # Fog
        51: "🌦️", 53: "🌦️", 55: "🌦️",  # Drizzle
        61: "🌧️", 63: "🌧️", 65: "🌧️",  # Rain
        71: "🌨️", 73: "🌨️", 75: "❄️",  # Snow
        80: "🌦️", 81: "🌧️", 82: "🌧️",  # Showers
        95: "⛈️", 96: "⛈️", 99: "⛈️"   # Thunderstorm
    }
    return icons.get(code, "🌡️")

city = input("Enter your city: ").strip() or "Kathmandu"
unit = input("Choose unit (C/F): ").strip().upper() or "C"
geo_url="https://geocoding-api.open-meteo.com/v1/search"
wx_url="https://api.open-meteo.com/v1/forecast"

params = {
    "name" : city,
    "count" : 1,
    "language" : "en",
    "format" : "json"
}

r = safe_get(geo_url, params)

data = r.json()

if(not data.get("results")):
    print("City not found.")
    exit()

top = data["results"][0]

lat, lon = top["latitude"], top["longitude"]
print("Coords:", lat, lon)

temp_unit = "fahrenheit" if unit == "F" else "celsius"
unit_symbol = "°F" if unit == "F" else "°C"

wx_params = {
    "latitude": lat,
    "longitude": lon,
    "current_weather": True,
    "timezone": "auto",
    "daily" : ["weathercode","temperature_2m_max", "temperature_2m_min"],
    "temperature_unit": temp_unit,
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
codes = daily.get("weathercode", []) or []

print("3-day Forecast:")
print()
for d, lo, hi, c in zip(dates[:3], tmin[:3], tmax[:3], codes[:3]):
    icon = weather_icon(c)
    print(f"{icon} {d}: {fmt(lo)}{unit_symbol} → {fmt(hi)}{unit_symbol}")

cw = wx.get("current_weather", {})
temp_now = cw.get("temperature")
code_now = cw.get("weathercode")

print(f"\nNow: {weather_icon(code_now)} {fmt(temp_now)}{unit_symbol}")
