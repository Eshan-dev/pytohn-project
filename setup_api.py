#!/usr/bin/env python3
"""
Setup script to help configure the OpenWeatherMap API key
"""

import requests
import os

def test_api_key(api_key):
    """Test if the API key is valid"""
    try:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': 'London',
            'appid': api_key,
            'units': 'metric'
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            print("SUCCESS: API key is valid!")
            data = response.json()
            print(f"Test successful: {data['name']}, {data['main']['temp']}C")
            return True
        elif response.status_code == 401:
            print("ERROR: API key is invalid or expired")
            return False
        else:
            print(f"ERROR: API error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"ERROR: Error testing API: {e}")
        return False

def main():
    print("OpenWeatherMap API Setup")
    print("=" * 40)
    
    # Check if API key is already set
    current_key = os.getenv('OPENWEATHER_API_KEY', 'your_api_key_here')
    
    if current_key != 'your_api_key_here':
        print(f"Current API key: {current_key[:10]}...")
        if test_api_key(current_key):
            print("SUCCESS: Your API key is working!")
            return
        else:
            print("ERROR: Your current API key is not working.")
    
    print("\nTo get a free API key:")
    print("1. Go to: https://openweathermap.org/api")
    print("2. Click 'Sign Up' and create a free account")
    print("3. Go to 'API keys' in your account")
    print("4. Copy your API key")
    print("5. Set it as an environment variable:")
    print("   Windows: set OPENWEATHER_API_KEY=your_actual_key")
    print("   Linux/Mac: export OPENWEATHER_API_KEY=your_actual_key")
    
    # Ask user to enter API key for testing
    print("\nEnter your API key to test (or press Enter to skip):")
    api_key = input().strip()
    
    if api_key:
        if test_api_key(api_key):
            print("\nSUCCESS: Great! Your API key works!")
            print("Now set it as an environment variable:")
            print(f"Windows: set OPENWEATHER_API_KEY={api_key}")
            print(f"Linux/Mac: export OPENWEATHER_API_KEY={api_key}")
        else:
            print("\nERROR: The API key you entered is not working.")
            print("Please check the key and try again.")

if __name__ == "__main__":
    main()
