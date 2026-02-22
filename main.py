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
print("Raw geocoding JSON:", data)

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

w = safe_get(wx_url, params=wx_params)
wx = w.json()

cw = wx.get("current_weather" , {})
temp_now = cw.get("temperature")

summary_line = temp_now
print(summary_line)