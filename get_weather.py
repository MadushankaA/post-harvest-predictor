import requests

# Replace with your real API key from OpenWeatherMap
API_KEY = '30f8939c9a5662436197f0b531d59549'  # Example: 'b1a2c3d4e5f6g7h8i9'
city = 'Colombo'

# Build the API request URL
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

# Send request and parse JSON
res = requests.get(url).json()

# Extract temperature and humidity
temp = res['main']['temp']
humidity = res['main']['humidity']

# Display the results
print(f"✅ Current Temperature in {city}: {temp}°C")
print(f"✅ Current Humidity in {city}: {humidity}%")