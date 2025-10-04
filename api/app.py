from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

# OpenWeatherMap API configuration
API_KEY = os.getenv('OPENWEATHER_API_KEY', 'b2428934d76fef157adf02e3204af06c')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city):
    """Fetch weather data from OpenWeatherMap API"""
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'  # Get temperature in Celsius
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        print(f"Response status: {response.status_code if 'response' in locals() else 'No response'}")
        print(f"API Key being used: {API_KEY[:10]}..." if API_KEY != 'your_api_key_here' else 'Default API key')
        return None

def get_clothing_recommendations(weather_data):
    """Generate clothing recommendations based on weather conditions"""
    if not weather_data:
        return []
    
    temp = weather_data['main']['temp']
    description = weather_data['weather'][0]['description'].lower()
    wind_speed = weather_data.get('wind', {}).get('speed', 0)
    humidity = weather_data['main']['humidity']
    
    recommendations = []
    
    # Temperature-based recommendations
    if temp < 0:
        recommendations.extend([
            "Heavy winter coat or parka",
            "Thermal underwear",
            "Wool sweater or fleece",
            "Winter boots",
            "Warm hat and gloves",
            "Scarf"
        ])
    elif temp < 10:
        recommendations.extend([
            "Winter coat or heavy jacket",
            "Long-sleeved shirt",
            "Jeans or warm pants",
            "Closed-toe shoes or boots",
            "Light gloves",
            "Hat or beanie"
        ])
    elif temp < 20:
        recommendations.extend([
            "Light jacket or sweater",
            "Long-sleeved shirt",
            "Jeans or long pants",
            "Comfortable shoes",
            "Light scarf (optional)"
        ])
    elif temp < 30:
        recommendations.extend([
            "T-shirt or light shirt",
            "Shorts or light pants",
            "Sneakers or sandals",
            "Light cardigan (for evening)"
        ])
    else:
        recommendations.extend([
            "Light, breathable clothing",
            "Shorts and tank top",
            "Sandals or breathable shoes",
            "Sun hat",
            "Sunglasses"
        ])
    
    # Weather condition-based recommendations
    if 'rain' in description or 'drizzle' in description:
        recommendations.extend([
            "Waterproof jacket or raincoat",
            "Umbrella",
            "Waterproof shoes or boots"
        ])
    
    if 'snow' in description:
        recommendations.extend([
            "Snow boots",
            "Waterproof outer layer",
            "Warm gloves"
        ])
    
    if 'sun' in description or 'clear' in description:
        recommendations.extend([
            "Sunglasses",
            "Sun hat or cap",
            "Sunscreen"
        ])
    
    if wind_speed > 10:  # Strong wind
        recommendations.extend([
            "Windbreaker",
            "Secure hat"
        ])
    
    if humidity > 80:
        recommendations.append("Breathable, moisture-wicking clothing")
    
    return list(set(recommendations))  # Remove duplicates

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form.get('city')
    if not city:
        return jsonify({'error': 'Please enter a city name'}), 400
    
    weather_data = get_weather_data(city)
    
    if not weather_data:
        return jsonify({'error': 'Unable to fetch weather data. Please check the city name and try again.'}), 400
    
    clothing_recommendations = get_clothing_recommendations(weather_data)
    
    # Format the response
    result = {
        'city': weather_data['name'],
        'country': weather_data['sys']['country'],
        'temperature': round(weather_data['main']['temp']),
        'feels_like': round(weather_data['main']['feels_like']),
        'description': weather_data['weather'][0]['description'].title(),
        'humidity': weather_data['main']['humidity'],
        'wind_speed': weather_data.get('wind', {}).get('speed', 0),
        'pressure': weather_data['main']['pressure'],
        'clothing_recommendations': clothing_recommendations,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
