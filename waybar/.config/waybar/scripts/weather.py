#!/usr/bin/env python3

import json
import urllib.request
from datetime import datetime

WEATHER_CODES = {
    '113': '🌈', '116': '⛅️', '119': '☁️', '122': '☁️', '143': '🌫', '176': '🌦',
    '179': '🌧', '182': '🌧', '185': '🌧', '200': '⛈', '227': '🌨', '230': '❄️',
    '248': '🌫', '260': '🌫', '263': '🌦', '266': '🌦', '281': '🌧', '284': '🌧',
    '293': '🌦', '296': '🌦', '299': '🌧', '302': '🌧', '305': '🌧', '308': '🌧',
    '311': '🌧', '314': '🌧', '317': '🌧', '320': '🌨', '323': '🌨', '326': '🌨',
    '329': '❄️', '332': '❄️', '335': '❄️', '338': '❄️', '350': '🌧', '353': '🌦',
    '356': '🌧', '359': '🌧', '362': '🌧', '365': '🌧', '368': '🌨', '371': '❄️',
    '374': '🌧', '377': '🌧',    '386': '⛈', '389': '🌩', '392': '⛈', '395': '❄️'
}

def fetch_weather():
    url = "https://wttr.in/Aalborg?format=j1"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def format_time(t):
    return t.replace("00", "").zfill(2)

def format_temp(temp):
    return (temp + "°C").ljust(4)

def format_chances(hour):
    chances = {
        "chanceoffog": "Fog",
        "chanceoffrost": "Frost",
        "chanceofovercast": "Overcast",
        "chanceofrain": "Rain",
        "chanceofsnow": "Snow",
        "chanceofsunshine": "Sunshine",
        "chanceofthunder": "Thunder",
        "chanceofwindy": "Wind"
    }
    out = []
    for k, v in chances.items():
        if int(hour[k]) > 0:
            out.append(f"{v} {hour[k]}%")
    return ", ".join(out)

weather = fetch_weather()

data = {}

current = weather["current_condition"][0]

# -------------------------
#     TEXT (°C)
# -------------------------
data["text"] = (
    WEATHER_CODES[current["weatherCode"]] +
    " " + current["FeelsLikeC"] + "°C"
)

# -------------------------
#   TOOLTIP (°C)
# -------------------------
data["tooltip"] = (
    f"<b>{current['weatherDesc'][0]['value']} {current['temp_C']}°C</b>\n"
    f"Feels like: {current['FeelsLikeC']}°C\n"
    f"Wind: {current['windspeedKmph']} km/h\n"
    f"Humidity: {current['humidity']}%\n"
)

for i, day in enumerate(weather["weather"]):
    data["tooltip"] += "\n<b>"
    if i == 0:
        data["tooltip"] += "Today, "
    elif i == 1:
        data["tooltip"] += "Tomorrow, "
    data["tooltip"] += f"{day['date']}</b>\n"

    # Daily summary (°C)
    data["tooltip"] += (
        f"⬆️ {day['maxtempC']}° ⬇️ {day['mintempC']}° "
        f"🌅 {day['astronomy'][0]['sunrise']} 🌇 {day['astronomy'][0]['sunset']}\n"
    )

    for hour in day["hourly"]:
        if i == 0 and int(format_time(hour["time"])) < datetime.now().hour - 2:
            continue

        data["tooltip"] += (
            f"{format_time(hour['time'])} "
            f"{WEATHER_CODES[hour['weatherCode']]} "
            f"{format_temp(hour['FeelsLikeC'])} "
            f"{hour['weatherDesc'][0]['value']}, "
            f"{format_chances(hour)}\n"
        )

print(json.dumps(data))
