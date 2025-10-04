# Weather & Clothing Advisor

A beautiful web application that provides weather information and clothing recommendations for any location worldwide.

## Features

- 🌤️ Real-time weather data for any city
- 👕 Personalized clothing recommendations based on weather conditions
- 📱 Responsive design that works on all devices
- 🎨 Modern, beautiful UI with gradient backgrounds
- ⚡ Fast and lightweight

## Screenshots

The application features a modern interface with:
- Clean, gradient-based design
- Real-time weather information display
- Smart clothing recommendations
- Mobile-responsive layout

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get a free API key from OpenWeatherMap:**
   - Visit [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up for a free account
   - Get your API key

4. **Set up your API key:**
   
   **Option 1: Environment Variable (Recommended)**
   ```bash
   # Windows
   set OPENWEATHER_API_KEY=your_api_key_here
   
   # Linux/Mac
   export OPENWEATHER_API_KEY=your_api_key_here
   ```
   
   **Option 2: Direct in code**
   - Open `app.py`
   - Replace `'your_api_key_here'` with your actual API key

## Usage

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Open your browser and go to:**
   ```
   http://localhost:5000
   ```

3. **Enter a city name** (e.g., "London", "New York", "Tokyo") and click "Get Weather"

4. **View the results:**
   - Current weather conditions
   - Temperature and feels-like temperature
   - Humidity, wind speed, and pressure
   - Personalized clothing recommendations

## How It Works

### Weather Data
- Uses the OpenWeatherMap API to fetch real-time weather data
- Displays temperature, humidity, wind speed, pressure, and weather description
- Shows both actual temperature and "feels like" temperature

### Clothing Recommendations
The app provides smart clothing suggestions based on:

**Temperature-based recommendations:**
- Below 0°C: Heavy winter gear
- 0-10°C: Winter coat and warm clothing
- 10-20°C: Light jacket and long sleeves
- 20-30°C: T-shirt and light clothing
- Above 30°C: Light, breathable summer wear

**Weather condition-based recommendations:**
- Rain: Waterproof clothing and umbrella
- Snow: Snow boots and warm gear
- Sunny: Sun protection items
- Windy: Wind-resistant clothing
- High humidity: Breathable, moisture-wicking fabrics

## API Key Setup

The application requires a free API key from OpenWeatherMap:

1. Go to [OpenWeatherMap API](https://openweathermap.org/api)
2. Sign up for a free account
3. Navigate to "API keys" in your account
4. Copy your API key
5. Set it as an environment variable or update the code directly

## File Structure

```
finalProject/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── templates/
    └── index.html        # Main HTML template
```

## Technologies Used

- **Backend:** Python Flask
- **Frontend:** HTML5, CSS3, JavaScript
- **API:** OpenWeatherMap
- **Styling:** Custom CSS with gradients and animations
- **Icons:** Font Awesome

## Customization

You can easily customize the application:

- **Styling:** Modify the CSS in `templates/index.html`
- **Clothing recommendations:** Update the `get_clothing_recommendations()` function in `app.py`
- **Weather data:** Add more weather parameters in the API response
- **UI:** Change colors, fonts, and layout in the HTML template

## Troubleshooting

**Common Issues:**

1. **"Unable to fetch weather data"**
   - Check your API key is correct
   - Ensure you have internet connection
   - Verify the city name is spelled correctly

2. **"Please enter a city name"**
   - Make sure to enter a valid city name
   - Try different city names or formats

3. **Application won't start**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (3.6+ required)

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests
- Improving documentation

## Support

If you encounter any issues or have questions, please check the troubleshooting section above or create an issue in the project repository.
