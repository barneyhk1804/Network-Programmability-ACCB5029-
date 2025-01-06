import requests
import sys
from datetime import datetime

def get_weather(api_key, city, units='metric'):
    """Fetch the current weather for a specified city."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': units
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        
        # Extract relevant data
        weather_info = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'pressure': data['main']['pressure'],
            'visibility': data['visibility'],
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S'),
            'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')
        }
        return weather_info
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return None

def main():
    api_key = "52e056792f8ed99c2fb9f686ed660d11"  # Replace with your actual API key
    if len(sys.argv) > 1:
        city = ' '.join(sys.argv[1:])
    else:
        city = input("Enter the city name: ")
    
    units_input = input("Choose units (m for metric, i for imperial): ").strip().lower()
    if units_input == 'm':
        units = 'metric'
    elif units_input == 'i':
        units = 'imperial'
    else:
        print("Invalid unit choice. Defaulting to metric.")
        units = 'metric'
    
    weather = get_weather(api_key, city, units)
    
    if weather:
        print(f"\nCurrent weather in {weather['city']}:")
        print(f"Temperature: {weather['temperature']}°{'C' if units == 'metric' else 'F'}")
        print(f"Description: {weather['description']}")
        print(f"Humidity: {weather['humidity']}%")
        print(f"Wind Speed: {weather['wind_speed']} m/s")
        print(f"Pressure: {weather['pressure']} hPa")
        print(f"Visibility: {weather['visibility']} meters")
        print(f"Sunrise: {weather['sunrise']}")
        print(f"Sunset: {weather['sunset']}")
    else:
        print("City not found or API request failed.")

if __name__ == "__main__":
    main()