# api/app.py
import os
import traceback
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import requests

# Make sure Flask finds templates in repo-root /templates
app = Flask(__name__, template_folder="../templates")

# Logging setup: stdout so Vercel captures it
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weather-app")

# IMPORTANT: set this env var in Vercel settings: OPENWEATHER_API_KEY
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city):
    """Fetch weather data from OpenWeatherMap API, return dict or raise."""
    if not API_KEY:
        raise RuntimeError("OPENWEATHER_API_KEY not set in environment")

    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        resp = requests.get(BASE_URL, params=params, timeout=8)
        # Raise for network errors / 4xx/5xx
        resp.raise_for_status()
        data = resp.json()
        # Basic validation
        if "main" not in data or "weather" not in data:
            raise ValueError(f"Unexpected API response shape: {data}")
        return data
    except requests.exceptions.RequestException as e:
        logger.exception("HTTP error while calling OpenWeather API")
        raise
    except ValueError:
        logger.exception("Bad data from OpenWeather API")
        raise

def get_clothing_recommendations(weather_data):
    """Same as before but tolerant to missing keys."""
    if not weather_data:
        return []

    main = weather_data.get("main", {})
    weather_arr = weather_data.get("weather", [{}])
    description = weather_arr[0].get("description", "").lower()
    temp = main.get("temp", None)
    wind_speed = weather_data.get("wind", {}).get("speed", 0)
    humidity = main.get("humidity", 0)

    recommendations = []
    try:
        if temp is None:
            # If temp missing, don't crash — give a generic suggestion
            recommendations.append("Unable to determine temperature — bring a light layer")
        else:
            if temp < 0:
                recommendations.extend(["Heavy winter coat or parka", "Thermal underwear"])
            elif temp < 10:
                recommendations.extend(["Winter coat or heavy jacket", "Long-sleeved shirt"])
            elif temp < 20:
                recommendations.extend(["Light jacket or sweater", "Long-sleeved shirt"])
            elif temp < 30:
                recommendations.extend(["T-shirt or light shirt", "Shorts or light pants"])
            else:
                recommendations.extend(["Light, breathable clothing", "Shorts and tank top"])

        if "rain" in description or "drizzle" in description:
            recommendations.extend(["Waterproof jacket or raincoat", "Umbrella"])
        if "snow" in description:
            recommendations.extend(["Snow boots", "Warm gloves"])
        if "clear" in description or "sun" in description:
            recommendations.extend(["Sunglasses", "Sunscreen"])
        if wind_speed > 10:
            recommendations.extend(["Windbreaker", "Secure hat"])
        if humidity > 80:
            recommendations.append("Breathable, moisture-wicking clothing")
    except Exception:
        logger.exception("Error computing clothing recommendations")

    return list(dict.fromkeys(recommendations))  # preserve order, unique

@app.route("/")
def index():
    try:
        return render_template("index.html")
    except Exception:
        logger.exception("Failed to render template")
        # Return a fallback message with 500 (so logs show why)
        return "<h1>Template render error — check logs</h1>", 500

@app.route("/weather", methods=["POST"])
def get_weather():
    try:
        city = request.form.get("city") or request.json.get("city")
        if not city:
            return jsonify({"error": "Please enter a city name"}), 400

        weather_data = get_weather_data(city)
        clothing = get_clothing_recommendations(weather_data)

        result = {
            "city": weather_data.get("name", city),
            "country": weather_data.get("sys", {}).get("country", ""),
            "temperature": round(weather_data.get("main", {}).get("temp", 0)),
            "feels_like": round(weather_data.get("main", {}).get("feels_like", 0)),
            "description": weather_data.get("weather", [{}])[0].get("description", "").title(),
            "humidity": weather_data.get("main", {}).get("humidity", 0),
            "wind_speed": weather_data.get("wind", {}).get("speed", 0),
            "pressure": weather_data.get("main", {}).get("pressure", 0),
            "clothing_recommendations": clothing,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }
        return jsonify(result)
    except Exception as e:
        # Log full traceback to Vercel logs
        logger.error("Unhandled exception in /weather endpoint:\n%s", traceback.format_exc())
        # Return a helpful error message (but avoid exposing secrets)
        return jsonify({"error": "Internal server error — check logs for details"}), 500

# Small debug endpoint: can be removed after debugging
@app.route("/__health")
def health():
    info = {
        "ok": True,
        "OPENWEATHER_API_KEY_set": bool(API_KEY),
        "python_env": dict(os.environ) if os.getenv("VERCEL_ENV") == "development" else None
    }
    return jsonify(info)
